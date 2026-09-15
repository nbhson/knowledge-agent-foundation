# Graph Engineering — Designing Graph-Based Knowledge Systems for AI Agents

> **"Vector search finds similar passages. Graph search finds the relationships hidden behind those passages."**  
> — GraphRAG Team, Microsoft Research (2024)

---

## Table of Contents

- [Graph Engineering — Designing Graph-Based Knowledge Systems for AI Agents](#graph-engineering--designing-graph-based-knowledge-systems-for-ai-agents)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [Context](#context)
    - [Goals](#goals)
  - [2. What Is Graph Engineering?](#2-what-is-graph-engineering)
    - [Definition](#definition)
    - [Core Philosophy](#core-philosophy)
    - [Comparison With Other Paradigms](#comparison-with-other-paradigms)
  - [3. The Three Stages of Retrieval Evolution](#3-the-three-stages-of-retrieval-evolution)
  - [4. Why Does Graph Engineering Matter?](#4-why-does-graph-engineering-matter)
  - [5. The Core Components of a Graph](#5-the-core-components-of-a-graph)
  - [6. Overall Architecture: 7 Components → 9 Modules](#6-overall-architecture-7-components--9-modules)
  - [7. Case Studies](#7-case-studies)
  - [8. Graph Design Principles](#8-graph-design-principles)
  - [9. Best Practices](#9-best-practices)
  - [10. Tools and Frameworks](#10-tools-and-frameworks)
  - [11. The Future of Graph Engineering](#11-the-future-of-graph-engineering)
  - [12. References](#12-references)

---

## 1. Introduction

In the RAG era (2023–2025), we proved: **get the right context into the LLM and small models beat big models**. But vector-search RAG has one fatal blind spot: it only finds **"passages that resemble the question"** — it can't find **"relationships between entities."**

**Example:**
- Ask: *"Who approved the contract for project X, and who does that person report to?"*
- Vector RAG: finds the chunk containing "project X" but **cannot connect** `Approver → Manager` if the two pieces of information live in two different documents.
- Graph RAG: traverses `Project X —[approved_by]→ Person A —[reports_to]→ Person B` → returns the exact answer with a **citation path**.

### Context

In 2024, Microsoft Research released **GraphRAG**: use an LLM to extract a Knowledge Graph from an entire corpus, then apply community detection + hierarchical summarization. The result: **30–40% more comprehensiveness and diversity** than vanilla RAG on synthetic (global sensemaking) questions.

At the same time, Neo4j, NebulaGraph, and FalkorDB brought graph databases into production AI stacks. Graph-structured knowledge went from "nice-to-have" to a **required substrate** for agents that need multi-step reasoning.

### Goals

This document gives a comprehensive view of Graph Engineering:

- Definitions, philosophy, and comparison with pure Vector/RAG
- Analysis of the three evolutionary stages: Keyword → Vector → Graph
- The 7 core components of a graph system
- Mapping the 7 components → 9 hands-on modules in `graph/`
- Case studies: Microsoft GraphRAG, Neo4j + LangChain, DeepSeek Knowledge Graph
- Design principles, best practices, and a 2026–2028 roadmap

---

## 2. What Is Graph Engineering?

### Definition

**Graph Engineering** is the craft of building and operating **graph-based knowledge systems** that power AI Agents — including entity/relation extraction, graph storage, embeddings, querying, reasoning, and integration into RAG/Workflow pipelines.

In plain terms:
- **Vector DB** answers: *"Which passage most resembles the question?"*
- **Graph DB** answers: *"Which entities are related, how many hops away, with what confidence?"*
- **Graph Engineering** combines both to answer: *"The most correct answer, explainable, with a proof path."*

### Core Philosophy

> *"Every time an LLM hallucinates for lack of a link, you don't write a longer prompt — you build a new edge in the graph."*

1. **Relationships over Chunks**: Real knowledge lives in **relations**, not isolated passages. Chunking splits text apart; a graph **reconnects** it.
2. **Structure over Similarity**: Similarity finds what looks alike; structure finds **what is related through intermediaries** (multi-hop).
3. **Explainability over Black-box**: Every answer can be traced back to a **path** in the graph — auditable, citable.

### Comparison With Other Paradigms

| Aspect | Keyword Search (BM25) | Vector Search (RAG) | Graph Engineering |
|-----------|----------------------|---------------------|-------------------|
| **Focus** | Exact keywords | Semantic meaning | Entities + relations + inference |
| **Unit** | Document / Chunk | Chunk embedding | Node / Edge / Path / Community |
| **Query** | `MATCH keyword` | `cosine(query, chunk)` | `TRAVERSE / SHORTEST_PATH / COMMUNITY` |
| **Multi-hop** | ❌ No | ❌ Weak | ✅ Strong (2–6 hops) |
| **Explainability** | Low | Low | High (path + subgraph) |
| **Updates** | Re-index | Re-embed | Add node/edge (incremental) |
| **Example** | Search "BHYT" | Search "health insurance ≈ BHYT" | `BHYT —covers→ Heart disease —treated_at→ Cho Ray Hospital` |

> **Insight:** Graph does not replace Vector — Graph **wraps and amplifies** Vector. The best system is **Hybrid: Vector for recall, Graph for precision + reasoning**.

---

## 3. The Three Stages of Retrieval Evolution

```
┌──────────────────────────────────────────────────────────────────┐
│                    RETRIEVAL EVOLUTION                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  2020-2022: KEYWORD RETRIEVAL                                    │
│  ┌─────────────────────────────────┐                             │
│  │ "Find the exact keyword"        │                             │
│  │ BM25, TF-IDF, Inverted Index    │                             │
│  │ Control: ⭐ Low                 │                             │
│  └─────────────────────────────────┘                             │
│                    │                                             │
│                    ▼                                             │
│  2023-2025: VECTOR RETRIEVAL (RAG)                               │
│  ┌─────────────────────────────────┐                             │
│  │ "Find similar meaning"          │                             │
│  │ Embeddings + ANN (HNSW, IVF)    │                             │
│  │ Control: ⭐⭐⭐ Medium            │                             │
│  └─────────────────────────────────┘                             │
│                    │                                             │
│                    ▼                                             │
│  2026+: GRAPH RETRIEVAL (GraphRAG)                               │
│  ┌─────────────────────────────────┐                             │
│  │ "Find relations + reasoning"    │                             │
│  │ Knowledge Graph + GraphRAG + GNN│                             │
│  │ Control: ⭐⭐⭐⭐⭐ High           │                             │
│  └─────────────────────────────────┘                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Each stage **adds to** the previous one, it does not replace it:
- You still need **BM25** for exact matches (contract codes, document numbers).
- You still need **Vector** for semantic recall (paraphrase, synonym).
- You need **Graph** on top for multi-hop, aggregation, and global sensemaking.

---

## 4. Why Does Graph Engineering Matter?

### 4.1. Getting Past the Limits of Chunking

Vector RAG depends on chunking. If two facts sit in two different chunks and no chunk contains both → RAG will **never** answer the question that joins them. Graph extraction pulls out entities/relations **before** chunking breaks the links.

### 4.2. Global Sensemaking vs Local Lookup

Microsoft GraphRAG research (2024):

| Question type | Vector RAG | GraphRAG |
|--------------|-----------|----------|
| Local: "What does section 5 of contract X say?" | ✅ Good | ✅ Good |
| Global: "Which main themes recur across all 1000 of these documents?" | ❌ Weak | ✅ Far superior (+35% comprehensiveness) |
| Multi-hop: "Who approved project X and what other projects does that person manage?" | ❌ Hallucinates | ✅ Exact, with path |

### 4.3. Verifiable Hallucination Reduction

A graph provides a **grounding path**: every edge carries `source_document`, `confidence`, `timestamp`. The LLM must follow the path instead of making things up. Microsoft reports a **25–30% reduction in hallucination** when replacing vanilla RAG with GraphRAG on QA benchmarks.

### 4.4. Incremental Knowledge Updates

- Vector DB: update one document → re-chunk + re-embed many chunks, hard to keep consistent.
- Graph DB: update one fact → add/modify one node/edge, **does not affect** the rest of the graph. Ideal for enterprise knowledge bases that change daily.

### 4.5. Foundation for Agent Reasoning

Agents need **plan → retrieve → reason → act**. A graph provides:
- **Planning**: traverse dependencies between tasks (`Task A —blocks→ Task B`)
- **Reasoning**: path finding, community detection for indirect inference
- **Memory**: store episodic memory as a graph (`User —prefers→ Dark Mode —since→ 2025-11-01`)

---

## 5. The Core Components of a Graph

```
┌──────────────────────────────────────────────────────────────────┐
│                    COMPLETE GRAPH ARCHITECTURE                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌──────────────┐     │
│  │   ENTITIES  │◄────►│  RELATIONS  │◄────►│   ONTOLOGY   │     │
│  │  (Nodes)    │      │  (Edges)    │      │  (Schema)    │     │
│  └─────────────┘      └─────────────┘      └──────────────┘     │
│         ▲                    ▲                     ▲              │
│         │                    │                     │              │
│         ▼                    ▼                     ▼              │
│  ┌────────────────────────────────────────────────────┐          │
│  │           GRAPH STORAGE & QUERY                    │          │
│  │   Neo4j / NebulaGraph / FalkorDB / RDF Triple Store│          │
│  └────────────────────────────────────────────────────┘          │
│         ▲                    ▲                     ▲              │
│         │                    │                     │              │
│  ┌─────────────┐      ┌─────────────┐      ┌──────────────┐     │
│  │ EMBEDDINGS  │      │   REASONING │      │   GRAPH RAG  │     │
│  │ (Vector+Graph)│    │(Traversal)  │      │ (Retrieval)  │     │
│  └─────────────┘      └─────────────┘      └──────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| # | Component | Role | Corresponding module |
|---|-----------|---------|-----------------|
| 1 | **Entities & Nodes** | Unit of knowledge (person, project, doc, concept) | `01-foundations` |
| 2 | **Relations & Edges** | Directional, weighted, time-stamped relationships | `01-foundations`, `02-knowledge-graph` |
| 3 | **Ontology & Schema** | Rules: which node/edge types are valid, constraints | `02-knowledge-graph` |
| 4 | **Storage & Query** | Store and query (Cypher, GQL, SPARQL) | `03-graph-storage` |
| 5 | **Embeddings** | Vectorize node/edge/path for hybrid search | `04-graph-embeddings` |
| 6 | **Reasoning** | Traversal, shortest path, community, centrality | `06-graph-reasoning` |
| 7 | **GraphRAG** | Combine graph + LLM to generate grounded output | `05-graph-rag` |

---

## 6. Overall Architecture: 7 Components → 9 Modules

```
┌──────────────────────────────────────────────────────────────────────────┐
│                 GRAPH ENGINEERING → MODULE MAPPING                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ FOUNDATIONS  │────►│ 01-foundations                         │         │
│  │ Graph Theory │     │ Graph types, representations, metrics  │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ KNOWLEDGE    │────►│ 02-knowledge-graph                     │         │
│  │ GRAPH BUILD  │     │ Entity/relation extraction, ontology   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ STORAGE      │────►│ 03-graph-storage                       │         │
│  │ & QUERY      │     │ Neo4j, Cypher, indexing, transaction   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ EMBEDDINGS   │────►│ 04-graph-embeddings                    │         │
│  │              │     │ Node2Vec, GraphSAGE, hybrid search     │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ GRAPH RAG    │────►│ 05-graph-rag                           │         │
│  │              │     │ Subgraph retrieval, community summary  │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ REASONING    │────►│ 06-graph-reasoning                     │         │
│  │              │     │ Path finding, inference, rules         │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ LEARNING     │────►│ 07-gnn                                 │         │
│  │ (GNN)        │     │ GNN, link prediction, classification   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ WORKFLOW     │────►│ 08-graph-workflow                      │         │
│  │              │     │ Pipeline, incremental updates, ETL     │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
│  ┌──────────────┐     ┌────────────────────────────────────────┐         │
│  │ EVALUATION   │────►│ 09-evaluation                          │         │
│  │              │     │ Correctness, coverage, hallucination   │         │
│  └──────────────┘     └────────────────────────────────────────┘         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Integration With Harness and Loop

```
HARNESS (harness/01-11)  ──►  provides Tools, Memory, Context, Guardrails for 1 Agent run
GRAPH   (graph/01-09)    ──►  provides the Knowledge substrate for the Harness (instead of just a Vector DB)
LOOP    (loop/01-07)     ──►  orchestrates MANY Harness runs over time

Full flow:
  Documents ──► Graph Construction (graph/02) ──► Graph Storage (graph/03)
      │
      ▼
  User Query ──► GraphRAG Retrieval (graph/05) ──► Context Building (harness/02)
      │
      ▼
  Prompt + Graph Context ──► LLM ──► Answer with citation path

Loop in operation:
  Loop Scheduler ──► detects new document ──► incremental graph update (graph/08)
```

---

## 7. Case Studies

### 7.1. Microsoft GraphRAG — Global Sensemaking

**Architecture:**

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
                      - Local Search (entity-centric)
                      - Global Search (community summaries)
```

**Result:** On a benchmark of synthetic Q&A over podcast transcripts + news articles, GraphRAG achieved a **70% win rate** against vanilla RAG when judged by an LLM (comprehensiveness, diversity, empowerment).

**Lesson:** Investing in **graph construction pre-processing** costs more (LLM calls), but pays off big on complex/long-tail questions.

### 7.2. Neo4j + LangChain — Enterprise Knowledge Graph

The most common production stack:

```python
# Construction
from langchain_experimental.graph_transformers import LLMGraphTransformer
transformer = LLMGraphTransformer(llm=ChatOpenAI(model="gpt-4o"))
graph_docs = await transformer.convert_to_graph_documents(raw_docs)

# Storage
from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="***")
graph.add_graph_documents(graph_docs)

# Retrieval
from langchain_community.chains import GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(llm=ChatOpenAI(model="gpt-4o"), graph=graph)
answer = chain.invoke("Who approved project X?")
```

### 7.3. DeepSeek Harness — Trajectory as Graph

DeepSeek stores agent trajectories **not** as flat logs, but as an **event graph**: each tool call is a node, dependencies are edges → branches can be forked/replayed like git branches (`harness/03-update-memory-store/trajectory-fork-replay.md`). This pattern is exactly **graph thinking** applied to agent execution.

### Common Lessons

1. **Graph construction is the bottleneck** — the quality of entity/relation extraction determines the entire downstream pipeline.
2. **Hybrid always wins** — Vector for recall, Graph for reasoning. Don't pick just one.
3. **Schema matters** — without an ontology, the graph becomes a "hairball" you can't query.

---

## 8. Graph Design Principles

### 8.1. SOLID Principles for Graphs

| Principle | Application to Graphs |
|-----------|-------------------|
| **Single Responsibility** | Each node type does one job (Person ≠ Organization ≠ Document) |
| **Open/Closed** | Adding new node/edge types doesn't modify the old schema (extend, don't modify) |
| **Liskov Substitution** | A subgraph must be substitutable for the full graph in tests |
| **Interface Segregation** | Separate query interfaces: read-only vs write vs admin |
| **Dependency Inversion** | Code depends on the Graph abstraction, not on Neo4j specifically |

### 8.2. The 8 Commandments of Graph Engineering

1. **Schema First, Data Second** — define the ontology before ingesting.
2. **Every Edge Has Provenance** — every relation must carry `source`, `confidence`, `timestamp`.
3. **Incremental Over Batch** — update the graph per event, don't rebuild it wholesale.
4. **Hybrid Search By Default** — always combine vector + graph, never pick one.
5. **Paths Are Citations** — every answer must come with a verifiable path.
6. **Community Before Detail** — summarize communities before diving into local detail.
7. **Temporal Awareness** — relations are time-stamped (`valid_from`, `valid_until`), not permanent.
8. **Evaluate With Graphs** — measure coverage, connectivity, hallucination rate, not just BLEU/ROUGE.

### 8.3. Graph Design Pattern

```python
# Complete Graph Engineering Example
from graph_engine import GraphHarness

graph = GraphHarness(
    ontology={
        "node_types": ["Person", "Project", "Document", "Organization"],
        "edge_types": ["APPROVES", "REPORTS_TO", "BELONGS_TO", "REFERENCES"],
        "constraints": ["Person -[REPORTS_TO]-> Person", "Project -[APPROVES]-> Person"]
    },
    storage="neo4j://localhost:7687",
    embeddings={"model": "nomic-embed-text", "dim": 768},
    retrieval={
        "strategy": "hybrid",  # vector + graph traversal
        "max_hops": 3,
        "community_search": True,
    },
    reasoning={
        "path_finding": "shortest_path",
        "community_detection": "leiden",
    },
    evaluation={
        "metrics": ["coverage", "hallucination_rate", "path_precision"]
    }
)
```

---

## 9. Best Practices

### 9.1. Graph Construction
- ✅ Use LLM + rule-based hybrid for extraction (LLM for recall, rules for precision).
- ✅ Deduplicate entities by embedding similarity + canonical name resolution.
- ✅ Batch extraction with checkpoints; don't ingest a large corpus in one shot.

### 9.2. Storage & Query
- ✅ Index on frequently used `label + property` combinations (e.g. `Person.name`).
- ✅ Cap `max_hops` (usually 2–3) to avoid explosion.
- ✅ Use parameterized Cypher, not string concatenation.

### 9.3. Retrieval
- ✅ Retrieve **subgraphs** (nodes + edges), not isolated nodes.
- ✅ Re-rank paths with a cross-encoder, just like re-ranking chunks.
- ✅ Summarize the community before returning local detail.

### 9.4. Guardrails
- ✅ Validate against the ontology before writing (don't allow `Person -[EATS]-> Project`).
- ✅ Access control at the subgraph level (a user only sees permitted subgraphs).
- ✅ Temporal versioning: soft-delete edges with `valid_until`, don't hard-delete.

### 9.5. Testing a Graph
- ✅ Unit tests: each extractor, each Cypher query.
- ✅ Integration tests: ingest → query → retrieve round-trip.
- ✅ Chaos tests: add junk nodes/edges, measure retrieval robustness.

---

## 10. Tools and Frameworks

### 10.1. Graph Databases

| Tool | Type | Scale | Best For |
|------|------|-------|----------|
| **Neo4j** | Property Graph | Billions of nodes | Production, Cypher, large ecosystem |
| **NebulaGraph** | Distributed Property Graph | Trillions of edges | Large-scale, horizontal scaling |
| **FalkorDB** | Redis-based Graph | Millions | Low-latency, Redis stack |
| **Amazon Neptune** | Managed (Property + RDF) | Billions | AWS managed, SPARQL + Gremlin |
| **Kuzu** | Embedded Graph DB | Millions | Local, Python-native, fast |
| **NetworkX** | In-memory Library | Thousands | Prototyping, algorithms |

### 10.2. LLM + Graph Frameworks

| Framework | Description |
|-----------|-------|
| **Microsoft GraphRAG** | End-to-end: extract → communities → hierarchical Q&A |
| **LangChain GraphTransformers** | LLM → graph documents, Cypher QA chains |
| **LlamaIndex Property Graph** | Property graph index + retrievers |
| **NebulaGraph + LLM** | NGQL generation from natural language |

### 10.3. Embeddings & GNN

| Tool | Description |
|------|-------|
| **Node2Vec / DeepWalk** | Random walk embeddings, unsupervised |
| **GraphSAGE / GAT** | GNNs for inductive learning |
| **PyG (PyTorch Geometric)** | Complete GNN library |
| **DGL (Deep Graph Library)** | Scalable GNNs, multi-backend |

### 10.4. Starter Template

```
my-graph-project/
├── graph/
│   ├── 01-foundations/
│   ├── 02-knowledge-graph/
│   └── ... (09 modules)
├── data/
│   ├── raw_docs/
│   └── ontology.yaml
├── scripts/
│   ├── extract_graph.py
│   ├── query_graph.py
│   └── evaluate.py
└── docker-compose.yml  # Neo4j + app
```

---

## 11. The Future of Graph Engineering

### 11.1. 2026–2028 Trends

| Year | Trend |
|-----|---------|
| **2026** | GraphRAG becomes the default for enterprise RAG (replacing vanilla vector RAG) |
| **2026** | Graph databases add native vector indexes → a single DB for hybrid search |
| **2027** | Temporal graphs go mainstream: every edge has a lifecycle, time-aware queries |
| **2027** | GNN + LLM fusion: LLMs call GNNs as tools for reasoning over large graphs |
| **2028** | Auto-ontology: LLMs propose and evolve the schema from the data on their own |
| **2028** | Federated graphs: multiple orgs share subgraphs without sharing raw data |

### 11.2. Challenges

- **Construction cost**: LLM extraction is expensive in tokens; cheaper distilled extractors are needed.
- **Schema drift**: ontologies change over time; migrations are complex.
- **Evaluation**: there is still no standard benchmark for graph correctness the way SWE-bench is for coding.

### 11.3. Advice

> **"Start with 100 documents, 3 node types, 5 edge types. Don't try to build the Wikipedia graph on day one."**

---

## 12. References

### Papers & Research
- Microsoft Research — *GraphRAG: Unlocking LLM discovery on narrative private data* (2024)
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — Lewis et al. (2020, original RAG)
- *Knowledge Graph Completion via Embeddings* — Bordes et al. (TransE, 2013)

### Frameworks & Tools
- [Microsoft GraphRAG (GitHub)](https://github.com/microsoft/graphrag)
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
- [LangChain — Graph QA](https://python.langchain.com/docs/use_cases/graph/)
- [LlamaIndex — Property Graph Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)

### Communities
- Neo4j Community Forum
- GraphRAG Discord
- Knowledge Graph Conference (KGC)

### Courses & Tutorials
- Neo4j GraphAcademy — *Introduction to Neo4j & Cypher*
- Stanford CS224W — *Machine Learning with Graphs*

---

*Part of the [AI Coding Skills Framework](./AI_AGENT_FRAMEWORK.md) — Graph Engineering Track*
