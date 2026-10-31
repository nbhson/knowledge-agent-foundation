hybrid[doc] = alpha * text_score.get(doc, 0) + (1 - alpha) * graph_score.get(doc, 0)
fused[doc]  = sum(1 / (60 + rank + 1) for lst in ranked_lists for rank, doc in enumerate(lst))
