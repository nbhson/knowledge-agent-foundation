class FunctionCallingAgent:
    """
    Agent using OpenAI-style function calling
    
    Supports: Multi-turn tool calls, parallel calls, forced tool use,
    chained tool calls, automatic retry on malformed calls
    """
    
    def __init__(self, llm_func, tool_registry):
        self.llm = llm_func
        self.registry = tool_registry
        self.executor = ToolExecutor(tool_registry)
        self.conversation_history = []
    
    def run(self, user_message: str, max_rounds: int = 10, 
            auto_retry: bool = True) -> Dict:
        """
        Execute agent loop with function calling
        """
        messages = self.conversation_history + [
            {"role": "user", "content": user_message}
        ]
        tools = self.registry.to_openai_format()
        
        total_tool_calls = 0
        tool_usage = {}
        
        for round_num in range(max_rounds):
            # Call LLM
            response = self._call_llm(messages, tools)
            
            # Check for tool calls
            if not response.get("tool_calls"):
                final_answer = response.get("content", "")
                self.conversation_history = messages + [
                    {"role": "assistant", "content": final_answer}
                ]
                return {
                    "answer": final_answer,
                    "rounds": round_num + 1,
                    "total_tool_calls": total_tool_calls,
                    "tool_usage": tool_usage,
                }
            
            # Add assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": response.get("content"),
                "tool_calls": response["tool_calls"],
            })
            
            # Execute each tool call
            for tc in response["tool_calls"]:
                func_name = tc["function"]["name"]
                total_tool_calls += 1
                tool_usage[func_name] = tool_usage.get(func_name, 0) + 1
                
                try:
                    func_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError as e:
                    if auto_retry:
                        # Ask LLM to fix malformed arguments
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc["id"],
                            "content": json.dumps({
                                "error": f"Invalid JSON arguments: {e}",
                                "hint": "Please provide valid JSON arguments",
                            }),
                        })
                        continue
                    func_args = {}
                
                # Execute tool
                result = self.executor.execute(func_name, func_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": json.dumps(result, ensure_ascii=False, default=str),
                })
        
        return {
            "answer": "Max rounds reached without final answer",
            "rounds": max_rounds,
            "total_tool_calls": total_tool_calls,
            "tool_usage": tool_usage,
        }
    
    def forced_tool_call(self, user_message: str, tool_name: str) -> Dict:
        """
        Force LLM to use a specific tool
        Useful when intent is clear from pre-classification
        """
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        messages = [{"role": "user", "content": user_message}]
        tools = self.registry.to_openai_format()
        
        # Force specific tool
        response = self._call_llm(
            messages, 
            tools,
            tool_choice={"type": "function", "function": {"name": tool_name}}
        )
        
        if response.get("tool_calls"):
            tc = response["tool_calls"][0]
            try:
                func_args = json.loads(tc["function"]["arguments"])
            except json.JSONDecodeError:
                func_args = {}
            
            result = self.executor.execute(tool_name, func_args)
            
            return {
                "tool": tool_name,
                "args": func_args,
                "result": result,
            }
        
        return {"error": "LLM did not call the forced tool"}
    
    def parallel_tool_calls(self, user_message: str) -> Dict:
        """
        Enable parallel tool calling
        LLM can call multiple tools simultaneously
        """
        messages = [{"role": "user", "content": user_message}]
        tools = self.registry.to_openai_format()
        
        response = self._call_llm(messages, tools)
        
        if response.get("tool_calls"):
            # Execute all in parallel (simulated with batch)
            calls = []
            for tc in response["tool_calls"]:
                try:
                    func_args = json.loads(tc["function"]["arguments"])
                except json.JSONDecodeError:
                    func_args = {}
                calls.append({
                    "tool": tc["function"]["name"],
                    "params": func_args,
                })
            
            results = self.executor.execute_batch(calls)
            
            return {
                "parallel_results": results,
                "tools_called": len(results),
                "all_success": all(r["success"] for r in results),
            }
        
        return {"answer": response.get("content", "")}
    
    def _call_llm(self, messages, tools, tool_choice=None):
        """Call LLM with function calling support"""
        if self.llm:
            kwargs = {"messages": messages, "tools": tools}
            if tool_choice:
                kwargs["tool_choice"] = tool_choice
            return self.llm(**kwargs)
        return {"content": "No LLM configured"}
