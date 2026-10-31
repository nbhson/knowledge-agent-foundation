"""
Bước 4: Xử lý query trước khi search

Techniques:
- Query Expansion: Tạo nhiều variations
- HyDE: Tạo hypothetical answer trước khi search
- Query Rewriting: Viết lại query rõ hơn
"""

class QueryProcessor:
    def __init__(self, llm_func):
        self.llm = llm_func
    
    def expand_query(self, query):
        """
        Tạo nhiều variations của query để tăng recall
        
        Input: "BHYT đóng bao nhiêu?"
        Output: [
            "mức đóng bảo hiểm y tế",
            "phí BHYT là bao nhiêu",
            "tỷ lệ đóng bảo hiểm y tế"
        ]
        """
        prompt = f"""Tạo 3 câu hỏi khác nhau dựa trên câu hỏi sau để tìm kiếm thông tin:
        
Câu hỏi gốc: {query}

Viết 3 câu hỏi (mỗi câu 1 dòng):"""
        
        response = self.llm(prompt)
        variations = [q.strip() for q in response.split('\n') if q.strip()]
        return [query] + variations
    
    def hyde_query(self, query):
        """
        HyDE (Hypothetical Document Embeddings):
        Tạo một câu trả lời giả định, rồi dùng nó để search
        
        Ý tưởng: Câu trả lời giả định sẽ gần hơn với câu trả lời thật
        trong không gian embedding
        """
        prompt = f"""Viết một đoạn ngắn trả lời câu hỏi sau:
        
Câu hỏi: {query}

Trả lời ngắn:"""
        
        hypothetical_answer = self.llm(prompt)
        return hypothetical_answer
    
    def classify_query(self, query):
        """
        Phân loại query để chọn chiến lược search phù hợp
        
        Simple: Chỉ cần 1 nguồn
        Complex: Cần nhiều nguồn
        Aggregation: Cần tính toán/gộp dữ liệu
        """
        prompt = f"""Phân loại câu hỏi sau:
        
Câu hỏi: {query}

Loại (simple/complex/aggregation):"""
        
        response = self.llm(prompt).strip().lower()
        return response if response in ["simple", "complex", "aggregation"] else "simple"
