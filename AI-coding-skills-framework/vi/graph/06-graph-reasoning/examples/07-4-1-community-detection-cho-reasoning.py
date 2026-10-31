import networkx as nx

G = nx.karate_club_graph()

# Louvain (nhanh, tốt cho medium graphs)
import community as community_louvain
partition = community_louvain.best_partition(G)
print(f"Communities: {len(set(partition.values()))}")

# Label Propagation (nhanh nhất, cho large graphs)
communities_lpa = list(nx.algorithms.community.label_propagation_communities(G))
print(f"LPA communities: {len(communities_lpa)}")

# Dùng community để reasoning:
# "Alice và Bob có cùng community không? → họ có làm cùng domain không?"
def same_community(node_a: str, node_b: str, partition: dict) -> bool:
    return partition.get(node_a) == partition.get(node_b)
