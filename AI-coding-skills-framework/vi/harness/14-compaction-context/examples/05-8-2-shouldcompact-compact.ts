export const COMPACT_AT = 0.70, RESUME_BUDGET = 300, MAX_TURNS = 20;

export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}

export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock;
  ratio: number; dropped: string[]; writeBack: DurableExtract;
}

export function compact(
  spans: ContextSpan[], budget: number, goal: string,
  pins: PinSet, plan: PlanGraph, activeLoop: ActiveLoop | null,
): CompactOutcome {
  // 1. Pin set trước — không bao giờ là ứng viên bị loại, bất kể điểm số.
  const pinned = spans.filter(s => isPinned(s, pins, plan.state));
  const now = maxTurn(spans);
  const activeTask = plan.activeTask ?? null;   // task mà resume block phải tiếp tục

  // 2. Phần còn lại xếp theo utility nhận thức trajectory, cao xuống thấp.
  const rest = spans.filter(s => !isPinned(s, pins, plan.state))
    .map(s => ({ s, u: utility(s, plan, activeLoop, now) }))
    .sort((a, b) => b.u - a.u);

  // 3. Lấp ngân sách từ trên xuống.
  let used = pinned.reduce((n, s) => n + s.tokens, 0) + RESUME_BUDGET;
  const kept = [...pinned];
  for (const { s } of rest) if (used + s.tokens <= budget) { kept.push(s); used += s.tokens; }

  // 4. Gộp retry giống hệt thay vì bỏ hẳn.
  const { kept: collapsed, resumeHints } = collapseRetries(kept);

  // 5. Trích nội dung bền từ những gì sắp đi.
  const dropped = spans.filter(s => !collapsed.some(k => k.id === s.id));
  const writeBack = extractDurable(dropped, goal);

  // 6. Resume block có cấu trúc, dựng từ nội dung bền + trạng thái plan.
  const resume: ResumeBlock = {
    goal,
    decisions: writeBack.decisions.slice(0, 5),
    open: plan.pending(activeTask).map(t => ({ taskId: t.id, title: t.title })),
    repro: activeLoop
      ? { command: activeLoop.command, error: firstLine(activeLoop.error) }
      : { command: plan.reproCommand(activeTask), error: plan.lastError(activeTask) },
    next: plan.nextAction(activeTask),
    invariants: pins.invariants,
    evicted: dropped.map(s => s.id),
  };
  resumeHints.forEach(h => resume.decisions.push(h));   // "retry 6×, last_err: …"

  return {
    kept: collapsed, resume, writeBack,
    dropped: dropped.map(s => s.id),
    ratio: totalTokens(spans) / (used || 1),
  };
}
