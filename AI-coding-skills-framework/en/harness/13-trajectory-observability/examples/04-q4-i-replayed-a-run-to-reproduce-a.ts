export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;
}
// replay: key already in `done` → skip the call, use the recorded tool_result
