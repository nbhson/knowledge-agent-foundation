# 📊 09. Evaluation — Đánh Giá Chất Lượng Graph & GraphRAG

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Evaluation Quan Trọng?](#tại-sao-evaluation-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Graph Quality Metrics](#1-graph-quality-metrics)
> - [2. Retrieval Evaluation](#2-retrieval-evaluation)
> - [3. Generation Evaluation (RAG)](#3-generation-evaluation-rag)
> - [4. Knowledge Graph Completion Metrics](#4-knowledge-graph-completion-metrics)
> - [5. Benchmarks & Datasets](#5-benchmarks--datasets)
> - [6. Evaluation Framework](#6-evaluation-framework)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã xây xong GraphRAG, demo cho sếp: *"Hỏi gì cũng trả lời được!"*

Sếp hỏi 3 câu:

1. *"Dự án Phoenix ngân sách bao nhiêu?"* → Trả lời: "500 triệu" ✅ (đúng, trong doc)
2. *"Ai duyệt Phoenix?"* → Trả lời: "Alice" ✅ (đúng, nhưng confidence 0.6 — thấp!)
3. *"Team AI có bao nhiêu người?"* → Trả lời: "15 người" ❌ (doc ghi 10, LLM hallucinate)

Không có evaluation framework, bạn **không biết** GraphRAG đúng bao nhiêu %, hallucinate bao nhiêu %, và **tại sao** sai (extraction sai? retrieval sai? generation sai?).

**Evaluation là cách biến "demo hay" thành "production đáng tin".**

### Tại Sao Evaluation Quan Trọng?

> *"Không đo được thì không cải thiện được. Không tách được retrieval vs generation thì không biết sửa ở đâu."*
> — RAG Evaluation Best Practices (2024)

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | LLM-as-judge (comprehensiveness, diversity) phân biệt GraphRAG vs vanilla RAG với **p<0.01** |
| 2 | **RAGAS Framework (2024)** | Tách faithfulness (generation) vs context relevance (retrieval) giúp **giảm 50% debug time** |
| 3 | **OGB + FB15k-237** | KG completion: Hits@10 và MRR là metrics chuẩn — không dùng accuracy thuần |

---

## Tổng Quan

```
                    ┌─────────────────────────────────┐
                    │      EVALUATION FRAMEWORK        │
                    │                                  │
  Knowledge Graph ──►│  1. Graph Quality               │
  (nodes, edges)     │     Coverage, Density, Connectivity│
                     │                                  │
  Retrieval ────────►│  2. Retrieval Quality            │
  (subgraph, paths)  │     Precision, Recall, MRR, Path Precision│
                     │                                  │
  Generation ───────►│  3. Generation Quality           │
  (answer + citation)│     Faithfulness, Relevance, Hallucination│
                     │                                  │
  KG Completion ────►│  4. KG Completion                │
  (link prediction)  │     Hits@K, MRR, MR              │
                     │                                  │
                     └──────────────┬──────────────────┘
                                    │
                     ┌──────────────▼──────────────────┐
                     │  BENCHMARKS & REPORTING          │
                     │  HotpotQA, 2Wiki, Custom, Dashboard│
                     └─────────────────────────────────┘
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Graph Quality](#1-graph-quality-metrics) | Coverage, connectivity, density |
| 2 | [Retrieval](#2-retrieval-evaluation) | Precision, recall, MRR, path precision |
| 3 | [Generation](#3-generation-evaluation-rag) | Faithfulness, hallucination, LLM-as-judge |
| 4 | [KG Completion](#4-knowledge-graph-completion-metrics) | Hits@K, MRR, MR |
| 5 | [Benchmarks](#5-benchmarks--datasets) | HotpotQA, GraphRAG-Bench, KGHaluBench, evidence recall |
| 6 | [Framework](#6-evaluation-framework) | Code evaluation pipeline |

---

## 1. Graph Quality Metrics

> **📌 Khái Niệm Cơ Bản:**
> **Trước khi đánh giá "AI trả lời đúng không", phải đánh giá "graph có tốt không"?** Nếu graph thiếu sót hoặc sai, kết quả RAG dù code hoàn hảo cũng sẽ vô nghĩa (GIGO — garbage in, garbage out).
>
> **9 thước đo sức khỏe của graph.** Dùng phép so sánh analogies:
>
> - **Node/Edge Coverage** = *độ phủ* — "trích xuất được bao nhiêu % sự thật từ documents?" Giống kiểm tra kiến thức: bỏ sót 30% kiến thức thì trả lời chỉ đúng 70%.
> - **Duplicate Rate** = *độ sạch* — "có bao nhiêu entities trùng lặp?" Giống danh bạ ghi "Nguyễn Văn A" và "NV A" thành 2 người → truy vấn bị chia cắt.
> - **Connectivity** = *độ liên thông* — "các nodes có nối liền nhau hay rời rạc?" Graph gãy làm nhiều mảnh → truy vấn multi-hop không đi sang được mảnh khác.
> - **Density / Avg Degree** = *độ dày* — graph quá thưa → thiếu kết nối; quá đặc → nhiễu.
> - **Isolated Nodes** = nodes **không có mối quan hệ nào** — vô dụng, chỉ tốn chỗ.
> - **Invalid Edge Rate** = edges **vi phạm quy tắc** (Person → MANAGES → Document) — 100% phải bằng 0.
> - **Temporal Freshness** = edge cũ **hết hạn** nhưng chưa cập nhật — trả lời bằng thông tin lỗi thời.

### 1.1 Metrics Cho Bản Thân Graph

Trước khi đo retrieval/generation, phải đo **graph có tốt không**:

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Tốt khi              │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Node Coverage        │ % entities thực tế được trích    │ Cao (>80%)           │
│ Edge Coverage        │ % relations thực tế được trích   │ Cao (>70%)           │
│ Duplicate Rate       │ % nodes trùng lặp (chưa dedup)   │ Thấp (<5%)           │
│ Connectivity         │ % nodes trong largest component  │ Cao (>90%)           │
│ Density              │ 2|E| / |V|(|V|-1)                │ Tùy domain           │
│ Avg Degree           │ Số quan hệ trung bình / node     │ 3-10 (enterprise)    │
│ Isolated Nodes       │ Nodes không có edge nào          │ Thấp (<5%)           │
│ Invalid Edge Rate    │ % edges vi phạm ontology         │ 0%                   │
│ Temporal Freshness   │ % edges còn valid (chưa expire)  │ Cao (>95%)           │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Graph Quality Metrics (Click để xem)</summary>

```python
import networkx as nx
from typing import Dict, List

def evaluate_graph_quality(graph: nx.Graph, ontology=None) -> Dict:
    """Đo chất lượng graph."""
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    
    # Connectivity
    if isinstance(graph, nx.DiGraph):
        is_connected = nx.is_weakly_connected(graph) if n_nodes > 0 else True
        components = list(nx.weakly_connected_components(graph))
    else:
        is_connected = nx.is_connected(graph) if n_nodes > 0 else True
        components = list(nx.connected_components(graph))
    
    largest_component_size = max(len(c) for c in components) if components else 0
    connectivity = largest_component_size / n_nodes if n_nodes > 0 else 0
    
    # Isolated nodes
    isolated = list(nx.isolates(graph))
    isolated_rate = len(isolated) / n_nodes if n_nodes > 0 else 0
    
    # Density & avg degree
    density = nx.density(graph)
    avg_degree = sum(dict(graph.degree()).values()) / n_nodes if n_nodes > 0 else 0
    
    # Invalid edges (nếu có ontology)
    invalid_edges = 0
    if ontology:
        for u, v, data in graph.edges(data=True):
            edge_type = data.get("type", "")
            from_type = graph.nodes[u].get("type", "")
            to_type = graph.nodes[v].get("type", "")
            ok, _ = ontology.validate_edge(edge_type, from_type, to_type)
            if not ok:
                invalid_edges += 1
    invalid_rate = invalid_edges / n_edges if n_edges > 0 else 0
    
    return {
        "nodes": n_nodes,
        "edges": n_edges,
        "density": round(density, 4),
        "avg_degree": round(avg_degree, 2),
        "connectivity": round(connectivity, 3),
        "is_connected": is_connected,
        "num_components": len(components),
        "isolated_nodes": len(isolated),
        "isolated_rate": round(isolated_rate, 3),
        "invalid_edges": invalid_edges,
        "invalid_rate": round(invalid_rate, 3),
    }

# Usage
G = nx.karate_club_graph()
G_labeled = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
for n in G_labeled.nodes():
    G_labeled.nodes[n]["type"] = "Person"

metrics = evaluate_graph_quality(G_labeled)
print(metrics)
# {'nodes': 34, 'edges': 78, 'density': 0.139, 'avg_degree': 4.59, 
#  'connectivity': 1.0, 'isolated_rate': 0.0, ...}
```

</details>

### 1.2 Coverage — So Với Ground Truth

```python
def evaluate_coverage(
    extracted_entities: List[str],
    ground_truth_entities: List[str],
    threshold: float = 0.85,  # embedding similarity threshold
) -> Dict:
    """
    Đo coverage: bao nhiêu ground truth entities được trích đúng.
    
    Dùng embedding similarity để fuzzy match (Alice ≈ Alice Nguyen).
    """
    import numpy as np
    
    # Simplified: exact match (production: embedding similarity)
    extracted_set = set(e.lower().strip() for e in extracted_entities)
    gt_set = set(e.lower().strip() for e in ground_truth_entities)
    
    correct = extracted_set & gt_set
    precision = len(correct) / len(extracted_set) if extracted_set else 0
    recall = len(correct) / len(gt_set) if gt_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "extracted": len(extracted_set),
        "ground_truth": len(gt_set),
        "correct": len(correct),
        "missed": list(gt_set - extracted_set)[:5],
        "hallucinated": list(extracted_set - gt_set)[:5],
    }

# Usage
print(evaluate_coverage(
    ["Alice", "Bob", "Phoenix", "Alice Nguyen"],  # extracted (có duplicate)
    ["Alice", "Bob", "Phoenix", "Atlas"],           # ground truth
))
# {'precision': 0.75, 'recall': 0.75, 'f1': 0.75, 'missed': ['atlas'], 'hallucinated': ['alice nguyen']}
```

---

## 2. Retrieval Evaluation

> **📌 Khái Niệm Cơ Bản:**
> **Retrieval Evaluation = đo "hệ thống tìm đúng thông tin không?"** Trước khi LLM trả lời, hệ thống phải *lấy đúng context từ graph*. Nếu retrieval lấy sai context → LLM trả lời sai dù model giỏi.
>
> **Analogies để nhớ 3 metrics chính:**
> - **Precision@k** = *độ chính xác* — "trong 5 thứ lấy ra, bao nhiêu cái ĐÚNG?" Lấy 5 nhưng 3 sai → precision thấp.
> - **Recall@k** = *độ đầy đủ* — "trong tổng N thứ đúng, mình bắt được bao nhiêu?" Có 10 sự thật nhưng chỉ lấy được 4 → recall thấp.
> - **MRR** = *độ nhanh gặp đúng* — "câu trả lời đúng nằm ở hạng bao nhiêu?" Đúng nằm đầu (rank 1) → điểm 1.0; nằm hạng 5 → 0.2.
>
> **Biểu thức Pre/Recall như phong phanh trong fishing:** Precision = trong rổ cá, mấy con ăn được. Recall = trong ao, mình vớt được bao nhiêu con cá có.

### 2.1 Metrics Cho Retrieval

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Công thức            │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Precision@K          │ % retrieved đúng trong top-K     │ |relevant ∩ retrieved| / K │
│ Recall@K             │ % ground truth được retrieve     │ |relevant ∩ retrieved| / |relevant| │
│ MRR (Mean Reciprocal)│ Vị trí trung bình của đáp án đúng│ mean(1/rank)         │
│ Path Precision       │ % paths trả về là đúng           │ |correct paths| / |all paths| │
│ Context Relevance    │ Retrieved context có liên quan?  │ LLM-as-judge (0-1)   │
│ Hop Accuracy         │ Số hops có đúng không?           │ |correct hops| / |total| │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Retrieval Evaluation (Click để xem)</summary>

```python
from typing import List, Dict

def precision_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & set(relevant))
    return hits / k

def recall_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & set(relevant))
    return hits / len(relevant) if relevant else 0

def mrr(retrieved: List[str], relevant: List[str]) -> float:
    for rank, doc_id in enumerate(retrieved, 1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0

def path_precision(retrieved_paths: List[List[str]], ground_truth_paths: List[List[str]]) -> float:
    """Đo: bao nhiêu paths trả về khớp với ground truth (exact hoặc subset)."""
    retrieved_set = set(tuple(p) for p in retrieved_paths)
    gt_set = set(tuple(p) for p in ground_truth_paths)
    hits = len(retrieved_set & gt_set)
    return hits / len(retrieved_set) if retrieved_set else 0

# Usage
retrieved = ["doc_1", "doc_3", "doc_5", "doc_7", "doc_9"]
relevant = ["doc_1", "doc_5", "doc_10"]

print(f"P@5: {precision_at_k(retrieved, relevant, 5):.2f}")  # 0.40 (2/5)
print(f"R@5: {recall_at_k(retrieved, relevant, 5):.2f}")     # 0.67 (2/3)
print(f"MRR: {mrr(retrieved, relevant):.2f}")                 # 1.00 (doc_1 ở rank 1)

# Path precision
retrieved_paths = [["Alice", "Bob", "Phoenix"], ["Alice", "Dave", "Atlas"]]
gt_paths = [["Alice", "Bob", "Phoenix"]]
print(f"Path P: {path_precision(retrieved_paths, gt_paths):.2f}")  # 0.50
```

</details>

### 2.2 So Sánh Vanilla RAG vs GraphRAG Retrieval

```python
def compare_retrieval(queries: List[Dict], vanilla_results: List[List[str]], 
                       graphrag_results: List[List[str]]) -> Dict:
    """
    So sánh retrieval quality giữa vanilla RAG và GraphRAG.
    
    queries: [{"query": "...", "relevant": ["doc_1", ...]}, ...]
    """
    vanilla_p, vanilla_r, graphrag_p, graphrag_r = [], [], [], []
    
    for q, v_ret, g_ret in zip(queries, vanilla_results, graphrag_results):
        relevant = q["relevant"]
        vanilla_p.append(precision_at_k(v_ret, relevant, 5))
        vanilla_r.append(recall_at_k(v_ret, relevant, 5))
        graphrag_p.append(precision_at_k(g_ret, relevant, 5))
        graphrag_r.append(recall_at_k(g_ret, relevant, 5))
    
    import numpy as np
    return {
        "vanilla": {"P@5": round(float(np.mean(vanilla_p)), 3), "R@5": round(float(np.mean(vanilla_r)), 3)},
        "graphrag": {"P@5": round(float(np.mean(graphrag_p)), 3), "R@5": round(float(np.mean(graphrag_r)), 3)},
        "delta": {"P@5": round(float(np.mean(graphrag_p) - np.mean(vanilla_p)), 3),
                  "R@5": round(float(np.mean(graphrag_r) - np.mean(vanilla_r)), 3)},
    }
```

---

## 3. Generation Evaluation (RAG)

### 3.1 RAGAS-Style Metrics

> **📌 Khái Niệm Cơ Bản:**
> **2 câu hỏi quan trọng nhất về chất lượng câu trả lời RAG:**
> - **Faithfulness (trung thành)** = *Có bịa không?* — mỗi claim (lời khẳng định) trong câu trả lời phải **nằm trong context** lấy từ graph. "Phoenix ngân sách 700 triệu" mà graph không có → không trung thành → hallucination.
> - **Answer Relevance (đáng trả lời)** = *Có trả lời đúng câu hỏi không?* — trả lời dài dòng nhưng không trúng câu hỏi = điểm thấp.
>
> **Analogies:** Faithfulness = "nhân chứng có khai bám vào bằng chứng không hay tự bịa?" Answer Relevance = "trả lời có đúng trọng tâm câu hỏi không?"
>
> **Cách đo (LLM-as-judge):** Tách câu trả lời thành các **claims** (mệnh đề nhỏ) → kiểm tra từng claim có trong context không. Hallucination Rate = 1 - Faithfulness.

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Ý nghĩa                          │ Đo thế nào           │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Faithfulness         │ Câu trả lời có grounded trong    │ LLM-as-judge: claims │
│                      │ context không? (không bịa)       │ có trong context?    │
│ Answer Relevance     │ Câu trả lời có trả lời đúng      │ LLM-as-judge: câu trả│
│                      │ câu hỏi không?                   │ lời liên quan?       │
│ Context Precision    │ Context có chứa thông tin cần?   │ LLM-as-judge         │
│ Hallucination Rate   │ % claims không có trong context  │ 1 - faithfulness     │
│ Citation Accuracy    │ % citations trỏ đúng source      │ Check path/source    │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Faithfulness & Hallucination Detection (Click để xem)</summary>

```python
import requests

OLLAMA_URL = "http://localhost:11434"

FAITHFULNESS_PROMPT = """Đánh giá xem câu trả lời có trung thành với context không.

Context:
{context}

Câu trả lời:
{answer}

Nhiệm vụ: Tách câu trả lời thành các claims (từng sự thật riêng lẻ), 
và đánh giá mỗi claim có được hỗ trợ bởi context không.

Trả về JSON:
{{"claims": [{{"claim": "...", "supported": true/false, "reason": "..."}}],
  "faithfulness": 0.0-1.0}}

faithfulness = số claims supported / tổng claims
"""

def evaluate_faithfulness(context: str, answer: str, model: str = "gemma3:12b") -> Dict:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        result = json.loads(resp.json()["response"])
        # Tính hallucination rate
        result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
        return result
    except:
        return {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": []}

# Usage
context = "Dự án Phoenix ngân sách 500 triệu, do Nguyễn Văn A phê duyệt. Team AI có 10 người."
answer_good = "Phoenix ngân sách 500 triệu, do Nguyễn Văn A duyệt."
answer_bad = "Phoenix ngân sách 700 triệu, do Trần Thị B duyệt. Team AI có 15 người."

print(evaluate_faithfulness(context, answer_good))
# {"faithfulness": 1.0, "hallucination_rate": 0.0, ...}

print(evaluate_faithfulness(context, answer_bad))
# {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": [
#   {"claim": "Phoenix ngân sách 700 triệu", "supported": false},
#   {"claim": "Trần Thị B duyệt Phoenix", "supported": false},
# ]}

# Graph-specific: citation accuracy
def evaluate_citation_accuracy(answer: str, cited_paths: List[List[str]], 
                                graph: "nx.Graph") -> Dict:
    """Kiểm tra citations (paths) có tồn tại trong graph không."""
    valid = 0
    for path in cited_paths:
        # Kiểm tra path có tồn tại trong graph không
        is_valid = True
        for i in range(len(path) - 1):
            if not graph.has_edge(path[i], path[i+1]):
                is_valid = False
                break
        if is_valid:
            valid += 1
    
    return {
        "total_citations": len(cited_paths),
        "valid_citations": valid,
        "citation_accuracy": valid / len(cited_paths) if cited_paths else 0,
    }
```

</details>

### 3.2 LLM-as-Judge Cho Global Sensemaking (Microsoft Pattern)

```python
JUDGE_PROMPT = """So sánh 2 câu trả lời cho cùng câu hỏi. Đánh giá theo 4 tiêu chí:

Câu hỏi: {question}

Câu trả lời A: {answer_a}
Câu trả lời B: {answer_b}

Đánh giá (thang 0-10 cho mỗi tiêu chí):
1. Comprehensiveness: bao quát đầy đủ khía cạnh?
2. Diversity: đa dạng góc nhìn?
3. Empowerment: giúp người đọc hiểu và hành động?
4. Directness: trả lời trực tiếp câu hỏi?

Trả về JSON:
{{"comprehensiveness": {{"A": 7, "B": 8, "winner": "B"}},
  "diversity": {{"A": 6, "B": 9, "winner": "B"}},
  ...,
  "overall_winner": "B"}}
"""

def llm_judge(question: str, answer_a: str, answer_b: str, model: str = "gemma3:12b") -> Dict:
    prompt = JUDGE_PROMPT.format(question=question, answer_a=answer_a, answer_b=answer_b)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        return json.loads(resp.json()["response"])
    except:
        return {"overall_winner": "unknown"}
```

---

## 4. Knowledge Graph Completion Metrics

Cho link prediction / KG completion (GNN, TransE, v.v.):

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric       │ Ý nghĩa                          │ Tốt khi              │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ Hits@K       │ % đáp án đúng trong top-K        │ Cao (Hits@10 > 0.5)  │
│ MRR          │ Mean Reciprocal Rank             │ Cao (>0.3)           │
│ MR (Mean Rank)│ Vị trí trung bình của đáp án    │ Thấp (<100)          │
│ AUC          │ Area under ROC cho link predict  │ Cao (>0.8)           │
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — KG Completion Evaluation (Click để xem)</summary>

```python
import torch

def evaluate_kg_completion(
    model, test_triples: list, all_entities: int, k_values: list = [1, 3, 10]
) -> dict:
    """
    Đánh giá KG completion.
    
    model: có method predict_tail(h, r) -> scores cho tất cả entities
    test_triples: [(h, r, t), ...] — ground truth
    """
    hits = {k: 0 for k in k_values}
    mrr = 0.0
    ranks = []
    
    for h, r, t_true in test_triples:
        scores = model.predict_tail(h, r, all_entities)  # (num_entities,)
        # Rank: vị trí của t_true khi sort scores tăng dần (thấp = tốt cho TransE)
        sorted_indices = torch.argsort(scores)
        rank = (sorted_indices == t_true).nonzero(as_tuple=True)[0].item() + 1  # 1-indexed
        ranks.append(rank)
        mrr += 1.0 / rank
        for k in k_values:
            if rank <= k:
                hits[k] += 1
    
    n = len(test_triples)
    return {
        **{f"Hits@{k}": round(hits[k] / n, 3) for k in k_values},
        "MRR": round(mrr / n, 3),
        "MR": round(sum(ranks) / n, 1),
        "num_test": n,
    }

# Usage (với TransE model từ 04-graph-embeddings)
# metrics = evaluate_kg_completion(transe_model, test_triples, num_entities=1000)
# print(metrics)
# {'Hits@1': 0.15, 'Hits@10': 0.45, 'MRR': 0.28, 'MR': 85.3, 'num_test': 100}
```

</details>

---

## 5. Benchmarks & Datasets

### 5.1 Benchmarks Cho GraphRAG

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Task                 │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ HotpotQA             │ Multi-hop QA (2 hops)│ EM, F1                       │
│ 2WikiMultihopQA      │ Multi-hop (2-4 hops) │ EM, F1                       │
│ MuSiQue              │ Multi-hop (2-4 hops) │ EM, F1 (khó hơn)             │
│ Natural Questions    │ Open-domain QA       │ EM                           │
│ GraphRAG-Bench (MSFT)│ Domain KGQA, 1018 câu│ Multi-hop + single-hop +   │
│                      │ 5 dạng câu hỏi       │ explainability (reasoning)  │
│ KGHaluBench          │ KG-rag hallucination │ Hallucination rate           │
│ Custom Enterprise QA │ Domain-specific      │ Faithfulness, P@K, MRR       │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.2 Benchmarks Cho KG Completion

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Triples              │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ FB15k-237            │ 310K (Freebase)      │ Hits@10, MRR                 │
│ WN18RR               │ 93K (WordNet)        │ Hits@10, MRR                 │
│ OGB-WikiKG2          │ 17M (Wikidata)       │ MRR                          │
│ Custom Enterprise KG │ Tùy domain           │ Hits@K, coverage             │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.3 Tạo Custom Benchmark

```python
# Tạo benchmark từ chính documents của bạn

def create_custom_benchmark(documents: List[str], num_questions: int = 20) -> List[Dict]:
    """
    Tự động tạo benchmark: dùng LLM sinh câu hỏi + đáp án từ documents.
    Cần human review sau đó!
    """
    questions = []
    for doc in documents[:num_questions]:
        prompt = f"""Từ tài liệu sau, tạo 1 câu hỏi và đáp án.

Tài liệu: {doc[:1000]}

Trả về JSON:
{{"question": "...", "answer": "...", "relevant_docs": ["..."], "type": "factoid/multi-hop/global"}}

Câu hỏi nên đa dạng: factoid, multi-hop, global.
"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": "gemma3:12b", "prompt": prompt, "stream": False, "format": "json"
        })
        import json
        try:
            q = json.loads(resp.json()["response"])
            q["source_doc"] = doc[:200]
            questions.append(q)
        except:
            continue
    return questions
```

### 5.4 Những "Lỗ Hổng Đánh Giá" Trong GraphRAG (2025-2026)

> **📌 Khái Niệm Cơ Bản — đánh giá GraphRAG chỉ đo retrieval/faithfulness là CHƯA đủ.** Nghiên cứu mới chỉ ra 3 thiếu hụt hay gặp trong pipeline đánh giá hiện tại:

**1. Thiếu "Evidence Recall" & "Context Relevancy"** — Hầu hết hệ thống chỉ đo *"câu trả lời có khớp đáp án không"* (EM/F1) mà không đo *"chứng cớ đưa vào LLM có đúng/đủ không"*.
- **Evidence Recall** = trong các bằng chứng LLM nhận được (chunks + path graph), bao nhiêu % **thực sự cần để trả lời** câu hỏi đó đã được đưa vào.
- **Context Relevancy** = bằng chứng đưa vào có **dư thừa ngoài lề** bao nhiêu. Đo bằng câu hỏi nhỏ: *"Trong context này, câu nào không giúp trả lời câu hỏi?"*
- Vì sao quan trọng: EM/F1 cao mà evidence lệch → system không tin tưởng được (retrieval sai nhưng LLM "mạnh miệng" đoán trúng — *lucky*).

**2. Retrieval Drift (CS-RAG)** — Hệ thống RAG nhiều bước (như agentic/DRIFT) có thể **lệch hướng** giữa chừng: bước 1 đúng anchor nhưng bước 2 không theo hướng câu hỏi nữa → trả lời trôi ra ngoài. Cách đo: giám sát **độ 'bám câu hỏi'** của từng hop retrieval (attention/score của hop với câu hỏi gốc).

**3. KGHaluBench & Hallucination đặc thù KG** — Hallucination trong GraphRAG có 2 nguồn khác vanilla RAG:
- **Graph hallucination**: KG tự xây bị trích sai triplet (entity Linking sai → answer kéo theo sai).
- **Summary hallucination**: community summary của LLM "bịa" chi tiết không có trong graph.
- **KGHaluBench** đo riêng rate hallucination khi bối cảnh gốc là graph thay vì text. Cần đánh giá **riêng từng nguồn** — đừng gộp chung vào 1 chỉ số faithfulness.

**4. Systematic Eval RAG vs GraphRAG — đừng tự tin thái quá** — Kết quả benchmark có hệ thống 2025-2026: GraphRAG thắng trên multi-hop/global nhưng **thua vanilla RAG trên single-hop/factoid**. Vì vậy evaluation của bạn nên **chia 3 track** (single-hop / multi-hop / global) và báo cáo riêng — như Module 05 đã cảnh báo.

```python
# Đo Evidence Recall trên kết quả retrieval
def evidence_recall(gold_evidence: list[str], retrieved: list[str]) -> float:
    """% bằng chứng 'vàng' nằm trong các đoạn đưa vào LLM."""
    r = set(c.lower() for c in retrieved)
    hit = sum(1 for ev in gold_evidence if ev.lower() in r)
    return hit / len(gold_evidence) if gold_evidence else 1.0

# Context Relevancy (đơn giản hoá — ngưỡng theo lần đánh giá thủ công)
def context_relevancy(retrieved: list[str], question: str) -> float:
    """Tỷ lệ đoạn thực sự liên quan trong context (điểm từ LLM-as-judge)."""
    ...
```

---

## 6. Evaluation Framework

<details>
<summary>Python Code — Complete Evaluation Pipeline (Click để xem)</summary>

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime
import json

@dataclass
class EvalResult:
    run_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    graph_quality: Dict = field(default_factory=dict)
    retrieval_metrics: Dict = field(default_factory=dict)
    generation_metrics: Dict = field(default_factory=dict)
    kg_completion_metrics: Dict = field(default_factory=dict)
    overall_score: float = 0.0

class GraphEvaluationFramework:
    """
    Framework đánh giá toàn diện cho Graph Engineering.
    
    Chạy: Graph Quality → Retrieval → Generation → KG Completion
    Output: Report JSON + Markdown
    """
    
    def __init__(self, graph, model_name: str = "gemma3:12b"):
        self.graph = graph
        self.model_name = model_name
        self.results: List[EvalResult] = []
    
    def evaluate_graph_quality(self, ontology=None) -> Dict:
        print("  📊 Evaluating graph quality...")
        metrics = evaluate_graph_quality(self.graph, ontology)
        print(f"    Nodes: {metrics['nodes']}, Edges: {metrics['edges']}, "
              f"Connectivity: {metrics['connectivity']:.0%}, Isolated: {metrics['isolated_rate']:.0%}")
        return metrics
    
    def evaluate_retrieval(self, queries: List[Dict],
                           retrieval_fn) -> Dict:
        """
        retrieval_fn: (query: str) -> List[str] (retrieved doc_ids)
        """
        print(f"  🔍 Evaluating retrieval on {len(queries)} queries...")
        precisions, recalls, mrrs = [], [], []
        for q in queries:
            retrieved = retrieval_fn(q["query"])
            relevant = q["relevant"]
            precisions.append(precision_at_k(retrieved, relevant, 5))
            recalls.append(recall_at_k(retrieved, relevant, 5))
            mrrs.append(mrr(retrieved, relevant))
        
        import numpy as np
        return {
            "P@5": round(float(np.mean(precisions)), 3),
            "R@5": round(float(np.mean(recalls)), 3),
            "MRR": round(float(np.mean(mrrs)), 3),
            "num_queries": len(queries),
        }
    
    def evaluate_generation(self, qa_pairs: List[Dict],
                            generation_fn) -> Dict:
        """
        generation_fn: (query: str, context: str) -> str (answer)
        qa_pairs: [{"query": "...", "context": "...", "expected": "..."}, ...]
        """
        print(f"  💬 Evaluating generation on {len(qa_pairs)} QA pairs...")
        faithfulness_scores = []
        for qa in qa_pairs:
            answer = generation_fn(qa["query"], qa["context"])
            result = evaluate_faithfulness(qa["context"], answer, self.model_name)
            faithfulness_scores.append(result.get("faithfulness", 0))
        
        import numpy as np
        avg_faith = float(np.mean(faithfulness_scores)) if faithfulness_scores else 0
        return {
            "faithfulness": round(avg_faith, 3),
            "hallucination_rate": round(1 - avg_faith, 3),
            "num_qa": len(qa_pairs),
        }
    
    def run_full_evaluation(
        self, queries: List[Dict] = None,
        qa_pairs: List[Dict] = None,
        retrieval_fn=None, generation_fn=None,
        ontology=None,
    ) -> EvalResult:
        import uuid
        result = EvalResult(run_id=str(uuid.uuid4())[:8])
        
        print(f"\n{'='*60}")
        print(f"  Evaluation Run: {result.run_id}")
        print(f"{'='*60}")
        
        # 1. Graph quality
        result.graph_quality = self.evaluate_graph_quality(ontology)
        
        # 2. Retrieval
        if queries and retrieval_fn:
            result.retrieval_metrics = self.evaluate_retrieval(queries, retrieval_fn)
            print(f"    P@5: {result.retrieval_metrics['P@5']}, "
                  f"R@5: {result.retrieval_metrics['R@5']}, "
                  f"MRR: {result.retrieval_metrics['MRR']}")
        
        # 3. Generation
        if qa_pairs and generation_fn:
            result.generation_metrics = self.evaluate_generation(qa_pairs, generation_fn)
            print(f"    Faithfulness: {result.generation_metrics['faithfulness']}, "
                  f"Hallucination: {result.generation_metrics['hallucination_rate']}")
        
        # Overall score (weighted)
        gq = 1 - result.graph_quality.get("isolated_rate", 0) - result.graph_quality.get("invalid_rate", 0)
        rm = result.retrieval_metrics.get("MRR", 0)
        gm = result.generation_metrics.get("faithfulness", 0)
        # Nếu thiếu metrics, chỉ tính những gì có
        scores = [s for s in [gq, rm, gm] if s > 0]
        result.overall_score = round(sum(scores) / len(scores), 3) if scores else round(gq, 3)
        
        print(f"\n  ⭐ Overall Score: {result.overall_score:.3f}")
        self.results.append(result)
        return result
    
    def generate_report(self, result: EvalResult, format: str = "markdown") -> str:
        if format == "json":
            return json.dumps(result.__dict__, indent=2, ensure_ascii=False)
        
        # Markdown
        report = f"""# Graph Evaluation Report — {result.run_id}

> Generated: {result.timestamp} | Model: {self.model_name}

## Graph Quality

| Metric | Value |
|--------|-------|
| Nodes | {result.graph_quality.get('nodes', '-')} |
| Edges | {result.graph_quality.get('edges', '-')} |
| Connectivity | {result.graph_quality.get('connectivity', '-')} |
| Isolated Rate | {result.graph_quality.get('isolated_rate', '-')} |
| Invalid Edge Rate | {result.graph_quality.get('invalid_rate', '-')} |

## Retrieval

| Metric | Value |
|--------|-------|
| P@5 | {result.retrieval_metrics.get('P@5', '-')} |
| R@5 | {result.retrieval_metrics.get('R@5', '-')} |
| MRR | {result.retrieval_metrics.get('MRR', '-')} |

## Generation

| Metric | Value |
|--------|-------|
| Faithfulness | {result.generation_metrics.get('faithfulness', '-')} |
| Hallucination Rate | {result.generation_metrics.get('hallucination_rate', '-')} |

## Overall Score: {result.overall_score:.3f} / 1.0
"""
        return report

# Usage
import networkx as nx
G = nx.karate_club_graph()
G = nx.relabel_nodes(G, {n: f"n{n}" for n in G.nodes()})
for n in G.nodes():
    G.nodes[n]["type"] = "Person"

framework = GraphEvaluationFramework(G)
result = framework.run_full_evaluation()
print(framework.generate_report(result))
```

</details>

---

## 7. Labs Thực Hành

### Lab 1: Đánh Giá Graph Quality

1. Tạo 2 graphs: 1 tốt (đầy đủ, connected) và 1 tệ (nhiều isolated, duplicate)
2. Chạy `evaluate_graph_quality` cho cả 2, so sánh metrics

### Lab 2: So Sánh Vanilla RAG vs GraphRAG

1. Chuẩn bị 20 queries với ground truth `relevant` docs
2. Chạy cả 2 retrievers, đo P@5, R@5, MRR
3. Dùng `llm_judge` cho 5 global queries — GraphRAG phải thắng

### Lab 3: Hallucination Measurement

1. Tạo 20 QA pairs với `context` + `expected answer`
2. Cho LLM generate với context đúng vs không có context
3. Đo faithfulness — có context phải >0.8, không context hallucination cao

---

## Tài Liệu Tham Khảo

- Microsoft GraphRAG — *Evaluation: LLM-as-Judge* (https://microsoft.github.io/graphrag/)
- RAGAS — *RAG Assessment* (https://docs.ragas.io/)
- OGB — *Open Graph Benchmark Evaluation* (https://ogb.stanford.edu/docs/score/)
- HotpotQA — *Leaderboard* (https://hotpotqa.github.io/)
- *GraphRAG-Bench: A Domain-Specific Benchmark for GraphRAG* (arXiv:2506.02404) — 1018 câu, 5 dạng
- *KGHaluBench* — KG-augmented hallucination benchmark (2025)
- *CS-RAG: Retrieval Drift in Multi-Step RAG* (2025)
- *RAG vs GraphRAG: A Systematic Evaluation* (arXiv 2025) — tách 3 track single/multi/global
- *A Survey on Evaluation of Knowledge Graph Quality* — Paulheim (2017)

---

*Hoàn thành Graph Engineering Track — quay lại [README](../README.md) để tổng kết.*
