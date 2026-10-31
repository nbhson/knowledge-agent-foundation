function validateSpec(s: SubAgentSpec): string[] {
  const errs: string[] = [];
  if (!s.goal || s.goal.length < 20) errs.push("goal must be narrow + testable (>=20 chars)");
  if (!s.context.files.length && !s.context.parentSummary) errs.push("need files[] or parentSummary");
  if (s.role === "implementer" && !s.worktree) errs.push("implementer requires worktree");
  if (s.role === "reviewer" && s.tools.includes("shell")) errs.push("reviewer must not have shell");
  if (s.budget.maxTokens > 8000) errs.push("sub-agent budget too large; split task");
  return errs;
}

const researcherSpawn: SubAgentSpec = {
  role: "researcher", taskId: "T-101",
  goal: "Locate token-refresh logic; return 3 files with file:line citations",
  context: { files: ["src/auth/"], artifactRefs: [], parentSummary: "Parent: refresh fails after expiry; suspect interceptor." },
  tools: ["fs.read", "code.search"],
  budget: { maxTokens: 2000, maxSteps: 10, timeoutMs: 120_000 },
  lease: { leaseId: 1, deadlineMs: Date.now() + 120_000, maxAttempts: 3 },
};

const implementerSpawn: SubAgentSpec = {
  role: "implementer", taskId: "T-102",
  goal: "Fix refresh in src/auth/refresh.ts per AC-3; do not touch other modules",
  context: { files: ["src/auth/refresh.ts", "src/auth/interceptor.ts"],
    artifactRefs: [{ path: "s3://artifacts/research-T101.md", hash: "sha256:abc" }],
    parentSummary: "Research T-101: refresh() drops timer on 401; see artifact." },
  tools: ["fs.read", "fs.write.scoped", "shell.sandboxed"],
  worktree: "/tmp/wt/T-102",
  budget: { maxTokens: 6000, maxSteps: 25, timeoutMs: 300_000 },
  lease: { leaseId: 7, deadlineMs: Date.now() + 300_000, maxAttempts: 3 },
  secrets: { scope: "ci:read", ttlMinutes: 10 },
};
