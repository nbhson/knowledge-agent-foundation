# 🗄️ Vector Databases — Memory Storage & Retrieval for the Harness

This page explains **vector databases** — the storage that lets your agent find information *by meaning*, not just by exact keywords. It is the memory layer of the harness (harness = your agent's code skeleton, split into numbered components).

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Vector DBs Matter?](#why-vector-dbs-matter)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of Vector DBs](#overview-of-vector-dbs)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section shows why plain keyword search fails and what replaces it.

Your harness needs memory. But plain keyword memory is not enough — when a user asks *"what were the worker insurance terms we talked about last time?"*, a search that only matches exact words will miss the answer (the user said "worker insurance", the note said "employee compensation").

> *"Memory is the difference between a stateless function and an agent that learns."*

**Vector databases** fix this by turning each piece of text into a **vector embedding** (a list of numbers that captures *meaning*, computed by an embedding model) — and then searching by **cosine distance** (cosine distance = a similarity score between two vectors: small distance = similar meaning). This is the heart of `harness/01-retrieve-memory-knowledge`: instead of handing the LLM the whole library, you hand it only **the chunks that match best in meaning** (chunk = a slice of a document).

> **One-line summary:** A vector DB finds text by meaning instead of keywords, so the agent gets the right notes even when the wording differs.

### Why Vector DBs Matter?

This section gives the definition and four reasons this storage matters.

> - **Vector Embedding** turns text into a sequence of numbers (a vector) so computers can compare them
> - **Vector Database** stores and searches vectors quickly
> — HARNESS_ENGINEERING.md

How to read it: each row is one reason; "Explanation" says in plain words what it buys you. For instance, row 2 means the agent loads only the relevant pages into its context, not the whole archive.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Semantic search** | Find the right *meaning*, not just *keywords* — the base of RAG |
| 2 | **Memory tiers** | Only load what is relevant into context — saves a lot of tokens |
| 3 | **Independent of the LLM** | Embeddings live apart from generation — index once, search many times |
| 4 | **Already in the harness** | HARNESS_ENGINEERING.md uses a vectorStore for Tier 2 Warm Memory |

Glossary for the table: **RAG** (Retrieval-Augmented Generation) = the agent first retrieves documents, then answers from them; **context** = the text the model can read in one request; **tokens** = the billing units of model usage; **Tier 2 Warm Memory** = the harness's mid-speed memory layer (see the case study below).

> **One-line summary:** Vector search finds by meaning and keeps context small, and the harness already depends on it for warm memory.

### Relationship to the Harness

This section shows which harness components a vector DB plugs into.

```
┌────────────────────────────────────────────────────────────┐
│  VECTOR DB MAP VS HARNESS COMPONENTS                       │
│                                                            │
│  harness/01-retrieve-memory-knowledge → Retrieval (main)   │
│  harness/02-build-context            → Top-k chunks into ctx│
│  harness/03-update-memory-store      → Upsert embeddings   │
│  harness/06-decide-tools-mcp         → vector_search tool  │
└────────────────────────────────────────────────────────────┘
```

How to read the diagram: each line pairs one harness component with a vector-DB job. For instance, harness/03 writes new embeddings in (upsert = insert or update), and harness/06 exposes searching as a tool the agent can call.

```
In harness/01:
    User Query → Embedding → Vector DB → [relevant_chunk_1, relevant_chunk_2, ...]
                                                         ↓
                                        Context for the LLM (top-k chunks)
```

How to read this flow: a user question is turned into a vector, the DB returns the best-matching chunks (top-k = the k best matches, e.g. top-5), and those chunks become the context the LLM reads.

> **One-line summary:** The vector DB serves four harness components — retrieving memories, building context, storing updates, and the `vector_search` tool.

## Overview of Vector DBs

This section compares the four databases covered here so you can pick one.

How to read it: "Type" says open-source or managed cloud; "Standout features" says what makes it different; "Best for" says the situation it suits. For instance, Chroma installs with one `pip install` and runs locally, so it is ideal for a first prototype.

| Vector DB | Type | Standout features | Best for |
|-----------|------|-------------------|----------|
| **Chroma** | Open-source, local | `pip install chromadb`, Python-native, persistent local | Dev/Lab, quick learning, simple RAG |
| **Pinecone** | Managed cloud | Serverless, scales well, zero-ops, free tier available | Production, large scale, native cloud |
| **Qdrant** | Open-source + Cloud | Rust core, semantic + metadata filtering, very fast | Complex filtering, production |
| **Weaviate** | Open-source + Cloud | GraphQL native, hybrid search (vector + keyword) | Hybrid search, flexibility |

Glossary for the table: **managed** = the vendor runs the servers for you; **serverless** = you pay per use, no server to manage; **zero-ops** = no operations work on your side; **metadata filtering** = narrowing search by tags like date or author; **hybrid search** = combining vector meaning-matching with classic keyword matching; **GraphQL** = a query language for APIs.

## Vector DB Landscape 2025-2026

This section adds a wider market view, including the Postgres option.

| DB | Traits | Good for |
|----|---------|--------|
| Qdrant | Open source, Rust, hybrid search | Self-hosted, high performance |
| pgvector | Postgres extension | Small-medium scale, simple setup |
| Pinecone | Cloud-native, managed | Enterprise, managed infra |
| Weaviate | Open source, hybrid search | Multimodal (text+image) |
| Chroma | Local/embedded | Prototyping, local dev |

Glossary for the table: **pgvector** = a vector-search add-on for Postgres (Postgres = a widely used relational database); **multimodal** = handling more than one data type, e.g. text and images; **embedded** = running inside your own process, no separate server.

New embedding models (2026): OpenAI text-embedding-3-large, BGE-M3 (flag_embedding), Cohere v4.

> **A note on pgvector:** if your project already runs Postgres, `pgvector` is usually the lowest-friction choice — no new infrastructure, backups and permissions follow the database you already have. Its only limit is that at very large scale, raw speed trails dedicated engines like Qdrant or Pinecone.

> **One-line summary:** Start local with Chroma, move to a managed or self-hosted engine at scale — and if you already run Postgres, pgvector is the easiest first step.

### Chroma — Quick Start (Local)

This section points to a minimal working Chroma example.

> 📄 **Example code:** [`examples/01-chroma-quick-start-local.py`](examples/01-chroma-quick-start-local.py)

### Vector DB in the Tool Registry (harness/06)

This section shows the vector search exposed as a callable tool.

> 📄 **Example code:** [`examples/02-vector-db-in-the-tool-registry-harness-06.py`](examples/02-vector-db-in-the-tool-registry-harness-06.py)

## Learning Roadmap (Directory Structure)

This section maps the folder so you know what to read in which order.

```
vector-db/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Embeddings, cosine similarity, chunking, collections
├── 02-setup/            ← (TODO) Installing local Chroma → scaling to Pinecone/Qdrant cloud
├── 03-patterns/         ← (TODO) RAG, memory tiers, hybrid search, re-ranking
├── 04-savings/          ← (TODO) Token savings from top-k retrieval vs full context
└── 05-troubleshooting/  ← (TODO) Embedding mismatch, chunk boundaries, cold start
```

Glossary for the map: **chunking** = slicing documents into retrievable pieces; **collections** = named groups of vectors inside the DB; **re-ranking** = re-sorting retrieved chunks by a smarter second pass; **cold start** = an empty DB that returns nothing useful yet.

### Recommended Roadmap

This section gives the learning order in four steps, from concepts to scaling.

```
Step 1: Understand embeddings + cosine similarity (01-concepts)
   ↓
Step 2: Install local Chroma, create a collection + upsert a few test docs (02-setup)
   ↓
Step 3: Integrate into harness/01 — query top-k → feed into context
   ↓
Step 4: Upgrade to Pinecone/Qdrant when you need to scale (03-patterns)
```

This table points you to related reading elsewhere in the repo. "If you want to..." names your goal; "Read" names the page for it.

| If you want to... | Read |
|-------------------|------|
| Understand memory tiers | [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) |
| Build context from chunks | [harness/02-build-context](../../harness/02-build-context/) |
| Update the memory store | [harness/03-update-memory-store](../../harness/03-update-memory-store/) |
| LangChain RAG | [tools/langchain](../langchain/) |
| Embedding models | [ollama/MODEL.md](../../../../ollama/MODEL.md) |

> **One-line summary:** Learn embeddings first, prototype in local Chroma, wire it into harness/01, and switch engines only when scale demands it.

## Real-World Case Studies

This section shows two setups in use: project knowledge RAG and tiered memory.

### 1. RAG for Project Knowledge

This flow takes your project docs and answers questions from them. (RAG = retrieve documents first, then answer from them.)

```
Docs/ (Markdown, PDF)
   → Chunk (01-concepts: 500-1000 tokens/chunk with overlap)
   → Embed (sentence-transformers / ollama embeddings)
   → Upsert into the Chroma collection "project_memory"
   ↓
Agent asks → vector query → top-5 chunks → context for the LLM
```

How to read the flow: documents are sliced into chunks (overlap = neighboring chunks share a few tokens, so no idea is cut in half), converted to embeddings, stored, and the best 5 are handed to the model per question.

### 2. Memory Tiering (harness/01 Warm Memory)

This example shows the three memory speed tiers and where the vector DB sits. (Tiering = keeping data at different speeds and costs.)

```
Tier 1 Cold  → not embedded, stored as system files
Tier 2 Warm  → Chroma vector_store — fast retrieval, semantic
Tier 3 Hot   → context window — always available

HARNESS_ENGINEERING.md line 1954:
  // Tier 2: Warm Memory (Vector DB)
```

How to read the tiers: Cold = on disk, rarely read; Warm = in the vector DB, found by meaning in milliseconds; Hot = already inside the model's context window (the text the model can read in one request).

> **One-line summary:** Cut docs into chunks, embed them into a vector store, and keep hot facts in context, warm facts in the vector DB, cold facts on disk.

## Reference Materials

This section lists official pages and one research paper behind the tools above.

- **Chroma**: https://www.trychroma.com
- **Pinecone**: https://www.pinecone.io
- **Qdrant**: https://qdrant.tech
- **Weaviate**: https://weaviate.io
- **pgvector**: https://github.com/pgvector/pgvector
- **BGE-M3**: https://huggingface.co/BAAI/bge-m3
- **HNSW index paper**: https://arxiv.org/abs/1603.09320

### Links to Other Branches

This section links to the related pages in this repo.

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Tier 2 Warm Memory
- [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) — The retrieval component
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — The `vector_search` tool
- [tools/langchain](../langchain/) — LangChain retriever integrations
- [ollama/](../../../../ollama/) — Local embedding models (nomic-embed-text)

---

> **"Don't give your LLM the whole library — give it the three most relevant pages."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — vector-db*
