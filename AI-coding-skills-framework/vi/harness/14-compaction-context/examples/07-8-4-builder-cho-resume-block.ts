export function buildResume(o: {
  goal: string; decisions: string[]; pending: Task[]; lastCmd: string; lastErr: string;
  invariants: string[]; evicted: string[];
}): ResumeBlock {
  const b: ResumeBlock = {
    goal: o.goal.slice(0, 200),
    decisions: o.decisions.slice(0, 5).map(d => d.slice(0, 200)),
    open: o.pending.map(t => ({ taskId: t.id, title: t.title.slice(0, 80) })),
    repro: { command: o.lastCmd.slice(0, 200), error: firstLine(o.lastErr).slice(0, 200) },
    next: o.pending[0] ? `Tiếp tục với ${o.pending[0].id}: ${o.pending[0].title}` : "Tóm tắt và bàn giao",
    invariants: o.invariants.slice(0, 5),
    evicted: o.evicted,
  };
  const t = countTokens(b);
  if (t > RESUME_BUDGET) {                                  // ngân sách cứng, được ép
    b.decisions = b.decisions.slice(0, 3);
    b.invariants = b.invariants.slice(0, 3);
    b.open = b.open.slice(0, 8);
    b.evicted = b.evicted.slice(0, 40);
  }
  return b;
}

export function renderResume(b: ResumeBlock): string {
  return [
    `Goal: ${b.goal}`,
    `Decisions: ${b.decisions.map(d => `[${d}]`).join("") || "[không có]"}`,
    `Open: ${b.open.map(t => `[${t.taskId}: ${t.title}]`).join("") || "[không có]"}`,
    `Repro: ${b.repro.command} → ${b.repro.error}`,
    `Next: ${b.next}`,
    `Invariants: ${b.invariants.join(" | ")} || "(chưa khai báo)"}`,
    `Evicted: [${b.evicted.join(",")}]`,
  ].join("\n");
}
