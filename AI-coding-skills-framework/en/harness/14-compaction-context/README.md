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
> **Cross-cutting module.** Compaction is why an agent can run for hours instead of
> minutes. It looks after the line between *short-lived context* (→ 02) and *long-lived memory*
> (→ 03) — that agreement breaks in production more than any other.

---

### Opening Story

This story shows what happens when compaction is missing. Compaction = shrinking the
conversation when it no longer fits, without losing what matters.

It's turn 47. The agent is deep in a refactor: 31 tool calls (tool call = the agent
runs a tool, like reading a file), four files rewritten, two test suites run, one
confusing stack trace (stack trace = the error report that lists what called what)
buried somewhere in the middle. The context window (context window = the model's
working memory, measured in tokens; 1 token ≈ ¾ of a word) is at 96%. The next tool
result will be 4,000 tokens and it doesn't fit.

Now the team has three bad options and no good one:

1. **Let it fail.** The run dies at turn 47 with a context-length error. The user sees
   "something went wrong" after 20 minutes.
2. **Naive truncation.** Truncation = cutting the oldest messages off the top. The
   agent loses the task specification it was given in turn 1. It re-reads a file it
   already read in turn 12 (because the *result* is gone but the *edit* is not). It
   then confidently produces a patch that undoes its own work from turn 30.
3. **Summarize everything equally.** Compress the whole transcript (transcript = the
   full turn-by-turn log of the run) into a paragraph. The paragraph mentions the
   stack trace and omits the task definition. So the agent solves the wrong problem,
   fluently.

**None of these is real "compaction".** Compaction is a friendly but firm *routine*: a
trigger (when to shrink), a pin set (what to always keep), a utility ranking (what to
drop first), and a resume block (a fixed-shape note that rebuilds the run's state).
Get those four right and turn 47 feels boring. Get them wrong and the failure is
quiet — the run *finishes*, it just finishes the wrong job.

> **One-line summary:** Without a compaction routine, a long agent run either crashes
> at the context ceiling or quietly finishes the wrong job.

### Why Is Compaction Non-Optional?

> *"Any agent that can't survive its own context window is a demo, not a product."*

This section shows the math: without compaction every run has a hard expiration date.

#### The Arithmetic

How to read it: each row is one context-window size. "Input per turn" is how many
tokens one turn adds. "Turns before exhaustion" is how soon the window fills up with
no compaction. The last column shows the same run with a 70% trigger plus compaction.

| Budget | Input per turn | Turns before exhaustion | With 70% trigger + compaction |
|--------|----------------|------------------------|----------------------------------|
| 200k (large) | ~6k | ~33 | unbounded |
| 128k (typical) | ~4k | ~32 | unbounded |
| 32k (small/local) | ~2k | ~16 | unbounded |

**Unbounded** is the whole goal. Compaction isn't just a nice speedup; it's what turns
a fixed-size context into a run that can go as long as you need. It's also what makes
`07-workflow` checkpoint-resume work (→ 07 §13), `09-multi-agent` sub-agent handoffs
possible (→ 09 §16.2), and the `10-automation` loop budget doable (→ 10 §17.3) —
each of those needs a run that lives past one context window.

#### Second-Order Effects

Compaction changes more than capacity. Three side effects to plan for:

- **Cost.** Compaction reduces per-turn input tokens dramatically on long runs, because
  a 60 KB resume block replaces 180 KB of history. Teams routinely see 40–70% cost
  reduction on runs over 30 turns.
- **Quality.** Compaction *can* hurt quality — that is what §5–7 are about. Done badly
  it's strictly worse than no compaction, because the model confidently reasons on a
  lossy summary (lossy = some detail is thrown away for good).
- **Auditability.** Compaction produces a `compaction` event (→ 13) recording exactly
  what was kept and evicted. Event = a log entry you can query later. A harness where
  you can't reconstruct what the model lost is a harness you can't debug.

> **One-line summary:** Every context window has a turn limit; compaction is the only
> thing that removes it, and it must be done carefully or it trades crashes for silent quality loss.

---

## Overview

> **📌 Core Concept**
>
> - **Concept:** Compaction is **triggered summarization** (summarization that fires
>   automatically at a threshold): when context exceeds a threshold, low-value spans
>   (span = one piece of the conversation, e.g. one tool result) are replaced by a
>   structured resume block instead of hitting the token ceiling. **Pruning** is its
>   companion — deciding *what* goes first by utility (usefulness to the rest of the
>   run), not by recency (how old it is).
> - **Analogy:** Packing a small suitcase for a long trip. When it's full you don't
>   toss things at random — you have rules (hygiene kit stays, old receipts go) and
>   you leave a note listing what you removed.
> - **Why it matters:** Every long agent run dies without compaction: context
>   overflow, lost-in-the-middle accuracy collapse, and a 3–5× token bill from
>   resending dead tool output. Compaction at 70% keeps runs alive indefinitely at
>   flat cost.

**Context Compaction** is what lets a small, fixed context window support a long,
open-ended run. It's the part of most agent harnesses that gets the least attention,
and the most painful to get wrong.

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

Reading the diagram: the "before" box is nearly full — 178k of its 200k tokens can be
thrown away. The trigger fires at 70% usage. The "after" box keeps the system prompt
and goal, a 280-token resume block, and the last 3 turns verbatim (verbatim = word
for word, not summarized).

**Four components, and a missing one is a bug.** How to read it: each row is one
required part; the last column is the failure you get if that part is missing.

| # | Component | Failure if missing |
|---|-----------|-------------------|
| 1 | **Trigger** | Run dies at the ceiling |
| 2 | **Pin set** | Task definition evicted; agent solves the wrong problem |
| 3 | **Utility ranking** | FIFO eviction throws away the goal, keeps yesterday's `ls` |
| 4 | **Resume block** | Agent wakes up with no state, re-reads everything, bill triples |
| 5 | **Memory write-back** *(the commonly-missed one)* | Decisions vanish with the evicted span and are never persisted |

Glossary for the table: **trigger** = the rule that decides when to compact. **Pin
set** = the "do not delete" list. **Utility ranking** = scoring each span by
usefulness. **FIFO** = "first in, first out" — drop the oldest item first. **`ls`** =
the directory-listing command; its output is usually cheap to re-run. **Resume
block** = the fixed-shape summary the agent reads after compaction. **Write-back** =
saving decisions to long-term memory before they leave the context.

> **One-line summary:** Compaction = trigger + pin set + utility ranking + resume
> block + memory write-back; miss any one and the run crashes or silently goes wrong.

## Contents

How to read it: this table maps each numbered section to one line on what it covers.

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

> **One-line summary:** Sections 1–7 explain the design, 8–9 make it runnable and
> tested, 10–16 cover real systems, principles, and checklists.

---

## 1. Definitions & Vocabulary

This section defines the seven terms the rest of the module uses. Read it once;
every later section assumes these names.

### 1.1 Core Terms

How to read it: each row is one term, its plain meaning, and the failure mode when
the term is ignored.

| Term | Definition | Fails when… |
|------|-----------|-------------|
| **Auto-compaction** | Summarization triggered by `used > threshold`; evictable spans are replaced by a resume summary | trigger missing → run dies |
| **Resume block** | Struct ≤300 tokens: `Goal / Decisions / Open / Repro / Next` + `evicted_span_ids` | unconstrained → grows until it is the problem |
| **Trajectory-aware pruning** | Eviction order derived from the execution graph (keep the critical path, drop dead branches) | recency-only → drops the goal |
| **Compaction ratio** | `tokens_before ÷ tokens_after` — a health metric | <1.5 on a large context → the summarizer is failing |
| **Pin set** | The non-evictable core: system, goal, constraints, open diff, last failure | absent → task spec evicted |
| **Write-back** | Persisting resume + decisions + open items to memory *before* they leave context | skipped → decisions are lost forever |
| **Lost in the middle** | Accuracy degrades when relevant info sits mid-context | ignored → pinning is arbitrary |

Plain-language notes: **evictable** = "allowed to delete". **Critical path** = the
chain of steps the current goal still depends on. **Diff** = the set of edits made to
files so far. **Repro** = the exact command that reproduces the current error.

> **One-line summary:** Seven terms — auto-compaction, resume block, trajectory-aware
> pruning, compaction ratio, pin set, write-back, lost in the middle — are the shared
> vocabulary for everything below.

### 1.2 The Two Families: Summarization vs Pruning

This section separates two operations people confuse. They are complements, not
alternatives; mixing them up is the root of most bad implementations.

How to read it: each row compares the two on one dimension — what it does, when to
use it, what it costs, and what can go wrong.

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
prune later pay roughly 40% more and keep less information.

> **One-line summary:** Prune dead weight first (free), then summarize what's left
> but too big (expensive and lossy) — in that order.

---

## 2. Trigger Policy

This section answers "when do we compact?" — too late and the run dies; too often and
you pay quality and cost.

> **One-line summary:** The trigger is a measured, deterministic rule — and 70% is
> the sweet spot.

### 2.1 Why 70% and Not 90%

The ladder below shows what happens at each usage level:

```
100% ──── hard ceiling: the request itself fails. Unrecoverable, no logging.
 90% ──── "close enough" — but the next tool result routinely exceeds 10% of budget.
 70% ──── leaves 30% headroom: next 2-3 turns of tool results fit without re-compacting.
 50% ──── too eager: 2 compactions per run, quality cost, wasted LLM calls.
```

The failure at 90% is specific and common: a single `read_file` of a 30 KB file
consumes 8% of a 200k window in one step. Trigger at 90%, get one 8% result, and you
are at 98% — now the *next* result overflows and you compact again, mid-task, with
less room to summarize. Compaction under pressure is exactly when you can't afford
lossy summarization.

**The rule: trigger when you can still afford to summarize well.**

> **One-line summary:** Trigger at 70% so 30% of the window is headroom — compacting
> at 90% means compacting under pressure, the worst time to lose detail.

### 2.2 Trigger Strategies

How to read it: each row is one way to decide "compact now", the rule itself, and
when that rule fits.

| Strategy | Rule | Use when |
|----------|------|----------|
| **Threshold** | `used / budget > 0.70` | default, simple, predictable |
| **Turn-count** | `turns > 20` | token estimates are unreliable; cheap backstop |
| **Growth-rate** | compact when `used` grew >25% in the last 3 turns | runaway tool loops |
| **Task-boundary** | compact between tasks, not inside one | long multi-task sessions; keeps a task's reasoning intact |
| **Size-of-next** | compact when `est(next_result) > headroom` | tight budgets (32k) |

Production recommendation: **threshold OR turn-count**, whichever fires first, plus
task-boundary compaction when the plan (→ 08) has a natural seam (seam = a clean
break point between two tasks). Growth-rate is a useful alarm for "this run is in a
loop" (→ 10 §17.3).

**Never let the model decide.** Compaction is a harness policy computed from measured
token counts. A model asked "should we compact?" will answer "no, I'm fine" while
holding 195k tokens.

> **One-line summary:** Use a threshold at 70% or a turn cap at 20 — whichever fires
> first — and never ask the model whether it needs compacting.

---

## 3. The Pin Set — What Must Survive

This section defines the "never delete" list. It is the safety net that keeps the
agent solving the *right* problem after compaction.

> **One-line summary:** Pin anything whose loss would change the task itself — and
> let pins expire when their work is done.

### 3.1 Pinned vs Evictable

The pin set is the answer to "what would make the run wrong if it disappeared?"
Anything whose absence changes the *task* rather than the *taste* is pinned.

How to read it: the left column is the never-delete list; the right column lists
what may be deleted, roughly in the order you'd delete it.

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

Glossary for the table: **stdout** = the raw text a tool prints. **Retrieved chunks
with score <0.3** = search results that scored too low to matter. **`cat`** = print a
file's contents. **Output schema** = the exact shape the answer must have. **Pointer
to durable memory** = a short reference to a fact stored in long-term memory.

**The subtlety:** "the last failure signal" is pinned *for the active loop only*.
Once the loop is resolved, that failure becomes evictable. Pinning it forever means
your pin set grows monotonically and eventually exceeds the budget — which is its own
failure mode, and a quiet one.

> **One-line summary:** Pin the task itself (goal, constraints, active edits, live
> failure), evict the rest by usefulness — and unpin when a loop is resolved.

### 3.2 The Pin Set

> 📄 **Example code:** [`examples/01-3-2-the-pin-set.ts`](examples/01-3-2-the-pin-set.ts)

**Rule: the pin set is derived, not hand-maintained.** Derived = computed
automatically from other state, not typed in by hand. It's computed from the plan,
the active loop, and the pending gate list — so it shrinks automatically as work
completes instead of accumulating.

> **One-line summary:** Compute the pin set from the plan and active loop; never
> maintain it by hand.

---

## 4. Utility-Based Pruning

This section answers "in what order do we delete?" — by usefulness to the rest of
the run, not by age.

> **One-line summary:** Score each span by recency + plan reachability + failure
> signal, then evict the lowest scores first.

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

> **One-line summary:** Age is a bad proxy for value: the oldest span may be the
> constraint the whole run depends on.

### 4.2 Scoring Trajectory-Aware Utility

Each span gets a utility score between 0 and 1. High score = keep; low score = evict
first.

```
utility = 0.30·recency + 0.40·structural_reachability + 0.30·failure_signal
```

How to read it: the three ingredients, what each means, and how to compute it.

| Term | Meaning | Implementation |
|------|---------|----------------|
| `recency` | Normalized age: `exp(-turns_old / 12)` | cheap, prevents unbounded staleness |
| `structural_reachability` | Is this span on the current critical path to the goal? | BFS over the plan graph (→ 04) from the active task; a span feeding a *pending* node scores high, a span feeding a *completed* node scores low |
| `failure_signal` | Does this span carry the error the active loop is chasing? | string/trace match against the loop's last error (see §8.3) |

Plain notes: **normalized age** = age squashed to a 0–1 number so old spans decay
smoothly. **BFS** = breadth-first search — walking the plan graph outward from the
active task to see which spans feed work that is still pending.

Then evict ascending utility (lowest score first), never crossing the budget.
Crucially, **this ordering operates on the plan graph, not on the message list** —
which is why it needs `08` and `04` to be useful.

> 📄 **Example code:** [`examples/02-4-2-scoring-trajectory-aware-utility.ts`](examples/02-4-2-scoring-trajectory-aware-utility.ts)

> **One-line summary:** Utility = 30% recency + 40% "still on the path to the goal"
> + 30% "carries the error being chased"; evict the lowest first.

### 4.3 Collapse, Don't Delete

Two refinements that separate a good implementation from a working one:

1. **Collapse identical retries.** Three identical `npm test` failures become
   `retried 3×, last_err: E2BIG at test_refresh_rotation`. The information that
   matters (it failed, here's why, it was retried) survives at 1/30th the cost.
2. **Summarize before dropping dead branches.** A completed branch is not *worthless* —
   it explains why the agent is now in a different place. One line: `branch t3
   (vector cache) rejected: adds 400ms p99`. Cheap, and it prevents the agent from
   re-exploring it.

Reading the diagram: six identical failed test runs collapse into one 24-token line
that keeps the last error.

```
turns 38,39,40:  npm test (exit 1)  ──┐
turns 41,42,43:  npm test (exit 1)  ──┼──▶  [retried 6×, last_err: E2BIG @ test_refresh_rotation]
turn  44:        npm test (exit 1)  ──┘         (from turn 38, 18k tokens → 24 tokens)
```

> **One-line summary:** Don't delete repeated or dead work outright — squeeze it
> into one line that keeps the last error or the reason it was rejected.

---

## 5. The Resume Block

This section defines the note the agent reads after compaction — the single object
that decides whether the run continues correctly.

> **One-line summary:** The resume block is a fixed-format, ≤300-token state note;
> its quality bar is "a fresh agent can continue from it alone".

### 5.1 Format

Fixed keys, hard budget, machine-checkable (machine-checkable = a parser can read
it, not just a human):

```
Goal:<one line — the task, not the plan>
Decisions:[D1: …][D2: …][D3: …]        ≤5, each ≤25 words
Open:[t5: …][t6: …]                    pending tasks with IDs (→ 08)
Repro:<exact command + last error line>
Next:<the single next action>
Invariants:[…]                          the ≤5 pinned constraints
Evicted:[span-id list]                  for audit + reconstruction
```

What each key means: **Goal** = the task in one line. **Decisions** = choices already
made, with IDs. **Open** = unfinished tasks, each with its task ID. **Repro** = the
exact command that reproduces the current failure. **Next** = the one action to do
now. **Invariants** = rules that must not be broken. **Evicted** = the IDs of spans
that were deleted, for audit.

**Why the keys are fixed:** the resume block is re-read by *code*, not just by the
model. A parser extracts `Open[]` to rebuild the pending task list, `Repro` to seed
the retry, and `Evicted[]` to write back to memory and to emit the audit event.
Free-form prose breaks all three.

> **One-line summary:** Seven fixed keys — Goal, Decisions, Open, Repro, Next,
> Invariants, Evicted — because code, not just the model, reads them back.

### 5.2 Quality Bar

A resume block is good when a **fresh agent with an empty context** can pick up the
run and do the next step correctly (this test is called *cold-start*: start cold,
with nothing in context). Test it exactly that way:

> 📄 **Example code:** [`examples/03-5-2-quality-bar.ts`](examples/03-5-2-quality-bar.ts)

A block that says "we were refactoring authentication and hit some issues" fails every
one of these lines. It feels informative and is useless — this is the most common way
compaction silently destroys a run.

> **One-line summary:** Judge a resume block by one test only: can an agent with an
> empty context take the correct next step from it?

---

## 6. The Compaction↔Memory Contract

This section draws the line between short-lived context and long-term memory. Getting
this line wrong is the most common way compaction loses information permanently.

> **One-line summary:** Context owns what dies with the run; memory owns what a
> future run needs — and you must save to memory *before* evicting.

### 6.1 The Boundary

How to read it: each row pairs a piece of data with its owner — left column means
"context keeps it and may delete it", right column means "save it to durable memory".

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

> **One-line summary:** Ask "needed after this run?" — no → context may evict it;
> yes → it must be written to memory first.

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

Plain notes on the sequence: **tenant + task scoped** = saved under keys that bind
the data to one tenant and one task, so it can't leak across. **fsync** = force the
data physically onto disk before moving on, so a crash can't lose it. **resumeHash**
= a fingerprint of the resume block, so audits can detect changes.

Step 3 failing must abort step 5. Not log a warning — abort. A compaction that loses a
decision has produced a run that can't be trusted, and the cheapest way to make that
impossible is to make it fail loudly.

**The verification test** is in §9.2, and it's the single most valuable test in this
module: kill the memory backend, run a compaction, and assert the run refuses to
proceed.

> **One-line summary:** Persist to memory (with fsync) before evicting — if the save
> fails, abort the compaction rather than lose a decision silently.

---

## 7. Compaction-Safe Prompts

This section shows how to write a prompt that survives summarization. Compaction is
lossy, so the prompt must put what can't be lost where summarizers keep it.

> **One-line summary:** Put invariants at the very start and very end of the prompt;
> pin literal values — paraphrase is where precision dies.

### 7.1 Header / Body / Footer

Structure a prompt in three zones. Compaction is lossy, so design the prompt to
survive it:

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

Plain notes: **invariants** = rules that must never be broken. **Unified diff** = the
standard text format that shows added and removed lines. **JWT** = signed login
tokens. The **HEADER** holds the rules, the **BODY** holds bulky reference material
that may be evicted, and the **FOOTER** repeats the rules.

**The empirical basis** is the lost-in-the-middle result (§10.5): models attend most
reliably to the beginning and end of a long context. Putting the invariants in both
places means a summarizer that keeps only the head *and* the tail still preserves the
constraints — and a summarizer that keeps 80% of tokens preserves them with near-certainty.

> **One-line summary:** Invariants in the header, repeated in the footer, bulky
> material in the middle — because summarizers reliably keep the two ends.

### 7.2 What Summarizers Drop

Knowing the failure modes tells you what to pin. How to read it: left column = what
summarizers typically lose; right column = the counter-move.

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

> **One-line summary:** Summarizers lose negations, numbers, IDs, error structure,
> and ordering — pin each of those verbatim instead of trusting the summary.

---

## 8. TypeScript Implementation

This section points to runnable code for every piece designed above, in order.

> **One-line summary:** Five code files cover types, the compact routine, the
> scorer, the resume builder, and memory write-back.

### 8.1 Types

The data structures the whole module is built on: spans, the pin set, the resume
block, and the compaction event.

> 📄 **Example code:** [`examples/04-8-1-types.ts`](examples/04-8-1-types.ts)

> **One-line summary:** Start from the types — they encode the pin set and resume
> block shapes used by every other file.

### 8.2 shouldCompact + compact()

<details>
<summary>TypeScript Code — trigger + pin + utility prune + resume (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-8-2-shouldcompact-compact.ts`](examples/05-8-2-shouldcompact-compact.ts)

</details>

`shouldCompact()` = the trigger check; `compact()` = the full routine (pin → prune →
summarize → write back → resume block).

> **One-line summary:** This file is the whole pipeline in two functions: one decides
> when, one does it.

### 8.3 Trajectory Utility Scorer

The `recency` + `structural_reachability` + `failure_signal` scorer from §4.2, as
runnable code.

> 📄 **Example code:** [`examples/06-8-3-trajectory-utility-scorer.ts`](examples/06-8-3-trajectory-utility-scorer.ts)

> **One-line summary:** The eviction ordering lives here — score every span, sort
> ascending, evict from the bottom.

### 8.4 Resume Block Builder

Turns the kept state into the fixed-key ≤300-token resume block from §5.1.

> 📄 **Example code:** [`examples/07-8-4-resume-block-builder.ts`](examples/07-8-4-resume-block-builder.ts)

> **One-line summary:** The builder enforces the format and the 300-token cap in
> code, not by hoping the model behaves.

### 8.5 Memory Write-Back

Persists decisions, open items, and invariants to memory before eviction (§6.2's
sequence, as code).

> 📄 **Example code:** [`examples/08-8-5-memory-write-back.ts`](examples/08-8-5-memory-write-back.ts)

> **One-line summary:** Write-back runs before eviction and aborts the compaction if
> the persist fails.

---

## 9. Testing Compaction

This section covers the three test layers: invariants, the memory contract, and
quality regression.

> **One-line summary:** Test invariants on real trajectories, test the
> write-before-evict contract, and track success rates before vs after compaction.

### 9.1 Invariant Tests

Invariant tests = checks that must pass on *every* compaction (e.g. the pin set is
intact, the resume block parses, the ratio is sane).

> 📄 **Example code:** [`examples/09-9-1-invariant-tests.ts`](examples/09-9-1-invariant-tests.ts)

Run these on **every** recorded trajectory that hits a compaction, in nightly CI
(CI = automated checks that run on every code change). Real trajectories catch the
edge cases synthetic ones never do.

> **One-line summary:** Replay every recorded compaction nightly and assert the
> invariants held.

### 9.2 The Contract Test That Matters Most

The contract test: break the memory backend on purpose, run a compaction, and assert
the run refuses to continue (because the write-back could not happen).

> 📄 **Example code:** [`examples/10-9-2-the-contract-test-that-matters-most.ts`](examples/10-9-2-the-contract-test-that-matters-most.ts)

The second test is the real acceptance criterion for the whole module. It's also the
test most teams skip, and it's the one that would have caught the turn-47 failure
described at the top.

> **One-line summary:** If memory write-back fails, compaction must abort — and this
> test proves it.

### 9.3 Quality Regression Suite

Track, per compaction, whether the run still succeeds. If quality drops after
compaction, the pin set is wrong — and this is the measurement that finds it:

> 📄 **Example code:** [`examples/11-9-3-quality-regression-suite.sql`](examples/11-9-3-quality-regression-suite.sql)

A specific run that fails only when a compaction happened immediately before the
failure is the strongest possible signal that the pin set is missing something.

> **One-line summary:** Compare success rates of runs with and without compaction;
> a drop right after a compaction points at a missing pin.

---

## 10. Real-World Case Studies

This section shows how four production systems and one research paper solved the
same problems above.

> **One-line summary:** Claude Code, Aider, Devin, and Letta each implement a piece
> of this module in production; lost-in-the-middle explains why pinning works.

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
   compacted; here's what I remember" because it's phrased like a save point, not a
   hidden truncation.

> **One-line summary:** Make compaction visible and user-controllable, and use one
> implementation for both the manual and automatic paths.

### 10.2 Aider — Repository Map + History Digest

Aider's `repo map` is the purest form of the pin set: a compact, always-present index
of the repository's structure (file paths, signatures, class/function names) that
survives every eviction. The model rarely needs a full file body to navigate — it needs
to *know the file exists and what is in it*.

Its history digest is the resume block: a structured summary of the conversation's
direction with the actual edits preserved verbatim. The lesson is about **what to keep
raw**: the diffs are the irreplaceable part. A summary of a diff is nearly useless,
because a diff's value is in its exact bytes.

> **One-line summary:** Keep a tiny always-present map of the repo (pin set) and keep
> diffs raw — a summarized diff is nearly useless.

### 10.3 Devin — Long-Run Context Management

Autonomous coding agents running for tens of minutes hit context limits constantly, and
handle it as an ordinary operation rather than an exception:

- **Task-scoped context.** Each task in the plan gets its own context window; completing a task *is* a compaction boundary. This is the "task-boundary" trigger from §2.2, and it's the cleanest variant when the plan has clear seams.
- **Progress summaries as artifacts.** Each task produces a summary that is written to the session record, not just kept in context. That artifact is what a human reads to review the run, and what a later run loads if it resumes.
- **Test output kept structured, not summarized.** The failing test name and assertion are preserved exactly; the surrounding stack frames are dropped.

> **One-line summary:** Compact at task boundaries, store progress summaries as
> reviewable records, and keep failure details exact.

### 10.4 Letta / MemGPT — Tiered Memory as Virtual Context

The MemGPT paper reframes compaction as a **memory architecture** rather than a
summarization trick: the model has a small in-context "working memory" and a larger
external store, and it issues explicit tool calls to page information in and out
(paging = moving data between fast small memory and big slow storage, like an OS does
with RAM and disk). The agent controls what is resident (resident = currently loaded
in context).

This is a more powerful model of the same problem, and it makes the memory↔context
boundary explicit rather than implicit. The trade-off is that paging decisions are made
by a stochastic model (stochastic = non-deterministic — it may choose differently each
time), so you still want the deterministic pin set underneath as a floor. The
production pattern that emerges: **Letta-style paging for *what* to load,
deterministic pinning for *what must never be lost*.**

> **One-line summary:** Let the model page data in and out of a big external store —
> but keep the deterministic pin set underneath as a floor.

### 10.5 Lost in the Middle — The Research Behind Pinning

Liu et al. (2023) showed that transformer performance degrades sharply when relevant
information sits in the middle of a long context, while the beginning and end are
attended to reliably. Two direct consequences for compaction design:

1. **Header/footer prompt structure** (§7.1) isn't superstition — it exploits the
   measured attention profile.
2. **Pruning should be front-loaded.** Old content (which lands mid-context after new
   content is appended) is the cheapest thing to drop, which is why `recency` is only
   30% of the utility function — the graph terms dominate.

The paper also explains a confusing empirical result: models often *do* worse with
summarized context than with truncated context, because a fluent summary creates a
false impression of coverage. Hence §5.2's acceptance test — evaluate the block by
cold-start continuation, not by reading it.

> **One-line summary:** Models remember the start and end of context best — put
> must-keep facts there, and judge summaries by behavior, not by how they read.

---

## 11. TypeScript Interfaces for Compaction

The full public type surface of the module (type surface = all the interfaces other
code may depend on), in one file for reference and reuse.

> 📄 **Example code:** [`examples/12-11-typescript-interfaces-for-compaction.ts`](examples/12-11-typescript-interfaces-for-compaction.ts)

> **One-line summary:** One file holds every interface — copy it as the contract
> between compaction, memory, and the harness.

---

## 12. Design Principles for Compaction

This section distills the module into reusable principles: SOLID applied to context,
then six rules of thumb.

> **One-line summary:** Prune before summarizing, derive pins, cap budgets, persist
> before evicting, stay deterministic, and test with a cold agent.

### 12.1 SOLID for Context Management

SOLID = five classic software-design principles (Single responsibility, Open/closed,
Liskov substitution, Interface segregation, Dependency inversion). How to read it:
each row maps one principle to a concrete design choice in this module.

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `Compactor` decides what goes; `MemoryStore` persists; `TrajectorySink` records. None of them summarizes prose — that is a `Summarizer` dependency. |
| **O**pen/closed | A different eviction strategy is a new `CompactionPolicy` + scorer, not a rewritten compactor. |
| **L**iskov substitution | `MemoryStore` implementations (Postgres, vector DB, file) are interchangeable; the write-back contract is identical. |
| **I**nterface segregation | The context assembler needs `shouldCompact()`; the debugger needs `render()`. Don't make debug tooling drag in the plan graph. |
| **D**ependency inversion | Compaction depends on `PlanGraph` as an interface, so a synthetic graph works in unit tests without a planner. |

Plain notes: **Postgres** = a relational database. **Vector DB** = a database that
stores embeddings for similarity search. **TrajectorySink** = the component that
records the run log. **Synthetic graph** = a fake plan graph for tests.

> **One-line summary:** Keep deciding, persisting, recording, and summarizing in
> separate swappable components.

### 12.2 Six Design Principles

1. **Prune before you summarize.** Dropping dead spans is free and lossless; summarizing is expensive and lossy. Doing it in the wrong order costs money and information.
2. **Pin by derivation, not by hand.** The pin set is computed from the plan, the active loop, and the pending gate list — so it shrinks as work completes instead of growing until it breaks the budget.
3. **The budget is a hard cap.** 300 tokens for the resume block, 70% to trigger. Both enforced in code, both asserted in tests.
4. **Persist before evicting, or don't evict.** A compaction that can't write back aborts. A run that loses a decision silently is worse than a run that stops with an error.
5. **Deterministic policy.** Trigger, pin, and eviction order are computed from measured state. The model never decides what it forgets.
6. **The contract is with a cold agent.** Accept a resume block only if a fresh agent with an empty context takes the correct next action from it.

> **One-line summary:** Six rules: prune first, derive pins, hard-cap budgets,
> persist before evicting, keep policy deterministic, and accept only cold-start-proven blocks.

---

## 13. Best Practices

A quick reference list. Each line compresses a section above into one action.

### 13.1 DO ✅

- Trigger at 70% utilization or 20 turns, whichever comes first; leave 30% headroom for the next tool result.
- Pin system, goal, invariants, active diffs, the last user instruction, and the unresolved loop failure.
- Rank eviction by plan-graph reachability, not by age.
- Collapse 3+ identical retries into one line with the last error preserved verbatim.
- Cap the resume block at 300 tokens with fixed keys, and assert it in CI.
- Persist decisions, open items, and invariants to memory with `fsync` **before** evicting.
- Emit a `compaction` event with `keptIds`, `evictedIds`, and `ratio` (→ 13).
- Test with a cold agent: same next action from the resume block as from the full context.

> **One-line summary:** Do: trigger early, pin the task, score eviction by the plan,
> collapse retries, cap the block, and write back before evicting.

### 13.2 DON'T ❌

- ❌ Don't trigger at 90% and hope the next result fits. It won't, and you compact under pressure — the worst time to be lossy.
- ❌ Don't use FIFO/oldest-first eviction. It keeps yesterday's `ls` and drops the task definition.
- ❌ Don't let the model decide when to compact.
- ❌ Don't summarize the whole transcript when most of it's dead branches.
- ❌ Don't paraphrase pinned values (numbers, IDs, negative constraints). Paraphrase is where precision dies.
- ❌ Don't let the pin set grow monotonically. A resolved loop's failure signal must become evictable.
- ❌ Don't write back to memory "later". Later is after the decision is gone.
- ❌ Don't treat a fluent summary as evidence of coverage. Test by cold-start continuation.
- ❌ Don't compact inside a task when the plan has a natural seam — compact at the seam.

> **One-line summary:** Don't: compact late, evict by age, trust the model's judgment,
> paraphrase pinned values, or delay the write-back.

---

## 14. Anti-Patterns & Solutions

How to read it: each row is one recurring mistake, the symptom you'd observe in
production, and the fix from this module.

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

> **One-line summary:** Most compaction failures reduce to three causes — evicting
> the wrong thing, compacting too late, or skipping the write-back.

---

## 15. Production Checklist

How to read it: each checkbox is one gate to pass before shipping compaction; the
bold word names the area, the rest is the acceptance condition.

- [ ] **Trigger** — 70% utilization OR 20 turns; deterministic, computed from measured tokens
- [ ] **Headroom** — 30% reserved; a single large tool result can't trigger a cascade
- [ ] **Pin set** — system, goal, schema, invariants, active diffs, last user message, unresolved loop failure, pending approvals
- [ ] **Pin expiry** — resolved-loop pins become evictable; pin set doesn't grow monotonically
- [ ] **Eviction order** — plan-graph reachability weighted ≥ recency; no FIFO
- [ ] **Retry collapse** — 3+ identical calls collapse to one line with the last error verbatim
- [ ] **Resume block** — fixed keys, ≤300 tokens, asserted in CI, `evicted[]` for audit
- [ ] **Write-back** — facts persisted with `fsync` before eviction; failure aborts compaction
- [ ] **Audit** — `compaction` event with `keptIds`, `evictedIds`, `ratio`, `resumeHash` (→ 13)
- [ ] **Ratio monitoring** — alert when ratio < 1.5 on a large context
- [ ] **Prompt structure** — HEADER/FOOTER invariants; literals pinned, not paraphrased
- [ ] **Tests** — invariants on every recorded compaction; cold-agent continuation test; memory-down test
- [ ] **Quality tracking** — post-compaction eval score tracked and compared to non-compacted runs

Plain notes: **schema** here = the output shape the model must produce. **Cascade** =
one oversized result forcing an immediate second compaction. **Memory-down test** =
the §9.2 test with the memory backend deliberately broken.

> **One-line summary:** Thirteen gates — trigger, headroom, pins with expiry,
> eviction order, resume cap, write-back, audit, monitoring, prompt structure, and
> three test layers — all pass before shipping.

---

## 16. Future Trends in Compaction

This section looks at where compaction design is heading between 2026 and 2028.

> **One-line summary:** Compaction is moving from an emergency response to a
> designed, verifiable, plan-aware step — and eventually to not needing the raw
> data in context at all.

### 16.1 Structure-Aware Compaction (2026-2028)

- **Summarize the plan, not the transcript.** If the plan graph (→ 04) plus the resume block fully determine the next action, the transcript is largely redundant — a much smaller and more reliable compaction target.
- **Learned eviction policies.** Train the utility function on which spans actually preceded successful vs failed outcomes, instead of hand-weighting three terms.
- **Prefetch during summarization.** The summarizer's own call already knows what the next step needs; have it emit that as a `prefetch` alongside the resume block, so the following turn starts with the right context already resident.

> **One-line summary:** Next: compact the plan instead of the transcript, learn the
> utility weights from outcomes, and prefetch what the next turn needs.

### 16.2 Verifiable Compaction

Compaction is lossy by nature, and today nothing proves what was preserved matters. Two
directions: **coverage metrics** (fraction of *goal-relevant* facts that survived,
measurable against the eval set — eval set = a fixed batch of test questions), and
**auditable drop lists** (`evicted[]` already exists; the next step is making it
queryable so "what did we lose" is a one-query question before it becomes an incident).

> **One-line summary:** Make loss measurable: score how many goal-relevant facts
> survived and make the drop list queryable.

### 16.3 Compaction as a First-Class Step Type

Once a plan contains explicit `compact` nodes — at task seams, before risky operations,
before context handed to a sub-agent (→ 09 §16.2) — compaction stops being an
emergency response to a threshold and becomes a designed part of execution. That is the
difference between an agent that survives long runs and one that is merely lucky.

> **One-line summary:** Put explicit `compact` steps in the plan so compaction is a
> design decision, not an emergency.

### 16.4 Beyond Summarization

- **State externalization.** Move large state (test fixtures, file bodies) to a store and keep only handles in context. The strongest form of compaction isn't summarizing the data — it's never putting it there.
- **Tiered residency à la MemGPT**, with the deterministic pin set as the floor beneath the model's paging decisions.

Plain notes: **test fixtures** = fixed sample data used by tests. **Handles** = short
references (like a file path or ID) instead of the full content.

> **One-line summary:** The best compaction is avoiding the bulk in the first place:
> store big state outside and keep only references in context.

---

## References

Sources behind this module. How to read it: papers explain the research, frameworks
are tools you can use today, production systems are shipped implementations.

### Papers & Research

- **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al., 2023 · https://arxiv.org/abs/2307.03172
- **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · https://arxiv.org/abs/2310.08560
- **LongLoRA: Efficient Fine-tuning of Long-Context Large Language Models** · https://arxiv.org/abs/2309.12307
- **StreamingLLM: Efficient Streaming Language Models with Attention Sinks** — Xiao et al., 2023 · https://arxiv.org/abs/2309.17453
- **SWE-agent: Agent-Computer Interfaces for Automated Software Engineering** · https://arxiv.org/abs/2405.15793
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

Plain notes: **attention sinks** (StreamingLLM) = the first tokens of a context,
which models attend to reliably no matter how long the run gets. **Fine-tuning**
(LongLoRA) = cheaply retraining a model to handle longer contexts.

### Frameworks & Tools

1. **Anthropic Claude Code** — https://docs.anthropic.com/en/docs/claude-code — `/compact` and auto-compact
2. **Aider** — https://aider.chat/docs/ — repo map + history digest
3. **Letta (MemGPT)** — https://docs.letta.com/ — tiered memory
4. **LangGraph** — https://langchain-ai.github.io/langgraph/ — summarization node pattern
5. **tiktoken** — https://github.com/openai/tiktoken — exact token counting for triggers
6. **LiteLLM** — https://docs.litellm.ai/ — token accounting per call

Plain notes: **LangGraph** = a library for building agent workflows as graphs; its
"summarization node" is a step that compacts mid-flow. **tiktoken / LiteLLM** = the
two tools that give you the exact token counts the trigger depends on.

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

Plain notes: **fan-out** = copying context to several sub-calls at once. **GDPR** =
the EU privacy law, which constrains what memory may store. **Audit trail** = the
queryable record of what happened.

> **One-line summary:** Six papers, six tools, four shipped systems, and nine
> sibling modules — this module sits in the middle of them all.

---

*Document: Harness 14. Context Compaction — HARNESS ENGINEERING EDITION*
*Cross-cutting module · what lets a fixed context window support an unbounded run*
*Last updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Compaction According to Anthropic (09/2025)

> Added from the article **"Effective context engineering for AI agents"** (Anthropic, 09/2025) —
> more concrete guidance on how to write a compaction prompt and what is actually safe to remove.

This update translates Anthropic's field guidance into the terms of this module.

### 1. Tool Result Clearing — The "Lightest Touch" Compaction

**Old tool results** are the safest removal candidates because: they were already *read*
(not just floating around) and contain only *intermediate state* — not decisions,
not invariants, not the task definition.

In other words, **tool result clearing is the lightest-touch form of compaction**
that still makes sense. If you haven't done anything about compaction, start here — it has
already been shipped by Anthropic as the official **"Context Management"** feature on the Claude
Developer Platform.

Principle: tool results deep in conversation history have already served their purpose;
the model has extracted the needed information from them — **the raw result now just takes up space**.

> **One-line summary:** Old tool results are the safest first thing to clear — the
> model already read them, so the raw text is now dead weight.

### 2. Compaction Prompt Tuning — Start with Recall, Then Iterate Precision

Anthropic recommends a 2-phase process for writing a compaction prompt. **Recall** =
did we keep everything important? **Precision** = did we keep only what's important?

1. **Phase 1 — Maximize recall:** Ask the summarizer to capture **every important piece
   of information** first. It doesn't need to be compact yet — as long as nothing is missed.
   This error (adding too much) is cheaper than the other error (missing something needed).
2. **Phase 2 — Iterate precision:** Once the prompt reaches 100% recall, iteratively try
   removing information that "seems superfluous" and check whether runs are still correct. Repeat
   until precision is high without losing recall.

**Things you MUST keep** (in every compaction):

- Architectural decisions already made
- Unresolved bugs (which bug is open, why)
- Implementation details currently in use
- Current task state — goal + progress + next step

**Things that CAN be dropped:**

- Old raw tool outputs (already read, no longer needed)
- Tool definitions already read (the model doesn't need a reminder of how to use the tool)
- Messages already summarized in the previous compaction

> **One-line summary:** Write the compaction prompt in two passes — first keep
> everything important (recall), then trim until only the important remains (precision).

### 3. Contract With Module 02-Build-Context

Compaction output is the **`history` field** in the `BuiltContext` structure (module 02).
The pin set derives from that boundary:

- **Absolute pin set** = `system` + `goal` — the two parts never cut, no matter
  what compaction happens.
- Every other part of `BuiltContext` (`retrieved`, `immediate`, `history`) is
  in the evictable list and follows the utility-based eviction order (§4).

```
BuiltContext (→ 02)
├── system  ───────────────────► PIN (never cut)
├── goal    ───────────────────► PIN (never cut)
├── retrieved ─────────────────► evictable (by utility)
├── history ────────────────────► evictable (by utility) ← COMPACTION LANDS HERE
└── immediate ─────────────────► evictable (by utility)
```

Reading the diagram: `BuiltContext` is the assembled prompt from module 02. Only
`system` and `goal` are pinned; everything else can be evicted, and compaction
writes its output into `history`.

> **One-line summary:** In module 02's assembled context, only `system` and `goal`
> are uncuttable — compaction's output replaces the `history` field.

### 4. "Keep vs Drop" Table

How to read it: left column = never drop, in any compaction; right column = safe to
drop *after* the information has been read or summarized.

| Keep (never drop) | Can drop (after reading) |
|-------------------|--------------------------|
| Architectural decisions | Old raw tool outputs |
| Unresolved bugs + stack trace | Tool definitions already read |
| Current task state (goal, progress, next step) | Messages summarized in the previous compaction |
| File paths being worked on | Resolved failure branches |
| Invariants / constraints (HEADER/FOOTER, → §7) | Chit-chat, greetings |

**Quick rule to remember:** "discard the thing needed **later** after discarding the thing needed **earlier**" —
a tool result is something needed earlier (you read it to extract information), so after extraction
it becomes "no longer needed" and falls into the droppable group.

> **One-line summary:** Keep decisions, open bugs, task state, active paths, and
> invariants; drop already-read tool output, old definitions, and chatter.

### 5. Sample Code — should_compact + compact

<details>
<summary>Python Code — should_compact + compact with keeping the 5 most recent files (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/13-5-sample-code-should-compact-compact.py`](examples/13-5-sample-code-should-compact-compact.py)

</details>

A minimal Python version of §8.2: check the trigger, keep the 5 most recent files,
and compact the rest.

> **One-line summary:** The smallest working version: trigger check + keep the 5
> most recent files + compact everything older.

### 6. Related In This Repo

- [02-build-context](../02-build-context/README.md) — Compaction output is the
  `history` field in `BuiltContext`; hybrid pre-computed + just-in-time retrieval goes together
  with compaction so context always stays high-signal.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 3**
  (build context) pairs with **Layer 4** (compaction/memory) in the agent architecture.

Plain notes: **just-in-time retrieval** = fetching information exactly when needed,
instead of loading it up front. **High-signal** = mostly useful content, little noise.

> **One-line summary:** Compaction plugs into module 02's context assembly and sits
> in Layer 4 of the architecture, next to memory.
