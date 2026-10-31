/** PHẢI chạy trước khi các span bị loại được bỏ đi. Lỗi ở đây phải huỷ
 *  compaction — một run lặng lẽ mất quyết định tệ hơn một run dừng lại
 *  với một lỗi rõ ràng. */
export async function writeBackAndCompact(
  spans: ContextSpan[], budget: number, memory: MemoryStore, traj: TrajectorySink,
  pins: PinSet, plan: PlanGraph, loop: ActiveLoop | null, goal: string,
): Promise<CompactOutcome> {
  const o = compact(spans, budget, goal, pins, plan, loop);

  const facts = o.writeBack.facts.map(f => ({ ...f, tenantId: pins.tenantId, taskId: plan.activeTask }));
  await memory.persist(facts, { fsync: true });          // bền TRƯỚC khi loại

  await traj.append({                                       // → 13
    kind: "compaction", parentTaskId: plan.activeTask,
    payload: { keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio,
               resumeHash: hash(renderResume(o.resume)), factsWritten: facts.length },
    tokens: { in: totalTokens(spans), out: countTokens(o.resume) },
  });

  return o;
}
