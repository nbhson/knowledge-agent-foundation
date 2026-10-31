import networkx as nx

G = nx.karate_club_graph()

# Louvain (fast, good for medium graphs)
import community as community_louvain
partition = community_louvain.best_partition(G)
print(f"Communities: {len(set(partition.values()))}")

# Label Propagation (fastest, for large graphs)
communities_lpa = list(nx.algorithms.community.label_propagation_communities(G))
print(f"LPA communities: {len(communities_lpa)}")

# Use communities to reason:
# "Are Alice and Bob in the same community? → do they work in the same domain?"
def same_community(node_a: str, node_b: str, partition: dict) -> bool:
    return partition.get(node_a) == partition.get(node_b)
