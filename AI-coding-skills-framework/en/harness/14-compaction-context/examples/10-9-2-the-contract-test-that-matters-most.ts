/** If memory is down, compaction MUST NOT silently proceed. */
it("refuses to evict unpersisted decisions", async () => {
  const spans = realTrajectorySpans();                     // 40 messages incl. 4 decisions
  const memory = brokenMemoryStore();                     // persist() always throws
  await expect(writeBackAndCompact(spans, 12_000, memory, sink, pins, plan, null, goal))
    .rejects.toThrow(/memory unavailable/);
  expect(spans.length).toBe(40);                           // nothing was evicted
});

it("a cold agent can continue from the resume block alone", async () => {
  const o = await writeBackAndCompact(realTrajectorySpans(), 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: originalSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));   // same next move
});
