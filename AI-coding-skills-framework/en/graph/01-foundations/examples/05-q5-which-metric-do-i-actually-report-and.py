G = nx.karate_club_graph()          # 34 nodes — the standard smoke test
nx.average_clustering(G)            # ≈0.57 -> are friends also friends?
nx.diameter(G)                      # 5     -> set max_hops from this
top = sorted(nx.betweenness_centrality(G).items(),
             key=lambda kv: -kv[1])[:3]
