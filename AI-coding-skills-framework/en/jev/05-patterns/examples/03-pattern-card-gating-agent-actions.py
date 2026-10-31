import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
AUTH_THRESHOLD = 0.80   # tune from YOUR labelled examples, not defaults

def authorize_destructive_action(state: dict) -> tuple[bool, dict]:
    """Noul gate before a destructive tool call. Jev classifies; code decides."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": state,   # user's latest message + tool name + target summary
            "questions": {
                "user_authorizes": {"type": "noul"},
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    n = r.json()["results"]["user_authorizes"]
    p_yes = n["probability"]                    # P(yes), 0–1
    # Noul has no separate confidence: margin = |p - 0.5| * 2
    margin = abs(p_yes - 0.5) * 2

    audit = {"p_yes": p_yes, "margin": margin, "threshold": AUTH_THRESHOLD}

    # below threshold → block; the agent must not fire the tool
    allowed = p_yes >= AUTH_THRESHOLD and margin >= 0.5
    return allowed, audit


def run_tool_if_authorized(tool_name: str, args: dict, state: dict):
    allowed, audit = authorize_destructive_action(state)
    log_decision(tool_name, audit)            # request id, probs, threshold, outcome
    if not allowed:
        return escalate_or_ask_human(tool_name, audit)
    return execute_tool(tool_name, args)      # code acts
