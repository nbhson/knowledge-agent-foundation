import networkx as nx

G = nx.karate_club_graph()  # Sample graph, 34 nodes

# Degree
degrees = dict(G.degree())
print(f"Avg degree: {sum(degrees.values())/len(degrees):.1f}")

# Centrality
betweenness = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G)
print(f"Top betweenness: {sorted(betweenness, key=betweenness.get, reverse=True)[:3]}")
print(f"Top PageRank: {sorted(pagerank, key=pagerank.get, reverse=True)[:3]}")

# Clustering
clustering = nx.average_clustering(G)
print(f"Average clustering: {clustering:.3f}")

# Path
print(f"Diameter: {nx.diameter(G)}")
print(f"Avg shortest path: {nx.average_shortest_path_length(G):.2f}")

# Community (modularity)
import community as community_louvain  # python-louvain
partition = community_louvain.best_partition(G)
modularity = community_louvain.modularity(partition, G)
print(f"Modularity: {modularity:.3f}, Communities: {len(set(partition.values()))}")
