# 📈 XIII. Trajectory & Observability

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
> **Cross-cutting module.** Trajectory is the spine of the whole harness. Every stage
> emits into it; every debug session reads from it. This module is the map;
> `03-update-memory-store/trajectory-fork-replay.md` holds the engine implementation.

---

### Opening Story

Ticket: *"The agent deleted `src/auth/middleware.ts` and the user reported it 40 minutes
later. Why?"*

Without a trajectory, this question is unanswerable. You have a chat log (the model's
words, not its actions), a partial CI log, and a gut feeling ("it was working on the auth
refactor"). You cannot say which turn contained the delete, what the tool returned before
it, whether the file was even in the current branch at that moment, or what the agent
thought it was doing. You write a post-mortem that is really just a guess.

With a trajectory, the same question takes eleven seconds and one query:

```sql
SELECT seq, kind, payload->>'tool' AS tool, payload->>'path' AS path
FROM trajectory
WHERE session_id = 'ses_44a' AND payload->>'path' LIKE '%middleware%'
ORDER BY seq;
-- seq 31: read_file  src/auth/middleware.ts  → 4.1KB
-- seq 32: edit_file  (patch applied)
-- seq 33: write_file  ← the delete
-- seq 34: eval        "tests pass" (they did — nothing imported it any more)
```

**And the follow-up questions answer themselves.** Why did it delete? `seq 29: prompt` —
the exports were unused, and the model chose deletion over leaving dead code. Was that
reversible? `seq 33` records `git worktree`, so yes, and the final patch is in `seq 51`.
Should this have been gated? Blast radius was one file — below the `write` threshold —
but the file was *imported by 3 other files the agent never read*. That is a policy
question, and now it is an answerable one.

**This is what a trajectory buys: the difference between "it broke" and "here is exactly
what happened, here is why, and here is what we should change."**

### Why Is Trajectory Non-Optional?

> *"An agent system without a trajectory log is a system where every incident is
> unreproducible, every cost is unattributable, and every regression is invisible."*

#### Four Capabilities That Fall Apart Without It

| Capability | Without trajectory | With trajectory |
|-----------|-------------------|-----------------|
| **Debug** | Guess from chat transcripts | `SELECT` the exact turn |
| **Eval** (→ 11) | Only final output; step efficiency invisible | Step precision, recovery rate, loop detection |
| **Cost** | Bill ÷ run count; no attribution | `GROUP BY task_id` with tokens + model tier |
| **Audit** (→ 15) | "Who approved the deploy?" → scroll Slack | One immutable, hash-linked record |

The cost angle deserves emphasis. Without per-step tokens and per-step model tier you
cannot answer *"why did our bill triple last month?"* — only that it did. With a
trajectory it is `SELECT SUM(tokens) WHERE model='frontier' GROUP BY session`, and the
answer is usually "a retry loop on 3% of runs" or "compaction stopped firing" — both
fixable in an afternoon.

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
> - **Why it matters:** Without it you cannot answer "why did it edit the wrong file?", "which retrieved chunk poisoned the answer?", or "what did this run cost?". With it, debugging is a query, evaluation is SQL, and incidents are reproducible.

**Trajectory & Observability** turns an opaque agent run into a queryable, replayable,
auditable object. It is the difference between an agent you *operate* and an agent you
*hope*.

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

**Two invariants make it work:** (1) *append-only* — no event is ever mutated, so the
history is trustworthy; (2) *every event carries `sessionId` + `parentTaskId`* — so no
event is an orphan and every question has a join.

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

One shape, emitted by every module, read by every tool. This is the single most
important artifact in a harness's observability layer.

```typescript
export type EventKind =
  | "session_start" | "session_end"
  | "context_assembly" | "prompt"
  | "plan" | "plan_revision"
  | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write"
  | "delegate" | "message"
  | "approval_request" | "approval_verdict"
  | "compaction" | "checkpoint" | "eval" | "error";

export interface TrajectoryEvent {
  id: string;             // evt_01HZX… — lexicographically sortable (ULID/KSUID)
  seq: number;            // 0-based, gapless, monotonic within a session
  sessionId: string;      // one user request = one session
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // one engine invocation; a session may have several
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: EventPayload;  // redacted; ≤64KB; oversize → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;         // which tier served this step → cost attribution
  costUsd?: number;       // computed at emit, not recomputed at query time
  error?: { code: string; retryable: boolean };
  fingerprint?: string;   // prompt hash → replay dedupe, compaction audit
}
```

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

**Rule:** if a module produces a fact that someone will eventually want to correlate,
it emits an event. A fact that lives only in memory is a fact you cannot debug with.

### 1.3 Validation & Versioning

```typescript
import { z } from "zod";

export const TrajectoryEventSchema = z.object({
  id: z.string().regex(/^evt_[0-9A-HJKMNP-TV-Z]{26}$/),  // ULID
  seq: z.number().int().nonnegative(),
  sessionId: z.string().min(1),
  parentTaskId: z.string().optional(),
  runId: z.string().optional(),
  ts: z.number().int(),
  kind: z.enum([/* … */]),
  actor: z.string().min(1),
  payload: z.unknown(),
  tokens: z.object({ in: z.number(), out: z.number(), cached: z.number().optional() }).optional(),
  latencyMs: z.number().nonnegative().optional(),
  model: z.string().optional(),
  costUsd: z.number().nonnegative().optional(),
  error: z.object({ code: z.string(), retryable: z.boolean() }).optional(),
  fingerprint: z.string().optional(),
}).superRefine((e, ctx) => {
  if (e.kind !== "session_start" && !e.parentTaskId)
    ctx.addIssue({ code: "custom", message: "orphan event: parentTaskId required" });
});
```

**Version the schema, not the fields.** Add `v: 2` and keep readers that handle both.
A trajectory written six months ago must still be readable — that is the whole point of
keeping it. Silent field renames destroy the only copy of the truth.

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
- **`compaction` between the prompt it shrank and the prompt that followed.** Otherwise you cannot explain why the model forgot something.

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

```bash
# One file per session. Append-only, newline-delimited JSON.
./trajectories/ses_44a.jsonl
./trajectories/ses_44b.jsonl
```

**Why JSONL and not a table?** Append-only writes, no locking for the common case,
`grep`-able, trivially portable, and replayable. The index is a *derived* concern; load
into DuckDB/SQLite for analysis. Storing the log as a table first means every event is
a transactional write in the hot path — a latency tax on the agent loop for the benefit
of a query you run once a week.

### 2.3 Read Path & Live Tailing

```bash
# 1. What happened, in order?
jq -r '[.seq, .kind, .actor, (.payload.tool // "-")] | @tsv' ses_44a.jsonl

# 2. Find the expensive steps
jq -s 'sort_by(-(.latencyMs // 0))[:10] | .[] | {seq, kind, latencyMs, model}' ses_44a.jsonl

# 3. Find unpaired tool calls (hang detector)
jq -s '[.[] | select(.kind=="tool_call") | .seq] as $c
       | [.[] | select(.kind=="tool_result") | .seq] as $r
       | ($c - $r)' ses_44a.jsonl

# 4. Live tail
tail -f ses_44a.jsonl | jq -c '{seq, kind, tool: .payload.tool}'
```

Load into DuckDB for anything heavier:

```sql
INSTALL httpfs; LOAD httpfs;
SELECT model, COUNT(*) AS steps, SUM(tokens.in + tokens.out) AS total_tokens,
       SUM(costUsd) AS usd
FROM read_json_auto('trajectories/*.jsonl')
GROUP BY model ORDER BY usd DESC;
```

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

```typescript
import { createHash } from "node:crypto";
import { createInterface } from "node:readline";
import { createReadStream } from "node:fs";
import { ulid } from "ulid";

export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}

export async function loadSession(path: string): Promise<TrajectoryEvent[]> {
  const out: TrajectoryEvent[] = [];
  const rl = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of rl) if (line.trim()) out.push(JSON.parse(line));
  return assertGapless(out);
}

/** Gapless seq proves no write was lost. A gap means the log is incomplete —
 *  every downstream conclusion (cost, replay) is then suspect. */
function assertGapless(evts: TrajectoryEvent[]): TrajectoryEvent[] {
  evts.sort((a, b) => a.seq - b.seq);
  for (let i = 1; i < evts.length; i++)
    if (evts[i].seq !== evts[i - 1].seq + 1)
      throw new Error(`trajectory gap: seq ${evts[i - 1].seq} → ${evts[i].seq}`);
  return evts;
}

/** FORK — clone the prefix, mint a new identity, continue divergently. */
export function fork(src: Session, atSeq: number, by: string): Session {
  const prefix = src.events.filter(e => e.seq <= atSeq);
  const clone: Session = {
    sessionId: `ses_${ulid()}`,
    forkedFrom: { sessionId: src.sessionId, atSeq, by },
    events: prefix.map(e => ({ ...e })),      // new ids on write, same seq
  };
  return clone;
}

export interface ReplayDiff { step: number; kind: string; drift: "none" | "output" | "error" | "latency" }

/** REPLAY — compare a fresh execution against the recorded one. */
export function diffRun(recorded: TrajectoryEvent[], fresh: TrajectoryEvent[]): ReplayDiff[] {
  const diffs: ReplayDiff[] = [];
  const n = Math.max(recorded.length, fresh.length);
  for (let i = 0; i < n; i++) {
    const a = recorded[i], b = fresh[i];
    if (!a || !b) { diffs.push({ step: i, kind: a?.kind ?? b?.kind ?? "?", drift: "output" }); continue; }
    if (a.kind !== b.kind) { diffs.push({ step: i, kind: a.kind, drift: "output" }); continue; }
    if (hash(a.payload) !== hash(b.payload)) diffs.push({ step: i, kind: a.kind, drift: "output" });
    else if ((a.latencyMs ?? 0) > (b.latencyMs ?? 0) * 3 + 500) diffs.push({ step: i, kind: a.kind, drift: "latency" });
  }
  return diffs;
}
const hash = (o: unknown) => createHash("sha256").update(JSON.stringify(o)).digest("hex").slice(0, 16);

/** RESUME — idempotency keys make re-execution after a crash safe. */
export function stepsToSkip(events: TrajectoryEvent[], done: Set<string>): string[] {
  return events.filter(e => e.kind === "tool_call" && done.has(idempotencyKeyOf(e)))
               .map(e => e.payload.callId as string);
}
export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;  // → 07 §13.3
}
```

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
`07-workflow/README.md` §13.3 requires idempotency keys on every step — replay is not a
nice-to-have, it is the *reason* those keys exist.

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

```sql
-- "Why was retrieval cited but not used?" — join context_assembly → prompt → eval
SELECT c.session_id,
       c.payload->>'chunkIds'    AS retrieved,
       p.payload->>'chunkIds'    AS used,
       e.payload->>'score'       AS judge_score
FROM trajectory c
JOIN trajectory p ON p.session_id = c.session_id AND p.kind='prompt'
JOIN trajectory e ON e.session_id = c.session_id AND e.kind='eval'
WHERE c.kind='context_assembly';
```

Join keys turn "the model gave a wrong answer" into "it retrieved 12 chunks, used 4,
and the 3 highest-scoring ones were stale" — which has an owner and a fix.

### 4.3 Orphan Detection

An event with no `parentTaskId` (or a task that does not exist) is a wiring bug. Run
this continuously:

```sql
SELECT kind, COUNT(*) AS orphans, MIN(ts) AS first_seen
FROM trajectory
WHERE parent_task_id IS NULL AND kind NOT IN ('session_start','session_end')
GROUP BY kind;
```

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

```typescript
const PII = [
  /sk-[A-Za-z0-9_-]{20,}/g,                 // API keys
  /gh[pousr]_\w{20,}/g,                     // GitHub tokens
  /AKIA[0-9A-Z]{16}/g,                      // AWS access key id
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/g,     // private keys
  /[\w.+-]+@[\w-]+\.[\w.]{2,}/g,             // email
  /\b(?:\d[ -]?){13,19}\b/g,                 // card numbers
];

export function redactPayload<T>(payload: T): { payload: T; redactions: number } {
  let s = JSON.stringify(payload), n = 0;
  for (const re of PII) s = s.replace(re, () => { n++; return "[REDACTED]"; });
  return { payload: JSON.parse(s), redactions: n };
}
```

Store `redactions` as a field on the event. Then:

```sql
-- Quarterly assertion: zero secret-shaped strings in warm store
SELECT COUNT(*) FROM read_json_auto('trajectories-warm/*.jsonl')
WHERE payload::TEXT ~ 'sk-[A-Za-z0-9]{20}';
-- must be 0. Non-zero = incident.
```

### 5.3 Tenant Isolation & Deletion Receipts

- **`tenantId` on every event, enforced at write.** A missing `tenantId` is a write rejection, not a warning.
- **Row-level security or separate buckets per tenant.** Cross-tenant leakage in a trajectory store is a data breach in the strictest sense.
- **GDPR delete** removes: trajectory events, cold aggregates, derived reports, and any cached projections — then emits a receipt:

```json
{ "kind": "deletion_receipt", "tenantId": "acme",
  "sessionsDeleted": 1841, "eventsDeleted": 214883, "coldAggregatesPurged": true,
  "ref": "receipts/acme-2026-07-19.json", "at": 1752900000000 }
```

The receipt is itself stored immutably. "We deleted it" must be verifiable without
trusting the system that deleted it.

---

## 6. Metrics for Free

### 6.1 The Query Catalog

Every metric is a query over the same table. This is the payoff for the schema work.

```sql
-- Step efficiency (→ 11 §15.1)
SELECT AVG(steps) AS avg_steps, AVG(tokens_out) AS avg_out
FROM (SELECT session_id, COUNT(*) AS steps, MAX(tokens_out) AS tokens_out
      FROM trajectory WHERE kind IN ('tool_call','prompt') GROUP BY session_id);

-- Tool precision: useful ÷ total (label useful calls at the tool layer)
SELECT payload->>'tool' AS tool,
       COUNT(*) AS calls,
       AVG(CASE WHEN payload->>'useful'='true' THEN 1.0 ELSE 0.0 END) AS precision
FROM trajectory WHERE kind='tool_call' GROUP BY tool ORDER BY calls DESC;

-- Recovery rate: runs that hit an error and still finished
SELECT COUNT(*) FILTER (WHERE err THEN 1)/COUNT(*)::float AS recovered
FROM (SELECT session_id, BOOL_OR(kind='error') AS err
      FROM trajectory GROUP BY session_id);

-- Loop detector: same argvHash 3+ times in one session
SELECT session_id, payload->>'argvHash' AS h, COUNT(*) AS n
FROM trajectory WHERE kind='tool_call'
GROUP BY session_id, h HAVING COUNT(*) >= 3 ORDER BY n DESC;

-- Compaction health (→ 14)
SELECT AVG((payload->>'ratio')::float) AS avg_ratio,
       AVG((payload->>'dropped')::int)  AS avg_dropped
FROM trajectory WHERE kind='compaction';

-- Fallback rate (→ 01): degraded retrieval paths
SELECT AVG(CASE WHEN payload->>'degraded'='true' THEN 1.0 ELSE 0.0 END)
FROM trajectory WHERE kind='context_assembly';
```

### 6.2 Cost Attribution

```sql
-- Cost by task, by model, by tenant — the three questions finance asks
SELECT t.session_id, e.model,
       SUM(e.cost_usd) AS usd, SUM(e.tokens_out) AS out_tok
FROM trajectory e JOIN trajectory t ON t.session_id = e.session_id AND t.kind='session_start'
WHERE e.cost_usd IS NOT NULL
GROUP BY t.session_id, e.model
ORDER BY usd DESC LIMIT 20;
```

The most common finding: **cost is not in the prompts, it is in the retry loops and the
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

```typescript
export function diffSessions(a: TrajectoryEvent[], b: TrajectoryEvent[]): string {
  const A = new Map(a.map(e => [e.seq, e])), B = new Map(b.map(e => [e.seq, e]));
  const lines: string[] = [];
  for (const seq of new Set([...A.keys(), ...B.keys()]).values()) {
    const x = A.get(seq), y = B.get(seq);
    if (!x) { lines.push(`+${seq} ${y!.kind} ${y!.payload.tool ?? ""}`); continue; }
    if (!y) { lines.push(`-${seq} ${x.kind} ${x.payload.tool ?? ""}`); continue; }
    if (JSON.stringify(x.payload) !== JSON.stringify(y.payload))
      lines.push(`~${seq} ${x.kind} ${x.payload.tool ?? ""} (${x.latencyMs}ms → ${y.latencyMs}ms)`);
  }
  return lines.join("\n");
}
```

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

```typescript
import { appendFile, open, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { ulid } from "ulid";
import { redactPayload, TrajectoryEventSchema } from "./schema";

const FSYNC_KINDS = new Set(["approval_verdict", "memory_write", "eval", "session_start", "session_end"]);
const MAX_PAYLOAD = 64_000;

export class TrajectoryStore {
  private seq = 0;
  private buffer: string[] = [];
  private timer?: NodeJS.Timeout;

  constructor(private root: string) {}

  /** Every module calls this. Never throws into the agent loop — a telemetry
   *  failure must not fail the task. Failures are counted and surfaced. */
  async append(e: Omit<TrajectoryEvent, "id" | "seq">): Promise<void> {
    try {
      const { payload, redactions } = redactPayload(e.payload);
      const ev = TrajectoryEventSchema.parse({
        ...e, id: `evt_${ulid()}`, seq: this.seq++, redactions,
        payload: JSON.stringify(payload).length > MAX_PAYLOAD ? { ref: blobRef(payload) } : payload,
      });
      const line = JSON.stringify(ev) + "\n";
      if (FSYNC_KINDS.has(ev.kind)) {
        await this.flush();
        const fh = await open(this.path(ev.sessionId), "a");
        await fh.appendFile(line); await fh.sync(); await fh.close();
      } else {
        this.buffer.push(line);
        this.timer ??= setTimeout(() => void this.flush(), 100);
      }
    } catch (err) { this.dropped++; this.lastError = err; }
  }

  async flush(): Promise<void> {
    clearTimeout(this.timer); this.timer = undefined;
    if (!this.buffer.length) return;
    const b = this.buffer; this.buffer = [];
    await mkdir(this.root, { recursive: true });
    await appendFile(this.path(this.currentSession), b.join(""), "utf8");
  }

  async close(): Promise<void> { await this.flush(); }
  path(sessionId: string) { return join(this.root, `${sessionId}.jsonl`); }
  dropped = 0; lastError?: unknown; currentSession = "";
}
```

</details>

### 8.2 Live Progress Projector

```typescript
/** Projects the event stream into a live UI state. Same stream, different view —
 *  the UI is a fold over the trajectory, not a parallel source of truth. */
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string; status: "running" | "waiting" | "done" | "failed";
}

export function project(e: TrajectoryEvent, prev: RunProgress): RunProgress {
  const next = { ...prev, stepsDone: prev.stepsDone + (e.kind === "tool_result" ? 1 : 0) };
  if (e.tokens) next.tokens += e.tokens.in + e.tokens.out;
  next.costUsd += e.costUsd ?? 0;
  if (e.kind === "plan") next.currentTask = (e.payload as any).firstPendingTask;
  if (e.kind === "approval_request") next.status = "waiting";
  if (e.kind === "approval_verdict") next.status = "running";
  if (e.kind === "error") next.lastError = e.error?.code;
  if (e.kind === "session_end") next.status = (e.payload as any).tasksDone === (e.payload as any).tasksTotal ? "done" : "failed";
  return next;
}
```

### 8.3 Debug Logger Adapter

```typescript
/** One-line human-readable trace, for `DEBUG=agent` runs. Same events, formatted. */
export function formatEvent(e: TrajectoryEvent): string {
  const t = `${String(e.seq).padStart(3, "0")} ${e.kind.padEnd(16)} ${e.actor.padEnd(12)}`;
  const detail = e.kind === "tool_call" ? `${e.payload.tool} ${JSON.stringify(e.payload.args).slice(0, 60)}`
    : e.kind === "tool_result" ? `exit=${e.payload.exitCode} ${e.latencyMs}ms ${e.payload.bytes}B`
    : e.kind === "eval" ? `score=${e.payload.score}`
    : e.kind === "compaction" ? `ratio=${e.payload.ratio} dropped=${e.payload.dropped}`
    : "";
  const cost = e.costUsd ? ` $${e.costUsd.toFixed(4)}` : "";
  return `${t} ${detail}${cost}`;
}
```

---

## 9. Testing Trajectory

### 9.1 Contract Tests

Run in CI. These catch the class of bug where a new module emits an event that breaks
every downstream query.

```typescript
import { TrajectoryEventSchema } from "./schema";

export function validateEmitter(name: string, evts: unknown[]): void {
  for (const e of evts) {
    const r = TrajectoryEventSchema.safeParse(e);
    if (!r.success) throw new Error(`${name} emitted invalid event: ${r.error.message}`);
  }
  const seqs = evts.map((e: any) => e.seq).sort((a: number, b: number) => a - b);
  seqs.forEach((s, i) => { if (s !== i) throw new Error(`${name} produced a seq gap at ${i}`); });
}
```

Also assert: every `tool_call` has a matching `tool_result`; every `tool_result.parentTaskId`
exists in the plan; no event's payload contains a secret pattern.

### 9.2 Replay Test Suite

```typescript
/** Deterministic steps must be byte-identical. LLM steps are compared by
 *  fingerprint + score tolerance. Anything else is a bug in the harness. */
export async function replayTest(cases: ReplayCase[]): Promise<{ name: string; drift: ReplayDiff[] }[]> {
  const out: { name: string; drift: ReplayDiff[] }[] = [];
  for (const c of cases) {
    const recorded = await loadSession(c.path);
    const fresh = await c.run();
    out.push({ name: c.name, drift: diffRun(recorded, fresh) });
  }
  return out;
}
```

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
that generalizes: **traces are not just logs, they are the raw material for evaluation
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

```typescript
span.setAttributes({
  "gen_ai.system": "anthropic",
  "gen_ai.request.model": "claude-sonnet-4-5",
  "gen_ai.usage.input_tokens": 12_480,
  "gen_ai.usage.output_tokens": 1_120,
  "gen_ai.agent.id": "agent:coder",
  "gen_ai.trajectory.session_id": "ses_44a",
});
```

### 10.4 OpenHands — Event Stream Runtime

OpenHands makes the event stream the runtime's interface: the agent emits
`Action`/`Observation` pairs, and every action is recorded as it executes rather than
afterwards. Design consequences:

1. **Recording is not a side effect — it is the loop.** You cannot "forget to log" because logging *is* how the loop communicates.
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

```typescript
// ── Event ─────────────────────────────────────────────────────────────────
export type EventKind =
  | "session_start" | "session_end" | "context_assembly" | "prompt"
  | "plan" | "plan_revision" | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write" | "delegate" | "message"
  | "approval_request" | "approval_verdict" | "compaction" | "checkpoint"
  | "eval" | "error";

export interface TrajectoryEvent {
  id: string; seq: number; sessionId: string; parentTaskId?: string; runId?: string;
  ts: number; kind: EventKind; actor: string; payload: unknown;
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number; model?: string; costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string; redactions?: number; tenantId: string;
}

export type NewEvent = Omit<TrajectoryEvent, "id" | "seq" | "redactions">;

// ── Store ──────────────────────────────────────────────────────────────────
export interface TrajectoryStore {
  append(e: NewEvent): Promise<void>;
  flush(): Promise<void>;
  load(sessionId: string): Promise<TrajectoryEvent[]>;
  tail(sessionId: string, fromSeq: number): AsyncIterable<TrajectoryEvent>;
}

// ── Derived views ──────────────────────────────────────────────────────────
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string;
  status: "running" | "waiting" | "done" | "failed";
}

// ── Fork / replay ──────────────────────────────────────────────────────────
export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}
export type ReplayDrift = "none" | "output" | "error" | "latency";
export interface ReplayDiff { step: number; kind: EventKind | string; drift: ReplayDrift }

// ── Redaction ──────────────────────────────────────────────────────────────
export interface RedactionResult<T> { payload: T; redactions: number }
export interface Redactor { redact(s: string): RedactionResult<string> }

// ── Retention ──────────────────────────────────────────────────────────────
export type RetentionTier = "hot" | "warm" | "cold" | "purged";
export interface RetentionPolicy {
  hotDays: number; warmDays: number; coldDays: number;
  inlineMaxBytes: number;             // > this → { ref } in warm tier
  tenantTtlDays?: number;             // GDPR
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface ReplayCase {
  name: string; path: string;
  run(): Promise<TrajectoryEvent[]>;
  expectDeterministic: EventKind[];
}
```

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

1. **Append-only.** Events are facts; facts are not edited. Corrections are new events (`plan_revision`), never mutations.
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
- Turn every failed run into a curated eval case; it is already in the right shape.
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

- **Trajectory-aware evaluation.** Rubrics that score *the path* — did it check the test before declaring success? — rather than the final answer. The data is already there; it is a query problem.
- **Automatic drift detection.** A trajectory embedder that flags runs structurally unlike your known-good population before a human looks at them.
- **Causal attribution.** Given a bad outcome, identify the earliest decision that caused it. This is the frontier: not "what happened" but "which turn do I change".

### 16.2 Privacy-Preserving Telemetry

- **On-device redaction with differential privacy aggregates** for the metrics you keep globally while the payloads stay tenant-local.
- **Confidential-compute trace sinks** so even the observability vendor cannot read the trajectory — the same SEV-SNP/TDX pattern as `12-sandbox-execution` §16.3.

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
- `08-task/README.md` §11 — the task producer (`parentTaskId` source)
- `11-evaluation/README.md` §15 — the eval consumer (trajectory eval, human calibration)
- `12-sandbox-execution/README.md` §9 — the `sandbox` event producer
- `14-compaction-context/README.md` — the `compaction` event producer
- `15-approval-gates/README.md` §6 — the audit consumer (`approval_verdict`)

---

*Document: XIII. Trajectory & Observability — HARNESS ENGINEERING EDITION*
*Cross-cutting module · the spine of harness observability*
*Last updated: 19/07/2026*
*Author: AI Knowledge Repository*
