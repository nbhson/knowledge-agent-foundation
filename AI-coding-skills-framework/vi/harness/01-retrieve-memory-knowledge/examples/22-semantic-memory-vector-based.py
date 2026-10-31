class SemanticMemory:
    """
    Store và retrieve facts using vector search
    
    ✅ Scalable
    ✅ Semantic search capability
    ❌ Dependent on embedding quality
    """
    
    def __init__(self, vector_store, embedder):
        self.store = vector_store
        self.embedder = embedder
        self.fact_count = 0
    
    def add_fact(self, fact, metadata=None):
        """Store a new fact"""
        embedding = self.embedder.embed(fact)
        self.store.add(
            document=fact,
            vector=embedding,
            metadata={
                "type": "fact",
                "id": f"fact_{self.fact_count}",
                **(metadata or {}),
            }
        )
        self.fact_count += 1
    
    def recall(self, query, top_k=5):
        """Recall relevant facts"""
        query_embedding = self.embedder.embed_query(query)
        results = self.store.search(query_embedding, top_k)
        return results
    
    def consolidate(self, llm_func):
        """
        Consolidate similar facts (reduce redundancy)
        """
        # Get all facts
        all_facts = self.store.search(
            self.embedder.embed("fact"), top_k=1000
        )
        
        # Group similar facts
        groups = self._cluster_facts(all_facts)
        
        # Summarize each group
        consolidated = []
        for group in groups:
            if len(group) == 1:
                consolidated.append(group[0]["document"])
            else:
                facts_text = "\n".join(
                    f"- {f['document']}" for f in group
                )
                summary = llm_func(
                    f"Consolidate these facts:\n{facts_text}\n\nConsolidated:"
                )
                consolidated.append(summary)
        
        return consolidated
    
    def _cluster_facts(self, facts, threshold=0.8):
        """Group similar facts together"""
        import numpy as np
        
        if not facts:
            return []
        
        embeddings = [f.get("vector", []) for f in facts]
        
        groups = []
        used = set()
        
        for i, emb_i in enumerate(embeddings):
            if i in used:
                continue
            
            group = [facts[i]]
            used.add(i)
            
            for j, emb_j in enumerate(embeddings):
                if j in used or not emb_i or not emb_j:
                    continue
                
                sim = np.dot(emb_i, emb_j) / (
                    np.linalg.norm(emb_i) * np.linalg.norm(emb_j)
                )
                if sim > threshold:
                    group.append(facts[j])
                    used.add(j)
            
            groups.append(group)
        
        return groups
