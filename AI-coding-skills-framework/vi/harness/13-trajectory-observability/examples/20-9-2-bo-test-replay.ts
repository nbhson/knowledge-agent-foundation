/** Step tất định phải giống byte. Step LLM so bằng fingerprint + dung sai score.
 *  Bất cứ thứ gì khác là bug của harness. */
export async function replayTest(cases: ReplayCase[]): Promise<{ name: string; drift: ReplayDiff[] }[]> {
  const out: { name: string; drift: ReplayDiff[] }[] = [];
  for (const c of cases) {
    const recorded = await loadSession(c.path);
    const fresh = await c.run();
    out.push({ name: c.name, drift: diffRun(recorded, fresh) });
  }
  return out;
}
