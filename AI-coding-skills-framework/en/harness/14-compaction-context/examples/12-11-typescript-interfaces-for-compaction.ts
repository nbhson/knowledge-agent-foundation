// ── Context ────────────────────────────────────────────────────────────────
export interface ContextSpan {
  id: string;
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number; tokens: number;
  text?: string; path?: string; tool?: string; gateKey?: string;
  producedFor?: string[];      // task ids served (plan graph, → 08)
  keep?: boolean;              // hard pin
}

// ── Policy ─────────────────────────────────────────────────────────────────
export interface CompactionPolicy {
  triggerRatio: number;        // 0.70
  maxTurns: number;            // 20
  resumeBudgetTokens: number;  // 300
  minRatio: number;            // 1.2 — below this, compaction "failed"
  weights: { recency: number; reachability: number; failure: number };
  collapseRetryThreshold: number;  // 3
}
export const DEFAULT_POLICY: CompactionPolicy = {
  triggerRatio: 0.70, maxTurns: 20, resumeBudgetTokens: 300, minRatio: 1.2,
  weights: { recency: 0.30, reachability: 0.40, failure: 0.30 },
  collapseRetryThreshold: 3,
};

// ── Pin set ────────────────────────────────────────────────────────────────
export interface PinSet {
  tenantId: string; system: true; goal: true; schema: true;
  lastUserMessage: true; invariants: string[];
  activeDiffPaths: string[]; pendingApprovals: string[];   // → 15
}

// ── Resume ─────────────────────────────────────────────────────────────────
export interface ResumeBlock {
  goal: string; decisions: string[];
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string; invariants: string[]; evicted: string[];
}

// ── Outcome ────────────────────────────────────────────────────────────────
export interface DurableExtract {
  facts: { key: string; value: string; kind: "decision" | "constraint" | "preference" | "todo" }[];
}
export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock; ratio: number;
  dropped: string[]; writeBack: DurableExtract;
}

// ── Compactor ──────────────────────────────────────────────────────────────
export interface Compactor {
  shouldCompact(used: number, budget: number, turns: number): boolean;
  compact(spans: ContextSpan[], budget: number, goal: string, pins: PinSet,
          plan: PlanGraph, loop: ActiveLoop | null): CompactOutcome;
  buildResume(input: ResumeInput): ResumeBlock;
  render(b: ResumeBlock): string;
  /** MUST persist before returning. A throw here must abort the compaction. */
  writeBackAndCompact(spans: ContextSpan[], budget: number, memory: MemoryStore,
                      traj: TrajectorySink, pins: PinSet, plan: PlanGraph,
                      loop: ActiveLoop | null, goal: string): Promise<CompactOutcome>;
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface CompactionInvariant { name: string; assert(o: CompactOutcome, budget: number): void }
export interface ColdStartTest {
  name: string; spans: ContextSpan[]; budget: number;
  expectSameNextAction: boolean;
}
