export async function runStep(step: Step, ctx: Ctx): Promise<void> {
  const tier = resolveTier(step, ctx.risk);                  // §2.1 rule, không phải model
  await checkpoint(ctx, step);                               // (→ 07 §13) TRƯỚC khi throw

  if (tier === "read") { await step.run(ctx); return; }      // auto-approve, chỉ log

  const gate = ctx.gates.request({ taskId: step.id, runId: ctx.runId, tier,
    actorId: ctx.actorId, summary: step.summary, diff: step.renderDiff(),
    blastRadius: step.blastRadius(ctx), dryRun: await step.dryRun(ctx),
    rollback: step.rollback(ctx) });
  await ctx.notify(gate);                                    // §7.2

  throw new Paused(`PAUSED:${gate.key}`);                    // đóng băng, audit thấy nó

  // được driver resume sau khi có verdict:
  //   verdict=approved → hàm này trả về, step.run() thực thi đúng một lần
  //   verdict=denied/expired → markBlocked → replanner.excludeBranch(step.id)
}
