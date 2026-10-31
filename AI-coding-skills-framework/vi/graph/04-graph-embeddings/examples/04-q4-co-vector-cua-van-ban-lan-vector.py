# RRF — không cần chuẩn hoá điểm, k = 60
fused = {}
for lst in [vector_rank, graph_rank, fulltext_rank]:
    for rank, item in enumerate(lst, start=1):
        fused[item] = fused.get(item, 0.0) + 1.0 / (60 + rank)
final = sorted(fused.items(), key=lambda x: -x[1])[:10]
