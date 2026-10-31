export interface ActiveLoop { command: string; error: string; unresolved: boolean }

/** 0.30 recency + 0.40 structural reachability + 0.30 failure signal.
 *  Thành phần giữa là lý do compaction cần plan graph (→ 04/08): nó biết
 *  span nào vẫn đang nuôi một node *đang chờ*. */
export function utility(s: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - s.turn) / 12);

  const serves = s.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // vẫn cần
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // nhánh đã xong
    : 0.4;                                                       // song song / chưa biết

  const failure = loop?.unresolved && s.text?.includes(firstLine(loop.error)) ? 1 : 0;

  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}

/** N lần gọi thất bại giống hệt → 1 dòng. 18k token → 24. */
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
    hints.push(`retry ${g.length}× (${g[0]!.turn}→${last.turn}): ${firstLine(last.text ?? "")}`);
  }
  return { kept: spans.filter(s => !drop.has(s.id)), resumeHints: hints };
}
