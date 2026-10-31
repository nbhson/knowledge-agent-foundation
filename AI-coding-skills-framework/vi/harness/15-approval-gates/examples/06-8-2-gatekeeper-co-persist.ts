import { randomBytes, createHash } from "node:crypto";

export class Gatekeeper {
  private gates = new Map<string, Gate>();
  constructor(
    private store: TrajectoryStore,          // audit/độ bền (→ 13)
    private risk: RiskTableEntry[],          // registry tier
  ) {
    this.reloadOpen();                       // sống sót qua restart
  }

  private key(): string { return `gate_${randomBytes(4).toString("hex")}`; }

  /** Validate tier + bằng chứng, persist, nạp đạn timer fail-closed. */
  request(input: Omit<Gate, "key" | "state" | "createdAt" | "diffHash">
      | { diff: string; dryRun: string }): Gate {
    const missing = validatePayload(input);              // §3.2 bằng chứng bắt buộc
    if (missing.length) throw new Error(`gate missing evidence: ${missing.join(",")}`);
    const gate: Gate = {
      ...input, key: this.key(), createdAt: Date.now(), state: { status: "waiting" },
      diffHash: createHash("sha256").update(input.diff).digest("hex"),
      dryRunHash: createHash("sha256").update(input.dryRun).digest("hex"),
    };
    this.gates.set(gate.key, gate);
    this.store.append({ kind: "approval_request", payload: gate });
    this.armTimer(gate);
    return gate;
  }

  private armTimer(g: Gate): void {
    const ms = g.expiresAt - Date.now();
    setTimeout(() => this.settle(g.key, "expired", "timer"), Math.max(0, ms));
  }

  /** Một verdict thắng. Tự duyệt trên prod-auth bị từ chối và được audit. */
  settle(key: string, v: Verdict, by: string, reason?: string): boolean {
    const g = this.gates.get(key);
    if (!g || g.state.status === "settled") return false;
    if (v === "approved" && g.tier === "prod-auth" && by === g.actorId) {
      this.store.append({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
      return false;
    }
    g.state = { status: "settled", verdict: v, by, at: Date.now() };
    this.store.append({ kind: "approval_verdict",
      payload: { key, verdict: v, by, reason, diffHash: g.diffHash, dryRunHash: g.dryRunHash } });
    return true;
  }

  verdict(key: string): Verdict | undefined {
    return this.gates.get(key)?.state.status === "settled"
      ? (this.gates.get(key)!.state as { verdict: Verdict }).verdict : undefined;
  }

  private reloadOpen(): void {
    for (const ev of this.store.query({ kind: "approval_request" })) {
      if (!this.verdict(ev.payload.key)) {                    // gate đang mở → nạp lại timer
        const g = ev.payload as Gate;
        this.gates.set(g.key, g);
        this.armTimer(g);
      }
    }
  }
}
