it("a cold agent can continue from the resume block alone", async () => {
  const o = await writeBackAndCompact(realSpans, 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: realSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));
});
