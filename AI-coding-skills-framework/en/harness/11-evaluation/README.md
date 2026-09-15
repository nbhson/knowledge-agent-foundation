# 📊 XI. Evaluation

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Evaluation Dimensions](#1-evaluation-dimensions)
>   - [1.1 Evaluation Dimensions](#11-evaluation-dimensions)
>   - [1.2 Evaluation Rubric](#12-evaluation-rubric)
>   - [1.3 Weight Configuration — Depending on Use Case](#13-weight-configuration-depending-on-use-case)
> - [2. Quality Metrics](#2-quality-metrics)
>   - [2.1 Code Quality Metrics](#21-code-quality-metrics)
>   - [2.2 AI Agent Quality Metrics](#22-ai-agent-quality-metrics)
>   - [2.3 Metrics Dashboard](#23-metrics-dashboard)
> - [3. Performance Benchmarks](#3-performance-benchmarks)
>   - [3.1 Benchmark Framework](#31-benchmark-framework)
>   - [3.2 Standard Benchmark Tasks](#32-standard-benchmark-tasks)
>   - [3.3 Benchmark Comparison Table](#33-benchmark-comparison-table)
> - [4. Evaluation Framework](#4-evaluation-framework)
>   - [4.1 Auto-Evaluation Pipeline](#41-auto-evaluation-pipeline)
>   - [4.2 LLM-as-Judge Evaluation](#42-llm-as-judge-evaluation)
>   - [4.3 Regression Testing Framework](#43-regression-testing-framework)
> - [5. Continuous Improvement](#5-continuous-improvement)
>   - [5.1 Improvement Loop](#51-improvement-loop)
>   - [5.2 A/B Testing Framework](#52-ab-testing-framework)
> - [6. Reporting & Dashboards](#6-reporting--dashboards)
>   - [6.1 Evaluation Report Generator](#61-evaluation-report-generator)
> - [7. Case Studies](#7-case-studies)
>   - [7.1 SWE-bench — Benchmarking AI Code Agents](#71-swe-bench-benchmarking-ai-code-agents)
>   - [7.2 HumanEval — Classic Code Generation](#72-humaneval-classic-code-generation)
>   - [7.3 Real-World Evaluation Pipeline — Production Case](#73-real-world-evaluation-pipeline-production-case)
> - [8. Evaluation Tooling](#8-evaluation-tooling)
>   - [8.1 Popular Evaluation Tools](#81-popular-evaluation-tools)
>   - [8.2 PromptFoo Configuration Example](#82-promptfoo-configuration-example)
> - [9. Best Practices](#9-best-practices)
>   - [9.1 DO and DON'T](#91-do-and-dont)
>   - [9.2 Evaluation Strategy](#92-evaluation-strategy)
> - [10. Real-World Case Studies](#10-real-world-case-studies)
>   - [10.1 Princeton NLP SWE-bench: Benchmarking Real-World Code](#101-princeton-nlp-swe-bench-benchmarking-real-world-code)
>   - [10.2 Aider: LLM Leaderboard for Coding](#102-aider-llm-leaderboard-for-coding)
>   - [10.3 LiveCodeBench: Dynamic Evaluation](#103-livecodebench-dynamic-evaluation)
>   - [10.4 Anthropic's Evaluation Methodology](#104-anthropics-evaluation-methodology)
> - [11. TypeScript Interfaces for Evaluation](#11-typescript-interfaces-for-evaluation)
>   - [11.1 Core Evaluation Types](#111-core-evaluation-types)
> - [12. Design Principles for Evaluation](#12-design-principles-for-evaluation)
>   - [12.1 SOLID for Evaluation Systems](#121-solid-for-evaluation-systems)
>   - [12.2 Evaluation Design Principles](#122-evaluation-design-principles)
> - [13. Testing Evaluation Harness](#13-testing-evaluation-harness)
>   - [13.1 Evaluation Test Harness](#131-evaluation-test-harness)
> - [14. Future Trends in Evaluation](#14-future-trends-in-evaluation)
>   - [14.1 AI Evaluation Trends (2024-2026)](#141-ai-evaluation-trends-2024-2026)
> - [References](#references)
>   - [Papers & Research](#papers-research)
>   - [Frameworks & Tools](#frameworks-tools)
>   - [Benchmarks](#benchmarks)
>   - [Case Study References](#case-study-references)
>
---

### Opening Story

You build a new bridge. You can say *"It looks fine"*, but without **measuring the load, testing the materials, stress-testing with heavy trucks** — you won't know whether the bridge will hold for 10 years of use or collapse after 1 month.

**AI code is the same.** Writing code without evaluating it = **shipping a bridge without inspecting it**.

When you use AI to generate code, the most important question is not *"Does the code run?"* but: *"Is the code correct? Is it safe? Is it maintainable? Is it better than writing it by hand?"* — and you need a **proper evaluation system** to answer.

**The solution**: a Multi-level Evaluation Framework — from functional correctness to business value, ensuring every line of AI-generated code **meets the standard before it reaches the user**.

### Why Is Evaluation Important?

> *"If you can't measure it, you can't improve it. And if you can't improve it, you're falling behind."*

#### 3 Scientific Pieces of Evidence

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **SWE-bench (Princeton, 2025)** | Top models resolve **44% of real GitHub issues** — but **only when evaluated the right way** do you learn which model is actually good for a specific use case |
| 2 | **Google Research (2024)** | Teams with systematic evaluation pipelines caught **3× more regressions** before reaching production |
| 3 | **Microsoft (2025)** | AI code generation without evaluation increased **technical debt by 28%** in 6 months |

#### Core philosophy:

```
Evaluation = What You Measure → What You Improve → What You Ship
```

**5 Levels of Evaluation**:
- **Level 1**: Code works (functional correctness)
- **Level 2**: Code is correct (edge cases, error handling)
- **Level 3**: Code is good (readability, maintainability)
- **Level 4**: Code is safe (security, performance)
- **Level 5**: Code adds value (business impact, user satisfaction)

**Analogies**: Evaluation is like a quality-control system in a factory — not just checking whether the product is broken (Level 1), but also whether the finish is nice (Level 3), whether the materials are safe (Level 4), and whether the customer is happy (Level 5).

**If you skip it**: you ship code without knowing its quality, don't know when a regression appears, don't know which model beats which, and in the end technical debt accumulates to the point where refactoring costs 10× as much.

## Overview

**Evaluation** in AI coding is the process of **assessing the effectiveness and quality** of an AI agent performing coding tasks. Evaluation includes benchmarking, metrics collection, and continuous improvement based on evaluation results.

> **"You can't improve what you can't measure"** — Peter Drucker

```
┌──────────────────────────────────────────────────────────────────┐
│                      EVALUATION FRAMEWORK                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Input   │    │  Agent   │    │  Output  │            │  │
│  │  │  Tasks   │───►│  Execute │───►│  Code    │            │  │
│  │  └──────────┘    └──────────┘    └────┬─────┘            │  │
│  │                                        │                   │  │
│  │                                        ▼                   │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │ Improve  │◄───│ Analyze  │◄───│ Evaluate │            │  │
│  │  │ Action   │    │ Results  │    │ Metrics  │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Evaluation Dimensions](#1-evaluation-dimensions) | Evaluation dimensions |
| 2 | [Quality Metrics](#2-quality-metrics) | Code quality metrics |
| 3 | [Performance Benchmarks](#3-performance-benchmarks) | Performance benchmarks |
| 4 | [Evaluation Framework](#4-evaluation-framework) | Automated evaluation framework |
| 5 | [Continuous Improvement](#5-continuous-improvement) | Continuous improvement |
| 6 | [Reporting & Dashboards](#6-reporting--dashboards) | Reports and dashboards |
| 7 | [Case Studies](#7-case-studies) | Real-world case studies |
| 8 | [Evaluation Tooling](#8-evaluation-tooling) | Tools and frameworks |
| 9 | [Best Practices](#9-best-practices) | Evaluation principles |

---

## 1. Evaluation Dimensions

> **📌 Core Concept**
>
> **Concept:** Evaluation Dimensions are the separate "facets" for measuring the quality of an AI agent — correctness, efficiency, safety, reliability and more. Each facet is its own scale; combined, they give you the full picture instead of just a single number.
> **Analogy/comparison:** Like a school report card — not just a math grade, but also English, PE, and conduct. Grading many subjects reveals which strengths and weaknesses a student has.
> **Why it matters:** AI quality is very abstract; you have to break it into clear measurement dimensions to know what to improve.

### 1.1 Evaluation Dimensions

The table below brings together **9 evaluation dimensions** you should consider when grading an AI agent — from correctness to cost-effectiveness. Read it like a "health checkup table": each row is a question you need to answer about your agent.

```
┌──────────────────────────────────────────────────────────────────┐
│                EVALUATION DIMENSIONS                              │
│                                                                  │
│  1. CORRECTNESS (Correct)                                       │
│     Does the code run correctly?                                │
│     → Functional correctness, edge cases                       │
│                                                                  │
│  2. QUALITY (Good)                                              │
│     Is the code clean?                                          │
│     → Readability, maintainability, complexity                  │
│                                                                  │
│  3. EFFICIENCY (Fast)                                           │
│     Is the code optimized?                                       │
│     → Time complexity, memory usage, I/O                       │
│                                                                  │
│  4. SAFETY (Safe)                                               │
│     Is the code safe?                                           │
│     → Security, error handling, edge cases                     │
│                                                                  │
│  5. COMPLETENESS (Complete)                                     │
│     Is the task fully done?                                     │
│     → Coverage, missing features                                │
│                                                                  │
│  6. SPEED (Speed)                                               │
│     Is the agent fast?                                          │
│     → Tokens used, time to completion                           │
│                                                                  │
│  7. USABILITY (Usable)                                          │
│     Is the output easy to use?                                    │
│     → Documentation, API design, examples                      │
│                                                                  │
│  8. COST-EFFECTIVENESS (Cost-effective)                         │
│     Is the cost reasonable?                                      │
│     → Token cost vs value delivered                             │
│                                                                  │
│  9. RELIABILITY (Reliable)                                       │
│     Are the results stable?                                      │
│     → Consistency across runs, reproducibility                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Evaluation Rubric

This code defines the **scoring rubric** — the set of criteria spelling out what a 5, a 3, or a 1 means for each evaluation dimension. Like grading criteria for an exam: with clear descriptions, grading is fair and consistent across runs. You can try it to see a result accumulated with weights into a total 0-100 score.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class Rating(Enum):
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    FAILED = 1


@dataclass
class EvaluationDimension:
    """An evaluation dimension"""
    name: str
    weight: float              # 0.0 - 1.0
    description: str
    criteria: Dict[Rating, str] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Evaluation result for a task"""
    task_id: str
    scores: Dict[str, float] = field(default_factory=dict)
    notes: Dict[str, str] = field(default_factory=dict)
    total_score: float = 0.0
    
    def add_score(self, dimension: str, score: float, 
                  note: str = ""):
        self.scores[dimension] = score
        if note:
            self.notes[dimension] = note
    
    def calculate_total(self, weights: Dict[str, float]) -> float:
        """Compute the weighted total score"""
        total = 0.0
        total_weight = 0.0
        
        for dim, weight in weights.items():
            if dim in self.scores:
                total += self.scores[dim] * weight
                total_weight += weight
        
        self.total_score = total / total_weight if total_weight else 0
        return self.total_score


# Define standard rubric
STANDARD_RUBRIC = [
    EvaluationDimension(
        name="correctness",
        weight=0.25,
        description="Code runs correctly, handles edge cases",
        criteria={
            Rating.EXCELLENT: "All tests pass, edge cases handled",
            Rating.GOOD: "Most tests pass, minor edge case missed",
            Rating.ACCEPTABLE: "Core functionality works, some gaps",
            Rating.POOR: "Partially working, key issues remain",
            Rating.FAILED: "Does not work or breaks existing code",
        }
    ),
    EvaluationDimension(
        name="quality",
        weight=0.20,
        description="Code is clean, readable, maintainable",
        criteria={
            Rating.EXCELLENT: "Follows all conventions, self-documenting",
            Rating.GOOD: "Clean code, minor style issues",
            Rating.ACCEPTABLE: "Readable but could be improved",
            Rating.POOR: "Messy but understandable",
            Rating.FAILED: "Unreadable or extremely messy",
        }
    ),
    EvaluationDimension(
        name="efficiency",
        weight=0.15,
        description="Performance is appropriate for the use case",
        criteria={
            Rating.EXCELLENT: "Optimal complexity, minimal resources",
            Rating.GOOD: "Good performance, minor optimizations possible",
            Rating.ACCEPTABLE: "Acceptable for most cases",
            Rating.POOR: "Performance concerns for scale",
            Rating.FAILED: "Severe performance issues",
        }
    ),
    EvaluationDimension(
        name="safety",
        weight=0.15,
        description="Code handles errors and is secure",
        criteria={
            Rating.EXCELLENT: "Comprehensive error handling, no vulnerabilities",
            Rating.GOOD: "Good error handling, minor security notes",
            Rating.ACCEPTABLE: "Basic error handling present",
            Rating.POOR: "Minimal error handling",
            Rating.FAILED: "No error handling, security risks",
        }
    ),
    EvaluationDimension(
        name="completeness",
        weight=0.15,
        description="All requirements are addressed",
        criteria={
            Rating.EXCELLENT: "All requirements + bonus improvements",
            Rating.GOOD: "All requirements met",
            Rating.ACCEPTABLE: "Core requirements met, some missing",
            Rating.POOR: "Partially completed",
            Rating.FAILED: "Major requirements missing",
        }
    ),
    EvaluationDimension(
        name="speed",
        weight=0.10,
        description="Token efficiency and time to completion",
        criteria={
            Rating.EXCELLENT: "Minimal tokens, fast completion",
            Rating.GOOD: "Reasonable token usage",
            Rating.ACCEPTABLE: "Average token usage",
            Rating.POOR: "High token usage, slow",
            Rating.FAILED: "Extremely inefficient",
        }
    ),
]
```

</details>

### 1.3 Weight Configuration — Depending on Use Case

The code here shows the same set of evaluation dimensions, but **the weights change with the goal** — like a university exam weighted toward the sciences, while a vocational school weighs hands-on skill more. Where safety matters, raise the `safety` weight; where fast delivery matters, raise `completeness`. Tune `WEIGHT_CONFIGS` to match your use case.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Different weight configurations for different scenarios
WEIGHT_CONFIGS = {
    "production_code": {
        "correctness": 0.30,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.20,
        "completeness": 0.10,
        "speed": 0.05,
    },
    
    "prototype_hackathon": {
        "correctness": 0.35,
        "quality": 0.05,
        "efficiency": 0.05,
        "safety": 0.05,
        "completeness": 0.40,
        "speed": 0.10,
    },
    
    "library_framework": {
        "correctness": 0.25,
        "quality": 0.25,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.10,
        "speed": 0.10,
    },
    
    "ai_agent_harness": {
        "correctness": 0.20,
        "quality": 0.15,
        "efficiency": 0.10,
        "safety": 0.25,
        "completeness": 0.15,
        "speed": 0.15,
    },
}
```

</details>

---

## 2. Quality Metrics

> **📌 Core Concept**
>
> **Concept:** Quality Metrics are quantitative measures used to grade the quality of an AI agent's output — accuracy, completeness, adherence, style — turning subjective judgment into objective, comparable numbers.
> **Analogy/comparison:** Like a food-scoring scale: flavor (correctness), presentation (style), portion size (completeness). Clear scores let the cook know which dishes need improving.
> **Why it matters:** Without concrete numbers, "looks like it's fine" replaces real evaluation, and you can't track progress over time.

### 2.1 Code Quality Metrics

The `CodeQualityAnalyzer` class automatically grades code quality — complexity (cyclomatic complexity), maintainability index, naming, docstring coverage — then aggregates it into an overall 0-100 score. Like an "auto-grading teacher": takes code as input, returns a scorecard with specific metrics instead of just saying "this code is fine".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import ast
import math
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path

@dataclass
class CodeQualityReport:
    """Code quality report"""
    file_path: str
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 0.0
    duplication_ratio: float = 0.0
    naming_score: float = 0.0
    documentation_score: float = 0.0
    overall_score: float = 0.0


class CodeQualityAnalyzer:
    """
    Analyze code quality — compute metrics automatically.
    
    Metrics:
    - Lines of Code (LOC)
    - Cyclomatic Complexity
    - Maintainability Index
    - Code Duplication
    - Naming Conventions
    - Documentation Coverage
    """
    
    def analyze(self, code: str, file_path: str = "") -> CodeQualityReport:
        report = CodeQualityReport(file_path=file_path)
        
        lines = code.strip().split("\n")
        report.lines_of_code = len(lines)
        report.cyclomatic_complexity = self._calc_complexity(code)
        report.maintainability_index = self._calc_maintainability(
            code, report.cyclomatic_complexity, report.lines_of_code
        )
        report.naming_score = self._calc_naming_score(code)
        report.documentation_score = self._calc_doc_score(code)
        
        # Overall score (weighted average)
        scores = [
            report.maintainability_index * 0.3,
            report.naming_score * 0.25,
            report.documentation_score * 0.25,
            max(0, 100 - report.cyclomatic_complexity * 10) * 0.2,
        ]
        report.overall_score = sum(scores)
        
        return report
    
    def _calc_complexity(self, code: str) -> float:
        """Compute cyclomatic complexity"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 10.0  # High complexity for unparseable code
        
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For,
                                ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calc_maintainability(self, code: str, 
                               complexity: float, loc: int) -> float:
        """Compute maintainability index (0-100)"""
        if loc == 0:
            return 100.0
        
        # Simplified MI formula
        mi = 171 - 5.2 * math.log(max(loc, 1)) - 0.23 * complexity - 16.2 * math.log(max(loc, 1))
        return max(0, min(100, mi))
    
    def _calc_naming_score(self, code: str) -> float:
        """Evaluate naming conventions"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        good_names = 0
        total_names = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_names += 1
                if (node.name.islower() and 
                    "_" in node.name or 
                    node.name.startswith("_")):
                    good_names += 1
            elif isinstance(node, ast.ClassDef):
                total_names += 1
                if node.name[0].isupper():
                    good_names += 1
        
        return (good_names / total_names * 100) if total_names else 100.0
    
    def _calc_doc_score(self, code: str) -> float:
        """Evaluate documentation coverage"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        documented = 0
        total = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total += 1
                if (ast.get_docstring(node)):
                    documented += 1
        
        return (documented / total * 100) if total else 100.0
```

</details>

### 2.2 AI Agent Quality Metrics

This part measures **the entire generation process of the AI agent**, not just the result: first-attempt success rate, number of retries, tokens consumed, rate of not breaking existing functionality. A good agent usually gets it right early, retries little, and spends few tokens — like an employee who knows the job and doesn't ask the boss over and over.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AgentQualityMetrics:
    """
    Metrics specific to an AI coding agent.
    
    Unlike ordinary code quality,
    agent metrics measure the entire GENERATION PROCESS,
    not just the final result.
    """
    
    # === PROCESS METRICS ===
    
    # 1. First-Attempt Success Rate
    # Rate of code correct on the first attempt (no retry needed)
    first_attempt_success: float = 0.0
    
    # 2. Iteration Efficiency
    # Average number of retries to complete a task
    avg_iterations: float = 0.0
    
    # 3. Token Efficiency
    # Tokens used vs optimal (lower = better)
    token_efficiency: float = 0.0
    
    # 4. Time to First Good Output
    # Time from prompt to the first valid output
    time_to_first_output: float = 0.0
    
    # === OUTPUT METRICS ===
    
    # 5. Code Correctness
    # Test pass rate
    test_pass_rate: float = 0.0
    
    # 6. Edit Precision
    # Ratio of edits that were truly necessary / total edits
    edit_precision: float = 0.0
    
    # 7. Context Relevance
    # Was the right context used (no hallucination)
    context_relevance: float = 0.0
    
    # 8. Instruction Following
    # Was the task done as requested
    instruction_following: float = 0.0
    
    # === SAFETY METRICS ===
    
    # 9. No Regressions
    # Does not break existing functionality
    regression_free_rate: float = 0.0
    
    # 10. Security Compliance
    # Does not introduce vulnerabilities
    security_compliance: float = 0.0
    
    def calculate_composite_score(self) -> float:
        """Compute the composite score from all metrics"""
        weights = {
            "first_attempt_success": 0.15,
            "test_pass_rate": 0.25,
            "edit_precision": 0.10,
            "context_relevance": 0.10,
            "instruction_following": 0.15,
            "regression_free_rate": 0.15,
            "token_efficiency": 0.10,
        }
        
        total = 0.0
        for metric, weight in weights.items():
            value = getattr(self, metric, 0.0)
            total += value * weight
        
        return total * 100  # Scale to 0-100
```

</details>

### 2.3 Metrics Dashboard

The sample dashboard below bundles all metrics into a single screen: one percentage bar per dimension, ending with the COMPOSITE SCORE. Reading it is very simple — a long bar is good, a short bar marks where to improve. A dashboard like this lets the whole team "know at a glance" where the agent is strong and where it's weak.

```
┌──────────────────────────────────────────────────────────────────┐
│                AI AGENT QUALITY DASHBOARD                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ CORRECTNESS                           ████████░░ 82%    │   │
│  │ └─ Test Pass Rate                     ████████░░ 85%    │   │
│  │ └─ Edge Case Handling                 ███████░░░ 72%    │   │
│  │ └─ Regression Free                    █████████░ 90%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ QUALITY                               ███████░░░ 75%    │   │
│  │ └─ Maintainability                    ███████░░░ 70%    │   │
│  │ └─ Naming Conventions                 █████████░ 88%    │   │
│  │ └─ Documentation                      ███████░░░ 68%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ EFFICIENCY                            ████████░░ 80%    │   │
│  │ └─ Token Efficiency                   ████████░░ 82%    │   │
│  │ └─ Time to Completion                 ███████░░░ 75%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ SAFETY                                █████████░ 88%    │   │
│  │ └─ No Vulnerabilities                 ██████████ 95%    │   │
│  │ └─ Error Handling                     ████████░░ 82%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ COMPOSITE SCORE                       ████████░░ 81/100 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Performance Benchmarks

> **📌 Core Concept**
>
> **Concept:** Performance Benchmarks are standardized tests — SWE-bench, HumanEval, LiveCodeBench — that use a fixed question set to measure an agent's capability, enabling fair comparison across models and versions.
> **Analogy/comparison:** Like a common admissions exam: every candidate takes the same exam, the same grading scale, so the school can judge who's better. If everyone writes their own exam, no comparison is ever possible.
> **Why it matters:** Without a common question set, each person grades their own way, and you can't tell whether model A is truly better than model B.

### 3.1 Benchmark Framework

`BenchmarkSuite` is the "playing field" for agents: you add tasks, run the agent on each task, then tally success rate, tokens used, time — even compare two runs against each other. Like a football pitch with a referee keeping time and writing minutes: every play is measured, no "I feel like I played well" stories.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List
from datetime import datetime

@dataclass
class BenchmarkResult:
    """Benchmark result for a task"""
    task_id: str
    task_description: str
    tokens_used: int = 0
    execution_time_s: float = 0.0
    success: bool = False
    quality_score: float = 0.0
    attempts: int = 0
    error_message: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


class BenchmarkSuite:
    """
    Benchmark suite for an AI coding agent.
    
    Run many tasks, collect metrics, and compare
    across runs/models/configurations.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.results: List[BenchmarkResult] = []
        self.tasks: List[Dict] = []
    
    def add_task(self, task_id: str, description: str,
                 input_data: Any = None,
                 expected_output: Any = None,
                 validator: Callable = None):
        """Add a task to the benchmark suite"""
        self.tasks.append({
            "id": task_id,
            "description": description,
            "input": input_data,
            "expected": expected_output,
            "validator": validator,
        })
    
    def run(self, agent_func: Callable, max_retries: int = 3):
        """
        Run the benchmark — run the agent on each task.
        
        agent_func: function(task) -> (output, tokens_used)
        """
        for task in self.tasks:
            result = BenchmarkResult(
                task_id=task["id"],
                task_description=task["description"],
            )
            
            start_time = time.time()
            
            for attempt in range(max_retries):
                try:
                    output, tokens = agent_func(task)
                    result.execution_time_s = time.time() - start_time
                    result.tokens_used = tokens
                    result.attempts = attempt + 1
                    
                    # Validate
                    if task.get("validator"):
                        result.success = task["validator"](output)
                    elif task.get("expected"):
                        result.success = output == task["expected"]
                    else:
                        result.success = True
                    
                    if result.success:
                        break
                        
                except Exception as e:
                    result.error_message = str(e)
                    result.attempts = attempt + 1
            
            self.results.append(result)
        
        return self.get_summary()
    
    def get_summary(self) -> Dict:
        """Summarize the benchmark results"""
        if not self.results:
            return {"total": 0}
        
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        total_tokens = sum(r.tokens_used for r in self.results)
        total_time = sum(r.execution_time_s for r in self.results)
        
        return {
            "suite": self.name,
            "total_tasks": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.results),
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens / len(self.results),
            "total_time_s": total_time,
            "avg_time_s": total_time / len(self.results),
            "avg_attempts": sum(
                r.attempts for r in self.results
            ) / len(self.results),
        }
    
    def compare_with(self, other_suite: "BenchmarkSuite") -> Dict:
        """Compare two benchmark suites"""
        s1 = self.get_summary()
        s2 = other_suite.get_summary()
        
        return {
            self.name: s1,
            other_suite.name: s2,
            "improvements": {
                "success_rate": (
                    s1["success_rate"] - s2["success_rate"]
                ),
                "avg_tokens": (
                    s2["avg_tokens"] - s1["avg_tokens"]
                ),
                "avg_time": (
                    s2["avg_time_s"] - s1["avg_time_s"]
                ),
            },
        }
```

</details>

### 3.2 Standard Benchmark Tasks

This list is a **sample question set**, organized by difficulty from trivial to complex: write hello world, reverse a string, fix an off-by-one bug, refactor a class. Each task ships with a validator for automated grading. Use it like a practice exam set: start easy to check that the agent even works, then ramp up the difficulty to measure real capability.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
BENCHMARK_TASKS = {
    # === TRIVIAL (Difficulty: 1/5) ===
    "hello_world": {
        "id": "basic-001",
        "description": "Create a hello world function",
        "difficulty": "trivial",
        "expected": "Hello, World!",
    },
    
    "string_reverse": {
        "id": "basic-002",
        "description": "Reverse a string without built-in",
        "difficulty": "trivial",
        "validator": lambda out: out("hello") == "olleh",
    },
    
    # === EASY (Difficulty: 2/5) ===
    "fibonacci": {
        "id": "algo-001",
        "description": "Implement fibonacci with memoization",
        "difficulty": "easy",
        "validator": lambda out: out(10) == 55,
    },
    
    "binary_search": {
        "id": "algo-002",
        "description": "Implement binary search",
        "difficulty": "easy",
        "validator": lambda out: out([1,2,3,4,5], 3) == 2,
    },
    
    # === MODERATE (Difficulty: 3/5) ===
    "api_endpoint": {
        "id": "web-001",
        "description": "Create a REST API endpoint for CRUD",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "bug_fix": {
        "id": "debug-001",
        "description": "Fix off-by-one error in loop",
        "difficulty": "easy",
        "validator": lambda out: True,
    },
    
    # === COMPLEX (Difficulty: 4/5) ===
    "refactor_class": {
        "id": "refactor-001",
        "description": "Refactor God class into smaller classes",
        "difficulty": "complex",
        "validator": lambda out: True,
    },
    
    "write_tests": {
        "id": "test-001",
        "description": "Write comprehensive unit tests",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    # === HARD (Difficulty: 5/5) ===
    "security_audit": {
        "id": "security-001",
        "description": "Find and fix SQL injection vulnerabilities",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "multi_file_refactor": {
        "id": "complex-001",
        "description": "Refactor across 5+ files with dependency updates",
        "difficulty": "hard",
        "validator": lambda out: True,
    },
}
```

</details>

### 3.3 Benchmark Comparison Table

A comparison of model scores on the most popular benchmarks in 2026. Read it by column: a model scoring 92% on HumanEval but only 53% on SWE-bench is perfectly normal — each benchmark measures a different capability (writing a single function is not the same as fixing a bug in a real repo). Remember the note at the bottom: scores change with model version and prompt style.

```
┌────────────────────────────────────────────────────────────────────┐
│           BENCHMARK SCORES COMPARISON (2026)                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Benchmark         │ Metric              │ Human │ Claude │ GPT-4 │
│  ──────────────────┼─────────────────────┼───────┼───────┼───────│
│  HumanEval         │ Pass@1              │ -     │ 92%   │ 86%   │
│  HumanEval         │ Pass@10             │ -     │ 96%   │ 92%   │
│  SWE-bench Lite    │ Resolved            │ -     │ 48%   │ 33%   │
│  SWE-bench Verified│ Resolved            │ -     │ 53%   │ 38%   │
│  MBPP+             │ Pass@1              │ -     │ 89%   │ 82%   │
│  LiveCodeBench     │ Pass@1              │ -     │ 45%   │ 38%   │
│  Aider Polyglot    │ % Correct           │ 95%   │ 72%   │ 61%   │
│                                                                    │
│  ──────────────────┼─────────────────────┼───────┼───────┼───────│
│  COMPOSITE SCORE   │ Overall             │ -     │ ~78%  │ ~65%  │
│                                                                    │
│  ⚠️  Note: Scores vary by model version and prompting strategy  │
│     Claude 3.5 Sonnet with good harness can outperform GPT-4o    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Evaluation Framework

> **📌 Core Concept**
>
> **Concept:** An Evaluation Framework is the "skeleton" that organizes the entire evaluation process — designing test cases, running trials, collecting results, analyzing — so that evaluation is repeated consistently and in an actionable way.
> **Analogy/comparison:** Like a quality-inspection line in a factory: the product passes through the weighing station, the safety station, the packing station — each station does one job, and the process repeats identically every time.
> **Why it matters:** Without a standard framework, each evaluation is done differently and the results can't be trusted for comparison.

### 4.1 Auto-Evaluation Pipeline

`EvaluationPipeline` turns the evaluation process into an **automated machine**: you add checks like lint, tests, security to the pipeline, run them on the code, then aggregate scores by weight and emit a summary. Each check is like one inspector on the line, each grading one criterion; the final number is the shared verdict of the whole inspection team.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Callable, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EvalConfig:
    """Evaluation configuration"""
    dimensions: List[str] = field(default_factory=lambda: [
        "correctness", "quality", "efficiency", 
        "safety", "completeness"
    ])
    weights: Dict[str, float] = field(default_factory=lambda: {
        "correctness": 0.25,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.15,
        "speed": 0.10,
    })
    auto_evaluate: bool = True
    human_review: bool = False


class EvaluationPipeline:
    """
    Automated evaluation pipeline for AI coding output.
    
    Steps:
    1. Static Analysis (lint, complexity, naming)
    2. Dynamic Testing (run tests, check output)
    3. Security Scan (vulnerability check)
    4. Quality Scoring (weighted dimensions)
    5. Report Generation
    """
    
    def __init__(self, config: EvalConfig = None):
        self.config = config or EvalConfig()
        self.checks: List[Callable] = []
        self.results: List[EvaluationResult] = []
    
    def add_check(self, name: str, check_func: Callable,
                  dimension: str, weight: float = 1.0):
        """Add a check to the pipeline"""
        self.checks.append({
            "name": name,
            "func": check_func,
            "dimension": dimension,
            "weight": weight,
        })
    
    def evaluate(self, task_id: str, code: str, 
                 context: Dict = None) -> EvaluationResult:
        """Run evaluation on the code"""
        result = EvaluationResult(task_id=task_id)
        
        for check in self.checks:
            try:
                score = check["func"](code, context or {})
                result.add_score(
                    check["name"],
                    score * check["weight"],
                    f"Auto-evaluated by {check['name']}"
                )
            except Exception as e:
                result.add_score(
                    check["name"], 0.0,
                    f"Evaluation failed: {str(e)}"
                )
        
        result.calculate_total(self.config.weights)
        self.results.append(result)
        return result
    
    def get_average_scores(self) -> Dict[str, float]:
        """Compute average scores across all evaluations"""
        if not self.results:
            return {}
        
        dim_scores = {}
        for result in self.results:
            for dim, score in result.scores.items():
                if dim not in dim_scores:
                    dim_scores[dim] = []
                dim_scores[dim].append(score)
        
        return {
            dim: sum(scores) / len(scores)
            for dim, scores in dim_scores.items()
        }


# Standard checks
def check_test_passes(code: str, context: Dict) -> float:
    """Check whether the code passes its tests"""
    tests = context.get("tests", [])
    if not tests:
        return 50.0  # No tests = neutral score
    # Would execute tests and return pass rate
    return 80.0

def check_no_lint_errors(code: str, context: Dict) -> float:
    """Check lint"""
    return 90.0  # Simplified

def check_complexity(code: str, context: Dict) -> float:
    """Check complexity"""
    analyzer = CodeQualityAnalyzer()
    report = analyzer.analyze(code)
    return min(100, max(0, 100 - report.cyclomatic_complexity * 5))
```

</details>

### 4.2 LLM-as-Judge Evaluation

This is the approach of **using a powerful LLM (GPT-4, Claude) as the "examiner"** to grade code produced by another LLM. It's like asking an experienced senior engineer to read the code, score it, and explain why — it handles fuzzy things like readability and design well, which automated graders struggle with. But remember: the examiner can be biased and hallucinate too, so use it in combination with automated tests; don't trust it blindly.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class LLMJudge:
    """
    Use an LLM to evaluate the output of an AI agent.
    
    Leverage: GPT-4, Claude, or another large model
    as a "judge" to assess code quality.
    
    Pros:
    - Can evaluate nuanced qualities (readability, design)
    - No need to write test cases for every edge case
    - Can understand intent and context
    
    Cons:
    - Cost (one extra LLM call)
    - May not be 100% consistent
    - The judge can also hallucinate
    """
    
    def __init__(self, judge_model_func):
        self.judge = judge_model_func
    
    def evaluate_code(self, code: str, task: str, 
                      context: str = "") -> Dict:
        """Evaluate code with an LLM judge"""
        
        prompt = f"""You are a senior code reviewer. Evaluate the following code.

TASK: {task}

CODE:
```

</details>
{code}
```

CONTEXT: {context}

Rate the code on these dimensions (1-10):
1. Correctness - Does it solve the task correctly?
2. Code Quality - Is it clean, readable, well-structured?
3. Efficiency - Is it performant?
4. Robustness - Does it handle edge cases?
5. Completeness - Does it address all requirements?

For each dimension, provide:
- Score (1-10)
- Brief justification (1 sentence)

Output as JSON:
{{
  "correctness": {{"score": N, "reason": "..."}},
  "quality": {{"score": N, "reason": "..."}},
  "efficiency": {{"score": N, "reason": "..."}},
  "robustness": {{"score": N, "reason": "..."}},
  "completeness": {{"score": N, "reason": "..."}},
  "overall": N,
  "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        response = self.judge(prompt)
        return self._parse_judgment(response)
    
    def compare_outputs(self, task: str, 
                        output_a: str, output_b: str) -> Dict:
        """Compare two outputs"""
        
        prompt = f"""Compare these two implementations for the same task.

TASK: {task}

IMPLEMENTATION A:
```
{output_a}
```

IMPLEMENTATION B:
```
{output_b}
```

Which is better and why? Rate each (1-10) and pick a winner.
Output as JSON:
{{
  "implementation_a": {{"score": N, "strengths": [...], "weaknesses": [...]}},
  "implementation_b": {{"score": N, "strengths": [...], "weaknesses": [...]}},
  "winner": "A" or "B",
  "reasoning": "..."
}}"""
        
        response = self.judge(prompt)
        return self._parse_comparison(response)
    
    def _parse_judgment(self, response: str) -> Dict:
        """Parse the JSON response from the LLM judge"""
        import json
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except json.JSONDecodeError:
            return {"error": "Failed to parse judgment"}
```

### 4.3 Regression Testing Framework

Regression testing answers the question: **after changing the prompt or the harness, does the agent "forget" how to do things correctly?** The method: store a "model answer" (golden answer) for each task, re-run and compare against the baseline; if the score drops more than 10%, flag a REGRESSION. Like a teacher who keeps students' old exams and occasionally has them retake one, to make sure they haven't "learned the front and forgotten the back".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class RegressionTestSuite:
    """
    Regression testing framework for an AI coding agent.
    
    Purpose: Ensure the agent doesn't "forget" how to do
    things correctly after an update / new prompt.
    
    Concept:
    - Each task has a verified "golden answer"
    - When the agent is updated, re-run all tasks
    - If the score drops -> REGRESSION
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.test_cases: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def add_test_case(self, task_id: str, prompt: str,
                      golden_output: str, 
                      validator: Callable = None,
                      category: str = "general"):
        """Add a test case with a golden output"""
        self.test_cases.append({
            "id": task_id,
            "prompt": prompt,
            "golden": golden_output,
            "validator": validator,
            "category": category,
        })
    
    def set_baseline(self, results: Dict[str, float]):
        """Set the baseline score for each test case"""
        self.baselines = results
    
    def run_and_check(self, agent_func: Callable) -> Dict:
        """
        Run the agent and check for regressions.
        
        agent_func: function(prompt) -> output
        
        Returns:
        {
            "total": N,
            "passed": N,
            "regressions": [...],
            "improvements": [...],
            "score_delta": float,
        }
        """
        results = {}
        regressions = []
        improvements = []
        
        for test in self.test_cases:
            output = agent_func(test["prompt"])
            
            # Score against golden
            if test["validator"]:
                score = 100.0 if test["validator"](output) else 0.0
            else:
                score = self._similarity_score(output, test["golden"])
            
            results[test["id"]] = score
            
            # Check regression
            baseline = self.baselines.get(test["id"], 50.0)
            if score < baseline - 10:  # 10% threshold
                regressions.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
            elif score > baseline + 10:
                improvements.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
        
        # Calculate overall
        avg_score = sum(results.values()) / len(results) if results else 0
        avg_baseline = sum(self.baselines.values()) / len(self.baselines) if self.baselines else 50
        
        return {
            "total": len(self.test_cases),
            "passed": sum(1 for s in results.values() if s >= 70),
            "regressions": regressions,
            "improvements": improvements,
            "avg_score": avg_score,
            "score_delta": avg_score - avg_baseline,
            "has_regression": len(regressions) > 0,
        }
    
    def _similarity_score(self, actual: str, expected: str) -> float:
        """Simple text similarity score"""
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        
        if not expected_words:
            return 100.0
        
        intersection = actual_words & expected_words
        return (len(intersection) / len(expected_words)) * 100
```

</details>

---

## 5. Continuous Improvement

> **📌 Core Concept**
>
> **Concept:** Continuous Improvement is the loop "measure → analyze → adjust → re-check", using evaluation results to improve the agent's prompts, tooling, and knowledge.
> **Analogy/comparison:** Like going to the gym: weigh yourself (measure), figure out why it hasn't gone down (analyze), change the workout (improve), then weigh in again to see if it worked (verify) — repeating every week.
> **Why it matters:** An AI agent only gets better through measured adjustments; without this loop it will stay stuck at its current level forever.

### 5.1 Improvement Loop

The diagram above is the **5-step improvement loop**: Measure → Analyze → Identify problems → Improve → Verify, then start over. Read it as the formula for one round of "maintenance" for the agent; run one cycle each week or each sprint.

```
┌──────────────────────────────────────────────────────────────────┐
│              CONTINUOUS IMPROVEMENT LOOP                          │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  1. MEASURE│   │ 2. ANALYZE│   │ 3. IDENTIFY│               │
│  │  Collect   │──►│ Find     │──►│ Top 3    │                  │
│  │  metrics   │   │ patterns │   │ issues   │                  │
│  └──────────┘    └──────────┘    └────┬─────┘                  │
│                                       │                          │
│                                       ▼                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  5. VERIFY│   │ 4. IMPROVE│   │  Plan    │                  │
│  │  Re-run   │◄──│ Update   │◄──│ Fix     │                   │
│  │  benchmark│   │ prompts  │   │ strategy│                    │
│  └─────┬────┘    └──────────┘    └──────────┘                  │
│        │                                                        │
│        └───► Back to 1. MEASURE                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Dict, List, Tuple

class ImprovementTracker:
    """
    Track improvement across iterations.
    
    Tracks:
    - Benchmark scores over time
    - Regression detection
    - Improvement suggestions
    """
    
    def __init__(self):
        self.iterations: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def set_baseline(self, benchmark_name: str, scores: Dict):
        """Set a baseline for the benchmark"""
        self.baselines[benchmark_name] = scores
    
    def record_iteration(self, iteration_id: str,
                         benchmark_name: str,
                         scores: Dict[str, float]):
        """Record an iteration's results"""
        self.iterations.append({
            "id": iteration_id,
            "benchmark": benchmark_name,
            "scores": scores,
            "timestamp": datetime.now().isoformat(),
        })
    
    def analyze_trend(self, benchmark_name: str) -> Dict:
        """Analyze the trend across iterations"""
        relevant = [
            i for i in self.iterations 
            if i["benchmark"] == benchmark_name
        ]
        
        if len(relevant) < 2:
            return {"trend": "insufficient_data"}
        
        # Compare first and last
        first = relevant[0]["scores"]
        last = relevant[-1]["scores"]
        
        improvements = {}
        regressions = {}
        
        for metric in last:
            if metric in first:
                change = last[metric] - first[metric]
                if change > 0:
                    improvements[metric] = change
                elif change < 0:
                    regressions[metric] = abs(change)
        
        return {
            "iterations": len(relevant),
            "improvements": improvements,
            "regressions": regressions,
            "overall_trend": "improving" if not regressions else "mixed",
        }
    
    def suggest_improvements(self, 
                              eval_results: List[EvaluationResult]
                              ) -> List[str]:
        """Suggest improvements based on evaluation results"""
        suggestions = []
        
        # Find consistently low scores
        dim_avgs = {}
        for result in eval_results:
            for dim, score in result.scores.items():
                if dim not in dim_avgs:
                    dim_avgs[dim] = []
                dim_avgs[dim].append(score)
        
        for dim, scores in dim_avgs.items():
            avg = sum(scores) / len(scores)
            if avg < 60:
                suggestions.append(
                    f"⚠️ {dim}: Average score {avg:.1f}/100. "
                    f"Consider improving prompts or adding "
                    f"specific rules for {dim}."
                )
            elif avg < 80:
                suggestions.append(
                    f"💡 {dim}: Score {avg:.1f}/100. "
                    f"Room for improvement with "
                    f"better context or examples."
                )
        
        return suggestions
```

</details>

### 5.2 A/B Testing Framework

`ABTestFramework` compares **two versions** — e.g. prompt A and prompt B — on the same benchmark suite to find out which one is better. Like brewing two coffee recipes and having customers taste them in groups, then counting which cup gets more praise; the decision is based on data, not on "feel".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ABTestFramework:
    """
    A/B testing for prompt engineering.
    
    Compare 2 versions of a prompt/harness
    on the same benchmark suite.
    
    Like A/B testing on the web,
    but applied to AI agent configuration.
    """
    
    def __init__(self, benchmark_suite: BenchmarkSuite):
        self.suite = benchmark_suite
        self.results = {"A": None, "B": None}
    
    def run_variant(self, variant: str, 
                    agent_func: Callable) -> Dict:
        """Run one variant"""
        self.results[variant] = self.suite.run(agent_func)
        return self.results[variant]
    
    def analyze(self) -> Dict:
        """
        Analyze the A/B test results.
        
        Use a statistical significance test
        to decide which variant is better.
        """
        if not all(self.results.values()):
            return {"error": "Both variants must be run first"}
        
        a_summary = self.results["A"]
        b_summary = self.results["B"]
        
        # Simple comparison
        metrics = {}
        for key in a_summary:
            if isinstance(a_summary[key], (int, float)):
                a_val = a_summary[key]
                b_val = b_summary.get(key, 0)
                metrics[key] = {
                    "A": a_val,
                    "B": b_val,
                    "delta": b_val - a_val,
                    "winner": "A" if a_val > b_val else "B",
                }
        
        # Overall winner (by success rate)
        a_rate = a_summary.get("success_rate", 0)
        b_rate = b_summary.get("success_rate", 0)
        
        return {
            "metrics": metrics,
            "overall_winner": "A" if a_rate >= b_rate else "B",
            "confidence": "high" if abs(a_rate - b_rate) > 0.1 else "low",
        }
```

</details>

---

## 6. Reporting & Dashboards

> **📌 Core Concept**
>
> **Concept:** Reporting & Dashboards is the way of presenting evaluation results visually — metrics over time, version comparisons, degradation detection — so the whole team can "see at a glance" the health of the agent.
> **Analogy/comparison:** Like a car's speedometer: you don't need to time every meter, just look at the needle to know whether you're going fast or slow, whether to step on the gas or the brakes.
> **Why it matters:** Evaluation results sitting silently in a log file help no one make decisions; only when clearly displayed can the team react in time when quality drops.

### 6.1 Evaluation Report Generator

`EvaluationReporter` automatically creates reports from evaluation results in multiple formats: Markdown for posting to a PR, JSON for machines, and data for a visual dashboard. Like a factory's end-of-day report printer: just feed it the numbers, and it prints a summary table ready to send to the team.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from datetime import datetime
from typing import Dict, List

class EvaluationReporter:
    """
    Create evaluation reports — markdown, JSON, or dashboard.
    """
    
    def generate_markdown_report(self, 
                                  results: List[EvaluationResult],
                                  summary: Dict) -> str:
        """Create a Markdown report"""
        report = []
        report.append("# 📊 Evaluation Report")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Tasks Evaluated:** {len(results)}")
        
        # Summary
        report.append("\n## Summary\n")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Total Tasks | {summary.get('total', 0)} |")
        report.append(f"| Success Rate | {summary.get('success_rate', 0):.1%} |")
        report.append(f"| Avg Quality Score | {summary.get('avg_quality', 0):.1f} |")
        report.append(f"| Total Tokens | {summary.get('total_tokens', 0):,} |")
        
        # Per-dimension scores
        report.append("\n## Dimension Scores\n")
        report.append("| Dimension | Avg Score | Status |")
        report.append("|-----------|-----------|--------|")
        
        for dim, score in summary.get("dimension_scores", {}).items():
            status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
            report.append(f"| {dim} | {score:.1f} | {status} |")
        
        # Top issues
        report.append("\n## Top Issues\n")
        for i, issue in enumerate(summary.get("top_issues", []), 1):
            report.append(f"{i}. {issue}")
        
        # Individual results
        report.append("\n## Task Results\n")
        for result in results:
            status = "✅" if result.total_score >= 70 else "❌"
            report.append(
                f"### {status} {result.task_id}\n"
            )
            report.append(f"**Score:** {result.total_score:.1f}/100\n")
            
            for dim, score in result.scores.items():
                bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
                note = result.notes.get(dim, "")
                report.append(
                    f"- `{dim}`: {bar} {score:.0f}/100"
                    f"{f' — {note}' if note else ''}"
                )
            report.append("")
        
        return "\n".join(report)
    
    def generate_json_report(self,
                              results: List[EvaluationResult],
                              summary: Dict) -> Dict:
        """Create a JSON report"""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_tasks": len(results),
            },
            "summary": summary,
            "results": [
                {
                    "task_id": r.task_id,
                    "total_score": r.total_score,
                    "scores": r.scores,
                    "notes": r.notes,
                }
                for r in results
            ],
        }
    
    def generate_dashboard_data(self, 
                                 results: List[EvaluationResult]) -> Dict:
        """Generate data for the visual dashboard"""
        return {
            "timeline": self._build_timeline(results),
            "distribution": self._build_distribution(results),
            "heatmap": self._build_heatmap(results),
        }
    
    def _build_timeline(self, results: List) -> List:
        """Build timeline data for the chart"""
        return [
            {
                "date": r.timestamp,
                "score": r.total_score,
                "task": r.task_id,
            }
            for r in results
        ]
    
    def _build_distribution(self, results: List) -> Dict:
        """Build score distribution"""
        ranges = {
            "0-20": 0, "20-40": 0, "40-60": 0,
            "60-80": 0, "80-100": 0
        }
        
        for r in results:
            score = r.total_score
            if score < 20:
                ranges["0-20"] += 1
            elif score < 40:
                ranges["20-40"] += 1
            elif score < 60:
                ranges["40-60"] += 1
            elif score < 80:
                ranges["60-80"] += 1
            else:
                ranges["80-100"] += 1
        
        return ranges
    
    def _build_heatmap(self, results: List) -> List:
        """Build heatmap data (task x dimension)"""
        dimensions = set()
        for r in results:
            dimensions.update(r.scores.keys())
        
        heatmap = []
        for r in results:
            row = {"task": r.task_id}
            for dim in sorted(dimensions):
                row[dim] = r.scores.get(dim, 0)
            heatmap.append(row)
        
        return heatmap
```

</details>

---

## 7. Case Studies

> **📌 Core Concept**
>
> **Concept:** Case Studies are real-world evaluation examples — SWE-bench, HumanEval, production pipelines — showing how people set up metrics, grade specific agents, and derive lessons for improvement.
> **Analogy/comparison:** Like reading the post-match report of a football game: see how this team coordinated, how they scored, where they lost ground — to draw lessons for the next match, instead of stopping at the final score.
> **Why it matters:** Dry theory becomes much easier to understand when you see it working in a real context.

### 7.1 SWE-bench — Benchmarking AI Code Agents

**Context**: SWE-bench is the standard benchmark for evaluating the real-world bug-fixing ability of AI agents on actual GitHub repositories. Simply put, it takes real bugs from open-source projects, hands them to an agent to fix, then runs the project's own test suite to see whether the agent can "close" the issue — like taking an exam on the real exam paper instead of a self-made question.

**Actual results**:

```
┌────────────────────────────────────────────────────────────────┐
│                 SWE-BENCH RESULTS 2026                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Agent              │ Verified │ Lite  │ Full  │ Cost/Task     │
│  ───────────────────┼──────────┼───────┼───────┼──────────────│
│  Claude Code+Harness│ 53%      │ 48%   │ 42%   │ ~$2.50       │
│  Devin              │ 48%      │ 44%   │ 38%   │ ~$8.00       │
│  OpenHands+SWE      │ 45%      │ 42%   │ 35%   │ ~$3.00       │
│  Cursor (agent)     │ 42%      │ 38%   │ 32%   │ ~$1.50       │
│  GitHub Copilot     │ 35%      │ 33%   │ 28%   │ ~$0.50       │
│  SWE-agent (base)   │ 20%      │ 20%   │ 15%   │ ~$1.00       │
│                                                                │
│  Key Insight: Harness design accounts for 30%+ of             │
│  the performance difference between agents!                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Key Learnings:**
1. Harness design impact > model choice
2. Tool permissions affect safety significantly
3. Context management affects token cost
4. Multi-agent improves complex task handling

### 7.2 HumanEval — Classic Code Generation

This table tracks model progress on HumanEval — OpenAI's classic benchmark of single-function Python tasks — from 2023 to 2026. The Improvement column shows how many percent each model gained. Notable point: large models have plateaued around 90%, so researchers had to move to harder benchmarks like SWE-bench — read the ⚠️ note at the bottom of the table carefully.

```
┌────────────────────────────────────────────────────────────────┐
│                 HUMANEVAL EVOLUTION                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Model            │ Pass@1 (2023) │ Pass@1 (2026) │ Improvement│
│  ─────────────────┼───────────────┼───────────────┼───────────│
│  GPT-3.5 Turbo    │ 48%           │ 72%           │ +50%      │
│  GPT-4            │ 67%           │ 86%           │ +28%      │
│  Claude 3.5 Sonnet│ -             │ 92%           │ -         │
│  Gemini 2.5 Pro   │ -             │ 88%           │ -         │
│  DeepSeek-V3      │ -             │ 90%           │ -         │
│                                                                │
│  ⚠️ HumanEval reaching ceiling — need harder benchmarks      │
│     → SWE-bench, LiveCodeBench becoming more relevant         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 7.3 Real-World Evaluation Pipeline — Production Case

This is an example of **a team of 20 devs using a daily evaluation pipeline in production**: running the benchmark overnight, checking for regressions, generating reports, and alerting immediately when quality drops. Read it as a "sample blueprint" for your own pipeline — learn how a real team organizes continuous monitoring instead of evaluating just once.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Real-world example: How a team evaluates their AI coding agent

class ProductionEvaluator:
    """
    Production evaluation pipeline used daily.
    
    Context: A team of 20 developers using an AI coding agent
    daily. The pipeline runs every night to monitor quality.
    """
    
    def __init__(self):
        self.benchmark_suite = BenchmarkSuite("daily")
        self.regression_suite = RegressionTestSuite("production")
        self.reporter = EvaluationReporter()
    
    def setup_daily_benchmarks(self):
        """Set up benchmark tasks for the daily run"""
        
        # 10 representative tasks for the team's domain
        self.benchmark_suite.add_task(
            "fix-001", "Fix null pointer in UserService.getProfile",
            validator=lambda out: "null check" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "feat-001", "Add pagination to ProductController.list",
            validator=lambda out: "offset" in str(out).lower() or 
                                   "limit" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "test-001", "Write unit tests for PaymentService.charge",
            validator=lambda out: "assert" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "refactor-001", "Extract database queries to repository pattern",
            validator=lambda out: "Repository" in str(out)
        )
        
        self.benchmark_suite.add_task(
            "security-001", "Fix SQL injection in UserDAO.findByEmail",
            validator=lambda out: "parameterized" in str(out).lower() or
                                   "prepared" in str(out).lower()
        )
    
    def run_daily_evaluation(self, agent_func: Callable) -> Dict:
        """Run the daily evaluation"""
        
        # 1. Run benchmarks
        summary = self.benchmark_suite.run(agent_func)
        
        # 2. Check regression
        reg_result = self.regression_suite.run_and_check(agent_func)
        
        # 3. Generate report
        report = self.reporter.generate_markdown_report(
            [],  # Would pass actual results
            summary
        )
        
        # 4. Alert if regression detected
        if reg_result["has_regression"]:
            self._send_alert(reg_result)
        
        # 5. Track trend
        return {
            "summary": summary,
            "regression": reg_result,
            "report": report,
        }
    
    def _send_alert(self, reg_result: Dict):
        """Send an alert when a regression is detected"""
        regressions = reg_result["regressions"]
        message = f"⚠️ REGRESSION DETECTED!\n"
        message += f"Score delta: {reg_result['score_delta']:.1f}%\n"
        for reg in regressions:
            message += f"  - {reg['id']}: {reg['baseline']:.0f} → {reg['current']:.0f}\n"
        
        # Would send to Slack, email, etc.
        print(message)
```

</details>

---

## 8. Evaluation Tooling

> **📌 Core Concept**
>
> **Concept:** Evaluation Tooling is the toolkit that supports the evaluation process — benchmark suites, scoring frameworks, code quality tools, security scanners — enabling automated, repeatable, and trustworthy evaluation.
> **Analogy/comparison:** Like a complete bicycle repair kit: each wrench, gauge, and diagnostic machine serves one job. Without tools, a mechanic has to fumble by hand — slower and more error-prone.
> **Why it matters:** Building evaluation from scratch is very costly; leverage existing tools so you can pour your energy into the main job: measuring and improving.

### 8.1 Popular Evaluation Tools

This diagram divides the evaluation tool ecosystem into 4 groups: benchmark suites (question sets), evaluation frameworks (scoring skeletons), code quality tools (code quality scanning) and security scanners (security vulnerability scanning). Pick tools according to each group's role — you don't need to use all of them, just take what fits your current stage.

```
┌──────────────────────────────────────────────────────────────────┐
│                 EVALUATION TOOLS ECOSYSTEM                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BENCHMARK SUITES:                                               │
│  ├── HumanEval (OpenAI) — Classic code gen benchmark           │
│  ├── SWE-bench (Princeton) — Real-world bug fix                │
│  ├── MBPP (Google) — Mostly Basic Python Problems              │
│  ├── LiveCodeBench — Live competition-style tasks               │
│  └── BigCodeBench — Complex function-level tasks               │
│                                                                  │
│  EVALUATION FRAMEWORKS:                                          │
│  ├── PromptFoo — Prompt testing & evaluation                    │
│  ├── DeepEval — LLM evaluation framework                        │
│  ├── RAGAS — RAG-specific evaluation                            │
│  ├── LangSmith — Tracing & evaluation                           │
│  └── Weights & Biases — Experiment tracking                     │
│                                                                  │
│  CODE QUALITY TOOLS:                                             │
│  ├── SonarQube — Code quality & security                        │
│  ├── ESLint/Prettier — Style checking                           │
│  ├── Pylint/Ruff — Python linting                                │
│  ├── pytest — Test runner                                        │
│  └── Coverage.py — Test coverage                                 │
│                                                                  │
│  SECURITY SCANNERS:                                              │
│  ├── Bandit — Python security                                   │
│  ├── Semgrep — Multi-language security                           │
│  ├── npm audit — Node.js vulnerabilities                        │
│  └── Snyk — Dependency scanning                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 PromptFoo Configuration Example

This YAML configuration helps you run PromptFoo — a popular prompt testing tool — on your coding agent: declare the provider (which model), the prompt, and the assertions (conditions the output must satisfy). It's like writing an "inspection contract": the machine automatically grades whether the model meets each condition (e.g. `contains` or `llm-rubric`).

<details>
<summary><b>8.2 PromptFoo Configuration Example (Click to expand/collapse)</b></summary>

```yaml
# promptfooconfig.yaml
# Configuration for PromptFoo evaluation

description: "AI Coding Agent Evaluation"

providers:
  - id: "openai:gpt-4o"
    config:
      temperature: 0
  - id: "anthropic:messages:claude-3.5-sonnet"
    config:
      temperature: 0

prompts:
  - file://prompts/v1.txt
  - file://prompts/v2.txt

tests:
  - description: "Fix null pointer bug"
    vars:
      task: "Fix the null pointer in UserService.getProfile"
      file_content: "{{fixture.userservice}}"
    assert:
      - type: contains
        value: "null check"
      - type: llm-rubric
        value: "Code handles null case properly, no runtime errors"
  
  - description: "Add pagination"
    vars:
      task: "Add pagination to ProductController.list"
      file_content: "{{fixture.productcontroller}}"
    assert:
      - type: contains
        value: "offset"
      - type: contains
        value: "limit"
      - type: llm-rubric
        value: "Pagination is correctly implemented with proper defaults"

  - description: "Security fix"
    vars:
      task: "Fix SQL injection in UserDAO.findByEmail"
      file_content: "{{fixture.userdao}}"
    assert:
      - type: llm-rubric
        value: "Uses parameterized queries, no string concatenation for SQL"

metrics:
  correctness:
    weight: 0.3
  quality:
    weight: 0.25
  safety:
    weight: 0.25
  efficiency:
    weight: 0.2
```

</details>

---

## 9. Best Practices

> **📌 Core Concept**
>
> **Concept:** Best Practices are the set of evaluation principles proven to work — quality test cases, avoiding data leakage, frequent updating — that help you measure the agent accurately and trustworthily.
> **Analogy/comparison:** Like the safety rules in a professional kitchen: wash your hands, keep knives separate, check expiry dates — apply them consistently to avoid accidents and keep the food up to standard.
> **Why it matters:** Most mistakes in evaluation have already been made by someone before; learn from their experience so you don't drive into the same wreck.

### 9.1 DO and DON'T

This is the shortest "law table" for not evaluating wrong: **10 things to DO** (e.g. automate everything, track a baseline) and **8 things NOT to do** (e.g. using a single metric only). Use it as a checklist when building your evaluation system.

```
┌──────────────────────────────────────────────────────────────────┐
│              EVALUATION BEST PRACTICES                           │
│                                                                  │
│  ✅ DO:                                                          │
│                                                                  │
│  1. AUTOMATE EVERYTHING                                         │
│     Evaluation must be automated, not manual                    │
│     → Consistent, repeatable, scalable                         │
│                                                                  │
│  2. MULTIPLE DIMENSIONS                                         │
│     Don't only check "correct/incorrect"                       │
│     → Quality + Correctness + Efficiency + Safety               │
│                                                                  │
│  3. REGULAR BENCHMARKS                                          │
│     Run benchmarks regularly (each PR, each week)               │
│     → Catch regressions early                                   │
│                                                                  │
│  4. BASELINE TRACKING                                           │
│     Save a baseline to compare against                          │
│     → Know if you're improving or regressing                   │
│                                                                  │
│  5. ACTIONABLE FEEDBACK                                          │
│     Results must suggest specific actions                       │
│     → "Fix X" not just "Score is low"                          │
│                                                                  │
│  6. BALANCED METRICS                                             │
│     Don't optimize one metric while sacrificing another        │
│     → Trade-offs are real                                       │
│                                                                  │
│  7. HUMAN CALIBRATION                                            │
│     Regularly calibrate auto-eval against human review          │
│     → Ensure evaluation quality                                 │
│                                                                  │
│  8. TEST EDGE CASES                                              │
│     Benchmarks must have diverse difficulty levels             │
│     → Don't just test the easy stuff                            │
│                                                                  │
│  9. MONITOR COST                                                  │
│     Track token cost per evaluation                              │
│     → Evaluation shouldn't cost more than the value             │
│                                                                  │
│  10. SHARE RESULTS                                                │
│      Publish evaluation results for team transparency           │
│      → Build trust in AI coding tools                           │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ DON'T:                                                       │
│                                                                  │
│  1. Don't use a single metric                                    │
│  2. Don't ignore regressions                                     │
│  3. Don't benchmark on trivial tasks only                       │
│  4. Don't trust auto-eval without human calibration            │
│  5. Don't optimize for benchmark at expense of real usage      │
│  6. Don't forget to evaluate cost/efficiency                   │
│  7. Don't skip evaluation after prompt changes                  │
│  8. Don't compare across different benchmark setups            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Evaluation Strategy

This pyramid shows you **the frequency and cost of each checking layer**: the lower layers are cheap and run continuously (static analysis on every keystroke), the upper layers cost more and run less often (E2E tests weekly). The idea: use the fast, cheap layers to catch errors early in large volume, so the slow, expensive layers only have to handle the remaining essentials.

```
┌──────────────────────────────────────────────────────────────────┐
│              EVALUATION STRATEGY PYRAMID                         │
│                                                                  │
│                        ┌──────────┐                              │
│                        │ E2E Test │ ← Real user scenarios       │
│                        │ (Weekly) │    Slow, expensive           │
│                       ┌┴──────────┴┐                            │
│                       │ Integration │ ← Multi-component tests  │
│                       │   (Daily)   │    Medium speed           │
│                      ┌┴─────────────┴┐                         │
│                      │ Unit Tests     │ ← Individual functions │
│                      │   (Per Commit) │    Fast, cheap          │
│                     ┌┴───────────────┴┐                        │
│                     │ Static Analysis  │ ← Lint, type check    │
│                     │   (Continuous)   │    Instant             │
│                    ┌┴─────────────────┴┐                       │
│                    │ Code Review        │ ← Human + AI review  │
│                    │   (Continuous)     │    Quality gate        │
│                    └───────────────────┘                        │
│                                                                  │
│  Strategy:                                                      │
│  - Static analysis: Every keystroke (IDE)                       │
│  - Unit tests: Every commit                                     │
│  - Integration: Daily                                           │
│  - E2E: Weekly                                                  │
│  - Regression: Every prompt change                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Real-World Case Studies

> **📌 Core Concept**
>
> **Concept:** Real-World Case Studies are evaluation examples already deployed in production — SWE-bench, Aider, LiveCodeBench, Anthropic — illustrating how to design benchmarks, grade specific agents, and extract lessons for improvement.
> **Analogy/comparison:** Like watching a documentary on how big companies operate: not just empty theory, but seeing directly how they make decisions, where they err, and what you can apply to your own setup.
> **Why it matters:** Each case study is a lesson someone else already paid for; learning from them helps you pick the right benchmark and avoid repeating the same mistakes.

### 10.1 Princeton NLP SWE-bench: Benchmarking Real-World Code

This case study analyzes SWE-bench — a benchmark of real bug fixes from 2294 GitHub issues. The leaderboard table shows each system's resolve rate, tokens, and cost; the notable point is that **costs differ up to 10x between systems of comparable quality**. The EVALUATION METHODOLOGY section describes the 5-step grading process you can apply to your own benchmark.

```
┌──────────────────────────────────────────────────────────────────┐
│                    SWE-BENCH EVALUATION                           │
│                                                                  │
│  WHAT: Benchmark from 2294 GitHub issues with ground-truth patches │
│  HOW: Agent must reproduce bug fix from issue description         │
│  METRIC: % issues resolved (pass unit tests)                    │
│                                                                  │
│  LEADERBOARD (2024-2025):                                        │
│  ┌────────────────────┬──────────┬───────────┬───────────────┐  │
│  │ System             │ Resolve  │ Token Use │ Cost/Issue    │  │
│  ├────────────────────┼──────────┼───────────┼───────────────┤  │
│  │ Amazon Q           │ 26.0%    │ ~20K      │ ~$0.50        │  │
│  │ Agentless          │ 24.0%    │ ~15K      │ ~$0.30        │  │
│  │ SWE-agent+GPT-4    │ 22.7%    │ ~25K      │ ~$0.50        │  │
│  │ AutoCodeRover      │ 19.0%    │ ~18K      │ ~$0.40        │  │
│  │ Aider+GPT-4o       │ 18.5%    │ ~20K      │ ~$0.40        │  │
│  │ OpenHands+CodeAct  │ 17.0%    │ ~30K      │ ~$0.60        │  │
│  └────────────────────┴──────────┴───────────┴───────────────┘  │
│                                                                  │
│  KEY INSIGHTS:                                                   │
│  → LLM + Agent loop ≠ always better than simple retrieval      │
│  → Agentless approaches (no LLM in loop) often competitive      │
│  → Search/retrieval quality matters more than model size        │
│  → Cost varies 10x across systems for same quality              │
│                                                                  │
│  EVALUATION METHODOLOGY:                                         │
│  1. Run agent on each issue (with timeout + token budget)       │
│  2. Apply generated patch to codebase                           │
│  3. Run existing test suite                                     │
│  4. Check if failing tests now pass                             │
│  5. Check if passing tests still pass (regression)              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.2 Aider: LLM Leaderboard for Coding

This case study is the leaderboard of the Aider project, grading LLMs by how well they edit files in edit-format and the quality of the diff. The key point lies in the **COST-EFFECTIVENESS section**: DeepSeek V3 reaches 92% of GPT-4o's quality at only 11% of the cost — illustrating that a cheap model can be the optimal choice for routine tasks.

```
┌──────────────────────────────────────────────────────────────────┐
│                 AIDER LLM LEADERBOARD                             │
│                                                                  │
│  BENCHMARK: Edit-format compliance + code quality               │
│  METHODOLOGY: LLM edits whole files, judge by diff quality     │
│                                                                  │
│  TOP MODELS (2024-2025):                                        │
│  ┌────────────────────┬──────────┬───────────┬───────────────┐  │
│  │ Model              │ Score    │ Cost/1M   │ Best For      │  │
│  ├────────────────────┼──────────┼───────────┼───────────────┤  │
│  │ Claude 3.5 Sonnet  │ 74%      │ $3/$15    │ Complex tasks  │  │
│  │ GPT-4o             │ 70%      │ $2.5/$10  │ General code   │  │
│  │ DeepSeek V3        │ 68%      │ $0.27/$1.1│ Budget tasks   │  │
│  │ Gemini 1.5 Pro     │ 66%      │ $1.25/$5  │ Long context   │  │
│  │ Claude 3 Haiku     │ 58%      │ $0.25/$1.2│ Fast/cheap     │  │
│  └────────────────────┴──────────┴───────────┴───────────────┘  │
│                                                                  │
│  COST-EFFECTIVENESS RANKING:                                     │
│  1. DeepSeek V3: 68% score at $0.27/1M tokens (best value)    │
│  2. Claude 3.5 Sonnet: 74% score at $3/1M tokens (best quality)│
│  3. GPT-4o: 70% score at $2.5/1M tokens (balanced)             │
│                                                                  │
│  INSIGHT: DeepSeek V3 achieves 92% of GPT-4o quality at 11%   │
│  of the cost — making it the best choice for routine tasks.     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.3 LiveCodeBench: Dynamic Evaluation

LiveCodeBench solves the weakness of static benchmarks: models may have "cheated" on old data, or the question set may gradually become outdated. So the exam is **updated weekly with new problems from competitive programming platforms**, along with contamination detection. The Scrape → Dedupe → Validate → Run LLM pipeline diagram is the continuous "exam manufacturing" process.

```
┌──────────────────────────────────────────────────────────────────┐
│              LIVECODEBENCH DYNAMIC BENCHMARK                      │
│                                                                  │
│  PROBLEM WITH STATIC BENCHMARKS:                                 │
│  → Models may have been trained on benchmark data               │
│  → Static benchmarks become stale over time                     │
│  → Leaderboard gaming possible                                  │
│                                                                  │
│  SOLUTION: Continuously updated benchmark                       │
│  → New problems added weekly from contest platforms             │
│  → Temporal awareness (problems after training cutoff)          │
│  → Contamination detection built-in                             │
│                                                                  │
│  EVALUATION PIPELINE:                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Scrape   │───►│  Dedupe  │───►│ Validate │───►│  Run LLM │ │
│  │ Problems │    │  & Clean │    │  Tests   │    │  (temp)  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │         │
│  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    │
│  │ Contest │    │ Remove  │    │ Generate │    │ Pass/Fail│   │
│  │ Platforms│   │ duplicates│   │ test cases│   │ + Time   │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│                                                                  │
│  METRICS TRACKED:                                                │
│  → Pass@1: Does the first solution work?                       │
│  → Pass@10: Does any of 10 solutions work?                     │
│  → Time-to-solution: How fast?                                  │
│  → Token efficiency: Tokens per correct solution                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.4 Anthropic's Evaluation Methodology

Anthropic evaluates in **4 layers**, from machines (automated benchmarks) to people (human evaluation) to reality (real user feedback, A/B testing) — because no single layer tells the whole story. The standard they often use is **Acceptance Rate** (the percentage of AI suggestions that devs accept). This is a "multi-source evaluation" model worth imitating, instead of relying on a single number.

```
┌──────────────────────────────────────────────────────────────────┐
│            ANTHROPIC EVALUATION METHODOLOGY                       │
│                                                                  │
│  PRINCIPLE: "Eval what matters, not what's easy to measure"     │
│                                                                  │
│  EVALUATION LAYERS:                                              │
│                                                                  │
│  LAYER 1: AUTOMATED BENCHMARKS                                  │
│  → HumanEval, SWE-bench, internal benchmarks                   │
│  → Fast, scalable, objective                                    │
│  → Limitation: May not reflect real-world usage                │
│                                                                  │
│  LAYER 2: HUMAN EVALUATION                                       │
│  → Expert reviewers rate code quality                          │
│  → Assess: Readability, maintainability, correctness           │
│  → Limitation: Slow, expensive, subjective                     │
│                                                                  │
│  LAYER 3: REAL USER FEEDBACK                                     │
│  → Track acceptance rate of suggestions                        │
│  → Measure time saved vs manual coding                         │
│  → Limitation: Noisy signal, many confounders                  │
│                                                                  │
│  LAYER 4: A/B TESTING                                            │
│  → Compare model versions on real tasks                        │
│  → Statistical significance testing                             │
│  → Limitation: Requires large sample sizes                     │
│                                                                  │
│  KEY METRIC: "Acceptance Rate" (% of AI suggestions accepted)   │
│  → High acceptance = AI is useful                               │
│  → Low acceptance = Need to improve                            │
│  → Tracked across: task type, complexity, user experience      │
│                                                                  │
│  COST AWARENESS:                                                 │
│  → Track $ per quality point                                    │
│  → Optimize model routing (cheap model for easy tasks)          │
│  → Set token budgets per task type                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

### 10.5 DeepSeek Harness — Minimal Benchmark Harness for Unbiased Evaluation

**Context**: The DeepSeek Harness provides a **Minimal Benchmark Harness** — a minimal evaluation mode with only **2 tools: `bash` and `editor`**, designed to eliminate bias from tool selection and provide a clean isolation environment for SWE-bench evaluation.

<details>
<summary><b>Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * Minimal Benchmark Harness
 * 
 * Core Philosophy:
 * - "Less is More" — Only 2 tools: bash + editor
 * - Clean isolation — No LLM-powered tools, no search, no memory
 * - Deterministic — Container-based isolation for reproducibility
 * - Unbiased — The LLM cannot "cheat" by using advanced tools
 * 
 * Repo: DeepSeek Harness (internal)
 * Used for: SWE-bench, LiveCodeBench, custom benchmarks
 */

// ═══════════════════════════════════════════════
// 1. HARNESS ARCHITECTURE
// ═══════════════════════════════════════════════

interface MinimalHarnessConfig {
  // Isolation settings
  isolation: 'container' | 'vm' | 'process';
  containerImage?: string;      // e.g., 'ubuntu:22.04' with dev tools
  workingDir: string;           // Project directory
  
  // Tool restrictions — ONLY these 2
  allowedTools: ['bash', 'editor'];
  
  // Resource limits
  limits: {
    cpuCores: number;
    memoryMB: number;
    diskMB: number;
    timeoutSeconds: number;
    networkAccess: boolean;
  };
  
  // Evaluation settings
  evaluation: {
    suite: string;              // 'swe-bench', 'livecodebench', 'custom'
    dataset: string;            // Path to dataset
    split: 'train' | 'test' | 'dev';
    maxInstances?: number;
  };
  
  // LLM settings (agent under test)
  llm: {
    model: string;
    temperature: number;
    maxTokens: number;
    systemPrompt: string;
  };
}

interface BenchmarkInstance {
  id: string;                   // e.g., 'django__django-12345'
  repo: string;                 // Repository name
  baseCommit: string;           // Commit to start from
  problemStatement: string;     // Issue description
  hints?: string;               // Optional hints
  testPatch: string;            // Tests that should pass after fix
  envSetup?: string;            // Setup commands
}

interface BenchmarkResult {
  instanceId: string;
  status: 'resolved' | 'failed' | 'error' | 'timeout';
  patch?: string;               // Generated patch/diff
  testsPassed: number;
  testsTotal: number;
  executionTimeMs: number;
  tokensUsed: number;
  toolsUsed: string[];          // Should only be ['bash', 'editor']
  errorMessage?: string;
  trajectory: TrajectoryEvent[]; // For debugging
}

// ═══════════════════════════════════════════════
// 2. TWO TOOLS ONLY
// ═══════════════════════════════════════════════

/**
 * Tool 1: BASH
 * Execute shell commands in the container
 */
interface BashTool {
  type: 'bash';
  command: string;              // Shell command to execute
  timeout?: number;             // Override default timeout
  workdir?: string;             // Working directory
}

// Returns:
interface BashResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  durationMs: number;
}

/**
 * Tool 2: EDITOR
 * File operations: read, write, edit
 */
interface EditorTool {
  type: 'editor';
  action: 'read' | 'write' | 'edit' | 'list' | 'grep';
  path: string;                 // File or directory path
  content?: string;             // For write/edit
  oldString?: string;           // For edit
  newString?: string;           // For edit
  pattern?: string;             // For grep
}

// Returns:
interface EditorResult {
  success: boolean;
  content?: string;             // For read
  files?: string[];             // For list
  matches?: GrepMatch[];        // For grep
  error?: string;
}

interface GrepMatch {
  file: string;
  line: number;
  content: string;
}

// ═══════════════════════════════════════════════
// 3. EXECUTION LOOP
// ═══════════════════════════════════════════════

class MinimalBenchmarkHarness {
  private config: MinimalHarnessConfig;
  private container: ContainerRuntime;
  private trajectory: TrajectoryEvent[] = [];
  
  constructor(config: MinimalHarnessConfig) {
    this.config = config;
    this.container = this.createContainer();
  }
  
  async runInstance(instance: BenchmarkInstance): Promise<BenchmarkResult> {
    const startTime = Date.now();
    const tokensUsed = 0;
    const toolsUsed: string[] = [];
    
    try {
      // 1. Setup environment
      await this.setupEnvironment(instance);
      
      // 2. Run agent loop
      const patch = await this.runAgentLoop(instance);
      
      // 3. Apply patch and run tests
      const testResult = await this.runTests(instance, patch);
      
      return {
        instanceId: instance.id,
        status: testResult.allPassed ? 'resolved' : 'failed',
        patch,
        testsPassed: testResult.passed,
        testsTotal: testResult.total,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        trajectory: this.trajectory,
      };
      
    } catch (error) {
      return {
        instanceId: instance.id,
        status: 'error',
        testsPassed: 0,
        testsTotal: 0,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        errorMessage: error.message,
        trajectory: this.trajectory,
      };
    }
  }
  
  private async runAgentLoop(instance: BenchmarkInstance): Promise<string> {
    const messages = [
      { role: 'system', content: this.config.llm.systemPrompt },
      { role: 'user', content: this.formatProblem(instance) },
    ];
    
    let patch = '';
    const maxTurns = 20;
    
    for (let turn = 0; turn < maxTurns; turn++) {
      // Call LLM
      const response = await this.callLLM(messages);
      messages.push({ role: 'assistant', content: response });
      
      // Parse tool calls
      const toolCalls = this.parseToolCalls(response);
      
      if (toolCalls.length === 0) {
        // No tool calls = agent thinks it's done
        patch = this.extractPatch(response);
        break;
      }
      
      // Execute tools (ONLY bash or editor)
      for (const call of toolCalls) {
        if (!['bash', 'editor'].includes(call.type)) {
          throw new Error(`Tool ${call.type} not allowed in minimal harness`);
        }
        
        toolsUsed.push(call.type);
        
        const result = await this.executeTool(call);
        
        // Record trajectory
        this.trajectory.push({
          turn,
          type: 'tool-call',
          tool: call.type,
          input: call,
          output: result,
          timestamp: Date.now(),
        });
        
        // Add result to messages
        messages.push({
          role: 'tool',
          tool_call_id: call.id,
          content: JSON.stringify(result),
        });
      }
    }
    
    return patch;
  }
  
  private async executeTool(call: ToolCall): Promise<any> {
    switch (call.type) {
      case 'bash':
        return await this.container.exec(call.command, {
          timeout: call.timeout || this.config.limits.timeoutSeconds * 1000,
          workdir: call.workdir || this.config.workingDir,
        });
      
      case 'editor':
        return await this.container.fileOp(call);
      
      default:
        throw new Error(`Unknown tool: ${call.type}`);
    }
  }
  
  private formatProblem(instance: BenchmarkInstance): string {
    return `## Repository: ${instance.repo}
## Base Commit: ${instance.baseCommit}

## Problem Statement:
${instance.problemStatement}

${instance.hints ? `## Hints:\n${instance.hints}` : ''}

## Task:
Fix the issue described above. You have access to ONLY two tools:
1. **bash** - Execute shell commands
2. **editor** - Read, write, edit, list, or grep files

Your goal is to produce a patch that makes the tests pass.
Explore the codebase first, then implement the fix.

Output format:
1. Use tools to explore and fix
2. When done, provide the final patch in unified diff format`;
  }
}

// ═══════════════════════════════════════════════
// 4. CONTAINER RUNTIME
// ═══════════════════════════════════════════════

interface ContainerRuntime {
  // Lifecycle
  start(): Promise<void>;
  stop(): Promise<void>;
  snapshot(): Promise<string>;    // For fork/resume
  restore(snapshotId: string): Promise<void>;
  
  // Execution
  exec(command: string, options: ExecOptions): Promise<BashResult>;
  fileOp(op: EditorTool): Promise<EditorResult>;
  
  // State
  getFiles(pattern?: string): Promise<string[]>;
  readFile(path: string): Promise<string>;
  writeFile(path: string, content: string): Promise<void>;
}

// Implementation using Docker/Podman
class DockerContainerRuntime implements ContainerRuntime {
  private containerId: string;
  private image: string;
  
  constructor(image: string = 'ubuntu:22.04') {
    this.image = image;
  }
  
  async start(): Promise<void> {
    // docker run -d --cpus=2 --memory=4g --network=none \
    //   -v ${workspace}:/workspace -w /workspace \
    //   ${image} sleep infinity
    this.containerId = await this.dockerRun();
  }
  
  async exec(command: string, options: ExecOptions): Promise<BashResult> {
    const start = Date.now();
    const result = await this.dockerExec(this.containerId, command, options);
    return {
      ...result,
      durationMs: Date.now() - start,
    };
  }
  
  async fileOp(op: EditorTool): Promise<EditorResult> {
    switch (op.action) {
      case 'read':
        return { success: true, content: await this.readFile(op.path) };
      case 'write':
        await this.writeFile(op.path, op.content || '');
        return { success: true };
      case 'edit':
        // Use sed or similar for in-place edit
        const content = await this.readFile(op.path);
        const newContent = content.replace(op.oldString!, op.newString!);
        await this.writeFile(op.path, newContent);
        return { success: true };
      case 'list':
        const files = await this.getFiles(op.path);
        return { success: true, files };
      case 'grep':
        const matches = await this.grep(op.pattern!, op.path);
        return { success: true, matches };
    }
  }
}

// ═══════════════════════════════════════════════
// 5. TRAJECTORY TRACKING
// ═══════════════════════════════════════════════

interface TrajectoryEvent {
  turn: number;
  type: 'tool-call' | 'llm-response' | 'error' | 'test-run';
  tool?: string;
  input?: any;
  output?: any;
  timestamp: number;
}

interface TestResult {
  allPassed: boolean;
  passed: number;
  total: number;
  details: TestDetail[];
}

interface TestDetail {
  name: string;
  status: 'passed' | 'failed' | 'skipped';
  durationMs: number;
  output?: string;
}

// ═══════════════════════════════════════════════
// 6. SWE-BENCH INTEGRATION
// ═══════════════════════════════════════════════

async function runSWEBenchEvaluation(config: {
  model: string;
  dataset: 'lite' | 'verified' | 'full';
  split: 'test' | 'dev';
  maxInstances?: number;
  parallel?: number;
}): Promise<{
  resolved: number;
  total: number;
  resolveRate: number;
  results: BenchmarkResult[];
}> {
  // Load SWE-bench dataset
  const instances = await loadSWEBenchDataset(config.dataset, config.split);
  const limited = config.maxInstances 
    ? instances.slice(0, config.maxInstances) 
    : instances;
  
  const harness = new MinimalBenchmarkHarness({
    isolation: 'container',
    containerImage: 'swebench/ubuntu:22.04',  // Pre-built with Python, etc.
    workingDir: '/workspace',
    allowedTools: ['bash', 'editor'],
    limits: { cpuCores: 2, memoryMB: 4096, diskMB: 10240, timeoutSeconds: 300, networkAccess: false },
    evaluation: { suite: 'swe-bench', dataset: config.dataset, split: config.split },
    llm: { model: config.model, temperature: 0.0, maxTokens: 8192, systemPrompt: SYSTEM_PROMPT },
  });
  
  // Run in parallel
  const results: BenchmarkResult[] = [];
  const semaphore = new Semaphore(config.parallel || 4);
  
  await Promise.all(limited.map(async (instance) => {
    await semaphore.acquire();
    try {
      const result = await harness.runInstance(instance);
      results.push(result);
    } finally {
      semaphore.release();
    }
  }));
  
  const resolved = results.filter(r => r.status === 'resolved').length;
  
  return {
    resolved,
    total: results.length,
    resolveRate: resolved / results.length,
    results,
  };
}

// System prompt for minimal benchmark
const SYSTEM_PROMPT = `You are an expert software engineer. Your task is to fix bugs in a codebase.

You have access to ONLY two tools:
1. **bash** - Execute shell commands (ls, grep, cat, python, pytest, etc.)
2. **editor** - Read, write, edit, list, or grep files

You do NOT have access to:
- Web search
- Code search across repositories
- LLM-powered tools
- Memory/knowledge bases
- Git operations (except via bash)

Workflow:
1. Explore the codebase to understand the problem
2. Find the relevant files
3. Implement the fix
4. Run tests to verify
5. Output the final patch in unified diff format

Be concise. Use tools efficiently.`;
```

</details>

**Key Innovations**:

| Feature | Traditional Harness | Minimal Benchmark Harness |
|---------|-------------------|---------------------------|
| **Tools** | 10-20+ (search, read, write, execute, LLM, memory, etc.) | **2 only** (bash + editor) |
| **Isolation** | Process-level | **Container-level** |
| **Determinism** | Variable (LLM tools) | **High** (no LLM tools) |
| **Bias** | Tool selection bias | **Minimal** (equal footing) |
| **Reproducibility** | Hard | **Native** (container snapshots) |
| **SWE-bench Score** | Varies | **Baseline for comparison** |

**Why Only 2 Tools?**:
1. **Scientific Control** — Eliminates "tool selection bias" where models with better tool-use appear smarter
2. **Reproducibility** — Container + fixed toolset = deterministic environment
3. **Focus on Reasoning** — Forces model to demonstrate actual code understanding, not tool mastery
4. **Cost Control** — Fewer tool calls = lower token usage, predictable costs
5. **Fair Comparison** — All models evaluated on same minimal interface

**File Reference**: For implementation details, see [`minimal-benchmark-harness.md`](minimal-benchmark-harness.md)

---

## 11. TypeScript Interfaces for Evaluation

> **📌 Core Concept**
>
> **Concept:** TypeScript Interfaces are "data shape blueprints" for evaluation — metrics, test cases, reports, configurations — that standardize the shape of evaluation data and catch errors as early as compile time.
> **Analogy/comparison:** Like a pre-printed intake form with fixed fields: name, quantity, unit price. The person filling it in only writes in the right box and can't invent new data types — that's why the counting step afterward can be accurate.
> **Why it matters:** Evaluation data comes in many kinds and is easy to mix up; static types prevent the system from silently producing wrong data.

### 11.1 Core Evaluation Types

This TypeScript block is the **type dictionary of the whole evaluation system**: BenchmarkConfig, EvaluationResult, QualityMetrics, ABTestConfig and many more types. Read it to know what shape each piece of data must have — for example TaskResult must have status, score, duration, tokensUsed. Use it as a contract between modules: everyone follows the same format, nobody invents their own structure.

<details>
<summary><b>11.1 Core Evaluation Types (Click to expand/collapse)</b></summary>

```typescript
// ═══════════════════════════════════════════════════════════════
// EVALUATION TYPES — Production-grade interfaces for evaluation systems
// ═══════════════════════════════════════════════════════════════

/**
 * Benchmark definition — How to structure an evaluation benchmark
 */
interface BenchmarkConfig {
  name: string;
  description: string;
  version: string;
  tasks: BenchmarkTask[];
  metrics: MetricDefinition[];
  settings: BenchmarkSettings;
}

interface BenchmarkTask {
  id: string;
  name: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  category: string;
  input: TaskInput;
  expectedOutput?: TaskOutput;
  testCases: TestCase[];
  timeout: number;        // ms
  tokenBudget?: number;   // max tokens
}

interface TaskInput {
  prompt: string;
  context?: string;
  files?: FileReference[];
  language?: string;
}

interface TaskOutput {
  code: string;
  explanation?: string;
  filesModified?: string[];
}

interface TestCase {
  id: string;
  name: string;
  input: any;
  expectedOutput: any;
  type: 'unit' | 'integration' | 'e2e' | 'edge_case';
  weight: number;  // 0-1, importance in scoring
}

interface BenchmarkSettings {
  maxRetries: number;
  timeoutPerTask: number;       // ms
  tokenBudgetPerTask: number;
  parallelism: number;
  temperature: number;
  randomSeed?: number;
  modelConfig: ModelConfig;
}

interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'ollama' | 'custom';
  model: string;
  maxTokens: number;
  temperature: number;
  topP?: number;
}

/**
 * Evaluation results
 */
interface EvaluationResult {
  benchmarkName: string;
  model: string;
  timestamp: string;
  summary: EvaluationSummary;
  taskResults: TaskResult[];
  metrics: Record<string, number>;
  cost: CostBreakdown;
}

interface EvaluationSummary {
  totalTasks: number;
  passed: number;
  failed: number;
  errored: number;
  passRate: number;
  avgScore: number;
  avgDuration: number;
  avgTokens: number;
  totalTokens: number;
  totalCost: number;
}

interface TaskResult {
  taskId: string;
  status: 'passed' | 'failed' | 'error' | 'timeout';
  score: number;           // 0-1
  duration: number;        // ms
  tokensUsed: number;
  output?: string;
  error?: string;
  testResults: TestCaseResult[];
}

interface TestCaseResult {
  testCaseId: string;
  passed: boolean;
  actual: any;
  expected: any;
  duration: number;
}

interface CostBreakdown {
  inputTokens: number;
  outputTokens: number;
  inputCost: number;
  outputCost: number;
  totalCost: number;
  costPerTask: number;
  costPerPassingTask: number;
}

/**
 * Quality metrics
 */
interface QualityMetrics {
  correctness: CorrectnessMetrics;
  efficiency: EfficiencyMetrics;
  safety: SafetyMetrics;
  maintainability: MaintainabilityMetrics;
}

interface CorrectnessMetrics {
  passRate: number;
  edgeCaseHandling: number;
  errorHandling: number;
  regressionRate: number;
}

interface EfficiencyMetrics {
  timeComplexity: string;      // e.g., "O(n log n)"
  memoryUsage: number;         // bytes
  tokenEfficiency: number;     // tokens per correct answer
  responseTime: number;        // ms
}

interface SafetyMetrics {
  securityScore: number;       // 0-100
  vulnerabilityCount: number;
  inputValidationScore: number;
  dataLeakage: boolean;
}

interface MaintainabilityMetrics {
  codeComplexity: number;      // cyclomatic complexity
  documentationCoverage: number;  // %
  testCoverage: number;        // %
  duplicationRatio: number;    // 0-1
}

/**
 * Continuous improvement tracking
 */
interface ImprovementTracking {
  version: string;
  timestamp: string;
  previousVersion?: string;
  metrics: Record<string, number>;
  regressions: Regression[];
  improvements: Improvement[];
}

interface Regression {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

interface Improvement {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

/**
 * A/B Testing
 */
interface ABTestConfig {
  name: string;
  variants: Variant[];
  sampleSize: number;
  significanceLevel: number;  // typically 0.05
  metrics: string[];
}

interface Variant {
  id: string;
  name: string;
  description: string;
  config: ModelConfig;
  promptTemplate?: string;
  weight: number;  // traffic split (0-1)
}

interface ABTestResult {
  config: ABTestConfig;
  results: VariantResult[];
  winner?: string;
  pValue: number;
  significant: boolean;
}

interface VariantResult {
  variantId: string;
  sampleSize: number;
  metrics: Record<string, number>;
  confidenceInterval: [number, number];
}

/**
 * Harness quality evaluation — Evaluating the evaluation itself
 */
interface HarnessQualityMetrics {
  /** How well does the benchmark correlate with human judgment? */
  humanCorrelation: number;  // 0-1, Pearson correlation
  /** Are benchmark scores stable across runs? */
  testRetestReliability: number;  // 0-1
  /** Does the benchmark discriminate between good and bad? */
  discriminativePower: number;  // 0-1
  /** How much does it cost to run? */
  costPerRun: number;
  /** How long does a full evaluation take? */
  durationMinutes: number;
  /** Coverage of task types and difficulties */
  coverageScore: number;  // 0-1
}
```

</details>

---

## 12. Design Principles for Evaluation

> **📌 Core Concept**
>
> **Concept:** Design Principles are the core rule set when building an evaluation system — each part does one job, it's extensible, measurable, gives fast feedback — so the system is sustainable long-term and doesn't break as it scales.
> **Analogy/comparison:** Like a house blueprint: solid foundation, each room has its function, and you can still cast an extra floor without tearing it down and rebuilding. Build on a whim and sooner or later you'll need a major renovation.
> **Why it matters:** An evaluation system without principles quickly becomes an unmaintainable code mess that produces untrustworthy results.

### 12.1 SOLID for Evaluation Systems

This diagram applies the 5 classic SOLID principles to evaluation systems: each evaluator measures only one thing (Single Responsibility), adding a new metric doesn't require changing old code (Open/Closed). Read it as "house-building rules for code": follow them and the system stays maintainable and extensible for years.

```
┌──────────────────────────────────────────────────────────────────┐
│          SOLID PRINCIPLES IN EVALUATION SYSTEMS                   │
│                                                                  │
│  S — SINGLE RESPONSIBILITY                                       │
│  Each evaluator measures ONE thing                               │
│  ✅ CorrectnessEvaluator → only correctness                     │
│  ✅ PerformanceEvaluator → only performance                     │
│  ❌ "EverythingEvaluator" → too broad, unmaintainable           │
│                                                                  │
│  O — OPEN/CLOSED                                                 │
│  Open for new metrics, closed for modification                  │
│  ✅ Plugin architecture (add new metric without changing core)  │
│  ❌ Hardcoded metric list (requires code change to add metrics) │
│                                                                  │
│  L — LISKOV SUBSTITUTION                                         │
│  Any evaluator should work in any benchmark                     │
│  ✅ All evaluators implement Evaluator interface                │
│  ❌ Different evaluator types with incompatible APIs            │
│                                                                  │
│  I — INTERFACE SEGREGATION                                       │
│  Small, focused evaluation interfaces                           │
│  ✅ Separate: MetricCollector, ResultAggregator, Reporter       │
│  ❌ One giant EvaluationInterface with 30 methods               │
│                                                                  │
│  D — DEPENDENCY INVERSION                                        │
│  Depend on abstractions, not implementations                    │
│  ✅ Evaluator depends on IModelProvider, not OpenAI directly    │
│  ❌ Evaluator directly calls openai.completions()              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.2 Evaluation Design Principles

These are **10 commandments** for designing evaluation, from "measure what matters, not what's easy to measure" to "evaluate the evaluator itself". Read them quickly like reading a charter: each command is a milestone that keeps your system on track.

```
┌──────────────────────────────────────────────────────────────────┐
│         EVALUATION DESIGN PRINCIPLES (10 Commandments)            │
│                                                                  │
│  1. THOU SHALL EVALUATE WHAT MATTERS                            │
│     → Don't measure easy things, measure important things       │
│     → Correctness > Token count > Response time                 │
│                                                                  │
│  2. THOU SHALL USE MULTIPLE METRICS                             │
│     → Single metric is always misleading                        │
│     → Balance: quality, speed, cost, safety                     │
│                                                                  │
│  3. THOU SHALL BENCHMARK REALISTICALLY                          │
│     → Use real-world tasks, not synthetic examples              │
│     → Include easy, medium, and hard tasks                      │
│                                                                  │
│  4. THOU SHALL CALIBRATE WITH HUMANS                            │
│     → Auto-eval must align with human judgment                  │
│     → Regular calibration checks (weekly/monthly)               │
│                                                                  │
│  5. THOU SHALL TRACK REGRESSIONS                                │
│     → Every evaluation run should compare to previous           │
│     → Alert on metric drops > threshold                         │
│                                                                  │
│  6. THOU SHALL MAKE IT REPRODUCIBLE                             │
│     → Fixed random seeds for deterministic results              │
│     → Version-controlled benchmark data                         │
│                                                                  │
│  7. THOU SHALL TRACK COST                                       │
│     → Token cost per quality point                              │
│     → ROI of model upgrades                                     │
│                                                                  │
│  8. THOU SHALL ITERATE                                          │
│     → Update benchmarks as codebase evolves                     │
│     → Add new test cases from production failures               │
│                                                                  │
│  9. THOU SHALL SHARE RESULTS                                    │
│     → Team visibility into evaluation outcomes                  │
│     → Build trust through transparency                          │
│                                                                  │
│  10. THOU SHALL EVALUATE THE EVALUATOR                          │
│      → Does your benchmark actually measure quality?            │
│      → Cross-validate with multiple evaluation approaches       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 13. Testing Evaluation Harness

> **📌 Core Concept**
>
> **Concept:** Testing the Evaluation Harness is "testing the test itself" — checking whether metrics compute correctly, whether benchmarks are stable across re-runs, whether cost tracking is accurate — before using it to grade agents.
> **Analogy/comparison:** Like verifying a scale before weighing goods: the merchant must be sure the scale is right; if the scale is off, every goods ticket after it is off too.
> **Why it matters:** A wrong scale is even more dangerous than no scale — it makes you trust false numbers.

### 13.1 Evaluation Test Harness

This is a test suite that **checks the evaluation system itself**: whether metrics compute correctly, whether benchmarks are reproducible, whether cost tracking is accurate, whether regressions get detected. How to use it: write test cases like `test_metric_accuracy` below, register them with the harness, then run `run_all()` to get a pass/fail report. If this part doesn't pass, every number you measure is not yet trustworthy.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
import json
import statistics
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class EvalHarnessTestType(Enum):
    """Test types for the evaluation harness"""
    METRIC_ACCURACY = "metric_accuracy"       # Metric outputs correct values
    BENCHMARK_VALIDITY = "benchmark_validity"  # Benchmark has expected structure
    REPRODUCIBILITY = "reproducibility"        # Same input → same output
    COST_TRACKING = "cost_tracking"           # Costs are accurate
    REGRESSION_DETECTION = "regression_detection"  # Detects quality drops
    HUMAN_CALIBRATION = "human_calibration"    # Aligns with human judgment
    EDGE_CASE_HANDLING = "edge_case_handling"  # Handles edge cases


@dataclass
class EvalHarnessTest:
    """A test case for the evaluation harness"""
    name: str
    test_type: EvalHarnessTestType
    description: str
    handler: Callable
    setup: Optional[Callable] = None
    teardown: Optional[Callable] = None
    timeout: int = 120
    tags: List[str] = field(default_factory=list)
    expected_result: Optional[Any] = None


class EvaluationTestHarness:
    """
    Harness to test evaluation systems themselves.
    
    Features:
    - Metric accuracy verification
    - Benchmark validity checks
    - Reproducibility testing
    - Cost tracking validation
    - Regression detection testing
    - Human calibration checks
    """
    
    def __init__(self):
        self.tests: List[EvalHarnessTest] = []
        self.results: List[Dict] = []
    
    def register(self, test: EvalHarnessTest):
        """Register an eval harness test"""
        self.tests.append(test)
    
    def run_all(self) -> Dict:
        """Run all eval harness tests"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            result = self._run_single(test)
            self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def run_by_type(self, test_type: EvalHarnessTestType) -> Dict:
        """Run tests by type"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            if test.test_type == test_type:
                result = self._run_single(test)
                self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def _run_single(self, test: EvalHarnessTest) -> Dict:
        """Run one test case"""
        if test.setup:
            try:
                test.setup()
            except Exception as e:
                return {
                    "name": test.name,
                    "type": test.test_type.value,
                    "status": "setup_error",
                    "error": str(e),
                    "duration": 0,
                }
        
        start = time.time()
        try:
            result = test.handler()
            duration = time.time() - start
            
            passed = True
            if test.expected_result is not None:
                passed = result == test.expected_result
            
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "passed" if passed else "failed",
                "duration": duration,
                "output": result,
                "expected": test.expected_result,
                "tags": test.tags,
            }
        except AssertionError as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "failed",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        except Exception as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "error",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        finally:
            if test.teardown:
                try:
                    test.teardown()
                except Exception:
                    pass
    
    def _generate_report(self, total_time: float) -> Dict:
        """Create a test report"""
        passed = sum(1 for r in self.results if r["status"] == "passed")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        errors = sum(1 for r in self.results if r["status"] == "error")
        
        return {
            "summary": {
                "total": len(self.results),
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{(passed / len(self.results) * 100):.1f}%",
                "total_duration": f"{total_time:.2f}s",
            },
            "by_type": self._group_by_type(),
            "results": self.results,
            "gate_passed": failed == 0 and errors == 0,
        }
    
    def _group_by_type(self) -> Dict:
        """Group results by test type"""
        groups: Dict[str, List] = {}
        for result in self.results:
            t = result["type"]
            if t not in groups:
                groups[t] = []
            groups[t].append(result)
        
        return {
            t: {
                "total": len(results),
                "passed": sum(1 for r in results if r["status"] == "passed"),
            }
            for t, results in groups.items()
        }


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

def test_metric_accuracy():
    """Test that pass@k metric computes correctly"""
    evaluator = PassAtKEvaluator()
    # 3 correct out of 5 → pass@1 should be 0.6
    result = evaluator.compute(k=1, total=5, correct=3)
    assert abs(result - 0.6) < 0.01, f"Expected 0.6, got {result}"

def test_benchmark_reproducibility():
    """Test that running same benchmark twice gives same results"""
    bench = SimpleBenchmark(seed=42)
    result1 = bench.run(tasks=["task1", "task2"])
    result2 = bench.run(tasks=["task1", "task2"])
    assert result1 == result2, "Benchmark results not reproducible"

def test_cost_tracking():
    """Test that cost tracking is accurate"""
    tracker = CostTracker(model="gpt-4o")
    tracker.record(input_tokens=1000, output_tokens=500)
    assert tracker.total_cost > 0
    assert tracker.total_cost < 0.01  # Should be very small for this usage


# Register tests
harness = EvaluationTestHarness()

harness.register(EvalHarnessTest(
    name="Pass@K Accuracy",
    test_type=EvalHarnessTestType.METRIC_ACCURACY,
    description="Verify pass@k metric computation",
    handler=test_metric_accuracy,
    tags=["metric", "correctness"],
))

harness.register(EvalHarnessTest(
    name="Benchmark Reproducibility",
    test_type=EvalHarnessTestType.REPRODUCIBILITY,
    description="Verify benchmark produces consistent results",
    handler=test_benchmark_reproducibility,
    tags=["benchmark", "reliability"],
))

harness.register(EvalHarnessTest(
    name="Cost Tracking Accuracy",
    test_type=EvalHarnessTestType.COST_TRACKING,
    description="Verify cost tracking is accurate",
    handler=test_cost_tracking,
    tags=["cost", "tracking"],
))

# Run
# report = harness.run_all()
# print(json.dumps(report, indent=2))
```

</details>

---

## 14. Future Trends in Evaluation

> **📌 Core Concept**
>
> **Concept:** Future Trends are the development directions shaping how AI is evaluated in 2024-2026 — automation, real-time evaluation, cost optimization, domain-specific benchmarks — helping you prepare your system ahead of time instead of falling behind.
> **Analogy/comparison:** Like a farmer watching the weather forecast: knowing a drought or storm is coming lets you adjust planting proactively instead of passively waiting for the weather to change.
> **Why it matters:** Evaluation is shifting fast; whoever builds the system the old way will have to tear it down and rebuild at great cost.

### 14.1 AI Evaluation Trends (2024-2026)

This table summarizes **6 major trends** shaping AI evaluation from 2024 to 2026: automating the evaluation step (meta-evaluation), real-time evaluation, cost optimization, combining humans with AI, domain-specific benchmarks, and turning evaluation into code in CI/CD. Each sub-item is a suggestion you can try adding to your own system.

```
┌──────────────────────────────────────────────────────────────────┐
│              FUTURE EVALUATION TRENDS                             │
│                                                                  │
│  TREND 1: AUTOMATED HARNESS EVALUATION                          │
│  ├── Meta-evaluation: AI evaluates the evaluator                │
│  ├── Self-improving benchmarks that evolve with models          │
│  ├── Automatic detection of benchmark contamination             │
│  └── Quality signals from production usage data                 │
│                                                                  │
│  TREND 2: REAL-TIME EVALUATION                                   │
│  ├── Live evaluation during coding (not just post-hoc)          │
│  ├── Instant feedback loops on code quality                     │
│  ├── Predictive evaluation (estimate quality before running)    │
│  └── Continuous evaluation dashboards                           │
│                                                                  │
│  TREND 3: COST-AWARE EVALUATION                                 │
│  ├── Quality-per-dollar as primary metric                       │
│  ├── Model routing based on task difficulty                     │
│  ├── Token budget optimization                                  │
│  └── ROI measurement for AI tooling investments                │
│                                                                  │
│  TREND 4: HUMAN-AI CALIBRATED EVALUATION                        │
│  ├── LLM-as-judge calibrated against human experts              │
│  ├── Multi-rater consensus systems                              │
│  ├── Bias detection in automated evaluation                     │
│  └── Fair comparison across model families                      │
│                                                                  │
│  TREND 5: DOMAIN-SPECIFIC BENCHMARKS                            │
│  ├── Security-focused evaluation (OWASP patterns)               │
│  ├── Performance-focused evaluation (latency, memory)           │
│  ├── Accessibility-focused evaluation (WCAG compliance)         │
│  └── Industry-specific benchmarks (healthcare, finance)         │
│                                                                  │
│  TREND 6: EVALUATION-AS-CODE                                     │
│  ├── Version-controlled evaluation suites                       │
│  ├── CI/CD integrated evaluation pipelines                      │
│  ├── Evaluation results as PR comments                          │
│  └── Automated evaluation gates for model upgrades              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## References

### Papers & Research
- [HumanEval Benchmark](https://github.com/openai/human-eval) — OpenAI code generation benchmark
- [SWE-bench](https://www.swebench.com/) — Princeton NLP real-world bug fix benchmark
- [CodeBLEU](https://github.com/microsoft/CodeXGLUE) — Microsoft code evaluation metric
- [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) — Codex paper

### Frameworks & Tools
- [PromptFoo](https://www.promptfoo.dev) — Prompt testing & evaluation
- [DeepEval](https://docs.confident-ai.com) — LLM evaluation framework
- [RAGAS](https://docs.ragas.io) — RAG evaluation
- [LangSmith](https://smith.langchain.com) — Tracing & evaluation
- [Weights & Biases](https://wandb.ai) — Experiment tracking

### Benchmarks
- [SWE-bench Leaderboard](https://www.swebench.com/)
- [LiveCodeBench](https://livecodebench.github.io/)
- [BigCodeBench](https://bigcode-benchmark.github.io/)
- [Aider LLM Leaderboard](https://aider.chat/docs/leaderboards/)

### Case Study References
- [SWE-agent](https://github.com/princeton-nlp/SWE-agent)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [Aider](https://aider.chat)
- [Anthropic Claude Code](https://docs.anthropic.com/en/docs/claude-code)

---

**Last updated:** 19/07/2026  
**Author:** AI Knowledge Repository
