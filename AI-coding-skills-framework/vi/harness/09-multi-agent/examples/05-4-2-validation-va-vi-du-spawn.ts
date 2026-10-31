function validateSpec(s: SubAgentSpec): string[] {
  const errs: string[] = [];
  if (!s.goal || s.goal.length < 20) errs.push("goal phải hẹp + kiểm được (>=20 ký tự)");
  if (!s.context.files.length && !s.context.parentSummary) errs.push("cần files[] hoặc parentSummary");
  if (s.role === "implementer" && !s.worktree) errs.push("implementer bắt buộc worktree");
  if (s.role === "reviewer" && s.tools.includes("shell")) errs.push("reviewer không được có shell");
  if (s.budget.maxTokens > 8000) errs.push("budget sub-agent quá lớn; tách task");
  return errs;
}

const researcherSpawn: SubAgentSpec = {
  role: "researcher", taskId: "T-101",
  goal: "Tìm logic token-refresh; trả 3 files kèm citations file:line",
  context: { files: ["src/auth/"], artifactRefs: [], parentSummary: "Parent: refresh fail sau expiry; nghi interceptor." },
  tools: ["fs.read", "code.search"],
  budget: { maxTokens: 2000, maxSteps: 10, timeoutMs: 120_000 },
  lease: { leaseId: 1, deadlineMs: Date.now() + 120_000, maxAttempts: 3 },
};

const implementerSpawn: SubAgentSpec = {
  role: "implementer", taskId: "T-102",
  goal: "Sửa refresh trong src/auth/refresh.ts theo AC-3; không chạm module khác",
  context: { files: ["src/auth/refresh.ts", "src/auth/interceptor.ts"],
    artifactRefs: [{ path: "s3://artifacts/research-T101.md", hash: "sha256:abc" }],
    parentSummary: "Research T-101: refresh() mất timer khi 401; xem artifact." },
  tools: ["fs.read", "fs.write.scoped", "shell.sandboxed"],
  worktree: "/tmp/wt/T-102",
  budget: { maxTokens: 6000, maxSteps: 25, timeoutMs: 300_000 },
  lease: { leaseId: 7, deadlineMs: Date.now() + 300_000, maxAttempts: 3 },
  secrets: { scope: "ci:read", ttlMinutes: 10 },
};
