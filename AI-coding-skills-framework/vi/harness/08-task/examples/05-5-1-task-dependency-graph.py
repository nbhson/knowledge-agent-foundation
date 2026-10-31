from collections import defaultdict, deque
from typing import List, Dict, Set, Optional

class TaskDependencyGraph:
    """
    Directed Acyclic Graph (DAG) cho task dependencies.
    
    Features:
    - Thêm/bỏ dependencies
    - Topological sort (execution order)
    - Parallel groups (tasks chạy cùng lúc)
    - Cycle detection
    """
    
    def __init__(self):
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
        for dep_id in task.dependencies:
            self.adj[dep_id].add(task.id)
    
    def has_cycle(self) -> bool:
        """DFS-based cycle detection"""
        visited = set()
        in_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in in_stack:
                    return True
            in_stack.discard(node)
            return False
        
        return any(dfs(t) for t in self.tasks if t not in visited)
    
    def topological_sort(self) -> List[str]:
        """Trả về execution order (topological sort)"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in task dependencies")
        
        return order
    
    def parallel_groups(self) -> List[List[str]]:
        """Tách thành các nhóm có thể chạy song song"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        groups = []
        remaining = dict(in_degree)
        
        while remaining:
            ready = [t for t, d in remaining.items() if d == 0]
            if not ready:
                raise ValueError("Unresolvable dependency cycle")
            
            groups.append(ready)
            
            for task_id in ready:
                del remaining[task_id]
                for neighbor in self.adj[task_id]:
                    if neighbor in remaining:
                        remaining[neighbor] -= 1
        
        return groups
