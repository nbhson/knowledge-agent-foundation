import * as fs from "node:fs";
type Step = { id: string; run: (ctx: Ctx) => Promise<any>; needsApproval?: boolean; idem?: boolean };
type Ctx = { signal: AbortSignal; idemKey: string; artifacts: Map<string, any> };
const idemStore = new Map<string, any>();
function sem(max: number) { let n = max; const q: (() => void)[] = []; return async (fn: () => Promise<any>) => { if (n <= 0) await new Promise<void>(r => q.push(r)); n--; try { return await fn(); } finally { n++; q.shift()?.(); } }; }
const gate = sem(4); // max parallel
export class DurableEngine {
  constructor(private log = "./checkpoints.jsonl", private approvals = new Map<string, "ok" | "no">()) {}
  ckpt(e: object) { fs.appendFileSync(this.log, JSON.stringify(e) + "\n"); }
  done(key: string) { try { return JSON.parse(fs.readFileSync(this.log, "utf8").split("\n").filter(Boolean).map(l => JSON.parse(l)).filter((e: any) => e.key === key && e.status === "ok").pop()?.val ?? "null"); } catch { return undefined; } }
  async run(runId: string, steps: Step[], inputs: any, deadlineMs = 120_000) {
    const deadlineAt = Date.now() + deadlineMs;
    for (const s of steps) {
      const key = `${runId}:${s.id}:${JSON.stringify(inputs).length}:${s.id}`;
      const cached = s.idem !== false ? (idemStore.get(key) ?? this.done(key)) : undefined;
      if (cached !== undefined) { inputs = cached; continue; }
      if (s.needsApproval && this.approvals.get(key) !== "ok") { this.ckpt({ runId, key, status: "waiting_approval", at: Date.now() }); throw new Error(`PAUSED:${s.id}: awaiting approval`); }
      const remain = deadlineAt - Date.now() - 500; if (remain <= 0) throw new Error("deadline exceeded");
      const out = await gate(async () => s.run({ signal: AbortSignal.timeout(remain), idemKey: key, artifacts: new Map() }));
      idemStore.set(key, out); this.ckpt({ runId, key, status: "ok", val: JSON.stringify(out).slice(0, 64_000), at: Date.now() });
      inputs = out;
    }
    return inputs;
  }
}
