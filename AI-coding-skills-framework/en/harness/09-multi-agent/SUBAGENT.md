# 🧬 Sub-Agent — Lifecycle, Spawn, Permissions and Budget Spec

> Companion to `README.md` (esp. §16 Fault tolerance / Messaging / Isolation).
> Consolidates conventions from `loop/01-concepts` (§2.5 Maker/Checker),
> `loop/02-patterns/*`, `loop/04-operating`, `loop/06-anti-patterns`,
> and the Claude Code example in `README.md §16.5`.

> ## 📑 Table of Contents
>
> - [Overview](#overview) - [Contents](#contents)
> - [1. Definitions](#1-definitions)
> - [2. Role Taxonomy](#2-role-taxonomy)
> - [3. Lifecycle](#3-lifecycle)
> - [4. Spawn API](#4-spawn-api-minimum-contract)
> - [5. Context and Memory](#5-context-and-memory)
> - [6. Isolation and Secrets](#6-isolation-and-secrets)
> - [7. Result Aggregation](#7-result-aggregation)
> - [8. Budget & Cost Guards](#8-budget--cost-guards)
> - [9. Testing Sub-Agents](#9-testing-sub-agents)
> - [10. Anti-Patterns](#10-anti-patterns--solutions)
> - [11. Real-World Implementations](#11-real-world-implementations)
> - [12. Checklist](#12-checklist--production-deployment)
> - [Best Practices](#best-practices) - [References](#references)
>
> ---

### Opening Story

Imagine a **special-ops mission**. The commander (parent) does not storm every building herself. She sends a **recon team** (researcher) to map terrain, a **breach squad** (implementer) to open one door, and an **inspector** (verifier) to confirm it is clear. Each squad gets a map excerpt — not the war plan — a time window, and a rule: report back, do not freelance.

**A sub-agent is that squad.** Without narrow mission + trimmed map + own budget + deadline (lease), it is not a squad — just noise in the same room.

### Why Does This Spec Matter?

> *"A parent without sub-agent discipline forwards the entire inbox to every intern — everyone drowns, nobody owns the outcome."*

| # | Research | Key Finding |
|---|----------|-------------|
| 1 | **Anthropic — Claude Code (2025)** | Isolated subagents cut privilege-escalation risk ~70% |
| 2 | **Google DeepMind (2025)** | Maker/checker split cuts rubber-stamp approvals ~45% |
| 3 | **LangGraph (2025)** | Lease + heartbeat + idempotent requeue recovers ~90% crashed subtasks |

```
Sub-Agent = Narrow Role + Trimmed Context + Narrowed Tools + Own Budget + Lease + Independent Check
```

## Overview

> **📌 Core Concept**
>
> - **Concept:** A Sub-Agent is a child agent for **one narrow task**, running the same harness with **trimmed context, narrowed tools, own budget, lease**.
> - **Analogy:** Like a kitchen ticket — one chef, one recipe excerpt, one timer. Timer rings → ticket reassigned, old plate discarded (fencing).
> - **Why it matters:** Without this contract, sub-agents bloat context, leak secrets, double-write files, and self-approve weak work.

```
┌───────────────────────────────────────────────────────────────┐
│  PARENT (full ctx, all tools) ──spawn(spec)──► SUB-AGENT      │
│    files[] + summary │ tools[] │ budget │ lease │ worktree    │
│                      └── artifact + transcript ──► aggregate   │
└───────────────────────────────────────────────────────────────┘
```

How to read this diagram? Left is the parent with full context. The arrow is `spawn(SubAgentSpec)` carrying only files + summary + tool allow-list + budget + lease. Right is the sub-agent in its worktree. The return arrow is artifact + trimmed transcript into the aggregator (checker/quorum). Nothing else flows back.

## Contents

| # | Topic | Key idea |
|---|-------|----------|
| 1 | [Definitions](#1-definitions) | Agent vs sub-agent vs loop vs function call |
| 2 | [Role Taxonomy](#2-role-taxonomy) | implementer / verifier / reviewer / researcher |
| 3 | [Lifecycle](#3-lifecycle) | spawn → heartbeat → done / DEAD / TIMED_OUT / SUSPECT |
| 4 | [Spawn API](#4-spawn-api-minimum-contract) | Minimum contract + validation + examples |
| 5 | [Context/Memory](#5-context-and-memory) | Private scratchpad + versioned blackboard |
| 6 | [Isolation/Secrets](#6-isolation-and-secrets) | Least tools per role + short leases |
| 7 | [Aggregation](#7-result-aggregation) | Maker/checker + quorum + message caps |
| 8 | [Budget](#8-budget--cost-guards) | Max 3 spawns/run + kill switch |
| 9 | [Testing](#9-testing-sub-agents) | Unit + chaos drills |
| 10 | [Anti-patterns](#10-anti-patterns--solutions) | 8 traps |
| 11 | [Implementations](#11-real-world-implementations) | Claude Code, triage loop |
| 12 | [Checklist](#12-checklist--production-deployment) | Ship-ready gate |

---

## 1. Definitions

> **📌 Core Concept**
>
> - **Concept:** Hard boundary — **Agent** owns task + full loop; **Sub-agent** owns exactly one narrow task under lease; **Loop** is a cron schedule; a function call has no lease/budget/tools.
> - **Analogy:** Agent = manager; sub-agent = line cook with one ticket; loop = shift schedule; function call = handing a knife with no ticket.
> - **Why it matters:** Calling everything "sub-agent" loses fencing and verification — work gets overwritten, secrets leak.

### 1.1 Comparison Table

| Entity | Owns | Context | Tools | Budget | Lease | Verifier |
|---|---|---|---|---|---|---|
| **Agent** | task + memory, full harness (01→11) | full | broad | large | own deadline | external |
| **Sub-agent** | **one narrow task** | **trimmed (files[] + summary)** | **allow-list** | **own small budget** | **leaseId + deadline + maxAttempts** | **independent** |
| **Loop** | schedule (cron), may spawn each run | watchlist state | triage tools | per-run cap (<5k if idle) | run deadline | state gate |
| Function call | nothing (returns value) | args only | callee scope | caller budget | none | caller |

* **Agent**: entity running the full harness loop (01→11), owning a task and memory.
* **Sub-agent**: child spawned by parent/orchestrator for **one narrow task**, running same harness but with **trimmed context + narrowed tools + own budget + lease**.
* **Loop**: scheduled loop (cron) that may spawn sub-agents each run (`loop/05-multi-loop`).

Rule: without lease + deadline + own budget + own tool allow-list, it is not a sub-agent — just a function call.

### 1.2 Sub-Agent Contract Guard

<details>
<summary>Python — reject fake sub-agents</summary>

> 📄 **Example code:** [`examples/01-1-2-sub-agent-contract-guard.py`](examples/01-1-2-sub-agent-contract-guard.py)

</details>

---

## 2. Role Taxonomy

> **📌 Core Concept**
>
> - **Concept:** Four narrow roles — maker writes, checker tests, reviewer judges diff, researcher reports facts. Each role gets minimal tools.
> - **Analogy:** Like a newsroom — reporter gathers, writer drafts, editor cuts, fact-checker verifies. Never let writer fact-check herself.
> - **Why it matters:** Role + tool binding is the privilege boundary. Same agent implementing AND verifying = confirmation bias.

### 2.1 Role Matrix

| Role | Does | Must not | Tools (from 12-sandbox §6) |
|---|---|---|---|
| `implementer` / `maker` | Writes code in assigned worktree | Self-merge, final self-verify | sandboxed shell (no net), scoped FS write |
| `verifier` / `checker` | Runs tests, gates, rubric (default REJECT) | Edit code directly (comments only) | test runner, read FS, no write |
| `reviewer` | Reviews diffs, severity Blocker/Major/Minor | Run shell, write files outside comments | read-only FS, no shell |
| `researcher` / `triage` | Reads code/docs, facts + `file:line` citations | Change behavior, write long-term memory | read-only FS + search, no exec |

Forbidden anti-pattern (`loop/06-anti-patterns`): same agent implements AND verifies → weak tests get rubber-stamped.

### 2.2 Detailed Role Definitions

<details>
<summary>Python — role specs with DoD</summary>

> 📄 **Example code:** [`examples/02-2-2-detailed-role-definitions.py`](examples/02-2-2-detailed-role-definitions.py)

</details>

---

## 3. Lifecycle

> **📌 Core Concept**
>
> - **Concept:** Every sub-agent lives under a lease: heartbeat proves liveness, deadline bounds cost, hang detector catches silent stalls, fencing makes stale completions harmless.
> - **Analogy:** Like a taxi meter + GPS — driver pings location every 5s; no ping 15s = lost; meter expiry = trip cancelled; new driver gets new ticket number (fencing).
> - **Why it matters:** Without fencing + idempotent requeue, a zombie agent wakes up late and overwrites good work.

### 3.1 Lifecycle State Machine

The diagram is a one-way flow with one retry loop: spawn carries the §4 spec, heartbeat ticks every 5s with a progress stream, done returns artifact + trimmed transcript. Faults branch to DEAD (no heartbeat >15s), TIMED_OUT (past deadline), SUSPECT (alive but no progress >60s). Requeue bumps fencing token + attempt and attaches prior transcript; after 3 attempts escalate to human / fail closed.

```text
spawn (with section-4 spec) → heartbeat 5s → progress stream
  → done (artifact + trimmed transcript)
  → fault: DEAD (heartbeat lost >15s) / TIMED_OUT (deadline) / SUSPECT (no progress >60s)
  → requeue (fencing token++, attempt++, prior transcript attached) → >3 attempts → escalate / fail closed
```

```
┌─────────┐  heartbeat 5s   ┌──────────┐  artifact  ┌──────┐
│  SPAWN  │────────────────►│ RUNNING  │───────────►│ DONE │
│ spec §4 │  progress stream│ lease    │  transcript│      │
└────┬────┘                 └────┬─────┘            └──────┘
     │  DEAD / TIMED_OUT /       │ SUSPECT (>60s no progress)
     │  SUSPECT                  ▼
     │                     ┌──────────┐  attempt++ ┌──────────┐
     └────────────────────►│ REQUEUE  │───────────►│ ESCALATE │
        fencing token++     │ idempotent│  >3 tries │ human    │
        prior transcript    └──────────┘            └──────────┘
```

* Every task has `lease_id + deadlineMs + max_attempts` (default 300s deadline, max 3).
* Stateless supervisor backed by queue (Redis/BullMQ); workers must be idempotent for safe requeue. Judge/voter quorum: 2f+1 tolerates f faults, majority required (e.g. 2/3).
* Implementation: `README.md §16.1–16.2` (heartbeat + reassignment sample).

### 3.2 Heartbeat Supervisor

<details>
<summary>Python — lease + heartbeat + fencing</summary>

> 📄 **Example code:** [`examples/03-3-2-heartbeat-supervisor.py`](examples/03-3-2-heartbeat-supervisor.py)

</details>

---

## 4. Spawn API (Minimum Contract)

> **📌 Core Concept**
>
> - **Concept:** Spawn carries the narrowest sufficient context: file allow-list + artifact refs + trimmed parent summary — never a full dump.
> - **Analogy:** Like handing a plumber the blueprint of one bathroom, not the whole city sewage map.
> - **Why it matters:** Full-context dump multiplies tokens per spawn and leaks secrets/prompts into every child.

### 4.1 Spawn Interface

> 📄 **Example code:** [`examples/04-4-1-spawn-interface.ts`](examples/04-4-1-spawn-interface.ts)

### 4.2 Spawn Validation and Examples

<details>
<summary>TypeScript — validate + two spawn examples</summary>

> 📄 **Example code:** [`examples/05-4-2-spawn-validation-and-examples.ts`](examples/05-4-2-spawn-validation-and-examples.ts)

</details>

### 4.3 Spawn Rules and Cost Guards

Spawn rules (`loop/04-operating`): cheap triage first, spawn only when state reports actionable work; empty watchlist → exit <5k tokens, no spawn. **Max 3 sub-agents/run** by default.

| Rule | Threshold | Action |
|---|---|---|
| Idle run | watchlist empty | exit <5k tokens, spawn nothing |
| Fan-out cap | >3 spawns requested | queue remainder, escalate or next run |
| Budget cap | child >8k tokens | split goal into 2+ narrower tasks |
| Triage first | unknown scope | researcher before implementer |

---

## 5. Context and Memory

> **📌 Core Concept**
>
> - **Concept:** Scratchpads stay private; only diffs/facts publish to a versioned blackboard via CAS. Single-writer per file/section prevents overwrite races.
> - **Analogy:** Like Google Docs suggestions — everyone drafts privately, only accepted edits land, and concurrent edits merge instead of clobbering.
> - **Why it matters:** Blind overwrites are the #1 multi-agent data-loss bug.

### 5.1 Private by Default + Blackboard

* **Private by default:** each sub-agent has its own scratchpad; publishes only diffs/facts to the shared blackboard via `blackboard.write(key, value, expectedVersion)` (CAS semantics).
* **Single-writer:** orchestrator assigns file/section ownership (e.g. only `coder` writes `auth.ts`).
* **Namespaced:** keys under `agent_id/task_id/*`; cross-agent reads via allow-listed projections only (`README.md §16.3`).

### 5.2 CAS + Single-Writer + Namespacing

<details>
<summary>Python — versioned blackboard with CAS</summary>

> 📄 **Example code:** [`examples/06-5-2-cas-single-writer-namespacing.py`](examples/06-5-2-cas-single-writer-namespacing.py)

</details>

Good vs bad handoff:

| ❌ Bad (full dump) | ✅ Good (trimmed) |
|---|---|
| Paste 40k-token parent log | 5-line parentSummary + 2 files + 1 artifact ref |
| Inline 2MB test log | Artifact ref `s3://.../logs` + hash + top-20 failing lines |
| Share raw secrets | Short lease scope + env injection, redacted in logs |

---

## 6. Isolation and Secrets

> **📌 Core Concept**
>
> - **Concept:** Each role resolves to the same sandbox policy solo or in swarm; secrets are short per-agent leases, never shared context.
> - **Analogy:** Like hotel key cards — each opens one room, expires at checkout, and the master key never leaves the front desk.
> - **Why it matters:** One over-privileged child can exfiltrate repo + secrets for the whole run.

### 6.1 Least-Privilege Tool Matrix

* Tiers/controls/runners belong to `12-sandbox-execution` sections 2-6; the multi/sub-agent addition is: **least tools per role** (reviewer: read-only FS, no shell; coder: sandboxed shell, no net), resolved from the same role matrix so solo and swarm runs resolve to the same policy for the same role.

> 🔑 **Policy / Permission highlight:** sub-agent tool grants are **permission projections, not new policy** — each role inherits the minimum tools from `12-sandbox-execution` §6, and any grant outside that matrix must be denied at spawn validation (§4).
* Deny-by-default egress with per-agent domain allow-list; every tool I/O audited with `agent_id + lease_id`.
* Code-editing sub-agents: `isolation: worktree` + lock/queue in state (`"PR #1234 — worktree in progress"`) so two sub-agents never edit the same files.

| Role | FS | Shell | Network | Extra |
|---|---|---|---|---|
| implementer | scoped write (worktree) | sandboxed, no net | deny default | worktree lock required |
| verifier | read + test output | test runner only | deny default | cannot edit code |
| reviewer | read-only | none | deny default | comment API only |
| researcher | read-only + search | none | allow-listed docs | no memory write |

### 6.2 Secret Leases and Audit

* Secrets are **per-agent leases** (short-lived scoped tokens, 5–15m, env injection), supervisor redacts `sk-*, ghp_*, AWS_*` from logs/transcripts; one agent's secret never appears in another agent's context (`README.md §16.4`).

<details>
<summary>Python — redact + scoped secret</summary>

> 📄 **Example code:** [`examples/07-6-2-secret-leases-and-audit.py`](examples/07-6-2-secret-leases-and-audit.py)

</details>

---

## 7. Result Aggregation

> **📌 Core Concept**
>
> - **Concept:** Maker output is untrusted until an independent checker or quorum accepts it; messages are small, ordered, deduplicated.
> - **Analogy:** Like peer review — author submits, two reviewers vote, editor (aggregator) decides; oversized appendices become supplementary links (artifact refs).
> - **Why it matters:** Self-accepted work drifts; unbounded messages blow context and reorder results.

### 7.1 Maker / Checker and Quorum

* Maker/checker: implementer finishes → independent verifier runs tests/gates; default verdict REJECT until evidence is sufficient (build OK, tests OK, AC traced).
* Quorum: reviewers vote 2-of-3; one crashed voter never blocks merge.

<details>
<summary>Python — quorum aggregator</summary>

> 📄 **Example code:** [`examples/08-7-1-maker-checker-and-quorum.py`](examples/08-7-1-maker-checker-and-quorum.py)

</details>

### 7.2 Messaging Guarantees

* Payload: 64KB header + 512KB body caps; larger → artifact ref. Messages carry `msg_id` (dedupe), per-task FIFO (reject out-of-order `seq`), 30s request/reply timeout.

| Guarantee | Mechanism | Limit |
|---|---|---|
| Dedupe | `msg_id` set | drop duplicates |
| Ordering | per-task `seq` FIFO | reject gap/out-of-order |
| Size | header/body caps | overflow → artifact ref |
| Liveness | 30s req/reply timeout | timeout → SUSPECT → requeue |

---

## 8. Budget and Cost Guards

> **📌 Core Concept**
>
> - **Concept:** Every spawn spends from a capped envelope; idle runs spend almost nothing; over-budget work splits instead of sprawling.
> - **Analogy:** Like a film shoot — each scene has a budget; no actionable footage → wrap early and send crew home.
> - **Why it matters:** Unbounded fan-out is the fastest way to burn $50 on a no-op cron run.

| Guard | Default | Behavior |
|---|---|---|
| Max spawns / run | 3 | queue or defer the rest |
| Idle exit | <5k tokens | triage only, no spawn |
| Child budget | 2–8k tokens | split task if larger |
| Step cap | 10–25 steps | stop → summarize → escalate |
| Timeout | 120–300s | TIMED_OUT → requeue (max 3) |
| Kill switch | run budget exceeded | cancel lowest-priority leases first |

<details>
<summary>Python — budget guard</summary>

> 📄 **Example code:** [`examples/09-8-budget-and-cost-guards.py`](examples/09-8-budget-and-cost-guards.py)

</details>

---

## 9. Testing Sub-Agents

> **📌 Core Concept**
>
> - **Concept:** Test the contract, not just the model — validation, fencing, CAS, redaction, and crash recovery all have deterministic tests.
> - **Why it matters:** Sub-agent bugs are concurrency + security bugs; they only show up under crash/reorder/adversarial input.

| # | Test | Expected |
|---|---|---|
| 1 | `validateSpec` rejects implementer without worktree | error list non-empty |
| 2 | Reviewer with `shell` tool | rejected |
| 3 | Kill child mid-run (no heartbeat 15s) | DEAD → requeue with token++ |
| 4 | Stale token result arrives late | discarded (fencing) |
| 5 | Two writers same key, same version | one CAS win, one retry |
| 6 | Log contains `ghp_fake123` | redacted |
| 7 | 2MB result payload | artifact ref, not inline |
| 8 | Out-of-order `seq` | rejected |
| 9 | Verifier edits code | policy denial |
| 10 | Idle watchlist run | <5k tokens, zero spawns |

<details>
<summary>Python — fencing + CAS test</summary>

> 📄 **Example code:** [`examples/10-9-testing-sub-agents.py`](examples/10-9-testing-sub-agents.py)

</details>

---

## 10. Anti-Patterns and Solutions

> **📌 Core Concept**
>
> - **Concept:** Most sub-agent failures are contract violations with innocent names: "just share everything", "just let it verify itself", "just one more spawn".
> - **Why it matters:** Naming the trap + fix turns tribal knowledge into a gateable checklist.

| # | Anti-Pattern | Symptom | Fix |
|---|---|---|---|
| 1 | God child (full context dump) | 40k tokens/spawn | files[] + summary + artifact refs |
| 2 | Self-verify | weak tests pass | independent verifier, default REJECT |
| 3 | Spawn storm | 20 children, $ burst | max 3/run + queue |
| 4 | Shared scratchpad | overwritten facts | private pad + CAS blackboard |
| 5 | Secret smuggling | key in child log | per-agent lease + redact |
| 6 | Zombie write | late result clobbers fix | fencing token check |
| 7 | Tool creep (reviewer + shell) | unexpected `rm -rf` | role→tool matrix gate |
| 8 | Silent hang | alive, 0 progress, burns budget | 60s SUSPECT detector + deadline |

---

## 11. Real-World Implementations

### 11.1 Claude Code — Explore Subagents (Anthropic, 2025)

Claude Code's Explore agents are researchers: read-heavy, write-restricted, spawned for codebase Q&A. Lesson copied here: **narrow tools + trimmed context + independent aggregation** — the child never merges, the parent decides.

> 📄 **Example code:** [`examples/11-11-1-claude-code-explore-subagents-anthropic-2025.py`](examples/11-11-1-claude-code-explore-subagents-anthropic-2025.py)

### 11.2 Nightly Triage Loop (`loop/05-multi-loop` style)

```text
cron 02:00 → triage (cheap) → watchlist empty? exit <5k
  → else spawn ≤3: researcher ×1 → implementer ×1 (worktree) → verifier ×1
  → quorum 2-of-3 → artifact PR → state records lease + verdict
```

Spawn only when state reports actionable work; otherwise exit cheap. This is the `loop/04-operating` cost guard applied to sub-agents.

### 11.3 Debug Squad (from README §7.3)

One researcher isolates the failing path with citations, one implementer patches in a worktree, one verifier reproduces before/after. Shared memory holds only the failing test + artifact refs — never full logs.

---

## 12. Checklist and Production Deployment

### 12.1 Pre-Spawn Gate

[ ] Full section-4 spec (narrow role, trimmed context, tool allow-list, worktree for code edits, budget/timeout/lease) [ ] heartbeat + deadline + hang detector [ ] fencing token on requeue

### 12.2 Safety and Cost Gate

[ ] max 3 attempts + escalation path [ ] CAS + single-writer + namespacing [ ] short secret leases + redaction + no cross-leak [ ] max 3 spawns/run + kill switch [ ] independent verifier, never self-verify

### 12.3 Deployment Checklist

| Area | Check |
|---|---|
| Supervisor | stateless, queue-backed, idempotent workers |
| Observability | `agent_id + lease_id` on every tool I/O; heartbeat dashboard |
| Audit | secret redaction test green; egress deny-default |
| Rollback | fencing on; stale results discarded |
| Cost | run cap + per-child cap + idle-exit verified |

---

## Best Practices

1. **Triage before spawn** — researcher first when scope is unknown.
2. **One ticket per child** — split broad goals; reject >8k-token children.
3. **Trim context aggressively** — summary + refs beat dumps.
4. **Bind role to tools** — resolve from one matrix (12-sandbox §6).
5. **Isolate edits** — worktree + lock per code-editing child.
6. **Default REJECT** — verifier needs build + tests + AC trace.
7. **Fence everything** — token check on every late result.
8. **Lease secrets** — 5–15m scope, env injection, redact logs.
9. **Cap messages** — refs over inline for large payloads.
10. **Exit cheap when idle** — <5k tokens, zero spawns.

## References

### Frameworks

* Claude Code — subagent tool + permission modes (Anthropic, 2025)
* LangGraph — Supervisor + worker + checkpointing
* AutoGen / CrewAI — role-based delegation (`tools/`)

### Research and Papers

* Anthropic: tool-use + least-privilege delegation (2025)
* DeepMind: structured workflows −45% failure (2025)

### Production Systems

* `README.md §16` — heartbeat, messaging, isolation samples
* `12-sandbox-execution §2–§6` — tiers, controls, role policy matrix
* `loop/04-operating` — cost guards; `loop/06-anti-patterns` — maker/checker split
* `08-task` — TaskNode lifecycle linked via `taskId`

### Architecture Patterns

* Maker/Checker, Judge quorum (2f+1), Blackboard (CAS), Lease + Fencing, Worktree isolation
