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

This section explains what problem graphs solve that plain search cannot — the reason this whole document exists.

In the RAG era (RAG = Retrieval-Augmented Generation, "give the model documents to read before it answers"), 2023–2025, we learned: **give the LLM the right context and small models can beat big ones**. But plain vector-search RAG (vector search = finding text whose *meaning* is mathematically closest to the question, even if the words differ) has one big blind spot: it only finds **"passages that look like the question"** — it can't find **"how things are linked."**

**Example:**
- Ask: *"Who approved the contract for project X, and who does that person report to?"*
- Vector RAG: finds the chunk (chunk = a slice of text, usually a few hundred words, cut from a document for storage) containing "project X" but **cannot connect** `Approver → Manager` if the two pieces of information live in two different documents.
- Graph RAG: traverses `Project X —[approved_by]→ Person A —[reports_to]→ Person B` → returns the exact answer with a **citation path** (citation path = the chain of links in the graph that led to the answer, so you can re-check it).

### Context

In 2024, Microsoft Research released **GraphRAG**: use an LLM to extract a Knowledge Graph (Knowledge Graph = a database of real-world things and how they connect, e.g. "Alice approves Contract C") from an entire corpus, then apply community detection (community detection = an algorithm that finds groups of tightly connected nodes, like spotting teams in an org chart) + hierarchical summarization (hierarchical summarization = summarizing each group, then summarizing the group-of-groups). The result: **30–40% more comprehensiveness and diversity** than vanilla RAG (vanilla = the plain, unmodified version) on synthetic (global sensemaking) questions (global sensemaking = questions about themes across the *whole* collection, not one document).

At the same time, Neo4j, NebulaGraph, and FalkorDB brought graph databases (databases that store data as nodes and links, not tables) into production AI stacks. Graph-structured knowledge went from "nice-to-have" to a **required substrate** (substrate = the foundation layer other things are built on) for agents that need multi-step reasoning.

### Goals

This document gives a comprehensive view of Graph Engineering:

- Definitions, philosophy, and comparison with pure Vector/RAG
- Analysis of the three evolutionary stages: Keyword → Vector → Graph
- The 7 core components of a graph system
- Mapping the 7 components → 9 hands-on modules in `graph/`
- Case studies: Microsoft GraphRAG, Neo4j + LangChain, DeepSeek Knowledge Graph
- Design principles, best practices, and a 2026–2028 roadmap

> **One-line summary:** Vector search finds text that *sounds* like the question; graphs find the *connections* behind it — and this document teaches you to build those connections.

---

## 2. What Is Graph Engineering?

This section defines the term and shows how it differs from the search you already know.

### Definition

**Graph Engineering** is the craft of building and operating **graph-based knowledge systems** that power AI Agents — including entity/relation extraction (extraction = getting an LLM to pull out "who did what to whom" from text), graph storage, embeddings (embeddings = turning text into number-vectors so "similar meaning" becomes "nearby numbers"), querying, reasoning, and integration into RAG/Workflow pipelines.

In plain terms:
- **Vector DB** (a database storing text as number-vectors) answers: *"Which passage most resembles the question?"*
- **Graph DB** (a database storing things as nodes and links) answers: *"Which entities are related, how many hops away (hop = one step along a link), with what confidence?"*
- **Graph Engineering** combines both to answer: *"The most correct answer, explainable, with a proof path."*

### Core Philosophy

> *"Every time an LLM hallucinates for lack of a link, you don't write a longer prompt — you build a new edge in the graph."*
> (hallucinate = the model confidently makes things up; edge = one link between two nodes)

1. **Relationships over Chunks**: Real knowledge lives in **relations**, not isolated passages. Chunking splits text apart; a graph **reconnects** it.
2. **Structure over Similarity**: Similarity finds what looks alike; structure finds **what is related through intermediaries** (multi-hop, e.g. Alice → Bob → Carol, two steps away).
3. **Explainability over Black-box** (black-box = you see the answer but not why): Every answer can be traced back to a **path** in the graph — auditable, citable.

### Comparison With Other Paradigms

How to read this table: each column is a search technology, each row is one property of it. For instance, the "Multi-hop" row asks "can it follow a chain like A→B→C?"; only Graph Engineering says yes. BM25 = the classic keyword-matching algorithm behind most search boxes.

| Aspect | Keyword Search (BM25) | Vector Search (RAG) | Graph Engineering |
|-----------|----------------------|---------------------|-------------------|
| **Focus** | Exact keywords | Semantic meaning | Entities + relations + inference |
| **Unit** | Document / Chunk | Chunk embedding | Node / Edge / Path / Community |
| **Query** | `MATCH keyword` | `cosine(query, chunk)` (cosine = a 0-to-1 score of how alike two vectors point) | `TRAVERSE / SHORTEST_PATH / COMMUNITY` |
| **Multi-hop** | ❌ No | ❌ Weak | ✅ Strong (2–6 hops) |
| **Explainability** | Low | Low | High (path + subgraph) |
| **Updates** | Re-index | Re-embed | Add node/edge (incremental) |
| **Example** | Search "BHYT" | Search "health insurance ≈ BHYT" | `BHYT —covers→ Heart disease —treated_at→ Cho Ray Hospital` |

> **Insight:** Graph does not replace Vector — Graph **wraps and amplifies** Vector. The best system is **Hybrid: Vector for recall (recall = casting a wide net so nothing relevant is missed), Graph for precision + reasoning**.

> **One-line summary:** Graph Engineering = building knowledge as nodes and links so agents can answer "how are things connected" with a checkable proof path.

---

## 3. The Three Stages of Retrieval Evolution

This section tells the history in one picture: search got smarter in three steps, and each step kept the previous one.

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

Reading the diagram, bottom to top: **BM25/TF-IDF** = classic algorithms that score how often rare words appear; **Inverted Index** = the "word → documents" lookup behind every search box. **ANN (HNSW, IVF)** = fast approximate nearest-neighbour search over vectors — HNSW and IVF are just two well-known ANN algorithms. **GNN** = a neural network that learns from the link structure itself, not just the text.

Each stage **adds to** the previous one, it does not replace it:
- You still need **BM25** for exact matches (contract codes, document numbers).
- You still need **Vector** for semantic recall (paraphrase, synonym).
- You need **Graph** on top for multi-hop, aggregation, and global sensemaking.

> **One-line summary:** Keyword → Vector → Graph are three layers stacked on each other, not three generations replacing each other.

---

## 4. Why Does Graph Engineering Matter?

This section gives the five concrete payoffs: what breaks without a graph, and what a graph fixes.

### 4.1. Getting Past the Limits of Chunking

Vector RAG depends on chunking. If two facts sit in two different chunks and no chunk contains both → RAG will **never** answer the question that joins them. Graph extraction pulls out entities/relations **before** chunking breaks the links.

> **One-line summary:** Chunking cuts the links between facts; graph extraction saves them before the cut.

### 4.2. Global Sensemaking vs Local Lookup

Microsoft GraphRAG research (2024) compared the two on real questions.

How to read this table: row 1 is a "local" question (one document); rows 2–3 are "global" or "multi-hop" questions (spanning many documents or links). ✅ = works, ❌ = fails or hallucinates.

| Question type | Vector RAG | GraphRAG |
|--------------|-----------|----------|
| Local: "What does section 5 of contract X say?" | ✅ Good | ✅ Good |
| Global: "Which main themes recur across all 1000 of these documents?" | ❌ Weak | ✅ Far superior (+35% comprehensiveness) |
| Multi-hop: "Who approved project X and what other projects does that person manage?" | ❌ Hallucinates | ✅ Exact, with path |

> **One-line summary:** For questions spanning many documents or many links, vector RAG guesses and graphs answer exactly.

### 4.3. Verifiable Hallucination Reduction

A graph provides a **grounding path** (grounding = tying the answer to real source text, so the model cannot float free): every edge carries `source_document`, `confidence`, `timestamp`. The LLM must follow the path instead of making things up. Microsoft reports a **25–30% reduction in hallucination** when replacing vanilla RAG with GraphRAG on QA benchmarks.

> **One-line summary:** Every graph link carries its source and confidence, so the model answers from evidence instead of imagination.

### 4.4. Incremental Knowledge Updates

- Vector DB: update one document → re-chunk + re-embed many chunks (re-embed = recompute the number-vectors), hard to keep consistent.
- Graph DB: update one fact → add/modify one node/edge, **does not affect** the rest of the graph. Ideal for enterprise knowledge bases that change daily.

> **One-line summary:** In a graph, updating one fact touches one node — no wholesale re-computation.

### 4.5. Foundation for Agent Reasoning

Agents need **plan → retrieve → reason → act**. A graph provides:
- **Planning**: traverse dependencies between tasks (`Task A —blocks→ Task B`)
- **Reasoning**: path finding, community detection for indirect inference (inference = deducing a fact that is not written down, from facts that are)
- **Memory**: store episodic memory (episodic memory = a record of what happened, when) as a graph (`User —prefers→ Dark Mode —since→ 2025-11-01`)

> **One-line summary:** A graph doubles as the agent's planning board, reasoning tool, and long-term memory.

---

## 5. The Core Components of a Graph

This section names the 7 building blocks. The diagram shows how they fit; the table maps each block to a learning module.

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

How to read this table: row 1 is a part of a graph system, row 2 is what that part does, row 3 names the module in `graph/` that teaches it. For instance, "Ontology & Schema" is the rulebook saying which node/edge types are allowed, and you learn it in `02-knowledge-graph`.

| # | Component | Role | Corresponding module |
|---|-----------|---------|-----------------|
| 1 | **Entities & Nodes** | Unit of knowledge (person, project, doc, concept) | `01-foundations` |
| 2 | **Relations & Edges** | Directional, weighted, time-stamped relationships | `01-foundations`, `02-knowledge-graph` |
| 3 | **Ontology & Schema** | Rules: which node/edge types are valid, constraints | `02-knowledge-graph` |
| 4 | **Storage & Query** | Store and query (Cypher, GQL, SPARQL — three query languages, all "SQL for graphs") | `03-graph-storage` |
| 5 | **Embeddings** | Vectorize node/edge/path for hybrid search | `04-graph-embeddings` |
| 6 | **Reasoning** | Traversal, shortest path, community, centrality | `06-graph-reasoning` |
| 7 | **GraphRAG** | Combine graph + LLM to generate grounded output | `05-graph-rag` |

> **One-line summary:** A graph system is 7 parts — nodes, links, a rulebook (schema), storage, embeddings, reasoning, and GraphRAG — each mapped to one module.

---

## 6. Overall Architecture: 7 Components → 9 Modules

This section shows how the 7 components above map onto the 9 `graph/` modules in this repo.

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

(In the diagram: **Node2Vec, GraphSAGE** = algorithms that turn graph positions into vectors; **ETL** = Extract-Transform-Load, the standard name for moving data from one system into another in usable form.)

### Integration With Harness and Loop

Signpost: the graph does not live alone — this shows how it plugs into the rest of the framework.

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

> **One-line summary:** The 9 `graph/` modules implement the 7 components; the Harness uses the graph as its knowledge base and the Loop keeps it fresh.

---

## 7. Case Studies

This section shows three real systems and what each one teaches you.

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

(Reading the diagram: **Leiden** = a standard algorithm for community detection — grouping nodes into tightly connected clusters. "Local Search" zooms into one entity; "Global Search" reads the pre-written group summaries.)

**Result:** On a benchmark of synthetic Q&A over podcast transcripts + news articles, GraphRAG achieved a **70% win rate** against vanilla RAG when judged by an LLM (comprehensiveness, diversity, empowerment).

**Lesson:** Investing in **graph construction pre-processing** costs more (LLM calls), but pays off big on complex/long-tail questions (long-tail = rare, specific questions instead of common ones).

> **One-line summary:** GraphRAG spends extra LLM effort up front building a summarized graph, and wins 70% of the time on hard, wide-scope questions.

### 7.2. Neo4j + LangChain — Enterprise Knowledge Graph

The most common production stack:

> 📄 **Example code:** [`examples/01-7-2-neo4j-langchain-enterprise-knowledge-graph.py`](examples/01-7-2-neo4j-langchain-enterprise-knowledge-graph.py)

> **One-line summary:** For companies, the default recipe is Neo4j for storage plus LangChain for the LLM glue.

### 7.3. DeepSeek Harness — Trajectory as Graph

Signpost: this example shows graph thinking applied to something unexpected — an agent's own execution history.

DeepSeek stores agent trajectories (trajectory = the full record of every step an agent took) **not** as flat logs, but as an **event graph**: each tool call is a node, dependencies are edges → branches can be forked/replayed like git branches (`harness/03-update-memory-store/trajectory-fork-replay.md`). This pattern is exactly **graph thinking** applied to agent execution.

> **One-line summary:** DeepSeek stores an agent's step history as a graph, so any branch can be replayed like a git branch.

### Common Lessons

1. **Graph construction is the bottleneck** — the quality of entity/relation extraction determines the entire downstream pipeline.
2. **Hybrid always wins** — Vector for recall, Graph for reasoning. Don't pick just one.
3. **Schema matters** — without an ontology, the graph becomes a "hairball" you can't query.

> **One-line summary:** Build the graph well, keep vector + graph together, and define a schema before ingesting.

---

## 8. Graph Design Principles

This section gives the design rules: a classic OOP principle set applied to graphs, then 8 commandments.

### 8.1. SOLID Principles for Graphs

How to read this table: the left column is a classic software-design principle (SOLID = five rules for keeping code maintainable); the right column is what that rule means when the "code" is a graph.

| Principle | Application to Graphs |
|-----------|-------------------|
| **Single Responsibility** | Each node type does one job (Person ≠ Organization ≠ Document) |
| **Open/Closed** | Adding new node/edge types doesn't modify the old schema (extend, don't modify) |
| **Liskov Substitution** | A subgraph must be substitutable for the full graph in tests |
| **Interface Segregation** | Separate query interfaces: read-only vs write vs admin |
| **Dependency Inversion** | Code depends on the Graph abstraction, not on Neo4j specifically |

> **One-line summary:** Design graph types like good classes: one job each, extendable, and never hard-wired to one vendor.

### 8.2. The 8 Commandments of Graph Engineering

1. **Schema First, Data Second** — define the ontology before ingesting.
2. **Every Edge Has Provenance** (provenance = where a fact came from) — every relation must carry `source`, `confidence`, `timestamp`.
3. **Incremental Over Batch** — update the graph per event, don't rebuild it wholesale.
4. **Hybrid Search By Default** — always combine vector + graph, never pick one.
5. **Paths Are Citations** — every answer must come with a verifiable path.
6. **Community Before Detail** — summarize communities before diving into local detail.
7. **Temporal Awareness** — relations are time-stamped (`valid_from`, `valid_until`), not permanent.
8. **Evaluate With Graphs** — measure coverage, connectivity, hallucination rate, not just BLEU/ROUGE (BLEU/ROUGE = word-overlap scores originally built for translation and summarization).

> **One-line summary:** The 8 commandments: schema first, provenance on every edge, incremental updates, hybrid search, path-as-citation, summarize-then-detail, time-aware edges, and graph-native evaluation.

### 8.3. Graph Design Pattern

> 📄 **Example code:** [`examples/02-8-3-graph-design-pattern.py`](examples/02-8-3-graph-design-pattern.py)

> **One-line summary:** See the principles applied in runnable code.

---

## 9. Best Practices

This section is the checklist: what to do (✅) at each stage of a graph project.

### 9.1. Graph Construction
- ✅ Use LLM + rule-based hybrid for extraction (LLM for recall, rules for precision).
- ✅ Deduplicate entities by embedding similarity + canonical name resolution (canonical name = the one official spelling you merge all variants into).
- ✅ Batch extraction with checkpoints (checkpoint = a saved stopping point you can resume from); don't ingest a large corpus in one shot.

> **One-line summary:** Mix LLM and rules, merge duplicate names into one canonical form, and never extract a whole corpus in one run.

### 9.2. Storage & Query
- ✅ Index on frequently used `label + property` combinations (e.g. `Person.name`).
- ✅ Cap `max_hops` (usually 2–3) to avoid explosion.
- ✅ Use parameterized Cypher (parameterized = values passed as safe placeholders, not pasted into the query string), not string concatenation.

> **One-line summary:** Index what you search, cap how far you traverse, and never build query strings by hand.

### 9.3. Retrieval
- ✅ Retrieve **subgraphs** (subgraph = a node plus its surrounding links, not just the node), not isolated nodes.
- ✅ Re-rank paths with a cross-encoder (cross-encoder = a model that reads query and candidate *together* and scores the pair — slower but sharper), just like re-ranking chunks.
- ✅ Summarize the community before returning local detail.

> **One-line summary:** Give the LLM connected subgraphs, re-ranked and pre-summarized — not a pile of loose nodes.

### 9.4. Guardrails
- ✅ Validate against the ontology before writing (don't allow `Person -[EATS]-> Project`).
- ✅ Access control at the subgraph level (a user only sees permitted subgraphs).
- ✅ Temporal versioning: soft-delete edges with `valid_until`, don't hard-delete (soft-delete = mark as expired but keep the row, so history survives).

> **One-line summary:** Block bad writes at the schema, restrict who sees which subgraph, and expire edges instead of erasing them.

### 9.5. Testing a Graph
- ✅ Unit tests: each extractor, each Cypher query.
- ✅ Integration tests: ingest → query → retrieve round-trip.
- ✅ Chaos tests (chaos testing = deliberately feeding junk or breaking things to see if the system survives): add junk nodes/edges, measure retrieval robustness.

> **One-line summary:** Test the parts, the whole round-trip, and the system's behaviour under garbage input.

---

## 10. Tools and Frameworks

This section is the shopping list: three tables of tools, one per layer of the stack.

### 10.1. Graph Databases

How to read this table: each row is one product. "Type" is how it stores/deploys the graph, "Scale" is the size it can handle, "Best For" tells you when to pick it.

| Tool | Type | Scale | Best For |
|------|------|-------|----------|
| **Neo4j** | Property Graph | Billions of nodes | Production, Cypher, large ecosystem |
| **NebulaGraph** | Distributed Property Graph | Trillions of edges | Large-scale, horizontal scaling |
| **FalkorDB** | Redis-based Graph | Millions | Low-latency, Redis stack |
| **Amazon Neptune** | Managed (Property + RDF) | Billions | AWS managed, SPARQL + Gremlin |
| **Kuzu** | Embedded Graph DB | Millions | Local, Python-native, fast |
| **NetworkX** | In-memory Library | Thousands | Prototyping, algorithms |

> **One-line summary:** Pick Neo4j for production, Kuzu/NetworkX to learn and prototype, NebulaGraph only at extreme scale.

### 10.2. LLM + Graph Frameworks

How to read this table: each row is a framework — pre-built software that connects LLMs to graphs so you don't write the plumbing yourself.

| Framework | Description |
|-----------|-------|
| **Microsoft GraphRAG** | End-to-end: extract → communities → hierarchical Q&A |
| **LangChain GraphTransformers** | LLM → graph documents, Cypher QA chains |
| **LlamaIndex Property Graph** | Property graph index + retrievers |
| **NebulaGraph + LLM** | NGQL generation from natural language |

> **One-line summary:** These four frameworks give you the extraction-to-answer pipeline pre-built.

### 10.3. Embeddings & GNN

How to read this table: each row is a research tool for turning graph positions into vectors (embedding) or training neural networks on graphs (GNN).

| Tool | Description |
|------|-------|
| **Node2Vec / DeepWalk** | Random walk embeddings, unsupervised |
| **GraphSAGE / GAT** | GNNs for inductive learning |
| **PyG (PyTorch Geometric)** | Complete GNN library |
| **DGL (Deep Graph Library)** | Scalable GNNs, multi-backend |

> **One-line summary:** Node2Vec family for simple embeddings; PyG or DGL when you need full GNN training.

### 10.4. Starter Template

The folder layout below is a ready-to-copy skeleton for a new graph project.

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

> **One-line summary:** Copy this folder skeleton and you have a home for data, schema, scripts, and the Neo4j container.

---

## 11. The Future of Graph Engineering

This section covers what changed recently and where the field is heading.

## GraphRAG — 2026 Update

> Microsoft GraphRAG (2024-2025): uses knowledge graphs to enhance RAG. Complex (multi-hop) queries outperform vector-only RAG.
> Ref: https://microsoft.github.io/graphrag/

### Key Developments 2025-2026:

How to read this table: each row is one recent release or report — the year, its name, and in plain words what it changes.

| Year | Development | Details |
|------|------------|---------|
| 2024-2025 | **LazyGraphRAG** (Microsoft) | LLM summarisation deferred to query time → indexing cost equal to vector RAG, quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local. |
| 2025 | **LightRAG** (HKUDS, EMNLP 2025) | Dual-layer graph + vector index, incremental update instead of full re-index, cost ~1/100 of full GraphRAG. |
| 2025 | **GraphRAG-Bench** (Microsoft, 06/2025) | Systematic benchmark: single-hop vanilla RAG wins; multi-hop and global GraphRAG wins clearly. |
| 2026 | **Gartner** "Top Trends in D&A 2026" | GraphRAG named as the path for complex cases where high-accuracy vanilla RAG falls short. |
| 2026 | **Knowledge Graph Market** | $1.48B (2025) → $2.04B (2026). GraphRAG shifting from "enterprise luxury" → production baseline. |

### When to use GraphRAG vs LazyGraphRAG vs LightRAG:

How to read this table: match your situation in the left column to the recommended tool in the right column.

| Scenario | Recommendation |
|----------|---------------|
| Need global/sensemaking queries across entire corpus | Full GraphRAG |
| Very large corpus, need cheap indexing, complex queries | LazyGraphRAG or LightRAG |
| Need incremental updates (documents changing continuously) | LightRAG |
| Only single-hop, factoid queries (factoid = a simple one-fact question) | Vanilla RAG (no graph needed) |

### 11.1. 2026–2028 Trends

How to read this table: each row is a prediction — the year it is expected to become mainstream, and what happens.

| Year | Trend |
|-----|---------|
| **2026** | GraphRAG becomes the default for enterprise RAG (replacing vanilla vector RAG) |
| **2026** | Graph databases add native vector indexes → a single DB for hybrid search |
| **2027** | Temporal graphs go mainstream: every edge has a lifecycle, time-aware queries |
| **2027** | GNN + LLM fusion: LLMs call GNNs as tools for reasoning over large graphs |
| **2028** | Auto-ontology: LLMs propose and evolve the schema from the data on their own |
| **2028** | Federated graphs: multiple orgs share subgraphs without sharing raw data |

### 11.2. Challenges

- **Construction cost**: LLM extraction is expensive in tokens; cheaper distilled extractors (distilled = a smaller model trained to imitate a bigger one) are needed.
- **Schema drift**: ontologies change over time; migrations are complex.
- **Evaluation**: there is still no standard benchmark for graph correctness the way SWE-bench is for coding.

> **One-line summary:** The three open problems: extraction cost, schema changes over time, and no standard quality benchmark.

### 11.3. Advice

> **"Start with 100 documents, 3 node types, 5 edge types. Don't try to build the Wikipedia graph on day one."**

> **One-line summary:** Start embarrassingly small; grow the graph only when the small one answers real questions.

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

> **One-line summary:** Everything above is the primary source list; start with GraphAcademy and CS224W if you want courses.

---

*Part of the [AI Coding Skills Framework](./AI_AGENT_FRAMEWORK.md) — Graph Engineering Track*
