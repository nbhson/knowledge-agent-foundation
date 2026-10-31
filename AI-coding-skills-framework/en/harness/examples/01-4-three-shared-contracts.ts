// A. Trajectory event — the single source of truth for debugging (13 produces, every module emits)
interface TrajectoryEvent {
  id: string;            // evt_01H…
  sessionId: string;
  parentTaskId?: string; // links to 08-task
  ts: number;
  kind: "prompt" | "tool_call" | "tool_result" | "plan" | "eval" | "memory_write" | "approval";
  payload: unknown;
  tokens?: { in: number; out: number };
  latencyMs?: number;
}

// B. Context object — 02 builds, 05 renders
interface BuiltContext {
  system: string;        // identity, rules (never trimmed)
  goal: string;          // current task + definition of done
  retrieved: Chunk[];    // from 01, with scores
  history: string;       // compressed summary, not the raw log
  immediate: FileSnap[]; // open files, diffs
  budget: { limit: number; used: number };
}

// C. Task node — 04 creates, 07 runs, 08 tracks
interface TaskNode {
  id: string;
  title: string;
  status: "pending" | "running" | "blocked" | "done" | "failed";
  idempotencyKey: string; // safe retry
  needsApproval: boolean;
  budget: { maxSteps: number; maxTokens: number; timeoutMs: number };
  deps: string[];
}
