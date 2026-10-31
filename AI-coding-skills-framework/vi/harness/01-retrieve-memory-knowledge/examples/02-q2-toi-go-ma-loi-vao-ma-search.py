def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for lst in rankings:
        for rank, doc_id in enumerate(lst, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)
