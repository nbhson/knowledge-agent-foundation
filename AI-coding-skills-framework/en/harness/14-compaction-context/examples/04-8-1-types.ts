export interface ContextSpan {
  id: string;                    // span_01H…  — the unit of eviction
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number;
  tokens: number;
  text?: string;
  path?: string;                 // for diff spans
  tool?: string;
  gateKey?: string;              // for approval spans
  producedFor?: string[];        // task ids this span serves (plan graph, → 08)
  keep?: boolean;                // hard pin, overrides scoring
}

export interface ResumeBlock {
  goal: string;
  decisions: string[];           // ≤5
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string;
  invariants: string[];
  evicted: string[];             // span ids
}
