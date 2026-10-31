paths = list(nx.all_simple_paths(G, source="Bob", target="Atlas", cutoff=4))
evidence = [(p[i], p[i+1], G.get_edge_data(p[i], p[i+1])["type"])
            for p in paths for i in range(len(p) - 1)]
