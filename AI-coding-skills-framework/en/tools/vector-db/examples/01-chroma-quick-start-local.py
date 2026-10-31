import chromadb

client = chromadb.PersistentClient(path="./memory")   # harness/03 memory store
collection = client.get_or_create_collection("project_memory")

# Save memory (upsert — harness/03)
collection.upsert(
    ids=["doc-1"],
    documents=["Health insurance for workers: 4.5% contribution rate from 2026"],
    metadatas=[{"topic": "insurance", "tier": "warm"}]   # Tier 2 Warm Memory
)

# Retrieve (harness/01) — semantic search
results = collection.query(
    query_texts=["worker insurance benefits"],
    n_results=3  # top-k → harness/02 build context
)
