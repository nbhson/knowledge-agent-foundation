results = constrained_bfs(G, "Alice", max_hops=3,
    allowed_edge_types={"MANAGES", "WORKS_ON"}, min_confidence=0.7)
# ['Alice','Bob','Carol'] (hops=2, conf=0.90)
# ['Alice','Bob','Phoenix'] (hops=2, conf=0.85)
# Dave bị loại: KNOWS không nằm trong allowed types
