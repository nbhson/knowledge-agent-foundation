LEVELS = ["irrelevant", "weak", "relevant", "core"]
FLOOR  = "weak"
kept = [c for c in ranked if LEVELS.index(c["selected"]) > LEVELS.index(FLOOR)]
kept.sort(key=lambda c: c["weighted_score"], reverse=True)
