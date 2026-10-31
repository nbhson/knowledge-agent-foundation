class PlanAndSolve:
    """
    Plan-and-Solve prompting strategy
    
    Based on paper: "Plan-and-Solve Prompting" (Wang et al., 2023)
    
    1. Plan: Break down the problem into sub-problems
    2. Solve: Execute each sub-problem
    3. Verify: Check results against original problem
    4. Re-plan: If verification fails, create new plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.max_replan_attempts = 3
    
    def plan(self, problem):
        """Step 1: Create a plan"""
        prompt = f"""Hãy lập kế hoạch giải quyết vấn đề sau. 
Đưa ra các bước cụ thể, rõ ràng.

Vấn đề: {problem}

Kế hoạch (mỗi bước trên 1 dòng, bắt đầu bằng số):
1. ...
2. ...
3. ..."""
        
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Bước 1: Phân tích {problem}", "Bước 2: Thực hiện"]
    
    def solve_step(self, step, context=""):
        """Step 2: Solve a single step"""
        prompt = f"""Thực hiện bước sau:

Bước: {step}
Context: {context}

Kết quả:"""
        
        if self.llm:
            return self.llm(prompt)
        return f"Kết quả cho: {step}"
    
    def verify(self, problem, solution):
        """Step 3: Verify solution"""
        prompt = f"""Kiểm tra giải pháp cho vấn đề:

Vấn đề: {problem}
Giải pháp: {solution}

Đánh giá (JSON):
{{
  "complete": true/false,
  "correct": true/false,
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1"]
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"complete": True, "correct": True, "issues": [], "suggestions": []}
    
    def replan(self, problem, original_plan, failed_step, error):
        """Create a new plan based on failure"""
        prompt = f"""Kế hoạch ban đầu thất bại. Hãy tạo kế hoạch mới.

Vấn đề: {problem}
Kế hoạch cũ: {original_plan}
Bước thất bại: {failed_step}
Lỗi: {error}

Kế hoạch mới (mỗi bước trên 1 dòng):
"""
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Fix: {failed_step}"]
    
    def run(self, problem):
        """Execute full plan-and-solve cycle with re-planning"""
        plan = self.plan(problem)
        
        for attempt in range(self.max_replan_attempts):
            results = []
            context = ""
            all_succeeded = True
            
            for i, step in enumerate(plan):
                result = self.solve_step(step, context)
                results.append({"step": step, "result": result})
                context += f"\nBước {i+1} đã hoàn thành: {result[:200]}"
            
            # Xác minh
            verification = self.verify(problem, "\n".join(
                f"{r['step']}: {r['result']}" for r in results
            ))
            
            if verification.get("complete", True) and verification.get("correct", True):
                return {
                    "plan": plan,
                    "results": results,
                    "verification": verification,
                    "attempts": attempt + 1,
                }
            
            # Lập lại kế hoạch dựa trên các vấn đề
            if verification.get("issues"):
                plan = self.replan(
                    problem, plan, 
                    verification["issues"][0],
                    str(verification.get("suggestions", []))
                )
        
        return {
            "plan": plan,
            "results": results,
            "verification": verification,
            "attempts": self.max_replan_attempts,
            "status": "max_attempts_reached",
        }
