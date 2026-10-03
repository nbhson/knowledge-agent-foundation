# ❓ FAQ — Build Context (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My search returns 10 good documents, I put all of them in the prompt — and the answer got *worse*. Why? [→ §1.2 Token Budget Allocation / §3.1 Why Compression Is Needed]

**What you see**

You built the obvious version: pull `top_k=100` documents from the vector store, glue on the **entire** chat history, and hand the result to the model. The prompt comes out at 100,000+ tokens. The model answers confidently, cites one document you never even retrieved, and ignores the document that actually answered the question. At $0.03 per 1K tokens, that single call costs about **$3**.

The numbers that explain it, straight from the source: 10 documents × 2,000 tokens each = **20,000 tokens** of raw context, against a budget of **8,000**. Twenty thousand does not fit into eight thousand. Something has to be cut, and if you did not choose what gets cut, the model chose by ignoring things.

**Why**

A context window is a fixed tray with a few slots. Without a written split, the longest component — usually chat history — eats the whole tray and the retrieved documents get whatever is left over. Anthropic's 2025 finding: a 200K window is not meant to be filled. Peak accuracy sits at **40–60% utilization**.

**What to do**

1. Reserve output space first. With `total_tokens=128000` and `reserve_output=4000`, only 124,000 remain for input.
2. Write down a percentage split before you retrieve anything, then enforce it in code.
3. Set a realistic `top_k` — 10, not 100 — and keep only the last 10 messages.
4. Compress to a stated ratio instead of truncating blindly. Compression ratio = compressed size ÷ original size; aim for 0.4 here.
5. Stop the loop when the budget is spent. Do not "just add one more doc".

```python
docs = vector_store.search(query, top_k=10)   # not 100
remaining = budget.available; parts = []
for doc in docs:
    t = estimate_tokens(doc)
    if t < remaining:
        parts.append(doc); remaining -= t
print(budget.report())   # retrieved_context 62,000 (50%)
```

**Verify**

Run `budget.report()` and confirm each bar matches your intent. Run the compression step and print `Original: N chars / Compressed: M chars / Ratio`. The ratio should land at 40%, and total input should sit between 40% and 60% of the window. Then check the bill: 100K → 50K tokens should halve the per-query cost from ~$3 to ~$1.5 while accuracy moves from 50–60% up to 75–85%.

---

## Q2. The one document that actually answers the question is in the prompt, and the model still says "not found in the provided documents." [→ §1.4 "Lost in the Middle" Problem]

**What you see**

You rank your 10 retrieved documents by relevance, then dump them in retrieval order. Document #7 is the one that answers the question. The model skips it, quotes document #2 instead, and finishes with "the context does not contain this information." This happens even though nothing was truncated and every token fit in the budget.

**Why**

Large language models attend most strongly to the **beginning and the end** of the context window, and least to the middle. Google's 2024 study measured the damage: accuracy falls **from 76% down to 20%** when the important information sits in the middle. Move the same information to the start or the end and accuracy climbs back to **80%+**. Your pipeline was fine; the ordering was not.

**What to do**

1. Stop using retrieval order as prompt order. Re-rank first.
2. Put the single most important document at the **beginning** and the second most important at the **end**.
3. Fill the middle with lower-value material, where mistakes cost least.
4. Repeat the key fact at a second strategic position instead of relying on one copy.
5. Use section labels (`[SYSTEM]`, `[CONTEXT]`, `[HISTORY]`) so attention has a shape to land on.

```python
docs = rank_by_relevance(all_docs)   # never random.shuffle(all_docs)
context = f"""
MOST IMPORTANT: {docs[0]}    ← beginning, high attention
{docs[1:-1]}                  ← middle, lower attention
MOST IMPORTANT: {docs[-1]}   ← end, high attention
"""
```

**Verify**

Build the same prompt twice — once in retrieval order, once in the edge-loaded order — and ask 20 held-out questions. Record how many times each version cites the correct document. If the middle-loaded version wins, your re-ranking is not actually ranking. You can also move one known-critical document to the very end alone and confirm accuracy jumps before you change anything else.

---

## Q3. The API bill tripled and nobody knows which change helped. Where do I cut first? [→ §11.2 Cost Optimization Strategies / §11.1 Context Quality Metrics]

**What you see**

A support assistant runs ~10,000 queries a day. Each query re-embeds the query, re-searches the vector store, re-summarizes the same 20 documents, and calls the most expensive model available — even when the user only asked a one-line factual question. Your cache hit rate is `0.0%` because nobody built one. Roughly 1,000 wasted extra tokens per query is about **$300 a month** thrown away, and the growth is linear: twice the queries, twice the bill.

**Why**

Context is the bulk of a retrieval-augmented generation (RAG) pipeline's cost, and each of the four cost drivers was left uncapped: no cache, no compression, no cheap first pass, one model for everything. The four strategies below cut **60–80% of total context cost** when combined, without losing quality.

**What to do**

1. **Cache similar queries** with a 5-minute time-to-live (TTL) — the value is how long an entry stays valid. Target hit rate 40–60%; 80% is achievable on repetitive workloads.
2. **Compress hard**: summarize conversation history after 10 turns, and use extractive summarization (picking sentences, no model call) for key facts. Target 60–80% size reduction.
3. **Retrieve in two passes**: cheap embedding model first, then run the expensive reranker on only the top 20.
4. **Route by tier**: simple questions to `gemma3:12b` (free locally via Ollama), complex questions to `claude-3.5`.

```python
metrics.record(query_type="factual", latency_ms=250, tokens=8500,
               relevance=[0.95, 0.88, 0.72], cache_hit=False,
               compression_ratio=0.4)
print(metrics.report())   # avg + P95 latency, avg/max tokens,
                         # avg relevance, hit_rate, query distribution
```

**Verify**

Read the metrics report every week, not just average latency — P95 (the 95th percentile, meaning 95% of requests are faster than this) is where users actually feel pain. Confirm cache hit rate climbs above 40% and compression ratio stays at or below 0.4. Call `health_check()`: a hit rate of exactly `0.0%` returns status `cold_start`, which tells you the cache is wired up but never used.

---

## Q4. At message 25 the chatbot forgets what we were talking about — "and the validity period?" means nothing to it. [→ §8.4 Multi-turn Context Management / §3.4 SmartContextManager]

**What you see**

You are 25 messages into a conversation about health insurance. The user asks "so what about the validity period?" and the model answers about something else entirely. Meanwhile you have two options and neither is good: keep the full history and blow the token budget, or keep only the last 10 messages and lose the topic the conversation started with.

**Why**

A long conversation does not fit a finite window, and a naive truncation throws away the *beginning* of the conversation — which is exactly where the topic was named. The reference implementation in the source (Claude Code's leaked context manager) compresses instead of truncating: when messages exceed 20, everything older than the last 10 becomes a summary, and decisions are kept separately.

**What to do**

1. Keep the last 10 messages verbatim — that is recent context.
2. Compress messages 1–20 into one summary once you pass the threshold (`summary_threshold=20`).
3. Extract **key facts** — decisions, figures, preferences — into their own small block and put them first, because they are both cheap and the most important.
4. Layer by priority: system → task → domain → history → immediate. When full, delete from the bottom up. Never delete the system layer.
5. Keep the immediate context (open file, cursor position, recent edits) — forgetting it is a listed mistake in the source.

```python
mgr = MultiTurnContextManager(max_turns=50, summary_threshold=20)
mgr.add_turn("user", "health insurance contribution?")
mgr.add_turn("assistant", "4.5% employee share")
mgr.add_turn("user", "and the validity period?")
prompt = mgr.build_context(max_tokens=4000)  # facts + summary + last 10
```

**Verify**

Run a 40-message scripted conversation. Assert that after each turn the built context contains the extracted key facts, contains the last 10 messages verbatim, and stays inside `max_tokens`. Then test the real sentence: ask "what is the validity period?" without naming the topic. If the model cannot answer, the key-facts block is missing something.

---

## Q5. I only found out my context was broken after paying for the model call. Can I check it first? [→ §10. Context Validation & Testing]

**What you see**

Your code builds a context, then calls the model. No checks. Once you scale up you hit two failure modes: an `OVERFLOW` error returned by the API after the request is already billed, and worse — a request that succeeds with 12 documents where 8 are irrelevant, so you get a confident, wrong answer and pay for both the input tokens and the output tokens.

**Why**

Validation was never a separate step, so every defect surfaced downstream, where the only diagnostic is the model's answer. The validator in the source runs five checks and reports a machine-readable issue list, so the pipeline can auto-fix before spending anything.

**What to do**

1. Validate the context *before* the model call, every time. Never trust it without checking.
2. Fail hard on `OVERFLOW` (token count above 128,000) and warn on `NEAR_OVERFLOW` (above 90% of budget).
3. Require the mandatory sections — `["system", "query"]` — and error on a missing one.
4. Warn when any document scores below `min_relevance_score = 0.5`, and when data is older than `max_context_age_hours = 24`.
5. Auto-fix instead of failing: overflow triggers hierarchical summarization, a missing system section gets a default header.

```python
result = validator.validate(context)   # 5 checks: budget, sections,
                                       # relevance, freshness, structure
if not result["valid"]:
    context = auto_fix(context, result["issues"])
response = llm.generate(context)
```

**Verify**

Put it in continuous integration / continuous delivery (CI/CD) so it runs on every code change. Keep these five assertions green: `test_context_fits_budget`, `test_context_includes_relevant_docs`, `test_context_budget_allocation` (usage between 10% and 90%), `test_context_with_large_query`, and `test_cache_hit`. Add one alert for sustained usage above 80% of budget — that is the early warning before the `OVERFLOW` error starts.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*