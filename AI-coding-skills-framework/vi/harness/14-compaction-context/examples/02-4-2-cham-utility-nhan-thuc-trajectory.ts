/** Cài đặt tham chiếu: §8.3. Tín hiệu lỗi cuối của loop đáng 0.30 — thiếu nó, một
 *  run mắc kẹt trong vòng retry sẽ chấm mọi span điểm giống nhau. */
export function utility(span: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - span.turn) / 12);
  const serves = span.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // vẫn cần
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // nhánh đã xong
    : 0.4;                                                       // song song / chưa rõ
  const failure = loop?.unresolved && span.text?.includes(firstLine(loop.error)) ? 1 : 0;
  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}
