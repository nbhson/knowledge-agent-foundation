class HTNPlanner:
    """
    Hierarchical Task Network planning
    
    Unlike simple decomposition, HTN uses:
    - Primitive tasks (can be executed directly)
    - Compound tasks (need further decomposition)
    - Methods (ways to decompose compound tasks)
    """
    
    def __init__(self):
        self.methods = {}  # task_type -> list of task decomposition methods
        self.primitive_actions = {}  # action_name -> implementation
    
    def add_method(self, task_type, method):
        if task_type not in self.methods:
            self.methods[task_type] = []
        self.methods[task_type].append(method)
    
    def decompose(self, task, depth=0, max_depth=5):
        if depth >= max_depth:
            return [task]
        
        if task["type"] in self.methods:
            for method in self.methods[task["type"]]:
                if method["precondition"](task):
                    subtasks = method["decompose"](task)
                    result = []
                    for subtask in subtasks:
                        result.extend(self.decompose(subtask, depth + 1, max_depth))
                    return result
        
        return [task]  # Primitive task
    
    def execute_plan(self, plan):
        results = []
        for task in plan:
            if task["name"] in self.primitive_actions:
                result = self.primitive_actions[task["name"]](task)
                results.append({"task": task, "result": result})
        return results
