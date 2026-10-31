# 🔄 Trajectory Traceability Engine — Session Event Stream, Fork, Replay & Resume

> **Pattern inherited from DeepSeek Harness**: The system manages the entire execution trace (trajectory — the full record of one agent run) as a **Session Event Stream** (an ordered log of events that can only be appended to), supporting 100% traceability, Replay for audit/debug, and Fork/Resume to experiment with multiple solution branches without corrupting the original history.

> **⚠️ Canonical schema lives in `13-trajectory-observability`.** The `TrajectoryEvent` shape,
> the `EventKind` catalog, retention/redaction, and the metric queries are specified in
> [`13-trajectory-observability`](../13-trajectory-observability/README.md) — that module is the
> contract every producer and consumer codes against. **This file is the engine**: the concrete
> store, and the four operations (append / replay / fork / resume) implemented against the `13`
> schema. If the two ever disagree, `13` wins — fix this file.
>
> This split exists because writing to memory and observing the run are different jobs.
> `03-update-memory-store` decides *what is worth keeping*; `13` decides *what must be recorded*.
> The same event log serves both, which is why the schema is shared rather than duplicated.

---

## 📑 Contents

- [1. Context & Motivation](#1-context-&-motivation)
- [2. Trajectory Traceability Engine Philosophy](#2-trajectory-traceability-engine-philosophy)
- [3. Session Event Stream Architecture](#3-session-event-stream-architecture)
- [4. Core Operations: Replay, Fork, Resume & Search](#4-core-operations-replay-fork-resume-&-search)
  - [4.1. Replay (Replaying a Trajectory)](#41-replay-replaying-a-trajectory)
  - [4.2. Fork (Branching a Session)](#42-fork-branching-a-session)
  - [4.3. Resume (Continuing a Work Session)](#43-resume-continuing-a-work-session)
  - [4.4. Event Search (Searching Execution Traces)](#44-event-search-searching-execution-traces)
- [5. Illustrative Implementation (TypeScript Implementation)](#5-illustrative-implementation-typescript-implementation)
- [6. DeepSeek Harness Case Study: Trajectory Viewer & Event Inspector](#6-deepseek-harness-case-study-trajectory-viewer-&-event-inspector)
- [7. Best Practices & Anti-Patterns](#7-best-practices-&-anti-patterns)

---

## 1. Context & Motivation

This section names the three pain points the engine solves — read it to know why the rest exists.

In complex AI agent systems (especially AI Coding Agents), a single interaction session can span dozens of turns, call hundreds of tools (file search, edit, terminal, git), and generate a huge amount of context.

**Common problems with traditional agents:**
- **Black-box Execution**: When an agent fails at step 15, the user cannot tell which step the error came from (a bad prompt, a tool returning a faulty result, or an LLM reasoning error).
- **No State Undo/Branching**: If the agent goes down the wrong path at step 10, the only option is to delete the entire session and start over from scratch.
- **Hard Debugging & Evaluation**: You cannot replay the exact sequence of events that occurred to reproduce a bug or benchmark a model.

> **One-line summary:** Without an event log, a failed agent run is a black box: you cannot locate the failure, undo it, or reproduce it.

---

## 2. Trajectory Traceability Engine Philosophy

This section states the core idea: store the run as events, not as a chat transcript.

DeepSeek Harness solves the problems above with the **Full Traceability** philosophy:

```
Agent Execution = Sequence of State-Changing Events (Event Stream)
```

In plain words: every action that changes the agent's state becomes one recorded event, in order. Instead of storing a conversation as a flat list of messages (`[{role, content}]`), the system stores it as an **Append-Only Event Stream** (events can be added, never edited or deleted). Every action, tool result, state change, and prompt injection is recorded as an Event with a timestamp and a unique ID.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SESSION EVENT STREAM                            │
├────────────────────────────────────────────────────────────────────────┤
│  [Evt 1: User Prompt] ──► [Evt 2: System Context Inject]              │
│       │                                                                │
│       ▼                                                                │
│  [Evt 3: Reasoning Step] ──► [Evt 4: Tool Call (search_file)]          │
│       │                                                                │
│       ▼                                                                │
│  [Evt 5: Tool Result] ──► [Evt 6: Checkpoint Alpha]                    │
│                                   │                                    │
│                 ┌─────────────────┴─────────────────┐                  │
│                 ▼                                   ▼                  │
│       [Main Branch: Evt 7a...]            [Fork Branch: Evt 7b...]     │
└────────────────────────────────────────────────────────────────────────┘
```

How to read the diagram: each box is one event, top to bottom in time order. At Evt 6 (a checkpoint — a marked safe point), the run can split: the main branch continues, and a fork branch tries a different path from the same history.

> **One-line summary:** Treat a run as an ordered, append-only stream of state-changing events — that is what makes it inspectable, undoable, and reproducible.

---

## 3. Session Event Stream Architecture

This section points to the event schema contract and explains how to migrate an older store onto it.

Every Event uses the `TrajectoryEvent` contract defined in `13-trajectory-observability` §1.1. This file does not restate it — the only thing worth adding here is how the engine's legacy DeepSeek event names map onto the canonical `EventKind` catalog, because a store that predates `13` will have `user_prompt` / `agent_reasoning` / `state_change` records that must be queryable by the modern kinds:

> 📄 **Example code:** [`examples/01-3-session-event-stream-architecture.ts`](examples/01-3-session-event-stream-architecture.ts)

**Migration map for pre-`13` stores.** Three fields and three kinds changed. `timestamp` → `ts`,
`type` → `kind`, `parentId` → `parentTaskId`, and `metadata.tokensUsed` (a single scalar) →
`tokens: { in, out }`. Note that `parentId` pointed at the *previous event in the stream* while
`parentTaskId` points at the *plan node* (a step in the task plan) — they are different relationships, so a migration must
derive `parentTaskId` from the plan graph rather than by renaming the field.

How to read the table: column 1 is the old (legacy) name; column 2 is the new canonical name; column 3 says how to migrate it. For instance, row 1: `user_prompt` becomes kind `prompt` plus `actor: "human:*"` — a rename. Row 7 is the trap: `parentId` and `parentTaskId` point at different things, so it must be recomputed, not renamed.

| Legacy (`03` engine) | Canonical (`13` contract) | Note |
|----------------------|--------------------------|------|
| `user_prompt` | `prompt` (with `actor: "human:*"`) | |
| `system_injection` | `context_assembly` | |
| `agent_reasoning` | `message` (with `actor: "agent:*"`) | reasoning is a message, not a distinct kind |
| `state_change` | `plan` / `plan_revision` / `compaction` | one legacy kind, three canonical ones — split by payload |
| `timestamp` | `ts` | rename |
| `type` | `kind` | rename |
| `parentId` (previous event) | `parentTaskId` (plan node) | **recompute, do not rename** |
| `metadata.tokensUsed: number` | `tokens: { in, out }` | split; unknown split becomes `in` |
| *(none)* | `seq`, `actor`, `model`, `costUsd`, `fingerprint` | backfill: `seq` by position, `actor` by source, rest nullable |

The engine below emits the canonical shape directly. If you are migrating an existing store, run
the backfill once and then delete the legacy path — two live schemas in one store is how orphan
events and un-joinable audits start.

> **One-line summary:** One schema only: migrate legacy names once, recompute `parentTaskId` from the plan graph (never rename it), then delete the old path.

---

## 4. Core Operations: Replay, Fork, Resume & Search

This section defines the four things you can do with an event stream. Everything else builds on them.

### 4.1. Replay (Replaying a Trajectory)
Replay loads back the full list of Events from step 1 to step $N$ and reconstructs the exact state of the agent at any point in time — like `git checkout` for a conversation.
- **Deterministic Replay**: Exactly reproduces answers and tool results stored in the past without calling the LLM again or re-executing real commands (nothing in the real world is touched).
- **Live Replay (Dry-run)**: Keeps the tool execution history but calls a newer-generation LLM to compare results.

Replay *fidelity* — which steps are safe to re-execute, which must be served from the recorded
result, and how to detect drift when a live replay diverges — is specified in
`13-trajectory-observability` §3.3. The short rule: a replayed `tool_call` whose
`fingerprint` (a hash of the call's inputs) matches a recorded result reuses the recorded result; anything that would
produce a side effect must be gated by the idempotency key from `07-workflow` §13.3 (a key that makes a retry a no-op).

### 4.2. Fork (Branching a Session)
If the user sees the agent going down the wrong path at Event $K$, the user can **Fork** at Event $K$ — branch the session like a git branch:
- Create a child session (`parentSessionId`) that shares the Event history from $1 \to K$.
- All new Events in the fork session from step $K+1$ onward live on an independent branch.
- Lets the user experiment with different prompt calls or different tools without affecting the original session.

The fork record itself is stored as a `checkpoint` event carrying `forkedFrom: { atSeq, by }` —
see `13` §3.2. A fork is logically *not* a copy: the prefix is immutable history, so the fork
branches from it rather than replacing or re-executing it. The example below re-keys the
prefix into the new session for clarity — it is illustrative, not the storage strategy. Real
implementations share the prefix by reference (or by a parent-chain pointer) so that a
10,000-event session does not physically become 20,000 events; that dedup rule is specified in
`13` §2.2, not here.

### 4.3. Resume (Continuing a Work Session)
All session state is persisted to disk/DB using an Event Sourcing mechanism (the current state is rebuilt by replaying the event log, like a bank statement rebuilding a balance). When the system is interrupted (crash, restart, network timeout), the agent can **Resume** immediately from the last event without losing any context.

Resume must not re-execute committed side effects (real-world actions like sending email or charging money). The engine loads the last `checkpoint`, then
tails the events written after the crash and derives the set of already-completed steps
(`13` §3.2 `stepsToSkip()`); `07-workflow` §13.3 supplies the idempotency keys that make that
skip safe, and `08-task` §11 is where the task state is reconciled.

### 4.4. Event Search (Searching Execution Traces)
Allows searching inside the Trajectory Log:
- Find all failed Tool Calls (`error.retryable === false`, or `kind === "error"`).
- Find bash commands that ran successfully and contain the keyword `pnpm build`.
- Filter by token usage per turn (`tokens.in + tokens.out`).

The production query catalog for these — plus unpaired `tool_call` detection, cost
attribution, and compaction health — is in `13-trajectory-observability` §6.1. The engine here
keeps a typed filter for tests; the store is the right place for the SQL.

> **One-line summary (section 4):** Replay rebuilds any past state, fork branches safely from history, resume skips already-done side effects, and search finds events by kind, keyword, or cost.

---

## 5. Illustrative Implementation (TypeScript Implementation)

This section points to a runnable demo implementation of the engine.

Below is a simulated implementation of an engine that manages the Trajectory Event Stream,
emitting the canonical `13` shape. Durability tiers, live tailing, and the append-only
guarantees are specified in `13` §2.2; `inMemory` here stands in for a JSONL sink (a file where each line is one JSON event).

> 📄 **Example code:** [`examples/02-5-illustrative-implementation-typescript-implementation.ts`](examples/02-5-illustrative-implementation-typescript-implementation.ts)

---

## 6. DeepSeek Harness Case Study: Trajectory Viewer & Event Inspector

This section shows the same engine shipped as a UI, so the concepts above have a concrete face.

In the DeepSeek Harness Web UI (running on port `3080`), the **Trajectory View** feature provides an intuitive interface that lets engineers:
1. **Visual Timeline**: View the session's timeline with color blocks corresponding to Reasoning, Tool Calls (Bash/Edit), and Execution Results.
2. **One-Click Replay**: Click any node in the timeline to replay the exact dialogue and context at that point.
3. **Fork & Branch**: The "Fork Session from here" button branches immediately from the web interface, creating a safe experimentation environment.

---

## 7. Best Practices & Anti-Patterns

This section condenses the rules: five "always do", three "never do".

### ✅ Best Practices
- **Append-Only Immutability**: Never directly edit Events that have already been recorded. If you want to roll back or modify, fork the session or append a compensating Event of the canonical kind — `plan_revision` for a plan change, `compaction` for a context-window reduction. (`state_change` is a *legacy* name; see the migration map in §1, not a kind you should write.)
- **Compact Payloads**: For Tool Results that return huge amounts of data (e.g. a 10,000-line log), store a compact payload and extract a reference to a blob file to avoid filling up RAM/DB. The `13` contract caps inline payloads at 64KB and requires an `{ ref }` beyond that.
- **Regular Checkpointing**: Record `checkpoint` events after each completion of an important task milestone (e.g. end of the planning phase, end of the refactoring phase) to make forking easy.
- **Always set `actor`**: A `tool_call` with no `actor` is unattributable, which is the one thing an audit cannot repair after the fact.
- **Always set `parentTaskId`**: An event without it is an orphan — unjoinable to the plan, and therefore invisible to every cross-module query in `13` §4.1.

### ❌ Anti-Patterns
- **Incomplete Logging**: Only storing the chat dialogue between user and agent while failing to record background events (Context Injection, Internal Tool Calls, System Errors). A chat log is not a trajectory — see `13` §14.
- **Non-deterministic Events**: Storing Tool Call results but not storing the environment/parameters configuration, which breaks future Replay.
- **Two live schemas**: Running this engine's legacy `type`/`timestamp`/`parentId` shape alongside the `13` contract. Pick one, migrate, delete the other.

> **One-line summary (file):** Log every run as an append-only event stream with checkpoints, actors, and plan links — then replay, fork, and resume become safe by construction.
