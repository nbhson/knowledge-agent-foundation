# 📈 Harness 13. Trajectory & Observability

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Is Trajectory Non-Optional?](#why-is-trajectory-non-optional)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. The TrajectoryEvent Contract](#1-the-trajectoryevent-contract)
>   - [1.1 Core Schema](#11-core-schema)
>   - [1.2 Event Kind Catalog](#12-event-kind-catalog)
>   - [1.3 Validation & Versioning](#13-validation--versioning)
> - [2. Session Event Stream Lifecycle](#2-session-event-stream-lifecycle)
>   - [2.1 The Shape of a Run](#21-the-shape-of-a-run)
>   - [2.2 Write Path — Durability Tiers](#22-write-path--durability-tiers)
>   - [2.3 Read Path & Live Tailing](#23-read-path--live-tailing)
> - [3. Fork, Replay, Resume](#3-fork-replay-resume)
>   - [3.1 Semantics of Each](#31-semantics-of-each)
>   - [3.2 Implementation](#32-implementation)
>   - [3.3 Replay Fidelity & Idempotency](#33-replay-fidelity--idempotency)
> - [4. Cross-Module Join Keys](#4-cross-module-join-keys)
>   - [4.1 The Join Table](#41-the-join-table)
>   - [4.2 Five Questions One Query Answers](#42-five-questions-one-query-answers)
>   - [4.3 Orphan Detection](#43-orphan-detection)
> - [5. Retention, Redaction & GDPR](#5-retention-redaction--gdpr)
>   - [5.1 Hot / Warm / Cold Tiers](#51-hot--warm--cold-tiers)
>   - [5.2 Redaction at Emit](#52-redaction-at-emit)
>   - [5.3 Tenant Isolation & Deletion Receipts](#53-tenant-isolation--deletion-receipts)
> - [6. Metrics for Free](#6-metrics-for-free)
>   - [6.1 The Query Catalog](#61-the-query-catalog)
>   - [6.2 Cost Attribution](#62-cost-attribution)
> - [7. Debugging Workflows](#7-debugging-workflows)
>   - [7.1 The Five Debug Questions](#71-the-five-debug-questions)
>   - [7.2 Diffing Two Runs](#72-diffing-two-runs)
>   - [7.3 Sampling Strategy](#73-sampling-strategy)
> - [8. TypeScript Implementation](#8-typescript-implementation)
>   - [8.1 TrajectoryStore](#81-trajectorystore)
>   - [8.2 Live Progress Projector](#82-live-progress-projector)
>   - [8.3 Debug Logger Adapter](#83-debug-logger-adapter)
> - [9. Testing Trajectory](#9-testing-trajectory)
>   - [9.1 Contract Tests](#91-contract-tests)
>   - [9.2 Replay Test Suite](#92-replay-test-suite)
> - [10. Real-World Case Studies](#10-real-world-case-studies)
>   - [10.1 SWE-bench Harness — Structured Trajectories](#101-swe-bench-harness--structured-trajectories)
>   - [10.2 LangSmith / Langfuse — Trace as Product](#102-langsmith--langfuse--trace-as-product)
>   - [10.3 OpenTelemetry GenAI Conventions](#103-opentelemetry-genai-conventions)
>   - [10.4 OpenHands — Event Stream Runtime](#104-openhands--event-stream-runtime)
>   - [10.5 Claude Code — Session Replay for Support](#105-claude-code--session-replay-for-support)
> - [11. TypeScript Interfaces for Observability](#11-typescript-interfaces-for-observability)
> - [12. Design Principles for Observability](#12-design-principles-for-observability)
>   - [12.1 SOLID for Trace Systems](#121-solid-for-trace-systems)
>   - [12.2 Six Design Principles](#122-six-design-principles)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do-)
>   - [13.2 DON'T ❌](#132-dont-)
> - [14. Anti-Patterns & Solutions](#14-anti-patterns--solutions)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Future Trends in Observability](#16-future-trends-in-observability)
> - [References](#references)
>
> **Cross-cutting module.** Think of trajectory as the backbone of the whole harness. Every stage
> writes to it, and every debugging session reads from it. This guide is the map;
> `03-update-memory-store/trajectory-fork-replay.md` has the engine code.

---

### Opening Story

Ticket: *"The agent deleted `src/auth/middleware.ts` and the user reported it 40 minutes
later. Why?"*

Without a trajectory, you can't answer this. You have the chat text (what the model
said, not what it did), a partial CI log, and a hunch ("it was working on the auth
refactor"). You can't tell which turn made the delete, what the tool returned just
before it, whether the file was even in the current branch at that moment, or what
the agent thought it was doing. You end up writing a post-mortem that is really just
a guess.

With a trajectory, the same question takes eleven seconds and one query:

> 📄 **Example code:** [`examples/01-opening-story.sql`](examples/01-opening-story.sql)

**And the follow-up questions answer themselves.** Why did it delete? `seq 29: prompt` —
the exports were unused, and the model chose deletion over leaving dead code. Could you
undo it? `seq 33` records `git worktree`, so yes, and the final patch is in `seq 51`.
Should this have been gated? The blast radius was one file — below the `write` threshold —
but that file was *imported by 3 other files the agent never read*. That is a policy
question, and now you can actually answer it.

**This is what a trajectory gives you: the difference between "it broke" and "here is exactly
what happened, here is why, and here is what we should change."

### Why Is Trajectory Non-Optional?

> *"If your agent system has no trajectory log, every incident is
> hard to reproduce, every cost is hard to explain, and every regression stays hidden."*

#### Four Capabilities That Fall Apart Without It

| Capability | Without trajectory | With trajectory |
|-----------|-------------------|-----------------|
| **Debug** | Guess from chat transcripts | `SELECT` the exact turn |
| **Eval** (→ 11) | Only final output; step efficiency invisible | Step precision, recovery rate, loop detection |
| **Cost** | Bill ÷ run count; no attribution | `GROUP BY task_id` with tokens + model tier |
| **Audit** (→ 15) | "Who approved the deploy?" → scroll Slack | One immutable, hash-linked record |

The cost story is worth highlighting. Without per-step tokens and per-step model tier you
can't answer *"why did our bill triple last month?"* — you only know that it did. With a
trajectory it is `SELECT SUM(tokens) WHERE model='frontier' GROUP BY session`, and the
answer is usually "a retry loop on 3% of runs" or "compaction stopped working" — both
easy to fix in an afternoon.

#### Core Philosophy

```
Trajectory   = the only durable evidence of what an agent actually did
Observability = the discipline of querying that evidence before opinions form
```

## Overview

> **📌 Core Concept**
>
> - **Concept:** A trajectory is an **append-only event log** of a run: every prompt, tool call, tool result, plan revision, eval verdict, memory write, approval, and compaction — each timestamped, attributed, and joined by keys. **Observability** is the practice of querying that log to debug, replay, attribute cost, and improve the system.
> - **Analogy:** The flight data recorder. A routine landing gets no attention; a crash is investigated entirely from the recorder, and the same data replays the flight path.
> - **Why it matters:** Without it you can't answer "why did it edit the wrong file?", "which retrieved chunk poisoned the answer?", or "what did this run cost?". With it, debugging is a query, evaluation is SQL, and incidents are reproducible.

**Trajectory & Observability** turns a hidden agent run into something you can query, replay,
and audit. It's the difference between an agent you *run* and an agent you just
*hope works*.

```
┌────────────────────── HARNESS EMITTERS ──────────────────────┐
│                                                              │
│  01 retrieve ┐  02 context ┐  04 plan  ┐  06 tools ┐  11 eval│
│  03 memory  ─┤  05 prompt ─┤  07 flow ─┤  09 agents┤  14 compact
│  12 sandbox ─┤  13 self   ─┘  15 gate  ─┘  10 auto ─┘        │
└──────────────────────────────┬───────────────────────────────┘
                               │  append(event)  ← one shape, one sink
                               ▼
                 ┌─────────────────────────────┐
                 │   TrajectoryStore           │
                 │   ses_44a.jsonl (append)    │
                 │   ┌───────────────────────┐ │
                 │   │ evt_01  prompt        │ │
                 │   │ evt_02  plan          │ │
                 │   │ evt_03  tool_call     │ │  ← seq, ts, taskId,
                 │   │ evt_04  tool_result   │ │    tokens, latency,
                 │   │ evt_05  eval          │ │    redacted payload
                 │   │ evt_06  memory_write  │ │
                 │   └───────────────────────┘ │
                 └──────┬───────────────┬───────┘
                        │               │
          ┌─────────────┴──┐      ┌─────┴──────────────┐
          │ Replay / Fork /│      │ SQL / dashboards   │
          │ Resume (→ 3)   │      │ metrics (→ 6)      │
          └────────────────┘      └────────────────────┘
```

**Two simple rules make it work:** (1) *append-only* — you never change an old event, so the
history stays trustworthy; (2) *every event carries `sessionId` + `parentTaskId`* — so no
event is lost on its own and every question has a join.

## Contents

| # | Topic | Description |
|---|-------|-------------|
| 1 | [TrajectoryEvent Contract](#1-the-trajectoryevent-contract) | The one schema every module emits |
| 2 | [Session Event Stream](#2-session-event-stream-lifecycle) | Lifecycle, durability, tailing |
| 3 | [Fork / Replay / Resume](#3-fork-replay-resume) | Determinism, A/B, crash recovery |
| 4 | [Cross-Module Joins](#4-cross-module-join-keys) | Task ↔ Context ↔ Eval ↔ Gate |
| 5 | [Retention & Redaction](#5-retention-redaction--gdpr) | Hot/warm/cold, GDPR receipts |
| 6 | [Metrics for Free](#6-metrics-for-free) | The query catalog |
| 7 | [Debugging](#7-debugging-workflows) | Five questions, run diffs, sampling |
| 8 | [Implementation](#8-typescript-implementation) | Store, projector, logger |
| 9 | [Testing](#9-testing-trajectory) | Contract + replay tests |
| 10 | [Case Studies](#10-real-world-case-studies) | SWE-bench, LangSmith, OTel, OpenHands, Claude Code |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-for-observability) | Full type surface |
| 12 | [Design Principles](#12-design-principles-for-observability) | SOLID for traces |
| 13 | [Best Practices](#13-best-practices) | DO / DON'T |
| 14 | [Anti-Patterns](#14-anti-patterns--solutions) | Common failures |
| 15 | [Production Checklist](#15-production-checklist) | Ship gate |
| 16 | [Future Trends](#16-future-trends-in-observability) | 2026-2028 |

---

## 1. The TrajectoryEvent Contract

### 1.1 Core Schema

One shape, used by every module, read by every tool. This is the single most
important piece of your observability layer.

> 📄 **Example code:** [`examples/02-1-1-core-schema.ts`](examples/02-1-1-core-schema.ts)

**Every field earns its place:**

| Field | What it enables that nothing else does |
|-------|------------------------------------------|
| `id` (ULID) | Sortable insert order without a clock dependency; cross-store dedupe |
| `seq` | Gap detection — a missing seq means a lost write, not a lost thought |
| `parentTaskId` | The join to the plan (→ 08); without it every event is an orphan |
| `actor` | Distinguishes "the model did this" from "a human did this" — the core of audit |
| `model` + `costUsd` | Per-step cost; the only way to find the run that ate the budget |
| `fingerprint` | Detects a prompt that changed under you; makes compaction auditable |
| `error.retryable` | Lets replay and eval reason about failure classes, not just text |

### 1.2 Event Kind Catalog

| Kind | Emitted by | Key payload | Consumed by |
|------|-----------|-------------|-------------|
| `session_start` | supervisor | user request, tenant, config hash | replay, cost |
| `context_assembly` | 02 | retrieved chunk ids + scores + token counts | attribution (→ 01) |
| `prompt` | 05 | fingerprint, tier, template id, est tokens | replay, cache stats (→ 06) |
| `plan` / `plan_revision` | 04 | task graph, reason for revision | recovery analysis |
| `tool_call` | 06 | tool, argvHash, policyHash, tier | precision metrics |
| `tool_result` | 06/12 | exit code, bytes, truncated, redactions | failure analysis |
| `sandbox` | 12 | runtime, image digest, allowlist | security audit (→ 12) |
| `memory_read` / `memory_write` | 03 | fact ids, scope, hit/miss | grounding analysis (→ 03) |
| `approval_request` / `approval_verdict` | 15 | tier, approver, diffHash, expiresAt | audit (→ 15) |
| `compaction` | 14 | keptIds, evictedIds, ratio, resume hash | context health (→ 14) |
| `eval` | 11 | judge, score, rubric, humanSampleId | regression detection (→ 11) |
| `error` | any | code, retryable, stack ref | SLO, alerting |

**Rule:** if a module creates a fact that someone might want to look up later,
it should emit an event. A fact that only lives in memory is a fact you can't debug with.

### 1.3 Validation & Versioning

> 📄 **Example code:** [`examples/03-1-3-validation-versioning.ts`](examples/03-1-3-validation-versioning.ts)

**Version the schema, not the fields.** Add `v: 2` and keep readers that handle both.
A trajectory written six months ago should still be readable — that is the whole point of
keeping it. Quietly renaming fields destroys your only copy of the truth.

---

## 2. Session Event Stream Lifecycle

### 2.1 The Shape of a Run

```
session_start
  → context_assembly   (retrieved 12 chunks, 8.1k tokens)
  → prompt             (fingerprint a3f9, tier=standard)
  → plan               (5 tasks: t1..t5, t2,t3 parallel)
  → tool_call/tool_result × N   (sandboxed; every call emits both)
  → compaction         (used 74% → kept 41, evicted 63)
  → eval               (judge score 0.82)
  → memory_write       (3 facts persisted)
  → session_end        (tasks done: 5/5, cost $0.41, duration 214s)
```

Interleaving that matters:

- **`tool_call` then `tool_result`, always paired.** An unpaired `tool_call` is a hung step — and a query that finds them is your hang detector (→ `09` §16.1).
- **`plan_revision` interleaved with the tool calls that motivated it.** Reconstruction requires cause and effect adjacent.
- **`compaction` between the prompt it shrank and the prompt that followed.** Otherwise you can't explain why the model forgot something.

### 2.2 Write Path — Durability Tiers

Not every event deserves an `fsync`. Ranked by cost of losing it:

| Event | Durability | Rationale |
|-------|-----------|-----------|
| `approval_verdict` | **fsync** | Legal record; losing it loses the audit chain |
| `memory_write` | **fsync** | Durable fact lost = silent correctness bug |
| `session_start` / `session_end` | **fsync** | Anchors cost and duration accounting |
| `eval` | **fsync** | Regression detection depends on completeness |
| `tool_call` / `tool_result` | flush ≤100 ms | Needed for debugging, tolerable to lose the last 100 ms |
| `prompt` / `context_assembly` | buffered | Reconstructable from the run itself |

> 📄 **Example code:** [`examples/04-2-2-write-path-durability-tiers.sh`](examples/04-2-2-write-path-durability-tiers.sh)

**Why JSONL and not a table?** Append-only writes, no locking for the common case,
`grep`-able, trivially portable, and replayable. The index is a *derived* concern; load
into DuckDB/SQLite for analysis. Storing the log as a table first means every event is
a transactional write in the hot path — a latency tax on the agent loop for the benefit
of a query you run once a week.

### 2.3 Read Path & Live Tailing

> 📄 **Example code:** [`examples/05-2-3-read-path-live-tailing.sh`](examples/05-2-3-read-path-live-tailing.sh)

Load into DuckDB for anything heavier:

> 📄 **Example code:** [`examples/06-2-3-read-path-live-tailing.sql`](examples/06-2-3-read-path-live-tailing.sql)

---

## 3. Fork, Replay, Resume

### 3.1 Semantics of Each

| Operation | What it does | When you need it | Fidelity requirement |
|-----------|--------------|------------------|----------------------|
| **Replay** | Re-execute events `0..N` with the same inputs; assert the outputs match | Reproduce a bug report exactly | Deterministic steps must be byte-identical |
| **Fork** | Clone the session at event `K`, continue with a different prompt/model/policy | "What if we'd used a big model here?" | Prefix identical; suffix may diverge wildly |
| **Resume** | Load the last checkpoint + tail the events written after the crash | Durable workflows (→ 07 §13) | Must not re-execute committed side effects |

These are three different tools with three different guarantees. Confusing them is how
teams end up with a "replay" that silently re-sends a production email.

### 3.2 Implementation

<details>
<summary>TypeScript Code — fork / replay / resume (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-3-2-implementation.ts`](examples/07-3-2-implementation.ts)

</details>

### 3.3 Replay Fidelity & Idempotency

**Not every step is deterministic.** Classify each kind before promising replay:

| Kind | Deterministic? | Fidelity contract |
|------|---------------|-------------------|
| `memory_read` | ✅ (given the same index state) | byte-identical |
| `tool_call` to a sandboxed command | ⚠️ (filesystem/time dependent) | same exit code; stdout may differ in timestamps |
| `tool_call` to a live API | ❌ | log the response; replay re-requests and compares shape |
| `prompt` | ❌ (sampling) | same `fingerprint` (template + context hash), not the same tokens |
| `eval` (LLM judge) | ❌ | same rubric + same input; expect score within ±0.1 |

**The rule that prevents disasters:** replay never re-triggers an irreversible side
effect. `idempotencyKeyOf()` = `(taskId, tool, argvHash)`; on replay, a completed key is
skipped and its recorded `tool_result` is substituted. This is why
`07-workflow/README.md` §13.3 requires idempotency keys on every step — replay isn't a
nice-to-have, it's the *reason* those keys exist.

`fingerprint` deserves a note: it hashes `(template, retrieved chunk ids, memory ids,
policy hash)`. If a replay produces a different fingerprint, the *inputs* changed — and
no amount of comparing outputs will tell you why. Check the fingerprint first.

---

## 4. Cross-Module Join Keys

### 4.1 The Join Table

| Question | Join path |
|----------|-----------|
| Which tool call belongs to which task? | `tool_call.parentTaskId → TaskNode.id` (→ 08) |
| Which retrieved chunks fed this answer? | `prompt.payload.chunkIds[] → chunk.id` (→ 01) |
| What did compaction keep vs evict? | `compaction.payload.{keptIds, evictedIds, ratio}` (→ 14) |
| Who approved this deploy? | `approval_verdict.{approver, diffHash, expiresAt}` (→ 15) |
| Did the judge agree with a human? | `eval.{judge, score, humanSampleId}` (→ 11 §15.4) |
| Was this step sandboxed correctly? | `sandbox.policyHash` ↔ `tool_call.policyHash` (→ 12) |

Each row is a question a user will ask within a week of shipping. Each is a single SQL
query. Each is impossible without the keys.

### 4.2 Five Questions One Query Answers

> 📄 **Example code:** [`examples/08-4-2-five-questions-one-query-answers.sql`](examples/08-4-2-five-questions-one-query-answers.sql)

Join keys turn "the model gave a wrong answer" into "it retrieved 12 chunks, used 4,
and the 3 highest-scoring ones were stale" — which has an owner and a fix.

### 4.3 Orphan Detection

An event with no `parentTaskId` (or a task that doesn't exist) is a wiring bug. Run
this continuously:

> 📄 **Example code:** [`examples/09-4-3-orphan-detection.sql`](examples/09-4-3-orphan-detection.sql)

Non-zero is a page. Orphans are how a harness ends up with a dashboard that silently
under-counts cost by 12% for eight months.

---

## 5. Retention, Redaction & GDPR

### 5.1 Hot / Warm / Cold Tiers

| Tier | Age | Contents | Storage | Query pattern |
|------|-----|----------|---------|---------------|
| **Hot** | 0–7 days | full payloads | fast SSD / in-memory | live tail, live debug |
| **Warm** | 7–90 days | payloads >4KB replaced by `ref`; rest inline | object storage | incident review |
| **Cold** | 90 days – 1 year | aggregates only (`steps`, `tokens`, `costUsd`, `latencyMs`, verdicts) | columnar | trends, SLO, cost reporting |
| **Purged** | per tenant TTL | deleted | — | GDPR erasure |

**The 4KB rule:** warm-tier payloads that exceed 4KB are replaced by a pointer. Large
tool outputs are the bulk of the bytes and the least useful six weeks later; a `ref` plus
`stdoutHash` preserves auditability without the storage bill.

### 5.2 Redaction at Emit

Redaction happens **at write time**, not at read time. Read-time redaction fails the
moment anything reads the raw table, and raw tables get read by ad-hoc queries.

> 📄 **Example code:** [`examples/10-5-2-redaction-at-emit.ts`](examples/10-5-2-redaction-at-emit.ts)

Store `redactions` as a field on the event. Then:

> 📄 **Example code:** [`examples/11-5-2-redaction-at-emit.sql`](examples/11-5-2-redaction-at-emit.sql)

### 5.3 Tenant Isolation & Deletion Receipts

- **`tenantId` on every event, enforced at write.** A missing `tenantId` is a write rejection, not a warning.
- **Row-level security or separate buckets per tenant.** Cross-tenant leakage in a trajectory store is a data breach in the strictest sense.
- **GDPR delete** removes: trajectory events, cold aggregates, derived reports, and any cached projections — then emits a receipt:

> 📄 **Example code:** [`examples/12-5-3-tenant-isolation-deletion-receipts.json`](examples/12-5-3-tenant-isolation-deletion-receipts.json)

The receipt is itself stored immutably. "We deleted it" must be verifiable without
trusting the system that deleted it.

---

## 6. Metrics for Free

### 6.1 The Query Catalog

Every metric is a query over the same table. This is the payoff for the schema work.

> 📄 **Example code:** [`examples/13-6-1-the-query-catalog.sql`](examples/13-6-1-the-query-catalog.sql)

### 6.2 Cost Attribution

> 📄 **Example code:** [`examples/14-6-2-cost-attribution.sql`](examples/14-6-2-cost-attribution.sql)

The most common finding: **cost isn't in the prompts, it's in the retry loops and the
frontier-tier steps nobody needed.** A cost dashboard built on this query usually finds
15–30% savings in the first week with no quality change.

---

## 7. Debugging Workflows

### 7.1 The Five Debug Questions

| # | Question | Query |
|---|----------|-------|
| 1 | What did the agent *do*? | `SELECT kind, payload ORDER BY seq` |
| 2 | What did it *see*? | `context_assembly` + `prompt.payload` |
| 3 | What did it *believe*? | `plan` + `plan_revision.reason` |
| 4 | Where did it *fail*? | `tool_result.exit_code != 0` + `error` |
| 5 | What did the *judge* say? | `eval.payload` |

Answering 2 and 3 before 4 is the discipline. Most "the model did something dumb" tickets
are actually question 2 failures: the model lacked the information, and question 3
correctly reflected that.

### 7.2 Diffing Two Runs

> 📄 **Example code:** [`examples/15-7-2-diffing-two-runs.ts`](examples/15-7-2-diffing-two-runs.ts)

Use it for prompt A/B tests, model upgrades, and "it worked yesterday" reports. The
first `~` line is almost always the interesting one.

### 7.3 Sampling Strategy

Full fidelity for everything is unaffordable and unnecessary.

| Signal class | Sampling | Rationale |
|--------------|----------|-----------|
| Errors, approvals, prod-auth | 100% | Low volume, high value |
| `eval.score < 0.6` | 100% | Failures are the training data |
| Successful `read` tools | 5% | High volume, low information |
| Successful writes | 20% | Medium value, needs coverage |
| Happy-path frontier prompts | 1% | Cost control |

Always keep the *counters* at 100% even when dropping payloads. A sampled log with
complete aggregates answers SLO questions; a sampled log without them answers nothing.

---

## 8. TypeScript Implementation

### 8.1 TrajectoryStore

<details>
<summary>TypeScript Code — append-only store with durability tiers (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-8-1-trajectorystore.ts`](examples/16-8-1-trajectorystore.ts)

</details>

### 8.2 Live Progress Projector

> 📄 **Example code:** [`examples/17-8-2-live-progress-projector.ts`](examples/17-8-2-live-progress-projector.ts)

### 8.3 Debug Logger Adapter

> 📄 **Example code:** [`examples/18-8-3-debug-logger-adapter.ts`](examples/18-8-3-debug-logger-adapter.ts)

---

## 9. Testing Trajectory

### 9.1 Contract Tests

Run in CI. These catch the class of bug where a new module emits an event that breaks
every downstream query.

> 📄 **Example code:** [`examples/19-9-1-contract-tests.ts`](examples/19-9-1-contract-tests.ts)

Also assert: every `tool_call` has a matching `tool_result`; every `tool_result.parentTaskId`
exists in the plan; no event's payload contains a secret pattern.

### 9.2 Replay Test Suite

> 📄 **Example code:** [`examples/20-9-2-replay-test-suite.ts`](examples/20-9-2-replay-test-suite.ts)

**Schedule:** replay the top-20 production trajectories nightly against a pinned model.
Drift on a deterministic step is a hard failure. Drift on an LLM step beyond ±0.1 score
is a signal to investigate — that is how you catch a provider silently changing
behavior before your users do.

---

## 10. Real-World Case Studies

### 10.1 SWE-bench Harness — Structured Trajectories

SWE-bench evaluation records, per instance: the model trajectory (patch, test results),
the resolution status, and the token cost. Because the trajectory is structured the same
way for every submission, it doubles as (a) the evaluation input (→ 11), (b) the
contamination surface (→ 11 §15.2), and (c) the debugging artifact when a submission
that used to pass starts failing.

The design lesson: **make the trajectory the evaluation artifact, not the final output.**
A final-output-only eval tells you *that* it failed. A trajectory eval tells you whether
it failed because it couldn't find the bug (retrieval problem), because it wrote a wrong
patch (reasoning problem), or because its patch was correct but the test harness was
flaky (infrastructure problem). Those demand completely different fixes.

### 10.2 LangSmith / Langfuse — Trace as Product

Observability vendors turned the trajectory into a product: trace waterfalls, prompt
versioning, dataset curation from traces, and eval runs over saved traces. The insight
that generalizes: **traces aren't just logs, they are the raw material for evaluation
datasets.** Every failed run is a curated eval case, already in the right shape, with the
real context that produced it.

The failure mode to avoid: building a trace UI nobody queries. The payoff is in the SQL,
not the waterfall. Teams that invest first in *queries* over a dumb JSONL store get more
value than teams with a beautiful dashboard and no way to ask questions of it.

### 10.3 OpenTelemetry GenAI Conventions

The OpenTelemetry GenAI semantic conventions standardize span names and attributes for
LLM calls: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`,
`gen_ai.usage.output_tokens`. The agent-specific conventions add spans for tool calls,
retrieval, and chain steps.

Why this matters: if you emit `gen_ai.*` attributes, your traces light up in whatever
observability backend the company already pays for, and your cost/latency dashboards come
for free. The cost of not adopting the conventions is re-implementing dashboards forever.

> 📄 **Example code:** [`examples/21-10-3-opentelemetry-genai-conventions.ts`](examples/21-10-3-opentelemetry-genai-conventions.ts)

### 10.4 OpenHands — Event Stream Runtime

OpenHands makes the event stream the runtime's interface: the agent emits
`Action`/`Observation` pairs, and every action is recorded as it executes rather than
afterwards. Design consequences:

1. **Recording isn't a side effect — it's the loop.** You can't "forget to log" because logging *is* how the loop communicates.
2. **Observations are first-class events**, not implicit return values. The difference matters: a truncated tool result is an event with `truncated: true`, not a silent string cut.
3. **Replay comes nearly free** because the event stream is the execution model.

### 10.5 Claude Code — Session Replay for Support

Coding agents used at scale lean on session replay for support: when a user reports
"it changed my config", support reads the trajectory rather than asking the user to
describe it. Two practices worth copying:

1. **The user's own transcript is the primary UI.** A visible, scrollable trace is a trust mechanism — the user can see what happened without asking.
2. **Sensitive-value redaction happens at emit.** Files like `.env`, key files, and credential patterns are redacted in the transcript the user sees, not just in the log you store.

---

## 11. TypeScript Interfaces for Observability

> 📄 **Example code:** [`examples/22-11-typescript-interfaces-for-observability.ts`](examples/22-11-typescript-interfaces-for-observability.ts)

---

## 12. Design Principles for Observability

### 12.1 SOLID for Trace Systems

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `TrajectoryStore` records. It does not interpret, alert, or decide sampling. |
| **O**pen/closed | New event kinds are data, not code — adding `delegation` requires no store change. |
| **L**iskov substitution | Any store (file, Postgres, OTel) satisfies `TrajectoryStore`; the engine does not care. |
| **I**nterface segregation | The live UI needs `tail()`; the debugger needs `load()`. Don't force the debugger to depend on streaming. |
| **D**ependency inversion | Modules depend on an `EventSink` interface, so a test harness can capture in memory. |

### 12.2 Six Design Principles

1. **Append-only.** Events are facts; facts aren't edited. Corrections are new events (`plan_revision`), never mutations.
2. **Every event is attributable.** `actor` and `parentTaskId` are mandatory. No orphans, ever.
3. **Redact at write.** Read-time redaction has already lost.
4. **Telemetry must never fail the task.** Append errors are counted, not thrown into the agent loop. An agent that stops working because logging broke is worse than one that is silently unobserved.
5. **Deterministic before sampled.** Full fidelity for errors, approvals, and low scores; sampling only for the happy path.
6. **Idempotency keys are part of the schema.** Without them, replay is a liability rather than a feature.

---

## 13. Best Practices

### 13.1 DO ✅

- Emit from *every* module, including the ones that feel trivial (context assembly, compaction).
- `fsync` approvals, memory writes, and session boundaries; buffer the rest.
- Store `seq` gaplessly and alert on gaps — a gap means lost evidence.
- Build cost attribution from step-level `model` + `tokens`, not from aggregate billing.
- Turn every failed run into a curated eval case; it's already in the right shape.
- Replay the top-20 production trajectories nightly against a pinned model.
- Emit `gen_ai.*` OpenTelemetry attributes so traces land in existing backends.

### 13.2 DON'T ❌

- ❌ Don't log full tool output with secrets in it. Cap, redact, keep a `ref`.
- ❌ Don't use a chat transcript as the trajectory — it records what the model *said*, not what it *did*.
- ❌ Don't `UPDATE` a past event to "fix" it. Append a correction.
- ❌ Don't let a telemetry exception propagate into the agent loop.
- ❌ Don't build a dashboard before you can express the questions in SQL.
- ❌ Don't promise byte-identical replay for LLM steps. Classify determinism per event kind.
- ❌ Don't store trajectories without `tenantId` and treat tenant filtering as a query-time concern.

---

## 14. Anti-Patterns & Solutions

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| **Chat log ≠ trajectory** | You can see the answer, not the actions | Emit `tool_call`/`tool_result` for every action |
| **Orphan events** | Dashboard under-counts cost by 10% | Make `parentTaskId` required; validate in CI |
| **Log everything at full fidelity** | Storage bill dwarfs the inference bill | Hot/warm/cold tiers; 4KB inline rule; sampling |
| **Redact at read** | One ad-hoc query leaks PII into a notebook | Redact at emit; audit the warm store quarterly |
| **Replay re-triggers side effects** | A replayed run emails a customer | Idempotency keys + substitute recorded results (→ 07 §13.3) |
| **Immutable log, mutable meaning** | Teams "fix" events in place, history is lost | Append-only + `*_revision` events |
| **Sampling without counters** | Metrics become statistically meaningless | 100% aggregates, sampled payloads |
| **No gap detection** | A lost write is discovered during an incident | `seq` gapless + CI assertion + alert |
| **UI as source of truth** | Progress state diverges from the event log | UI is a fold over events (`project()`) |

---

## 15. Production Checklist

- [ ] **Schema** — one `TrajectoryEvent` shape, zod-validated, versioned, gapless `seq`
- [ ] **Attribution** — `sessionId` + `parentTaskId` + `actor` + `tenantId` mandatory on every event
- [ ] **Durability** — fsync on approval/memory/eval/session boundaries; flush ≤100 ms otherwise
- [ ] **Redaction** — at emit; PII + secret patterns; `redactions` count stored and audited
- [ ] **Caps** — payload ≤64 KB, oversize → `ref`; stdout already capped at the sandbox
- [ ] **Cost** — step-level `model` + `tokens` + `costUsd`; per-task and per-tenant attribution working
- [ ] **Retention** — hot 7d / warm 90d / cold 1y; 4KB inline rule; tenant TTL honoured
- [ ] **Isolation** — RLS or per-tenant buckets; cross-tenant query returns nothing
- [ ] **GDPR** — delete path covers events, aggregates, projections; receipt stored immutably
- [ ] **Fork/replay/resume** — all three implemented and tested; idempotency keys on every step
- [ ] **Hang detection** — unpaired `tool_call` query wired to an alert
- [ ] **Sampling** — 100% on errors/approvals/low scores; 5–20% on happy path
- [ ] **Replay CI** — nightly replay of top-20 trajectories against a pinned model
- [ ] **Standards** — `gen_ai.*` OTel attributes emitted

---

## 16. Future Trends in Observability

### 16.1 Agent-Native Tracing (2026-2028)

- **Trajectory-aware evaluation.** Rubrics that score *the path* — did it check the test before declaring success? — rather than the final answer. The data is already there; it's a query problem.
- **Automatic drift detection.** A trajectory embedder that flags runs structurally unlike your known-good population before a human looks at them.
- **Causal attribution.** Given a bad outcome, identify the earliest decision that caused it. This is the frontier: not "what happened" but "which turn do I change".

### 16.2 Privacy-Preserving Telemetry

- **On-device redaction with differential privacy aggregates** for the metrics you keep globally while the payloads stay tenant-local.
- **Confidential-compute trace sinks** so even the observability vendor can't read the trajectory — the same SEV-SNP/TDX pattern as `12-sandbox-execution` §16.3.

### 16.3 Self-Describing Trajectories

Events that carry a machine-readable *rationale* — not just "I ran `pytest`" but "I ran
`pytest` because the previous run failed on `test_auth_refresh`" — make automatic
post-mortems possible. Expect the model's own plan-revision reasons to become a
first-class field rather than buried in prose.

### 16.4 Observability as a Security Primitive

Trajectories are the input to anomaly detection for prompt injection: a sudden cluster of
`path-escape` denials, egress to a new host, or a redaction spike in one tenant is a
detectible pattern. The flight recorder is how you find the flight that was hijacked.

---

## References

### Papers & Research

- **Event Sourcing** — Martin Fowler · https://martinfowler.com/eaaDev/EventSourcing.html
- **The Tail at Scale** — Dean & Barroso, CACM 2013 · https://cacm.acm.org/research/the-tail-at-scale/
- **DORA: Accelerate State of DevOps** — research into deployment frequency and change failure rate
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Jimenez et al., 2024 · https://arxiv.org/abs/2310.06770
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

### Frameworks & Tools

1. **OpenTelemetry GenAI semantic conventions** — https://opentelemetry.io/docs/specs/semconv/gen-ai/
2. **LangSmith** — https://docs.smith.langchain.com/ — trace + eval platform
3. **Langfuse** — https://langfuse.com/docs — open-source observability
4. **Arize Phoenix** — https://arize.com/docs/phoenix — open-source tracing + eval
5. **DuckDB** — https://duckdb.org/docs/stable/data/json/loading_json.html — query JSONL directly
6. **Zod** — https://zod.dev — schema validation at emit
7. **ULID / KSUID** — https://github.com/ulid/spec — sortable event IDs
8. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code

### Production Systems

- **SWE-bench harness** — https://github.com/SWE-bench/SWE-bench — structured trajectories for eval
- **OpenHands** — https://github.com/All-Hands-AI/OpenHands — event-stream runtime
- **Langfuse** — https://langfuse.com — self-hostable trace store
- **Phoenix** — https://github.com/Arize-ai/phoenix — trace + eval loop

### Related Modules

- `03-update-memory-store/trajectory-fork-replay.md` — the engine implementation (fork/replay/resume)
- `07-workflow/README.md` §13 — the resume consumer (checkpoint-resume, idempotency)
- `07-workflow/README.md` §5 — *adjacent, not a duplicate*: per-run distributed tracing (`trace_id`/spans/logs/metrics) for a single workflow. Joins this module on `runId`; a span isn't a `TrajectoryEvent`.
- `08-task/README.md` §11 — the task producer (`parentTaskId` source)
- `11-evaluation/README.md` §15 — the eval consumer (trajectory eval, human calibration)
- `12-sandbox-execution/README.md` §9 — the `sandbox` event producer
- `14-compaction-context/README.md` — the `compaction` event producer
- `15-approval-gates/README.md` §6 — the audit consumer (`approval_verdict`)

---

*Document: Harness 13. Trajectory & Observability — HARNESS ENGINEERING EDITION*
*Cross-cutting module · the spine of harness observability*
*Last updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Python Trajectory & Cost-per-Run

> Adds the Python equivalent of the §8.1 TypeScript TrajectoryStore, plus
> **cost-per-run** analysis — the thing that turns trajectory from "a log to debug"
> into "a log to manage costs".

### 1. TrajectoryEvent + JSONL Append-Only (Python)

> 📄 **Example code:** [`examples/23-1-trajectoryevent-jsonl-append-only-python.py`](examples/23-1-trajectoryevent-jsonl-append-only-python.py)

The two invariants stay the same as the TypeScript version: **append-only** (a ledger that never deletes) and
**every event carries a `session_id`** (no orphan events — §4.3).

### 2. Cost-per-Run: Detecting Abnormally Expensive Runs

> 📄 **Example code:** [`examples/24-2-cost-per-run-detecting-abnormally-expensive-runs.py`](examples/24-2-cost-per-run-detecting-abnormally-expensive-runs.py)

Why this metric is worth building first: Anthropic's analysis (06/2025) showed
**token usage explains ~80% of performance variance** between agent runs — slow runs
and failed runs are usually the runs that swallowed the most tokens, and the cause
can almost always be traced (retry loops, repeated retrieval, compaction stopped
running — §6.2). Measuring cost-per-run by task type is the cheapest way to see that
distribution tail **before** the invoice does.

Known gap: there is no **cost-per-task SLO** yet — the threshold for "this run is
abnormally expensive" is still a rule-of-thumb number, not standardized into a
measurable SLO. This gap is recorded in
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (§8);
until an SLO exists, store the cost distribution per task type so you have
calibration data.

### 3. Trace Decisions — Not Conversation Content

The privacy boundary carries over unchanged to the Python version: emit **decision
patterns** (kind, tool, tier, exit code, token count, latency), **not** the
prompt/response content of conversations. The reason is Anthropic Research's
production lesson: logging verbatim conversations turns the trajectory store into a
second copy of sensitive data — every ad-hoc query, every dashboard, every export is
a potential leak (→ §5.2: redact at emit time, not at read time). Payloads that need
to be traceable → store a `{ref}` pointing to a blob with its own ACL, never inline
them in the event.

### 4. Architecture Links

Trajectory is **Layer 8 (Observability & Feedback)** — every other layer emits into it,
every debugging session reads from it. See
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (Layer 8).
