"""
Bước 6: Generate câu trả lời với context đã retrieve
"""

class RAGGenerator:
    def __init__(self, llm_model="gemma3:12b"):
        self.llm_model = llm_model
        self.ollama_url = "http://localhost:11434"
    
    def generate(self, query, context_docs, system_prompt=None):
        """
        Generate câu trả lời với retrieved context
        """
        # Build context
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            score = doc.get("score", 0)
            text = doc["document"]
            source = doc.get("metadata", {}).get("source", "unknown")
            context_parts.append(f"[{i}] (độ tin cậy: {score:.2f}) {text}\nNguồn: {source}")
        
        context = "\n\n".join(context_parts)
        
        # Build prompt
        system = system_prompt or """Bạn là trợ lý thông minh. Trả lời câu hỏi dựa trên thông tin được cung cấp.

Quy tắc:
1. Chỉ dùng thông tin từ context được cung cấp
2. Luôn trích dẫn nguồn [1], [2]...
3. Nếu thông tin không đủ, nói rõ
4. Trả lời bằng tiếng Việt"""
        
        prompt = f"""{system}

THÔNG TIN THAM KHẢO:
{context}

CÂU HỎI: {query}

TRẢ LỜI:"""
        
        # Call LLM
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
        # Step 1: Process query
        expanded_queries = self.query_processor.expand_query(question)
        
        # Step 2: Retrieve
        context_docs = self.retriever.multi_query_retrieve(expanded_queries)
        
        # Step 3: Generate
        result = self.generator.generate(question, context_docs)
        
        return result
