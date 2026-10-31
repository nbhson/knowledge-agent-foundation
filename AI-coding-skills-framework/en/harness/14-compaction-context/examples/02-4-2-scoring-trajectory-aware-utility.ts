/** Reference implementation: §8.3. The loop's last-error signal is worth 0.30 —
 *  without it, a run stuck in a retry loop keeps scoring every span identical. */
export function utility(span: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - span.turn) / 12);
  const serves = span.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // still needed
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // branch is done
    : 0.4;                                                       // parallel / unknown
  const failure = loop?.unresolved && span.text?.includes(firstLine(loop.error)) ? 1 : 0;
  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}
