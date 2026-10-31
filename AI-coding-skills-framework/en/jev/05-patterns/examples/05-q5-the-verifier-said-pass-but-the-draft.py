PASS_THRESHOLD = 0.85
p_pass = res["grounded_in_policy"]["probability"]
if p_pass >= PASS_THRESHOLD:
    return {"status": "pass", "draft": draft}
return {"status": "fail", "flag": res["worst_violation"]["selected"],
        "next": "fallback_llm"}     # stronger model, human, or discard
