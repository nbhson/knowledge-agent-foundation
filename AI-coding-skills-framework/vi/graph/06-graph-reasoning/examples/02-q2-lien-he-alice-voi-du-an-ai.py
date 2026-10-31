path = nx.dijkstra_path(G, source="Alice", target="Carol", weight="weight")
all_p = list(nx.all_simple_paths(G, "Alice", "Carol", cutoff=4))
k_p = list(nx.shortest_simple_paths(G, "Alice", "Carol", weight="weight"))
