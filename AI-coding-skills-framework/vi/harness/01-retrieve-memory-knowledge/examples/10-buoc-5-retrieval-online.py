"""
Bước 5: Tìm kiếm documents liên quan

Strategies:
- Single vector search
- Multi-query search (kết hợp expanded queries)
- Hybrid search (vector + BM25)
"""

class Retriever:
    def __init__(self, vector_store, embedder, top_k=10):
        self.vector_store = vector_store
        self.embedder = embedder
        self.top_k = top_k
    
    def retrieve(self, query):
        """Basic vector search"""
        query_embedding = self.embedder.embed_query(query)
        results = self.vector_store.search(query_embedding, self.top_k)
        return results
    
    def multi_query_retrieve(self, queries):
        """Search với nhiều queries, gộp kết quả"""
        all_results = {}
        
        for query in queries:
            results = self.retrieve(query)
            for r in results:
                doc_text = r["document"]
                if doc_text not in all_results:
                    all_results[doc_text] = r
                else:
                    # Boost score nếu xuất hiện trong nhiều queries
                    all_results[doc_text]["score"] += r["score"] * 0.5
        
        # Sort and return top_k
        sorted_results = sorted(
            all_results.values(), 
            key=lambda x: x["score"], 
            reverse=True
        )
        return sorted_results[:self.top_k]
    
    def mmr_retrieve(self, query, lambda_param=0.5):
        """
        Maximal Marginal Relevance:
        Balance giữa RELEVANCE và DIVERSITY
        
        Tránh return nhiều documents quá giống nhau
        
        lambda_param:
        - 1.0: Chỉ quan tâm relevance
        - 0.0: Chỉ quan tâm diversity
        - 0.5: Cân bằng cả hai
        """
        query_embedding = self.embedder.embed_query(query)
        candidates = self.vector_store.search(query_embedding, self.top_k * 3)
        
        selected = []
        remaining = list(candidates)
        
        while len(selected) < self.top_k and remaining:
            best_score = -1
            best_idx = 0
            
            for i, candidate in enumerate(remaining):
                # Relevance score
                relevance = candidate["score"]
                
                # Diversity: max similarity to already selected
                diversity_penalty = 0
                for s in selected:
                    sim = self._cosine_sim(
                        candidate["vector"], s["vector"]
                    )
                    diversity_penalty = max(diversity_penalty, sim)
                
                # MMR score
                mmr_score = lambda_param * relevance - (1 - lambda_param) * diversity_penalty
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = i
            
            selected.append(remaining.pop(best_idx))
        
        return selected
