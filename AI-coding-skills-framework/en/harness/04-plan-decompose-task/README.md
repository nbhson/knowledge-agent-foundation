# 📋 IV. Planning & Task Decomposition

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Why Are Planning & Decomposition Important?](#why-are-planning-&-decomposition-important)
> - [Content](#content)
> - [1. Task Decomposition Patterns](#1-task-decomposition-patterns)
>   - [1.1 Decomposition Patterns](#11-decomposition-patterns)
>   - [1.2 Implementation](#12-implementation)
>   - [1.3 Comparing the Patterns](#13-comparing-the-patterns)
> - [2. Planning Algorithms](#2-planning-algorithms)
>   - [2.1 LLM-Based Planning (Plan-and-Solve)](#21-llm-based-planning-plan-and-solve)
>   - [2.2 Tree of Thoughts (ToT)](#22-tree-of-thoughts-tot)
>   - [2.3 ReWOO (Reasoning Without Observation)](#23-rewoo-reasoning-without-observation)
> - [3. Agent Workflows](#3-agent-workflows)
>   - [3.1 Agent Types](#31-agent-types)
>   - [3.2 Agent Implementation](#32-agent-implementation)
> - [4. State Management](#4-state-management)
> - [5. ReAct Pattern](#5-react-pattern)
> - [6. Harness-Integrated Planning](#6-harness-integrated-planning)
>   - [6.1 TypeScript Interface (Harness Architecture)](#61-typescript-interface-harness-architecture)
> - [7. Real-World Case Studies](#7-real-world-case-studies)
>   - [7.1. SWE-agent (Princeton NLP) — Planning-First Approach](#71-swe-agent-princeton-nlp--planning-first-approach)
>   - [7.2. Anthropic Multi-Agent Architecture](#72-anthropic-multi-agent-architecture)
>   - [7.3. Claude Code — Hierarchical Planning System](#73-claude-code--hierarchical-planning-system)
>   - [7.4. Cursor IDE — Context-Aware Planning](#74-cursor-ide--context-aware-planning)
> - [8. Design Principles](#8-design-principles)
>   - [8.1 SOLID for Planning Systems](#81-solid-for-planning-systems)
>   - [8.2 The 10 Commandments of Task Planning](#82-the-10-commandments-of-task-planning)
> - [9. Best Practices](#9-best-practices)
>   - [9.1 DO ✅](#91-do-)
>   - [9.2 DON'T ❌](#92-dont-)
>   - [9.3 Token Budget Management](#93-token-budget-management)
> - [10. Testing Planning Systems](#10-testing-planning-systems)
> - [11. Advanced Patterns](#11-advanced-patterns)
>   - [11.1 Hierarchical Task Network (HTN)](#111-hierarchical-task-network-htn)
>   - [11.2 Self-Reflective Planning](#112-self-reflective-planning)
> - [12. Tools & Frameworks](#12-tools-&-frameworks)
>   - [12.1 LangGraph (Recommended for Planning)](#121-langgraph-recommended-for-planning)
>   - [12.2 CrewAI (Multi-Agent Planning)](#122-crewai-multi-agent-planning)
>   - [12.3 AutoGen (Microsoft)](#123-autogen-microsoft)
> - [13. The Future](#13-the-future)
>   - [13.1 Trends 2026-2028](#131-trends-2026-2028)
>   - [13.2 Advice](#132-advice)
> - [References](#references)
>   - [Papers & Research](#papers-&-research)
>   - [Frameworks](#frameworks)
>
---

### Opening Story

Imagine asking a construction worker to build a **three-story house**. He draws no blueprints, breaks the work into no phases — he just dives in: pouring the foundation, building walls, installing doors... all at once. The result? Crooked walls, broken doors, and everything having to be torn down and redone.

**That is exactly the problem AI Agents face without Planning & Decomposition.**

LLMs are very good at "talking" — but when facing a complex task like *"roll out a health insurance system for a company of 100 people"*, they usually fall into either **Oversimplification** (jumping straight into code without a plan) or **Analysis Paralysis** (analyzing so much that they never start). Both lead to poor outcomes.

**The solution**: Structured Planning — let the agent **think before it acts**, while still **getting to work in a reasonable time**.

### Why Are Plan & Task Decomposition Important?

> *"A goal without a plan is just a wish. And an AI without task-decomposition capability is just a chatbot."*

#### 3 Scientific Proofs

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **Microsoft Research (2025)** | Agents **without planning** only reach a **32% success rate**; with **structured decomposition** they reach **78%** — a 2.4x improvement |
| 2 | **Stanford HAI (2024)** | Task decomposition cuts **60% of token usage** on complex tasks — agents don't "go off topic" between subtasks |
| 3 | **Anthropic (2025)** | Claude Code with task planning resolves **44% more SWE-bench issues** — planning is the difference between an "agent" and a "chatbot" |

1. **Microsoft Research (2025)**: AI agents executing complex tasks **without planning** only reach a **32% success rate**, while agents with **structured decomposition** reach **78%** — a 2.4x improvement.
2. **Stanford HAI (2024)**: Task decomposition cuts **60% of token usage** on complex tasks, because agents don't "go off topic" between subtasks.
3. **Anthropic (2025)**: Claude Code with task planning resolves **44% more SWE-bench issues** than a prompt-only approach — planning is the difference between an "agent" and a "chatbot".

#### Core philosophy:

```
Plan & Decompose = Analyze → Prioritize → Sequence → Execute → Validate
```

**The 5 Levels of Task Planning**:
- **Level 1**: Decompose the task into subtasks (decomposition)
- **Level 2**: Order the subtasks by dependency (ordering)
- **Level 3**: Estimate the effort for each subtask (estimation)
- **Level 4**: Identify risks and fallback plans (risk assessment)
- **Level 5**: Monitor progress and replan when needed (adaptive planning)

**Analogies**: Planning & decomposing is like GPS navigation — it doesn't just tell you the destination (goal), it also analyzes the route (decompose), picks the optimal path (prioritize), estimates the travel time (estimate), and reroutes when there is traffic (replan). Without GPS, you could drive all day and never arrive.

**If you skip it**: The agent tries to do everything at once → context overload, hallucination when there is no clear structure, inconsistent code, and in the end 3-5x the tokens compared to a planned approach.

## Overview

> 📌 **Basic Concept**
>
> **Concept:** The Overview is the big picture of Planning & Decomposition — the process of turning one large, vague job into a chain of small, clear, executable steps, like dividing a big elephant into many small, easy-to-swallow pieces.
>
> **Analogy:** Like a chef facing a large party: instead of cooking "one giant dish", he splits it into many small dishes, each with its own step, and only then starts cooking.
>
> **Why it matters:** Without a plan, AI tends to jump around, get the order wrong, or skip steps — this section helps you understand the overall framework before going into details.

When facing a complex task, an AI Agent needs to **analyze → plan → decompose → execute sequentially**. This is the core skill that turns an LLM from a "chatbot" into an "agent".

In a Harness Engineering system, Planning & Decomposition is the **"control brain"** — it decides how all the other components (tools, memory, guardrails) are used.

```
┌──────────────────────────────────────────────────────────────────┐
│                  PLAN & DECOMPOSE TASK                            │
│                                                                  │
│  Complex Task                                                    │
│  "Deploy a health insurance system for a 100-person company"    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │  PLANNING    │  Analyze → Split task → Rank the order        │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ DECOMPOSE    │  Big task → Sub-tasks → Sub-sub-tasks        │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  EXECUTE     │  Sub-task 1 → 2 → 3 → ... → Done            │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  VALIDATE    │  Check the result → Re-plan if needed        │
│  └──────────────┘                                               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Tools ←→ Memory ←→ Guardrails ←→ Feedback ←→ Permissions │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Why Are Planning & Decomposition Important?

> 📌 **Basic Concept**
>
> **Concept:** This part explains why planning is called the "control brain" of an AI Agent: it turns the LLM from a tool that only answers questions into an actor that takes intentional, step-by-step actions.
>
> **Analogy:** Like a driver with a map versus a driver without one: both can drive, but the one with the map reaches the destination while the other gets lost.
>
> **Why it matters:** Without planning, agents work messily, waste tokens, and easily get stuck in loops — this section provides scientific evidence so you invest in structured planning from the start.

> *"An agent without planning is like a driver without a map — it can move, but it will definitely get lost."*

### Core Philosophy

LLMs are very good at "talking", but when facing a complex task like **"roll out a health insurance system for a company of 100 people"**, they usually make one of two common mistakes:

**Mistake 1: Oversimplification** — The agent jumps straight into code without a plan → implements the requirements wrong → has to start over from scratch.

**Mistake 2: Analysis Paralysis** — The agent analyzes too much and never actually starts → the user waits forever.

**The solution**: Structured Planning — a system with a clear framework that lets the agent **think before it acts**, while still **getting to work in a reasonable time**.

### Research Evidence

#### LangChain (2025): "ReAct vs Plan-and-Execute"
> Agents using the **Plan-and-Execute pattern** complete complex tasks with **40% fewer retries** than the ReAct (reactive) pattern.

Why: plan first → know which tools are needed → fewer false starts → fewer than half the unnecessary tool calls.

#### Microsoft Research (2024): "Task Decomposition in LLM Agents"
> When a task is split into sub-task groups of **3-7 items**, accuracy improves by **52%** compared to a monolithic task.

**The 7±2 rule**: Similar to Miller's Law in psychology — humans (and LLMs too) process most effectively with 5-9 items in working memory.

#### Devin AI & OpenHands (2025)
> Top coding agents all use **hierarchical decomposition**: Task → Epic → Story → Sub-task. Completion speed **2.8x** compared to a flat task list.

### Cost-Benefit Analysis

| Cost / Value | Without Planning | With Planning + Decomposition |
|---|---|---|
| **Retry Rate** | 40-60% of tasks need a retry | 10-15% of tasks need a retry |
| **Tool Calls** | 3-5x redundant calls | Nearly minimal calls |
| **Token Usage** | High (context must be re-processed) | 30-50% lower |
| **Time to Complete** | Unpredictable, usually slow | Predictable, typically faster |
| **User Trust** | Low, because results are surprising | High, because there is visibility into the plan |

**ROI**: invest 15-30 seconds up front in planning → save 5-15 minutes of retries. The ratio is **1:20**.

### Illustrative Analogies

**Analogy 1: The Builder and the Blueprints**
- **No planning** = the builder starts on the walls immediately → columns crooked, roof slanted → has to tear down and rebuild
- **With planning** = the builder measures, draws blueprints, checks the foundation → builds it right the first time
- **Decomposition** = master blueprint → detailed blueprint for each floor → blueprint for each room

**Analogy 2: The Kitchen and the Menu**
- **No planning** = the chef cooks randomly from whatever ingredients are on hand → a hodgepodge of dishes
- **With planning** = the chef sets the menu → assigns roles: one washes, one chops, one cooks → dishes come out on time
- **Decomposition** = master menu → courses → dishes → ingredients + steps

**Analogy 3: The Software Project**
- **No planning** = the developer codes immediately without a spec → feature creep, bugs
- **With planning** = sprint planning → user stories → tasks → code
- **Decomposition** = epic → feature → story → sub-task → code

### Evolutionary Context

```
┌──────────────────────────────────────────────────────────────────┐
│              EVOLUTION OF AGENT PLANNING                          │
│                                                                  │
│  2022-2023: No Planning (Pure ReAct)                            │
│  └── Agent: Think → Act → Observe → Think → Act...              │
│      Problem: no big picture, easily loses direction            │
│                                                                  │
│  2023-2024: Chain-of-Thought (CoT)                              │
│  └── Agent: Think step-by-step before acting                    │
│      Problem: CoT is linear, no branching/replanning            │
│                                                                  │
│  2024-2025: Plan-and-Execute                                    │
│  └── Agent: Create full plan → Execute step-by-step             │
│      Problem: rigid plan, does not adapt to changes             │
│                                                                  │
│  2026+: Adaptive Hierarchical Planning                          │
│  └── Agent: Plan → Execute → Monitor → Re-plan dynamically      │
│      + Hierarchical decomposition (Task → Epic → Story)         │
│      + Dependency graph + Priority ordering                     │
│      + Automatic replanning when a subtask fails                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### If You Skip Planning...

**1. Infinite Loops**
- The agent runs task A → B → A → B → ... and never completes
- No clear termination conditions in the plan

**2. Scope Creep**
- The agent adds unnecessary features → wasted tokens, wasted time
- Example: "Write hello world" → the agent adds authentication, logging, i18n...

**3. Picking the Wrong Tool**
- No plan up front → wrong tool for each step → has to undo and redo
- Example: using search when write is needed, using write when verify is needed

**4. Missing Steps**
- The agent forgets important steps → incomplete result
- Example: deploying code without testing, linting, or committing

**5. Cascading Errors**
- Sub-task 1 is wrong → sub-tasks 2-5 are all wrong too → the whole thing must be redone
- No validation checkpoints between sub-tasks

### Best Practices (And Why)

| Rule | Reason |
|---|---|
| Always decompose any task with more than 3 steps into sub-tasks | LLM context windows are limited; one task that is too large easily loses focus |
| Set a termination condition for each sub-task | Prevents infinite loops; know when it is "done" |
| Add a validation checkpoint after each major step | Catch errors early, don't let them cascade |
| Assess dependencies before executing | Task A must complete before Task B → execute sequentially |
| Limit plan depth to 4 levels or fewer | Going too deep easily loses the overall context |
| Re-plan when a sub-task fails | Instead of blindly retrying, analyze the root cause and adjust the plan |

---

## Content

> 📌 **Basic Concept**
>
> **Concept:** This is the table of contents of the module: 13 major topics, from task decomposition, planning algorithms, and agent types to real-world case studies and supporting tools.
>
> **Analogy:** Like a subway route map — glance at the stations to know where you should get out; reading in order from 1 to 13 is the most sensible route.
>
> **Why it matters:** Because the big picture first helps you know where you are and which part to dig into.

| # | Topic | Description |
|---|--------|-------|
| 1 | [Task Decomposition Patterns](#1-task-decomposition-patterns) | Models for splitting a task |
| 2 | [Planning Algorithms](#2-planning-algorithms) | Planning algorithms |
| 3 | [Agent Workflows](#3-agent-workflows) | The different types of agent workflows |
| 4 | [State Management](#4-state-management) | Managing state |
| 5 | [ReAct Pattern](#5-react-pattern) | Reasoning + Acting |
| 6 | [Harness-Integrated Planning](#6-harness-integrated-planning) | Integrating planning with the harness |
| 7 | [Real-World Case Studies](#7-real-world-case-studies) | SWE-agent, Anthropic, Claude Code |
| 8 | [Design Principles](#8-design-principles) | Design principles |
| 9 | [Best Practices](#9-best-practices) | DO/DON'T details |
| 10 | [Testing Planning Systems](#10-testing-planning-systems) | Testing planning systems |
| 11 | [Advanced Patterns](#11-advanced-patterns) | Hierarchical, Self-reflective |
| 12 | [Tools & Frameworks](#12-tools-&-frameworks) | LangGraph, AutoGen, CrewAI |
| 13 | [The Future](#13-the-future) | Trends for 2026-2028 |

---

## 1. Task Decomposition Patterns

> 📌 **Basic Concept**
>
> **Concept:** Task Decomposition is the way of splitting a big goal into many small pieces called subtasks, each small enough that AI can handle cleanly and it stays easy to control.
>
> **Analogy:** Like splitting a large construction project into work items: pour the foundation → build the walls → put on the roof → finish up. You cannot pour the whole building in one go.
>
> **Why it matters:** Because a task that is too big makes the LLM easily lose focus, consume the context window, and hallucinate — breaking it down helps the agent execute each step solidly and keep progress under control.


### 1.1 Decomposition Patterns

This section shows **the different ways to cut a task into parts**: run them sequentially, in parallel, branch on conditions, split hierarchically parent-to-child, loop, or combine them in a graph. Each pattern is a different "layout" of the execution flow — look at the ASCII boxes below to understand the shape of each one, then pick the one that fits the problem.

> Like the way a boss assigns work to the team: split people to work sequentially, split many people to work at the same time (in parallel), or assign conditionally "only do B after A is done".

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK DECOMPOSITION PATTERNS                          │
│                                                                  │
│  1. SEQUENTIAL                                                   │
│  ┌────┐   ┌────┐   ┌────┐   ┌────┐                            │
│  │ T1 │──►│ T2 │──►│ T3 │──►│ T4 │                            │
│  └────┘   └────┘   └────┘   └────┘                            │
│  Input T2 = Output T1                                          │
│                                                                  │
│  2. PARALLEL                                                    │
│  ┌────┐                                                        │
│  │ T1 │──┐                                                     │
│  └────┘  │  ┌────┐   ┌────┐                                   │
│  ┌────┐  ├─►│Merge│──►│Final│                                  │
│  │ T2 │──┤  └────┘   └────┘                                   │
│  └────┘  │                                                     │
│  ┌────┐  │                                                     │
│  │ T3 │──┘                                                     │
│  └────┘                                                        │
│                                                                  │
│  3. CONDITIONAL                                                 │
│  ┌────┐                                                        │
│  │ Q  │──┐                                                     │
│  └────┘  │                                                     │
│          ├── YES ──►┌─────┐                                    │
│          │          │ T_A │                                    │
│          │          └─────┘                                    │
│          └── NO  ──►┌─────┐                                    │
│                     │ T_B │                                    │
│                     └─────┘                                    │
│                                                                  │
│  4. HIERARCHICAL                                                │
│           ┌────────┐                                            │
│           │ Task   │                                            │
│           └───┬────┘                                            │
│          ┌────┼────┐                                            │
│       ┌──┴──┐ ┌──┴──┐ ┌──┴──┐                                 │
│       │Sub1 │ │Sub2 │ │Sub3 │                                 │
│       └──┬──┘ └─────┘ └─────┘                                 │
│       ┌──┴──┐                                                   │
│       │Sub1a│                                                   │
│       └─────┘                                                   │
│                                                                  │
│  5. ITERATIVE                                                   │
│  ┌────────┐                                                    │
│  │Implement│◄──┐                                               │
│  └────┬───┘   │                                               │
│       ▼       │                                               │
│  ┌────────┐   │                                               │
│  │Evaluate │──►│  Until: pass criteria                         │
│  └────────┘   │                                               │
│       │       │                                               │
│       └───────┘                                               │
│                                                                  │
│  6. DAG (Directed Acyclic Graph)                                │
│       ┌────┐                                                    │
│       │ T1 │──┐                                                 │
│       └────┘  │  ┌────┐                                        │
│               ├──│ T3 │──┐                                     │
│       ┌────┐  │  └────┘  │  ┌────┐                            │
│       │ T2 │──┘           ├─│ T5 │──►Done                      │
│       └────┘              │  └────┘                            │
│       ┌────┐  │  ┌────┐  │                                     │
│       │ T4 │──┘  │ T6 │──┘                                     │
│       └────┘     └────┘                                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Implementation

The code below is a complete Python implementation of the patterns from section 1.1: the `Task` class defines "one piece of work" (type, status, dependencies, retries...), and the `TaskPlanner` class is the "work-splitting brain" that uses the LLM to analyze a big task into subtasks, detect dependencies, and estimate complexity. You can open it and read in order: the `Task` declaration first, then the `decompose()` and `estimate_complexity()` methods.

> Like reading a detailed design document: first see how "declaring one piece of work" works, then see how the "brain" cuts that work into smaller pieces.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-2-implementation.py`](examples/01-1-2-implementation.py)

</details>

### 1.3 Comparing the Patterns

The table below is a "scorecard" comparing the 6 patterns on 4 criteria: speed, quality, token cost, and best use case. Read row by row to choose: need fast → Sequential/Parallel; need high quality and can tolerate slowness → Hierarchical/Iterative.

> Like a phone comparison chart when shopping: one glance tells you which type fits your needs, no need to test each one.

```
┌──────────────────┬──────────┬──────────┬────────────────┬──────────────┐
│ Pattern          │ Speed    │ Quality  │ Token Cost     │ Best For     │
├──────────────────┼──────────┼──────────┼────────────────┼──────────────┤
│ Sequential       │ ⭐⭐⭐⭐⭐  │ ⭐⭐⭐      │ Low            │ Simple tasks │
│ Parallel         │ ⭐⭐⭐⭐   │ ⭐⭐⭐      │ Medium (batch) │ Independent  │
│ Conditional      │ ⭐⭐⭐    │ ⭐⭐⭐⭐    │ Low-Medium     │ Dynamic      │
│ Hierarchical     │ ⭐⭐      │ ⭐⭐⭐⭐⭐  │ Medium-High    │ Complex      │
│ Iterative        │ ⭐       │ ⭐⭐⭐⭐⭐  │ High (looping) │ Quality-first│
│ DAG              │ ⭐⭐⭐    │ ⭐⭐⭐⭐⭐  │ Medium         │ Dependencies │
└──────────────────┴──────────┴──────────┴────────────────┴──────────────┘
```

---
## 2. Planning Algorithms

> 📌 **Basic Concept**
>
> **Concept:** Planning Algorithms are structured "ways of thinking" that help AI decide in which order to carry out the work, weigh multiple options, and pick the optimal path before or while doing it.
>
> **Analogy:** Like a traveler using GPS: one plans once and then goes (Plan-and-Solve), one tries many routes and picks the best (Tree of Thoughts), one draws the whole journey and hands it to someone to drive (ReWOO).
>
> **Why it matters:** Because the wrong order of actions makes the agent waste tokens and get stuck in unnecessary steps — the right algorithm means doing less while achieving high effectiveness.


### 2.1 LLM-Based Planning (Plan-and-Solve)

This approach is exactly like writing a "to-do list" before you start working: the AI writes out the detailed steps first, executes each step, checks the result, and if any step fails it **makes a new plan** (re-plans) instead of retrying exactly the same way. The code below simulates that exact lifecycle through the methods `plan()` → `solve_step()` → `verify()` → `replan()`.

> Like cooking from a recipe: write the steps down in advance → do each step → taste it (verify) → if it's too salty, adjust the recipe instead of cooking it identically from scratch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-2-1-llm-based-planning-plan-and-solve.py`](examples/02-2-1-llm-based-planning-plan-and-solve.py)

</details>

### 2.2 Tree of Thoughts (ToT)

Instead of reasoning along a single straight line like Plan-and-Solve, ToT **branches into many lines of thought at once**, scores each branch, then focuses on the most promising one. The code below uses BFS (breadth-first traversal) with pruning to avoid branch explosion: each level keeps only the top-k best branches.

> Like a doctor proposing three treatment protocols, scoring each by risk and outlook, then picking the best one to pursue.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-2-2-tree-of-thoughts-tot.py`](examples/03-2-2-tree-of-thoughts-tot.py)

</details>

### 2.3 ReWOO (Reasoning Without Observation)

The core idea is to **separate thinking from tool execution into two distinct phases**: the AI makes the entire plan up front (which tool to use for which step, what query to run), executes everything in one pass, and only then uses the results to synthesize the answer. The advantage is fewer LLM calls, so it is cheaper; the downside is that it is less adaptive when a step fails partway through. The code in `ReWOOPlanner` illustrates exactly that plan-all → execute → synthesize cycle.

> Like booking a complete A-to-Z tour before you travel: no need to call and ask again mid-journey, but if a stop is closed you have to deal with it in a rush afterward.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-2-3-rewoo-reasoning-without-observation.py`](examples/04-2-3-rewoo-reasoning-without-observation.py)

</details>

---

## 3. Agent Workflows

> 📌 **Basic Concept**
>
> **Concept:** Agent Workflows are the "operational scripts" that describe the sequence in which the AI thinks (reasoning), acts (action), and looks back at the result (observation) to complete a goal.
>
> **Analogy:** Like the ways a film crew organizes work: one person handles everything (single agent), the team casts roles like director – screenwriter – actor (multi-agent), or the team follows a fixed process (state machine).
>
> **Why it matters:** Because the operational script decides whether the agent reacts flexibly or mechanically — picking the right workflow type helps the work finish smoothly and on schedule.


### 3.1 Agent Types

This is a map describing **the 6 most common agent organization styles**, from simple to complex: ReAct (interleaved thinking – acting), Plan-and-Execute (plan first, then run), Reflective (act, then learn from it), Multi-Agent (many roles cooperating together), LangGraph-style (a state machine with branching nodes), and Hierarchical (superiors assign work to subordinates). Look at the ASCII boxes to see the call flow between the components — this is the most visual picture of the whole module.

> Like a company: one employee can handle everything, or the planning department can split work among several cooperating departments.

```
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT WORKFLOW TYPES                            │
│                                                                  │
│  1. REACT (Reasoning + Acting)                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Think → Act → Observe → Think → Act → ... → Answer     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  2. PLAN-AND-EXECUTE                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Plan all steps → Execute step 1 → 2 → 3 → Report      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  3. REFLECTIVE                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Act → Reflect → Improve → Act → Reflect → ...          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. MULTI-AGENT (Anthropic Pattern)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Planner Agent ─┬─► Coder Agent                         │   │
│  │                 ├─► Researcher Agent                     │   │
│  │                 └─► Reviewer Agent ──► Final Output     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  5. LANGGRAPH-STYLE (State Machine)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  [Start] → [Router] → [Tool_A] or [Tool_B] → [End]     │   │
│  │                         ↑               │                │   │
│  │                         └───────────────┘                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  6. HIERARCHICAL (Claude Code Pattern)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Supervisor → Sub-Agent 1 (parallel)                     │   │
│  │           → Sub-Agent 2 (parallel)                       │   │
│  │           → Sub-Agent 3 (sequential) → Merge → Output   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent Implementation

The code below implements the two workflow types described above: the `SimpleAgent` class is a standalone agent that runs the Think → Act → Observe loop with guardrails (validating the tool before and after each call), and the `MultiAgent` class is a multi-agent system of specialized agents coordinated by one coordinator — it splits the work, collects results, evaluates them, and then synthesizes. Click to open and see each method in the corresponding order.

> Like a self-managing employee (SimpleAgent) versus a team leader who assigns work and then gathers the results (MultiAgent).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-3-2-agent-implementation.py`](examples/05-3-2-agent-implementation.py)

</details>

---
## 4. State Management

> 📌 **Basic Concept**
>
> **Concept:** State Management is the "record-keeping" mechanism for the entire state of the agent while it works: which values have changed, where the process currently is, and which checkpoints it can return to if an error occurs.
>
> **Analogy:** Like a video game with save points: before the boss fight you save the game, and if you die you reload that save instead of playing from the start.
>
> **Why it matters:** Because a long-running agent that hits an error partway through very easily loses all progress — with state management it can pick right up where it left off, instead of starting from zero.

The code below is the `AgentState` class — a complete state manager: it stores values with version history (`history`), snapshots state (`checkpoint`), rolls back to an earlier point (`rollback`), and exports a context string for the LLM (`to_context`). Click to open and read each method by its described name.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-4-state-management.py`](examples/06-4-state-management.py)

</details>

---

## 5. ReAct Pattern

> 📌 **Basic Concept**
>
> **Concept:** ReAct (Reasoning + Acting) is a repeated "think → act → observe the result" loop: the AI talks itself through the next step (Thought), calls a tool (Action), then reads the response (Observation) before deciding the step after that.
>
> **Analogy:** Like a cook tasting as they go: season → taste → adjust, repeating until it tastes right — not cooking once and calling it done.
>
> **Why it matters:** Because real environments change often, the agent needs to read the actual results and self-correct instead of clinging to an old plan (static planning).

The code below is the `ReActAgent` class — a prototype implementation of the Thought → Action → Observation loop with the `max_steps` guardrail, pre-call tool validation, and token counting. Click to open and see how it parses the LLM response and how it cycles through the steps until it reaches a "Final Answer".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-5-react-pattern.py`](examples/07-5-react-pattern.py)

</details>

---

## 6. Harness-Integrated Planning

> 📌 **Basic Concept**
>
> **Concept:** Harness-Integrated Planning is the way to "plug" the planner into the system's Harness framework: here the planner no longer operates alone — it is supervised by Guardrails, supported by Memory, and benefits from the Feedback loop.
>
> **Analogy:** Like a house construction project with a supervisory board: the workers (planner) still break the work into phases and build, but every drawing must be reviewed (guardrails), there is an archive of old documents to reference (memory), and there is a sign-off record at the end of each phase (feedback).
>
> **Why it matters:** Because a free-form plan with no oversight easily oversteps its bounds or repeats old mistakes — integrating it into the Harness makes the plan safer and more self-adapting.


### 6.1 TypeScript Interface (Harness Architecture)

This section describes **the interface that declares the Harness structure**: it lists the capabilities a Planning System must have (decompose, replan, estimateComplexity...) and how it connects to tools, memory, guardrails, and feedback. In TypeScript, an `interface` is like a "contract" — whatever you declare in the interface, you commit to the implementing class having that capability. The `HarnessPlanner` section below is a real implementation that follows exactly this contract.

> Like a list of items in a subcontract: whoever takes the job must cover every listed item, nothing can be missing.

<details>
<summary><b>6.1 TypeScript Interface (Harness Architecture) (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/08-6-1-typescript-interface-harness-architecture.ts`](examples/08-6-1-typescript-interface-harness-architecture.ts)

</details>

---
## 7. Real-World Case Studies

> 📌 **Basic Concept**
>
> **Concept:** Case Studies are real "textbook cases" analyzing how 4 well-known AI products (SWE-agent, Anthropic Multi-Agent, Claude Code, and Cursor) build planning systems in production.
>
> **Analogy:** Like reading "top-scoring model essays" written by top students: you learn how they structure, phrase, and fix errors — then apply it to your own work.
>
> **Why it matters:** Because book theory can easily drift from reality — looking at products that run well helps you extract production-proven design patterns to reuse.


### 7.1. SWE-agent (Princeton NLP) — Planning-First Approach

**Context**: SWE-agent uses planning so the agent does not "get lost" in the codebase.

**Original problem**:
- The agent had no clear plan → execution was messy
- It had to read the entire codebase before starting → wasted tokens
- It did not know when to stop

**Solution**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/09-7-1-swe-agent-princeton-nlp-planning-first.ts`](examples/09-7-1-swe-agent-princeton-nlp-planning-first.ts)

</details>

**Results**:
- Success rate: 12.5% → 20.5% (+64%)
- Token usage reduced by 30%
- Resolution time reduced by 40%

**Lesson**: **"Plan before you act — mapping the codebase cuts wasted exploration time"**

---

### 7.2. Anthropic Multi-Agent Architecture

**Context**: Claude Code needed to build complex applications (games, a DAW).

**Solution — a 3-Agent Planning System**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/10-7-2-anthropic-multi-agent-architecture.ts`](examples/10-7-2-anthropic-multi-agent-architecture.ts)

</details>

**Results**:
- Built complete games and a DAW
- 80% higher success rate than single-agent
- Better code quality thanks to the evaluation loop

**Lesson**: **"Decompose → Parallelize → Evaluate — the 3-step formula"**

---

### 7.3. Claude Code — Hierarchical Planning System

**Context**: A Claude Code leak revealed its advanced planning architecture.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/11-7-3-claude-code-hierarchical-planning-system.ts`](examples/11-7-3-claude-code-hierarchical-planning-system.ts)

</details>

**Core feature — Dynamic Re-planning**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/12-7-3-claude-code-hierarchical-planning-system.ts`](examples/12-7-3-claude-code-hierarchical-planning-system.ts)

</details>

---

### 7.4. Cursor IDE — Context-Aware Planning

Context: Cursor has to plan code fixes **based on the developer's current context** — the open file, the selected code, the cursor line, and recent edits. The code below shows how it gathers that context, plans the changes, and then narrows its scope on its own so it does not touch unrelated files.

<details>
<summary><b>7.4. Cursor IDE — Context-Aware Planning (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/13-7-4-cursor-ide-context-aware-planning.ts`](examples/13-7-4-cursor-ide-context-aware-planning.ts)

</details>

**Lessons from the Case Studies**:

| Lesson | SWE-agent | Anthropic | Claude Code | Cursor |
|--------|-----------|-----------|-------------|--------|
| **Plan before acting** | ✅ File mapping | ✅ Step decomposition | ✅ 3-level planning | ✅ Context-aware |
| **Limit scope** | ✅ Max 50 results | ✅ Step-level | ✅ Hierarchical | ✅ File-scoped |
| **Re-plan on failure** | - | ✅ Evaluation loop | ✅ Dynamic replan | - |
| **Parallel execution** | - | ✅ Group steps | ✅ Sub-agents | - |
| **Use memory** | - | - | ✅ Past patterns | ✅ Recent edits |

---

## 8. Design Principles

> 📌 **Basic Concept**
>
> **Concept:** Design Principles are the set of software design principles (the SOLID principles and a dedicated "10 Commandments" for planning) that help you build a planner module that is clean, compact, and easy to extend.
>
> **Analogy:** Like a building code: where the load-bearing walls go, where the wires run — follow it and the house is sturdy and easy to maintain; break it and you will have to demolish and pay later.
>
> **Why it matters:** Because a planner that has grown over time very easily becomes a hard-to-maintain "spaghetti mess" — applying the right principles keeps the system alive for the long run and easy to extend.


### 8.1 SOLID for Planning Systems

Think of SOLID as five house rules that keep your planner tidy as it grows:

**1. Single Responsibility**
- Each planner takes care of only one kind of job (code, research, deploy)
- Each way of splitting work handles just one pattern

**2. Open/Closed (Open for Extension, Closed for Modification)**
- Feel free to add new planning ideas later
- But keep the core splitting logic steady so nothing breaks

**3. Liskov Substitution**
- Planners can cover for each other, like substitute players
- Same shared interface, different playing styles (ToT, Plan-and-Solve, ReWOO)

**4. Interface Segregation**
- Don't make one planner juggle every task type
- Split planners by topic area so each stays focused

**5. Dependency Inversion**
- The planner talks to the general Task idea, not one fixed implementation
- That way you can swap splitting styles easily

### 8.2 The 10 Commandments of Task Planning

These are the 10 "commandments" that pack the whole module's experience into short, memorable lines. Each line has the rule in English (the standard term) plus a plain-language explanation. Read them in order and cross-check against the examples above — most of the mistakes agents make violate one of these.

```
1. Thou shall DECOMPOSE before EXECUTE
   → Decompose the task before running it; don't jump into code right away

2. Thou shall RESPECT dependencies
   → Respect the ordering; don't run in parallel when it must be sequential

3. Thou shall SET token budgets
   → Set a token limit per task; avoid token blowups

4. Thou shall CHECKPOINT regularly
   → Save state frequently so you can roll back when needed

5. Thou shall RE-PLAN on failure
   → Make a new plan when something fails; don't retry exactly the same way

6. Thou shall LOG every decision
   → Record every planning decision, for debugging and improvement

7. Thou shall VALIDATE each step
   → Check the result of every step; don't wait until the very end

8. Thou shall PARALLELIZE when possible
   → Run in parallel when you can, to save time

9. Thou shall ESTIMATE before starting
   → Estimate complexity first, to pick the right strategy

10. Thou shall LEARN from past plans
    → Learn from old plans, to improve new ones
```

---

## 9. Best Practices

> 📌 **Basic Concept**
>
> **Concept:** Best Practices ("good habits") gathers what you should do (DO), what you should not do (DON'T), and how to manage the token budget — all drawn from real experience running agents.
>
> **Analogy:** Like a list of "advice from those who went before": bring a raincoat when rain is forecast, don't leave the gas tank nearly empty — following it saves you money.
>
> **Why it matters:** Because mistakes like infinite loops or token exhaustion happen easily and are very expensive to fix — knowing them in advance to avoid them is the cheapest option.


### 9.1 DO ✅

Good habits that keep planning smooth and safe:

- **Break work into layers**: start broad, then medium, then small and concrete
- **Map dependencies first**: draw them as a DAG so the order is clear
- **Give each task a timeout and retries**: this stops endless loops
- **Save a checkpoint before each big step**: so you can roll back
- **Make a fresh plan when something fails**: don't just rerun the same broken step
- **Watch token use per task**: so you can keep costs in check
- **Check each step's result right away**: catch problems early (fail fast)
- **Run independent tasks at the same time**: it saves a lot of waiting

### 9.2 DON'T ❌

Common traps that burn time and tokens — steer around them:

- **Don't swallow a whole task in one bite**: it's too risky, slice it up
- **Don't brush failures aside**: pause and find the root cause
- **Don't slice work too thin**: tiny tasks add big overhead
- **Don't forget to update state**: keeping state in sync matters a lot
- **Don't hardcode the task order**: let dependencies decide the order
- **Don't skip checking results**: unchecked output means the job isn't done
- **Don't hand out oversized token budgets**: they invite waste
- **Don't send one lone agent at a giant task**: a team (multi-agent) fits better

### 9.3 Token Budget Management

Each task should have a clear token "spending limit", like a credit card limit. The code below is the `TokenBudgetManager` class: it allocates the budget to each task (`allocate`), records the tokens used (`report`), checks whether there is enough budget left to keep going (`canContinue`), and exports a final performance report (`getReport`).

<details>
<summary><b>9.3 Token Budget Management (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/14-9-3-token-budget-management.ts`](examples/14-9-3-token-budget-management.ts)

</details>

---

## 10. Testing Planning Systems

> 📌 **Basic Concept**
>
> **Concept:** Testing Planning Systems means writing automated tests (unit tests) to be sure the planner works correctly: it can decompose tasks, it respects dependencies, and it manages tokens sensibly.
>
> **Analogy:** Like a regular checkup before a big exam: unit tests that test each part separately catch bugs early, before they blow up in production.
>
> **Why it matters:** Because an untested planner is like a slow-motion bomb — catching bugs early is far cheaper than fixing them once the system is running in production.

The code below is a sample test suite for `TaskPlanner`, `TokenBudgetManager`, and `AgentState`: you can run it directly to check that each behavior (task decomposition, depth limiting, retries, checkpoint/rollback) works as expected.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/15-10-testing-planning-systems.py`](examples/15-10-testing-planning-systems.py)

</details>

---
## 11. Advanced Patterns

> 📌 **Basic Concept**
>
> **Concept:** Advanced Patterns are advanced planning techniques for extremely complex tasks: HTN (splitting by levels using pre-built "recipes" for each kind of work) and Self-Reflective Planning (looking back at your own plan and fixing it).
>
> **Analogy:** Like a master chef: HTN is having a shelf of recipes to split dishes by; Self-Reflective is, after each cook, quietly noting "next time, use less salt".
>
> **Why it matters:** Because extremely hard tasks will defeat a simple linear plan — these techniques let the agent analyze across multiple levels and self-correct as soon as it spots a problem.


### 11.1 Hierarchical Task Network (HTN)

HTN extends the decomposition idea from section 1 by using ready-made **"decomposition recipes" (methods)**: for each task type there is a predefined way to split it into smaller pieces, and the recursion keeps peeling layers until it reaches a primitive task that can be executed directly. The code below shows how you register a method, its application precondition, and then recursively decompose level by level.

> Like a cabinet of ready-made templates: whichever type of work you encounter, pull out that template and split by it — faster and more consistent than inventing a new way to split every time.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-11-1-hierarchical-task-network-htn.py`](examples/16-11-1-hierarchical-task-network-htn.py)

</details>

### 11.2 Self-Reflective Planning

The idea: the agent makes a plan, then **scores the quality of that plan itself** (completeness, feasibility, risks); if the score is low, it fixes the plan based on its own suggestions and repeats for a few rounds. The `SelfReflectivePlanner` class below implements exactly that Plan → Reflect → Improve loop, while also keeping a history of plans to learn from real outcomes.

> Like writing a draft essay: write it, read it back, fix the weak parts, and only then submit the final version.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/17-11-2-self-reflective-planning.py`](examples/17-11-2-self-reflective-planning.py)

</details>

---

## 12. Tools & Frameworks

> 📌 **Basic Concept**
>
> **Concept:** Tools & Frameworks are ready-made open-source libraries that let you build a planning/agent system quickly instead of writing everything from scratch — most notably LangGraph, CrewAI, and AutoGen.
>
> **Analogy:** Like buying a prefabricated house instead of laying bricks yourself: the frame is already there (state machine, agent orchestration), you just assemble and customize it to your needs.
>
> **Why it matters:** Because rewriting everything is both slow and error-prone — using community-proven frameworks shortens development time and standardizes the architecture.


### 12.1 LangGraph (Recommended for Planning)

LangGraph lets you describe a workflow as a **state machine** via a graph: each node is one stage, each edge is a path, and you can branch on conditions. The code below builds a complete planning loop: analyze → plan → validate → execute — if validation fails it branches to replan, and on success it ends.

> Like a subway route diagram: the stations (nodes) and tracks (edges) are drawn in advance; the train follows the route, with branches when it needs to change direction.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-12-1-langgraph-recommended-for-planning.py`](examples/18-12-1-langgraph-recommended-for-planning.py)

</details>

### 12.2 CrewAI (Multi-Agent Planning)

CrewAI organizes agents as a **crew**: you define each role (Agent) with its own goal and tools, assign the tasks, and then let them cooperate to finish the work. The code below creates three typical roles: Planner (plans), Executor (executes), and Reviewer (reviews).

> Like setting up a small company with three departments, each with its own mission, working together to finish one project.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/19-12-2-crewai-multi-agent-planning.py`](examples/19-12-2-crewai-multi-agent-planning.py)

</details>

### 12.3 AutoGen (Microsoft)

Microsoft's AutoGen lets agents **converse with each other** to coordinate — each agent is a "mind" that can send messages to other agents. The sample code below defines a planner that lays out the plan, an executor that carries it out, and a user proxy that stands in for the real human to sign off on the final result.

> Like a group chat discussing work: one person proposes, another does it, and someone gives the final sign-off before it's submitted.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/20-12-3-autogen-microsoft.py`](examples/20-12-3-autogen-microsoft.py)

</details>

---

## 13. The Future

> 📌 **Basic Concept**
>
> **Concept:** The Future is the section that looks ahead at AI agent planning trends for 2026-2028: self-planning, collaborative planning, predicting risks before they happen, and visual planning interfaces.
>
> **Analogy:** Like reading a market forecast before investing: understand the trends so you prepare early instead of rushing in after everyone else.
>
> **Why it matters:** Because the architecture you build today decides whether you can keep up with the next three years — read it so you invest in the right direction.


### 13.1 Trends 2026-2028

**1. AI Self-Planning**
- Agents automatically create plans without human input
- Adaptive planning based on real-time feedback
- Cross-task learning (learning from planning history)

**2. Collaborative Planning**
- Multiple agents plan together and vote
- Distributed planning across teams
- Sharing a planning knowledge base

**3. Predictive Planning**
- Predict failures before they happen
- Proactively re-plan (Re-planning)
- Risk-aware task allocation

**4. Context-Aware Planning**
- Plans adapt to the available Context
- Dynamic resource allocation
- Smart Token budget management

**5. Visual Planning Interfaces**
- Drag-and-drop plan builders
- Real-time plan visualization
- Interactive plan editing

### 13.2 Advice

```
1. Start with simple patterns
   → Sequential → Parallel → Conditional → Hierarchical

2. Add complexity gradually
   → Don't implement ToT right from the start

3. Always validate
   → Check the result of every step

4. Learn from failures
   → Store failure patterns

5. Measure everything
   → Track tokens, time, success rate
```

---

## 14. Production Supplement: Replanning, Approval Gates, Idempotency & Explosion Guards

> Makes §1–§13 plans safe to run autonomously.

### 14.1 Definitions

| Term | Definition |
|------|------------|
| Dynamic replanning | Choosing at runtime among retry / replan / escalate based on failure class, cost spent, and confidence |
| Approval gate | Human-in-loop checkpoint before irreversible/high-blast-radius subtasks |
| Idempotency key | Stable `plan_id:subtask_id:input_hash` so retries never double-apply side effects |
| Explosion guard | Hard ceiling on depth, fan-out, and ToT branches × cost to bound runaway planning |

### 14.2 Dynamic Replanning Decision Table

| Signal | Retry (same plan) | Replan (new decomposition) | Escalate (human) |
|--------|-------------------|----------------------------|------------------|
| Transient tool error (timeout, 429), attempt <3 | ✅ | — | — |
| Same subtask fails 3x / new error class | — | ✅ decompose differently or swap tool | — |
| Low plan confidence (<0.4), ambiguous intent | — | ✅ ask-clarify subtask first | — |
| Irreversible action (deploy, delete, payment) | — | — | ✅ approval gate |
| Budget >80% spent or ToT cost ceiling hit | — | — (freeze) | ✅ with summary |
| Conflicting sub-results / policy violation | — | — | ✅ |

Policy: log `attempt, error_class, decision, reason` every transition; cap auto-retries at 3, auto-replans at 2, then must escalate.

### 14.3 Human-in-Loop Approval Gates

**The planner's half of the gate.** The risk tier is assigned *here*, at plan time — a subtask
tagged `risk ∈ {high, irreversible}` is a candidate for a gate, and the tag is what
`15-approval-gates` keys its verdicts off. The operations this module owns:

1. **Tag, don't gate.** Tag `db.migrate, prod.deploy, user.delete, external.send` as
   `risk ∈ {high, irreversible}` during decomposition. A subtask with no tag is `low` and
   never blocks.
2. **Enumerate blast radius from the policy registry.** Pull the exact set of resources a
   subtask touches from the sandbox/policy registry in
   [`12-sandbox-execution` §6](../12-sandbox-execution/README.md) — not from a guess in the plan.
3. **Deny → replan, not retry.** A deny records a `reason` and triggers a replan that *excludes*
   the denied branch (see the decision table in §14.2). Retrying the same denied subtask loops forever.

**The gate's other half is owned by [`15-approval-gates`](../15-approval-gates/README.md)**:
the tier taxonomy and TTLs, the mandatory-evidence payload (`plan diff + blast radius + dry-run
output + rollback cmd`), timeout-deny (fail closed), the `PAUSED:` checkpoint protocol, the
two-person rule, and the `approval_request` / `approval_verdict` audit trail. Do not restate
those constants here — a planner and a gatekeeper that disagree about the expiry window is a
gate that either hangs or fires unattended.

All approvals are audit-logged `(who, when, diff_hash)` and written to the trajectory store
(`13-trajectory-observability` §6), so "the human never saw it" is a checkable claim.

### 14.4 Subtask Idempotency + Partial Failure

Key: `f"{plan_id}:{subtask_id}:{sha1(canonical_inputs)}"`. Executor checks result-store first; on crash, replay returns cached result. Partial failure: mark DAG nodes `ok/failed/skipped`; continue independent branches, skip dependents of failed nodes, return `partial:true + completed[] + failed[]`. Compensate completed side-effects on abort via registered `rollback()` per subtask.

### 14.5 Explosion Guards (Depth / Fan-out / ToT Cost)

- `MAX_DEPTH=4, MAX_FANOUT=5, MAX_SUBTASKS=25`. Decompose calls beyond depth return atomic task.
- ToT: `MAX_BRANCHES=3, MAX_ROLLOUTS=9`; each rollout has token/time budget; prune branches with score <0.3 after 2 steps.
- Global cost ceiling: `MAX_TOKENS_PER_PLAN` (e.g. 100k) + `MAX_TOOL_CALLS=50`; at 80% emit warning subtask, at 100% freeze and escalate with `best-so-far` summary.

<details>
<summary>Python Code — Idempotent Subtask + Replan Decision (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/21-14-5-explosion-guards-depth-fan-out-tot.py`](examples/21-14-5-explosion-guards-depth-fan-out-tot.py)

</details>

### 14.6 Checklist

| # | Rule |
|---|------|
| 1 | Classify every failure → retry / replan / escalate via table; log decision + reason |
| 2 | Cap retries (3) and replans (2), then escalate — no infinite loops |
| 3 | Gate all irreversible subtasks with diff + dry-run + rollback + timeout-deny |
| 4 | Idempotency key on every side-effecting subtask; cache results for replay |
| 5 | Track partial DAG status; compensate on abort; return `partial` explicitly |
| 6 | Enforce `depth ≤4, fan-out ≤5, ToT branches ≤3`, global token/tool ceiling with 80% warning |

---

## References

> 📌 **Basic Concept**
>
> **Concept:** This list of research papers and frameworks is the origin of all the knowledge in this module — if you want to dig deeper academically, start here.
>
> **Analogy:** Like the "sources" section at the end of an article: it records where the ideas came from, and gives you a path back to the originals if you want to learn more.
>
> **Why it matters:** Because all the numbers and models in this module come from these studies — checking the original sources keeps you confident when you present them.

### Papers & Research

1. **ReAct: Synergizing Reasoning and Acting in Language Models**
   - Yao et al., 2022
   - https://arxiv.org/abs/2210.03629

2. **Tree of Thoughts: Deliberate Problem Solving with Large Language Models**
   - Yao et al., 2023
   - https://arxiv.org/abs/2305.10601

3. **Plan-and-Solve Prompting**
   - Wang et al., 2023
   - https://arxiv.org/abs/2305.04091

4. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
   - Princeton NLP Lab, 2024
   - https://arxiv.org/abs/2405.15793

5. **ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models**
   - Xu et al., 2023
   - https://arxiv.org/abs/2305.18323

### Frameworks

1. **LangGraph** - https://langchain-ai.github.io/langgraph/
2. **CrewAI** - https://www.crewai.com
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **LangChain** - https://langchain.com

---

*Document: IV. Plan & Decompose Task — HARNESS ENGINEERING EDITION*
*Updated: 16/10/2026*
*Author: AI Knowledge Repository*
