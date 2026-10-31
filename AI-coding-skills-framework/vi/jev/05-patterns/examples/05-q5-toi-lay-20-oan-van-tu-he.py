def rerank(query, passages, min_score=1.5):
    scored = [dict(score_candidate(query, p), passage=p) for p in passages]
    scored.sort(key=lambda r: r["score"], reverse=True)
    return [r for r in scored if r["score"] >= min_score]
