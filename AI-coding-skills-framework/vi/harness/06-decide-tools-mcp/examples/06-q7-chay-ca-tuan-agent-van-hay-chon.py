rate = s["success_count"] / s["total_count"]
penalty = min(s["avg_latency"] / 1000, 1)
score = rate * (1 - penalty) if s["total_count"] else 0.5
