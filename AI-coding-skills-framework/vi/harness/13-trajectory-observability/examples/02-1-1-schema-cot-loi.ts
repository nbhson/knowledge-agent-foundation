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
  id: string;             // evt_01HZX… — sắp xếp được theo lexicographic (ULID/KSUID)
  seq: number;            // 0-based, liền mạch, tăng đơn điệu trong session
  sessionId: string;      // một user request = một session
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // một lần engine chạy; một session có thể có nhiều lần
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: EventPayload;  // đã redact; ≤64KB; quá lớn → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;         // tier nào phục vụ step này → quy chi phí
  costUsd?: number;       // tính lúc emit, không tính lại lúc query
  error?: { code: string; retryable: boolean };
  fingerprint?: string;   // hash prompt → dedupe replay, audit compaction
}
