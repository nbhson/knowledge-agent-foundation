/** Deterministic steps must be byte-identical. LLM steps are compared by
 *  fingerprint + score tolerance. Anything else is a bug in the harness. */
export async function replayTest(cases: ReplayCase[]): Promise<{ name: string; drift: ReplayDiff[] }[]> {
  const out: { name: string; drift: ReplayDiff[] }[] = [];
  for (const c of cases) {
    const recorded = await loadSession(c.path);
    const fresh = await c.run();
    out.push({ name: c.name, drift: diffRun(recorded, fresh) });
  }
  return out;
}
