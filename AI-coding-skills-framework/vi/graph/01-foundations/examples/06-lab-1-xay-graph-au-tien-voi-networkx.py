import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node("Alice", type="Person", role="CTO")
G.add_node("Bob", type="Person", role="Engineer")
G.add_node("Phoenix", type="Project", budget=500000)
G.add_edges_from([
    ("Alice", "Bob", {"type": "MANAGES"}),
    ("Bob", "Phoenix", {"type": "WORKS_ON"}),
])

print(f"Nodes: {list(G.nodes(data=True))}")
print(f"Edges: {list(G.edges(data=True))}")
print(f"Is DAG? {nx.is_directed_acyclic_graph(G)}")

# Vẽ
nx.draw(G, with_labels=True, node_color="lightblue", arrows=True)
plt.show()
