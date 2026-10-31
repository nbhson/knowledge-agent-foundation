class ReWOOPlanner:
    """
    ReWOO: Decouple planning from execution
    
    1. PLAN all steps upfront (no observation between steps)
    2. EXECUTE all steps
    3. USE evidence to synthesize answer
    
    Advantage: Fewer LLM calls (batch planning)
    Disadvantage: Less adaptive to failures
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def plan_all(self, task, tools):
        """Generate all plan steps at once"""
        prompt = f"""Tạo kế hoạch hoàn chỉnh cho task sau.

Task: {task}
Tools có sẵn: {list(tools.keys())}

Output JSON:
{{
  "plan": [
    {{"step_id": "e1", "tool": "tool_name", "query": "query for tool"}},
    {{"step_id": "e2", "tool": "tool_name", "query": "query using #e1"}},
    ...
  ],
  "synthesis_prompt": "Dựa trên #e1, #e2, ..., trả lời: {task}"
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"plan": [], "synthesis_prompt": task}
    
    def execute_plan(self, plan, tools):
        """Execute all plan steps, collecting evidence"""
        evidence = {}
        
        for step in plan.get("plan", []):
            tool_name = step.get("tool", "")
            query = step.get("query", "")
            
            # Thay thế tham chiếu bằng bằng chứng trước đó
            for ref_id, ref_val in evidence.items():
                query = query.replace(f"#{ref_id}", str(ref_val))
            
            if tool_name in tools:
                try:
                    result = tools[tool_name](query)
                    evidence[step["step_id"]] = result
                except Exception as e:
                    evidence[step["step_id"]] = f"Error: {e}"
        
        return evidence
