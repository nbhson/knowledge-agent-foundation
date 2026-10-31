questions = {
    "queue":    {"type": "choice", "options": ["billing","infra","product","data"]},
    "priority": {"type": "score",  "levels": ["p0","p1","p2","p3"]},
}
band = "auto" if res["queue"]["confidence"] >= 0.7 else "human_review"
