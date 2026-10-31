/** One-line human-readable trace, for `DEBUG=agent` runs. Same events, formatted. */
export function formatEvent(e: TrajectoryEvent): string {
  const t = `${String(e.seq).padStart(3, "0")} ${e.kind.padEnd(16)} ${e.actor.padEnd(12)}`;
  const detail = e.kind === "tool_call" ? `${e.payload.tool} ${JSON.stringify(e.payload.args).slice(0, 60)}`
    : e.kind === "tool_result" ? `exit=${e.payload.exitCode} ${e.latencyMs}ms ${e.payload.bytes}B`
    : e.kind === "eval" ? `score=${e.payload.score}`
    : e.kind === "compaction" ? `ratio=${e.payload.ratio} dropped=${e.payload.dropped}`
    : "";
  const cost = e.costUsd ? ` $${e.costUsd.toFixed(4)}` : "";
  return `${t} ${detail}${cost}`;
}
