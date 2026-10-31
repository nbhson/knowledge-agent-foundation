embedder = Embedder(model="nomic-embed-text")
embedder.embed_batch(chunks, batch_size=32)   # ngoài đường chạy
qv = embedder.embed_query("mức đóng BHYT hiện tại")  # = embed("query: ...")
hits = vector_store.search(qv, top_k=50)
best = reranker.rerank(query, hits, top_k=5)
