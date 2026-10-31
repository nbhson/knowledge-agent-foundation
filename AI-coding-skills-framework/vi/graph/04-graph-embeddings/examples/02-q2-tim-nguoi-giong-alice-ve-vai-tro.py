walks = [get_random_walk(G, n, walk_length=20) for n in G for _ in range(10)]
model = Word2Vec(walks, vector_size=64, window=5, sg=1, min_count=0, epochs=5)
sim = cosine(model.wv["node_0"], model.wv["node_7"])   # càng cao càng giống
