"""
Step 6: Generate the answer with the retrieved context
"""

class RAGGenerator:
    def __init__(self, llm_model="gemma3:12b"):
        self.llm_model = llm_model
        self.ollama_url = "http://localhost:11434"

    def generate(self, query, context_docs, system_prompt=None):
        """
        Generate an answer with the retrieved context
        """
        # Build the context
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            score = doc.get("score", 0)
            text = doc["document"]
            source = doc.get("metadata", {}).get("source", "unknown")
            context_parts.append(f"[{i}] (confidence: {score:.2f}) {text}\nSource: {source}")

        context = "\n\n".join(context_parts)

        # Build the prompt
        system = system_prompt or """You are a smart assistant. Answer the question based on the provided information.

Rules:
1. Use only information from the provided context
2. Always cite sources [1], [2]...
3. If the information is insufficient, say so clearly
4. Answer in English"""

        prompt = f"""{system}

REFERENCE INFORMATION:
{context}

QUESTION: {query}

ANSWER:"""

        # Call the LLM
        response = requests.post(f"{self.ollama_url}/api/generate", json={
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False
        })

        return {
            "answer": response.json()["response"],
            "sources": context_docs,
            "context_used": len(context_docs),
        }


# Complete RAG Pipeline
class RAGPipeline:
    def __init__(self, vector_store, embedder, llm_model="gemma3:12b"):
        self.retriever = Retriever(vector_store, embedder)
        self.query_processor = QueryProcessor(self._llm_call)
        self.generator = RAGGenerator(llm_model)

    def query(self, question):
        # Step 1: Process the query
        expanded_queries = self.query_processor.expand_query(question)

        # Step 2: Retrieve
        context_docs = self.retriever.multi_query_retrieve(expanded_queries)

        # Step 3: Generate
        result = self.generator.generate(question, context_docs)

        return result
