from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HIERARCHICAL = "hierarchical"
    ITERATIVE = "iterative"
    DAG = "dag"

@dataclass
class Task:
    id: str
    name: str
    description: str
    task_type: TaskType = TaskType.SEQUENTIAL
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List['Task'] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    max_retries: int = 3
    retry_count: int = 0
    timeout_seconds: int = 300
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    token_budget: Optional[int] = None  # Token limit for this task
    tools_allowed: List[str] = field(default_factory=list)  # Tools allowed to use
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "type": self.task_type.value,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "dependencies": self.dependencies,
            "retry_count": self.retry_count,
            "token_budget": self.token_budget,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }
    
    def mark_completed(self, result):
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now().isoformat()
    
    def mark_failed(self, error):
        self.status = TaskStatus.FAILED
        self.error = error
    
    def can_retry(self):
        return self.retry_count < self.max_retries
    
    def can_execute(self, completed_tasks: set):
        """Check if all dependencies are satisfied"""
        return all(dep in completed_tasks for dep in self.dependencies)

class TaskPlanner:
    """
    LLM-based task planner
    
    Analyzes a big task and splits it into sub-tasks
    Supports: hierarchical decomposition, dependency detection, complexity estimation
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def decompose(self, task_description, max_depth=3, current_depth=0):
        """
        Analyze a task and split it into sub-tasks
        
        Strategy:
        - depth 0-1: Broad decomposition (major phases)
        - depth 2+: Fine-grained decomposition (specific actions)
        """
        if current_depth >= max_depth:
            return [Task(
                id=f"leaf_{current_depth}",
                name=task_description[:50],
                description=task_description,
            )]
        
        if self.llm:
            prompt = f"""Analyze the following task and split it into sub-tasks:

Task: {task_description}
Depth: {current_depth}/{max_depth}

Rules:
- Each sub-task must be concrete and actionable
- Identify dependencies between sub-tasks
- Evaluate the type (sequential/parallel/conditional)
- Estimate the token budget for each sub-task
- List the tools needed for each sub-task

Output JSON:
{{
  "analysis": "Task analysis",
  "subtasks": [
    {{
      "name": "...",
      "description": "...",
      "type": "sequential|parallel|conditional",
      "dependencies": [],
      "estimated_tokens": 5000,
      "required_tools": ["tool1", "tool2"]
    }}
  ],
  "estimated_steps": 3
}}"""
            
            response = self.llm(prompt)
            try:
                import json
                data = json.loads(response)
                tasks = []
                for i, st in enumerate(data.get("subtasks", [])):
                    task_type_map = {
                        "sequential": TaskType.SEQUENTIAL,
                        "parallel": TaskType.PARALLEL,
                        "conditional": TaskType.CONDITIONAL,
                    }
                    task = Task(
                        id=f"task_{current_depth}_{i}",
                        name=st["name"],
                        description=st["description"],
                        task_type=task_type_map.get(st.get("type", "sequential"), TaskType.SEQUENTIAL),
                        dependencies=st.get("dependencies", []),
                        token_budget=st.get("estimated_tokens"),
                        tools_allowed=st.get("required_tools", []),
                    )
                    tasks.append(task)
                return tasks
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Fallback reaction: simple task decomposition
        return [Task(
            id=f"task_{current_depth}_0",
            name=task_description[:50],
            description=task_description,
        )]
    
    def create_execution_plan(self, root_task):
        """
        Create an execution plan from the task tree
        
        Returns: Ordered list of tasks to execute with dependency info
        """
        plan = []
        self._traverse(root_task, plan)
        return plan
    
    def _traverse(self, task, plan):
        """DFS traversal to create execution order"""
        if task.task_type == TaskType.SEQUENTIAL:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.PARALLEL:
            plan.append(task)  # Parallel marker
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.ITERATIVE:
            task.metadata["max_iterations"] = 5
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        else:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
    
    def estimate_complexity(self, task):
        """
        Evaluate the complexity of a task
        
        Returns: Score 1-10 with detailed breakdown
        """
        depth = self._get_depth(task)
        breadth = self._get_breadth(task)
        
        # Advanced scoring
        score = min(10, depth * 2 + breadth)
        
        # Estimate Tokens
        estimated_tokens = self._estimate_tokens(task)
        
        # Recommended strategy
        if score <= 3:
            strategy = "direct"
            reasoning = "Simple task, execute directly"
        elif score <= 6:
            strategy = "sequential"
            reasoning = "Medium task, split sequentially"
        else:
            strategy = "hierarchical"
            reasoning = "Complex task, needs multi-level hierarchy"
        
        return {
            "score": score,
            "depth": depth,
            "total_subtasks": breadth,
            "complexity": "simple" if score <= 3 else "medium" if score <= 6 else "complex",
            "estimated_tokens": estimated_tokens,
            "recommended_strategy": strategy,
            "reasoning": reasoning,
        }
    
    def _get_depth(self, task, current=0):
        if not task.subtasks:
            return current
        return max(self._get_depth(s, current + 1) for s in task.subtasks)
    
    def _get_breadth(self, task):
        count = 1
        for sub in task.subtasks:
            count += self._get_breadth(sub)
        return count
    
    def _estimate_tokens(self, task):
        """Estimate the number of tokens needed"""
        base_tokens = len(task.description.split()) * 2  # Rough estimate
        for sub in task.subtasks:
            base_tokens += self._estimate_tokens(sub)
        return base_tokens
