# 📊 09. Evaluation — Evaluating Graph & GraphRAG Quality

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Is Evaluation Important?](#why-is-evaluation-important)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Graph Quality Metrics](#1-graph-quality-metrics)
> - [2. Retrieval Evaluation](#2-retrieval-evaluation)
> - [3. Generation Evaluation (RAG)](#3-generation-evaluation-rag)
> - [4. Knowledge Graph Completion Metrics](#4-knowledge-graph-completion-metrics)
> - [5. Benchmarks & Datasets](#5-benchmarks--datasets)
> - [6. Evaluation Framework](#6-evaluation-framework)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You've built your GraphRAG and demo it to your boss: *"Ask anything, it answers!"*

The boss asks 3 questions:

1. *"What's the Phoenix project budget?"* → Answer: "500 million" ✅ (correct, it's in the doc)
2. *"Who approved Phoenix?"* → Answer: "Alice" ✅ (correct, but confidence is 0.6 — low!)
3. *"How many people are on the AI team?"* → Answer: "15 people" ❌ (the doc says 10 — the LLM hallucinated)

Without an evaluation framework, you **don't know** what % your GraphRAG is correct, what % is hallucination, and **why** it's wrong (bad extraction? bad retrieval? bad generation?).

**Evaluation is how you turn a "cool demo" into "production you can trust."**

### Why Is Evaluation Important?

> *"If you can't measure it, you can't improve it. If you can't separate retrieval from generation, you don't know where to fix."*
> — RAG Evaluation Best Practices (2024)

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | LLM-as-judge (comprehensiveness, diversity) distinguishes GraphRAG vs vanilla RAG at **p<0.01** |
| 2 | **RAGAS Framework (2024)** | Separating faithfulness (generation) from context relevance (retrieval) cuts **debug time by 50%** |
| 3 | **OGB + FB15k-237** | KG completion: Hits@10 and MRR are the standard metrics — don't use plain accuracy |

---

## Overview

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

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Graph Quality](#1-graph-quality-metrics) | Coverage, connectivity, density |
| 2 | [Retrieval](#2-retrieval-evaluation) | Precision, recall, MRR, path precision |
| 3 | [Generation](#3-generation-evaluation-rag) | Faithfulness, hallucination, LLM-as-judge |
| 4 | [KG Completion](#4-knowledge-graph-completion-metrics) | Hits@K, MRR, MR |
| 5 | [Benchmarks](#5-benchmarks--datasets) | HotpotQA, GraphRAG-Bench, KGHaluBench, evidence recall |
| 6 | [Framework](#6-evaluation-framework) | Evaluation pipeline code |

---

## 1. Graph Quality Metrics

> **📌 Core Concept:**
> **Before asking "does the AI answer correctly", ask "is the graph good?"** If the graph is incomplete or wrong, the RAG results are meaningless no matter how perfect the code is (GIGO — garbage in, garbage out).
>
> **9 measures of graph health.** Use these analogies:
>
> - **Node/Edge Coverage** = *coverage* — "what % of the facts did we extract from the documents?" Like a knowledge check: miss 30% of the knowledge and you only get 70% of the answers right.
> - **Duplicate Rate** = *cleanliness* — "how many entities are duplicated?" Like a phone book listing "Nguyen Van A" and "NV A" as two people → queries get split.
> - **Connectivity** = *connectedness* — "are the nodes linked together or scattered?" A graph broken into fragments → multi-hop queries can't reach the other fragment.
> - **Density / Avg Degree** = *thickness* — too sparse a graph → missing connections; too dense → noise.
> - **Isolated Nodes** = nodes **with no relationships at all** — useless, just taking up space.
> - **Invalid Edge Rate** = edges **violating the rules** (Person → MANAGES → Document) — must be 0%.
> - **Temporal Freshness** = old edges that have **expired** but weren't updated — answering with stale information.

### 1.1 Metrics for the Graph Itself

Before measuring retrieval/generation, measure **whether the graph is good**:

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ Good when            │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Node Coverage        │ % of real entities extracted     │ High (>80%)          │
│ Edge Coverage        │ % of real relations extracted    │ High (>70%)          │
│ Duplicate Rate       │ % duplicate nodes (not dedup'd)  │ Low (<5%)            │
│ Connectivity         │ % of nodes in the largest component │ High (>90%)      │
│ Density              │ 2|E| / |V|(|V|-1)                │ Domain-dependent     │
│ Avg Degree           │ Average relations per node       │ 3-10 (enterprise)    │
│ Isolated Nodes       │ Nodes with no edges at all       │ Low (<5%)            │
│ Invalid Edge Rate    │ % of edges violating the ontology│ 0%                   │
│ Temporal Freshness   │ % of edges still valid (not expired) │ High (>95%)     │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Graph Quality Metrics (Click to view)</summary>

```python
import networkx as nx
from typing import Dict, List

def evaluate_graph_quality(graph: nx.Graph, ontology=None) -> Dict:
    """Measure graph quality."""
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
    
    # Invalid edges (if there's an ontology)
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

### 1.2 Coverage — Against Ground Truth

```python
def evaluate_coverage(
    extracted_entities: List[str],
    ground_truth_entities: List[str],
    threshold: float = 0.85,  # embedding similarity threshold
) -> Dict:
    """
    Measure coverage: how many ground truth entities were extracted correctly.
    
    Uses embedding similarity for fuzzy matching (Alice ≈ Alice Nguyen).
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
    ["Alice", "Bob", "Phoenix", "Alice Nguyen"],  # extracted (has duplicates)
    ["Alice", "Bob", "Phoenix", "Atlas"],           # ground truth
))
# {'precision': 0.75, 'recall': 0.75, 'f1': 0.75, 'missed': ['atlas'], 'hallucinated': ['alice nguyen']}
```

---

## 2. Retrieval Evaluation

> **📌 Core Concept:**
> **Retrieval Evaluation = measuring "did the system find the right information?"** Before the LLM answers, the system must *pull the right context from the graph*. If retrieval pulls the wrong context → the LLM answers wrong no matter how good the model is.
>
> **Analogies to remember the 3 main metrics:**
> - **Precision@k** = *accuracy* — "of the 5 items retrieved, how many are RIGHT?" Retrieved 5 but 3 are wrong → low precision.
> - **Recall@k** = *completeness* — "of all N correct items total, how many did we catch?" There are 10 facts but we only retrieved 4 → low recall.
> - **MRR** = *how fast the correct answer appears* — "at what rank is the correct answer?" Correct at the top (rank 1) → score 1.0; at rank 5 → 0.2.
>
> **Think of the Precision/Recall formulas through a fishing analogy:** Precision = of the fish in the basket, how many are edible. Recall = of the fish in the pond, how many of the fish that exist did you catch.

### 2.1 Metrics for Retrieval

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ Formula              │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Precision@K          │ % of top-K retrieved that are right │ |relevant ∩ retrieved| / K │
│ Recall@K             │ % of ground truth that was retrieved │ |relevant ∩ retrieved| / |relevant| │
│ MRR (Mean Reciprocal)│ Average rank position of the correct answer │ mean(1/rank)    │
│ Path Precision       │ % of returned paths that are correct │ |correct paths| / |all paths| │
│ Context Relevance    │ Is the retrieved context related?  │ LLM-as-judge (0-1)   │
│ Hop Accuracy         │ Is the hop count right?            │ |correct hops| / |total| │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Retrieval Evaluation (Click to view)</summary>

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
    """Measure: how many returned paths match the ground truth (exact or subset)."""
    retrieved_set = set(tuple(p) for p in retrieved_paths)
    gt_set = set(tuple(p) for p in ground_truth_paths)
    hits = len(retrieved_set & gt_set)
    return hits / len(retrieved_set) if retrieved_set else 0

# Usage
retrieved = ["doc_1", "doc_3", "doc_5", "doc_7", "doc_9"]
relevant = ["doc_1", "doc_5", "doc_10"]

print(f"P@5: {precision_at_k(retrieved, relevant, 5):.2f}")  # 0.40 (2/5)
print(f"R@5: {recall_at_k(retrieved, relevant, 5):.2f}")     # 0.67 (2/3)
print(f"MRR: {mrr(retrieved, relevant):.2f}")                 # 1.00 (doc_1 at rank 1)

# Path precision
retrieved_paths = [["Alice", "Bob", "Phoenix"], ["Alice", "Dave", "Atlas"]]
gt_paths = [["Alice", "Bob", "Phoenix"]]
print(f"Path P: {path_precision(retrieved_paths, gt_paths):.2f}")  # 0.50
```

</details>

### 2.2 Comparing Vanilla RAG vs GraphRAG Retrieval

```python
def compare_retrieval(queries: List[Dict], vanilla_results: List[List[str]], 
                       graphrag_results: List[List[str]]) -> Dict:
    """
    Compare retrieval quality between vanilla RAG and GraphRAG.
    
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

> **📌 Core Concept:**
> **The 2 most important questions about RAG answer quality:**
> - **Faithfulness** = *Did it make things up?* — every claim in the answer must **be grounded in the context** pulled from the graph. "Phoenix's budget is 700 million" when the graph doesn't say that → not faithful → hallucination.
> - **Answer Relevance** = *Does it actually answer the question?* — a long-winded answer that misses the point of the question scores low.
>
> **Analogies:** Faithfulness = "does the witness stick to the evidence or make things up?" Answer Relevance = "does the answer hit the heart of the question?"
>
> **How to measure (LLM-as-judge):** Split the answer into **claims** (small statements) → check whether each claim is in the context. Hallucination Rate = 1 - Faithfulness.

```
┌──────────────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric               │ Meaning                          │ How it's measured    │
├──────────────────────┼──────────────────────────────────┼──────────────────────┤
│ Faithfulness         │ Is the answer grounded in the    │ LLM-as-judge: are the│
│                      │ context? (no fabrication)        │ claims in the context?│
│ Answer Relevance     │ Does the answer actually answer  │ LLM-as-judge: is the │
│                      │ the question?                    │ answer relevant?     │
│ Context Precision    │ Does the context contain the needed info? │ LLM-as-judge  │
│ Hallucination Rate   │ % of claims not in the context   │ 1 - faithfulness     │
│ Citation Accuracy    │ % of citations that point to the right source │ Check path/source │
└──────────────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — Faithfulness & Hallucination Detection (Click to view)</summary>

```python
import requests

OLLAMA_URL = "http://localhost:11434"

FAITHFULNESS_PROMPT = """Evaluate whether the answer is faithful to the context.

Context:
{context}

Answer:
{answer}

Task: Split the answer into claims (individual facts),
and assess whether each claim is supported by the context.

Return JSON:
{{"claims": [{{"claim": "...", "supported": true/false, "reason": "..."}}],
  "faithfulness": 0.0-1.0}}

faithfulness = number of supported claims / total claims
"""

def evaluate_faithfulness(context: str, answer: str, model: str = "gemma3:12b") -> Dict:
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model, "prompt": prompt, "stream": False, "format": "json"
    })
    import json
    try:
        result = json.loads(resp.json()["response"])
        # Compute the hallucination rate
        result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
        return result
    except:
        return {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": []}

# Usage
context = "The Phoenix project has a budget of 500 million, approved by Nguyen Van A. The AI team has 10 people."
answer_good = "Phoenix's budget is 500 million, approved by Nguyen Van A."
answer_bad = "Phoenix's budget is 700 million, approved by Tran Thi B. The AI team has 15 people."

print(evaluate_faithfulness(context, answer_good))
# {"faithfulness": 1.0, "hallucination_rate": 0.0, ...}

print(evaluate_faithfulness(context, answer_bad))
# {"faithfulness": 0.0, "hallucination_rate": 1.0, "claims": [
#   {"claim": "Phoenix's budget is 700 million", "supported": false},
#   {"claim": "Tran Thi B approved Phoenix", "supported": false},
# ]}

# Graph-specific: citation accuracy
def evaluate_citation_accuracy(answer: str, cited_paths: List[List[str]], 
                                graph: "nx.Graph") -> Dict:
    """Check that citations (paths) exist in the graph."""
    valid = 0
    for path in cited_paths:
        # Check whether the path exists in the graph
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

### 3.2 LLM-as-Judge for Global Sensemaking (Microsoft Pattern)

```python
JUDGE_PROMPT = """Compare two answers to the same question. Evaluate on 4 criteria:

Question: {question}

Answer A: {answer_a}
Answer B: {answer_b}

Evaluate (0-10 scale for each criterion):
1. Comprehensiveness: does it cover the aspects fully?
2. Diversity: does it offer diverse perspectives?
3. Empowerment: does it help the reader understand and act?
4. Directness: does it answer the question directly?

Return JSON:
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

For link prediction / KG completion (GNN, TransE, etc.):

```
┌──────────────┬──────────────────────────────────┬──────────────────────┐
│ Metric       │ Meaning                          │ Good when            │
├──────────────┼──────────────────────────────────┼──────────────────────┤
│ Hits@K       │ % of correct answers in the top-K│ High (Hits@10 > 0.5) │
│ MRR          │ Mean Reciprocal Rank             │ High (>0.3)          │
│ MR (Mean Rank)│ Average rank position of the answer │ Low (<100)       │
│ AUC          │ Area under ROC for link prediction │ High (>0.8)        │
└──────────────┴──────────────────────────────────┴──────────────────────┘
```

<details>
<summary>Python Code — KG Completion Evaluation (Click to view)</summary>

```python
import torch

def evaluate_kg_completion(
    model, test_triples: list, all_entities: int, k_values: list = [1, 3, 10]
) -> dict:
    """
    Evaluate KG completion.
    
    model: has a predict_tail(h, r) method -> scores for all entities
    test_triples: [(h, r, t), ...] — ground truth
    """
    hits = {k: 0 for k in k_values}
    mrr = 0.0
    ranks = []
    
    for h, r, t_true in test_triples:
        scores = model.predict_tail(h, r, all_entities)  # (num_entities,)
        # Rank: position of t_true when sorting scores ascending (low = good for TransE)
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

# Usage (with a TransE model from 04-graph-embeddings)
# metrics = evaluate_kg_completion(transe_model, test_triples, num_entities=1000)
# print(metrics)
# {'Hits@1': 0.15, 'Hits@10': 0.45, 'MRR': 0.28, 'MR': 85.3, 'num_test': 100}
```

</details>

---

## 5. Benchmarks & Datasets

### 5.1 Benchmarks for GraphRAG

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Task                 │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ HotpotQA             │ Multi-hop QA (2 hops)│ EM, F1                       │
│ 2WikiMultihopQA      │ Multi-hop (2-4 hops) │ EM, F1                       │
│ MuSiQue              │ Multi-hop (2-4 hops) │ EM, F1 (harder)              │
│ Natural Questions    │ Open-domain QA       │ EM                           │
│ GraphRAG-Bench (MSFT)│ Domain KGQA, 1018 questions, 5 question types │ Multi-hop + single-hop + explainability (reasoning) │
│ KGHaluBench          │ KG-RAG hallucination │ Hallucination rate           │
│ Custom Enterprise QA │ Domain-specific      │ Faithfulness, P@K, MRR       │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.2 Benchmarks for KG Completion

```
┌──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Benchmark            │ Triples              │ Metric                       │
├──────────────────────┼──────────────────────┼──────────────────────────────┤
│ FB15k-237            │ 310K (Freebase)      │ Hits@10, MRR                 │
│ WN18RR               │ 93K (WordNet)        │ Hits@10, MRR                 │
│ OGB-WikiKG2          │ 17M (Wikidata)       │ MRR                          │
│ Custom Enterprise KG │ Domain-dependent     │ Hits@K, coverage             │
└──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 5.3 Creating a Custom Benchmark

```python
# Create a benchmark from your own documents

def create_custom_benchmark(documents: List[str], num_questions: int = 20) -> List[Dict]:
    """
    Automatically create a benchmark: use an LLM to generate questions + answers from the documents.
    Requires human review afterwards!
    """
    questions = []
    for doc in documents[:num_questions]:
        prompt = f"""From the document below, create 1 question and its answer.

Document: {doc[:1000]}

Return JSON:
{{"question": "...", "answer": "...", "relevant_docs": ["..."], "type": "factoid/multi-hop/global"}}

Questions should be diverse: factoid, multi-hop, global.
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

### 5.4 The "Evaluation Gaps" in GraphRAG (2025-2026)

> **📌 Core Concept — evaluating GraphRAG by measuring only retrieval/faithfulness is NOT enough.** New research shows 3 common gaps in today's evaluation pipelines:

**1. Missing "Evidence Recall" & "Context Relevancy"** — most systems only measure *"does the answer match the expected answer"* (EM/F1), not *"was the evidence fed to the LLM correct/sufficient"*.
- **Evidence Recall** = of the evidence the LLM received (chunks + graph paths), what % was **actually needed to answer** the question.
- **Context Relevancy** = how much **irrelevant filler** was in the evidence fed in. Measured with a small question: *"In this context, which sentences do not help answer the question?"*
- Why it matters: high EM/F1 with skewed evidence → the system can't be trusted (retrieval was wrong but the LLM "bluffed" its way to the right answer — *lucky*).

**2. Retrieval Drift (CS-RAG)** — multi-step RAG systems (agentic/DRIFT, etc.) can **drift off track** partway through: step 1 has the right anchor but step 2 no longer follows the question → the answer drifts off course. How to measure: monitor the **"question anchoring"** of each retrieval hop (the hop's attention/score relative to the original question).

**3. KGHaluBench & KG-specific Hallucination** — GraphRAG hallucinations have 2 sources different from vanilla RAG:
- **Graph hallucination**: the self-built KG has a wrongly-extracted triplet (bad entity linking → the answer follows wrong).
- **Summary hallucination**: the LLM's community summary "fabricates" details that aren't in the graph.
- **KGHaluBench** measures the hallucination rate specifically when the underlying context is a graph instead of text. You need to evaluate **each source separately** — don't lump them into one faithfulness number.

**4. Systematic RAG vs GraphRAG Evaluation — don't be overconfident** — systematic benchmark results from 2025-2026: GraphRAG wins on multi-hop/global but **loses to vanilla RAG on single-hop/factoid**. So your evaluation should **split into 3 tracks** (single-hop / multi-hop / global) and report each separately — as Module 05 warned.

```python
# Measure Evidence Recall on retrieval results
def evidence_recall(gold_evidence: list[str], retrieved: list[str]) -> float:
    """% of the 'gold' evidence that made it into the chunks fed to the LLM."""
    r = set(c.lower() for c in retrieved)
    hit = sum(1 for ev in gold_evidence if ev.lower() in r)
    return hit / len(gold_evidence) if gold_evidence else 1.0

# Context Relevancy (simplified — threshold from manual evaluations)
def context_relevancy(retrieved: list[str], question: str) -> float:
    """The fraction of context passages that are actually relevant (scored by LLM-as-judge)."""
    ...
```

---

## 6. Evaluation Framework

<details>
<summary>Python Code — Complete Evaluation Pipeline (Click to view)</summary>

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
    A comprehensive evaluation framework for Graph Engineering.
    
    Runs: Graph Quality → Retrieval → Generation → KG Completion
    Output: JSON + Markdown report
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
        # If some metrics are missing, only compute from what's available
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

## 7. Hands-On Labs

### Lab 1: Evaluate Graph Quality

1. Create 2 graphs: 1 good (complete, connected) and 1 bad (many isolated, many duplicates)
2. Run `evaluate_graph_quality` on both, compare the metrics

### Lab 2: Compare Vanilla RAG vs GraphRAG

1. Prepare 20 queries with ground-truth `relevant` docs
2. Run both retrievers, measure P@5, R@5, MRR
3. Use `llm_judge` on 5 global queries — GraphRAG must win

### Lab 3: Hallucination Measurement

1. Create 20 QA pairs with `context` + `expected answer`
2. Have the LLM generate with the correct context vs without context
3. Measure faithfulness — with context it should be >0.8, without context the hallucination rate is high

---

## References

- Microsoft GraphRAG — *Evaluation: LLM-as-Judge* (https://microsoft.github.io/graphrag/)
- RAGAS — *RAG Assessment* (https://docs.ragas.io/)
- OGB — *Open Graph Benchmark Evaluation* (https://ogb.stanford.edu/docs/score/)
- HotpotQA — *Leaderboard* (https://hotpotqa.github.io/)
- *GraphRAG-Bench: A Domain-Specific Benchmark for GraphRAG* (arXiv:2506.02404) — 1018 questions, 5 types
- *KGHaluBench* — KG-augmented hallucination benchmark (2025)
- *CS-RAG: Retrieval Drift in Multi-Step RAG* (2025)
- *RAG vs GraphRAG: A Systematic Evaluation* (arXiv 2025) — splits into 3 tracks: single/multi/global
- *A Survey on Evaluation of Knowledge Graph Quality* — Paulheim (2017)

---

*End of the Graph Engineering Track — return to [README](../README.md) for the wrap-up.*
