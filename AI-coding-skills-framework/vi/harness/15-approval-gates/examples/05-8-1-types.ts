export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;                 // node plan graph (→ 04)
  runId: string;                  // cho resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;                // proposer (two-person rule)
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

export interface RiskTableEntry {
  action: string;                 // registry key, ví dụ "db.migrate"
  defaultTier: Tier;
  paths?: RegExp[];               // ví dụ force-push trên "release/*"
  noDryRunAllowlist?: boolean;    // bản thân phải được duyệt policy
}
