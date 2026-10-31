class GraphRAG:
    """A graph-based RAG system"""

    def __init__(self, knowledge_graph, embedder, llm_model):
        self.kg = knowledge_graph
        self.embedder = embedder
        self.llm_model = llm_model

    def retrieve(self, query):
        """
        Retrieve context from the knowledge graph

        1. Extract entities from the query
        2. Find the related subgraph
        3. Rank by relevance
        4. Convert to context
        """
        # Step 1: Extract entities from the query
        entities = self._extract_entities(query)

        # Step 2: Get the subgraph for each entity
        subgraph_facts = []
        for entity in entities:
            related = self.kg.query_entity(entity, max_hops=2)
            subgraph_facts.extend(related)

        # Step 3: Rank by relevance to the query
        query_embedding = self.embedder.embed_query(query)

        ranked_facts = []
        for subj, pred, obj, depth in subgraph_facts:
            fact_text = f"{subj} {pred} {obj}"
            fact_embedding = self.embedder.embed(fact_text)

            # Score = relevance × (1 / (depth + 1))
            import numpy as np
            similarity = np.dot(query_embedding, fact_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(fact_embedding)
            )
            score = similarity * (1 / (depth + 1))
            ranked_facts.append((fact_text, score))

        ranked_facts.sort(key=lambda x: x[1], reverse=True)

        # Step 4: Convert to context
        context = "\n".join([
            f"[{i+1}] {fact}"
            for i, (fact, _) in enumerate(ranked_facts[:10])
        ])

        return context

    def _extract_entities(self, text):
        """Simple entity extraction (can use an NER model)"""
        # Placeholder - use the LLM for better extraction
        prompt = f"""Extract all entities (names, products, concepts) from:
{text}

Entities (one per line):"""

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False
        })

        entities = [
            e.strip() for e in response.json()["response"].split('\n')
            if e.strip()
        ]
        return entities
