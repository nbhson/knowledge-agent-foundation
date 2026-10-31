import networkx as nx

# Tạo weighted graph
G = nx.DiGraph()
G.add_weighted_edges_from([
    ("Alice", "Bob", 1.0),      # MANAGES, weight = 1/confidence
    ("Bob", "Carol", 1.2),
    ("Alice", "Dave", 3.0),     # KNOWS, weight cao (ít tin cậy)
    ("Dave", "Carol", 1.5),
    ("Bob", "Phoenix", 1.0),
    ("Carol", "Atlas", 1.0),
])

# 1. Shortest path (unweighted — ít hops nhất)
path = nx.shortest_path(G, source="Alice", target="Carol")
print(f"Shortest (hops): {path}")  # ['Alice', 'Bob', 'Carol']

# 2. Weighted shortest (Dijkstra — tổng weight nhỏ nhất)
path_w = nx.dijkstra_path(G, source="Alice", target="Carol", weight="weight")
print(f"Weighted shortest: {path_w}")  # Có thể khác nếu weight khác

# 3. All simple paths (giới hạn hops)
all_paths = list(nx.all_simple_paths(G, source="Alice", target="Carol", cutoff=4))
print(f"All paths (≤4 hops): {all_paths}")

# 4. K-shortest paths
k_paths = list(nx.shortest_simple_paths(G, source="Alice", target="Carol", weight="weight"))
print(f"Top-3 shortest: {list(k_paths)[:3]}")

# 5. Path với bằng chứng (edges + confidence)
def path_with_evidence(graph, source, target, weight="weight"):
    path = nx.dijkstra_path(graph, source, target, weight=weight)
    evidence = []
    total_confidence = 1.0
    for i in range(len(path) - 1):
        edata = graph.get_edge_data(path[i], path[i+1])
        evidence.append({
            "from": path[i], "to": path[i+1],
            "type": edata.get("type", "RELATED"),
            "weight": edata.get("weight", 1.0),
        })
        # Confidence = 1/weight (nếu weight = 1/confidence)
        total_confidence *= (1.0 / edata.get("weight", 1.0))
    return {"path": path, "evidence": evidence, "total_confidence": total_confidence}

print(path_with_evidence(G, "Alice", "Atlas"))
