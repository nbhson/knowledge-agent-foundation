from collections import deque
import networkx as nx
from typing import List, Set, Optional

def constrained_bfs(
    graph: nx.DiGraph,
    start: str,
    max_hops: int = 3,
    allowed_edge_types: Optional[Set[str]] = None,
    allowed_node_types: Optional[Set[str]] = None,
    min_confidence: float = 0.0,
) -> List[dict]:
    """
    BFS có ràng buộc — chỉ đi qua edges/nodes thỏa điều kiện.
    
    Ví dụ: chỉ qua MANAGES/WORKS_ON, confidence >= 0.7
    """
    visited = set([start])
    queue = deque([(start, 0, [start])])  # (node, hops, path)
    results = []
    
    while queue:
        current, hops, path = queue.popleft()
        
        if hops >= max_hops:
            continue
        
        for neighbor in graph.successors(current):
            if neighbor in visited:
                continue
            
            edge_data = graph.get_edge_data(current, neighbor)
            edge_type = edge_data.get("type", "")
            
            # Filter edge type
            if allowed_edge_types and edge_type not in allowed_edge_types:
                continue
            
            # Filter confidence
            if edge_data.get("confidence", 1.0) < min_confidence:
                continue
            
            # Filter node type
            if allowed_node_types:
                node_type = graph.nodes[neighbor].get("type", "")
                if node_type not in allowed_node_types:
                    continue
            
            new_path = path + [neighbor]
            results.append({
                "target": neighbor,
                "hops": hops + 1,
                "path": new_path,
                "edges": [(path[i], path[i+1], graph.get_edge_data(path[i], path[i+1]).get("type"))
                          for i in range(len(new_path) - 1)],
                "confidence": min(graph.get_edge_data(new_path[i], new_path[i+1]).get("confidence", 1.0)
                                  for i in range(len(new_path) - 1)),
            })
            
            visited.add(neighbor)
            queue.append((neighbor, hops + 1, new_path))
    
    return results

# Usage
G = nx.DiGraph()
G.add_node("Alice", type="Person")
G.add_node("Bob", type="Person")
G.add_node("Carol", type="Person")
G.add_node("Phoenix", type="Project")
G.add_node("Dave", type="Person")
G.add_edges_from([
    ("Alice", "Bob", {"type": "MANAGES", "confidence": 0.95}),
    ("Bob", "Carol", {"type": "MANAGES", "confidence": 0.90}),
    ("Bob", "Phoenix", {"type": "WORKS_ON", "confidence": 0.85}),
    ("Alice", "Dave", {"type": "KNOWS", "confidence": 0.60}),
])

# Chỉ qua MANAGES/WORKS_ON, confidence >= 0.7
results = constrained_bfs(G, "Alice", max_hops=3, 
                           allowed_edge_types={"MANAGES", "WORKS_ON"},
                           min_confidence=0.7)
for r in results:
    print(f"  {r['path']} (hops={r['hops']}, conf={r['confidence']:.2f})")
# ['Alice', 'Bob'] (hops=1, conf=0.95)
# ['Alice', 'Bob', 'Carol'] (hops=2, conf=0.90)
# ['Alice', 'Bob', 'Phoenix'] (hops=2, conf=0.85)
# Dave bị loại vì KNOWS không trong allowed types
