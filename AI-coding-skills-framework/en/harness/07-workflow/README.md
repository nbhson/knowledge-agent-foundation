# ⚙️ VII. Workflow

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Workflow Patterns](#1-workflow-patterns)
>   - [1.1 Sequential Workflow (In Order)](#11-sequential-workflow-in-order)
>   - [1.2 Parallel Workflow (Concurrent)](#12-parallel-workflow-concurrent)
>   - [1.3 DAG Workflow (Directed Acyclic Graph)](#13-dag-workflow-directed-acyclic-graph)
>   - [1.4 Event-Driven Workflow](#14-event-driven-workflow)
> - [2. Pipeline Design](#2-pipeline-design)
>   - [2.1 Data Pipeline with Branching](#21-data-pipeline-with-branching)
> - [3. State Machine](#3-state-machine)
>   - [3.1 Hierarchical State Machine](#31-hierarchical-state-machine)
> - [4. Error Recovery](#4-error-recovery)
>   - [4.1 Retry Strategies](#41-retry-strategies)
>   - [4.2 Circuit Breaker Pattern](#42-circuit-breaker-pattern)
>   - [4.3 Saga Pattern](#43-saga-pattern)
> - [5. Observability](#5-observability)
>   - [5.1 Distributed Tracing](#51-distributed-tracing)
>   - [5.2 Structured Logging + Metrics](#52-structured-logging--metrics)
> - [6. Workflow Orchestration Engine](#6-workflow-orchestration-engine)
> - [7. Workflow Testing](#7-workflow-testing)
> - [8. Harness Integration](#8-harness-integration)
>   - [8.1 TypeScript Interfaces](#81-typescript-interfaces)
> - [9. Case Studies](#9-case-studies)
>   - [9.1. GitHub Actions — Event-Driven CI/CD](#91-github-actions--event-driven-cicd)
>   - [9.2. Apache Airflow — Data Pipeline Orchestration](#92-apache-airflow--data-pipeline-orchestration)
>   - [9.3. Temporal — Durable Workflow Execution](#93-temporal--durable-workflow-execution)
> - [10. Design Principles](#10-design-principles)
>   - [10.1 SOLID for Workflows](#101-solid-for-workflows)
>   - [10.2 6 Design Principles](#102-6-design-principles)
> - [11. Best Practices](#11-best-practices)
>   - [11.1 DO ✅](#111-do-)
>   - [11.2 DON'T ❌](#112-dont-)
> - [12. Future](#12-future)
>   - [12.1 Trends 2026-2028](#121-trends-2026-2028)
> - [References](#references)
>   - [Papers & Research](#papers-&-research)
>   - [Frameworks](#frameworks)
>
---

### Opening Story

Picture an **car factory** on a busy Monday morning. Every car rolls through hundreds of small stations: frame assembly → engine mounting → painting → quality inspection → packaging. Now imagine there is **no shared checklist** — everyone just does what feels right that day. You can guess the ending: missing bolts, streaky paint, skipped inspections.

**An AI Agent is exactly the same when it lacks a Workflow.**

Many of us start out building agents the same way: just **one function call after another** — no saved state, no plan for errors, no checkpoints along the way. That is fine for a tiny demo. But on a real, multi-step job, **one small failure means starting all over again from zero**.

**The friendly fix**: a Structured Workflow — think of it as a caring tour guide for your task. It walks with the job through its **whole journey**, from the starting trigger to the final feedback, and at every stop it can **pick up after a fall, save your place, and show you what is happening**.

> **One-line summary:** A workflow is the shared checklist for a multi-step agent job — it saves progress after each step and has a plan for errors, so one failure does not throw away all the work.

### Why Is a Workflow Important?

> *"An agent without a workflow is like a chef without a recipe — you have the ingredients, you have the tools, but the dish comes out by whim."*

#### 3 Scientific Pieces of Evidence

| # | Research | Key Finding |
|---|----------|-------------|
| 1 | **Google DeepMind (2025)** | Structured workflows reduce the **45% task failure rate** in multi-step coding agents |
| 2 | **Anthropic (2025)** | Workflow engines with retry + checkpoint reduce **data loss by 70%** when agents hit errors |
| 3 | **LangGraph Benchmark (2025)** | State machine workflows handle **3× complex tasks** better than simple sequential chains |

How to read the table: each row is one study. Column **Research** = who measured it and when. Column **Key Finding** = the number they found; for instance, row 2 means adding retry (try again) + checkpoint (save progress) cut lost work by 70%.

#### Core philosophy:

```
Workflow = Trigger → Plan → Execute → Validate → Deploy → Feedback
```

Every step must have **state management**, **error recovery**, and **observability**. A workflow is not just "an order of steps" — it is a system that manages the **entire lifecycle** of a task.

**Analogies**: A workflow is like a transportation system — traffic lights (guardrails), routes (steps), a control center (orchestrator), and surveillance cameras (logging).

**If you skip it**: Agents execute tasks messily, cannot recover from errors, cannot track progress, and debugging becomes a nightmare.

> **One-line summary:** A workflow is the full lifecycle manager for a task — steps in order, state saved, errors recovered, everything logged — not just a list of steps.

## Overview

> **📌 Core Concept**
>
> - **Concept:** A workflow is how the execution steps of an AI Agent are arranged into a clear plan — which step comes first, which comes next, how errors are handled — so that a complex task is completed in the right order and safely.
> - **Analogy:** Like a restaurant kitchen: a chef (agent) with good ingredients still needs a recipe and a service routine (workflow) to deliver dishes on time, at the right quality, every time.
> - **Why it matters:** Without a workflow, an agent works on instinct — slow, hard to reproduce results, and any mid-way failure means starting over from scratch.

**Workflow** is simply the art of **laying out the steps** that finish a tricky coding job. Inside Harness Engineering, the Workflow Engine is the friendly **"dispatch center"** — it waves each job through from trigger → plan → execute → validate → deploy, while keeping an eye on everything (observability), catching falls (error recovery), and remembering where everyone is (state).

This section explains the whole toolbox: the shapes a workflow can take, how to recover from errors, how to watch it run, and how it plugs into the rest of the Harness.

```
┌──────────────────────────────────────────────────────────────────┐
│                         WORKFLOW ENGINE                           │
│                                                                  │
│  Trigger (Event/Schedule/Webhook)                                │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  WORKFLOW ORCHESTRATOR                                     │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  State   │  │  Task    │  │  Guard   │  │  Retry   │  │  │
│  │  │  Machine │  │  Queue   │  │  Rails   │  │  Engine  │  │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │  │
│  │       └──────────────┼──────────────┼──────────────┘        │  │
│  │                      ▼                                       │  │
│  │  ┌──────────────────────────────────────────────────┐      │  │
│  │  │              EXECUTION ENGINE                     │      │  │
│  │  │  Sequential | Parallel | DAG | Conditional       │      │  │
│  │  └──────────────────────┬───────────────────────────┘      │  │
│  │                         │                                    │  │
│  │  ┌──────────────────────┼───────────────────────────┐      │  │
│  │  │        OBSERVABILITY & RECOVERY                   │      │  │
│  │  │  Tracing | Metrics | Circuit Breaker | Saga      │      │  │
│  │  └──────────────────────────────────────────────────┘      │  │
│  └────────────────────────────────────────────────────────────┘  │
│       │                                                          │
│       ▼                                                          │
│  Result + Logs + Metrics + Artifacts                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Memory ←→ Guardrails ←→ Feedback ←→ Observability       │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

How to read the diagram: follow the arrows from top to bottom. A **trigger** (event, schedule, or webhook = a call from outside) starts the job. The **orchestrator** (dispatcher) routes it through four helpers: State Machine (where the job is now), Task Queue (waiting line), Guard Rails (safety rules), Retry Engine (try again logic). The Execution Engine picks the run shape (in order, side by side, or DAG), and Observability & Recovery watches and heals. The Harness Integration row shows how this module connects to the other Harness modules.

> **One-line summary:** The Workflow Engine = dispatcher + state + queue + guardrails + retry + execution + observability, all wrapped so a task goes from trigger to result without getting lost.

## Contents

| # | Topic | Description |
|---|-------|-------------|
| 1 | [Workflow Patterns](#1-workflow-patterns) | Sequential, Parallel, DAG, Event-driven |
| 2 | [Pipeline Design](#2-pipeline-design) | Transform, Branching, Fan-out/Fan-in |
| 3 | [State Machine](#3-state-machine) | Advanced FSM, hierarchical states |
| 4 | [Error Recovery](#4-error-recovery) | Retry, Circuit Breaker, Saga pattern |
| 5 | [Observability](#5-observability) | Structured logging, distributed tracing |
| 6 | [Workflow Orchestration](#6-workflow-orchestration-engine) | Integrated engine |
| 7 | [Workflow Testing](#7-workflow-testing) | Unit, integration, chaos testing |
| 8 | [Harness Integration](#8-harness-integration) | TypeScript interfaces |
| 9 | [Case Studies](#9-case-studies) | GitHub Actions, Airflow, Temporal |
| 10 | [Design Principles](#10-design-principles) | SOLID for workflows |
| 11 | [Best Practices](#11-best-practices) | Detailed DO/DON'Ts |
| 12 | [Future](#12-future) | Trends 2026-2028 |

How to read the table: each row is one section of this document. Column **Topic** = the section name (click to jump). Column **Description** = what you will learn there; for instance, row 4 covers the three tools for surviving errors: retry (try again), circuit breaker (cut the power when a service keeps failing), and saga (undo finished steps).

> **One-line summary:** Twelve sections take you from run shapes and error recovery to a real engine, testing, production durability, and future trends.

---

## 1. Workflow Patterns

> **📌 Core Concept**
>
> - **Concept:** Workflow patterns are the "molds" that organize an AI Agent's chain of activities — run in order (sequential), run at the same time (parallel), or branch on conditions (conditional branching) — to reach the task objective in a controlled way.
> - **Analogy:** Like roads in a city: a straight road (sequential), many lanes running at the same time (parallel), or an intersection that diverts traffic according to signs (conditional branching).
> - **Why it matters:** Choosing the right pattern determines the speed, complexity, and fault tolerance of the entire workflow.

> **One-line summary:** Pick a run shape — in order, side by side, dependency-based, or reaction-based — and everything downstream (speed, debugging, failure handling) follows from that choice.

### 1.1 Sequential Workflow (In Order)

Think of following a favorite home recipe: you finish step 1 before touching step 2 — no skipping, no shuffling. That is the whole idea here, and it is the simplest pattern to learn: easy to write, easy to debug, just a little slow because every step patiently waits in line. Reach for it when a later step truly needs what the earlier step made. The little map below shows the classic 5-stop trip Parse → Analyze → Build → Test → Deploy:

```
┌──────────────────────────────────────────────────────────────────┐
│                   SEQUENTIAL WORKFLOW                             │
│                                                                  │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐     │
│  │Step 1│───►│Step 2│───►│Step 3│───►│Step 4│───►│Step 5│     │
│  │Parse │    │Analyze│   │Build │    │Test  │    │Deploy│     │
│  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘     │
│                                                                  │
│  Each step runs only AFTER the previous step completes          │
│  → Simple, easy to debug, but slow                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-1-sequential-workflow-in-order.py`](examples/01-1-1-sequential-workflow-in-order.py)

</details>

> **One-line summary:** Sequential = one step at a time, each waiting for the previous one — the simplest and safest shape, best when step 2 truly needs step 1's output.

### 1.2 Parallel Workflow (Concurrent)

Think of cooking a big family dinner with friends helping out: while you wash the vegetables, someone else cooks the rice and another friend fries the main dish — then you all meet back at the table to serve. That teamwork is why this pattern feels fast: lots of things happen at once. The tricky part is the reunion at the end (fan-in), where you gather every dish together. Use it when the jobs do not really need each other to finish first. Two words to keep straight: **fan-out** = split one input into many tasks running at once; **fan-in** = merge all their results back into one output:

```
┌──────────────────────────────────────────────────────────────────┐
│                    PARALLEL WORKFLOW (Concurrent)                  │
│                                                                  │
│                        ┌──────────┐                              │
│                        │  Input   │                              │
│                        └────┬─────┘                              │
│                             │                                    │
│                             ▼                                    │
│                  ┌─────────────────────┐                         │
│                  │   Fan-Out (split)   │                         │
│                  └───┬────┬────┬────┬──┘                         │
│                      │    │    │    │                            │
│                      ▼    ▼    ▼    ▼                            │
│              ┌──────┐┌──────┐┌──────┐┌──────┐                    │
│              │Task A││Task B││Task C││Task D│                    │
│              │Parse ││Analyze││Build ││Test  │                    │
│              └──────┘└──────┘└──────┘└──────┘                    │
│                      │    │    │    │                            │
│                      ▼    ▼    ▼    ▼                            │
│                  ┌─────────────────────┐                         │
│                  │   Fan-In (merge)    │                         │
│                  └─────────┬───────────┘                         │
│                            │                                     │
│                            ▼                                     │
│                        ┌──────────┐                              │
│                        │  Output  │                              │
│                        └──────────┘                              │
│                                                                  │
│  Many steps run AT THE SAME TIME, waiting for all to complete  │
│  → Fast, but complex when merging results                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-1-2-parallel-workflow-concurrent.py`](examples/02-1-2-parallel-workflow-concurrent.py)

</details>

> **One-line summary:** Parallel = fan out many tasks at once, fan in the results — much faster, but you must handle the merge (fan-in) carefully.

### 1.3 DAG Workflow (Directed Acyclic Graph)

Think of a weekend sports bracket: the semifinal cannot start until both quarterfinal games are done, but those two quarterfinals happily run side by side. A DAG works just like that — it is the most flexible playbook. Each small job runs as soon as the jobs it depends on are finished, level by level, and the rules simply say "no going in circles." In the sketch below, A and B play at the same time → C waits for A, D waits for B → E waits for C, F waits for D. Plain words: **DAG (directed acyclic graph)** = a diagram of tasks with arrows meaning "must finish before", and **acyclic** = no arrow ever loops back, so circular waiting is impossible:

```
┌──────────────────────────────────────────────────────────────────┐
│                    DAG WORKFLOW (Directed Acyclic Graph)          │
│                                                                  │
│   Level 1          Level 2          Level 3                      │
│                                                                  │
│   ┌──────┐         ┌──────┐         ┌──────┐                     │
│   │Node A│────────►│Node C│────────►│Node E│                     │
│   └──────┘         └──────┘         └──────┘                     │
│                                                                  │
│   ┌──────┐         ┌──────┐         ┌──────┐                     │
│   │Node B│────────►│Node D│────────►│Node F│                     │
│   └──────┘         └──────┘         └──────┘                     │
│                                                                  │
│   A, B run in parallel → C waits for A, D waits for B          │
│   → E waits for C, F waits for D                                │
│   → Dependency-optimized, no loops (acyclic)                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-1-3-dag-workflow-directed-acyclic-graph.py`](examples/03-1-3-dag-workflow-directed-acyclic-graph.py)

</details>

> **One-line summary:** DAG = tasks with "finish before" arrows and no loops — each task starts the moment its dependencies are done, giving maximum parallelism with correct order.

### 1.4 Event-Driven Workflow

Think of a friendly neighborhood fire station: wherever the bell rings (that is your event), the crew on duty (the handler) rolls out — and what they find there can ring the next bell. Unlike the tidy step-by-step recipes above, you do not plan every turn in advance here. The workflow simply listens and reacts as things happen, which makes it a lovely fit for busy, unpredictable real life. Plain words: an **event** = something that just happened ("a commit was pushed", "a file changed"), and a **handler** = the function that reacts to it:

```
┌──────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN WORKFLOW                          │
│                                                                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                 │
│   │  Event   │────►│  Event   │────►│  Event   │                 │
│   │  A       │     │  B       │     │  C       │                 │
│   └────┬─────┘     └────┬─────┘     └────┬─────┘                 │
│        │                │                │                       │
│        ▼                ▼                ▼                       │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                 │
│   │ Handler  │     │ Handler  │     │ Handler  │                 │
│   │  1       │     │  2       │     │  3       │                 │
│   └──────────┘     └──────────┘     └──────────┘                 │
│                                                                  │
│   The workflow reacts to events; a handler may spawn a         │
│   new event → a flexible chain of reactions, no need to        │
│   predefine the order                                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-1-4-event-driven-workflow.py`](examples/04-1-4-event-driven-workflow.py)

</details>

> **One-line summary:** Event-driven = react when something happens, no fixed script — flexible and lifelike, but harder to trace because the order of reactions is not written down in advance.

---

## 2. Pipeline Design

> **📌 Core Concept**
>
> - **Concept:** Pipeline design is how to split a large task into successive stages; each stage receives data from the previous stage, processes it, and passes it on, with branching and fan-out/fan-in capabilities.
> - **Analogy:** Like a beer factory line: mash → boil → filter → ferment → bottle; each step takes the output of the previous step, with a fork if the customer orders a different kind of beer.
> - **Why it matters:** Pipelines keep large data processing tidy, let you inspect every stage, and are easy to update when the business changes.

> **One-line summary:** A pipeline chops one big task into stages on a conveyor belt — each stage takes the previous stage's output, and the whole flow stays easy to inspect and change.

### 2.1 Data Pipeline with Branching

Think of this as the friendly assembly line for your data: every station has one clear job (transform, filter, branch, fan_out, validator, sink), and your data rides the belt from one station to the next, just like a parcel in a post office. The fun twist is branching — at one station you peek at the parcel and flip a switch that sends it left or right, like a railway junction. The code sample right below shows how you snap those stations together and press "go" on the whole line. Plain words: **transform** = change the data's shape, **filter** = drop rows you do not need, **validator** = check the data is good enough to continue, and **sink** = the final stop where results are written out:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-2-1-data-pipeline-with-branching.py`](examples/05-2-1-data-pipeline-with-branching.py)

</details>

> **One-line summary:** A branching pipeline = stations on a belt, plus switches that route each data parcel down different paths — one clear job per station keeps it debuggable.

---

## 3. State Machine

> **📌 Core Concept**
>
> - **Concept:** A state machine is a "state machine" — a model that records which state the agent is in (reading code, writing code, running tests) and only allows moving to the next state when certain conditions are met.
> - **Analogy:** Like a three-color traffic light: a car may only proceed on green, and the green → yellow → red sequence is always in order and never jumps straight from red to green.
> - **Why it matters:** It prevents the agent from jumping around between steps, keeping the execution flow always valid and predictable.

> **One-line summary:** A state machine only lets the agent move between agreed states (reading → writing → testing) when conditions are met — like a traffic light that never jumps from red to green.

### 3.1 Hierarchical State Machine

Think of this as the state machine all grown up: on top of the usual "if this, then go there" moves, it also understands parent-and-child rooms (hierarchical states), friendly bouncers at the door (guards that stop illegal moves), alarm clocks (automatic timeouts), and a cap on how many laps you can run. That makes it steady enough to chauffeur a whole AI coding agent. The code sample below is a little play where our agent walks the hallway IDLE → THINKING → PLANNING → READING_CODE → WRITING_CODE → RUNNING_TESTS → DONE. Plain words: **hierarchical** = a state can contain smaller states (like "WORKING" containing "READING_CODE"), a **guard** = a rule that blocks a forbidden move, and a **timeout** = a clock that force-moves the machine if a state takes too long:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-3-1-hierarchical-state-machine.py`](examples/06-3-1-hierarchical-state-machine.py)

</details>

> **One-line summary:** A hierarchical state machine adds states-within-states, guards, and timeouts on top of a plain state machine — strong enough to run a whole coding agent without illegal moves.

---

## 4. Error Recovery

> **📌 Core Concept**
>
> - **Concept:** Error recovery is the set of strategies for handling what happens when a workflow hits an error — retry with increasing waits (retry/backoff), fall back to an alternative, or cut the circuit as protection (circuit breaker) — so the system stays stable instead of the whole process crashing.
> - **Analogy:** Like making a phone call when the line is busy: try again after a minute (retry), if that fails wait longer (backoff), or dial a second person instead (fallback).
> - **Why it matters:** Errors will happen for sure; with a recovery strategy, the workflow doesn't just die midway.

> **One-line summary:** Errors are guaranteed — this section gives you the three tools to survive them: retry with growing waits, cut off a failing service, and undo finished steps.

### 4.1 Retry Strategies

We have all tapped "resend" when the wifi hiccups — this is that same instinct, just done with a little science. You wait a bit longer each time (1s → 2s → 4s) so you do not overwhelm the service, and you sprinkle in a touch of randomness (jitter) so a crowd of clients does not all stampede back at the exact same second. The tiny helper below wraps any function — sync or async — with that patient retry habit. Plain words: **exponential backoff** = double the wait after each failed try (1s, 2s, 4s, 8s), and **jitter** = a small random extra wait so thousands of clients do not retry at the same millisecond:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-4-1-retry-strategies.py`](examples/07-4-1-retry-strategies.py)

</details>

> **One-line summary:** Retry = try again with doubled waits plus random jitter — it fixes temporary glitches (bad wifi, rate limits) without hammering the service.

### 4.2 Circuit Breaker Pattern

Think of the fuse box in your home: when too much faulty current rushes in, the fuse pops and cuts the power to save the whole house. Our circuit breaker is that same caring fuse. When a service keeps stumbling past the limit, we flip from CLOSED (calls flowing normally) to OPEN (pause — stop calling for a while); after a short rest we peek through the door in HALF_OPEN to ask, "are you feeling better yet?" Plain words: **CLOSED** = breaker intact, calls pass through; **OPEN** = breaker tripped, all calls fail fast without hitting the sick service; **HALF_OPEN** = trial run — let one test call through, and only fully reopen if it succeeds:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-4-2-circuit-breaker-pattern.py`](examples/08-4-2-circuit-breaker-pattern.py)

</details>

> **One-line summary:** Circuit breaker = stop calling a failing service (OPEN), rest, then test it gently (HALF_OPEN) — it protects your workflow from a sick dependency.

### 4.3 Saga Pattern

Think of booking a group vacation: hotel booked, insurance paid — then the flights fall through. You do not just walk away; you kindly undo what already worked: refund the hotel, cancel the insurance. That undo-everything-neatly idea is the Saga. For jobs that stretch across many services, every step brings its own "sorry, let me undo that" companion step, so if any stop fails, the whole trip unwinds gracefully. Plain words: a **compensating action** = the pre-written undo for a finished step (charge → refund, reserve → release):

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-4-3-saga-pattern.py`](examples/09-4-3-saga-pattern.py)

</details>

> **One-line summary:** Saga = every step ships with its own undo step — when a mid-way step fails, run the undo steps in reverse to leave nothing half-done.

---

## 5. Observability

> **📌 Core Concept**
>
> - **Concept:** Observability is the ability to "see inside" a workflow through three kinds of data — logs (event records), metrics (measurements), and traces (the footprints of each request) — to know exactly what happened at each step.
> - **Analogy:** Like a taxi's dashcam + instrument cluster + GPS map: you know where the car is going, how fast or slow it's moving, and where it's stuck.
> - **Why it matters:** Without observability, when a workflow is slow or wrong you can't find the root cause and you have to debug step by step by feel.

> **One-line summary:** Observability = logs (what happened) + metrics (how much/how fast) + traces (the request's footprints) — the three views that turn "it's broken" into "here is the broken step".

> **Ownership note — two different layers, do not conflate them.** This section is
> **per-run instrumentation for one workflow**: a `trace_id` threaded through the steps of a
> single execution, spans with parent/child structure, a logger, and a metrics collector. That
> is the classic distributed-tracing toolkit and it is the right tool for "why was *this run*
> slow".
>
> The **cross-module event contract** — the append-only `TrajectoryEvent` stream that every
> harness module emits into and every debugging tool reads from, with join keys, fork/replay,
> retention, and redaction — is owned by
> [`13-trajectory-observability`](../13-trajectory-observability/README.md). A `trace_id` is
> not a `sessionId`, and a span is not a `TrajectoryEvent`; the two join on `runId`. If you are
> building the harness's spine, read `13`. If you are instrumenting one workflow, what follows
> is enough.

### 5.1 Distributed Tracing

Think of tucking a little travel diary onto every request: it gets a unique trace_id at the door, and every service it visits stamps the page (those stamps are called spans — parents and children). Later you can open the diary and replay the whole adventure, spotting exactly where it lingered or tripped. Plain words: **trace_id** = a unique ID stamped on one request's whole journey, and a **span** = one timed entry in that journey (parent span = the whole trip, child spans = each stop):

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-5-1-distributed-tracing.py`](examples/10-5-1-distributed-tracing.py)

</details>

> **One-line summary:** Distributed tracing = one trace_id travels with a request and each step adds a timed span — the diary that shows exactly which stop was slow or broken.

### 5.2 Structured Logging + Metrics

Think of a cozy kitchen thermometer plus a notebook: one side (structured logging) jots down every event as tidy JSON you can easily search later, the other side (metrics) keeps the scoreboard — how many runs, how many wins, and how slow the slowest bites were (p50/p95/p99). The sample below gives you both companions, WorkflowLogger and MetricsCollector. Plain words: **structured logging** = writing each log line as JSON with fixed fields (time, step, level) instead of free text, and **p50/p95/p99** = the wait time that 50%, 95%, and 99% of runs stay under — so p95 = "the slow 5% can be worse than this":

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/11-5-2-structured-logging-metrics.py`](examples/11-5-2-structured-logging-metrics.py)

</details>

> **One-line summary:** Structured logs (searchable JSON) + metrics (scoreboard with p50/p95/p99 timings) = the two tools that answer "what happened" and "how bad is it".

---

## 6. Workflow Orchestration Engine

> **📌 Core Concept**
>
> - **Concept:** The workflow orchestration engine is the "heart" of the system — the central component responsible for starting, dispatching, monitoring, and canceling workflows, while managing scheduling, per-step state, retries, and dependencies between steps.
> - **Analogy:** Like an airport air traffic control tower: it dispatches each flight (task) to take off and land on the right runway, in the right order, and knows exactly where every plane is.
> - **Why it matters:** This is where all the knowledge from the previous sections — patterns, pipelines, state machines, error recovery, observability — gets bundled into one engine you can actually use.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/12-6-workflow-orchestration-engine.py`](examples/12-6-workflow-orchestration-engine.py)

</details>

> **One-line summary:** The orchestration engine = the control tower that bundles everything from sections 1–5 into one component that starts, runs, watches, retries, and cancels workflows.

---

## 7. Workflow Testing

> **📌 Core Concept**
>
> - **Concept:** Workflow testing is the process of testing a workflow before running it in production — unit tests for each step, integration tests for the whole chain, end-to-end tests for the full flow — to make sure the steps chain together correctly and errors are handled as expected.
> - **Analogy:** Like test-running a production line with dummy goods: a single stuck stage immediately shows where it's broken, without spending money on real goods.
> - **Why it matters:** The more complex the workflow, the harder it is to find failures at the seams between steps; proper testing catches bugs before they break the real system.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/13-7-workflow-testing.py`](examples/13-7-workflow-testing.py)

</details>

> **One-line summary:** Test the workflow like you test code — unit-test each step, integration-test the chain, and rehearse failures (chaos testing) before real data hits the line.

---

## 8. Harness Integration

> **📌 Core Concept**
>
> - **Concept:** Harness integration is the layer that connects the Workflow module to the entire Harness framework — Memory, Guardrails, Tool Execution, Feedback — through unified interfaces so the modules communicate through a common "language".
> - **Analogy:** Like a universal power outlet: any device (module) plugged in fits and works, as long as it follows the interface standard.
> - **Why it matters:** Without standard interfaces, every module invents its own calling convention — integration becomes a tangled mess of wires that's hard to maintain.

> **One-line summary:** Harness integration = one agreed set of function names so the Workflow module can talk to Memory, Guardrails, Tools, and Feedback without custom wiring.

### 8.1 TypeScript Interfaces

Think of this as the friendly handshake agreement between the Workflow module and the rest of the Harness family — a short list of promises like createWorkflow, execute, pause, resume, cancel, getTrace, getMetrics. Once everyone agrees on the same handshake, any module knows exactly how to ask the engine for help. Plain words: a **TypeScript interface** = a written contract listing which functions exist and what they take/return — no behavior, just the shape (like a power-socket standard, not the electricity):

<details>
<summary><b>8.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/14-8-1-typescript-interfaces.ts`](examples/14-8-1-typescript-interfaces.ts)

</details>

> **One-line summary:** TypeScript interfaces = the handshake contract (createWorkflow, execute, pause, resume, cancel, getTrace, getMetrics) that makes every module plug-compatible.

---

## 9. Case Studies

> **📌 Core Concept**
>
> - **Concept:** Case studies are practical analyses of how large systems (GitHub Actions, Apache Airflow, Temporal, DeepSeek Harness) design their workflows, so you can distill lessons to apply to your own project.
> - **Analogy:** Like watching a documentary and learning from its lessons: instead of charging headlong into the same pitfall, you learn right away from how those who came before solved the problem.
> - **Why it matters:** Pure theory is hard to picture; learning from real systems shows you which patterns actually work in production conditions.

> **One-line summary:** Four real systems (GitHub Actions, Airflow, Temporal, DeepSeek Harness) show the theory above working in production — steal their proven patterns.

### 9.1. GitHub Actions — Event-Driven CI/CD

Here is one you have probably met in real life: a short YAML file that runs your CI/CD every time you push or open a pull request. Notice the two friendly ideas living side by side — the doorbell that starts it all (the `on:` trigger) plus polite waiting in line (deploy patiently waits for build, build waits for lint and test). Plain words: **CI/CD** = automatic build-test-deploy that runs after every push, **YAML** = a simple indent-based text format for configs, and `on:` = the doorbell line listing which events start the pipeline:

<details>
<summary><b>9.1. GitHub Actions — Event-Driven CI/CD (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/15-9-1-github-actions-event-driven-ci-cd.yaml`](examples/15-9-1-github-actions-event-driven-ci-cd.yaml)

</details>

**Takeaway**: GitHub Actions is a lovely real-life DAG — a doorbell (event trigger) rings, jobs fan out and wait their turn (dependency resolution), and the whole party flows in order.

> **One-line summary:** GitHub Actions = event trigger + DAG dependencies in one small YAML file — a production-proven mix of patterns 1.3 and 1.4.

### 9.2. Apache Airflow — Data Pipeline Orchestration

Airflow feels like writing a recipe card in plain Python: you simply name your chores (extract, transform, load, validate) and link them with the little `>>` arrows to say who goes first. The whole journey lays out like a subway map on the fridge — easy to read, easy to reshuffle. Plain words: **ETL (extract, transform, load)** = pull data out of a source, reshape it, write it into a warehouse, and `>>` = Airflow's arrow meaning "run after":

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-9-2-apache-airflow-data-pipeline-orchestration.py`](examples/16-9-2-apache-airflow-data-pipeline-orchestration.py)

</details>

**Takeaway**: Airflow showed the world why clear "who waits for whom" DAGs became the gold standard for data pipelines — draw the map once, and everyone can follow it.

> **One-line summary:** Airflow = draw your data pipeline as a Python DAG with `>>` arrows — readable, reshufflable, and now the industry standard.

### 9.3. Temporal — Durable Workflow Execution

Temporal has one big heart-warming promise: your workflow should "survive" even if the server takes a nap halfway through — progress is saved safely (durable), retries happen on their own, and there is always an undo plan. The little story below is a shop order told Saga-style: reserve stock → charge payment → ship order; if shipping stumbles, we gently walk backward and refund. Plain words: **durable execution** = every finished step is saved to disk, so a crash costs one step, not the whole run, and **compensating transaction** = the pre-written undo for a step:

```
Temporal pattern: Saga with compensating transactions

Workflow:
  1. ReserveInventory() → success
  2. ChargePayment() → success
  3. ShipOrder() → FAIL
  
Compensation (reverse):
  2. RefundPayment()
  1. ReleaseInventory()
```

**Takeaway**: Temporal's big heart-warming lesson — a good workflow naps safely through a crash (durable state), wakes up and retries on its own, and always knows how to undo things kindly (compensation).

> **One-line summary:** Temporal = durable execution: save every step, survive crashes, retry automatically, and undo in reverse when a late step fails.

---

### 9.4. DeepSeek Harness — Cordis Micro-Kernel Plugin Architecture

**Context**: DeepSeek Harness uses **Cordis** — a micro-kernel plugin engine designed around the philosophy **"Agent = Model + Harness"** and **"Everything is a plugin"**. Cordis provides a lightweight kernel (~2KB gzipped) that manages the entire agent lifecycle through a plugin system, with dependency injection via a Context service registry.

In plain everyday words: the kernel is a tiny operating system, and each plugin is an app on your phone — every app just says "here is what I need" (consumes) and "here is what I share" (provides), and the phone quietly plugs the wires together so everything starts in the right order. Plain words for the jargon: **micro-kernel** = a tiny core (~2KB) that only wires things together, **plugin** = a self-contained app that adds one capability, and **dependency injection** = a plugin asks for what it needs instead of building it itself — like ordering room service instead of installing a kitchen.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts`](examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts)

</details>

**Key Architectural Innovations**:

1. ✅ **Micro-Kernel Design** — The kernel is only ~2KB, everything is a plugin. Load on demand, hot-reloadable. (**Hot-reload** = swap a plugin while the system keeps running, no restart.)

2. ✅ **Lifecycle Management** — 4 phases: `init` → `attach` → `ready` → `detach`. Deterministic startup/shutdown. (**Lifecycle** = the fixed life stages of a plugin: prepare → connect → working → disconnect.)

3. ✅ **Context Service Registry** — `ctx.provide()` / `ctx.inject()` / `ctx.get()` for dependency injection. Plugins declare `provides`/`consumes` for auto-wiring. (Plain words: one plugin offers a service with `provide`, another picks it up with `inject` — the registry is the matchmaker.)

4. ✅ **Event Bus** — Pub/sub for inter-plugin communication. Loose coupling, extensible. (**Pub/sub** = publish-subscribe: senders shout into a channel, listeners who care react — senders never need to know who is listening.)

4. ✅ **4 Runtime Modes** (provided by the `runtime-mode` plugin):
   - **Standard** — Full agent, all tools, process isolation
   - **Code** — `@deepseek-ai/dsh` SDK, single-turn, batched, VM sandbox, 70-90% latency reduction
   - **Benchmark** — Minimal (bash + editor only), container isolation, deterministic for SWE-bench
   - **Creator** — Visual timeline, presets, time-travel debugging, fork/replay

5. ✅ **Trajectory Traceability** (by the `trajectory-recorder` plugin):
   - Append-only Session Event Stream
   - `replayToStep()`, `forkSession()`, `resumeSession()`
   - Event search by type, time, step

   (Plain words: **append-only** = the event log only gains lines, never edits, so it stays a trustworthy record; **replay** = re-run from the log, **fork** = branch off a copy of the session, **resume** = continue where it stopped.)

6. ✅ **Plugin Composition** — DeepSeek Harness = composition of plugins. Easy to swap, extend, test.

**Cordis vs Traditional Frameworks**:

How to read the table: each row compares one aspect of building agents. Column **LangGraph / AutoGen** = how mainstream frameworks do it; column **Cordis (DeepSeek Harness)** = how Cordis does it; for instance, the **Hot Reload** row says swapping a plugin live is "difficult" in traditional frameworks but native (built-in) in Cordis.

| Aspect | LangGraph / AutoGen | Cordis (DeepSeek Harness) |
|--------|---------------------|---------------------------|
| **Architecture** | Framework-specific | Micro-kernel + Plugins |
| **Extensibility** | Subclass/override | Register plugin |
| **Dependency Injection** | Manual/prop drilling | `ctx.provide` / `ctx.inject` |
| **Lifecycle** | Implicit | Explicit: init→attach→ready→detach |
| **Hot Reload** | Difficult | Native (detach + attach) |
| **Size** | Heavy (~MB) | ~2KB kernel |
| **Runtime Modes** | Single | 4 distinct modes |
| **Trajectory** | External logging | Built-in plugin |

**File Reference**: Implementation details in [`cordis-kernel-plugin.md`](cordis-kernel-plugin.md)

> **One-line summary:** Cordis = a 2KB kernel + plugins that declare what they provide and consume — swap, extend, and hot-reload pieces without touching the core.

---

## 10. Design Principles

> **📌 Core Concept**
>
> - **Concept:** Design principles are the architectural guidelines (including SOLID) applied specifically to workflows — helping you decide how to split steps, organize dependencies, and draw responsibility boundaries in your system.
> - **Analogy:** Like house-building regulations: no one forbids building, but following the building codes makes the house safe, easy to fix, and spared from being torn down and rebuilt.
> - **Why it matters:** Good principles make workflows easy to scale, easy to test, and low in technical debt as the system grows.

> **One-line summary:** Design principles = building codes for workflows — follow them and the system stays testable and scalable; ignore them and every change gets riskier.

### 10.1 SOLID for Workflows

**SOLID** = five classic code-quality rules, one letter each: **S**ingle responsibility, **O**pen/closed, **L**iskov substitution, **I**nterface segregation, **D**ependency inversion. Here is what each means when your "code" is a workflow:

**1. Single Responsibility**
- Each step = 1 clear job
- Don't combine parse + validate + transform in one step

**2. Open/Closed**
- Open for adding new steps
- Closed for modifying existing workflow logic

**3. Liskov Substitution**
- Step A can be swapped for step B (same interface)
- Conditional branches can be swapped

**4. Interface Segregation**
- Step input/output schemas kept separate
- No shared mutable state

**5. Dependency Inversion**
- The workflow engine depends on the Step abstraction
- No hardcoded step implementations

> **One-line summary:** SOLID for workflows: one job per step, add steps without rewriting the engine, keep steps swappable, and never hardcode implementations into the engine.

### 10.2 6 Design Principles

Meet your pocket compass for workflow design — six little stars to steer by. They range from "it is safe to press replay" (idempotency) all the way to "keep your notes outside your head" (state externalization), so you can always pick up where you left off:

```
┌──────────────────────────────────────────────────────────────────┐
│                 WORKFLOW DESIGN PRINCIPLES                        │
│                                                                  │
│  1. IDEMPOTENCY                                                  │
│     Every step must be safe to run multiple times               │
│     → Use UUID/idempotency key for mutations                     │
│                                                                  │
│  2. OBSERVABILITY                                                │
│     Every step must log input/output + metrics                  │
│     → Use structured logging + distributed tracing              │
│                                                                  │
│  3. SEPARATION OF CONCERNS                                       │
│     Each step does exactly one thing                            │
│     → Easy to test, easy to replace, easy to debug             │
│                                                                  │
│  4. PROGRESSIVE DISCLOSURE                                       │
│     Start simple, add complexity only when needed               │
│     → Sequential first, Parallel when there's a bottleneck      │
│                                                                  │
│  5. FAIL-FAST + RECOVER                                          │
│     Detect errors early, have a recovery strategy               │
│     → Retry + Circuit Breaker + Saga pattern                    │
│                                                                  │
│  6. STATE EXTERNALIZATION                                        │
│     Store state outside memory                                  │
│     → Can resume from checkpoint                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

How to read the diagram: six numbered rules, each with a plain rule line and an arrow showing the tool to use. For instance, rule 1 (**IDEMPOTENCY**) means running a step twice must leave the same result as running it once — so use a **UUID/idempotency key** (a unique tag per operation) when a step changes data, and the engine can safely skip repeats. Rule 6 (**STATE EXTERNALIZATION**) means keep state in a file or database, not in program memory, so a restart can resume from the last **checkpoint**.

> **One-line summary:** Six rules for any workflow: repeat-safe steps, full logging, one job per step, start simple, fail fast with recovery, and keep state outside program memory.

---

## 11. Best Practices

> **📌 Core Concept**
>
> - **Concept:** Best practices are the list of things to do (DO) and not do (DON'T) distilled from real experience building workflows for AI Agents.
> - **Analogy:** Like a pilot's pre-flight checklist: everyone knows it by heart, but writing it down and checking it off in sequence is what really makes sure you don't skip a small task with big consequences.
> - **Why it matters:** This is your "trap-avoidance map" — do it right and you save headaches; do it wrong and you invite bugs that are hard to debug.

> **One-line summary:** Best practices = the pre-flight checklist: do these ten things, avoid these eight traps, and most workflow bugs never get written.

### 11.1 DO ✅

- **Define clear input/output for each step**: Easier to test and debug
- **Add structured logging at every step**: JSON logs with timestamps
- **Implement retry with exponential backoff**: Handle transient failures
- **Use circuit breakers for external services**: Prevent cascade failures
- **Design for idempotency**: Safe to replay any step
- **Add timeout for every step**: Prevent hanging workflows
- **Use saga pattern for distributed transactions**: Compensate on failure
- **Track metrics**: Latency, success rate, error rate per step
- **Validate DAG structure**: Detect cycles before execution
- **Add checkpointing**: Resume from last successful step

> **One-line summary:** DO: clear step boundaries, JSON logs, retry with backoff, circuit breakers, idempotency, timeouts, saga compensation, metrics, cycle checks, and checkpoints.

### 11.2 DON'T ❌

- **Don't share mutable state between steps**: Use immutable data passing
- **Don't skip error handling**: Every step can fail
- **Don't use infinite loops**: Always set max iterations
- **Don't ignore timeout**: A hanging step = stuck workflow
- **Don't hardcode step dependencies**: Use DAG configuration
- **Don't skip testing**: Unit test each step independently
- **Don't use blocking calls in parallel steps**: Use async/executor
- **Don't forget compensation logic**: Every forward action needs a rollback

> **One-line summary:** DON'T: share changeable state, skip error handling, loop forever, ignore timeouts, hardcode dependencies, skip tests, block parallel steps, or leave actions un-undoable.

---

## 12. Future

> **📌 Core Concept**
>
> - **Concept:** The Future section sketches the trends in workflow orchestration and agent pipelines for 2026-2028 — AI-generated workflows, serverless engines, cross-platform execution, and real-time adaptive workflows.
> - **Analogy:** Like checking next week's weather forecast: not 100% certain, but enough direction to pick an architecture that won't be obsolete two years from now.
> - **Why it matters:** Knowing the trends helps you invest in the right technology and avoid building something about to be replaced.

> **One-line summary:** The 2026-2028 forecast: workflows generated by AI, engines you rent per run, definitions that port across platforms, and self-adjusting pipelines — plan for these, don't bet against them.

### 12.1 Trends 2026-2028

**1. AI-Generated Workflows**
- Agents auto-generate workflows from task descriptions
- Auto-optimize workflow structure based on execution history
- Self-healing workflows

**2. Serverless Workflow Engines**
- Workflow-as-code (no infrastructure management)
- Auto-scaling per step
- Pay-per-execution pricing

**3. Cross-Platform Workflow Portability**
- Standard workflow definition format (CNCF WASM?)
- Portable across Temporal, Airflow, Step Functions
- Universal workflow marketplace

(Plain words: **CNCF** = the Cloud Native Computing Foundation, the open-source standards body; **WASM (WebAssembly)** = a portable binary format that runs anywhere — here, the idea that one workflow file could run on any engine; **Step Functions** = AWS's workflow service. **Marketplace** = a store where teams sell/reuse ready-made workflows.)

**4. Real-time Adaptive Workflows**
- Dynamic step adjustment based on runtime metrics
- ML-based bottleneck prediction
- Auto-parallelization

(Plain words: the workflow rewrites its own plan while running — for example, if metrics show step 3 is the **bottleneck** (the slowest link), the engine splits it into parallel pieces by itself.)

**5. Workflow Observability 2.0**
- AI-powered root cause analysis
- Predictive alerting
- Automated incident response

(Plain words: the tools stop just recording and start thinking — AI reads the traces, names the likely root cause, warns before failure, and can even run the fix playbook.)

> **One-line summary:** Five trends to watch: AI-written workflows, serverless engines, portable definitions (WASM), self-adapting pipelines, and AI-assisted observability.

---

## 13. Production Durability: Checkpoint-Resume, Idempotency, Backpressure, Approvals

This section explains how to keep a workflow alive and correct in production — where crashes, repeats, overload, and human sign-offs are daily facts. Each subsection covers one of the four defenses.

> **One-line summary:** Production durability = four defenses: checkpoint-resume for crashes, idempotency keys for repeats, backpressure for overload, and approval nodes for human sign-off.

### 13.1 Definitions

How to read the table: each row defines one durability term used in this section. For instance, **Idempotency key** = a unique tag (`stepId + inputHash`) for an operation; running it twice with the same tag returns the saved result instead of doing the work twice (no double charge, no double write).

| Term | Definition |
|------|------------|
| Durable execution | Every step completion is checkpointed (event log + snapshot); restart resumes from last checkpoint, never from zero |
| Idempotency key | `stepId + inputHash (+ attempt ceiling)`; re-execution with same key returns stored result, no double side-effect |
| Backpressure | Bounded queue + semaphore (`maxParallel`), per-run deadline propagated via `AbortSignal`/ctx; shed or defer instead of OOM |
| Approval node | Step with state `WAITING_APPROVAL`; engine pauses, persists, resumes on approve/reject/timeout |

Plain-language glosses for the table's jargon:

- **Checkpointed** = progress saved to durable storage (disk, DB, S3) after each step. **Snapshot** = a full picture of the state at one moment, saved in one go.
- **`stepId + inputHash`** = the step's name plus a fingerprint of its input; same step + same input = same key = same stored result. **Attempt ceiling** = max number of tries.
- **Bounded queue** = a waiting line with a max length. **Semaphore** = a counter that only lets N tasks run at once (`maxParallel` = that N). **`AbortSignal`** = a cancel flag you can pass to a task to stop it. **OOM** = out of memory — the process dies from overload. **Shed or defer** = refuse now or postpone, instead of dying.
- **`WAITING_APPROVAL`** = the step is parked, waiting for a human to approve or reject.

> **One-line summary:** Four defenses keep production runs safe: save progress (checkpoint), tag operations so repeats are harmless (idempotency), cap the load (backpressure), and pause for human sign-off (approval nodes).

### 13.2 Checkpoint-Resume (Across Restart)

Signpost: this explains how a workflow survives the process being killed and restarted, losing nothing but at most the step that was in flight.

Use a **write-ahead log** = write the record down *before* doing the work, like a kitchen ticket before cooking: `append({seq, stepId, inputHash, status, outputRef})` — that record holds a sequence number, which step, an input fingerprint, its status, and a pointer to the output. Add an **atomic snapshot** = save the whole state picture in one indivisible write, every N steps. On boot the recovery dance is: `load snapshot → replay log tail → skip completed (idempotent) → resume pending`. Snapshot to local JSON/SQLite (a small local database file); outputs larger than 64KB go to an **artifact store** (external file storage like S3) referenced by a pointer (**ref**) instead of inline. Keep `runId` stable across restarts — same `runId` = same run history.

> **One-line summary:** Write each step's record before running it, snapshot periodically, and on restart replay the log and skip completed steps — a crash then costs one step, not the whole run.

### 13.3 Per-Step Idempotency + Backpressure + Deadlines

Signpost: this explains the three per-step safety knobs — harmless repeats, load limits, and time limits.

**Idempotency**: keep a store `Map<idempotencyKey, resultRef>` with a **TTL** (time-to-live = how long an entry stays valid before expiring). Steps that *change* data (mutations) must carry a key; read-only steps don't need one.

**Backpressure**: one global **semaphore** (concurrency counter) `Semaphore(maxParallel=4–8)` limits how many steps run at once, plus a per-step queue cap (say 100 items). When the queue is full, `enqueue` throws `BackpressureError` — the caller retries later with **jitter** (random extra wait), instead of piling up until memory dies.

**Deadline**: one `deadlineAt` (due time) per run. Each step computes `remaining = deadlineAt - now()` (minus a safety buffer) and gets it via `AbortSignal.timeout(remaining)` — a cancel flag that fires automatically when time is up. Never extend deadlines silently; a late run must be visible, not quietly forgiven.

> **One-line summary:** Three per-step knobs: tag mutations so repeats are harmless, cap concurrency and queue size to shed load, and give every run one visible deadline that cancels overdue steps.

### 13.4 Human Approval / Pause-Resume Nodes

**This section owns the checkpoint primitive; the gate policy belongs to
[`15-approval-gates`](../15-approval-gates/README.md).** The engine below provides *mechanism* —
a typed `PAUSED:` throw after a durable checkpoint, a write-ahead log, an idempotency store,
and a `WAITING_APPROVAL` state that survives process death. It does **not** decide *whether* a
step needs a human or what the approver is shown. Those are specified in `15`: the risk-tier
taxonomy and TTLs, the mandatory-evidence payload, timeout-deny (fail closed), the two-person
rule, and the `approval_request` / `approval_verdict` audit trail. The protocol's ordering
contract — checkpoint first, then throw; the human's approval is a *verdict delivery*, not a
restart — is written out in `15` §5.2.

Treat `needsApproval?: boolean` below as the seam: `07` moves the run to `WAITING_APPROVAL`
and throws; `15` decides who settles it and what happens on timeout. A `true` here does not
mean "ask someone", it means "ask the Gatekeeper".

Plain words for the policy terms owned by `15`: **mechanism vs policy** = this module supplies the machinery (pause, save, resume), `15` supplies the rules (who approves, when); **risk-tier taxonomy** = sorting steps by danger level; **TTL** = how long an approval request stays open; **fail closed** = if the approval times out, block the action rather than letting it through; **two-person rule** = sensitive actions need two humans to agree; **audit trail** = an un-editable record of who asked and who approved.

<details>
<summary>TypeScript Code — Durable Engine (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-13-4-human-approval-pause-resume-nodes.ts`](examples/18-13-4-human-approval-pause-resume-nodes.ts)

</details>

Resume: re-invoke `run()` with same `runId`; completed keys hit `done()`/store and skip. Pause: catch `PAUSED:*`, persist UI state, approve then re-run.

Plain words: **`PAUSED:` throw** = the engine raises a special exception to say "I stopped at a checkpoint on purpose" — pausing is safe because everything was already saved before the throw.

> **One-line summary:** Approval nodes = pause at a checkpoint with state `WAITING_APPROVAL`, survive process death, then resume on approve/reject/timeout — mechanism here, approval policy in doc 15.

### 13.5 Checklist

How to use it: tick each box only when you have actually tested it — for instance, the first box means literally kill the process mid-run (`kill -9` = force-kill, no cleanup chance) and confirm the next run resumes correctly.

- [ ] Checkpoint after every step (log + snapshot); restart test passes (kill -9 mid-run)?
- [ ] All mutating steps use idempotency keys; double-run is side-effect-free?
- [ ] `maxParallel` + queue cap set; deadline propagated to every step signal?
- [ ] Approval nodes persist `WAITING_APPROVAL`; approve/reject/timeout paths resume correctly?

> **One-line summary:** Ship durable workflows only after proving all four: crash-resume works, double-runs are harmless, load limits and deadlines are wired, and approvals survive restarts.

---

## References

Where to read deeper: papers explain the theory, framework docs show the tools in action. Both lists below keep only sources this document actually leans on.

> **One-line summary:** Nine sources total — four research references and five framework manuals — each directly used in the patterns above.

### Papers & Research

1. **Temporal: Durable Execution**
   - https://docs.temporal.io
   - Durable workflow execution with automatic retry and compensation

2. **Apache Airflow Documentation**
   - https://airflow.apache.org/docs/
   - DAG-based workflow orchestration

3. **Microservices Patterns**
   - Chris Richardson, 2018
   - Saga pattern, CQRS, Event Sourcing

4. **Designing Data-Intensive Applications**
   - Martin Kleppmann, 2017
   - Pipeline design, distributed systems patterns

> **One-line summary:** These four sources cover durable execution (Temporal), DAG orchestration (Airflow), and the classic patterns book (Richardson) plus the data-systems bible (Kleppmann).

### Frameworks

The list below = the tools this document's patterns come from; each URL is its official documentation.

1. **Temporal** - https://temporal.io
2. **Apache Airflow** - https://airflow.apache.org
3. **Prefect** - https://www.prefect.io
4. **GitHub Actions** - https://docs.github.com/en/actions
5. **AWS Step Functions** - https://aws.amazon.com/step-functions/

> **One-line summary:** Five workflow engines worth knowing: Temporal, Airflow, Prefect, GitHub Actions, and AWS Step Functions — each docs link above is the official manual.

---

> **Oct-2026 addendum:** want "guards at the doors" for your agent? Read
> [`hooks-standard.md`](./hooks-standard.md). In short: each lifecycle point
> (`preToolUse`, `postToolUse`...) gets a check script — allow, ask a human, or block.

*Document: VII. Workflow — HARNESS ENGINEERING EDITION*
*Last updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Production Reliability Patterns (Anthropic 2025)

> **📌 Context:** The three patterns below are distilled from the article *Effective Harnesses for Long-Running Agents* (Anthropic, 2025) — for when the agent is no longer a 5-minute demo but a production system running for hours, deploying continuously, where failure is a given.

> **One-line summary:** Three production-grade patterns for long-running agents: resume from checkpoints instead of restarting, shift traffic gradually between versions, and avoid sync bottlenecks in orchestration.

### 1. Checkpoint & Resume (no restart)

Agents are **stateful** — state accumulates step by step, so small errors tend to **compound**: a small slip at step 3 creates a big error at step 7. When an error happens, don't run again from scratch — **resume from the latest checkpoint**. Plain words: **stateful** = each step builds on what earlier steps did, and **compound** = small mistakes snowball, like one wrong turn on a road trip putting you in the wrong city by noon:

| Component | Role |
|---|---|
| **Checkpoint** | Each completed step saves state (outputs, variables, progress) to durable storage (JSON file, S3, DB) |
| **Resume** | Crash/timeout → load latest checkpoint → skip finished steps → continue |
| **Deterministic retry/backoff** | Transient errors (network, rate limit) → exponential backoff, bounded retries |
| **Model adaptation** | Logic errors → **report tool failure to the agent** so it can adapt (change approach) instead of retrying the same way |

How to read the table: each row is one part of the resume machine. For instance, the **Checkpoint** row means: after every finished step, save outputs and progress to durable storage (a JSON file, S3, or a database) so a crash can restart from there, not from zero.

The triage principle: **deterministic problems get retry/backoff; anything requiring judgment goes back to the model** — an agent that can see the error will fix its own strategy; blind mechanical retries cannot.

> **One-line summary:** Save state after every step, resume from the last checkpoint, and triage errors: mechanical failures get retry with backoff, judgment calls go back to the model.

### 2. Rainbow Deployments

Agents may be **mid-run** when you deploy a new version — cutting them off mid-flight loses state and breaks in-progress tasks. Solution: **shift traffic gradually** from the old version to the new one, keeping both running in parallel. Plain words: **rainbow deployment** = run old and new versions side by side and move users over gradually (named for versions of different "colors" running at once), instead of a big-bang swap:

| Phase | Old version | New version | Notes |
|---|---|---|---|
| 1. Parallel deploy | 100% | 0% | New version stands by, ready to receive tasks |
| 2. Gradual shift | 80% → 50% → 20% | 20% → 50% → 80% | New tasks go to the new version; old tasks run out their lifecycle on the old version |
| 3. Complete | 0% | 100% | Shut down the old version when no task is still running on it |

How to read the table: each row is one phase of the rollout. Columns **Old version** and **New version** show what share of new tasks each gets; for instance, row 2 means new tasks split 20/80, while tasks already running on the old version are allowed to finish there.

The key point: **don't kill the old version immediately** — agents running mid-flight on it need to complete fully (**drain** = let every in-progress task finish before shutting down, like letting the last guests leave before closing the restaurant). Reference: **rainbow deploys in Kubernetes** (Argo Rollouts, Flagger) — weighted routing between versions.

> **One-line summary:** Deploy new versions by shifting traffic gradually and draining the old one — no agent ever loses its in-flight work.

### 3. Sync Bottleneck in Orchestration

Running subagents **synchronously** (the lead waits for each subagent to finish before assigning the next task) is the simplest model — but it creates a serious **bottleneck** (one slow part holds up everything behind it):

- The lead **cannot steer** a subagent mid-run: if the subagent drifts off course, you still have to wait for it to finish before correcting.
- The lead is **blocked** when one subagent is slow: the whole system stalls behind the slowest subagent (**waterfall effect** = delays pile up downstream, like cars stacking behind one slow truck).

**Async orchestration** solves throughput, but you must answer 3 hard questions:

| Problem | Question | Solution direction |
|---|---|---|
| **Result coordination** | When do results from many subagents come back, and how are they collected? | Completion queue, callbacks, or barrier sync |
| **State consistency** | Multiple subagents write shared state — how are conflicts handled? | Versioning, optimistic locking, or partitioned write zones |
| **Error propagation** | If one subagent fails, do dependent subagents know? | Cancellation tree + shared error bus |

How to read the table: each row is one hard question that async orchestration forces you to answer. Column **Question** = the problem; column **Solution direction** = the known tool for it; for instance, the **State consistency** row means: when several subagents write the same data, use versioning, optimistic locking (write freely, check for clashes at save time), or separate write zones per agent.

Pragmatic rule: **sync when there are few subagents and tasks are short** (easier to debug); **async when tasks are long and highly independent** (but invest in the 3 issues above from the start — don't let them become technical debt).

> **One-line summary:** Sync orchestration is simple but stalls behind the slowest subagent; going async buys speed but obligates you to solve result collection, state conflicts, and error spreading.

### 4. Python Code — Workflow Runner with Checkpoint/Resume

Signpost: this example shows checkpoint/resume from section 1 of this update as real code, so you can see the mechanics, not just the idea.

The code below illustrates the pattern: each completed step saves a checkpoint (JSON), crash → resume from the last checkpoint, retry with exponential backoff, max 3 times:

> 📄 **Example code:** [`examples/19-4-python-code-workflow-runner-with-checkpoint-resume.py`](examples/19-4-python-code-workflow-runner-with-checkpoint-resume.py)

**Key points in the code:**
- `_save()` runs **immediately after** each step finishes — the checkpoint is always fresh, so a crash at step N means the next run only repeats that exact step.
- A fixed `run_id` makes multiple reruns of the same task **share one checkpoint set** — this is exactly what resume means.
- Retry is **deterministic** (fixed backoff formula) for transient errors; when retries run out, the exception is raised so the **agent can notice and adapt** (change approach) rather than retrying forever.

> **One-line summary:** The runner saves a JSON checkpoint after every step under a fixed `run_id`, so a crash reruns only the failed step — and gives up retrying loudly so the model can adapt.

### 5. Cross-Reference

> 📎 **Related:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 2** (Orchestration) + **Section 4.3** (Long-Running Agent Pattern). See also Section 4 (Error Recovery) above for retry/circuit breaker/saga — checkpoint/resume is a complementary layer, not a replacement.

> **One-line summary:** Checkpoint/resume fits alongside (not instead of) the error-recovery tools in section 4 — see the architecture doc's Layer 2 for where orchestration sits overall.

---

*Document: VII. Workflow — HARNESS ENGINEERING EDITION*
*Updated: 26/10/2026*
*Author: AI Knowledge Repository*
