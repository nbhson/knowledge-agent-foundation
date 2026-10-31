// ── The Gate ───────────────────────────────────────────────────────────────
export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;            // plan graph node (→ 04)
  runId: string;             // resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;           // proposer — two-person rule anchor
  summary: string;
  diff: string;
  blastRadius: string[];
  dryRun: string;
  rollback: string;
  diffHash: string;
  dryRunHash: string;
  createdAt: number;
  expiresAt: number;
  state: GateState;
}

// ── Risk Registry ──────────────────────────────────────────────────────────
export interface RiskTableEntry {
  action: string;
  defaultTier: Tier;
  paths?: RegExp[];
  noDryRunAllowlist?: boolean;
}
export interface RoleRiskMatrix {
  role: string;               // → 12 §6 per-role policy
  entries: RiskTableEntry[];
  override?: { action: string; tier: Tier; reason: string; approvedBy: string; at: number };
}

// ── Gatekeeper ─────────────────────────────────────────────────────────────
export interface Gatekeeper {
  request(input: GateRequestInput): Gate;
  settle(key: string, v: Verdict, by: string, reason?: string): boolean;
  verdict(key: string): Verdict | undefined;
  armed(key: string): boolean;
}
export interface GateEngineContract {
  before(action: Step): Tier;              // enforcement at plan-time tag (§2.2)
  request(input: GateRequestInput): Gate;  // throws PAUSED:<key> after checkpoint
  onVerdict(key: string, v: Verdict): void; // approved→resume; denied/expired→replan
}

// ── Audit ──────────────────────────────────────────────────────────────────
export interface ApprovalAuditEvent {
  kind: "approval_request" | "approval_verdict" | "approval_policy" | "notification_sent";
  payload: { key: string; tier: Tier; actorId: string; approver?: string;
             verdict?: Verdict; reason?: string; diffHash?: string; dryRunHash?: string;
             by?: string; at: number };
  sessionId: string; taskId: string;     // join keys (→ 13 §4)
  tokens: { in: number; out: number };
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface GateInvariant { name: string; assert(g: Gate): void }
export interface FatigueMetric { tier: Tier; approvalRate: number; medianWaitMs: number }
