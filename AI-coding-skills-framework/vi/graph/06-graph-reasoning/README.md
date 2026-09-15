# 🧩 06. Graph Reasoning — Suy Luận Trên Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Reasoning Quan Trọng?](#tại-sao-graph-reasoning-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Traversal Strategies](#1-traversal-strategies)
> - [2. Path Finding](#2-path-finding)
> - [3. Inference Rules & Reasoning](#3-inference-rules--reasoning)
> - [4. Community Detection & Centrality](#4-community-detection--centrality)
> - [5. Temporal Reasoning](#5-temporal-reasoning)
> - [6. Triển Khai Reasoning Engine](#6-triển-khai-reasoning-engine)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có Knowledge Graph:

```
Alice —[MANAGES]→ Bob —[WORKS_ON]→ Phoenix
  │
  └──[KNOWS]→ Carol —[WORKS_ON]→ Atlas (AI Platform)
```

Bạn hỏi: *"Team của Alice có ai làm AI không?"*

Đây **không phải** câu hỏi lookup — mà là **suy luận**:

1. `MANAGES` là transitive? Alice quản lý Bob, Bob có thuộc "team của Alice" không?
2. `WORKS_ON → Atlas` có phải là "làm AI" không? Atlas có property `domain: AI` không?
3. Có cần traverse `Alice → Bob → Phoenix → Atlas` (3 hops) để nối?

**Graph Reasoning** biến những câu hỏi mơ hồ này thành **logic có thể thực thi**: rules, path constraints, và inference chains có thể verify.

### Tại Sao Graph Reasoning Quan Trọng?

> *"Retrieval finds facts. Reasoning connects them into answers you didn't know to ask for."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **HotpotQA Benchmark** | Multi-hop reasoning trên graph tăng **27% accuracy** vs single-hop retrieval |
| 2 | **Neo4j GDS (2024)** | Shortest path + centrality giúp phát hiện **bottleneck persons** giảm 40% approval time |
| 3 | **Temporal KG Papers (2024)** | Temporal reasoning giảm **35% stale answers** (trả lời bằng thông tin đã hết hạn) |

---

## Tổng Quan

```
Knowledge Graph
    │
    ├──► Traversal (BFS/DFS, constrained)
    │      "Tìm tất cả nodes cách Alice 2 hops qua MANAGES/WORKS_ON"
    │
    ├──► Path Finding (shortest, all-paths, weighted)
    │      "Đường ngắn nhất giữa Bob và project AI nào?"
    │
    ├──► Inference (rules, transitivity, composition)
    │      "Nếu A MANAGES B và B WORKS_ON P → A INDIRECTLY_MANAGES P"
    │
    ├──► Community & Centrality
    │      "Ai là người quan trọng nhất trong org?"
    │
    └──► Temporal (valid_from/until, event ordering)
           "Ai quản lý team AI vào Q2/2024?"
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Traversal](#1-traversal-strategies) | BFS, DFS, constrained traversal, sampling |
| 2 | [Path Finding](#2-path-finding) | Shortest path, all paths, weighted, k-shortest |
| 3 | [Inference](#3-inference-rules--reasoning) | Rules, transitivity, composition, OWL-lite |
| 4 | [Community & Centrality](#4-community-detection--centrality) | Leiden, Louvain, PageRank, betweenness |
| 5 | [Temporal](#5-temporal-reasoning) | Time-aware traversal, versioning, expiration |
| 6 | [Engine](#6-triển-khai-reasoning-engine) | Code reasoning engine hoàn chỉnh |
| 7 | [Neuro-Symbolic QA](#7-neuro-symbolic-qa) | Think-on-Graph, KG-Agent, Planner-Executor-Reasoner |

---

## 1. Traversal Strategies

> **📌 Khái Niệm Cơ Bản:**
> **Traversal = "đi thăm" graph** — bắt đầu từ 1 node, lần lượt ghé qua các nodes khác theo mối quan hệ. Giống như "theo dõi" ai đó trên mạng xã hội: bắt đầu từ mình, xem bạn bè của mình → rồi xem bạn bè của bạn mình → tiếp tục...
>
> **3 kiểu đi:**
> - **BFS (Breadth-First)** = "Đi theo vòng tròn" — thăm tất cả nodes cách 1 hop trước, rồi 2 hops, rồi 3 hops... **Analogies:息多社会然后去半圈** (đổ nước trên mạng — nước lan đều trước khi sâu hơn)
> - **DFS (Depth-First)** = "Đi hết 1 nhánh trước" — đi sâu nhất 1 đường, quay lại, rồi đi đường khác. **Analogies: 走单线** (đi một đường hết rồi mới quay)
> - **Constrained** = BFS/DFS có điều kiện — chỉ đi qua nodes/edges thỏa điều kiện (ví dụ: chỉ qua `MANAGES` edges, chỉ đến Person nodes)

### 1.1 BFS vs DFS vs Constrained

```
Graph: Alice → Bob → Carol
         │      │
         └────→ Dave → Eve

BFS từ Alice (level-order):       DFS từ Alice (depth-first):
  Level 0: Alice                    Path 1: Alice → Bob → Carol (dead end, backtrack)
  Level 1: Bob, Dave                Path 2: Alice → Bob → Dave → Eve
  Level 2: Carol, Eve

Constrained BFS (chỉ qua MANAGES):
  Alice —[MANAGES]→ Bob —[MANAGES]→ Carol  ✅
  Alice —[KNOWS]→ Dave                     ❌ (bị filter)
```

**Khi nào chọn BFS, DFS?**
| Tình huống | Chọn | Lý do |
|-----------|------|-------|
| Muốn biết tất cả nodes cách 1-2 hops | **BFS** | Đảm bảo tìm được tất cả trước khi đi sâu |
| Muốn tìm đường ngắn nhất | **BFS** | BFS luôn tìm đường ngắn nhất đầu tiên |
| Muốn tìm đường bất kỳ, kiểm tra tồn tại | **DFS** | Nhanh hơn BFS khi muốnExists check |
| Graph lớn, cần giới hạn số nodes thăm | **Sampled BFS** | BFS có sampling, không visit hết |
| Chỉ cần nodes thỏa điều kiện | **Constrained BFS** | Kết hợp BFS + filter |

<details>
<summary>Python Code — Constrained Traversal (Click để xem)</summary>

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
    BFS có ràng buộc — chỉ đi qua edges/nodes thỏa điều kiện.
    
    Ví dụ: chỉ qua MANAGES/WORKS_ON, confidence >= 0.7
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

# Chỉ qua MANAGES/WORKS_ON, confidence >= 0.7
results = constrained_bfs(G, "Alice", max_hops=3, 
                           allowed_edge_types={"MANAGES", "WORKS_ON"},
                           min_confidence=0.7)
for r in results:
    print(f"  {r['path']} (hops={r['hops']}, conf={r['confidence']:.2f})")
# ['Alice', 'Bob'] (hops=1, conf=0.95)
# ['Alice', 'Bob', 'Carol'] (hops=2, conf=0.90)
# ['Alice', 'Bob', 'Phoenix'] (hops=2, conf=0.85)
# Dave bị loại vì KNOWS không trong allowed types
```

</details>

### 1.2 Sampling Cho Graph Lớn

Trên graph 1M+ nodes, không thể traverse toàn bộ:

```python
import random

def sampled_traversal(
    graph: nx.Graph,
    start: str,
    max_hops: int = 2,
    max_neighbors_per_hop: int = 10,
    sample_strategy: str = "random",  # random | top-confidence | pagerank
) -> List[dict]:
    """Sample traversal — giới hạn số neighbors mỗi hop."""
    visited = set([start])
    current_level = [start]
    all_results = []
    
    for hop in range(max_hops):
        next_level = []
        for node in current_level:
            neighbors = list(graph.neighbors(node))
            
            # Sample nếu quá nhiều neighbors
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

> **📌 Khái Niệm Cơ Bản:**
> **Path Finding = tìm "con đường" nối 2 nodes trong graph.** Giống như Google Maps: từ điểm A đến điểm B có thể đi nhiều đường khác nhau, và bạn muốn tìm đường tối ưu theo tiêu chí (ít bước, nhanh nhất, đáng tin nhất).
>
> **Khi nào cần trong Agent?**
> - "Liên hệ Alice thông qua ai?" → shortest path Alice → Bob (sếp chung)
> - "Bob có mấy cách tiếp cận Project Atlas?" → all paths, giới hạn 4 hops
> - "Tìm đường đáng tin nhất (confidence cao)" → weighted shortest using confidence as weight

### 2.1 Các Loại Path Finding

> **Đọc bảng này như sau:** Mỗi loại trả lời 1 câu hỏi khác nhau — *cùng bộ dữ liệu nhưng "ý nghĩa đường đi" khác nhau*.

```
┌────────────────────┬──────────────────────────────────┬──────────────────┐
│ Loại               │ Trả lời câu hỏi                  │ Cypher / NetworkX│
├────────────────────┼──────────────────────────────────┼──────────────────┤
│ Shortest Path      │ "Đường nào ít bước nhất?"        │ shortestPath() / nx.shortest_path │
│ All Paths          │ "Có những đường nào (≤N hops)?"  │ MATCH *1..3 / nx.all_simple_paths │
│ K-Shortest Paths   │ "Top-K đường ưu tiên nhất?"      │ Yen's algo / nx.shortest_simple_paths │
│ Weighted Shortest  │ "Đường nào đáng tin nhất?"       │ Dijkstra / nx.dijkstra_path │
│ Constrained Path   │ "Đường nào chỉ qua MANAGES?"     │ WHERE + pattern      │
└────────────────────┴──────────────────────────────────┴──────────────────┘
```

**Mẹo chọn:** Nếu bạn không biết graph "dài bao nhiêu" → dùng Shortest Path. Nếu bạn muốn LLM cân nhắc nhiều lựa chọn (để suy luận, hợp lý thay vì may rủi) → dùng All Paths hoặc K-Shortest và đưa cả K paths vào prompt giúp LLM chọn logical alternative.

<details>
<summary>Python Code — Path Finding (Click để xem)</summary>

```python
import networkx as nx

# Tạo weighted graph
G = nx.DiGraph()
G.add_weighted_edges_from([
    ("Alice", "Bob", 1.0),      # MANAGES, weight = 1/confidence
    ("Bob", "Carol", 1.2),
    ("Alice", "Dave", 3.0),     # KNOWS, weight cao (ít tin cậy)
    ("Dave", "Carol", 1.5),
    ("Bob", "Phoenix", 1.0),
    ("Carol", "Atlas", 1.0),
])

# 1. Shortest path (unweighted — ít hops nhất)
path = nx.shortest_path(G, source="Alice", target="Carol")
print(f"Shortest (hops): {path}")  # ['Alice', 'Bob', 'Carol']

# 2. Weighted shortest (Dijkstra — tổng weight nhỏ nhất)
path_w = nx.dijkstra_path(G, source="Alice", target="Carol", weight="weight")
print(f"Weighted shortest: {path_w}")  # Có thể khác nếu weight khác

# 3. All simple paths (giới hạn hops)
all_paths = list(nx.all_simple_paths(G, source="Alice", target="Carol", cutoff=4))
print(f"All paths (≤4 hops): {all_paths}")

# 4. K-shortest paths
k_paths = list(nx.shortest_simple_paths(G, source="Alice", target="Carol", weight="weight"))
print(f"Top-3 shortest: {list(k_paths)[:3]}")

# 5. Path với bằng chứng (edges + confidence)
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
        # Confidence = 1/weight (nếu weight = 1/confidence)
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

// All paths với constraint
MATCH (a:Person {name: 'Alice'}), (b:Project {name: 'Atlas'})
MATCH path = (a)-[:MANAGES|WORKS_ON*1..4]->(b)
WHERE all(r in relationships(path) WHERE r.confidence > 0.7)
RETURN path, length(path)
ORDER BY length(path)
LIMIT 5

// Weighted path (dùng GDS)
// CALL gds.graph.project('myGraph', '*', '*', {relationshipProperties: 'weight'})
// CALL gds.shortestPath.dijkstra.stream('myGraph', {sourceNode: id(a), targetNode: id(b)})
```

---

## 3. Inference Rules & Reasoning

> **📌 Khái Niệm Cơ Bản:**
> **Inference (suy diễn) = tạo ra kiến thức MỚI từ kiến thức CŨ.** Graph của bạn có thể thiếu kết nối trực tiếp — nhưng nếu bạn biết *quy luật ngầm* giữa các quan hệ, bạn "suy ra" được kết nối bị thiếu đó.
>
> **Ví dụ dễ nhất — Transitivity (bắc cầu):**
> ```
> Biết:  Alice ─MANAGES→ Bob ─MANAGES→ Carol
> Suy ra: Alice ─INDIRECTLY_MANAGES→ Carol   (bắc cầu)
>
> Giống trong đời thực: "Bạn của bạn không hẳn là bạn của tôi" — nhưng:
> A là quản lý của B, B là quản lý của C → A có quyền gián tiếp với C.
> Đây là "suy ra mới": ta không cần edge EU trực tiếp — vẫn trả lời được
> câu hỏi "ai thực ra có ảnh hưởng lên Carol?".
> ```
>
> **Tại sao cần?** Vì graph thực tế rất **thưa (sparse)** — không thể lưu mọi kết nối ngầm. Inference "nén" tri thức vào **các rule** thay vì lưu tất cả quan hệ dẫn xuất thủ công.

### 3.1 Rule-Based Inference

> **Quy trình khai báo rule rồi để máy chạy pattern matching:**
> 1. Bạn viết rule dạng `IF (pattern xuất hiện) THEN (tạo edge mới)`
> 2. Máy quét toàn bộ graph tìm mọi chỗ khớp pattern
> 3. Mỗi chỗ khớp → tạo edge suy ra (kèm confidence + evidence bằng chứng)

```python
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
```

### 3.2 Confidence Propagation

Khi suy diễn qua nhiều bước, confidence giảm:

```python
def propagate_confidence(path_confidences: List[float], method: str = "product") -> float:
    """
    Tính confidence của inferred edge từ chain.
    
    product: conf = c1 * c2 * ... (nhân — chain càng dài, conf càng thấp)
    min: conf = min(c1, c2, ...) (lấy yếu nhất)
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

# Ví dụ: Alice(0.95) → Bob(0.90) → Carol
# Inferred: Alice INDIRECTLY_MANAGES Carol
print(propagate_confidence([0.95, 0.90], "product"))  # 0.855
print(propagate_confidence([0.95, 0.90], "min"))       # 0.90
```

---

## 4. Community Detection & Centrality

### 4.1 Community Detection Cho Reasoning

```python
import networkx as nx

G = nx.karate_club_graph()

# Louvain (nhanh, tốt cho medium graphs)
import community as community_louvain
partition = community_louvain.best_partition(G)
print(f"Communities: {len(set(partition.values()))}")

# Label Propagation (nhanh nhất, cho large graphs)
communities_lpa = list(nx.algorithms.community.label_propagation_communities(G))
print(f"LPA communities: {len(communities_lpa)}")

# Dùng community để reasoning:
# "Alice và Bob có cùng community không? → họ có làm cùng domain không?"
def same_community(node_a: str, node_b: str, partition: dict) -> bool:
    return partition.get(node_a) == partition.get(node_b)
```

### 4.2 Centrality — Ai Quan Trọng?

<details>
<summary>Python Code — Centrality Analysis (Click để xem)</summary>

```python
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([
    ("Alice", "Bob"), ("Alice", "Carol"), ("Alice", "Dave"),
    ("Bob", "Phoenix"), ("Carol", "Phoenix"), ("Dave", "Atlas"),
    ("Phoenix", "Atlas"),
])

# Degree centrality: ai có nhiều kết nối nhất
deg = nx.degree_centrality(G)
print(f"Degree: {sorted(deg.items(), key=lambda x: x[1], reverse=True)}")

# Betweenness: ai là bottleneck (nằm trên nhiều shortest paths)
bet = nx.betweenness_centrality(G)
print(f"Betweenness: {sorted(bet.items(), key=lambda x: x[1], reverse=True)}")
# Node có betweenness cao = nếu remove, graph bị chia cắt

# PageRank: ai được "vote" bởi nodes quan trọng
pr = nx.pagerank(G)
print(f"PageRank: {sorted(pr.items(), key=lambda x: x[1], reverse=True)}")

# Closeness: ai gần mọi người nhất (trung bình path ngắn)
try:
    close = nx.closeness_centrality(G)
    print(f"Closeness: {sorted(close.items(), key=lambda x: x[1], reverse=True)}")
except:
    pass

# Ứng dụng: "Ai là approver bottleneck?"
# → Person có betweenness cao trong approval subgraph
```

</details>

---

## 5. Temporal Reasoning

### 5.1 Time-Aware Graph

```python
from datetime import datetime, date

# Edge có thời gian hiệu lực
temporal_edges = [
    {"from": "Alice", "to": "TeamA", "type": "MANAGES", 
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)},
    {"from": "Alice", "to": "TeamB", "type": "MANAGES",
     "valid_from": date(2024, 7, 1), "valid_until": None},  # hiện tại
    {"from": "Bob", "to": "Phoenix", "type": "WORKS_ON",
     "valid_from": date(2024, 1, 1), "valid_until": date(2024, 12, 31)},
]

def query_at_time(edges: list, query_date: date, node: str) -> list:
    """Truy vấn graph tại một thời điểm cụ thể."""
    active = []
    for e in edges:
        valid_from = e["valid_from"]
        valid_until = e.get("valid_until") or date(9999, 12, 31)
        if valid_from <= query_date <= valid_until:
            if e["from"] == node or e["to"] == node:
                active.append(e)
    return active

# Hỏi: Alice quản lý team nào vào 2024-03-01?
print(query_at_time(temporal_edges, date(2024, 3, 1), "Alice"))
# → TeamA

# Hỏi: Alice quản lý team nào vào 2024-08-01?
print(query_at_time(temporal_edges, date(2024, 8, 1), "Alice"))
# → TeamB

# Cypher tương đương:
# MATCH (a:Person {name: 'Alice'})-[r:MANAGES]->(team)
# WHERE r.valid_from <= date('2024-03-01') <= r.valid_until
# RETURN team
```

### 5.2 Versioning

```python
# Thay vì xóa edge cũ, đánh dấu hết hạn và tạo edge mới
def update_temporal_edge(edges: list, from_node: str, to_node: str, 
                          edge_type: str, new_valid_from: date):
    """Cập nhật temporal edge: expire cũ, tạo mới."""
    for e in edges:
        if e["from"] == from_node and e["to"] == to_node and e["type"] == edge_type:
            if e.get("valid_until") is None:  # đang active
                e["valid_until"] = new_valid_from  # expire
    
    edges.append({
        "from": from_node, "to": to_node, "type": edge_type,
        "valid_from": new_valid_from, "valid_until": None,
    })
    return edges
```

---

## 6. Triển Khai Reasoning Engine

<details>
<summary>Python Code — Complete Reasoning Engine (Click để xem)</summary>

```python
from typing import List, Dict, Set, Optional
from collections import deque
import networkx as nx

class GraphReasoningEngine:
    """
    Engine suy luận trên Knowledge Graph.
    Hỗ trợ: traversal, path finding, rule inference, temporal.
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
        """Chạy tất cả rules để suy ra edges mới."""
        return apply_rules(self.graph, self.rules)
    
    def answer_with_reasoning(self, query: str) -> Dict:
        """
        Trả lời câu hỏi với reasoning chain.
        Ví dụ: "Team của Alice có ai làm AI không?"
        """
        # Parse query (simplified — production dùng LLM để parse)
        # Giả sử: start=Alice, relation=team, target_domain=AI
        results = self.traverse("Alice", max_hops=3, edge_types={"MANAGES", "WORKS_ON"})
        
        # Filter: ai WORKS_ON project có domain AI
        ai_workers = []
        for r in results:
            target = r["target"]
            node_data = self.graph.nodes.get(target, {})
            if node_data.get("domain") == "AI" or "AI" in target:
                ai_workers.append(r)
        
        # Thêm inferred
        inferred = self.infer()
        
        return {
            "query": query,
            "traversal_results": results,
            "ai_workers": ai_workers,
            "inferred": inferred,
            "answer": f"Team của Alice có {len(ai_workers)} người làm AI" if ai_workers else "Không tìm thấy",
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
print(engine.answer_with_reasoning("Team của Alice có ai làm AI không?"))
```

</details>

---

## 7. Neuro-Symbolic QA — Kết Hợp LLM + Graph Traversal

> **📌 Khái Niệm Cơ Bản:**
> **Neuro-symbolic QA** = kết hợp hai thế mạnh: **LLM hiểu ngôn ngữ tự nhiên (neuro)** + **graph traversal tìm bằng chứng chính xác (symbolic)**. Thay vì LLM tự "nhớ" tri thức từ tham số (hay nhầm lẫn), LLM đóng vai **chỉ huy — lên kế hoạch, graph thực thi — tìm path — LLM tổng hợp**.
>
> **Vì sao đây là xu hướng?** Nghiên cứu cho thấy: LLM "đọc" graph thay vì "tự nhớ" → hallucination giảm đáng kể. Graph thực thi đảm bảo mỗi "bước suy luận" đều được **hỗ trợ bằng chứng** thực tế trong KG.
>
> Các mô hình tiêu biểu:

### 7.1 Think-on-Graph (ToG)

> LLM **đọc KG như người** — mỗi bước suy luận mới **thăm 1-2 nút**, xem dataframe, rồi quyết định bước tiếp. Nếu BFS không đúng hướng → **LLM tự điều chỉnh hướng** (đổi branch) — giống người "suy nghĩ trong đầu".

```python
# Pseudocode — Think-on-Graph
def Think_on_Graph(question: str, graph):
    entities = find_entities(question, graph)          # Bước 1: tìm nodes liên quan
    best_reasoning_path = None
    
    for _ in range(max_depth):                         # BFS style
        neighbors = get_neighbors(entities, graph)     # Lấy các neighbors tiềm năng
        reasoning_paths = llm(f"""
            Câu hỏi: {question}
            Đang ở: {entities}
            Các bước tiếp theo có thể thực hiện: {neighbors}
            Chọn 1 hướng đi hợp lý nhất.""")
        # LLM tự quyết định: đây là LLM làm planner
        entities = advance(reasoning_paths)            # Di chuyển đến nodes tiếp
        if is_answer(entities): 
            return llm(f"Tóm tắt: {reasoning_path}")  # LLM tổng hợp từ bằng chứng
    
    return "Không tìm được"
```

### 7.2 Plan-on-Graph — Planner-Executor-Reasoner (PER)

> **Đóng 3 vai** — phân tách rõ ràng:
> - **Planner** (LLM): sinh "kế hoạch" — 1 chuỗi relation types cần đi qua (`GET_REPORTER`, `GET_PROJECT`, `GET_STATUS`)
> - **Executor** (Graph BFS): thực thi mối relation theo kế hoạch
> - **Reasoner** (LLM): **đọc kết quả thực thi** → tóm tắt answer
>
> **Kết quả chính:** Planner-Executor-Reasoner (PER) đạt **micro-F1 > 0.90** trên KGQA benchmark (2025-2026), với chi phí computation thấp hơn nhiều so với Neo4j full-LLM reasoning.

### 7.3 KG-Agent

> Agent **thao tác KG qua API** (CRUD) thay vì chỉ query — agent có thể **thêm relation, sửa node, viết bằng chứng mới** vào graph nếu cần, rồi dùng kết quả cho câu trả lời.

```python
# Pseudocode — Planner-Executor-Reasoner (PER)
def PER(question: str, graph):
    # PLANNER: LLM sinh sequence relations
    plan = llm(f"""
        Câu hỏi: {question}
        Để trả lời, cần thực hiện theo trình tự:
        1. FIND entities liên quan đến '{question}'
        2. TRAVERSE relation1 → entity2
        3. TRAVERSE relation2 → entity3
        4. SUMMARIZE kết quả
        Trả về JSON list các bước.""")  # ["FIND", "GET_REPORTER", "GET_PROJECT", "SUM"]
    
    # EXECUTOR: graph thực thi từng bước
    entities = find_start_entities(question, graph)
    for step in plan:
        if step.startswith("GET_"):
            entities = traverse(step.replace("GET_", ""), entities, graph)
    
    # REASONER: LLM đọc kết quả graph (không phải LLM tự nhớ) → trả lời
    return llm(f"Kết quả từ graph: {entities}\n\nTrả lời câu hỏi: {question}")
```

> **So với Think-on-Graph:** PER tách rõ Planner (đổi hướng) / Executor / Reasoner. Think-on-Graph remix mọi thứ trong LLM + graph. PER thường **hiệu quả hơn về chi phí** vì Executor không tốn token LLM.

---

## 8. Labs Thực Hành

### Lab 1: Constrained Traversal Benchmark

1. Tạo graph 1K nodes, 5K edges với random types
2. Chạy BFS không constraint vs constrained (chỉ 2 edge types) — so sánh số nodes thăm và thời gian

### Lab 2: Rule Inference

1. Định nghĩa 5 rules cho org chart (transitive, composition)
2. Chạy `apply_rules` trên graph 50 nodes, đếm số inferred edges
3. Kiểm tra: inferred edges có đúng logic không? Có false positive không?

### Lab 3: Temporal Query

1. Tạo temporal graph với 20 edges có `valid_from/until` khác nhau
2. Hỏi: "Ai quản lý team X vào 2023-06-01 vs 2024-06-01?" — verify kết quả khác nhau

---

## Tài Liệu Tham Khảo

- *Reasoning with Knowledge Graphs* — Paulheim & Gangemi (2023)
- Neo4j GDS — *Path Finding & Centrality* (https://neo4j.com/docs/graph-data-science/current/)
- HotpotQA — *Multi-hop QA Benchmark* (https://hotpotqa.github.io/)
- *Temporal Knowledge Graphs* — Cai et al. (2024, survey)
- *Think-on-Graph: Deep and Responsible Reasoning of Large Language Model on Knowledge Graph* (ICLR 2024)
- *Plan-on-Graph & Planner-Executor-Reasoner* — LLM-planned multi-hop KGQA, micro-F1 > 0.90 (arXiv:2511.19648)
- *KG-Agent: An Efficient and Agentic LLM for Knowledge Graph Reasoning* (2025)

---

*Tiếp theo: [07 — GNN](../07-gnn/)*
