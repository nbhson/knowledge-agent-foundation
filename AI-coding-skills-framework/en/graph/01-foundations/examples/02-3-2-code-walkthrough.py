import networkx as nx
import numpy as np

# Create a sample graph
edges = [("Alice", "Bob"), ("Bob", "Carol"), ("Alice", "Carol"), ("Carol", "Dave")]
G = nx.Graph()
G.add_edges_from(edges)

# 1. Adjacency List (dict of sets) — the most common
adj_list = {n: list(G.neighbors(n)) for n in G.nodes()}
print("Adjacency List:", adj_list)
# {'Alice': ['Bob', 'Carol'], 'Bob': ['Alice', 'Carol'], ...}

# 2. Adjacency Matrix (V x V)
nodes = sorted(G.nodes())
matrix = nx.adjacency_matrix(G, nodelist=nodes).todense()
print("Adjacency Matrix:\n", matrix)
# [[0 1 1 0]
#  [1 0 1 0]
#  [1 1 0 1]
#  [0 0 1 0]]

# 3. Edge List (simplest, easy to serialize)
edge_list = list(G.edges(data=True))
print("Edge List:", edge_list)
# [('Alice', 'Bob', {}), ('Bob', 'Carol', {}), ...]

# 4. CSR — used for large-scale / GNN
# (scipy sparse matrix)
from scipy.sparse import csr_matrix
csr = csr_matrix(matrix)
print("CSR:", csr.data, csr.indices, csr.indptr)

# 5. Property Graph (Neo4j-style) — nodes/edges carry properties
G_prop = nx.DiGraph()
G_prop.add_node("Alice", label="Person", age=35, role="CTO")
G_prop.add_node("Phoenix", label="Project", budget=500000)
G_prop.add_edge("Alice", "Phoenix", type="MANAGES", since="2024-01-01", confidence=0.95)
print("Properties:", dict(G_prop.nodes(data=True)))
