class LLMJudge:
    """
    Use an LLM to evaluate the output of an AI agent.
    
    Leverage: GPT-4, Claude, or another large model
    as a "judge" to assess code quality.
    
    Pros:
    - Can evaluate nuanced qualities (readability, design)
    - No need to write test cases for every edge case
    - Can understand intent and context
    
    Cons:
    - Cost (one extra LLM call)
    - May not be 100% consistent
    - The judge can also hallucinate
    """
    
    def __init__(self, judge_model_func):
        self.judge = judge_model_func
    
    def evaluate_code(self, code: str, task: str, 
                      context: str = "") -> Dict:
        """Evaluate code with an LLM judge"""
        
        prompt = f"""You are a senior code reviewer. Evaluate the following code.

TASK: {task}

CODE:
