import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
LEVELS = ["irrelevant", "weak", "relevant", "core"]
FLOOR = "weak"   # drop everything at or below this level


def rerank_shortlist(query: str, candidates: list[dict]) -> list[dict]:
    """Score each candidate in one batch of parallel questions, then sort."""
    questions = {
        f"rel_{i}": {"type": "score", "levels": LEVELS}
        for i in range(len(candidates))
    }
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "jev-latest",
              "state": {"query": query, "candidates": candidates},
              "questions": questions},
        timeout=10.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    ranked = []
    for i, cand in enumerate(candidates):
        s = res[f"rel_{i}"]
        ranked.append({
            "candidate": cand,
            # probability-weighted score — may fall BETWEEN levels
            "weighted_score": s.get("score", 0),
            "selected": s["selected"],
            "confidence": s["confidence"],
            "distribution": s.get("probabilities", {}),
        })

    # filter below floor, then rank by weighted score descending
    kept = [c for c in ranked
            if LEVELS.index(c["selected"]) > LEVELS.index(FLOOR)]
    kept.sort(key=lambda c: c["weighted_score"], reverse=True)
    return kept
