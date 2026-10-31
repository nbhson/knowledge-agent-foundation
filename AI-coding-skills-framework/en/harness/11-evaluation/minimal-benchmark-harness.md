# 🧪 Minimal Benchmark Harness — A Minimal Evaluation Environment for Raw LLM Reasoning

> **Pattern inherited from the DeepSeek Harness (Minimal Mode):** A minimal evaluation environment that isolates the LLM's raw reasoning ability from the intervention of complex framework layers (heavy prompts, multi-agent orchestration, complex memory pipelines).

---

## 📑 Table of Contents

- [🧪 Minimal Benchmark Harness — A Minimal Evaluation Environment for Raw LLM Reasoning](#-minimal-benchmark-harness--a-minimal-evaluation-environment-for-raw-llm-reasoning)
  - [📑 Table of Contents](#-table-of-contents)
  - [1. Context & Motivation](#1-context--motivation)
  - [2. The Philosophy of the Minimal Benchmark Harness](#2-the-philosophy-of-the-minimal-benchmark-harness)
  - [3. Architecture of the Minimal Mode Environment](#3-architecture-of-the-minimal-mode-environment)
  - [4. The Minimal Tool Set (Minimal Tool Set: Bash + Editor)](#4-the-minimal-tool-set-minimal-tool-set-bash--editor)
    - [1. `bash`](#1-bash)
    - [2. `editor`](#2-editor)
  - [5. Implementing the Benchmark Runner (TypeScript Implementation)](#5-implementing-the-benchmark-runner-typescript-implementation)
  - [6. Evaluation Criteria & Metrics (SWE-bench / HumanEval)](#6-evaluation-criteria--metrics-swe-bench--humaneval)
  - [7. Best Practices & Isolation Guardrails](#7-best-practices--isolation-guardrails)
    - [✅ Best Practices](#-best-practices)
    - [❌ Anti-Patterns](#-anti-patterns)

---

## 1. Context & Motivation

This section explains why benchmark scores can lie — so you know why the minimal harness exists.

When evaluating the performance of an AI Coding Agent on benchmarks such as
**SWE-bench** (real GitHub bug-fixing tasks), **HumanEval** (small Python
function-writing tasks), or **MBPP** (basic Python problems), the measured
results are often noisy because of:
- **System Prompt Overhead**: A system prompt that is too long (2,000+ tokens) steers the model's behavior excessively. (System prompt = the standing instructions sent before every conversation.)
- **Framework Intervention**: RAG layers, Memory Consolidation, or Guardrails automatically modify the model's answers. (RAG = the system fetches extra documents into the prompt; Guardrails = rules that rewrite or block answers.)
- **Tool Complexity**: Too many unwieldy tools degrade the ability to pick the correct tool (Tool Selection Overhead).

**The consequence**: It becomes very hard to answer the question: *"Is this LLM actually good at programming reasoning, or is the framework harness hiding its weaknesses?"* (Harness = the wrapper code around the model: prompts, tools, and plumbing.)

> **One-line summary:** Heavy prompts, framework layers, and tool clutter muddle
> benchmark scores, so you can't tell the model's real skill from the harness's
> help.

---

## 2. The Philosophy of the Minimal Benchmark Harness

This section states the core principle of the minimal harness: strip the environment down to measure the model itself.

The Minimal Benchmark Harness solves this problem with the principle of **Isolation Testing** (test the model alone, with nothing else in the room):

```
Minimal Harness = Minimal System Prompt + Zero Framework Middleware + 2 Core Tools (Bash + Editor)
```

Read the formula left to right: one short system prompt, no middle-layer
software between the model and its tools, and only the two tools named.

By removing every auxiliary component, the system measures precisely the **native capability** of the LLM in solving technical problems.

> **One-line summary:** Test the model with almost nothing around it — one short
> prompt, no middleware, two tools — so the score reflects the model, not the
> wrapper.

---

## 3. Architecture of the Minimal Mode Environment

This section draws the same idea as a diagram: what talks to what at runtime.
```
┌────────────────────────────────────────────────────────────────────────┐
│                      MINIMAL BENCHMARK HARNESS                         │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌──────────────┐         ┌─────────────────────────┐                 │
│   │   TESTER     │────────►│  Minimal System Prompt  │                 │
│   │ (SWE-bench)  │         │  "You are a coder..."   │                 │
│   └──────────────┘         └────────────┬────────────┘                 │
│                                         │                              │
│                                         ▼                              │
│                            ┌─────────────────────────┐                 │
│                            │    LLM UNDER TEST       │                 │
│                            │  (DeepSeek-R1 / V3...)  │                 │
│                            └────────────┬────────────┘                 │
│                                         │                              │
│                    ┌────────────────────┴────────────────────┐         │
│                    ▼                                         ▼         │
│         ┌────────────────────┐                    ┌──────────────────┐ │
│         │ 🛠️ TOOL 1: BASH     │                    │ 📝 TOOL 2: EDITOR│ │
│         │ (Run tests, git)   │                    │ (View/Edit code) │ │
│         └────────────────────┘                    └──────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

How to read the diagram: arrows are the flow of requests. The tester (the benchmark, e.g. SWE-bench) sends a task; the short system prompt wraps it; the model answers; and the model may call either tool — `bash` for running tests and git, `editor` for reading and changing code.

> **One-line summary:** One task source feeds one short prompt into one model,
> which reaches the outside world only through bash and editor.

---

## 4. The Minimal Tool Set (Minimal Tool Set: Bash + Editor)

This section defines the only two tools the agent gets — everything else must be done with them.

In Minimal Mode, the agent is given exactly **2 standardized tools**:

### 1. `bash`

Allows running commands in the sandbox environment's terminal.
(Sandbox = a sealed-off environment; breaking things there cannot harm your
real machine. Example commands: `pytest` to run tests, `git diff` to see
changes.)
> 📄 **Example code:** [`examples/01-1-bash.json`](examples/01-1-bash.json)

### 2. `editor`

Allows viewing and editing files at specified line ranges.
(Example: read lines 10–40 of a file, then replace lines 12–15 to fix a bug.)
> 📄 **Example code:** [`examples/02-2-editor.json`](examples/02-2-editor.json)

> **One-line summary:** The agent gets exactly two tools — `bash` to run
> commands and `editor` to view and edit files by line range — nothing more.

---

## 5. Implementing the Benchmark Runner (TypeScript Implementation)

This section points to the code that runs the whole loop automatically: give the model a task, replay its tool calls, and record the result.

Below is the source code of a **Minimal Benchmark Runner** that fully isolates the execution environment:

> 📄 **Example code:** [`examples/03-5-implementing-the-benchmark-runner-typescript-implementation.ts`](examples/03-5-implementing-the-benchmark-runner-typescript-implementation.ts)

> **One-line summary:** Don't hand-run benchmarks — use the provided runner
> script to drive each task start-to-finish in a sealed environment.

---

## 6. Evaluation Criteria & Metrics (SWE-bench / HumanEval)

This section lists the four numbers to record for every run — these are the scoreboard of the benchmark.

| METRIC | MEANING | GOAL |
|---|---|---|
| **Pass@1 Rate** | The rate of fixing the bug correctly on the first attempt | Higher (measures precise reasoning) |
| **Average Turns per Task** | The average number of conversation turns to resolve one task | Lower (saves cost & time) |
| **Tool Error Rate** | The rate of tool calls with wrong parameters / syntax | Lower (< 5%) |
| **Token Efficiency** | Total tokens consumed per successful task | Lower |

How to read it: "METRIC" = the number you record; "MEANING" = what it counts;
"GOAL" = which direction is better. For instance, Pass@1 = 0.6 means the model
fixes 6 out of 10 bugs on the first try, and higher is better; a Tool Error Rate
of 7% means 7 out of 100 tool calls are malformed, and you want it under 5%.
(Tokens = text units the model reads and writes — fewer per task means cheaper.)

> **One-line summary:** Score each run on Pass@1 (higher), turns, tool errors,
> and tokens (all lower) to compare models fairly.

---

## 7. Best Practices & Isolation Guardrails

This section lists habits that keep the test clean (best practices) and the mistakes that ruin it (anti-patterns).

### ✅ Best Practices

- **Clean Docker Container**: Reset the Docker environment to its pristine state (git clean/reset) before running each benchmark task. (Docker container = a disposable virtual machine; pristine = as if brand new, no leftover files or commits.)
- **Zero Injected Memory**: Do not load any data from previous sessions, guaranteeing absolute objectivity. (So the model can't "recall" an answer from an earlier run.)
- **Timeouts & Deadlocks**: Set strict timeouts (e.g., 5 minutes/task) on bash commands to avoid hung processes. (Timeout = kill the command after a time limit; a hung process = a program stuck forever doing nothing.)

> **One-line summary:** Reset the container before every task, never carry over
> old context, and cap every command with a timeout.

### ❌ Anti-Patterns

- **Prompt Leakage / Over-engineering**: Putting problem-solution information or detailed instructions into the Benchmark Harness's system prompt. (This turns "testing the model" into "testing your hints" — the score stops meaning anything.)
- **Shared Workspace**: Letting tasks share a working directory, which causes side-effects between tests. (Example: task 1 leaves a broken file behind, and task 2 fails because of it, not because the model is weak.)

> **One-line summary:** Never leak solution hints into the prompt, and give each
> task its own workspace so leftovers can't corrupt the next test.
