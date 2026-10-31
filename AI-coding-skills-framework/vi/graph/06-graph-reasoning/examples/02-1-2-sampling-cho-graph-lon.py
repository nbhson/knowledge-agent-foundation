import random

def sampled_traversal(
    graph: nx.Graph,
    start: str,
    max_hops: int = 2,
    max_neighbors_per_hop: int = 10,
    sample_strategy: str = "random",  # random | top-confidence | pagerank
) -> List[dict]:
    """Sample traversal — giới hạn số neighbors mỗi hop."""
    visited = set([start])
    current_level = [start]
    all_results = []
    
    for hop in range(max_hops):
        next_level = []
        for node in current_level:
            neighbors = list(graph.neighbors(node))
            
            # Sample nếu quá nhiều neighbors
            if len(neighbors) > max_neighbors_per_hop:
                if sample_strategy == "random":
                    neighbors = random.sample(neighbors, max_neighbors_per_hop)
                elif sample_strategy == "top-confidence":
                    neighbors.sort(key=lambda n: graph.get_edge_data(node, n).get("confidence", 0), reverse=True)
                    neighbors = neighbors[:max_neighbors_per_hop]
            
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    next_level.append(nb)
                    all_results.append({"node": nb, "hops": hop + 1, "via": node})
        
        current_level = next_level
        if not current_level:
            break
    
    return all_results
