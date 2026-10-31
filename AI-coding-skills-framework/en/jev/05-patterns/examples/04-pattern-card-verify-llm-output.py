import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
PASS_THRESHOLD = 0.85

def verified_cascade(policy_text: str, draft: str) -> dict:
    """LLM drafts → Jev verifies grounding against policy → pass/fail."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {
                "policy": policy_text,     # the standard to check against
                "draft": draft,            # what the LLM wrote
            },
            "questions": {
                "grounded_in_policy": {"type": "noul"},
                "worst_violation": {       # only consulted when Noul fails
                    "type": "choice",
                    "options": ["none", "unsupported_claim",
                                "wrong_number", "tone", "pii_leak"],
                },
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    p_pass = res["grounded_in_policy"]["probability"]
    if p_pass >= PASS_THRESHOLD:
        return {"status": "pass", "p_pass": p_pass, "draft": draft}

    # fail → fallback: stronger LLM, human review, or discard
    return {
        "status": "fail",
        "p_pass": p_pass,
        "flag": res["worst_violation"]["selected"],
        "next": "fallback_llm",   # e.g. call a stronger model for a rewrite
    }
