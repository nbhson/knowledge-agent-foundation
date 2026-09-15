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

AutoGen models multi-agent as a conversation — but sometimes you want a clearer structure: **each agent one role, each role one task, and agents coordinated inside a crew**. Like a company where the planner makes plans, the executor executes, and the reviewer approves — everyone has one job, and nobody talks over anyone.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** is a role-based multi-agent framework: you define an `Agent` (role, goal, backstory), a `Task` (description, expected_output, agent), and a `Crew` (agents, tasks, process). Crucially, sample code already exists in HARNESS_ENGINEERING.md section 9.1.

### Why CrewAI Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Clear role-based** | Each agent has a role/goal/backstory — easy to map onto harness components |
| 2 | **Task-first** | `Task` is the unit of work — exactly the harness/04 philosophy (task decomposition) |
| 3 | **Process orchestrates** | `Process.sequential` / `Process.hierarchical` — control of execution order |
| 4 | **Human-in-the-loop** | The `human_input` flag allows interjection between steps |

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

```python
from crewai import Agent, Task, Crew

# Multi-agent harness
planner = Agent(role='Planner', goal='Create plan')
executor = Agent(role='Executor', goal='Execute plan')
reviewer = Agent(role='Reviewer', goal='Review output')

harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task]
)
```

### Process: Sequential vs Hierarchical

```python
# Sequential — linear pipeline: plan → execute → review
harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task],
    process=Process.sequential
)

# Hierarchical — manager agent orchestrates, assigns tasks
harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,  # adds a "harness manager"
    manager_llm=llm
)
```

`Process.hierarchical` is exactly **harness/09-multi-agent** — a manager orchestrates like a harness orchestrator. `Process.sequential` maps to the **harness/07-workflow** pipeline.

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

```python
planner = Agent(role='Planner', goal='Break down feature into tasks')
coder = Agent(role='Coder', goal='Implement tasks', tools=[code_editor])
reviewer = Agent(role='Reviewer', goal='Find bugs and security issues')

plan_task = Task(description='Plan the login API', expected_output='Task list')
code_task = Task(description='Implement per plan', expected_output='Working code')
review_task = Task(description='Review code', expected_output='Review report')

crew = Crew(
    agents=[planner, coder, reviewer],
    tasks=[plan_task, code_task, review_task],
    process=Process.sequential  # plan → code → review → (reviewer feedback loop)
)
```

### 2. Human-in-the-Loop

```python
task = Task(
    description="Deploy to production",
    expected_output="Deployment confirmation",
    human_input=True  # pause and wait for confirmation before deploying
)
```

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

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — crewai*
