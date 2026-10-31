import chromadb

client = chromadb.PersistentClient(path="./memory")   # harness/03 memory store
collection = client.get_or_create_collection("project_memory")

# Lưu memory (upsert — harness/03)
collection.upsert(
    ids=["doc-1"],
    documents=["BHYT cho người lao động: mức đóng 4.5% từ 2026"],
    metadatas=[{"topic": "insurance", "tier": "warm"}]   # Tier 2 Warm Memory
)

# Retrieve (harness/01) — semantic search
results = collection.query(
    query_texts=["chế độ bảo hiểm lao động"],
    n_results=3  # top-k → harness/02 build context
)
