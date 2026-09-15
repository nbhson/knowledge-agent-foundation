# 🗄️ Vector Databases — Memory Storage & Retrieval for the Harness

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

Your harness needs memory. But keyword-style "memory" isn't enough — when the user asks *"what were the terms of the worker insurance we discussed last time?"*, memory that only finds exact-word matches will miss.

> *"Memory is the difference between a stateless function and an agent that learns."*

**Vector databases** solve this by turning every text into a **vector embedding** — a sequence of numbers that represents *meaning* — then searching by **cosine distance**. This is the foundation of `harness/01-retrieve-memory-knowledge`: instead of giving the LLM the entire knowledge base, you only give it **the semantically most relevant chunks**.

### Why Vector DBs Matter?

> - **Vector Embedding** turns text into a sequence of numbers (a vector) so computers can compare them
> - **Vector Database** stores and searches vectors quickly
> — HARNESS_ENGINEERING.md

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Semantic search** | Find the right *meaning*, not just *keywords* — the RAG foundation |
| 2 | **Memory tiers** | Only put what's relevant into context — significant token savings |
| 3 | **Independent of the LLM** | Embeddings are separated from generation — index once, query forever |
| 4 | **Already in the harness** | HARNESS_ENGINEERING.md uses a vectorStore for Tier 2 Warm Memory |

### Relationship to the Harness

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

```
In harness/01:
    User Query → Embedding → Vector DB → [relevant_chunk_1, relevant_chunk_2, ...]
                                                         ↓
                                        Context for the LLM (top-k chunks)
```

## Overview of Vector DBs

| Vector DB | Type | Standout features | Best for |
|-----------|------|-------------------|----------|
| **Chroma** | Open-source, local | `pip install chromadb`, Python-native, persistent local | Dev/Lab, quick learning, simple RAG |
| **Pinecone** | Managed cloud | Serverless, scales well, zero-ops, free tier available | Production, large scale, native cloud |
| **Qdrant** | Open-source + Cloud | Rust core, semantic + metadata filtering, very fast | Complex filtering, production |
| **Weaviate** | Open-source + Cloud | GraphQL native, hybrid search (vector + keyword) | Hybrid search, flexibility |

### Chroma — Quick Start (Local)

```python
import chromadb

client = chromadb.PersistentClient(path="./memory")   # harness/03 memory store
collection = client.get_or_create_collection("project_memory")

# Save memory (upsert — harness/03)
collection.upsert(
    ids=["doc-1"],
    documents=["Health insurance for workers: 4.5% contribution rate from 2026"],
    metadatas=[{"topic": "insurance", "tier": "warm"}]   # Tier 2 Warm Memory
)

# Retrieve (harness/01) — semantic search
results = collection.query(
    query_texts=["worker insurance benefits"],
    n_results=3  # top-k → harness/02 build context
)
```

### Vector DB in the Tool Registry (harness/06)

```python
registry.register(ToolDefinition(
    name="vector_search",
    description="Semantic search in the vector database",
    parameters={
        "query": {"type": "string", "required": True},
        "top_k": {"type": "integer", "default": 5},
        "collection": {"type": "string"},
        "filters": {"type": "object"},
    },
    category="search",
    tags=["semantic", "vector", "embedding"],
))
```

## Learning Roadmap (Directory Structure)

```
vector-db/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Embeddings, cosine similarity, chunking, collections
├── 02-setup/            ← (TODO) Installing local Chroma → scaling to Pinecone/Qdrant cloud
├── 03-patterns/         ← (TODO) RAG, memory tiers, hybrid search, re-ranking
├── 04-savings/          ← (TODO) Token savings from top-k retrieval vs full context
└── 05-troubleshooting/  ← (TODO) Embedding mismatch, chunk boundaries, cold start
```

### Recommended Roadmap

```
Step 1: Understand embeddings + cosine similarity (01-concepts)
   ↓
Step 2: Install local Chroma, create a collection + upsert a few test docs (02-setup)
   ↓
Step 3: Integrate into harness/01 — query top-k → feed into context
   ↓
Step 4: Upgrade to Pinecone/Qdrant when you need to scale (03-patterns)
```

| If you want to... | Read |
|-------------------|------|
| Understand memory tiers | [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) |
| Build context from chunks | [harness/02-build-context](../../harness/02-build-context/) |
| Update the memory store | [harness/03-update-memory-store](../../harness/03-update-memory-store/) |
| LangChain RAG | [tools/langchain](../langchain/) |
| Embedding models | [ollama/MODEL.md](../../../ollama/MODEL.md) |

## Real-World Case Studies

### 1. RAG for Project Knowledge

```
Docs/ (Markdown, PDF)
   → Chunk (01-concepts: 500-1000 tokens/chunk with overlap)
   → Embed (sentence-transformers / ollama embeddings)
   → Upsert into the Chroma collection "project_memory"
   ↓
Agent asks → vector query → top-5 chunks → context for the LLM
```

### 2. Memory Tiering (harness/01 Warm Memory)

```
Tier 1 Cold  → not embedded, stored as system files
Tier 2 Warm  → Chroma vector_store — fast retrieval, semantic
Tier 3 Hot   → context window — always available

HARNESS_ENGINEERING.md line 1954:
  // Tier 2: Warm Memory (Vector DB)
```

## Reference Materials

- **Chroma**: https://www.trychroma.com
- **Pinecone**: https://www.pinecone.io
- **Qdrant**: https://qdrant.tech
- **Weaviate**: https://weaviate.io
- **HNSW index paper**: https://arxiv.org/abs/1603.09320

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Tier 2 Warm Memory
- [harness/01-retrieve-memory-knowledge](../../harness/01-retrieve-memory-knowledge/) — The retrieval component
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — The `vector_search` tool
- [tools/langchain](../langchain/) — LangChain retriever integrations
- [ollama/](../../../ollama/) — Local embedding models (nomic-embed-text)

---

> **"Don't give your LLM the whole library — give it the three most relevant pages."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — vector-db*
