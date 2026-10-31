import numpy as np

def rrf_score(ranked_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fuse several ranked lists → RRF score, no score normalization needed."""
    fused: dict[str, float] = {}
    for lst in ranked_lists:
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))

# vector_rank, graph_rank, fulltext_rank = ...  (3 top-k lists)
# final = rrf_score([vector_rank, graph_rank, fulltext_rank])
