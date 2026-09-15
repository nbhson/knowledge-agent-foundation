# 🕸️ XIII. Graph Engineering

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Does Graph Engineering Matter?](#why-does-graph-engineering-matter)
> - [Overview](#overview)
> - [Learning Path (Directory Structure)](#learning-path-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [References](#references)

---

### Opening Story

You have a 10,000-page document repository about your company: contracts, reports, org charts, emails. You ask the RAG chatbot:

> *"Who approved the Phoenix project contract, and what AI-related projects has that person managed before?"*

**Vector RAG** finds 5 chunks containing "Phoenix" — but no chunk contains both the `approver` and the `AI project` at the same time. It guesses and hallucinates a name.

**GraphRAG** is different. It has already extracted:

```
(Phoenix) —[APPROVED_BY]→ (Nguyen Van A) —[MANAGED]→ (Project Atlas - AI Platform)
                  └—[REPORTS_TO]→ (Tran Thi B - CTO)
```

A single `TRAVERSE 2 hops` query returns the exact answer **with a proof path** — no guessing, no fabrication.

> *"Vector search finds similar passages. Graph search finds the relationships hidden behind those passages."*
> — **Microsoft Research, GraphRAG (2024)**

> *"Knowledge is not a pile of chunks. It's a web of relationships."*

**Graph Engineering** is the craft of designing a **graph-structured knowledge substrate** — so that AI doesn't just *find* information, but can also *reason* over it in multiple steps, with explanations and citations.

### Why Does Graph Engineering Matter?

> **"Stop chunking. Start connecting. Get a path."**

#### 3 Scientific & Practical Pieces of Evidence

| # | Research / Source | Key Finding |
|---|-------------------|----------------------|
| 1 | **Microsoft GraphRAG (2024)** | GraphRAG increases **comprehensiveness by 30–40%** on synthetic questions (global sensemaking) versus vanilla RAG; 70% win rate when judged by an LLM |
| 2 | **Neo4j + LangChain Benchmark (2025)** | Hybrid Vector + Graph reduces **hallucination by 25–30%** on an enterprise QA benchmark (10K docs) |
| 3 | **Stanford CS224W (2024)** | Knowledge Graph retrieval solves **multi-hop QA** with 68% accuracy vs 41% for vector-only RAG |

#### Core philosophy:

```
Graph Engineering = Entity & relation extraction → Store as a graph → Query + Reason → GraphRAG
```

**Key distinction:**

```
Harness  = the environment one agent runs in (tools, context, permissions)
Loop     = harness + schedule + state + verification (runs many times, self-maintaining)
Graph    = the durable knowledge substrate (knowledge substrate) that both Harness and Loop share

Vector DB  = "which passage resembles the question?"
Graph DB   = "which entities are related, how many hops away, with what evidence?"
GraphRAG   = Vector (recall) + Graph (precision + reasoning)
```

**Analogy**: Graph Engineering is like a **city map** — vector search tells you "there's a restaurant nearby", a graph tells you "who owns that restaurant, what else they own, and what the shortest route there is". Pure **chunking**, on the other hand, is like tearing the map into pieces and trying to reassemble it when you need it.

**If you skip it**: Your agents answer simple questions correctly but hallucinate on every multi-hop question, can't explain their sources, and can't update knowledge without re-embedding everything.

## Overview

**Graph Engineering** is the design of **graph-structured knowledge systems** so that AI agents can store, query, and reason over structured knowledge — with multi-hop traversal, community detection, and citation-backed grounding.

Unlike Module 01 (Retrieve Memory & Knowledge), which focuses on vector/hybrid search over chunks, Graph Engineering focuses on **knowledge graphs**: every fact is an edge (triple), every answer is a path, and every summary is a community.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GRAPH ENGINEERING                               │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              7 CORE COMPONENTS                                 │  │
│  │  Entities · Relations · Ontology · Storage · Embeddings        │  │
│  │  Reasoning · GraphRAG                                          │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              GRAPH LIFECYCLE                                   │  │
│  │  Extract → Build → Store → Embed → Query → Reason → Evaluate  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              HARNESS & LOOP INTEGRATION                        │  │
│  │  Graph is the knowledge substrate for the Harness (context)   │  │
│  │  The Loop updates the Graph automatically when a new document arrives │  │
│  └───────────────────────────────────────────────────────────────┘  │
│       │                                                            │
│       ▼                                                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              EVALUATION + OBSERVABILITY                        │  │
│  │  Coverage · Connectivity · Hallucination · Path Precision      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Learning Path (Directory Structure)

Module XIII is split into **9 specialized sub-modules** — consistent with the `harness/` convention (each module is `NN-name/README.md`).

```
graph/
├── README.md                    ← YOU ARE HERE — overview + learning path + case studies
├── 01-foundations/              ← Foundations: graph theory, types, representations, metrics
├── 02-knowledge-graph/          ← Building the KG: entity/relation extraction, ontology, deduplication
├── 03-graph-storage/            ← Storage & querying: Neo4j, Cypher, indexing, transactions
├── 04-graph-embeddings/         ← Embeddings: Node2Vec, GraphSAGE, hybrid vector+graph search
├── 05-graph-rag/                ← GraphRAG: subgraph retrieval, community summaries, Microsoft pattern
├── 06-graph-reasoning/          ← Reasoning: traversal, path finding, inference rules, temporal reasoning
├── 07-gnn/                      ← GNN: Graph Neural Networks, link prediction, classification
├── 08-graph-workflow/           ← Workflow: ETL pipelines, incremental updates, versioning
└── 09-evaluation/               ← Evaluation: coverage, hallucination, path precision, benchmarks
```

> Each directory contains a `README.md` — consistent with the `harness/` and `loop/` conventions.

### Suggested Path

```
Step 1: Read this README.md + GRAPH_ENGINEERING.md to understand the context
   ↓
Step 2: 01-foundations/ — learn graph types, representations, basic metrics
   ↓
Step 3: 02-knowledge-graph/ — learn how to extract entities/relations, design an ontology
   ↓
Step 4: 03-graph-storage/ — pick a DB, write Cypher, build indexes
   ↓
Step 5: 04-graph-embeddings/ + 05-graph-rag/ — embeddings + GraphRAG pipeline
   ↓
Step 6: 06-graph-reasoning/ + 07-gnn/ — advanced reasoning, GNNs
   ↓
Step 7: 08-graph-workflow/ + 09-evaluation/ — production pipeline + evaluation
```

| If you want to... | Read |
|-------------|-----|
| Understand what a graph is, graph types, metrics | [01-foundations](01-foundations/) |
| Extract a Knowledge Graph from documents | [02-knowledge-graph](02-knowledge-graph/) |
| Pick a DB, store and query a graph | [03-graph-storage](03-graph-storage/) |
| Combine vector + graph embeddings | [04-graph-embeddings](04-graph-embeddings/) |
| Build a complete GraphRAG pipeline | [05-graph-rag](05-graph-rag/) |
| Multi-hop reasoning, path finding | [06-graph-reasoning](06-graph-reasoning/) |
| Use GNNs for link prediction/classification | [07-gnn](07-gnn/) |
| ETL pipeline, incremental updates | [08-graph-workflow](08-graph-workflow/) |
| Measure the quality of your graph & GraphRAG | [09-evaluation](09-evaluation/) |

---

## Real-World Case Studies

### 1. Microsoft GraphRAG — Global Sensemaking

Microsoft's GraphRAG is the **reference implementation** for this entire track:

```
Documents ──► LLM Entity/Relation Extraction ──► Knowledge Graph
                                                         │
                              ┌──────────────────────────┘
                              ▼
                    Community Detection (Leiden)
                              │
                              ▼
                    Community Summarization (LLM)
                              │
                              ▼
                    Hierarchical Search:
                      - Local Search (entity-centric, 1-2 hops)
                      - Global Search (community summaries, map-reduce)
```

| Loop | Pattern | Result |
|------|---------|---------|
| Entity Extraction | LLM + gleaning loop | Extracts 3–5× more entities than a single pass |
| Community Detection | Leiden algorithm | Automatically groups entities into meaningful communities |
| Global Search | Map-reduce over community summaries | 70% win rate vs vanilla RAG on global Q&A |
| Local Search | Entity → neighbors → context | Accurate for factoid + multi-hop queries |

### 2. Neo4j + LangChain — Enterprise Stack

The most common production stack in 2025–2026:

- **Construction**: `LLMGraphTransformer` (LangChain) → `Neo4jGraph.add_graph_documents()`
- **Query**: `GraphCypherQAChain` → LLM generates Cypher from natural language
- **Hybrid**: Vector index on `Document` nodes + graph traversal on `Person/Project` nodes
- **Scale**: Neo4j Aura / self-hosted cluster, billions of nodes

### 3. Trajectory as Graph — DeepSeek Pattern

DeepSeek's harness doesn't store trajectories as flat logs — it stores them as an **event graph**: each tool call is a node, dependencies are edges → branches can be forked/replayed like git branches. Details: [`harness/03-update-memory-store/trajectory-fork-replay.md`](../harness/03-update-memory-store/trajectory-fork-replay.md). This is exactly **graph thinking** applied to agent execution.

### 4. Codebase Knowledge Graph

Applying graphs to AI coding:

```
File ─[DEFINES]→ Function ─[CALLS]→ Function ─[TESTED_BY]→ TestFile
  │                │                     │
  └[IMPORTS]→ Module  └[USES]→ Class ─[INHERITS]→ BaseClass
```

Used to answer: "where is this function called?", "what breaks if I change this file?", "which tests cover this function?" — questions vector search can't answer.

---

## References

### Articles & Sources

- [Microsoft Research — GraphRAG: Unlocking LLM discovery on narrative private data](https://microsoft.github.io/graphrag/) — paper + open-source implementation
- [Neo4j — GraphRAG Use Cases](https://neo4j.com/use-cases/knowledge-graph/) — enterprise patterns
- [LangChain — Graph QA](https://python.langchain.com/docs/use_cases/graph/) — Cypher QA chains
- [LlamaIndex — Property Graph Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/) — LPG + retrievers
- [DeepSeek Harness — Micro-Kernel & Trajectory Graph](../harness/07-workflow/cordis-kernel-plugin.md) — event graph pattern
- [Stanford CS224W — Machine Learning with Graphs](http://web.stanford.edu/class/cs224w/) — GNN foundations

### Frameworks & Tools

- **graphrag** (Microsoft) — `pip install graphrag` — end-to-end GraphRAG pipeline
- **Neo4j** — `docker run neo4j:5` — graph DB + Cypher + GDS library
- **NetworkX / igraph** — local graph algorithms & prototyping
- **PyG / DGL** — GNN training & inference
- **Kuzu** — embedded graph DB, Python-native

### Datasets & Benchmarks

- **HotpotQA / 2WikiMultihopQA** — multi-hop QA benchmarks
- **FB15k-237 / WN18RR** — knowledge graph completion benchmarks
- **OGB (Open Graph Benchmark)** — large-scale GNN benchmarks

Details for each module: [01-foundations](01-foundations/) → [09-evaluation](09-evaluation/).

---

> **"Knowledge is not a pile of chunks. It's a web of relationships. Graph Engineering is how you weave that web."**

---

*Part of the [AI Coding Skills Framework](../) — Module XIII: Graph Engineering*
