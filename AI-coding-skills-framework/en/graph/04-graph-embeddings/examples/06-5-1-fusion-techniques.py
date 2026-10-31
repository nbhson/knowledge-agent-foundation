import numpy as np
from typing import List, Dict

def reciprocal_rank_fusion(
    ranked_lists: List[List[str]],
    k: int = 60,
) -> Dict[str, float]:
    """RRF: merge several ranked lists into one score."""
    scores: Dict[str, float] = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return scores

def hybrid_search(
    query_text: str,
    query_vector: List[float],
    text_index,       # Vector DB for text embeddings
    graph_embeddings: Dict[str, np.ndarray],
    top_k: int = 10,
    alpha: float = 0.6,  # weight for text search
) -> List[Dict]:
    """
    Hybrid: α * text_score + (1-α) * graph_score
    
    alpha=1.0 → text search only
    alpha=0.0 → graph search only
    alpha=0.6 → balanced (recommended)
    """
    # 1. Text search (semantic)
    text_results = text_index.search(query_vector, top_k=top_k * 2)
    # text_results = [{"id": "doc_1", "score": 0.92}, ...]
    
    # 2. Graph search (structural)
    query_graph_vec = embed(query_text)  # or the query entity embedding
    graph_scores = []
    for node_id, node_vec in graph_embeddings.items():
        sim = float(np.dot(query_graph_vec, node_vec) / 
                    (np.linalg.norm(query_graph_vec) * np.linalg.norm(node_vec)))
        graph_scores.append((node_id, sim))
    graph_scores.sort(key=lambda x: x[1], reverse=True)
    graph_ranked = [node_id for node_id, _ in graph_scores[:top_k * 2]]
    
    # 3a. Fusion by Weighted Score
    text_score_map = {r["id"]: r["score"] for r in text_results}
    graph_score_map = {node_id: score for node_id, score in graph_scores}
    
    all_ids = set(text_score_map.keys()) | set(graph_score_map.keys())
    hybrid_scores = {}
    for doc_id in all_ids:
        t_score = text_score_map.get(doc_id, 0)
        g_score = graph_score_map.get(doc_id, 0)
        hybrid_scores[doc_id] = alpha * t_score + (1 - alpha) * g_score
    
    ranked = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    return [{"id": doc_id, "score": score} for doc_id, score in ranked[:top_k]]

# 3b. Fusion by RRF (no need to tune alpha)
def hybrid_search_rrf(text_ranked: List[str], graph_ranked: List[str], top_k: int = 10):
    fused = reciprocal_rank_fusion([text_ranked, graph_ranked])
    ranked = sorted(fused.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]
