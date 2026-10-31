results = constrained_bfs(G, "Alice", max_hops=3,
                          allowed_edge_types={"MANAGES", "WORKS_ON"},
                          min_confidence=0.7)
# Dave is excluded twice: KNOWS not allowed, and 0.60 < 0.7
