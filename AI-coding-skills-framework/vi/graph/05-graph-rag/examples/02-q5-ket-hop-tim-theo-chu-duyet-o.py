def rrf_score(lists, k=60):
    fused = {}
    for lst in lists:                     # vector_rank, graph_rank, fulltext_rank
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))
