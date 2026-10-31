export function diffSessions(a: TrajectoryEvent[], b: TrajectoryEvent[]): string {
  const A = new Map(a.map(e => [e.seq, e])), B = new Map(b.map(e => [e.seq, e]));
  const lines: string[] = [];
  for (const seq of new Set([...A.keys(), ...B.keys()]).values()) {
    const x = A.get(seq), y = B.get(seq);
    if (!x) { lines.push(`+${seq} ${y!.kind} ${y!.payload.tool ?? ""}`); continue; }
    if (!y) { lines.push(`-${seq} ${x.kind} ${x.payload.tool ?? ""}`); continue; }
    if (JSON.stringify(x.payload) !== JSON.stringify(y.payload))
      lines.push(`~${seq} ${x.kind} ${x.payload.tool ?? ""} (${x.latencyMs}ms → ${y.latencyMs}ms)`);
  }
  return lines.join("\n");
}
