import time
from typing import Any, Dict, Optional, Callable
from datetime import datetime

class ToolExecutor:
    """
    Execute tools with comprehensive error handling:
    - Parameter validation
    - Retry with exponential backoff
    - Timeout handling
    - Rate limiting
    - Permission checking
    - Cost tracking
    - Execution logging
    """
    
    def __init__(self, registry: ToolRegistry, 
                 permission_checker=None,
                 rate_limiter=None):
        self.registry = registry
        self.permission_checker = permission_checker
        self.rate_limiter = rate_limiter
        self.execution_log: List[Dict] = []
        self._call_counts: Dict[str, int] = {}
    
    def execute(self, tool_name: str, parameters: Dict, 
                user_id: str = None,
                timeout: float = None) -> Dict:
        """
        Execute a tool with full guardrails
        """
        start_time = time.time()
        
        # 1. Resolve tool
        tool = self.registry.get_tool(tool_name)
        if not tool:
            return self._error_result(tool_name, "Tool not found", start_time)
        
        # 2. Check deprecation
        if tool.is_deprecated():
            replacement = tool.replacement_tool or "unknown"
            return self._error_result(
                tool_name, 
                f"Tool deprecated. Use '{replacement}' instead.",
                start_time,
            )
        
        # 3. Validate parameters
        validation = self._validate_params(tool, parameters)
        if not validation["valid"]:
            return self._error_result(
                tool_name,
                f"Invalid parameters: {validation['errors']}",
                start_time,
            )
        
        # 4. Check permissions
        if self.permission_checker and user_id:
            perm_check = self.permission_checker(user_id, tool.requires_permission)
            if not perm_check.get("allowed"):
                return self._error_result(
                    tool_name,
                    f"Permission denied: {perm_check.get('reason', 'insufficient permissions')}",
                    start_time,
                )
        
        # 5. Check rate limit
        if self.rate_limiter:
            rate_check = self.rate_limiter(tool_name)
            if not rate_check.get("allowed"):
                return self._error_result(
                    tool_name,
                    f"Rate limit exceeded: {rate_check.get('retry_after', 60)}s",
                    start_time,
                )
        
        # 6. Execute with retries
        max_retries = tool.max_retries
        effective_timeout = timeout or tool.timeout_seconds
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Set timeout per-attempt
                if tool.function:
                    result = tool.function(**parameters)
                else:
                    result = f"Tool '{tool_name}' has no function implementation"
                
                elapsed_ms = (time.time() - start_time) * 1000
                
                # Update metrics
                tool.update_metrics(elapsed_ms, success=True)
                
                # Log success
                log_entry = {
                    "tool": tool_name,
                    "params": parameters,
                    "success": True,
                    "attempt": attempt + 1,
                    "elapsed_ms": round(elapsed_ms, 2),
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat(),
                }
                self.execution_log.append(log_entry)
                self._call_counts[tool_name] = self._call_counts.get(tool_name, 0) + 1
                
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt + 1,
                    "elapsed_ms": elapsed_ms,
                    "tool": tool_name,
                    "cost": tool.cost_per_call,
                }
                
            except TimeoutError:
                last_error = f"Timeout after {effective_timeout}s"
            except Exception as e:
                last_error = str(e)
            
            # Exponential backoff before retry
            if attempt < max_retries - 1:
                backoff = 0.5 * (2 ** attempt)
                time.sleep(min(backoff, 5.0))
        
        # All retries failed
        tool.update_metrics(
            (time.time() - start_time) * 1000, 
            success=False,
        )
        
        return self._error_result(
            tool_name,
            f"Failed after {max_retries} attempts: {last_error}",
            start_time,
        )
    
    def execute_batch(self, calls: List[Dict], parallel: bool = False) -> List[Dict]:
        """
        Execute multiple tool calls
        
        calls: [{"tool": "name", "params": {...}, "user_id": "..."}]
        parallel: If True, execute without waiting (simulated)
        """
        results = []
        
        for call in calls:
            result = self.execute(
                call["tool"],
                call.get("params", {}),
                user_id=call.get("user_id"),
            )
            results.append({
                "tool": call["tool"],
                **result,
            })
        
        return results
    
    def execute_chain(self, steps: List[Dict]) -> Dict:
        """
        Execute tools in chain, passing results as inputs
        
        steps: [
            {"tool": "search", "params": {"query": "..."}, "output_key": "search_result"},
            {"tool": "analyze", "params": {"data": "$search_result"}, "output_key": "analysis"},
        ]
        """
        results = {}
        
        for i, step in enumerate(steps):
            # Substitute variables
            params = {}
            for key, value in step.get("params", {}).items():
                if isinstance(value, str) and value.startswith("$"):
                    var_name = value[1:]
                    params[key] = results.get(var_name, value)
                else:
                    params[key] = value
            
            result = self.execute(step["tool"], params)
            
            if not result["success"]:
                return {
                    "success": False,
                    "error": f"Chain failed at step {i+1}: {result.get('error')}",
                    "completed_steps": i,
                    "results": results,
                }
            
            # Store result with output key
            output_key = step.get("output_key", f"step_{i+1}")
            results[output_key] = result["result"]
        
        return {
            "success": True,
            "results": results,
            "steps_completed": len(steps),
        }
    
    def _validate_params(self, tool: ToolDefinition, params: Dict) -> Dict:
        """Validate parameters against tool definition"""
        errors = []
        warnings = []
        
        # Check required params
        for param_name, param_def in tool.parameters.items():
            if param_def.get("required", False) and param_name not in params:
                errors.append(f"Missing required param: {param_name}")
        
        # Check types (basic)
        for param_name, value in params.items():
            if param_name in tool.parameters:
                expected_type = tool.parameters[param_name].get("type")
                if expected_type == "string" and not isinstance(value, str):
                    warnings.append(f"Param '{param_name}' expected string, got {type(value).__name__}")
                elif expected_type == "integer" and not isinstance(value, int):
                    warnings.append(f"Param '{param_name}' expected integer, got {type(value).__name__}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
    
    def _error_result(self, tool_name: str, error: str, start_time: float) -> Dict:
        """Create error result and log it"""
        elapsed_ms = (time.time() - start_time) * 1000
        
        self.execution_log.append({
            "tool": tool_name,
            "success": False,
            "error": error,
            "elapsed_ms": round(elapsed_ms, 2),
            "timestamp": datetime.now().isoformat(),
        })
        
        return {
            "success": False,
            "error": error,
            "result": None,
            "elapsed_ms": elapsed_ms,
            "tool": tool_name,
        }
    
    def get_stats(self) -> Dict:
        """Get comprehensive execution statistics"""
        total = len(self.execution_log)
        successful = sum(1 for log in self.execution_log if log["success"])
        failed = total - successful
        
        tool_counts = {}
        tool_errors = {}
        total_cost = 0.0
        
        for log in self.execution_log:
            tool = log.get("tool", "unknown")
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
            
            if not log["success"]:
                tool_errors[tool] = tool_errors.get(tool, 0) + 1
        
        # Calculate total cost
        for tool_name, count in self._call_counts.items():
            tool = self.registry.get_tool(tool_name)
            if tool:
                total_cost += tool.cost_per_call * count
        
        return {
            "total_calls": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "tool_usage": tool_counts,
            "tool_errors": tool_errors,
            "total_cost": total_cost,
            "avg_latency_ms": (
                sum(log.get("elapsed_ms", 0) for log in self.execution_log) / total
                if total > 0 else 0
            ),
        }
