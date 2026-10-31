if state.get("transient") and state.get("attempts", 0) < 3: return "retry"
if state.get("status") == "failed": return "replan"
if state.get("replans", 0) >= 2 or state.get("tokens", 0) > MAX_TOKENS * 0.8:
    return "escalate"
return "done"
