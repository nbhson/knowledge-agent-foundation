// ── Event ─────────────────────────────────────────────────────────────────
export type EventKind =
  | "session_start" | "session_end" | "context_assembly" | "prompt"
  | "plan" | "plan_revision" | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write" | "delegate" | "message"
  | "approval_request" | "approval_verdict" | "compaction" | "checkpoint"
  | "eval" | "error";

export interface TrajectoryEvent {
  id: string; seq: number; sessionId: string; parentTaskId?: string; runId?: string;
  ts: number; kind: EventKind; actor: string; payload: unknown;
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number; model?: string; costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string; redactions?: number; tenantId: string;
}

export type NewEvent = Omit<TrajectoryEvent, "id" | "seq" | "redactions">;

// ── Store ──────────────────────────────────────────────────────────────────
export interface TrajectoryStore {
  append(e: NewEvent): Promise<void>;
  flush(): Promise<void>;
  load(sessionId: string): Promise<TrajectoryEvent[]>;
  tail(sessionId: string, fromSeq: number): AsyncIterable<TrajectoryEvent>;
}

// ── Derived views ──────────────────────────────────────────────────────────
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string;
  status: "running" | "waiting" | "done" | "failed";
}

// ── Fork / replay ──────────────────────────────────────────────────────────
export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}
export type ReplayDrift = "none" | "output" | "error" | "latency";
export interface ReplayDiff { step: number; kind: EventKind | string; drift: ReplayDrift }

// ── Redaction ──────────────────────────────────────────────────────────────
export interface RedactionResult<T> { payload: T; redactions: number }
export interface Redactor { redact(s: string): RedactionResult<string> }

// ── Retention ──────────────────────────────────────────────────────────────
export type RetentionTier = "hot" | "warm" | "cold" | "purged";
export interface RetentionPolicy {
  hotDays: number; warmDays: number; coldDays: number;
  inlineMaxBytes: number;             // > ngưỡng này → { ref } ở tầng warm
  tenantTtlDays?: number;             // GDPR
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface ReplayCase {
  name: string; path: string;
  run(): Promise<TrajectoryEvent[]>;
  expectDeterministic: EventKind[];
}
