import time

# Create a large graph with 10K nodes
G_large = nx.erdos_renyi_graph(10000, 0.001)

start = time.time()
path = nx.shortest_path(G_large, source=0, target=100)
print(f"Shortest path length: {len(path)}, time: {(time.time()-start)*1000:.1f}ms")

start = time.time()
centrality = nx.degree_centrality(G_large)
print(f"Degree centrality time: {(time.time()-start)*1000:.1f}ms")
