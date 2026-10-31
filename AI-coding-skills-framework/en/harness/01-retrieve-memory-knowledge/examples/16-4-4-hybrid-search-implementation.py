class HybridSearch:
    """Combines semantic (vector) search with keyword (BM25) search"""

    def __init__(self, vector_store, embedder, bm25_index,
                 rrf_k=60, semantic_weight=1.0, keyword_weight=1.0):
        self.vector_store = vector_store
        self.embedder = embedder
        self.bm25 = bm25_index
        self.rrf_k = rrf_k
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

    def search(self, query, top_k=10):
        """Perform hybrid search"""

        # 1. Semantic search
        query_embedding = self.embedder.embed_query(query)
        semantic_results = self.vector_store.search(
            query_embedding, top_k=top_k * 2
        )
        semantic_ranking = [r["document"] for r in semantic_results]

        # 2. Keyword search (BM25)
        bm25_results = self.bm25.search(query, top_k=top_k * 2)
        keyword_ranking = [doc for doc, score in bm25_results]

        # 3. Combine using RRF
        combined_ranking = reciprocal_rank_fusion(
            [semantic_ranking, keyword_ranking],
            k=self.rrf_k
        )

        # 4. Return the top_k
        return combined_ranking[:top_k]

    def search_with_scores(self, query, top_k=10):
        """Hybrid search with individual scores"""

        # Semantic
        query_embedding = self.embedder.embed_query(query)
        semantic_results = self.vector_store.search(
            query_embedding, top_k=top_k * 2
        )

        # BM25
        bm25_results = self.bm25.search(query, top_k=top_k * 2)

        # Score normalization and combination
        # Normalize the scores to [0, 1]
        max_semantic = max(r["score"] for r in semantic_results) if semantic_results else 1
        max_bm25 = max(score for _, score in bm25_results) if bm25_results else 1

        combined_scores = {}

        for r in semantic_results:
            doc = r["document"]
            norm_score = r["score"] / max_semantic
            combined_scores[doc] = {
                "semantic_score": r["score"],
                "keyword_score": 0,
                "combined_score": norm_score * self.semantic_weight,
            }

        for doc, score in bm25_results:
            norm_score = score / max_bm25
            if doc in combined_scores:
                combined_scores[doc]["keyword_score"] = score
                combined_scores[doc]["combined_score"] += norm_score * self.keyword_weight
            else:
                combined_scores[doc] = {
                    "semantic_score": 0,
                    "keyword_score": score,
                    "combined_score": norm_score * self.keyword_weight,
                }

        # Sort by the combined score
        sorted_results = sorted(
            combined_scores.items(),
            key=lambda x: x[1]["combined_score"],
            reverse=True
        )

        return sorted_results[:top_k]
