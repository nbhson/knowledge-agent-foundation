try:
    partition = community_louvain.best_partition(graph, resolution=1.0)  # Louvain
except ImportError:
    raise RuntimeError("python-louvain missing — greedy fallback is NOT Leiden")
