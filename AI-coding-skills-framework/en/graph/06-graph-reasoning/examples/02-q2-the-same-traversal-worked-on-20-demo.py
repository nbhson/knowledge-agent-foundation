results = sampled_traversal(G, start="Alice", max_hops=2,
                            max_neighbors_per_hop=10,
                            sample_strategy="top-confidence")
