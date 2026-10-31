import json
from typing import Dict, Optional

RUBRIC_PROMPT = """You are a strict evaluator. Grade the agent's answer.

TASK: {task}
AGENT ANSWER: {answer}
SOURCES USED: {sources}

Score each dimension 0.0-1.0:
- factual_accuracy: Do claims match the sources?
- citation_accuracy: Are citations correct for each claim?
- completeness: Does it address all parts of the task?
- source_quality: Are primary sources preferred over secondary?
- tool_efficiency: Were tool calls reasonable, minimal, purposeful?

Return ONLY valid JSON:
{{"scores": {{"factual_accuracy": 0.0, "citation_accuracy": 0.0,
"completeness": 0.0, "source_quality": 0.0, "tool_efficiency": 0.0}},
"overall": 0.0, "verdict": "pass"|"fail", "reason": "..."}}"""

PASS_THRESHOLD = 0.7

def llm_judge(task: str, answer: str, sources: str,
              call_llm, threshold: float = PASS_THRESHOLD) -> Optional[Dict]:
    """Chấm 1 output bằng LLM-as-judge: 1 call, 1 rubric, trả score + pass/fail."""
    prompt = RUBRIC_PROMPT.format(task=task, answer=answer, sources=sources)
    raw = call_llm(prompt)  # 1 LLM call duy nhất

    try:
        start, end = raw.find("{"), raw.rfind("}") + 1
        verdict = json.loads(raw[start:end])  # parse score JSON
    except (ValueError, json.JSONDecodeError):
        return None  # judge lỗi format → bỏ qua, không chấm bừa

    score = float(verdict.get("overall", 0.0))
    return {
        "score": round(score, 2),
        "pass": score >= threshold,          # pass/fail theo threshold
        "verdict": verdict.get("verdict", "fail"),
        "reason": verdict.get("reason", ""),
    }

# Ví dụ dùng:
# result = llm_judge(task="Tóm tắt paper X", answer="...", sources="...",
#                    call_llm=my_llm_client)
# if result and not result["pass"]:
#     print(f"❌ Fail ({result['score']}): {result['reason']}")
