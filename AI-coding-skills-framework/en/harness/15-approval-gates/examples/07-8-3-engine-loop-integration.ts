export async function runStep(step: Step, ctx: Ctx): Promise<void> {
  const tier = resolveTier(step, ctx.risk);                  // §2.1 rule, not model
  await checkpoint(ctx, step);                               // (→ 07 §13) BEFORE throw

  if (tier === "read") { await step.run(ctx); return; }      // auto-approve, log

  const gate = ctx.gates.request({ taskId: step.id, runId: ctx.runId, tier,
    actorId: ctx.actorId, summary: step.summary, diff: step.renderDiff(),
    blastRadius: step.blastRadius(ctx), dryRun: await step.dryRun(ctx),
    rollback: step.rollback(ctx) });
  await ctx.notify(gate);                                    // §7.2

  throw new Paused(`PAUSED:${gate.key}`);                    // freezes, audit sees it

  // resumed later by driver after human verdict:
  //   verdict=approved → this function returns, step.run() executes once
  //   verdict=denied/expired → markBlocked → replanner.excludeBranch(step.id)
}
