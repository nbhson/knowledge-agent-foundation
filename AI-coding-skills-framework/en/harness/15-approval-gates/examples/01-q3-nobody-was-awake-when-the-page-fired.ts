export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  audit.append({ kind: "approval_verdict",
    payload: { key, verdict: "expired", reason: "ttl_elapsed" } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);
}
