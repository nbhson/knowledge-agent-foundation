# ❓ FAQ — GraphRAG (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. Our indexing bill jumped from $0.05 to $5.55 on the same 1,000 documents — did we build something wrong? [→ §1, §7]

**What you see**

Same corpus, same 1,000 documents (~500K tokens). Vanilla RAG index: `500K × $0.0001/1K = $0.05`. GraphRAG index: entity extraction `500K × $0.005/1K × 2 gleanings = $5.00`, community summaries `50 communities × 2K tokens × $0.005/1K = $0.50`, embeddings `$0.05` → **$5.55 total, 111× more expensive**. Nothing crashed, no error was logged. The bill just arrived.

**Why**

The graph index is not built by reading text — it is built by *paying a model to read it, twice*. "Gleaning" is the second extraction pass where the model is asked what it missed on the first pass. Then every detected community gets its own LLM summary. That cost is paid once per corpus, offline — but if you re-run `index()` every night on unchanged documents, you pay it every night.

**What to do**

1. Treat indexing as a **build step with a cache**: run it once, store the graph, communities, and summaries. Re-index only when a document hash changes.
2. Extract and summarize with a local model (the reference code calls `gemma3:12b` on `http://localhost:11434` plus `nomic-embed-text`) — no per-token bill at all.
3. Cut the number of communities. Summaries are billed per community, so a graph split into 400 groups costs 8× more than one split into 50.
4. If cost still blocks you, switch variants: **LightRAG** (dual-level index, 10× faster, 1/3–1/4 the cost) or **HippoRAG2** (personalized PageRank, ~20× cheaper per answer). Both give up some global aggregation quality.

```python
rag.index(documents)          # ~$5.55 for 1,000 docs / 500K tokens — ONE TIME
save(graph, communities, summaries)   # cache; queries never re-pay this
```

**Verify**

Your index job logs "skipped, 0 documents changed" on re-runs. Compare actual spend against the `$5.55` estimate line by line — extraction vs summaries vs embeddings. Query cost should *drop* versus vanilla RAG, because a 2K-token community summary replaces 20 raw chunks in the prompt.

---

## Q2. I asked "What are the AI trends of 2024?" and got five disconnected sentences — which search mode am I supposed to use? [→ §3, §8]

**What you see**

Vanilla RAG returns the top-5 most similar chunks; each one covers a different aspect and none of them combine. Switch to GraphRAG and you have to choose: local search finds **no matching nodes**, because a general question names no entity to start from. Global search answers it, and the evaluation says it wins **70%** of the time against vanilla RAG (LLM judge), with **+35% comprehensiveness** and **+30% diversity**.

**Why**

The two modes answer different shapes of question. **Local search is entity-centric**: extract entities from the query (`["Phoenix", "contract"]`), find them in the graph, walk 1–2 hops, rerank with a cross-encoder. It produces a proof path like `Phoenix —[BELONGS_TO]→ Contract C-2024 —[APPROVED_BY]→ Alice (confidence: 0.95)`. **Global search deliberately does not extract entities** — "the query is too general to map to a specific entity" — and instead map-reduces over all ~50 community summaries: one LLM call per community, then a second call to merge the answers.

**What to do**

1. Route by shape, not by keyword: names something concrete → Local; spans the whole corpus → Global.
2. Log the map step. The code prints `Map: 12/50 communities have information` — if only 2 of 50 respond, your summaries are off-topic or too thin.
3. For hybrid questions, run Global first, then Local on the entities the Global answer surfaced. That is where the good evidence paths come from.
4. Keep the community id on every claim so a reviewer can open that summary and check it.

```python
def route(q):                        # q = the user's question
    if has_named_entity(q): return local_search(q, max_hops=2)
    return global_search(q)          # map-reduce over community summaries
```

**Verify**

Judge 10 real questions by hand, vanilla vs GraphRAG, and log which mode wins each one. Expect local to win factoid/multi-hop and global to win themes and comparisons. If global wins nothing, check the map-step ratio first.

---

## Q3. `detect_communities()` gave me 400 communities of 3 nodes each — is that a bug, and what is `resolution`? [→ §4.1, §4.3]

**What you see**

The log prints `Detected 400 communities` where every one holds three nodes — or, at the other extreme, `Community 0: 1800 nodes`. Global answers get vague or miss half the corpus. And here is the sneaky one: if `python-louvain` is not installed, the reference code silently falls back to NetworkX's `greedy_modularity_communities`. You think you are running Leiden (an improvement over the older Louvain algorithm); you are not.

**Why**

`resolution` is the granularity knob and nothing else. Low (`0.5`) → fewer, larger communities. High (`2.0`) → many small ones. Default `1.0`. Communities exist so you can summarize a *group* instead of walking millions of nodes, so a group of 3 nodes means the summarizer is doing useless work, and a group of 1,800 means the summary describes nothing in particular.

**What to do**

1. Print the size distribution **before** you call the summarizer. Sanity band: most communities between 10 and 200 nodes.
2. Run the tuning lab — same corpus at `resolution` 0.5, 1.0, 2.0 — and compare the global answers side by side. Pick by answer quality, not by count.
3. Make the fallback loud. A silent swap to a different algorithm invalidates every community id you cached.
4. Respect the token caps the summarizer uses: `members[:20]`, `relations[:20]`, `chunks[:5]` at 500 chars each. Bigger communities are silently truncated, so the summary is built from the first 20 members and the rest never appear.

```python
try:
    partition = community_louvain.best_partition(graph, resolution=1.0)  # Louvain
except ImportError:
    raise RuntimeError("python-louvain missing — greedy fallback is NOT Leiden")
```

**Verify**

Print `len(members)` per community and confirm ~90% fall inside 10–200. Re-run at resolution ±0.5 and check that the global answer barely changes — if it swings wildly, you are sitting on a knife edge, not a tuned setting.

---

## Q4. The model wrote a Cypher query, it ran, and returned zero rows — what now? [→ §6.2]

**What you see**

`Text2Cypher` handles questions like "Who manages the most projects?" The LLM translates the question into Cypher (the query language Neo4j speaks) and runs it. You get `[]`. Sometimes the label is wrong (`Person.employee_id` when the schema only has `name`), sometimes the relation direction is flipped, and occasionally it returns a *wrong but non-empty* answer, which is worse.

**Why**

Two separate mistakes. First, people dump the entire database schema into the prompt — token-hungry and confusing, so the model invents fields. Second, the result is accepted on the first try. Text2Cypher has two built-in repair loops that are easy to skip: **self-correction** (the query came back empty → rewrite the Cypher) and **schema refinement** (the query needs a field that does not exist → go ask for more metadata).

**What to do**

1. Inject only labels, attribute names, and two or three semantically important parent–child relations. Add one sample triple so the model sees the shape.
2. Never accept an empty result. Feed the error back and let it rewrite — that is the self-correction loop, and skipping it turns a typo into a support ticket.
3. Validate labels before execution: if the query mentions a label not in the schema, reject it.
4. Have a fallback retriever ready: `HybridRetriever` fuses vector search with full-text using **RRF** (Reciprocal Rank Fusion), which combines ranked lists without needing comparable scores.

```python
Nodes: Person(name,role), Project(name,budget)
Edges: Person-WORKS_ON->Project, Person-REPORTS_TO->Person
Sample: (Alice,REPORTS_TO,Bob) — Bob is Alice's manager
score = sum(1/(k + rank))   for k ≈ 60      # RRF fusion, no normalization
```

**Verify**

Track the empty-result rate per day; it should fall as self-correction is added. Check RRF actually rewards agreement: an item ranked #1 in vectors only (`≈1/61`) is beaten by one ranked #8 that appears in two lists (`1/68 + 1/68`).

---

## Q5. We have 50 internal docs and most questions are "what does section 5 say?" — is GraphRAG worth building at all? [→ §8, §7]

**What you see**

The 1,000-financial-report demo looks impressive, so someone asks for a knowledge graph. Then the log of real questions shows almost everything is single-hop: a section number, a name, a number in a table. Nobody is asking for themes.

**Why**

Three findings from the counter-evidence in the README. (1) On single-hop, factoid questions, **vanilla RAG beats GraphRAG** — the traversal cost buys you nothing. (2) Global community search can hallucinate: a summary does not contain the specific detail, so the model fills the gap and invents it. (3) Indexing cost is per document and very high, so 50 documents is the worst possible ratio of build cost to corpus size.

**What to do**

| Corpus size / question shape | Build what |
|---|---|
| < 100 docs, mostly factoid | vanilla RAG — it is enough |
| Multi-hop 2–4 hops ("who approved X, and who do they report to?") | Local GraphRAG |
| Themes and trends across hundreds of docs | Global GraphRAG |
| In between, cost-sensitive | LightRAG / HippoRAG2 |

Run the last two weeks of real questions through vanilla RAG first. Build a graph only for the ones it misses, and file those under "multi-hop" or "global" — that list *is* your justification, and it tells you which mode to buy.

**Verify**

You can name the specific question shapes that vanilla RAG failed on, and each one maps to a row of the table. If you cannot name any, do not build the index — you would be paying $5.55 to answer questions you already answer.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
