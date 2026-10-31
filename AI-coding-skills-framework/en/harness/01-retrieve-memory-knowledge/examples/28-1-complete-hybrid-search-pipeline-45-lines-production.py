import requests
import numpy as np
from rank_bm25 import BM25Okapi

OLLAMA = "http://localhost:11434"
TOP_K = 20
RERANK_TOP = 5

def embed(texts):
    """Embed via Ollama nomic-embed-text."""
    res = requests.post(f"{OLLAMA}/api/embed", json={
        "model": "nomic-embed-text",
        "input": texts if isinstance(texts, list) else [texts]
    })
    return res.json()["embeddings"]

def bm25_search(query, chunks, tokenizer):
    """BM25 keyword search."""
    tokenized_corpus = [tokenizer(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(tokenizer(query))
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [(idx, score) for idx, score in ranked[:TOP_K]]

def vector_search(query, chunks):
    """Semantic search via vector similarity."""
    q_emb = embed(query)[0]
    results = []
    for i, c in enumerate(chunks):
        v_emb = embed(c["text"])[0]
        sim = np.dot(q_emb, v_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(v_emb))
        results.append((i, sim))
    return sorted(results, key=lambda x: x[1], reverse=True)[:TOP_K]

def rrf_fusion(bm25_results, vec_results, k=60):
    """Reciprocal Rank Fusion."""
    fused = {}
    for rank, (idx, _) in enumerate(bm25_results):
        fused[idx] = fused.get(idx, 0) + 1 / (k + rank + 1)
    for rank, (idx, _) in enumerate(vec_results):
        fused[idx] = fused.get(idx, 0) + 1 / (k + rank + 1)
    return sorted(fused.items(), key=lambda x: x[1], reverse=True)

def rerank_crossencoder(query, chunks, indices):
    """Cross-encoder rerank (simulated — replace with sentence-transformers in production)."""
    results = []
    for idx in indices:
        c = chunks[idx]
        # Simulated cross-encoder score; use CrossEncoder("cross-encoder/ms-marco-MiniLML-6-v2") in production
        score = len([w for w in query.lower().split() if w in c["text"].lower()]) / max(len(query.split()), 1)
        results.append((idx, score))
    return sorted(results, key=lambda x: x[1], reverse=True)[:RERANK_TOP]

def hybrid_search(query, chunks):
    """Complete hybrid pipeline."""
    tokenizer = lambda t: t.lower().split()
    bm25_scores = bm25_search(query, chunks, tokenizer)
    vec_scores = vector_search(query, chunks)
    fused = rrf_fusion(bm25_scores, vec_scores)
    indices = [idx for idx, _ in fused]
    reranked = rerank_crossencoder(query, chunks, indices)
    return [chunks[idx] for idx, _ in reranked]

# Usage
chunks = [{"text": "BHYT là bảo hiểm y tế bắt buộc"}, {"text": "Mức đóng BHYT là 4.5%"}]
results = hybrid_search("mức đóng BHYT", chunks)
print([r["text"] for r in results])
