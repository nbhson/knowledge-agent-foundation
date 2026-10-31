# Complete hybrid search demo
import requests
import numpy as np
from collections import Counter
import math

OLLAMA_URL = "http://localhost:11434"

# --- Documents ---
documents = [
    "BHYT (Bảo hiểm y tế) là hình thức bảo hiểm bắt buộc tại Việt Nam.",
    "Mức đóng BHYT cho người lao động là 4.5% mức lương cơ sở.",
    "Người có thẻ BHYT được khám chữa bệnh tại các cơ sở y tế.",
    "BHYT chi trả từ 80% đến 100% chi phí tùy tuyến.",
    "Thẻ BHYT có hiệu lực trong 5 năm kể từ ngày cấp.",
    "Đăng ký BHYT tại cơ quan bảo hiểm xã hội.",
    "BHYT tự nguyện dành cho người không thuộc diện bắt buộc.",
]

# --- Semantic Search ---
def get_embedding(text):
    response = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]

def semantic_search(query, docs, top_k=3):
    query_emb = get_embedding(query)
    doc_embs = [get_embedding(doc) for doc in docs]
    
    scores = []
    for i, doc_emb in enumerate(doc_embs):
        score = np.dot(query_emb, doc_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
        )
        scores.append((i, score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return [(docs[i], score) for i, score in scores[:top_k]]

# --- BM25 Search ---
class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
    
    def fit(self, docs):
        self.docs = docs
        self.n = len(docs)
        self.doc_freqs = {}
        self.doc_lens = []
        
        for doc in docs:
            terms = doc.lower().split()
            self.doc_lens.append(len(terms))
            for term in set(terms):
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
        
        self.avgdl = sum(self.doc_lens) / self.n
    
    def search(self, query, top_k=3):
        query_terms = query.lower().split()
        scores = []
        
        for i, doc in enumerate(self.docs):
            terms = doc.lower().split()
            tf = Counter(terms)
            score = 0
            
            for term in query_terms:
                if term in tf:
                    idf = math.log(
                        (self.n - self.doc_freqs.get(term, 0) + 0.5) /
                        (self.doc_freqs.get(term, 0) + 0.5) + 1
                    )
                    f = tf[term]
                    numerator = f * (self.k1 + 1)
                    denominator = f + self.k1 * (
                        1 - self.b + self.b * self.doc_lens[i] / self.avgdl
                    )
                    score += idf * numerator / denominator
            
            scores.append((i, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(self.docs[i], score) for i, score in scores[:top_k]]

# --- Hybrid Search ---
def rrf_fusion(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking, 1):
            if doc not in scores:
                scores[doc] = 0
            scores[doc] += 1 / (k + rank)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

# --- Run Demo ---
query = "BHYT đóng bao nhiêu tiền?"

print("=== Semantic Search ===")
for doc, score in semantic_search(query, documents):
    print(f"  {score:.4f} | {doc[:60]}...")

print("\n=== BM25 Search ===")
bm25 = BM25()
bm25.fit(documents)
for doc, score in bm25.search(query):
    print(f"  {score:.4f} | {doc[:60]}...")

print("\n=== Hybrid Search (RRF) ===")
semantic_results = [doc for doc, _ in semantic_search(query, documents, 5)]
bm25_results = [doc for doc, _ in bm25.search(query, 5)]

hybrid = rrf_fusion([semantic_results, bm25_results])
for i, doc in enumerate(hybrid[:3]):
    print(f"  #{i+1} | {doc[:60]}...")
