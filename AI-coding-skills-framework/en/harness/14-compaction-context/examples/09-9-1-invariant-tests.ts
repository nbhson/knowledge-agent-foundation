export function assertInvariants(o: CompactOutcome, budget: number): void {
  const keptIds = new Set(o.kept.map(s => s.id));

  for (const p of PINNED_KINDS)                                            // (1) pins survive
    if (o.dropped.some(id => kindOf(id) === p)) throw new Error(`evicted pinned ${p}`);

  if (totalTokens(o.kept) > budget) throw new Error("over budget");       // (2) fits
  if (countTokens(o.resume) > RESUME_BUDGET) throw new Error("resume too big");
  if (!resumeIsSufficient(o.resume, o.resume.next)) throw new Error("resume insufficient");
  if (o.resume.evicted.length !== o.dropped.length) throw new Error("audit ids mismatch");
  if (o.ratio < 1.2) throw new Error(`weak ratio ${o.ratio.toFixed(2)}`);  // (3) actually compacted
  for (const s of o.kept) if (!keptIds.has(s.id)) throw new Error("kept/evicted overlap");
}
