import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
DESTRUCTIVE = {"delete_files", "charge_account", "send_email"}
AUTHORIZE_THRESHOLD = 0.80


def tool_gateway(proposed_tool: str, args: dict, agent_state: dict) -> dict:
    """Jev gates side-effecting tool calls before execution."""
    if proposed_tool not in DESTRUCTIVE:
        return {"allow": True, "gate": "passthrough"}

    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {
                "user_request": agent_state.get("last_user_message", ""),
                "tool": proposed_tool,
                "target_summary": args.get("summary", str(args))[:500],
            },
            "questions": {"authorized": {"type": "noul"}},
        },
        timeout=5.0,
    )
    r.raise_for_status()
    p_yes = r.json()["results"]["authorized"]["probability"]

    allow = p_yes >= AUTHORIZE_THRESHOLD
    log_decision(proposed_tool, {"p_yes": p_yes,
                                 "threshold": AUTHORIZE_THRESHOLD,
                                 "model": "jev-latest"})
    if not allow:
        return {"allow": False, "gate": "blocked",
                "next": "request_approval"}   # tie into auth/approval system
    return {"allow": True, "gate": "authorized"}
