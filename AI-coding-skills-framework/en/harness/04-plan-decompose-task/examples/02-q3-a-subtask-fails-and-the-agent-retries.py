if state.get("replans", 0) >= MAX_REPLAN: return "escalate"
if state.get("transient") and state.get("attempts", 0) < MAX_RETRY: return "retry"
if state.get("status") == "failed": return "replan"
