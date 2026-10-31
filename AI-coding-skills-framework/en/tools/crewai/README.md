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

AutoGen treats multi-agent work like a conversation — but sometimes you want something more clear and organized: **each agent has one role, each role has one task, and they all work together in a crew**. It is like a small company where the planner makes the plan, the builder builds it, and the reviewer checks it — everyone has one job, and no one talks over anyone else.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** is a role-based framework for teams of agents: you set up an `Agent` (role, goal, backstory), a `Task` (description, expected_output, agent), and a `Crew` (agents, tasks, process). You can already find example code in section 9.1 of HARNESS_ENGINEERING.md.

### Why CrewAI Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Clear role-based** | Each agent has a role, goal, and backstory — easy to match with harness parts |
| 2 | **Task-first** | `Task` is the basic unit of work — much like the harness/04 idea of breaking tasks down |
| 3 | **Process orchestrates** | `Process.sequential` / `Process.hierarchical` controls the order of work |
| 4 | **Human-in-the-loop** | The `human_input` flag lets a person step in between steps |

### Relationship to the Harness

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

## Overview

### Three Core Concepts

```
Agent  →  AI worker with role/goal/backstory + tools
Task   →  Concrete piece of work, expected output, which agent it's assigned to
Crew   →  Collection of agents + tasks + process (how they coordinate)
```

### Sample Code From HARNESS_ENGINEERING.md

> 📄 **Example code:** [`examples/01-sample-code-from-harness-engineering-md.py`](examples/01-sample-code-from-harness-engineering-md.py)

### Process: Sequential vs Hierarchical

> 📄 **Example code:** [`examples/02-process-sequential-vs-hierarchical.py`](examples/02-process-sequential-vs-hierarchical.py)

`Process.hierarchical` matches **harness/09-multi-agent** — a manager guides the work like a harness organizer. `Process.sequential` matches the **harness/07-workflow** pipeline.

## Learning Roadmap (Directory Structure)

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

| If you want to... | Read |
|-------------------|------|
| Understand task decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Multi-agent concepts | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Task lifecycle | [harness/08-task](../../harness/08-task/) |

## Real-World Case Studies

### 1. Code Review Crew

> 📄 **Example code:** [`examples/03-1-code-review-crew.py`](examples/03-1-code-review-crew.py)

### 2. Human-in-the-Loop

> 📄 **Example code:** [`examples/04-2-human-in-the-loop.py`](examples/04-2-human-in-the-loop.py)

## Reference Materials

- **CrewAI**: https://docs.crewai.com/
- **GitHub**: https://github.com/crewAIInc/crewAI
- **Blog**: https://blog.crewai.com

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (sample CrewAI code)
- [harness/07-workflow](../../harness/07-workflow/) — Workflow orchestration
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent patterns
- [tools/autogen](../autogen/) — Equivalent multi-agent (conversation-based)
- [tools/langchain](../langchain/) — Graph-based orchestration

---

> **"CrewAI gives your harness an org chart — roles, tasks, and a crew that ships."**

---

## ⚠️ Update 10/2026: CrewAI v1.x — Latest Version

CrewAI released **v1.0.0 (10/2025)** and is now at **v1.15.x (2026)** — significant updates:

| Change | Details |
|--------|---------|
| **v1.0.0** | Knowledge & guardrail event handling in Agent, response_format support |
| **v1.5.0** | Structured outputs, before/after tool call hooks |
| **v1.14+** | Inline skill definitions, Flow Definition authoring, dynamic LLM model pull |
| **CrewAI CLI** | `crewai run` with `crew.jsonc` config file |

**Note:** CrewAI >= 1.0 requires **Python 3.10 – 3.13**.

> 📄 **Example code:** [`examples/05-update-10-2026-crewai-v1-x-latest-version.sh`](examples/05-update-10-2026-crewai-v1-x-latest-version.sh)

Ref: https://docs.crewai.com/

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — crewai*
