def compare_retrieval(queries: List[Dict], vanilla_results: List[List[str]], 
                       graphrag_results: List[List[str]]) -> Dict:
    """
    Compare retrieval quality between vanilla RAG and GraphRAG.
    
    queries: [{"query": "...", "relevant": ["doc_1", ...]}, ...]
    """
    vanilla_p, vanilla_r, graphrag_p, graphrag_r = [], [], [], []
    
    for q, v_ret, g_ret in zip(queries, vanilla_results, graphrag_results):
        relevant = q["relevant"]
        vanilla_p.append(precision_at_k(v_ret, relevant, 5))
        vanilla_r.append(recall_at_k(v_ret, relevant, 5))
        graphrag_p.append(precision_at_k(g_ret, relevant, 5))
        graphrag_r.append(recall_at_k(g_ret, relevant, 5))
    
    import numpy as np
    return {
        "vanilla": {"P@5": round(float(np.mean(vanilla_p)), 3), "R@5": round(float(np.mean(vanilla_r)), 3)},
        "graphrag": {"P@5": round(float(np.mean(graphrag_p)), 3), "R@5": round(float(np.mean(graphrag_r)), 3)},
        "delta": {"P@5": round(float(np.mean(graphrag_p) - np.mean(vanilla_p)), 3),
                  "R@5": round(float(np.mean(graphrag_r) - np.mean(vanilla_r)), 3)},
    }
