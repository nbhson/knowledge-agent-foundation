collection.upsert(
    ids=["doc-1"],
    documents=["Health insurance for workers: 4.5% contribution rate"],
    metadatas=[{"topic": "insurance", "tier": "warm"}],
)
results = collection.query(query_texts=["worker insurance"], n_results=3)
