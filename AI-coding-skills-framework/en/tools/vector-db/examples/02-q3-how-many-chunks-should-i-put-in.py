results = collection.query(
    query_texts=["worker insurance benefits"],
    n_results=5,                       # top-k into harness/02 build context
    where={"topic": "insurance"},
)
