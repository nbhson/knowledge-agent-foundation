// engine từ chối materialize action tới khi một human KHÁC approve
export function tryApprove(key: string, approverId: string, reason?: string): boolean {
  const g = gates.get(key); if (!g || g.verdict) return false;
  if (g.req.actorId === approverId) {
    traj.warn({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
    return false;                                  // proposer ≠ approver, cứng
  }
  gates.get(key)!.actorApproval = approverId;      // human độc lập thứ hai xác nhận
}
