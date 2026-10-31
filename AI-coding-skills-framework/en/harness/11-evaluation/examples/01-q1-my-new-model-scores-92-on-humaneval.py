summary = suite.run(agent_func)
print(summary["success_rate"], summary["avg_tokens"], summary["avg_attempts"])
# 0.45  21500  2.4   <- resolve rate, tokens, attempts
