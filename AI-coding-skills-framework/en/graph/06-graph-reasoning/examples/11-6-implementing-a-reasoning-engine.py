from typing import List, Dict, Set, Optional
from collections import deque
import networkx as nx

class GraphReasoningEngine:
    """
    A reasoning engine on the Knowledge Graph.
    Supports: traversal, path finding, rule inference, temporal.
    """
    
    def __init__(self, graph: nx.DiGraph, rules: Optional[List[Dict]] = None):
        self.graph = graph
        self.rules = rules or []
    
    def traverse(
        self, start: str, max_hops: int = 3,
        edge_types: Optional[Set[str]] = None,
        min_confidence: float = 0.0,
    ) -> List[Dict]:
        return constrained_bfs(self.graph, start, max_hops, edge_types, min_confidence=min_confidence)
    
    def find_path(self, source: str, target: str, max_hops: int = 4) -> Optional[Dict]:
        try:
            path = nx.shortest_path(self.graph, source, target)
            if len(path) - 1 > max_hops:
                return None
            evidence = []
            for i in range(len(path) - 1):
                edata = self.graph.get_edge_data(path[i], path[i+1])
                evidence.append(f"({path[i]}) -[{edata.get('type')}]→ ({path[i+1]})")
            return {"path": path, "evidence": evidence, "hops": len(path) - 1}
        except nx.NetworkXNoPath:
            return None
    
    def find_all_paths(self, source: str, target: str, max_hops: int = 4) -> List[Dict]:
        try:
            paths = list(nx.all_simple_paths(self.graph, source, target, cutoff=max_hops))
            return [{"path": p, "hops": len(p) - 1} for p in paths]
        except:
            return []
    
    def infer(self) -> List[Dict]:
        """Run all the rules to infer new edges."""
        return apply_rules(self.graph, self.rules)
    
    def answer_with_reasoning(self, query: str) -> Dict:
        """
        Answer a question with a reasoning chain.
        Example: "Does anyone on Alice's team work on AI?"
        """
        # Parse the query (simplified — production uses an LLM to parse)
        # Assume: start=Alice, relation=team, target_domain=AI
        results = self.traverse("Alice", max_hops=3, edge_types={"MANAGES", "WORKS_ON"})
        
        # Filter: who works on a project with domain AI
        ai_workers = []
        for r in results:
            target = r["target"]
            node_data = self.graph.nodes.get(target, {})
            if node_data.get("domain") == "AI" or "AI" in target:
                ai_workers.append(r)
        
        # Add inferred results
        inferred = self.infer()
        
        return {
            "query": query,
            "traversal_results": results,
            "ai_workers": ai_workers,
            "inferred": inferred,
            "answer": f"Alice's team has {len(ai_workers)} people working on AI" if ai_workers else "Not found",
        }

# Usage
G = nx.DiGraph()
G.add_node("Alice", type="Person")
G.add_node("Bob", type="Person")
G.add_node("Carol", type="Person")
G.add_node("Phoenix", type="Project", domain="Finance")
G.add_node("Atlas", type="Project", domain="AI")
G.add_edges_from([
    ("Alice", "Bob", {"type": "MANAGES", "confidence": 0.95}),
    ("Bob", "Phoenix", {"type": "WORKS_ON", "confidence": 0.85}),
    ("Alice", "Carol", {"type": "MANAGES", "confidence": 0.90}),
    ("Carol", "Atlas", {"type": "WORKS_ON", "confidence": 0.92}),
])

engine = GraphReasoningEngine(G, rules=INFERENCE_RULES)
print(engine.find_path("Alice", "Atlas"))
print(engine.answer_with_reasoning("Does anyone on Alice's team work on AI?"))
