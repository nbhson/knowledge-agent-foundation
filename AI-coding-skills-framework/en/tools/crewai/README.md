# 🚢 CrewAI — Multi-Agent Harness (Role-Based)

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why CrewAI Matters?](#why-crewai-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview](#overview)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section explains what CrewAI is and why "roles" make multi-agent work easier to manage.

AutoGen treats multi-agent work like a conversation — but sometimes you want something more clear and organized: **each agent has one role, each role has one task, and they all work together in a crew**. It is like a small company where the planner makes the plan, the builder builds it, and the reviewer checks it — everyone has one job, and no one talks over anyone else.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** is a role-based framework for teams of agents: you set up an `Agent` (role, goal, backstory), a `Task` (description, expected_output, agent), and a `Crew` (agents, tasks, process). To unpack those terms: an `Agent` = one AI worker with a job title (role), a target (goal), and a short work history (backstory) that shapes how it behaves. A `Task` = one concrete job handed to one agent, with the result you expect spelled out. A `Crew` = the whole team plus the order in which they work. You can already find example code in section 9.1 of HARNESS_ENGINEERING.md.

> **One-line summary:** CrewAI organizes AI agents like a small company — one role per agent, one task per role, and a defined order of work.

### Why CrewAI Matters?

This table lists four reasons CrewAI fits a harness well.

How to read it: the **#** column is just a row number; **Reason** is the short label; **Explanation** says in plain words why it helps. For example, row 1 means: because each agent has a role, goal, and backstory, you can map it directly to a harness part.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Clear role-based** | Each agent has a role, goal, and backstory — easy to match with harness parts |
| 2 | **Task-first** | `Task` is the basic unit of work — much like the harness/04 idea of breaking tasks down |
| 3 | **Process orchestrates** | `Process.sequential` / `Process.hierarchical` controls the order of work |
| 4 | **Human-in-the-loop** | The `human_input` flag lets a person step in between steps |

Plain glosses for the jargon above: `Task` = one piece of work with a named owner and an expected result. `Process.sequential` = run tasks one after another, like a queue. `Process.hierarchical` = a manager agent decides who does what, like a boss delegating. `human_input` = a switch that pauses the run so a person can review or correct before the next step.

> **One-line summary:** CrewAI matters because its role + task + process structure maps almost one-to-one onto harness ideas you already know.

### Relationship to the Harness

This diagram shows which CrewAI building block corresponds to which harness module. Read `→` as "matches" or "plays the same role as". For example, `Agent(role="Planner") → harness/04` means: a Planner agent does the same job as the plan/decompose module in the harness.

```
┌────────────────────────────────────────────────────────────┐
│  CREWAI MAP VS HARNESS COMPONENTS                          │
│                                                            │
│  Agent(role="Planner")   → harness/04 (plan/decompose)     │
│  Agent(role="Executor")  → harness/06 (tool execution)     │
│  Agent(role="Reviewer")  → harness/11 (evaluation)         │
│  Task + expected_output  → harness/08 (task)               │
│  Crew(process=...)       → harness/07 (workflow)           │
│  Crew + agents           → harness/09 (multi-agent)        │
└────────────────────────────────────────────────────────────┘
```

> **One-line summary:** Every CrewAI piece has a twin in the harness — so learning one teaches you the other.

## Overview

> **One-line summary:** Overview = the three building blocks, sample code, and the two process modes.

### Three Core Concepts

This is the whole framework in three words: Agent, Task, Crew. Read `→` as "then feeds into".

```
Agent  →  AI worker with role/goal/backstory + tools
Task   →  Concrete piece of work, expected output, which agent it's assigned to
Crew   →  Collection of agents + tasks + process (how they coordinate)
```

> **One-line summary:** Agent = who, Task = what, Crew = how they work together.

### Sample Code From HARNESS_ENGINEERING.md

This points to a runnable sample so you can see Agent/Task/Crew in real code instead of diagrams.

> 📄 **Example code:** [`examples/01-sample-code-from-harness-engineering-md.py`](examples/01-sample-code-from-harness-engineering-md.py)

> **One-line summary:** Start from the existing sample code — it already shows a working Crew.

### Process: Sequential vs Hierarchical

This section explains the two ways a Crew can order its work — the choice affects who decides what happens next.

> 📄 **Example code:** [`examples/02-process-sequential-vs-hierarchical.py`](examples/02-process-sequential-vs-hierarchical.py)

`Process.hierarchical` matches **harness/09-multi-agent** — a manager guides the work like a harness organizer. `Process.sequential` matches the **harness/07-workflow** pipeline.

> **One-line summary:** Sequential = a fixed pipeline; hierarchical = a manager delegates — pick based on whether the order must be decided at runtime.

## Learning Roadmap (Directory Structure)

> **One-line summary:** This section maps the folder layout and a step-by-step learning path.

This tree shows the folder layout of this directory. `←` comments say what each folder will contain; `(TODO)` means the folder is not written yet.

```
crewai/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Agent, Task, Crew, Process, Flows
├── 02-setup/            ← (TODO) Installing crewai, configuring LLM, tools
├── 03-patterns/         ← (TODO) Sequential pipeline, hierarchical, flows
├── 04-savings/          ← (TODO) Token usage + cost per crew run
└── 05-troubleshooting/  ← (TODO) Agent misalignment, task delegation, memory
```

### Recommended Roadmap

This is a suggested order to learn CrewAI, one step at a time. Read `↓` as "then do this next".

```
Step 1: Read HARNESS_ENGINEERING.md section 9.1 — sample CrewAI code is provided
   ↓
Step 2: Create a simple Crew: planner → executor → reviewer (sequential)
   ↓
Step 3: Add tools to the executor (search, code, db) — harness/06
   ↓
Step 4: Scale up to Process.hierarchical with a manager — harness/09
   ↓
Step 5: Connect evaluation + observability (tools/evaluation, tools/observability)
```

This table tells you which harness doc to read for each question. How to read it: the left column is your goal ("If you want to..."); the right column is the doc that answers it. For example, "Understand task decomposition" = breaking a big job into smaller ones — read harness/04.

| If you want to... | Read |
|-------------------|------|
| Understand task decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Multi-agent concepts | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Task lifecycle | [harness/08-task](../../harness/08-task/) |

> **One-line summary:** Learn in this order: sample code → simple sequential crew → tools → hierarchical manager → evaluation and monitoring.

## Real-World Case Studies

These are two worked scenarios with runnable code — read the scenario, then the file.

> **One-line summary:** Two complete scenarios — a code-review crew and a human-approval pause — each with code.

### 1. Code Review Crew

What this shows: several agents playing planner/executor/reviewer to review code together — the "small company" pattern from the opening story, in practice.

> 📄 **Example code:** [`examples/03-1-code-review-crew.py`](examples/03-1-code-review-crew.py)

> **One-line summary:** A code-review crew is the clearest example of role-based agents dividing one job.

### 2. Human-in-the-Loop

What this shows: pausing the crew at chosen steps so a person approves or corrects before work continues — `human_input` in action.

> 📄 **Example code:** [`examples/04-2-human-in-the-loop.py`](examples/04-2-human-in-the-loop.py)

> **One-line summary:** Human-in-the-loop puts a person back in the driver's seat at the steps you choose.

## Reference Materials

These are the official CrewAI resources for deeper reading.

> **One-line summary:** Official docs, GitHub, and blog — start with docs.crewai.com.

- **CrewAI**: https://docs.crewai.com/
- **GitHub**: https://github.com/crewAIInc/crewAI
- **Blog**: https://blog.crewai.com

### Links to Other Branches

These links connect this page to related pages in the repo — follow them when you need the neighboring topic.

> **One-line summary:** Neighboring topics: the harness docs, and the two sibling multi-agent tools (autogen, langchain).

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (sample CrewAI code)
- [harness/07-workflow](../../harness/07-workflow/) — Workflow orchestration
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent patterns
- [tools/autogen](../autogen/) — Equivalent multi-agent (conversation-based)
- [tools/langchain](../langchain/) — Graph-based orchestration

---

> **"CrewAI gives your harness an org chart — roles, tasks, and a crew that ships."**

---

## ⚠️ Update 10/2026: CrewAI v1.x — Latest Version

This section summarizes what changed in CrewAI recently, so you don't learn an outdated API.

CrewAI released **v1.0.0 (10/2025)** and is now at **v1.15.x (2026)** — significant updates:

How to read it: the left column is the version or tool; the right column says what that release added, in short. For example, "structured outputs" = the model returns data in a fixed format (like JSON fields) instead of free text.

| Change | Details |
|--------|---------|
| **v1.0.0** | Knowledge & guardrail event handling in Agent, response_format support |
| **v1.5.0** | Structured outputs, before/after tool call hooks |
| **v1.14+** | Inline skill definitions, Flow Definition authoring, dynamic LLM model pull |
| **CrewAI CLI** | `crewai run` with `crew.jsonc` config file |

Plain glosses: "guardrail event handling" = the Agent can react to safety checks that fire. "Hooks before/after a tool call" = code you can run just before and just after a tool is used. `crewai run` = one command to launch a crew; `crew.jsonc` = the config file describing that crew (JSONC = JSON with comments allowed).

**Note:** CrewAI >= 1.0 requires **Python 3.10 – 3.13** — older Python versions will not install it.

> 📄 **Example code:** [`examples/05-update-10-2026-crewai-v1-x-latest-version.sh`](examples/05-update-10-2026-crewai-v1-x-latest-version.sh)

> **One-line summary:** Use CrewAI v1.x with Python 3.10–3.13; the CLI, hooks, and structured outputs are the headline additions.

Ref: https://docs.crewai.com/

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — crewai*
