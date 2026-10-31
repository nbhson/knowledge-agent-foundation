# 🔐 Harness 15. Approval Gates — Human-in-the-Loop for Irreversible Actions

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Are Approval Gates Non-Optional?](#why-are-approval-gates-non-optional)
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Definitions & Vocabulary](#1-definitions--vocabulary)
>   - [1.1 Core Terms](#11-core-terms)
>   - [1.2 The Two Families: Hard Blocks vs Advisory Signals](#12-the-two-families-hard-blocks-vs-advisory-signals)
> - [2. Risk Tiers — What Needs a Gate](#2-risk-tiers--what-needs-a-gate)
>   - [2.1 Tier Taxonomy](#21-tier-taxonomy)
>   - [2.2 Tagging at Plan Time](#22-tagging-at-plan-time)
>   - [2.3 Blast Radius Enumeration](#23-blast-radius-enumeration)
> - [3. Gate Payload — What the Human Sees](#3-gate-payload--what-the-human-sees)
>   - [3.1 The Payload Fields](#31-the-payload-fields)
>   - [3.2 The Mandatory-Evidence Rule](#32-the-mandatory-evidence-rule)
> - [4. Timeout, Deny & Escalation Semantics](#4-timeout-deny--escalation-semantics)
>   - [4.1 The Four Outcomes](#41-the-four-outcomes)
>   - [4.2 Timeout-Deny (Fail Closed)](#42-timeout-deny-fail-closed)
>   - [4.3 Deny → Replan, Not Retry](#43-deny--replan-not-retry)
>   - [4.4 Escalation & Delegation](#44-escalation--delegation)
> - [5. Engine Integration (Pause / Resume)](#5-engine-integration-pause--resume)
>   - [5.1 The Gatekeeper API](#51-the-gatekeeper-api)
>   - [5.2 The PAUSED Protocol](#52-the-paused-protocol)
>   - [5.3 Resume & Idempotency](#53-resume--idempotency)
>   - [5.4 Two-Person Rule Enforcement](#54-two-person-rule-enforcement)
> - [6. Audit Log](#6-audit-log)
>   - [6.1 The Record](#61-the-record)
>   - [6.2 Policy Violation Detection](#62-policy-violation-detection)
> - [7. Human-in-the-Loop UX](#7-human-in-the-loop-ux)
>   - [7.1 Batching & Decision Fatigue](#71-batching--decision-fatigue)
>   - [7.2 Notification Channels](#72-notification-channels)
> - [8. TypeScript Implementation](#8-typescript-implementation)
>   - [8.1 Types](#81-types)
>   - [8.2 Persisted Gatekeeper](#82-persisted-gatekeeper)
>   - [8.3 Engine Loop Integration](#83-engine-loop-integration)
>   - [8.4 Two-Person Gatekeeper](#84-two-person-gatekeeper)
> - [9. Testing Approval Gates](#9-testing-approval-gates)
>   - [9.1 Invariant Tests](#91-invariant-tests)
>   - [9.2 Contract Tests](#92-contract-tests)
>   - [9.3 Regression Suite](#93-regression-suite)
> - [10. Real-World Case Studies](#10-real-world-case-studies)
>   - [10.1 Claude Code — Permission Modes & Confirmation](#101-claude-code--permission-modes--confirmation)
>   - [10.2 Aider — Read/Write Modes as a Deny-By-Default Canon](#102-aider--readwrite-modes-as-a-deny-by-default-canon)
>   - [10.3 OpenHands — Confirmation Modes](#103-openhands--confirmation-modes)
>   - [10.4 Devin — Asynchronous Oversight](#104-devin--asynchronous-oversight)
>   - [10.5 Human-AI Delegation Research — Automation Bias](#105-human-ai-delegation-research--automation-bias)
> - [11. TypeScript Interfaces for Approval](#11-typescript-interfaces-for-approval)
> - [12. Design Principles for Approval](#12-design-principles-for-approval)
>   - [12.1 SOLID for Approval Systems](#121-solid-for-approval-systems)
>   - [12.2 Six Design Principles](#122-six-design-principles)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do-)
>   - [13.2 DON'T ❌](#132-dont-)
> - [14. Anti-Patterns & Solutions](#14-anti-patterns--solutions)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Future Trends in Approval](#16-future-trends-in-approval)
> - [References](#references)
>
> **Cross-cutting module.** Approval gates are the one place where a
> person steps into the *running* loop, not just the setup. Every other part
> lets the run decide and act on its own; this one adds a thoughtful pause —
> the cheapest safety net in the whole harness (→ 12 §1.2, → 06 §17.4).

---

### Opening Story

What this explains: a real-shaped story of a 3 AM near-miss, so you can see what a gate actually prevents before we define it.

3:47 AM. A migration run has been going for six hours. The agent, confident and on
turn 214, has just detached a stalled `db.migrate` retry (a command that changes the
database's structure) and decided it is "stuck in
incremental steps," so it builds a recovery path: `ALTER TABLE users DROP COLUMN
mfa_secret` — a SQL command that permanently deletes one column of the `users`
table. Why? A downstream check complained the column is `NOT NULL` without a
default, and the agent's crude model of "remove the blocker" won.

The column held 2.1M MFA enrollments (MFA = multi-factor authentication, the
"second step" login codes users set up). There's no backup of it. The action is
irreversible, destructive, and *wrong*.

What keeps this from becoming a late-night disaster is one kind choice the harness made
earlier: **tag `prod-auth` at plan time, pause the run, and show a person the "before"
evidence, not the model's reasoning.** (Tagging at plan time = labeling risky actions
as needing approval *before* anything runs. Evidence = the actual diff, not a
"trust me" summary.) The gate pops up. The human looks at a 12-line
diff at 3:47 AM, says "no", adds a reason, and twenty minutes later the agent plans
around the change — *without ever touching the column*.

The gate didn't make the agent smarter. It made the harness *safe to be wrong* — which
is the only thing that really counts for self-running systems. Every bold action
that almost happened and a person calmly stopped is invisible in the metrics, costs nothing, and is
the whole point.

> **One-line summary:** A gate turned a 3 AM "agent silently deletes a column" disaster into a 20-second "human says no" moment.

### Why Are Approval Gates Non-Optional?

> *"An agent that can confidently ask for production credentials at 3 AM and receive
> them isn't an agent. It's a muzzle-loading cannon."*

#### The Math of Confident Failure

Signpost: this part gives the numbers behind the rule — why the rare, expensive mistakes are the ones gates exist for.

LLM agents are wrong at non-trivial rates and *never know it* — calibration studies
consistently show overconfidence that grows with context size and plan depth (→ 10.5).
(Calibration = how well the model's own confidence matches reality; overconfident means
it is wrong more often than it acts wrong.) Put that against the blast radius of the actions agents are asked to take.
**Blast radius** = the set of things that get damaged if the action goes wrong.

How to read the table: each row is one kind of action. Column 1 names the action
(`edit_file` = change a source file; `db.migrate` = change a production database's
structure; IAM = identity and access management, i.e. who is allowed to do what;
`git push --force` = overwrite the commit history on the remote repo, erasing the
backup that history provides). Column 2 says how often the *decision* is wrong.
Column 3 says how bad it is when it is wrong.

| Action | Error rate of the *decision* | If wrong, blast radius |
|--------|------------------------------|------------------------|
| `edit_file` in `src/` | high (hallucinated APIs, wrong file) | locally reversible via git |
| `db.migrate` on prod | low but *catastrophic when wrong* | irreversible schema, hours of rollback |
| `user.delete` / IAM change | rare | permanent, identity + compliance |
| `git push --force` | low-frequency, high-novelty | shared history rewritten, multi-repo blast |

The failure modes that kill companies aren't the frequent ones — they are the rare
ones whose cost dominates the whole distribution. A gate is a *guard at the expensive
tail*, and it costs essentially nothing on the frequent cheap tail (`read` tier is
auto-approved).

The second, subtler force: **a human-in-the-loop gate changes agent behavior, not just
outcomes.** Models instructed that an irreversible action requires a visible, auditable,
second-party approval are measurably more conservative in their reasoning — they stop
"improvising" destructive recovery paths because they know the plan will be *shown*,
not just executed. The gate is a deterrent before it's a firewall.

> **One-line summary:** Rare mistakes cost the most; a gate guards exactly that expensive tail and is nearly free everywhere else.

#### Core Philosophy

Approval is **not** "ask a person about everything" and **not** "never ask." It's:
*spot risky work early, show clear evidence for the blast radius, and let
failures be loud and easy to review instead of quiet and costly.* The gate should be the
spot where the system is *meant to pause*, so that when the agent is wrong — and it
will be — being wrong stays cheap and visible.

> **One-line summary:** Ask only where risk is high, show hard evidence, and make failures loud and cheap instead of silent and costly.

## Overview

> **📌 Core Concept**
>
> - **Concept:** An approval gate is a pause point before an irreversible or high-blast-radius action: execution freezes, a human sees *what / why / blast radius / rollback*, and the run resumes only on approve (or replans on deny/timeout).
> - **Analogy:** Like a bank vault requiring two keys — the agent holds one (the plan), the human holds the other (the judgment). Either key alone opens nothing.
> - **Why it matters:** Agents are wrong with confidence. Without gates, one hallucinated `prod.db.drop()` (a command that deletes a whole production database) or `git push --force` at 3 AM becomes an incident. Gates are the cheapest incident insurance in the whole harness.

**Approval Gates** are the friendly control layer for actions where getting it wrong would hurt more
than the agent's guess is worth. They work hand in hand with sandboxing (→ 12): the sandbox
sets *what an agent can touch* (an allowlist — "danh sách trắng" style whitelist of permitted
paths and tools), the gate decides *what a trusted person should
see first*. One is a technical limit; the other is a team agreement.

The diagram below is the whole module in one picture. Read top to bottom: the agent wants to
act, a tier check at plan time decides how much approval it needs, then the gate opens
(payload shown, run paused, timer armed, audit written), and finally the human's verdict
routes the run to one of four endings.

```
AGENT WANTS TO ACT
     │
     ▼
┌──────────────────────────────────────────────┐
│ TIER CHECK at plan time (→ 04 §14.3)         │
│ read        → auto-approve, log only         │
│ write       → diff preview + 1-click, 5 min  │
│ elevated    → typed confirm + dry-run        │
│               + rollback, 30 min             │
│ prod-auth   → TWO-PERSON rule, 4h + page     │
└──────────────────────────────────────────────┘
     │ if tier ≥ write
     ▼
┌──────────────────────────────────────────────┐
│ GATE OPENS                                    │
│ 1. payload rendered (what/why/blast/rollback) │
│ 2. engine PAUSED at a checkpoint (→ 07 §13)   │
│ 3. timeout-deny race armed                    │
│ 4. audit record written (hash-linked, → 13)   │
└──────────────────────────────────────────────┘
     │
     ▼
 HUMAN -> approve ──────────────▶ resume same runId
       │  -> deny + reason ──────▶ replan excluding branch
       │  -> no verdict ──────▶ timeout → deny (fail closed)
       │  -> escalated ───────▶ on-call page, delegation w/ trail
```

Gloss for the diagram: **dry-run** = a rehearsal of the action with no real effects (like
`terraform plan` showing what *would* change); **checkpoint** = a saved snapshot of run
progress so it can resume later; **hash-linked** = each audit record stores a fingerprint
(hash) of what was shown, so nobody can secretly swap the content; **runId** = the unique
ID of one run; **page** = wake the on-call engineer via pager alert.

**The gate has a lifecycle, not a boolean:** one `request()`, three settled outcomes
(`approved` / `denied` / `expired`), one audit trail, zero silent branches. Any
implementation that can't answer "who, what, when, and why *for every irreversibility*"
isn't an approval system — it's a button with extra steps.

> **One-line summary:** A gate is a mandatory pause with full evidence before risky actions; the human's verdict is the only way the run continues.

## Contents

How to read it: this table is the map of the rest of the document. Column "#" is the
section number, "Topic" is the short name, "Description" says in one line what you'll
learn there.

| # | Topic | Description |
|---|-------|-------------|
| 1 | [Definitions](#1-definitions--vocabulary) | Vocabulary and the two families |
| 2 | [Risk Tiers](#2-risk-tiers--what-needs-a-gate) | What needs a gate, tagged at plan time |
| 3 | [Gate Payload](#3-gate-payload--what-the-human-sees) | What the human sees, mandatory evidence |
| 4 | [Timeout & Deny](#4-timeout-deny--escalation-semantics) | Fail-closed semantics, replan, escalation |
| 5 | [Pause / Resume](#5-engine-integration-pause--resume) | Engine integration, PAUSED protocol, idempotency |
| 6 | [Audit Log](#6-audit-log) | The immutable record and policy violations |
| 7 | [Human UX](#7-human-in-the-loop-ux) | Batching, decision fatigue, notifications |
| 8 | [Implementation](#8-typescript-implementation) | Runnable Gatekeeper + engine loop |
| 9 | [Testing](#9-testing-approval-gates) | Invariants + contract tests |
| 10 | [Case Studies](#10-real-world-case-studies) | Claude Code, Aider, OpenHands, Devin, automation bias |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-for-approval) | Full type surface |
| 12 | [Design Principles](#12-design-principles-for-approval) | SOLID for approval |
| 13 | [Best Practices](#13-best-practices) | DO / DON'T |
| 14 | [Anti-Patterns](#14-anti-patterns--solutions) | Common failures |
| 15 | [Production Checklist](#15-production-checklist) | Ship gate |
| 16 | [Future Trends](#16-future-trends-in-approval) | 2026-2028 |

> **One-line summary:** The document moves from vocabulary → risk tiers → the payload humans see → timeout/deny rules → engine integration → audit → UX → code → tests → case studies → checklists.

---

## 1. Definitions & Vocabulary

Signpost: these seven terms come back in every later section, so learn them once here.

### 1.1 Core Terms

How to read it: column 1 is the term, column 2 is a plain definition, column 3 names the
mistake that breaks it ("fails when…" = what bad implementations do).

| Term | Definition | Fails when… |
|------|-----------|-------------|
| **Approval gate** | Workflow node in state `WAITING_APPROVAL`; persists, notifies, resumes on verdict | only in-memory → lost on restart |
| **Blast radius** | Enumerated set of affected resources if the action runs (files, DBs, envs, users) | vague ("prod stuff") → human cannot judge |
| **Dry-run** | Side-effect-free preview of the action (plan diff, `terraform plan`, `--dry-run`) — mandatory in gate payload | skipped → approval is blind |
| **Timeout-deny** | No verdict within TTL → treated as **deny** (fail closed), never as approve | fail-open → "I was going to approve it" |
| **Two-person rule** | Proposer ≠ approver; a second independent human decides | self-approval → reverts to no gate |
| **Deny → replan** | A deny records `reason` and triggers replanning that excludes the denied branch (→ 04 §14.2) | deny → retry same → loops forever |
| **Approval event** | Every request + verdict written to trajectory as `approval_request` / `approval_verdict` (→ 13) | not traced → post-incident review is impossible |

Plain examples: **TTL** = time-to-live, the timer on a gate (e.g. 5 minutes). **Fail
closed** = when something goes wrong, the safe answer is "no" — like a door that locks
itself when power cuts. **Trajectory** (→ 13) = the full event log of a run, so you can
replay what happened.

> **One-line summary:** A gate is a durable wait-state with evidence (dry-run, blast radius), a timer that defaults to "no", and a second-person rule — each term fails in a specific, known way.

### 1.2 The Two Families: Hard Blocks vs Advisory Signals

Signpost: this section separates two look-alike mechanisms so you don't mix them — mixing them is how gates rot.

How to read it: each column is one mechanism. A **hard block (gate)** freezes the run
until a person answers. An **advisory signal** just shows a warning (banner = on-screen
notice; toast = small pop-up message) and lets the run continue.

| | **Hard block (gate)** | **Advisory signal** |
|---|---|---|
| **What it does** | Freezes the run until a verdict | Warns the user, keeps running |
| **State machine** | `request → WAITING_APPROVAL → settle` | banner / toast / highlighted line |
| **Used for** | Irreversible, high-cost, high-blast actions | Suspicious-but-reversible patterns |
| **If ignored** | run does not proceed | run proceeds with a visible note |
| **Audit** | full request + verdict record | optional, often absent |
| **Cost** | human attention, real latency | near-zero |
| **Danger** | over-gating → approval fatigue (→ 7.1) | under-gating → "we warned them" incidents |

The trap is mixing them: turning advisory signals into hard blocks (every `npm install`
becomes a click → humans rubber-stamp → the *real* gates get approved in muscle memory),
or turning hard blocks into advisory signals ("confirmation but the run continues").
Pick one per action. A gate is a gate is a gate.

> **One-line summary:** Hard blocks stop the run and demand a verdict; advisories only warn — never convert one into the other or both stop working.

---

## 2. Risk Tiers — What Needs a Gate?

Signpost: this section defines the four risk levels and how each one gets tagged, so the model never picks its own approval level.

### 2.1 Tier Taxonomy

How to read it: rows go from safest to riskiest. "Gate" = what approval the action
needs. `rm -rf` = the shell command that deletes a folder and everything inside it,
with no trash bin. `push --force` = overwrite remote git history.

| Tier | Examples | Gate |
|------|----------|------|
| `read` (low) | `read_file`, `grep`, `list`, `view` | Auto-approve, log only |
| `write` (medium) | `edit_file` in `src/`, `run_tests`, local commits | Diff preview + one-click approve, 5-min expiry |
| `elevated` (high) | `db.migrate`, `deploy`, `user.delete`, `external.send`, `push --force`, `rm -rf` | Typed confirm + reason + dry-run + rollback cmd, 30-min expiry |
| `prod-auth` (critical) | IAM change, secret rotation, prod data delete, payment/legal action | Two-person rule (proposer ≠ approver) + incident channel notice, 4h + page |

**The tier is a property of the *action class*, not of the specific invocation.** Push
to a feature branch is `write`; force-push to `main` is `elevated`; force-push to a
shared `release/*` branch is `prod-auth`. (Feature branch = a side branch for one piece
of work; `main` = the shared primary branch.) The mapping lives in the permission/risk
table (`permission.ts`), updated in review — never inferred per-message by the model.

> **One-line summary:** Four tiers from read to prod-auth, each with a fixed approval cost — and the tier belongs to the action type, not to what the model claims.

### 2.2 Tagging at Plan Time

Signpost: this explains *when* tiers get assigned — at plan time, before anything runs — and why that order matters.

Tiers are assigned **at plan time** (→ 04 §14.3), not at execution time:

1. The planner emits each task/tool with an explicit `tier` field.
2. The engine validates the tier against a global risk table before the step even
   builds its payload.
3. The model can't self-downgrade — a request to "just run this as `write`" isn't a
   policy path; changing the tag is a policy change that must come from the risktable
   owner. (Self-downgrade = the model deciding for itself "this is only medium risk.")

> **Rule:** *the agent proposes, the engine enforces, the human overrides only via a
> recorded reason.* Tag-at-plan-time is what makes that three-way split possible —
> without it, the model picks its own speed bumps and picks the ones it can ignore.

The diagram shows the three moments: the plan assigns tiers, the toolbox checks them
against `permission.ts`, and the engine blocks anything mislabeled right before it runs.

```
plan time (→ 04)     build time (→ 08)          exec time (→ 07)
┌────────────────┐   ┌─────────────────┐        ┌─────────────────────┐
│ task 3          │   │ toolbox (→ 06)   │        │ task 3 arrives,      │
│  tier write      │   │  tiers from      │        │ risk table check     │
│ task 5          │   │  permission.ts   │        │ tier=write ok        │
│  tier elevated   │──▶│  + per-role      │───────▶│ task 5 tier=elevated │
│ task 8          │   │  override        │        │ → GATE REQUESTED     │
│  tier prod-auth  │   │  (audited)       │        └─────────────────────┘
└────────────────┘   └─────────────────┘
```

> **One-line summary:** Tiers are stamped on the plan and checked by the engine — the model proposes but never chooses its own risk level.

### 2.3 Blast Radius Enumeration

Signpost: this explains how the system lists, precisely, everything a risky action touches — the list the human needs in order to judge.

**Enumeration** = listing each item one by one. A gate payload is only as good as its blast-radius enumeration. The system must
enumerate, from the sandbox/policy registry (→ 12 §6), the exact set of resources the
action touches (registry = the central catalog of known resources and their owners).

```
ACTION:   db.migrate 20260719_add_mfa_cols (tier: elevated)
BLAST:    prod-db.host=postgres-5a2f (primary, no replica for this schema)
          database=users  size=2.1M rows
          table migration lock ~4s (downtime window: ok)
          0 down migrations — NOT reversible by migration engine
          connected microservices: auth-svc (read), consent-svc (write)
```

Gloss: `db.migrate` here adds MFA columns to a table; "migration lock ~4s" = the table
is briefly locked for writes for about 4 seconds; "0 down migrations" = there is no
pre-written undo script, so the migration engine cannot reverse it; microservices =
small separate backend services (auth-svc handles login, consent-svc handles user
consent).

Enumeration failure modes — how to read it: column 1 is the mistake, column 2 a real
example of it, column 3 the fix.

| Failure | Example | Fix |
|---------|---------|-----|
| Too coarse | "edits prod database" | exact db, host, size, lock estimate |
| Missing blast | forgets connected services | registry-driven enumeration, not model-written |
| Confusing with cost | "costs $0.40" listed but no lock time | cost is a *row* in the payload, not the blast radius |
| Rollback unproven | "rollback: revert migration" with no test | `rollback` field must carry a tested command/hash |

> **One-line summary:** The blast-radius list must come from the registry — exact database, size, lock time, connected services, and a tested undo command — never from the model's own summary.

---

## 3. Gate Payload — What the Human Sees

Signpost: this section defines the exact card of information a person sees when a gate opens.

### 3.1 The Payload Fields

A sample payload, field by field: ACTION = what will run and its tier; TASK = which
plan step this belongs to; DIFF = the actual text change; BLAST = what it touches;
DRY-RUN = rehearsal result; ROLLBACK = the tested undo command; COST = price in
money and time.

```
ACTION:   db.migrate (tier: elevated)
TASK:     auth-refactor / step 3 (trajectory: traj_x, event: evt_41)
DIFF:     +ALTER TABLE users ADD COLUMN mfa_secret TEXT (12 lines…)
BLAST:    prod-db.users (2.1M rows), lock ~4s, 0 down migrations
DRY-RUN:  ✓ shadow-migrate passed (3.8s), rollback tested
ROLLBACK: db.migrate down v48 (cmd attached, tested 2h ago)
COST:     ~$0.40, ~90s                       [Approve] [Deny + reason]
```

Every field must be **derived from evidence**, not narrated (narrated = the model
describing in words what it claims is true, with no proof):

How to read it: column 1 is the payload field, column 2 says where the value must come
from, column 3 says what goes wrong if the field is missing.

| Field | Source | Absent → |
|-------|--------|----------|
| `ACTION` + `tier` | the step's tier tag (→ 2.2) | gate cannot render |
| `TASK` + trajectory link | plan graph node + span IDs (→ 04, 13) | post-incident review cannot replay |
| `DIFF` | the actual command/materialized diff | approve is blind |
| `BLAST` | registry enumeration (→ 2.3) | human under-judges |
| `DRY-RUN` | the dry-run *output*, hash-linked | approve is an act of faith |
| `ROLLBACK` | tested rollback command + when it was tested | approve commits to irreversibility |
| `COST` | estimated tokens/money/time | human cannot compare options |

> **One-line summary:** Every payload field is machine-derived evidence — diff, blast radius, dry-run output, tested rollback — not the model's word for it.

### 3.2 The Mandatory-Evidence Rule

Signpost: this section turns the payload table into a hard rule: no evidence, no gate, no action.

> **No dry-run → no gate → action blocked.** The gate refuses to open if any
> mandatory-evidence field is empty. This is *not* a UX nicety — it's the invariant
> that makes approval different from consent. (Invariant = a rule that must always
> hold, checked by the system itself.)

Implementation-wise it's a validation function that runs *before* `request()` is
called:

> 📄 **Example code:** [`examples/01-3-2-the-mandatory-evidence-rule.ts`](examples/01-3-2-the-mandatory-evidence-rule.ts)

A `request()` with a non-empty `missing` array throws; the run **can't** proceed until
the evidence exists. Teams that allow "approve anyway" on an invalid payload consistently
discover that the approve button becomes a *posting medium for un-reviewed actions*.

The payload itself is a trajectory event (→ 13), so post-incident review replays
exactly what the human saw — including the dry-run output that justified (or failed to
justify) the verdict.

> **One-line summary:** If any evidence field is empty, the gate throws and the action is blocked — "approve anyway" must not exist.

---

## 4. Timeout, Deny & Escalation Semantics

Signpost: this section defines the only four ways a gate can end, and the rules for the awkward ones (nobody answers, answer is "no", answer is late).

### 4.1 The Four Outcomes

How to read it: column 1 is the outcome name, column 2 is what happened in plain
words, column 3 is what the run does next.

| Outcome | Meaning | Next state |
|---------|---------|-----------|
| `approved` | human verified evidence, run resumes | continues on same `runId`, idempotency cache skips done steps |
| `denied` | human rejects with a reason | task marked `blocked(denied)`, replan excludes branch |
| `expired` | no verdict within TTL | treated exactly as deny (fail closed), unless escalated |
| `escalated` | TTL crossed a threshold and on-call was paged | new TTL, delegation chain recorded |

Gloss: **idempotency cache** (→ 08 §11) = a memory of finished steps so a resumed run
skips them instead of running them twice. **On-call** = the engineer on duty who can be
paged. The state machine is small and closed; any implementation that "creates" a new outcome
at runtime (e.g. *"user said ok on Slack"*) is a policy gap, not a feature.

> **One-line summary:** Only four endings exist — approve, deny, expire (which counts as deny), escalate — and inventing a fifth at runtime is a bug.

### 4.2 Timeout-Deny (Fail Closed)

Signpost: this section covers the timer: what happens when no human answers in time.

Time budgets per tier: `write` 5 min · `elevated` 30 min · `prod-auth` 4h + page.

- Expiry marks the task `blocked(approval-timeout)` — a distinct state from `denied`,
  because the *next* action differs (see 4.3).
- **Fail closed, never fail open.** Expiry must never be interpreted as approval. The
  one exception requiring explicit policy sign-off: a *store-closed, unattended* deploy
  window where the approved-timeout is documented as "expired = rolled back and paged".
  (Sign-off = a named person formally accepting the risk, in writing.)
- The expiry timer runs in the *engine*, not in the UI session. Closing the review
  laptop can't extend a gate's life.

> 📄 **Example code:** [`examples/02-4-2-timeout-deny-fail-closed.ts`](examples/02-4-2-timeout-deny-fail-closed.ts)

> **One-line summary:** When the timer runs out the answer is always "no" — expiry is computed by the engine, never by whether someone's laptop is open.

### 4.3 Deny → Replan, Not Retry

Signpost: this section explains what a "no" should trigger: a new plan, never the same question again.

- Record `reason` — it's the *most valuable* audit artifact in the whole gate: it
  tells future planners what the human rejects, and repeated denials on the same reason
  are a product signal (the agent keeps proposing things the team doesn't want).
- Trigger replanning that excludes the denied branch (→ 04 §14.2). Never re-ask the
  same payload twice. If the *same* plan can satisfy the denial another way, the planner
  emits a new plan; the new plan generates a *new* gate only if the new action is again
  high-tier.
- Repeatedly re-asking the identical action after a deny is the #1 way approval systems
  become contemptible, and the #1 way they get bypassed by users who approve "just to
  stop the noise."

> **One-line summary:** A deny records the reason and sends the planner back to the drawing board — asking the same question again trains humans to approve to make the noise stop.

### 4.4 Escalation & Delegation

Signpost: this section covers the cases where the first approver isn't available: paging on-call and handing approval to someone else.

- **Page on-call** if `elevated` stays ungated >15 min in prod hours (or >T for non-prod,
  configurable). The run stays frozen at the checkpoint (→ 07 §13); the checkpoint is the
  safety property that makes escalation free.
- **Approval delegation** allowed (on-call → secondary) — but *delegation is separate
  from the two-person rule*: delegating the notification doesn't turn one approver into
  two. For `prod-auth`, delegation keeps the two-person requirement (proposer + one
  independent approver); it can change *who* that approver is, never *how many*.
  (Delegation = forwarding the approval request to another qualified person.)
- Every hop of the escalation chain (`paged_oncall` → `delegated_to:x` → `approved`)
  is an audit entry. The chain is what makes "who actually decided?" answerable under
  scrutiny.

> **One-line summary:** Stuck gates page a human; approval can be forwarded to a different person but never reduced to fewer people, and every hop is logged.

---

## 5. Engine Integration (Pause / Resume)

Signpost: this section shows how the gate hooks into the run engine — how the run stops, survives a crash, and continues after a verdict.

### 5.1 The Gatekeeper API

Signpost: the Gatekeeper is the component that owns gates: it takes requests, waits, and records verdicts. The full API lives in the example file.

> 📄 **Example code:** [`examples/03-5-1-the-gatekeeper-api.ts`](examples/03-5-1-the-gatekeeper-api.ts)

> **One-line summary:** The Gatekeeper is the single owner of every gate: request in, verdict out, record written.

### 5.2 The PAUSED Protocol

Signpost: this explains the surprising design choice — pausing is a thrown, typed state, not a "wait" loop — and why that makes gates survive crashes.

The engine does **not** "wait." It throws a typed `PAUSED:<key>` after checkpointing
(a `PAUSED:gate_9a3f` exception means "this run is parked, waiting on gate `gate_9a3f`"):

- **Checkpoint first, then throw.** All completed steps are in the idempotency cache
  and trajectory store (→ 07 §13, → 13). Pausing *without* a checkpoint means resume
  can't distinguish "never ran" from "ran and half-finished."
- `PAUSED:<key>` propagates to the driver/CLI/UI as a first-class state, not an error.
  The human's "approve" is a *verdict delivery*, not a restart.
- **The run object persists.** A gate survives process death: on restart, the
  Gatekeeper reloads open gates from the trajectory store, re-arms their timers, and
  any run still pinned at a `WAITING_APPROVAL` checkpoint resumes or expires correctly.
  (Re-arms = restarts the countdown timer from where it should be.)

The diagram traces one gate end to end: tier check at turn 214, checkpoint saved, gate
requested, process may even die and restart, then the human approves and the run
resumes from the cache.

```
turn 214  pre_gate_check ──────▶ tier=elevated
    │
    ▼
checkpoint(runId, "t214")      ──▶ trajectory: snapshot_link
    │
    ▼
gatekeeper.request(key=gate_9a3f, …)
    │ emits approval_request { key, tier, diffHash, dryRunHash, expiresAt }
    │ writes audit record
    │ throws PAUSED:gate_9a3f
    │
    ▼       [process restarts? reload open gates, re-arm timers]
    │
    ▼   human settles gate_9a3f = approved
    │
    ▼
resume(runId) ──▶ replay cache hit for t1..t214 ──▶ t215 proceeds
    (or)       ──▶ denied/expired ──▶ mark blocked → replan (→ 04 §14.2)
```

> **One-line summary:** Pausing = save a checkpoint, then throw a typed PAUSED state that survives restarts — approval later resumes the same run, nothing re-runs.

### 5.3 Resume & Idempotency

Signpost: this section shows why resuming after a gate is safe: finished steps are skipped, and the gated action runs exactly once.

- Resume re-invokes the run with the **same `runId`**; completed steps hit the
  idempotency cache and skip (→ 07 §13, 08 §11). Nothing re-executes, nothing
  re-asks.
- The gated action itself is re-run **only after** approval, exactly once — the
  checkpoint sits *before* the action, so resume re-runs the action, not a crossed
  boundary.
- Idempotency of the *approval*: settling the same key twice is a no-op (`if (!g ||
  g.verdict) return`). A double-clicked "approve" can't double-run a migration.

> **One-line summary:** Resume reuses the same runId and skips everything already done; the gated action runs once, and a double-clicked Approve is harmless.

### 5.4 Two-Person Rule Enforcement

Signpost: this section shows where the "second pair of eyes" rule is actually enforced — inside the settle function, not in the interface.

`prod-auth` gates require a second pair of human eyes whose identity differs from the
proposer (proposer = whoever — or whatever step — created the gate request):

> 📄 **Example code:** [`examples/04-5-4-two-person-rule-enforcement.ts`](examples/04-5-4-two-person-rule-enforcement.ts)

The proposer is recorded at `request()` time (the step that spawned the gate). The rule
is enforced *inside* `tryApprove`, so there's no model path around it. Self-approval
attempts aren't silent — they are audited as a policy event, which is itself a
weird-behavior signal worth watching.

> **One-line summary:** The proposer is stamped at request time and the "approver ≠ proposer" check lives inside the code path — self-approval is impossible, and any attempt is logged.

---

## 6. Audit Log

Signpost: this section defines the permanent record each gate leaves, and how automated checks turn that record into policy enforcement.

### 6.1 The Record

Every gate writes an immutable record: `{key, tier, actor(proposer), approver, verdict,
reason, diffHash, dryRunHash, at}` → trajectory store (→ 13) + SIEM. (Immutable =
cannot be edited after writing; SIEM = a central security system that collects logs
from everything for alerting and review.)

How to read it: column 1 is the record field, column 2 says in plain words what it
holds, column 3 says which rule or analysis depends on it. `diffHash` = a fingerprint
of the exact diff the human saw; if content changes, the hash changes.

| Field | Meaning | Required for |
|-------|---------|-------------|
| `key` | opaque gate id | join across request/verdict |
| `tier` | risk tier | approval-rate analytics (→ 9.3) |
| `actor` | proposer (who triggered the run) | two-person rule |
| `approver` | who settled | delegation chain, two-person rule |
| `verdict` | approved/denied/expired | outcome analytics |
| `reason` | human's free text | replan input, product signal |
| `diffHash` | hash of the diff shown | prove what was approved |
| `dryRunHash` | hash of the dry-run evidence shown | prove evidence existed |
| `at` | timestamp | latency, time-of-day patterns |

The `diffHash`/`dryRunHash` pairing is the heart of the audit: it makes "approve a
*different* action than the one shown" impossible to launder (launder = sneak past
review by swapping the content after the human looked). If the payload rendered at
request time hashes to X but the executed action hashes to Y ≠ X, that is a hard
incident, flagged automatically.

> **One-line summary:** Every gate leaves a tamper-evident record whose hashes prove the human approved exactly what was shown.

### 6.2 Policy Violation Detection

Signpost: this section lists the checks that run over the audit stream automatically, so violations surface without waiting for a human to notice.

Automated checks over the audit stream:

- Gate approved **without** a `dryRunHash` → policy violation, flag + page (unless the
  action class is in an explicit "no-dry-run" allowlist, which itself must be approved).
  (Allowlist = an explicit "these exceptions are permitted" list.)
- `approver === actor` on a `prod-auth` gate → violation (self-approval).
- Verdict recorded **after** the action already touched resources → violation
  (out-of-order approval).
- Timeout-deny that was followed by a *new identical request* within X minutes →
  violation of deny→no-retry (→ 4.3).

Quarterly review cadence (cadence = fixed schedule): approval rate per tier, median wait, override incidents,
delegation-chain depth. The point of the review isn't policing — it's *design*
intelligence: a tier with a 98% approval rate and 30-second median wait isn't being
read, it's being rubber-stamped, and the gate has become theater (→ 14).

> 🔑 **Policy / Permission highlight:** this section is the **policy-compliance sensor** — it turns the audit log (§6.1) into enforceable policy verdicts (missing dry-run evidence, self-approval, out-of-order approval, deny→retry). Pair with `12-sandbox-execution` (deny-by-default) and `06` §8 (RBAC) for the full policy loop: decide → enforce → audit → detect.

> **One-line summary:** Automated checks on the audit stream catch missing evidence, self-approvals, out-of-order verdicts, and deny-then-retry — and a 98% approval rate is itself the alarm.

---

## 7. Human-in-the-Loop UX

Signpost: this section is about the human's experience — because a gate that wastes attention gets approved blindly.

### 7.1 Batching & Decision Fatigue

Signpost: this explains why fewer, grouped gates beat one gate per action.

Humans are the scarce, expensive resource; the design target is *minimum tokens of
human attention per safe decision* (batching = grouping several small approvals into
one review).

- **One notification per decision**, not one per action — batch `write`-tier edits in
  a single reviewable diff when they belong to the same step.
- **Context, not trivia.** Show the *task it belongs to*, the *plan phase*, the
  *previous attempt* — so a "deploy" approval during a rehearsed run reads differently
  from one mid-refactor.
- **Default-action guidance**: the payload should make the *right* decision the easy
  one. If the correct answer is usually "deny", the approve path costs more friction, not
  less (typed confirm + reason on `prod-auth`). (Friction = extra effort, e.g. typing a
  reason, added on purpose to slow down a risky click.)
- **Fatigue is the #1 silent failure** — measured as a rising approval rate with
  falling median decision time. When that happens, the gate is no longer protecting; it
  is cosigning. Fix by *raising* the tier bar, not by removing gates.

> **One-line summary:** Batch small approvals, show context, add friction where "no" is right — because approval fatigue turns gates into rubber stamps.

### 7.2 Notification Channels

Signpost: this maps each tier to where its approval request should arrive and how loud it should be.

How to read it: column 1 is the tier, column 2 is the channel (in-app = inside the
product; push + email = phone/desktop alerts; page = pager that wakes a human), column
3 is the intended tone.

| Tier | Channel | Tone |
|------|---------|------|
| `write` | in-app/PR comment; quiet, batched | informative |
| `elevated` | push + email, actionable | needs attention, 30-min budget |
| `prod-auth` | incident channel + page; two-person | escalation, 4h TTL |

Every notification carries the *same* payload the UI would show (diff, blast, dry-run
hash) — no channel truncates the evidence, because a truncated channel silently lowers
the quality of the decision. Notification delivery is itself traced (`notification_sent`
event → 13) so "the human never saw it" is a checkable claim, not an excuse.

> **One-line summary:** Louder tiers get louder channels, every channel carries the full evidence, and delivery itself is logged so "nobody saw it" is checkable.

---

## 8. TypeScript Implementation

Signpost: this section points to runnable code for each piece described above.

### 8.1 Types

> 📄 **Example code:** [`examples/05-8-1-types.ts`](examples/05-8-1-types.ts)

> **One-line summary:** Start from the types — GateRequest, Verdict, and the tier enum — since they encode the rules in this module.

### 8.2 Persisted Gatekeeper

A **persisted** Gatekeeper = one that saves gates to disk, so they survive a process
restart and reload with timers re-armed (see §8.2 of the example, "reload + audit").

<details>
<summary>TypeScript Code — persisted Gatekeeper with reload + audit (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-8-2-persisted-gatekeeper.ts`](examples/06-8-2-persisted-gatekeeper.ts)

</details>

> **One-line summary:** The Gatekeeper must persist gates and reload them on restart — an in-memory gate forgets what it was guarding.

### 8.3 Engine Loop Integration

> 📄 **Example code:** [`examples/07-8-3-engine-loop-integration.ts`](examples/07-8-3-engine-loop-integration.ts)

Note what the engine loop *doesn't* contain: no branch where the model "asks nicely" and
continues. The only way past the throw is a persisted verdict from the Gatekeeper —
which is the whole integrity story.

> **One-line summary:** The loop has no "pretty please" path — only a persisted verdict gets a run past a gate.

### 8.4 Two-Person Gatekeeper

> 📄 **Example code:** [`examples/08-8-4-two-person-gatekeeper.ts`](examples/08-8-4-two-person-gatekeeper.ts)

> **One-line summary:** The two-person variant is a drop-in subclass that adds the proposer ≠ approver check inside approval.

---

## 9. Testing Approval Gates

Signpost: this section lists the three test layers that prove gates actually work — including after a crash.

### 9.1 Invariant Tests

**Invariant tests** = checks that a rule always holds, e.g. "an expired gate is never
approved."

> 📄 **Example code:** [`examples/09-9-1-invariant-tests.ts`](examples/09-9-1-invariant-tests.ts)

Run these across **every recorded gate in production** (like §9.1 of → 13): the invariant
suite is cheap and catches regressions the unit tests never will — e.g. a timer that
doesn't survive a restart.

> **One-line summary:** Cheap always-true checks, replayed over real production gates, catch regressions unit tests miss.

### 9.2 Contract Tests

**Contract tests** = tests of promises between components, here mostly: "kill the
process mid-gate, restart, and the gate must still be enforced."

> 📄 **Example code:** [`examples/10-9-2-contract-tests.ts`](examples/10-9-2-contract-tests.ts)

The restart test is the one teams skip, and it's the one that proves a gate is a
*durable security control* rather than a memory object.

> **One-line summary:** The restart test is the one that proves gates survive crashes — don't skip it.

### 9.3 Regression Suite

**Regression suite** = a fixed set of checks rerun regularly to catch old bugs coming
back; here it's a SQL query set over the audit data.

> 📄 **Example code:** [`examples/11-9-3-regression-suite.sql`](examples/11-9-3-regression-suite.sql)

Add both to the nightly observability query catalog (→ 13 §6). Approval-rate drift is a
first-class metric: a rising slope is the signal that fatigue has set in and evidence is
being rubber-stamped — *before* the incident that rubber-stamping eventually causes.

> **One-line summary:** Nightly queries watch approval-rate drift — rising approvals with falling wait time is the early alarm before an incident.

---

## 10. Real-World Case Studies

Signpost: this section shows how five real tools and research findings validate (or warn about) the rules above.

### 10.1 Claude Code — Permission Modes & Confirmation

Claude Code model permission modes (acceptEdits / bypassPermissions / plan mode / sandbox)
map almost exactly onto the tier taxonomy: file edits and shell commands are permissioned
by a consent stream (consent stream = the running feed of "may I do this?" prompts), and
its `/permissions` is the "escalate to read manually, with
reason" path. Three lessons:

1. **Granularity by action class, not by trust level.** A user trusts *a command* (a
   tool call stripped of the model's reasoning), not "the agent" as a persona. This is
   why tiering edits (`write`) separately from deploys (`elevated`) reads correctly.
2. **The model learns the consent boundary.** Agents that observe gates adjust their
   plans — they stop *proposing* force-pushes when the harness reliably shows them the
   red line. The deterrent effect is real (§ "Core Philosophy").
3. **Manual opt-out exists and is audited.** "Always allow" / `--dangerously-skip-permissions`
   is the documented, flag-protected escape hatch (escape hatch = a deliberate,
   documented way to bypass the safety); the *default* remains gated. A harness
   without such an escape hatch fails in crisis, but the escape must never be the default.

> **One-line summary:** Claude Code shows tiering by action class works, models learn where the red line is, and any bypass flag must exist but never be the default.

### 10.2 Aider — Read/Write Modes as a Deny-By-Default Canon

Aider (a pair-programming CLI tool) signature is the explicit read/write prompt mode: a user runs it *without*
`--no-verify-edits` and explicitly opts into full-write (`--yes-always`) when they
choose to. That's two design decisions every gate loop should copy:

1. **Default is gated, and gating is visible.** Being able to *see* that the model will
   edit files is a consent to a *class* of action, not a per-call click-storm.
2. **It pairs with --auto-test and git history.** Every edit is a reversible, diffable,
   git-tracked event — so the *middle* tier can be auto-approved while the *irreversible*
   tier still gates. The lesson: the write tier should cost almost nothing, because the
   real safety net is reversibility (git + tests), and the real gate is reserved for
   things git/tests can't undo.
   (Reversibility = you can undo it cheaply; git keeps the history so any edit can be reverted.)

> **One-line summary:** Aider proves the default should be gated and visible, and that cheap reversible work needs almost no gate — save gates for what git can't undo.

### 10.3 OpenHands — Confirmation Modes

OpenHands (formerly OpenDevin) exposes a fine-grained confirmation strategy for MCP and
code actions — "confirm on every action" vs "confirm on major changes" vs "never" —
mapping to `write` and `elevated` gates. The research-y punchline it shows:
per-action confirmation ("confirm every change") is the *worst* ergonomics because it
trains rubber-stamping; the harness should instead model confirmation at plan-segment
granularity with batching (→ 7.1), not per tool call. (Ergonomics = how comfortable
and efficient the interaction feels.)

> **One-line summary:** OpenHands is the cautionary tale: confirm-every-action trains humans to click without reading — confirm per plan segment instead.

### 10.4 Devin — Asynchronous Oversight

Signpost: this case is about agents that run unattended, where the gate must wait for a human who is not watching.

Asynchronous agents (long-run, unattended) force the *gate to travel.* Devin surfaces a
"what am I doing right now / ask me for approval" panel that the human polls rather than
being interrupted — the gate is a *checkpoint you can pick up*, not a ping you must be
awake for. Its failure mode is familiar: the longer the run, the more the human stops
reading before approving. The design answer embedded in this module is timeout-deny
(→ 4.2) plus fatigue metrics (→ 9.3): asynchronous oversight is only safe when an
unanswered gate *fails closed and pages*, rather than silently waiting forever.

> **One-line summary:** For unattended agents the gate becomes a pick-up-able panel — and it is only safe if an unanswered gate times out to deny and pages someone.

### 10.5 Human-AI Delegation Research — Automation Bias

Signpost: this section grounds every rule above in psychology research on why humans over-trust machines.

Psych research on automation bias (automation complacency, e.g. Parasuraman & Manzey,
2010) is the empirical basis for every rule here: humans over-trust automated
suggestions, under-monitor, and — critically — *false alarms erode vigilance*.
(Automation bias = the tendency to accept what the machine says without checking;
false alarm = a warning that turns out to be nothing; erode vigilance = wear down
attention.)

The harness-level conclusions:

- If gates fire on benign things, humans stop checking the real ones (the cry-wolf
  curve, §14).
- Evidence beats narration: a human with a dry-run hash and a diff is measurably more
  discriminating than one with a "trust me, I checked" summary.
- Two-person rule exists because *one* human in a 3 AM post-incident state is exactly
  the automation-bias setup: tired, trusting, and approving.

> **One-line summary:** Humans over-trust automation and false alarms wear them down — so gates must fire only on real risks and always show hard evidence.

---

## 11. TypeScript Interfaces for Approval

The full type surface (all the interfaces and type definitions in one place) for the
Gatekeeper, payloads, and verdicts lives in the example file:

> 📄 **Example code:** [`examples/12-11-typescript-interfaces-for-approval.ts`](examples/12-11-typescript-interfaces-for-approval.ts)

> **One-line summary:** All approval types are collected in one example file so implementations stay consistent.

---

## 12. Design Principles for Approval

Signpost: this section packages the module into reusable design rules — first via SOLID, then six principles of its own.

### 12.1 SOLID for Approval Systems

**SOLID** = five classic software design principles; here is what each means for gate
code. How to read it: column 1 is the principle, column 2 is how it applies here.

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `RiskTable` tags tiers; `Gatekeeper` persists + settles; `Notifier` channels; audit is a *trajectory event*, not a gate concern |
| **O**pen/closed | New action classes = new `RiskTableEntry`, no Gatekeeper change |
| **L**iskov substitution | `TwoPersonGatekeeper` and `Gatekeeper` are interchangeable to the engine via the `Gatekeeper` interface |
| **I**nterface segregation | Debug UI needs `verdict()`; compliance needs `auditEvent`; the engine needs `request()/onVerdict()`. Don't couple them. |
| **D**ependency inversion | Gatekeeper depends on `TrajectoryStore` + risk table, not on the model or the engine loop |

> **One-line summary:** Each job — tagging, gating, notifying, auditing — lives in its own component, so adding action classes never means rewriting the Gatekeeper.

### 12.2 Six Design Principles

Signpost: these six sentences are the checklist-version of the whole module.

1. **Tag at plan time, enforce at run time.** Tiers are a plan-time registry decision
   (→ 04 §14.3); the engine is a dumb enforcer. The model's view of its own tier is
   advisory at best.
2. **Evidence over narration.** Diff, blast radius, dry-run, rollback — each hashable,
   each mandatory. An approve without evidence is a policy violation by construction.
3. **Fail closed & loud.** Timeout = deny. Expired gate with no page = a bug. The price
   of safety is being woken up; that's the whole deal.
4. **Deny teaches; approve proves.** Deny reasons feed the planner; approvals create the
   auditable trail. Neither should be possible without the other's record.
5. **Human attention is the budget.** Design gates like scarce resources: batch, tier,
   default-guidance, and measure approval rate/wait so a gate that became theater is
   caught by metrics (→ 9.3) before it costs an incident.
6. **A gate must survive restarts.** Persisted, reloadable, re-armed timers. An
   in-memory gate is a security control with amnesia.

> **One-line summary:** Tag early, demand evidence, fail closed and loud, learn from denies, budget human attention, and persist every gate.

---

## 13. Best Practices

Signpost: this section is the quick do/don't list distilled from everything above.

### 13.1 DO ✅

- Tag tiers at plan time from a risk registry; let the engine enforce, never the model.
- Require diff + blast radius + dry-run + rollback in every payload; gate refuses to open without them.
- Fail closed: timeout → deny, with distinct `blocked(approval-timeout)` state.
- Deny → replan excluding the branch; recorded reason feeds the planner (→ 04 §14.2).
- Keep the two-person rule for `prod-auth`, enforced inside `settle`, not in the UI. (Settle = the code step that records a verdict.)
- Persist gates, reload them across restarts, re-arm expiry timers.
- Write every request/verdict as a trajectory event with `diffHash`/`dryRunHash` (→ 13).
- Batch `write`-tier reviews to keep human attention on the decisions that need it (§7.1).
- Measure approval rate + median wait per tier and treat drift as an incident signal.
- Test the restart path: open gate, kill process, restart, verdict still enforced.

> **One-line summary:** Tag early, demand full evidence, fail closed, replan on deny, persist gates, log everything, batch small reviews, and test restarts.

### 13.2 DON'T ❌

- ❌ Don't let the model decide if it "needs approval" — that's self-selected speed bumps.
- ❌ Don't approve with no diff ("trust me" buttons). Evidence is the point.
- ❌ Don't timeout-approve — timeouts are always fail-closed.
- ❌ Don't retry the same payload after a deny. Replan, don't nag.
- ❌ Don't allow self-approval on `prod-auth`, silently or audited — both are violations of two-person.
- ❌ Don't keep gates in memory only; a restarted process forgetting an open gate is a hole.
- ❌ Don't confirm every `write` action; the fatigue curve will turn your safety into theater.
- ❌ Don't let Slack/vocal "ok" count as a verdict without a record.
- ❌ Don't truncate notifications — a truncated channel lowers decision quality silently.

> **One-line summary:** Never let the model grade its own risk, approve blind, timeout-approve, nag after deny, self-approve, keep gates in memory, or confirm everything.

---

## 14. Anti-Patterns & Solutions

Signpost: this table is the field guide to broken gate systems — each row names a failure, how to spot it, and the fix.

How to read it: column 1 is the anti-pattern (a named way this goes wrong), column 2 is
the symptom you'd observe, column 3 is the concrete fix. Rubber-stamping = approving
reflexively without reading.

| Anti-pattern | Symptom | Fix |
|--------------|---------|-----|
| **Rubber-stamping** | approval rate 98% + median wait <10s | raise tier bar; batch writes; require typed confirm (→ 9.3) |
| **Fail-open timeout** | "well it was approved *eventually*" | never expire-to-approve; expired = deny + page |
| **Deny → retry loop** | same payload re-asked, human goes hostile | deny → replan, never resubmit identical action |
| **Self-approval** | proposer approves own prod-auth | enforce `by !== actorId` inside `settle`, audit the attempt |
| **In-memory gates** | process restart mints a fresh empty map | reload from trajectory, re-arm timers (§8.2) |
| **No evidence** | a gate opens with a summary and no dry-run hash | `validatePayload` throws; action blocked at gate (→ 3.2) |
| **Per-action confirmation** | a click per `write` action, humans zone out | batch + tier, confirm at plan-segment granularity (→ 7.1) |
| **Model-sized tiers** | agent "knew" it was a risk and asked nicely | tiers from risk registry, engine-enforced (→ 2.2) |
| **Gate without checkpoint** | resume re-runs the crossed boundary | checkpoint *before* gate, resume from cache (→ 5.2, 07 §13) |
| **Approval as Slack vibes** | "ok" voice-Channel consent, no record | notification ≠ verdict; verdict only via `settle()` (→ 7.2) |
| **Expired gate, no page** | quiet deadlock, run "looks stuck" | TTL crossing escalates; frozen run keeps a checkpoint |
| **Fatigue undetected** | rising approval slope, no metric | fatigue metrics in the nightly catalog (→ 9.3) |

> **One-line summary:** Every broken gate system shows up in one of these twelve rows — spot the symptom, apply the fix, and most are caught by metrics before incidents.

---

## 15. Production Checklist

Signpost: run through this before shipping a gate system; each item links back to the section that explains it.

- [ ] **Tiers tagged at plan time** from a risk registry; model can't self-select tier (→ 2.2)
- [ ] **Blast radius enumerated** by registry for every gated action (→ 2.3)
- [ ] **Payload complete:** diff + blast + dry-run + rollback, each hashable (→ 3.2)
- [ ] **Fail closed:** expiry → deny with distinct blocked state; no fail-open paths (→ 4.2)
- [ ] **Deny → replan** excluding the branch; no same-payload-retry (→ 4.3)
- [ ] **Escalation chain** defined per tier; delegation audited (→ 4.4)
- [ ] **Pause/resume tested** incl. process restart: open gate reloads + re-arms timers (→ 5.2, 8.2)
- [ ] **Idempotent resume**: same `runId`, idempotency cache skips done steps, gated action runs exactly once (→ 5.3)
- [ ] **Two-person rule** enforced inside `settle` for `prod-auth`; self-approval rejected + audited (→ 5.4)
- [ ] **Audit immutability**: request/verdict hash-linked events → trajectory + SIEM (→ 6.1)
- [ ] **Policy violations auto-flagged** (approve-without-dry-run, out-of-order, self-approval) (→ 6.2)
- [ ] **UX batching** — write-tier batched; human attention budget measured (→ 7.1)
- [ ] **Notification channels** carry full evidence, delivery traced (→ 7.2)
- [ ] **Test suite** — invariants on every recorded gate + restart contract tests + fatigue metrics (→ 9)
- [ ] **Review cadence** — quarterly approval-rate/wait review; drift = alarm (→ 9.3)

> **One-line summary:** Fifteen boxes, one per guarantee — a gate system that ticks them all is safe to run unattended.

---

## 16. Future Trends in Approval

Signpost: this section looks at where gate design is heading between 2026 and 2028.

### 16.1 Policy-as-Code Gate Registries (2026-2028)

**Policy-as-code** = keeping rules in a version-controlled file (like code) instead of
in someone's head or a wiki. The risk table migrates into a versioned, reviewable, policy-as-code artifact
(`approval-policy.yml`), diffed in PRs like any other infra. Tiers become auditable
declarations ("every `prod-auth` action in repo X must now page two people"), and a
policy diff that silently downgrades a tier is blocked by the same two-person rule that
protects the actions themselves. The gate system becomes both *enforcer* and *public
spec* — the "who can approve what" contract, versioned next to the code it protects.

> **One-line summary:** Risk tiers become a reviewable code file in the repo, so a quiet weakening of a gate is caught like any other bad code change.

### 16.2 Adaptive Trust with Continuous Evidence

Signpost: this explores gates whose strictness adjusts automatically based on track record.

Instead of a fixed `elevated` tier, the gate weight learns from trajectories: an action
class with a 6-month perfect dry-run + no-incident history gets a faster, quieter
pathway; a class with a recent incident gets an *automatic* stricter gate. Crucially,
downgrading trust must be automatic and metrics-driven (cheap, safe), while *restoring*
trust stays a human decision (expensive, slow). This is the same one-way trust ratchet
that makes security systems stable. (Ratchet = moves one way only — trust is lost fast,
regained slowly.)

> **One-line summary:** Trust drops automatically when evidence worsens but is only restored by a human decision — a one-way ratchet that keeps gates honest.

### 16.3 Approval as a Checkpoint Theorem

Signpost: this predicts gates merging into the general checkpoint/resume machinery.

Gates collapse into the checkpoint/resume story (→ 07 §13): *gate = a checkpoint with a
verdict attached.* Then everything the checkpoint ecosystem already gives you — replay,
idempotency, audit, fork — applies to gates for free. A "deploy gate" is just a
`checkpoint(pause_until=verdict)` node in the plan graph, rendered as a timeline panel
and replayed for post-incident review.

> **One-line summary:** The endgame: a gate is just a checkpoint that waits for a verdict, inheriting replay, audit, and resume for free.

### 16.4 Human-Scale Supervision at Agent Scale

Signpost: this covers the near future where one human oversees many agents at once.

As one human supervises many agents, gates must multiplex (multiplex = combine many
streams into one surface): a single review surface
showing *all* concurrent pending gates grouped by risk, batchable by decision, with
"approve identical class except prod-auth" flows — while never allowing one tired click
to authorize a `prod-auth` action. The cost of this future is vigilance economics: the
system must stop asking when the human is zoned out, which is exactly why the rubber-stamp
metric (→ 9.3) becomes the product dashboard of the next five years.

> **One-line summary:** One human, many agents: gates group into one review surface with batch approvals — except prod-auth, which can never be batch-approved.

---

## References

### Papers & Research

- **Automation Bias and Automation Complacency** — Parasuraman & Manzey (2010) · https://link.springer.com/article/10.1007/s12170-010-0080-4
- **Trust in Automation: Designing for Appropriate Reliance** — Lee & See (2004) · https://journals.sagepub.com/doi/10.1518/hfes.46.1.50.30392
- **Human-AI Delegation** — Mapping delegation ontologies for AI agents · https://arxiv.org/abs/2309.01564
- **Comprehensible AI systems: Automation tragedy** — on why evidence beats narration · https://arxiv.org/abs/2003.02334
- **Behavioral Data Science for Agent Oversight** *(design framing for fatigue metrics)* · https://arxiv.org/abs/2405.07355

### Frameworks & Tools

1. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code — permission modes, `/permissions`, consent stream
2. **Aider** — https://aider.chat/docs/ — read/write modes, `--yes-always`, git-backed reversibility
3. **OpenHands** — https://github.com/All-Hands-AI/OpenHands — confirmation strategies for code + MCP
4. **NATS / webhook based approval bots** — https://nats.io — notification + verdict transport
5. **OpenPolicyAgent (OPA)** — https://www.openpolicyagent.org — policy-as-code for tier registries (→ 16.1)
6. **PolicyEngine** *(server-side policy gateways)* — https://github.com/policyengine

### Production Systems

- **Spacelift** — https://spacelift.io — plan/workflow approvals with run-review (the "approval as review," not "approval as click")
- **Atlantis** — https://www.runatlantis.io/apply-requirements — `apply_requirements` = tier system for terraform
- **Claude Code** — https://claude.com/product/claude-code — permission consent stream
- **Devin** — https://devin.ai — asynchronous oversight panel
- **CircleCI / GitHub Environments** — https://docs.github.com/en/actions/managing-workflow-runs/reviewing-deployments — protected environment approvals

### Related Modules

- `04-plan-decompose-task/README.md` §14.3 — planning-side gates ("who can override"), deny→replan
- `06-decide-tools-mcp/README.md` §17.4 — tool-side consent UX
- `07-workflow/README.md` §13.4 — pause/resume engine + checkpoint (the gate's host)
- `12-sandbox-execution/README.md` — technical ceiling that gates complement
- `13-trajectory-observability/` — gate as event, audit + replay (§6 of this module consumes it)
- `14-compaction-context/README.md` — pending approvals are part of the pin set (→ 14 §3.2)
- `08-task/README.md` §11 — idempotency cache that makes resume safe

> **One-line summary:** Sources span automation-bias research, real tool docs (Claude Code, Aider, OpenHands, Devin, Atlantis), and the sibling modules this one plugs into.

---

*Document: Harness 15. Approval Gates — HARNESS ENGINEERING EDITION*
*Cross-cutting module · control plane for irreversible actions · human-in-the-loop*
*Updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Approval Fatigue & UX

> A deeper look at approval fatigue (raised in §7.1) — the #1 silent failure mode of
> human-in-the-loop systems: the gate isn't bypassed, it gets **rubber-stamped reflexively**.

### 1. What Is Approval Fatigue — And Why It's Dangerous

Signpost: this section defines the failure where the gate stays in place but stops being read.

Approval fatigue happens when gates fire too often: the user faces dozens of approval boxes
every day, and the brain optimizes by approving reflexively — which is exactly **automation
bias** (Parasuraman & Manzey, 2010; → §10.5). In that state:

- The gate still *technically* works — every action has an approval.
- The gate is *substantively* dead — the "Approve" button becomes a second Enter key.
- It's worse than having no gate: you **believe** there's human review, so you lower your
  guard at other layers; while in reality nobody is reading anything.

Human-delegation research shows false alarms erode vigilance:
the gate fires on something harmless, the human stops checking the real threats too
(the cry-wolf curve). The early-detection metric lives in §9.3: **approval rate rising +
decision time falling at the same time** = fatigue has set in.

> **One-line summary:** Approval fatigue keeps the gate formally alive but turns Approve into a reflex — and it's detectable by rising approval rates plus falling decision times.

### 2. Five Mitigations

Signpost: five concrete fixes for fatigue, in priority order.

How to read it: column 1 is the mitigation (the fix), column 2 says exactly how to do
it, column 3 says when it applies. S1/S2/S3 = severity levels, here shorthand for the
top and bottom of the tier ladder.

| Mitigation | How | When to use |
|-----------|-----|-------------|
| **Risk-based approval** | Only gate S1/S2 (prod-auth, elevated); S3 read-only auto-approves + logs. Put the gate on the expensive tail (§2.1), don't burn attention on the cheap tier | Always — the default of the tier taxonomy |
| **Batching** | Group low-risk ops in the same plan segment into **one** gate with a combined diff | Many `write` edits in one task (§7.1) |
| **Approval summary** | Payload always carries diff + consequences + rollback; humans approve *evidence*, not *narrative* | Every gate (evidence rule §3.2) |
| **Timeout-deny stays** | Fatigue is not a reason to loosen TTL or fail-open; expired is still deny (§4.2) | Always — no exceptions |
| **Audit + weekly review** | Watch approval rate / median wait / deny patterns per tier to **calibrate**: a tier being machine-stamped gets a raised threshold or loses its gate | Fixed cadence — not ad hoc |

Every mitigation shares one principle: *spend the least human attention per safe
decision* — kill useless gates so real gates stay alive.

> **One-line summary:** Gate only the risky tail, batch the rest, always show evidence, keep timeout-deny, and review the numbers weekly to kill useless gates.

### 3. Anti-Pattern: Gating by Tool Call, When You Should Gate by Business Operation

Signpost: this section names the single most common cause of fatigue: gating the wrong unit.

**Anti-pattern:** gate *every tool call* — reading a file needs approval, search needs
approval, grep needs approval. After two days, the user unconsciously click-throughs
everything, including `db.migrate` on prod. (Click-through = approving without reading,
just to move on.)

Principle: **gate by BUSINESS OPERATION, not by technique.** A business operation is
what the action *means* to the company ("deploy to prod"), not the low-level technique
used ("run this shell command"). Read-only technical actions are already protected by
other layers, as the table shows:

| Gate ❌ by technique | Gate ✅ by business operation |
|---------------------|------------------------------|
| `read_file`, `search`, `grep` | Deploy to prod, force-push a release branch |
| `list`, `view`, `stat` | Delete data, change IAM / rotate secrets |
| running local tests | Sending messages/emails outside the system |

Read-only technical actions have git + sandbox + audit as cover (reversibility — → §10.2
Aider); save real gates for what git cannot undo. OpenHands ("confirm every
change") is the main case study of this mistake — the worst ergonomics because it *trains*
rubber-stamping (§10.3).

> **One-line summary:** Gate the business meaning ("deploy to prod"), not the tool call ("run a command") — gating reads and searches trains humans to click through everything.

### 4. Architecture Links

Signpost: this final note places the module in the larger architecture map.

The approval gate sits at **Layer 7 (Execution & Safety)** — the technical ceiling that gates
complement, in the 9-layer architecture. See
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (Layer 7).

> **One-line summary:** Approval gates live in Layer 7 (Execution & Safety) of the 9-layer architecture — the human checkpoint layered over the technical limits.

