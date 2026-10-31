import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {"Authorization": "Bearer <KEY>", "Content-Type": "application/json"}


def noul_confidence(p_yes: float) -> float:
    return abs(p_yes - 0.5) * 2


def gate_tool_call(
    conversation_context: str,
    tool_name: str,
    tool_args: dict,
    p_threshold: float = 0.6,
    conf_threshold: float = 0.5,
) -> bool:
    """
    Trả về True nếu tool được phép chạy.
    KHÔNG dựa mỗi p_yes — đọc cả confidence (margin).
    """
    state = (
        f"Conversation:\n{conversation_context}\n\n"
        f"Tool the agent wants to call: {tool_name}\n"
        f"Arguments: {tool_args}"
    )
    resp = requests.post(
        API,
        headers=HEADERS,
        json={
            "model": "jev-1.13.0",
            "state": state,
            "questions": {
                # Noul: yes/no — không có confidence riêng,
                # confidence = |p - 0.5| * 2
                "authorized": {"type": "noul"},
            },
        },
        timeout=5,
    )
    resp.raise_for_status()
    ans = resp.json()["answers"]["authorized"]
    p_yes = ans.get("p_yes", ans.get("probability_yes", 0.5))
    conf = noul_confidence(p_yes)

    if p_yes >= p_threshold and conf >= conf_threshold:
        return True                      # allow
    # block → human approval hoặc deny
    request_human_approval(tool_name, tool_args, p_yes, conf)
    return False


# Giống tinh thần LangChain AutoModeMiddleware:
# middleware wrap tool, decide allow/block trước khi tool thực thi.
def auto_mode_middleware(tool_call, context) -> bool:
    return gate_tool_call(
        conversation_context=context,
        tool_name=tool_call["name"],
        tool_args=tool_call["args"],
    )
