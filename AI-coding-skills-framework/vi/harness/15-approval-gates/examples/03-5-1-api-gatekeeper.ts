type Verdict = "approved" | "denied" | "expired";
interface GateRequest {
  key: string; tier: "write" | "elevated" | "prod-auth";
  summary: string; diff: string; blastRadius: string[];
  dryRun: string; rollback: string; expiresAt: number;
}
export class Gatekeeper {
  private gates = new Map<string, { req: GateRequest; verdict?: Verdict }>();
  request(r: GateRequest): void {
    ensureValid(r);                          // quy tắc bằng chứng bắt buộc (§3.2)
    this.gates.set(r.key, { req: r });       // engine throws PAUSED:<key>
    setTimeout(() => this.settle(r.key, "expired"), r.expiresAt - Date.now());
  }
  settle(key: string, v: Verdict, by = "human"): void {
    const g = this.gates.get(key); if (!g || g.verdict) return;  // một verdict thắng
    g.verdict = v; // audit: { key, v, by, at: Date.now() } → trajectory (→ 13)
  }
  verdict(key: string): Verdict | undefined { return this.gates.get(key)?.verdict; }
}
// Engine loop: trước khi chạy gated step → gatekeeper.request(...) → checkpoint
// → throw PAUSED → verdict approved: resume; denied/expired: mark blocked → replan.
