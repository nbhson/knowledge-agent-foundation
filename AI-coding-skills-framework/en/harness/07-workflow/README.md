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

Imagine an **automotive factory**. Every car passes through hundreds of stations: frame assembly → engine mounting → painting → quality inspection → packaging. Without a **standardized process** — with each worker doing whatever they feel like — the result would be a disaster: missing bolts, streaky paint, missed inspections.

**An AI Agent is exactly the same when it lacks a Workflow.**

Many developers write agents that are just **a chain of consecutive function calls** — no state management, no error recovery, no checkpoints. For simple tasks, it works. But for complex tasks — **every failure means running again from the start**.

**The solution**: Structured Workflow — a system that manages the **entire lifecycle** of a task, from trigger to feedback, with the ability to **recover, checkpoint, and observe** at every step.

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

**Workflow** is the process of **designing and organizing execution steps** to complete a complex coding task. In Harness Engineering, the Workflow Engine is the **"dispatch center"** — managing the entire flow from trigger → plan → execute → validate → deploy, with observability, error recovery, and state management.

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

Like cooking a dish from a recipe: finish step 1 before moving to step 2, no skipping, no reordering. This is the simplest pattern — easy to write, easy to debug, but a bit slow because every step queues up behind the previous one. Use it when a later step must depend on the result of an earlier step. The diagram below illustrates the 5-step flow Parse → Analyze → Build → Test → Deploy:

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

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import uuid
import time
import json

class WorkflowError(Exception):
    """Error in workflow"""
    pass

class SequentialWorkflow:
    """Sequential workflow — each step's input is the previous step's output"""
    
    def __init__(self, name: str = "sequential"):
        self.name = name
        self.steps = []
        self.state = {}
        self.history = []
        self.hooks = {"before": [], "after": [], "on_error": [], "on_step": []}
    
    def add_step(self, name: str, func: Callable, **kwargs):
        self.steps.append({"name": name, "func": func, "kwargs": kwargs})
        return self
    
    def on(self, event: str, func: Callable):
        if event in self.hooks:
            self.hooks[event].append(func)
        return self
    
    def run(self, initial_input: Any) -> Any:
        current_input = initial_input
        self.state["status"] = "running"
        self.state["start_time"] = time.time()
        
        for hook in self.hooks["before"]:
            hook(self.name, initial_input)
        
        for i, step in enumerate(self.steps):
            step_name = step["name"]
            step_start = time.time()
            
            for hook in self.hooks["on_step"]:
                hook(step_name, i, len(self.steps))
            
            try:
                result = step["func"](current_input, **step["kwargs"])
                step_duration = time.time() - step_start
                
                self.history.append({
                    "step": step_name,
                    "input_type": type(current_input).__name__,
                    "output_type": type(result).__name__,
                    "status": "success",
                    "duration_ms": round(step_duration * 1000, 2),
                    "timestamp": datetime.now().isoformat(),
                })
                
                current_input = result
                
            except Exception as e:
                step_duration = time.time() - step_start
                error_entry = {
                    "step": step_name,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "status": "failed",
                    "duration_ms": round(step_duration * 1000, 2),
                    "timestamp": datetime.now().isoformat(),
                }
                self.history.append(error_entry)
                self.state["status"] = "failed"
                self.state["failed_step"] = step_name
                
                for hook in self.hooks["on_error"]:
                    hook(step_name, e)
                
                raise WorkflowError(f"Step '{step_name}' failed: {e}")
        
        total_duration = time.time() - self.state["start_time"]
        self.state["status"] = "completed"
        self.state["total_duration_ms"] = round(total_duration * 1000, 2)
        
        for hook in self.hooks["after"]:
            hook(self.name, current_input)
        
        return current_input
    
    def get_history(self) -> List[Dict]:
        return self.history
    
    def get_summary(self) -> Dict:
        total = len(self.history)
        success = sum(1 for h in self.history if h["status"] == "success")
        total_ms = sum(h.get("duration_ms", 0) for h in self.history)
        
        return {
            "workflow": self.name,
            "total_steps": total,
            "successful": success,
            "failed": total - success,
            "total_duration_ms": total_ms,
            "status": self.state.get("status", "unknown"),
        }
```

</details>

### 1.2 Parallel Workflow (Concurrent)

Like cooking a party with several helpers: at the same time one person washes the vegetables, one cooks the rice, one fries the meat — only after everything is done do they gather and clear the table. This pattern is fast because many steps run at once, but the hard part is gathering (fan-in) the results. Use it when the steps are independent of each other and don't need to wait on one another:

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

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

class ParallelWorkflow:
    """Parallel workflow — multiple steps at the same time"""
    
    def __init__(self, name: str = "parallel", max_workers: int = 4):
        self.name = name
        self.parallel_groups = []
        self.max_workers = max_workers
        self.history = []
    
    def add_parallel_group(self, steps):
        """
        Add a group of steps that run in parallel.
        steps: list of (name, func, args_dict)
        """
        self.parallel_groups.append({"type": "parallel", "steps": steps})
        return self
    
    def add_sequential_step(self, name: str, func: Callable):
        self.parallel_groups.append({
            "type": "sequential",
            "steps": [(name, func, {})],
        })
        return self
    
    def run(self, initial_input: Any) -> Any:
        current_input = initial_input
        
        for group_idx, group in enumerate(self.parallel_groups):
            if group["type"] == "sequential":
                name, func, args = group["steps"][0]
                current_input = func(current_input, **args)
            else:
                # Parallel group
                results = {}
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    futures = {}
                    for name, func, args in group["steps"]:
                        future = executor.submit(func, current_input, **args)
                        futures[future] = name
                    
                    for future in as_completed(futures):
                        name = futures[future]
                        try:
                            results[name] = future.result()
                        except Exception as e:
                            results[name] = {"error": str(e)}
                
                current_input = results
        
        return current_input
    
    def run_async(self, initial_input: Any) -> Any:
        """Async version for I/O-bound workflows"""
        return asyncio.run(self._run_async_impl(initial_input))
    
    async def _run_async_impl(self, initial_input: Any) -> Any:
        current_input = initial_input
        
        for group in self.parallel_groups:
            if group["type"] == "sequential":
                name, func, args = group["steps"][0]
                if asyncio.iscoroutinefunction(func):
                    current_input = await func(current_input, **args)
                else:
                    current_input = func(current_input, **args)
            else:
                tasks = []
                for name, func, args in group["steps"]:
                    if asyncio.iscoroutinefunction(func):
                        tasks.append(func(current_input, **args))
                    else:
                        loop = asyncio.get_event_loop()
                        tasks.append(loop.run_in_executor(None, func, current_input, **args))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                current_input = {
                    group["steps"][i][0]: r 
                    for i, r in enumerate(results)
                }
        
        return current_input
```

</details>

### 1.3 DAG Workflow (Directed Acyclic Graph)

Like a sports tournament bracket: the semifinal has to wait for both quarterfinals, but the two quarterfinals are played in parallel. A DAG is the most flexible pattern — each node runs only after the nodes it depends on (dependencies) have completed, one "level" at a time, with absolutely no loops. Example below: A and B run in parallel → C waits for A, D waits for B → E waits for C, F waits for D:

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

```python
class DAGWorkflow:
    """
    Workflow based on a Dependency Graph (DAG).
    
    Allows independent nodes to run in parallel,
    and waits for dependencies to complete before proceeding.
    
    Example:
        A ──► C ──► E
        B ──► D ──► F
        
    A and B run in parallel → C waits for A, D waits for B → E waits for C, F waits for D
    """
    
    def __init__(self, name: str = "dag"):
        self.name = name
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, List[str]] = {}  # node -> [dependents]
        self.reverse_edges: Dict[str, List[str]] = {}  # node -> [dependencies]
        self.history = []
    
    def add_node(self, name: str, func: Callable, depends_on: List[str] = None):
        """Add a node with optional dependencies"""
        self.nodes[name] = {"func": func, "name": name}
        self.edges[name] = []
        self.reverse_edges[name] = depends_on or []
        
        for dep in (depends_on or []):
            if dep not in self.edges:
                self.edges[dep] = []
            self.edges[dep].append(name)
        
        return self
    
    def topological_sort(self) -> List[List[str]]:
        """
        Topological sort — returns a list of levels
        Each level contains nodes that can run in parallel
        """
        in_degree = {node: 0 for node in self.nodes}
        for node, deps in self.reverse_edges.items():
            for dep in deps:
                in_degree[node] += 1
        
        levels = []
        queue = [n for n, d in in_degree.items() if d == 0]
        
        while queue:
            levels.append(sorted(queue))
            next_queue = []
            for node in queue:
                for dependent in self.edges.get(node, []):
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_queue.append(dependent)
            queue = next_queue
        
        # Validate: check for cycles
        total_nodes = sum(len(level) for level in levels)
        if total_nodes != len(self.nodes):
            raise WorkflowError("Cycle detected in DAG!")
        
        return levels
    
    def run(self, initial_data: Any = None) -> Dict:
        """Execute DAG level by level"""
        levels = self.topological_sort()
        results = {}
        node_results = {}
        
        for level_idx, level in enumerate(levels):
            if len(level) == 1:
                # Single node — run directly
                node_name = level[0]
                deps = {dep: results[dep] for dep in self.reverse_edges[node_name] if dep in results}
                input_data = {**deps, "_original": initial_data} if deps else initial_data
                
                result = self.nodes[node_name]["func"](input_data)
                results[node_name] = result
                node_results[node_name] = {"status": "success", "level": level_idx}
            else:
                # Parallel level
                with ThreadPoolExecutor(max_workers=len(level)) as executor:
                    futures = {}
                    for node_name in level:
                        deps = {dep: results[dep] for dep in self.reverse_edges[node_name] if dep in results}
                        input_data = {**deps, "_original": initial_data} if deps else initial_data
                        future = executor.submit(self.nodes[node_name]["func"], input_data)
                        futures[future] = node_name
                    
                    for future in as_completed(futures):
                        node_name = futures[future]
                        try:
                            result = future.result()
                            results[node_name] = result
                            node_results[node_name] = {"status": "success", "level": level_idx}
                        except Exception as e:
                            node_results[node_name] = {"status": "failed", "error": str(e), "level": level_idx}
        
        return {
            "results": results,
            "node_status": node_results,
            "levels": levels,
            "total_nodes": len(self.nodes),
            "successful": sum(1 for v in node_results.values() if v["status"] == "success"),
        }
    
    def validate(self) -> Dict:
        """Validate DAG structure"""
        issues = []
        
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for dep in self.reverse_edges.get(node, []):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    issues.append(f"Cycle: {node} → {dep}")
                    return True
            rec_stack.discard(node)
            return False
        
        for node in self.nodes:
            if node not in visited:
                has_cycle(node)
        
        # Check for missing dependencies
        for node, deps in self.reverse_edges.items():
            for dep in deps:
                if dep not in self.nodes:
                    issues.append(f"Missing dependency: {dep} (required by {node})")
        
        # Check for orphan nodes
        all_deps = set()
        for deps in self.reverse_edges.values():
            all_deps.update(deps)
        roots = [n for n in self.nodes if n not in all_deps and not self.reverse_edges.get(n)]
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "roots": roots,
            "levels": len(self.topological_sort()),
        }
```

</details>

### 1.4 Event-Driven Workflow

Like a fire alarm control center: wherever the bell rings (event), the on-duty team (handler) responds there, and each response can trigger a new alarm. Unlike the patterns above, the flow is not predefined from the start — the workflow reacts to each event as it occurs, making it very flexible for unpredictable systems:

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

```python
import queue
from typing import Callable, Dict, List, Optional
from datetime import datetime

class EventDrivenWorkflow:
    """
    Workflow reacts to events.
    
    Events trigger handlers, which may emit new events.
    Supports: pub/sub, event filtering, event chains.
    """
    
    def __init__(self, name: str = "event-driven"):
        self.name = name
        self.handlers: Dict[str, List[Callable]] = {}
        self.event_log: List[Dict] = []
        self.event_queue = queue.Queue()
        self._running = False
        self._max_events = 1000
    
    def on(self, event_type: str, handler: Callable):
        """Register handler for event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        return self
    
    def emit(self, event_type: str, data: Any = None):
        """Emit an event"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())[:8],
        }
        self.event_queue.put(event)
        self.event_log.append(event)
    
    def process_event(self, event: Dict):
        """Process a single event"""
        event_type = event["type"]
        handlers = self.handlers.get(event_type, [])
        
        if not handlers:
            self.event_log.append({
                **event,
                "status": "unhandled",
                "timestamp": datetime.now().isoformat(),
            })
            return
        
        for handler in handlers:
            try:
                result = handler(event["data"])
                self.event_log.append({
                    **event,
                    "handler": handler.__name__,
                    "status": "processed",
                    "result": str(result)[:200] if result else None,
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception as e:
                self.event_log.append({
                    **event,
                    "handler": handler.__name__,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })
    
    def run(self):
        """Process all queued events"""
        self._running = True
        event_count = 0
        
        while self._running and not self.event_queue.empty():
            if event_count >= self._max_events:
                break
            
            try:
                event = self.event_queue.get(timeout=1)
                self.process_event(event)
                event_count += 1
            except queue.Empty:
                break
        
        self._running = False
    
    def stop(self):
        self._running = False
    
    def get_stats(self) -> Dict:
        total = len(self.event_log)
        processed = sum(1 for e in self.event_log if e.get("status") == "processed")
        errors = sum(1 for e in self.event_log if e.get("status") == "error")
        
        event_types = {}
        for e in self.event_log:
            t = e.get("type", "unknown")
            event_types[t] = event_types.get(t, 0) + 1
        
        return {
            "total_events": total,
            "processed": processed,
            "errors": errors,
            "event_types": event_types,
            "queue_size": self.event_queue.qsize(),
        }
```

</details>

---

## 2. Pipeline Design

> **📌 Core Concept**
>
> - **Concept:** Pipeline design is how to split a large task into successive stages; each stage receives data from the previous stage, processes it, and passes it on, with branching and fan-out/fan-in capabilities.
> - **Analogy:** Like a beer factory line: mash → boil → filter → ferment → bottle; each step takes the output of the previous step, with a fork if the customer orders a different kind of beer.
> - **Why it matters:** Pipelines keep large data processing tidy, let you inspect every stage, and are easy to update when the business changes.

### 2.1 Data Pipeline with Branching

This is the "work line" for data: each stage is a stage (transform, filter, branch, fan_out, validator, sink), and data flows through the stages just like a product through a production line. The special part is branching — a stage checks a condition and then diverts the data into two different branches, like a conveyor belt with a diverting gate. The code below shows how to assemble and run a complete pipeline:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
@dataclass
class PipelineEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class PipelineResult:
    success: bool
    data: Any = None
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class Pipeline:
    """
    Advanced Pipeline with branching, transforms, filters, and sinks.
    
    Features:
    - Transform chain
    - Conditional branching
    - Fan-out / Fan-in
    - Error handling per stage
    - Metrics collection
    """
    
    def __init__(self, name: str):
        self.name = name
        self.stages: List[Dict] = []
        self.hooks = {"before": [], "after": [], "on_error": [], "on_stage": []}
        self.metrics = PipelineMetrics()
    
    def add_transform(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "transform",
            "name": name or func.__name__,
            "func": func,
        })
        return self
    
    def add_filter(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "filter",
            "name": name or "filter",
            "func": func,
        })
        return self
    
    def add_branch(self, condition: Callable, true_pipeline: "Pipeline", 
                   false_pipeline: Optional["Pipeline"] = None, name: str = "branch") -> "Pipeline":
        self.stages.append({
            "type": "branch",
            "name": name,
            "condition": condition,
            "true_pipeline": true_pipeline,
            "false_pipeline": false_pipeline,
        })
        return self
    
    def add_fan_out(self, tasks: List[Dict], aggregator: Callable = None) -> "Pipeline":
        """Fan-out: split into parallel tasks, then aggregate"""
        self.stages.append({
            "type": "fan_out",
            "name": "fan_out",
            "tasks": tasks,
            "aggregator": aggregator or (lambda results: results),
        })
        return self
    
    def add_sink(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "sink",
            "name": name or func.__name__,
            "func": func,
        })
        return self
    
    def add_validator(self, func: Callable, name: str = None) -> "Pipeline":
        self.stages.append({
            "type": "validator",
            "name": name or "validate",
            "func": func,
        })
        return self
    
    def on(self, event: str, func: Callable) -> "Pipeline":
        if event in self.hooks:
            self.hooks[event].append(func)
        return self
    
    def run(self, data: Any) -> PipelineResult:
        start_time = time.time()
        errors = []
        
        for hook in self.hooks["before"]:
            hook(self.name, data)
        
        try:
            for stage in self.stages:
                stage_start = time.time()
                stage_name = stage["name"]
                
                for hook in self.hooks["on_stage"]:
                    hook(stage_name, data)
                
                try:
                    if stage["type"] == "transform":
                        data = stage["func"](data)
                    
                    elif stage["type"] == "filter":
                        if not stage["func"](data):
                            return PipelineResult(
                                success=False,
                                errors=[f"Filter '{stage_name}' rejected data"],
                                metrics=self.metrics.get_summary(),
                            )
                    
                    elif stage["type"] == "branch":
                        condition_result = stage["condition"](data)
                        if condition_result and stage["true_pipeline"]:
                            result = stage["true_pipeline"].run(data)
                            data = result.data
                        elif not condition_result and stage["false_pipeline"]:
                            result = stage["false_pipeline"].run(data)
                            data = result.data
                    
                    elif stage["type"] == "fan_out":
                        task_results = {}
                        with ThreadPoolExecutor(max_workers=4) as executor:
                            futures = {}
                            for task in stage["tasks"]:
                                f = executor.submit(task["func"], data)
                                futures[f] = task["name"]
                            for f in as_completed(futures):
                                task_results[futures[f]] = f.result()
                        data = stage["aggregator"](task_results)
                    
                    elif stage["type"] == "validator":
                        valid = stage["func"](data)
                        if not valid:
                            return PipelineResult(
                                success=False,
                                errors=[f"Validation '{stage_name}' failed"],
                                metrics=self.metrics.get_summary(),
                            )
                    
                    elif stage["type"] == "sink":
                        stage["func"](data)
                    
                    stage_duration = (time.time() - stage_start) * 1000
                    self.metrics.record(stage_name, stage_duration, True)
                    
                except Exception as e:
                    stage_duration = (time.time() - stage_start) * 1000
                    self.metrics.record(stage_name, stage_duration, False)
                    errors.append(f"{stage_name}: {str(e)}")
                    
                    for hook in self.hooks["on_error"]:
                        hook(stage_name, e)
                    
                    if stage["type"] != "sink":
                        raise WorkflowError(f"Pipeline stage '{stage_name}' failed: {e}")
            
            total_duration = (time.time() - start_time) * 1000
            
            for hook in self.hooks["after"]:
                hook(self.name, data)
            
            return PipelineResult(
                success=True,
                data=data,
                metrics=self.metrics.get_summary(),
            )
            
        except Exception as e:
            return PipelineResult(
                success=False,
                errors=errors or [str(e)],
                metrics=self.metrics.get_summary(),
            )


class PipelineMetrics:
    def __init__(self):
        self.stages: Dict[str, Dict] = {}
    
    def record(self, stage_name: str, duration_ms: float, success: bool):
        if stage_name not in self.stages:
            self.stages[stage_name] = {
                "runs": 0, "success": 0, "fail": 0, "total_ms": 0
            }
        s = self.stages[stage_name]
        s["runs"] += 1
        s["total_ms"] += duration_ms
        if success:
            s["success"] += 1
        else:
            s["fail"] += 1
    
    def get_summary(self) -> Dict:
        return {
            stage: {
                "runs": s["runs"],
                "avg_ms": round(s["total_ms"] / s["runs"], 2) if s["runs"] else 0,
                "success_rate": round(s["success"] / s["runs"], 2) if s["runs"] else 0,
            }
            for stage, s in self.stages.items()
        }
```

</details>

---

## 3. State Machine

> **📌 Core Concept**
>
> - **Concept:** A state machine is a "state machine" — a model that records which state the agent is in (reading code, writing code, running tests) and only allows moving to the next state when certain conditions are met.
> - **Analogy:** Like a three-color traffic light: a car may only proceed on green, and the green → yellow → red sequence is always in order and never jumps straight from red to green.
> - **Why it matters:** It prevents the agent from jumping around between steps, keeping the execution flow always valid and predictable.

### 3.1 Hierarchical State Machine

This is the "upgraded" version of a state machine: besides conditional state transitions, it also supports parent/child states (hierarchical), guards that block illegal transitions, automatic timeouts, and iteration limits — safe enough to drive a whole AI coding agent. The code below simulates an agent moving through the state chain IDLE → THINKING → PLANNING → READING_CODE → WRITING_CODE → RUNNING_TESTS → DONE:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Callable, Optional, List, Any

class AgentState(Enum):
    IDLE = "idle"
    THINKING = "thinking"
    PLANNING = "planning"
    READING_CODE = "reading_code"
    WRITING_CODE = "writing_code"
    RUNNING_TESTS = "running_tests"
    FIXING_ERRORS = "fixing_errors"
    REVIEWING = "reviewing"
    COMMITTING = "committing"
    DONE = "done"
    ERROR = "error"
    WAITING_APPROVAL = "waiting_approval"
    ROLLING_BACK = "rolling_back"


@dataclass
class Transition:
    from_state: AgentState
    to_state: AgentState
    condition: Callable[[Dict], bool]
    action: Optional[Callable] = None
    guard: Optional[Callable] = None  # Extra validation
    name: str = ""


class HierarchicalStateMachine:
    """
    Advanced Finite State Machine for AI coding agents.
    
    Features:
    - Hierarchical states (parent/child)
    - Guards on transitions
    - Actions on transitions
    - History tracking
    - Max iteration protection
    - State timeout handling
    """
    
    def __init__(self, name: str = "agent"):
        self.name = name
        self.state = AgentState.IDLE
        self.transitions: List[Transition] = []
        self.history: List[Dict] = []
        self.context: Dict = {}
        self.max_history = 100
        self._state_enter_time = time.time()
        self._state_timeouts: Dict[AgentState, float] = {}
    
    def set_timeout(self, state: AgentState, seconds: float):
        """Set timeout for a state (auto-transition to ERROR)"""
        self._state_timeouts[state] = seconds
    
    def add_transition(self, transition: Transition):
        self.transitions.append(transition)
        return self
    
    def can_transition(self, to_state: AgentState) -> bool:
        """Check if transition to target state is possible"""
        for t in self.transitions:
            if t.from_state == self.state and t.to_state == to_state:
                if t.guard and not t.guard(self.context):
                    return False
                return t.condition(self.context)
        return False
    
    def transition(self) -> Optional[Transition]:
        """Try all transitions from current state"""
        for t in self.transitions:
            if t.from_state == self.state and t.condition(self.context):
                # Check guard
                if t.guard and not t.guard(self.context):
                    continue
                
                old_state = self.state
                
                # Execute action
                if t.action:
                    t.action(self.context)
                
                # Record history
                entry = {
                    "from": old_state.value,
                    "to": t.to_state.value,
                    "transition": t.name or f"{old_state.value} → {t.to_state.value}",
                    "context_keys": list(self.context.keys()),
                    "timestamp": datetime.now().isoformat(),
                    "state_duration_ms": round((time.time() - self._state_enter_time) * 1000, 2),
                }
                self.history.append(entry)
                
                # Enforce history limit
                if len(self.history) > self.max_history:
                    self.history = self.history[-self.max_history:]
                
                self.state = t.to_state
                self._state_enter_time = time.time()
                return t
        
        return None
    
    def check_timeout(self) -> bool:
        """Check if current state has timed out"""
        if self.state in self._state_timeouts:
            elapsed = time.time() - self._state_enter_time
            if elapsed > self._state_timeouts[self.state]:
                self.context["error"] = f"State {self.state.value} timed out after {elapsed:.1f}s"
                self.state = AgentState.ERROR
                return True
        return False
    
    def run(self, task: Dict, max_iterations: int = 50) -> Any:
        """Run FSM until DONE or ERROR"""
        self.context["task"] = task
        self._state_enter_time = time.time()
        
        for i in range(max_iterations):
            # Check timeout
            if self.check_timeout():
                break
            
            if self.state == AgentState.DONE:
                return self.context.get("result")
            
            if self.state == AgentState.ERROR:
                raise RuntimeError(f"Agent error: {self.context.get('error')}")
            
            transition = self.transition()
            if not transition:
                break
        
        return self.context.get("result")
    
    def get_state_path(self) -> List[str]:
        """Get the path of states visited"""
        return [h["from"] for h in self.history] + [self.state.value]
    
    def get_stats(self) -> Dict:
        transitions_count = len(self.history)
        state_counts = {}
        for h in self.history:
            state = h["from"]
            state_counts[state] = state_counts.get(state, 0) + 1
        
        return {
            "current_state": self.state.value,
            "total_transitions": transitions_count,
            "state_visits": state_counts,
            "avg_transition_ms": (
                sum(h.get("state_duration_ms", 0) for h in self.history) / transitions_count
                if transitions_count else 0
            ),
        }
```

</details>

---

## 4. Error Recovery

> **📌 Core Concept**
>
> - **Concept:** Error recovery is the set of strategies for handling what happens when a workflow hits an error — retry with increasing waits (retry/backoff), fall back to an alternative, or cut the circuit as protection (circuit breaker) — so the system stays stable instead of the whole process crashing.
> - **Analogy:** Like making a phone call when the line is busy: try again after a minute (retry), if that fails wait longer (backoff), or dial a second person instead (fallback).
> - **Why it matters:** Errors will happen for sure; with a recovery strategy, the workflow doesn't just die midway.

### 4.1 Retry Strategies

Like pressing "resend" on an email when the network is flaky — but done scientifically: retry with increasing wait intervals (1s → 2s → 4s) so you don't overload the service, and add jitter (random noise) so clients don't all rush in at once like a stampede (thundering herd). The code below is a retry decorator that works for both sync and async functions:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
from functools import wraps
from typing import Type, Tuple, Optional

class RetryExhausted(Exception):
    pass

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    max_backoff: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable = None,
    jitter: bool = True,
):
    """
    Retry decorator with exponential backoff + jitter.
    
    Jitter prevents thundering herd when many clients retry simultaneously.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import random
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        wait_time = backoff_factor * (2 ** (attempt - 1))
                        if jitter:
                            wait_time *= (0.5 + random.random())
                        wait_time = min(wait_time, max_backoff)
                        
                        if on_retry:
                            on_retry(attempt, e, wait_time)
                        
                        time.sleep(wait_time)
            
            raise RetryExhausted(
                f"All {max_attempts} attempts failed. Last error: {last_exception}"
            )
        return wrapper
    return decorator


def async_retry(
    max_attempts: int = 3,
    backoff_factor: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """Async version of retry decorator"""
    import asyncio
    import random
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait = backoff_factor * (2 ** (attempt - 1)) * (0.5 + random.random())
                        await asyncio.sleep(wait)
            raise RetryExhausted(f"All {max_attempts} attempts failed: {last_exception}")
        return wrapper
    return decorator
```

</details>

### 4.2 Circuit Breaker Pattern

Like a fuse in a house: when the fault current gets too heavy the fuse blows, cutting the power to protect the whole system. Here, when a service keeps failing past the threshold, the circuit switches from CLOSED (closed, still calling) to OPEN (open, blocking calls); after a recovery period, it tries again in the HALF_OPEN state to see whether the service is healthy again:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """
    Circuit Breaker — avoids calling a service that keeps failing.
    
    CLOSED → OPEN (when enough failures) → HALF_OPEN (after recovery timeout) → CLOSED/OPEN
    """
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0,
                 half_open_max_calls: int = 1):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.half_open_calls = 0
        self.history: List[Dict] = []
    
    def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                self._log_transition("OPEN", "HALF_OPEN")
            else:
                raise CircuitOpenError(
                    f"Circuit is OPEN. Retry after {self._time_until_half_open():.0f}s"
                )
        
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise CircuitOpenError("Half-open limit reached")
            self.half_open_calls += 1
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self._log_transition("HALF_OPEN", "CLOSED")
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self._log_transition("HALF_OPEN", "OPEN")
            elif self.state == CircuitState.CLOSED:
                self.state = CircuitState.OPEN
                self._log_transition("CLOSED", "OPEN")
    
    def _time_until_half_open(self) -> float:
        return max(0, self.recovery_timeout - (time.time() - self.last_failure_time))
    
    def _log_transition(self, from_state: str, to_state: str):
        self.history.append({
            "from": from_state,
            "to": to_state,
            "failure_count": self.failure_count,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_state(self) -> Dict:
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "time_until_half_open": self._time_until_half_open() if self.state == CircuitState.OPEN else 0,
        }


class CircuitOpenError(Exception):
    pass
```

</details>

### 4.3 Saga Pattern

Like processing a package tour booking: if something breaks midway at the "book flight tickets" step, you have to cancel the steps that already succeeded — refund the hotel, refund the insurance. Sagas are used for business processes spanning multiple services: every step has a compensation (compensating step) to roll back when any step fails:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable  # Rollback function
    max_retries: int = 3

class SagaOrchestrator:
    """
    Saga Pattern — distributed transactions across multiple services.
    
    If any step fails → compensating transactions run in reverse
    to undo the previously successful steps.
    
    Flow:
    1. Step A (success) → Step B (success) → Step C (FAIL)
    2. Compensation: undo B → undo A
    """
    
    def __init__(self, name: str = "saga"):
        self.name = name
        self.steps: List[SagaStep] = []
        self.completed_steps: List[Dict] = []
        self.history: List[Dict] = []
    
    def add_step(self, name: str, action: Callable, compensation: Callable):
        self.steps.append(SagaStep(name=name, action=action, compensation=compensation))
        return self
    
    def execute(self, initial_data: Any = None) -> Dict:
        data = initial_data
        compensated = False
        
        for step in self.steps:
            try:
                result = step.action(data)
                self.completed_steps.append({
                    "name": step.name,
                    "result": result,
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                })
                data = result
            except Exception as e:
                self.history.append({
                    "failed_step": step.name,
                    "error": str(e),
                    "compensating": True,
                    "timestamp": datetime.now().isoformat(),
                })
                
                # Compensate in reverse order
                for completed in reversed(self.completed_steps):
                    try:
                        completed["compensation"]()
                        self.history.append({
                            "compensated": completed["name"],
                            "status": "success",
                            "timestamp": datetime.now().isoformat(),
                        })
                    except Exception as comp_e:
                        self.history.append({
                            "compensation_failed": completed["name"],
                            "error": str(comp_e),
                            "timestamp": datetime.now().isoformat(),
                        })
                
                compensated = True
                return {
                    "success": False,
                    "failed_step": step.name,
                    "error": str(e),
                    "compensated": True,
                    "compensation_history": [
                        h for h in self.history if "compensated" in h
                    ],
                }
        
        return {
            "success": True,
            "completed_steps": [s["name"] for s in self.completed_steps],
            "result": data,
        }
```

</details>

---

## 5. Observability

> **📌 Core Concept**
>
> - **Concept:** Observability is the ability to "see inside" a workflow through three kinds of data — logs (event records), metrics (measurements), and traces (the footprints of each request) — to know exactly what happened at each step.
> - **Analogy:** Like a taxi's dashcam + instrument cluster + GPS map: you know where the car is going, how fast or slow it's moving, and where it's stuck.
> - **Why it matters:** Without observability, when a workflow is slow or wrong you can't find the root cause and you have to debug step by step by feel.

### 5.1 Distributed Tracing

Like a "tracing order" that follows an entire journey: each request is assigned a unique trace_id, and however many services it passes through, each hop is recorded as spans (parent span, child span) — that way you can reconstruct the whole journey of a request and pinpoint exactly which step is slow or broken:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
import uuid
from contextlib import contextmanager
from typing import Dict, List, Any, Optional

class Span:
    """A single unit of work in a trace"""
    
    def __init__(self, name: str, trace_id: str, parent_span_id: str = None):
        self.name = name
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id
        self.parent_span_id = parent_span_id
        self.start_time = time.time()
        self.end_time = None
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict] = []
        self.status = "OK"
    
    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value
    
    def add_event(self, name: str, attributes: Dict = None):
        self.events.append({
            "name": name,
            "attributes": attributes or {},
            "timestamp": datetime.now().isoformat(),
        })
    
    def finish(self, status: str = "OK"):
        self.end_time = time.time()
        self.status = status
    
    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return (time.time() - self.start_time) * 1000
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
        }


class Tracer:
    """
    Distributed tracing system for workflow observability.
    
    Creates traces with nested spans, enabling:
    - End-to-end latency tracking
    - Bottleneck identification
    - Error attribution
    """
    
    _current_trace_id: Optional[str] = None
    _current_span_id: Optional[str] = None
    
    def __init__(self):
        self.traces: Dict[str, List[Span]] = {}
    
    def start_trace(self, name: str) -> str:
        trace_id = str(uuid.uuid4())[:12]
        span = Span(name, trace_id)
        self.traces[trace_id] = [span]
        Tracer._current_trace_id = trace_id
        Tracer._current_span_id = span.span_id
        return trace_id
    
    @contextmanager
    def span(self, name: str, attributes: Dict = None):
        trace_id = Tracer._current_trace_id or str(uuid.uuid4())[:12]
        parent_id = Tracer._current_span_id
        
        new_span = Span(name, trace_id, parent_id)
        if attributes:
            for k, v in attributes.items():
                new_span.set_attribute(k, v)
        
        if trace_id not in self.traces:
            self.traces[trace_id] = []
        self.traces[trace_id].append(new_span)
        
        old_span_id = Tracer._current_span_id
        Tracer._current_span_id = new_span.span_id
        
        try:
            yield new_span
            new_span.finish("OK")
        except Exception as e:
            new_span.set_attribute("error", str(e))
            new_span.finish("ERROR")
            raise
        finally:
            Tracer._current_span_id = old_span_id
    
    def get_trace(self, trace_id: str) -> List[Dict]:
        spans = self.traces.get(trace_id, [])
        return [s.to_dict() for s in sorted(spans, key=lambda s: s.start_time)]
    
    def get_trace_summary(self, trace_id: str) -> Dict:
        spans = self.traces.get(trace_id, [])
        if not spans:
            return {"error": "Trace not found"}
        
        root = min(spans, key=lambda s: s.start_time)
        total_duration = max(s.end_time or time.time() for s in spans) - root.start_time
        
        return {
            "trace_id": trace_id,
            "root_span": root.name,
            "total_spans": len(spans),
            "total_duration_ms": round(total_duration * 1000, 2),
            "errors": sum(1 for s in spans if s.status == "ERROR"),
            "spans": [s.to_dict() for s in spans],
        }
```

</details>

### 5.2 Structured Logging + Metrics

Like a machine's thermometer + logbook: one side (structured logging) records each event as structured JSON that's easy to filter and search, the other side (metrics) counts and aggregates numbers — run counts, success rates, p50/p95/p99 latencies. The code below contains two layers, WorkflowLogger and MetricsCollector:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class WorkflowLogger:
    """Structured logger for workflow"""
    
    def __init__(self, workflow_name: str, log_file: str = None):
        self.workflow_name = workflow_name
        self.logs = []
        self.log_file = log_file
    
    def log_step(self, step: str, status: str, data: Dict = None, duration: float = None):
        entry = {
            "workflow": self.workflow_name,
            "step": step,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": round(duration * 1000, 2) if duration else None,
            "data": data or {},
        }
        self.logs.append(entry)
        
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
    
    @contextmanager
    def track(self, step_name: str):
        start = time.time()
        self.log_step(step_name, "start")
        try:
            yield
            duration = time.time() - start
            self.log_step(step_name, "success", duration=duration)
        except Exception as e:
            duration = time.time() - start
            self.log_step(step_name, "error", data={"error": str(e)}, duration=duration)
            raise
    
    def export_json(self, path: str = None) -> str:
        output = json.dumps(self.logs, indent=2, ensure_ascii=False)
        if path:
            with open(path, "w") as f:
                f.write(output)
        return output


class MetricsCollector:
    """Collects and aggregates metrics"""
    
    def __init__(self):
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        self.histograms: Dict[str, List[float]] = {}
    
    def counter(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value
    
    def gauge(self, name: str, value: float):
        self.gauges[name] = value
    
    def histogram(self, name: str, value: float):
        if name not in self.histograms:
            self.histograms[name] = []
        self.histograms[name].append(value)
    
    def get_summary(self) -> Dict:
        summary = {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {},
        }
        
        for name, values in self.histograms.items():
            sorted_vals = sorted(values)
            n = len(sorted_vals)
            summary["histograms"][name] = {
                "count": n,
                "min": sorted_vals[0] if n else 0,
                "max": sorted_vals[-1] if n else 0,
                "mean": sum(sorted_vals) / n if n else 0,
                "p50": sorted_vals[n // 2] if n else 0,
                "p95": sorted_vals[int(n * 0.95)] if n else 0,
                "p99": sorted_vals[int(n * 0.99)] if n else 0,
            }
        
        return summary
```

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

```python
class WorkflowOrchestrator:
    """
    Complete workflow orchestration engine combining all patterns:
    - State machine for flow control
    - Pipeline for data processing
    - Saga for error recovery
    - Tracing for observability
    - Metrics for monitoring
    """
    
    def __init__(self, name: str):
        self.name = name
        self.tracer = Tracer()
        self.logger = WorkflowLogger(name)
        self.metrics = MetricsCollector()
        self.state_machine = HierarchicalStateMachine(name)
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.workflows: Dict[str, Callable] = {}
        self._setup_default_transitions()
    
    def _setup_default_transitions(self):
        """Setup default state transitions"""
        sm = self.state_machine
        
        sm.add_transition(Transition(
            from_state=AgentState.IDLE,
            to_state=AgentState.THINKING,
            condition=lambda ctx: ctx.get("task") is not None,
            name="task_received",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.THINKING,
            to_state=AgentState.PLANNING,
            condition=lambda ctx: ctx.get("analysis_done"),
            name="analysis_complete",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.PLANNING,
            to_state=AgentState.READING_CODE,
            condition=lambda ctx: ctx.get("plan_ready"),
            name="plan_approved",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.READING_CODE,
            to_state=AgentState.WRITING_CODE,
            condition=lambda ctx: ctx.get("code_read"),
            name="context_gathered",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.WRITING_CODE,
            to_state=AgentState.RUNNING_TESTS,
            condition=lambda ctx: ctx.get("code_written"),
            name="code_written",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.RUNNING_TESTS,
            to_state=AgentState.DONE,
            condition=lambda ctx: ctx.get("tests_passed"),
            name="tests_passed",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.RUNNING_TESTS,
            to_state=AgentState.FIXING_ERRORS,
            condition=lambda ctx: ctx.get("tests_failed"),
            name="tests_failed",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.FIXING_ERRORS,
            to_state=AgentState.RUNNING_TESTS,
            condition=lambda ctx: True,
            name="fix_applied",
        ))
        
        # Max fix attempts → ROLLBACK
        sm.add_transition(Transition(
            from_state=AgentState.FIXING_ERRORS,
            to_state=AgentState.ROLLING_BACK,
            condition=lambda ctx: ctx.get("fix_attempts", 0) >= 3,
            name="max_fixes_reached",
        ))
        
        sm.add_transition(Transition(
            from_state=AgentState.ROLLING_BACK,
            to_state=AgentState.ERROR,
            condition=lambda ctx: ctx.get("rollback_done"),
            name="rollback_complete",
        ))
    
    def register_workflow(self, name: str, func: Callable):
        self.workflows[name] = func
        return self
    
    def get_circuit_breaker(self, service: str) -> CircuitBreaker:
        if service not in self.circuit_breakers:
            self.circuit_breakers[service] = CircuitBreaker(
                failure_threshold=5, recovery_timeout=30
            )
        return self.circuit_breakers[service]
    
    def execute(self, task: Dict) -> Dict:
        trace_id = self.tracer.start_trace(f"workflow_{self.name}")
        
        with self.tracer.span("orchestrate", {"task": str(task)[:200]}):
            try:
                self.state_machine.context["task"] = task
                result = self.state_machine.run(task, max_iterations=50)
                
                self.metrics.counter("workflow.success")
                self.metrics.counter(f"workflow.{self.name}.success")
                
                return {
                    "success": True,
                    "result": result,
                    "trace_id": trace_id,
                    "state_path": self.state_machine.get_state_path(),
                    "stats": self.state_machine.get_stats(),
                }
            except Exception as e:
                self.metrics.counter("workflow.error")
                return {
                    "success": False,
                    "error": str(e),
                    "trace_id": trace_id,
                    "state_path": self.state_machine.get_state_path(),
                }
    
    def get_dashboard(self) -> Dict:
        """Get comprehensive dashboard data"""
        return {
            "workflow": self.name,
            "state": self.state_machine.state.value,
            "stats": self.state_machine.get_stats(),
            "circuit_breakers": {
                name: cb.get_state()
                for name, cb in self.circuit_breakers.items()
            },
            "traces_count": len(self.tracer.traces),
            "metrics": self.metrics.get_summary(),
            "history": self.logger.logs[-10:],  # Last 10 logs
        }
```

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

```python
import unittest

class TestSequentialWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = SequentialWorkflow("test_seq")
        self.workflow.add_step("step1", lambda x: x * 2)
        self.workflow.add_step("step2", lambda x: x + 10)
        self.workflow.add_step("step3", lambda x: x ** 2)
    
    def test_basic_run(self):
        result = self.workflow.run(5)
        self.assertEqual(result, 400)  # (5*2 + 10)^2 = 400
    
    def test_history_recorded(self):
        self.workflow.run(5)
        history = self.workflow.get_history()
        self.assertEqual(len(history), 3)
        self.assertTrue(all(h["status"] == "success" for h in history))
    
    def test_error_handling(self):
        workflow = SequentialWorkflow("test_error")
        workflow.add_step("fail", lambda x: 1/0)
        
        with self.assertRaises(WorkflowError):
            workflow.run(1)
        
        self.assertEqual(workflow.state["status"], "failed")
    
    def test_summary(self):
        self.workflow.run(5)
        summary = self.workflow.get_summary()
        self.assertEqual(summary["total_steps"], 3)
        self.assertEqual(summary["successful"], 3)
        self.assertEqual(summary["status"], "completed")


class TestDAGWorkflow(unittest.TestCase):
    def test_linear_dag(self):
        dag = DAGWorkflow("test_linear")
        dag.add_node("A", lambda x: 1)
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        dag.add_node("C", lambda x: 3, depends_on=["B"])
        
        result = dag.run()
        self.assertEqual(result["total_nodes"], 3)
        self.assertEqual(result["successful"], 3)
    
    def test_parallel_dag(self):
        dag = DAGWorkflow("test_parallel")
        dag.add_node("A", lambda x: 10)
        dag.add_node("B", lambda x: 20)
        dag.add_node("C", lambda x: 30, depends_on=["A", "B"])
        
        result = dag.run()
        self.assertEqual(result["total_nodes"], 3)
    
    def test_cycle_detection(self):
        dag = DAGWorkflow("test_cycle")
        dag.add_node("A", lambda x: 1, depends_on=["C"])
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        dag.add_node("C", lambda x: 3, depends_on=["B"])
        
        validation = dag.validate()
        self.assertFalse(validation["valid"])
    
    def test_validation(self):
        dag = DAGWorkflow("test_valid")
        dag.add_node("A", lambda x: 1)
        dag.add_node("B", lambda x: 2, depends_on=["A"])
        
        validation = dag.validate()
        self.assertTrue(validation["valid"])


class TestCircuitBreaker(unittest.TestCase):
    def setUp(self):
        self.cb = CircuitBreaker(failure_threshold=3, recovery_timeout=0.1)
    
    def test_normal_flow(self):
        result = self.cb.call(lambda: "ok")
        self.assertEqual(result, "ok")
        self.assertEqual(self.cb.state, CircuitState.CLOSED)
    
    def test_trips_after_failures(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        self.assertEqual(self.cb.state, CircuitState.OPEN)
    
    def test_rejects_when_open(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        
        with self.assertRaises(CircuitOpenError):
            self.cb.call(lambda: "ok")
    
    def test_half_open_recovery(self):
        for _ in range(3):
            try:
                self.cb.call(lambda: 1/0)
            except:
                pass
        
        time.sleep(0.15)
        result = self.cb.call(lambda: "recovered")
        self.assertEqual(result, "recovered")


class TestSagaOrchestrator(unittest.TestCase):
    def test_successful_saga(self):
        saga = SagaOrchestrator("test_saga")
        saga.add_step("step1", lambda x: "result1", lambda: None)
        saga.add_step("step2", lambda x: "result2", lambda: None)
        
        result = saga.execute()
        self.assertTrue(result["success"])
    
    def test_compensation_on_failure(self):
        compensated = []
        
        saga = SagaOrchestrator("test_compensate")
        saga.add_step("step1", lambda x: "ok", lambda: compensated.append("undo1"))
        saga.add_step("step2", lambda x: 1/0, lambda: compensated.append("undo2"))
        saga.add_step("step3", lambda x: "ok", lambda: compensated.append("undo3"))
        
        result = saga.execute()
        self.assertFalse(result["success"])
        self.assertTrue(result["compensated"])
        self.assertIn("undo1", compensated)


class TestTracer(unittest.TestCase):
    def test_trace_creation(self):
        tracer = Tracer()
        trace_id = tracer.start_trace("test_trace")
        self.assertIn(trace_id, tracer.traces)
    
    def test_span_nesting(self):
        tracer = Tracer()
        trace_id = tracer.start_trace("test")
        
        with tracer.span("parent") as parent:
            with tracer.span("child") as child:
                pass
        
        trace = tracer.get_trace(trace_id)
        self.assertEqual(len(trace), 2)


if __name__ == "__main__":
    unittest.main()
```

</details>

---

## 8. Harness Integration

> **📌 Core Concept**
>
> - **Concept:** Harness integration is the layer that connects the Workflow module to the entire Harness framework — Memory, Guardrails, Tool Execution, Feedback — through unified interfaces so the modules communicate through a common "language".
> - **Analogy:** Like a universal power outlet: any device (module) plugged in fits and works, as long as it follows the interface standard.
> - **Why it matters:** Without standard interfaces, every module invents its own calling convention — integration becomes a tangled mess of wires that's hard to maintain.

### 8.1 TypeScript Interfaces

This is the "contract" between the Workflow module and the rest of the Harness framework — declaring the standard methods such as createWorkflow, execute, pause, resume, cancel, getTrace, getMetrics, so everyone knows what the engine provides and how to use it:

<details>
<summary><b>8.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

```typescript
// Workflow Engine — Full Harness Integration
interface WorkflowEngine {
  // Workflow management
  createWorkflow: (config: WorkflowConfig) => Workflow;
  getWorkflow: (id: string) => Workflow | null;
  
  // Execution
  execute: (workflowId: string, input: any) => Promise<WorkflowResult>;
  pause: (workflowId: string) => void;
  resume: (workflowId: string) => void;
  cancel: (workflowId: string) => void;
  
  // State management
  getState: (workflowId: string) => WorkflowState;
  getHistory: (workflowId: string) => WorkflowStep[];
  
  // Observability
  getTrace: (workflowId: string) => TraceData;
  getMetrics: (workflowId: string) => WorkflowMetrics;
  
  // Error recovery
  retry: (workflowId: string) => void;
  rollback: (workflowId: string) => void;
}

interface WorkflowConfig {
  name: string;
  steps: WorkflowStepDef[];
  triggers: TriggerDef[];
  errorPolicy: ErrorPolicy;
  timeout: number;
  maxRetries: number;
}

interface WorkflowStepDef {
  name: string;
  type: 'transform' | 'action' | 'condition' | 'parallel' | 'sub_workflow';
  handler: string;
  dependsOn: string[];
  timeout: number;
  retryPolicy: RetryPolicy;
}

interface WorkflowResult {
  success: boolean;
  output: any;
  duration: number;
  stepsExecuted: number;
  errors: WorkflowError[];
  traceId: string;
}

interface WorkflowMetrics {
  totalRuns: number;
  successRate: number;
  avgDuration: number;
  p95Duration: number;
  errorRate: number;
  stepMetrics: Record<string, StepMetrics>;
}

interface StepMetrics {
  runs: number;
  success: number;
  failed: number;
  avgDurationMs: number;
  lastRun: string;
}

// Complete Harness Workflow Engine
class HarnessWorkflowEngine implements WorkflowEngine {
  private workflows: Map<string, Workflow>;
  private tracer: Tracer;
  private metrics: MetricsCollector;
  private logger: WorkflowLogger;
  
  constructor(config: HarnessConfig) {
    this.workflows = new Map();
    this.tracer = new Tracer();
    this.metrics = new MetricsCollector();
    this.logger = new WorkflowLogger('harness');
  }
  
  async execute(workflowId: string, input: any): Promise<WorkflowResult> {
    const traceId = this.tracer.startTrace(`workflow_${workflowId}`);
    
    using span = this.tracer.span('execute', { workflowId });
    
    try {
      const workflow = this.workflows.get(workflowId);
      if (!workflow) throw new Error(`Workflow ${workflowId} not found`);
      
      const startTime = Date.now();
      const output = await workflow.run(input);
      const duration = Date.now() - startTime;
      
      this.metrics.counter('workflow.success');
      this.metrics.histogram('workflow.duration', duration);
      
      return {
        success: true,
        output,
        duration,
        stepsExecuted: workflow.getStepsExecuted(),
        errors: [],
        traceId,
      };
    } catch (error) {
      this.metrics.counter('workflow.error');
      return {
        success: false,
        output: null,
        duration: 0,
        stepsExecuted: 0,
        errors: [{ message: error.message }],
        traceId,
      };
    }
  }
  
  getMetrics(workflowId: string): WorkflowMetrics {
    return this.metrics.getSummary() as WorkflowMetrics;
  }
  
  // ... other interface implementations
}
```

</details>

---

## 9. Case Studies

> **📌 Core Concept**
>
> - **Concept:** Case studies are practical analyses of how large systems (GitHub Actions, Apache Airflow, Temporal, DeepSeek Harness) design their workflows, so you can distill lessons to apply to your own project.
> - **Analogy:** Like watching a documentary and learning from its lessons: instead of charging headlong into the same pitfall, you learn right away from how those who came before solved the problem.
> - **Why it matters:** Pure theory is hard to picture; learning from real systems shows you which patterns actually work in production conditions.

### 9.1. GitHub Actions — Event-Driven CI/CD

A familiar example for most developers: a YAML file that describes CI/CD that runs on push or pull request. You'll immediately see the event-driven trigger (on:) combined with job dependencies — deploy waits for build, build waits for lint and test:

<details>
<summary><b>9.1. GitHub Actions — Event-Driven CI/CD (Click to expand/collapse)</b></summary>

```yaml
# Workflow pattern: Event-driven with parallel jobs
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  lint:          # Parallel job 1
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run lint
  
  test:          # Parallel job 2
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
  
  build:         # Depends on lint + test
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
  
  deploy:        # Depends on build + manual approval
    needs: [build]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: npm run deploy
```

</details>

**Lesson**: GitHub Actions uses DAG-based workflow execution with event triggers and dependency resolution.

### 9.2. Apache Airflow — Data Pipeline Orchestration

Airflow is famous for declaring pipelines as Python DAGs in just a few lines: declare the tasks (extract, transform, load, validate) and use the >> operator to chain the order. This approach makes the whole process visible like a map and easy to reorder:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Airflow pattern: DAG with task dependencies
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('data_pipeline', schedule_interval='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    load = PythonOperator(task_id='load', python_callable=load_data)
    validate = PythonOperator(task_id='validate', python_callable=validate_data)
    
    extract >> transform >> load >> validate
```

</details>

**Lesson**: Airflow proved that DAG-based workflows with clear task dependencies are the gold standard for data pipelines.

### 9.3. Temporal — Durable Workflow Execution

The key point of Temporal: a workflow must "survive" even when the server crashes — state is stored durably (durable) with automatic retry, plus compensation. The example below is an order flow in Saga style: reserve stock → charge payment → ship order; if the shipping step fails, it cancels in reverse:

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

**Lesson**: Temporal's key insight — workflows should survive process crashes via durable state and automatic retry with compensation.

---

### 9.4. DeepSeek Harness — Cordis Micro-Kernel Plugin Architecture

**Context**: DeepSeek Harness uses **Cordis** — a micro-kernel plugin engine designed around the philosophy **"Agent = Model + Harness"** and **"Everything is a plugin"**. Cordis provides a lightweight kernel (~2KB gzipped) that manages the entire agent lifecycle through a plugin system, with dependency injection via a Context service registry.

Put simply: the kernel is like a tiny operating system, and the plugins are like apps installed on it — an app only needs to declare "what service I need" (consumes) and "what service I provide" (provides), and the operating system handles the wiring so they run in the right order.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * Cordis Micro-Kernel Plugin Engine
 * 
 * Core philosophy: 
 * - "Agent = Model + Harness" — Model provides reasoning, Harness provides tools/workflow
 * - "Everything is a plugin" — all functionality is a plugin
 * - Lightweight kernel: ~2KB gzipped core
 * 
 * Repo: https://github.com/cordisjs/cordis
 * Used by: DeepSeek Harness, Koishi bot framework
 */

// ═══════════════════════════════════════════════
// 1. CORE KERNEL ARCHITECTURE
// ═══════════════════════════════════════════════

interface CordisKernel {
  /** Plugin registry */
  plugins: Map<string, Plugin>;
  
  /** Service registry (dependency injection) */
  services: Map<string, any>;
  
  /** Event bus for inter-plugin communication */
  events: EventEmitter;
  
  /** Lifecycle hooks */
  hooks: {
    init: Hook[];
    attach: Hook[];
    ready: Hook[];
    detach: Hook[];
  };
  
  /** Start kernel and all plugins */
  start(): Promise<void>;
  
  /** Stop kernel gracefully */
  stop(): Promise<void>;
  
  /** Register a plugin */
  plugin(plugin: Plugin | PluginFactory): this;
  
  /** Get service by name */
  getService<T>(name: string): T | undefined;
  
  /** Provide service to registry */
  provide<T>(name: string, service: T): this;
  
  /** Inject service (for plugin constructors) */
  inject<T>(name: string): T | undefined;
}

interface Plugin {
  name: string;
  description?: string;
  version?: string;
  
  /** Dependencies on other plugins */
  requires?: string[];
  
  /** Optional: only load if these plugins are present */
  optional?: string[];
  
  /** Service this plugin provides */
  provides?: string | string[];
  
  /** Service this plugin consumes */
  consumes?: string | string[];
  
  /** Configuration schema */
  config?: Schema;
  
  /** Default config */
  defaultConfig?: any;
  
  /** Lifecycle hooks */
  init?: (ctx: Context) => void | Promise<void>;
  attach?: (ctx: Context) => void | Promise<void>;
  ready?: (ctx: Context) => void | Promise<void>;
  detach?: (ctx: Context) => void | Promise<void>;
}

type PluginFactory = (ctx: Context, config: any) => Plugin | Promise<Plugin>;

// ═══════════════════════════════════════════════
// 2. CONTEXT & DEPENDENCY INJECTION
// ═══════════════════════════════════════════════

class Context {
  private kernel: CordisKernel;
  private plugin: Plugin;
  private services: Map<string, any> = new Map();
  private disposables: (() => void)[] = [];
  
  constructor(kernel: CordisKernel, plugin: Plugin) {
    this.kernel = kernel;
    this.plugin = plugin;
  }
  
  /** Get service from kernel registry */
  get<T>(name: string): T | undefined {
    return this.kernel.getService(name);
  }
  
  /** Provide service to kernel registry */
  provide<T>(name: string, service: T): this {
    this.kernel.provide(name, service);
    this.disposables.push(() => this.kernel.provide(name, undefined));
    return this;
  }
  
  /** Inject service (shorthand for get) */
  inject<T>(name: string): T | undefined {
    return this.get(name);
  }
  
  /** Register disposable for cleanup */
  onDispose(fn: () => void): void {
    this.disposables.push(fn);
  }
  
  /** Dispose all services provided by this plugin */
  dispose(): void {
    for (const fn of this.disposables) {
      fn();
    }
    this.disposables = [];
  }
  
  /** Access plugin config */
  get config(): any {
    return this.kernel.config[this.plugin.name];
  }
  
  /** Access global config */
  get globalConfig(): any {
    return this.kernel.config;
  }
  
  /** Event bus access */
  get event(): EventEmitter {
    return this.kernel.events;
  }
  
  /** Emit event */
  emit(event: string, ...args: any[]): void {
    this.kernel.events.emit(event, ...args);
  }
  
  /** Listen to event */
  on(event: string, listener: (...args: any[]) => void): () => void {
    this.kernel.events.on(event, listener);
    return () => this.kernel.events.off(event, listener);
  }
  
  /** One-time event listener */
  once(event: string, listener: (...args: any[]) => void): void {
    this.kernel.events.once(event, listener);
  }
}

// ═══════════════════════════════════════════════
// 3. LIFECYCLE MANAGEMENT
// ═══════════════════════════════════════════════

/**
 * Plugin Lifecycle:
 * 
 * 1. INIT     — Plugin registered, config validated
 *    ↓
 * 2. ATTACH   — Plugin attaches to kernel, provides/consumes services
 *    ↓
 * 3. READY    — All plugins attached, kernel ready for work
 *    ↓
 * 4. RUNNING  — Kernel processing events, handling requests
 *    ↓
 * 5. DETACH   — Graceful shutdown, cleanup services
 */

class CordisKernelImpl implements CordisKernel {
  plugins = new Map<string, Plugin>();
  services = new Map<string, any>();
  events = new EventEmitter();
  hooks = {
    init: [],
    attach: [],
    ready: [],
    detach: [],
  };
  
  private config: Record<string, any> = {};
  private started = false;
  private pluginOrder: string[] = [];
  
  plugin(plugin: Plugin | PluginFactory): this {
    const instance = typeof plugin === 'function' 
      ? plugin(this.createContext({} as Plugin), plugin.defaultConfig || {})
      : plugin;
    
    // Validate config
    if (instance.config) {
      // Schema validation here
    }
    
    this.plugins.set(instance.name, instance);
    this.config[instance.name] = { ...instance.defaultConfig, ...this.config[instance.name] };
    
    return this;
  }
  
  async start(): Promise<void> {
    if (this.started) return;
    this.started = true;
    
    // Resolve dependency order
    this.pluginOrder = this.resolvePluginOrder();
    
    // Phase 1: INIT
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.init) {
        await plugin.init(ctx);
      }
      this.hooks.init.push({ plugin: name, ctx });
    }
    
    // Phase 2: ATTACH
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      // Inject consumed services
      this.injectConsumedServices(plugin, ctx);
      
      if (plugin.attach) {
        await plugin.attach(ctx);
      }
      this.hooks.attach.push({ plugin: name, ctx });
    }
    
    // Phase 3: READY
    for (const name of this.pluginOrder) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.ready) {
        await plugin.ready(ctx);
      }
      this.hooks.ready.push({ plugin: name, ctx });
    }
    
    this.emit('ready');
  }
  
  async stop(): Promise<void> {
    if (!this.started) return;
    
    // Phase 4: DETACH (reverse order)
    for (const name of [...this.pluginOrder].reverse()) {
      const plugin = this.plugins.get(name)!;
      const ctx = this.createContext(plugin);
      
      if (plugin.detach) {
        await plugin.detach(ctx);
      }
      
      // Dispose context (cleanup provided services)
      ctx.dispose();
      
      this.hooks.detach.push({ plugin: name, ctx });
    }
    
    this.started = false;
    this.emit('stop');
  }
  
  private createContext(plugin: Plugin): Context {
    return new Context(this, plugin);
  }
  
  private injectConsumedServices(plugin: Plugin, ctx: Context): void {
    const consumes = Array.isArray(plugin.consumes) ? plugin.consumes : 
                     plugin.consumes ? [plugin.consumes] : [];
    
    for (const serviceName of consumes) {
      const service = this.services.get(serviceName);
      if (service) {
        // Service available in context
        ctx.provide(serviceName, service);
      }
    }
  }
  
  private resolvePluginOrder(): string[] {
    // Topological sort based on requires/optional
    const visited = new Set<string>();
    const order: string[] = [];
    
    const visit = (name: string) => {
      if (visited.has(name)) return;
      visited.add(name);
      
      const plugin = this.plugins.get(name);
      if (!plugin) return;
      
      const requires = plugin.requires || [];
      for (const dep of requires) {
        visit(dep);
      }
      
      order.push(name);
    };
    
    for (const name of this.plugins.keys()) {
      visit(name);
    }
    
    return order;
  }
  
  provide<T>(name: string, service: T): this {
    if (service === undefined) {
      this.services.delete(name);
    } else {
      this.services.set(name, service);
    }
    return this;
  }
  
  getService<T>(name: string): T | undefined {
    return this.services.get(name);
  }
}

// ═══════════════════════════════════════════════
// 4. DEEPSEEK HARNESS PLUGIN EXAMPLES
// ═══════════════════════════════════════════════

/**
 * Example: Code Execution Plugin
 * Provides: code-executor service
 * Consumes: logger, config
 */
const codeExecutionPlugin: Plugin = {
  name: 'code-executor',
  description: 'Execute code in isolated sandbox',
  version: '1.0.0',
  provides: 'code-executor',
  consumes: ['logger', 'config'],
  config: {
    timeout: { type: 'number', default: 30000 },
    memoryLimit: { type: 'number', default: 128 },
  },
  
  init(ctx) {
    ctx.get('logger')?.info('[code-executor] Initializing...');
  },
  
  attach(ctx) {
    const logger = ctx.get('logger');
    const config = ctx.get('config');
    
    // Provide the code execution service
    ctx.provide('code-executor', {
      async execute(script: string, options?: { timeout?: number }) {
        logger?.info('[code-executor] Executing script...');
        // Implementation using VM sandbox
        return { success: true, result: 'output' };
      },
      
      async executeBatch(calls: Array<{tool: string, args: any}>) {
        // Batched execution for Code Mode
        return Promise.all(calls.map(c => this.execute(c.tool, c.args)));
      },
    });
  },
  
  ready(ctx) {
    ctx.get('logger')?.info('[code-executor] Ready!');
  },
  
  detach(ctx) {
    ctx.get('logger')?.info('[code-executor] Shutting down...');
  },
};

/**
 * Example: Trajectory Recorder Plugin
 * Provides: trajectory service
 * Consumes: memory-store, event-bus
 */
const trajectoryPlugin: Plugin = {
  name: 'trajectory-recorder',
  description: 'Record and replay agent trajectories',
  version: '1.0.0',
  provides: 'trajectory',
  consumes: ['memory-store', 'event-bus'],
  
  init(ctx) {
    // Setup trajectory schema
  },
  
  attach(ctx) {
    const memory = ctx.get('memory-store');
    const events = ctx.get('event-bus');
    
    ctx.provide('trajectory', {
      record(event: TrajectoryEvent) {
        // Append to session event stream
        return memory.append('trajectory', event);
      },
      
      replay(sessionId: string, toStep?: number) {
        // Replay trajectory to specific step
        return memory.query('trajectory', { sessionId, step: toStep });
      },
      
      fork(sessionId: string, fromStep: number) {
        // Fork trajectory from step
        return memory.fork('trajectory', { sessionId, fromStep });
      },
      
      search(query: TrajectoryQuery) {
        // Search trajectory events
        return memory.search('trajectory', query);
      },
    });
    
    // Listen to agent events
    events.on('agent:tool-call', (data) => {
      this.record({ type: 'tool-call', ...data, timestamp: Date.now() });
    });
  },
};

/**
 * Example: Runtime Mode Plugin
 * Manages 4 runtime modes: Standard, Code, Minimal Benchmark, Creator Inspector
 */
const runtimeModePlugin: Plugin = {
  name: 'runtime-modes',
  description: 'Manage 4 runtime modes',
  version: '1.0.0',
  provides: 'runtime-mode',
  consumes: ['code-executor', 'trajectory', 'logger'],
  
  init(ctx) {
    ctx.get('logger')?.info('[runtime-modes] Available modes: standard, code, benchmark, creator');
  },
  
  attach(ctx) {
    const executor = ctx.get('code-executor');
    const trajectory = ctx.get('trajectory');
    const logger = ctx.get('logger');
    
    const modes = {
      standard: {
        name: 'Standard Mode',
        description: 'Full agent with all tools',
        tools: ['read', 'write', 'search', 'execute', 'llm', 'memory', ...],
        isolation: 'process',
      },
      
      code: {
        name: 'Code Mode (@deepseek-ai/dsh)',
        description: 'Single-turn script execution, batched tools',
        tools: ['bash', 'editor', 'llm_complete'],
        isolation: 'vm-sandbox',
        batching: true,
        latencyReduction: '70-90%',
      },
      
      benchmark: {
        name: 'Minimal Benchmark Harness',
        description: 'Clean isolation for SWE-bench evaluation',
        tools: ['bash', 'editor'],
        isolation: 'container',
        deterministic: true,
      },
      
      creator: {
        name: 'Creator Inspector',
        description: 'Visual timeline, presets, debugging',
        tools: ['all'],
        features: ['timeline', 'presets', 'time-travel', 'fork'],
        isolation: 'process',
      },
    };
    
    ctx.provide('runtime-mode', {
      getMode(name: string) {
        return modes[name] || modes.standard;
      },
      
      listModes() {
        return Object.entries(modes).map(([key, m]) => ({ key, ...m }));
      },
      
      async execute(modeName: string, task: any) {
        const mode = modes[modeName] || modes.standard;
        logger?.info(`[runtime-modes] Executing in ${mode.name}`);
        
        switch (modeName) {
          case 'code':
            return await executor.executeBatch(task.script);
          case 'benchmark':
            return await executor.execute(task.script, { isolation: 'container' });
          default:
            return await this.executeStandard(task);
        }
      },
    });
  },
};

/**
 * Example: Minimal Benchmark Plugin
 * Clean isolation for SWE-bench evaluation
 */
const minimalBenchmarkPlugin: Plugin = {
  name: 'minimal-benchmark',
  description: 'Minimal harness for unbiased LLM evaluation',
  version: '1.0.0',
  provides: 'benchmark-harness',
  consumes: ['runtime-mode', 'logger'],
  
  attach(ctx) {
    const logger = ctx.get('logger');
    
    ctx.provide('benchmark-harness', {
      async runEvaluation(suite: string, model: string) {
        logger?.info(`[benchmark] Running ${suite} on ${model}`);
        
        // Only bash + editor tools available
        const result = await ctx.get('runtime-mode').execute('benchmark', {
          script: `
            // Isolated evaluation environment
            const fs = require('fs');
            const { execSync } = require('child_process');
            
            // Run test suite
            const result = execSync('npm test', { encoding: 'utf-8' });
            return { passed: result.includes('passed') };
          `,
        });
        
        return result;
      },
    });
  },
};

// ═══════════════════════════════════════════════
// 5. COMPOSING THE HARNESS
// ═══════════════════════════════════════════════

async function createDeepSeekHarness() {
  const kernel = new CordisKernelImpl();
  
  // Core infrastructure plugins
  kernel.plugin({
    name: 'logger',
    init(ctx) {
      ctx.provide('logger', console);
    },
  });
  
  kernel.plugin({
    name: 'config',
    init(ctx) {
      ctx.provide('config', {
        timeout: 30000,
        memoryLimit: 128,
        logLevel: 'info',
      });
    },
  });
  
  kernel.plugin({
    name: 'memory-store',
    provides: 'memory-store',
    attach(ctx) {
      // Implementation using vector DB or file-based
      ctx.provide('memory-store', {
        append: async (collection, data) => { /* ... */ },
        query: async (collection, query) => { /* ... */ },
        fork: async (collection, opts) => { /* ... */ },
        search: async (collection, query) => { /* ... */ },
      });
    },
  });
  
  kernel.plugin({
    name: 'event-bus',
    provides: 'event-bus',
    init(ctx) {
      ctx.provide('event-bus', new EventEmitter());
    },
  });
  
  // Feature plugins (order matters via requires)
  kernel.plugin(codeExecutionPlugin);    // provides: code-executor
  kernel.plugin(trajectoryPlugin);       // provides: trajectory, consumes: memory-store, event-bus
  kernel.plugin(runtimeModePlugin);      // provides: runtime-mode, consumes: code-executor, trajectory
  kernel.plugin(minimalBenchmarkPlugin); // provides: benchmark-harness, consumes: runtime-mode
  
  // Start the kernel
  await kernel.start();
  
  return kernel;
}

// Usage
const harness = await createDeepSeekHarness();

// Execute in Code Mode
const codeExecutor = harness.getService('code-executor');
const result = await codeExecutor.execute(`
  const files = await list_files({path: './src'});
  const content = await read_file({path: files[0]});
  const fixed = await llm_complete({prompt: \`Fix: \${content}\`});
  await write_file({path: files[0], content: fixed});
`);

// Or use Runtime Mode
const runtime = harness.getService('runtime-mode');
const benchmarkResult = await runtime.execute('benchmark', {
  script: 'npm test',
});

// Access trajectory
const trajectory = harness.getService('trajectory');
const events = await trajectory.search({ sessionId: 'abc123' });
await trajectory.replay('abc123', 5);  // Replay to step 5
await trajectory.fork('abc123', 3);    // Fork from step 3

interface TrajectoryEvent {
  type: 'prompt' | 'thought' | 'tool-call' | 'tool-result' | 'error';
  sessionId: string;
  step: number;
  timestamp: number;
  data: any;
}

interface TrajectoryQuery {
  sessionId?: string;
  type?: TrajectoryEvent['type'];
  stepRange?: [number, number];
  timeRange?: [number, number];
}
```

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

The six principles below are the "compass" when designing any workflow — from safe re-runs (idempotency) to storing state outside memory (state externalization) so you can resume from a checkpoint:

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

*Document: VII. Workflow — HARNESS ENGINEERING EDITION*
*Last updated: 07/19/2026*
*Author: AI Knowledge Repository*
