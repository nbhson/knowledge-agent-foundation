# 🤖 IX. Multi-Agent

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Agent Roles](#1-agent-roles)
>   - [1.1 Agent Role Taxonomy](#11-agent-role-taxonomy)
>   - [1.2 Detailed Agent Definitions](#12-detailed-agent-definitions)
> - [2. Communication Patterns](#2-communication-patterns)
>   - [2.1 Communication Patterns Overview](#21-communication-patterns-overview)
>   - [2.2 Message Protocol](#22-message-protocol)
> - [3. Orchestration Strategies](#3-orchestration-strategies)
>   - [3.1 Strategy Comparison](#31-strategy-comparison)
>   - [3.2 Orchestrator Implementation](#32-orchestrator-implementation)
> - [4. Shared Memory](#4-shared-memory)
>   - [4.1 Memory Architecture](#41-memory-architecture)
>   - [4.2 Shared Memory Manager](#42-shared-memory-manager)
> - [5. Conflict Resolution](#5-conflict-resolution)
>   - [5.1 Conflict Types & Resolution](#51-conflict-types-resolution)
>   - [5.2 Conflict Resolution Manager](#52-conflict-resolution-manager)
> - [6. Agent Selection Guide](#6-agent-selection-guide)
>   - [6.1 When to Use Multi-Agent](#61-when-to-use-multi-agent)
> - [7. Real-World Implementations](#7-real-world-implementations)
>   - [7.1 Code Review Pipeline](#71-code-review-pipeline)
>   - [7.2 Feature Development Team](#72-feature-development-team)
>   - [7.3 Debug Squad](#73-debug-squad)
> - [8. Debugging Multi-Agent Systems](#8-debugging-multi-agent-systems)
>   - [8.1 Debug Strategy](#81-debug-strategy)
>   - [8.2 Debug Logger](#82-debug-logger)
> - [9. Performance Optimization](#9-performance-optimization)
>   - [9.1 Optimization Strategies](#91-optimization-strategies)
>   - [9.2 Cost Estimation](#92-cost-estimation)
> - [10. Anti-Patterns & Solutions](#10-anti-patterns-solutions)
>   - [10.1 Common Anti-Patterns](#101-common-anti-patterns)
> - [11. Production Deployment](#11-production-deployment)
>   - [11.1 Deployment Checklist](#111-deployment-checklist)
> - [Best Practices](#best-practices)
> - [12. Case Studies — Real-World Multi-Agent Architectures](#12-case-studies-real-world-multi-agent-architectures)
>   - [12.1 Claude Code — Anthropic's Multi-Agent Architecture](#121-claude-code-anthropics-multi-agent-architecture)
>   - [12.2 Devin — Autonomous Software Engineering Agent](#122-devin-autonomous-software-engineering-agent)
>   - [12.3 OpenHands (OpenDevin) — Open-Source Multi-Agent](#123-openhands-opendevin-open-source-multi-agent)
> - [13. Advanced Multi-Agent Patterns](#13-advanced-multi-agent-patterns)
>   - [13.1 MapReduce Pattern for Code Generation](#131-mapreduce-pattern-for-code-generation)
>   - [13.2 Debate Pattern — Multi-Agent Discussion](#132-debate-pattern-multi-agent-discussion)
>   - [13.3 Critique-Revision Pattern](#133-critique-revision-pattern)
>   - [13.4 Ensemble Pattern — Multiple Agents, Best Output](#134-ensemble-pattern-multiple-agents-best-output)
> - [14. Multi-Agent Testing Strategies](#14-multi-agent-testing-strategies)
>   - [14.1 Testing Multi-Agent Systems](#141-testing-multi-agent-systems)
>   - [14.2 Test Implementation](#142-test-implementation)
> - [15. Cost-Benefit Analysis](#15-cost-benefit-analysis)
>   - [15.1 When Multi-Agent Is Worth It](#151-when-multi-agent-is-worth-it)
>   - [15.2 Token Cost Comparison](#152-token-cost-comparison)
> - [17. October 2026 Update — Multi-Agent Production Research (Anthropic, A2A)](#17-october-2026-update--multi-agent-production-research-anthropic-a2a)
>   - [17.1 Production results (Anthropic Research, 06/2025)](#171-production-results-anthropic-research-062025)
>   - [17.2 A2A Protocol (Linux Foundation, 2026)](#172-a2a-protocol-linux-foundation-2026)
>   - [17.3 8 prompting principles for multi-agent](#173-8-prompting-principles-for-multi-agent)
>   - [17.4 Sub-agent output via filesystem](#174-sub-agent-output-via-filesystem)
>   - [17.5 Sync vs Async](#175-sync-vs-async)
> - [References](#references)
>   - [Frameworks](#frameworks)
>   - [Research & Papers](#research-papers)
>   - [Production Systems](#production-systems)
>   - [Architecture Patterns](#architecture-patterns)
>
---

### Opening Story

Remember the fun of a **heist** movie like *Ocean's Eleven*? Eleven friends, eleven superpowers: Danny plans, Basher cracks locks, Saul masters disguises, Terry drives the getaway. Ask any one of them to pull the whole job solo and they would laugh — but together? Pure movie magic.

**AI Multi-Agent works exactly the same way.**

One AI agent is like one talented friend who says "I can do it all!" — and for small favors, that is true. But hand them a monster job like *"Build our payment system, with tests, docs, and a security review"* and watch them **burn out**. Their notebook overflows with five jobs' worth of notes, nobody double-checks their work, and worst of all, **they end up nodding along to their own mistakes**.

**The friendly fix**: a Multi-Agent crew — each agent becomes a **specialist in just one craft**, they chat through a shared walkie-talkie protocol, and they double-check each other like good teammates, so quality stays high.

### Why Is Multi-Agent Important?

> *"A single agent is like one person doing everything — capable but slow, easily overloaded, and without checks & balances."*

#### 3 Scientific Pieces of Evidence

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **AutoGen (Microsoft, 2025)** | Multi-agent architecture solved **68% of complex coding tasks** successfully, compared to **41%** for single-agent |
| 2 | **CrewAI Research (2025)** | Agent teams with role specialization improved **code quality by 52%** (measured by review scores) |
| 3 | **Google DeepMind (2025)** | The multi-agent debate pattern reduced the **hallucination rate by 35%** in code generation |

#### Core philosophy:

```
Multi-Agent = Specialization + Communication + Coordination + Checks & Balances
```

Each agent = **a specialist in one domain**. Like a multi-specialty hospital — the general practitioner (Orchestrator), the cardiologist (Backend Agent), the surgeon (Frontend Agent), the pharmacist (Testing Agent). They don't do everything — they do their own part **best in class**.

**If you skip it**: the single agent overloads, there is no peer review, wrong code is produced without anyone catching it, and the context window is wasted by having to hold knowledge for every domain.

## Overview

> **📌 Core Concept**
>
> - **Concept:** A Multi-Agent System is an architecture in which **multiple AI agents work together**, each taking on a specialized role (writing code, reviewing, testing...) to complete tasks that are too complex for a single agent.
> - **Analogy/comparison:** Like a hospital — the general practitioner does the initial exam, the cardiology specialist handles heart issues, the pharmacist prescribes medication. No one does everything, but the coordination produces the correct outcome.
> - **Why it matters:** A single agent easily overloads and "confirms its own mistakes" on complex tasks — multi-agent adds cross-checks (checks & balances).

**Multi-Agent Systems** in AI coding simply mean **a small team of AI friends building something together** — each friend owns one specialty, and by chatting and double-checking each other they finish big jobs that would exhaust any solo agent.

```
┌──────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │ Planner  │───►│ Coder    │───►│ Reviewer │            │  │
│  │  │ Agent    │    │ Agent    │    │ Agent    │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │       │               │               │                   │  │
│  │       └───────────────┴───────────────┘                   │  │
│  │                       │                                    │  │
│  │              ┌────────┴────────┐                          │  │
│  │              │  Coordinator    │                          │  │
│  │              │  / Orchestrator │                          │  │
│  │              └────────┬────────┘                          │  │
│  │                       │                                    │  │
│  │         ┌─────────────┼─────────────┐                    │  │
│  │         ▼             ▼             ▼                     │  │
│  │    ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │    │ Tester   │  │ Debugger │  │ DevOps   │             │  │
│  │    │ Agent    │  │ Agent    │  │ Agent    │             │  │
│  │    └──────────┘  └──────────┘  └──────────┘             │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Agent Roles](#1-agent-roles) | Common agent roles |
| 2 | [Communication Patterns](#2-communication-patterns) | Communication patterns between agents |
| 3 | [Orchestration Strategies](#3-orchestration-strategies) | Orchestration strategies |
| 4 | [Shared Memory](#4-shared-memory) | Shared memory among agents |
| 5 | [Conflict Resolution](#5-conflict-resolution) | Resolving conflicts |
| 6 | [Agent Selection Guide](#6-agent-selection-guide) | Choosing the right structure |
| 7 | [Real-World Implementations](#7-real-world-implementations) | Real-world examples |
| 8 | [Debugging Multi-Agent Systems](#8-debugging-multi-agent-systems) | Debug & troubleshoot |
| 9 | [Performance Optimization](#9-performance-optimization) | Optimizing performance |
| 10 | [Anti-Patterns & Solutions](#10-anti-patterns--solutions) | Common mistakes |
| 11 | [Production Deployment](#11-production-deployment) | Real-world deployment |

---

## 1. Agent Roles

> **📌 Core Concept**
>
> - **Concept:** Agent Roles are the way expertise is divided up — each agent (orchestrator, coder, reviewer, tester...) owns a single responsibility and a set of skills so they can cooperate on complex work.
> - **Analogy/comparison:** Like a soccer team: the goalkeeper specializes in catching the ball, the striker in scoring goals. Clear roles keep the whole team in sync.
> - **Why it matters:** Without clearly assigned roles, agents duplicate each other's work, drop the ball, and no one is fully accountable.

### 1.1 Agent Role Taxonomy

Think of the picture below as the team's bulletin board with everyone's name tag on it, grouped into 4 friendly floors: **Coordination** (the planners), **Execution** (the builders), **Quality** (the checkers), and **Support** (the helpers). Read it like a small company org chart — the top floor steers, the lower floors build and double-check each other. No mystery about "who does what" anymore.

```
┌──────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ROLE TAXONOMY                      │
│                                                                  │
│  COORDINATION LAYER                                              │
│  ├── Orchestrator     → Overall orchestration, routing tasks     │
│  ├── Planner          → Analyze, decompose, plan                │
│  └── Supervisor       → Monitor progress, quality gates         │
│                                                                  │
│  EXECUTION LAYER                                                 │
│  ├── Coder            → Write code to spec                      │
│  ├── Architect        → Design the system, choose patterns      │
│  ├── Refactorer       → Improve code quality                    │
│  └── Integrator       → Integrate modules and APIs              │
│                                                                  │
│  QUALITY LAYER                                                   │
│  ├── Code Reviewer    → Assess code quality                     │
│  ├── Tester           → Write & run tests                       │
│  ├── Security Auditor → Check for vulnerabilities               │
│  └── Performance Analyst → Analyze & optimize performance       │
│                                                                  │
│  SUPPORT LAYER                                                   │
│  ├── Debugger         → Find & fix bugs                         │
│  ├── Doc Writer       → Write documentation                     │
│  ├── DevOps           → CI/CD, deployment, monitoring           │
│  └── Git Manager      → Branching, commits, PRs                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Detailed Agent Definitions

The big code card below is basically a stack of employee badges: each role gets its **own pep-talk instructions** (system prompt), a **cap on how many clones can run at once**, a rough **token appetite**, and the **toolbox** it may touch. Yes, it looks long — but just read each badge as "who is this, and what may they touch?" That clarity keeps everyone happily inside their own lane.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-2-detailed-agent-definitions.py`](examples/01-1-2-detailed-agent-definitions.py)

</details>

---

## 2. Communication Patterns

> **📌 Core Concept**
>
> - **Concept:** Communication Patterns are the information-exchange structures between agents — sequential passing, parallel fan-out, via a message bus... — plus a standard message protocol so data is transmitted reliably and stays in sync.
> - **Analogy/comparison:** Like a company: a few people pass documents down an assembly line (pipeline), or everyone reads from the same shared notice board (blackboard).
> - **Why it matters:** If agents don't communicate to a standard ⟶ information gets lost, agents work on stale data and produce wrong results.

### 2.1 Communication Patterns Overview

Think of this section as six ways friends can keep in touch: passing notes down a line (pipeline), splitting chores and regrouping (fan-out), scribbling on the same fridge whiteboard (blackboard), chatting back and forth (request-reply), letting a team lead hand out jobs (hierarchical), or shouting into a group chat channel (pub/sub). Each style has its shiny ✓ upsides and its honest ✗ trade-offs — a pipeline feels like an assembly line, a blackboard feels like the office fridge door. Pick the vibe that fits your job.
```
┌──────────────────────────────────────────────────────────────────┐
│              AGENT COMMUNICATION PATTERNS                         │
│                                                                  │
│  PATTERN 1: SEQUENTIAL PIPELINE                                  │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │Agent A │──►│Agent B │──►│Agent C │──►│Agent D │            │
│  │Planner │   │Coder   │   │Reviewer│   │Tester  │            │
│  └────────┘   └────────┘   └────────┘   └────────┘            │
│  Output of A → Input of B → Output of C → Input of D           │
│  ✓ Simple, predictable  ✗ Slow (no parallelism)                │
│                                                                  │
│  PATTERN 2: FAN-OUT / FAN-IN                                    │
│                    ┌────────┐                                   │
│               ┌───►│Agent A │───┐                              │
│  ┌────────┐  │    └────────┘   │    ┌────────┐                │
│  │Router  │──┤    ┌────────┐   ├───►│Merger  │                │
│  └────────┘  ├───►│Agent B │──┤    └────────┘                │
│               │    └────────┘   │                               │
│               └───►│Agent C │──┘                               │
│                    └────────┘                                   │
│  ✓ Parallel execution  ✓ Throughput  ✗ Merge conflicts          │
│                                                                  │
│  PATTERN 3: BLACKBOARD (Shared State)                            │
│  ┌─────────────────────────────────────┐                       │
│  │           BLACKBOARD                │                       │
│  │  ┌─────────────────────────────┐   │                       │
│  │  │  Shared State / Knowledge   │   │                       │
│  │  └─────────────────────────────┘   │                       │
│  └──────┬──────┬──────┬──────┬────────┘                       │
│         │      │      │      │                                  │
│    ┌────┴─┐┌───┴──┐┌──┴───┐┌─┴─────┐                         │
│    │Agent ││Agent ││Agent ││Agent  │                          │
│    │  A   ││  B   ││  C   ││  D    │                          │
│    └──────┘└──────┘└──────┘└───────┘                          │
│  Agents read/write shared state independently                    │
│  ✓ Decoupled  ✓ Flexible  ✗ Race conditions, consistency       │
│                                                                  │
│  PATTERN 4: REQUEST-REPLY (Conversation)                        │
│  ┌────────┐         ┌────────┐                                  │
│  │Agent A │◄───────►│Agent B │                                  │
│  └────────┘ Request │        │                                  │
│       │   ┌────────►└────────┘                                  │
│       │   │    Reply                                            │
│       ▼   ▼                                                     │
│  Multi-turn conversation until consensus                        │
│  ✓ Negotiation  ✓ Rich  ✗ Token-heavy, can loop                │
│                                                                  │
│  PATTERN 5: HIERARCHICAL (Manager → Workers)                    │
│  ┌──────────────┐                                               │
│  │   Manager    │                                               │
│  │   Agent      │                                               │
│  └──┬───┬───┬──┘                                               │
│     │   │   │                                                   │
│  ┌──┴┐┌─┴─┐┌┴──┐                                               │
│  │W1 ││W2 ││W3 │   Workers process sub-tasks in parallel       │
│  └───┘└───┘└───┘                                               │
│  ✓ Scalable  ✓ Clear authority  ✗ Single point of failure       │
│                                                                  │
│  PATTERN 6: EVENT-DRIVEN (Pub/Sub)                              │
│  ┌────────┐  event   ┌──────────────────┐  event   ┌────────┐ │
│  │Agent A │─────────►│  Event Bus       │─────────►│Agent B │ │
│  └────────┘          │  (pub/sub)       │          └────────┘ │
│                       │  ┌────────────┐ │                       │
│                       │  │ subscribers│ │                       │
│                       │  └────────────┘ │                       │
│                       └──────────────────┘                       │
│  ✓ Decoupled  ✓ Scalable  ✗ Hard to debug, eventual consistency │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Message Protocol

Think of the snippet below as designing the perfect inter-office envelope: every letter carries **who sent it, who should read it, what kind of news it is** (new job, job done, quick question…), plus the **letter itself** (payload), a timestamp, a priority sticker, and an expiry date. The `MessageRouter` is our cheerful post office — it collects, sorts into pigeonholes, and shouts across the room when everyone needs to hear. Without a shared envelope, it would be like one friend handwriting cursive while the other only reads spreadsheets — lost in translation.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-2-2-message-protocol.py`](examples/02-2-2-message-protocol.py)

</details>

---

## 3. Orchestration Strategies

> **📌 Core Concept**
>
> - **Concept:** Orchestration Strategies are the way a multi-agent workflow is organized — running sequentially, in parallel, in a manager/worker hierarchy, or by discussion until a decision is reached — deciding which agent starts, how they coordinate, and how results are synthesized.
> - **Analogy/comparison:** Like a film director: shoot scenes one at a time in sequence (sequential), let multiple crews shoot in parallel (parallel), or have the on-set manager delegate the work (hierarchical).
> - **Why it matters:** Picking the wrong strategy ⟶ the whole system runs slowly, burns tokens, or produces inconsistent results.

### 3.1 Strategy Comparison

A table comparing 6 orchestration strategies, with columns for **when to use** and the **pros/cons** of each type. How to read it: identify the characteristics of your task (independent? dependent? needs debate?) and find the matching row. The metaphor: like choosing how to organize work — clearly defined work gets a sequential assembly line, independent work gets split among several people at once.

```
┌──────────────────────────────────────────────────────────────────┐
│              ORCHESTRATION STRATEGIES                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ STRATEGY        │ WHEN TO USE         │ PROS/CONS       │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Sequential      │ Simple workflows    │ ✓ Predictable   │    │
│  │ Pipeline        │ Clear dependencies  │ ✗ No parallel   │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Parallel        │ Independent tasks   │ ✓ Fast          │    │
│  │ Fan-out         │ No dependencies     │ ✗ Merge issues  │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Hierarchical    │ Complex projects    │ ✓ Scalable      │    │
│  │ (Manager/Worker)│ Need coordination   │ ✗ Bottleneck    │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Blackboard      │ Research/creative   │ ✓ Flexible      │    │
│  │ (Shared state)  │ Emergent solutions  │ ✗ Race cond.    │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Negotiation     │ Design decisions    │ ✓ Rich dialogue │    │
│  │ (Conversation)  │ Need consensus      │ ✗ Token-heavy   │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Event-driven    │ Loosely coupled     │ ✓ Decoupled     │    │
│  │ (Pub/Sub)       │ Scalable systems    │ ✗ Hard to trace │    │
│  └─────────────────┴─────────────────────┴─────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Orchestrator Implementation

Meet the team's kind project manager in code form: it **lines up your to-do list by who-waits-for-whom**, **walks each chore to the right specialist**, **gives it another try when it stumbles**, and keeps an eye on the token piggy bank. The little `_resolve_execution_order` helper is the auto-scheduler scribbling "you first, you next" on the whiteboard. In short: schedule, delegate, check off, repeat.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-3-2-orchestrator-implementation.py`](examples/03-3-2-orchestrator-implementation.py)

</details>

---

## 4. Shared Memory

> **📌 Core Concept**
>
> - **Concept:** Shared Memory is a centralized data store that many agents read/write together — project context, task queue, finalized decisions — so agents can share understanding without retransmitting all the information.
> - **Analogy/comparison:** Like the whiteboard in a meeting room: everyone can see it and add to it, instead of each person keeping a private notebook and reading it aloud to the others.
> - **Why it matters:** Without shared memory, each agent "remembers things differently" ⟶ they work on stale context and the results are inconsistent.

### 4.1 Memory Architecture

Picture two cozy memory corners: the big **Global Memory** whiteboard in the middle of the room (project notes, the to-do queue, shared facts, the "why did we decide that?" diary) plus each agent's own **Agent Memory** journal (private thoughts + scratch paper). Rule of thumb: if everyone needs it, pin it on the board; if it is just your doodles, keep it in your drawer — just like a real office with a shared wall and private notebooks.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT SHARED MEMORY                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   GLOBAL MEMORY                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Project Context (codebase, config, docs)         │   │   │
│  │  │ Task Queue (pending, in-progress, done)          │   │   │
│  │  │ Shared State (variables, results, artifacts)     │   │   │
│  │  │ Decision Log (choices made and reasoning)        │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Agent Memory │ │ Agent Memory │ │ Agent Memory │              │
│  │   Agent A    │ │   Agent B    │ │   Agent C    │              │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │              │
│  │ │Private  │ │ │ │Private  │ │ │ │Private  │ │              │
│  │ │Context  │ │ │ │Context  │ │ │ │Context  │ │              │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │              │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │              │
│  │ │Working  │ │ │ │Working  │ │ │ │Working  │ │              │
│  │ │Memory   │ │ │ │Memory   │ │ │ │Memory   │ │              │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Shared Memory Manager

This snippet builds that shared whiteboard with bumpers on: many hands can reach for it at once, but a gentle `Lock` makes sure nobody scribbles over anyone mid-sentence. Alongside the board it keeps a treasure chest of **artifacts** (files, test results) and a diary of "who changed what." Think bank vault: one person inside at a time, every visit written in the ledger.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-4-2-shared-memory-manager.py`](examples/04-4-2-shared-memory-manager.py)

</details>

---

## 5. Conflict Resolution

> **📌 Core Concept**
>
> - **Concept:** Conflict Resolution is the mechanism for handling disagreements between agents — two agents editing the same file, opposing viewpoints, resource contention — by classifying the conflict and applying a controlled reconciliation strategy.
> - **Analogy/comparison:** Like two coworkers editing the same report: the risk of overwriting each other. With rules about "who locks the file, who gets the final call", neither person's work gets broken.
> - **Why it matters:** Without a conflict resolution mechanism, agents can overwrite and "break" each other's results.

### 5.1 Conflict Types & Resolution

Think of the chart below as the team's traffic-light handbook for its 5 classic fender-benders: editing the same file, disagreeing on approach, fighting over the same tool, reading stale notes, or shouting different answers. Spot which bump you just hit, then follow the ready-made "what to do" lane beside it — just like drivers who instantly know who yields at a crossing once they know the rules.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT CONFLICT RESOLUTION                      │
│                                                                  │
│  CONFLICT TYPE 1: CODE CONFLICT                                  │
│  Agent A and Agent B are editing the same file                   │
│  → SOLUTION: File locking + merge strategy                       │
│    - Last-write-wins (simple but risky)                          │
│    - Three-way merge (safe)                                      │
│    - Agent negotiation (discuss changes)                         │
│                                                                  │
│  CONFLICT TYPE 2: APPROACH CONFLICT                              │
│  Agent A and Agent B disagree on approach                        │
│  → SOLUTION: Debate protocol                                     │
│    - Each agent presents rationale (max 3 points)               │
│    - Orchestrator evaluates evidence                             │
│    - Majority vote or authority decision                         │
│                                                                  │
│  CONFLICT TYPE 3: RESOURCE CONFLICT                              │
│  Multiple agents need same tool/API at same time                 │
│  → SOLUTION: Resource scheduling                                 │
│    - Priority-based access                                       │
│    - Time-sliced access                                          │
│    - Queue with fair scheduling                                  │
│                                                                  │
│  CONFLICT TYPE 4: STATE CONFLICT                                 │
│  Agents read inconsistent shared state                            │
│  → SOLUTION: Consistency protocol                                │
│    - Optimistic locking (retry on conflict)                     │
│    - Pessimistic locking (acquire lock first)                   │
│    - Event sourcing (replay from events)                        │
│                                                                  │
│  CONFLICT TYPE 5: OUTPUT CONFLICT                                │
│  Multiple agents produce contradictory results                    │
│  → SOLUTION: Validation protocol                                 │
│    - Cross-validation (agent B validates agent A)               │
│    - Authority agent has final say                               │
│    - Quality metrics decide                                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Conflict Resolution Manager

Think of this snippet as the team's friendly referee with a whistle: it hands out file locks ("one writer at a time, please!"), scores competing ideas when two agents disagree, and writes every call in the match log. The `_score_approach` helper is the scorecard — the clearer the reasoning (a good "because…", an honest "trade-off…", a proud "we tested…"), the more points it earns. May the clearest argument win!

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-5-2-conflict-resolution-manager.py`](examples/05-5-2-conflict-resolution-manager.py)

</details>

---

## 6. Agent Selection Guide

> **📌 Core Concept**
>
> - **Concept:** The Agent Selection Guide is a set of criteria for deciding when to use multi-agent and when a single agent is enough, based on task complexity, token cost, and specialization requirements.
> - **Analogy/comparison:** Like choosing transportation: walk for short distances (single-agent), hire a team only for far-and-many jobs (multi-agent). Driving 100 meters just to save effort is a pointless expense.
> - **Why it matters:** Using multi-agent for a simple task only wastes tokens and adds slowness — the guide helps you avoid over-engineering.

### 6.1 When to Use Multi-Agent

Treat the flowchart below like a "which exit should I take?" road-trip quiz. Start with your task up top, answer each friendly yes/no question (can one friend handle it alone? are the chores independent? is there an obvious assembly line? do we need a good debate? lots of sub-jobs?), and each "Yes!" parks you at the right architecture. The little price table at the bottom shows the token toll for each route.

```
┌──────────────────────────────────────────────────────────────────┐
│           MULTI-AGENT DECISION GUIDE                              │
│                                                                  │
│  Task arrives                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Single agent can │──────────►│ USE SINGLE AGENT  │           │
│  │ handle it?       │          │ (simpler, cheaper) │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Tasks are        │──────────►│ PARALLEL FAN-OUT  │           │
│  │ independent?     │          │ (max throughput)   │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Clear pipeline?  │──────────►│ SEQUENTIAL        │           │
│  │ (Plan→Code→Test) │          │ PIPELINE          │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Need multi-turn  │──────────►│ NEGOTIATION       │           │
│  │ discussion?      │          │ PATTERN           │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Complex, many    │──────────►│ HIERARCHICAL      │           │
│  │ sub-tasks?       │          │ (Manager/Workers)  │           │
│  └──────────────────┘          └──────────────────┘           │
│                                                                  │
│  COST COMPARISON:                                                │
│  • Single agent:     ~5K-20K tokens per task                    │
│  • 2 agents:         ~10K-40K tokens (2x base)                 │
│  • Pipeline:         ~15K-60K tokens (3x base)                 │
│  • Hierarchical:     ~20K-80K tokens (4x base)                 │
│  • But: Quality may improve 20-40% with specialist agents      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Real-World Implementations

> **📌 Core Concept**
>
> - **Concept:** Real-World Implementations are multi-agent examples applied in production — a code review pipeline, a feature development team, a debug squad — showing how roles are assigned and communication flows set up concretely.
> - **Analogy/comparison:** Like watching a software company's actual workflow: who reviews, who writes code, who tests — instead of just reading dry theory.
> - **Why it matters:** Real examples give you a battle-tested design to "copy" and adapt, so you don't have to fumble your way from scratch.

### 7.1 Code Review Pipeline

This snippet sets up the review line just like a real software team does: gather the changed files → read the code → invite security → invite performance → gather all the notes into one kind letter. To "read" it, just follow the `depends_on` tags — they whisper "wait for me first." It feels exactly like a merge request where two or three teammates must hit Approve before the big green merge button.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-7-1-code-review-pipeline.py`](examples/06-7-1-code-review-pipeline.py)

</details>

### 7.2 Feature Development Team

Welcome to the feature dream team, organized **family-style** with a lead at the top: the Architect sketches the blueprints first → two Coders build different rooms at the same time → the Tester checks every door and window → the Reviewer does the final walkthrough. Notice the cute detail: `implement-core` and `implement-api` both wait for `design`, but not for each other — so they happily hammer away side by side. Just like real builders: the electrician and the plumber work in parallel, but both wait for the same blueprint.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-7-2-feature-development-team.py`](examples/07-7-2-feature-development-team.py)

</details>

### 7.3 Debug Squad

Think of this snippet as speed-dialing your 4-person rescue squad in order: the Debugger plays detective and finds the culprit → the Coder patches it up → the Tester makes sure nothing else broke → the Reviewer gives the warm thumbs-up. The `depends_on` chain holds hands tightly so nobody runs ahead — catch, patch, verify, approve. Just like a real on-call rotation: support spots it, engineering fixes it, QA confirms it, the lead signs it off.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-7-3-debug-squad.py`](examples/08-7-3-debug-squad.py)

</details>

---

## 8. Debugging Multi-Agent Systems

> **📌 Core Concept**
>
> - **Concept:** Debugging Multi-Agent Systems is the process of tracing fault causes in a system of interacting agents — communication errors, out-of-sync state, conflicting results — using logging, tracing, and isolating individual components.
> - **Analogy/comparison:** Like finding a leak in a multi-story building: you must inspect each pipe (message log), each floor (agent state), and each timer (timeline) instead of just guessing.
> - **Why it matters:** Multi-agent faults rarely sit inside one agent — they usually live "between" agents, so dedicated tracing tools are needed.

### 8.1 Debug Strategy

Keep this diagram taped to the garage wall like a mechanic's cheat sheet. For each familiar groan — an agent gone quiet, a job sent to the wrong teammate, a loop that never ends, two answers that clash, work that feels sloppy — it lists gentle "have you checked…?" steps and then the "here is the fix" remedy. Match your symptom, walk the checklist, cross suspects off one by one — out of gas? loose spark plug? — until the engine hums again.

```
┌──────────────────────────────────────────────────────────────────┐
│          DEBUGGING MULTI-AGENT SYSTEMS                            │
│                                                                  │
│  SYMPTOM 1: Agent not responding                                 │
│  ├── Check: Message queue empty?                                 │
│  ├── Check: Agent registered with router?                        │
│  ├── Check: Token budget exhausted?                              │
│  └── Fix: Restart agent, check message format                    │
│                                                                  │
│  SYMPTOM 2: Wrong agent handling task                            │
│  ├── Check: Task type → role mapping correct?                    │
│  ├── Check: Agent role definition matches?                       │
│  └── Fix: Update routing logic, verify role assignments          │
│                                                                  │
│  SYMPTOM 3: Infinite loop between agents                         │
│  ├── Check: Circular dependencies in pipeline?                   │
│  ├── Check: Negotiation without convergence?                     │
│  ├── Check: Missing termination condition?                       │
│  └── Fix: Add max iterations, timeout, convergence check         │
│                                                                  │
│  SYMPTOM 4: Conflicting outputs                                  │
│  ├── Check: Shared state consistency?                            │
│  ├── Check: File lock contention?                                │
│  └── Fix: Add conflict resolution, merge strategy                │
│                                                                  │
│  SYMPTOM 5: Poor quality output                                  │
│  ├── Check: System prompts clear enough?                         │
│  ├── Check: Context passed between agents complete?              │
│  ├── Check: Right agent for the task?                            │
│  └── Fix: Improve prompts, add validation step                   │
│                                                                  │
│  DEBUGGING TOOLS:                                                │
│  • Message log analysis (trace message flow)                     │
│  • Agent state inspection (what each agent knows)                │
│  • Execution timeline (what happened when)                       │
│  • Token usage per agent (identify bottlenecks)                  │
│  • Conflict report (what conflicts occurred)                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Debug Logger

This code is the "replay the game footage" toolkit for multi-agent: `trace_message_flow` replays every message between agents over time, `inspect_agent_state` shows what a single agent currently knows, and `generate_timeline` reconstructs the sequence of events. When the system misbehaves, this is where you see "who said what, did what, when". The metaphor: like checking the security camera to find out who bumped into whom.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-8-2-debug-logger.py`](examples/09-8-2-debug-logger.py)

</details>

---

## 9. Performance Optimization

> **📌 Core Concept**
>
> - **Concept:** Performance Optimization is the set of techniques that reduce latency and cost for a multi-agent system — more parallelism, fewer redundant messages, caching, token estimation — so the system responds faster and costs less.
> - **Analogy/comparison:** Like optimizing a factory: cut unnecessary middle stages, let independent production lines run in parallel instead of one after another.
> - **Why it matters:** Multi-agent already costs 2-5× the tokens — without optimization, operating costs climb very quickly.

### 9.1 Optimization Strategies

A list of 5 optimization strategies for multi-agent systems: reduce tokens, maximize parallelism, reduce communication, keep the team just big enough, and cache for reuse. Each strategy is a "practical trick" you can apply right away, without any complex tooling. The metaphor: like cleaning out a warehouse — remove the excess (tokens), arrange things so people can work in parallel, and keep frequently used items where they're easy to grab (cache).

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT PERFORMANCE OPTIMIZATION                      │
│                                                                  │
│  1. REDUCE TOKEN USAGE                                           │
│     • Pass summaries between agents, not full context            │
│     • Use structured messages (JSON), not prose                  │
│     • Cache common context (project structure, conventions)      │
│     • Limit agent memory to relevant information                 │
│                                                                  │
│  2. MAXIMIZE PARALLELISM                                         │
│     • Identify independent tasks early                           │
│     • Fan-out independent work to multiple agents                │
│     • Use async message passing                                  │
│     • Don't serialize what can be parallel                       │
│                                                                  │
│  3. MINIMIZE COMMUNICATION                                       │
│     • Batch messages instead of many small ones                  │
│     • Use shared memory for frequently accessed data             │
│     • Define clear interfaces between agents                     │
│     • Avoid unnecessary back-and-forth                            │
│                                                                  │
│  4. RIGHT-SIZE AGENTS                                            │
│     • Don't over-specialize (too many agents = overhead)         │
│     • Match agent capability to task complexity                  │
│     • Use single agent for simple tasks                          │
│     • Reserve multi-agent for genuinely complex work             │
│                                                                  │
│  5. CACHE AND REUSE                                              │
│     • Cache file reads across agents                             │
│     • Reuse analysis results                                     │
│     • Share test fixtures                                        │
│     • Persist decisions (don't re-derive)                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Cost Estimation

A "token budget" estimation table for multi-agent: cost = cost per agent × number of agents × communication cost. It prices out each role (orchestrator ~2K, coder ~5K tokens...), adds the "post office fee" (messages, handoffs, conflicts), then gives you typical scenarios. The metaphor: like estimating a project's cost — once you know the price of each line item, you can predict the total spend.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT COST ESTIMATION                          │
│                                                                  │
│  Cost = Base Agent Cost × Number of Agents × Communication      │
│                                                                  │
│  Base Cost per Agent (avg tokens per task):                      │
│  ├── Orchestrator:  2,000 tokens (planning + routing)           │
│  ├── Coder:         5,000 tokens (reading + writing code)       │
│  ├── Reviewer:      3,000 tokens (reading + feedback)           │
│  ├── Tester:        4,000 tokens (writing + running tests)      │
│  ├── Debugger:      4,000 tokens (investigating + fixing)       │
│  └── DevOps:        3,000 tokens (config + deployment)          │
│                                                                  │
│  Communication Overhead:                                         │
│  ├── Message passing:  200-500 tokens per message               │
│  ├── Context transfer: 1,000-3,000 tokens per handoff           │
│  └── Conflict resolution: 1,000-2,000 tokens per conflict       │
│                                                                  │
│  Typical Scenarios:                                              │
│  ├── Simple feature (1 agent):     5,000 tokens                 │
│  ├── Code review (2 agents):       8,000 tokens                 │
│  ├── Feature dev (3 agents):      20,000 tokens                 │
│  ├── Complex project (5 agents):  50,000 tokens                 │
│  └── Full team (7 agents):        80,000 tokens                 │
│                                                                  │
│  ROI Consideration:                                              │
│  • Multi-agent costs 2-5x more in tokens                         │
│  • But may produce 20-40% better quality                         │
│  • Best ROI: Code review, security audit, testing                │
│  • Worst ROI: Simple tasks, documentation                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Anti-Patterns & Solutions

> **📌 Core Concept**
>
> - **Concept:** Anti-Patterns & Solutions is a collection of common design mistakes in multi-agent systems — overlapping roles, agents that "chat" too much, single points of dependency — together with how to avoid and fix them.
> - **Analogy/comparison:** Like a distilled "don'ts" list from experience: knowing the traps other people fall into means you won't repeat them.
> - **Why it matters:** Most multi-agent systems fail because of these anti-patterns, not because the model is weak.

### 10.1 Common Anti-Patterns

A list of 8 "traps" that almost everyone who builds multi-agent systems has stepped in — too many agents, agents talking too much, single points of dependency, unclear roles... — each trap comes with its solution right on the "→ SOLUTION" line. How to use it: check your project against each trap, and if you hit one, apply the fix. The metaphor: like a "check before confirming the order" list — knowing where things go wrong beats patching things later.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT ANTI-PATTERNS                                 │
│                                                                  │
│  ❌ ANTI-PATTERN 1: OVER-ENGINEERING                             │
│     Using 5 agents for a task that needs 1                      │
│     → SOLUTION: Start with single agent, add only if needed     │
│                                                                  │
│  ❌ ANTI-PATTERN 2: CHATTY AGENTS                                │
│     Agents exchange 20+ messages for simple coordination         │
│     → SOLUTION: Batch communication, use shared memory          │
│                                                                  │
│  ❌ ANTI-PATTERN 3: SINGLE POINT OF FAILURE                      │
│     All agents depend on one orchestrator                        │
│     → SOLUTION: Add fallback routing, health checks             │
│                                                                  │
│  ❌ ANTI-PATTERN 4: UNCLEAR RESPONSIBILITIES                     │
│     Multiple agents try to do the same thing                    │
│     → SOLUTION: Strict role definitions, task routing           │
│                                                                  │
│  ❌ ANTI-PATTERN 5: NO CONFLICT RESOLUTION                       │
│     Agents modify same file, corrupt each other's work          │
│     → SOLUTION: File locking, conflict resolution manager       │
│                                                                  │
│  ❌ ANTI-PATTERN 6: TOKEN BOMB                                   │
│     Communication overhead exceeds task execution cost          │
│     → SOLUTION: Monitor token ratio, simplify messages          │
│                                                                  │
│  ❌ ANTI-PATTERN 7: INFINITE NEGOTIATION                         │
│     Agents debate forever without reaching consensus            │
│     → SOLUTION: Max rounds limit, authority fallback            │
│                                                                  │
│  ❌ ANTI-PATTERN 8: LOST CONTEXT                                 │
│     Agent B doesn't know what Agent A decided                   │
│     → SOLUTION: Shared decision log, context handoff protocol   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 11. Production Deployment

> **📌 Core Concept**
>
> - **Concept:** Production Deployment is the process of putting a multi-agent system into real operation — ensuring readiness, monitoring, security, and scalability — with a checklist to run before going live.
> - **Analogy/comparison:** Like putting a building into use: before opening, you must check the electrical and water systems, fire alarms, and who does what when something fails — you can't just hand over the keys and start living there.
> - **Why it matters:** A system that works fine in the lab can fall over the moment it hits production without monitoring and failure-handling procedures.

### 11.1 Deployment Checklist

This checklist splits into 3 phases before a multi-agent system goes to production: **preparation** (clear roles, tested routing, conflict handling, token limits...), **monitoring** (tokens, latency, conflicts...) and **continuous optimization**. How to use it: check each box; any box that stays unchecked means the system is not yet ready to run for real. The metaphor: like the pre-flight checklist — missing one small item can lead to a big incident.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT PRODUCTION CHECKLIST                          │
│                                                                  │
│  BEFORE DEPLOYMENT:                                              │
│  □ All agents have clear role definitions                        │
│  □ Message routing is tested                                     │
│  □ Conflict resolution is implemented                            │
│  □ Token budget limits are set                                   │
│  □ Error handling and retry logic in place                       │
│  □ Logging and monitoring configured                             │
│  □ Cost estimation reviewed                                      │
│                                                                  │
│  MONITORING:                                                     │
│  □ Token usage per agent (track anomalies)                       │
│  □ Message latency (detect bottlenecks)                          │
│  □ Conflict frequency (identify problematic pairs)               │
│  □ Task completion rate (measure effectiveness)                  │
│  □ Error rates per agent (find weak links)                       │
│                                                                  │
│  OPTIMIZATION:                                                   │
│  □ Review token usage weekly                                     │
│  □ Identify unnecessary agent communication                      │
│  □ Cache frequently accessed context                              │
│  □ Right-size team (remove underperforming agents)               │
│  □ Update prompts based on failure analysis                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

> **📌 Core Concept**
>
> - **Concept:** Best Practices are the foundational principles distilled from building multi-agent systems — start simple, keep roles clear, communicate in a structured way, design defensively, and track cost.
> - **Analogy/comparison:** Like a veteran team's code of conduct — they know what makes a project succeed because they've stumbled a great many times.
> - **Why it matters:** Applying them from the start costs far less than repairing a system after it has grown big.

```
┌──────────────────────────────────────────────────────────────────┐
│           MULTI-AGENT BEST PRACTICES                              │
│                                                                  │
│  1. START SIMPLE                                                 │
│     Single agent first → add agents only when needed            │
│     Each new agent must justify its overhead                     │
│                                                                  │
│  2. CLEAR ROLES                                                  │
│     Every agent has ONE primary responsibility                   │
│     Document what each agent does and doesn't do                │
│                                                                  │
│  3. STRUCTURED COMMUNICATION                                     │
│     Use standard message format (not free-form)                  │
│     Pass summaries, not raw data between agents                  │
│                                                                  │
│  4. EXPLICIT HANDOFFS                                            │
│     Clear contract: what sender provides, receiver expects      │
│     Validate inputs before processing                            │
│                                                                  │
│  5. DEFENSIVE DESIGN                                             │
│     Handle agent failures gracefully                             │
│     Never assume another agent's output is correct              │
│                                                                  │
│  6. MONITOR TOKEN COST                                           │
│     Track tokens per agent, per task                             │
│     Set budgets, alert on overruns                               │
│                                                                  │
│  7. LOG EVERYTHING                                               │
│     Message flow, decisions, conflicts                           │
│     Enables debugging and optimization                           │
│                                                                  │
│  8. TEST THE SYSTEM                                              │
│     Unit test individual agents                                  │
│     Integration test agent interactions                          │
│     Chaos test agent failures                                    │
│                                                                  │
│  9. ITERATE AND IMPROVE                                          │
│     Review failure cases regularly                               │
│     Tune prompts based on output quality                         │
│     Add/remove agents based on actual needs                      │
│                                                                  │
│  10. KNOW WHEN NOT TO                                           │
│      Multi-agent is NOT always better                            │
│      Simple tasks → single agent                                 │
│      Complex coordination → multi-agent                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 12. Case Studies — Real-World Multi-Agent Architectures

> **📌 Core Concept**
>
> - **Concept:** Case Studies are analyses of the multi-agent architectures of famous real systems — Claude Code, Devin, OpenHands — to extract lessons on role design, workflows, and how to pick an architecture.
> - **Analogy/comparison:** Like studying the tactical diagrams of top football teams before building your own lineup.
> - **Why it matters:** Learning from systems that already run in production means you don't have to "reinvent the wheel".

### 12.1 Claude Code — Anthropic's Multi-Agent Architecture

Claude Code uses a complex multi-agent pattern with planner, coder, and reviewer agents that coordinate through shared context.

```
┌──────────────────────────────────────────────────────────────────┐
│         CLAUDE CODE MULTI-AGENT ARCHITECTURE                      │
│                                                                  │
│  User Request                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────┐                                            │
│  │  PLANNER AGENT   │  Analyzes task, creates plan              │
│  │  (Claude 3.5)    │  Outputs: ordered subtask list            │
│  └────────┬─────────┘  Max tokens: ~2K                          │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  CODING AGENT    │  Executes each subtask                    │
│  │  (Claude 3.5)    │  Tools: read_file, write_to_file          │
│  │                  │  Tool: search_files, execute_command       │
│  │  ┌────────────┐  │  Iterates until task complete             │
│  │  │ Edit Loop  │  │  Max iterations: 20-50                    │
│  │  │ Read→Edit  │  │  Token budget: ~100K per task             │
│  │  │ →Verify    │  │                                           │
│  │  └────────────┘  │                                           │
│  └────────┬─────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  REVIEW AGENT    │  Validates output quality                 │
│  │  (Same model)    │  Checks: correctness, style, safety       │
│  │                  │  Can reject and send back for fix          │
│  └────────┬─────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  COORDINATOR     │  Manages state, handles errors            │
│  │  (System code)   │  Tracks progress, manages context         │
│  │                  │  Handles tool permissions & safety         │
│  └──────────────────┘                                            │
│                                                                  │
│  Key Insight: Multiple agents share SAME model but              │
│  different system prompts → different behaviors                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.2 Devin — Autonomous Software Engineering Agent

Devin (Cognition AI) uses a multi-agent pattern with specialized modules:

```
┌──────────────────────────────────────────────────────────────────┐
│              DEVIN AGENT ARCHITECTURE                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CORE BRAIN (LLM)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │ Planning   │  │ Reasoning  │  │ Reflection │         │   │
│  │  │ Module     │  │ Module     │  │ Module     │         │   │
│  │  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘         │   │
│  └─────────┼───────────────┼───────────────┼────────────────┘   │
│            │               │               │                     │
│  ┌─────────▼───────────────▼───────────────▼────────────────┐   │
│  │                 TOOL USE LAYER                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │ Code     │ │ Browser  │ │ Terminal │ │ Planner  │   │   │
│  │  │ Editor   │ │          │ │          │ │          │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 ENVIRONMENT (Sandbox)                     │   │
│  │  Full VM with: codebase, browser, terminal               │   │
│  │  Agent has full autonomy to read, write, test, deploy    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.3 OpenHands (OpenDevin) — Open-Source Multi-Agent

This code simulates the OpenHands/Devin-style architecture: a **central brain (LLM)** decides actions in a **observe → decide → act → observe again** loop (visible in `run_agent_loop`), living in a safe **sandbox** and automatically retrying on errors. How to read it: focus on the `run_agent_loop` function — that is the heart of the whole pattern. The metaphor: like a chess player who looks at the board between moves, evaluating the result before each next move.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-12-3-openhands-opendevin-open-source-multi-agent.py`](examples/10-12-3-openhands-opendevin-open-source-multi-agent.py)

</details>

---

## 13. Advanced Multi-Agent Patterns

> **📌 Core Concept**
>
> - **Concept:** Advanced Multi-Agent Patterns are refined architectural patterns — MapReduce, Debate, Critique-Revision, Ensemble — that use multiple agents in parallel to push quality far beyond what a single agent can achieve.
> - **Analogy/comparison:** Like organizing a competition round: give several people the same job and pick the best entry (ensemble), or have them critique each other before settling on an approach (debate).
> - **Why it matters:** This is the family of patterns that reduces hallucination and increases reliability when quality is the top priority.

### 13.1 MapReduce Pattern for Code Generation

MapReduce is the "divide and conquer" pattern: **MAP** splits a big task into independent sub-tasks that multiple agents process in parallel, and **REDUCE** merges the results into a final output. In the code, `parallel_code_generation` is an example of generating code for many modules at once and then merging them. How to read it: if your task splits into independent parts — map-reduce fits; if the parts depend on each other — it does not. The metaphor: like cooking a feast — many chefs cook many dishes in parallel, then everything lands on the same table.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/11-13-1-mapreduce-pattern-for-code-generation.py`](examples/11-13-1-mapreduce-pattern-for-code-generation.py)

</details>

### 13.2 Debate Pattern — Multi-Agent Discussion

The debate pattern lets multiple agents "argue" their way to a more reliable decision: round 1 each agent states its position, round 2 they rebut the opponents, round 3 they wrap up, and then a **judge agent** scores who was most persuasive. How to read it: `_judge_decision` scores based on the number of arguments and content length — a simple simulation of the principle that "a good argument wins". The metaphor: like a review committee before approving a loan — listen to all sides, then decide.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/12-13-2-debate-pattern-multi-agent-discussion.py`](examples/12-13-2-debate-pattern-multi-agent-discussion.py)

</details>

### 13.3 Critique-Revision Pattern

This pattern simulates the exact "write - grade - fix" loop: the **Writer** writes code, the **Critic** gives feedback, the **Writer** revises based on it, repeating until quality reaches the threshold (`quality_threshold`) or the rounds run out. How to read it: the `iterate` loop is the learn-from-feedback mechanism — whichever round scores higher is the one that gets kept. The metaphor: like submitting a draft to an editor for feedback and revising it — a few rounds produce a better result than the first raw draft.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/13-13-3-critique-revision-pattern.py`](examples/13-13-3-critique-revision-pattern.py)

</details>

### 13.4 Ensemble Pattern — Multiple Agents, Best Output

The ensemble pattern runs **multiple agents on the same task at the same time**, each producing its own result; a judge scores them all and picks the best output. It is like "ensembles" in machine learning — combining many different opinions to reduce risk. How to read it: note `_generate_recommendation` — if the agents agree (low variance), the result is trustworthy; if they strongly disagree, a closer review is needed. The metaphor: like drafting several versions before finalizing the last one — take the one done best.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/14-13-4-ensemble-pattern-multiple-agents-best-output.py`](examples/14-13-4-ensemble-pattern-multiple-agents-best-output.py)

</details>

---

## 14. Multi-Agent Testing Strategies

> **📌 Core Concept**
>
> - **Concept:** Multi-Agent Testing Strategies are the methods for verifying a multi-agent system — routing tests, message tests, per-agent tests, interaction tests, chaos tests — to make sure the system behaves correctly and stays stable.
> - **Analogy/comparison:** Like testing a production line: test each machine (agent), test the whole line, even deliberately break one machine to see if the system stops.
> - **Why it matters:** Multi-agent systems often have "no individual fault but a systemic fault" — you need to test at several different levels.

### 14.1 Testing Multi-Agent Systems

This triangle shows that multi-agent testing happens at **many levels**, bottom-up: routing tests (does the task go to the right agent?), message tests (is the protocol standard?), per-agent tests, interaction tests between agents, and finally **chaos tests** — deliberately killing an agent to see if the system survives. How to read it: the lower levels are the foundation; do them well before moving up. The metaphor: like inspecting a building — check each brick, then test the whole structure before subjecting it to an earthquake.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT TESTING PYRAMID                               │
│                                                                  │
│                        ┌──────────┐                              │
│                        │  Chaos   │  ← Kill agents mid-task     │
│                        │  Tests   │  ← Corrupt shared state     │
│                       ┌┴──────────┴┐                            │
│                       │ Integration │  ← Agent interactions     │
│                       │    Tests    │  ← Full pipeline runs     │
│                      ┌┴─────────────┴┐                         │
│                      │  Agent Tests   │  ← Individual agent     │
│                      │  (Unit equiv.) │  ← with mock tools      │
│                     ┌┴───────────────┴┐                        │
│                     │  Message Tests   │  ← Protocol correctness│
│                     │  (Contract)      │  ← Format validation   │
│                    ┌┴─────────────────┴┐                       │
│                    │  Routing Tests     │  ← Task → Agent mapping│
│                    │  (Logic)           │  ← Edge cases          │
│                    └───────────────────┘                        │
│                                                                  │
│  Each level tests different aspects:                             │
│  - Routing: Does the right agent get the right task?             │
│  - Messages: Are messages formatted correctly?                   │
│  - Agents: Does each agent produce quality output?               │
│  - Integration: Do agents work together?                         │
│  - Chaos: Does the system survive failures?                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 14.2 Test Implementation

This code comes with ready-made example tests: `test_routing_accuracy` checks whether tasks land on the correct agent, `test_agent_failure_recovery` "kills" one agent to see if the system keeps running, `test_token_budget_enforcement` checks the token limit, `test_conflict_resolution` checks file locking and reconciliation. How to use it: you can extend this very test suite for your own system. The metaphor: like the driving-test questions before you're allowed on the road — if any item FAILs, you're not ready yet.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/15-14-2-test-implementation.py`](examples/15-14-2-test-implementation.py)

</details>

---

## 15. Cost-Benefit Analysis

> **📌 Core Concept**
>
> - **Concept:** Cost-Benefit Analysis is a comparison between the extra token cost of multi-agent and the quality improvement, so you know when multi-agent is actually worth it versus single-agent.
> - **Analogy/comparison:** Like weighing whether to hire a specialist team: it costs more, but if product quality improves enough, it's still a profit.
> - **Why it matters:** Multi-agent isn't always better — this analysis helps you spend money where it pays off.

### 15.1 When Multi-Agent Is Worth It

A "worth it or not" decision table per task type: comparing single vs multi fit, the quality improvement percentage, the cost multiplier, and the final verdict (SINGLE / MULTI / DEPENDS). How to read it: look at the `Cost` and `Quality` columns — tasks where quality improves a lot while cost only rises a little are good multi-agent candidates. The metaphor: like an outsourcing decision table — do simple work yourself, hire a specialist for hard work.

```
┌────────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT COST-BENEFIT ANALYSIS                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Task Type          │ Single │ Multi │ Quality │ Cost │ Verdict   │
│  ───────────────────┼────────┼───────┼─────────┼──────┼──────────│
│  Simple bug fix     │  ★★★★★ │ ★★☆☆☆ │ +10%    │ 3×   │ SINGLE   │
│  Code review        │  ★★★☆☆ │ ★★★★★ │ +35%    │ 2×   │ MULTI ✓  │
│  Feature dev        │  ★★★☆☆ │ ★★★★☆ │ +25%    │ 3×   │ MULTI ✓  │
│  Security audit     │  ★★☆☆☆ │ ★★★★★ │ +40%    │ 2×   │ MULTI ✓  │
│  Refactoring        │  ★★★☆☆ │ ★★★★☆ │ +20%    │ 3×   │ DEPENDS  │
│  Documentation      │  ★★★★★ │ ★★☆☆☆ │ +5%     │ 4×   │ SINGLE   │
│  Complex debugging  │  ★★☆☆☆ │ ★★★★★ │ +45%    │ 3×   │ MULTI ✓  │
│  Performance tuning │  ★★★☆☆ │ ★★★★☆ │ +30%    │ 2×   │ MULTI ✓  │
│  Multi-file refactor│  ★★☆☆☆ │ ★★★★★ │ +35%    │ 3×   │ MULTI ✓  │
│                                                                    │
│  ROI Formula:                                                      │
│  ROI = (Quality Improvement × Business Value) /                   │
│        (Additional Token Cost + Overhead)                          │
│                                                                    │
│  Break-even: When quality improvement > 20% AND task complexity   │
│  warrants specialization (code review, security, testing)         │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 15.2 Token Cost Comparison

This code writes a Python ROI calculator for multi-agent: each `CostEstimate` holds the single vs multi token counts plus the quality improvement percentage, from which it automatically computes `cost_ratio`, `roi`, and issues a `RECOMMEND` / `CONSIDER` / `AVOID` recommendation. How to run it: the final `print()` section prints a comparison table for each task type. The metaphor: like a pocket calculator for spending decisions — put in the numbers and it tells you right away whether it's a good idea.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-15-2-token-cost-comparison.py`](examples/16-15-2-token-cost-comparison.py)

</details>

---

## 16. Fault Tolerance, Messaging & Isolation

At production scale agents crash, hang, double-write, and leak secrets. This section adds the missing hardening: failure detection + reassignment, explicit messaging guarantees, memory consistency rules, and per-agent sandboxing. Analogy: like a kitchen crew — if a chef collapses someone takes over his ticket (reassignment), orders have sequence numbers (ordering), only one chef plates a dish (write conflicts), and cleaners can't enter the safe (secret containment).

### 16.1 Fault Tolerance — Crash / Timeout / Hang Detection

```
HEARTBEAT: every 5s agent → supervisor {agent_id, task_id, state}
TIMEOUT RULES:
 • crash = heartbeat missing > 15s → mark DEAD
 • timeout = task exceeds deadline (e.g. 300s) → mark TIMED_OUT
 • hang = heartbeat alive but no progress log > 60s → SUSPECT
REASSIGNMENT:
 1. freeze task lease (fencing token++) → old agent writes rejected
 2. requeue task with attempt++ and prior transcript attached
 3. if attempts > 3 → escalate to human / fail closed
QUORUM (judges/voters): 2f+1 agents tolerate f faults; require majority (e.g. 2/3)
```

Rules: every task has `lease_id + deadline + max_attempts`; supervisor is stateless + backed by queue (Redis/BullMQ); prefer idempotent workers so reassignment is safe to retry.

### 16.2 Messaging Guarantees — Ordering, Delivery, Payload Caps

| Guarantee | Default choice | Rule |
|---|---|---|
| Ordering | Per-task FIFO (sequence no.) | Orchestrator rejects out-of-order `seq`; agents buffer + request resend |
| Delivery | At-least-once + idempotency keys | Every message has `msg_id`; handler dedups on `msg_id` |
| At-most-once | Only for non-retryable side effects (send email, push) — gate via outbox + fencing token | Never retry without guard |
| Payload caps | 64 KB headers + 512 KB body; larger → artifact ref (path + hash) | Drop + log oversized messages |
| Timeouts | Request/reply 30s default; streaming progress 5s heartbeat | Missing reply → retry with backoff, then reassign (§16.1) |

### 16.3 Memory Consistency — Shared vs Private, Write Conflicts

- **Private by default:** each agent has scratchpad; only publishes diffs/facts to shared blackboard.
- **Shared via versioned keys:** `blackboard.write(key, value, expectedVersion)` — CAS semantics; on version mismatch re-read + merge, never blind-overwrite.
- **Single-writer per artifact:** orchestrator assigns file/section ownership (e.g. only `coder` writes `auth.ts`); reviewers emit comments, not edits.
- **Per-agent isolation:** namespace keys `agent_id/task_id/*`; cross-agent reads go through allow-listed projections (no raw prompt/secret bleed).

### 16.4 Per-Agent Sandboxing + Secret Containment

The **isolation mechanism** — isolation tiers, the five mandatory controls, the hardened
runner, and the per-role policy matrix — is owned by
[`12-sandbox-execution`](../12-sandbox-execution/README.md) §2–§6. This section only adds the
two things that are specific to *a team* of agents rather than to a single run:

- **Least-privilege tools per role, resolved through the role matrix.** `reviewer` gets
  read-only FS + no shell; `coder` gets a sandboxed shell with no net. Rather than restating
  the grants, look them up: `12` §6's per-role policy matrix is keyed by role name, so
  multi-agent and single-agent runs resolve the *same* policy for the *same* role. A `reviewer`
  that can shell out in a swarm but not in a solo run is a privilege-escalation bug.
- **Secrets are per-agent leases, never per-message.** Agents receive short-lived scoped tokens
  (5–15 min) via env injection, and the supervisor redacts `sk-*, ghp_*, AWS_*` from logs and
  transcripts before they are written. Secret *containment* inside the sandbox is `12` §3.5;
  the multi-agent-specific part is that a secret handed to one agent must never appear in
  another agent's context through a shared blackboard projection.
- **Egress policy: deny-by-default, allow-list domains per agent.** All tool I/O is audited with
  `agent_id + lease_id`, which is what makes the redaction above auditable — a leaked token in
  the shared blackboard is traceable to exactly one lease.

<details>
<summary>TypeScript Code — Heartbeat + Reassignment (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/17-16-4-per-agent-sandboxing-secret-containment.ts`](examples/17-16-4-per-agent-sandboxing-secret-containment.ts)

</details>

### 16.5 Checklist + Real-World Example

**Checklist:** [ ] heartbeat + deadline + stall detector wired [ ] fencing token on requeue [ ] max_attempts + escalate path [ ] per-task FIFO + `msg_id` dedup [ ] payload caps + artifact refs [ ] CAS writes + single-writer ownership [ ] per-role tool allow-list + scoped short-lived secrets + redaction.

**Real-world:** Claude Code subagents run isolated with bounded tool grants; on subagent stall the orchestrator kills the process, bumps the task lease, and respawns with condensed transcript — reviewers vote 2-of-3 (quorum) so one crashed voter never blocks merge.

**File Reference**: For the full sub-agent spec (lifecycle, spawn contract, roles, budget, testing), see [`SUBAGENT.md`](SUBAGENT.md)

---

## References

### Frameworks
- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — LangChain multi-agent orchestration
- [CrewAI Framework](https://docs.crewai.com/) — Role-based multi-agent framework
- [AutoGen by Microsoft](https://microsoft.github.io/autogen/) — Multi-agent conversation framework
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) — Open-source AI coding agent (formerly OpenDevin)
- [Swarm by OpenAI](https://github.com/openai/swarm) — Lightweight multi-agent orchestration

### Research & Papers
- [Multi-Agent Systems - MIT](https://ocw.mit.edu/courses/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/) — MIT course on MAS
- [Blackboard Architecture Pattern](https://wwwPatterns.com/catalog/patterns/view/Blackboard) — Classic coordination pattern
- [Actor Model - Erlang/OTP](https://www.erlang.org/doc/design_principles/actors) — Message-passing concurrency model
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) — Reasoning + Action in LLMs
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) — Tool use in language models

### Production Systems
- [Devin by Cognition AI](https://www.cognition.ai/) — Autonomous software engineer
- [Claude Code by Anthropic](https://docs.anthropic.com/en/docs/claude-code) — CLI coding agent
- [GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace) — Multi-agent dev environment
- [Cursor Agent Mode](https://cursor.sh/) — AI-first code editor with agent capabilities

### Architecture Patterns
- [Saga Pattern](https://microservices.io/patterns/data/saga.html) — Distributed transactions
- [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cQRS) — Command Query Responsibility Segregation
- [Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — State via events

## 17. October 2026 Update — Multi-Agent Production Research (Anthropic, A2A)

> **📌 Core Concepts**
>
> - **Concept:** A synthesis of the latest production findings (10/2026) on multi-agent from Anthropic Research and the A2A (Agent-to-Agent) protocol from the Linux Foundation — when multi-agent is worth the cost, how to prompt the orchestrator, and how agents "shake hands" through an open standard.
> - **Analogy:** Anthropic Research is like a film studio with a director (LeadResearcher) and many parallel film crews (subagents); A2A is like a "shared labor contract" that lets companies (different frameworks) hire work from each other without opening their internal books.
> - **Why it matters:** This is real production data (not lab benchmarks) — it tells you exactly how expensive multi-agent is (15× tokens), how effective it is (+90.2%), and when you should NOT use it.

### 17.1 Production results (Anthropic Research, 06/2025)

Anthropic's "How we built our multi-agent research system" report is one of the few sources with **real production numbers** (not synthetic benchmarks). The figures below directly answer "is multi-agent worth it?" — and just as important: "when should you NOT use it?".

| Metric | Value | Meaning |
|---|---|---|
| Orchestrator-worker performance | **+90.2%** vs single-agent Opus 4 | On the internal research eval, the Opus lead + Sonnet subagents architecture clearly outperforms |
| Token usage | Explains **80% of performance variance** | On BrowseComp, token consumption is the #1 predictor of outcomes |
| 3 factors explain 95% | Token usage + tool call count + model choice | No other mystery factors remain — optimize all 3 |
| Token economics | Chat 1× · Single agent ≈ 4× · Multi-agent ≈ **15×** | Multi-agent costs ~4× more than a single agent — it must be worth it |

**When to use / not use multi-agent:**

| ✓ Good fit | ✗ Poor fit |
|---|---|
| High-value tasks (token spend justified) | Coding (not truly parallelizable) |
| Truly parallelizable (splittable into independent subtasks) | Tasks needing tight shared context across steps |
| Exceeding a single context window | Real-time coordination (low latency) |
| Many complex tools, multi-domain | Simple tasks — 1 agent is enough |

**Research feature architecture (end-to-end flow):**

```
LeadResearcher (Opus)
   │
   ├─ 1. Phân tích query, LƯU PLAN vào Memory (bền vững, không mất khi context dài)
   │
   ├─ 2. Spawn subagents — mỗi subagent nhận 4 thứ:
   │       objective + output format + tool guidance + task boundaries
   │
   ├─ 3. Subagents dùng interleaved thinking SAU MỖI tool result
   │      (không chỉ "nghĩ rồi làm" một lần đầu)
   │
   ├─ 4. Lead synthesize kết quả từ các subagent
   │
   └─ 5. CitationAgent xử lý citations riêng (tách khỏi luồng nghiên cứu)
```

### 17.2 A2A Protocol (Linux Foundation, 2026)

A2A (Agent-to-Agent Protocol) is an open standard for **agent talking to agent** — it complements MCP (agent talking to tools), it does not compete with it.

| | MCP | A2A |
|---|---|---|
| Scope | agent → tool | agent → agent |
| Model | Agent calls tools/data within its own system | Agent delegates to + receives results from another agent |
| Relationship | Complementary — not competitors | |

**Core points of A2A:**
- Agents built with **different frameworks/vendors** (LangGraph, CrewAI, ADK, custom) can still **discover + delegate + share results** with each other
- Each agent does **NOT expose internal memory/tools/logic** — communication happens through standard interfaces, opaque and secure (the other side doesn't need to know how you implement it)

**Governance status (08/2026):** A2A has joined the **Agentic AI Foundation** (Linux Foundation). Technical Steering Committee: AWS, Cisco, Google, IBM, Microsoft, Salesforce, SAP, ServiceNow.

**Official SDKs:** Python, JS, Java, .NET, Go, Rust — plus the **A2A CLI** (released 10/2026).

**A2A is NOT:**
- ❌ A development kit (it does not replace agent-building frameworks)
- ❌ A sub-agent protocol (sub-agents within one system use native primitives / MCP — no A2A needed)
- ❌ A replacement for MCP (the two solve two different problems)

### 17.3 8 prompting principles for multi-agent

Drawn from Anthropic's own production Research system — 8 rules that keep the orchestrator's command of subagents from descending into chaos:

1. **Think like your agents** — simulate each step in your head to surface real failure modes (not the ones you imagine, but the ones a real subagent will hit).
2. **Teach the orchestrator how to delegate** — every subtask needs all 4 components: `objective` + `output format` + `tool guidance` + `task boundaries`. Vague instructions → subagents duplicate work or miss coverage.
3. **Scale effort to query complexity** — not every query needs 10 subagents:

   | Query type | Appropriate effort |
   |---|---|
   | Simple fact-finding | 1 agent, 3–10 tool calls |
   | Comparison | 2–4 subagents, 10–15 calls each |
   | Complex research | 10+ subagents |

4. **Tool design critical** — heuristic: examine all tools first, match tool to intent, prefer specialized over generic.
5. **Let agents improve themselves** — a dedicated "tool-testing" agent rewrites tool descriptions → **40% decrease in task completion time**.
6. **Start wide, then narrow down** — guards against over-long, over-specific early queries (like searching Google: broad first, refine later).
7. **Guide thinking** — extended thinking for the lead, interleaved thinking after each tool result for subagents.
8. **Parallel tool calling** — 3–5 subagents in parallel + 3+ tools in parallel per subagent → up to **90% research time reduction**.

### 17.4 Sub-agent output via filesystem

Reduces the **"game of telephone"** effect (information getting distorted through multiple hand-offs): instead of the subagent copying its full output through the conversation history, the subagent **writes results to a filesystem/artifact store**, then returns **lightweight references** (path + hash). The orchestrator reads files when it needs detail — it doesn't have to keep full output in its own context.

> Analogy: instead of each employee reading a 50-page report aloud in the meeting, they send a file link — anyone who needs the details opens it themselves.

### 17.5 Sync vs Async

Anthropic runs subagents **synchronously** — simple, easy to debug, but with a bottleneck: the lead **cannot steer a subagent mid-run** (it must wait for the subagent to finish before responding). Async allows higher parallelism but trades for complexity in result coordination, state consistency, and error propagation.

| Mode | Pros | Cons |
|---|---|---|
| **Sync** (Anthropic's choice) | Simple, deterministic, easy to debug | Bottleneck — lead cannot steer mid-run |
| **Async** | Higher parallelism | Complex: result coordination + state consistency + error propagation |

**Illustrative code — Orchestrator-Worker with effort-scaling rules:**

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-17-5-sync-vs-async.py`](examples/18-17-5-sync-vs-async.py)

</details>

> Cross-link: see also [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — Section 3.5 (Orchestration) and 4.2/4.4 (production patterns).
