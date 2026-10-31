# 💾 03. Graph Storage & Query — Storing and Querying the Graph

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Storage & Query Matter?](#why-storage--query-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Choosing a Graph Database](#1-choosing-a-graph-database)
> - [2. Cypher & GQL — The Query Language](#2-cypher--gql--the-query-language)
> - [3. Indexing & Performance](#3-indexing--performance)
> - [4. Transactions & Consistency](#4-transactions--consistency)
> - [5. Deployment with Neo4j & Kuzu](#5-deployment-with-neo4j--kuzu)
> - [6. Hands-On Labs](#6-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have extracted 5,000 entities and 12,000 relations. You store them in `graph.json` — a 50MB JSON file.

The next week, you need to answer: *"Find all projects that Alice's team has worked on, up to 3 steps of REPORTS_TO/MANAGES."*

With JSON, you end up writing a manual BFS loop, loading the whole file into memory, and waiting about 2 seconds per query. 100 queries? That gets slow fast.

A **Graph Database** makes this easy: it comes with **built-in storage, indexes, and a query engine** — so you can answer the same question in about 15ms with a single line of Cypher.

### Why Storage & Query Matter?

> *"Without the right DB, a graph is just an expensive JSON file. Without a query language, a graph is just a drawing."*

| # | Source | Finding |
|---|-------|-----------|
| 1 | **Neo4j Benchmark (2024)** | Native graph storage is **100–1000× faster** than relational JOINs for 3-hop queries |
| 2 | **KuzuDB Paper (2024)** | An embedded graph DB (Kuzu) achieves **10× the throughput** of in-memory NetworkX on 10M edges |
| 3 | **LDBC SNB Benchmark** | Indexes on `label + property` cut latency by **80%** for lookup queries |

---

## Overview

```
Knowledge Graph (from 02)
    │
    ▼
┌──────────────────────┐
│  CHOOSE DATABASE     │  ← Neo4j, Kuzu, NebulaGraph, FalkorDB, NetworkX
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  SCHEMA & INDEXING   │  ← Create constraints, indexes
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  INGEST & TRANSACTIONS│ ← Batch insert, ACID, upsert
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  QUERY (Cypher/GQL)  │  ← Traversal, aggregation, path finding
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  OBSERVABILITY       │  ← Query log, slow queries, metrics
└──────────────────────┘
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Choosing a DB](#1-choosing-a-graph-database) | Comparing 6 DBs, decision matrix |
| 2 | [Cypher & GQL](#2-cypher--gql--the-query-language) | CRUD, traversal, aggregation, full-text |
| 3 | [Indexing](#3-indexing--performance) | Index types, query optimization |
| 4 | [Transactions](#4-transactions--consistency) | ACID, batch ingest, idempotency |
| 5 | [Deployment](#5-deployment-with-neo4j--kuzu) | Docker, Python client, sample code |

---

## 1. Choosing a Graph Database

> **📌 When do you need a graph DB?** When your question is **"which entities are related to this one / how are they related?"** (multi-hop traversal) — SQL has to JOIN repeatedly and gets very slow; a graph DB walks the edges directly. **Sign you need a graph DB:** your queries always have the pattern `A —[...]→ B —[...]→ C` (2+ hops).
>
> **Quick Q&A to choose:**
> - Learning / prototyping? → **Kuzu / NetworkX** (no Docker needed)
> - Need stable production, big ecosystem? → **Neo4j** (Community → Aura when scaling)
> - Trillions of edges? → **NebulaGraph** (scale-out)
> - Need sub-millisecond responses? → **FalkorDB / Memgraph** (in-memory)

### 1.1 Detailed Comparison

```
┌────────────────┬──────────┬──────────┬──────────┬────────────────────────────┐
│ Database       │ Type     │ Scale    │ Query    │ Best For                   │
├────────────────┼──────────┼──────────┼──────────┼────────────────────────────┤
│ Neo4j          │ Property │ Billions │ Cypher   │ Production, large ecosystem│
│ (Community/Ent)│ Graph    │ nodes    │ GQL      │ Full-text, GDS, Aura cloud │
│ NebulaGraph    │ Distrib. │ Trillions│ nGQL     │ Trillions of edges, scale-out │
│                │ Property │ edges    │          │ Alibaba, Tencent scale     │
│ FalkorDB       │ Redis    │ Millions │ Cypher   │ Low-latency, Redis stack   │
│ Kuzu           │ Embedded │ Millions │ Cypher   │ Local, Python-native, <1s  │
│ NetworkX       │ Library  │ 100K     │ Python   │ Prototyping, algorithms    │
│ Amazon Neptune │ Managed  │ Billions │ Gremlin/ │ AWS managed, SPARQL+PG     │
│                │ PG + RDF │          │ SPARQL   │                            │
│ Memgraph       │ In-memory│ Millions │ Cypher   │ Real-time, streaming       │
└────────────────┴──────────┴──────────┴──────────┴────────────────────────────┘
```

### 1.2 Decision Matrix

> 📄 **Example code:** [`examples/01-1-2-decision-matrix.py`](examples/01-1-2-decision-matrix.py)

**Recommendation for this Framework:**

| Stage | DB | Reason |
|-----------|----|-------|
| **Learning & Prototyping** | Kuzu or NetworkX | Zero setup, `pip install`, runs locally |
| **Development** | Neo4j Community (Docker) | Standard Cypher, GDS library, easy migration to Aura |
| **Production** | Neo4j Aura / NebulaGraph | Managed, HA, backup |

> **📌 Bonus Concept: FalkorDB & Hybrid Indexing**
>
> **FalkorDB** = a graph database that runs **directly on Redis** (formerly "RedisGraph"). It stores the graph as **sparse matrices** (using the GraphBLAS sparse-matrix library) — essentially "computing traversal with matrix multiplication", extremely fast for data held in RAM. Queries use Cypher, with **sub-millisecond** responses even at millions of nodes.
>
> **"Hybrid indexing in a single engine"**: FalkorDB indexes **multiple data types on the same node** — full-text (find "names containing 'Phoenix'"), vector search (find "entities similar to this embedding"), and range indexes (filter by number). That means a GraphRAG query can filter by text + vector + time **right inside the DB**, without pulling results back to the application layer. Neo4j also combines full-text + vector indexes since 5.x; Kuzu added vector indexes in v1.5 — the general trend is **one engine, many index types**.

---

## 2. Cypher & GQL — The Query Language

> **�📌 Core Concept:**
> **Cypher** = a graph query language (like SQL for relational DBs). A Cypher statement **"draws"** the pattern you want to find — it reads quite intuitively:
>
> ```
> MATCH (a:Person)-[:MANAGES]->(b:Person)  ← "draw": Person a —MANAGES→ Person b
> WHERE a.name = 'Alice'                   ← "filter": Alice only
> RETURN b.name                            ← "take out": the employees' names
> ```
>
> **Symbol syntax:**
> - `(n)` = node, `(n:Label)` = node with a label, `(n:Label {prop: 'val'})` = node with a property
> - `--` = undirected, `-->`/`<--` = directed, `-[:TYPE]->` = typed edge
> - `*1..3` = 1 to 3 hops (traversal)
>
> **Analogy:** SQL = questions about a spreadsheet (you have to know the columns in advance). Cypher = describing a picture of the relationship (draw the pattern, the DB finds the match itself).

### 2.1 Basic CRUD

### 2.1 Basic CRUD

<details>
<summary>Cypher Code — CRUD (Click to view)</summary>

> 📄 **Example code:** [`examples/02-2-1-basic-crud.cypher`](examples/02-2-1-basic-crud.cypher)

</details>

### 2.2 Traversal — The Power of Graphs

<details>
<summary>Cypher Code — Traversal Patterns (Click to view)</summary>

> 📄 **Example code:** [`examples/03-2-2-traversal-the-power-of-graphs.cypher`](examples/03-2-2-traversal-the-power-of-graphs.cypher)

</details>

### 2.3 Full-Text & Vector Search Inside the Graph

Neo4j supports hybrid: graph traversal + full-text + vector indexes in the same DB.

> 📄 **Example code:** [`examples/04-2-3-full-text-vector-search-inside-the.cypher`](examples/04-2-3-full-text-vector-search-inside-the.cypher)

---

## 3. Indexing & Performance

> **📌 Core Concept:**
> **An index = the "table of contents" of a database** — like the index at the back of a book: to find which page "Alice" is on, you don't flip through every page, you just look at the index. No index → every query must **scan the entire** graph (very slow at millions of nodes).
>
> **Principle:** Every index has a **write cost** (each new node must update the index). So only create indexes on **fields you query frequently** — don't create them willy-nilly.
>
> **Index type = the query type you need:**
> - Look up by exact name/id → **Range Index**
> - Search by fuzzy keywords in text → **Full-Text Index** (works like Google search)
> - Search by meaning (semantic, using vectors) → **Vector Index** (ANN finds the closest matches)
> - Filter on multiple properties → **Composite Index**
> - Need to guarantee no duplicates → **Unique Constraint** (creates an index behind the scenes)

### 3.1 The Index Types

```
┌──────────────────┬─────────────────────────────────┬─────────────────────────┐
│ Index Type       │ When to use                    │ Cypher                  │
├──────────────────┼─────────────────────────────────┼─────────────────────────┤
│ Range Index      │ Lookup by property (name, id)  │ CREATE INDEX FOR (n:Person) ON (n.name) │
│ Full-Text Index  │ Search by keyword               │ CREATE FULLTEXT INDEX ... ON EACH [n.bio] │
│ Vector Index     │ Semantic search                │ CREATE VECTOR INDEX ... ON n.embedding │
│ Composite Index  │ Filter on multiple properties  │ CREATE INDEX FOR (n:Project) ON (n.name, n.status) │
│ Constraint (unique)│ Guarantee uniqueness + hidden index │ CREATE CONSTRAINT FOR (n:Person) REQUIRE n.name IS UNIQUE │
└──────────────────┴─────────────────────────────────┴─────────────────────────┘
```

### 3.2 Query Optimization

> 📄 **Example code:** [`examples/05-3-2-query-optimization.py`](examples/05-3-2-query-optimization.py)

### 3.3 Profiling

> 📄 **Example code:** [`examples/06-3-3-profiling.cypher`](examples/06-3-3-profiling.cypher)

---

## 4. Transactions & Consistency

### 4.1 ACID for Graphs

```
┌───────────┬──────────────────────────────────────────────────────────┐
│ Property  │ Meaning for graphs                                       │
├───────────┼──────────────────────────────────────────────────────────┤
│ Atomicity │ Batch ingest: either everything succeeds, or full rollback │
│ Consistency│ No violation of ontology constraints                   │
│ Isolation │ Two concurrent transactions don't create duplicate nodes │
│ Durability│ After commit, data survives a crash                     │
└───────────┴──────────────────────────────────────────────────────────┘
```

### 4.2 Batch Ingest (Idempotent)

<details>
<summary>Python Code — Batch Ingest with MERGE (Click to view)</summary>

> 📄 **Example code:** [`examples/07-4-2-batch-ingest-idempotent.py`](examples/07-4-2-batch-ingest-idempotent.py)

**Key pattern:** `MERGE` instead of `CREATE` → idempotent, re-running doesn't create duplicates.

</details>

---

## 5. Deployment with Neo4j & Kuzu

### 5.1 Neo4j with Docker

> 📄 **Example code:** [`examples/08-5-1-neo4j-with-docker.yaml`](examples/08-5-1-neo4j-with-docker.yaml)

> 📄 **Example code:** [`examples/09-5-1-neo4j-with-docker.sh`](examples/09-5-1-neo4j-with-docker.sh)

### 5.2 Kuzu (Embedded, Python-Native)

<details>
<summary>Python Code — Kuzu Embedded (Click to view)</summary>

> 📄 **Example code:** [`examples/10-5-2-kuzu-embedded-python-native.py`](examples/10-5-2-kuzu-embedded-python-native.py)

</details>

### 5.3 NetworkX (Prototyping, No DB Needed)

> 📄 **Example code:** [`examples/11-5-3-networkx-prototyping-no-db-needed.py`](examples/11-5-3-networkx-prototyping-no-db-needed.py)

---

## 6. Hands-On Labs

### Lab 1: Neo4j Docker + Cypher CRUD

1. `docker compose up -d neo4j`
2. Open `http://localhost:7474`, run the Cypher queries from §2.1
3. Create 20 nodes + 30 edges for a mini org chart

### Lab 2: Benchmark the Impact of Indexes

1. Create 10K nodes without an index → measure the time for `MATCH (n:Person {name: 'Alice'})`
2. Create the index `CREATE INDEX FOR (n:Person) ON (n.name)` → measure again
3. Compare latency (typically an 80–90% reduction)

### Lab 3: Compare 3 DBs

- Take the same 1K-node dataset, ingest it into NetworkX, Kuzu, and Neo4j
- Run the same `MATCH (a)-[*1..3]->(b)` query and compare latency

---

## References

- Neo4j Docs — *Cypher Manual* (https://neo4j.com/docs/cypher-manual/current/)
- Kuzu Docs — *Cypher Query* (https://docs.kuzudb.com/cypher/)
- *Graph Databases* — Robinson, Webber, Eifrem (O'Reilly, 2nd Edition)
- FalkorDB Docs — *Hybrid index: vector + full-text + range* (https://www.falkordb.com/docs/)
- LDBC — *Social Network Benchmark* (https://ldbcouncil.org/benchmarks/snb/)

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

*Next: [04 — Graph Embeddings](../04-graph-embeddings/)*
