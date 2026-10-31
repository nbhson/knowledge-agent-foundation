class DAGWorkflow:
    """
    Workflow based on a Dependency Graph (DAG).
    
    Allows independent nodes to run in parallel,
    and waits for dependencies to complete before proceeding.
    
    Example:
        A ──► C ──► E
        B ──► D ──► F
        
    A and B run in parallel → C waits for A, D waits for B → E waits for C, F waits for D
    """
    
    def __init__(self, name: str = "dag"):
        self.name = name
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, List[str]] = {}  # node -> [dependents]
        self.reverse_edges: Dict[str, List[str]] = {}  # node -> [dependencies]
        self.history = []
    
    def add_node(self, name: str, func: Callable, depends_on: List[str] = None):
        """Add a node with optional dependencies"""
        self.nodes[name] = {"func": func, "name": name}
        self.edges[name] = []
        self.reverse_edges[name] = depends_on or []
        
        for dep in (depends_on or []):
            if dep not in self.edges:
                self.edges[dep] = []
            self.edges[dep].append(name)
        
        return self
    
    def topological_sort(self) -> List[List[str]]:
        """
        Topological sort — returns a list of levels
        Each level contains nodes that can run in parallel
        """
        in_degree = {node: 0 for node in self.nodes}
        for node, deps in self.reverse_edges.items():
            for dep in deps:
                in_degree[node] += 1
        
        levels = []
        queue = [n for n, d in in_degree.items() if d == 0]
        
        while queue:
            levels.append(sorted(queue))
            next_queue = []
            for node in queue:
                for dependent in self.edges.get(node, []):
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_queue.append(dependent)
            queue = next_queue
        
        # Validate: check for cycles
        total_nodes = sum(len(level) for level in levels)
        if total_nodes != len(self.nodes):
            raise WorkflowError("Cycle detected in DAG!")
        
        return levels
    
    def run(self, initial_data: Any = None) -> Dict:
        """Execute DAG level by level"""
        levels = self.topological_sort()
        results = {}
        node_results = {}
        
        for level_idx, level in enumerate(levels):
            if len(level) == 1:
                # Single node — run directly
                node_name = level[0]
                deps = {dep: results[dep] for dep in self.reverse_edges[node_name] if dep in results}
                input_data = {**deps, "_original": initial_data} if deps else initial_data
                
                result = self.nodes[node_name]["func"](input_data)
                results[node_name] = result
                node_results[node_name] = {"status": "success", "level": level_idx}
            else:
                # Parallel level
                with ThreadPoolExecutor(max_workers=len(level)) as executor:
                    futures = {}
                    for node_name in level:
                        deps = {dep: results[dep] for dep in self.reverse_edges[node_name] if dep in results}
                        input_data = {**deps, "_original": initial_data} if deps else initial_data
                        future = executor.submit(self.nodes[node_name]["func"], input_data)
                        futures[future] = node_name
                    
                    for future in as_completed(futures):
                        node_name = futures[future]
                        try:
                            result = future.result()
                            results[node_name] = result
                            node_results[node_name] = {"status": "success", "level": level_idx}
                        except Exception as e:
                            node_results[node_name] = {"status": "failed", "error": str(e), "level": level_idx}
        
        return {
            "results": results,
            "node_status": node_results,
            "levels": levels,
            "total_nodes": len(self.nodes),
            "successful": sum(1 for v in node_results.values() if v["status"] == "success"),
        }
    
    def validate(self) -> Dict:
        """Validate DAG structure"""
        issues = []
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for dep in self.reverse_edges.get(node, []):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    issues.append(f"Cycle: {node} → {dep}")
                    return True
            rec_stack.discard(node)
            return False
        
        for node in self.nodes:
            if node not in visited:
                has_cycle(node)
        
        # Check for missing dependencies
        for node, deps in self.reverse_edges.items():
            for dep in deps:
                if dep not in self.nodes:
                    issues.append(f"Missing dependency: {dep} (required by {node})")
        
        # Check for orphan nodes
        all_deps = set()
        for deps in self.reverse_edges.values():
            all_deps.update(deps)
        roots = [n for n in self.nodes if n not in all_deps and not self.reverse_edges.get(n)]
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "roots": roots,
            "levels": len(self.topological_sort()),
        }
