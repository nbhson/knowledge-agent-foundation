class SimpleAgent:
    """
    Simple agent with tool-calling loop
    
    Pattern: Think → Act → Observe → Repeat
    
    Harness integration:
    - Respects max_iterations (guardrail)
    - Logs all steps (feedback loop)
    - Validates tool permissions
    """
    
    def __init__(self, tools, llm_func, max_iterations=10):
        self.tools = {tool["name"]: tool for tool in tools}
        self.llm = llm_func
        self.max_iterations = max_iterations
        self.memory = []
        self.metrics = {
            "total_iterations": 0,
            "tools_used": {},
            "errors": 0,
            "total_tokens": 0,
        }
    
    def run(self, task):
        """Execute task with tool calls"""
        self.memory = []
        context = f"Task: {task}\n\nAvailable tools: {list(self.tools.keys())}"
        
        for i in range(self.max_iterations):
            # Suy luận (Think): quyết định bước tiếp theo
            thought = self._think(context)
            
            # Kiểm tra nếu đã hoàn thành
            if thought.get("done"):
                return {
                    "answer": thought.get("answer", ""),
                    "steps": self.memory,
                    "iterations": i + 1,
                    "metrics": self.metrics,
                }
            
            # Hành động (Act): thực thi tool với kiểm tra hợp lệ
            tool_name = thought.get("tool")
            tool_input = thought.get("input", {})
            
            if tool_name and tool_name in self.tools:
                # Kiểm tra hợp lệ trước khi thực thi
                if not self._validate_tool_call(tool_name, tool_input):
                    context += f"\n\nStep {i+1}: Tool validation failed for '{tool_name}'. Try different approach."
                    continue
                
                result = self._execute_tool(tool_name, tool_input)
                
                # Kiểm tra hợp lệ sau khi thực thi
                if not self._validate_result(result):
                    self.metrics["errors"] += 1
                    context += f"\n\nStep {i+1}: Result validation failed. Retry with different parameters."
                    continue
                
                # Quan sát (Observe): thêm kết quả vào Context
                observation = f"Tool '{tool_name}' returned: {result}"
                context += f"\n\nStep {i+1}: {thought.get('reasoning', '')}"
                context += f"\n→ Used {tool_name}({tool_input})"
                context += f"\n→ Result: {result}"
                
                self.memory.append({
                    "step": i + 1,
                    "thought": thought,
                    "action": tool_name,
                    "result": result,
                })
                
                self.metrics["tools_used"][tool_name] = self.metrics["tools_used"].get(tool_name, 0) + 1
            else:
                context += f"\n\nStep {i+1}: Invalid tool '{tool_name}'. Try again."
            
            self.metrics["total_iterations"] = i + 1
        
        return {
            "answer": "Max iterations reached",
            "steps": self.memory,
            "iterations": self.max_iterations,
            "metrics": self.metrics,
        }
    
    def _think(self, context):
        """LLM decides next action"""
        prompt = f"""{context}

Based on the information above, decide your next action.

Output JSON:
{{
  "reasoning": "Why I'm doing this",
  "tool": "tool_name" or null if done,
  "input": {{"param": "value"}},
  "done": false,
  "answer": null
}}

If you have enough information to answer, set "done": true and provide "answer"."""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"done": True, "answer": "No LLM available"}
    
    def _validate_tool_call(self, tool_name, tool_input):
        """Pre-execution validation (Harness guardrail)"""
        # Kiểm tra tool có tồn tại không
        if tool_name not in self.tools:
            return False
        
        # Kiểm tra các tham số bắt buộc
        tool = self.tools[tool_name]
        required = tool.get("required_params", [])
        for param in required:
            if param not in tool_input:
                return False
        
        return True
    
    def _validate_result(self, result):
        """Post-execution validation (Harness guardrail)"""
        if result is None:
            return False
        if isinstance(result, str) and result.startswith("Error:"):
            return False
        return True
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool"""
        tool = self.tools.get(tool_name)
        if tool and "function" in tool:
            try:
                return tool["function"](**tool_input)
            except Exception as e:
                return f"Error: {str(e)}"
        return f"Tool '{tool_name}' not found"


class MultiAgent:
    """
    Multi-agent system with specialized agents
    
    Based on Anthropic's multi-agent architecture pattern:
    - Planner Agent: Creates the plan
    - Generator Agent: Executes each step
    - Evaluator Agent: Validates results
    """
    
    def __init__(self, agents, coordinator_llm=None):
        self.agents = agents  # {tên: agent}
        self.coordinator = coordinator_llm
    
    def run(self, task):
        """Coordinate multiple agents"""
        plan = self._create_plan(task)
        
        results = {}
        for step in plan:
            agent_name = step["agent"]
            subtask = step["task"]
            
            if agent_name in self.agents:
                result = self.agents[agent_name].run(subtask)
                results[agent_name] = result
                
                # Kiểm tra xem kết quả có đạt yêu cầu không
                if not self._evaluate_result(result, subtask):
                    # Thử lại với phản hồi (feedback)
                    retry_result = self.agents[agent_name].run(
                        f"{subtask}\n\nLần trước thất bại vì: {result.get('answer', 'unknown error')}"
                    )
                    results[agent_name] = retry_result
        
        return self._synthesize(results, task)
    
    def _create_plan(self, task):
        """Decompose task across agents"""
        agent_names = list(self.agents.keys())
        
        if self.coordinator:
            prompt = f"""Assign subtasks to available agents.

Task: {task}
Available agents: {agent_names}

Output JSON:
{{"steps": [{{"agent": "...", "task": "...", "dependencies": []}}]}}"""
            
            response = self.coordinator(prompt)
            try:
                import json
                return json.loads(response).get("steps", [])
            except json.JSONDecodeError:
                pass
        
        return [{"agent": agent_names[0], "task": task}]
    
    def _evaluate_result(self, result, original_task):
        """Evaluate if result meets requirements"""
        if result.get("iterations", 0) >= 10:
            return False
        if not result.get("answer"):
            return False
        return True
    
    def _synthesize(self, results, original_task):
        """Combine results from all agents"""
        combined = "\n".join(
            f"Agent {name}: {r.get('answer', 'N/A')}"
            for name, r in results.items()
        )
        
        if self.coordinator:
            prompt = f"""Tổng hợp kết quả từ nhiều agents:

Task gốc: {original_task}

Kết quả:
{combined}

Tổng hợp:"""
            return self.coordinator(prompt)
        
        return combined
