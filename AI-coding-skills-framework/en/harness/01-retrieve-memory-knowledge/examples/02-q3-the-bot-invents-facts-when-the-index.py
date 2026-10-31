TOP_SCORE_FLOOR, TOP_K = 0.25, 5
hits = vector_search(q_emb, tenant_id)
top = max([h["score"] for h in hits], default=0.0)
if not hits or top < TOP_SCORE_FLOOR:
    hits = bm25_search(q, tenant_id)          # one retry, keyword only
if not hits:
    return {"answer": None, "abstain": True, "reason": "no grounding found"}
