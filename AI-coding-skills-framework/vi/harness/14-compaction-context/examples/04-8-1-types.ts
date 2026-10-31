export interface ContextSpan {
  id: string;                    // span_01H…  — đơn vị bị loại
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number;
  tokens: number;
  text?: string;
  path?: string;                 // cho span diff
  tool?: string;
  gateKey?: string;              // cho span approval
  producedFor?: string[];        // các task id span này phục vụ (plan graph, → 08)
  keep?: boolean;                // pin cứng, thắng điểm chấm
}

export interface ResumeBlock {
  goal: string;
  decisions: string[];           // ≤5
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string;
  invariants: string[];
  evicted: string[];             // span id
}
