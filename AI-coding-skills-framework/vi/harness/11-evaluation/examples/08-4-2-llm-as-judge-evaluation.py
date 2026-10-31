class LLMJudge:
    """
    Dùng LLM để đánh giá output của AI agent.
    
    Leverage: GPT-4, Claude, hoặc model lớn khác
    làm "judge" để đánh giá code quality.
    
    Ưu điểm:
    - Có thể đánh giá nuanced qualities (readability, design)
    - Không cần viết test cases cho mọi edge case
    - Có thể hiểu intent và context
    
    Nhược điểm:
    - Chi phí (cần thêm 1 LLM call)
    - Có thể không consistent 100%
    - Judge cũng có thể hallucinate
    """
    
    def __init__(self, judge_model_func):
        self.judge = judge_model_func
    
    def evaluate_code(self, code: str, task: str, 
                      context: str = "") -> Dict:
        """Đánh giá code bằng LLM judge"""
        
        prompt = f"""You are a senior code reviewer. Evaluate the following code.

TASK: {task}

CODE:
