if (s.needsApproval && this.approvals.get(key) !== "ok") {
  this.ckpt({ runId, key, status: "waiting_approval", at: Date.now() });
  throw new Error(`PAUSED:${s.id}: awaiting approval`);
}
