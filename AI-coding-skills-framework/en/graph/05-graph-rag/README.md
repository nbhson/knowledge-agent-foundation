# 🔍 05. GraphRAG — Retrieval-Augmented Generation on Graphs

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Does GraphRAG Matter?](#why-does-graphrag-matter)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Vanilla RAG vs GraphRAG](#1-vanilla-rag-vs-graphrag)
> - [2. The GraphRAG Pipeline in Detail — 6 Steps](#2-the-graphrag-pipeline-in-detail--6-steps)
> - [3. Local Search vs Global Search](#3-local-search-vs-global-search)
> - [4. Community Summarization](#4-community-summarization)
> - [5. Implementing GraphRAG in Python](#5-implementing-graphrag-in-python)
> - [6. When to Use GraphRAG?](#6-when-to-use-graphrag)
> - [7. Hands-On Labs](#7-hands-on-labs)
> - [References](#references)

---

### Opening Story

You have 1,000 financial reports. You ask:

> *"What are the standout trends in the AI market in 2024?"*

**Vanilla RAG**: chop 1,000 reports into pieces → embed them → pick the 5 chunks closest to the question → hand them to the LLM. You get back 5 separate passages about "AI trends" but **no big picture** — each chunk only covers one small angle.

**GraphRAG**: before the question even arrives, it has extracted a KG + detected communities (e.g. an "AI Investment" community of 200 entities, an "AI Regulation" community of 150 entities) + summarized each community with an LLM. When asked, it **map-reduces over the community summaries** → a comprehensive answer with **30–40% higher comprehensiveness + diversity** (Microsoft, 2024).

**GraphRAG does not replace RAG. It makes RAG smarter by using the shape of the graph.**

### Why Does GraphRAG Matter?

> *"Vanilla RAG answers WHERE. GraphRAG answers WHY and HOW, with evidence paths."*

| # | Research | Finding |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | On global sensemaking Q&A, GraphRAG wins **70%** of the time vs vanilla RAG (LLM judge) |
| 2 | **Microsoft GraphRAG (2024)** | Comprehensiveness: GraphRAG is **+35%**, Diversity: **+30%** vs baseline |
| 3 | **Anthropic (2025)** | Graph-grounded generation cuts **hallucination by 28%** on enterprise QA |

---

## Overview

```
                    ┌─────────────────────────────────┐
                    │         INDEXING PIPELINE         │
                    │         (Offline, once)          │
Documents ──────────►│  Extract KG → Communities →      │
(1K-100K docs)      │  Community Summaries              │
                    └──────────────┬──────────────────┘
                                   │ Graph Index
                    ┌──────────────▼──────────────────┐
                    │       QUERY PIPELINE              │
User Query ────────►│  Local Search  vs  Global Search  │
                    │  (entity-centric)  (community)    │
                    └──────────────┬──────────────────┘
                                   │ Retrieved Context
                    ┌──────────────▼──────────────────┐
                    │     GENERATION (LLM)              │
                    │  Context + Query → Answer + Paths │
                    └─────────────────────────────────┘
```

---

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Vanilla vs GraphRAG](#1-vanilla-rag-vs-graphrag) | Detailed comparison, trade-offs |
| 2 | [The 6-Step Pipeline](#2-the-graphrag-pipeline-in-detail--6-steps) | From documents to answer |
| 3 | [Local vs Global](#3-local-search-vs-global-search) | The two query modes |
| 4 | [Community Summarization](#4-community-summarization) | Leiden + LLM summarization |
| 5 | [Implementation](#5-implementing-graphrag-in-python) | Complete Python code |
| 6 | [Retriever Types & Fusion](#6-retriever-types--fusion) | Text2Cypher, DRIFT, agentic + RRF |
| 7 | [GraphRAG Variants](#7-graphrag-variants-sota) | LightRAG, HippoRAG2, KAG, GRAG |
| 8 | [When to Use](#8-when-to-use-graphrag) | Decision guide + counter-evidence |
| 9 | [Hands-On Labs](#9-hands-on-labs) | Practice |

---

## 1. Vanilla RAG vs GraphRAG

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│ Aspect           │ Vanilla RAG                      │ GraphRAG                         │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Index unit       │ Chunk embeddings (vector DB)     │ Entities + Relations + Communities│
│ Retrieval        │ Cosine similarity top-K          │ Subgraph traversal + community   │
│ Context          │ 5-10 disconnected chunks         │ Subgraph + community summaries   │
│ Global Q&A       │ ❌ Weak (can't synthesize)       │ ✅ Strong (map-reduce summaries) │
│ Local Q&A        │ ✅ Good                          │ ✅ Good (entity-centric)         │
│ Multi-hop        │ ❌ Hallucinates                  │ ✅ Path-based, with citations    │
│ Cost (indexing)  │ Low (just embedding)             │ High (LLM extraction + summary)  │
│ Cost (query)     │ Low                              │ Medium (traversal + rerank)      │
│ Explainability   │ Low (chunks)                     │ High (path + subgraph)           │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

**GraphRAG's indexing cost** is higher (LLM calls to extract + summarize), but it's a **one-time offline cost**. Query cost is equivalent or lower thanks to the more concise context.

> 📄 **Example code:** [`examples/01-1-vanilla-rag-vs-graphrag.py`](examples/01-1-vanilla-rag-vs-graphrag.py)

---

## 2. The GraphRAG Pipeline in Detail — 6 Steps

### Step 1: Document Processing & Chunking

> 📄 **Example code:** [`examples/02-step-1-document-processing-chunking.py`](examples/02-step-1-document-processing-chunking.py)

### Step 2: Entity & Relation Extraction (LLM)

See details: [`02-knowledge-graph`](../02-knowledge-graph/) — use the gleaning loop `extract_entities` + `extract_relations`.

### Step 3: Community Detection (Leiden)

> **Concept:** split the graph into tightly connected **groups (communities)** — like dividing 1000 employees into teams/departments. Each community = one "topic" grouping all related entities.
>
> **Why is it needed?** Querying an entire graph of millions of nodes is very expensive. Grouping them → you only need to summarize each group (Step 4), and a global query reads the group summaries instead of the raw entities.
>
> The **Leiden** algorithm: an improvement over Louvain — faster + yields more clearly separated communities. Details in §4.1.

### Step 4: Community Summarization (LLM)

> **Concept:** for each community (group) found in Step 3, use the **LLM to summarize it into a short passage** describing what the group is about.
>
> **Analogy:** like a "meeting-minutes summary" for each team: 100 teams → 100 short minutes instead of reading every person's file. When asked "what is the whole company doing?", you only read those 100 minutes.
>
> Result: each community gets one `summary` → stored in the graph as a node/attribute. Details in §4.2.

### Step 5: Retrieval (Local vs Global)

> **Concept:** queries split into two types:
> - **Local Search** (asking details about one entity): find the node → expand neighbors with BFS → collect the embeddings + context of the related nodes
> - **Global Search** (asking the big picture, comparisons, trends): map-reduce over **community summaries** — each summary goes to the LLM, then the results are merged
>
> **Analogy:** Local = looking up one person's file (reading their friends, team, projects). Global = reading a company-wide aggregate report (reading each department, then merging). Details in §3.

### Step 6: Generation (LLM with Graph Context)

> **Concept:** the final step — put the context (a list of entities, relations, paths, or summaries) + the question into the prompt; the LLM produces the answer with **evidence sources** (the triple/paths taken from the graph).
>
> **The difference from regular RAG:** because the context is **graph structure** (not a string of disconnected text), the LLM answers along the relationships — "Alice is friends with Bob through Phoenix" instead of "Alice might know Bob".

The whole pipeline is implemented in detail in §5.

---

## 3. Local Search vs Global Search

This is the **core distinction** of GraphRAG that vanilla RAG doesn't have:

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────────┐
│                  │ Local Search                     │ Global Search                    │
├──────────────────┼──────────────────────────────────┼──────────────────────────────────┤
│ Sample question  │ "Who approved the Phoenix contract?"│ "What are the AI trends of 2024?" │
│ Starts from      │ Entities in the query            │ All community summaries          │
│ Query            │ Entity → neighbors (1-2 hops)    │ Map-Reduce over summaries        │
│ Context          │ Subgraph around the entities     │ Summaries from many communities  │
│ Best for         │ Factoid, multi-hop, entity Q&A   │ Synthesis, thematic, sensemaking │
│ Similar to vanilla?│ Yes, but with paths             │ No — vanilla RAG can't do this  │
└──────────────────┴──────────────────────────────────┴──────────────────────────────────┘
```

### 3.1 Local Search — Entity-Centric

```
Query: "Who approved the Phoenix contract?"

1. Extract entities from the query: ["Phoenix", "contract"]
2. Find entities in the KG matching the query (vector similarity)
3. Traverse 1-2 hops around those entities:
   Phoenix —[BELONGS_TO]→ Contract C-2024 —[APPROVED_BY]→ Alice (confidence: 0.95)
4. Collect: nodes + edges + text chunks of the entities/relations
5. Re-rank with a cross-encoder
6. Feed the LLM prompt with the paths
```

### 3.2 Global Search — Community-Based

```
Query: "What are the AI trends of 2024?"

1. Do NOT extract entities — the query is too general to map to a specific entity
2. Take ALL community summaries (e.g. 50 communities)
3. Map: the LLM answers the query BASED ON each community summary (in parallel)
   - Community "AI Investment" → "AI investment up 40%..."
   - Community "AI Regulation" → "The EU AI Act takes effect..."
   - Community "AI in Healthcare" → "AI diagnostics increasing..."
4. Reduce: the LLM synthesizes the partial answers into a final answer
5. Each claim carries a citation back to its source community
```

---

## 4. Community Summarization

### 4.1 Community Detection (Leiden Algorithm)

Leiden is currently the best community-detection algorithm (an improvement over Louvain):

> 📄 **Example code:** [`examples/03-4-1-community-detection-leiden-algorithm.py`](examples/03-4-1-community-detection-leiden-algorithm.py)

### 4.2 LLM Community Summarization

<details>
<summary>Python Code — Community Summarization (Click to view)</summary>

> 📄 **Example code:** [`examples/04-4-2-llm-community-summarization.py`](examples/04-4-2-llm-community-summarization.py)

</details>

### 4.3 Hierarchical Communities

GraphRAG does **hierarchical clustering**: low-level communities are merged into higher-level communities → creating a hierarchy for global search at multiple levels of detail.

```
Level 0: the whole graph (1 community)
  └── Level 1: 5 large communities (AI, Finance, HR, ...)
        └── Level 2: 20 small communities (AI-Investment, AI-Regulation, ...)
              └── Level 3: Entities + Relations (leaves)
```

---

## 5. Implementing GraphRAG in Python

<details>
<summary>Python Code — Complete GraphRAG Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/05-5-implementing-graphrag-in-python.py`](examples/05-5-implementing-graphrag-in-python.py)

</details>

---

## 6. Retriever Types & Fusion

> **📌 Core Concept:**
> **Retriever** here means "the thing that pulls" — the part that decides **what to take** from the graph/vector to feed the LLM. It's not just "Local/Global". In practice there's a **catalog of many retriever types**, each fitting a different kind of question.

### 6.1 Catalog of Retriever Types

| Retriever | How it works | Example question it fits | Neo4j counterpart |
|---|---|---|---|
| **VectorRetriever** | Embed the question → similarity over entities/LLM text | "Find documents about X" | KNN vector index |
| **VectorCypherRetriever** | Vector top-k → **traverse further to neighbors** via Cypher | "Which people are related to documents about X?" | vector + `MATCH` |
| **HybridRetriever** | Vector + full-text → **RRF fusion** | "The keyword 'Phoenix' or fuzzy text" | combined indexes |
| **Text2Cypher** | LLM translates the question → Cypher → run the query | "Who manages the most projects?" | LLM-generated Cypher |
| **DRIFT** (Microsoft) | "Drive the search": fetch as fast and wide as possible | The first path hits a dead end → pivot | Agentic traversal |
| **Tools/Agentic retriever** | An LLM agent picks its own tools (vector/traversal/cypher) | A mix of many question types | `ToolsRetriever` |

### 6.2 Text2Cypher (NL → Cypher) in Detail

> **📌 Core Concept:**
> **Text2Cypher** = the LLM acting as a "translator from human questions to Cypher". Unlike regular retrieval (pulling text back) — here **the answer is the query itself**; once it runs, the DB returns structured results.
>
> The formula for success: **Enhanced Schema Injection** — don't stuff the entire schema in (token-hungry, confuses the LLM); inject only:
> - labels (entity types) + attribute names
> - a few **semantically important parent-child relations** (`(Person)-[:REPORTS_TO]->(Person)`)
>
> ```python
> # Enhanced schema for Text2Cypher — inject only what's needed
> def enhanced_schema_snippet() -> str:
>     return """Nodes: Person(name,role), Project(name,budget)
> Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
> Sample: (Alice,REPORTS_TO,Bob) — Bob is Alice's manager"""
>
> # When a query returns empty → Text2Cypher self-corrects the Cypher statement (Self-correction)
> # When the schema is insufficient → ask for more metadata itself (schema refinement)
> ```

### 6.3 RRF — Merging Multiple Sources Without "Scores"

> **📌 Core Concept:**
> **RRF (Reciprocal Rank Fusion)** = a way to combine multiple ranked lists (from vectors, from graph traversal, from full-text) **without normalizing scores**. The new score for each item:
>
> ```
> score = Σ  1 / (k + rank_i)      with k ≈ 60
> ```
>
> Original meaning: **the higher an item ranks in more lists, the more it gets rewarded**. An item at #1 in vectors (receiving ~1/61) but absent from graph traversal is outscored by an item at #8 that appears in both sources (receiving ~1/68 + 1/68 > 1/61).
>
> **Analogy:** like an "inside track" vote: only people nominated on many different ballots make the final — even if nobody ranked them first. RRF is a technique in the **hybrid retrieval** problem — combining graph traversal results + vector similarity.

> 📄 **Example code:** [`examples/06-6-3-rrf-merging-multiple-sources-without-scores.py`](examples/06-6-3-rrf-merging-multiple-sources-without-scores.py)

---

## 7. GraphRAG Variants (SOTA)

> **📌 Core Concept:**
> **GraphRAG is not "one formula"** — from Microsoft's original GraphRAG (index + the subsequent connected variants) up to 2025–2026, many different optimization directions have appeared for different problems. The table below is a **map of the most-cited variants**:

| Variant | Core idea | Strong when | Weakness/limits |
|---|---|---|---|
| **GraphRAG (MSFT)** | Index + Leiden communities + LLM summaries | Global/sensemaking, multi-doc | Expensive (indexing costs tokens), slow |
| **LazyGraphRAG** (MSFT, 2024-2025) | Defers LLM summarisation to query time | Indexing cost equal to vector RAG, quality equal to GraphRAG, ~700× lower query cost | Integrated into Microsoft Discovery (2025) |
| **LightRAG** | Dual-level index (low/high); retrieval per query; 10× faster than GraphRAG, 1/3–1/4 the cost | Retrieval coverage, low cost | Not as good at global aggregation as the original |
| **HippoRAG (v2)** | Personalized PageRank on the KG + pairwise hybrid | Multi-hop, answers with **fewer tokens** (20× cheaper) | Depends on KG quality |
| **KAG** | KG-augmented generation, semantic reasoning | When explanation/logic answers are needed | Complex configuration |
| **DRIFT (MSFT)** | "Drive the search": explore in as many directions as needed | Complex queries needing multi-direction | Complex agent loop |
| **GRAG** | Divide-and-conquer subgraph retrieval | Less noise on large graphs | Needs a complex pipeline |

> **Summary for picking a variant:**
> - Need **fast + cheap + broad coverage**: `LightRAG`
> - Answer **multi-hop with few tokens**: `HippoRAG2`
> - **Global/sensemaking over the whole corpus**: original `GraphRAG`
> - **Complex queries that need to rethink**: `DRIFT`
>
> In this learning framework, **knowing the mechanisms (index + retrieve + community summary)** matters most — the variants are just refinements of those three stages.

---

## 8. When to Use GraphRAG?

```
┌──────────────────────────┬──────────────┬──────────────────────────────┐
│ Question type            │ Use what?     │ Example                      │
├──────────────────────────┼──────────────┼──────────────────────────────┤
│ Factoid (1-hop)          │ Vanilla RAG  │ "What does section 5 of contract X say?" │
│                          │ or Local     │ "Who manages team Y?"         │
│ Multi-hop (2-4 hops)     │ Local GraphRAG│ "Who approved the contract of project X │
│                          │              │  and who does that person report to?"│
│ Global / Sensemaking     │ Global GraphRAG│ "What are the main themes in these 1000 │
│                          │              │  documents?"            │
│ Aggregation              │ Global       │ "How many AI projects are there │
│                          │              │  and who manages them?"       │
│ Codebase Q&A             │ Local (code  │ "Where is function X called?"   │
│                          │  graph)      │                              │
└──────────────────────────┴──────────────┴──────────────────────────────┘
```

**Decision flowchart:**

```
Does the question need synthesis across MANY documents?
  ├── No → Local Search (entity → subgraph)
  └── Yes → Global Search (community summaries → map-reduce)

Does the question have specific entities?
  ├── Yes → Local Search (start from those entities)
  └── No → Global Search (no anchor to traverse from)
```

> **⚠️ When NOT to Use GraphRAG (2025–2026 benchmark evidence):**
>
> Systematic comparison studies (RAG vs GraphRAG) show **GraphRAG doesn't always win**:
> 1. **Single-hop / factoid**: vanilla RAG **beats** GraphRAG on "single fact" questions (e.g. NQ) — because graph retrieval adds unnecessary traversal cost.
> 2. **Global community search can hallucinate**: a community summary may **lack specific context** → the LLM "makes things up" when asked for details from that summary.
> 3. **Indexing is extremely expensive**: LLM-summarizing all communities ≈ very high indexing cost on large corpora — if you only have 50 internal docs, don't build GraphRAG.
>
> **Pragmatic decision:**
> - Corpus < 100 docs, answers mostly factoid → **vanilla RAG is enough**.
> - Need multi-hop, aggregation, themes spanning many docs → **GraphRAG**.
> - In between: **LightRAG / HippoRAG** (lighter, cheaper text2cypher retriever).

---

## 9. Hands-On Labs

### Lab 1: Compare Vanilla RAG vs GraphRAG

1. Prepare 20 documents on one topic (e.g. "AI in Healthcare" — create or scrape them)
2. Run vanilla RAG (vector top-5) and GraphRAG (local search) on 10 queries
3. Judge manually: which questions does GraphRAG win? (global queries win clearly)

### Lab 2: Tuning Community Resolution

1. Try `resolution` = 0.5, 1.0, 2.0 in `detect_communities`
2. Observe the number of communities and global search quality
3. Find the optimal resolution for your dataset

### Lab 3: Build a Codebase GraphRAG

1. Parse a small repo (50 files) → build a code graph (File → Function → Calls)
2. Ask: "Changing function X affects which files?" → local search on the code graph
3. Compare with plain `grep`

---

## References

- Edge et al. — *From Local to Global: A GraphRAG Approach to Query-Focused Summarization* (Microsoft Research, 2024) — https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG — *GitHub* (https://github.com/microsoft/graphrag) — implementation + config
- Neo4j — *Building a Knowledge Graph with LLM* (https://neo4j.com/blog/developer/knowledge-graph-llm/)
- LangChain — *GraphCypherQAChain* (https://python.langchain.com/docs/use_cases/graph/)
- *GraphRAG in Practice: A Survey of Research Gaps* (arXiv:2507.03226) — RRF, retrieval & indexing at scale
- Neo4j graphrag-python — *Retriever types: Vector, VectorCypher, Hybrid, Text2Cypher, DRIFT* (https://neo4j.com/docs/graphrag-python/current/)
- *RAG vs GraphRAG: A Systematic Evaluation* — multi-hop wins, single-hop loses to vanilla RAG (arXiv 2025)
- LightRAG / HippoRAG2 — *Reducing graph retrieval cost* (https://github.com/HKUDS/LightRAG)

---

*Next: [06 — Graph Reasoning](../06-graph-reasoning/)*
