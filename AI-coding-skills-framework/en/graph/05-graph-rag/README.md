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

> **One-line summary:** Vanilla RAG returns scattered chunks; GraphRAG pre-builds a graph with community summaries, so big-picture questions get one synthesized answer with citations.

(KG = Knowledge Graph — a network of entities and labeled relations; chunk = a small slice of text cut from a document.)

### Why Does GraphRAG Matter?

> *"Vanilla RAG answers WHERE. GraphRAG answers WHY and HOW, with evidence paths."*

How to read this table: each row is one published result. **#** = row number, **Research** = who published it, **Finding** = the measured effect. For instance, row 1 says an LLM judge preferred GraphRAG's answers 70% of the time on big-picture questions.

| # | Research | Finding |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | On global sensemaking Q&A, GraphRAG wins **70%** of the time vs vanilla RAG (LLM judge) |
| 2 | **Microsoft GraphRAG (2024)** | Comprehensiveness: GraphRAG is **+35%**, Diversity: **+30%** vs baseline |
| 3 | **Anthropic (2025)** | Graph-grounded generation cuts **hallucination by 28%** on enterprise QA |

(sensemaking = "make sense of the whole corpus" questions; hallucination = the model inventing facts with a confident tone.)

> **One-line summary:** Benchmarks show GraphRAG clearly wins on synthesis and hallucination reduction — that is the value you are paying extra indexing cost for.

---

## Overview

This diagram shows the two halves of GraphRAG: a one-time offline indexing pipeline, and the per-query pipeline that runs when a user asks something.

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

> **One-line summary:** Index once (extract graph → group → summarize), then at query time choose local (entity) or global (community) search and generate an answer with evidence paths.

---

## Contents

How to read this table: each row is one section of this file. **#** = order, **Topic** = the clickable title, **Description** = what you will learn. For instance, row 3 covers the two query modes.

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

> **One-line summary:** The file walks from the comparison, through the 6-step pipeline and query modes, to variants and a "when to use" decision guide.

---

## 1. Vanilla RAG vs GraphRAG

This section compares the two systems side by side, so you can see exactly what GraphRAG adds and what it costs.

How to read it: each row compares one aspect. **Aspect** = the property, **Vanilla RAG** = plain chunk-based retrieval, **GraphRAG** = graph-based retrieval. For instance, the "Multi-hop" row says vanilla RAG invents missing connections, while GraphRAG follows real paths with citations.

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

(multi-hop = a question whose answer needs 2+ chained relations, e.g. "who approved the contract of the project Alice works on?")

> **One-line summary:** GraphRAG costs more to build but less (or equal) per query, and it answers multi-hop and big-picture questions that vanilla RAG cannot.

> 📄 **Example code:** [`examples/01-1-vanilla-rag-vs-graphrag.py`](examples/01-1-vanilla-rag-vs-graphrag.py)

---

## 2. The GraphRAG Pipeline in Detail — 6 Steps

This section walks through the six steps that take raw documents to an answerable graph index.

### Step 1: Document Processing & Chunking

**What this step does:** cut every document into small chunks, because LLMs read and embed text in pieces.

> 📄 **Example code:** [`examples/02-step-1-document-processing-chunking.py`](examples/02-step-1-document-processing-chunking.py)

> **One-line summary:** Documents are split into chunks — the unit everything downstream (extraction, embedding) works on.

### Step 2: Entity & Relation Extraction (LLM)

**What this step does:** the LLM reads each chunk and pulls out entities (people, projects) and relations (WORKS_ON, MANAGES) between them.

See details: [`02-knowledge-graph`](../02-knowledge-graph/) — use the gleaning loop `extract_entities` + `extract_relations`.

(gleaning loop = a second extraction pass where the model is asked "what did you miss?", repeated until nothing new appears.)

> **One-line summary:** An LLM turns text chunks into graph entities and relations, with a second "gleaning" pass to catch what it missed.

### Step 3: Community Detection (Leiden)

> **Concept:** split the graph into tightly connected **groups (communities)** — like dividing 1000 employees into teams/departments. Each community = one "topic" grouping all related entities.
>
> **Why is it needed?** Querying an entire graph of millions of nodes is very expensive. Grouping them → you only need to summarize each group (Step 4), and a global query reads the group summaries instead of the raw entities.
>
> The **Leiden** algorithm: an improvement over Louvain — faster + yields more clearly separated communities. Details in §4.1.

> **One-line summary:** The graph is split into tightly connected communities, so global queries can read a few group summaries instead of millions of nodes.

### Step 4: Community Summarization (LLM)

> **Concept:** for each community (group) found in Step 3, use the **LLM to summarize it into a short passage** describing what the group is about.
>
> **Analogy:** like a "meeting-minutes summary" for each team: 100 teams → 100 short minutes instead of reading every person's file. When asked "what is the whole company doing?", you only read those 100 minutes.
>
> Result: each community gets one `summary` → stored in the graph as a node/attribute. Details in §4.2.

> **One-line summary:** Each community gets one short LLM-written summary — the "meeting minutes" that global search later reads.

### Step 5: Retrieval (Local vs Global)

> **Concept:** queries split into two types:
> - **Local Search** (asking details about one entity): find the node → expand neighbors with BFS → collect the embeddings + context of the related nodes
> - **Global Search** (asking the big picture, comparisons, trends): map-reduce over **community summaries** — each summary goes to the LLM, then the results are merged
>
> **Analogy:** Local = looking up one person's file (reading their friends, team, projects). Global = reading a company-wide aggregate report (reading each department, then merging). Details in §3.

(BFS = Breadth-First Search — visiting neighbors level by level, like ripples spreading on water.)

> **One-line summary:** Retrieval splits into two modes: entity-centric local search and community-summary global search.

### Step 6: Generation (LLM with Graph Context)

> **Concept:** the final step — put the context (a list of entities, relations, paths, or summaries) + the question into the prompt; the LLM produces the answer with **evidence sources** (the triple/paths taken from the graph).
>
> **The difference from regular RAG:** because the context is **graph structure** (not a string of disconnected text), the LLM answers along the relationships — "Alice is friends with Bob through Phoenix" instead of "Alice might know Bob".

The whole pipeline is implemented in detail in §5.

> **One-line summary:** The LLM writes the final answer from graph context, and because the context carries real paths, the answer cites its evidence.

---

## 3. Local Search vs Global Search

This section explains the core split in GraphRAG: two query modes that answer two different shapes of question.

How to read it: each row compares the two modes on one property. **Local Search** = start from named entities; **Global Search** = sweep all community summaries. For instance, "Who approved the Phoenix contract?" is local; "What are the AI trends of 2024?" is global.

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

> **One-line summary:** Local search extracts entities from the query, walks 1–2 hops around them, and hands the LLM a proof path with confidence scores.

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

> **One-line summary:** Global search asks the LLM about each community summary in parallel, then merges those partial answers into one cited big-picture response.

---

## 4. Community Summarization

This section zooms into the two steps that create the community summaries: detecting groups, then summarizing each one.

### 4.1 Community Detection (Leiden Algorithm)

**What this does:** the Leiden algorithm partitions the graph into tightly connected groups — the "departments" of your data.

Leiden is currently the best community-detection algorithm (an improvement over Louvain):

> 📄 **Example code:** [`examples/03-4-1-community-detection-leiden-algorithm.py`](examples/03-4-1-community-detection-leiden-algorithm.py)

> **One-line summary:** Leiden finds the natural clusters in your graph; those clusters are the unit that gets summarized and queried.

### 4.2 LLM Community Summarization

<details>
<summary>Python Code — Community Summarization (Click to view)</summary>

> 📄 **Example code:** [`examples/04-4-2-llm-community-summarization.py`](examples/04-4-2-llm-community-summarization.py)

</details>

> **One-line summary:** Each community is summarized once by an LLM and stored in the graph — these summaries are what global search reads.

### 4.3 Hierarchical Communities

GraphRAG does **hierarchical clustering**: low-level communities are merged into higher-level communities → creating a hierarchy for global search at multiple levels of detail.

```
Level 0: the whole graph (1 community)
  └── Level 1: 5 large communities (AI, Finance, HR, ...)
        └── Level 2: 20 small communities (AI-Investment, AI-Regulation, ...)
              └── Level 3: Entities + Relations (leaves)
```

> **One-line summary:** Communities stack into levels — small groups merge into big ones — so global search can pick how coarse or fine an answer should be.

---

## 5. Implementing GraphRAG in Python

This section points to the complete, runnable pipeline code combining all six steps.

<details>
<summary>Python Code — Complete GraphRAG Pipeline (Click to view)</summary>

> 📄 **Example code:** [`examples/05-5-implementing-graphrag-in-python.py`](examples/05-5-implementing-graphrag-in-python.py)

</details>

> **One-line summary:** The full pipeline — chunking, extraction, Leiden, summarization, retrieval, generation — exists as one runnable Python example.

---

## 6. Retriever Types & Fusion

This section catalogs the retriever types you can plug into GraphRAG, and how to merge results from several of them.

> **📌 Core Concept:**
> **Retriever** here means "the thing that pulls" — the part that decides **what to take** from the graph/vector to feed the LLM. It's not just "Local/Global". In practice there's a **catalog of many retriever types**, each fitting a different kind of question.

### 6.1 Catalog of Retriever Types

How to read this table: each row is one retriever you can pick. **Retriever** = its name, **How it works** = the mechanism, **Example question it fits** = the kind of question it serves best, **Neo4j counterpart** = the equivalent feature in the Neo4j graph database. For instance, Text2Cypher fits counting/aggregation questions like "who manages the most projects?"

| Retriever | How it works | Example question it fits | Neo4j counterpart |
|---|---|---|---|
| **VectorRetriever** | Embed the question → similarity over entities/LLM text | "Find documents about X" | KNN vector index |
| **VectorCypherRetriever** | Vector top-k → **traverse further to neighbors** via Cypher | "Which people are related to documents about X?" | vector + `MATCH` |
| **HybridRetriever** | Vector + full-text → **RRF fusion** | "The keyword 'Phoenix' or fuzzy text" | combined indexes |
| **Text2Cypher** | LLM translates the question → Cypher → run the query | "Who manages the most projects?" | LLM-generated Cypher |
| **DRIFT** (Microsoft) | "Drive the search": fetch as fast and wide as possible | The first path hits a dead end → pivot | Agentic traversal |
| **Tools/Agentic retriever** | An LLM agent picks its own tools (vector/traversal/cypher) | A mix of many question types | `ToolsRetriever` |

(Cypher = Neo4j's query language, the SQL of graphs; KNN = k-nearest-neighbors, the standard "closest vectors" search.)

> **One-line summary:** Pick the retriever by question type — vector for fuzzy text, Cypher for structured counts, hybrid for keywords, agentic for mixed workloads.

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
>
> **One-line summary:** Text2Cypher turns a question into a Cypher query; feed it a small schema sample, validate labels before running, and let it self-correct empty results.

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

> **One-line summary:** RRF merges ranked lists using only positions (score = Σ 1/(60+rank)), rewarding items that rank decently in several sources.

> 📄 **Example code:** [`examples/06-6-3-rrf-merging-multiple-sources-without-scores.py`](examples/06-6-3-rrf-merging-multiple-sources-without-scores.py)

---

## 7. GraphRAG Variants (SOTA)

> **📌 Core Concept:**
> **GraphRAG is not "one formula"** — from Microsoft's original GraphRAG (index + the subsequent connected variants) up to 2025–2026, many different optimization directions have appeared for different problems. The table below is a **map of the most-cited variants**:

This section maps the main GraphRAG variants, so you can pick one by cost and question type instead of by hype. (SOTA = state of the art, the best-performing methods right now.)

How to read this table: each row is one variant. **Variant** = its name, **Core idea** = what it does differently, **Strong when** = its sweet spot, **Weakness/limits** = what it gives up. For instance, LightRAG trades some global quality for 10× speed and lower cost.

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
>
> **One-line summary:** All variants share the same three stages (index, retrieve, summarize) — choose by your bottleneck: cost (LightRAG), token budget (HippoRAG2), or global synthesis (original GraphRAG).

---

## 8. When to Use GraphRAG?

This section gives a decision guide, including honest evidence for when GraphRAG is NOT worth it.

How to read it: each row is one question type. **Question type** = what the user asks, **Use what?** = the recommended system, **Example** = a real question of that type. For instance, a one-fact question ("what does section 5 say?") → plain RAG, not GraphRAG.

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
>
> **One-line summary:** Build GraphRAG only for multi-hop and corpus-wide questions; single-fact questions and tiny corpora are cheaper with plain RAG.

---

## 9. Hands-On Labs

These labs compare GraphRAG against plain RAG on real questions, so you learn where each wins.

### Lab 1: Compare Vanilla RAG vs GraphRAG

1. Prepare 20 documents on one topic (e.g. "AI in Healthcare" — create or scrape them)
2. Run vanilla RAG (vector top-5) and GraphRAG (local search) on 10 queries
3. Judge manually: which questions does GraphRAG win? (global queries win clearly)

> **One-line summary:** Run both systems on the same 10 queries and see for yourself that GraphRAG wins on big-picture questions, not fact lookups.

### Lab 2: Tuning Community Resolution

1. Try `resolution` = 0.5, 1.0, 2.0 in `detect_communities`
2. Observe the number of communities and global search quality
3. Find the optimal resolution for your dataset

(`resolution` = the granularity knob for community detection: low → few big groups, high → many small ones.)

> **One-line summary:** Sweep the `resolution` parameter and judge global-answer quality at each setting — the best number is dataset-specific.

### Lab 3: Build a Codebase GraphRAG

1. Parse a small repo (50 files) → build a code graph (File → Function → Calls)
2. Ask: "Changing function X affects which files?" → local search on the code graph
3. Compare with plain `grep`

(`grep` = a command-line text search that finds lines matching a pattern — fast, but it can't follow "who calls whom" chains.)

> **One-line summary:** Build a graph over code (File → Function → Calls) and use local search for impact questions that `grep` can't trace.

---

## References

> **One-line summary:** The sources behind this module — start with the original Microsoft GraphRAG paper (arXiv 2404.16130) and the Neo4j graphrag-python docs.

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
