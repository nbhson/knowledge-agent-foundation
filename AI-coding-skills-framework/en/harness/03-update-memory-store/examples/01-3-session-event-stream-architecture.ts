// Canonical contract — defined once, in 13-trajectory-observability §1.1
export type EventKind =
  | "session_start" | "session_end"
  | "context_assembly" | "prompt"
  | "plan" | "plan_revision"
  | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write"
  | "delegate" | "message"
  | "approval_request" | "approval_verdict"
  | "compaction" | "checkpoint" | "eval" | "error";

export interface TrajectoryEvent {
  id: string;             // evt_01HZX… — lexicographically sortable (ULID/KSUID)
  seq: number;            // 0-based, gapless, monotonic within a session
  sessionId: string;
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // one engine invocation; a session may have several
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: unknown;       // redacted; ≤64KB; oversize → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;
  costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string;
}
