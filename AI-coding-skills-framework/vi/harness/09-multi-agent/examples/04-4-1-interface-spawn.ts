interface SubAgentSpec {
  role: "implementer" | "verifier" | "reviewer" | "researcher";
  taskId: string;            // link tới TaskNode ở 08-task
  goal: string;              // hẹp, một việc, có definition of done
  context: {                 // KHÔNG dump toàn bộ context cha
    files: string[];         // allow-list đường dẫn
    artifactRefs: { path: string; hash: string }[]; // payload lớn → ref, không inline
    parentSummary: string;   // transcript cha đã rút gọn, không raw log
  };
  tools: string[];           // allow-list thu hẹp từ ma trận role ở 12-sandbox §6
  worktree?: string;         // BẮT BUỘC với code-editing sub-agents (isolation)
  budget: { maxTokens: number; maxSteps: number; timeoutMs: number };
  lease: { leaseId: number; deadlineMs: number; maxAttempts: number };
  secrets?: { scope: string; ttlMinutes: number }; // 5–15p, env injection, redact trước khi log
}
