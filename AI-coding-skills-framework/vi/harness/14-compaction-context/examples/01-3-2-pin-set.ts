export interface PinSet {
  tenantId: string;                   // khoá định tuyến + nhất quán (→ 05 §17.5)
  system: true;                       // luôn luôn
  goal: true;                         // task spec + definition of done
  invariants: string[];               // ≤5 ràng buộc từ plan (→ 05 §17.5)
  activeDiffPaths: string[];          // file có edit chưa commit
  lastUserMessage: true;              // chỉ dẫn gần nhất thắng
  activeLoopFailure?: { cmd: string; error: string };   // chỉ khi loop chưa xong
  pendingApprovals: string[];         // gate key đang chờ verdict (→ 15)
  schema: true;                       // hình dạng câu trả lời cuối
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
