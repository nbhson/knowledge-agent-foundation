class PromptBuilder:
    """Advanced prompt building techniques for RAG"""
    
    def __init__(self, system_prompt=None):
        self.system_prompt = system_prompt or "Bạn là trợ lý AI thông minh."
    
    def build_with_instructions(self, query, context_docs, 
                                  custom_instructions=None):
        """
        Prompt với instructions tùy chỉnh
        
        Techniques:
        - Explicit constraints
        - Step-by-step instructions
        - Output format specification
        """
        instructions = custom_instructions or """
Quy tắc:
1. Chỉ dùng thông tin từ context được cung cấp
2. Luôn trích dẫn nguồn [1], [2]...
3. Nếu không đủ thông tin, nói rõ
4. Trả lời ngắn gọn, rõ ràng
"""
        
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            score = doc.get("score", 0)
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""{self.system_prompt}

{instructions}

CONTEXT:
{context}

CÂU HỎI: {query}

TRẢ LỜI:"""
    
    def build_with_reasoning(self, query, context_docs):
        """
        Prompt yêu cầu model "suy nghĩ" trước khi trả lời
        
        Giúp giảm hallucination và tăng accuracy
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""Bạn là trợ lý phân tích.

THÔNG TIN:
{context}

CÂU HỎI: {query}

HÃY LÀM THEO CÁC BƯỚC SAU:
1. [PHÂN TÍCH] Xác định thông tin nào trong context liên quan
2. [ĐÁNH GIÁ] Đánh giá độ đầy đủ của thông tin
3. [TỔNG HỢP] Tổng hợp thông tin liên quan
4. [TRẢ LỜI] Trả lời câu hỏi một cách rõ ràng

BẮT ĐẦU:"""
    
    def build_with_format(self, query, context_docs, 
                           output_format="markdown"):
        """
        Prompt với output format cụ thể
        
        output_format: "markdown", "json", "table", "list"
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        format_instructions = {
            "markdown": "Trả lời bằng Markdown format với headers và bullet points.",
            "json": 'Trả lời bằng JSON format: {"answer": "...", "sources": [...], "confidence": 0.0-1.0}',
            "table": "Trả lời dưới dạng bảng Markdown.",
            "list": "Trả lời dưới dạng danh sách có đánh số.",
        }
        
        return f"""{self.system_prompt}

CONTEXT:
{context}

CÂU HỎI: {query}

OUTPUT FORMAT: {format_instructions.get(output_format, "Text tự nhiên.")}

TRẢ LỜI:"""
    
    def build_with_guardrails(self, query, context_docs):
        """
        Prompt với guardrails để prevent hallucination
        
        Techniques:
        - Explicit "don't make up" instruction
        - Confidence scoring
        - Source verification
        """
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            text = doc["content"] if isinstance(doc, dict) else doc
            context_parts.append(f"[{i}] {text}")
        
        context = "\n".join(context_parts)
        
        return f"""Bạn là trợ lý chính xác. TUÂN THỦ NGHIÊM NGẶT:

⚠️ QUY TẮC AN TOÀN:
- KHÔNG BAO GIỜ bịa đặt thông tin
- KHÔNG suy luận thêm từ context
- Nếu context không đủ → Nói "Không có đủ thông tin"
- Mỗi luận điểm PHẢI trích dẫn được nguồn [n]

CONTEXT:
{context}

CÂU HỎI: {query}

ĐÁNH GIÁ TRƯỚC KHI TRẢ LỜI:
1. Context có chứa thông tin trả lời câu hỏi không?
2. Nếu CÓ → Trả lời + trích dẫn nguồn
3. Nếu KHÔNG → Nói rõ "Chưa có thông tin từ nguồn tham khảo"

TRẢ LỜI:"""


# Usage
builder = PromptBuilder()

prompt = builder.build_with_guardrails(
    query="BHYT đóng bao nhiêu?",
    context_docs=[
        {"content": "Mức đóng BHYT là 4.5% lương cơ sở", "score": 0.95},
        {"content": "Thẻ BHYT có hiệu lực 5 năm", "score": 0.7},
    ]
)
