interface SubAgentSpec {
  role: "implementer" | "verifier" | "reviewer" | "researcher";
  taskId: string;
  goal: string;              // narrow, single job, with definition of done
  context: {                 // NEVER dump the full parent context
    files: string[];
    artifactRefs: { path: string; hash: string }[];
    parentSummary: string;   // trimmed parent transcript, not raw log
  };
  tools: string[];           // narrowed allow-list from the role matrix in 12-sandbox section 6
  worktree?: string;         // REQUIRED for code-editing sub-agents
  budget: { maxTokens: number; maxSteps: number; timeoutMs: number };
  lease: { leaseId: number; deadlineMs: number; maxAttempts: number };
  secrets?: { scope: string; ttlMinutes: number }; // 5-15m, env injection, redact before logging
}
