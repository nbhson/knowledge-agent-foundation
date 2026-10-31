def decide_or_fallback(state, questions):
    ans = jev_decide(state, questions)["answers"]["queue"]
    conf = ans["confidence"]
    if conf >= 0.8:
        return {"by": "jev", "value": ans["selected"]}
    if conf >= 0.5:
        return {"by": "jev", "value": ans["selected"], "needs_confirm": True}
    return {"by": "llm_or_human", "value": llm_decide(state, questions)}
