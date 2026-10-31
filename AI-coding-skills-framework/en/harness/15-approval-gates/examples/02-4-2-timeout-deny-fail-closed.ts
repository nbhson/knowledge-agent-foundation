// fail-closed consequence of expiry
export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  traj.append({ kind: "approval_verdict", payload: { key, verdict: "expired",
    reason: "ttl_elapsed", at: Date.now() } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);   // → 04 §14.2
}
