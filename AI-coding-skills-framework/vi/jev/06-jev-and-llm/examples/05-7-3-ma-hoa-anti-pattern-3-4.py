# Mẫu nhỏ nhấn mạnh: confidence cao VẪN cần đường fallback tổng thể
def decide_or_fallback(state: str, questions: dict) -> dict:
    result = jev_decide(state, questions)          # 70–500ms, rẻ
    ans = result["answers"]["queue"]
    conf = ans.get("confidence", 0)

    if conf >= 0.8:
        return {"by": "jev", "value": ans["selected"], "conf": conf}
    if conf >= 0.5:
        return {"by": "jev", "value": ans["selected"],
                "conf": conf, "needs_confirm": True}

    # LOW band — KHÔNG tin Jev ở đây → fallback LLM / human
    return {"by": "llm_or_human", "value": llm_decide(state, questions),
            "conf": None, "reason": "low confidence band"}
