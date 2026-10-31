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

This is **not** a simple lookup question — it takes a bit of **reasoning**:

1. Is `MANAGES` transitive? Alice manages Bob — is Bob in "Alice's team"?
2. Does `WORKS_ON → Atlas` count as "working on AI"? Does Atlas have the property `domain: AI`?
3. Do I need to traverse `Alice → Bob → Phoenix → Atlas` (3 hops) to connect them?

**Graph Reasoning** turns these fuzzy questions into **clear steps you can run**: rules, path limits, and chains of logic you can check.

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

> 📄 **Example code:** [`examples/01-1-1-bfs-vs-dfs-vs-constrained.py`](examples/01-1-1-bfs-vs-dfs-vs-constrained.py)

</details>

### 1.2 Sampling for Large Graphs

On graphs of 1M+ nodes, you can't traverse the whole thing:

> 📄 **Example code:** [`examples/02-1-2-sampling-for-large-graphs.py`](examples/02-1-2-sampling-for-large-graphs.py)

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

> 📄 **Example code:** [`examples/03-2-1-the-kinds-of-path-finding.py`](examples/03-2-1-the-kinds-of-path-finding.py)

</details>

### 2.2 Cypher Path Queries

> 📄 **Example code:** [`examples/04-2-2-cypher-path-queries.cypher`](examples/04-2-2-cypher-path-queries.cypher)

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

> 📄 **Example code:** [`examples/05-3-1-rule-based-inference.py`](examples/05-3-1-rule-based-inference.py)

### 3.2 Confidence Propagation

When inferring across multiple steps, confidence drops:

> 📄 **Example code:** [`examples/06-3-2-confidence-propagation.py`](examples/06-3-2-confidence-propagation.py)

---

## 4. Community Detection & Centrality

### 4.1 Community Detection for Reasoning

> 📄 **Example code:** [`examples/07-4-1-community-detection-for-reasoning.py`](examples/07-4-1-community-detection-for-reasoning.py)

### 4.2 Centrality — Who Matters?

<details>
<summary>Python Code — Centrality Analysis (Click to view)</summary>

> 📄 **Example code:** [`examples/08-4-2-centrality-who-matters.py`](examples/08-4-2-centrality-who-matters.py)

</details>

---

## 5. Temporal Reasoning

### 5.1 Time-Aware Graph

> 📄 **Example code:** [`examples/09-5-1-time-aware-graph.py`](examples/09-5-1-time-aware-graph.py)

### 5.2 Versioning

> 📄 **Example code:** [`examples/10-5-2-versioning.py`](examples/10-5-2-versioning.py)

---

## 6. Implementing a Reasoning Engine

<details>
<summary>Python Code — Complete Reasoning Engine (Click to view)</summary>

> 📄 **Example code:** [`examples/11-6-implementing-a-reasoning-engine.py`](examples/11-6-implementing-a-reasoning-engine.py)

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

> 📄 **Example code:** [`examples/12-7-1-think-on-graph-tog.py`](examples/12-7-1-think-on-graph-tog.py)

### 7.2 Plan-on-Graph — Planner-Executor-Reasoner (PER)

> **Three roles** — clearly separated:
> - **Planner** (LLM): generates the "plan" — a sequence of relation types to traverse (`GET_REPORTER`, `GET_PROJECT`, `GET_STATUS`)
> - **Executor** (Graph BFS): executes the relations according to the plan
> - **Reasoner** (LLM): **reads the execution results** → summarizes the answer
>
> **Key result:** Planner-Executor-Reasoner (PER) achieves **micro-F1 > 0.90** on the KGQA benchmark (2025–2026), at much lower computational cost than Neo4j full-LLM reasoning.

### 7.3 KG-Agent

> The agent **operates the KG through an API** (CRUD), not just queries it — the agent can **add relations, fix nodes, write new evidence** into the graph when needed, then use the results for its answer.

> 📄 **Example code:** [`examples/13-7-3-kg-agent.py`](examples/13-7-3-kg-agent.py)

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

## GraphRAG — 2026 Update

Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG. Complex (multi-hop) queries outperform vector-only RAG.

**New 2025-2026 developments:**
- **LazyGraphRAG** (Microsoft, late 2024): defers LLM summarisation to query time — indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **LightRAG** (HKUDS, EMNLP 2025): dual-layer graph + vector, incremental update instead of full re-index.
- **GraphRAG-Bench** (Microsoft, 06/2025): multi-hop + global queries GraphRAG wins; single-hop factoid vanilla RAG wins.
- **Gartner (2026)**: GraphRAG in "Top Trends in D&A for 2026" for complex cases where high-accuracy RAG falls short.
- **Knowledge Graph Market**: $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline.

Ref: https://microsoft.github.io/graphrag/

---

*Next: [07 — GNN](../07-gnn/)*
