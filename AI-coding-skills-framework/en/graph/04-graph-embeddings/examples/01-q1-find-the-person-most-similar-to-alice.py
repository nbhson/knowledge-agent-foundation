model = Node2Vec(G, dimensions=64, walk_length=20, num_walks=10,
                 p=0.5, q=2.0)   # q=2.0 -> BFS-like -> "same team"
