import numpy as np

def rrf_score(ranked_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    """Fuse nhiều danh sách rank → điểm RRF, không cần score chuẩn."""
    fused: dict[str, float] = {}
    for lst in ranked_lists:
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))

# vector_rank, graph_rank, fulltext_rank = ...  (3 danh sách top-k)
# final = rrf_score([vector_rank, graph_rank, fulltext_rank])
