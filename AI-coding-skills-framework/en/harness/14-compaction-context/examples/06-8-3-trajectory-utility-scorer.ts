export interface ActiveLoop { command: string; error: string; unresolved: boolean }

/** 0.30 recency + 0.40 structural reachability + 0.30 failure signal.
 *  The middle term is why compaction needs the plan graph (→ 04/08): it knows
 *  which spans still feed a *pending* node. */
export function utility(s: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - s.turn) / 12);

  const serves = s.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // still needed
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // branch is done
    : 0.4;                                                       // parallel / unknown

  const failure = loop?.unresolved && s.text?.includes(firstLine(loop.error)) ? 1 : 0;

  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}

/** N identical failed calls → 1 line. 18k tokens → 24. */
export function collapseRetries(spans: ContextSpan[]): { kept: ContextSpan[]; resumeHints: string[] } {
  const groups = new Map<string, ContextSpan[]>();
  for (const s of spans.filter(s => s.kind === "tool_output" || s.kind === "failure")) {
    const key = `${s.tool}:${s.kind}`;
    (groups.get(key) ?? groups.set(key, []).get(key)!).push(s);
  }
  const hints: string[] = [];
  const drop = new Set<string>();
  for (const [, g] of groups) {
    if (g.length < 3) continue;
    const last = g[g.length - 1]!;
    drop.add(last.id);
    for (const s of g.slice(0, -1)) drop.add(s.id);
    hints.push(`retried ${g.length}× (${g[0]!.turn}→${last.turn}): ${firstLine(last.text ?? "")}`);
  }
  return { kept: spans.filter(s => !drop.has(s.id)), resumeHints: hints };
}
