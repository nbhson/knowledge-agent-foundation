docs = vector_store.search(query, top_k=10)   # not 100
remaining = budget.available; parts = []
for doc in docs:
    t = estimate_tokens(doc)
    if t < remaining:
        parts.append(doc); remaining -= t
print(budget.report())   # retrieved_context 62,000 (50%)
