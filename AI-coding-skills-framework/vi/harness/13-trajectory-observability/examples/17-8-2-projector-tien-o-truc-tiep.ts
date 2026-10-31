/** Chiếu event stream thành trạng thái UI sống. Cùng một stream, khác cái nhìn —
 *  UI là một phép gấp trên trajectory, không phải nguồn sự thật thứ hai. */
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string; status: "running" | "waiting" | "done" | "failed";
}

export function project(e: TrajectoryEvent, prev: RunProgress): RunProgress {
  const next = { ...prev, stepsDone: prev.stepsDone + (e.kind === "tool_result" ? 1 : 0) };
  if (e.tokens) next.tokens += e.tokens.in + e.tokens.out;
  next.costUsd += e.costUsd ?? 0;
  if (e.kind === "plan") next.currentTask = (e.payload as any).firstPendingTask;
  if (e.kind === "approval_request") next.status = "waiting";
  if (e.kind === "approval_verdict") next.status = "running";
  if (e.kind === "error") next.lastError = e.error?.code;
  if (e.kind === "session_end")
    next.status = (e.payload as any).tasksDone === (e.payload as any).tasksTotal ? "done" : "failed";
  return next;
}
