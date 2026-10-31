import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def decide_tools(harness_context: str, available_tools: list[str]) -> dict:
    """Harness step: Jev chọn tool set (Choice) thay vì LLM đọc & chọn."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": harness_context,
            "questions": {
                "tool_choice": {"type": "choice", "options": available_tools},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["tool_choice"]
    if ans.get("confidence", 0) < 0.5:
        return {"action": "escalate", "reason": "low confidence tool select"}
    return {"action": "use", "tool": ans["selected"],
            "probs": ans.get("probabilities", {})}


def workflow_gate(step_result: str, policy: str) -> bool:
    """Harness step: Noul gate — bước sau có được chạy không."""
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": f"Policy:\n{policy}\n\nStep result:\n{step_result}",
            "questions": {"ready_for_next": {"type": "noul"}},
        },
        timeout=5,
    )
    resp.raise_for_status()
    p = resp.json()["answers"]["ready_for_next"].get("p_yes", 0.5)
    return p >= 0.7 and abs(p - 0.5) * 2 >= 0.5
