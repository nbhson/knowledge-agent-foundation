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

```python
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HIERARCHICAL = "hierarchical"
    ITERATIVE = "iterative"
    DAG = "dag"

@dataclass
class Task:
    id: str
    name: str
    description: str
    task_type: TaskType = TaskType.SEQUENTIAL
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List['Task'] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    max_retries: int = 3
    retry_count: int = 0
    timeout_seconds: int = 300
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    token_budget: Optional[int] = None  # Token limit for this task
    tools_allowed: List[str] = field(default_factory=list)  # Tools allowed to use
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "type": self.task_type.value,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "dependencies": self.dependencies,
            "retry_count": self.retry_count,
            "token_budget": self.token_budget,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }
    
    def mark_completed(self, result):
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now().isoformat()
    
    def mark_failed(self, error):
        self.status = TaskStatus.FAILED
        self.error = error
    
    def can_retry(self):
        return self.retry_count < self.max_retries
    
    def can_execute(self, completed_tasks: set):
        """Check if all dependencies are satisfied"""
        return all(dep in completed_tasks for dep in self.dependencies)

class TaskPlanner:
    """
    LLM-based task planner
    
    Analyzes a big task and splits it into sub-tasks
    Supports: hierarchical decomposition, dependency detection, complexity estimation
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def decompose(self, task_description, max_depth=3, current_depth=0):
        """
        Analyze a task and split it into sub-tasks
        
        Strategy:
        - depth 0-1: Broad decomposition (major phases)
        - depth 2+: Fine-grained decomposition (specific actions)
        """
        if current_depth >= max_depth:
            return [Task(
                id=f"leaf_{current_depth}",
                name=task_description[:50],
                description=task_description,
            )]
        
        if self.llm:
            prompt = f"""Analyze the following task and split it into sub-tasks:

Task: {task_description}
Depth: {current_depth}/{max_depth}

Rules:
- Each sub-task must be concrete and actionable
- Identify dependencies between sub-tasks
- Evaluate the type (sequential/parallel/conditional)
- Estimate the token budget for each sub-task
- List the tools needed for each sub-task

Output JSON:
{{
  "analysis": "Task analysis",
  "subtasks": [
    {{
      "name": "...",
      "description": "...",
      "type": "sequential|parallel|conditional",
      "dependencies": [],
      "estimated_tokens": 5000,
      "required_tools": ["tool1", "tool2"]
    }}
  ],
  "estimated_steps": 3
}}"""
            
            response = self.llm(prompt)
            try:
                import json
                data = json.loads(response)
                tasks = []
                for i, st in enumerate(data.get("subtasks", [])):
                    task_type_map = {
                        "sequential": TaskType.SEQUENTIAL,
                        "parallel": TaskType.PARALLEL,
                        "conditional": TaskType.CONDITIONAL,
                    }
                    task = Task(
                        id=f"task_{current_depth}_{i}",
                        name=st["name"],
                        description=st["description"],
                        task_type=task_type_map.get(st.get("type", "sequential"), TaskType.SEQUENTIAL),
                        dependencies=st.get("dependencies", []),
                        token_budget=st.get("estimated_tokens"),
                        tools_allowed=st.get("required_tools", []),
                    )
                    tasks.append(task)
                return tasks
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Fallback reaction: simple task decomposition
        return [Task(
            id=f"task_{current_depth}_0",
            name=task_description[:50],
            description=task_description,
        )]
    
    def create_execution_plan(self, root_task):
        """
        Create an execution plan from the task tree
        
        Returns: Ordered list of tasks to execute with dependency info
        """
        plan = []
        self._traverse(root_task, plan)
        return plan
    
    def _traverse(self, task, plan):
        """DFS traversal to create execution order"""
        if task.task_type == TaskType.SEQUENTIAL:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.PARALLEL:
            plan.append(task)  # Parallel marker
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.ITERATIVE:
            task.metadata["max_iterations"] = 5
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        else:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
    
    def estimate_complexity(self, task):
        """
        Evaluate the complexity of a task
        
        Returns: Score 1-10 with detailed breakdown
        """
        depth = self._get_depth(task)
        breadth = self._get_breadth(task)
        
        # Advanced scoring
        score = min(10, depth * 2 + breadth)
        
        # Estimate Tokens
        estimated_tokens = self._estimate_tokens(task)
        
        # Recommended strategy
        if score <= 3:
            strategy = "direct"
            reasoning = "Simple task, execute directly"
        elif score <= 6:
            strategy = "sequential"
            reasoning = "Medium task, split sequentially"
        else:
            strategy = "hierarchical"
            reasoning = "Complex task, needs multi-level hierarchy"
        
        return {
            "score": score,
            "depth": depth,
            "total_subtasks": breadth,
            "complexity": "simple" if score <= 3 else "medium" if score <= 6 else "complex",
            "estimated_tokens": estimated_tokens,
            "recommended_strategy": strategy,
            "reasoning": reasoning,
        }
    
    def _get_depth(self, task, current=0):
        if not task.subtasks:
            return current
        return max(self._get_depth(s, current + 1) for s in task.subtasks)
    
    def _get_breadth(self, task):
        count = 1
        for sub in task.subtasks:
            count += self._get_breadth(sub)
        return count
    
    def _estimate_tokens(self, task):
        """Estimate the number of tokens needed"""
        base_tokens = len(task.description.split()) * 2  # Rough estimate
        for sub in task.subtasks:
            base_tokens += self._estimate_tokens(sub)
        return base_tokens
```

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

```python
class PlanAndSolve:
    """
    Plan-and-Solve prompting strategy
    
    Based on paper: "Plan-and-Solve Prompting" (Wang et al., 2023)
    
    1. Plan: Break down the problem into sub-problems
    2. Solve: Execute each sub-problem
    3. Verify: Check results against original problem
    4. Re-plan: If verification fails, create new plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.max_replan_attempts = 3
    
    def plan(self, problem):
        """Step 1: Create a plan"""
        prompt = f"""Make a plan to solve the following problem.
Give concrete, clear steps.

Problem: {problem}

Plan (each step on 1 line, starting with a number):
1. ...
2. ...
3. ..."""
        
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Step 1: Analyze {problem}", "Step 2: Execute"]
    
    def solve_step(self, step, context=""):
        """Step 2: Solve a single step"""
        prompt = f"""Execute the following step:

Step: {step}
Context: {context}

Result:"""
        
        if self.llm:
            return self.llm(prompt)
        return f"Result for: {step}"
    
    def verify(self, problem, solution):
        """Step 3: Verify solution"""
        prompt = f"""Check the solution for the problem:

Problem: {problem}
Solution: {solution}

Evaluation (JSON):
{{
  "complete": true/false,
  "correct": true/false,
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1"]
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"complete": True, "correct": True, "issues": [], "suggestions": []}
    
    def replan(self, problem, original_plan, failed_step, error):
        """Create a new plan based on failure"""
        prompt = f"""The initial plan failed. Please make a new plan.

Problem: {problem}
Old plan: {original_plan}
Failed step: {failed_step}
Error: {error}

New plan (each step on 1 line):
"""
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Fix: {failed_step}"]
    
    def run(self, problem):
        """Execute full plan-and-solve cycle with re-planning"""
        plan = self.plan(problem)
        
        for attempt in range(self.max_replan_attempts):
            results = []
            context = ""
            all_succeeded = True
            
            for i, step in enumerate(plan):
                result = self.solve_step(step, context)
                results.append({"step": step, "result": result})
                context += f"\nStep {i+1} completed: {result[:200]}"
            
            # Verify
            verification = self.verify(problem, "\n".join(
                f"{r['step']}: {r['result']}" for r in results
            ))
            
            if verification.get("complete", True) and verification.get("correct", True):
                return {
                    "plan": plan,
                    "results": results,
                    "verification": verification,
                    "attempts": attempt + 1,
                }
            
            # Re-plan based on the issues
            if verification.get("issues"):
                plan = self.replan(
                    problem, plan, 
                    verification["issues"][0],
                    str(verification.get("suggestions", []))
                )
        
        return {
            "plan": plan,
            "results": results,
            "verification": verification,
            "attempts": self.max_replan_attempts,
            "status": "max_attempts_reached",
        }
```

</details>

### 2.2 Tree of Thoughts (ToT)

Instead of reasoning along a single straight line like Plan-and-Solve, ToT **branches into many lines of thought at once**, scores each branch, then focuses on the most promising one. The code below uses BFS (breadth-first traversal) with pruning to avoid branch explosion: each level keeps only the top-k best branches.

> Like a doctor proposing three treatment protocols, scoring each by risk and outlook, then picking the best one to pursue.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class TreeOfThoughts:
    """
    Tree of Thoughts: Explore multiple reasoning paths
    
    Better than linear chain-of-thought for complex problems
    Based on paper: "Tree of Thoughts" (Yao et al., 2023)
    
    Key insight: Not all reasoning paths are equal.
    ToT explores multiple branches and evaluates which path is most promising.
    """
    
    def __init__(self, llm_func=None, branching_factor=3, max_depth=3):
        self.llm = llm_func
        self.branching_factor = branching_factor
        self.max_depth = max_depth
    
    def generate_thoughts(self, state, n=None):
        """Generate multiple candidate thoughts"""
        n = n or self.branching_factor
        
        prompt = f"""From the current state, come up with {n} different solution directions.

State: {state}

Direction 1: 
Direction 2: 
Direction 3: """
        
        if self.llm:
            response = self.llm(prompt)
            thoughts = [t.strip() for t in response.split('\n') 
                       if t.strip().startswith("Direction")]
            return thoughts[:n]
        
        return [f"Thought {i+1}" for i in range(n)]
    
    def evaluate_thought(self, state, thought):
        """Evaluate how promising a thought is"""
        prompt = f"""Evaluate this solution direction (1-10):

State: {state}
Direction: {thought}

Criteria:
- Feasibility (0-3)
- Speed of resolution (0-3)
- Result quality (0-4)

Score (1-10):"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                score = int(''.join(c for c in response if c.isdigit())[:2])
                return min(max(score, 1), 10)
            except (ValueError, IndexError):
                pass
        
        return 5  # Default score
    
    def solve(self, problem):
        """
        Tree search: explore best paths
        
        Uses BFS with pruning to avoid exponential explosion
        """
        root_state = {"problem": problem, "path": [], "score": 0}
        
        frontier = [root_state]
        best_solution = None
        best_score = -1
        
        for depth in range(self.max_depth):
            next_frontier = []
            
            for state in frontier:
                thoughts = self.generate_thoughts(
                    f"{state['problem']} | Path: {' → '.join(state['path'])}"
                )
                
                for thought in thoughts:
                    score = self.evaluate_thought(state['problem'], thought)
                    
                    new_state = {
                        "problem": state["problem"],
                        "path": state["path"] + [thought],
                        "score": state["score"] + score,
                    }
                    
                    if new_state["score"] > best_score:
                        best_score = new_state["score"]
                        best_solution = new_state
                    
                    next_frontier.append(new_state)
            
            # Prune: keep only the top-k best paths
            frontier = sorted(next_frontier, key=lambda x: x["score"], reverse=True)
            frontier = frontier[:self.branching_factor]
        
        return {
            "solution": best_solution["path"] if best_solution else [],
            "total_score": best_score,
            "paths_explored": self.branching_factor ** self.max_depth,
        }
```

</details>

### 2.3 ReWOO (Reasoning Without Observation)

The core idea is to **separate thinking from tool execution into two distinct phases**: the AI makes the entire plan up front (which tool to use for which step, what query to run), executes everything in one pass, and only then uses the results to synthesize the answer. The advantage is fewer LLM calls, so it is cheaper; the downside is that it is less adaptive when a step fails partway through. The code in `ReWOOPlanner` illustrates exactly that plan-all → execute → synthesize cycle.

> Like booking a complete A-to-Z tour before you travel: no need to call and ask again mid-journey, but if a stop is closed you have to deal with it in a rush afterward.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ReWOOPlanner:
    """
    ReWOO: Decouple planning from execution
    
    1. PLAN all steps upfront (no observation between steps)
    2. EXECUTE all steps
    3. USE evidence to synthesize answer
    
    Advantage: Fewer LLM calls (batch planning)
    Disadvantage: Less adaptive to failures
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def plan_all(self, task, tools):
        """Generate all plan steps at once"""
        prompt = f"""Create a complete plan for the following task.

Task: {task}
Tools available: {list(tools.keys())}

Output JSON:
{{
  "plan": [
    {{"step_id": "e1", "tool": "tool_name", "query": "query for tool"}},
    {{"step_id": "e2", "tool": "tool_name", "query": "query using #e1"}},
    ...
  ],
  "synthesis_prompt": "Based on #e1, #e2, ..., answer: {task}"
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"plan": [], "synthesis_prompt": task}
    
    def execute_plan(self, plan, tools):
        """Execute all plan steps, collecting evidence"""
        evidence = {}
        
        for step in plan.get("plan", []):
            tool_name = step.get("tool", "")
            query = step.get("query", "")
            
            # Replace references with earlier evidence
            for ref_id, ref_val in evidence.items():
                query = query.replace(f"#{ref_id}", str(ref_val))
            
            if tool_name in tools:
                try:
                    result = tools[tool_name](query)
                    evidence[step["step_id"]] = result
                except Exception as e:
                    evidence[step["step_id"]] = f"Error: {e}"
        
        return evidence
```

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

```python
class SimpleAgent:
    """
    Simple agent with tool-calling loop
    
    Pattern: Think → Act → Observe → Repeat
    
    Harness integration:
    - Respects max_iterations (guardrail)
    - Logs all steps (feedback loop)
    - Validates tool permissions
    """
    
    def __init__(self, tools, llm_func, max_iterations=10):
        self.tools = {tool["name"]: tool for tool in tools}
        self.llm = llm_func
        self.max_iterations = max_iterations
        self.memory = []
        self.metrics = {
            "total_iterations": 0,
            "tools_used": {},
            "errors": 0,
            "total_tokens": 0,
        }
    
    def run(self, task):
        """Execute task with tool calls"""
        self.memory = []
        context = f"Task: {task}\n\nAvailable tools: {list(self.tools.keys())}"
        
        for i in range(self.max_iterations):
            # Think: decide the next step
            thought = self._think(context)
            
            # Check whether it is done
            if thought.get("done"):
                return {
                    "answer": thought.get("answer", ""),
                    "steps": self.memory,
                    "iterations": i + 1,
                    "metrics": self.metrics,
                }
            
            # Act: execute the tool with validation checks
            tool_name = thought.get("tool")
            tool_input = thought.get("input", {})
            
            if tool_name and tool_name in self.tools:
                # Pre-execution validity check
                if not self._validate_tool_call(tool_name, tool_input):
                    context += f"\n\nStep {i+1}: Tool validation failed for '{tool_name}'. Try different approach."
                    continue
                
                result = self._execute_tool(tool_name, tool_input)
                
                # Post-execution validity check
                if not self._validate_result(result):
                    self.metrics["errors"] += 1
                    context += f"\n\nStep {i+1}: Result validation failed. Retry with different parameters."
                    continue
                
                # Observe: add the result to the Context
                observation = f"Tool '{tool_name}' returned: {result}"
                context += f"\n\nStep {i+1}: {thought.get('reasoning', '')}"
                context += f"\n→ Used {tool_name}({tool_input})"
                context += f"\n→ Result: {result}"
                
                self.memory.append({
                    "step": i + 1,
                    "thought": thought,
                    "action": tool_name,
                    "result": result,
                })
                
                self.metrics["tools_used"][tool_name] = self.metrics["tools_used"].get(tool_name, 0) + 1
            else:
                context += f"\n\nStep {i+1}: Invalid tool '{tool_name}'. Try again."
            
            self.metrics["total_iterations"] = i + 1
        
        return {
            "answer": "Max iterations reached",
            "steps": self.memory,
            "iterations": self.max_iterations,
            "metrics": self.metrics,
        }
    
    def _think(self, context):
        """LLM decides next action"""
        prompt = f"""{context}

Based on the information above, decide your next action.

Output JSON:
{{
  "reasoning": "Why I'm doing this",
  "tool": "tool_name" or null if done,
  "input": {{"param": "value"}},
  "done": false,
  "answer": null
}}

If you have enough information to answer, set "done": true and provide "answer"."""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"done": True, "answer": "No LLM available"}
    
    def _validate_tool_call(self, tool_name, tool_input):
        """Pre-execution validation (Harness guardrail)"""
        # Check that the tool exists
        if tool_name not in self.tools:
            return False
        
        # Check the required parameters
        tool = self.tools[tool_name]
        required = tool.get("required_params", [])
        for param in required:
            if param not in tool_input:
                return False
        
        return True
    
    def _validate_result(self, result):
        """Post-execution validation (Harness guardrail)"""
        if result is None:
            return False
        if isinstance(result, str) and result.startswith("Error:"):
            return False
        return True
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool"""
        tool = self.tools.get(tool_name)
        if tool and "function" in tool:
            try:
                return tool["function"](**tool_input)
            except Exception as e:
                return f"Error: {str(e)}"
        return f"Tool '{tool_name}' not found"


class MultiAgent:
    """
    Multi-agent system with specialized agents
    
    Based on Anthropic's multi-agent architecture pattern:
    - Planner Agent: Creates the plan
    - Generator Agent: Executes each step
    - Evaluator Agent: Validates results
    """
    
    def __init__(self, agents, coordinator_llm=None):
        self.agents = agents  # {name: agent}
        self.coordinator = coordinator_llm
    
    def run(self, task):
        """Coordinate multiple agents"""
        plan = self._create_plan(task)
        
        results = {}
        for step in plan:
            agent_name = step["agent"]
            subtask = step["task"]
            
            if agent_name in self.agents:
                result = self.agents[agent_name].run(subtask)
                results[agent_name] = result
                
                # Check whether the result meets the requirements
                if not self._evaluate_result(result, subtask):
                    # Retry with feedback
                    retry_result = self.agents[agent_name].run(
                        f"{subtask}\n\nLast attempt failed because: {result.get('answer', 'unknown error')}"
                    )
                    results[agent_name] = retry_result
        
        return self._synthesize(results, task)
    
    def _create_plan(self, task):
        """Decompose task across agents"""
        agent_names = list(self.agents.keys())
        
        if self.coordinator:
            prompt = f"""Assign subtasks to available agents.

Task: {task}
Available agents: {agent_names}

Output JSON:
{{"steps": [{{"agent": "...", "task": "...", "dependencies": []}}]}}"""
            
            response = self.coordinator(prompt)
            try:
                import json
                return json.loads(response).get("steps", [])
            except json.JSONDecodeError:
                pass
        
        return [{"agent": agent_names[0], "task": task}]
    
    def _evaluate_result(self, result, original_task):
        """Evaluate if result meets requirements"""
        if result.get("iterations", 0) >= 10:
            return False
        if not result.get("answer"):
            return False
        return True
    
    def _synthesize(self, results, original_task):
        """Combine results from all agents"""
        combined = "\n".join(
            f"Agent {name}: {r.get('answer', 'N/A')}"
            for name, r in results.items()
        )
        
        if self.coordinator:
            prompt = f"""Synthesize the results from multiple agents:

Original task: {original_task}

Results:
{combined}

Synthesis:"""
            return self.coordinator(prompt)
        
        return combined
```

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

```python
class AgentState:
    """
    Manage state across agent execution steps
    
    Supports: state persistence, checkpointing, rollback, versioning
    """
    
    def __init__(self):
        self.state = {}
        self.history = []
        self.checkpoints = []
        self.version = 0
    
    def set(self, key, value):
        """Set state value with versioning"""
        old_value = self.state.get(key)
        self.state[key] = value
        self.version += 1
        
        self.history.append({
            "action": "set",
            "key": key,
            "old": old_value,
            "new": value,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get(self, key, default=None):
        """Get state value"""
        return self.state.get(key, default)
    
    def checkpoint(self):
        """Save current state snapshot"""
        self.checkpoints.append({
            "state": dict(self.state),
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
        return len(self.checkpoints) - 1
    
    def rollback(self, checkpoint_id=None):
        """Rollback to checkpoint"""
        if checkpoint_id is None:
            checkpoint_id = len(self.checkpoints) - 1
        
        if 0 <= checkpoint_id < len(self.checkpoints):
            self.state = dict(self.checkpoints[checkpoint_id]["state"])
            self.version = self.checkpoints[checkpoint_id]["version"]
            return True
        return False
    
    def to_context(self):
        """Convert state to context string for LLM"""
        lines = [f"{k}: {v}" for k, v in self.state.items()]
        return "\n".join(lines)
    
    def diff(self, checkpoint_id):
        """Compare current state with checkpoint"""
        if 0 <= checkpoint_id < len(self.checkpoints):
            old = self.checkpoints[checkpoint_id]["state"]
            current = self.state
            
            changes = {
                "added": {k: v for k, v in current.items() if k not in old},
                "removed": {k: v for k, v in old.items() if k not in current},
                "modified": {k: (old.get(k), current.get(k)) 
                           for k in current if k in old and current[k] != old[k]},
            }
            return changes
        return {}
    
    def reset(self):
        """Clear all state"""
        self.state = {}
        self.version = 0
```

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

```python
class ReActAgent:
    """
    ReAct: Reasoning + Acting
    
    Thought → Action → Observation → Thought → ...
    
    Based on paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
    (Yao et al., 2022)
    
    Harness integration:
    - max_steps as guardrail
    - tool validation before execution
    - metrics tracking
    - error recovery
    """
    
    def __init__(self, tools, llm_func, max_steps=10):
        self.tools = tools
        self.llm = llm_func
        self.max_steps = max_steps
        self.trace = []
        self.token_usage = 0
    
    def run(self, query):
        """Execute ReAct loop"""
        prompt = f"""Solve this step by step using Thought/Action/Observation.

Question: {query}

Available actions:
{self._format_tools()}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(input)]
Observation: [result of action]
... (repeat Thought/Action/Observation as needed)
Thought: [final reasoning]
Final Answer: [your answer]"""
        
        history = prompt
        
        for step in range(self.max_steps):
            response = self._llm_call(history)
            
            # Parse the response
            parsed = self._parse_response(response)
            
            if parsed.get("final_answer"):
                return {
                    "answer": parsed["final_answer"],
                    "steps": step + 1,
                    "trace": self.trace,
                    "token_usage": self.token_usage,
                }
            
            # Execute the action
            if parsed.get("action"):
                tool_name, tool_input = self._parse_action(parsed["action"])
                
                # Validate the tool call
                if not self._validate_tool(tool_name):
                    history += f"\n{response}"
                    history += f"\nObservation: Invalid tool '{tool_name}'. Use available tools only."
                    continue
                
                observation = self._execute_tool(tool_name, tool_input)
                
                self.trace.append({
                    "step": step + 1,
                    "thought": parsed.get("thought", ""),
                    "action": parsed["action"],
                    "observation": observation,
                })
                
                history += f"\n{response}"
                history += f"\nObservation: {observation}"
            else:
                history += f"\n{response}"
        
        return {
            "answer": "Max steps reached without final answer",
            "steps": self.max_steps,
            "trace": self.trace,
            "token_usage": self.token_usage,
        }
    
    def _format_tools(self):
        lines = []
        for name, tool in self.tools.items():
            params = tool.get("params", [])
            lines.append(f"- {name}({', '.join(params)})")
        return "\n".join(lines)
    
    def _parse_response(self, response):
        """Parse Thought/Action/Observation from response"""
        result = {}
        
        if "Final Answer:" in response:
            result["final_answer"] = response.split("Final Answer:")[-1].strip()
        
        if "Thought:" in response:
            thought_lines = [l for l in response.split('\n') if l.strip().startswith('Thought:')]
            if thought_lines:
                result["thought"] = thought_lines[-1].replace('Thought:', '').strip()
        
        if "Action:" in response:
            action_line = [l for l in response.split('\n') if l.strip().startswith('Action:')]
            if action_line:
                result["action"] = action_line[0].replace('Action:', '').strip()
        
        return result
    
    def _parse_action(self, action_str):
        """Parse tool_name(input) format"""
        import re
        match = re.match(r'(\w+)\((.+)\)', action_str)
        if match:
            return match.group(1), match.group(2)
        return action_str, ""
    
    def _validate_tool(self, tool_name):
        """Check if tool exists in available tools"""
        return tool_name in self.tools
    
    def _execute_tool(self, tool_name, tool_input):
        if tool_name in self.tools:
            try:
                func = self.tools[tool_name].get("function")
                if func:
                    return func(tool_input)
            except Exception as e:
                return f"Error: {e}"
        return f"Unknown tool: {tool_name}"
    
    def _llm_call(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "Thought: I don't know\nFinal Answer: N/A"
```

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

```typescript
// Planning System Interface — fully integrated with the Harness
interface PlanningSystem {
  // Core planning capabilities
  decompose: (task: Task) => Promise<DecomposedPlan>;
  replan: (task: Task, failure: FailureInfo) => Promise<DecomposedPlan>;
  estimateComplexity: (task: Task) => ComplexityEstimate;
  
  // State management
  getState: () => AgentState;
  checkpoint: () => number;
  rollback: (checkpointId: number) => boolean;
  
  // Integration points
  tools: ToolRegistry;
  memory: MemorySystem;
  guardrails: GuardrailSystem;
  feedback: FeedbackSystem;
}

interface DecomposedPlan {
  rootTask: Task;
  subtasks: Task[];
  executionOrder: ExecutionStep[];
  estimatedTokens: number;
  estimatedTime: number;
  requiredTools: string[];
}

interface ExecutionStep {
  taskId: string;
  agentId: string;
  dependencies: string[];
  timeoutMs: number;
  tokenBudget: number;
  requiredPermissions: string[];
}

// The complete Harness-integrated planner
class HarnessPlanner implements PlanningSystem {
  private tools: ToolRegistry;
  private memory: MemorySystem;
  private guardrails: GuardrailSystem;
  private feedback: FeedbackSystem;
  private state: AgentState;
  
  async decompose(task: Task): Promise<DecomposedPlan> {
    // 1. Validate the input
    const inputCheck = await this.guardrails.validateInput(task);
    if (!inputCheck.valid) {
      throw new Error(`Task validation failed: ${inputCheck.reason}`);
    }
    
    // 2. Check Memory for similar past tasks
    const similarTasks = await this.memory.longTerm.search(
      `task: ${task.description}`,
      { limit: 3 }
    );
    
    // 3. Decompose the task with Context from past experience
    const plan = await this.decomposeWithMemory(task, similarTasks);
    
    // 4. Check the plan against the Guardrails
    const planValidation = await this.guardrails.validatePlan(plan);
    if (!planValidation.valid) {
      throw new Error(`Plan validation failed: ${planValidation.reason}`);
    }
    
    // 5. Log for feedback
    await this.feedback.logPlan(task, plan);
    
    return plan;
  }
  
  async replan(task: Task, failure: FailureInfo): Promise<DecomposedPlan> {
    // Learn from the failure
    await this.memory.longTerm.add(
      `Failed task: ${task.name}, Error: ${failure.error}`,
      { type: 'failure_pattern', task: task.name }
    );
    
    // Re-plan with the failure Context
    const plan = await this.decompose(task);
    
    // Adjust based on the failure
    plan.executionOrder = plan.executionOrder.map(step => ({
      ...step,
      timeoutMs: step.timeoutMs * 1.5, // Increase the timeout
      tokenBudget: step.tokenBudget * 1.2, // Increase the Token budget
    }));
    
    return plan;
  }
  
  estimateComplexity(task: Task): ComplexityEstimate {
    const depth = this.getDepth(task);
    const breadth = this.getBreadth(task);
    
    return {
      score: Math.min(10, depth * 2 + breadth),
      depth,
      totalSubtasks: breadth,
      complexity: depth <= 1 ? 'simple' : depth <= 2 ? 'medium' : 'complex',
      recommendedApproach: breadth > 10 ? 'multi-agent' : 'single-agent',
    };
  }
  
  getState(): AgentState { return this.state; }
  checkpoint(): number { return this.state.checkpoint(); }
  rollback(id: number): boolean { return this.state.rollback(id); }
  
  private async decomposeWithMemory(task: Task, memories: any[]): Promise<DecomposedPlan> {
    // Use Memory from past tasks to implement
    // and improve the quality of task decomposition
    return { /* ... */ } as DecomposedPlan;
  }
  
  private getDepth(task: Task): number { /* ... */ return 0; }
  private getBreadth(task: Task): number { /* ... */ return 0; }
}
```

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

```typescript
// Harness planning for SWE-agent
const swePlanner = {
  async plan(issue: string, codebase: CodebaseInfo) {
    // 1. Analyze the issue
    const analysis = await analyzeIssue(issue);
    
    // 2. Find relevant files (DO NOT read everything)
    const relevantFiles = await findRelevantFiles(analysis, codebase);
    
    // 3. Build the execution plan
    return {
      steps: [
        { action: "read_file", path: relevantFiles[0], reason: "understand context" },
        { action: "search_code", pattern: analysis.functionName, reason: "find implementation" },
        { action: "edit_file", path: relevantFiles[0], changes: analysis.suggestedFix },
        { action: "run_tests", suite: "relevant", reason: "verify fix" },
      ],
      estimatedTokens: 15000,
      maxRetries: 2,
    };
  }
};
```

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

```typescript
// Planner → Generator → Evaluator
class AnthropicPlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  async plan(task: string): Promise<Plan> {
    // 1. Analyze the complexity of the task
    const complexity = await this.estimateComplexity(task);
    
    // 2. Create the step-by-step plan
    const steps = await this.generateSteps(task, complexity);
    
    // 3. Add the dependency graph
    const graphedSteps = this.addDependencies(steps);
    
    return {
      steps: graphedSteps,
      estimatedComplexity: complexity,
      parallelizableGroups: this.findParallelGroups(graphedSteps),
    };
  }
  
  private findParallelGroups(steps: Step[]): Step[][] {
    // Find steps that can run in parallel (no dependencies on each other)
    const groups: Step[][] = [];
    const remaining = [...steps];
    
    while (remaining.length > 0) {
      const group = remaining.filter(s => 
        s.dependencies.every(dep => 
          groups.some(g => g.some(gs => gs.id === dep))
        )
      );
      groups.push(group);
      remaining.splice(0, group.length);
    }
    
    return groups;
  }
}
```

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

```typescript
// Hierarchical Planning — 3 levels
class ClaudePlanningSystem {
  // Level 1: Strategic planning (task level)
  async strategicPlan(goal: string): Promise<StrategicPlan> {
    return {
      approach: await this.selectApproach(goal),
      phases: await this.definePhases(goal),
      estimatedTime: await this.estimateTime(goal),
      checkpoints: await this.defineCheckpoints(goal),
    };
  }
  
  // Level 2: Tactical planning (phase level)
  async tacticalPlan(phase: Phase): Promise<TacticalPlan> {
    return {
      steps: await this.breakDownPhase(phase),
      tools: await this.selectTools(phase),
      parallelizable: await this.findParallelSteps(phase),
      rollbackPoints: await this.identifyRollbackPoints(phase),
    };
  }
  
  // Level 3: Operational planning (step level)
  async operationalPlan(step: Step): Promise<OperationalPlan> {
    return {
      action: await this.defineAction(step),
      parameters: await this.extractParameters(step),
      validation: await this.defineValidation(step),
      errorHandling: await this.defineErrorHandling(step),
    };
  }
}
```

</details>

**Core feature — Dynamic Re-planning**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// Claude Code automatically re-plans when it hits a problem
class DynamicReplanner {
  async handleFailure(
    failedStep: Step, 
    error: Error, 
    currentPlan: Plan
  ): Promise<Plan> {
    // 1. Analyze the error
    const analysis = await this.analyzeFailure(failedStep, error);
    
    // 2. Try to fix the error within the current plan
    if (analysis.canFixInPlace) {
      return this.adjustStep(failedStep, analysis.fix);
    }
    
    // 3. Re-plan from this point
    const remainingSteps = currentPlan.steps.filter(
      s => !s.dependencies.includes(failedStep.id)
    );
    
    return this.replan(remainingSteps, analysis.context);
  }
}
```

</details>

---

### 7.4. Cursor IDE — Context-Aware Planning

Context: Cursor has to plan code fixes **based on the developer's current context** — the open file, the selected code, the cursor line, and recent edits. The code below shows how it gathers that context, plans the changes, and then narrows its scope on its own so it does not touch unrelated files.

<details>
<summary><b>7.4. Cursor IDE — Context-Aware Planning (Click to expand/collapse)</b></summary>

```typescript
class CursorPlanner {
  async plan(codeChange: string): Promise<Plan> {
    // 1. Understand the current Context
    const context = {
      currentFile: editor.getCurrentFile(),
      selectedCode: editor.getSelection(),
      cursorLine: editor.getCursorLine(),
      recentEdits: this.getRecentEdits(5),
      relatedFiles: await this.findRelatedFiles(),
      gitContext: await git.getContext(),
    };
    
    // 2. Plan the changes
    const plan = await this.planChanges(codeChange, context);
    
    // 3. Minimize the scope (do not touch unrelated files)
    const scopedPlan = this.minimizeScope(plan, context.currentFile);
    
    return scopedPlan;
  }
  
  private minimizeScope(plan: Plan, currentFile: string): Plan {
    return {
      ...plan,
      steps: plan.steps.filter(step => 
        this.isRelated(step.file, currentFile) || step.essential
      ),
    };
  }
}
```

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

**1. Single Responsibility**
- Each planner handles only one kind of task (code, research, deploy)
- Each decomposition strategy handles one specific pattern

**2. Open/Closed (Open for Extension, Closed for Modification)**
- Open to new planning strategies
- Closed to modifying the core decomposition logic

**3. Liskov Substitution**
- Planners can substitute for one another
- Same interface, different implementations (ToT, Plan-and-Solve, ReWOO)

**4. Interface Segregation**
- Do not force a planner to handle every type
- Split planners by domain

**5. Dependency Inversion**
- The planner depends on the Task abstraction, not on a concrete implementation
- Easy to swap decomposition strategies

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

- **Decompose tasks by granularity**: broad → medium → fine-grained
- **Identify dependencies before executing**: use a DAG to represent them
- **Set a timeout and retries for each task**: prevents infinite loops
- **Checkpoint before each important operation**: so you can roll back
- **Re-plan when a failure occurs**: don't retry exactly the same way
- **Track token usage per task**: so you can optimize cost
- **Validate the result of each step**: fail fast
- **Parallelize independent tasks**: saves time

### 9.2 DON'T ❌

- **Don't execute the whole task in one go**: too risky
- **Don't ignore failures**: analyze the cause
- **Don't over-decompose**: a task that is too small = big overhead
- **Don't forget to update state**: state sync is very important
- **Don't hardcode the task order**: it should be computed from dependencies
- **Don't skip validation**: unverified output = not done
- **Don't allocate a token budget that is too large**: prevents waste
- **Don't use a single agent for complex tasks**: multi-agent is better

### 9.3 Token Budget Management

Each task should have a clear token "spending limit", like a credit card limit. The code below is the `TokenBudgetManager` class: it allocates the budget to each task (`allocate`), records the tokens used (`report`), checks whether there is enough budget left to keep going (`canContinue`), and exports a final performance report (`getReport`).

<details>
<summary><b>9.3 Token Budget Management (Click to expand/collapse)</b></summary>

```typescript
class TokenBudgetManager {
  private totalBudget: number;
  private allocated: Map<string, number>;
  private used: Map<string, number>;
  
  constructor(totalBudget: number = 100000) {
    this.totalBudget = totalBudget;
    this.allocated = new Map();
    this.used = new Map();
  }
  
  allocate(taskId: string, budget: number): boolean {
    const totalAllocated = Array.from(this.allocated.values()).reduce((a, b) => a + b, 0);
    
    if (totalAllocated + budget > this.totalBudget) {
      return false; // Not enough Token budget
    }
    
    this.allocated.set(taskId, budget);
    return true;
  }
  
  report(taskId: string, tokens: number): void {
    this.used.set(taskId, (this.used.get(taskId) || 0) + tokens);
  }
  
  canContinue(taskId: string): boolean {
    const allocated = this.allocated.get(taskId) || 0;
    const used = this.used.get(taskId) || 0;
    return used < allocated * 0.9; // Allow using up to 90%
  }
  
  getRemaining(): number {
    const totalUsed = Array.from(this.used.values()).reduce((a, b) => a + b, 0);
    return this.totalBudget - totalUsed;
  }
  
  getReport(): TokenReport {
    return {
      totalBudget: this.totalBudget,
      allocated: Object.fromEntries(this.allocated),
      used: Object.fromEntries(this.used),
      remaining: this.getRemaining(),
      efficiency: Array.from(this.used.values()).reduce((a, b) => a + b, 0) / 
                  Array.from(this.allocated.values()).reduce((a, b) => a + b, 1),
    };
  }
}
```

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

```python
import unittest

class TestTaskPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = TaskPlanner()
    
    def test_simple_decomposition(self):
        """Simple task → 1-3 subtasks"""
        task = Task(id="t1", name="Fix typo", description="Fix typo in README")
        plan = self.planner.decompose("Fix typo in README")
        self.assertLessEqual(len(plan), 3)
    
    def test_complex_decomposition(self):
        """Complex task → multiple subtasks"""
        plan = self.planner.decompose(
            "Build a complete RAG system with vector search, "
            "chunking, embedding, and query processing"
        )
        self.assertGreater(len(plan), 3)
    
    def test_complexity_estimation(self):
        """Estimate complexity correctly"""
        task = Task(id="t1", name="Simple", description="Simple task")
        estimate = self.planner.estimate_complexity(task)
        self.assertIn(estimate["complexity"], ["simple", "medium", "complex"])
    
    def test_dependency_detection(self):
        """Verify dependency-based execution order"""
        t1 = Task(id="t1", name="Setup DB", dependencies=[])
        t2 = Task(id="t2", name="Create schema", dependencies=["t1"])
        t3 = Task(id="t3", name="Insert data", dependencies=["t2"])
        
        completed = set()
        # t1 must be executable first
        self.assertTrue(t1.can_execute(completed))
        
        # t2 is NOT allowed to run yet
        self.assertFalse(t2.can_execute(completed))
        
        # After t1 completes
        completed.add("t1")
        self.assertTrue(t2.can_execute(completed))
    
    def test_max_depth_limit(self):
        """Verify decomposition respects max depth"""
        plan = self.planner.decompose(
            "Build: a → b → c → d → e → f",
            max_depth=2
        )
        depth = self.planner._get_depth(
            Task(id="root", subtasks=plan)
        )
        self.assertLessEqual(depth, 2)
    
    def test_retry_logic(self):
        """Test task retry on failure"""
        task = Task(id="t1", name="Flaky task", max_retries=3)
        
        # Fail the first time
        task.mark_failed("timeout")
        self.assertTrue(task.can_retry())
        
        # After 3 retries
        task.retry_count = 3
        self.assertFalse(task.can_retry())

class TestTokenBudget(unittest.TestCase):
    def setUp(self):
        self.budget_manager = TokenBudgetManager(totalBudget=50000)
    
    def test_allocation_within_budget(self):
        """Allocate within budget"""
        result = self.budget_manager.allocate("task1", 20000)
        self.assertTrue(result)
    
    def test_allocation_exceeds_budget(self):
        """Allocation exceeds budget"""
        self.budget_manager.allocate("task1", 30000)
        result = self.budget_manager.allocate("task2", 25000)
        self.assertFalse(result)
    
    def test_usage_tracking(self):
        """Track token usage per task"""
        self.budget_manager.allocate("task1", 10000)
        self.budget_manager.report("task1", 5000)
        
        self.assertTrue(self.budget_manager.canContinue("task1"))
        
        self.budget_manager.report("task1", 4500)
        self.assertFalse(self.budget_manager.canContinue("task1"))

class TestAgentState(unittest.TestCase):
    def setUp(self):
        self.state = AgentState()
    
    def test_set_and_get(self):
        self.state.set("key1", "value1")
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_checkpoint_and_rollback(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.assertEqual(self.state.get("key1"), "value2")
        
        self.state.rollback(cp)
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_diff(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.state.set("key2", "value3")
        
        changes = self.state.diff(cp)
        self.assertIn("key2", changes["added"])
        self.assertIn("key1", changes["modified"])

if __name__ == "__main__":
    unittest.main()
```

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

```python
class HTNPlanner:
    """
    Hierarchical Task Network planning
    
    Unlike simple decomposition, HTN uses:
    - Primitive tasks (can be executed directly)
    - Compound tasks (need further decomposition)
    - Methods (ways to decompose compound tasks)
    """
    
    def __init__(self):
        self.methods = {}  # task_type -> list of task decomposition methods
        self.primitive_actions = {}  # action_name -> implementation
    
    def add_method(self, task_type, method):
        if task_type not in self.methods:
            self.methods[task_type] = []
        self.methods[task_type].append(method)
    
    def decompose(self, task, depth=0, max_depth=5):
        if depth >= max_depth:
            return [task]
        
        if task["type"] in self.methods:
            for method in self.methods[task["type"]]:
                if method["precondition"](task):
                    subtasks = method["decompose"](task)
                    result = []
                    for subtask in subtasks:
                        result.extend(self.decompose(subtask, depth + 1, max_depth))
                    return result
        
        return [task]  # Primitive task
    
    def execute_plan(self, plan):
        results = []
        for task in plan:
            if task["name"] in self.primitive_actions:
                result = self.primitive_actions[task["name"]](task)
                results.append({"task": task, "result": result})
        return results
```

</details>

### 11.2 Self-Reflective Planning

The idea: the agent makes a plan, then **scores the quality of that plan itself** (completeness, feasibility, risks); if the score is low, it fixes the plan based on its own suggestions and repeats for a few rounds. The `SelfReflectivePlanner` class below implements exactly that Plan → Reflect → Improve loop, while also keeping a history of plans to learn from real outcomes.

> Like writing a draft essay: write it, read it back, fix the weak parts, and only then submit the final version.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class SelfReflectivePlanner:
    """
    Planner that improves by reflecting on its own plans
    
    Pattern: Plan → Execute → Reflect → Improve Plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.plan_history = []  # History of plans and outcomes
    
    def plan_with_reflection(self, task, max_reflections=3):
        """Plan with self-reflection"""
        plan = self._initial_plan(task)
        
        for reflection_round in range(max_reflections):
            # Reflect on the quality of the plan
            reflection = self._reflect_on_plan(task, plan)
            
            if reflection["quality_score"] >= 8:
                break  # Stop if the plan is good enough
            
            # Improve the plan based on the reflection
            plan = self._improve_plan(plan, reflection["suggestions"])
        
        return plan
    
    def _initial_plan(self, task):
        return {
            "steps": [],
            "estimated_complexity": 0,
            "risks": [],
        }
    
    def _reflect_on_plan(self, task, plan):
        if self.llm:
            prompt = f"""Analyze the following plan:

Task: {task}
Plan: {plan}

Evaluation:
1. Completeness (1-10)
2. Feasibility (1-10)
3. Risks (list)
4. Improvements (suggestions)"""
            
            response = self.llm(prompt)
            return {"quality_score": 7, "suggestions": [], "risks": []}
        
        return {"quality_score": 5, "suggestions": ["Add more detail"], "risks": []}
    
    def _improve_plan(self, plan, suggestions):
        plan["improvements"] = suggestions
        return plan
    
    def learn_from_outcome(self, task, plan, outcome):
        """Store plan outcome for future learning"""
        self.plan_history.append({
            "task": task,
            "plan": plan,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
        })
```

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

```python
from langgraph.graph import StateGraph, END

# Define the planning State Machine
def create_planning_graph():
    graph = StateGraph(dict)
    
    # Add the Nodes
    graph.add_node("analyze", analyze_task)
    graph.add_node("plan", create_plan)
    graph.add_node("validate", validate_plan)
    graph.add_node("execute", execute_step)
    graph.add_node("replan", replan_on_failure)
    
    # Add the Edges
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "validate")
    graph.add_conditional_edges("validate", decide_next, {
        "pass": "execute",
        "fail": "replan",
        "done": END,
    })
    graph.add_edge("execute", "validate")
    graph.add_edge("replan", "validate")
    
    return graph.compile()
```

</details>

### 12.2 CrewAI (Multi-Agent Planning)

CrewAI organizes agents as a **crew**: you define each role (Agent) with its own goal and tools, assign the tasks, and then let them cooperate to finish the work. The code below creates three typical roles: Planner (plans), Executor (executes), and Reviewer (reviews).

> Like setting up a small company with three departments, each with its own mission, working together to finish one project.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from crewai import Agent, Task, Crew

# Create specialized planning Agents
planner = Agent(
    role="Task Planner",
    goal="Break down complex tasks into actionable steps",
    backstory="Expert at task decomposition and dependency analysis",
    tools=[analysis_tool, research_tool],
)

executor = Agent(
    role="Task Executor", 
    goal="Execute planned tasks efficiently",
    backstory="Expert at implementation and testing",
    tools=[code_tool, test_tool],
)

reviewer = Agent(
    role="Plan Reviewer",
    goal="Review and validate task plans",
    backstory="Expert at quality assurance and risk assessment",
)

# Create the tasks
planning_task = Task(
    description="Create execution plan for: {task}",
    agent=planner,
)

execution_task = Task(
    description="Execute the plan created by planner",
    agent=executor,
)

# Assemble the Crew
crew = Crew(
    agents=[planner, executor, reviewer],
    tasks=[planning_task, execution_task],
    verbose=True,
)
```

</details>

### 12.3 AutoGen (Microsoft)

Microsoft's AutoGen lets agents **converse with each other** to coordinate — each agent is a "mind" that can send messages to other agents. The sample code below defines a planner that lays out the plan, an executor that carries it out, and a user proxy that stands in for the real human to sign off on the final result.

> Like a group chat discussing work: one person proposes, another does it, and someone gives the final sign-off before it's submitted.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from autogen import AssistantAgent, UserProxyAgent

planner = AssistantAgent(
    name="planner",
    llm_config={"model": "gpt-4"},
    system_message="""You are a planning specialist.
    Break down tasks into clear steps with dependencies.
    Always output JSON format."""
)

executor = AssistantAgent(
    name="executor",
    llm_config={"model": "gpt-4"},
    system_message="""You execute tasks based on the plan.
    Report completion status for each step."""
)

user = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
)
```

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
*Updated: 13/07/2026*
*Author: AI Knowledge Repository*
