import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("Alice", "Bob"), ("Alice", "Carol"), ("Alice", "Dave"),
    ("Bob", "Phoenix"), ("Carol", "Phoenix"), ("Dave", "Atlas"),
    ("Phoenix", "Atlas"),
])

# Degree centrality: who has the most connections
deg = nx.degree_centrality(G)
print(f"Degree: {sorted(deg.items(), key=lambda x: x[1], reverse=True)}")

# Betweenness: who is the bottleneck (sits on many shortest paths)
bet = nx.betweenness_centrality(G)
print(f"Betweenness: {sorted(bet.items(), key=lambda x: x[1], reverse=True)}")
# A node with high betweenness = removing it splits the graph

# PageRank: who is "voted for" by important nodes
pr = nx.pagerank(G)
print(f"PageRank: {sorted(pr.items(), key=lambda x: x[1], reverse=True)}")

# Closeness: who is closest to everyone (lowest average path length)
try:
    close = nx.closeness_centrality(G)
    print(f"Closeness: {sorted(close.items(), key=lambda x: x[1], reverse=True)}")
except:
    pass

# Application: "Who is the approval bottleneck?"
# → The Person with high betweenness in the approval subgraph
