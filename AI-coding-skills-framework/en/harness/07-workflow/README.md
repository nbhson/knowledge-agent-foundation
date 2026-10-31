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

### Why Is a Workflow Important?

> *"An agent without a workflow is like a chef without a recipe — you have the ingredients, you have the tools, but the dish comes out by whim."*

#### 3 Scientific Pieces of Evidence

| # | Research | Key Finding |
|---|----------|-------------|
| 1 | **Google DeepMind (2025)** | Structured workflows reduce the **45% task failure rate** in multi-step coding agents |
| 2 | **Anthropic (2025)** | Workflow engines with retry + checkpoint reduce **data loss by 70%** when agents hit errors |
| 3 | **LangGraph Benchmark (2025)** | State machine workflows handle **3× complex tasks** better than simple sequential chains |

#### Core philosophy:

```
Workflow = Trigger → Plan → Execute → Validate → Deploy → Feedback
```

Every step must have **state management**, **error recovery**, and **observability**. A workflow is not just "an order of steps" — it is a system that manages the **entire lifecycle** of a task.

**Analogies**: A workflow is like a transportation system — traffic lights (guardrails), routes (steps), a control center (orchestrator), and surveillance cameras (logging).

**If you skip it**: Agents execute tasks messily, cannot recover from errors, cannot track progress, and debugging becomes a nightmare.

## Overview

> **📌 Core Concept**
>
> - **Concept:** A workflow is how the execution steps of an AI Agent are arranged into a clear plan — which step comes first, which comes next, how errors are handled — so that a complex task is completed in the right order and safely.
> - **Analogy:** Like a restaurant kitchen: a chef (agent) with good ingredients still needs a recipe and a service routine (workflow) to deliver dishes on time, at the right quality, every time.
> - **Why it matters:** Without a workflow, an agent works on instinct — slow, hard to reproduce results, and any mid-way failure means starting over from scratch.

**Workflow** is simply the art of **laying out the steps** that finish a tricky coding job. Inside Harness Engineering, the Workflow Engine is the friendly **"dispatch center"** — it waves each job through from trigger → plan → execute → validate → deploy, while keeping an eye on everything (observability), catching falls (error recovery), and remembering where everyone is (state).

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

---

## 1. Workflow Patterns

> **📌 Core Concept**
>
> - **Concept:** Workflow patterns are the "molds" that organize an AI Agent's chain of activities — run in order (sequential), run at the same time (parallel), or branch on conditions (conditional branching) — to reach the task objective in a controlled way.
> - **Analogy:** Like roads in a city: a straight road (sequential), many lanes running at the same time (parallel), or an intersection that diverts traffic according to signs (conditional branching).
> - **Why it matters:** Choosing the right pattern determines the speed, complexity, and fault tolerance of the entire workflow.

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

### 1.2 Parallel Workflow (Concurrent)

Think of cooking a big family dinner with friends helping out: while you wash the vegetables, someone else cooks the rice and another friend fries the main dish — then you all meet back at the table to serve. That teamwork is why this pattern feels fast: lots of things happen at once. The tricky part is the reunion at the end (fan-in), where you gather every dish together. Use it when the jobs do not really need each other to finish first:

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

### 1.3 DAG Workflow (Directed Acyclic Graph)

Think of a weekend sports bracket: the semifinal cannot start until both quarterfinal games are done, but those two quarterfinals happily run side by side. A DAG works just like that — it is the most flexible playbook. Each small job runs as soon as the jobs it depends on are finished, level by level, and the rules simply say "no going in circles." In the sketch below, A and B play at the same time → C waits for A, D waits for B → E waits for C, F waits for D:

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

### 1.4 Event-Driven Workflow

Think of a friendly neighborhood fire station: wherever the bell rings (that is your event), the crew on duty (the handler) rolls out — and what they find there can ring the next bell. Unlike the tidy step-by-step recipes above, you do not plan every turn in advance here. The workflow simply listens and reacts as things happen, which makes it a lovely fit for busy, unpredictable real life:

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

---

## 2. Pipeline Design

> **📌 Core Concept**
>
> - **Concept:** Pipeline design is how to split a large task into successive stages; each stage receives data from the previous stage, processes it, and passes it on, with branching and fan-out/fan-in capabilities.
> - **Analogy:** Like a beer factory line: mash → boil → filter → ferment → bottle; each step takes the output of the previous step, with a fork if the customer orders a different kind of beer.
> - **Why it matters:** Pipelines keep large data processing tidy, let you inspect every stage, and are easy to update when the business changes.

### 2.1 Data Pipeline with Branching

Think of this as the friendly assembly line for your data: every station has one clear job (transform, filter, branch, fan_out, validator, sink), and your data rides the belt from one station to the next, just like a parcel in a post office. The fun twist is branching — at one station you peek at the parcel and flip a switch that sends it left or right, like a railway junction. The code sample right below shows how you snap those stations together and press "go" on the whole line:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-2-1-data-pipeline-with-branching.py`](examples/05-2-1-data-pipeline-with-branching.py)

</details>

---

## 3. State Machine

> **📌 Core Concept**
>
> - **Concept:** A state machine is a "state machine" — a model that records which state the agent is in (reading code, writing code, running tests) and only allows moving to the next state when certain conditions are met.
> - **Analogy:** Like a three-color traffic light: a car may only proceed on green, and the green → yellow → red sequence is always in order and never jumps straight from red to green.
> - **Why it matters:** It prevents the agent from jumping around between steps, keeping the execution flow always valid and predictable.

### 3.1 Hierarchical State Machine

Think of this as the state machine all grown up: on top of the usual "if this, then go there" moves, it also understands parent-and-child rooms (hierarchical states), friendly bouncers at the door (guards that stop illegal moves), alarm clocks (automatic timeouts), and a cap on how many laps you can run. That makes it steady enough to chauffeur a whole AI coding agent. The code sample below is a little play where our agent walks the hallway IDLE → THINKING → PLANNING → READING_CODE → WRITING_CODE → RUNNING_TESTS → DONE:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-3-1-hierarchical-state-machine.py`](examples/06-3-1-hierarchical-state-machine.py)

</details>

---

## 4. Error Recovery

> **📌 Core Concept**
>
> - **Concept:** Error recovery is the set of strategies for handling what happens when a workflow hits an error — retry with increasing waits (retry/backoff), fall back to an alternative, or cut the circuit as protection (circuit breaker) — so the system stays stable instead of the whole process crashing.
> - **Analogy:** Like making a phone call when the line is busy: try again after a minute (retry), if that fails wait longer (backoff), or dial a second person instead (fallback).
> - **Why it matters:** Errors will happen for sure; with a recovery strategy, the workflow doesn't just die midway.

### 4.1 Retry Strategies

We have all tapped "resend" when the wifi hiccups — this is that same instinct, just done with a little science. You wait a bit longer each time (1s → 2s → 4s) so you do not overwhelm the service, and you sprinkle in a touch of randomness (jitter) so a crowd of clients does not all stampede back at the exact same second. The tiny helper below wraps any function — sync or async — with that patient retry habit:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-4-1-retry-strategies.py`](examples/07-4-1-retry-strategies.py)

</details>

### 4.2 Circuit Breaker Pattern

Think of the fuse box in your home: when too much faulty current rushes in, the fuse pops and cuts the power to save the whole house. Our circuit breaker is that same caring fuse. When a service keeps stumbling past the limit, we flip from CLOSED (calls flowing normally) to OPEN (pause — stop calling for a while); after a short rest we peek through the door in HALF_OPEN to ask, "are you feeling better yet?"

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-4-2-circuit-breaker-pattern.py`](examples/08-4-2-circuit-breaker-pattern.py)

</details>

### 4.3 Saga Pattern

Think of booking a group vacation: hotel booked, insurance paid — then the flights fall through. You do not just walk away; you kindly undo what already worked: refund the hotel, cancel the insurance. That undo-everything-neatly idea is the Saga. For jobs that stretch across many services, every step brings its own "sorry, let me undo that" companion step, so if any stop fails, the whole trip unwinds gracefully:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-4-3-saga-pattern.py`](examples/09-4-3-saga-pattern.py)

</details>

---

## 5. Observability

> **📌 Core Concept**
>
> - **Concept:** Observability is the ability to "see inside" a workflow through three kinds of data — logs (event records), metrics (measurements), and traces (the footprints of each request) — to know exactly what happened at each step.
> - **Analogy:** Like a taxi's dashcam + instrument cluster + GPS map: you know where the car is going, how fast or slow it's moving, and where it's stuck.
> - **Why it matters:** Without observability, when a workflow is slow or wrong you can't find the root cause and you have to debug step by step by feel.

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

Think of tucking a little travel diary onto every request: it gets a unique trace_id at the door, and every service it visits stamps the page (those stamps are called spans — parents and children). Later you can open the diary and replay the whole adventure, spotting exactly where it lingered or tripped:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-5-1-distributed-tracing.py`](examples/10-5-1-distributed-tracing.py)

</details>

### 5.2 Structured Logging + Metrics

Think of a cozy kitchen thermometer plus a notebook: one side (structured logging) jots down every event as tidy JSON you can easily search later, the other side (metrics) keeps the scoreboard — how many runs, how many wins, and how slow the slowest bites were (p50/p95/p99). The sample below gives you both companions, WorkflowLogger and MetricsCollector:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/11-5-2-structured-logging-metrics.py`](examples/11-5-2-structured-logging-metrics.py)

</details>

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

---

## 8. Harness Integration

> **📌 Core Concept**
>
> - **Concept:** Harness integration is the layer that connects the Workflow module to the entire Harness framework — Memory, Guardrails, Tool Execution, Feedback — through unified interfaces so the modules communicate through a common "language".
> - **Analogy:** Like a universal power outlet: any device (module) plugged in fits and works, as long as it follows the interface standard.
> - **Why it matters:** Without standard interfaces, every module invents its own calling convention — integration becomes a tangled mess of wires that's hard to maintain.

### 8.1 TypeScript Interfaces

Think of this as the friendly handshake agreement between the Workflow module and the rest of the Harness family — a short list of promises like createWorkflow, execute, pause, resume, cancel, getTrace, getMetrics. Once everyone agrees on the same handshake, any module knows exactly how to ask the engine for help:

<details>
<summary><b>8.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/14-8-1-typescript-interfaces.ts`](examples/14-8-1-typescript-interfaces.ts)

</details>

---

## 9. Case Studies

> **📌 Core Concept**
>
> - **Concept:** Case studies are practical analyses of how large systems (GitHub Actions, Apache Airflow, Temporal, DeepSeek Harness) design their workflows, so you can distill lessons to apply to your own project.
> - **Analogy:** Like watching a documentary and learning from its lessons: instead of charging headlong into the same pitfall, you learn right away from how those who came before solved the problem.
> - **Why it matters:** Pure theory is hard to picture; learning from real systems shows you which patterns actually work in production conditions.

### 9.1. GitHub Actions — Event-Driven CI/CD

Here is one you have probably met in real life: a short YAML file that runs your CI/CD every time you push or open a pull request. Notice the two friendly ideas living side by side — the doorbell that starts it all (the `on:` trigger) plus polite waiting in line (deploy patiently waits for build, build waits for lint and test):

<details>
<summary><b>9.1. GitHub Actions — Event-Driven CI/CD (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/15-9-1-github-actions-event-driven-ci-cd.yaml`](examples/15-9-1-github-actions-event-driven-ci-cd.yaml)

</details>

**Takeaway**: GitHub Actions is a lovely real-life DAG — a doorbell (event trigger) rings, jobs fan out and wait their turn (dependency resolution), and the whole party flows in order.

### 9.2. Apache Airflow — Data Pipeline Orchestration

Airflow feels like writing a recipe card in plain Python: you simply name your chores (extract, transform, load, validate) and link them with the little `>>` arrows to say who goes first. The whole journey lays out like a subway map on the fridge — easy to read, easy to reshuffle:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-9-2-apache-airflow-data-pipeline-orchestration.py`](examples/16-9-2-apache-airflow-data-pipeline-orchestration.py)

</details>

**Takeaway**: Airflow showed the world why clear "who waits for whom" DAGs became the gold standard for data pipelines — draw the map once, and everyone can follow it.

### 9.3. Temporal — Durable Workflow Execution

Temporal has one big heart-warming promise: your workflow should "survive" even if the server takes a nap halfway through — progress is saved safely (durable), retries happen on their own, and there is always an undo plan. The little story below is a shop order told Saga-style: reserve stock → charge payment → ship order; if shipping stumbles, we gently walk backward and refund:

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

---

### 9.4. DeepSeek Harness — Cordis Micro-Kernel Plugin Architecture

**Context**: DeepSeek Harness uses **Cordis** — a micro-kernel plugin engine designed around the philosophy **"Agent = Model + Harness"** and **"Everything is a plugin"**. Cordis provides a lightweight kernel (~2KB gzipped) that manages the entire agent lifecycle through a plugin system, with dependency injection via a Context service registry.

In plain everyday words: the kernel is a tiny operating system, and each plugin is an app on your phone — every app just says "here is what I need" (consumes) and "here is what I share" (provides), and the phone quietly plugs the wires together so everything starts in the right order.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts`](examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts)

</details>

**Key Architectural Innovations**:

1. ✅ **Micro-Kernel Design** — The kernel is only ~2KB, everything is a plugin. Load on demand, hot-reloadable.

2. ✅ **Lifecycle Management** — 4 phases: `init` → `attach` → `ready` → `detach`. Deterministic startup/shutdown.

3. ✅ **Context Service Registry** — `ctx.provide()` / `ctx.inject()` / `ctx.get()` for dependency injection. Plugins declare `provides`/`consumes` for auto-wiring.

4. ✅ **Event Bus** — Pub/sub for inter-plugin communication. Loose coupling, extensible.

4. ✅ **4 Runtime Modes** (provided by the `runtime-mode` plugin):
   - **Standard** — Full agent, all tools, process isolation
   - **Code** — `@deepseek-ai/dsh` SDK, single-turn, batched, VM sandbox, 70-90% latency reduction
   - **Benchmark** — Minimal (bash + editor only), container isolation, deterministic for SWE-bench
   - **Creator** — Visual timeline, presets, time-travel debugging, fork/replay

5. ✅ **Trajectory Traceability** (by the `trajectory-recorder` plugin):
   - Append-only Session Event Stream
   - `replayToStep()`, `forkSession()`, `resumeSession()`
   - Event search by type, time, step

6. ✅ **Plugin Composition** — DeepSeek Harness = composition of plugins. Easy to swap, extend, test.

**Cordis vs Traditional Frameworks**:

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

---

## 10. Design Principles

> **📌 Core Concept**
>
> - **Concept:** Design principles are the architectural guidelines (including SOLID) applied specifically to workflows — helping you decide how to split steps, organize dependencies, and draw responsibility boundaries in your system.
> - **Analogy:** Like house-building regulations: no one forbids building, but following the building codes makes the house safe, easy to fix, and spared from being torn down and rebuilt.
> - **Why it matters:** Good principles make workflows easy to scale, easy to test, and low in technical debt as the system grows.

### 10.1 SOLID for Workflows

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

---

## 11. Best Practices

> **📌 Core Concept**
>
> - **Concept:** Best practices are the list of things to do (DO) and not do (DON'T) distilled from real experience building workflows for AI Agents.
> - **Analogy:** Like a pilot's pre-flight checklist: everyone knows it by heart, but writing it down and checking it off in sequence is what really makes sure you don't skip a small task with big consequences.
> - **Why it matters:** This is your "trap-avoidance map" — do it right and you save headaches; do it wrong and you invite bugs that are hard to debug.

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

### 11.2 DON'T ❌

- **Don't share mutable state between steps**: Use immutable data passing
- **Don't skip error handling**: Every step can fail
- **Don't use infinite loops**: Always set max iterations
- **Don't ignore timeout**: A hanging step = stuck workflow
- **Don't hardcode step dependencies**: Use DAG configuration
- **Don't skip testing**: Unit test each step independently
- **Don't use blocking calls in parallel steps**: Use async/executor
- **Don't forget compensation logic**: Every forward action needs a rollback

---

## 12. Future

> **📌 Core Concept**
>
> - **Concept:** The Future section sketches the trends in workflow orchestration and agent pipelines for 2026-2028 — AI-generated workflows, serverless engines, cross-platform execution, and real-time adaptive workflows.
> - **Analogy:** Like checking next week's weather forecast: not 100% certain, but enough direction to pick an architecture that won't be obsolete two years from now.
> - **Why it matters:** Knowing the trends helps you invest in the right technology and avoid building something about to be replaced.

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

**4. Real-time Adaptive Workflows**
- Dynamic step adjustment based on runtime metrics
- ML-based bottleneck prediction
- Auto-parallelization

**5. Workflow Observability 2.0**
- AI-powered root cause analysis
- Predictive alerting
- Automated incident response

---

## 13. Production Durability: Checkpoint-Resume, Idempotency, Backpressure, Approvals

### 13.1 Definitions

| Term | Definition |
|------|------------|
| Durable execution | Every step completion is checkpointed (event log + snapshot); restart resumes from last checkpoint, never from zero |
| Idempotency key | `stepId + inputHash (+ attempt ceiling)`; re-execution with same key returns stored result, no double side-effect |
| Backpressure | Bounded queue + semaphore (`maxParallel`), per-run deadline propagated via `AbortSignal`/ctx; shed or defer instead of OOM |
| Approval node | Step with state `WAITING_APPROVAL`; engine pauses, persists, resumes on approve/reject/timeout |

### 13.2 Checkpoint-Resume (Across Restart)

Write-ahead log: `append({seq, stepId, inputHash, status, outputRef})` + atomic snapshot every N steps. On boot: `load snapshot → replay log tail → skip completed (idempotent) → resume pending`. Snapshot to local JSON/SQLite; outputs >64KB go to artifact store by ref. Keep `runId` stable across restarts.

### 13.3 Per-Step Idempotency + Backpressure + Deadlines

Idempotency store: `Map<idempotencyKey, resultRef>` with TTL; mutations require key, reads don't. Backpressure: global `Semaphore(maxParallel=4–8)`, per-step queue cap (e.g. 100); `enqueue` throws `BackpressureError` when full — caller retries with jitter. Deadline: single `deadlineAt` per run; each step gets `remaining = deadlineAt - now()` (minus buffer); propagate via `AbortSignal.timeout(remaining)`. Never extend deadlines silently.

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

<details>
<summary>TypeScript Code — Durable Engine (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-13-4-human-approval-pause-resume-nodes.ts`](examples/18-13-4-human-approval-pause-resume-nodes.ts)

</details>

Resume: re-invoke `run()` with same `runId`; completed keys hit `done()`/store and skip. Pause: catch `PAUSED:*`, persist UI state, approve then re-run.

### 13.5 Checklist

- [ ] Checkpoint after every step (log + snapshot); restart test passes (kill -9 mid-run)?
- [ ] All mutating steps use idempotency keys; double-run is side-effect-free?
- [ ] `maxParallel` + queue cap set; deadline propagated to every step signal?
- [ ] Approval nodes persist `WAITING_APPROVAL`; approve/reject/timeout paths resume correctly?

---

## References

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

### Frameworks

1. **Temporal** - https://temporal.io
2. **Apache Airflow** - https://airflow.apache.org
3. **Prefect** - https://www.prefect.io
4. **GitHub Actions** - https://docs.github.com/en/actions
5. **AWS Step Functions** - https://aws.amazon.com/step-functions/

---

> **Oct-2026 addendum:** want "guards at the doors" for your agent? Read
> [`hooks-standard.md`](./hooks-standard.md). In short: each lifecycle point
> (`preToolUse`, `postToolUse`...) gets a check script — allow, ask a human, or block.

*Document: VII. Workflow — HARNESS ENGINEERING EDITION*
*Last updated: 16/10/2026*
*Author: AI Knowledge Repository*

## October 2026 Update — Production Reliability Patterns (Anthropic 2025)

> **📌 Context:** The three patterns below are distilled from the article *Effective Harnesses for Long-Running Agents* (Anthropic, 2025) — for when the agent is no longer a 5-minute demo but a production system running for hours, deploying continuously, where failure is a given.

### 1. Checkpoint & Resume (no restart)

Agents are **stateful** — state accumulates step by step, so small errors tend to **compound**: a small slip at step 3 creates a big error at step 7. When an error happens, don't run again from scratch — **resume from the latest checkpoint**:

| Component | Role |
|---|---|
| **Checkpoint** | Each completed step saves state (outputs, variables, progress) to durable storage (JSON file, S3, DB) |
| **Resume** | Crash/timeout → load latest checkpoint → skip finished steps → continue |
| **Deterministic retry/backoff** | Transient errors (network, rate limit) → exponential backoff, bounded retries |
| **Model adaptation** | Logic errors → **report tool failure to the agent** so it can adapt (change approach) instead of retrying the same way |

The triage principle: **deterministic problems get retry/backoff; anything requiring judgment goes back to the model** — an agent that can see the error will fix its own strategy; blind mechanical retries cannot.

### 2. Rainbow Deployments

Agents may be **mid-run** when you deploy a new version — cutting them off mid-flight loses state and breaks in-progress tasks. Solution: **shift traffic gradually** from the old version to the new one, keeping both running in parallel:

| Phase | Old version | New version | Notes |
|---|---|---|---|
| 1. Parallel deploy | 100% | 0% | New version stands by, ready to receive tasks |
| 2. Gradual shift | 80% → 50% → 20% | 20% → 50% → 80% | New tasks go to the new version; old tasks run out their lifecycle on the old version |
| 3. Complete | 0% | 100% | Shut down the old version when no task is still running on it |

The key point: **don't kill the old version immediately** — agents running mid-flight on it need to complete fully (drain). Reference: **rainbow deploys in Kubernetes** (Argo Rollouts, Flagger) — weighted routing between versions.

### 3. Sync Bottleneck in Orchestration

Running subagents **synchronously** (the lead waits for each subagent to finish before assigning the next task) is the simplest model — but it creates a serious bottleneck:

- The lead **cannot steer** a subagent mid-run: if the subagent drifts off course, you still have to wait for it to finish before correcting.
- The lead is **blocked** when one subagent is slow: the whole system stalls behind the slowest subagent (waterfall effect).

**Async orchestration** solves throughput, but you must answer 3 hard questions:

| Problem | Question | Solution direction |
|---|---|---|
| **Result coordination** | When do results from many subagents come back, and how are they collected? | Completion queue, callbacks, or barrier sync |
| **State consistency** | Multiple subagents write shared state — how are conflicts handled? | Versioning, optimistic locking, or partitioned write zones |
| **Error propagation** | If one subagent fails, do dependent subagents know? | Cancellation tree + shared error bus |

Pragmatic rule: **sync when there are few subagents and tasks are short** (easier to debug); **async when tasks are long and highly independent** (but invest in the 3 issues above from the start — don't let them become technical debt).

### 4. Python Code — Workflow Runner with Checkpoint/Resume

The code below illustrates the pattern: each completed step saves a checkpoint (JSON), crash → resume from the last checkpoint, retry with exponential backoff, max 3 times:

> 📄 **Example code:** [`examples/19-4-python-code-workflow-runner-with-checkpoint-resume.py`](examples/19-4-python-code-workflow-runner-with-checkpoint-resume.py)

**Key points in the code:**
- `_save()` runs **immediately after** each step finishes — the checkpoint is always fresh, so a crash at step N means the next run only repeats that exact step.
- A fixed `run_id` makes multiple reruns of the same task **share one checkpoint set** — this is exactly what resume means.
- Retry is **deterministic** (fixed backoff formula) for transient errors; when retries run out, the exception is raised so the **agent can notice and adapt** (change approach) rather than retrying forever.

### 5. Cross-Reference

> 📎 **Related:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 2** (Orchestration) + **Section 4.3** (Long-Running Agent Pattern). See also Section 4 (Error Recovery) above for retry/circuit breaker/saga — checkpoint/resume is a complementary layer, not a replacement.

---

*Document: VII. Workflow — HARNESS ENGINEERING EDITION*
*Updated: 26/10/2026*
*Author: AI Knowledge Repository*
