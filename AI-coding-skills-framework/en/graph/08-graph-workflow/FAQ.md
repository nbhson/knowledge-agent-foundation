# ❓ FAQ — Graph Workflow (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. One new document arrives and my ingest pipeline takes two hours and costs $100 — why? [→ §2 Incremental Updates]

**What you see**

Monday: 50 new documents land in `data/raw_docs/`. Your scheduled job wakes up, sends all 10,000 documents through the LLM extraction step again, and takes ~2 hours and ~$100 in API calls to produce a graph that is 99% identical to yesterday's.

**Why**

Full rebuild treats every document as if it had never been seen. The arithmetic in the source is blunt: 10K docs × 2 LLM calls per doc × $0.005/1K tokens ≈ $100 + 2 hours for a no-op change, versus 1 doc × 2 calls ≈ **$0.01 and 5 seconds** when you process only what is new.

This is not a rare edge case. The Neo4j Production Survey (2024) attributes **68% of graph incidents to the absence of an incremental pipeline** — full rebuilds cause downtime, and downtime is the incident. Microsoft GraphRAG reports the same effect from the cost side: incremental indexing cuts re-indexing cost by **90%** when adding documents.

**What to do**

1. Pick the mode first — do not use one pipeline for everything.

| Mode | Volume per run | Use for |
|---|---|---|
| Batch | 100–10K docs | initial load, nightly job |
| Micro-batch | 10–100 docs | hourly incremental (the default) |
| Streaming | 1 doc / event | user uploads, webhooks |

```
Batch      : 100–10K docs   → initial load, nightly job
Micro-batch: 10–100 docs    → hourly incremental   ← default choice
Streaming  : 1 doc / event  → user edits, API webhooks
```

2. Keep a state file (e.g. `STATE.md`) of what has already been ingested, and feed only unseen files to `add_document()`. The daily-triage loop pattern in the source does exactly this: compare the file list against state, call the incremental updater per new file.
3. Re-run expensive derived work only when it is actually stale — the source rule is "re-run community detection if >100 new nodes". Re-clustering 10,000 nodes because 12 arrived is the same mistake at a smaller scale.
4. Tag every write with its source document (`source_doc`) so a later delete or rollback can find exactly the nodes that document created.

**Verify**

Run Lab 2 from the source: ingest 1,000 docs by batch, record time and cost; then add 10 docs and compare (a) incremental — only the 10 — against (b) full rebuild — 1,010 docs. The incremental run should show roughly two orders of magnitude less time and cost. A useful regression guard: assert that a run over zero new files completes and issues **zero** LLM calls.

---

## Q2. I re-ran yesterday's ingest and now the graph has twice as many entities and doubled edges — what went wrong? [→ §1 Graph ETL Pipeline]

**What you see**

A retry, a manual re-run, or an overlapping schedule runs the same 200 documents twice. Afterwards your node count doubled, relations that should appear once appear twice, and any question about counts ("how many companies do we know?") returns a number that is quietly wrong. Nothing errored — the pipeline reported success both times.

**Why**

The load step used `CREATE`/`INSERT` instead of `MERGE`. Spreadsheet habits die hard: an `INSERT` always makes a new row, so the pipeline is **not idempotent** — running it 100 times gives 100 copies. The source states the requirement plainly: graph ETL load must be idempotent, and dedup plus validation are mandatory before the write, because LLM extraction is never 100% correct.

A second, sneakier cause: dedup that only compares entities *within the current batch*. A batch of 200 documents has no idea that "Alice" from last week already exists in the graph. The dedup check must run **against the existing graph**, not just inside the incoming payload.

**What to do**

1. Make the write idempotent at the database level, not in application logic.

```cypher
-- Wrong: every run creates a new node
CREATE (e:Entity {name: $name}) SET e += $props
-- Right: match-or-create, then update in place
MERGE (e:Entity {name: $name}) SET e += $props, e.source_doc = $doc_id
```

2. Before writing, run three gates in order: **dedup** (normalize names — "NV A" and "Nguyen Van A" are one person), **validate** (reject nonsense like `Person -[WORKS_ON]-> Person`), then load.
3. On ingest of a new document, check existence per entity: new → upsert, already present → update properties only, never insert a second copy.
4. Store `source_doc` on every node and relation. It is what makes a later correction or a document-level delete possible at all.
5. Choose a delete policy deliberately: **soft delete** marks `deleted = true` (recoverable, keeps history) versus hard delete with `DETACH DELETE` (permanent, removes the nodes and their edges).

**Verify**

Load the same document batch twice in a row and assert the graph is byte-identical: same node count, same edge count, no duplicated relations. Then check the audit log for that run — it should show `UPSERT`/`UPDATE` operations, not a second wave of `CREATE_NODE`. A non-zero dedup rate on a re-run of identical data is a bug signal, not normal behaviour.

---

## Q3. We found 200 duplicate entities — how do I merge them without breaking every relation that touches them? [→ §2 Incremental Updates]

**What you see**

A dedup pass reports 200 duplicate entity clusters: "Alice" / "Alice Nguyen" / "Alice N.", "Acme Corp" / "Acme Corporation". Merging is easy for the node; the mess is the edges. Delete the duplicate and every relation pointing at it silently disappears — and relations are the actual knowledge in a graph.

**Why**

`merge_entities()` is not a node operation; it is an **edge migration** operation. Each incoming edge and each outgoing edge of the duplicate must be recreated on the canonical node *before* the duplicate is removed. In NetworkX (the in-memory graph library used in the source examples) that means copying `successors` and `predecessors` with their edge data (`get_edge_data`), then `remove_node(dup_name)`.

**What to do**

1. Pick one canonical name per cluster and treat it as the stable ID. Everything downstream — property updates, later merges, queries — should key off the canonical name, never the raw string.
2. In Neo4j, do it in one transaction: match duplicates and the canonical node, create replacement edges with the same type and properties, then delete the old relationship.

```cypher
MATCH (dup:Entity) WHERE dup.name IN $duplicates
MATCH (dup)-[r]->(other)
MATCH (c:Entity {name: $canonical})
CREATE (c)-[r2:RELATED {type: r.type}]->(other)
SET r2 = properties(r)
DELETE r
```

3. Also move **incoming** edges — the pattern above only shows `-[r]->`; reverse-direction edges need the mirrored query, and forgetting this is the most common merge bug.
4. Run the merge inside a workflow stage with `checkpoint=True`, so a crash halfway through 200 clusters is recoverable instead of leaving you with a half-merged graph.
5. Log each merge as a `MERGE` event with an `actor` such as `pipeline:etl` or `user:alice`, so you can later answer "who decided these two were the same person?"

**Verify**

For one cluster, count edges before and after: `sum(degree)` over the cluster must be unchanged (or changed only by the de-duplication of genuinely parallel edges). Pick three relations that touched a duplicate and query them after the merge — they must still resolve. Add a check that no entity name exists twice under different casing or whitespace, and keep it in CI, because duplicates come back the moment extraction runs again.

---

## Q4. A batch ingest died at 70% and I have no idea what state the graph is in — how do I roll back? [→ §6 Implementing a Complete Workflow Engine]

**What you see**

The job fails partway through — an API timeout during extraction, a validation error, a Neo4j connection drop. The log shows `❌ validate: ...`, and then nothing. You cannot tell which nodes were written, whether the ones already written are correct, or where a re-run would resume. The naive fix — re-run the whole batch — re-introduces Q2.

**Why**

Without a checkpoint, "rollback" is a manual reconstruction job. The source measurement is unambiguous: workflows with checkpoints reduce **recovery time by 80%** when a batch ingest fails (Prefect + Graph Benchmark, 2025). Recovery cost, not ingest cost, is what makes an un-checkpointed pipeline dangerous at 10K-doc scale.

**What to do**

1. Declare, per stage, three things up front: whether it is a **checkpoint** stage, what happens on error (`fail` / `skip` / `retry`), and a timeout. The engine defaults are `on_error="fail"` and `timeout_s=300`.

```python
engine.add_stage("extract",  extract_stage,  checkpoint=True)
engine.add_stage("validate", validate_stage, on_error="fail", timeout_s=300)
engine.add_stage("load",     load_stage,     checkpoint=True)
# on fail → status "rolled_back" to nearest checkpoint, else "failed"
```

2. Log **every** stage transition to the audit log as a `GraphEvent` with `action`, `payload`, `actor`, and `prev_state`. `prev_state` is what makes rollback an operation rather than an archaeology exercise.
3. Add retries *around* the flaky layer only: `@task(retries=3, retry_delay_seconds=10)` in Prefect, or `retry_with_backoff(max_attempts=3, backoff_factor=2.0)` locally — which waits 2s, then 4s.
4. Put a circuit breaker in front of the LLM call so a dead API key does not burn 200 documents' worth of retries: `CircuitBreaker(failure_threshold=5, reset_timeout=60)` opens the circuit after 5 consecutive failures and fails fast for 60 seconds.
5. On error, escalate to a human instead of looping forever — the daily-triage loop in the source ends with "on error → escalate".

**Verify**

Lab 1 is the drill: force `validate` to fail on a 100-document batch and confirm the run ends with status `rolled_back` pointing at the last checkpoint stage, then confirm the graph matches the pre-run state. Also assert the run's final status is never `success` while `error_count > 0` — a pipeline that fails silently and reports success is the worst outcome, worse than a hard failure.

---

## Q5. I deleted the old edges to keep the graph small, and now I cannot answer "who managed TeamA in February 2024?" [→ §3 Versioning & Temporal Graphs]

**What you see**

Someone cleans up stale relations to reduce node/edge count. Six months later a question arrives that the graph can no longer answer: what did the org look like in Q1 2024? Which contract was active when this decision was made? The information existed once and was overwritten with a hard delete.

**Why**

A graph without history is a **snapshot**, not a system. The source proposes a two-layer fix, and both layers are needed:

- **Temporal properties** — every edge carries `valid_from` / `valid_until`, so a relation has an *effective period*. A query at a past date only considers edges active on that date.
- **Audit trail (event sourcing)** — every change is appended as an event (`CREATE_NODE`, `CREATE_EDGE`, `UPDATE`, `DELETE`, `MERGE`). There is no "delete forever", only "append a DELETE event", so **rollback stays possible**.

**What to do**

1. Stop hard-deleting edges. Set an end date instead.

```python
e = {"type": "MANAGES", "from": "Alice", "to": "TeamA",
     "valid_from": date(2023, 1, 1), "valid_until": date(2024, 6, 30)}
# valid_until = None means "still active"
active = [e for e in edges if e["valid_from"] <= q <= (e["valid_until"] or date(9999, 12, 31))]
```

2. Query by date, not by assumption. Wrap "current state" and "state at date T" behind one function so callers stop asking the ambiguous question.
3. Append events, never rewrite history. Store `actor` on each one (`user:alice`, `pipeline:etl`, `loop:daily-triage`) so you can audit *who* changed a fact, not just what changed.
4. Keep the delete path itself append-only: a document removal writes a DELETE event plus soft-delete flags, so a mistaken ingest is reversible for as long as you retain the log.
5. Route it through the workflow engine so history is a by-product of running the pipeline — not a separate project someone forgets.

**Verify**

Pick three historical questions ("who managed TeamA on 2024-02-01?", "was Acme an active customer in 2023?", "what changed in Q1 2024?") and assert each returns a non-empty answer in a test. Then take a known bad change from last week, roll it back from the audit log by event id, and confirm the graph returns to its previous state — recovery time should be measured, since the checkpoint-plus-history path is what the 80% figure refers to.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*