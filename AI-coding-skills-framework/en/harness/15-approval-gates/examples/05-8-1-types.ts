export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;                 // plan graph node (→ 04)
  runId: string;                  // for resume idempotency (→ 07 §13)
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
  action: string;                 // registry key, e.g. "db.migrate"
  defaultTier: Tier;
  paths?: RegExp[];               // e.g. force-push on "release/*"
  noDryRunAllowlist?: boolean;    // must itself be policy-approved
}
