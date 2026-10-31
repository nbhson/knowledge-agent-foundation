class ToolLearner:
    """
    Agent learns which tools work best for which tasks
    
    Based on execution history, learns:
    - Tool preference per task type
    - Parameter patterns
    - Failure modes
    """
    
    def __init__(self):
        self.history: List[Dict] = []
        self.tool_scores: Dict[str, Dict] = {}
    
    def record(self, task_type: str, tool_name: str, 
               params: Dict, success: bool, latency_ms: float):
        """Record a tool usage"""
        self.history.append({
            "task_type": task_type,
            "tool": tool_name,
            "params": params,
            "success": success,
            "latency_ms": latency_ms,
            "timestamp": datetime.now().isoformat(),
        })
        
        # Update scores
        key = f"{task_type}:{tool_name}"
        if key not in self.tool_scores:
            self.tool_scores[key] = {"success_count": 0, "total_count": 0, "avg_latency": 0}
        
        score = self.tool_scores[key]
        score["total_count"] += 1
        if success:
            score["success_count"] += 1
        score["avg_latency"] = (
            0.1 * latency_ms + 0.9 * score["avg_latency"]
        )
    
    def recommend(self, task_type: str, available_tools: List[str]) -> List[str]:
        """Recommend tools for a task type based on history"""
        scored = []
        
        for tool in available_tools:
            key = f"{task_type}:{tool}"
            score = self.tool_scores.get(key, {"success_count": 0, "total_count": 0})
            
            if score["total_count"] > 0:
                success_rate = score["success_count"] / score["total_count"]
                # Penalize high latency
                latency_penalty = min(score["avg_latency"] / 1000, 1)
                final_score = success_rate * (1 - latency_penalty)
            else:
                final_score = 0.5  # Unknown = medium score
            
            scored.append((final_score, tool))
        
        scored.sort(reverse=True)
        return [tool for _, tool in scored]
