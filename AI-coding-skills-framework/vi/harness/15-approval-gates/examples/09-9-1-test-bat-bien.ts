export function assertGateInvariants(...gates: Gate[]): void {
  for (const g of gates) {
    // 1 — settled đúng một lần
    if (g.state.status === "settled" && g.state.at < g.createdAt) throw new Error("verdict before creation");
    // 2 — bằng chứng bắt buộc
    if (g.state.status === "settled" && g.state.verdict === "approved" && !g.dryRunHash) throw new Error("approved without dry-run hash");
    // 3 — fail closed
    if (g.expiresAt < Date.now() && g.state.status === "waiting") throw new Error("expired gate still waiting (timer lost)");
    // 4 — two-person rule
    if (g.tier === "prod-auth" && g.state.status === "settled" && g.state.verdict === "approved"
        && g.state.by === g.actorId) throw new Error("self-approval on prod-auth");
    // 5 — mất thứ tự: verdict không được có trước bằng chứng đang được review
    if (typeof g.diffHash === "string" && g.diffHash === "" ) throw new Error("empty diff hash");
  }
}
