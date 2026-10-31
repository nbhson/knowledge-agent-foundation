if score["total_count"] < 5:
    final_score = 0.1                       # unknown, not competitive
else:
    final_score = success_rate * (1 - min(score["avg_latency"] / 1000, 1))
