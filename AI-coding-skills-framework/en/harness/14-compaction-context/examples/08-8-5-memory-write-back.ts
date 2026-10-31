/** MUST run before the evicted spans are dropped. A failure here must abort the
 *  compaction — a run that silently loses a decision is worse than a run that
 *  stops with a clear error. */
export async function writeBackAndCompact(
  spans: ContextSpan[], budget: number, memory: MemoryStore, traj: TrajectorySink,
  pins: PinSet, plan: PlanGraph, loop: ActiveLoop | null, goal: string,
): Promise<CompactOutcome> {
  const o = compact(spans, budget, goal, pins, plan, loop);

  const facts = o.writeBack.facts.map(f => ({ ...f, tenantId: pins.tenantId, taskId: plan.activeTask }));
  await memory.persist(facts, { fsync: true });          // durable BEFORE eviction

  await traj.append({                                       // → 13
    kind: "compaction", parentTaskId: plan.activeTask,
    payload: { keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio,
               resumeHash: hash(renderResume(o.resume)), factsWritten: facts.length },
    tokens: { in: totalTokens(spans), out: countTokens(o.resume) },
  });

  return o;
}
