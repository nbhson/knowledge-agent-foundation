export interface PinSet {
  tenantId: string;                   // routing + consistency key (→ 05 §17.5)
  system: true;                       // always
  goal: true;                         // task spec + definition of done
  invariants: string[];               // ≤5 constraints from the plan (→ 05 §17.5)
  activeDiffPaths: string[];          // files with uncommitted edits
  lastUserMessage: true;              // most recent instruction wins
  activeLoopFailure?: { cmd: string; error: string };   // only while unresolved
  pendingApprovals: string[];         // gate keys awaiting verdict (→ 15)
  schema: true;                       // the shape the final answer must take
}

export function isPinned(span: ContextSpan, pins: PinSet, planState: PlanState): boolean {
  if (span.role === "system" || span.kind === "goal" || span.kind === "schema") return true;
  if (span.kind === "user" && span.id === pins.lastUserMessage) return true;
  if (span.kind === "invariant") return true;
  if (span.kind === "diff" && pins.activeDiffPaths.includes(span.path!)) return true;
  if (span.kind === "failure" && planState.activeLoopUnresolved) return true;
  if (span.kind === "approval" && pins.pendingApprovals.includes(span.gateKey!)) return true;
  return false;
}
