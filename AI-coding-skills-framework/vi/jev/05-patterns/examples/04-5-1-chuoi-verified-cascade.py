import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def verify_draft(policy_text: str, draft: str) -> dict:
    """
    Jev check: draft có grounded theo policy_text không?
    Noul → P(yes), confidence = |p-0.5|*2
    """
    state = (
        f"Policy document:\n{policy_text}\n\n"
        f"Draft output to check:\n{draft}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                "grounded": {"type": "noul"},          # có grounded policy?
                "severity": {                           # mức vi phạm nếu fail
                    "type": "score",
                    "levels": ["none", "minor", "major", "critical"],
                },
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]
    p_yes = ans["grounded"].get("p_yes", 0.5)
    conf = abs(p_yes - 0.5) * 2
    return {
        "pass": p_yes >= 0.7 and conf >= 0.5,
        "p_yes": p_yes,
        "confidence": conf,
        "severity": ans["severity"].get("score"),
    }


def verified_cascade(policy_text: str, draft: str, max_retries: int = 2) -> str:
    """LLM writes → Jev verifies → pass/fail → fallback."""
    for attempt in range(max_retries + 1):
        v = verify_draft(policy_text, draft)
        if v["pass"] and v["severity"] in (0, "none", None):
            return draft                          # ship
        if v["confidence"] < 0.5:
            escalate_to_human(draft, v)           # Jev mơ hồ → người
            return draft
        draft = llm_regenerate(policy_text, draft, v)   # fail → viết lại
    escalate_to_human(draft, {"reason": "max retries"})
    return draft
