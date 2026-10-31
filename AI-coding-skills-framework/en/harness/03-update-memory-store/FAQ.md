# ❓ FAQ — Update Memory & Knowledge Store (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets). The memory store = where the agent keeps facts it learned; write-back = saving new knowledge into it.

---

## README.md

The first four questions come from `README.md` (keeping the store clean, fast, compliant, and reversible).

## Q1. The agent answered with last year's number — "health insurance contribution is 4.5%" when it has been 5% since 2025. Where do I start? [→ §2.1 What Is Consolidation?]

This section explains consolidation: merging and expiring stored facts so the current one wins.

**What you see**

Five facts about one topic sit in the store at the same time, and the agent answers with whichever one retrieval happens to rank first.

```
day 1   source A: "HI contribution 4.5%"
day 2   source B: "HI contribution 4.5% of base salary"
day 3   source C: "2024 HI rate is 4.5%"
day 5   source A: "HI contribution 4.5%"    ← exact duplicate
day 10  source D: "HI contribution 5% starting 2025"
```

Four of those five rows are the same fact said different ways, so the one correct 2025 value loses to the crowd of 2024 values. Left alone, vector search slows by 30–50% within 6 months, and the doc cites research saying a fact 6 months old has a 73% chance of being outdated.

**Why**

Write-back without consolidation is a one-way ratchet: the store only grows. Nothing merges duplicates, nothing expires old values, and nothing tells the retriever which of the contradicting rows is current.

**What to do**

1. Timestamp every fact at write time. Without a time on each row, "latest wins" is not a decision you can make.
2. Deduplicate before storing, using a similarity threshold of 0.85 — two texts scoring 0.85+ alike are treated as the same fact. This is the same number Mem0 (a memory library) and the consolidation pipeline both use.
3. Run consolidation on a trigger, not on a whim: `unconsolidated_writes > 500`, an hourly cron (a scheduled job), `conflict_rate > 5%`, or a negative rating on a fact.
4. Expire by memory class: session memory drops after 24h, episodic memory (records of specific events) archives after 30–90 days, semantic facts (general facts) have no time limit but must carry `valid_until` + `source`.
5. Never overwrite silently — keep both values and link them with a `supersedes` edge (a link saying "this fact replaces that one").

**Verify**

`generate_memory_report()` prints `Total triplets` (stored facts), `Communities`, and `Conflicts found`. After a run, those five rows must collapse to two, and `conflict_resolution()` must return an empty list for that subject. Alert when `conflict_rate > 5%`.

> **One-line summary:** Timestamp and dedupe every fact, consolidate on triggers, expire by memory class, and link superseded values instead of silently overwriting.

---

## Q2. Writes got slow — every fact save now blocks the reply. Can I make it fast again without losing data? [→ §7.1 Write-Behind Cache Pattern]

This section explains the write-behind cache: answer first, save in the background — and what that risks.

**What you see**

Write latency crosses the 300ms budget the doc sets as the p99 target (p99 = the 99th percentile: 99% of requests are faster than this). The user waits for the disk. The heavy part is not the read path — it is the fact write plus the duplicate check plus the embedding call.

**Why**

Every write goes straight to the durable store, serialized (one at a time, in order). The doc's own guidance is that consolidation must not run per write: batch processing is about 5x more efficient, and heavy merges belong off the critical path (away from the code the user is waiting on).

**What to do**

1. Write to a fast cache first and answer immediately; queue the entry for the durable store.
2. Flush in the background on a timer and on batch size — the reference uses `flush_interval=5.0` seconds and `batch_size=100`.
3. Mark entries `dirty` (in cache, not yet saved) until flushed, and **re-queue the whole batch at the front of the queue if the flush throws**. A silent drop here is invisible data loss.
4. On read, check the cache, then fall back to the store and populate the cache for next time.

```
write()  → cache[key] = entry (dirty=True)
          pending_writes.append(entry)
          if len(pending_writes) >= 100: _flush()
_flush() → persistent_store.batch_write(batch); mark clean
          on exception: pending_writes = batch + pending_writes
```

5. Acknowledge the caller only after the write-ahead log (WAL — a journal written before the real save, so a crash can be recovered) **and** the primary store both accepted the write, and carry an idempotency key `tenant:doc_hash` (a unique key so a retry cannot double-write).

**Accept the trade honestly**: this pattern knowingly risks losing the last few seconds of writes if the process crashes. That is the price of the speed.

**Verify**

`get_stats()` returns `cache_size`, `pending_writes`, `dirty_entries`. Watch the write SLO dashboard (SLO = the service quality target): `p50 < 80ms`, `p99 < 300ms`, async consolidation `p99 < 5min`, and alert on `write_error% > 1%` or `queue_lag > 10k`. Force a flush failure and confirm nothing was lost.

> **One-line summary:** Answer from a fast cache, flush to the durable store in background batches, and re-queue failed flushes — knowingly trading a few seconds of write durability for speed.

---

## Q3. A user asked to be deleted, but their text is still in the vector index. Am I done? [→ §12.2 Retention / Compliance]

This section explains why "delete" must mean every copy — table, vector index, graph, logs, backups.

**What you see**

`DELETE /memory?user=X` removed the rows from the main store. Search still returns their sentences, because the same text was embedded into the vector index, written into the knowledge graph, and pasted into logs during debugging.

**Why**

Memory is not one store. "Deleted" only means deleted from the table you remembered to touch. Until the vector index, the graph triplets, and the log copies are purged too, the data is still readable — and still personal data.

**What to do**

1. Run the full purge in order: tombstone (a marker saying "this is deleted") → purge vector index + knowledge graph + logs (redact — replace with `[REDACTED]`, do not just delete the line) → vacuum backups (rebuild them without the data) → return a receipt.
2. Return a machine-checkable receipt: `deletion_receipt{id, scope, ts}` (what was deleted, where, when), and meet the 24-hour service level.
3. Partition everything by `tenant_id`. A cross-tenant read must be rejected at both the API and the database policy level (row-level security — each row carries its owner and the DB enforces it), and each enterprise tenant gets its own encryption key.
4. Set time limits per memory class and sweep hourly: `session: 24h → drop`, `episodic: 30–90d → archive`, `semantic fact: no TTL but needs valid_until + source`, `user profile: until delete request`.
5. Archive to cold storage (cheap, rarely-accessed storage) **before** hard delete, so a purge is still reversible until the retention window closes.

```text
DELETE /memory?user=X
  → tombstone → purge vector + KG + logs (redact)
  → vacuum backups ≤30d
  → { deletion_receipt{id, scope, ts} }   SLA 24h
```

**Verify**

After the delete, search for the user's known sentences and expect zero hits in the store, the vector index, and the log search. Confirm the receipt is recorded. Re-run the same check against a backup restore.

> **One-line summary:** A delete request is not done until the vector index, graph, logs, and backups are purged too — and you return a receipt proving it within 24 hours.

---

## Q4. I updated one fact and now the old value is gone forever. How do I undo a bad write-back? [→ §7.3 Versioned Memory (Git-like Memory)]

This section explains versioned memory: keep every past state so any write can be undone.

**What you see**

`update_knowledge("health insurance", "contribution rate", "4.5%", "5%")` ran during a session. Two days later a user proves 5% was wrong for their case. There is no "before" to go back to — only the change log entry, which records the shape of the change but not a restorable snapshot (a full saved copy of the state at that moment).

**Why**

Overwriting without versioning is listed as a flat anti-pattern. A memory store that only keeps the present cannot answer "when did this change?", "who changed it?", or "what was true last Tuesday?" — which are exactly the questions an audit or a confused user asks.

**What to do**

1. Snapshot the whole state on every change and chain versions with a `parent` link — the `VersionedMemory.set()` pattern. Three writes of `hi_rate` ("4.5%" → "4.5% of base salary" → "4.5% MEC 2024") give you three restorable versions.
2. Use `diff(v1, v2)` to see exactly what changed between two versions; it returns a `changes` list with `added` / `removed` / `modified` per key.
3. Use `rollback(version_id)` to restore a snapshot as the live state.
4. Keep the event log as the source of truth and derive current state by replaying it: `record_event` appends, then `_apply_event` updates state. `get_state_at(event_id)` answers "what did memory look like at event 412?" and `undo_last()` rebuilds state from the remaining events.

> 📄 **Example code:** [`examples/01-q4-i-updated-one-fact-and-now-the.py`](examples/01-q4-i-updated-one-fact-and-now-the.py)

**Verify**

After `rollback(0)`, `get()` returns the original value and the change history is still intact. If rolling back destroys history, the versioning is fake — fix that before shipping.

> **One-line summary:** Snapshot the state on every write and chain versions — rollback must restore values *without* destroying history.

---

## trajectory-fork-replay.md

The last four questions come from `trajectory-fork-replay.md` (making agent runs replayable, branchable, and crash-safe).

## Q5. The agent failed at step 15 and I cannot tell which step caused it — a bad prompt, a flaky tool, or bad reasoning? [→ §4.1 Replay (Replaying a Trajectory)]

This section explains replay: rebuilding the exact agent state at any past step to find the failure.

**What you see**

A session that took dozens of turns and hundreds of tool calls ends with a wrong result. Your only artifact is a chat log of user and assistant messages. The tool calls, the injected system context, and the errors that were swallowed are simply not there, so you cannot tell whether the agent searched the wrong directory or the search tool returned garbage.

**Why**

A conversation stored as a flat list of `{role, content}` messages is not a trajectory (the full event record of a run). The doc names this as *incomplete logging* — the single most common reason a bug cannot be reproduced.

**What to do**

1. Store the run as an **append-only event stream** (events can be added, never edited): every prompt, reasoning step, tool call, tool result, state change, and context injection gets its own event with a timestamp and a unique id.
2. Replay instead of guessing. `replayToStep(sessionId, targetEventId)` returns the exact slice; if the id is wrong it throws `Event ID <id> not found in session <id>`, which tells you immediately that you are looking at the wrong run.
3. Use **deterministic replay** to reproduce the original answers and tool results without calling the model or re-running commands — safe for anything with a side effect.
4. Use **live replay (dry-run)** deliberately: same history, newer model, compare the outputs. Treat divergence as drift (the new model behaving differently), not as a bug report.
5. Record the environment and parameters with every tool result. A stored result without its inputs cannot be replayed later.

**Verify**

Pick a random mid-session event and replay to it — the reconstructed state must match. Confirm the stream contains `context_assembly`, `tool_call`, `tool_result`, and `error` events, not just user and assistant messages.

> **One-line summary:** Log every run as an append-only event stream, then replay to any step instead of guessing which step failed.

---

## Q6. I forked a session at step 400 and my 10,000-event log became 20,000 events — and something got sequence number 0 twice [→ §4.2 Fork (Branching a Session)]

This section explains how forking should work: branch from history, never copy it.

**What you see**

Storage roughly doubles after each fork (a fork = a new branch of the session sharing the earlier history, like a git branch). `findOrphans(sessionId)` starts reporting gaps. In the reference implementation the cause is a specific ordering bug: if you append the fork's `checkpoint` event *before* registering the copied prefix, `append()` mints `seq: 0` (sequence number 0) — colliding with the first copied event.

**Why**

A fork is logically **not a copy**. The prefix (events 1→400) is immutable history: the fork branches *from* it rather than replacing or re-executing it. Physically re-keying every event is what turns 10,000 events into 20,000.

**What to do**

1. Register the prefix first, then append. The reference code does exactly this, and the comment says why: appending first would mint `seq 0` and collide with the first copied event — precisely what `findOrphans()` would flag.
2. Record the fork as a `checkpoint` event carrying `forkedFrom: { sessionId, atSeq, by }`, not as an implicit copy of history.
3. In production, share the prefix by reference or with a parent-chain pointer instead of materializing it (that dedup rule lives in `13-trajectory-observability` §2.2). The copy in this file is illustrative.
4. Register a `checkpoint` event after each real milestone — end of planning, end of refactoring — so forking is cheap and the fork point is meaningful.
5. Set `actor` (e.g. `"human:ui"`) on every event you write. A `tool_call` with no `actor` is unattributable, and an audit cannot repair that after the fact.

**Verify**

`findOrphans(sessionId)` returns `[]` for both parent and fork. Forking a 10,000-event session adds a handful of events, not 10,000. Each fork contains exactly one `checkpoint` event with `forkedFrom`.

> **One-line summary:** A fork branches from shared history — register the prefix first, record one `checkpoint` with `forkedFrom`, and never physically copy 10,000 events.

---

## Q7. I resumed after a crash and it sent the customer email again — how do I make resume safe? [→ §4.3 Resume (Continuing a Work Session)]

This section explains crash-safe resume: how to skip steps that already had real-world effects.

**What you see**

The process died mid-task. On restart the agent picked up from the last event and re-executed a step that had already committed: a second email, a duplicate database row, a second charge. From the event stream alone, "already done" and "was interrupted before finishing" look identical.

**Why**

Resume rebuilds state by replaying events, but replay alone cannot know whether a side effect (an effect outside the agent: email sent, DB row written, money charged) landed. Without a recorded completion record and a stable idempotency key, every resume is a small chance of doing the irreversible thing twice.

**What to do**

1. Load the last `checkpoint`, then tail only the events written after the crash.
2. Derive the set of already-completed steps — `stepsToSkip()` — instead of guessing from timestamps.
3. Require an idempotency key (`07-workflow` §13.3) for anything with a side effect: the same key must collapse a retry into a no-op (an operation that does nothing).
4. Let `08-task` §11 reconcile task state after the skip, so the plan graph and the event stream agree.
5. Never edit recorded events. To roll back, fork the session or append a compensating event of a canonical kind: `plan_revision` for a plan change, `compaction` for a context-window reduction. `state_change` is a legacy name — do not write it.
6. Keep oversized payloads out of RAM/DB: a 10,000-line log becomes a compact payload plus a reference to a blob file. The contract caps inline payloads at 64KB and requires `{ ref }` beyond that.

**Verify**

Crash the run right after the email step, resume, and confirm exactly one email exists. Run the same drill on a `tool_call` with a recorded `fingerprint`. Assert every event has `actor` and `parentTaskId` — an event without `parentTaskId` is an orphan, invisible to every cross-module query in `13` §4.1.

> **One-line summary:** On resume, skip already-completed steps using checkpoints and idempotency keys — a retried side effect must collapse into a no-op, never run twice.

---

## Q8. My old store still writes `type` / `timestamp` / `parentId`, and the new queries return nothing. Rename or rewrite? [→ §3 Session Event Stream Architecture]

This section is a migration map from the legacy event schema to the canonical one — with one field you must not just rename.

**What you see**

Queries written against the canonical contract come back empty, and cross-module joins fail. Your store has records with `type: "user_prompt"`, a `timestamp` field, a `parentId`, and a single `metadata.tokensUsed: number`. Six fields and kinds changed, and one of them cannot be fixed by renaming.

**Why**

Two live schemas in one store is how orphan events and un-joinable audits start. `13-trajectory-observability` is the contract; where this file disagrees with it, `13` wins.

**What to do**

1. Map the legacy names onto the canonical ones, then **delete the legacy path** after a single backfill run.

How to read it: column 1 is the old field/kind name; column 2 is the new canonical one; column 3 says what the move involves. For instance, `user_prompt` becomes kind `prompt` with `actor: "human:*"` — a rename. But `parentId` → `parentTaskId` is **not** a rename; the two point at different things.

| Legacy (this engine) | Canonical (`13` contract) | Note |
|---|---|---|
| `user_prompt` | `prompt` + `actor: "human:*"` | rename kind |
| `system_injection` | `context_assembly` | rename kind |
| `agent_reasoning` | `message` + `actor: "agent:*"` | reasoning is a message |
| `state_change` | `plan` / `plan_revision` / `compaction` | one kind → three; split by payload |
| `parentId` (previous event) | `parentTaskId` (plan node) | **recompute, do not rename** |

2. `parentId` is the trap: it pointed at the *previous event in the stream*, while `parentTaskId` points at the *plan node* (a step in the plan). Derive it from the plan graph, or every cross-module query silently returns nothing.
3. Split `metadata.tokensUsed: number` into `tokens: { in, out }`. When the split is unknown, put the whole value in `in` rather than discarding it.
4. Rename `timestamp` → `ts` and `type` → `kind`. Backfill the rest: `seq` by position, `actor` by source, and `model` / `costUsd` / `fingerprint` nullable.

**Verify**

After migration, `findOrphans(sessionId)` returns `[]` and every event carries `seq`, `actor`, and `parentTaskId`. Run one known production query from `13` §6.1 and confirm it returns rows. Grep the codebase for `parentId` and `state_change` — zero hits.

> **One-line summary:** Backfill once from the legacy schema to the canonical one, recompute `parentTaskId` from the plan graph (never rename it), then delete the legacy path.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md, trajectory-fork-replay.md.*
