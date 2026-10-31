import networkx as nx

def detect_communities(graph: nx.Graph, resolution: float = 1.0) -> dict:
    """
    Leiden-style community detection.
    
    resolution: điều khiển granularity
      - thấp (0.5) → ít community lớn
      - cao (2.0) → nhiều community nhỏ
    """
    try:
        import community as community_louvain  # python-louvain (Louvain)
        partition = community_louvain.best_partition(graph, resolution=resolution)
    except ImportError:
        # Fallback: greedy modularity
        from networkx.algorithms.community import greedy_modularity_communities
        comms = list(greedy_modularity_communities(graph))
        partition = {}
        for cid, comm in enumerate(comms):
            for node in comm:
                partition[node] = cid
    
    # Nhóm nodes theo community
    communities = {}
    for node, cid in partition.items():
        communities.setdefault(cid, []).append(node)
    
    print(f"Detected {len(communities)} communities")
    for cid, members in communities.items():
        print(f"  Community {cid}: {len(members)} nodes — {members[:5]}...")
    
    return communities

# Usage
G = nx.karate_club_graph()
G_labeled = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
communities = detect_communities(G_labeled)
