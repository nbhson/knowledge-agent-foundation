# ❓ FAQ — Vector Databases (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets). Each answer follows the same shape: **What you see** (the symptom), **Why** (the root cause), **What to do** (the fix), **Verify** (how to confirm it worked).

---

## Q1. A user asked about "worker insurance terms" and my keyword memory found nothing — why? [→ Why Vector DBs Matter?]

**What you see**

You stored "Health insurance for workers: 4.5% contribution rate from 2026". The user asks "what were the terms of the worker insurance we discussed last time?" Keyword search matches none of those words and returns nothing.

**Why**

Keyword memory needs the exact words. Vector memory compares *meaning*. Text is turned into a vector (a sequence of numbers representing the meaning — an "embedding"), stored in a collection, and searched by **cosine distance** (a similarity score: the smaller the distance, the closer the meaning) — the closest meaning wins even when no word matches.

**What to do**

1. Install local **Chroma** — it is one pip package and stores to a folder. (Chroma = an open-source vector database that runs on your own machine.)
2. Create a collection and `upsert` your documents with metadata (topic, tier). (`upsert` = insert new, or update if it already exists.)
3. Query with the user's own sentence, not with keywords.

> 📄 **Example code:** [`examples/01-q1-a-user-asked-about-worker-insurance-terms.py`](examples/01-q1-a-user-asked-about-worker-insurance-terms.py)

**Verify**

The same `query_texts` returns `doc-1` even though it shares no words with the query. Ask `n_results=3` and confirm the three results are all on-topic.

> **One-line summary:** Keyword search matches words; vector search matches meaning — so "worker insurance terms" still finds the 4.5% contribution note.

---

## Q2. Chroma, Pinecone, Qdrant, Weaviate or pgvector — which one do I start with? [→ Overview of Vector DBs]

**What you see**

Five names — two "managed cloud", three "open-source" — and you need to pick before you can retrieve anything. ("Managed cloud" = someone else runs the servers for you, usually paid; "open-source" = you can run it yourself for free.)

**Why**

The right choice depends on where you are, not on which one is "best".

How to read this table: each row is one vector DB, its type, and the situation where it is the right first pick. For instance, start with **Chroma** when you are learning on a laptop; pick **Pinecone** only when you need production scale with zero server maintenance.

| Vector DB | Type | Start here when |
|---|---|---|
| Chroma | open-source, local | learning, laptop, simple RAG |
| Pinecone | managed cloud | production at scale, zero ops |
| Qdrant | open-source + cloud | you need metadata filtering, self-hosted performance |
| Weaviate | open-source + cloud | you want hybrid vector + keyword or multimodal search |
| pgvector | Postgres extension | you already run Postgres, small-medium scale |

On embedding models (the models that turn text into those meaning-vectors), the 2026 shortlist: **OpenAI text-embedding-3-large**, **BGE-M3** (flag_embedding, runs locally), **Cohere v4**.

**What to do**

1. Learn and prototype on Chroma — `pip install chromadb`, no account, no server.
2. Move to Pinecone or Qdrant only when you outgrow one machine.
3. Keep the collection and document shapes the same so the swap is a client change, not a rewrite.
4. If Postgres is already in your stack, try pgvector first — no new service to operate.

**Verify**

On Chroma you can upsert and query in under a minute with no network. Migrating later should only change the client object, not your `documents` and `metadatas`.

> **One-line summary:** Start with Chroma on your laptop; switch to a managed or self-hosted DB only when one machine is no longer enough.

---

## Q3. How many chunks should I put in the context, and how big should each chunk be? [→ Real-World Case Studies]

**What you see**

You paste the whole knowledge base "to be safe" and the token bill explodes. Or you chunk tiny and answers lose their thread. (A "chunk" = one cut piece of a document that gets stored and retrieved.)

**Why**

The whole point of retrieval is to hand the model **only the most relevant pages**. The roadmap's project-knowledge case uses 500–1000 tokens per chunk with overlap (overlap = neighboring chunks share a few lines, so a sentence is never cut in half), and the tool default `top_k` is 5. (`top_k` = how many chunks to retrieve per search.)

**What to do**

1. Chunk at 500–1000 tokens with overlap so a sentence is never cut in half.
2. Start with `top_k=5`, then try 3 — if accuracy holds, keep 3 and pay less.
3. Use metadata filters to narrow the search space before ranking.

> 📄 **Example code:** [`examples/02-q3-how-many-chunks-should-i-put-in.py`](examples/02-q3-how-many-chunks-should-i-put-in.py)

**Verify**

Compare answer quality at top-3 and top-5. If quality is flat, keep the smaller number. If answers get vague, your chunks are too small or missing overlap — not too few.

> **One-line summary:** 500–1000 tokens per chunk with overlap, and start with `top_k=5` — shrink it only when quality holds.

---

## Q4. Where do I register this as a tool, and how do callers use it? [→ Relationship to the Harness]

**What you see**

Retrieval works in your notebook, but the agent cannot reach it. You are unsure whether it is a tool, a memory store, or something else.

**Why**

Retrieval has two faces. It is the main component in `harness/01-retrieve-memory-knowledge`, and it also appears as the `vector_search` tool in the registry (`harness/06` — the component that decides which tool to use). The same collection is written by `harness/03-update-memory-store` and read into context by `harness/02-build-context`.

**What to do**

1. Register `vector_search` once, with `query`, `top_k` (default 5), `collection` and `filters` as parameters.
2. Tag it `semantic`, `vector`, `embedding` so routing can find it.
3. Keep writes in `harness/03` and context assembly in `harness/02` — the tool only searches.

> 📄 **Example code:** [`examples/03-q4-where-do-i-register-this-as-a.py`](examples/03-q4-where-do-i-register-this-as-a.py)

**Verify**

The agent can call `vector_search` by name and receives the same chunks your notebook returned for the same query. A run with no `top_k` uses 5.

> **One-line summary:** Register it once as a `vector_search` tool in the registry — writes stay in harness/03, context assembly in harness/02, and the tool only searches.

---

## Q5. What are the memory tiers and why does my collection say `tier: warm`? [→ Real-World Case Studies]

**What you see**

Your upsert metadata has `"tier": "warm"`, and the source file comments point at `HARNESS_ENGINEERING.md` line 1954 with no explanation of the tiers.

**Why**

Memory is split by cost and speed. Cold, Warm and Hot are three different stores, and the vector database is only the middle one.

How to read this table: each row is one memory tier, where it physically lives, and how it is reached. For instance, **Hot** = facts already sitting in the context window (no search needed); **Warm** = the vector store, reached by a semantic (meaning-based) query.

| Tier | Store | Retrieved by |
|---|---|---|
| Cold | system files | not embedded, no search |
| Warm | Chroma vector store | semantic query |
| Hot | context window | always present |

**What to do**

1. Put durable reference material in Warm and search it by meaning.
2. Keep the currently relevant facts in Hot so the model always sees them.
3. Do not embed everything — Cold stays as files because it is rarely needed.

**Verify**

A Warm query returns a chunk that is *not* in the context window, proving it was retrieved by the vector store rather than already sitting in the prompt.

> **One-line summary:** Cold = files on disk, Warm = the vector store you search by meaning, Hot = what is already in the prompt — your collection is the Warm middle tier.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
