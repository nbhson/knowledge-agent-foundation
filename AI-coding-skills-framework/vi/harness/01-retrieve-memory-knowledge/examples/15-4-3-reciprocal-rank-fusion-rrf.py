def reciprocal_rank_fusion(rankings, k=60):
    """
    Combine multiple ranked lists using RRF
    
    RRF_score(d) = Σ 1/(k + rank_i(d))
    
    k: constant (default 60, used by many implementations)
    
    Advantages:
    - Simple to implement
    - No need to normalize scores across different methods
    - Robust to outlier scores
    """
    scores = {}
    
    for ranking_list in rankings:
        for rank, doc_id in enumerate(ranking_list, start=1):
            if doc_id not in scores:
                scores[doc_id] = 0
            scores[doc_id] += 1 / (k + rank)
    
    # Sort by RRF score descending
    sorted_docs = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return sorted_docs


# Example with detailed calculation
semantic_ranking = ["doc_A", "doc_B", "doc_C", "doc_D", "doc_E"]
keyword_ranking = ["doc_B", "doc_D", "doc_A", "doc_F", "doc_C"]
metadata_ranking = ["doc_A", "doc_C", "doc_E", "doc_B", "doc_D"]

merged = reciprocal_rank_fusion(
    [semantic_ranking, keyword_ranking, metadata_ranking], k=60
)

# Score calculation for doc_A:
# semantic: 1/(60+1) = 0.01639
# keyword:  1/(60+3) = 0.01587
# metadata: 1/(60+1) = 0.01639
# Total:    0.04866
