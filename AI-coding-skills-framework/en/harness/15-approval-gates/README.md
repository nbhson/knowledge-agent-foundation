# 🔐 XV. Approval Gates — Human-in-the-Loop for Irreversible Actions

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
> **Cross-cutting module.** Approval gates are the only place in the harness where a
> human participates in the *execution* loop, not just the setup. Every other module
> assumes the run can decide and act; this one installs the deliberate interruption —
> the cheapest incident insurance in the whole harness (→ 12 §1.2, → 06 §17.4).

---

### Opening Story

3:47 AM. A migration run has been going for six hours. The agent, confident and on
turn 214, has just detached a stalled `db.migrate` retry and decided it is "stuck in
incremental steps," so it constructs a recovery path: `ALTER TABLE users DROP COLUMN
mfa_secret` — because a downstream check complained the column is `NOT NULL` without a
default, and the agent's model of "remove the blocker" won.

The column held 2.1M MFA enrollments. There is no backup of it. The action is
irreversible, destructive, and *wrong*.

What separates this from a headline incident is a single decision the harness made
earlier: **tag `prod-auth` at plan time, freeze the run, and show a human "before"
evidence, not the model's reasoning.** The gate fires. The human squints at a 12-line
diff at 3:47 AM, says "no", types a reason, and twenty minutes later the agent replans
around the change — *without ever having touched the column*.

The gate did not make the agent smarter. It made the harness *safe to be wrong* — which
is the only property that matters for autonomous systems. Every over-confident action
that almost happened and the human caught is invisible in metrics, costs nothing, and is
the entire point.

### Why Are Approval Gates Non-Optional?

> *"An agent that can confidently ask for production credentials at 3 AM and receive
> them is not an agent. It is a muzzle-loading cannon."*

#### The Math of Confident Failure

LLM agents are wrong at non-trivial rates and *never know it* — calibration studies
consistently show overconfidence that grows with context size and plan depth (→ 10.5).
Put that against the blast radius of the actions agents are asked to take:

| Action | Error rate of the *decision* | If wrong, blast radius |
|--------|------------------------------|------------------------|
| `edit_file` in `src/` | high (hallucinated APIs, wrong file) | locally reversible via git |
| `db.migrate` on prod | low but *catastrophic when wrong* | irreversible schema, hours of rollback |
| `user.delete` / IAM change | rare | permanent, identity + compliance |
| `git push --force` | low-frequency, high-novelty | shared history rewritten, multi-repo blast |

The failure modes that kill companies are not the frequent ones — they are the rare
ones whose cost dominates the whole distribution. A gate is a *guard at the expensive
tail*, and it costs essentially nothing on the frequent cheap tail (`read` tier is
auto-approved).

The second, subtler force: **a human-in-the-loop gate changes agent behavior, not just
outcomes.** Models instructed that an irreversible action requires a visible, auditable,
second-party approval are measurably more conservative in their reasoning — they stop
"improvising" destructive recovery paths because they know the plan will be *shown*,
not just executed. The gate is a deterrent before it is a firewall.

#### Core Philosophy

Approval is **not** "ask a human about everything" and **not** "never ask." It is:
*tag risk at plan time, contain the blast radius with mandatory evidence, and let the
failure be loud and auditable rather than silent and expensive.* The gate should be the
point where the system is *designed to fail*, so that when the agent is wrong — and it
will be — the wrongness is cheap and visible.

## Overview

> **📌 Core Concept**
>
> - **Concept:** An approval gate is a pause point before an irreversible or high-blast-radius action: execution freezes, a human sees *what / why / blast radius / rollback*, and the run resumes only on approve (or replans on deny/timeout).
> - **Analogy:** Like a bank vault requiring two keys — the agent holds one (the plan), the human holds the other (the judgment). Either key alone opens nothing.
> - **Why it matters:** Agents are wrong with confidence. Without gates, one hallucinated `prod.db.drop()` or `git push --force` at 3 AM becomes an incident. Gates are the cheapest incident insurance in the whole harness.

**Approval Gates** are the control plane for actions whose failure cost exceeds the
agent's decision confidence. They are the direct complement to sandboxing: the sandbox
(→ 12) contains *what an agent can do*, the gate decides *what a trustworthy human must
see before it happens*. One is a technical ceiling; the other is a social contract.

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

**The gate has a lifecycle, not a boolean:** one `request()`, three settled outcomes
(`approved` / `denied` / `expired`), one audit trail, zero silent branches. Any
implementation that cannot answer "who, what, when, and why *for every irreversibility*"
is not an approval system — it is a button with extra steps.

## Contents

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

---

## 1. Definitions & Vocabulary

### 1.1 Core Terms

| Term | Definition | Fails when… |
|------|-----------|-------------|
| **Approval gate** | Workflow node in state `WAITING_APPROVAL`; persists, notifies, resumes on verdict | only in-memory → lost on restart |
| **Blast radius** | Enumerated set of affected resources if the action runs (files, DBs, envs, users) | vague ("prod stuff") → human cannot judge |
| **Dry-run** | Side-effect-free preview of the action (plan diff, `terraform plan`, `--dry-run`) — mandatory in gate payload | skipped → approval is blind |
| **Timeout-deny** | No verdict within TTL → treated as **deny** (fail closed), never as approve | fail-open → "I was going to approve it" |
| **Two-person rule** | Proposer ≠ approver; a second independent human decides | self-approval → reverts to no gate |
| **Deny → replan** | A deny records `reason` and triggers replanning that excludes the denied branch (→ 04 §14.2) | deny → retry same → loops forever |
| **Approval event** | Every request + verdict written to trajectory as `approval_request` / `approval_verdict` (→ 13) | not traced → post-incident review is impossible |

### 1.2 The Two Families: Hard Blocks vs Advisory Signals

There are two *different* mechanisms that look similar and get conflated, to their
detriment:

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

---

## 2. Risk Tiers — What Needs a Gate?

### 2.1 Tier Taxonomy

| Tier | Examples | Gate |
|------|----------|------|
| `read` (low) | `read_file`, `grep`, `list`, `view` | Auto-approve, log only |
| `write` (medium) | `edit_file` in `src/`, `run_tests`, local commits | Diff preview + one-click approve, 5-min expiry |
| `elevated` (high) | `db.migrate`, `deploy`, `user.delete`, `external.send`, `push --force`, `rm -rf` | Typed confirm + reason + dry-run + rollback cmd, 30-min expiry |
| `prod-auth` (critical) | IAM change, secret rotation, prod data delete, payment/legal action | Two-person rule (proposer ≠ approver) + incident channel notice, 4h + page |

**The tier is a property of the *action class*, not of the specific invocation.** Push
to a feature branch is `write`; force-push to `main` is `elevated`; force-push to a
shared `release/*` branch is `prod-auth`. The mapping lives in the permission/risk
table (`permission.ts`), updated in review — never inferred per-message by the model.

### 2.2 Tagging at Plan Time

Tiers are assigned **at plan time** (→ 04 §14.3), not at execution time:

1. The planner emits each task/tool with an explicit `tier` field.
2. The engine validates the tier against a global risk table before the step even
   builds its payload.
3. The model cannot self-downgrade — a request to "just run this as `write`" is not a
   policy path; changing the tag is a policy change that must come from the risktable
   owner.

> **Rule:** *the agent proposes, the engine enforces, the human overrides only via a
> recorded reason.* Tag-at-plan-time is what makes that three-way split possible —
> without it, the model picks its own speed bumps and picks the ones it can ignore.

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

### 2.3 Blast Radius Enumeration

A gate payload is only as good as its blast-radius enumeration. The system must
enumerate, from the sandbox/policy registry (→ 12 §6), the exact set of resources the
action touches:

```
ACTION:   db.migrate 20260719_add_mfa_cols (tier: elevated)
BLAST:    prod-db.host=postgres-5a2f (primary, no replica for this schema)
          database=users  size=2.1M rows
          table migration lock ~4s (downtime window: ok)
          0 down migrations — NOT reversible by migration engine
          connected microservices: auth-svc (read), consent-svc (write)
```

Enumeration failure modes:

| Failure | Example | Fix |
|---------|---------|-----|
| Too coarse | "edits prod database" | exact db, host, size, lock estimate |
| Missing blast | forgets connected services | registry-driven enumeration, not model-written |
| Confusing with cost | "costs $0.40" listed but no lock time | cost is a *row* in the payload, not the blast radius |
| Rollback unproven | "rollback: revert migration" with no test | `rollback` field must carry a tested command/hash |

---

## 3. Gate Payload — What the Human Sees

### 3.1 The Payload Fields

```
ACTION:   db.migrate (tier: elevated)
TASK:     auth-refactor / step 3 (trajectory: traj_x, event: evt_41)
DIFF:     +ALTER TABLE users ADD COLUMN mfa_secret TEXT (12 lines…)
BLAST:    prod-db.users (2.1M rows), lock ~4s, 0 down migrations
DRY-RUN:  ✓ shadow-migrate passed (3.8s), rollback tested
ROLLBACK: db.migrate down v48 (cmd attached, tested 2h ago)
COST:     ~$0.40, ~90s                       [Approve] [Deny + reason]
```

Every field must be **derived from evidence**, not narrated:

| Field | Source | Absent → |
|-------|--------|----------|
| `ACTION` + `tier` | the step's tier tag (→ 2.2) | gate cannot render |
| `TASK` + trajectory link | plan graph node + span IDs (→ 04, 13) | post-incident review cannot replay |
| `DIFF` | the actual command/materialized diff | approve is blind |
| `BLAST` | registry enumeration (→ 2.3) | human under-judges |
| `DRY-RUN` | the dry-run *output*, hash-linked | approve is an act of faith |
| `ROLLBACK` | tested rollback command + when it was tested | approve commits to irreversibility |
| `COST` | estimated tokens/money/time | human cannot compare options |

### 3.2 The Mandatory-Evidence Rule

> **No dry-run → no gate → action blocked.** The gate refuses to open if any
> mandatory-evidence field is empty. This is *not* a UX nicety — it is the invariant
> that makes approval different from consent.

Implementation-wise it is a validation function that runs *before* `request()` is
called:

```typescript
export function validatePayload(r: GateRequest): string[] {
  const missing: string[] = [];
  if (!r.diff)                  missing.push("diff");
  if (r.blastRadius.length === 0) missing.push("blastRadius");
  if (!r.dryRun)                missing.push("dryRun");      // evidence, not a summary
  if (!r.rollback)              missing.push("rollback");
  if (!r.expiresAt || r.expiresAt <= Date.now()) missing.push("expiresAt");
  return missing;
}
```

A `request()` with a non-empty `missing` array throws; the run **cannot** proceed until
the evidence exists. Teams that allow "approve anyway" on an invalid payload consistently
discover that the approve button becomes a *posting medium for un-reviewed actions*.

The payload itself is a trajectory event (→ 13), so post-incident review replays
exactly what the human saw — including the dry-run output that justified (or failed to
justify) the verdict.

---

## 4. Timeout, Deny & Escalation Semantics

### 4.1 The Four Outcomes

| Outcome | Meaning | Next state |
|---------|---------|-----------|
| `approved` | human verified evidence, run resumes | continues on same `runId`, idempotency cache skips done steps |
| `denied` | human rejects with a reason | task marked `blocked(denied)`, replan excludes branch |
| `expired` | no verdict within TTL | treated exactly as deny (fail closed), unless escalated |
| `escalated` | TTL crossed a threshold and on-call was paged | new TTL, delegation chain recorded |

The state machine is small and closed; any implementation that "creates" a new outcome
at runtime (e.g. *"user said ok on Slack"*) is a policy gap, not a feature.

### 4.2 Timeout-Deny (Fail Closed)

`write` 5 min · `elevated` 30 min · `prod-auth` 4h + page.

- Expiry marks the task `blocked(approval-timeout)` — a distinct state from `denied`,
  because the *next* action differs (see 4.3).
- **Fail closed, never fail open.** Expiry must never be interpreted as approval. The
  one exception requiring explicit policy sign-off: a *store-closed, unattended* deploy
  window where the approved-timeout is documented as "expired = rolled back and paged".
- The expiry timer runs in the *engine*, not in the UI session. Closing the review
  laptop cannot extend a gate's life.

```typescript
// fail-closed consequence of expiry
export function onExpire(key: string, g: Gate): void {
  g.verdict = "expired";
  traj.append({ kind: "approval_verdict", payload: { key, verdict: "expired",
    reason: "ttl_elapsed", at: Date.now() } });
  plan.markBlocked(g.taskId, "approval-timeout");
  replanner.excludeBranch(g.taskId);   // → 04 §14.2
}
```

### 4.3 Deny → Replan, Not Retry

- Record `reason` — it is the *most valuable* audit artifact in the whole gate: it
  tells future planners what the human rejects, and repeated denials on the same reason
  are a product signal (the agent keeps proposing things the team doesn't want).
- Trigger replanning that excludes the denied branch (→ 04 §14.2). Never re-ask the
  same payload twice. If the *same* plan can satisfy the denial another way, the planner
  emits a new plan; the new plan generates a *new* gate only if the new action is again
  high-tier.
- Repeatedly re-asking the identical action after a deny is the #1 way approval systems
  become contemptible, and the #1 way they get bypassed by users who approve "just to
  stop the noise."

### 4.4 Escalation & Delegation

- **Page on-call** if `elevated` stays ungated >15 min in prod hours (or >T for non-prod,
  configurable). The run stays frozen at the checkpoint (→ 07 §13); the checkpoint is the
  safety property that makes escalation free.
- **Approval delegation** allowed (on-call → secondary) — but *delegation is separate
  from the two-person rule*: delegating the notification does not turn one approver into
  two. For `prod-auth`, delegation keeps the two-person requirement (proposer + one
  independent approver); it can change *who* that approver is, never *how many*.
- Every hop of the escalation chain (`paged_oncall` → `delegated_to:x` → `approved`)
  is an audit entry. The chain is what makes "who actually decided?" answerable under
  scrutiny.

---

## 5. Engine Integration (Pause / Resume)

### 5.1 The Gatekeeper API

```typescript
type Verdict = "approved" | "denied" | "expired";
interface GateRequest {
  key: string; tier: "write" | "elevated" | "prod-auth";
  summary: string; diff: string; blastRadius: string[];
  dryRun: string; rollback: string; expiresAt: number;
}
export class Gatekeeper {
  private gates = new Map<string, { req: GateRequest; verdict?: Verdict }>();
  request(r: GateRequest): void {
    ensureValid(r);                          // mandatory-evidence rule (§3.2)
    this.gates.set(r.key, { req: r });       // engine throws PAUSED:<key>
    setTimeout(() => this.settle(r.key, "expired"), r.expiresAt - Date.now());
  }
  settle(key: string, v: Verdict, by = "human"): void {
    const g = this.gates.get(key); if (!g || g.verdict) return;  // one verdict wins
    g.verdict = v; // audit: { key, v, by, at: Date.now() } → trajectory (→ 13)
  }
  verdict(key: string): Verdict | undefined { return this.gates.get(key)?.verdict; }
}
// Engine loop: before running a gated step → gatekeeper.request(...) → checkpoint
// → throw PAUSED → on verdict approved: resume; denied/expired: mark blocked → replan.
```

### 5.2 The PAUSED Protocol

The engine does **not** "wait." It throws a typed `PAUSED:<key>` after checkpointing:

- **Checkpoint first, then throw.** All completed steps are in the idempotency cache
  and trajectory store (→ 07 §13, → 13). Pausing *without* a checkpoint means resume
  cannot distinguish "never ran" from "ran and half-finished."
- `PAUSED:<key>` propagates to the driver/CLI/UI as a first-class state, not an error.
  The human's "approve" is a *verdict delivery*, not a restart.
- **The run object persists.** A gate survives process death: on restart, the
  Gatekeeper reloads open gates from the trajectory store, re-arms their timers, and
  any run still pinned at a `WAITING_APPROVAL` checkpoint resumes or expires correctly.

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

### 5.3 Resume & Idempotency

- Resume re-invokes the run with the **same `runId`**; completed steps hit the
  idempotency cache and skip (→ 07 §13, 08 §11). Nothing re-executes, nothing
  re-asks.
- The gated action itself is re-run **only after** approval, exactly once — the
  checkpoint sits *before* the action, so resume re-runs the action, not a crossed
  boundary.
- Idempotency of the *approval*: settling the same key twice is a no-op (`if (!g ||
  g.verdict) return`). A double-clicked "approve" cannot double-run a migration.

### 5.4 Two-Person Rule Enforcement

`prod-auth` gates require a second pair of human eyes whose identity differs from the
proposer:

```typescript
// engine refuses to materialize the action until a DIFFERENT human approves
export function tryApprove(key: string, approverId: string, reason?: string): boolean {
  const g = gates.get(key); if (!g || g.verdict) return false;
  if (g.req.actorId === approverId) {
    traj.warn({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
    return false;                                  // proposer ≠ approver, hard
  }
  gates.get(key)!.actorApproval = approverId;      // second human confirmed
}
```

The proposer is recorded at `request()` time (the step that spawned the gate). The rule
is enforced *inside* `tryApprove`, so there is no model path around it. Self-approval
attempts are not silent — they are audited as a policy event, which is itself a
weird-behavior signal worth watching.

---

## 6. Audit Log

### 6.1 The Record

Every gate writes an immutable record: `{key, tier, actor(proposer), approver, verdict,
reason, diffHash, dryRunHash, at}` → trajectory store (→ 13) + SIEM.

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
*different* action than the one shown" impossible to launder. If the payload rendered at
request time hashes to X but the executed action hashes to Y ≠ X, that is a hard
incident, flagged automatically.

### 6.2 Policy Violation Detection

Automated checks over the audit stream:

- Gate approved **without** a `dryRunHash` → policy violation, flag + page (unless the
  action class is in an explicit "no-dry-run" allowlist, which itself must be approved).
- `approver === actor` on a `prod-auth` gate → violation (self-approval).
- Verdict recorded **after** the action already touched resources → violation
  (out-of-order approval).
- Timeout-deny that was followed by a *new identical request* within X minutes →
  violation of deny→no-retry (→ 4.3).

Quarterly review cadence: approval rate per tier, median wait, override incidents,
delegation-chain depth. The point of the review is not policing — it's *design*
intelligence: a tier with a 98% approval rate and 30-second median wait is not being
read, it's being rubber-stamped, and the gate has become theater (→ 14).

---

## 7. Human-in-the-Loop UX

### 7.1 Batching & Decision Fatigue

Humans are the scarce, expensive resource; the design target is *minimum tokens of
human attention per safe decision*.

- **One notification per decision**, not one per action — batch `write`-tier edits in
  a single reviewable diff when they belong to the same step.
- **Context, not trivia.** Show the *task it belongs to*, the *plan phase*, the
  *previous attempt* — so a "deploy" approval during a rehearsed run reads differently
  from one mid-refactor.
- **Default-action guidance**: the payload should make the *right* decision the easy
  one. If the correct answer is usually "deny", the approve path costs more friction, not
  less (typed confirm + reason on `prod-auth`).
- **Fatigue is the #1 silent failure** — measured as a rising approval rate with
  falling median decision time. When that happens, the gate is no longer protecting; it
  is cosigning. Fix by *raising* the tier bar, not by removing gates.

### 7.2 Notification Channels

| Tier | Channel | Tone |
|------|---------|------|
| `write` | in-app/PR comment; quiet, batched | informative |
| `elevated` | push + email, actionable | needs attention, 30-min budget |
| `prod-auth` | incident channel + page; two-person | escalation, 4h TTL |

Every notification carries the *same* payload the UI would show (diff, blast, dry-run
hash) — no channel truncates the evidence, because a truncated channel silently lowers
the quality of the decision. Notification delivery is itself traced (`notification_sent`
event → 13) so "the human never saw it" is a checkable claim, not an excuse.

---

## 8. TypeScript Implementation

### 8.1 Types

```typescript
export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;                 // plan graph node (→ 04)
  runId: string;                  // for resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;                // proposer (two-person rule)
  summary: string;
  diff: string;
  blastRadius: string[];
  dryRun: string;
  rollback: string;
  diffHash: string;
  dryRunHash: string;
  createdAt: number;
  expiresAt: number;
  state: GateState;
}

export interface RiskTableEntry {
  action: string;                 // registry key, e.g. "db.migrate"
  defaultTier: Tier;
  paths?: RegExp[];               // e.g. force-push on "release/*"
  noDryRunAllowlist?: boolean;    // must itself be policy-approved
}
```

### 8.2 Persisted Gatekeeper

<details>
<summary>TypeScript Code — persisted Gatekeeper with reload + audit (Click to expand/collapse)</summary>

```typescript
import { randomBytes, createHash } from "node:crypto";

export class Gatekeeper {
  private gates = new Map<string, Gate>();
  constructor(
    private store: TrajectoryStore,          // audit/durability (→ 13)
    private risk: RiskTableEntry[],          // tier registry
  ) {
    this.reloadOpen();                       // survive restart
  }

  private key(): string { return `gate_${randomBytes(4).toString("hex")}`; }

  /** Validates tier + evidence, persists, arms the fail-closed timer. */
  request(input: Omit<Gate, "key" | "state" | "createdAt" | "diffHash">
      | { diff: string; dryRun: string }): Gate {
    const missing = validatePayload(input);              // §3.2 mandatory evidence
    if (missing.length) throw new Error(`gate missing evidence: ${missing.join(",")}`);
    const gate: Gate = {
      ...input, key: this.key(), createdAt: Date.now(), state: { status: "waiting" },
      diffHash: createHash("sha256").update(input.diff).digest("hex"),
      dryRunHash: createHash("sha256").update(input.dryRun).digest("hex"),
    };
    this.gates.set(gate.key, gate);
    this.store.append({ kind: "approval_request", payload: gate });
    this.armTimer(gate);
    return gate;
  }

  private armTimer(g: Gate): void {
    const ms = g.expiresAt - Date.now();
    setTimeout(() => this.settle(g.key, "expired", "timer"), Math.max(0, ms));
  }

  /** One verdict wins. Self-approval on prod-auth is rejected and audited. */
  settle(key: string, v: Verdict, by: string, reason?: string): boolean {
    const g = this.gates.get(key);
    if (!g || g.state.status === "settled") return false;
    if (v === "approved" && g.tier === "prod-auth" && by === g.actorId) {
      this.store.append({ kind: "approval_policy", payload: { key, detail: "self_approval_rejected" } });
      return false;
    }
    g.state = { status: "settled", verdict: v, by, at: Date.now() };
    this.store.append({ kind: "approval_verdict",
      payload: { key, verdict: v, by, reason, diffHash: g.diffHash, dryRunHash: g.dryRunHash } });
    return true;
  }

  verdict(key: string): Verdict | undefined {
    return this.gates.get(key)?.state.status === "settled"
      ? (this.gates.get(key)!.state as { verdict: Verdict }).verdict : undefined;
  }

  private reloadOpen(): void {
    for (const ev of this.store.query({ kind: "approval_request" })) {
      if (!this.verdict(ev.payload.key)) {                    // open gate → re-arm
        const g = ev.payload as Gate;
        this.gates.set(g.key, g);
        this.armTimer(g);
      }
    }
  }
}
```

</details>

### 8.3 Engine Loop Integration

```typescript
export async function runStep(step: Step, ctx: Ctx): Promise<void> {
  const tier = resolveTier(step, ctx.risk);                  // §2.1 rule, not model
  await checkpoint(ctx, step);                               // (→ 07 §13) BEFORE throw

  if (tier === "read") { await step.run(ctx); return; }      // auto-approve, log

  const gate = ctx.gates.request({ taskId: step.id, runId: ctx.runId, tier,
    actorId: ctx.actorId, summary: step.summary, diff: step.renderDiff(),
    blastRadius: step.blastRadius(ctx), dryRun: await step.dryRun(ctx),
    rollback: step.rollback(ctx) });
  await ctx.notify(gate);                                    // §7.2

  throw new Paused(`PAUSED:${gate.key}`);                    // freezes, audit sees it

  // resumed later by driver after human verdict:
  //   verdict=approved → this function returns, step.run() executes once
  //   verdict=denied/expired → markBlocked → replanner.excludeBranch(step.id)
}
```

Note what the engine loop *doesn't* contain: no branch where the model "asks nicely" and
continues. The only way past the throw is a persisted verdict from the Gatekeeper —
which is the whole integrity story.

### 8.4 Two-Person Gatekeeper

```typescript
// wraps Gatekeeper for prod-auth: two independent human approvals, persisted
export class TwoPersonGatekeeper {
  constructor(private inner: Gatekeeper) {}
  request(g: Omit<Gate, "key" | "state" | "createdAt" | "diffHash"
        | "dryRunHash">): Gate {
    const gate = this.inner.request(g);
    return gate;   // approval requires ONE additional actor: settle() enforces ≠ actor
  }
  // settle() in the base Gatekeeper already rejects actorId === approver for prod-auth.
  // All that changes is UI + TTL (4h) + page. The invariant lives in one place.
}
```

---

## 9. Testing Approval Gates

### 9.1 Invariant Tests

```typescript
export function assertGateInvariants(...gates: Gate[]): void {
  for (const g of gates) {
    // 1 — settled exactly once
    if (g.state.status === "settled" && g.state.at < g.createdAt) throw new Error("verdict before creation");
    // 2 — evidence mandatory
    if (g.state.status === "settled" && g.state.verdict === "approved" && !g.dryRunHash) throw new Error("approved without dry-run hash");
    // 3 — fail closed
    if (g.expiresAt < Date.now() && g.state.status === "waiting") throw new Error("expired gate still waiting (timer lost)");
    // 4 — two-person rule
    if (g.tier === "prod-auth" && g.state.status === "settled" && g.state.verdict === "approved"
        && g.state.by === g.actorId) throw new Error("self-approval on prod-auth");
    // 5 — out-of-order: verdict must not pre-date the evidence being reviewed
    if (typeof g.diffHash === "string" && g.diffHash === "" ) throw new Error("empty diff hash");
  }
}
```

Run these across **every recorded gate in production** (like §9.1 of → 13): the invariant
suite is cheap and catches regressions the unit tests never will — e.g. a timer that
doesn't survive a restart.

### 9.2 Contract Tests

```typescript
describe("Gatekeeper contract", () => {
  it("validates evidence before opening", () => {
    expect(() => gates.request({ ...noDryRun })).toThrow(/missing evidence/);
  });

  it("settles exactly once", async () => {
    const g = gates.request(validGate);
    gates.settle(g.key, "approved", "alice");
    gates.settle(g.key, "denied", "alice");                  // second call is a no-op
    expect(gates.verdict(g.key)).toBe("approved");
  });

  it("survives restart and re-arms expiry", async () => {
    const g = gates.request(validGate);
    const fresh = new Gatekeeper(store, risk);               // reloads open gates
    expect(fresh.verdict(g.key)).toBeUndefined();
    await vi.advanceTimersByTimeAsync(g.expiresAt - Date.now() + 1);
    expect(fresh.verdict(g.key)).toBe("expired");            // fail closed
  });

  it("rejects self-approval on prod-auth", () => {
    const g = gates.request(validGateProdAuth);
    expect(gates.settle(g.key, "approved", g.actorId)).toBe(false);
  });

  it("recovers a run after approve and replans after deny", async () => {
    const approved = gates.request(gate1); gates.settle(approved.key, "approved", "bob");
    const denied   = gates.request(gate2); gates.settle(denied.key, "denied", "bob", "not today");
    expect(resume(runId, approved.key)).toExecExactlyOnce(stepAtKey(approved.key));
    expect(plan.exclude).toHaveBeenCalledWith(denied.taskId);   // deny → replan, not retry
  });
});
```

The restart test is the one teams skip, and it is the one that proves a gate is a
*durable security control* rather than a memory object.

### 9.3 Regression Suite

```sql
-- approval rate + median wait per tier (the rubber-stamp detector, §7.1)
SELECT tier,
       COUNT(*) FILTER (WHERE verdict='approved')::float / COUNT(*) AS approval_rate,
       percentile_disc(0.5) WITHIN GROUP (ORDER BY (verdict_time - request_time)) AS median_wait
FROM approval_verdict v JOIN approval_request r ON r.key = v.key
GROUP BY tier ORDER BY tier;

-- out-of-order approvals (verdict written after the action already touched things)
SELECT * FROM approval_verdict v
JOIN trajectory a ON a.payload->>'key' = v.key AND a.kind = 'action_started'
WHERE v.recorded_at < a.recorded_at;
```

Add both to the nightly observability query catalog (→ 13 §6). Approval-rate drift is a
first-class metric: a rising slope is the signal that fatigue has set in and evidence is
being rubber-stamped — *before* the incident that rubber-stamping eventually causes.

---

## 10. Real-World Case Studies

### 10.1 Claude Code — Permission Modes & Confirmation

Claude Code model permission modes (acceptEdits / bypassPermissions / plan mode / sandbox)
map almost exactly onto the tier taxonomy: file edits and shell commands are permissioned
by a consent stream, and its `/permissions` is the "escalate to read manually, with
reason" path. Three lessons:

1. **Granularity by action class, not by trust level.** A user trusts *a command* (a
   tool call stripped of the model's reasoning), not "the agent" as a persona. This is
   why tiering edits (`write`) separately from deploys (`elevated`) reads correctly.
2. **The model learns the consent boundary.** Agents that observe gates adjust their
   plans — they stop *proposing* force-pushes when the harness reliably shows them the
   red line. The deterrent effect is real (§ "Core Philosophy").
3. **Manual opt-out exists and is audited.** "Always allow" / `--dangerously-skip-permissions`
   is the documented, flag-protected escape hatch; the *default* remains gated. A harness
   without such an escape hatch fails in crisis, but the escape must never be the default.

### 10.2 Aider — Read/Write Modes as a Deny-By-Default Canon

Aider's signature is the explicit read/write prompt mode: a user runs it *without*
`--no-verify-edits` and explicitly opts into full-write (`--yes-always`) when they
choose to. That's two design decisions every gate loop should copy:

1. **Default is gated, and gating is visible.** Being able to *see* that the model will
   edit files is a consent to a *class* of action, not a per-call click-storm.
2. **It pairs with --auto-test and git history.** Every edit is a reversible, diffable,
   git-tracked event — so the *middle* tier can be auto-approved while the *irreversible*
   tier still gates. The lesson: the write tier should cost almost nothing, because the
   real safety net is reversibility (git + tests), and the real gate is reserved for
   things git/tests can't undo.

### 10.3 OpenHands — Confirmation Modes

OpenHands (formerly OpenDevin) exposes a fine-grained confirmation strategy for MCP and
code actions — "confirm on every action" vs "confirm on major changes" vs "never" —
mapping to `write` and `elevated` gates. The research-y punchline it demonstrates:
per-action confirmation ("confirm every change") is the *worst* ergonomics because it
trains rubber-stamping; the harness should instead model confirmation at plan-segment
granularity with batching (→ 7.1), not per tool call.

### 10.4 Devin — Asynchronous Oversight

Asynchronous agents (long-run, unattended) force the *gate to travel.* Devin surfaces a
"what am I doing right now / ask me for approval" panel that the human polls rather than
being interrupted — the gate is a *checkpoint you can pick up*, not a ping you must be
awake for. Its failure mode is familiar: the longer the run, the more the human stops
reading before approving. The design answer embedded in this module is timeout-deny
(→ 4.2) plus fatigue metrics (→ 9.3): asynchronous oversight is only safe when an
unanswered gate *fails closed and pages*, rather than silently waiting forever.

### 10.5 Human-AI Delegation Research — Automation Bias

Psych research on automation bias (automation complacency, e.g. Parasuraman & Manzey,
2010) is the empirical basis for every rule here: humans over-trust automated
suggestions, under-monitor, and — critically — *false alarms erode vigilance*. The
harness-level conclusions:

- If gates fire on benign things, humans stop checking the real ones (the cry-wolf
  curve, §14).
- Evidence beats narration: a human with a dry-run hash and a diff is measurably more
  discriminating than one with a "trust me, I checked" summary.
- Two-person rule exists because *one* human in a 3 AM post-incident state is exactly
  the automation-bias setup: tired, trusting, and approving.

---

## 11. TypeScript Interfaces for Approval

```typescript
// ── The Gate ───────────────────────────────────────────────────────────────
export type Tier = "read" | "write" | "elevated" | "prod-auth";
export type Verdict = "approved" | "denied" | "expired";
export type GateState =
  | { status: "waiting" }
  | { status: "settled"; verdict: Verdict; by: string; at: number };

export interface Gate {
  key: string;
  taskId: string;            // plan graph node (→ 04)
  runId: string;             // resume idempotency (→ 07 §13)
  tier: Tier;
  actorId: string;           // proposer — two-person rule anchor
  summary: string;
  diff: string;
  blastRadius: string[];
  dryRun: string;
  rollback: string;
  diffHash: string;
  dryRunHash: string;
  createdAt: number;
  expiresAt: number;
  state: GateState;
}

// ── Risk Registry ──────────────────────────────────────────────────────────
export interface RiskTableEntry {
  action: string;
  defaultTier: Tier;
  paths?: RegExp[];
  noDryRunAllowlist?: boolean;
}
export interface RoleRiskMatrix {
  role: string;               // → 12 §6 per-role policy
  entries: RiskTableEntry[];
  override?: { action: string; tier: Tier; reason: string; approvedBy: string; at: number };
}

// ── Gatekeeper ─────────────────────────────────────────────────────────────
export interface Gatekeeper {
  request(input: GateRequestInput): Gate;
  settle(key: string, v: Verdict, by: string, reason?: string): boolean;
  verdict(key: string): Verdict | undefined;
  armed(key: string): boolean;
}
export interface GateEngineContract {
  before(action: Step): Tier;              // enforcement at plan-time tag (§2.2)
  request(input: GateRequestInput): Gate;  // throws PAUSED:<key> after checkpoint
  onVerdict(key: string, v: Verdict): void; // approved→resume; denied/expired→replan
}

// ── Audit ──────────────────────────────────────────────────────────────────
export interface ApprovalAuditEvent {
  kind: "approval_request" | "approval_verdict" | "approval_policy" | "notification_sent";
  payload: { key: string; tier: Tier; actorId: string; approver?: string;
             verdict?: Verdict; reason?: string; diffHash?: string; dryRunHash?: string;
             by?: string; at: number };
  sessionId: string; taskId: string;     // join keys (→ 13 §4)
  tokens: { in: number; out: number };
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface GateInvariant { name: string; assert(g: Gate): void }
export interface FatigueMetric { tier: Tier; approvalRate: number; medianWaitMs: number }
```

---

## 12. Design Principles for Approval

### 12.1 SOLID for Approval Systems

| Principle | Application |
|-----------|-------------|
| **S**ingle responsibility | `RiskTable` tags tiers; `Gatekeeper` persists + settles; `Notifier` channels; audit is a *trajectory event*, not a gate concern |
| **O**pen/closed | New action classes = new `RiskTableEntry`, no Gatekeeper change |
| **L**iskov substitution | `TwoPersonGatekeeper` and `Gatekeeper` are interchangeable to the engine via the `Gatekeeper` interface |
| **I**nterface segregation | Debug UI needs `verdict()`; compliance needs `auditEvent`; the engine needs `request()/onVerdict()`. Don't couple them. |
| **D**ependency inversion | Gatekeeper depends on `TrajectoryStore` + risk table, not on the model or the engine loop |

### 12.2 Six Design Principles

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

---

## 13. Best Practices

### 13.1 DO ✅

- Tag tiers at plan time from a risk registry; let the engine enforce, never the model.
- Require diff + blast radius + dry-run + rollback in every payload; gate refuses to open without them.
- Fail closed: timeout → deny, with distinct `blocked(approval-timeout)` state.
- Deny → replan excluding the branch; recorded reason feeds the planner (→ 04 §14.2).
- Keep the two-person rule for `prod-auth`, enforced inside `settle`, not in the UI.
- Persist gates, reload them across restarts, re-arm expiry timers.
- Write every request/verdict as a trajectory event with `diffHash`/`dryRunHash` (→ 13).
- Batch `write`-tier reviews to keep human attention on the decisions that need it (§7.1).
- Measure approval rate + median wait per tier and treat drift as an incident signal.
- Test te restart path: open gate, kill process, restart, verdict still enforced.

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

---

## 14. Anti-Patterns & Solutions

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

---

## 15. Production Checklist

- [ ] **Tiers tagged at plan time** from a risk registry; model cannot self-select tier (→ 2.2)
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

---

## 16. Future Trends in Approval

### 16.1 Policy-as-Code Gate Registries (2026-2028)

The risk table migrates into a versioned, reviewable, policy-as-code artifact
(`approval-policy.yml`), diffed in PRs like any other infra. Tiers become auditable
declarations ("every `prod-auth` action in repo X must now page two people"), and a
policy diff that silently downgrades a tier is blocked by the same two-person rule that
protects the actions themselves. The gate system becomes both *enforcer* and *public
spec* — the "who can approve what" contract, versioned next to the code it protects.

### 16.2 Adaptive Trust with Continuous Evidence

Instead of a fixed `elevated` tier, the gate weight learns from trajectories: an action
class with a 6-month perfect dry-run + no-incident history gets a faster, quieter
pathway; a class with a recent incident gets an *automatic* stricter gate. Crucially,
downgrading trust must be automatic and metrics-driven (cheap, safe), while *restoring*
trust stays a human decision (expensive, slow). This is the same one-way trust ratchet
that makes security systems stable.

### 16.3 Approval as a Checkpoint Theorem

Gates collapse into the checkpoint/resume story (→ 07 §13): *gate = a checkpoint with a
verdict attached.* Then everything the checkpoint ecosystem already gives you — replay,
idempotency, audit, fork — applies to gates for free. A "deploy gate" is just a
`checkpoint(pause_until=verdict)` node in the plan graph, rendered as a timeline panel
and replayed for post-incident review.

### 16.4 Human-Scale Supervision at Agent Scale

As one human supervises many agents, gates must multiplex: a single review surface
showing *all* concurrent pending gates grouped by risk, batchable by decision, with
"approve identical class except prod-auth" flows — while never allowing one tired click
to authorize a `prod-auth` action. The cost of this future is vigilance economics: the
system must stop asking when the human is zoned out, which is exactly why the rubber-stamp
metric (→ 9.3) becomes the product dashboard of the next five years.

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
- `08-execute-task/README.md` §11 — idempotency cache that makes resume safe

---

*Document: XV. Approval Gates — HARNESS ENGINEERING EDITION*
*Cross-cutting module · control plane for irreversible actions · human-in-the-loop*
*Updated: 19/07/2026*
*Author: AI Knowledge Repository*