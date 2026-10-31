from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class PriorityScore:
    """Computed priority score — Eisenhower Matrix + dependency bonus"""
    urgency: int        # 1-5: urgency level
    importance: int     # 1-5: importance level
    effort: int         # 1-5: required effort (lower = higher score)
    dependency_count: int  # Number of tasks that depend on this task
    
    @property
    def total(self) -> float:
        """Weighted score with quick-wins bonus"""
        base = self.urgency * 0.4 + self.importance * 0.4
        effort_bonus = (6 - self.effort) * 0.1   # Quick wins bonus
        dep_bonus = min(self.dependency_count * 0.1, 0.3)
        return base + effort_bonus + dep_bonus


class TaskScheduler:
    """
    Schedule tasks based on priority, dependencies, and token budget.
    
    Rules:
    1. Always do tasks with many dependents first
    2. Quick wins (low effort, high priority) should be done first
    3. Respect token budget per session
    """
    
    def __init__(self, max_tokens_per_session: int = 50000):
        self.max_tokens = max_tokens_per_session
    
    def schedule(self, tasks: List[Task]) -> List[List[Task]]:
        """
        Create an execution schedule — returns a list of batches.
        Each batch is a group of tasks that can run at the same time.
        """
        # Sort by priority score descending
        scored = [(t, self._score(t)) for t in tasks]
        scored.sort(key=lambda x: x[1].total, reverse=True)
        
        batches = []
        current_batch = []
        current_tokens = 0
        
        for task, score in scored:
            task_tokens = task.estimated_tokens or 1000
            
            if current_tokens + task_tokens > self.max_tokens:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [task]
                current_tokens = task_tokens
            else:
                current_batch.append(task)
                current_tokens += task_tokens
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _score(self, task: Task) -> PriorityScore:
        """Compute the priority score for a task"""
        effort = task.complexity.value
        urgency = max(1, 6 - task.priority)
        
        importance_map = {
            TaskCategory.MODIFICATION: 5,   # Bug fix = high
            TaskCategory.TESTING: 4,
            TaskCategory.GENERATION: 3,
            TaskCategory.ANALYSIS: 3,
            TaskCategory.DOCUMENTATION: 2,
        }
        importance = importance_map.get(task.category, 3)
        
        return PriorityScore(
            urgency=urgency,
            importance=importance,
            effort=effort,
            dependency_count=len(task.dependencies),
        )
