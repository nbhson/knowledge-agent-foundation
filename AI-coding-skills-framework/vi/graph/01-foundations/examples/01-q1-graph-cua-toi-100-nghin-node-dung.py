import networkx as nx
G = nx.karate_club_graph()             # 34 node, rất thưa
A = nx.to_scipy_sparse_array(G)
print(A.nnz, A.shape)                  # 78 ô khác 0 trên 1.156 ô
# shape (34, 34) — cùng dữ liệu này ở 100K node sẽ là (100000, 100000)
