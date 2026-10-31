def graphsage_layer(x, adjacency, weights, aggregator="mean"):
    neighbor_agg = adjacency @ x / adjacency.sum(axis=1, keepdims=True)  # mean of friends
    combined = np.concatenate([x, neighbor_agg], axis=1)  # "me" + "my friends"
    output = np.maximum(0, combined @ weights)             # one ReLU layer
    return output / np.linalg.norm(output, axis=1, keepdims=True)
