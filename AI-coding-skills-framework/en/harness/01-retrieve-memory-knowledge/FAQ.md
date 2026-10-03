# ❓ FAQ — Retrieve Memory & Knowledge (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Search ignores the exact word I typed — I paste an error code or a function name and get essays back [→ §4 Hybrid Search, §4.3 RRF]

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

Log both raw rankings for 20 real queries. The exact identifier must appear in the top 5 for every code/function-name query, and `precision@5` (how many of the 5 results are genuinely relevant) must beat the vector-only baseline. If a query returns nothing from keyword search at all, your corpus tokeniser is probably stripping punctuation.

---

## Q2. The retrieved chunk cuts a sentence in half, so the answer comes back wrong even though the document was indexed [→ §1.4 Chunking Strategies]

**What you see**

A 10-page policy PDF becomes 50 chunks. Someone asks for the contribution rate, and the chunk that got retrieved reads `"the rate is 4.5"` — the sentence was cut at character 500, right before `% of base salary`. The model cannot answer from half a sentence, and it either apologises or, worse, fills the gap with a made-up number.

**Why**

Chunking happens before embedding, so a bad cut becomes a permanent defect in the index. Fixed-size splitting is simple and predictable but ignores structure: it slices mid-sentence and mid-table. Semantic search cannot repair it — a truncated chunk is a truncated meaning.

| Strategy | Quality | Speed | Good for |
|---|---|---|---|
| Fixed-size (500 chars, overlap 50) | low | fastest | quick prototype |
| Recursive (paragraph → line → sentence → word) | medium | fast | general text |
| Semantic (split when meaning changes) | high | slow | complex documents |
| Document-aware (split on Markdown headers) | high | medium | structured docs |

**What to do**

Split on structure first, keep the overlap, and carry the section name as metadata so a retrieved chunk still knows where it came from.

```python
sections = re.split(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)
for section in sections:
    if re.match(r'^#{1,3}\s+', section):
        current_header = section.strip()      # the heading becomes metadata
    elif section.strip():
        for para in section.split('\n\n'):   # too big → split by paragraph
            chunks.append({"content": para.strip(),
                           "metadata": {"section": current_header}})
```

**Verify**

Pick 10 facts that sit in the middle of a paragraph, query each one, and read the retrieved chunk yourself. Every chunk must contain a whole sentence plus its heading. Re-index after changing the splitter — old chunks keep the old damage.

---

## Q3. The bot invents facts when the index has nothing useful — how do I make it admit "I don't know"? [→ §8.4 Failure & Observability, §2.4 RAG Evaluation]

**What you see**

`hits == 0`, or the best score is `0.18`, and the assistant still answers with three confident bullet points and a made-up policy number. Without grounding, hallucination rate sits at 15–27%; with good retrieval it drops to 2–5% (Google's 2020 RAG paper measured 27% → 3%). Retrieval only helps if you stop talking when retrieval failed.

**Why**

Most RAG code treats "zero results" and "one weak result" the same as "great results" — it hands whatever came back to the model and asks for an answer. There is no threshold and no refusal path.

**What to do**

Set a score floor, retry once with keyword search only, then abstain explicitly instead of inventing. Retrieval precision@10 above 85% is the threshold where this whole approach starts paying off.

```python
TOP_SCORE_FLOOR, TOP_K = 0.25, 5
hits = vector_search(q_emb, tenant_id)
top = max([h["score"] for h in hits], default=0.0)
if not hits or top < TOP_SCORE_FLOOR:
    hits = bm25_search(q, tenant_id)          # one retry, keyword only
if not hits:
    return {"answer": None, "abstain": True, "reason": "no grounding found"}
```

Log the fallback every time it fires, and watch four numbers on a dashboard: `hit_rate@k`, zero-hit percentage, low-score percentage, and latency at the 50th and 99th percentile.

**Verify**

Write 20 questions your corpus genuinely cannot answer. All 20 must abstain. Then 20 questions it can answer — abstaining on those is a retrieval bug, not humility. Also measure faithfulness: does every sentence in the answer trace back to a retrieved chunk?

---

## Q4. I upgraded the embedding model and search got quietly worse — and a full re-index of 1M documents is unaffordable [→ §8.1 Definitions, §8.2 Index Ops, §8.3 Security]

**What you see**

Two symptoms, one cause. First, after swapping `nomic-embed-text:v1` for `v2`, the same query returns worse documents with **no error message** — because old and new vectors sit in the same namespace and the cosine comparison is now meaningless. Mean top-1 score dropping by more than `0.08` is the alarm. Second, a full re-embed of 1M documents takes hours and real money. On the same write path, someone pastes a customer support log into the corpus and an API key ending in `sk-…` gets embedded and logged permanently.

**Why**

An embedding model is part of the index's meaning, like a key format. Nothing enforces that all vectors came from the same version, and nothing measures that a document actually changed before re-embedding it.

**What to do**

1. Stamp every vector with `doc_id`, `content_sha256`, `embed_version`.
2. On write: unchanged hash → skip; changed hash → delete old `chunk_ids`, embed, upsert.
3. On upgrade: pin `EMBED_MODEL="nomic-embed-text:v2"`, dual-write to `idx_v2`, shadow-compare hit-rate@5 for 7 days, then cut over. Roll back if hit-rate@5 regresses more than 5%.
4. Scrub personal data and secrets **before** embedding and before logging — email, phone, national ID, `sk-` keys become `[REDACTED:KEY]`.
5. Stamp `tenant_id` on every write and every query, plus a post-check that each hit belongs to that tenant.

```
if sha256(new_text) == row.content_sha256: return      # unchanged → skip
delete(row.chunk_ids); embed_and_upsert(new_text)      # changed   → replace
```

**Verify**

The nightly sweeper that re-embeds rows where `embed_version != CURRENT` must finish with zero rows. Search the vector store files for `sk-` and for a known email address — nothing should appear. Run a cross-tenant probe query nightly: a tenant ID must never return another tenant's chunk.

---

## Q5. The answer needs three documents joined together and vector search only ever finds one of them [→ §3 Knowledge Graph Retrieval, §3.4 Graph RAG]

**What you see**

The question is *"Which model runs on Ollama, and what else does Ollama support?"* The needed facts live in separate chunks: one says a model runs on Ollama, another lists Ollama's supported models. Vector search returns one chunk, the model answers half the question, and the user has to ask again. Same shape as *"health insurance for workers in Ho Chi Minh City"* — two hops from the entity you typed.

**Why**

A vector database stores every chunk as an independent island with no thread connecting it to its neighbours. Multi-hop questions — where you must follow A → B → C — are exactly what "closest vector" cannot express.

| | Vector search | Knowledge graph |
|---|---|---|
| Stores | text chunks | triplets `(subject, predicate, object)` |
| Finds by | embedding the query, nearest vector | walking relationships |
| Multi-hop | weak | strong |
| Build cost | low | high (a model must extract triplets) |

**What to do**

Extract triplets with a model pass offline, store them as `(gemma3:12b, runs_on, Ollama)`, then at query time pull entities out of the question and walk at most 2 hops — `max_hops=2` is the setting that makes "A relates to B, B relates to C" answerable. Rank by similarity to the query, break ties by shallower depth, then assemble the context.

```
for ent in query_entities(query):
    subgraph += kg.query_entity(ent, max_hops=2)
ranked = sorted(subgraph, key=lambda t: (-similarity(t, query), t.depth))
```

**Verify**

Take 10 multi-hop questions and run them twice: vector search only, then graph. The graph run must contain the full entity chain (`gemma3:12b → Ollama → qwen2.5-coder:14b`) in the context. Keep vector search for everything else — graphs are expensive to build, so add one only when your own logs show multi-hop questions failing.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md*