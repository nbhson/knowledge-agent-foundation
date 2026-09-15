# 🧩 06. Graph Reasoning — Reasoning Over Graphs

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Does Graph Reasoning Matter?](#why-does-graph-reasoning-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Traversal Strategies](#1-traversal-strategies)
> - [2. Path Finding](#2-path-finding)
> - [3. Inference Rules & Reasoning](#3-inference-rules--reasoning)
> - [4. Community Detection & Centrality](#4-community-detection--centrality)
> - [5. Temporal Reasoning](#5-temporal-reasoning)
> - [6. Implementing a Reasoning Engine](#6-implementing-a-reasoning-engine)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have a Knowledge Graph:

```
Alice —[MANAGES]→ Bob —[WORKS_ON]→ Phoenix
  │
  └──[KNOWS]→ Carol —[WORKS_ON]→ Atlas (AI Platform)
```

You ask: *"Does anyone on Alice's team work on AI?"*

This is **not** a lookup question — it is **reasoning**:

1. Is `MANAGES` transitive? Alice manages Bob — is Bob in "Alice's team"?
2. Does `WORKS_ON → Atlas` count as "working on AI"? Does Atlas have the property `domain: AI`?
3. Do I need to traverse `Alice → Bob → Phoenix → Atlas` (3 hops) to connect them?

**Graph Reasoning** turns these vague questions into **executable logic**: rules, path constraints, and inference chains that can be verified.

### Why Does Graph Reasoning Matter?

> *"Retrieval finds facts. Reasoning connects them into answers you didn't know to ask for."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **HotpotQA Benchmark** | Multi-hop reasoning on a graph increases **accuracy by 27%** vs single-hop retrieval |
| 2 | **Neo4j GDS (2024)** | Shortest path + centrality helps find **bottleneck persons**, reducing approval time by 40% |
| 3 | **Temporal KG Papers (2024)** | Temporal reasoning cuts **stale answers by 35%** (answering with expired information) |

---

## Overview

```
Knowledge Graph
    │
    ├──► Traversal (BFS/DFS, constrained)
    │      "Find all nodes 2 hops from Alice through MANAGES/WORKS_ON"
    │
    ├──► Path Finding (shortest, all-paths, weighted)
    │      "Shortest path from Bob to an AI project?"
    │
    ├──► Inference (rules, transitivity, composition)
    │      "If A MANAGES B and B WORKS_ON P → A INDIRECTLY_MANAGES P"
    │
    ├──► Community & Centrality
    │      "Who is the most important person in the org?"
    │
    └──► Temporal (valid_from/until, event ordering)
           "Who managed the AI team in Q2/2024?"
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Traversal](#1-traversal-strategies) | BFS, DFS, constrained traversal, sampling |
| 2 | [Path Finding](#2-path-finding) | Shortest path, all paths, weighted, k-shortest |
| 3 | [Inference](#3-inference-rules--reasoning) | Rules, transitivity, composition, OWL-lite |
| 4 | [Community & Centrality](#4-community-detection--centrality) | Leiden, Louvain, PageRank, betweenness |
| 5 | [Temporal](#5-temporal-reasoning) | Time-aware traversal, versioning, expiration |
| 6 | [Engine](#6-implementing-a-reasoning-engine) | Complete reasoning engine code |
| 7 | [Neuro-Symbolic QA](#7-neuro-symbolic-qa--combining-llm--graph-traversal) | Think-on-Graph, KG-Agent, Planner-Executor-Reasoner |

---

## 1. Traversal Strategies

> **📌 Core Concept:**
> **Traversal = "walking through" a graph** — start from one node and visit the others one by one according to the relationships. Like "following" someone on a social network: start from yourself, look at your friends → then look at your friends' friends → continue...
>
> **3 walking styles:**
> - **BFS (Breadth-First)** = "go in circles" — visit all nodes 1 hop away, then 2 hops, then 3 hops... **Analogy: flood fill** (pouring water on a network — water spreads evenly before going deeper)
> - **DFS (Depth-First)** = "finish one branch first" — follow one path as deep as possible, backtrack, then take the next path. **Analogy: walking a single road** (walk one road to the end before turning back)
> - **Constrained** = BFS/DFS with conditions — only go through nodes/edges that satisfy the conditions (e.g. only through `MANAGES` edges, only to Person nodes)

### 1.1 BFS vs DFS vs Constrained

```
Graph: Alice → Bob → Carol
         │      │
         └────→ Dave → Eve

BFS from Alice (level-order):       DFS from Alice (depth-first):
  Level 0: Alice                    Path 1: Alice → Bob → Carol (dead end, backtrack)
  Level 1: Bob, Dave                Path 2: Alice → Bob → Dave → Eve
  Level 2: Carol, Eve

Constrained BFS (only through MANAGES):
  Alice —[MANAGES]→ Bob —[MANAGES]→ Carol  ✅
  Alice —[KNOWS]→ Dave                     ❌ (filtered out)
```

**When to choose BFS, DFS?**
| Situation | Choose | Reason |
|-----------|------|-------|
| Want all nodes 1-2 hops away | **BFS** | Guarantees finding everything before going deep |
| Want the shortest path | **BFS** | BFS always finds the shortest path first |
| Want any path, check existence | **DFS** | Faster than BFS for an existence check |
| Large graph, need to limit nodes visited | **Sampled BFS** | BFS with sampling, doesn't visit everything |
| Only need nodes satisfying a condition | **Constrained BFS** | Combines BFS + filtering |

<details>
<summary>Python Code — Constrained Traversal (Click to view)</summary>

```python
from collections import deque
import networkx as nx
from typing import List, Set, Optional

def constrained_bfs(
    graph: nx.DiGraph,
    start: str,
    max_hops: int = 3,
    allowed_edge_types: Optional[Set[str]] = None,
    allowed_node_types: Optional[Set[str]] = None,
    min_confidence: float = 0.0,
) -> List[dict]:
    """
    Constrained BFS — only goes through edges/nodes that satisfy the conditions.
    
    Example: only through MANAGES/WORKS_ON, confidence >= 0.7
    """
    visited = set([start])
    queue = deque([(start, 0, [start])])  # (node, hops, path)
    results = []
    
    while queue:
        current, hops, path = queue.popleft()
        
        if hops >= max_hops:
            continue
        
        for neighbor in graph.successors(current):
            if neighbor in visited:
                continue
            
            edge_data = graph.get_edge_data(current, neighbor)
            edge_type = edge_data.get("type", "")
            
            # Filter edge type
            if allowed_edge_types and edge_type not in allowed_edge_types:
                continue
            
            # Filter confidence
            if edge_data.get("confidence", 1.0) < min_confidence:
                continue
            
            # Filter node type
            if allowed_node_types:
                node_type = graph.nodes[neighbor].get("type", "")
                if node_type not in allowed_node_types:
                    continue
            
            new_path = path + [neighbor]
            results.append({
                "target": neighbor,
                "hops": hops + 1,
                "path": new_path,
                "edges": [(path[i], path[i+1], graph.get_edge_data(path[i], path[i+1]).get("type"))
                          for i in range(len(new_path) - 1)],
                "confidence": min(graph.get_edge_data(new_path[i], new_path[i+1]).get("confidence", 1.0)
                                  for i in range(len(new_path) - 1)),
            })
            
            visited.add(neighbor)
            queue.append((neighbor, hops + 1, new_path))
    
    return results

# Usage
G = nx.DiGraph()
G.add_node("Alice", type="Person")
G.add_node("Bob", type="Person")
G.add_node("Carol", type="Person")
G.add_node("Phoenix", type="Project")
G.add_node("Dave", type="Person")
G.add_edges_from([
    ("Alice", "Bob", {"type": "MANAGES", "confidence": 0.95}),
    ("Bob", "Carol", {"type": "MANAGES", "confidence": 0.90}),
    ("Bob", "Phoenix", {"type": "WORKS_ON", "confidence": 0.85}),
    ("Alice", "Dave", {"type": "KNOWS", "confidence": 0.60}),
])

# Only through MANAGES/WORKS_ON, confidence >= 0.7
results = constrained_bfs(G, "Alice", max_hops=3, 
                           allowed_edge_types={"MANAGES", "WORKS_ON"},
                           min_confidence=0.7)
for r in results:
    print(f"  {r['path']} (hops={r['hops']}, conf={r['confidence']:.2f})")
# ['Alice', 'Bob'] (hops=1, conf=0.95)
# ['Alice', 'Bob', 'Carol'] (hops=2, conf=0.90)
# ['Alice', 'Bob', 'Phoenix'] (hops=2, conf=0.85)
# Dave is excluded because KNOWS is not in the allowed types
```

</details>

### 1.2 Sampling for Large Graphs

On graphs of 1M+ nodes, you can't traverse the whole thing:

```python
import random

def sampled_traversal(
    graph: nx.Graph,
    start: str,
    max_hops: int = 2,
    max_neighbors_per_hop: int = 10,
    sample_strategy: str = "random",  # random | top-confidence | pagerank
) -> List[dict]:
    """Sampled traversal — limits the number of neighbors per hop."""
    visited = set([start])
    current_level = [start]
    all_results = []
    
    for hop in range(max_hops):
        next_level = []
        for node in current_level:
            neighbors = list(graph.neighbors(node))
            
            # Sample if there are too many neighbors
            if len(neighbors) > max_neighbors_per_hop:
                if sample_strategy == "random":
                    neighbors = random.sample(neighbors, max_neighbors_per_hop)
                elif sample_strategy == "top-confidence":
                    neighbors.sort(key=lambda n: graph.get_edge_data(node, n).get("confidence", 0), reverse=True)
                    neighbors = neighbors[:max_neighbors_per_hop]
            
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb)
                    next_level.append(nb)
                    all_results.append({"node": nb, "hops": hop + 1, "via": node})
        
        current_level = next_level
        if not current_level:
            break
    
    return all_results
```

---

## 2. Path Finding

> **📌 Core Concept:**
> **Path Finding = finding "a route" connecting two nodes in a graph.** Like Google Maps: from point A to point B there may be many different routes, and you want the optimal one by some criterion (fewest steps, fastest, most reliable).
>
> **When do agents need it?**
> - "How can I reach Alice through whom?" → shortest path Alice → Bob (shared boss)
> - "How many ways can Bob approach Project Atlas?" → all paths, limited to 4 hops
> - "Find the most trustworthy path (high confidence)" → weighted shortest path using confidence as the weight

### 2.1 The Kinds of Path Finding

> **Read this table this way:** each kind answers a different question — *the same data, but a different "meaning of the path"*.

```
┌────────────────────┬──────────────────────────────────┬──────────────────┐
│ Kind               │ Answers the question             │ Cypher / NetworkX│
├────────────────────┼──────────────────────────────────┼──────────────────┤
│ Shortest Path      │ "Which path has the fewest steps?"│ shortestPath() / nx.shortest_path │
│ All Paths          │ "What paths exist (≤N hops)?"    │ MATCH *1..3 / nx.all_simple_paths │
│ K-Shortest Paths   │ "Which are the top-K preferred paths?" │ Yen's algo / nx.shortest_simple_paths │
│ Weighted Shortest  │ "Which path is most trustworthy?"│ Dijkstra / nx.dijkstra_path │
│ Constrained Path   │ "Which path only goes through MANAGES?" │ WHERE + pattern      │
└────────────────────┴──────────────────────────────────┴──────────────────┘
```

**Choosing tip:** if you don't know how "long" the graph is → use Shortest Path. If you want the LLM to weigh several options (to reason logically rather than gamble) → use All Paths or K-Shortest and put all K paths into the prompt so the LLM can pick a logical alternative.

<details>
<summary>Python Code — Path Finding (Click to view)</summary>

```python
import networkx as nx

# Create a weighted graph
G = nx.DiGraph()
G.add_weighted_edges_from([
    ("Alice", "Bob", 1.0),      # MANAGES, weight = 1/confidence
    ("Bob", "Carol", 1.2),
    ("Alice", "Dave", 3.0),     # KNOWS, high weight (low confidence)
    ("Dave", "Carol", 1.5),
    ("Bob", "Phoenix", 1.0),
    ("Carol", "Atlas", 1.0),
])

# 1. Shortest path (unweighted — fewest hops)
path = nx.shortest_path(G, source="Alice", target="Carol")
print(f"Shortest (hops): {path}")  # ['Alice', 'Bob', 'Carol']

# 2. Weighted shortest (Dijkstra — lowest total weight)
path_w = nx.dijkstra_path(G, source="Alice", target="Carol", weight="weight")
print(f"Weighted shortest: {path_w}")  # May differ if weights differ

# 3. All simple paths (limited hops)
all_paths = list(nx.all_simple_paths(G, source="Alice", target="Carol", cutoff=4))
print(f"All paths (≤4 hops): {all_paths}")

# 4. K-shortest paths
k_paths = list(nx.shortest_simple_paths(G, source="Alice", target="Carol", weight="weight"))
print(f"Top-3 shortest: {list(k_paths)[:3]}")

# 5. Path with evidence (edges + confidence)
def path_with_evidence(graph, source, target, weight="weight"):
    path = nx.dijkstra_path(graph, source, target, weight=weight)
    evidence = []
    total_confidence = 1.0
    for i in range(len(path) - 1):
        edata = graph.get_edge_data(path[i], path[i+1])
        evidence.append({
            "from": path[i], "to": path[i+1],
            "type": edata.get("type", "RELATED"),
            "weight": edata.get("weight", 1.0),
        })
        # Confidence = 1/weight (if weight = 1/confidence)
        total_confidence *= (1.0 / edata.get("weight", 1.0))
    return {"path": path, "evidence": evidence, "total_confidence": total_confidence}

print(path_with_evidence(G, "Alice", "Atlas"))
```

</details>

### 2.2 Cypher Path Queries

```cypher
// Shortest path
MATCH (a:Person {name: 'Alice'}), (b:Project {name: 'Atlas'})
MATCH path = shortestPath((a)-[*]-(b))
RETURN path, length(path)

// All paths with a constraint
MATCH (a:Person {name: 'Alice'}), (b:Project {name: 'Atlas'})
MATCH path = (a)-[:MANAGES|WORKS_ON*1..4]->(b)
WHERE all(r in relationships(path) WHERE r.confidence > 0.7)
RETURN path, length(path)
ORDER BY length(path)
LIMIT 5

// Weighted path (using GDS)
// CALL gds.graph.project('myGraph', '*', '*', {relationshipProperties: 'weight'})
// CALL gds.shortestPath.dijkstra.stream('myGraph', {sourceNode: id(a), targetNode: id(b)})
```

---

## 3. Inference Rules & Reasoning

> **📌 Core Concept:**
> **Inference = producing NEW knowledge from OLD knowledge.** Your graph may lack a direct connection — but if you know the *implicit rules* between relations, you can "derive" the missing connection.
>
> **The easiest example — Transitivity (bridging):**
> ```
> Know:  Alice ─MANAGES→ Bob ─MANAGES→ Carol
> Derive: Alice ─INDIRECTLY_MANAGES→ Carol   (bridging)
>
> In real life: "your friend is not necessarily my friend" — but:
> A manages B, B manages C → A has indirect authority over C.
> This is "deriving new knowledge": we don't need a direct edge
> and can still answer the question "who actually has influence over Carol?".
> ```
>
> **Why is it needed?** Real graphs are very **sparse** — you can't store every implicit connection. Inference "compresses" knowledge into **rules** instead of storing every derived relation by hand.

### 3.1 Rule-Based Inference

> **Process: declare the rules, then let the machine run the pattern matching:**
> 1. You write rules of the form `IF (a pattern appears) THEN (create a new edge)`
> 2. The machine scans the whole graph for every place the pattern matches
> 3. Each match → create an inferred edge (with confidence + evidence)

```python
from typing import List, Dict, Tuple

# Define rules in the form: IF pattern THEN new_edge
INFERENCE_RULES = [
    {
        "name": "transitive_manages",
        "pattern": [("A", "MANAGES", "B"), ("B", "MANAGES", "C")],
        "infer": ("A", "INDIRECTLY_MANAGES", "C"),
        "confidence": 0.8,  # an inference has lower confidence than the original fact
        "description": "If A manages B and B manages C → A indirectly manages C"
    },
    {
        "name": "works_on_implies_team",
        "pattern": [("A", "MANAGES", "B"), ("B", "WORKS_ON", "P")],
        "infer": ("A", "OVERSEES", "P"),
        "confidence": 0.75,
        "description": "If A manages B and B works on P → A oversees P"
    },
    {
        "name": "belongs_approved",
        "pattern": [("D", "BELONGS_TO", "P"), ("A", "APPROVES", "D")],
        "infer": ("A", "APPROVES_PROJECT", "P"),
        "confidence": 0.90,
    },
]

def apply_rules(graph: nx.DiGraph, rules: List[Dict]) -> List[Dict]:
    """Apply rules to infer new edges."""
    inferred = []
    
    for rule in rules:
        pattern = rule["pattern"]
        infer = rule["infer"]
        
        if len(pattern) == 2:
            # 2-hop pattern: A -[R1]-> B -[R2]-> C
            (a_var, r1, b_var), (b_var2, r2, c_var) = pattern
            assert b_var == b_var2, "The intermediate variable must match"
            
            for a in graph.nodes():
                for b in graph.successors(a):
                    if graph.get_edge_data(a, b).get("type") != r1:
                        continue
                    for c in graph.successors(b):
                        if graph.get_edge_data(b, c).get("type") != r2:
                            continue
                        # Infer: A -[infer]-> C
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
```

### 3.2 Confidence Propagation

When inferring across multiple steps, confidence drops:

```python
def propagate_confidence(path_confidences: List[float], method: str = "product") -> float:
    """
    Compute the confidence of an inferred edge from a chain.
    
    product: conf = c1 * c2 * ... (multiplicative — the longer the chain, the lower the confidence)
    min: conf = min(c1, c2, ...) (take the weakest)
    avg: conf = mean(c1, c2, ...)
    """
    if method == "product":
        result = 1.0
        for c in path_confidences:
            result *= c
        return result
    elif method == "min":
        return min(path_confidences)
    elif method == "avg":
        return sum(path_confidences) / len(path_confidences)

# Example: Alice(0.95) → Bob(0.90) → Carol
# Inferred: Alice INDIRECTLY_MANAGES Carol
print(propagate_confidence([0.95, 0.90], "product"))  # 0.855
print(propagate_confidence([0.95, 0.90], "min"))       # 0.90
```

---

## 4. Community Detection & Centrality

### 4.1 Community Detection for Reasoning

```python
import networkx as nx

G = nx.karate_club_graph()

# Louvain (fast, good for medium graphs)
import community as community_louvain
partition = community_louvain.best_partition(G)
print(f"Communities: {len(set(partition.values()))}")

# Label Propagation (fastest, for large graphs)
communities_lpa = list(nx.algorithms.community.label_propagation_communities(G))
print(f"LPA communities: {len(communities_lpa)}")

# Use communities to reason:
# "Are Alice and Bob in the same community? → do they work in the same domain?"
def same_community(node_a: str, node_b: str, partition: dict) -> bool:
    return partition.get(node_a) == partition.get(node_b)
```

### 4.2 Centrality — Who Matters?

<details>
<summary>Python Code — Centrality Analysis (Click to view)</summary>

```python
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("Alice", "Bob"), ("Alice", "Carol"), ("Alice", "Dave"),
    ("Bob", "Phoenix"), ("Carol", "Phoenix"), ("Dave", "Atlas"),
    ("Phoenix", "Atlas"),
])

# Degree centrality: who has the most connections
deg = nx.degree_centrality(G)
print(f"Degree: {sorted(deg.items(), key=lambda x: x[1], reverse=True)}")

# Betweenness: who is the bottleneck (sits on many shortest paths)
bet = nx.betweenness_centrality(G)
print(f"Betweenness: {sorted(bet.items(), key=lambda x: x[1], reverse=True)}")
# A node with high betweenness = removing it splits the graph

# PageRank: who is "voted for" by important nodes
pr = nx.pagerank(G)
print(f"PageRank: {sorted(pr.items(), key=lambda x: x[1], reverse=True)}")

# Closeness: who is closest to everyone (lowest average path length)
try:
    close = nx.closeness_centrality(G)
    print(f"Closeness: {sorted(close.items(), key=lambda x: x[1], reverse=True)}")
except:
    pass

# Application: "Who is the approval bottleneck?"
# → The Person with high betweenness in the approval subgraph
```

</details>

---

## 5. Temporal Reasoning

### 5.1 Time-Aware Graph

```python
from datetime import datetime, date

# Edges with validity periods
temporal_edges = [
    {"from": "Alice", "to": "TeamA", "type": "MANAGES", 
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)},
    {"from": "Alice", "to": "TeamB", "type": "MANAGES",
     "valid_from": date(2024, 7, 1), "valid_until": None},  # current
    {"from": "Bob", "to": "Phoenix", "type": "WORKS_ON",
     "valid_from": date(2024, 1, 1), "valid_until": date(2024, 12, 31)},
]

def query_at_time(edges: list, query_date: date, node: str) -> list:
    """Query the graph at a specific moment."""
    active = []
    for e in edges:
        valid_from = e["valid_from"]
        valid_until = e.get("valid_until") or date(9999, 12, 31)
        if valid_from <= query_date <= valid_until:
            if e["from"] == node or e["to"] == node:
                active.append(e)
    return active

# Question: which team did Alice manage on 2024-03-01?
print(query_at_time(temporal_edges, date(2024, 3, 1), "Alice"))
# → TeamA

# Question: which team did Alice manage on 2024-08-01?
print(query_at_time(temporal_edges, date(2024, 8, 1), "Alice"))
# → TeamB

# Equivalent Cypher:
# MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(team)
# WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
# RETURN team
```

### 5.2 Versioning

```python
# Instead of deleting old edges, mark them expired and create new ones
def update_temporal_edge(edges: list, from_node: str, to_node: str, 
                          edge_type: str, new_valid_from: date):
    """Update a temporal edge: expire the old one, create a new one."""
    for e in edges:
        if e["from"] == from_node and e["to"] == to_node and e["type"] == edge_type:
            if e.get("valid_until") is None:  # currently active
                e["valid_until"] = new_valid_from  # expire it
    
    edges.append({
        "from": from_node, "to": to_node, "type": edge_type,
        "valid_from": new_valid_from, "valid_until": None,
    })
    return edges
```

---

## 6. Implementing a Reasoning Engine

<details>
<summary>Python Code — Complete Reasoning Engine (Click to view)</summary>

```python
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
```

</details>

---

## 7. Neuro-Symbolic QA — Combining LLM + Graph Traversal

> **📌 Core Concept:**
> **Neuro-symbolic QA** = combining two strengths: the **LLM understands natural language (neuro)** + **graph traversal finds precise evidence (symbolic)**. Instead of the LLM trying to "remember" knowledge from its parameters (where it gets confused), the LLM acts as the **commander — plans, the graph executes — finds paths — the LLM synthesizes**.
>
> **Why is this a trend?** Research shows: an LLM that "reads" the graph instead of "remembering it" → hallucinations drop significantly. The graph execution guarantees every "reasoning step" is **backed by real evidence** in the KG.
>
> Representative models:

### 7.1 Think-on-Graph (ToG)

> The LLM **reads the KG like a human** — each new reasoning step **visits 1–2 nodes**, looks at the data, then decides the next step. If the BFS isn't heading the right way → **the LLM adjusts the direction on its own** (switches branch) — like a person "thinking out loud".

```python
# Pseudocode — Think-on-Graph
def Think_on_Graph(question: str, graph):
    entities = find_entities(question, graph)          # Step 1: find the related nodes
    best_reasoning_path = None
    
    for _ in range(max_depth):                         # BFS style
        neighbors = get_neighbors(entities, graph)     # Get the candidate neighbors
        reasoning_paths = llm(f"""
            Question: {question}
            Currently at: {entities}
            Next possible moves: {neighbors}
            Choose the most reasonable direction.""")
        # The LLM decides on its own: here the LLM is the planner
        entities = advance(reasoning_paths)            # Move to the next nodes
        if is_answer(entities): 
            return llm(f"Summary: {reasoning_path}")   # The LLM synthesizes from the evidence
    
    return "Not found"
```

### 7.2 Plan-on-Graph — Planner-Executor-Reasoner (PER)

> **Three roles** — clearly separated:
> - **Planner** (LLM): generates the "plan" — a sequence of relation types to traverse (`GET_REPORTER`, `GET_PROJECT`, `GET_STATUS`)
> - **Executor** (Graph BFS): executes the relations according to the plan
> - **Reasoner** (LLM): **reads the execution results** → summarizes the answer
>
> **Key result:** Planner-Executor-Reasoner (PER) achieves **micro-F1 > 0.90** on the KGQA benchmark (2025–2026), at much lower computational cost than Neo4j full-LLM reasoning.

### 7.3 KG-Agent

> The agent **operates the KG through an API** (CRUD), not just queries it — the agent can **add relations, fix nodes, write new evidence** into the graph when needed, then use the results for its answer.

```python
# Pseudocode — Planner-Executor-Reasoner (PER)
def PER(question: str, graph):
    # PLANNER: the LLM generates a sequence of relations
    plan = llm(f"""
        Question: {question}
        To answer, perform in order:
        1. FIND entities related to '{question}'
        2. TRAVERSE relation1 → entity2
        3. TRAVERSE relation2 → entity3
        4. SUMMARIZE the result
        Return a JSON list of the steps.""")  # ["FIND", "GET_REPORTER", "GET_PROJECT", "SUM"]
    
    # EXECUTOR: the graph executes each step
    entities = find_start_entities(question, graph)
    for step in plan:
        if step.startswith("GET_"):
            entities = traverse(step.replace("GET_", ""), entities, graph)
    
    # REASONER: the LLM reads the graph results (not from its own memory) → answers
    return llm(f"Results from the graph: {entities}\n\nAnswer to the question: {question}")
```

> **Versus Think-on-Graph:** PER clearly separates Planner (direction changes) / Executor / Reasoner. Think-on-Graph re-mixes everything inside the LLM + graph. PER is usually **more cost-efficient** because the Executor doesn't spend LLM tokens.

---

## 8. Hands-On Labs

### Lab 1: Constrained Traversal Benchmark

1. Create a 1K-node, 5K-edge graph with random types
2. Run unconstrained BFS vs constrained (only 2 edge types) — compare nodes visited and time

### Lab 2: Rule Inference

1. Define 5 rules for an org chart (transitive, composition)
2. Run `apply_rules` on a 50-node graph, count the inferred edges
3. Check: are the inferred edges logically correct? Any false positives?

### Lab 3: Temporal Query

1. Create a temporal graph with 20 edges having different `valid_from/until`
2. Ask: "Who managed team X on 2023-06-01 vs 2024-06-01?" — verify the results differ

---

## References

- *Reasoning with Knowledge Graphs* — Paulheim & Gangemi (2023)
- Neo4j GDS — *Path Finding & Centrality* (https://neo4j.com/docs/graph-data-science/current/)
- HotpotQA — *Multi-hop QA Benchmark* (https://hotpotqa.github.io/)
- *Temporal Knowledge Graphs* — Cai et al. (2024, survey)
- *Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph* (ICLR 2024)
- *Plan-on-Graph & Planner-Executor-Reasoner* — LLM-planned multi-hop KGQA, micro-F1 > 0.90 (arXiv:2511.19648)
- *KG-Agent: An Efficient and Agentic LLM for Knowledge Graph Reasoning* (2025)

---

*Next: [07 — GNN](../07-gnn/)*
