# 🗜️ Harness 14. Context Compaction

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Is Compaction Non-Optional?](#why-is-compaction-non-optional)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Definitions & Vocabulary](#1-definitions--vocabulary)
>   - [1.1 Core Terms](#11-core-terms)
>   - [1.2 The Two Families: Summarization vs Pruning](#12-the-two-families-summarization-vs-pruning)
> - [2. Trigger Policy](#2-trigger-policy)
>   - [2.1 Why 70% and Not 90%](#21-why-70-and-not-90)
>   - [2.2 Trigger Strategies](#22-trigger-strategies)
> - [3. The Pin Set — What Must Survive](#3-the-pin-set--what-must-survive)
>   - [3.1 Pinned vs Evictable](#31-pinned-vs-evictable)
>   - [3.2 The Pin Set](#32-the-pin-set)
> - [4. Utility-Based Pruning](#4-utility-based-pruning)
>   - [4.1 Why Recency-Only Fails](#41-why-recency-only-fails)
>   - [4.2 Scoring Trajectory-Aware Utility](#42-scoring-trajectory-aware-utility)
>   - [4.3 Collapse, Don't Delete](#43-collapse-dont-delete)
> - [5. The Resume Block](#5-the-resume-block)
>   - [5.1 Format](#51-format)
>   - [5.2 Quality Bar](#52-quality-bar)
> - [6. The Compaction↔Memory Contract](#6-the-compactionmemory-contract)
>   - [6.1 The Boundary](#61-the-boundary)
>   - [6.2 The Most Commonly Broken Contract in Production](#62-the-most-commonly-broken-contract-in-production)
> - [7. Compaction-Safe Prompts](#7-compaction-safe-prompts)
>   - [7.1 Header / Body / Footer](#71-header--body--footer)
>   - [7.2 What Summarizers Drop](#72-what-summarizers-drop)
> - [8. TypeScript Implementation](#8-typescript-implementation)
>   - [8.1 Types](#81-types)
>   - [8.2 shouldCompact + compact()](#82-shouldcompact--compact)
>   - [8.3 Trajectory Utility Scorer](#83-trajectory-utility-scorer)
>   - [8.4 Resume Block Builder](#84-resume-block-builder)
>   - [8.5 Memory Write-Back](#85-memory-write-back)
> - [9. Testing Compaction](#9-testing-compaction)
>   - [9.1 Invariant Tests](#91-invariant-tests)
>   - [9.2 The Contract Test That Matters Most](#92-the-contract-test-that-matters-most)
>   - [9.3 Quality Regression Suite](#93-quality-regression-suite)
> - [10. Real-World Case Studies](#10-real-world-case-studies)
>   - [10.1 Claude Code — /compact and Auto-Compact](#101-claude-code--compact-and-auto-compact)
>   - [10.2 Aider — Repository Map + History Digest](#102-aider--repository-map--history-digest)
>   - [10.3 Devin — Long-Run Context Management](#103-devin--long-run-context-management)
>   - [10.4 Letta / MemGPT — Tiered Memory as Virtual Context](#104-letta--memgpt--tiered-memory-as-virtual-context)
>   - [10.5 Lost in the Middle — The Research Behind Pinning](#105-lost-in-the-middle--the-research-behind-pinning)
> - [11. TypeScript Interfaces for Compaction](#11-typescript-interfaces-for-compaction)
> - [12. Design Principles for Compaction](#12-design-principles-for-compaction)
>   - [12.1 SOLID for Context Management](#121-solid-for-context-management)
>   - [12.2 Six Design Principles](#122-six-design-principles)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do-)
>   - [13.2 DON'T ❌](#132-dont-)
> - [14. Anti-Patterns & Solutions](#14-anti-patterns--solutions)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Future Trends in Compaction](#16-future-trends-in-compaction)
> - [References](#references)
>
> **Cross-cutting module.** Compaction is the reason an agent can run for hours instead of
> minutes. It owns the boundary between *transient context* (→ 02) and *durable memory*
> (→ 03) — the contract between those two is violated more often than any other in
> production systems.

---

### Opening Story

It's turn 47. The agent is deep in a refactor: 31 tool calls, four files rewritten, two
test suites run, one confusing stack trace buried somewhere in the middle. The context
window is at 96%. The next tool result will be 4,000 tokens and it does not fit.

Now the team has three bad options and no good one:

1. **Let it fail.** The run dies at turn 47 with a context-length error. The user sees
   "something went wrong" after 20 minutes.
2. **Naive truncation.** Drop the oldest messages. The agent loses the task
   specification it was given in turn 1, re-reads a file it already read in turn 12
   (because the *result* is gone but the *edit* is not), and confidently produces a
   patch that undoes its own work from turn 30.
3. **Summarize everything equally.** Compress the whole transcript into a paragraph.
   The paragraph mentions the stack trace and omits the task definition, so the agent
   solves the wrong problem fluently.

**None of these are "compaction".** Compaction is a *policy*: a trigger, a pin set of
things that must never be evicted, a utility function for deciding what goes next, and a
resume block that reconstructs the run's state in a fixed structure. Get those four
right and turn 47 is boring. Get them wrong and the failure is invisible — the run
*completes*, it just completes the wrong task.

### Why Is Compaction Non-Optional?

> *"Any agent that cannot survive its own context window is a demo, not a product."*

#### The Arithmetic

| Budget | Input per turn | Turns before exhaustion | With 70% trigger + compaction |
|--------|----------------|------------------------|----------------------------------|
| 200k (large) | ~6k | ~33 | unbounded |
| 128k (typical) | ~4k | ~32 | unbounded |
| 32k (small/local) | ~2k | ~16 | unbounded |

**Unbounded** is the point. Compaction is not an optimization; it is the mechanism that
converts a fixed-size context into an arbitrarily long run. It is also what makes
`07-workflow` checkpoint-resume viable (→ 07 §13), `09-multi-agent` sub-agent handoffs
possible (→ 09 §16.2), and the `10-automation` loop budget enforceable (→ 10 §17.3) —
each of those needs a run that outlives one context window.

#### Second-Order Effects

- **Cost.** Compaction reduces per-turn input tokens dramatically on long runs, because a 60 KB resume block replaces 180 KB of history. Teams routinely see 40–70% cost reduction on runs over 30 turns.
- **Quality.** Compaction *can* hurt quality — that is what §5–7 are about. Done badly it is strictly worse than no compaction, because the model confidently reasons on a lossy summary.
- **Auditability.** Compaction produces a `compaction` event (→ 13) recording exactly what was kept and evicted. A harness where you cannot reconstruct what the model lost is a harness you cannot debug.

## Overview

> **📌 Core Concept**
>
> - **Concept:** Compaction is **triggered summarization**: when context exceeds a threshold, low-value spans are replaced by a structured resume block instead of hitting the token ceiling. **Pruning** is its companion — deciding *what* goes first by utility, not by recency.
> - **Analogy:** Packing a small suitcase for a long trip. When it's full you don't toss things at random — you have rules (hygiene kit stays, old receipts go) and you leave a note listing what you removed.
> - **Why it matters:** Every long agent run dies without compaction: context overflow, lost-in-the-middle accuracy collapse, and a 3–5× token bill from resending dead tool output. Compaction at 70% keeps runs alive indefinitely at flat cost.

**Context Compaction** is what lets a fixed context window support an unbounded run. It
is the most under-engineered part of most agent harnesses, and the most expensive to
get wrong.

```
BEFORE compaction (188k of 200k budget)
┌──────────────────────────────────────────────────────────────┐
│ [system] [goal] [turn 1..46: 31 tool calls, 4 edits, tests]  │
│ ▲ pinned  ▲ everything here is evictable — 178k of it        │
└──────────────────────────────────────────────────────────────┘
                    │ trigger: used > 70% budget
                    ▼
AFTER compaction (74k of 200k budget)
┌──────────────────────────────────────────────────────────────┐
│ [system] [goal] [PIN: 3 open decisions] [PIN: last failure] │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ RESUME BLOCK (280 tok)                                  │ │
│ │ Goal: refactor auth middleware to use shared session    │ │
│ │ Decisions: session store = redis; kept jwt compat shim  │ │
│ │ Open: [t5] update 3 call sites; [t6] run integration    │ │
│ │ Repro: npm test -- auth → FAIL test_refresh_rotation    │ │
│ │ Next: fix refresh rotation, then t5, t6                │ │
│ │ Evicted: [span ids 7,12,18,22,29,31,…,46] (74 spans)    │ │
│ └──────────────────────────────────────────────────────────┘ │
│ [last 3 turns verbatim] ← recency tail stays readable        │
└──────────────────────────────────────────────────────────────┘
```

**Four components, and a missing one is a bug:**

| # | Component | Failure if missing |
|---|-----------|-------------------|
| 1 | **Trigger** | Run dies at the ceiling |
| 2 | **Pin set** | Task definition evicted; agent solves the wrong problem |
| 3 | **Utility ranking** | FIFO eviction throws away the goal, keeps yesterday's `ls` |
| 4 | **Resume block** | Agent wakes up with no state, re-reads everything, bill triples |
| 5 | **Memory write-back** *(the commonly-missed one)* | Decisions vanish with the evicted span and are never persisted |

## Contents

| # | Topic | Description |
|---|-------|-------------|
| 1 | [Definitions](#1-definitions--vocabulary) | Vocabulary and the two families |
| 2 | [Trigger Policy](#2-trigger-policy) | When, and why 70% |
| 3 | [Pin Set](#3-the-pin-set--what-must-survive) | What must never be evicted |
| 4 | [Utility Pruning](#4-utility-based-pruning) | Trajectory-aware eviction |
| 5 | [Resume Block](#5-the-resume-block) | Format and quality bar |
| 6 | [Compaction↔Memory Contract](#6-the-compactionmemory-contract) | The most-broken contract |
| 7 | [Compaction-Safe Prompts](#7-compaction-safe-prompts) | Surviving summarization |
| 8 | [Implementation](#8-typescript-implementation) | Runnable compaction |
| 9 | [Testing](#9-testing-compaction) | Invariants + the contract test |
| 10 | [Case Studies](#10-real-world-case-studies) | Claude Code, Aider, Devin, Letta, lost-in-the-middle |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-for-compaction) | Full type surface |
| 12 | [Design Principles](#12-design-principles-for-compaction) | SOLID for context |
| 13 | [Best Practices](#13-best-practices) | DO / DON'T |
| 14 | [Anti-Patterns](#14-anti-patterns--solutions) | Common failures |
| 15 | [Production Checklist](#15-production-checklist) | Ship gate |
| 16 | [Future Trends](#16-future-trends-in-compaction) | 2026-2028 |

---

## 1. Definitions & Vocabulary

### 1.1 Core Terms

| Term | Definition | Fails when… |
|------|-----------|-------------|
| **Auto-compaction** | Summarization triggered by `used > threshold`; evictable spans are replaced by a resume summary | trigger missing → run dies |
| **Resume block** | Struct ≤300 tokens: `Goal / Decisions / Open / Repro / Next` + `evicted_span_ids` | unconstrained → grows until it is the problem |
| **Trajectory-aware pruning** | Eviction order derived from the execution graph (keep the critical path, drop dead branches) | recency-only → drops the goal |
| **Compaction ratio** | `tokens_before ÷ tokens_after` — a health metric | <1.5 on a large context → the summarizer is failing |
| **Pin set** | The non-evictable core: system, goal, constraints, open diff, last failure | absent → task spec evicted |
| **Write-back** | Persisting resume + decisions + open items to memory *before* they leave context | skipped → decisions are lost forever |
| **Lost in the middle** | Accuracy degrades when relevant info sits mid-context | ignored → pinning is arbitrary |

### 1.2 The Two Families: Summarization vs Pruning

They are complements, not alternatives, and confusing them is the root of most bad
implementations.

| | **Summarization** | **Pruning** |
|---|------------------|------------|
| **What** | Compress a span into prose | Drop a span entirely |
| **When** | Span is needed but too big | Span is not needed |
| **How** | Model summarizes, or deterministic template | Utility score + evict |
| **Cost** | LLM call (~1–3 s) or template | Free |
| **Risk** | Loss of detail, hallucinated summary | Loss of information that *looked* unneeded |
| **Applied to** | Old tool output, long file reads | Failed branches, superseded diffs, chit-chat |

**The order matters:** prune first (free, no information loss for dead spans), then
summarize what remains oversized (expensive, lossy). Teams that summarize first and
prune never pay almost 40% less and keep more information.

---

## 2. Trigger Policy

### 2.1 Why 70% and Not 90%

```
100% ──── hard ceiling: the request itself fails. Unrecoverable, no logging.
 90% ──── "close enough" — but the next tool result routinely exceeds 10% of budget.
 70% ──── leaves 30% headroom: next 2-3 turns of tool results fit without re-compacting.
 50% ──── too eager: 2 compactions per run, quality cost, wasted LLM calls.
```

The failure at 90% is specific and common: a single `read_file` of a 30 KB file
consumes 8% of a 200k window in one step. Trigger at 90%, get one 8% result, and you
are at 98% — now the *next* result overflows and you compact again, mid-task, with
less room to summarize. Compaction under pressure is exactly when you cannot afford
lossy summarization.

**The rule: trigger when you can still afford to summarize well.**

### 2.2 Trigger Strategies

| Strategy | Rule | Use when |
|----------|------|----------|
| **Threshold** | `used / budget > 0.70` | default, simple, predictable |
| **Turn-count** | `turns > 20` | token estimates are unreliable; cheap backstop |
| **Growth-rate** | compact when `used` grew >25% in the last 3 turns | runaway tool loops |
| **Task-boundary** | compact between tasks, not inside one | long multi-task sessions; keeps a task's reasoning intact |
| **Size-of-next** | compact when `est(next_result) > headroom` | tight budgets (32k) |

Production recommendation: **threshold OR turn-count**, whichever fires first, plus
task-boundary compaction when the plan (→ 08) has a natural seam. Growth-rate is a
useful alarm for "this run is in a loop" (→ 10 §17.3).

**Never let the model decide.** Compaction is a harness policy computed from measured
token counts. A model asked "should we compact?" will answer "no, I'm fine" while
holding 195k tokens.

---

## 3. The Pin Set — What Must Survive

### 3.1 Pinned vs Evictable

The pin set is the answer to "what would make the run wrong if it disappeared?" Anything
whose absence changes the *task* rather than the *taste* is pinned.

| Pinned (never evict) | Evictable (in eviction order) |
|---------------------|------------------------------|
| System prompt | Tool stdout older than 3 turns |
| Task spec + definition of done | File versions superseded by a later edit |
| User's most recent instruction | Retrieved chunks with score <0.3 |
| Diffs currently being edited | Chit-chat, greetings, meta-commentary |
| Invariants / constraints from the plan | Repeated `ls`/`cat` of the same file |
| Last failure signal for the active loop | Abandoned hypothesis branches |
| Active approval state (→ 15) | Expired, resolved approvals |
| Output schema the model must produce | History of a completed sub-task |
| Pointer to durable memory | Token-heavy dead tool output (summarized, not dropped) |

**The subtlety:** "the last failure signal" is pinned *for the active loop only*. Once
the loop is resolved, that failure becomes evictable. Pinning it forever means your
pin set grows monotonically and eventually exceeds the budget — which is its own
failure mode, and a quiet one.

### 3.2 The Pin Set

```typescript
export interface PinSet {
  tenantId: string;                   // routing + consistency key (→ 05 §17.5)
  system: true;                       // always
  goal: true;                         // task spec + definition of done
  invariants: string[];               // ≤5 constraints from the plan (→ 05 §17.5)
  activeDiffPaths: string[];          // files with uncommitted edits
  lastUserMessage: true;              // most recent instruction wins
  activeLoopFailure?: { cmd: string; error: string };   // only while unresolved
  pendingApprovals: string[];         // gate keys awaiting verdict (→ 15)
  schema: true;                       // the shape the final answer must take
}

export function isPinned(span: ContextSpan, pins: PinSet, planState: PlanState): boolean {
  if (span.role === "system" || span.kind === "goal" || span.kind === "schema") return true;
  if (span.kind === "user" && span.id === pins.lastUserMessage) return true;
  if (span.kind === "invariant") return true;
  if (span.kind === "diff" && pins.activeDiffPaths.includes(span.path!)) return true;
  if (span.kind === "failure" && planState.activeLoopUnresolved) return true;
  if (span.kind === "approval" && pins.pendingApprovals.includes(span.gateKey!)) return true;
  return false;
}
```

**Rule: the pin set is derived, not hand-maintained.** It is computed from the plan, the
active loop, and the pending gate list — so it shrinks automatically as work completes
instead of accumulating.

---

## 4. Utility-Based Pruning

### 4.1 Why Recency-Only Fails

FIFO / oldest-first eviction assumes value decays with age. In agent trajectories it
does not:

```
turn  1  [goal]              ← 2k tokens, pinned, 4 hours old
turn  2  [plan]              ← 1k tokens, pinned
turn  3  [read package.json] ← 3k tokens, useless now
turn  4  [tool output 40KB]  ← needed for turn 44
turn 12  [key constraint: "no new deps"]  ← 80 tokens, still binding
turn 44  [edit]              ← pinned
```

Dropping the oldest non-pinned spans evicts turn 4's output and turn 12's constraint —
one irrelevant, one fatal — and keeps the three `ls` calls from turns 38–40 because
they are recent. The agent then re-derives a dependency that violates a standing
constraint.

### 4.2 Scoring Trajectory-Aware Utility

```
utility = 0.30·recency + 0.40·structural_reachability + 0.30·failure_signal
```

| Term | Meaning | Implementation |
|------|---------|----------------|
| `recency` | Normalized age: `exp(-turns_old / 12)` | cheap, prevents unbounded staleness |
| `structural_reachability` | Is this span on the current critical path to the goal? | BFS over the plan graph (→ 04) from the active task; a span feeding a *pending* node scores high, a span feeding a *completed* node scores low |
| `failure_signal` | Does this span carry the error the active loop is chasing? | string/trace match against the loop's last error (see §8.3) |

Then evict ascending utility, never crossing the budget. Crucially, **this ordering
operates on the plan graph, not on the message list** — which is why it needs `08` and
`04` to be useful.

```typescript
/** Reference implementation: §8.3. The loop's last-error signal is worth 0.30 —
 *  without it, a run stuck in a retry loop keeps scoring every span identical. */
export function utility(span: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - span.turn) / 12);
  const serves = span.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // still needed
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // branch is done
    : 0.4;                                                       // parallel / unknown
  const failure = loop?.unresolved && span.text?.includes(firstLine(loop.error)) ? 1 : 0;
  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}
```

### 4.3 Collapse, Don't Delete

Two refinements that separate a good implementation from a working one:

1. **Collapse identical retries.** Three identical `npm test` failures become
   `retried 3×, last_err: E2BIG at test_refresh_rotation`. The information that
   matters (it failed, here's why, it was retried) survives at 1/30th the cost.
2. **Summarize before dropping dead branches.** A completed branch is not *worthless* —
   it explains why the agent is now in a different place. One line: `branch t3
   (vector cache) rejected: adds 400ms p99`. Cheap, and it prevents the agent from
   re-exploring it.

```
turns 38,39,40:  npm test (exit 1)  ──┐
turns 41,42,43:  npm test (exit 1)  ──┼──▶  [retried 6×, last_err: E2BIG @ test_refresh_rotation]
turn  44:        npm test (exit 1)  ──┘         (from turn 38, 18k tokens → 24 tokens)
```

---

## 5. The Resume Block

### 5.1 Format

Fixed keys, hard budget, machine-checkable:

```
Goal:<one line — the task, not the plan>
Decisions:[D1: …][D2: …][D3: …]        ≤5, each ≤25 words
Open:[t5: …][t6: …]                    pending tasks with IDs (→ 08)
Repro:<exact command + last error line>
Next:<the single next action>
Invariants:[…]                          the ≤5 pinned constraints
Evicted:[span-id list]                  for audit + reconstruction
```

**Why the keys are fixed:** the resume block is re-read by *code*, not just by the
model. A parser extracts `Open[]` to rebuild the pending task list, `Repro` to seed the
retry, and `Evicted[]` to write back to memory and to emit the audit event. Free-form
prose breaks all three.

### 5.2 Quality Bar

A resume block is good when a **fresh agent with an empty context** can pick up the run
and do the next step correctly. Test it exactly that way:

```typescript
/** The acceptance test for a resume block: can a cold agent continue? */
export function resumeIsSufficient(block: ResumeBlock, nextAction: string): boolean {
  return block.goal.length > 0                                    // no goal, no task
      && block.open.length > 0                                    // must know what is still open
      && block.repro.command.length > 0                           // must be able to re-trigger the bug
      && block.next.length > 0                                    // must know what to do next
      && countTokens(block) <= 300;                               // hard budget
}
```

A block that says "we were refactoring authentication and hit some issues" fails every
one of these lines. It feels informative and is useless — this is the most common way
compaction silently destroys a run.

---

## 6. The Compaction↔Memory Contract

### 6.1 The Boundary

| Transient — context owns it (→ 02) | Durable — memory owns it (→ 03) |
|--------------------------------------|----------------------------------|
| Raw tool stdout | Pinned facts |
| Retrieved chunk bodies | Decisions and their rationale |
| Superseded file versions | Open TODOs |
| Chit-chat | User preferences |
| Dead branches | **The resume block** |
| — | Invariants / constraints |

The line is not "important vs unimportant". It is **"will this still be needed after
this run?"** Tool stdout from turn 4 might be needed at turn 44, but not after turn
60 — that is context's job. A decision made at turn 12 will be needed by a *different
run* next week — that is memory's job.

### 6.2 The Most Commonly Broken Contract in Production

**The failure:** compaction evicts a span, and the information inside it was never
persisted. Next turn, the model has no idea why it made the decision it made, and
re-derives it differently. The run *succeeds* and the codebase is subtly inconsistent
with the design the user agreed to forty minutes ago.

**The rule:** write back **before** evicting. Not after, not "later" — before. The
sequence is:

```
1. select spans to evict (utility ascending)
2. extract durable content: decisions, open items, invariants, user preferences
3. persist to memory (tenant + task scoped)          ← fsync (→ 13)
4. emit compaction event: { keptIds, evictedIds, ratio, resumeHash }
5. replace evicted spans with the resume block
6. continue the run
```

Step 3 failing must abort step 5. Not log a warning — abort. A compaction that loses a
decision has produced a run that cannot be trusted, and the cheapest way to make that
impossible is to make it fail loudly.

**The verification test** is in §9.2, and it is the single most valuable test in this
module: kill the memory backend, run a compaction, and assert the run refuses to
proceed.

---

## 7. Compaction-Safe Prompts

### 7.1 Header / Body / Footer

Compaction is lossy, so design the prompt to survive it:

```
[HEADER — invariants, always kept]
  You are refactoring the auth middleware onto a shared session store.
  Invariants: (1) no new runtime dependencies (2) JWT v1 tokens must still validate
  (3) no changes to the public API surface.
  Output: a unified diff + a one-paragraph migration note.

[BODY — retrieved context, evicted freely]
  … 12 chunks, 4 file bodies, 31 tool outputs …

[FOOTER — restated invariants]
  Reminder before you answer: no new deps; keep JWT v1 compat; output must be a diff
  followed by a migration note.
```

**The empirical basis** is the lost-in-the-middle result (§10.5): models attend most
reliably to the beginning and end of a long context. Putting the invariants in both
places means a summarizer that keeps only the head *and* the tail still preserves the
constraints — and a summarizer that keeps 80% of tokens preserves them with near-certainty.

### 7.2 What Summarizers Drop

Knowing the failure modes tells you what to pin:

| Commonly dropped | Mitigation |
|-----------------|------------|
| Negative statements ("do NOT add deps") | Put in HEADER + FOOTER, verbatim |
| Numbers (timeouts, counts, limits) | Pin exact values; never paraphrase |
| IDs and names (task ids, file paths) | Keep raw in `Open[]`, not in prose |
| Tool output structure (which field failed) | `Repro` keeps the raw error line |
| Uncertainty ("I think", "probably") | Pin the *last user instruction* which usually carries it |
| Ordering constraints (X before Y) | `Next` states order explicitly |

The general rule: **paraphrase is where precision dies.** A summarizer asked to
"compress" will write "the timeout is about 30 seconds" instead of
`timeoutMs: 30000`. Pin the literal value; let the summary explain around it.

---

## 8. TypeScript Implementation

### 8.1 Types

```typescript
export interface ContextSpan {
  id: string;                    // span_01H…  — the unit of eviction
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number;
  tokens: number;
  text?: string;
  path?: string;                 // for diff spans
  tool?: string;
  gateKey?: string;              // for approval spans
  producedFor?: string[];        // task ids this span serves (plan graph, → 08)
  keep?: boolean;                // hard pin, overrides scoring
}

export interface ResumeBlock {
  goal: string;
  decisions: string[];           // ≤5
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string;
  invariants: string[];
  evicted: string[];             // span ids
}
```

### 8.2 shouldCompact + compact()

<details>
<summary>TypeScript Code — trigger + pin + utility prune + resume (Click to expand/collapse)</summary>

```typescript
export const COMPACT_AT = 0.70, RESUME_BUDGET = 300, MAX_TURNS = 20;

export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}

export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock;
  ratio: number; dropped: string[]; writeBack: DurableExtract;
}

export function compact(
  spans: ContextSpan[], budget: number, goal: string,
  pins: PinSet, plan: PlanGraph, activeLoop: ActiveLoop | null,
): CompactOutcome {
  // 1. Pin set first — never a candidate for eviction, no matter the score.
  const pinned = spans.filter(s => isPinned(s, pins, plan.state));
  const now = maxTurn(spans);
  const activeTask = plan.activeTask ?? null;   // the task the resume block must continue

  // 2. Everything else ranked by trajectory-aware utility, highest first.
  const rest = spans.filter(s => !isPinned(s, pins, plan.state))
    .map(s => ({ s, u: utility(s, plan, activeLoop, now) }))
    .sort((a, b) => b.u - a.u);

  // 3. Fill the budget from the top down.
  let used = pinned.reduce((n, s) => n + s.tokens, 0) + RESUME_BUDGET;
  const kept = [...pinned];
  for (const { s } of rest) if (used + s.tokens <= budget) { kept.push(s); used += s.tokens; }

  // 4. Collapse repeated identical failures instead of dropping them wholesale.
  const { kept: collapsed, resumeHints } = collapseRetries(kept);

  // 5. Extract durable content from what is about to go.
  const dropped = spans.filter(s => !collapsed.some(k => k.id === s.id));
  const writeBack = extractDurable(dropped, goal);

  // 6. Structured resume block, built from durable content + plan state.
  const resume: ResumeBlock = {
    goal,
    decisions: writeBack.decisions.slice(0, 5),
    open: plan.pending(activeTask).map(t => ({ taskId: t.id, title: t.title })),
    repro: activeLoop
      ? { command: activeLoop.command, error: firstLine(activeLoop.error) }
      : { command: plan.reproCommand(activeTask), error: plan.lastError(activeTask) },
    next: plan.nextAction(activeTask),
    invariants: pins.invariants,
    evicted: dropped.map(s => s.id),
  };
  resumeHints.forEach(h => resume.decisions.push(h));   // "retried 6×, last_err: …"

  return {
    kept: collapsed, resume, writeBack,
    dropped: dropped.map(s => s.id),
    ratio: totalTokens(spans) / (used || 1),
  };
}
```

</details>

### 8.3 Trajectory Utility Scorer

```typescript
export interface ActiveLoop { command: string; error: string; unresolved: boolean }

/** 0.30 recency + 0.40 structural reachability + 0.30 failure signal.
 *  The middle term is why compaction needs the plan graph (→ 04/08): it knows
 *  which spans still feed a *pending* node. */
export function utility(s: ContextSpan, plan: PlanGraph, loop: ActiveLoop | null, now: number): number {
  const recency = Math.exp(-(now - s.turn) / 12);

  const serves = s.producedFor ?? [];
  const reachable = serves.length === 0 ? 0.4
    : serves.some(t => plan.pendingIds.includes(t))      ? 1.0    // still needed
    : serves.every(t => plan.completedIds.includes(t))    ? 0.1    // branch is done
    : 0.4;                                                       // parallel / unknown

  const failure = loop?.unresolved && s.text?.includes(firstLine(loop.error)) ? 1 : 0;

  return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
}

/** N identical failed calls → 1 line. 18k tokens → 24. */
export function collapseRetries(spans: ContextSpan[]): { kept: ContextSpan[]; resumeHints: string[] } {
  const groups = new Map<string, ContextSpan[]>();
  for (const s of spans.filter(s => s.kind === "tool_output" || s.kind === "failure")) {
    const key = `${s.tool}:${s.kind}`;
    (groups.get(key) ?? groups.set(key, []).get(key)!).push(s);
  }
  const hints: string[] = [];
  const drop = new Set<string>();
  for (const [, g] of groups) {
    if (g.length < 3) continue;
    const last = g[g.length - 1]!;
    drop.add(last.id);
    for (const s of g.slice(0, -1)) drop.add(s.id);
    hints.push(`retried ${g.length}× (${g[0]!.turn}→${last.turn}): ${firstLine(last.text ?? "")}`);
  }
  return { kept: spans.filter(s => !drop.has(s.id)), resumeHints: hints };
}
```

### 8.4 Resume Block Builder

```typescript
export function buildResume(o: {
  goal: string; decisions: string[]; pending: Task[]; lastCmd: string; lastErr: string;
  invariants: string[]; evicted: string[];
}): ResumeBlock {
  const b: ResumeBlock = {
    goal: o.goal.slice(0, 200),
    decisions: o.decisions.slice(0, 5).map(d => d.slice(0, 200)),
    open: o.pending.map(t => ({ taskId: t.id, title: t.title.slice(0, 80) })),
    repro: { command: o.lastCmd.slice(0, 200), error: firstLine(o.lastErr).slice(0, 200) },
    next: o.pending[0] ? `Continue with ${o.pending[0].id}: ${o.pending[0].title}` : "Summarize and hand off",
    invariants: o.invariants.slice(0, 5),
    evicted: o.evicted,
  };
  const t = countTokens(b);
  if (t > RESUME_BUDGET) {                                  // hard budget, enforced
    b.decisions = b.decisions.slice(0, 3);
    b.invariants = b.invariants.slice(0, 3);
    b.open = b.open.slice(0, 8);
    b.evicted = b.evicted.slice(0, 40);
  }
  return b;
}

export function renderResume(b: ResumeBlock): string {
  return [
    `Goal: ${b.goal}`,
    `Decisions: ${b.decisions.map(d => `[${d}]`).join("") || "[none]"}`,
    `Open: ${b.open.map(t => `[${t.taskId}: ${t.title}]`).join("") || "[none]"}`,
    `Repro: ${b.repro.command} → ${b.repro.error}`,
    `Next: ${b.next}`,
    `Invariants: ${b.invariants.join(" | ")} || "(none declared)"`,
    `Evicted: [${b.evicted.join(",")}]`,
  ].join("\n");
}
```

### 8.5 Memory Write-Back

```typescript
/** MUST run before the evicted spans are dropped. A failure here must abort the
 *  compaction — a run that silently loses a decision is worse than a run that
 *  stops with a clear error. */
export async function writeBackAndCompact(
  spans: ContextSpan[], budget: number, memory: MemoryStore, traj: TrajectorySink,
  pins: PinSet, plan: PlanGraph, loop: ActiveLoop | null, goal: string,
): Promise<CompactOutcome> {
  const o = compact(spans, budget, goal, pins, plan, loop);

  const facts = o.writeBack.facts.map(f => ({ ...f, tenantId: pins.tenantId, taskId: plan.activeTask }));
  await memory.persist(facts, { fsync: true });          // durable BEFORE eviction

  await traj.append({                                       // → 13
    kind: "compaction", parentTaskId: plan.activeTask,
    payload: { keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio,
               resumeHash: hash(renderResume(o.resume)), factsWritten: facts.length },
    tokens: { in: totalTokens(spans), out: countTokens(o.resume) },
  });

  return o;
}
```

---

## 9. Testing Compaction

### 9.1 Invariant Tests

```typescript
export function assertInvariants(o: CompactOutcome, budget: number): void {
  const keptIds = new Set(o.kept.map(s => s.id));

  for (const p of PINNED_KINDS)                                            // (1) pins survive
    if (o.dropped.some(id => kindOf(id) === p)) throw new Error(`evicted pinned ${p}`);

  if (totalTokens(o.kept) > budget) throw new Error("over budget");       // (2) fits
  if (countTokens(o.resume) > RESUME_BUDGET) throw new Error("resume too big");
  if (!resumeIsSufficient(o.resume, o.resume.next)) throw new Error("resume insufficient");
  if (o.resume.evicted.length !== o.dropped.length) throw new Error("audit ids mismatch");
  if (o.ratio < 1.2) throw new Error(`weak ratio ${o.ratio.toFixed(2)}`);  // (3) actually compacted
  for (const s of o.kept) if (!keptIds.has(s.id)) throw new Error("kept/evicted overlap");
}
```

Run these on **every** recorded trajectory that hits a compaction, in nightly CI. Real
trajectories catch the edge cases synthetic ones never do.

### 9.2 The Contract Test That Matters Most

```typescript
/** If memory is down, compaction MUST NOT silently proceed. */
it("refuses to evict unpersisted decisions", async () => {
  const spans = realTrajectorySpans();                     // 40 messages incl. 4 decisions
  const memory = brokenMemoryStore();                     // persist() always throws
  await expect(writeBackAndCompact(spans, 12_000, memory, sink, pins, plan, null, goal))
    .rejects.toThrow(/memory unavailable/);
  expect(spans.length).toBe(40);                           // nothing was evicted
});

it("a cold agent can continue from the resume block alone", async () => {
  const o = await writeBackAndCompact(realTrajectorySpans(), 12_000, mem, sink, pins, plan, loop, goal);
  const cold = await runAgent({ context: [systemPrompt, renderResume(o.resume)], tools });
  const warm = await runAgent({ context: originalSpans, tools });
  expect(await nextActionOf(cold)).toBe(await nextActionOf(warm));   // same next move
});
```

The second test is the real acceptance criterion for the whole module. It is also the
test most teams skip, and it is the one that would have caught the turn-47 failure
described at the top.

### 9.3 Quality Regression Suite

Track, per compaction, whether the run still succeeds. If quality drops after
compaction, the pin set is wrong — and this is the measurement that finds it:

```sql
SELECT s.kind, AVG(e.payload->>'score') AS score_after_compaction, COUNT(*) AS runs
FROM trajectory c
JOIN trajectory e ON e.session_id = c.session_id AND e.kind = 'eval'
JOIN trajectory s ON s.session_id = c.session_id AND s.kind = 'session_start'
WHERE c.kind = 'compaction'
GROUP BY s.kind ORDER BY score_after_compaction;
```

A specific run that fails only when a compaction happened immediately before the
failure is the strongest possible signal that the pin set is missing something.

---

## 10. Real-World Case Studies

### 10.1 Claude Code — /compact and Auto-Compact

Anthropic's coding agent exposes compaction as both a **user command** (`/compact`) and
an **automatic trigger** at high context utilization. Three design choices worth
adopting:

1. **Manual and automatic paths share one implementation.** Users who hit the problem
   manually get the same quality the automatic path produces — no second-class
   experience, and one code path to test.
2. **The user can see and control the budget.** Exposing context utilization makes
   compaction a visible part of the workflow rather than an invisible mutation.
3. **Compaction is presented as a checkpoint.** Users understand "context was
   compacted; here's what I remember" because it is phrased like a save point, not a
   hidden truncation.

### 10.2 Aider — Repository Map + History Digest

Aider's `repo map` is the purest form of the pin set: a compact, always-present index
of the repository's structure (file paths, signatures, class/function names) that
survives every eviction. The model rarely needs a full file body to navigate — it needs
to *know the file exists and what is in it*.

Its history digest is the resume block: a structured summary of the conversation's
direction with the actual edits preserved verbatim. The lesson is about **what to keep
raw**: the diffs are the irreplaceable part. A summary of a diff is nearly useless,
because a diff's value is in its exact bytes.

### 10.3 Devin — Long-Run Context Management

Autonomous coding agents running for tens of minutes hit context limits constantly, and
handle it as an ordinary operation rather than an exception:

- **Task-scoped context.** Each task in the plan gets its own context window; completing a task *is* a compaction boundary. This is the "task-boundary" trigger from §2.2, and it is the cleanest variant when the plan has clear seams.
- **Progress summaries as artifacts.** Each task produces a summary that is written to the session record, not just kept in context. That artifact is what a human reads to review the run, and what a later run loads if it resumes.
- **Test output kept structured, not summarized.** The failing test name and assertion are preserved exactly; the surrounding stack frames are dropped.

### 10.4 Letta / MemGPT — Tiered Memory as Virtual Context

The MemGPT paper reframes compaction as a **memory architecture** rather than a
summarization trick: the model has a small in-context "working memory" and a larger
external store, and it issues explicit tool calls to page information in and out. The
agent controls what is resident.

This is a more powerful model of the same problem, and it makes the memory↔context
boundary explicit rather than implicit. The trade-off is that paging decisions are made
by a stochastic model, so you still want the deterministic pin set underneath as a
floor. The production pattern that emerges: **Letta-style paging for *what* to load,
deterministic pinning for *what must never be lost*.**

### 10.5 Lost in the Middle — The Research Behind Pinning

Liu et al. (2023) showed that transformer performance degrades sharply when relevant
information sits in the middle of a long context, while the beginning and end are
attended to reliably. Two direct consequences for compaction design:

1. **Header/footer prompt structure** (§7.1) is not superstition — it exploits the
   measured attention profile.
2. **Pruning should be front-loaded.** Old content (which lands mid-context after new
   content is appended) is the cheapest thing to drop, which is why `recency` is only
   30% of the utility function — the graph terms dominate.

The paper also explains a confusing empirical result: models often *do* worse with
summarized context than with truncated context, because a fluent summary creates a
false impression of coverage. Hence §5.2's acceptance test — evaluate the block by
cold-start continuation, not by reading it.

---

## 11. TypeScript Interfaces for Compaction

```typescript
// ── Context ────────────────────────────────────────────────────────────────
export interface ContextSpan {
  id: string;
  kind: "system" | "goal" | "schema" | "invariant" | "user" | "assistant"
      | "tool_output" | "diff" | "failure" | "approval" | "chitchat" | "branch";
  role: "system" | "user" | "assistant" | "tool";
  turn: number; tokens: number;
  text?: string; path?: string; tool?: string; gateKey?: string;
  producedFor?: string[];      // task ids served (plan graph, → 08)
  keep?: boolean;              // hard pin
}

// ── Policy ─────────────────────────────────────────────────────────────────
export interface CompactionPolicy {
  triggerRatio: number;        // 0.70
  maxTurns: number;            // 20
  resumeBudgetTokens: number;  // 300
  minRatio: number;            // 1.2 — below this, compaction "failed"
  weights: { recency: number; reachability: number; failure: number };
  collapseRetryThreshold: number;  // 3
}
export const DEFAULT_POLICY: CompactionPolicy = {
  triggerRatio: 0.70, maxTurns: 20, resumeBudgetTokens: 300, minRatio: 1.2,
  weights: { recency: 0.30, reachability: 0.40, failure: 0.30 },
  collapseRetryThreshold: 3,
};

// ── Pin set ────────────────────────────────────────────────────────────────
export interface PinSet {
  tenantId: string; system: true; goal: true; schema: true;
  lastUserMessage: true; invariants: string[];
  activeDiffPaths: string[]; pendingApprovals: string[];   // → 15
}

// ── Resume ─────────────────────────────────────────────────────────────────
export interface ResumeBlock {
  goal: string; decisions: string[];
  open: { taskId: string; title: string }[];
  repro: { command: string; error: string };
  next: string; invariants: string[]; evicted: string[];
}

// ── Outcome ────────────────────────────────────────────────────────────────
export interface DurableExtract {
  facts: { key: string; value: string; kind: "decision" | "constraint" | "preference" | "todo" }[];
}
export interface CompactOutcome {
  kept: ContextSpan[]; resume: ResumeBlock; ratio: number;
  dropped: string[]; writeBack: DurableExtract;
}

// ── Compactor ──────────────────────────────────────────────────────────────
export interface Compactor {
  shouldCompact(used: number, budget: number, turns: number): boolean;
  compact(spans: ContextSpan[], budget: number, goal: string, pins: PinSet,
          plan: PlanGraph, loop: ActiveLoop | null): CompactOutcome;
  buildResume(input: ResumeInput): ResumeBlock;
  render(b: ResumeBlock): string;
  /** MUST persist before returning. A throw here must abort the compaction. */
  writeBackAndCompact(spans: ContextSpan[], budget: number, memory: MemoryStore,
                      traj: TrajectorySink, pins: PinSet, plan: PlanGraph,
                      loop: ActiveLoop | null, goal: string): Promise<CompactOutcome>;
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface CompactionInvariant { name: string; assert(o: CompactOutcome, budget: number): void }
export interface ColdStartTest {
  name: string; spans: ContextSpan[]; budget: number;
  expectSameNextAction: boolean;
}
```

---

## 12. Design Principles for Compaction

### 12.1 SOLID for Context Management

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `Compactor` decides what goes; `MemoryStore` persists; `TrajectorySink` records. None of them summarizes prose — that is a `Summarizer` dependency. |
| **O**pen/closed | A different eviction strategy is a new `CompactionPolicy` + scorer, not a rewritten compactor. |
| **L**iskov substitution | `MemoryStore` implementations (Postgres, vector DB, file) are interchangeable; the write-back contract is identical. |
| **I**nterface segregation | The context assembler needs `shouldCompact()`; the debugger needs `render()`. Don't make debug tooling drag in the plan graph. |
| **D**ependency inversion | Compaction depends on `PlanGraph` as an interface, so a synthetic graph works in unit tests without a planner. |

### 12.2 Six Design Principles

1. **Prune before you summarize.** Dropping dead spans is free and lossless; summarizing is expensive and lossy. Doing it in the wrong order costs money and information.
2. **Pin by derivation, not by hand.** The pin set is computed from the plan, the active loop, and the pending gate list — so it shrinks as work completes instead of growing until it breaks the budget.
3. **The budget is a hard cap.** 300 tokens for the resume block, 70% to trigger. Both enforced in code, both asserted in tests.
4. **Persist before evicting, or don't evict.** A compaction that cannot write back aborts. A run that loses a decision silently is worse than a run that stops with an error.
5. **Deterministic policy.** Trigger, pin, and eviction order are computed from measured state. The model never decides what it forgets.
6. **The contract is with a cold agent.** Accept a resume block only if a fresh agent with an empty context takes the correct next action from it.

---

## 13. Best Practices

### 13.1 DO ✅

- Trigger at 70% utilization or 20 turns, whichever comes first; leave 30% headroom for the next tool result.
- Pin system, goal, invariants, active diffs, the last user instruction, and the unresolved loop failure.
- Rank eviction by plan-graph reachability, not by age.
- Collapse 3+ identical retries into one line with the last error preserved verbatim.
- Cap the resume block at 300 tokens with fixed keys, and assert it in CI.
- Persist decisions, open items, and invariants to memory with `fsync` **before** evicting.
- Emit a `compaction` event with `keptIds`, `evictedIds`, and `ratio` (→ 13).
- Test with a cold agent: same next action from the resume block as from the full context.

### 13.2 DON'T ❌

- ❌ Don't trigger at 90% and hope the next result fits. It won't, and you compact under pressure — the worst time to be lossy.
- ❌ Don't use FIFO/oldest-first eviction. It keeps yesterday's `ls` and drops the task definition.
- ❌ Don't let the model decide when to compact.
- ❌ Don't summarize the whole transcript when most of it is dead branches.
- ❌ Don't paraphrase pinned values (numbers, IDs, negative constraints). Paraphrase is where precision dies.
- ❌ Don't let the pin set grow monotonically. A resolved loop's failure signal must become evictable.
- ❌ Don't write back to memory "later". Later is after the decision is gone.
- ❌ Don't treat a fluent summary as evidence of coverage. Test by cold-start continuation.
- ❌ Don't compact inside a task when the plan has a natural seam — compact at the seam.

---

## 14. Anti-Patterns & Solutions

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| **Naive truncation** | Agent re-reads files it already edited, undoes its own work | Pin set + resume block |
| **FIFO eviction** | Task spec gone, `ls` output retained | Utility ranking with plan graph |
| **Equal-weight summarization** | Stack trace survives, goal statement doesn't | Pin the goal; summarize only oversized dead output |
| **Compaction at 95%** | Summarization runs under pressure and loses detail | Trigger at 70% |
| **Silent write-back failure** | Decision never persisted; run "succeeds" inconsistently | Abort compaction on persist failure |
| **Model decides compaction** | Model answers "no" at 195k tokens | Deterministic policy from measured counts |
| **Unbounded resume block** | Resume grows to 2k tokens, then compaction becomes the problem | Hard 300-token cap with truncation |
| **Monotonic pin set** | Pins eventually exceed the budget; everything degrades quietly | Derive pins; expire resolved-loop pins |
| **Paraphrased invariants** | "About 30 seconds" instead of `timeoutMs: 30000` | Pin literal values; prose around them |
| **Compaction not audited** | Quality drops after compaction; nobody knows why | Emit the event; track post-compaction eval scores |
| **No cold-start test** | The block reads fine and is useless | Cold-agent continuation test in CI |

---

## 15. Production Checklist

- [ ] **Trigger** — 70% utilization OR 20 turns; deterministic, computed from measured tokens
- [ ] **Headroom** — 30% reserved; a single large tool result cannot trigger a cascade
- [ ] **Pin set** — system, goal, schema, invariants, active diffs, last user message, unresolved loop failure, pending approvals
- [ ] **Pin expiry** — resolved-loop pins become evictable; pin set does not grow monotonically
- [ ] **Eviction order** — plan-graph reachability weighted ≥ recency; no FIFO
- [ ] **Retry collapse** — 3+ identical calls collapse to one line with the last error verbatim
- [ ] **Resume block** — fixed keys, ≤300 tokens, asserted in CI, `evicted[]` for audit
- [ ] **Write-back** — facts persisted with `fsync` before eviction; failure aborts compaction
- [ ] **Audit** — `compaction` event with `keptIds`, `evictedIds`, `ratio`, `resumeHash` (→ 13)
- [ ] **Ratio monitoring** — alert when ratio < 1.5 on a large context
- [ ] **Prompt structure** — HEADER/FOOTER invariants; literals pinned, not paraphrased
- [ ] **Tests** — invariants on every recorded compaction; cold-agent continuation test; memory-down test
- [ ] **Quality tracking** — post-compaction eval score tracked and compared to non-compacted runs

---

## 16. Future Trends in Compaction

### 16.1 Structure-Aware Compaction (2026-2028)

- **Summarize the plan, not the transcript.** If the plan graph (→ 04) plus the resume block fully determine the next action, the transcript is largely redundant — a much smaller and more reliable compaction target.
- **Learned eviction policies.** Train the utility function on which spans actually preceded successful vs failed outcomes, instead of hand-weighting three terms.
- **Prefetch during summarization.** The summarizer's own call already knows what the next step needs; have it emit that as a `prefetch` alongside the resume block, so the following turn starts with the right context already resident.

### 16.2 Verifiable Compaction

Compaction is lossy by nature, and today nothing proves what was preserved matters. Two
directions: **coverage metrics** (fraction of *goal-relevant* facts that survived,
measurable against the eval set), and **auditable drop lists** (`evicted[]` already
exists; the next step is making it queryable so "what did we lose" is a one-query
question before it becomes an incident).

### 16.3 Compaction as a First-Class Step Type

Once a plan contains explicit `compact` nodes — at task seams, before risky operations,
before context handed to a sub-agent (→ 09 §16.2) — compaction stops being an
emergency response to a threshold and becomes a designed part of execution. That is the
difference between an agent that survives long runs and one that is merely lucky.

### 16.4 Beyond Summarization

- **State externalization.** Move large state (test fixtures, file bodies) to a store and keep only handles in context. The strongest form of compaction is not summarizing the data — it is never putting it there.
- **Tiered residency à la MemGPT**, with the deterministic pin set as the floor beneath the model's paging decisions.

---

## References

### Papers & Research

- **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al., 2023 · https://arxiv.org/abs/2307.03172
- **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · https://arxiv.org/abs/2310.08560
- **LongLoRA: Efficient Fine-tuning of Long-Context Large Language Models** · https://arxiv.org/abs/2309.12307
- **StreamingLLM: Efficient Streaming Language Models with Attention Sinks** — Xiao et al., 2023 · https://arxiv.org/abs/2309.17453
- **SWE-agent: Agent-Computer Interfaces for Automated Software Engineering** · https://arxiv.org/abs/2405.15793
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

### Frameworks & Tools

1. **Anthropic Claude Code** — https://docs.anthropic.com/en/docs/claude-code — `/compact` and auto-compact
2. **Aider** — https://aider.chat/docs/ — repo map + history digest
3. **Letta (MemGPT)** — https://docs.letta.com/ — tiered memory
4. **LangGraph** — https://langchain-ai.github.io/langgraph/ — summarization node pattern
5. **tiktoken** — https://github.com/openai/tiktoken — exact token counting for triggers
6. **LiteLLM** — https://docs.litellm.ai/ — token accounting per call

### Production Systems

- **Claude Code** — https://claude.com/product/claude-code — manual + auto compaction, visible budget
- **Aider** — https://aider.chat — repository map as an always-present pin set
- **Letta** — https://letta.com — memory as virtual context
- **Devin** — https://devin.ai — task-scoped context windows

### Related Modules

- `02-build-context/README.md` §16 — the transient side of the contract (assembly, marking, fan-out)
- `03-update-memory-store/README.md` §12 — the durable side (write-back target, GDPR, retrieval)
- `04-plan-decompose-task/README.md` — the plan graph that makes reachability scoring possible
- `05-prompt-builder/README.md` §17.5 — header/footer invariant structure
- `07-workflow/README.md` §13.4 — compaction as an explicit engine step type
- `09-multi-agent/README.md` §16.2 — compaction before handing context to a sub-agent
- `10-automation/README.md` §17.3 — loop budget, which compaction keeps affordable
- `13-trajectory-observability/README.md` — the `compaction` event and its audit trail
- `15-approval-gates/README.md` — pending approvals are part of the pin set

---

*Document: Harness 14. Context Compaction — HARNESS ENGINEERING EDITION*
*Cross-cutting module · what lets a fixed context window support an unbounded run*
*Last updated: 19/07/2026*
*Author: AI Knowledge Repository*
