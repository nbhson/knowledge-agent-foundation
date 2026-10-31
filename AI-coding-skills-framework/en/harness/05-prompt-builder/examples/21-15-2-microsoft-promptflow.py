# PromptFlow-style prompt management
class PromptFlow:
    """
    PromptFlow: Build, evaluate, deploy prompt flows
    
    Each flow is a DAG of prompt nodes
    """
    
    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[Tuple[str, str]] = []
    
    def add_node(self, name: str, prompt_template: str, node_type: str = "llm"):
        self.nodes[name] = {
            "template": prompt_template,
            "type": node_type,
        }
    
    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))
    
    def execute(self, inputs: Dict) -> Dict:
        """Execute flow topologically"""
        # Topological sort
        order = self._topological_sort()
        
        outputs = {}
        for node_name in order:
            node = self.nodes[node_name]
            # Substitute inputs and previous outputs
            context = {**inputs, **outputs}
            prompt = node["template"]
            for key, value in context.items():
                prompt = prompt.replace(f"{{{key}}}", str(value))
            outputs[node_name] = {"prompt": prompt, "node": node}
        
        return outputs
    
    def _topological_sort(self) -> List[str]:
        """Sort nodes in dependency order"""
        in_degree = {n: 0 for n in self.nodes}
        for from_node, to_node in self.edges:
            in_degree[to_node] += 1
        
        queue = [n for n, d in in_degree.items() if d == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            for from_n, to_n in self.edges:
                if from_n == node:
                    in_degree[to_n] -= 1
                    if in_degree[to_n] == 0:
                        queue.append(to_n)
        
        return result
