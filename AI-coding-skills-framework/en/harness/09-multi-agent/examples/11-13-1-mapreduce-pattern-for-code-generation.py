from typing import Dict, List, Callable

class MapReduceCodeGenerator:
    """
    MapReduce pattern applied to code generation.
    
    MAP: Split the task into sub-tasks → each agent processes one sub-task
    REDUCE: Merge results from all agents into a final output
    
    Pros:
    - Speed: sub-tasks run in parallel
    - Scalability: more agents = more throughput
    - Quality: each agent focuses on one part
    
    Cons:
    - Merging results can be complex
    - Not suitable for tasks with high dependency
    """
    
    def __init__(self):
        self.mapper_agents: List[Dict] = []
        self.reducer_agent: Dict = {}
        self.merge_strategy: str = "concatenate"
    
    def map_reduce(self, task: Dict, 
                   map_func: Callable,
                   reduce_func: Callable) -> Dict:
        """
        Execute the MapReduce pattern.
        
        task: {
            "description": str,
            "subtasks": [{"id": str, "input": Dict}],
        }
        """
        # MAP PHASE
        map_results = []
        for subtask in task["subtasks"]:
            result = map_func(subtask)
            map_results.append({
                "subtask_id": subtask["id"],
                "result": result,
            })
        
        # REDUCE PHASE
        reduced = reduce_func(map_results)
        
        return {
            "map_results": map_results,
            "final_output": reduced,
            "subtasks_completed": len(map_results),
        }
    
    def parallel_code_generation(self, modules: List[Dict],
                                  coder_func: Callable) -> Dict:
        """
        Generate code for multiple modules in parallel.
        
        modules: [{"name": "auth", "spec": "..."}, 
                  {"name": "api", "spec": "..."},
                  {"name": "db", "spec": "..."}]
        """
        # MAP: Each coder generates one module
        results = []
        for module in modules:
            code = coder_func(module)
            results.append({
                "module": module["name"],
                "code": code,
                "lines": len(code.split("\n")),
            })
        
        # REDUCE: Merge all modules
        merged_code = self._merge_modules(results)
        
        # Generate imports/connectors
        imports = self._generate_imports(results)
        
        return {
            "modules": results,
            "merged_code": merged_code,
            "imports": imports,
            "total_lines": sum(r["lines"] for r in results),
        }
    
    def _merge_modules(self, results: List[Dict]) -> str:
        """Merge code from multiple modules"""
        parts = []
        for r in results:
            parts.append(f"# === Module: {r['module']} ===")
            parts.append(r["code"])
            parts.append("")
        return "\n".join(parts)
    
    def _generate_imports(self, results: List[Dict]) -> str:
        """Automatically generate import statements"""
        module_names = [r["module"] for r in results]
        imports = []
        for name in module_names:
            imports.append(f"from .{name} import *")
        return "\n".join(imports)
