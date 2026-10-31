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

This section shows, with one real incident, what a trajectory log gives you that chat logs do not.

Ticket: *"The agent deleted `src/auth/middleware.ts` and the user reported it 40 minutes
later. Why?"*

Without a trajectory, you can't answer this. A **trajectory** = the full step-by-step
record of one agent run: every prompt it received, every tool it called, every result it
got back, with timestamps and order numbers. What you have instead: the chat text (what
the model *said*, not what it *did*), a partial CI log, and a hunch ("it was working on
the auth refactor"). You can't tell which turn made the delete, what the tool returned
just before it, whether the file was even in the current branch at that moment, or what
the agent thought it was doing. You end up writing a post-mortem that is really just
a guess.

With a trajectory, the same question takes eleven seconds and one query:

> 📄 **Example code:** [`examples/01-opening-story.sql`](examples/01-opening-story.sql)

**And the follow-up questions answer themselves.** Why did it delete? `seq 29: prompt` —
`seq` = the event's position number in the log (event 29 of this run); the *prompt* event
shows the exports were unused, and the model chose deletion over leaving dead code.
Could you undo it? Event `seq 33` records a `git worktree` (a `git worktree` = a second
checked-out copy of the repo in another folder, so old files survive there), so yes, and
the final patch is in `seq 51`. Should this have been gated? The blast radius was one
file — below the `write` gate threshold — but that file was *imported by 3 other files
the agent never read*. That is a policy question, and now you can actually answer it.

**This is what a trajectory gives you: the difference between "it broke" and "here is
exactly what happened, here is why, and here is what we should change."**

> **One-line summary:** A trajectory turns "the agent broke something and nobody knows why" into an eleven-second SQL query that answers what happened, why, and what to change.

### Why Is Trajectory Non-Optional?

> *"If your agent system has no trajectory log, every incident is
> hard to reproduce, every cost is hard to explain, and every regression stays hidden."*

#### Four Capabilities That Fall Apart Without It

How to read this table: each row is a capability you lose without a trajectory log. "Without
trajectory" = what you're stuck doing today; "with trajectory" = the same job done with a
query. For example, row **Debug**: today you re-read chat transcripts and guess; with a
trajectory you run one `SELECT` (a database read command) and land on the exact turn.

| Capability | Without trajectory | With trajectory |
|-----------|-------------------|-----------------|
| **Debug** | Guess from chat transcripts | `SELECT` the exact turn |
| **Eval** (→ 11) | Only final output; step efficiency invisible | Step precision, recovery rate, loop detection |
| **Cost** | Bill ÷ run count; no attribution | `GROUP BY task_id` with tokens + model tier |
| **Audit** (→ 15) | "Who approved the deploy?" → scroll Slack | One immutable, hash-linked record |

Glosses: **Eval** = measuring how good the agent is, by scoring its runs. **`GROUP BY
task_id`** = a SQL command that groups cost rows per task, so you see what each task spent.
**Model tier** = price class of the model used (cheap vs "frontier" = the most expensive,
most capable tier). **Immutable, hash-linked record** = a log entry that can't be edited,
where each entry's fingerprint covers the previous one — so tampering is detectable.

The cost story is worth highlighting. Without per-step tokens and per-step model tier you
can't answer *"why did our bill triple last month?"* — you only know that it did. With a
trajectory it is `SELECT SUM(tokens) WHERE model='frontier' GROUP BY session` (in plain
words: "add up the tokens used by the expensive model, grouped per session"), and the
answer is usually "a retry loop on 3% of runs" or "compaction stopped working" — both
easy to fix in an afternoon.

> **One-line summary:** Without a trajectory log, debugging is guessing, cost is a mystery bill, and audit trails don't exist — all four become simple queries once every step is recorded.

#### Core Philosophy

This is the two-line mental model for the whole chapter.

```
Trajectory   = the only durable evidence of what an agent actually did
Observability = the discipline of querying that evidence before opinions form
```

Glosses: **durable evidence** = data that survives on disk and can't be edited after the
fact. **Observability** = the habit of checking that recorded data before forming opinions
about what went wrong.

> **One-line summary:** The trajectory is your only trustworthy record of what the agent really did — so query it before you argue about it.

## Overview

This section defines the two core words of the chapter and shows how every module feeds one shared log.

> **📌 Core Concept**
>
> - **Concept:** A trajectory is an **append-only event log** of a run (**append-only** = you only ever add new lines, never edit or delete old ones — like a bank statement, not a whiteboard): every prompt, tool call, tool result, plan revision, eval verdict, memory write, approval, and compaction — each timestamped, attributed, and joined by keys. **Observability** is the practice of querying that log to debug, replay, attribute cost, and improve the system.
> - **Analogy:** The flight data recorder. A routine landing gets no attention; a crash is investigated entirely from the recorder, and the same data replays the flight path.
> - **Why it matters:** Without it you can't answer "why did it edit the wrong file?", "which retrieved chunk poisoned the answer?", or "what did this run cost?". With it, debugging is a query, evaluation is SQL, and incidents are reproducible.

Glosses: **compaction** = the step that shrinks the conversation when it gets too long for the model's context window (its working memory). **Eval verdict** = the score a checker gives a run. **Attributed** = each event records who/what caused it (which module, which model, which task). **Joined by keys** = events carry shared IDs, so you can connect "this tool call" to "the task it belonged to".

**Trajectory & Observability** turns a hidden agent run into something you can query, replay,
and audit (**replay** = re-run the recorded steps; **audit** = verify after the fact who did
what and who approved it). It's the difference between an agent you *run* and an agent you
just *hope works*.

How to read the diagram: every numbered module (01 retrieve, 02 context, … 15 gate) writes
its events into one file — `ses_44a.jsonl`, the trajectory store. Each event gets a number
(`evt_01`…) and metadata (order number `seq`, timestamp `ts`, task ID, token count, latency,
redacted payload). Replay/fork/resume reads that file to re-run history; SQL and dashboards
read it to answer questions.

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

Glosses: **emitter** = a module that writes events. **Sink** = the one place all events land. **JSONL** = a text file with one JSON object per line — easy to append and grep. **Payload** = the event's content (what happened, in detail); **redacted payload** = the content with secrets and personal data already stripped out.

**Two simple rules make it work:** (1) *append-only* — you never change an old event, so the
history stays trustworthy; (2) *every event carries `sessionId` + `parentTaskId`* (**session
ID** = which chat/run this belongs to; **parent task ID** = which step of the plan this event
belongs to) — so no event is lost on its own and every question has a join.

> **One-line summary:** Every module appends events in one shared, never-edited log file, and every event carries IDs that connect it to its task — that single design makes debugging, replay, cost tracking, and audit all possible.

## Contents

How to read this table: column **#** is the section number, **Topic** is the section name
(clickable), and **Description** says in one line what that section answers. For example,
row 3 covers replaying and resuming runs — how to re-run or continue an agent session from
its recorded log.

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

Glosses for the descriptions: **durability** = how strongly an event is guaranteed to be
saved to disk; **tailing** = watching the log live as events arrive (like `tail -f`);
**A/B** = running two variants and comparing; **crash recovery** = continuing a run after
a crash without redoing finished work; **GDPR** = the EU privacy law that gives users the
right to have their data deleted; **OTel** = OpenTelemetry, the standard format for traces.

---

## 1. The TrajectoryEvent Contract

This section defines the single event shape every module must emit. Get this wrong and
nothing downstream works.

### 1.1 Core Schema

One shape, used by every module, read by every tool. This is the single most
important piece of your observability layer. A **schema** = the fixed list of fields every
event must have — like a form every module must fill in the same way.

> 📄 **Example code:** [`examples/02-1-1-core-schema.ts`](examples/02-1-1-core-schema.ts)

**Every field earns its place.** How to read the table: column 1 is the field name, column 2
says what unique job that field does that no other field covers. For instance, `seq` exists
purely to detect lost events: if event numbers jump from 41 to 43, event 42 was lost.

| Field | What it enables that nothing else does |
|-------|------------------------------------------|
| `id` (ULID) | Sortable insert order without a clock dependency; cross-store dedupe |
| `seq` | Gap detection — a missing seq means a lost write, not a lost thought |
| `parentTaskId` | The join to the plan (→ 08); without it every event is an orphan |
| `actor` | Distinguishes "the model did this" from "a human did this" — the core of audit |
| `model` + `costUsd` | Per-step cost; the only way to find the run that ate the budget |
| `fingerprint` | Detects a prompt that changed under you; makes compaction auditable |
| `error.retryable` | Lets replay and eval reason about failure classes, not just text |

Glosses: **ULID** = an ID type that is unique *and* sorts by creation time (unlike a random UUID), so sorting by ID ≈ sorting by time, with no clock server needed. **Dedupe** = recognizing and dropping a duplicate copy. **Orphan** = an event with no parent task, so nobody can tell what it belonged to. **Fingerprint** = a short hash of the prompt's inputs; if it changes, the inputs changed. **`error.retryable`** = a flag saying "this failure can be safely retried" — so tools react to the *class* of error, not parse error text.

### 1.2 Event Kind Catalog

How to read this table: each row is one **event kind** (= a type of thing that happened).
**Emitted by** = which module writes it (the numbers are the other harness modules, e.g.
"02" is the context module). **Key payload** = the important fields inside that event.
**Consumed by** = who reads it later. For example, a `tool_call` event is written by module
06 and carries the tool name plus a hash of its arguments; precision metrics read it.

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

Glosses: **supervisor** = the top-level controller that starts and stops sessions. **Chunk** = a piece of retrieved text (from search over documents). **`argvHash`** = a hash of the tool's arguments, so you can compare calls without storing full arguments. **`policyHash`** = a hash of the security rules that applied to this call. **Allowlist** = a whitelist — the list of things (folders, commands) that are permitted. **Digest** = a hash identifying the exact container image. **Hit/miss** = whether memory lookup found something useful. **`diffHash`** = a hash of the change being approved. **Rubric** = the scoring checklist the judge uses. **SLO** = service level objective — a target like "error rate below 1%". **Tenant** = one customer/organization sharing the system with others.

**Rule:** if a module creates a fact that someone might want to look up later,
it should emit an event. A fact that only lives in memory is a fact you can't debug with.

> **One-line summary:** One shared event schema plus one catalog of event kinds means every module records what it does in the same format — and every later question becomes a query.

### 1.3 Validation & Versioning

This section explains how to change the event schema over time without breaking old logs.

> 📄 **Example code:** [`examples/03-1-3-validation-versioning.ts`](examples/03-1-3-validation-versioning.ts)

**Version the schema, not the fields.** In plain words: don't rename or repurpose old fields
(silently changing what `payload.size` means); instead add a version marker like `v: 2` to
the event and keep readers that handle both versions. Add **validation** = a schema check
(e.g. with Zod) that rejects malformed events at write time, so bad data never enters the
log. A trajectory written six months ago should still be readable — that is the whole point
of keeping it. Quietly renaming fields destroys your only copy of the truth.

> **One-line summary:** Validate events on write, and evolve the schema by adding versions — never by silently renaming fields — so six-month-old logs stay readable.

---

## 2. Session Event Stream Lifecycle

This section explains what a run looks like as a sequence of events, how strongly each
event must be saved, and how to read the log live.

### 2.1 The Shape of a Run

This walkthrough shows one typical run, event by event, in the order they are appended.

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

Glosses: the session started; retrieval fetched 12 text chunks; the prompt got fingerprint
`a3f9` at the standard price tier; the planner made 5 tasks with tasks 2 and 3 in parallel;
tools ran inside a sandbox (an isolated environment, so mistakes can't touch the host);
compaction shrank a 74%-full context, keeping 41 items and evicting 63; a judge scored the
run 0.82; 3 learned facts were saved; the session ended with all 5 tasks done for $0.41.

Interleaving that matters (why the *order* of events carries meaning):

- **`tool_call` then `tool_result`, always paired.** An unpaired `tool_call` is a hung step — a call that never returned — and a query that finds them is your hang detector (→ `09` §16.1).
- **`plan_revision` interleaved with the tool calls that motivated it.** Reconstruction requires cause and effect adjacent (**plan_revision** = the agent changing its plan mid-run; the revision event sits right next to the tool results that triggered it).
- **`compaction` between the prompt it shrank and the prompt that followed.** Otherwise you can't explain why the model forgot something.

> **One-line summary:** A run is a fixed rhythm of paired events — and the *gaps and ordering* in that rhythm (an unpaired call, a misplaced compaction) are themselves diagnostic signals.

### 2.2 Write Path — Durability Tiers

This section answers: for each event type, how hard must we try not to lose it?
**Durability tier** = how strongly a write is committed. **fsync** = a call that forces the
OS to physically write data to disk *now* (slow but survives a crash); **flush** = hand it
to the OS quickly (may lose the last moments on crash); **buffered** = sit in memory
briefly (fastest, can lose a batch). Ranked by cost of losing it:

| Event | Durability | Rationale |
|-------|-----------|-----------|
| `approval_verdict` | **fsync** | Legal record; losing it loses the audit chain |
| `memory_write` | **fsync** | Durable fact lost = silent correctness bug |
| `session_start` / `session_end` | **fsync** | Anchors cost and duration accounting |
| `eval` | **fsync** | Regression detection depends on completeness |
| `tool_call` / `tool_result` | flush ≤100 ms | Needed for debugging, tolerable to lose the last 100 ms |
| `prompt` / `context_assembly` | buffered | Reconstructable from the run itself |

How to read it: the more expensive it is to lose an event type, the stronger the durability.
For example, an `approval_verdict` (= the recorded decision of a human approval gate) is a
legal record — if it's lost, you can no longer prove who approved what — so it gets fsync.
A `prompt` event can be rebuilt from other events, so buffering is fine.

> 📄 **Example code:** [`examples/04-2-2-write-path-durability-tiers.sh`](examples/04-2-2-write-path-durability-tiers.sh)

**Why JSONL and not a table?** Append-only writes, no locking for the common case,
`grep`-able (you can search it with plain text tools), trivially portable, and replayable.
The index is a *derived* concern (**derived** = computed from the raw log when needed, not
stored as the source of truth); load into DuckDB/SQLite for analysis (**DuckDB/SQLite** =
small embedded databases you can query with SQL without running a server). Storing the log
as a table first means every event is a transactional write in the hot path — a latency tax
on the agent loop for the benefit of a query you run once a week.

> **One-line summary:** Spend durability where losing data hurts (approvals, memory writes, session boundaries) and keep the log as an append-only JSONL file — speed first, indexes derived later.

### 2.3 Read Path & Live Tailing

This section covers reading the log two ways: watching it live, and heavy analysis.
**Live tailing** = following the log file as new events land, like watching a terminal.
Use it for progress screens and "is it stuck?" checks.

> 📄 **Example code:** [`examples/05-2-3-read-path-live-tailing.sh`](examples/05-2-3-read-path-live-tailing.sh)

Load into DuckDB for anything heavier (joins, aggregates, dashboards — DuckDB can query a
JSONL file directly with SQL, no import step needed):

> 📄 **Example code:** [`examples/06-2-3-read-path-live-tailing.sql`](examples/06-2-3-read-path-live-tailing.sql)

> **One-line summary:** Tail the raw log for live status, and load it into DuckDB/SQLite with SQL when you need real analysis.

---

## 3. Fork, Replay, Resume

This section defines three operations that all read the same log but serve different
purposes — and have very different safety rules.

### 3.1 Semantics of Each

How to read this table: each row is one operation, what it concretely does, when you reach
for it, and how faithfully it must reproduce the original (**fidelity** = how exactly the
re-run must match the original). For instance, **Fork** (row 2) copies the session at a
chosen point and continues with different settings — like a "save game, then try a
different choice".

| Operation | What it does | When you need it | Fidelity requirement |
|-----------|--------------|------------------|----------------------|
| **Replay** | Re-execute events `0..N` with the same inputs; assert the outputs match | Reproduce a bug report exactly | Deterministic steps must be byte-identical |
| **Fork** | Clone the session at event `K`, continue with a different prompt/model/policy | "What if we'd used a big model here?" | Prefix identical; suffix may diverge wildly |
| **Resume** | Load the last checkpoint + tail the events written after the crash | Durable workflows (→ 07 §13) | Must not re-execute committed side effects |

Glosses: **byte-identical** = exactly the same output, down to every byte. **Checkpoint** = a saved snapshot of progress. **Side effect** = an action that touches the outside world (sending an email, charging money, pushing code) as opposed to internal computation. **Committed side effect** = one that already went through — resume must never redo those, or a customer gets a second email.

These are three different tools with three different guarantees. Confusing them is how
teams end up with a "replay" that silently re-sends a production email.

> **One-line summary:** Replay re-runs to reproduce, fork copies to try alternatives, resume continues after a crash — and only resume has the hard rule "never redo an outside-world action".

### 3.2 Implementation

<details>
<summary>TypeScript Code — fork / replay / resume (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-3-2-implementation.ts`](examples/07-3-2-implementation.ts)

</details>

> **One-line summary:** The fork/replay/resume engine lives in the companion file — see the example code above and `03-update-memory-store/trajectory-fork-replay.md`.

### 3.3 Replay Fidelity & Idempotency

This section explains which steps you can expect to reproduce exactly, and the one rule
that keeps replay from causing damage.

**Not every step is deterministic.** **Deterministic** = same input always gives the same
output. Classify each kind before promising replay:

| Kind | Deterministic? | Fidelity contract |
|------|---------------|-------------------|
| `memory_read` | ✅ (given the same index state) | byte-identical |
| `tool_call` to a sandboxed command | ⚠️ (filesystem/time dependent) | same exit code; stdout may differ in timestamps |
| `tool_call` to a live API | ❌ | log the response; replay re-requests and compares shape |
| `prompt` | ❌ (sampling) | same `fingerprint` (template + context hash), not the same tokens |
| `eval` (LLM judge) | ❌ | same rubric + same input; expect score within ±0.1 |

How to read it: ✅ = reproducible exactly, ⚠️ = mostly reproducible with known wiggle
(timestamps in output text may differ), ❌ = not reproducible, so compare *shape* (the
structure of the response) rather than exact bytes. For example, an LLM judge re-scoring
the same input may give 0.78 instead of 0.83 — that's normal; what matters is it's within
±0.1 with the same rubric (scoring checklist).

**The rule that prevents disasters:** replay never re-triggers an irreversible side
effect. **Idempotent** = safe to run twice with the same result (like setting a value,
unlike sending an email). `idempotencyKeyOf()` = `(taskId, tool, argvHash)` — a unique key
built from task + tool + arguments; on replay, a key that already completed is *skipped*
and its recorded `tool_result` is substituted instead of re-running the action. This is why
`07-workflow/README.md` §13.3 requires idempotency keys on every step — replay isn't a
nice-to-have, it's the *reason* those keys exist.

`fingerprint` deserves a note: it hashes `(template, retrieved chunk ids, memory ids,
policy hash)` — a short value summarizing all the inputs to a prompt. If a replay produces
a different fingerprint, the *inputs* changed — and no amount of comparing outputs will
tell you why. Check the fingerprint first.

> **One-line summary:** Classify each step's determinism honestly, and give every side-effecting step an idempotency key so replay skips completed actions instead of repeating them.

---

## 4. Cross-Module Join Keys

This section is about connecting events across modules. A **join key** = a shared ID that
lets one record point to another (like a foreign key in a database). Without these keys,
each module's data is an island.

### 4.1 The Join Table

How to read this table: column 1 is a real question someone will ask; column 2 is the exact
chain of IDs that answers it (read `A → B` as "use field A of this event to look up record
B"). For example, "which tool call belongs to which task?" is answered by taking the tool
call's `parentTaskId` and looking up that task in the plan (module 08).

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

> **One-line summary:** Join keys are the difference between "the data exists somewhere" and "I can answer this question in one query" — bake them into the schema from day one.

### 4.2 Five Questions One Query Answers

This example shows the payoff: one SQL query that answers several questions at once by
joining across modules.

> 📄 **Example code:** [`examples/08-4-2-five-questions-one-query-answers.sql`](examples/08-4-2-five-questions-one-query-answers.sql)

Join keys turn "the model gave a wrong answer" into "it retrieved 12 chunks, used 4,
and the 3 highest-scoring ones were stale" — a specific, fixable finding with an owner,
instead of a vague complaint.

> **One-line summary:** With join keys, a vague "the answer was wrong" becomes a precise diagnosis — which chunks were retrieved, which were used, and which were outdated.

### 4.3 Orphan Detection

This section covers a health check for the log itself. An **orphan event** = an event whose
`parentTaskId` is missing or points to a task that doesn't exist. That's not a data quirk —
it's a wiring bug: some module is emitting events without the linking ID.

> 📄 **Example code:** [`examples/09-4-3-orphan-detection.sql`](examples/09-4-3-orphan-detection.sql)

Non-zero is a page (i.e., if this query returns any rows, wake someone up). Orphans are how
a harness ends up with a dashboard that silently under-counts cost by 12% for eight months —
the orphaned events exist but no dashboard can attribute them.

> **One-line summary:** Run an orphan-event check continuously; any event without a valid parent task is a bug that silently corrupts your cost and audit numbers.

---

## 5. Retention, Redaction & GDPR

This section covers keeping the log affordable, stripping sensitive data, and honoring
deletion rights. **Retention** = how long you keep data. **Redaction** = removing or
masking sensitive content (emails, API keys). **GDPR** = the EU privacy law; among other
things it gives users the right to have their data deleted on request.

### 5.1 Hot / Warm / Cold Tiers

How to read this table: the log ages through four storage tiers, like a filing cabinet
moving from your desk to a warehouse. **Age** = how old the events are; **Contents** = how
much detail survives; **Storage** = where it lives; **Query pattern** = what it's used for.
For instance, **Hot** (0–7 days) keeps everything on fast storage for live debugging;
**Cold** (90 days–1 year) keeps only the numbers, not the payloads.

| Tier | Age | Contents | Storage | Query pattern |
|------|-----|----------|---------|---------------|
| **Hot** | 0–7 days | full payloads | fast SSD / in-memory | live tail, live debug |
| **Warm** | 7–90 days | payloads >4KB replaced by `ref`; rest inline | object storage | incident review |
| **Cold** | 90 days – 1 year | aggregates only (`steps`, `tokens`, `costUsd`, `latencyMs`, verdicts) | columnar | trends, SLO, cost reporting |
| **Purged** | per tenant TTL | deleted | — | GDPR erasure |

Glosses: **payload** = the full content of an event. **`ref`** = a pointer to where the big content is stored elsewhere. **Object storage** = cheap bulk storage (like S3). **Columnar** = a database format optimized for counting/aggregating columns rather than reading whole rows. **Aggregates** = pre-computed summary numbers. **TTL** = time to live — how long data is kept before automatic deletion; here, each customer (tenant) can have their own TTL.

**The 4KB rule:** warm-tier payloads that exceed 4KB are replaced by a pointer. Large
tool outputs are the bulk of the bytes and the least useful six weeks later; a `ref` plus
`stdoutHash` (a fingerprint of the output, proving it hasn't changed) preserves auditability
without the storage bill.

> **One-line summary:** Keep full detail for a week, trim big payloads after that, keep only summary numbers for a year, and delete on schedule — detail decays on purpose because old bulk data costs money and reads nothing.

### 5.2 Redaction at Emit

This section's key idea in one signpost: strip sensitive data when *writing* the event, not
when reading it.

Redaction happens **at write time**, not at read time. Read-time redaction fails the
moment anything reads the raw table (a single ad-hoc query — an unplanned, informal query
someone runs directly — bypasses your read filters), and raw tables get read by ad-hoc
queries.

> 📄 **Example code:** [`examples/10-5-2-redaction-at-emit.ts`](examples/10-5-2-redaction-at-emit.ts)

Store `redactions` as a field on the event (a count/list of what was masked, so auditors
can see *that* something was redacted without seeing the secret). Then you can query redaction
stats directly:

> 📄 **Example code:** [`examples/11-5-2-redaction-at-emit.sql`](examples/11-5-2-redaction-at-emit.sql)

> **One-line summary:** Redact secrets at write time and record that you did — once a secret is in the log, every reader is a potential leak.

### 5.3 Tenant Isolation & Deletion Receipts

This section covers keeping different customers' logs separate, and proving deletion when
a customer exercises their GDPR "right to be erased". **Tenant** = one customer/org on a
shared system. **Isolation** = tenant A must never be able to read tenant B's events.

- **`tenantId` on every event, enforced at write.** A missing `tenantId` is a write rejection, not a warning — an event without a tenant could belong to anyone.
- **Row-level security or separate buckets per tenant.** **Row-level security (RLS)** = a database rule that filters every query by tenant automatically; **separate buckets** = literally different storage per tenant. Cross-tenant leakage in a trajectory store is a data breach in the strictest sense.
- **GDPR delete** removes: trajectory events, cold aggregates, derived reports, and any cached projections (**projection** = a materialized view/dashboard state computed from the events) — then emits a receipt:

> 📄 **Example code:** [`examples/12-5-3-tenant-isolation-deletion-receipts.json`](examples/12-5-3-tenant-isolation-deletion-receipts.json)

The receipt is itself stored immutably. "We deleted it" must be verifiable without
trusting the system that deleted it — the receipt is the proof, not a promise.

> **One-line summary:** Stamp a tenant ID on every event and enforce it at write time, and when deleting a tenant's data, delete everywhere and store an immutable receipt as proof.

---

## 6. Metrics for Free

This section is the payoff of the schema work: because every step is recorded with model,
tokens, and cost, useful metrics are just queries — no separate metrics pipeline needed.

### 6.1 The Query Catalog

A **query catalog** = a ready-made set of SQL queries, one per metric (success rate, loop
detection, latency, etc.). Every metric is a query over the same table. This is the payoff
for the schema work.

> 📄 **Example code:** [`examples/13-6-1-the-query-catalog.sql`](examples/13-6-1-the-query-catalog.sql)

> **One-line summary:** Record every step in one well-keyed table, and your metrics dashboard is just a folder of SQL queries over it.

### 6.2 Cost Attribution

**Cost attribution** = working out *which* task, tenant, or step consumed the money, not
just the total.

> 📄 **Example code:** [`examples/14-6-2-cost-attribution.sql`](examples/14-6-2-cost-attribution.sql)

The most common finding: **cost isn't in the prompts, it's in the retry loops and the
frontier-tier steps nobody needed** (**frontier tier** = the most expensive, most capable
model tier). A cost dashboard built on this query usually finds
15–30% savings in the first week with no quality change.

> **One-line summary:** Attribute cost per step and per task, and the usual culprits appear immediately — retry loops and unnecessarily expensive model calls.

---

## 7. Debugging Workflows

This section turns debugging from an art into five fixed questions, plus two techniques:
comparing runs and sampling.

### 7.1 The Five Debug Questions

How to read this table: rows 1–5 are the questions to ask, in order; the **Query** column
is how the trajectory answers each. For instance, question 1 ("what did the agent *do*?")
is answered by listing every event kind in order (`ORDER BY seq` = sort by the event's
position number).

| # | Question | Query |
|---|----------|-------|
| 1 | What did the agent *do*? | `SELECT kind, payload ORDER BY seq` |
| 2 | What did it *see*? | `context_assembly` + `prompt.payload` |
| 3 | What did it *believe*? | `plan` + `plan_revision.reason` |
| 4 | Where did it *fail*? | `tool_result.exit_code != 0` + `error` |
| 5 | What did the *judge* say? | `eval.payload` |

Answering 2 and 3 before 4 is the discipline. Most "the model did something dumb" tickets
are actually question 2 failures: the model lacked the information (bad retrieval, missing
context), and question 3 — its beliefs, visible in the plan and revision reasons —
correctly reflected that.

> **One-line summary:** Debug in order — actions, then what it saw, then what it believed, then failures, then the judge's verdict — because most "dumb model" bugs are really "it never saw the right information" bugs.

### 7.2 Diffing Two Runs

**Diffing** = comparing two runs side by side, showing only the lines that differ (like
`diff` on two text files, but for event logs).

> 📄 **Example code:** [`examples/15-7-2-diffing-two-runs.ts`](examples/15-7-2-diffing-two-runs.ts)

Use it for prompt A/B tests (comparing two prompt versions), model upgrades, and "it worked
yesterday" reports. The first `~` line (a `~` marks a difference in the diff output) is
almost always the interesting one.

> **One-line summary:** When behavior changes and you don't know why, diff the two runs' event logs — the first differing line usually names the cause.

### 7.3 Sampling Strategy

This section answers: do we need to record *everything*? No — record 100% of what's rare
and valuable, and sample the rest. **Sampling** = recording only a percentage of events
(the rest are dropped to save storage).

How to read this table: each row is a class of events; **Sampling** = what fraction to keep;
**Rationale** = why. For example, errors are rare but precious, so keep 100%; a successful
file-read is common and tells you little, so keep 5%.

| Signal class | Sampling | Rationale |
|--------------|----------|-----------|
| Errors, approvals, prod-auth | 100% | Low volume, high value |
| `eval.score < 0.6` | 100% | Failures are the training data |
| Successful `read` tools | 5% | High volume, low information |
| Successful writes | 20% | Medium value, needs coverage |
| Happy-path frontier prompts | 1% | Cost control |

Glosses: **prod-auth** = production authentication events. **Happy path** = the normal,
everything-works flow. **Frontier prompts** = prompts that ran on the expensive top-tier
model — keep 1% of those payloads as a cost control.

Always keep the *counters* at 100% even when dropping payloads (a counter = just the
number of events, not their content). A sampled log with
complete aggregates answers SLO questions; a sampled log without them answers nothing.

> **One-line summary:** Record 100% of errors, approvals, and bad scores; sample the boring success traffic; but always keep full counts so your statistics stay honest.

---

## 8. TypeScript Implementation

This section points to the three reference implementations: the store, the live progress
view, and the debug logger. A **projector** (§8.2) = code that turns the raw event stream
into a view (e.g., "3 of 5 tasks done") by folding over the events in order.

### 8.1 TrajectoryStore

<details>
<summary>TypeScript Code — append-only store with durability tiers (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-8-1-trajectorystore.ts`](examples/16-8-1-trajectorystore.ts)

</details>

> **One-line summary:** The store is deliberately boring — append JSONL lines, apply the fsync/flush/buffer tiers from §2.2, and nothing else.

### 8.2 Live Progress Projector

> 📄 **Example code:** [`examples/17-8-2-live-progress-projector.ts`](examples/17-8-2-live-progress-projector.ts)

> **One-line summary:** The progress UI is computed from events (a fold over the stream), never stored separately — so it can't drift from the truth.

### 8.3 Debug Logger Adapter

> 📄 **Example code:** [`examples/18-8-3-debug-logger-adapter.ts`](examples/18-8-3-debug-logger-adapter.ts)

> **One-line summary:** The adapter bridges existing debug logging into trajectory events, so old logs and the new store speak the same language.

---

## 9. Testing Trajectory

This section covers the two test suites that keep the trajectory system itself honest:
contract tests (the format is right) and replay tests (history still re-runs correctly).

### 9.1 Contract Tests

Run in CI (**CI** = continuous integration — automated tests that run on every code change).
These catch the class of bug where a new module emits an event that breaks
every downstream query — e.g., a missing field or a renamed one.

> 📄 **Example code:** [`examples/19-9-1-contract-tests.ts`](examples/19-9-1-contract-tests.ts)

Also assert: every `tool_call` has a matching `tool_result`; every `tool_result.parentTaskId`
exists in the plan; no event's payload contains a secret pattern (e.g., something shaped
like an API key).

> **One-line summary:** Contract tests in CI stop a malformed event from one module silently breaking every downstream query and dashboard.

### 9.2 Replay Test Suite

> 📄 **Example code:** [`examples/20-9-2-replay-test-suite.ts`](examples/20-9-2-replay-test-suite.ts)

**Schedule:** replay the top-20 production trajectories nightly against a pinned model
(**pinned** = a fixed, unchanging model version, so any behavior change is a real signal,
not a model update). Drift on a deterministic step is a hard failure (**drift** = the
re-run's output no longer matches the recorded one). Drift on an LLM step beyond ±0.1 score
is a signal to investigate — that is how you catch a provider silently changing
behavior before your users do.

> **One-line summary:** Nightly replay of real production runs against a pinned model catches both regressions in your code and silent changes from your model provider.

---

## 10. Real-World Case Studies

This section shows five real systems and the transferable lesson from each.

### 10.1 SWE-bench Harness — Structured Trajectories

**SWE-bench** = a public benchmark that tests whether language models can fix real GitHub
issues. Its evaluation records, per instance (per problem): the model trajectory (patch,
test results), the resolution status, and the token cost. Because the trajectory is
structured the same way for every submission, it doubles as (a) the evaluation input (→ 11),
(b) the contamination surface (→ 11 §15.2; **contamination** = a model having memorized the
test problems from training data), and (c) the debugging artifact when a submission
that used to pass starts failing.

The design lesson: **make the trajectory the evaluation artifact, not the final output.**
A final-output-only eval tells you *that* it failed. A trajectory eval tells you whether
it failed because it couldn't find the bug (retrieval problem), because it wrote a wrong
patch (reasoning problem), or because its patch was correct but the test harness was
flaky (**flaky** = passes and fails randomly, without real changes — an infrastructure
problem). Those demand completely different fixes.

> **One-line summary:** Record and evaluate the whole trajectory, not just the final answer — the path tells you *which kind* of failure happened, and each kind has a different fix.

### 10.2 LangSmith / Langfuse — Trace as Product

**LangSmith and Langfuse** = commercial/open-source platforms built around LLM tracing
(**trace** = the recorded path of one request through the system). Observability vendors
turned the trajectory into a product: trace waterfalls (a timeline chart showing where
time went), prompt versioning, dataset curation from traces, and eval runs over saved
traces. The insight that generalizes: **traces aren't just logs, they are the raw material
for evaluation datasets.** Every failed run is a curated eval case, already in the right
shape, with the real context that produced it.

The failure mode to avoid: building a trace UI nobody queries. The payoff is in the SQL,
not the waterfall. Teams that invest first in *queries* over a dumb JSONL store get more
value than teams with a beautiful dashboard and no way to ask questions of it.

> **One-line summary:** Failed runs are ready-made eval cases — invest in queryable traces before pretty dashboards.

### 10.3 OpenTelemetry GenAI Conventions

**OpenTelemetry (OTel)** = an industry standard for naming and formatting telemetry (traces,
metrics, logs) so any backend can read them. The GenAI semantic conventions standardize
span names and attributes for LLM calls (**span** = one timed segment of a request, e.g.
"this LLM call took 1.2s"): `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`,
`gen_ai.usage.output_tokens`. The agent-specific conventions add spans for tool calls,
retrieval, and chain steps.

Why this matters: if you emit `gen_ai.*` attributes, your traces light up in whatever
observability backend the company already pays for, and your cost/latency dashboards come
for free. The cost of not adopting the conventions is re-implementing dashboards forever.

> 📄 **Example code:** [`examples/21-10-3-opentelemetry-genai-conventions.ts`](examples/21-10-3-opentelemetry-genai-conventions.ts)

> **One-line summary:** Emitting the standard `gen_ai.*` attributes makes your agent traces work with existing observability tools for free — a custom format means rebuilding dashboards forever.

### 10.4 OpenHands — Event Stream Runtime

**OpenHands** = an open-source coding agent whose runtime is literally an event stream.
The agent emits `Action`/`Observation` pairs (**Action** = the agent does something;
**Observation** = the result it sees back), and every action is recorded as it executes
rather than afterwards. Design consequences:

1. **Recording isn't a side effect — it's the loop.** You can't "forget to log" because logging *is* how the loop communicates.
2. **Observations are first-class events**, not implicit return values. The difference matters: a truncated tool result is an event with `truncated: true`, not a silent string cut.
3. **Replay comes nearly free** because the event stream is the execution model.

> **One-line summary:** If your architecture *is* an event stream, logging, truncation flags, and replay stop being features you add and become properties you get for free.

### 10.5 Claude Code — Session Replay for Support

**Claude Code** = Anthropic's coding agent, used at a scale where support teams read logs.
It leans on session replay for support: when a user reports
"it changed my config", support reads the trajectory rather than asking the user to
describe it. Two practices worth copying:

1. **The user's own transcript is the primary UI.** A visible, scrollable trace is a trust mechanism — the user can see what happened without asking.
2. **Sensitive-value redaction happens at emit.** Files like `.env` (environment files holding API keys), key files, and credential patterns are redacted in the transcript the user sees, not just in the log you store.

> **One-line summary:** Show users their own run transcript and redact secrets before anything is written — support gets answers from the log, and users get trust from visibility.

---

## 11. TypeScript Interfaces for Observability

This section is the complete type surface — every interface and type used by the
trajectory system, in one file.

> 📄 **Example code:** [`examples/22-11-typescript-interfaces-for-observability.ts`](examples/22-11-typescript-interfaces-for-observability.ts)

> **One-line summary:** All the trajectory interfaces live in one reference file, so modules and tools agree on the same types.

---

## 12. Design Principles for Observability

This section gives the design rules: first classic SOLID applied to trace systems, then
six observability-specific principles.

### 12.1 SOLID for Trace Systems

**SOLID** = five classic software design principles (Single responsibility, Open/closed,
Liskov substitution, Interface segregation, Dependency inversion). How to read the table:
each row takes one principle and shows what it means for a trajectory system specifically.

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `TrajectoryStore` records. It does not interpret, alert, or decide sampling. |
| **O**pen/closed | New event kinds are data, not code — adding `delegation` requires no store change. |
| **L**iskov substitution | Any store (file, Postgres, OTel) satisfies `TrajectoryStore`; the engine does not care. |
| **I**nterface segregation | The live UI needs `tail()`; the debugger needs `load()`. Don't force the debugger to depend on streaming. |
| **D**ependency inversion | Modules depend on an `EventSink` interface, so a test harness can capture in memory. |

Glosses: **Open/closed** = open to extension, closed to modification — new event types are just new data rows, not new code paths. **Liskov substitution** = any implementation of the store interface is swappable without callers noticing. **Interface segregation** = expose small, need-specific methods rather than one big interface. **Dependency inversion** = depend on an abstract `EventSink` (the "where events go" interface), so tests can swap in an in-memory sink.

> **One-line summary:** The store's only job is recording; everything else — alerting, sampling, analysis — plugs in around it through small interfaces.

### 12.2 Six Design Principles

These are the six rules to memorize if you remember nothing else from this chapter.

1. **Append-only.** Events are facts; facts aren't edited. Corrections are new events (`plan_revision`), never mutations.
2. **Every event is attributable.** `actor` and `parentTaskId` are mandatory. No orphans, ever.
3. **Redact at write.** Read-time redaction has already lost.
4. **Telemetry must never fail the task.** Append errors are counted, not thrown into the agent loop. An agent that stops working because logging broke is worse than one that is silently unobserved.
5. **Deterministic before sampled.** Full fidelity for errors, approvals, and low scores; sampling only for the happy path.
6. **Idempotency keys are part of the schema.** Without them, replay is a liability rather than a feature.

> **One-line summary:** Never edit history, never drop attribution, never leak secrets, never let logging break the agent — those four "nevers" plus idempotency keys are the whole discipline.

---

## 13. Best Practices

Two checklists: what to always do (DO) and what to never do (DON'T). Each item is
one concrete habit.

### 13.1 DO ✅

- Emit from *every* module, including the ones that feel trivial (context assembly, compaction) — the "boring" modules are often where bugs hide.
- `fsync` approvals, memory writes, and session boundaries; buffer the rest (see §2.2 for why).
- Store `seq` gaplessly and alert on gaps — a gap means lost evidence.
- Build cost attribution from step-level `model` + `tokens`, not from aggregate billing (aggregate = one total number; it can't tell you *what* cost the money).
- Turn every failed run into a curated eval case; it's already in the right shape.
- Replay the top-20 production trajectories nightly against a pinned model (§9.2).
- Emit `gen_ai.*` OpenTelemetry attributes so traces land in existing backends (§10.3).

> **One-line summary:** Emit everything, protect what matters with fsync, watch for sequence gaps, and turn failures into eval data.

### 13.2 DON'T ❌

- ❌ Don't log full tool output with secrets in it. Cap (truncate oversized output), redact, keep a `ref`.
- ❌ Don't use a chat transcript as the trajectory — it records what the model *said*, not what it *did*.
- ❌ Don't `UPDATE` a past event to "fix" it. Append a correction (a new event) instead.
- ❌ Don't let a telemetry exception propagate into the agent loop (i.e., a logging failure must never crash or stop the agent's actual work).
- ❌ Don't build a dashboard before you can express the questions in SQL.
- ❌ Don't promise byte-identical replay for LLM steps. Classify determinism per event kind (§3.3).
- ❌ Don't store trajectories without `tenantId` and treat tenant filtering as a query-time concern — filter-at-read is how tenants leak.

> **One-line summary:** Never log secrets, never mistake chat text for actions, never edit history, and never let logging failures break the agent.

---

## 14. Anti-Patterns & Solutions

How to read this table: each row is a common mistake. **Anti-Pattern** = the mistake's name;
**Symptom** = how you notice it in production; **Fix** = the corrective action. For example,
the first row: teams log the chat conversation and call it a trajectory — but the chat only
shows what the model *said*, so the fix is emitting `tool_call`/`tool_result` events for
every actual action.

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

Glosses: **PII** = personally identifiable information (names, emails, phone numbers). **Inference bill** = what you pay the model provider for tokens. **Fold over events** (§8.2) = computing the current state by walking the events in order, so the UI can never disagree with the log.

> **One-line summary:** The recurring theme: record actions (not chat), link every event, protect secrets at write time, and never let replay or sampling corrupt your numbers.

---

## 15. Production Checklist

This is the pre-launch checklist: before shipping, every box below should be checked.
Each item condenses one earlier section.

- [ ] **Schema** — one `TrajectoryEvent` shape, zod-validated, versioned, gapless `seq` (Zod = a library that checks objects against a schema)
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

> **One-line summary:** One schema, full attribution, tiered durability, write-time redaction, tenant isolation, and nightly replay — tick all fourteen before shipping.

---

## 16. Future Trends in Observability

This section looks at where agent observability is heading (2026–2028): four directions,
from smarter evaluation to security.

### 16.1 Agent-Native Tracing (2026-2028)

- **Trajectory-aware evaluation.** Rubrics that score *the path* — did it check the test before declaring success? — rather than the final answer. The data is already there; it's a query problem.
- **Automatic drift detection.** A trajectory embedder (**embedder** = a model that converts text into numeric vectors, so "similar" becomes "close together") that flags runs structurally unlike your known-good population before a human looks at them.
- **Causal attribution.** Given a bad outcome, identify the earliest decision that caused it. This is the frontier: not "what happened" but "which turn do I change".

> **One-line summary:** The next generation scores the agent's path (not just its answer), flags weird runs automatically, and pinpoints the exact turn to change.

### 16.2 Privacy-Preserving Telemetry

- **On-device redaction with differential privacy aggregates** for the metrics you keep globally while the payloads stay tenant-local (**differential privacy** = adding calibrated noise to statistics so individual records can't be reverse-engineered from them).
- **Confidential-compute trace sinks** so even the observability vendor can't read the trajectory — the same SEV-SNP/TDX pattern as `12-sandbox-execution` §16.3 (**SEV-SNP/TDX** = CPU features that encrypt memory so that not even the cloud host can read it).

> **One-line summary:** Future telemetry keeps payloads local, adds noise to shared statistics, and encrypts traces so even the vendor can't read them.

### 16.3 Self-Describing Trajectories

This trend is about events that explain *why* they happened, not just *what* happened.

Events that carry a machine-readable *rationale* — not just "I ran `pytest`" but "I ran
`pytest` because the previous run failed on `test_auth_refresh`" — make automatic
post-mortems possible. Expect the model's own plan-revision reasons to become a
first-class field rather than buried in prose.

> **One-line summary:** Events will carry their own machine-readable reasons, enabling automatic post-mortems instead of human archaeology.

### 16.4 Observability as a Security Primitive

This trend reframes the trajectory log as a security tool, not just a debugging tool.

Trajectories are the input to anomaly detection for prompt injection (**prompt injection**
= an attacker smuggling instructions into text the agent reads, hijacking its behavior):
a sudden cluster of
`path-escape` denials (attempts to break out of the allowed directory list), egress to a
new host (the agent suddenly talking to an unknown server), or a redaction spike in one
tenant is a detectible pattern. The flight recorder is how you find the flight that was
hijacked.

> **One-line summary:** The trajectory log doubles as a security sensor — attack patterns like prompt injection show up as anomalies in the event stream.

---

## References

This section lists sources and related modules. Each entry keeps its original link; short
notes explain what each thing is.

### Papers & Research

- **Event Sourcing** — Martin Fowler · https://martinfowler.com/eaaDev/EventSourcing.html — the classic write-up of the "store every change as an immutable event" pattern this module is built on
- **The Tail at Scale** — Dean & Barroso, CACM 2013 · https://cacm.acm.org/research/the-tail-at-scale/ — why a few slow requests dominate latency, and how to fight it
- **DORA: Accelerate State of DevOps** — research into deployment frequency and change failure rate — the evidence base for "small, observable changes ship safer"
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Jimenez et al., 2024 · https://arxiv.org/abs/2310.06770
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

### Frameworks & Tools

1. **OpenTelemetry GenAI semantic conventions** — https://opentelemetry.io/docs/specs/semconv/gen-ai/ — the standard attribute names for LLM traces (§10.3)
2. **LangSmith** — https://docs.smith.langchain.com/ — trace + eval platform
3. **Langfuse** — https://langfuse.com/docs — open-source observability
4. **Arize Phoenix** — https://arize.com/docs/phoenix — open-source tracing + eval
5. **DuckDB** — https://duckdb.org/docs/stable/data/json/loading_json.html — query JSONL directly with SQL, no server needed (§2.3)
6. **Zod** — https://zod.dev — schema validation at emit (§1.3)
7. **ULID / KSUID** — https://github.com/ulid/spec — sortable event IDs (§1.1)
8. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code

### Production Systems

- **SWE-bench harness** — https://github.com/SWE-bench/SWE-bench — structured trajectories for eval (§10.1)
- **OpenHands** — https://github.com/All-Hands-AI/OpenHands — event-stream runtime (§10.4)
- **Langfuse** — https://langfuse.com — self-hostable trace store (**self-hostable** = you can run it on your own servers, keeping data in-house)
- **Phoenix** — https://github.com/Arize-ai/phoenix — trace + eval loop

### Related Modules

Each line below is a neighboring module and how it connects to this one. **Adjacent, not a
duplicate** (in the third bullet) means: it covers a related but distinct topic, and the
bullet explains the boundary so nobody merges them.

- `03-update-memory-store/trajectory-fork-replay.md` — the engine implementation (fork/replay/resume)
- `07-workflow/README.md` §13 — the resume consumer (checkpoint-resume, idempotency)
- `07-workflow/README.md` §5 — *adjacent, not a duplicate*: per-run distributed tracing (`trace_id`/spans/logs/metrics) for a single workflow. Joins this module on `runId`; a span isn't a `TrajectoryEvent`.
- `08-task/README.md` §11 — the task producer (`parentTaskId` source)
- `11-evaluation/README.md` §15 — the eval consumer (trajectory eval, human calibration)
- `12-sandbox-execution/README.md` §9 — the `sandbox` event producer
- `14-compaction-context/README.md` — the `compaction` event producer
- `15-approval-gates/README.md` §6 — the audit consumer (`approval_verdict`)

> **One-line summary:** The pattern (event sourcing), the standards (OTel), and the neighboring modules are all linked here — this document is one part of a connected system.

---

*Document: Harness 13. Trajectory & Observability — HARNESS ENGINEERING EDITION*
*Cross-cutting module · the spine of harness observability*
*Last updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Python Trajectory & Cost-per-Run

> Adds the Python equivalent of the §8.1 TypeScript TrajectoryStore, plus
> **cost-per-run** analysis — the thing that turns trajectory from "a log to debug"
> into "a log to manage costs". **Cost-per-run** = how much money (tokens × model price)
> a single run consumed.

### 1. TrajectoryEvent + JSONL Append-Only (Python)

This section is the Python version of the event store: same design, Python code.

> 📄 **Example code:** [`examples/23-1-trajectoryevent-jsonl-append-only-python.py`](examples/23-1-trajectoryevent-jsonl-append-only-python.py)

The two invariants stay the same as the TypeScript version: **append-only** (a ledger that
never deletes — new lines are only ever added, like a bank statement) and
**every event carries a `session_id`** (no orphan events — §4.3).

> **One-line summary:** The Python store follows the same two iron rules: never edit or delete past events, and every event carries its session ID.

### 2. Cost-per-Run: Detecting Abnormally Expensive Runs

This section explains why cost-per-run is the first metric worth building.

> 📄 **Example code:** [`examples/24-2-cost-per-run-detecting-abnormally-expensive-runs.py`](examples/24-2-cost-per-run-detecting-abnormally-expensive-runs.py)

Why this metric is worth building first: Anthropic's analysis (06/2025) showed
**token usage explains ~80% of performance variance** between agent runs — slow runs
and failed runs are usually the runs that swallowed the most tokens, and the cause
can almost always be traced (retry loops, repeated retrieval, compaction stopped
running — §6.2). Measuring cost-per-run by task type is the cheapest way to see that
distribution tail **before** the invoice does.

Known gap: there is no **cost-per-task SLO** yet — an SLO is a formal target you can
measure against (e.g. "no task type should exceed $X per run"); the threshold for
"this run is abnormally expensive" is still a rule-of-thumb number, not standardized into a
measurable SLO. This gap is recorded in
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (§8);
until an SLO exists, store the cost distribution per task type so you have
calibration data (i.e., historical numbers to set that threshold from).

> **One-line summary:** Cost-per-run is the cheapest early-warning metric — token-hungry runs are usually broken runs — and until a formal SLO exists, log the distribution to calibrate one.

### 3. Trace Decisions — Not Conversation Content

This section sets the privacy boundary for what goes into events.

The privacy boundary carries over unchanged to the Python version: emit **decision
patterns** (kind, tool, tier, exit code, token count, latency), **not** the
prompt/response content of conversations. The reason is Anthropic Research's
production lesson: logging verbatim conversations turns the trajectory store into a
second copy of sensitive data — every ad-hoc query, every dashboard, every export is
a potential leak (→ §5.2: redact at emit time, not at read time). Payloads that need
to be traceable → store a `{ref}` pointing to a blob with its own ACL (**blob** = a
stored file; **ACL** = access control list — the rules saying who may read it), never inline
them in the event.

> **One-line summary:** Log the metadata of decisions (what tool, what outcome, what cost) — never the conversation text — and point to protected storage with a `{ref}` when content must be traceable.

### 4. Architecture Links

This closing section places the trajectory in the overall system architecture.

Trajectory is **Layer 8 (Observability & Feedback)** — every other layer emits into it,
every debugging session reads from it. See
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (Layer 8).

> **One-line summary:** Trajectory is Layer 8 of the architecture: the shared log every layer writes to and every debugging session reads from.
