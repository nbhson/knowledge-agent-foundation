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

This opening explains, with one picture, why evaluation matters before we go into the "how".

You build a new bridge. You can say *"It looks fine"*, but without **measuring the load, testing the materials, stress-testing with heavy trucks** — you won't know whether the bridge will hold for 10 years of use or collapse after 1 month.

**AI code is the same.** Writing code without evaluating it = **shipping a bridge without inspecting it**. Here, "evaluating" means testing and measuring the code *before* you trust it — not just glancing at it.

When you use AI to generate code, the most important question is not *"Does the code run?"* but: *"Is the code correct? Is it safe? Is it maintainable? Is it better than writing it by hand?"* — and you need a **proper evaluation system** to answer. (Maintainable = easy for the next developer — or the next agent — to read, fix, and extend without breaking things.)

**The solution**: a Multi-level Evaluation Framework — from functional correctness to business value, ensuring every line of AI-generated code **meets the standard before it reaches the user**.

> **One-line summary:** Never ship AI-generated code on a "looks fine" feeling — measure correctness, safety, and value with a proper evaluation system first.

### Why Is Evaluation Important?

> *"If you can't measure it, you can't improve it. And if you can't improve it, you're falling behind."*

#### 3 Scientific Pieces of Evidence

How to read it: each row is one research result; the **Key Finding** column is the one number worth remembering. For example, row 3 says Microsoft found that AI code written *without* evaluation added 28% more technical debt in 6 months (technical debt = messy shortcuts in code that make every future change slower and costlier).

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **SWE-bench (Princeton, 2025)** | Top models resolve **44% of real GitHub issues** — but **only when evaluated the right way** do you learn which model is actually good for a specific use case |
| 2 | **Google Research (2024)** | Teams with systematic evaluation pipelines caught **3× more regressions** before reaching production |
| 3 | **Microsoft (2025)** | AI code generation without evaluation increased **technical debt by 28%** in 6 months |

#### Core philosophy:

```
Evaluation = What You Measure → What You Improve → What You Ship
```

**5 Levels of Evaluation** (read it as a ladder: each level assumes the one below it already passes):
- **Level 1**: Code works (functional correctness — it does the job on the happy path)
- **Level 2**: Code is correct (edge cases = unusual situations like empty lists, year 0, or filenames with spaces; plus error handling)
- **Level 3**: Code is good (readability, maintainability)
- **Level 4**: Code is safe (security, performance)
- **Level 5**: Code adds value (business impact, user satisfaction)

**Analogies**: Evaluation is like a quality-control system in a factory — not just checking whether the product is broken (Level 1), but also whether the finish is nice (Level 3), whether the materials are safe (Level 4), and whether the customer is happy (Level 5).

**If you skip it**: you ship code without really knowing how good it is, you miss regressions when they appear, you can't tell which model is better, and tech debt quietly grows until fixing it costs about 10× more. (Regression = something that used to work but broke after a change.)

> **One-line summary:** Evaluation is the quality-control line for AI code — without it you ship blind, miss breakages, and pay 10× to fix the mess later.

## Overview

This section defines what "evaluation" means in this document and shows the big picture in one diagram.

**Evaluation** in AI coding means **checking how well** an AI agent does coding work. That includes running benchmarks, collecting simple metrics, and using what you learn to keep making the agent better. (Benchmark = a fixed, public set of test tasks used to score systems fairly. Metrics = the numbers you track, e.g. "% of tasks solved".)

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

How to read the diagram: follow the arrows — tasks go in, the agent runs, code comes out, metrics grade the code, results get analyzed, and improvements feed back into the next round. It is a loop, not a one-off check.

> **One-line summary:** Evaluation is a closed loop — run the agent, grade the output, analyze, improve, repeat.

## Contents

How to read it: the **#** column is the section number in this file; click the topic to jump there. For instance, row 4 covers the automated evaluation framework — prebuilt pipelines that run all the checks for you.

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

> **One-line summary:** This file walks from "what to measure" (sections 1–3) through "how to measure it" (4–8) to "how to do it well" (9+).

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

Example of the difference between dimensions: code that computes an average correctly (correctness) but takes 10 seconds instead of 10 milliseconds (efficiency) and writes passwords to a log file (safety). One piece of code, three different verdicts.

> **One-line summary:** Grade an agent on 9 separate facets — correctness, quality, efficiency, safety, completeness, speed, usability, cost, reliability — because a single number hides too much.

### 1.2 Evaluation Rubric

This code defines the **scoring rubric** — the set of criteria spelling out what a 5, a 3, or a 1 means for each evaluation dimension. Like grading criteria for an exam: with clear descriptions, grading is fair and consistent across runs. You can try it to see a result accumulated with weights into a total 0-100 score.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-2-evaluation-rubric.py`](examples/01-1-2-evaluation-rubric.py)

</details>

> **One-line summary:** A rubric pins down exactly what a 5, 3, or 1 means per dimension, so scores are fair and comparable across runs.

### 1.3 Weight Configuration — Depending on Use Case

The code here shows the same set of evaluation dimensions, but **the weights change with the goal** — like a university exam weighted toward the sciences, while a vocational school weighs hands-on skill more. Where safety matters, raise the `safety` weight; where fast delivery matters, raise `completeness`. Tune `WEIGHT_CONFIGS` to match your use case.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-1-3-weight-configuration-depending-on-use-case.py`](examples/02-1-3-weight-configuration-depending-on-use-case.py)

</details>

(For orientation: `safety` = weight given to security and error handling; `completeness` = weight given to whether the task is fully finished with nothing missing.)

> **One-line summary:** Same dimensions, different weights per use case — raise `safety` for risky domains, raise `completeness` when fast full delivery matters.

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

> 📄 **Example code:** [`examples/03-2-1-code-quality-metrics.py`](examples/03-2-1-code-quality-metrics.py)

</details>

(Quick gloss of the terms: **cyclomatic complexity** = how many separate paths the code can take — more paths, harder to test; **maintainability index** = a 0–100 estimate of how easy the code is to change; **docstring** = the explanatory text written inside a function describing what it does.)

> **One-line summary:** An auto-grader scores complexity, maintainability, naming, and docs, then rolls them into one 0–100 number.

### 2.2 AI Agent Quality Metrics

This part measures **the entire generation process of the AI agent**, not just the result: first-attempt success rate, number of retries, tokens consumed, rate of not breaking existing functionality. A good agent usually gets it right early, retries little, and spends few tokens — like an employee who knows the job and doesn't ask the boss over and over.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-2-2-ai-agent-quality-metrics.py`](examples/04-2-2-ai-agent-quality-metrics.py)

</details>

> **One-line summary:** Grade the agent's *process* too — first-try success, retries, tokens spent, and whether it broke existing features — not just the final code.

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

How to read it: each line is one metric, the bar shows the score, and the indented `└─` lines are sub-metrics under their parent group. COMPOSITE SCORE = the weighted total of everything above.

> **One-line summary:** A dashboard turns all metrics into one screen of bars — long bar = strong area, short bar = where to improve next.

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

> 📄 **Example code:** [`examples/05-3-1-benchmark-framework.py`](examples/05-3-1-benchmark-framework.py)

</details>

> **One-line summary:** `BenchmarkSuite` is the referee's pitch — add tasks, run the agent, tally success rate, tokens, and time, with no "I feel like I played well" stories.

### 3.2 Standard Benchmark Tasks

This list is a **sample question set**, organized by difficulty from trivial to complex: write hello world, reverse a string, fix an off-by-one bug, refactor a class. Each task ships with a validator for automated grading. Use it like a practice exam set: start easy to check that the agent even works, then ramp up the difficulty to measure real capability.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-3-2-standard-benchmark-tasks.py`](examples/06-3-2-standard-benchmark-tasks.py)

</details>

> **One-line summary:** A graded practice exam set — easy tasks first to confirm the agent works, then harder ones to measure real capability; a validator grades each task automatically.

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

Quick gloss of the terms: **Pass@1** = the model solves the task on its first try; **Pass@10** = at least one of 10 tries works; **Resolved** (SWE-bench) = the agent actually fixed the real bug and the project's tests pass; **Harness** = the tooling around a model (tools, prompts, loop) that lets it act.

> **One-line summary:** No model wins everywhere — 92% on HumanEval but 53% on SWE-bench is normal, because writing a fresh function and fixing a bug in a real repo are different skills.

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

> 📄 **Example code:** [`examples/07-4-1-auto-evaluation-pipeline.py`](examples/07-4-1-auto-evaluation-pipeline.py)

</details>

(A **pipeline** = a fixed chain of steps that runs automatically, one after another. Lint = a tool that flags style and bug-prone patterns in code, e.g. an unused variable.)

> **One-line summary:** `EvaluationPipeline` runs all your checks — lint, tests, security — automatically and aggregates them into one weighted score.

### 4.2 LLM-as-Judge Evaluation

This is the approach of **using a powerful LLM (GPT-4, Claude) as the "examiner"** to grade code produced by another LLM. It's like asking an experienced senior engineer to read the code, score it, and explain why — it handles fuzzy things like readability and design well, which automated graders struggle with. But remember: the examiner can be biased and hallucinate too, so use it in combination with automated tests; don't trust it blindly.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-4-2-llm-as-judge-evaluation.py`](examples/08-4-2-llm-as-judge-evaluation.py)

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

(The block above is the judge's prompt template: `{context}` is where the code under review gets inserted, and the judge must answer as JSON — score plus a one-sentence reason per dimension.)

> **One-line summary:** Let a strong LLM grade fuzzy things like readability — but always pair it with automated tests, because the judge itself can be biased or wrong.

### 4.3 Regression Testing Framework

Regression testing answers the question: **after changing the prompt or the harness, does the agent "forget" how to do things correctly?** The method: store a "model answer" (golden answer) for each task, re-run and compare against the baseline; if the score drops more than 10%, flag a REGRESSION. Like a teacher who keeps students' old exams and occasionally has them retake one, to make sure they haven't "learned the front and forgotten the back".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-4-3-regression-testing-framework.py`](examples/09-4-3-regression-testing-framework.py)

</details>

> **One-line summary:** Keep a golden answer per task, re-run after every prompt or harness change, and flag a REGRESSION when the score drops more than 10%.

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

> 📄 **Example code:** [`examples/10-5-1-improvement-loop.py`](examples/10-5-1-improvement-loop.py)

</details>

> **One-line summary:** Run the 5-step loop — measure, analyze, identify the top 3 issues, fix, verify — once per week or per sprint.

### 5.2 A/B Testing Framework

`ABTestFramework` compares **two versions** — e.g. prompt A and prompt B — on the same benchmark suite to find out which one is better. Like brewing two coffee recipes and having customers taste them in groups, then counting which cup gets more praise; the decision is based on data, not on "feel".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/11-5-2-a-b-testing-framework.py`](examples/11-5-2-a-b-testing-framework.py)

</details>

(A/B test = showing two variants to comparable groups and picking the winner by measured results, not opinion.)

> **One-line summary:** `ABTestFramework` races two versions on the same benchmark and picks the winner with data, not feel.

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

> 📄 **Example code:** [`examples/12-6-1-evaluation-report-generator.py`](examples/12-6-1-evaluation-report-generator.py)

</details>

> **One-line summary:** `EvaluationReporter` feeds on evaluation results and prints ready-to-send reports — Markdown for PRs, JSON for machines, data for dashboards.

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

How to read it: each row is one agent product; **Verified / Lite / Full** are the three SWE-bench difficulty tiers, and **Cost/Task** is the average spend per solved task. For instance, Claude Code+Harness solves 53% of the Verified tier at about $2.50 per task.

**Key Learnings:**
1. Harness design impact > model choice (the tooling around a model can matter more than the model itself)
2. Tool permissions affect safety significantly (which tools the agent may run, e.g. file writes or shell commands)
3. Context management affects token cost (tokens = billed text units; wasted context = wasted money)
4. Multi-agent improves complex task handling (several cooperating agents, each with a sub-job)

> **One-line summary:** On SWE-bench, the harness you build matters more than the model you pick — the same model can swing results by 30%+.

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

How to read it: **Pass@1 (2023)** is the first-try solve rate back then, **Pass@1 (2026)** is today's, and **Improvement** is the relative gain (e.g. GPT-3.5 went from 48% to 72%, which is a 50% relative jump). A `-` means the model didn't exist yet in 2023.

> **One-line summary:** HumanEval is nearly maxed out (models sit around 90%), so the field moved to harder benchmarks like SWE-bench and LiveCodeBench.

### 7.3 Real-World Evaluation Pipeline — Production Case

This is an example of **a team of 20 devs using a daily evaluation pipeline in production**: running the benchmark overnight, checking for regressions, generating reports, and alerting immediately when quality drops. Read it as a "sample blueprint" for your own pipeline — learn how a real team organizes continuous monitoring instead of evaluating just once.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/13-7-3-real-world-evaluation-pipeline-production-case.py`](examples/13-7-3-real-world-evaluation-pipeline-production-case.py)

</details>

> **One-line summary:** A real team's blueprint: run benchmarks overnight, diff against yesterday's baseline, auto-report, and alert the moment quality drops.

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

Quick glosses: **linting** = automatically flagging style mistakes and bug-prone patterns; **test coverage** = the share of your code that tests actually execute; **dependency scanning** = checking the third-party libraries you install for known security holes.

> **One-line summary:** Don't build evaluation from scratch — pick from 4 ready tool groups (benchmarks, frameworks, quality, security) whatever fits your current stage.

### 8.2 PromptFoo Configuration Example

This YAML configuration helps you run PromptFoo — a popular prompt testing tool — on your coding agent: declare the provider (which model), the prompt, and the assertions (conditions the output must satisfy). It's like writing an "inspection contract": the machine automatically grades whether the model meets each condition (e.g. `contains` or `llm-rubric`).

<details>
<summary><b>8.2 PromptFoo Configuration Example (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/14-8-2-promptfoo-configuration-example.yaml`](examples/14-8-2-promptfoo-configuration-example.yaml)

</details>

(YAML = a text format written as indented `key: value` lines, commonly used for config files. `llm-rubric` = an assertion where an LLM checks the output against a written criterion.)

> **One-line summary:** PromptFoo is an "inspection contract": you declare the model, prompt, and pass conditions in YAML, and it grades every output automatically.

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

How to read it: the top half is the ✅ DO list (each item = one rule, the `→` line explains the payoff), the bottom half is the ❌ DON'T list. For instance, DO #4 "Baseline Tracking" means: save today's scores so tomorrow you can tell improvement from decline.

> **One-line summary:** Use this as a checklist — automate, measure many dimensions, keep a baseline, and never trust auto-eval without human calibration.

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

How to read the pyramid: the bottom layer runs constantly and costs almost nothing (static analysis = tools checking code without executing it, e.g. a type checker), the top layer runs rarely and costs the most (E2E test = end-to-end test driving the app like a real user). Errors caught at the bottom are cheap; errors that slip to the top are expensive.

> **One-line summary:** Stack checks like a pyramid — cheap fast checks (lint, unit tests) run constantly and filter out most errors, so expensive slow checks (integration, E2E) stay rare.

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

How to read the leaderboard: **Resolve** = % of issues the system fixed; **Token Use** = how much text it consumed per issue (~20K ≈ 20,000 tokens, roughly 15 pages of text); **Cost/Issue** = money spent per attempted issue. Patch = the block of code changes that fixes the bug.

> **One-line summary:** SWE-bench grades real bug fixes from 2,294 GitHub issues — and shows a simple, cheap system can match a fancy agent loop at a fraction of the cost.

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

How to read it: **Score** = quality of the file edits; **Cost/1M** = price per million tokens as `$input/$output` (e.g. `$3/$15` means $3 per million input tokens and $15 per million output tokens); **Best For** = the use case where that model is the sensible pick. Diff = the record of what lines were added/removed by an edit.

> **One-line summary:** Aider's leaderboard shows quality per dollar — DeepSeek V3 delivers 92% of GPT-4o's quality for 11% of the cost, so match the model to the task's difficulty.

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

Gloss: **Contamination** = the benchmark's questions leaked into a model's training data, so the model may have memorized the answers instead of solving them. Temporal awareness = only grading on problems published *after* the model's training cutoff, so memorization is impossible.

> **One-line summary:** LiveCodeBench fights benchmark cheating by adding fresh problems weekly from coding contests and scoring only post-cutoff questions.

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

How to read it: the 4 layers go from fully automatic (Layer 1) to fully real-world (Layer 4); each layer lists what it measures plus its **Limitation** — the reason you can't rely on it alone. Model routing = automatically sending each task to the cheapest model that can handle it.

> **One-line summary:** Anthropic evaluates on 4 layers — automated benchmarks, human review, real user feedback, A/B tests — because every single layer has a blind spot; the headline metric is Acceptance Rate.

---

### 10.5 DeepSeek Harness — Minimal Benchmark Harness for Unbiased Evaluation

**Context**: The DeepSeek Harness provides a **Minimal Benchmark Harness** — a minimal evaluation mode with only **2 tools: `bash` and `editor`**, designed to eliminate bias from tool selection and provide a clean isolation environment for SWE-bench evaluation.

<details>
<summary><b>Architecture (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/15-10-5-deepseek-harness-minimal-benchmark-harness-for.ts`](examples/15-10-5-deepseek-harness-minimal-benchmark-harness-for.ts)

</details>

How to read the table: each row compares one property between a normal (traditional) harness and the minimal one. For instance, "Isolation: Process-level vs Container-level" means the minimal harness runs each task inside its own sealed container (a self-contained box with its own filesystem), not just a separate OS process — so tasks can't interfere with each other.

**Key Innovations**:

| Feature | Traditional Harness | Minimal Benchmark Harness |
|---------|-------------------|---------------------------|
| **Tools** | 10-20+ (search, read, write, execute, LLM, memory, etc.) | **2 only** (bash + editor) |
| **Isolation** | Process-level | **Container-level** |
| **Determinism** | Variable (LLM tools) | **High** (no LLM tools) |
| **Bias** | Tool selection bias | **Minimal** (equal footing) |
| **Reproducibility** | Hard | **Native** (container snapshots) |
| **SWE-bench Score** | Varies | **Baseline for comparison** |

**Why Only 2 Tools?** (tool selection bias = when a model looks smart only because it happens to have fancy tools, not because it reasons better):
1. **Scientific Control** — Eliminates "tool selection bias" where models with better tool-use appear smarter
2. **Reproducibility** — Container + fixed toolset = deterministic environment (same input always gives the same result)
3. **Focus on Reasoning** — Forces model to demonstrate actual code understanding, not tool mastery
4. **Cost Control** — Fewer tool calls = lower token usage, predictable costs
5. **Fair Comparison** — All models evaluated on same minimal interface

**File Reference**: For implementation details, see [`minimal-benchmark-harness.md`](minimal-benchmark-harness.md)

> **One-line summary:** Strip the harness down to `bash` + `editor` in a sealed container, and you measure the model's reasoning instead of its tool-collection.

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

> 📄 **Example code:** [`examples/16-11-1-core-evaluation-types.ts`](examples/16-11-1-core-evaluation-types.ts)

</details>

> **One-line summary:** TypeScript types are the shared data contract — every metric, test case, and report has a fixed shape, so mistakes surface at compile time instead of in production numbers.

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

How to read it: each letter of SOLID is one rule; the ✅ line shows the compliant way, the ❌ line the trap. For example, D (Dependency Inversion) means your evaluator talks to a generic `IModelProvider` interface, so swapping OpenAI for another provider touches one line, not the whole system.

> **One-line summary:** Apply SOLID to evaluators — one job each, easy to add new metrics without touching old code, so the system stays maintainable for years.

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

("Thou shall" is old-style English for "you must" — each numbered item is one commandment. E.g. #6, reproducible, means: pin the random seed and keep benchmark data in version control, so re-running gives identical scores.)

> **One-line summary:** Ten commandments of evaluation — measure what matters, use multiple metrics, calibrate with humans, track cost, and audit the evaluator itself.

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

> 📄 **Example code:** [`examples/17-13-1-evaluation-test-harness.py`](examples/17-13-1-evaluation-test-harness.py)

</details>

> **One-line summary:** Test the tests: verify your metrics compute correctly, benchmarks reproduce, and cost tracking is accurate — otherwise every number downstream is suspect.

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

How to read it: 6 trend blocks, each with 4 concrete sub-items you can adopt. For example, TREND 6 "Evaluation-as-Code" means your evaluation suite lives in the repo like source code — versioned, run by CI/CD (the automated build-and-test pipeline), and posting results as PR comments (CI/CD = Continuous Integration/Continuous Delivery, the automation that builds and tests every change).

> **One-line summary:** 2024–2026 direction: evaluation becomes automated, real-time, cost-aware, human-calibrated, domain-specific, and lives in code like any other test.

---

## 15. Trajectory, Contamination, Cost-per-Quality & Human Calibration

Pass/fail hides *how* an agent worked. This section adds trajectory scoring (efficiency, precision, recovery), leakage-proof harness hygiene, $/pass-task routing, and calibration of LLM judges against humans. Trajectory = the full path the agent took (every thought, tool call, and result), not just the final answer. Analogy: like judging a rally driver — finish line matters, but so do wrong turns (steps), detours (tool calls), crashes recovered from (recovery), and whether the track was already practiced on (contamination).

> **Dedup note:** §7 and §10 both narrate SWE-bench end-to-end. Convention: §7 = *benchmark definitions* (what SWE-bench/HumanEval measure); §10 = *case-study results* (who scored what). This §15 adds only *method* (trajectory metrics, isolation, cost, calibration).

### 15.1 Trajectory Eval — Step-Efficiency, Precision, Recovery

How to read it: each row is one metric — name, what it counts, and the target value you should hold it to. For instance, `tool_precision ≥ 0.6` means at least 60% of the agent's tool calls must actually help; p50 = the median (middle value across runs).

| Metric | Definition | Target |
|---|---|---|
| `pass` | Task solved (tests + hidden checks) | primary gate |
| `steps_used / steps_p50` | Step-efficiency = p50 reference steps ÷ actual steps (cap 1.0) | ≥ 0.7 |
| `tool_precision` | Useful tool calls ÷ total tool calls | ≥ 0.6 |
| `recovery_rate` | Errors fixed without human ÷ total error episodes | ≥ 0.5 |
| `wasted_edits` | File writes reverted in same run ÷ total writes | ≤ 0.2 |
| `trajectory_score` | `0.5·pass + 0.2·efficiency + 0.15·precision + 0.15·recovery` | CI gate ≥ 0.65 |

Score trajectories, not just outcomes: log every `(thought, tool, args, result, cost)` span; penalize brute-force retry loops that pass by luck. (Span = one logged unit of work: what the agent thought, which tool it called, with what arguments, what came back, and what it cost.)

> **One-line summary:** Score the journey as well as the destination — reward efficient steps and clean tool use, and punish lucky brute-force retries.

### 15.2 Contamination & Isolation Hygiene

(Contamination = benchmark tasks leaked into training data, so scores measure memory, not skill. Hygiene here = the habits that keep your measurements clean.)

- **Leakage:** quarantine any task whose solution/issue text appears in training cutoff; tag `leak_risk: high` and exclude from headline numbers (report separately). (Quarantine = pull it out of the main scoreboard into a side list, like isolating a sick patient.)
- **Seeds:** fix `seed` + `temperature=0` for regression suites; run nondeterministic evals 3× and report mean ± std. (Seed/temperature control the model's randomness; `temperature=0` = make output as deterministic as possible; mean ± std = average plus how much it wobbles.)
- **Flaky quarantine:** auto-quarantine tests failing <5% over 50 runs into `flaky/` lane; they never block promotion, but file a tracking issue. (Flaky test = passes and fails randomly on identical code, often due to timing or environment, not real bugs.)
- **Isolation:** fresh container/FS per task, no shared cache between tasks, network deny except allow-listed mirrors; hash dataset + record commit SHA in report. (FS = filesystem; commit SHA = the unique ID of the exact code version tested; hash of dataset = a fingerprint proving which task set was used.)

> **One-line summary:** Keep measurements clean: quarantine leaked or flaky items, pin randomness, isolate each task in its own container, and record exactly what you tested.

### 15.3 Cost-per-Quality — $/Pass-Task Routing Metric

(`$/pass-task` = total money spent on evaluation divided by number of tasks solved — your true price per success. Routing = choosing which model handles which task.)

`$/pass-task = total_eval_cost ÷ tasks_passed`. Track per model/route; route easy tasks to cheap model, escalate only on failure (cascade = try the cheap model first, and only hand the task to the expensive model if the cheap one fails). Report Pareto table (Pareto = comparing options where improving one axis — quality — worsens the other — cost):

How to read the table: each row is one routing strategy; **Pass %** is the solve rate, **$/pass-task** the price per solved task, and **Verdict** the recommendation. For instance, the cascade gets 71% solved at $0.065 each — nearly the quality of large-only at a quarter of the price.

| Route | Pass % | $/1k tasks | $/pass-task | Verdict |
|---|---|---|---|---|
| small-only | 52% | $18 | $0.035 | cheap baseline |
| small→large cascade | 71% | $46 | $0.065 | ✅ best tradeoff |
| large-only | 74% | $210 | $0.284 | only when quality-critical |

Gate model upgrades on *both* Δpass ≥ +2pp *and* Δ$/pass-task ≤ +10%. (Δ = "change in"; +2pp = at least 2 percentage points more tasks solved; the second condition = cost per solved task must not rise more than 10%.)

> **One-line summary:** Judge models by price per solved task, route easy work to cheap models with a cascade fallback, and only accept upgrades that add accuracy without inflating cost.

### 15.4 Human Calibration — Judge-vs-Human Agreement

(Calibration = periodically checking that the LLM judge scores the way skilled humans would, and correcting it when it drifts.)

- Sample 100–200 tasks/quarter for blind human re-grade; compute Cohen's κ and agreement rate per dimension (correctness/style/safety). (Blind = the human doesn't see the judge's score; Cohen's κ = a 0–1 statistic for agreement between two raters, where 1 is perfect and 0 is random chance.)
- Require κ ≥ 0.7 before judge gates promotion; below → retune rubric + few-shots, never lower the bar. (Few-shots = example input-output pairs added to the judge's prompt to teach it the standard.)
- **Bias checks:** length bias (longer ≠ better), self-preference (judge favoring own family), position bias (shuffle A/B order); report bias deltas alongside scores. (Bias delta = how much the judge's score shifts due to that quirk alone, e.g. favoring the longer of two equal answers.)

<details>
<summary>Python Code — Trajectory Scorer (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-15-4-human-calibration-judge-vs-human-agreement.py`](examples/18-15-4-human-calibration-judge-vs-human-agreement.py)

</details>

### 15.5 Checklist

(Each box is one habit to install; tick it when your pipeline does it automatically.)

- [ ] Log full trajectories + compute efficiency/precision/recovery
- [ ] Gate on `trajectory_score`, not pass% alone
- [ ] Leakage quarantine + seed pinning + 3× reruns for stochastic evals (stochastic = involving randomness, so results vary between runs)
- [ ] Flaky lane separate from blocking suite
- [ ] Report $/pass-task per route + cascade policy
- [ ] Quarterly human calibration (κ ≥ 0.7) + length/self/position bias checks
- [ ] Dataset hash + env SHA in every report

> **One-line summary:** If you install only one habit from §15, make it this checklist — it turns everything above into a repeatable routine.

---

## References

(These are the sources behind the document — papers first, then tools, benchmarks, and the case studies above. Each link opens the original page.)

### Papers & Research
- [HumanEval Benchmark](https://github.com/openai/human-eval) — OpenAI code generation benchmark
- [SWE-bench](https://www.swebench.com/) — Princeton NLP real-world bug fix benchmark
- [CodeBLEU](https://github.com/microsoft/CodeXGLUE) — Microsoft code evaluation metric (a formula that scores how similar generated code is to reference code)
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

> **One-line summary:** All primary sources in one place — use them to verify numbers or go deeper on any benchmark or tool named above.

---

---

> **Oct-2026 addendum:** evals now extend beyond chat to automation (per-node + workflow evals,
> Custom Graders Library, generated graders). Pair `minimal-benchmark-harness.md` with trajectory
> logs from `13-trajectory-observability` + OTel `_meta` trace keys for reproducible scoring.
> (Grader = the component that scores one output; OTel = OpenTelemetry, a standard for collecting
> traces and logs from software; per-node + workflow evals = grading each step *and* the whole run.)

**Last updated:** 16/10/2026  
**Author:** AI Knowledge Repository

## October 2026 Update — LLM-as-Judge & End-State Evaluation (Anthropic 06/2025)

> **📌 Context:** Distilled from the article *Demystifying Evals for AI Agents* (Anthropic, 06/2025). The core message: **don't wait for the perfect eval to get started** — start small, grade with an LLM, and evaluate the end state instead of every step.

This closing section distills Anthropic's practical advice: don't wait for a perfect eval, grade with an LLM, and evaluate final outcomes. It's included because it contradicts two common instincts — postpone evaluation, and grade every step.

### 1. Eval-First — Start with ~20 Test Cases

This section argues for building evaluation on day one, and tells you how many test cases you actually need at each stage.

The most common mistake: **postponing eval building** until the system is "stable" — then when you need to measure, there's no baseline to compare against. (Baseline = an earlier saved set of scores to diff against.) Reality is the opposite:

> **Key point:** The earliest changes have the **largest effect sizes** — when improving success rate from **30% → 80%**, you can **see the difference with a small sample** (~20 test cases). But once the system is at 85%, seeing a difference of 85% → 87% requires thousands of cases. (Effect size = how big the change you're looking for actually is — the bigger it is, the fewer samples you need to see it.)

How to read the table: each row is a project stage; the middle column is how many test cases are enough there, the last column explains why that's enough.

| Stage | Number of test cases | Why it's enough |
|---|---|---|
| Early project | ~20 | Large effect size (30%→80%), differences visible immediately |
| Maturing | 100–500 | Detect regressions as features are added |
| Stable | Hundreds–thousands | Compare models/versions, fine-tuning |

> **One-line summary:** Start evaluating with just ~20 test cases on day one — early improvements are so big that a tiny sample shows them.

### 2. LLM-as-Judge Pattern

This is the **simplest scoring method that aligns best with human judgment**: 1 LLM call, 1 prompt, graded against a fixed rubric. How to read the table: each row is one rubric criterion, and the question is what the judge asks itself for that criterion.

| Criterion | Scoring question |
|---|---|
| **Factual accuracy** | Does every claim in the output match the sources? |
| **Citation accuracy** | Does each citation point to the source supporting that claim? |
| **Completeness** | Is any part of the task missing? |
| **Source quality** | Are primary sources preferred over secondary? |
| **Tool efficiency** | Did the agent use tools sensibly or wastefully and redundantly? |

**Output:** score `0.0–1.0` + label `pass/fail`. Because the output is structured, it scales to **hundreds of outputs** without manually reading each one.

> **One-line summary:** One LLM call with a fixed rubric scores 0.0–1.0 with pass/fail — cheap enough to run on hundreds of outputs.

### 3. End-State Evaluation

This section tells you *what point in the run to grade* for agents that change things — grade the finish line, not the footprints.

For agents that **mutate state** (write files, run commands, change the DB — mutate state = permanently change something, not just produce text), don't grade each step — grade the **end state**:

> **Why?** The same destination can be reached via **many different paths**. Grading each step punishes unusual paths even when the result is correct; grading end-state is fair and reflects the real value the user receives. (End state = the final situation after the agent finishes, e.g. "tests pass and build succeeds".)

How to read the table: each row is one task type; the ✅ question is the single check that decides success.

| Task type | Evaluation |
|---|---|
| Agent fixes code | ✅ Do tests pass? Does the build succeed? No broken functionality? |
| Agent deploys infra | ✅ Does the endpoint return correct results? Is the cluster state correct? |
| Agent does research | ✅ Does the answer address the question with trustworthy sources? |

For **complex workflows**, split the progress into **checkpoints** — each checkpoint corresponds to an **expected state change** — so you grade end-state while also knowing where the break happened if it fails. (Checkpoint = a midway stop where you verify one state change, e.g. "config file written correctly" before moving on.)

> **One-line summary:** Grade where the agent *ended up*, not how it got there — with checkpoints in long workflows so failures are easy to locate.

### 4. Human Evaluation — Catching Edge Cases

This section covers what only humans can catch: failure types your automated rubric doesn't know how to grade yet.

Automation can't catch everything — you need **humans reading batches of outputs** (in the early stages) to catch error classes the rubric doesn't yet cover:

- **Hallucinated answers:** the agent asserts confidently with no supporting source.
- **System failures:** timeouts, wrong tool calls, silent crashes that don't get graded as fails.
- **Source selection bias:** the classic example — agents **choosing SEO content farms over academic PDFs**. (SEO content farm = websites mass-producing shallow articles to rank high in search, vs. trustworthy primary sources like university PDFs.) Fix: add **source quality heuristics to the prompt** (prefer `.edu`, `.gov`, reputable domains; penalize content farms). (Heuristic = a practical rule of thumb baked into the prompt.)

> **Pattern:** a human finds an edge case → turn the edge case into a new test case → rubric/heuristics get updated → the LLM-judge can grade that error class on its own next time. **Human evaluation feeds the automated eval; it doesn't replace it.**

> **One-line summary:** Humans read early outputs to discover failure types automation misses, then feed each one back into the rubric so the judge catches it next time.

### 5. Production Reliability Eval

This section is about evaluation *after* launch — its job shifts from scoring work to guarding quality.

After going to production, evaluation shifts roles from "grading papers" to "standing guard":

How to read the table: each row is one ongoing activity and the purpose it serves.

| Activity | Purpose |
|---|---|
| **Regression test after every deploy** | Re-run the eval suite before release — catch incidents caused by prompt/model/tool changes |
| **Tracing decision patterns** | Log **decision patterns** (which tools the agent picked, which branches it took) — not conversation content (privacy) — to debug root causes when quality drops |

### 6. Python Code — LLM-Judge with Rubric Prompt

> 📄 **Example code:** [`examples/19-6-python-code-llm-judge-with-rubric-prompt.py`](examples/19-6-python-code-llm-judge-with-rubric-prompt.py)

**Key point:** 1 call, 1 rubric, parseable JSON output, pass/fail by threshold — good enough for CI running hundreds of test cases without a complex harness. (CI = continuous integration, the robot that builds and tests every change automatically; threshold = the cutoff score, e.g. anything under 0.8 fails.)

### 7. Cross-Reference

Where to go next: the architecture doc places evaluation in the bigger system, section 4.2 above shows the same judge idea applied to code, and `07-workflow` covers the checkpoint idea for long runs.

> 📎 **Related:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 8** (Evaluation). See also Section 4.2 (LLM-as-Judge Evaluation) above for a more detailed code-grading pattern, and `07-workflow` for checkpoints during long agent runs.

---

**Last updated:** 26/10/2026  
**Author:** AI Knowledge Repository
