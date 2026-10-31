class MetaPromptBuilder:
    """
    Meta-prompting: Using prompts to generate/optimize other prompts
    
    Based on "Meta-Prompting" research (2024):
    - Generate prompts from task descriptions
    - Optimize prompts based on feedback
    - Compose prompts from components
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def generate_prompt(self, task_description: str, examples: List[Dict] = None) -> str:
        """Generate a prompt from task description"""
        
        examples_text = ""
        if examples:
            examples_text = "\nVí dụ:\n" + "\n".join(
                f"Input: {ex['input']}\nOutput: {ex['output']}" 
                for ex in examples
            )
        
        prompt = f"""Bạn là prompt engineering expert.
Tạo prompt hiệu quả cho task sau:

Task: {task_description}
{examples_text}

Yêu cầu prompt:
- Rõ ràng, cụ thể
- Có cấu trúc
- Bao gồm output format
- Có guardrails nếu cần

Prompt:"""
        
        if self.llm:
            return self.llm(prompt)
        
        return f"Execute the following task: {task_description}"
    
    def optimize_prompt(self, original_prompt: str, feedback: str) -> str:
        """Optimize a prompt based on feedback"""
        
        prompt = f"""Bạn là prompt optimization expert.
Cải thiện prompt sau dựa trên feedback:

PROMPT GỐC:
{original_prompt}

FEEDBACK:
{feedback}

Phân tích:
1. Điểm yếu của prompt gốc
2. Cụm từ nào cần thay đổi
3. Cấu trúc nào cần cải thiện

PROMPT CẢI THIỆN:"""
        
        if self.llm:
            return self.llm(prompt)
        
        return original_prompt
    
    def compose_prompts(self, prompts: List[Dict], template: str = "sequential") -> str:
        """
        Compose multiple prompts into one
        
        strategies:
        - sequential: Prompts in order
        - parallel: All prompts combined
        - hierarchical: Nested prompts
        """
        
        if template == "sequential":
            parts = []
            for i, p in enumerate(prompts):
                parts.append(f"Step {i+1}: {p.get('description', '')}\n{p.get('prompt', '')}")
            return "\n\n".join(parts)
        
        elif template == "parallel":
            combined = "\n\n".join(
                f"[Task {i+1}]: {p.get('prompt', '')}"
                for i, p in enumerate(prompts)
            )
            return f"Execute the following tasks in parallel:\n\n{combined}"
        
        elif template == "hierarchical":
            main = prompts[0].get("prompt", "")
            sub = "\n".join(
                f"- Sub-task {i+1}: {p.get('prompt', '')}"
                for i, p in enumerate(prompts[1:])
            )
            return f"""Main task: {main}

Sub-tasks (execute if needed):
{sub}"""
        
        return "\n\n".join(p.get("prompt", "") for p in prompts)
    
    def evaluate_prompt(self, prompt: str, test_cases: List[Dict]) -> Dict:
        """Evaluate prompt quality against test cases"""
        
        results = []
        for case in test_cases:
            if self.llm:
                response = self.llm(f"{prompt}\n\nInput: {case['input']}")
                
                # Simple correctness check
                correct = case.get("expected", "").lower() in response.lower()
                results.append({
                    "input": case["input"],
                    "expected": case.get("expected", ""),
                    "got": response[:100],
                    "correct": correct,
                })
        
        total = len(results)
        passed = sum(1 for r in results if r["correct"])
        
        return {
            "prompt": prompt[:100] + "...",
            "total_cases": total,
            "passed": passed,
            "accuracy": passed / total if total > 0 else 0,
            "details": results,
        }
