def verify_draft(policy_text, draft):
    ans = decide(state=f"Policy:\n{policy_text}\n\nDraft:\n{draft}", questions={
        "grounded":  {"type": "noul"},
        "severity":  {"type": "score",
                      "levels": ["none", "minor", "major", "critical"]}})
    p = ans["grounded"]["p"]; conf = abs(p - 0.5) * 2
    return {"pass": p >= 0.7 and conf >= 0.5, "confidence": conf,
            "severity": ans["severity"]["score"]}
