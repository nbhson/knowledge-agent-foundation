import networkx as nx

# Nhanh nhất để prototype — không cần install DB
G = nx.DiGraph()

# Add nodes
G.add_node("Alice", label="Person", role="CTO")
G.add_node("Phoenix", label="Project", budget=500000)

# Add edges
G.add_edge("Alice", "Phoenix", type="WORKS_ON", confidence=0.9)

# Query: BFS traversal
from collections import deque

def bfs_traversal(graph, start: str, max_hops: int = 2) -> list:
    visited = set([start])
    queue = deque([(start, 0)])
    result = []
    while queue:
        node, hops = queue.popleft()
        if hops >= max_hops:
            continue
        for neighbor in graph.successors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                result.append((node, neighbor, graph[node][neighbor]))
                queue.append((neighbor, hops + 1))
    return result

print(bfs_traversal(G, "Alice", max_hops=2))
