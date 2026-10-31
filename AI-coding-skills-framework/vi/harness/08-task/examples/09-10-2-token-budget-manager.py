class TokenBudgetManager:
    """
    Quản lý ngân sách token cho task execution.
    Prevents context overflow và optimizes token usage.
    """
    
    def __init__(self, total_budget: int = 128000):
        self.total_budget = total_budget
        self.allocated = {
            "system": 5000,
            "project_context": 0,
            "task_context": 0,
            "working_memory": 0,
        }
        self.min_reserve = 20000
    
    @property
    def remaining(self) -> int:
        used = sum(self.allocated.values())
        return self.total_budget - used - self.min_reserve
    
    @property
    def usage_percent(self) -> float:
        used = sum(self.allocated.values())
        return (used / self.total_budget) * 100
    
    def can_fit(self, estimated_tokens: int) -> bool:
        """Kiểm tra có đủ budget cho task không"""
        return self.remaining >= estimated_tokens
    
    def allocate_for_task(self, task: Task) -> bool:
        """Cấp budget cho task — trả False nếu không đủ"""
        needed = task.estimated_tokens or 2000
        if not self.can_fit(needed):
            return False
        
        self.allocated["task_context"] += needed
        return True
    
    def add_to_working_memory(self, tokens: int):
        """Thêm tokens vào working memory"""
        self.allocated["working_memory"] += tokens
    
    def summarize_context(self) -> str:
        """Tóm tắt tình trạng budget"""
        lines = [
            "=== Token Budget Status ===",
            f"Total:     {self.total_budget:,}",
            f"System:    {self.allocated['system']:,}",
            f"Project:   {self.allocated['project_context']:,}",
            f"Task:      {self.allocated['task_context']:,}",
            f"Working:   {self.allocated['working_memory']:,}",
            f"Reserve:   {self.min_reserve:,}",
            f"Remaining: {self.remaining:,}",
            f"Usage:     {self.usage_percent:.1f}%",
        ]
        
        if self.usage_percent > 80:
            lines.append("⚠️ WARNING: High context usage!")
        if self.remaining < 5000:
            lines.append("🚨 CRITICAL: Very low remaining budget!")
        
        return "\n".join(lines)
    
    def suggest_compaction(self) -> List[str]:
        """Gợi ý cách giảm token usage"""
        suggestions = []
        
        if self.allocated["working_memory"] > 30000:
            suggestions.append(
                "Summarize older working memory entries"
            )
        
        if self.allocated["project_context"] > 20000:
            suggestions.append(
                "Remove non-essential project files from context"
            )
        
        if self.usage_percent > 85:
            suggestions.append(
                "Complete current sub-task and start new session"
            )
        
        return suggestions
