class AdaptiveCoT:
    """
    Dynamically choose CoT strategy based on question complexity
    
    Simple question → Zero-shot CoT (fast)
    Medium question → Standard CoT (balanced)
    Complex question → Self-consistency or ToT (thorough)
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.builder = CoTPromptBuilder()
    
    def classify_complexity(self, question: str) -> str:
        """Classify question complexity"""
        if self.llm:
            prompt = f"""Đánh giá độ phức tạp của câu hỏi (1-10):

Câu hỏi: {question}

Phân loại:
- 1-3: Đơn giản (factual, simple calculation)
- 4-6: Trung bình (analysis, comparison)
- 7-10: Phức tạp (multi-step reasoning, creative)

Điểm (1-10):"""
            
            response = self.llm(prompt)
            try:
                score = int(''.join(c for c in response if c.isdigit())[:2])
                if score <= 3:
                    return "simple"
                elif score <= 6:
                    return "medium"
                else:
                    return "complex"
            except (ValueError, IndexError):
                pass
        
        return "medium"
    
    def build_prompt(self, question: str) -> str:
        """Automatically choose best CoT strategy"""
        complexity = self.classify_complexity(question)
        
        if complexity == "simple":
            return self.builder.zero_shot(question)
        elif complexity == "medium":
            return self.builder.standard(question)
        else:
            return self.builder.structured_reasoning(question)
    
    def execute(self, question: str) -> Dict:
        """Full adaptive CoT execution"""
        complexity = self.classify_complexity(question)
        prompt = self.build_prompt(question)
        
        return {
            "question": question,
            "complexity": complexity,
            "prompt": prompt,
            "strategy": self._get_strategy_name(complexity),
        }
    
    def _get_strategy_name(self, complexity: str) -> str:
        return {
            "simple": "Zero-shot CoT",
            "medium": "Standard CoT",
            "complex": "Structured Reasoning",
        }[complexity]
