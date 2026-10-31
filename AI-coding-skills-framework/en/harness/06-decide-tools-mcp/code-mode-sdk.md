# 💻 Code Mode SDK — Multi-Step Tool Orchestration via Code Execution

> **A pattern inherited from the DeepSeek Harness**: instead of forcing the LLM to perform dozens of dialogue turns (multi-turn round-trips) to call tools one at a time through JSON schema, **Code Mode SDK** lets the LLM write a single program (TypeScript/Python) that interacts with the Harness SDK. This program executes the entire complex processing flow in a single runtime loop.

---

## 📑 Table of Contents

- [💻 Code Mode SDK — Multi-Step Tool Orchestration via Code Execution](#-code-mode-sdk--multi-step-tool-orchestration-via-code-execution)
  - [📑 Table of Contents](#-table-of-contents)
  - [1. Context: Standard Tool Calling vs Code Mode SDK](#1-context-standard-tool-calling-vs-code-mode-sdk)
    - [Standard Tool Calling (Multi-turn Round-trips)](#standard-tool-calling-multi-turn-round-trips)
  - [2. Core Benefits of Code Mode SDK](#2-core-benefits-of-code-mode-sdk)
    - [Outstanding advantages:](#outstanding-advantages)
  - [3. SDK Architecture (`@deepseek-ai/dsh` Pattern)](#3-sdk-architecture-deepseek-aidsh-pattern)
  - [4. Programmatic Tool Pipeline Execution Flow](#4-programmatic-tool-pipeline-execution-flow)
  - [5. Illustrative Implementation (TypeScript Execution Sandbox)](#5-illustrative-implementation-typescript-execution-sandbox)
  - [6. Detailed Comparison (Standard vs Code Mode)](#6-detailed-comparison-standard-vs-code-mode)
  - [7. Best Practices \& Security Guardrails](#7-best-practices-&-security-guardrails)
    - [✅ Best Practices](#-best-practices)
    - [🛡️ Security Guardrails](#-security-guardrails)

---

## 1. Context: Standard Tool Calling vs Code Mode SDK

This section explains the two ways an agent can call tools, so the rest of the document makes sense.

### Standard Tool Calling (Multi-turn Round-trips)
In standard AI Agent frameworks, when completing a task consisting of 5 steps (e.g.: find `*.ts` files, read the files, filter `fetch` functions, fix the code, run the linter — linter = a tool that checks code style and errors), the LLM must perform **5 independent interaction turns** (turn = one full "send to model, wait, get answer" cycle) with the system:

```
Turn 1: LLM ──[JSON: search_files]──► Harness ──[Exec]──► LLM (Returns 20 files)
Turn 2: LLM ──[JSON: read_file_1]───► Harness ──[Exec]──► LLM (Returns content 1)
Turn 3: LLM ──[JSON: read_file_2]───► Harness ──[Exec]──► LLM (Returns content 2)
Turn 4: LLM ──[JSON: edit_file]─────► Harness ──[Exec]──► LLM (Edit done)
Turn 5: LLM ──[JSON: run_linter]────► Harness ──[Exec]──► LLM (Success)
```

Read it as: the model asks for one tool per turn, the Harness (the runtime around the model) runs it, and the result goes back into the conversation before the model can decide the next step.

**Drawbacks:**
- **High Latency**: Each turn takes 1-3 seconds to call the LLM API. 5 turns take 10-15 seconds.
- **Token Consumption**: The conversation history must balloon with every turn (the entire old context is re-sent — you pay for it again every time).
- **Lack of complex control flow**: The LLM cannot write loops (`for`), conditional statements (`if/else`), or handle errors (`try/catch`) directly between tools — it must rely entirely on step-by-step reasoning.

> **One-line summary:** Standard tool calling is one JSON request per step, so a 5-step task costs 5 round-trips, growing history, and no loops or error handling.

---

## 2. Core Benefits of Code Mode SDK

This section explains what Code Mode changes: the model writes code instead of single tool requests.

The DeepSeek Harness introduces **Code Mode** together with a standardized SDK (`@deepseek-ai/dsh` — SDK = a ready-made library of tool functions the generated code can call). Instead of calling tools via JSON, the LLM generates a TypeScript/JavaScript code snippet that executes inside a Sandboxing Runtime (sandbox = a locked-down environment where the code can only do what you allow):

> 📄 **Example code:** [`examples/01-2-core-benefits-of-code-mode-sdk.ts`](examples/01-2-core-benefits-of-code-mode-sdk.ts)

```
Single Turn: LLM ──[TypeScript Code]──► Code Runtime Engine ──[Exec All Steps]──► LLM (Final result)
```

### Outstanding advantages:
1. **80% Latency & Token Cost Reduction**: Merges $N$ API calls into **a single turn only** ($N$ = however many steps the task has).
2. **Powerful Control Flow**: Fully leverages the control structures of programming languages (loops, async/await, error boundaries, data filtering — the model can now write `for`, `if`, `try/catch` like a developer).
3. **Deterministic Output**: Reduces hallucination (hallucination = the model inventing plausible but wrong data) when stitching data together across tools.

> **One-line summary:** Code Mode replaces N tool turns with one generated program — faster, cheaper, and with real loops and error handling.

---

## 3. SDK Architecture (`@deepseek-ai/dsh` Pattern)

This section shows how all system tools are packaged into one typed object the generated code can use.

The Harness SDK packages all system tools (Search, File System, MCP Tools, Shell execution) into a single TypeScript object with clear type definitions (types = descriptions of what arguments each tool takes and what it returns, so the model's code can be checked before running):

> 📄 **Example code:** [`examples/02-3-sdk-architecture-deepseek-ai-dsh-pattern.ts`](examples/02-3-sdk-architecture-deepseek-ai-dsh-pattern.ts)

> **One-line summary:** Every tool the agent can use becomes one typed method on the `dsh` object — so generated code that calls tools is checkable and compilable.

---

## 4. Programmatic Tool Pipeline Execution Flow

This section walks through the four steps the execution engine takes for one Code Mode run.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      CODE MODE EXECUTION ENGINE                       │
├────────────────────────────────────────────────────────────────────────┤
│  1. LLM receives the task ──► Generates a Script: `solution.ts`      │
│                                                                        │
│  2. Sandboxing Engine (Node.js/V8 Isolate):                           │
│     ├── Injects the `dsh` SDK object                                   │
│     ├── Restricts Network / File System access                          │
│     └── Sets Timeout & Resource Limits (RAM / CPU)                    │
│                                                                        │
│  3. Executes the Script ──► Captures console.log / Trajectory Events   │
│                                                                        │
│  4. Returns the aggregated result + a Trajectory trace to the LLM      │
└────────────────────────────────────────────────────────────────────────┘
```

Plain-language glosses: V8 Isolate = a sealed mini-JavaScript engine that cannot touch your process; injects = hands the script the SDK object as its only way to reach tools; trajectory events = the recorded log of every step the script took.

> **One-line summary:** The engine takes the model's script, runs it in a restricted sandbox with the SDK injected, and returns one result plus a step-by-step trace.

---

## 5. Illustrative Implementation (TypeScript Execution Sandbox)

This section points to a simplified, real implementation of the sandbox runner.

Below is simplified source code for a **Code Mode Sandbox Executor** that runs LLM-generated TypeScript code:

> 📄 **Example code:** [`examples/03-5-illustrative-implementation-typescript-execution-sandbox.ts`](examples/03-5-illustrative-implementation-typescript-execution-sandbox.ts)

> **One-line summary:** The example file shows, in runnable code, how the sandbox injects the SDK, applies limits, and captures output.

---

## 6. Detailed Comparison (Standard vs Code Mode)

This section is the side-by-side scorecard for choosing a mode.

| CRITERION | STANDARD TOOL CALLING | CODE MODE SDK |
|---|---|---|
| **Execution mechanism** | LLM returns a JSON Schema → the server runs the tool → returns the result to the LLM | LLM writes TypeScript/Python code → runs it in a Sandbox |
| **Number of interactions (Turns)** | Multi-turn ($N$ turns for $N$ steps) | Single turn (1 turn for the whole chain of $N$ steps) |
| **Latency** | High (depends on many LLM API calls) | Low (only the actual script runtime) |
| **Intermediate data handling** | Shuttled back and forth through the LLM's Context Window | Processed directly in the Code Runtime's RAM |
| **Control structures** | None (the LLM reasons step by step) | Very strong (`for`, `while`, `try/catch`, `map/filter`) |
| **Best suited tasks** | Step-by-step analysis, interactive Q&A | Batch processing, code refactoring, data migration |

How to read it: each row compares one property, and the winner depends on your task. For instance, "Intermediate data handling" means a 900KB search result stays in RAM under Code Mode, but must be copied into the model's context window (and paid for twice) under standard calling.

> **One-line summary:** Standard calling wins for interactive analysis; Code Mode wins for batch, repetitive, code-shaped work.

---

## 7. Best Practices & Security Guardrails

This section lists the operating rules: three habits to follow, three walls that keep generated code safe.

### ✅ Best Practices
- **Strict Typing for the SDK**: Provide the complete `@types/dsh` definition file inside the System Prompt so the LLM can automatically write 100% correct code (typing definitions = the exact function signatures, so the model does not guess tool names or arguments).
- **Dry-run First**: Perform a syntax check (static analysis/TypeScript compilation) before executing the source code — a typo should fail cheaply, before any sandbox starts.
- **Detailed Logging**: Require the LLM to use `console.log()` at key processing milestones for easy tracing in the Event Stream.

> **One-line summary:** Give the model the full type definitions, dry-run before executing, and require milestone logs.

### 🛡️ Security Guardrails
- **Sandbox Isolation**: Always run code in an isolated environment (Docker Container, Worker Threads, or V8 Isolate). Never use `eval()` or `vm.runInThisContext()` — both run code inside your own process with full powers, so a malicious script could do anything. The tier taxonomy, the mandatory controls, and the hardened runner are specified in [`12-sandbox-execution`](../12-sandbox-execution/README.md) — this section only records that Code Mode scripts inherit them.
- **Resource Constraints**: Set execution time limits (`timeoutMs`), memory limits (`maxMemory`), and a maximum number of Shell commands — so a runaway loop cannot eat your RAM or spin forever. These are the `12` §3 resource caps applied to a Code Mode sandbox; change them there, not here.
- **Permission Approval**: If the script performs dangerous operations (e.g.: `rm -rf` = delete a whole folder with no undo, `git push --force` = overwrite remote commit history and lose backups), the Sandbox must pause and request confirmation from the User. The pause mechanism is the `PAUSED:` protocol in [`15-approval-gates`](../15-approval-gates/README.md) §5 — note that "pause and ask" is not the same as "deny on timeout", and it is `15` that decides which applies.

> **One-line summary:** Isolate the sandbox, cap time and memory, and pause for human approval on any irreversible operation.
