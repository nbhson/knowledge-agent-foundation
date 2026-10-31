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

/** Gapless seq proves no write was lost. A gap means the log is incomplete —
 *  every downstream conclusion (cost, replay) is then suspect. */
function assertGapless(evts: TrajectoryEvent[]): TrajectoryEvent[] {
  evts.sort((a, b) => a.seq - b.seq);
  for (let i = 1; i < evts.length; i++)
    if (evts[i].seq !== evts[i - 1].seq + 1)
      throw new Error(`trajectory gap: seq ${evts[i - 1].seq} → ${evts[i].seq}`);
  return evts;
}

/** FORK — clone the prefix, mint a new identity, continue divergently. */
export function fork(src: Session, atSeq: number, by: string): Session {
  const prefix = src.events.filter(e => e.seq <= atSeq);
  const clone: Session = {
    sessionId: `ses_${ulid()}`,
    forkedFrom: { sessionId: src.sessionId, atSeq, by },
    events: prefix.map(e => ({ ...e })),      // new ids on write, same seq
  };
  return clone;
}

export interface ReplayDiff { step: number; kind: string; drift: "none" | "output" | "error" | "latency" }

/** REPLAY — compare a fresh execution against the recorded one. */
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

/** RESUME — idempotency keys make re-execution after a crash safe. */
export function stepsToSkip(events: TrajectoryEvent[], done: Set<string>): string[] {
  return events.filter(e => e.kind === "tool_call" && done.has(idempotencyKeyOf(e)))
               .map(e => e.payload.callId as string);
}
export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;  // → 07 §13.3
}
