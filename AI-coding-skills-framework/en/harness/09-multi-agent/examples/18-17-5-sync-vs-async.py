from dataclasses import dataclass, field
from typing import List, Dict, Callable

@dataclass
class SubagentResult:
    agent_id: str
    findings: list          # refs tới artifact store, KHÔNG copy full output
    tool_calls: int
    tokens_used: int

def scale_effort(query: str) -> Dict:
    """Quy tắc 3: scale số subagent theo độ phức tạp query."""
    q = query.lower()
    if any(k in q for k in ["so sánh", "compare", "vs", "đối chiếu"]):
        return {"n_subagents": 4, "max_tool_calls": 15, "type": "comparison"}
    if any(k in q for k in ["nghiên cứu sâu", "deep research", "phân tích toàn diện"]):
        return {"n_subagents": 12, "max_tool_calls": 20, "type": "complex"}
    return {"n_subagents": 1, "max_tool_calls": 10, "type": "fact-finding"}

def run_orchestrator(query: str, tools: Dict[str, Callable]) -> Dict:
    """Orchestrator-worker: lead lên plan, spawn subagents song song,
    mỗi subagent ghi output ra filesystem và trả về refs (không full copy)."""
    plan = scale_effort(query)                     # Quy tắc 3: scale effort
    subagent_specs = []
    for i in range(plan["n_subagents"]):
        subagent_specs.append({
            "agent_id": f"sub-{i}",
            "objective": f"Phủ khía cạnh {i+1}/{plan['n_subagents']} của: {query}",
            "output_format": "markdown, mỗi finding kèm citation (artifact path + hash)",
            "tool_guidance": "3+ tools song song mỗi lượt nếu độc lập",  # Quy tắc 8
            "task_boundaries": "KHÔNG ôm khía cạnh của subagent khác",   # Quy tắc 2
            "max_tool_calls": plan["max_tool_calls"],
        })

    # Spawn song song (sync): lead chờ toàn bộ — không steer giữa chừng (Quy tắc 17.5)
    results: list[SubagentResult] = []
    for spec in subagent_specs:
        calls = 0
        while calls < spec["max_tool_calls"]:
            calls += 1                              # Đếm tool call
        results.append(SubagentResult(
            agent_id=spec["agent_id"],
            findings=[f"artifact://{spec['agent_id']}/report.md"],
            tool_calls=calls, tokens_used=calls * 4000,
        ))

    total_tokens = sum(r.tokens_used for r in results)
    return {
        "plan": plan,
        "subagent_count": len(results),
        "artifact_refs": [r.findings for r in results],   # Quy tắc 4.16.4: refs, không full copy
        "total_tokens": total_tokens,                     # Quy tắc 17.1: token = yếu tố 80% variance
    }
