# ❓ FAQ — Retrieve Memory & Knowledge (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets). Retrieval = finding the right stored information before the model answers.

---

## Q1. Search ignores the exact word I typed — I paste an error code or a function name and get essays back [→ §4 Hybrid Search, §4.3 RRF]

This section explains why exact tokens vanish and how merging two search types fixes it.

**What you see**

A developer searches `ECONNRESET` in `pg_hba.conf`, or `getUserById`. Vector search returns three paragraphs about connection pooling and never the file that actually throws the error. The same thing happens with version numbers, product codes, and people's names — the meaning is close, the exact string is missing.

**Why**

A vector search compares meaning, not spelling. It is strong on "heart disease" ≈ "cardiovascular disease" and weak on exact tokens: error codes, numbers, identifiers, proper names. Keyword search (BM25, a scoring formula that rewards rare exact words) does the opposite — perfect on exact matches, blind to synonyms. Each one loses what the other is good at.

**What to do**

Run both searches, ask each for twice the results you need, then merge by rank — not by raw score, because the two scores are on different scales.

```
semantic = [r["document"] for r in vector_store.search(q_emb, top_k=top_k * 2)]
keyword  = [doc for doc, _ in bm25.search(query, top_k=top_k * 2)]
return reciprocal_rank_fusion([semantic, keyword], k=60)[:top_k]
```

Reciprocal Rank Fusion (RRF) ignores the scores and only uses positions: every list adds `1 / (60 + rank)` to each document. With `k = 60`, a document ranked 1st by semantic and 3rd by keyword scores `0.01639 + 0.01587 = 0.032`, which beats a document that only one method loved. A document that shows up in several lists wins — that is the behaviour you want.

**Verify**

Log both raw rankings for 20 real queries. The exact identifier must appear in the top 5 for every code/function-name query, and `precision@5` (how many of the 5 results are genuinely relevant) must beat the vector-only baseline. If a query returns nothing from keyword search at all, your corpus tokeniser (the code that splits text into words) is probably stripping punctuation.

> **One-line summary:** Run keyword and vector search together and merge by rank (RRF) — vector handles meaning, keywords handle exact codes, and the union covers both.

---

## Q2. The retrieved chunk cuts a sentence in half, so the answer comes back wrong even though the document was indexed [→ §1.4 Chunking Strategies]

This section explains how to split documents so no fact gets sliced in two.

**What you see**

A 10-page policy PDF becomes 50 chunks (pieces of text stored in the index). Someone asks for the contribution rate, and the chunk that got retrieved reads `"the rate is 4.5"` — the sentence was cut at character 500, right before `% of base salary`. The model cannot answer from half a sentence, and it either apologises or, worse, fills the gap with a made-up number.

**Why**

Chunking happens before embedding (turning text into numeric vectors for search), so a bad cut becomes a permanent defect in the index. Fixed-size splitting is simple and predictable but ignores structure: it slices mid-sentence and mid-table. Semantic search cannot repair it — a truncated chunk is a truncated meaning.

How to read it: column 1 names a splitting strategy; columns 2–3 trade quality against speed; column 4 says when to use it. For instance, "Recursive" splits on the largest unit that fits (paragraph first, then line, then sentence), so it rarely cuts mid-sentence and stays fast.

| Strategy | Quality | Speed | Good for |
|---|---|---|---|
| Fixed-size (500 chars, overlap 50) | low | fastest | quick prototype |
| Recursive (paragraph → line → sentence → word) | medium | fast | general text |
| Semantic (split when meaning changes) | high | slow | complex documents |
| Document-aware (split on Markdown headers) | high | medium | structured docs |

**What to do**

Split on structure first, keep the overlap (repeating a few characters across neighbouring chunks so sentences that straddle a cut are still intact somewhere), and carry the section name as metadata so a retrieved chunk still knows where it came from.

> 📄 **Example code:** [`examples/01-q2-the-retrieved-chunk-cuts-a-sentence-in.py`](examples/01-q2-the-retrieved-chunk-cuts-a-sentence-in.py)

**Verify**

Pick 10 facts that sit in the middle of a paragraph, query each one, and read the retrieved chunk yourself. Every chunk must contain a whole sentence plus its heading. Re-index after changing the splitter — old chunks keep the old damage.

> **One-line summary:** Split on structure (headers, paragraphs) with overlap and carry the section name — a chunk cut mid-sentence is permanently broken, and no search can fix it later.

---

## Q3. The bot invents facts when the index has nothing useful — how do I make it admit "I don't know"? [→ §8.4 Failure & Observability, §2.4 RAG Evaluation]

This section explains how to add an explicit "I don't know" path so silence beats invention.

**What you see**

`hits == 0` (nothing found), or the best score is `0.18` (a weak match), and the assistant still answers with three confident bullet points and a made-up policy number. Without grounding, hallucination rate sits at 15–27%; with good retrieval it drops to 2–5% (Google's 2020 RAG paper measured 27% → 3%). Retrieval only helps if you stop talking when retrieval failed.

**Why**

Most RAG code treats "zero results" and "one weak result" the same as "great results" — it hands whatever came back to the model and asks for an answer. There is no threshold and no refusal path.

**What to do**

Set a score floor (a minimum match score below which you refuse to answer), retry once with keyword search only, then abstain explicitly instead of inventing. Retrieval precision@10 above 85% is the threshold where this whole approach starts paying off.

> 📄 **Example code:** [`examples/02-q3-the-bot-invents-facts-when-the-index.py`](examples/02-q3-the-bot-invents-facts-when-the-index.py)

Log the fallback (the switch to plan B) every time it fires, and watch four numbers on a dashboard: `hit_rate@k` (share of queries finding anything), zero-hit percentage, low-score percentage, and latency at the 50th and 99th percentile.

**Verify**

Write 20 questions your corpus genuinely cannot answer. All 20 must abstain (refuse to answer). Then 20 questions it can answer — abstaining on those is a retrieval bug, not humility. Also measure faithfulness: does every sentence in the answer trace back to a retrieved chunk?

> **One-line summary:** Put a score floor and an explicit refusal path in the pipeline — the model must be allowed to say "I don't know" instead of inventing.

---

## Q4. I upgraded the embedding model and search got quietly worse — and a full re-index of 1M documents is unaffordable [→ §8.1 Definitions, §8.2 Index Ops, §8.3 Security]

This section covers three index-ops risks at once: silent model upgrades, expensive re-indexing, and secrets leaking into the index.

**What you see**

Two symptoms, one cause. First, after swapping `nomic-embed-text:v1` for `v2` (two versions of the embedding model — the model that turns text into vectors), the same query returns worse documents with **no error message** — because old and new vectors sit in the same namespace and the cosine comparison (the similarity maths) is now meaningless. Mean top-1 score dropping by more than `0.08` is the alarm. Second, a full re-embed of 1M documents takes hours and real money. On the same write path, someone pastes a customer support log into the corpus and an API key ending in `sk-…` gets embedded and logged permanently.

**Why**

An embedding model is part of the index's meaning, like a key format. Nothing enforces that all vectors came from the same version, and nothing measures that a document actually changed before re-embedding it.

**What to do**

1. Stamp every vector with `doc_id`, `content_sha256` (a fingerprint of the text), `embed_version` (which model made this vector).
2. On write: unchanged hash → skip; changed hash → delete old `chunk_ids`, embed, upsert (insert new or overwrite existing).
3. On upgrade: pin `EMBED_MODEL="nomic-embed-text:v2"`, dual-write to `idx_v2`, shadow-compare hit-rate@5 for 7 days (run both indexes in parallel and compare without switching users over), then cut over. Roll back if hit-rate@5 regresses more than 5%.
4. Scrub personal data and secrets **before** embedding and before logging — email, phone, national ID, `sk-` keys become `[REDACTED:KEY]`.
5. Stamp `tenant_id` (which customer the data belongs to) on every write and every query, plus a post-check that each hit belongs to that tenant.

```
if sha256(new_text) == row.content_sha256: return      # unchanged → skip
delete(row.chunk_ids); embed_and_upsert(new_text)      # changed   → replace
```

**Verify**

The nightly sweeper that re-embeds rows where `embed_version != CURRENT` must finish with zero rows. Search the vector store files for `sk-` and for a known email address — nothing should appear. Run a cross-tenant probe query nightly: a tenant ID must never return another tenant's chunk.

> **One-line summary:** Version-stamp every vector, skip writes whose content hash is unchanged, shadow-test model upgrades before cut-over, and scrub secrets before anything is embedded or logged.

---

## Q5. The answer needs three documents joined together and vector search only ever finds one of them [→ §3 Knowledge Graph Retrieval, §3.4 Graph RAG]

This section explains when to add a knowledge graph on top of vector search, and how much of one you actually need.

**What you see**

The question is *"Which model runs on Ollama, and what else does Ollama support?"* The needed facts live in separate chunks: one says a model runs on Ollama, another lists Ollama's supported models. Vector search returns one chunk, the model answers half the question, and the user has to ask again. Same shape as *"health insurance for workers in Ho Chi Minh City"* — two hops (two relationship steps) from the entity you typed.

**Why**

A vector database stores every chunk as an independent island with no thread connecting it to its neighbours. Multi-hop questions — where you must follow A → B → C — are exactly what "closest vector" cannot express.

How to read it: column 1 is the comparison point; columns 2–3 contrast the two stores. For instance, on multi-hop questions vector search is weak because chunks are not linked to each other.

| | Vector search | Knowledge graph |
|---|---|---|
| Stores | text chunks | triplets `(subject, predicate, object)` |
| Finds by | embedding the query, nearest vector | walking relationships |
| Multi-hop | weak | strong |
| Build cost | low | high (a model must extract triplets) |

A triplet is one stored fact in three parts, e.g. `(gemma3:12b, runs_on, Ollama)`.

**What to do**

Extract triplets with a model pass offline, store them as `(gemma3:12b, runs_on, Ollama)`, then at query time pull entities out of the question and walk at most 2 hops — `max_hops=2` is the setting that makes "A relates to B, B relates to C" answerable. Rank by similarity to the query, break ties by shallower depth, then assemble the context.

```
for ent in query_entities(query):
    subgraph += kg.query_entity(ent, max_hops=2)
ranked = sorted(subgraph, key=lambda t: (-similarity(t, query), t.depth))
```

**Verify**

Take 10 multi-hop questions and run them twice: vector search only, then graph. The graph run must contain the full entity chain (`gemma3:12b → Ollama → qwen2.5-coder:14b`) in the context. Keep vector search for everything else — graphs are expensive to build, so add one only when your own logs show multi-hop questions failing.

> **One-line summary:** When questions need facts joined across documents, extract triplets into a small graph and walk at most 2 hops — keep vector search for everything else.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md*
