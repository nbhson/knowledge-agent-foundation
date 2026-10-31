# Pseudocode: GraphSAGE forward
def graphsage_layer(node_features, adjacency, weights, aggregator="mean"):
    """
    node_features: (N, D) — features của N nodes
    adjacency: (N, N) — adjacency matrix
    """
    # Aggregate neighbors
    if aggregator == "mean":
        neighbor_agg = adjacency @ node_features / adjacency.sum(axis=1, keepdims=True)
    
    # Concat self + neighbors
    combined = np.concatenate([node_features, neighbor_agg], axis=1)
    
    # Transform
    output = np.maximum(0, combined @ weights)  # ReLU
    # Normalize
    output = output / np.linalg.norm(output, axis=1, keepdims=True)
    return output
