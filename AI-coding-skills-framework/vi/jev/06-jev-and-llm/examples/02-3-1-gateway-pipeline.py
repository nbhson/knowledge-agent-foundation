import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def tool_call_gateway(context: str, tool: dict,
                      p_threshold: float = 0.6) -> tuple[bool, dict]:
    """
    Trả về (allowed, meta).
    allowed=False → chuyển approval flow, KHÔNG chạy tool.
    """
    state = (
        f"Context:\n{context}\n\n"
        f"Tool: {tool['name']}\nArgs: {tool.get('args', {})}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {"authorized": {"type": "noul"}},
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["authorized"]
    p_yes = ans.get("p_yes", 0.5)
    conf = abs(p_yes - 0.5) * 2
    meta = {"p_yes": p_yes, "confidence": conf,
            "request_id": resp.json().get("request_id")}

    if p_yes >= p_threshold and conf >= 0.5:
        return True, meta                      # allow → tool chạy

    # block → approval flow (auth layer thật quyết định tiếp)
    approval_request(tool, meta)               # human / policy engine
    return False, meta
