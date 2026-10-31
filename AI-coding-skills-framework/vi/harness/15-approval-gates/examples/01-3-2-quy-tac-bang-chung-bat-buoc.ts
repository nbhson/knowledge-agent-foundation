export function validatePayload(r: GateRequest): string[] {
  const missing: string[] = [];
  if (!r.diff)                  missing.push("diff");
  if (r.blastRadius.length === 0) missing.push("blastRadius");
  if (!r.dryRun)                missing.push("dryRun");      // bằng chứng, không phải tóm tắt
  if (!r.rollback)              missing.push("rollback");
  if (!r.expiresAt || r.expiresAt <= Date.now()) missing.push("expiresAt");
  return missing;
}
