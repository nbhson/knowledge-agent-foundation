// engine refuses to materialize the action until a DIFFERENT human approves
export function tryApprove(key: string, approverId: string, reason?: string): boolean {
  const g = gates.get(key); if (!g || g.verdict) return false;
  if (g.req.actorId === approverId) {
    traj.warn({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
    return false;                                  // proposer ≠ approver, hard
  }
  gates.get(key)!.actorApproval = approverId;      // second human confirmed
}
