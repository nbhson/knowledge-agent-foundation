// Hợp đồng chuẩn — định nghĩa đúng một lần, ở 13-trajectory-observability §1.1
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
  id: string;             // evt_01HZX… — sắp xếp được theo thứ tự chuỗi (ULID/KSUID)
  seq: number;            // 0-based, không lỗ hổng, đơn điệu trong một session
  sessionId: string;
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // một lần gọi engine; một session có thể có nhiều lần
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: unknown;       // đã redact; ≤64KB; vượt → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;
  costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string;
}
