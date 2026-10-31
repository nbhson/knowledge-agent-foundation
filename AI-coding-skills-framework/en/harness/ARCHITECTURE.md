# ARCHITECTURE — Harness (01–15)

> Architecture overview of the `en/harness/` cluster. Vietnamese mirror: `vi/harness/ARCHITECTURE.md`.
>
> * `README.md` — the map: where each folder sits in a real harness.
> * `ARCHITECTURE.md` (this file) — overall design: layering, data flow, contracts, dependencies, how to build/debug.
> * `../HARNESS_ENGINEERING.md` — the full theory: 7 components, SOLID, 10 commandments, case studies.

This document explains how the 15 harness modules fit together: what a harness is, how a request flows through it, and which parts you can build later.

## 1. What is a harness

A harness = everything around the model that makes it trustworthy. Plain terms: LLM = the language model itself; tool_call = a request from the model to run a tool (read a file, run a command); observation = the result the harness returns to the model.

The harness is **everything around the LLM** that turns a single
`prompt → completion` call into a trustworthy `request → verified outcome` system.

Two loops with clearly distinguished owners:

* **Inner loop** (owned by the harness runtime, e.g. Claude Code / opencode):
  `LLM → tool_call → observation → LLM → … → stop`. This is "ask model, run tool, feed result back", repeated.
* **Outer loop** (owned by you, the loop engineer):
  `plan → execute → validate → fix → persist → evaluate`. This is the bigger cycle of managing the whole job, end to end.

```
┌──────────────────────── REAL HARNESS LIFECYCLE ──────────────────────────────┐
│  User request                                                                │
│      ▼                                                                       │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │01 Retri│─▶│02 Build│─▶│04 Plan │─▶│05 Promp│─▶│06 Tools│─▶│ LLM    │        │
│  │eve     │  │Context │  │Decompo │  │Builder │  │Decide  │  │ call   │        │
│  └────────┘  └────────┘  └────────┘  └────────┘  └────────┘  └────┬───┘        │
│       ▲                                                        │              │
│       │                                                   tool outputs        │
│       │                                                        │              │
│       │         ┌────────┐  ┌────────┐  ┌────────┐  ┌────────▼───┐            │
│       │         │03 Updat│◀─│11 Evalu│◀─│07 Workf│◀─│08 Task     │            │
│       │         │e Memory│  │ate     │  │low     │  │Execute    │            │
│       │         └────────┘  └────────┘  └────────┘  └────────────┘            │
│       │              ▲            ▲            │                              │
│       │              │            │            ▼                              │
│       │         ┌────┴────────────┴─────┐  ┌────────┐  ┌────────┐             │
│       └─────────│09 Multi-Agent (opt-  │  │10 Autom│  │Guardrai│             │
│                 │   ional, on demand)  │  │ation   │  │ls+Perms│             │
│                 └──────────────────────┘  └────────┘  │ (every │             │
│                                                       │ step)  │             │
│                                                       └────────┘             │
└──────────────────────────────────────────────────────────────────────────────┘
```

How to read the diagram: follow the arrows from "User request" at the top left. Boxes `01`–`11` are pipeline stages in order; `09`/`10` are optional side branches; "Guardrails+Perms" touches every step; the arrow back to `01` on the left is the loop closing (memory updated → next request starts better informed).

## 2. Layering: 7 components → 15 modules

This section maps the 7 big ideas of a harness onto the 15 folders in this repo, so each folder has one job you can learn and test alone.

How to read it: `#` = module number; `Folder` = the directory to open; `Component` = which of the 7 logical components it implements; `Input → Output` = what goes in and what comes out; `Read when` = the situation that makes this module relevant. Glosses: hybrid search = combining meaning-based (vector) and keyword (BM25) search; RRF fusion = a simple way to merge two ranked lists; DAG = a task graph with arrows, no cycles; CoT = "chain of thought" — asking the model to reason step by step; RBAC = role-based access control (permissions by role); saga = splitting a multi-step operation into steps that can each be undone; circuit breaker = stop calling a failing service for a while, like a fuse; HSM = hierarchical state machine, a formal way to define states and transitions.

| # | Folder | Component | Input → Output | Read when |
|---|---|---|---|---|
| 01 | `01-retrieve-memory-knowledge/` | Memory (read) | query → ranked chunks (score) | Need to find information: vector + BM25 hybrid, RRF fusion, rerank, GraphRAG |
| 02 | `02-build-context/` | Context | chunks + goal + history + files → `BuiltContext` within token budget | Window, compression, routing, caching, 5-level hierarchy |
| 03 | `03-update-memory-store/` | Memory (write) | run result → versioned facts/patterns | Write-back, consolidation/dedupe, KB CRUD, event sourcing |
| 04 | `04-plan-decompose-task/` | Orchestration (plan) | goal → DAG of `TaskNode` | Decomposition, Plan-and-Solve, ToT, ReWOO, ReAct, replanning |
| 05 | `05-prompt-builder/` | Guardrails (input shaping) | `BuiltContext` + template → final prompt | Template registry, few-shot, CoT, schema, injection defense |
| 06 | `06-decide-tools-mcp/` | Tools + Permissions | intent → approved tool call → observation | Registry, intent classifier, MCP client, RBAC, executor (timeout/retry) |
| 07 | `07-workflow/` | Orchestration (run) | DAG → result with error compensation | Sequential/parallel/DAG/HSM, saga, circuit breaker, tracing |
| 08 | `08-task/` | Orchestration (unit of work) | defines one trackable unit | Lifecycle, DAG deps, priority, budget, timeout/cancel. Thinnest — if lost, start here |
| 09 | `09-multi-agent/` | Orchestration (scale-out) | 1 task → N collaborating agents | Roles, message protocol, shared memory. Only when 04+07 are overloaded. Sub-agent details: `09-multi-agent/SUBAGENT.md` |
| 10 | `10-automation/` | Feedback (periodic) | schedule/event → automated run | CI/CD, scheduler, code-gen, test automation, self-healing with cost guards |
| 11 | `11-evaluation/` | Feedback (measurement) | run → pass/fail + metrics | Rubric, quality metrics, benchmark, LLM-judge, regression |
| 12 | `12-sandbox-execution/` | Cross-cutting: execution | untrusted code → isolated result | Threat model, blast radius, tiers: language → container → syscall filter |
| 13 | `13-trajectory-observability/` | Cross-cutting: observability | every step → `TrajectoryEvent` stream | Event contract, session stream, fork/replay/resume, join keys |
| 14 | `14-compaction-context/` | Cross-cutting: context | long context → compact context that stays correct | Trigger at 70% (don't wait for 90%), pin set, summarization vs pruning, compaction-safe prompt |
| 15 | `15-approval-gates/` | Cross-cutting: control | risky op → human decision | Risk tier, gate payload, timeout-deny, pause/resume, audit |

One more gloss for the table: "cross-cutting" = a concern that applies to every stage, not one step in the line — like electricity in a building, not a room.

Guardrails + Permissions are **not a stage** — they wrap every arrow
(check input, approve tool, validate output).

## 3. End-to-end flow of a request

This section walks one concrete request — *"Fix login bug"* — through all 10 steps, so the module numbers become a story.

1. **Retrieve (01).** Embed the query (turn the text into a vector of numbers so similar texts can be found), hybrid-search vector DB + BM25, rerank top-k. Fallback when empty.
2. **Build context (02).** Merge system + goal + chunks + summary + current files into the budget (e.g. 100k tokens). Trim lowest priority first. Mark untrusted content.
3. **Plan (04) → Task graph (08).** Generate the DAG `reproduce → locate → patch → test` (a to-do graph with arrows); each node has an id, input, budget, timeout, approval flag.
4. **Build prompt (05).** Render each task from a versioned template, attach few-shot examples (worked examples shown to the model), include the output schema (the required shape of the answer).
5. **Decide tools (06).** Intent classifier picks `read_file`, `run_tests`, … Check permissions (is writing outside `src/` allowed?). Risky op → pause and request approval (15).
6. **Execute workflow (07).** Run the DAG: sequential where dependent, parallel where independent. Retry with backoff (wait longer between each retry), circuit-break on repeated failure, saga compensation on partial success (undo finished steps when a later step fails).
7. **Inner tool loop (06 ↔ sandbox 12).** LLM calls tools, harness executes them in isolation, returns observations. Memoize duplicate calls (remember a result instead of recomputing it), cap result size.
8. **Validate (11).** Syntax check, run tests, score with an LLM-judge rubric (a scoring checklist applied by a model), measure trajectory metrics (steps, tool precision, recovery). Fail → replan or escalate.
9. **Persist (03).** Write what's worth keeping: success patterns, new facts, file summaries (versioned). Drop the noise.
10. **Automate (10) / Scale-out (09) — optional.** Schedule regression runs or fan out reviewer/tester agents via shared memory.

### 3.1. RAG sits at the start of the lifecycle

This short section locates RAG in the picture: it is the head of the pipeline, not the whole body.

```mermaid
flowchart TD
    Q["🔍 User Query"] --> RET["① RETRIEVE = 01<br/>hybrid + KG + web → top-50"]
    RET --> RERANK["② RE-RANK = end of 01<br/>cross-encoder → top-5"]
    RERANK --> BUILD["③ BUILD CONTEXT = 02 + 05<br/>concat + system + compress"]
    BUILD --> LLM["🧠 LLM"]
    LLM --> HARNESS["⇣ harness: 04 plan → 06 tools → 07 workflow → 08 task → 11 eval → 03 persist"]
```

Glosses: RAG = retrieval-augmented generation, i.e. find documents and paste them into the prompt before the model answers. KG = knowledge graph (entities and their relations). Cross-encoder = a model that scores each (query, document) pair for fit. top-50 → top-5 = narrowing 50 raw candidates to the 5 best.

RAG **doesn't run once** — it reruns per task / per inner-loop iteration whenever the query changes
(replan at `04` → retrieve again at `01`). RAG alone gets you a one-shot chatbot;
an end-to-end agent needs the rest.

## 4. Three shared contracts

This section names the three data shapes every module must agree on — the minimum glue between parts.

If the 11 modules share nothing else, share these 3 shapes:

> 📄 **Example code:** [`examples/01-4-three-shared-contracts.ts`](examples/01-4-three-shared-contracts.ts)

## 5. The control plane 12–15 (wrapping every stage)

This section covers the four "control plane" modules: they do not add steps to the pipeline, they make every step safe, recorded, survivable, and accountable.

How to read it: each row = one module; `Question` = the problem it answers; `Key mechanisms` = the main tools it uses, in plain terms below the table.

| Module | Question | Key mechanisms |
|---|---|---|
| 12 Sandbox | Where does untrusted code run? | Isolation tiers + 5 mandatory controls + role-based matrix. Every `tool_call` in 06 goes through here |
| 13 Trajectory | How is a run recorded for replay/audit? | Event contract + session stream (durable append + live tail) + fork/replay/resume. Sample engine in `03-update-memory-store/trajectory-fork-replay.md` |
| 14 Compaction | How does a long run survive the token ceiling? | Trigger at 70% (don't wait for 90%), pin set (system/goal never trimmed), pruning + summarization, compaction-safe prompt |
| 15 Approval | Who approves irreversible actions? | Risk tier assigned at plan time (04), gate payload for the human, timeout-deny, pause/resume, audit trail |

Quick glosses: isolation tiers = progressively stronger cages (language → container → syscall filter); fork/replay/resume = copy a run / re-run a recording / continue a run; timeout-deny = an unanswered approval expires as a "no".

## 6. Reading, building, debugging

This section gives three ready-made paths through the repo, depending on your goal.

* **New to this:** `08 → 07 → 02 → 06 → 01 → 03 → 04 → 05 → 11 → 10 → 09`, then `12 → 13 → 14 → 15`.
* **Minimal harness:** `02 + 05 + 06 + 07 + 11` is enough. Add `01/03` when you need memory, `04/08` for complex tasks, `09/10` last.
* **Debugging a bad run:** trajectory (`03/trajectory-fork-replay.md`) → `02` (wrong context?) → `06` (wrong tool?) → `11` (wrong rubric?).

## 7. Companion docs in this cluster

This table lists the extra deep-dive documents that sit next to the module READMEs.

How to read it: `File` = where the doc lives; `What it adds` = what you get beyond the module's own README.

| File | What it adds beyond the module README |
|---|---|
| `03-update-memory-store/trajectory-fork-replay.md` | Session event stream engine, fork/replay/resume |
| `06-decide-tools-mcp/code-mode-sdk.md` | Code-mode vs JSON tool-call pattern + sandbox sketch |
| `07-workflow/cordis-kernel-plugin.md` | Micro-kernel + plugin lifecycle, 4 runtime modes |
| `09-multi-agent/SUBAGENT.md` | Sub-agent spec: lifecycle, spawn API, narrowed permissions, budget, result aggregation |
| `11-evaluation/minimal-benchmark-harness.md` | Minimal harness isolation so evals stay unbiased |

## 8. Known gaps

This closing section is honest about what is not covered anywhere yet, so you can track it yourself.

The old cross-cutting concerns now have a home (`12–15`). Still unowned by any module:
PII/secret scrubbing pipeline (removing personal data and keys from logs), tenant isolation (keeping customers' data apart), cost-per-task SLO (a spending target per task). Per-module gaps live in the supplementary section of each README.

> **One-line summary:** The harness is 11 pipeline stages plus 4 cross-cutting controls around the model, glued by 3 shared data shapes — start with 08, build the minimum five, and never skip 12–15.
