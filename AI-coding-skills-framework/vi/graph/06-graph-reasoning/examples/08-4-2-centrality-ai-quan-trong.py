import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("Alice", "Bob"), ("Alice", "Carol"), ("Alice", "Dave"),
    ("Bob", "Phoenix"), ("Carol", "Phoenix"), ("Dave", "Atlas"),
    ("Phoenix", "Atlas"),
])

# Degree centrality: ai có nhiều kết nối nhất
deg = nx.degree_centrality(G)
print(f"Degree: {sorted(deg.items(), key=lambda x: x[1], reverse=True)}")

# Betweenness: ai là bottleneck (nằm trên nhiều shortest paths)
bet = nx.betweenness_centrality(G)
print(f"Betweenness: {sorted(bet.items(), key=lambda x: x[1], reverse=True)}")
# Node có betweenness cao = nếu remove, graph bị chia cắt

# PageRank: ai được "vote" bởi nodes quan trọng
pr = nx.pagerank(G)
print(f"PageRank: {sorted(pr.items(), key=lambda x: x[1], reverse=True)}")

# Closeness: ai gần mọi người nhất (trung bình path ngắn)
try:
    close = nx.closeness_centrality(G)
    print(f"Closeness: {sorted(close.items(), key=lambda x: x[1], reverse=True)}")
except:
    pass

# Ứng dụng: "Ai là approver bottleneck?"
# → Person có betweenness cao trong approval subgraph
