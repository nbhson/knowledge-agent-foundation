# 📋 VIII. Task

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Task Classification](#1-task-classification)
>   - [1.1 Coding Task Classification](#11-coding-task-classification)
>   - [1.2 Task Classification Engine](#12-task-classification-engine)
>   - [1.3 Decision Tree: Choosing Task Handling Strategy](#13-decision-tree-choosing-task-handling-strategy)
> - [2. Task Decomposition](#2-task-decomposition)
>   - [2.1 Task Decomposition Patterns](#21-task-decomposition-patterns)
>   - [2.2 Task Decomposer](#22-task-decomposer)
> - [3. Priority & Scheduling](#3-priority-&-scheduling)
>   - [3.1 Priority Model](#31-priority-model)
> - [4. Task State Management](#4-task-state-management)
>   - [4.1 Task Lifecycle](#41-task-lifecycle)
>   - [4.2 Task State Manager](#42-task-state-manager)
> - [5. Dependency Management](#5-dependency-management)
>   - [5.1 Task Dependency Graph](#51-task-dependency-graph)
> - [6. Task Templates](#6-task-templates)
>   - [6.1 Common Task Templates](#61-common-task-templates)
> - [7. Estimation Techniques](#7-estimation-techniques)
>   - [7.1 Token Estimation Model](#71-token-estimation-model)
>   - [7.2 Effort Estimation Algorithm](#72-effort-estimation-algorithm)
> - [8. Anti-Patterns & Solutions](#8-anti-patterns-&-solutions)
>   - [8.1 Common Anti-Patterns](#81-common-anti-patterns)
>   - [8.2 Anti-Pattern Detector](#82-anti-pattern-detector)
> - [9. Real-World Workflows](#9-real-world-workflows)
>   - [9.1 Feature Implementation Workflow](#91-feature-implementation-workflow)
>   - [9.2 Debug Investigation Workflow](#92-debug-investigation-workflow)
>   - [9.3 Refactoring Workflow](#93-refactoring-workflow)
> - [10. Token Budget Management](#10-token-budget-management)
>   - [10.1 Context Window Budget Allocation](#101-context-window-budget-allocation)
>   - [10.2 Token Budget Manager](#102-token-budget-manager)
> - [Best Practices](#best-practices)
> - [References](#references)
>
---

### Opening Story

Imagine you just started as the **front-desk manager of a busy neighborhood clinic**. The doors open and in they come: someone clutching their stomach in pain, someone here for a routine checkup, a kid waiting for a quick vaccination. If you **skip triage** and ask the emergency case to wait behind the routine exam — well, you can feel how quickly that morning turns into a **mess**.

**AI Agents face the same problem without Task Management.**

Now swap the clinic for an AI agent, and the patients for a big request like *"Refactor the auth module, add tests, update docs, then deploy."* The agent hears **everything in one breath** — but where should it begin? What matters most? What can happen side by side? Without a plan, you get jumbled work, skipped steps, or worst of all — **shipping code nobody ever tested**.

**The friendly fix**: Structured Task Management — think of it as the clinic's calm triage nurse. It sorts, ranks, breaks down, and keeps an eye on every job, so the agent always does **the right thing, at the right time, in the right order**.

### Why Is Task Management Important?

> *"An agent that doesn't manage tasks is like a chef who takes on 100 dishes at once — accepts all of them but can't cook fast enough, so every dish turns out bad."*

#### 3 Scientific Evidence

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **Anthropic (2025)** | Task decomposition reduces **40% completion time** and **55% error rate** on complex coding tasks |
| 2 | **OpenAI (2025)** | Structured task tracking improves **35% accuracy** in multi-step reasoning compared to unstructured approaches |
| 3 | **Microsoft Research (2024)** | Task prioritization frameworks reduce **30% resource waste** in AI-assisted development workflows |

#### Core philosophy:

```
Task = Analyze → Classify → Prioritize → Decompose → Execute → Track → Report
```

**Analogy**: Task management is like running a hospital — triage patients (classify), prioritize emergencies (prioritize), prescribe treatment (plan), monitor the cure (track), and discharge (complete).

**If skipped**: The agent gets overwhelmed by too many tasks, delivers in the wrong order, wastes compute resources, and frustrates the user.

## Overview

> ## 📌 Basic Concept
>
> **Concept:** Task Management in AI coding is the process of classifying, decomposing, prioritizing, and tracking programming tasks so the agent does the right thing, at the right time, in the right order.
>
> **Analogy:** It's like managing a busy hospital — emergency cases must come first, routine appointments come later, and shifts must be clearly organized so no patient is overlooked.
>
> **Why it matters:** Without task management, the agent easily gets overloaded, works in the wrong order, and wastes resources.

**Task Management** in AI coding is just the habit of **sorting, slicing, ranking, and watching** your coding chores. Done well, it helps your agent focus on the right job, skip the overwhelm, and deliver work you can trust.

```
┌──────────────────────────────────────────────────────────────────┐
│                         TASK MANAGEMENT                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Input   │    │  Parse & │    │  Task    │            │  │
│  │  │  Request │───►│  Classify│───►│  Queue   │            │  │
│  │  └──────────┘    └──────────┘    └────┬─────┘            │  │
│  │                                        │                   │  │
│  │       ┌────────────────────────────────┘                   │  │
│  │       ▼                                                    │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Plan &  │    │  Execute │    │  Validate│            │  │
│  │  │  Assign  │───►│  & Track │───►│  & Close │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Contents

> ## 📌 Basic Concept
>
> **Concept:** This is the table of contents of the whole module — the ten main topics of Task Management, presented from task recognition (classification, decomposition), management (priority, state, dependencies), to resource management (estimation, token budget).
>
> **Analogy:** Like a metro line map — looking ahead you know which stations there are and where to get off for your destination.
>
> **Why it matters:** Each topic solves a part of the same problem, so grasping the whole makes it easier to know what to learn.

| # | Topic | Description |
|---|--------|-------|
| 1 | [Task Classification](#1-task-classification) | Classify tasks by type |
| 2 | [Task Decomposition](#2-task-decomposition) | Break large tasks into small ones |
| 3 | [Priority & Scheduling](#3-priority-&-scheduling) | Prioritize and schedule |
| 4 | [Task State Management](#4-task-state-management) | Manage task state |
| 5 | [Dependency Management](#5-dependency-management) | Manage dependencies between tasks |
| 6 | [Task Templates](#6-task-templates) | Common task templates |
| 7 | [Estimation Techniques](#7-estimation-techniques) | Task estimation techniques |
| 8 | [Anti-Patterns & Solutions](#8-anti-patterns-&-solutions) | Common mistakes |
| 9 | [Real-World Workflows](#9-real-world-workflows) | Real-world processes |
| 10 | [Token Budget Management](#10-token-budget-management) | Manage token budget |

---

## 1. Task Classification

> ## 📌 Basic Concept
>
> **Concept:** Task Classification is the "diagnosis" step before handling a task — read the request, identify which type of task it is (new code, bug fix, refactor, writing tests, etc.) and how complex it is (one file or a whole module), then pick an appropriate strategy.
>
> **Analogy:** Like an ER doctor triaging patients before treatment — a correct diagnosis leads to the right treatment; a wrong one throws every subsequent step off.
>
> **Why it matters:** Classifying correctly lets the agent pick the right approach, saving tokens and reducing mistakes from the start.

### 1.1 Coding Task Classification

Think of the picture below as the clinic's department directory with 5 friendly wings — writing new code, changing code, studying code, writing docs, and testing. Start at the top, follow the little branch that sounds like your job, and you will land exactly where your task belongs.

```
┌──────────────────────────────────────────────────────────────────┐
│                    TASK TYPE HIERARCHY                            │
│                                                                  │
│  Code Generation                                                 │
│  ├── New Feature        → Create a new feature                   │
│  ├── Code Snippet       → Create a short code snippet            │
│  ├── Boilerplate        → Create a template                      │
│  └── API Endpoint       → Create a REST/GraphQL endpoint         │
│                                                                  │
│  Code Modification                                               │
│  ├── Refactor           → Improve code structure                 │
│  ├── Bug Fix            → Fix bugs                               │
│  ├── Optimization       → Optimize performance                   │
│  └── Migration          → Move code/platform                     │
│                                                                  │
│  Code Analysis                                                   │
│  ├── Code Review        → Assess code quality                    │
│  ├── Debugging          → Find the root cause of bugs            │
│  ├── Profiling          → Analyze performance                    │
│  └── Security Audit     → Check for security issues              │
│                                                                  │
│  Documentation                                                   │
│  ├── README             → Project documentation                  │
│  ├── API Docs           → API documentation                      │
│  ├── Comments           → Inline comments                        │
│  └── Changelog          → Change history                         │
│                                                                  │
│  Testing                                                         │
│  ├── Unit Test          → Unit-level tests                       │
│  ├── Integration Test   → Integration tests                      │
│  ├── E2E Test           → End-to-end tests                       │
│  └── Test Fixtures      → Test data                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Task Classification Engine

Here is the little receptionist brain that does the sorting: you hand it a plain-English request, it listens for clue words (spot "fix" or "bug" and it thinks, "ah, MODIFICATION"), guesses how big the job is, and hands you back a tidy Task card. Go ahead and try it with any sentence — it is fun to watch the agent "get" what you mean.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-2-task-classification-engine.py`](examples/01-1-2-task-classification-engine.py)

</details>

### 1.3 Decision Tree: Choosing Task Handling Strategy

Think of the flowchart below as the receptionist's cheat sheet. A new task walks in: if the request is fuzzy, ask a kind clarifying question first; if it is tiny (under ~500 tokens), just do it on the spot; if it is big, split it into bite-size pieces and then pick your style — one-by-one, side-by-side, or test-first (TDD). Just follow the arrows down and you will see which door each task walks through.

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK HANDLING DECISION TREE                          │
│                                                                  │
│  Task arrived                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐     YES    ┌──────────────────┐                │
│  │ Is it clear? │──────────►│ Can be done in   │                │
│  │ (clear scope)│          │ < 500 tokens?     │                │
│  └──────┬──────┘          └────────┬─────────┘                  │
│         │ NO                       │ YES        NO               │
│         ▼                          ▼            ▼                │
│  ┌──────────────┐         ┌────────────┐  ┌──────────────┐     │
│  │  Clarify     │         │  Execute   │  │  Decompose   │     │
│  │  requirements│         │  directly  │  │  into sub-   │     │
│  │  first       │         │  (1 shot)  │  │  tasks       │     │
│  └──────────────┘         └────────────┘  └──────┬───────┘     │
│                                                   │              │
│                                    ┌──────────────┼──────────┐  │
│                                    ▼              ▼          ▼  │
│                             ┌──────────┐  ┌──────────┐ ┌────┐ │
│                             │Sequential│  │ Parallel │ │TDD │ │
│                             │ Pipeline │  │ Fan-out  │ │    │ │
│                             └──────────┘  └──────────┘ └────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Task Decomposition

> ## 📌 Basic Concept
>
> **Concept:** Task Decomposition is the technique of splitting a large, unwieldy task into many smaller sub-tasks, each with nearly independent input/output that can be delegated to a suitable agent for separate handling.
>
> **Analogy:** Like building a house — no one pours an entire house at once; the foundation, frame, and roof are each laid in stages; each stage is a small, controllable job.
>
> **Why it matters:** Large tasks easily make the agent lose context and miss steps; breaking them down reduces context load and raises the probability of completion.

### 2.1 Task Decomposition Patterns

The sketch below lays out 6 everyday ways to slice a big cake into servable pieces. Some slices must be eaten in order (sequential), some can be shared out and gathered back together (parallel, map-reduce), and some stack like a family tree (parent-child). Glance at the arrows and pick the slicing style that matches your appetite today.

```
┌──────────────────────────────────────────────────────────────────┐
│               TASK DECOMPOSITION PATTERNS                         │
│                                                                  │
│  Pattern 1: SEQUENTIAL DECOMPOSITION                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ Parent   │───►│ Sub 1    │───►│ Sub 2    │───► ...          │
│  │ Task     │    │ (must    │    │ (needs   │                   │
│  │          │    │  finish) │    │  sub 1)  │                   │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                                                  │
│  Pattern 2: PARALLEL DECOMPOSITION                              │
│  ┌──────────┐    ┌──────────┐                                  │
│  │ Parent   │───►│ Sub A    │ ─┐                                │
│  │ Task     │    │ (indep.) │   │    ┌──────────┐              │
│  │          │    ├──────────┤   ├───►│  Merge   │              │
│  │          │───►│ Sub B    │ ─┤    │  Results │              │
│  │          │    │ (indep.) │   │    └──────────┘              │
│  │          │    ├──────────┤   │                               │
│  │          │───►│ Sub C    │ ─┘                                │
│  │          │    │ (indep.) │                                   │
│  └──────────┘    └──────────┘                                  │
│                                                                  │
│  Pattern 3: HIERARCHICAL DECOMPOSITION                          │
│  ┌──────────┐                                                   │
│  │ Epic     │                                                   │
│  └────┬─────┘                                                   │
│       ├── Feature 1                                             │
│       │    ├── Sub-task 1.1                                     │
│       │    └── Sub-task 1.2                                     │
│       └── Feature 2                                             │
│            ├── Sub-task 2.1                                     │
│            ├── Sub-task 2.2                                     │
│            └── Sub-task 2.3                                     │
│                                                                  │
│  Pattern 4: MAP-REDUCE DECOMPOSITION                            │
│  ┌──────────┐    ┌──────────────────────────────┐              │
│  │ Input    │───►│ MAP: Process each item in    │              │
│  │ Data     │    │       parallel                │              │
│  │          │    ├──────────────────────────────┤              │
│  │          │    │ REDUCE: Combine results       │──► Output    │
│  └──────────┘    └──────────────────────────────┘              │
│                                                                  │
│  Pattern 5: SPIKE-THEN-EXECUTE                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  Spike   │───►│ Research │───►│ Execute  │                 │
│  │ (timebox)│    │ & Decide │    │ with     │                  │
│  │ 1-2 hrs  │    │ approach │    │ confidence│                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                                                  │
│  Pattern 6: VERTICAL SLICE                                      │
│  ┌──────────────────────────────────────────┐                  │
│  │  Full Stack Feature (thin slice)         │                  │
│  │  DB → API → Service → UI → Test          │                  │
│  │  Each slice = working increment          │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Task Decomposer

Here is the friendly kitchen helper that does the slicing for you: hand the TaskDecomposer your big Task, and it picks a slicing style (by feature, by layer, by file, test-first, thin vertical slice, or quick research spike). Out comes a neat to-do list of SubTasks — in order, with dependencies, token guesses, and a little "how do I know I am done?" note on each. Not sure which style fits? It happily suggests one based on your task's shape and size.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-2-2-task-decomposer.py`](examples/02-2-2-task-decomposer.py)

</details>

---

## 3. Priority & Scheduling

> ## 📌 Basic Concept
>
> **Concept:** Priority & Scheduling is the mechanism that decides which task to do first and which to defer, based on urgency, importance, required effort, and token consumption.
>
> **Analogy:** Like triage at a hospital — the emergency case goes in first, routine checkups wait; small, high-value jobs (quick wins) also get priority, like paying off a small debt to free up funds.
>
> **Why it matters:** The wrong order delays important work, wastes tokens, and easily misses user requirements.

### 3.1 Priority Model

Here is how the clinic decides who goes first — with a classic Eisenhower-style scorecard. Every task gets marks for urgency, importance, and effort, plus a little gold star if it is a quick win or if many other jobs are waiting on it. The TaskScheduler then lines everyone up into calm, orderly batches that respect your token budget for the session.

In plain coffee-chat terms: urgent-and-important jumps to the front, big-but-patient waits its turn, and tiny easy wins get fast-tracked just to clear the desk and build momentum.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-3-1-priority-model.py`](examples/03-3-1-priority-model.py)

</details>
---

## 4. Task State Management

> ## 📌 Basic Concept
>
> **Concept:** Task State Management is how you track the lifecycle of each task through states like pending, running, blocked, done — plus a mechanism to persist and restore state so you always know "where the work stopped" when interrupted.
>
> **Analogy:** Like a hospital shift log — every incoming shift reads it to learn what was reported, where each patient stands, and continues from there instead of asking everything from the start.
>
> **Why it matters:** If you don't know which state a task is in, the agent can't resume after an interruption and easily repeats or skips steps.

### 4.1 Task Lifecycle

Picture the life story of a task, from first hello to happy goodbye: PENDING → PLANNING → IN_PROGRESS → TESTING → REVIEW → DONE. Along the way there are a few side roads — BLOCKED (uh oh, wait a moment), FAILED (oops, let's try again), CANCELLED (never mind). Just follow the arrows to see which doors legally open from each room.

In everyday ward-talk: a newborn task waits in the lobby (PENDING), sees the doctor for a plan (PLANNING), gets treatment (IN_PROGRESS), visits the lab (TESTING), gets a second opinion (REVIEW), then happily goes home (DONE).

```
┌──────────────────────────────────────────────────────────────────┐
│                    TASK LIFECYCLE                                 │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ PENDING  │───►│ PLANNING │───►│IN_PROG...│                  │
│  │          │    │          │    │          │                  │
│  │ Not      │    │ Planning │    │ Working  │                  │
│  │ started  │    │          │    │          │                  │
│  └──────────┘    └──────────┘    └────┬─────┘                  │
│                                       │                         │
│                    ┌──────────────────┤                         │
│                    ▼                  ▼                         │
│              ┌──────────┐    ┌──────────┐                      │
│              │BLOCKED   │    │ TESTING  │                      │
│              │          │    │          │                      │
│              │ Blocked  │    │ Testing  │                      │
│              └────┬─────┘    └────┬─────┘                      │
│                   │              │                              │
│                   ▼              ▼                              │
│              ┌──────────┐    ┌──────────┐                      │
│              │PENDING   │    │ REVIEW   │                      │
│              │(retry)   │    │          │                      │
│              └──────────┘    └────┬─────┘                      │
│                                  │                              │
│                    ┌─────────────┼─────────────┐                │
│                    ▼             ▼             ▼                │
│              ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│              │  DONE    │  │  FAILED  │  │CANCELLED │         │
│              │          │  │          │  │          │          │
│              │ Complete │  │ Failed   │  │Canceled  │          │
│              └──────────┘  └──────────┘  └──────────┘         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Task State Manager

Here is the ward's trusty logbook keeper: TaskStateManager writes down every move each task makes, only allows legal moves (no sneaky shortcuts), and notes start times, try counts, and the last oopsie — while ringing a little bell (events) so the rest of the team can react. Try an illegal hop like TESTING → PENDING and it kindly but firmly says "nope" — just like a good hospital rule.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-4-2-task-state-manager.py`](examples/04-4-2-task-state-manager.py)

</details>

---

## 5. Dependency Management

> ## 📌 Basic Concept
>
> **Concept:** Dependency Management is the way of modeling "this task must finish before that task" relationships with a dependency graph, from which you derive the correct execution order and detect deadlocks.
>
> **Analogy:** Like the cooking order for a multi-dish meal — you must simmer the soup first, stir-fry later, because one dish needs ingredients from another; doing it backwards ruins the whole meal.
>
> **Why it matters:** The wrong order, or two tasks waiting on each other forever, will make the agent deadlock and never complete.

### 5.1 Task Dependency Graph

Here is a small traffic manager built on a DAG (just a fancy word for "a map with no roundabouts"). Reading it is easy: "A → B" simply means "please finish A before starting B." This helper spots traffic jams (cycles), works out who goes first (topological sort), and groups independent jobs so they can cruise side by side.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-5-1-task-dependency-graph.py`](examples/05-5-1-task-dependency-graph.py)

</details>

---

## 6. Task Templates

> ## 📌 Basic Concept
>
> **Concept:** Task Templates are ready-made patterns for each familiar task type (bug fixes, new features, refactoring, etc.) — a step list, token estimates, and completion criteria — so the agent doesn't have to start from scratch every time it meets the same kind of job.
>
> **Analogy:** Like a pre-filled form at a clinic — the necessary fields are already there, you just fill in the data and it's usable, without worrying about missing items.
>
> **Why it matters:** Using templates makes the agent work faster, more consistently, and with fewer forgotten steps than working freely.

### 6.1 Common Task Templates

Think of the snippet below as a box of well-loved recipe cards: one card each for bug_fix, new_feature, code_review, refactor, debug_investigation, performance_optimization, and migration. Every card lists the steps, a token guess for each step, and the full-meal total. The little `create_task_from_template` helper just asks for the card's name, fills in your details, and hands you a ready-to-cook Task.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-6-1-common-task-templates.py`](examples/06-6-1-common-task-templates.py)

</details>

---

## 7. Estimation Techniques

> ## 📌 Basic Concept
>
> **Concept:** Estimation Techniques are methods of predicting the execution cost of a task in advance — how many tokens, how much time — based on complexity, task type, and experience from previous runs.
>
> **Analogy:** Like a builder quoting before taking a job — looking at the blueprint (task) you immediately estimate how much material and how many days it will take, so the owner doesn't worry about running out of budget halfway.
>
> **Why it matters:** Estimating correctly helps plan resources and warn early before the context window overflows.

### 7.1 Token Estimation Model

Think of the table below as the menu prices at your favorite café: find your task type (bug fix, new feature, migration…), peek at the complexity, and the Estimated Tokens column tells you roughly what the bill looks like. The footer adds handy rules of thumb (a line of code sips about 5–10 tokens) plus a sample budget for a 128K context window.

```
┌──────────────────────────────────────────────────────────────────┐
│              TOKEN ESTIMATION GUIDE                               │
│                                                                  │
│  Task Type              │ Estimated Tokens │ Notes              │
│  ───────────────────────┼──────────────────┼───────────────────│
│  Bug Fix (simple)       │ 1,000 - 3,000    │ Single file       │
│  Bug Fix (complex)      │ 3,000 - 8,000    │ Multi-file        │
│  New Feature (small)    │ 3,000 - 6,000    │ 1-2 files         │
│  New Feature (large)    │ 6,000 - 15,000   │ 3-5 files         │
│  Refactor (simple)      │ 2,000 - 5,000    │ Rename, extract   │
│  Refactor (complex)     │ 5,000 - 12,000   │ Restructure       │
│  Code Review            │ 2,000 - 5,000    │ Per PR            │
│  Write Tests            │ 2,000 - 6,000    │ Unit + edge cases │
│  Documentation          │ 1,000 - 3,000    │ README, API docs  │
│  Debug Investigation    │ 3,000 - 10,000   │ Investigation     │
│  Migration              │ 5,000 - 20,000   │ Data + code       │
│                                                                  │
│  Context Window Budget (128K model):                             │
│  ├── System prompt:     ~5K tokens                              │
│  ├── Project context:   ~30K tokens                             │
│  ├── Task context:      ~20K tokens                             │
│  ├── Working memory:    ~50K tokens                             │
│  └── Reserve:           ~23K tokens (safety buffer)             │
│                                                                  │
│  Rules of Thumb:                                                 │
│  • 1 LOC ≈ 5-10 tokens (code)                                   │
│  • 1 line of comment ≈ 8-12 tokens                              │
│  • 1 function definition ≈ 20-50 tokens                         │
│  • 1 class definition ≈ 50-100 tokens                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 7.2 Effort Estimation Algorithm

Meet your friendly cost estimator: EffortEstimator glances at your Task, picks a starting price (BASE_TOKENS) from its size, adjusts it for the kind of work (writing docs costs less than brand-new code, for example), adds a small fee per file touched — and out pops a token guess, a rough time estimate (about 100 tokens a minute), plus a tidy batch summary.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-7-2-effort-estimation-algorithm.py`](examples/07-7-2-effort-estimation-algorithm.py)

</details>
---

## 8. Anti-Patterns & Solutions

> ## 📌 Basic Concept
>
> **Concept:** Anti-Patterns are mistaken task-handling habits that are very easy to fall into — e.g., tasks that are too big, vague descriptions, tasks whose scope changes mid-flight — along with corrective solutions and an automated detector.
>
> **Analogy:** Like a clinic's list of "common diseases" — each disease has identifying symptoms and a prescription, so you know which one you have and can treat it correctly.
>
> **Why it matters:** Recognizing anti-patterns early avoids most of the most expensive failures when running an agent.

### 8.1 Common Anti-Patterns

Think of the poster below as the clinic's "watch out for these 8 common colds" chart. Each cold gets a ❌ ANTI-PATTERN label, a list of tell-tale sniffles, and a → SOLUTION prescription right beside it. Feeling a symptom in your own task? Just look it up and take the remedy.

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK MANAGEMENT ANTI-PATTERNS                        │
│                                                                  │
│  ❌ ANTI-PATTERN 1: KILLER TASK                                  │
│     Task too large (> 20K tokens), spans many features          │
│     → SOLUTION: Decompose into sub-tasks < 5K tokens each       │
│                                                                  │
│  ❌ ANTI-PATTERN 2: AMBIGUOUS TASK                               │
│     Task description is vague: "improve the code"                │
│     → SOLUTION: Add specific acceptance criteria                │
│                                                                  │
│  ❌ ANTI-PATTERN 3: TASK CHURN                                    │
│     Task keeps changing scope mid-execution                      │
│     → SOLUTION: Lock scope, create new task for changes         │
│                                                                  │
│  ❌ ANTI-PATTERN 4: DEPENDENCY DEADLOCK                          │
│     Task A waits for B, B waits for A → never finishes          │
│     → SOLUTION: Cycle detection + forced break                  │
│                                                                  │
│  ❌ ANTI-PATTERN 5: CONTEXT DRIFT                                │
│     Task runs too long → agent forgets original intent           │
│     → SOLUTION: Timebox tasks, refresh context periodically     │
│                                                                  │
│  ❌ ANTI-PATTERN 6: MISSING ACCEPTANCE CRITERIA                  │
│     Task done but no way to know it meets the requirements      │
│     → SOLUTION: Every task must have a "definition of done"     │
│                                                                  │
│  ❌ ANTI-PATTERN 7: OVER-DECOMPOSITION                           │
│     Split too small → overhead > benefit                         │
│     → SOLUTION: Minimum 500 tokens per sub-task                  │
│                                                                  │
│  ❌ ANTI-PATTERN 8: IGNORING TOKEN BUDGET                        │
│     Task estimated at 5K tokens but context window has only 3K  │
│     → SOLUTION: Always check token budget before starting        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Anti-Pattern Detector

Think of this as the checkup machine at the clinic door: AntiPatternDetector gives your Task a quick once-over — too big? too vague? missing a cost guess? tangled in too many dependencies? — and hands you a gentle report with severity levels and "here is how to feel better" tips. Run it before you start, like washing your hands.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-8-2-anti-pattern-detector.py`](examples/08-8-2-anti-pattern-detector.py)

</details>

---

## 9. Real-World Workflows

> ## 📌 Basic Concept
>
> **Concept:** Real-World Workflows are standardized processes for real coding situations — adding features, investigating bugs, refactoring — that bundle all the task management lessons above into clearly ordered steps.
>
> **Analogy:** Like a pilot's flight checklist — no need to think through each step while things are tense; just follow the list and nothing gets missed.
>
> **Why it matters:** Having a ready-made workflow lets the agent handle real work in a disciplined way, with fewer mistakes and easier quality control.

### 9.1 Feature Implementation Workflow

The diagram below describes the new-feature process in 4 phases: UNDERSTAND → PLAN → IMPLEMENT → VERIFY. Each phase is a box containing specific jobs (reading requirements, finding similar code, estimating tokens, etc.). Follow the phase order exactly, like following a recipe — prepare the ingredients before you start cooking.

```
┌──────────────────────────────────────────────────────────────────┐
│           FEATURE IMPLEMENTATION WORKFLOW                         │
│                                                                  │
│  Phase 1: UNDERSTAND (5-10 min)                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Read requirements/spec                              │     │
│  │ 2. Search existing code for similar features           │     │
│  │ 3. Identify affected files and modules                 │     │
│  │ 4. Check for existing patterns to follow               │     │
│  │ 5. Ask clarifying questions if needed                  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 2: PLAN (5-10 min)                                        │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Design the approach (which files to change)         │     │
│  │ 2. Identify risks and edge cases                       │     │
│  │ 3. Estimate token budget                               │     │
│  │ 4. Create sub-task list with dependencies              │     │
│  │ 5. Choose decomposition strategy                       │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 3: IMPLEMENT (variable)                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Start with data models / types                      │     │
│  │ 2. Implement core business logic                       │     │
│  │ 3. Add API/interface layer                             │     │
│  │ 4. Add error handling                                  │     │
│  │ 5. Write tests (TDD if complex)                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 4: VERIFY (5-10 min)                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Run linter (flake8, ruff)                           │     │
│  │ 2. Run type checker (mypy)                             │     │
│  │ 3. Run tests (pytest)                                  │     │
│  │ 4. Check for regressions                               │     │
│  │ 5. Verify acceptance criteria met                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Debug Investigation Workflow

The diagram below is the bug investigation and fixing process with 5 steps: REPRODUCE → INVESTIGATE → HYPOTHESIZE → FIX → PREVENT. The key point is stopping to verify the hypothesis before rushing to fix — avoiding blindly patching until the bug disappears.

```
┌──────────────────────────────────────────────────────────────────┐
│             DEBUG INVESTIGATION WORKFLOW                          │
│                                                                  │
│  Step 1: REPRODUCE                                                │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Get exact error message and stack trace              │     │
│  │ • Find minimal reproduction steps                      │     │
│  │ • Note environment details (OS, versions, config)      │     │
│  │ • Check if intermittent or consistent                  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 2: INVESTIGATE                                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Read stack trace → identify entry point              │     │
│  │ • Search for error message in codebase                 │     │
│  │ • Read affected code top-to-bottom                     │     │
│  │ • Check recent git changes (git log --oneline -20)     │     │
│  │ • Add debug logging if needed                          │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 3: HYPOTHESIZE                                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Form hypothesis: "The bug is in X because Y"        │     │
│  │ • Test hypothesis with minimal code change             │     │
│  │ • If wrong, form new hypothesis and repeat             │     │
│  │ • Track hypotheses tried (avoid cycling)               │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 4: FIX                                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Implement minimal fix (not over-engineer)            │     │
│  │ • Verify fix resolves the original issue               │     │
│  │ • Check fix doesn't break other functionality          │     │
│  │ • Add regression test                                  │     │
│  │ • Document root cause in commit message                │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 5: PREVENT                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Add type hints to prevent similar type errors        │     │
│  │ • Add input validation if applicable                   │     │
│  │ • Consider if similar bugs exist elsewhere             │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.3 Refactoring Workflow

The diagram below is a safe refactoring process in 5 steps: characterize the current behavior, identify code smells, plan small steps, apply the refactoring, then verify. The golden rule is written right at the top of the diagram: don't refactor and add features at the same time, and run the tests after each step to make sure behavior hasn't changed.

```
┌──────────────────────────────────────────────────────────────────┐
│              REFACTORING WORKFLOW                                  │
│                                                                  │
│  ⚠️ RULE: Never refactor AND add features at the same time      │
│                                                                  │
│  Step 1: CHARACTERIZE CURRENT BEHAVIOR                           │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Ensure existing tests pass                           │     │
│  │ • If no tests → write characterization tests first     │     │
│  │ • Document current behavior (even if wrong)            │     │
│  │ • Take "before" snapshots (metrics, benchmarks)        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 2: IDENTIFY CODE SMELLS                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Long methods (> 30 lines)                            │     │
│  │ • Large classes (> 300 lines)                          │     │
│  │ • Duplicate code (> 3 similar blocks)                  │     │
│  │ • Deep nesting (> 3 levels)                            │     │
│  │ • God objects (doing too many things)                  │     │
│  │ • Feature envy (method uses other class's data more)   │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 3: PLAN REFACTORING STEPS                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Order refactoring steps from least to most risky     │     │
│  │ • Each step should be small and testable               │     │
│  │ • Run tests after EACH step                            │     │
│  │ • Commit after each successful step                    │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 4: APPLY REFACTORING (Small Steps)                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Extract Method / Extract Class                       │     │
│  │ • Rename for clarity                                   │     │
│  │ • Move methods to correct classes                      │     │
│  │ • Replace conditional with polymorphism                │     │
│  │ • Remove dead code                                     │     │
│  │ • Simplify conditional expressions                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 5: VERIFY                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • All tests still pass?                                │     │
│  │ • Behavior unchanged? (characterization tests)         │     │
│  │ • Metrics improved? (LOC, complexity, readability)     │     │
│  │ • No performance regression?                           │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Token Budget Management

> ## 📌 Basic Concept
>
> **Concept:** Token Budget Management is the strategy of dividing and controlling the token budget inside the context window — how much for the system prompt, project context, task context, and working memory — so you never hit the ceiling and run out of room to answer.
>
> **Analogy:** Like a shopping wallet — you know the total amount you have, how much to spend on each item, and always keep a reserve so you don't stop mid-way from an unexpected shortage.
>
> **Why it matters:** Overflowing the context window is one of the most fatal mistakes when running an agent — token budget prevents it up front.

### 10.1 Context Window Budget Allocation

The diagram below shows the token budget of a 128K context window split into 4 boxes: System Prompt (fixed), Project Context, Task Context, and Working Memory, plus a Reserve for safety. Read the token column on the right to see how much each box takes. Pay special attention to the warning at the bottom of the diagram: when the budget drops below 20%, summarize or clean up the context immediately.

```
┌──────────────────────────────────────────────────────────────────┐
│           TOKEN BUDGET ALLOCATION (128K context window)          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  System Prompt (fixed)              │  ~5,000 tokens  │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Project Context (dynamic)          │  ~30,000 tokens │     │
│  │  • File structure                   │  ~2,000         │     │
│  │  • Key code files                   │  ~20,000        │     │
│  │  • Config files                     │  ~3,000         │     │
│  │  • Documentation                    │  ~5,000         │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Task Context (dynamic)             │  ~20,000 tokens │     │
│  │  • Task description                 │  ~1,000         │     │
│  │  • Related code                     │  ~15,000        │     │
│  │  • Error logs                       │  ~4,000         │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Working Memory (growing)           │  ~50,000 tokens │     │
│  │  • Generated code                   │  ~30,000        │     │
│  │  • Intermediate results             │  ~10,000        │     │
│  │  • Tool outputs                     │  ~10,000        │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Reserve (safety buffer)            │  ~23,000 tokens │     │
│  │  • Response generation              │  ~15,000        │     │
│  │  • Overflow protection              │  ~8,000         │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ⚠️ When budget < 20% remaining:                                │
│     1. Summarize older context                                   │
│     2. Remove non-essential files from context                  │
│     3. Complete current sub-task, then start fresh               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.2 Token Budget Manager

This is the budget management code: TokenBudgetManager holds the total limit, allocates tokens to tasks via allocate_for_task (returns False if there's not enough "money"), tracks the usage ratio (usage_percent), prints a "wallet" status summary with summarize_context, and suggests cleanup methods when the context is nearly full. In short, this is the system's treasurer.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-10-2-token-budget-manager.py`](examples/09-10-2-token-budget-manager.py)

</details>

---

## 11. Harness Integration (TS)

Links tasks to the execution spine: every `TaskNode` carries `trajectoryId`, `idempotencyKey`, `permissions`, `budget`. The engine emits events the workflow/observability layers consume.

<details>
<summary>TypeScript Code — Task Engine (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-11-harness-integration-ts.ts`](examples/10-11-harness-integration-ts.ts)

</details>

Rules: `elevated` tasks require approval; `trajectoryId` joins prompt/tool/workflow logs; `idempotencyKey` dedupes retries.

## 12. Execution Semantics

Per-task: `timeoutMs` (default 60s, abort + mark `failed:timeout`), `maxRetries` with exponential backoff + jitter (retry only idempotent or checkpointed tasks), `cancel()` sets `cancelled` and aborts signal — children depending on it become `blocked`. Failure pipeline: `failed → classify(transient|perm|budget) → transient: retry | perm: park + emit task.failed | budget: compact + re-estimate → continue DAG`. Never auto-retry non-idempotent writes.

## 13. Concurrency

Scheduler: topological batches (ready = deps all `done`), semaphore cap (4–8) + token-budget gate (skip batch if `sum(budgetTokens) > remaining`). `race([primary, fallback])` for latency-sensitive reads; `join(all)` for fan-in merges. Resource limits: max tasks/run (e.g. 50), max tokens/session, per-task queue depth 1. Deadlock guard: fail if a batch makes no progress in 2 rounds (missing dep/cycle).

## 14. Case Studies

1. **Auth refactor (12 files, 4 layers):** classified MODIFICATION/COMPLEX → layer decomposition (db→svc→api→ui→test). Batch 1 (db) blocked svc/api; budget gate deferred UI docs to session 2. One `write_file:elevated` paused on approval with diff preview; idempotency key prevented double migration on retry after timeout. Result: 1 retry, 0 double-writes.
2. **Flaky E2E triage (30 tests):** map-reduce — 30 parallel `run_tests` shards (sem=6) with 90s timeouts each, `race(unit-shard, cached-baseline)` to skip green paths. 3 transient failures retried via idempotency cache; 1 perm failure parked as `failed` without blocking the merge report. Join aggregated pass/fail + trajectory links.

## 15. Hands-On Lab

**Exercise (30 min):** implement `schedule + execute` for 6 tasks (A→B, A→C, B+D→E, C→F) with budgets `[2k,3k,3k,5k,2k,2k]`, session cap 10k, `D: elevated`, `E: timeout 5s`.
1. Write topological batches; show which batch pauses for approval and which defers on budget.
2. Inject failure: E times out once — apply idempotency-key retry, log `trajectoryId` + `transition` events.
3. Add `race()` for C (cache vs live) and `join()` for E/F. Deliverable: batch table + event log + 1 paragraph on what moved to session 2 and why.

---

## Best Practices

> ## 📌 Basic Concept
>
> **Concept:** Best Practices are the collection of 12 golden rules drawn from real-world experience in building task management for AI agents — from "one task does one thing" to "manage the token budget".
>
> **Analogy:** Like a workplace safety ruleset — you don't need to remember why each rule is right; just follow it and most risks vanish automatically.
>
> **Why it matters:** This section distills the whole module into practice-ready rules you can use every day.

```
┌──────────────────────────────────────────────────────────────────┐
│                TASK MANAGEMENT BEST PRACTICES                     │
│                                                                  │
│  1. ONE TASK = ONE RESPONSIBILITY                                │
│     Each task does only one clear thing                          │
│     → Easy to estimate, easy to track, easy to review            │
│                                                                  │
│  2. SIZE MATTERS                                                  │
│     Tasks of 100-5000 tokens are ideal                           │
│     Too small → overhead, too large → easy to fail              │
│                                                                  │
│  3. VISIBLE STATE                                                 │
│     Always know what state the task is in                        │
│     → State machine + logging                                    │
│                                                                  │
│  4. EXPLICIT DEPENDENCIES                                        │
│     Write down which task depends on which                       │
│     → DAG + topological sort                                     │
│                                                                  │
│  5. ESTIMATE & TRACK TOKENS                                      │
│     Track token usage per task                                   │
│     → Budget awareness, avoid context overflow                   │
│                                                                  │
│  6. TEMPLATE COMMON PATTERNS                                     │
│     Create templates for frequently seen task types              │
│     → Save time, ensure consistency                               │
│                                                                  │
│  7. FAIL GRACEFULLY                                               │
│     Task fails → log the reason clearly, retry or skip           │
│     → Don't block the entire pipeline                            │
│                                                                  │
│  8. USE VERIFICATION CRITERIA                                    │
│     Every sub-task must have a "definition of done"              │
│     → Clear when the task is complete                            │
│                                                                  │
│  9. DETECT ANTI-PATTERNS EARLY                                   │
│     Check for killer tasks, ambiguous tasks, dependency overload │
│     → Fix before starting execution                               │
│                                                                  │
│  10. CHOOSE RIGHT DECOMPOSITION STRATEGY                         │
│      Auto-detect based on task type and complexity               │
│      → Feature, Layer, File, TDD, Vertical Slice, Spike          │
│                                                                  │
│  11. MANAGE TOKEN BUDGET                                         │
│      Check remaining budget before each sub-task                 │
│      → Prevent context overflow, plan session breaks             │
│                                                                  │
│  12. FOLLOW WORKFLOW PATTERNS                                     │
│      Feature → Understand, Plan, Implement, Verify               │
│      Debug → Reproduce, Investigate, Hypothesize, Fix            │
│      Refactor → Characterize, Identify, Plan, Apply, Verify      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## References

> ## 📌 Basic Concept
>
> **Concept:** This is the list of source materials the module is based on — from LangGraph and CrewAI to the Eisenhower Matrix, Martin Fowler's Refactoring, and Google's engineering standards.
>
> **Analogy:** Like the bibliography at the end of a textbook — if you want to go deeper or see the source, open exactly that book.
>
> **Why it matters:** When you need more complete technical detail, this gives you trustworthy places to look.

- [LangGraph State Management](https://langchain-ai.github.io/langgraph/)
- [CrewAI Task Management](https://docs.crewai.com/)
- [Eisenhower Matrix](https://www.mindtools.com/pages/article/newHTE_H.htm)
- [Martin Fowler - Refactoring](https://refactoring.com/)
- [Google Engineering Practices](https://google.github.io/eng-practices/review/)
- [Token Estimation - tiktoken](https://github.com/openai/tiktoken)
