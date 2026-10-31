import networkx as nx
from typing import Dict, List

def evaluate_graph_quality(graph: nx.Graph, ontology=None) -> Dict:
    """Đo chất lượng graph."""
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    
    # Connectivity
    if isinstance(graph, nx.DiGraph):
        is_connected = nx.is_weakly_connected(graph) if n_nodes > 0 else True
        components = list(nx.weakly_connected_components(graph))
    else:
        is_connected = nx.is_connected(graph) if n_nodes > 0 else True
        components = list(nx.connected_components(graph))
    
    largest_component_size = max(len(c) for c in components) if components else 0
    connectivity = largest_component_size / n_nodes if n_nodes > 0 else 0
    
    # Isolated nodes
    isolated = list(nx.isolates(graph))
    isolated_rate = len(isolated) / n_nodes if n_nodes > 0 else 0
    
    # Density & avg degree
    density = nx.density(graph)
    avg_degree = sum(dict(graph.degree()).values()) / n_nodes if n_nodes > 0 else 0
    
    # Invalid edges (nếu có ontology)
    invalid_edges = 0
    if ontology:
        for u, v, data in graph.edges(data=True):
            edge_type = data.get("type", "")
            from_type = graph.nodes[u].get("type", "")
            to_type = graph.nodes[v].get("type", "")
            ok, _ = ontology.validate_edge(edge_type, from_type, to_type)
            if not ok:
                invalid_edges += 1
    invalid_rate = invalid_edges / n_edges if n_edges > 0 else 0
    
    return {
        "nodes": n_nodes,
        "edges": n_edges,
        "density": round(density, 4),
        "avg_degree": round(avg_degree, 2),
        "connectivity": round(connectivity, 3),
        "is_connected": is_connected,
        "num_components": len(components),
        "isolated_nodes": len(isolated),
        "isolated_rate": round(isolated_rate, 3),
        "invalid_edges": invalid_edges,
        "invalid_rate": round(invalid_rate, 3),
    }

# Usage
G = nx.karate_club_graph()
G_labeled = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
for n in G_labeled.nodes():
    G_labeled.nodes[n]["type"] = "Person"

metrics = evaluate_graph_quality(G_labeled)
print(metrics)
# {'nodes': 34, 'edges': 78, 'density': 0.139, 'avg_degree': 4.59, 
#  'connectivity': 1.0, 'isolated_rate': 0.0, ...}
