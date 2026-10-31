export function assertInvariants(o: CompactOutcome, budget: number): void {
  const keptIds = new Set(o.kept.map(s => s.id));

  for (const p of PINNED_KINDS)                                            // (1) pin sống
    if (o.dropped.some(id => kindOf(id) === p)) throw new Error(`đã loại span pinned ${p}`);

  if (totalTokens(o.kept) > budget) throw new Error("vượt ngân sách");   // (2) vừa ngân sách
  if (countTokens(o.resume) > RESUME_BUDGET) throw new Error("resume quá lớn");
  if (!resumeIsSufficient(o.resume, o.resume.next)) throw new Error("resume không đủ");
  if (o.resume.evicted.length !== o.dropped.length) throw new Error("lệch danh sách audit");
  if (o.ratio < 1.2) throw new Error(`ratio yếu ${o.ratio.toFixed(2)}`); // (3) có compact thật
  for (const s of o.kept) if (!keptIds.has(s.id)) throw new Error("kept/evicted chồng nhau");
}
