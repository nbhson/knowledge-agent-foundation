class SelfReflectivePlanner:
    """
    Planner that improves by reflecting on its own plans
    
    Pattern: Plan → Execute → Reflect → Improve Plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.plan_history = []  # Lịch sử kế hoạch và kết quả
    
    def plan_with_reflection(self, task, max_reflections=3):
        """Plan with self-reflection"""
        plan = self._initial_plan(task)
        
        for reflection_round in range(max_reflections):
            # Tự ngẫm (Reflect) về chất lượng kế hoạch
            reflection = self._reflect_on_plan(task, plan)
            
            if reflection["quality_score"] >= 8:
                break  # Dừng lại nếu kế hoạch đã đủ tốt
            
            # Cải thiện kế hoạch dựa trên tự ngẫm
            plan = self._improve_plan(plan, reflection["suggestions"])
        
        return plan
    
    def _initial_plan(self, task):
        return {
            "steps": [],
            "estimated_complexity": 0,
            "risks": [],
        }
    
    def _reflect_on_plan(self, task, plan):
        if self.llm:
            prompt = f"""Phân tích kế hoạch sau:

Task: {task}
Plan: {plan}

Đánh giá:
1. Tính đầy đủ (1-10)
2. Tính khả thi (1-10)
3. Rủi ro (list)
4. Cải tiến (suggestions)"""
            
            response = self.llm(prompt)
            return {"quality_score": 7, "suggestions": [], "risks": []}
        
        return {"quality_score": 5, "suggestions": ["Add more detail"], "risks": []}
    
    def _improve_plan(self, plan, suggestions):
        plan["improvements"] = suggestions
        return plan
    
    def learn_from_outcome(self, task, plan, outcome):
        """Store plan outcome for future learning"""
        self.plan_history.append({
            "task": task,
            "plan": plan,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
        })
