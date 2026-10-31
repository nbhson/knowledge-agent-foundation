import { createHash } from "node:crypto";
import { createInterface } from "node:readline";
import { createReadStream } from "node:fs";
import { ulid } from "ulid";

export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}

export async function loadSession(path: string): Promise<TrajectoryEvent[]> {
  const out: TrajectoryEvent[] = [];
  const rl = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of rl) if (line.trim()) out.push(JSON.parse(line));
  return assertGapless(out);
}

/** seq liền mạch chứng minh không mất lần ghi nào. Có lỗ hổng nghĩa là log
 *  không đầy đủ — mọi kết luận suy ra (cost, replay) khi đó đáng ngờ. */
function assertGapless(evts: TrajectoryEvent[]): TrajectoryEvent[] {
  evts.sort((a, b) => a.seq - b.seq);
  for (let i = 1; i < evts.length; i++)
    if (evts[i].seq !== evts[i - 1].seq + 1)
      throw new Error(`trajectory gap: seq ${evts[i - 1].seq} → ${evts[i].seq}`);
  return evts;
}

/** FORK — clone tiền tố, tạo danh tính mới, đi tiếp theo hướng khác. */
export function fork(src: Session, atSeq: number, by: string): Session {
  const prefix = src.events.filter(e => e.seq <= atSeq);
  const clone: Session = {
    sessionId: `ses_${ulid()}`,
    forkedFrom: { sessionId: src.sessionId, atSeq, by },
    events: prefix.map(e => ({ ...e })),      // id mới khi ghi, seq giữ nguyên
  };
  return clone;
}

export interface ReplayDiff { step: number; kind: string; drift: "none" | "output" | "error" | "latency" }

/** REPLAY — so một lần chạy mới với lần đã ghi. */
export function diffRun(recorded: TrajectoryEvent[], fresh: TrajectoryEvent[]): ReplayDiff[] {
  const diffs: ReplayDiff[] = [];
  const n = Math.max(recorded.length, fresh.length);
  for (let i = 0; i < n; i++) {
    const a = recorded[i], b = fresh[i];
    if (!a || !b) { diffs.push({ step: i, kind: a?.kind ?? b?.kind ?? "?", drift: "output" }); continue; }
    if (a.kind !== b.kind) { diffs.push({ step: i, kind: a.kind, drift: "output" }); continue; }
    if (hash(a.payload) !== hash(b.payload)) diffs.push({ step: i, kind: a.kind, drift: "output" });
    else if ((a.latencyMs ?? 0) > (b.latencyMs ?? 0) * 3 + 500) diffs.push({ step: i, kind: a.kind, drift: "latency" });
  }
  return diffs;
}
const hash = (o: unknown) => createHash("sha256").update(JSON.stringify(o)).digest("hex").slice(0, 16);

/** RESUME — idempotency key làm cho chạy lại sau crash an toàn. */
export function stepsToSkip(events: TrajectoryEvent[], done: Set<string>): string[] {
  return events.filter(e => e.kind === "tool_call" && done.has(idempotencyKeyOf(e)))
               .map(e => e.payload.callId as string);
}
export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;  // → 07 §13.3
}
