class ReActAgent:
    """
    ReAct: Reasoning + Acting
    
    Thought → Action → Observation → Thought → ...
    
    Based on paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
    (Yao et al., 2022)
    
    Harness integration:
    - max_steps as guardrail
    - tool validation before execution
    - metrics tracking
    - error recovery
    """
    
    def __init__(self, tools, llm_func, max_steps=10):
        self.tools = tools
        self.llm = llm_func
        self.max_steps = max_steps
        self.trace = []
        self.token_usage = 0
    
    def run(self, query):
        """Execute ReAct loop"""
        prompt = f"""Solve this step by step using Thought/Action/Observation.

Question: {query}

Available actions:
{self._format_tools()}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(input)]
Observation: [result of action]
... (repeat Thought/Action/Observation as needed)
Thought: [final reasoning]
Final Answer: [your answer]"""
        
        history = prompt
        
        for step in range(self.max_steps):
            response = self._llm_call(history)
            
            # Phân tích cú pháp phản hồi
            parsed = self._parse_response(response)
            
            if parsed.get("final_answer"):
                return {
                    "answer": parsed["final_answer"],
                    "steps": step + 1,
                    "trace": self.trace,
                    "token_usage": self.token_usage,
                }
            
            # Thực thi hành động
            if parsed.get("action"):
                tool_name, tool_input = self._parse_action(parsed["action"])
                
                # Kiểm tra hợp lệ lệnh gọi tool
                if not self._validate_tool(tool_name):
                    history += f"\n{response}"
                    history += f"\nObservation: Invalid tool '{tool_name}'. Use available tools only."
                    continue
                
                observation = self._execute_tool(tool_name, tool_input)
                
                self.trace.append({
                    "step": step + 1,
                    "thought": parsed.get("thought", ""),
                    "action": parsed["action"],
                    "observation": observation,
                })
                
                history += f"\n{response}"
                history += f"\nObservation: {observation}"
            else:
                history += f"\n{response}"
        
        return {
            "answer": "Max steps reached without final answer",
            "steps": self.max_steps,
            "trace": self.trace,
            "token_usage": self.token_usage,
        }
    
    def _format_tools(self):
        lines = []
        for name, tool in self.tools.items():
            params = tool.get("params", [])
            lines.append(f"- {name}({', '.join(params)})")
        return "\n".join(lines)
    
    def _parse_response(self, response):
        """Parse Thought/Action/Observation from response"""
        result = {}
        
        if "Final Answer:" in response:
            result["final_answer"] = response.split("Final Answer:")[-1].strip()
        
        if "Thought:" in response:
            thought_lines = [l for l in response.split('\n') if l.strip().startswith('Thought:')]
            if thought_lines:
                result["thought"] = thought_lines[-1].replace('Thought:', '').strip()
        
        if "Action:" in response:
            action_line = [l for l in response.split('\n') if l.strip().startswith('Action:')]
            if action_line:
                result["action"] = action_line[0].replace('Action:', '').strip()
        
        return result
    
    def _parse_action(self, action_str):
        """Parse tool_name(input) format"""
        import re
        match = re.match(r'(\w+)\((.+)\)', action_str)
        if match:
            return match.group(1), match.group(2)
        return action_str, ""
    
    def _validate_tool(self, tool_name):
        """Check if tool exists in available tools"""
        return tool_name in self.tools
    
    def _execute_tool(self, tool_name, tool_input):
        if tool_name in self.tools:
            try:
                func = self.tools[tool_name].get("function")
                if func:
                    return func(tool_input)
            except Exception as e:
                return f"Error: {e}"
        return f"Unknown tool: {tool_name}"
    
    def _llm_call(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "Thought: I don't know\nFinal Answer: N/A"
