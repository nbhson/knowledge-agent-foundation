/** Nếu memory chết, compaction KHÔNG ĐƯỢC âm thầm tiếp tục. */
it("từ chối loại quyết định chưa lưu", async () => {
  const spans = realTrajectorySpans();                     // 40 message gồm 4 quyết định
  const memory = brokenMemoryStore();                     // persist() luôn ném lỗi
  await expect(writeBackAndCompact(spans, 12_000, memory, sink, pins, plan, null, goal))
    .rejects.toThrow(/memory unavailable/);
  expect(spans.length).toBe(40);                           // không có gì bị loại
});

it("agent lạnh đi tiếp được chỉ từ resume block", async () => {
  const o = await writeBackAndCompact(realTrajectorySpans(), 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: originalSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));   // cùng hành động kế
});
