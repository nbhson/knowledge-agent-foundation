MAX_DEPTH, MAX_FANOUT, MAX_TOKENS = 4, 5, 100_000
if state.get("tokens", 0) > MAX_TOKENS * 0.8: return "escalate"
