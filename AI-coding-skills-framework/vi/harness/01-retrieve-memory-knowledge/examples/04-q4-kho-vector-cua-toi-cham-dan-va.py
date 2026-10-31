CURRENT = "nomic-embed-text:v2"
if not hits or top < 0.25:
    hits = bm25_search(q, tenant_id); fallback = "bm25-only-retry"
if not hits:
    return {"answer": None, "abstain": True, "reason": "no grounding found"}
