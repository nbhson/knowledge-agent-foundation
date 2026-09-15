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

Imagine you are the **administrator of a general hospital**. Every day, hundreds of patients arrive: someone with acute abdominal pain, someone needing a routine checkup, someone wanting a vaccination. If you **don't triage** — sending an emergency patient behind a routine exam — the result will be a **disaster**.

**AI Agents face the same problem without Task Management.**

When a user sends a complex request like *"Refactor the auth module, add tests, update docs, then deploy"* — the agent receives **everything at once** but doesn't know where to start, what to prioritize, or what can run in parallel. The result: messy work, missed steps, or worse — **deploying untested code**.

**Solution**: Structured Task Management — a system for classifying, prioritizing, decomposing, and tracking tasks so the agent **does the right thing, at the right time, in the right order**.

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

**Task Management** in AI coding is the process of **analyzing, decomposing, prioritizing, and tracking** coding tasks. Good tasks help AI agents focus on the right work, avoid overload, and deliver quality results.

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

The diagram below summarizes the coding task taxonomy in 5 main groups — each group is a different "specialty" (new code, code modification, code analysis, documentation, testing). Read it as a classification tree: from the top-level group, follow a branch down to a specific task type, to find where your task belongs.

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

The code below is the actual classification engine: it takes a natural-language task description, searches keyword patterns (e.g., seeing "fix" or "bug" places it in the MODIFICATION group), then estimates complexity and returns a fully populated Task object. Try it with any description to see how the agent "understands" the request.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import re

class TaskCategory(Enum):
    GENERATION = "generation"
    MODIFICATION = "modification"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    UNKNOWN = "unknown"

class TaskComplexity(Enum):
    TRIVIAL = 1     # 1 file, < 50 LOC
    SIMPLE = 2      # 1-2 files, < 200 LOC
    MODERATE = 3    # 3-5 files, 200-500 LOC
    COMPLEX = 4     # 5-15 files, 500-2000 LOC
    EPIC = 5        # 15+ files, 2000+ LOC


@dataclass
class Task:
    """Represents a coding task"""
    id: str
    title: str
    description: str
    category: TaskCategory = TaskCategory.UNKNOWN
    complexity: TaskComplexity = TaskComplexity.SIMPLE
    priority: int = 5                    # 1=highest, 10=lowest
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    files_involved: List[str] = field(default_factory=list)


class TaskClassifier:
    """
    Automatically classify tasks based on keywords and patterns.
    
    Usage:
        classifier = TaskClassifier()
        task = classifier.classify(
            "Fix the authentication bug in login handler"
        )
        print(task.category)  # TaskCategory.MODIFICATION
        print(task.complexity)  # TaskComplexity.SIMPLE
    """
    
    PATTERNS = {
        TaskCategory.GENERATION: [
            r"tạo|create|generate|build|new|thêm|add",
            r"function|class|component|endpoint|api",
            r"from scratch|từ đầu|mới",
        ],
        TaskCategory.MODIFICATION: [
            r"sửa|fix|bug|error|broken",
            r"refactor|cải thiện|improve|optimize",
            r"thay đổi|change|update|migrate",
        ],
        TaskCategory.ANALYSIS: [
            r"kiểm tra|check|review|analyze|inspect",
            r"tìm|find|debug|trace|profile",
            r"security|audit|vulnerability",
        ],
        TaskCategory.DOCUMENTATION: [
            r"viết docs|write.*doc|readme|changelog",
            r"document|tài liệu|hướng dẫn|guide",
            r"comment|annotate",
        ],
        TaskCategory.TESTING: [
            r"test|viết test|write.*test|spec",
            r"mock|fixture|assert|coverage",
            r"integration|e2e|unit test",
        ],
    }
    
    COMPLEXITY_SIGNALS = {
        TaskComplexity.TRIVIAL: [
            r"1 dòng|one line|typo|formatting",
            r"rename|đổi tên|thay màu",
        ],
        TaskComplexity.SIMPLE: [
            r"fix.*bug|sửa lỗi đơn",
            r"thêm field|add field|add property",
            r"1 file|single file",
        ],
        TaskComplexity.MODERATE: [
            r"feature|tính năng|feature mới",
            r"refactor|cải trúc|restructure",
            r"multi.?file|nhiều file",
        ],
        TaskComplexity.COMPLEX: [
            r"module|system|hệ thống|architecture",
            r"migration|di chuyển|migrate",
            r"performance.*optimization|tối ưu lớn",
        ],
        TaskComplexity.EPIC: [
            r"redesign|thiết kế lại|rebuild",
            r"major.*overhaul|nâng cấp lớn",
            r"multiple.*module|nhiều module",
        ],
    }
    
    def classify(self, text: str) -> Task:
        text_lower = text.lower()
        
        # Classify category
        category_scores = {}
        for cat, patterns in self.PATTERNS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            category_scores[cat] = score
        
        category = max(category_scores, 
                      key=category_scores.get,
                      default=TaskCategory.UNKNOWN)
        if category_scores.get(category, 0) == 0:
            category = TaskCategory.UNKNOWN
        
        # Classify complexity
        complexity_scores = {}
        for comp, patterns in self.COMPLEXITY_SIGNALS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            complexity_scores[comp] = score
        
        complexity = max(complexity_scores,
                        key=complexity_scores.get,
                        default=TaskComplexity.SIMPLE)
        if complexity_scores.get(complexity, 0) == 0:
            complexity = TaskComplexity.SIMPLE
        
        return Task(
            id=f"task-{hash(text) % 10000:04d}",
            title=text[:100],
            description=text,
            category=category,
            complexity=complexity,
        )
```

</details>

### 1.3 Decision Tree: Choosing Task Handling Strategy

The diagram below describes the decision rules when a task arrives: if the request is unclear, clarify first; if it's under 500 tokens, just do it; if it's large, decompose it into sub-tasks and then choose a sequential, parallel, or TDD execution strategy. Follow the arrows from top to bottom to see which "door" the agent takes for each type of task.

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

The diagram below lists the 6 common task decomposition patterns. The difference lies in how sub-tasks relate to each other: running sequentially in a required order, running in parallel then merging results (parallel, map-reduce), or a parent-child hierarchy. Look at the arrows in the diagram to pick the pattern that fits the work you're doing.

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

This is the code that implements decomposition: the TaskDecomposer object takes a Task, automatically picks a decomposition strategy (feature, layer, file, TDD, vertical slice, spike), and returns an ordered list of SubTasks with dependencies, token estimates, and check criteria. If it doesn't know which to pick, it suggests one based on the task's type and complexity.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class SubTask:
    """Child sub-task in task decomposition"""
    id: str
    title: str
    description: str
    order: int
    parallel: bool = False
    estimated_tokens: int = 0
    dependencies: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    verification_criteria: str = ""


class TaskDecomposer:
    """
    Decompose a large task into sub-tasks that can be executed independently.
    
    Strategies:
    - feature-based: split by feature
    - layer-based: split by layer (UI, API, DB)
    - file-based: split by file
    - test-driven: write tests first, then code
    - vertical-slice: each slice = full-stack working increment
    - spike-then-execute: research first, then implement
    """
    
    def decompose(self, task: Task, strategy: str = "auto",
                  project_context: Dict = None) -> List[SubTask]:
        """Decompose a task into sub-tasks"""
        
        if strategy == "auto":
            strategy = self._suggest_strategy(task, project_context)
        
        if strategy == "feature":
            return self._decompose_by_feature(task)
        elif strategy == "layer":
            return self._decompose_by_layer(task)
        elif strategy == "file":
            return self._decompose_by_file(task)
        elif strategy == "tdd":
            return self._decompose_tdd(task)
        elif strategy == "vertical_slice":
            return self._decompose_vertical_slice(task)
        elif strategy == "spike":
            return self._decompose_spike(task)
        else:
            return self._decompose_by_feature(task)
    
    def _suggest_strategy(self, task: Task, 
                          context: Dict = None) -> str:
        """Suggest a suitable strategy based on task characteristics"""
        context = context or {}
        
        # Trivial tasks - don't decompose
        if task.complexity.value <= 1:
            return "simple"
        
        # Test-related tasks
        if "test" in task.description.lower():
            return "tdd"
        
        # Generation tasks - feature-based
        if task.category == TaskCategory.GENERATION:
            if len(task.files_involved) > 3:
                return "vertical_slice"
            return "feature"
        
        # Modification tasks - file-based or layer-based
        if task.category == TaskCategory.MODIFICATION:
            if len(task.files_involved) > 5:
                return "layer"
            return "file"
        
        # Complex/uncertain tasks - spike first
        if task.complexity.value >= 4:
            if context.get("uncertain_approach", False):
                return "spike"
            return "layer"
        
        return "feature"
    
    def _decompose_by_feature(self, task: Task) -> List[SubTask]:
        """Split by feature — full workflow"""
        subtasks = []
        
        subtasks.append(SubTask(
            id=f"{task.id}-01",
            title="Analyze requirements",
            description=f"Read and understand the requirements: {task.description}",
            order=1,
            estimated_tokens=500,
            verification_criteria="Clear list of requirements",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-02",
            title="Read current code",
            description="Review related codebase to understand context",
            order=2,
            dependencies=[f"{task.id}-01"],
            estimated_tokens=1500,
            verification_criteria="Identified affected files and patterns",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-03",
            title="Plan changes",
            description="Identify files to change and the approach",
            order=3,
            dependencies=[f"{task.id}-02"],
            estimated_tokens=800,
            verification_criteria="Concrete plan with file list and approach",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-04",
            title="Implement code",
            description="Write code according to the plan",
            order=4,
            dependencies=[f"{task.id}-03"],
            estimated_tokens=task.estimated_tokens or 3000,
            verification_criteria="Code written, no syntax errors",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-05",
            title="Check & validate",
            description="Run tests, lint, review results",
            order=5,
            dependencies=[f"{task.id}-04"],
            estimated_tokens=1000,
            verification_criteria="Tests pass, lint clean, no regressions",
        ))
        
        return subtasks
    
    def _decompose_by_layer(self, task: Task) -> List[SubTask]:
        """Split by layer: DB → Service → API → UI"""
        return [
            SubTask(f"{task.id}-db", "Database layer",
                    "Change schema, queries, migrations", 1,
                    estimated_tokens=1500,
                    verification_criteria="Schema updated, migrations run"),
            SubTask(f"{task.id}-svc", "Service layer",
                    "Business logic, validation", 2,
                    dependencies=[f"{task.id}-db"],
                    estimated_tokens=2000,
                    verification_criteria="Service logic complete, unit tests pass"),
            SubTask(f"{task.id}-api", "API layer",
                    "Endpoints, request/response, error handling", 3,
                    dependencies=[f"{task.id}-svc"],
                    estimated_tokens=1500,
                    verification_criteria="API endpoints working, OpenAPI spec updated"),
            SubTask(f"{task.id}-ui", "UI layer",
                    "Frontend components, forms, display", 4,
                    dependencies=[f"{task.id}-api"],
                    estimated_tokens=2000,
                    verification_criteria="UI renders correctly, forms submit"),
            SubTask(f"{task.id}-test", "Integration tests",
                    "End-to-end flow tests", 5,
                    dependencies=[f"{task.id}-ui"],
                    estimated_tokens=1500,
                    verification_criteria="All integration tests pass"),
        ]
    
    def _decompose_by_file(self, task: Task) -> List[SubTask]:
        """Split by file — each file is 1 sub-task"""
        subtasks = []
        for i, filepath in enumerate(task.files_involved, 1):
            subtasks.append(SubTask(
                id=f"{task.id}-f{i:02d}",
                title=f"Modify {filepath}",
                description=f"Modify file {filepath}",
                order=i,
                files_to_modify=[filepath],
                parallel=True,
                estimated_tokens=1000,
                verification_criteria=f"File {filepath} updated correctly",
            ))
        return subtasks
    
    def _decompose_tdd(self, task: Task) -> List[SubTask]:
        """Test-Driven Development decomposition"""
        return [
            SubTask(f"{task.id}-test-design", "Design test cases",
                    "Write test cases based on requirements", 1,
                    estimated_tokens=1000,
                    verification_criteria="Test cases cover all scenarios"),
            SubTask(f"{task.id}-test-write", "Write tests",
                    "Write test code (will fail at first)", 2,
                    dependencies=[f"{task.id}-test-design"],
                    estimated_tokens=1500,
                    verification_criteria="Tests compile, run, and fail (RED)"),
            SubTask(f"{task.id}-impl", "Implement code",
                    "Write code to pass the tests", 3,
                    dependencies=[f"{task.id}-test-write"],
                    estimated_tokens=task.estimated_tokens or 2000,
                    verification_criteria="All tests pass (GREEN)"),
            SubTask(f"{task.id}-refactor", "Refactor",
                    "Improve code quality", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1000,
                    verification_criteria="Code clean, tests still pass"),
        ]
    
    def _decompose_vertical_slice(self, task: Task) -> List[SubTask]:
        """Vertical slice — each slice = full-stack working feature"""
        return [
            SubTask(f"{task.id}-slice-core", "Core slice",
                    "Implement core logic + minimal API", 1,
                    estimated_tokens=3000,
                    verification_criteria="Core flow works end-to-end"),
            SubTask(f"{task.id}-slice-data", "Data slice",
                    "Database + repository layer", 2,
                    dependencies=[f"{task.id}-slice-core"],
                    estimated_tokens=2000,
                    verification_criteria="Data persistence working"),
            SubTask(f"{task.id}-slice-api", "API slice",
                    "Full API with validation + error handling", 3,
                    dependencies=[f"{task.id}-slice-data"],
                    estimated_tokens=2000,
                    verification_criteria="All API endpoints functional"),
            SubTask(f"{task.id}-slice-ui", "UI slice",
                    "Frontend integration", 4,
                    dependencies=[f"{task.id}-slice-api"],
                    estimated_tokens=2500,
                    verification_criteria="UI fully functional"),
            SubTask(f"{task.id}-slice-test", "Test slice",
                    "Integration + E2E tests", 5,
                    dependencies=[f"{task.id}-slice-ui"],
                    estimated_tokens=2000,
                    verification_criteria="Full test coverage"),
        ]
    
    def _decompose_spike(self, task: Task) -> List[SubTask]:
        """Spike-then-execute — research before implementing"""
        return [
            SubTask(f"{task.id}-spike", "Spike: Research & Decide",
                    "Timebox 1-2h research, compare approaches", 1,
                    estimated_tokens=3000,
                    verification_criteria="Chosen approach documented with rationale"),
            SubTask(f"{task.id}-poc", "Proof of Concept",
                    "Minimal implementation to validate approach", 2,
                    dependencies=[f"{task.id}-spike"],
                    estimated_tokens=2000,
                    verification_criteria="POC works, approach validated"),
            SubTask(f"{task.id}-impl", "Full Implementation",
                    "Implement complete solution", 3,
                    dependencies=[f"{task.id}-poc"],
                    estimated_tokens=task.estimated_tokens or 4000,
                    verification_criteria="Feature complete"),
            SubTask(f"{task.id}-validate", "Validation",
                    "Test, review, verify", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1500,
                    verification_criteria="All tests pass, code reviewed"),
        ]
```

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

The code below shows how to compute a priority score for each task with an Eisenhower-Matrix-style formula: each task gets scored on urgency, importance, and effort, with a bonus added if it's a small, easy job (quick win) or many other tasks depend on it. The TaskScheduler then lines up tasks into batches that follow the right order without exceeding the per-session token budget.

In plain terms, it's a queue-ranking scale: urgent and important work scores high; big but non-urgent work is placed later; small, easy jobs are prioritized to quickly "clear the desk".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class PriorityScore:
    """Computed priority score — Eisenhower Matrix + dependency bonus"""
    urgency: int        # 1-5: urgency level
    importance: int     # 1-5: importance level
    effort: int         # 1-5: required effort (lower = higher score)
    dependency_count: int  # Number of tasks that depend on this task
    
    @property
    def total(self) -> float:
        """Weighted score with quick-wins bonus"""
        base = self.urgency * 0.4 + self.importance * 0.4
        effort_bonus = (6 - self.effort) * 0.1   # Quick wins bonus
        dep_bonus = min(self.dependency_count * 0.1, 0.3)
        return base + effort_bonus + dep_bonus


class TaskScheduler:
    """
    Schedule tasks based on priority, dependencies, and token budget.
    
    Rules:
    1. Always do tasks with many dependents first
    2. Quick wins (low effort, high priority) should be done first
    3. Respect token budget per session
    """
    
    def __init__(self, max_tokens_per_session: int = 50000):
        self.max_tokens = max_tokens_per_session
    
    def schedule(self, tasks: List[Task]) -> List[List[Task]]:
        """
        Create an execution schedule — returns a list of batches.
        Each batch is a group of tasks that can run at the same time.
        """
        # Sort by priority score descending
        scored = [(t, self._score(t)) for t in tasks]
        scored.sort(key=lambda x: x[1].total, reverse=True)
        
        batches = []
        current_batch = []
        current_tokens = 0
        
        for task, score in scored:
            task_tokens = task.estimated_tokens or 1000
            
            if current_tokens + task_tokens > self.max_tokens:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [task]
                current_tokens = task_tokens
            else:
                current_batch.append(task)
                current_tokens += task_tokens
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _score(self, task: Task) -> PriorityScore:
        """Compute the priority score for a task"""
        effort = task.complexity.value
        urgency = max(1, 6 - task.priority)
        
        importance_map = {
            TaskCategory.MODIFICATION: 5,   # Bug fix = high
            TaskCategory.TESTING: 4,
            TaskCategory.GENERATION: 3,
            TaskCategory.ANALYSIS: 3,
            TaskCategory.DOCUMENTATION: 2,
        }
        importance = importance_map.get(task.category, 3)
        
        return PriorityScore(
            urgency=urgency,
            importance=importance,
            effort=effort,
            dependency_count=len(task.dependencies),
        )
```

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

The diagram below is the state map of a task from birth to end: PENDING → PLANNING → IN_PROGRESS → TESTING → REVIEW → DONE. Beyond the main path there are special branches — BLOCKED (when blocked, go back to waiting), FAILED (on failure, start over), CANCELLED (canceled). Follow the arrows to see which transitions from which state to which are valid.

Put simply, this is "the journey of a task through the wards": just created it waits for an exam (PENDING), planned (PLANNING), in treatment (IN_PROGRESS), in lab testing (TESTING), in consultation (REVIEW), then discharged (DONE).

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

This is the state management code: TaskStateManager keeps a "tracking log" for every task, only allows state changes when they are valid, records start times, attempt counts, and the last error, and emits events so other parts of the system can react. If you try an illegal state change (e.g., TESTING → PENDING), the code throws an error immediately — like a hospital rule that forbids cutting corners.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    TESTING = "testing"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskState:
    """Current state of a task"""
    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: float = 0.0        # 0.0 → 1.0
    attempts: int = 0
    last_error: Optional[str] = None
    notes: List[str] = field(default_factory=list)


class TaskStateManager:
    """
    Manage the task lifecycle — tracks status changes,
    enforces valid transitions, and emits events.
    """
    
    VALID_TRANSITIONS = {
        TaskStatus.PENDING: [
            TaskStatus.PLANNING, TaskStatus.CANCELLED
        ],
        TaskStatus.PLANNING: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED
        ],
        TaskStatus.IN_PROGRESS: [
            TaskStatus.TESTING, TaskStatus.BLOCKED,
            TaskStatus.FAILED, TaskStatus.DONE,
        ],
        TaskStatus.BLOCKED: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED,
            TaskStatus.PENDING,
        ],
        TaskStatus.TESTING: [
            TaskStatus.REVIEW, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.REVIEW: [
            TaskStatus.DONE, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.FAILED: [
            TaskStatus.PENDING, TaskStatus.CANCELLED,
        ],
    }
    
    def __init__(self):
        self.states: Dict[str, TaskState] = {}
        self.listeners: List[Callable] = []
    
    def create(self, task_id: str) -> TaskState:
        state = TaskState(task_id=task_id)
        self.states[task_id] = state
        return state
    
    def transition(self, task_id: str, new_status: TaskStatus,
                   note: str = "") -> TaskState:
        """Change the task's state — checks validity"""
        state = self.states.get(task_id)
        if not state:
            raise ValueError(f"Task {task_id} not found")
        
        valid = self.VALID_TRANSITIONS.get(state.status, [])
        if new_status not in valid:
            raise InvalidTransitionError(
                f"Cannot transition from {state.status.value} "
                f"to {new_status.value}"
            )
        
        old_status = state.status
        state.status = new_status
        
        if new_status == TaskStatus.IN_PROGRESS and not state.started_at:
            state.started_at = datetime.now().isoformat()
            state.attempts += 1
        
        if new_status in (TaskStatus.DONE, TaskStatus.FAILED, 
                         TaskStatus.CANCELLED):
            state.completed_at = datetime.now().isoformat()
        
        if note:
            state.notes.append(
                f"[{datetime.now().isoformat()}] {note}"
            )
        
        # Notify listeners
        for listener in self.listeners:
            listener(task_id, old_status, new_status)
        
        return state
    
    def on_transition(self, callback: Callable):
        self.listeners.append(callback)


class InvalidTransitionError(Exception):
    pass
```

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

The code below implements a DAG (Directed Acyclic Graph) to manage dependencies. The reading convention is simple: "A → B" means task A must finish before task B can start. This class supports cycle detection, execution-order sorting (topological sort), and splitting tasks into groups that can run in parallel.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from collections import defaultdict, deque
from typing import List, Dict, Set, Optional

class TaskDependencyGraph:
    """
    Directed Acyclic Graph (DAG) for task dependencies.
    
    Features:
    - Add/remove dependencies
    - Topological sort (execution order)
    - Parallel groups (tasks that run at the same time)
    - Cycle detection
    """
    
    def __init__(self):
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
        for dep_id in task.dependencies:
            self.adj[dep_id].add(task.id)
    
    def has_cycle(self) -> bool:
        """DFS-based cycle detection"""
        visited = set()
        in_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in in_stack:
                    return True
            in_stack.discard(node)
            return False
        
        return any(dfs(t) for t in self.tasks if t not in visited)
    
    def topological_sort(self) -> List[str]:
        """Return the execution order (topological sort)"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in task dependencies")
        
        return order
    
    def parallel_groups(self) -> List[List[str]]:
        """Split into groups that can run in parallel"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        groups = []
        remaining = dict(in_degree)
        
        while remaining:
            ready = [t for t, d in remaining.items() if d == 0]
            if not ready:
                raise ValueError("Unresolvable dependency cycle")
            
            groups.append(ready)
            
            for task_id in ready:
                del remaining[task_id]
                for neighbor in self.adj[task_id]:
                    if neighbor in remaining:
                        remaining[neighbor] -= 1
        
        return groups
```

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

The code below defines common task templates as a dictionary: each template (bug_fix, new_feature, code_review, refactor, debug_investigation, performance_optimization, migration) contains a title, a sub-task list with individual token estimates, and a total estimated token count. The create_task_from_template function just needs the template name and fills in specifics to immediately produce a complete Task.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
TASK_TEMPLATES = {
    "bug_fix": {
        "title": "Fix: {bug_description}",
        "subtasks": [
            {"title": "Reproduce the bug", "tokens": 500},
            {"title": "Read and understand affected code", "tokens": 1000},
            {"title": "Identify root cause", "tokens": 800},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Write regression test", "tokens": 1000},
            {"title": "Verify fix in all scenarios", "tokens": 500},
        ],
        "estimated_total_tokens": 5300,
    },
    
    "new_feature": {
        "title": "Feature: {feature_name}",
        "subtasks": [
            {"title": "Analyze requirements", "tokens": 500},
            {"title": "Read existing code patterns", "tokens": 1000},
            {"title": "Design approach", "tokens": 800},
            {"title": "Implement core logic", "tokens": 3000},
            {"title": "Add error handling", "tokens": 800},
            {"title": "Write tests", "tokens": 1500},
            {"title": "Update documentation", "tokens": 500},
        ],
        "estimated_total_tokens": 8100,
    },
    
    "code_review": {
        "title": "Review: {target}",
        "subtasks": [
            {"title": "Read all changed files", "tokens": 2000},
            {"title": "Check code style & conventions", "tokens": 500},
            {"title": "Analyze logic & correctness", "tokens": 1500},
            {"title": "Review for security issues", "tokens": 1000},
            {"title": "Write review comments", "tokens": 1000},
        ],
        "estimated_total_tokens": 6000,
    },
    
    "refactor": {
        "title": "Refactor: {target_module}",
        "subtasks": [
            {"title": "Analyze current structure", "tokens": 1000},
            {"title": "Identify code smells", "tokens": 800},
            {"title": "Plan refactoring steps", "tokens": 500},
            {"title": "Extract functions/classes", "tokens": 2000},
            {"title": "Update imports & references", "tokens": 1000},
            {"title": "Run existing tests", "tokens": 500},
            {"title": "Verify behavior unchanged", "tokens": 500},
        ],
        "estimated_total_tokens": 6300,
    },
    
    "debug_investigation": {
        "title": "Debug: {issue_description}",
        "subtasks": [
            {"title": "Gather error info and logs", "tokens": 800},
            {"title": "Read stack trace and affected files", "tokens": 1500},
            {"title": "Add strategic logging/breakpoints", "tokens": 1000},
            {"title": "Reproduce with minimal test case", "tokens": 800},
            {"title": "Identify root cause", "tokens": 1000},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Add regression test", "tokens": 800},
        ],
        "estimated_total_tokens": 7400,
    },
    
    "performance_optimization": {
        "title": "Optimize: {target}",
        "subtasks": [
            {"title": "Profile current performance", "tokens": 1000},
            {"title": "Identify bottlenecks", "tokens": 800},
            {"title": "Research optimization strategies", "tokens": 1000},
            {"title": "Implement optimizations", "tokens": 2000},
            {"title": "Benchmark before/after", "tokens": 800},
            {"title": "Verify no regressions", "tokens": 500},
        ],
        "estimated_total_tokens": 6100,
    },
    
    "migration": {
        "title": "Migrate: {source} → {target}",
        "subtasks": [
            {"title": "Analyze source and target", "tokens": 1500},
            {"title": "Create migration plan", "tokens": 800},
            {"title": "Write migration scripts", "tokens": 2000},
            {"title": "Test migration on sample data", "tokens": 1000},
            {"title": "Run full migration", "tokens": 1500},
            {"title": "Verify and cleanup", "tokens": 800},
        ],
        "estimated_total_tokens": 7600,
    },
}


def create_task_from_template(template_name: str, **kwargs) -> Task:
    """Create a task from a template"""
    template = TASK_TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")
    
    title = template["title"].format(**kwargs)
    
    return Task(
        id=f"task-{hash(title) % 10000:04d}",
        title=title,
        description=f"Task from template: {template_name}",
        category=TaskCategory.UNKNOWN,
        estimated_tokens=template["estimated_total_tokens"],
    )
```

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

The table below is an empirical "price list" for estimating tokens per task type: look up the task type (bug fix, new feature, migration, etc.) and complexity, read the Estimated Tokens column, and you know how much to budget. The bottom section gives quick estimation numbers (e.g., 1 line of code lands at 5-10 tokens) and how to allocate a 128K context window.

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

This is the automatic estimation code: EffortEstimator takes a Task, picks a base number (BASE_TOKENS) based on complexity, multiplies by a per-task-type factor (e.g., writing docs is cheaper than new code), adds a "fee" for each file touched, then returns tokens, an estimated duration (assuming about 100 tokens per minute), and a batch summary.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from enum import Enum
from typing import Dict, List, Tuple

class EffortEstimator:
    """
    Estimates effort for coding tasks based on historical data
    and task characteristics.
    """
    
    # Base tokens per complexity level
    BASE_TOKENS = {
        TaskComplexity.TRIVIAL: 500,
        TaskComplexity.SIMPLE: 2000,
        TaskComplexity.MODERATE: 5000,
        TaskComplexity.COMPLEX: 12000,
        TaskComplexity.EPIC: 25000,
    }
    
    # Multipliers per category
    CATEGORY_MULTIPLIERS = {
        TaskCategory.GENERATION: 1.0,
        TaskCategory.MODIFICATION: 0.8,
        TaskCategory.ANALYSIS: 0.6,
        TaskCategory.DOCUMENTATION: 0.4,
        TaskCategory.TESTING: 0.7,
    }
    
    # File involvement bonus
    FILE_BONUS_PER_FILE = 500
    
    def estimate_tokens(self, task: Task) -> int:
        """Estimate the number of tokens required"""
        base = self.BASE_TOKENS.get(task.complexity, 2000)
        multiplier = self.CATEGORY_MULTIPLIERS.get(task.category, 1.0)
        file_bonus = len(task.files_involved) * self.FILE_BONUS_PER_FILE
        
        return int(base * multiplier + file_bonus)
    
    def estimate_duration(self, task: Task) -> Dict[str, float]:
        """
        Estimate execution time (minutes).
        Assumption: ~100 tokens/minute processing speed.
        """
        tokens = self.estimate_tokens(task)
        processing_minutes = tokens / 100
        
        # Add overhead for coordination, review
        overhead = 1.2 if len(task.dependencies) > 2 else 1.1
        
        total_minutes = processing_minutes * overhead
        
        return {
            "processing_minutes": processing_minutes,
            "overhead_factor": overhead,
            "total_minutes": total_minutes,
            "total_hours": total_minutes / 60,
        }
    
    def estimate_batch(self, tasks: List[Task]) -> Dict[str, float]:
        """Estimate for the whole batch of tasks"""
        total_tokens = sum(self.estimate_tokens(t) for t in tasks)
        estimates = [self.estimate_duration(t) for t in tasks]
        
        return {
            "total_tokens": total_tokens,
            "total_minutes": sum(e["total_minutes"] for e in estimates),
            "task_count": len(tasks),
            "avg_tokens_per_task": total_tokens / len(tasks) if tasks else 0,
        }
```

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

The diagram below lists the 8 most common task management errors. Each error is marked "❌ ANTI-PATTERN", with identifying symptoms and a "→ SOLUTION" arrow showing how to cure it. Read it as a lookup table: when you see any symptom in your task, apply the corresponding solution immediately.

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

This is the automatic anti-pattern detection engine: AntiPatternDetector takes a Task, runs the checks in sequence (task larger than 20K tokens, vague description, missing estimate, too many dependencies, missing file scope), and returns a list of issues with severity and remediation suggestions. Run it before starting a task to "diagnose" early.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class AntiPatternDetector:
    """
    Detect anti-patterns in task management.
    """
    
    def detect(self, task: Task, context: Dict = None) -> List[Dict]:
        """Check the task and return a list of anti-patterns"""
        issues = []
        context = context or {}
        
        # Check 1: Killer Task
        if task.estimated_tokens > 20000:
            issues.append({
                "pattern": "KILLER_TASK",
                "severity": "HIGH",
                "message": f"Task estimated {task.estimated_tokens} tokens. "
                          f"Decompose into smaller tasks (< 5K each).",
                "suggestion": "Use TaskDecomposer with 'feature' or 'layer' strategy",
            })
        
        # Check 2: Ambiguous Task
        vague_keywords = [
            "improve", "optimize", "clean", "better",
            "refactor", "make it work", "fix it"
        ]
        if any(kw in task.description.lower() for kw in vague_keywords):
            if not task.verification_criteria:
                issues.append({
                    "pattern": "AMBIGUOUS_TASK",
                    "severity": "MEDIUM",
                    "message": "Task description is vague without clear criteria",
                    "suggestion": "Add specific acceptance criteria and expected outcomes",
                })
        
        # Check 3: Missing Token Estimate
        if task.estimated_tokens == 0:
            issues.append({
                "pattern": "MISSING_ESTIMATE",
                "severity": "LOW",
                "message": "No token estimate provided",
                "suggestion": "Use EffortEstimator to get initial estimate",
            })
        
        # Check 4: Too Many Dependencies
        if len(task.dependencies) > 5:
            issues.append({
                "pattern": "DEPENDENCY_OVERLOAD",
                "severity": "MEDIUM",
                "message": f"Task has {len(task.dependencies)} dependencies",
                "suggestion": "Consider reducing dependencies or splitting task",
            })
        
        # Check 5: No Files Involved (for modification tasks)
        if (task.category == TaskCategory.MODIFICATION 
            and len(task.files_involved) == 0):
            issues.append({
                "pattern": "MISSING_FILE_SCOPE",
                "severity": "MEDIUM",
                "message": "Modification task has no files identified",
                "suggestion": "Scan codebase to identify affected files",
            })
        
        return issues
```

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

```python
class TokenBudgetManager:
    """
    Manage the token budget for task execution.
    Prevents context overflow and optimizes token usage.
    """
    
    def __init__(self, total_budget: int = 128000):
        self.total_budget = total_budget
        self.allocated = {
            "system": 5000,
            "project_context": 0,
            "task_context": 0,
            "working_memory": 0,
        }
        self.min_reserve = 20000
    
    @property
    def remaining(self) -> int:
        used = sum(self.allocated.values())
        return self.total_budget - used - self.min_reserve
    
    @property
    def usage_percent(self) -> float:
        used = sum(self.allocated.values())
        return (used / self.total_budget) * 100
    
    def can_fit(self, estimated_tokens: int) -> bool:
        """Check if there is enough budget for the task"""
        return self.remaining >= estimated_tokens
    
    def allocate_for_task(self, task: Task) -> bool:
        """Allocate budget to the task — returns False if insufficient"""
        needed = task.estimated_tokens or 2000
        if not self.can_fit(needed):
            return False
        
        self.allocated["task_context"] += needed
        return True
    
    def add_to_working_memory(self, tokens: int):
        """Add tokens to working memory"""
        self.allocated["working_memory"] += tokens
    
    def summarize_context(self) -> str:
        """Summarize the budget status"""
        lines = [
            "=== Token Budget Status ===",
            f"Total:     {self.total_budget:,}",
            f"System:    {self.allocated['system']:,}",
            f"Project:   {self.allocated['project_context']:,}",
            f"Task:      {self.allocated['task_context']:,}",
            f"Working:   {self.allocated['working_memory']:,}",
            f"Reserve:   {self.min_reserve:,}",
            f"Remaining: {self.remaining:,}",
            f"Usage:     {self.usage_percent:.1f}%",
        ]
        
        if self.usage_percent > 80:
            lines.append("⚠️ WARNING: High context usage!")
        if self.remaining < 5000:
            lines.append("🚨 CRITICAL: Very low remaining budget!")
        
        return "\n".join(lines)
    
    def suggest_compaction(self) -> List[str]:
        """Suggest ways to reduce token usage"""
        suggestions = []
        
        if self.allocated["working_memory"] > 30000:
            suggestions.append(
                "Summarize older working memory entries"
            )
        
        if self.allocated["project_context"] > 20000:
            suggestions.append(
                "Remove non-essential project files from context"
            )
        
        if self.usage_percent > 85:
            suggestions.append(
                "Complete current sub-task and start new session"
            )
        
        return suggestions
```

</details>

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
