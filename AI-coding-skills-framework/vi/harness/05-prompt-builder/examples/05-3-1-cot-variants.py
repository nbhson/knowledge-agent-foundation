class CoTPromptBuilder:
    """
    Chain-of-Thought prompt builder with multiple variants
    
    Variants:
    1. Standard CoT: "Let's think step by step"
    2. Zero-shot CoT: Add "Think carefully"
    3. Few-shot CoT: Show reasoning examples
    4. Self-consistency: Generate N paths, majority vote
    5. Tree-of-Thoughts: Explore multiple branches
    6. Graph-of-Thoughts: Non-linear reasoning
    """
    
    @staticmethod
    def standard(question: str) -> str:
        """Standard Chain-of-Thought"""
        return f"""Câu hỏi: {question}

Hãy suy nghĩ từng bước một (step by step):

Bước 1: Phân tích vấn đề
Bước 2: Xác định thông tin cần thiết
Bước 3: Áp dụng kiến thức liên quan
Bước 4: Tổng hợp kết quả
...
Kết luận:"""
    
    @staticmethod
    def zero_shot(question: str) -> str:
        """Zero-shot CoT — no examples needed"""
        return f"""Câu hỏi: {question}

Hãy suy nghĩ kỹ trước khi trả lời. Giải thích logic từng bước.
Đừng bỏ qua bất kỳ bước nào.

Trả lời:"""
    
    @staticmethod
    def few_shot(question: str, examples_text: str) -> str:
        """Few-shot CoT — show reasoning patterns"""
        return f"""Ví dụ về cách suy nghĩ:

{examples_text}

Bây giờ, hãy suy nghĩ cho câu hỏi sau:

Câu hỏi: {question}

Suy nghĩ từng bước:"""
    
    @staticmethod
    def self_consistency(question: str, n_paths: int = 3) -> str:
        """
        Self-Consistency: Generate multiple reasoning paths,
        then take majority vote for final answer
        """
        paths = "\n\n".join(
            f"Cách {i+1}:\n... → Kết quả: ..."
            for i in range(n_paths)
        )
        
        return f"""Câu hỏi: {question}

Hãy giải quyết theo {n_paths} cách khác nhau:

{paths}

So sánh {n_paths} kết quả trên.
Kết quả cuối cùng (đa số đồng ý):"""
    
    @staticmethod
    def tree_of_thoughts(question: str, n_branches: int = 3) -> str:
        """Tree of Thoughts — explore multiple branches"""
        branches = "\n\n".join(
            f"Nhánh {i+1}:\n  Suy nghĩ: ...\n  Đánh giá (1-10): ...\n  Kết quả: ..."
            for i in range(n_branches)
        )
        
        return f"""Câu hỏi: {question}

Hãy khám phá {n_branches} hướng suy nghĩ khác nhau:

{branches}

Đánh giá {n_branches} nhánh:
- Nhánh nào có logic tốt nhất?
- Nhánh nào có kết quả khả thi nhất?

Chọn nhánh tốt nhất và đưa ra kết luận:"""
    
    @staticmethod
    def structured_reasoning(question: str) -> str:
        """Structured reasoning with clear phases"""
        return f"""Câu hỏi: {question}

=== PHASE 1: UNDERSTANDING ===
- Vấn đề chính là gì?
- Thông tin nào đã có?
- Thông tin nào còn thiếu?

=== PHASE 2: ANALYSIS ===
- Các yếu tố liên quan?
- Mối quan hệ giữa các yếu tố?
- Rủi ro và cơ hội?

=== PHASE 3: REASONING ===
- Áp dụng logic/knowledge
- Xem xét multiple perspectives
- Đánh giá alternatives

=== PHASE 4: CONCLUSION ===
- Kết luận chính
- Confidence level (1-10)
- Hạn chế của kết luận"""
