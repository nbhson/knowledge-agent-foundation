class ToolComposer:
    """
    Compose multiple tools into workflows
    
    Patterns:
    - Chain: A → B → C (sequential)
    - Parallel: A + B + C (simultaneous)
    - Conditional: if A > threshold then B else C
    - Pipeline: A → fan-out → B, C, D → fan-in → E
    """
    
    def __init__(self, executor: ToolExecutor):
        self.executor = executor
    
    def chain(self, steps: List[Dict], shared_context: Dict = None) -> Dict:
        """
        Execute tools in chain
        Each tool's output becomes next tool's input
        """
        context = shared_context or {}
        
        for i, step in enumerate(steps):
            tool_name = step["tool"]
            input_mapping = step.get("input_mapping", {})
            
            # Map inputs from context
            params = {}
            for param_name, source_key in input_mapping.items():
                params[param_name] = context.get(source_key, source_key)
            
            # Merge with static params
            params.update(step.get("params", {}))
            
            result = self.executor.execute(tool_name, params)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Chain broke at step {i+1} ({tool_name}): {result.get('error')}",
                    "partial_results": context,
                }
            
            # Store result in context
            output_key = step.get("output_key", f"step_{i+1}_result")
            context[output_key] = result["result"]
        
        return {"success": True, "results": context}
    
    def parallel(self, tasks: List[Dict]) -> Dict:
        """
        Execute tools in parallel
        All tools run simultaneously, results collected
        """
        results = self.executor.execute_batch(tasks)
        
        return {
            "success": all(r["success"] for r in results),
            "results": results,
            "total": len(results),
            "succeeded": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
        }
    
    def conditional(self, condition_tool: str, condition_params: Dict,
                    condition_check: Callable,
                    true_branch: List[Dict], 
                    false_branch: List[Dict] = None) -> Dict:
        """
        Execute tool conditionally
        
        1. Execute condition_tool
        2. Check result with condition_check function
        3. Execute true_branch or false_branch
        """
        # Execute condition
        condition_result = self.executor.execute(condition_tool, condition_params)
        
        if not condition_result["success"]:
            return {"success": False, "error": "Condition tool failed"}
        
        # Evaluate condition
        branch = true_branch if condition_check(condition_result["result"]) else (false_branch or [])
        
        # Execute branch
        if branch:
            return self.chain(branch, {"condition_result": condition_result["result"]})
        
        return {"success": True, "results": {"condition_result": condition_result["result"]}}
    
    def pipeline(self, stages: List[Dict]) -> Dict:
        """
        Fan-out / Fan-in pipeline
        
        Stage format:
        {
            "name": "stage_name",
            "tools": [{"tool": "name", "params": {...}}],
            "aggregator": "merge" | "first" | "all"
        }
        """
        results = {}
        
        for stage in stages:
            stage_name = stage["name"]
            tools = stage["tools"]
            aggregator = stage.get("aggregator", "merge")
            
            # Fan-out: execute all tools
            stage_results = self.executor.execute_batch(tools)
            
            # Fan-in: aggregate results
            if aggregator == "merge":
                results[stage_name] = [
                    r["result"] for r in stage_results if r["success"]
                ]
            elif aggregator == "first":
                for r in stage_results:
                    if r["success"]:
                        results[stage_name] = r["result"]
                        break
            elif aggregator == "all":
                results[stage_name] = all(r["success"] for r in stage_results)
        
        return {"success": True, "results": results}
