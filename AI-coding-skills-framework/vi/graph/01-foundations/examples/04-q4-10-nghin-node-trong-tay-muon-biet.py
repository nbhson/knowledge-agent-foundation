G = nx.karate_club_graph()          # 34 node mẫu
print(nx.average_clustering(G))     # bạn bè có quen nhau không
b = nx.betweenness_centrality(G)
print(max(b, key=b.get))            # cầu nối
print(nx.diameter(G), nx.average_shortest_path_length(G))
