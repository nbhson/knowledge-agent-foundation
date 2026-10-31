from typing import List, Dict, Tuple

# Định nghĩa rules dạng: IF pattern THEN new_edge
INFERENCE_RULES = [
    {
        "name": "transitive_manages",
        "pattern": [("A", "MANAGES", "B"), ("B", "MANAGES", "C")],
        "infer": ("A", "INDIRECTLY_MANAGES", "C"),
        "confidence": 0.8,  # suy diễn có độ tin cậy thấp hơn fact gốc
        "description": "Nếu A quản lý B và B quản lý C → A gián tiếp quản lý C"
    },
    {
        "name": "works_on_implies_team",
        "pattern": [("A", "MANAGES", "B"), ("B", "WORKS_ON", "P")],
        "infer": ("A", "OVERSEES", "P"),
        "confidence": 0.75,
        "description": "Nếu A quản lý B và B làm trên P → A giám sát P"
    },
    {
        "name": "belongs_approved",
        "pattern": [("D", "BELONGS_TO", "P"), ("A", "APPROVES", "D")],
        "infer": ("A", "APPROVES_PROJECT", "P"),
        "confidence": 0.90,
    },
]

def apply_rules(graph: nx.DiGraph, rules: List[Dict]) -> List[Dict]:
    """Áp dụng rules để suy ra edges mới."""
    inferred = []
    
    for rule in rules:
        pattern = rule["pattern"]
        infer = rule["infer"]
        
        if len(pattern) == 2:
            # 2-hop pattern: A -[R1]-> B -[R2]-> C
            (a_var, r1, b_var), (b_var2, r2, c_var) = pattern
            assert b_var == b_var2, "Biến trung gian phải khớp"
            
            for a in graph.nodes():
                for b in graph.successors(a):
                    if graph.get_edge_data(a, b).get("type") != r1:
                        continue
                    for c in graph.successors(b):
                        if graph.get_edge_data(b, c).get("type") != r2:
                            continue
                        # Suy ra: A -[infer]-> C
                        inferred.append({
                            "source": a, "target": c,
                            "type": infer[1],
                            "rule": rule["name"],
                            "confidence": rule["confidence"],
                            "evidence": [f"{a} -[{r1}]→ {b}", f"{b} -[{r2}]→ {c}"],
                        })
    
    return inferred

# Usage
G = nx.DiGraph()
G.add_node("Alice", type="Person")
G.add_node("Bob", type="Person")
G.add_node("Carol", type="Person")
G.add_node("Phoenix", type="Project")
G.add_edges_from([
    ("Alice", "Bob", {"type": "MANAGES"}),
    ("Bob", "Carol", {"type": "MANAGES"}),
    ("Bob", "Phoenix", {"type": "WORKS_ON"}),
])

inferred = apply_rules(G, INFERENCE_RULES)
for inf in inferred:
    print(f"Inferred: {inf['source']} -[{inf['type']}]→ {inf['target']} via {inf['rule']}")
    print(f"  Evidence: {' + '.join(inf['evidence'])} (conf={inf['confidence']})")
# Inferred: Alice -[INDIRECTLY_MANAGES]→ Carol via transitive_manages
# Inferred: Alice -[OVERSEES]→ Phoenix via works_on_implies_team
