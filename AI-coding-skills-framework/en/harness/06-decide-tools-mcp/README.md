# 🔧 VI. Decide Tools / MCP Calls

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Tool Selection Patterns](#1-tool-selection-patterns)
>   - [1.1 Tool Registry](#11-tool-registry)
>   - [1.2 Example Tools — Extended Set](#12-example-tools--extended-set)
> - [2. Intent Classification](#2-intent-classification)
>   - [2.1 Multi-Strategy Intent Classifier](#21-multi-strategy-intent-classifier)
> - [3. MCP Protocol](#3-mcp-protocol)
>   - [3.1 MCP Architecture Deep Dive](#31-mcp-architecture-deep-dive)
>   - [3.2 MCP Client Implementation](#32-mcp-client-implementation)
> - [4. Tool Executor](#4-tool-executor)
> - [5. Function Calling](#5-function-calling)
> - [6. Tool Decision Pipeline](#6-tool-decision-pipeline)
> - [7. Tool Composition](#7-tool-composition)
> - [8. Permission System](#8-permission-system)
> - [9. Rate Limiting](#9-rate-limiting)
> - [10. Harness Integration](#10-harness-integration)
>   - [10.1 TypeScript Interfaces](#101-typescript-interfaces)
> - [11. Case Studies](#11-case-studies)
>   - [11.1. SWE-agent — Tool-Use for Software Engineering](#111-swe-agent--tool-use-for-software-engineering)
>   - [11.2. Claude Code — Hierarchical Tool Access](#112-claude-code--hierarchical-tool-access)
>   - [11.3. Cursor IDE — Context-Aware Tool Selection](#113-cursor-ide--context-aware-tool-selection)
> - [12. Design Principles](#12-design-principles)
>   - [12.1 SOLID for Tools](#121-solid-for-tools)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 DO ✅](#131-do-)
>   - [13.2 DON'T ❌](#132-dont-)
> - [14. Testing](#14-testing)
> - [15. Advanced Patterns](#15-advanced-patterns)
>   - [15.1 Tool Learning](#151-tool-learning)
> - [16. Future](#16-future)
>   - [16.1 Trends 2026-2028](#161-trends-2026-2028)
> - [17. Production Hardening: MCP, Execution Boundaries, Memoization](#17-production-hardening-mcp-execution-boundaries-memoization)
>   - [17.1 Definitions](#171-definitions)
>   - [17.2 Execution Boundaries — What This Module Owns](#172-execution-boundaries--what-this-module-owns)
>   - [17.3 MCP Production Rules](#173-mcp-production-rules)
>   - [17.4 Dangerous-Op Approval UX](#174-dangerous-op-approval-ux)
>   - [17.5 Checklist](#175-checklist)
> - [Reference Materials](#reference-materials)
>   - [Papers & Research](#papers-&-research)
>   - [Frameworks & Tools](#frameworks-&-tools)
>
---

### Opening Story

This story explains why an agent needs a *tool-decision* step: an agent that picks tools badly wastes money and can cause damage.

Imagine walking into a **car repair workshop** with hundreds of tools: wrenches, screwdrivers, drills, welders... A skilled mechanic knows exactly which tool each job needs. A newcomer will **use a drill to remove a bolt** — or worse, **swat the engine with a hammer**.

**That is precisely the problem of an AI Agent without Tool Decision Intelligence.** Tool Decision Intelligence = the agent's skill of choosing the right tool, with the right settings, for the job at hand.

An LLM (large language model — the AI model that reads and writes text) can "know" how to call tools. But with **50+ tools** in the arsenal, picking the wrong tool or passing wrong parameters leads to: wasted tokens, wrong results, or worse — **unintended side effects** (side effects = changes to the world outside the agent, like deleting a file or sending an email).

**The solution**: Structured Tool Decision — a clear process from **intent analysis → tool selection → parameter validation → execution → result verification**.

> **One-line summary:** An agent with many tools but no decision process picks tools like a rookie mechanic — a structured pick-validate-execute-verify flow prevents wasted tokens and irreversible mistakes.

### Why Is Tool Decision Important?

This section backs up the claim with measured results, so you know the payoff is real, not a hunch.

> *"An agent with 50 tools that picks the wrong tool = a mechanic with 50 hammers who uses a hammer to break glass."*

#### 3 Scientific Evidences

How to read it: each row is one study. **#** is just the row number; **Study** names who measured it; **Key Finding** is the measured improvement. For instance, row 2 means: when the agent classifies the user's intent *before* picking a tool, the pick is correct 92% of the time instead of 65%.

| # | Study | Key Finding |
|---|-------|-------------|
| 1 | **Anthropic MCP Research (2025)** | Agents using structured tool selection reduce **failed tool calls by 60%** compared to an unstructured approach |
| 2 | **LangChain Benchmark (2025)** | Tool selection accuracy increased from **65% to 92%** when using intent classification before tool routing |
| 3 | **Princeton SWE-agent (2024)** | Limiting to 50 search results + tool validation increased **success rate by 64%** |

#### Core philosophy:

Read the formula as a checklist of five gates. Every tool call passes all five, in order:

```
Tool Selection = Intent Classification → Tool Matching → Parameter Validation → Execution → Result Validation
```

- **Intent Classification** = guess what the user wants (search? compute? edit code?).
- **Tool Matching** = pick the tool that fits that want.
- **Parameter Validation** = check the inputs (like `query="BHYT"`, `top_k=5`) before sending.
- **Execution** = run the tool.
- **Result Validation** = check the output is sane before showing it to the user.

**Analogies**: Tool decision is like a doctor prescribing medicine — diagnose the right illness (intent), pick the right drug (tool), at the right dose (parameters), and monitor side effects (result validation).

**If you skip it**: The agent calls the wrong tool → wasted tokens, wrong results, or worse — unintended side effects (file deletion, wrong emails, etc.).

> **One-line summary:** Five ordered gates — intent, tool match, parameter check, execution, result check — cut failed calls by up to 60% and stop dangerous mistakes.

## Overview

> **📌 Core Concept**
>
> **Definition:** Tool Decision is the process of deciding when to call which tool and with what parameters — from task analysis and tool selection, through the API call, to result handling.
>
> **Metaphor:** This module is the "hands and feet" of the agent: every plan only becomes a real action when it passes through here, like a robot arm receiving commands from the brain (the LLM) and executing them under safety control.
>
> **Why it matters:** Choosing the right tool, at the right time, with the right parameters determines whether the agent completes the job or breaks it.

An AI Agent needs to know **when to use which tool** and **how to call that tool**. This is the decision process: Analyze the task → Pick a tool → Call the API → Handle the result.

In Harness Engineering, Tool Decision is the **"hands and feet"** — where planning is converted into real actions. (Harness = the control program that wraps around the LLM and runs the whole agent loop.) Every tool call must pass through guardrails, validation, and logging. (Guardrails = automatic safety checks that block bad calls.)

The diagram below shows that path. Read it top to bottom: each box is one gate a tool call must pass.

```
┌──────────────────────────────────────────────────────────────────┐
│                 DECIDE TOOLS / MCP CALLS                          │
│                                                                  │
│  User Query                                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────┐                                             │
│  │  INTENT        │  Analyze user intent                       │
│  │  CLASSIFIER    │  "search" / "calculate" / "code" / ...     │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Pick the suitable tool from the list      │
│  │  SELECTOR      │  "vector_search" / "calculator" / ...      │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  PARAMETER     │  Extract & validate parameters             │
│  │  EXTRACTOR     │  query="BHYT", top_k=5, ...                │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  GUARDRAILS    │  Validate permission, safety, rate limit   │
│  │  CHECK         │                                             │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  TOOL          │  Call the tool (function call / MCP)       │
│  │  EXECUTOR      │  Handle errors, timeout, retry             │
│  └───────┬────────┘                                             │
│          ▼                                                       │
│  ┌────────────────┐                                             │
│  │  RESULT        │  Parse result → Format → Reply             │
│  │  PROCESSOR     │                                             │
│  └────────────────┘                                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Memory ←→ Guardrails ←→ Feedback ←→ Permissions          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **One-line summary:** Tool Decision is the agent's hands: every plan becomes a real action only after passing the gates of intent → tool → parameters → safety → execution → result.

## Contents

How to read it: **#** is the section number; **Topic** is a clickable link that jumps to that section; **Description** tells you in one phrase what the section covers. For instance, row 8 covers the permission system — who may call which tool.

| # | Topic | Description |
|---|-------|-------------|
| 1 | [Tool Selection Patterns](#1-tool-selection-patterns) | Registry, search, categories |
| 2 | [Intent Classification](#2-intent-classification) | Rule-based & LLM-based |
| 3 | [MCP Protocol](#3-mcp-protocol) | Model Context Protocol in detail |
| 4 | [Tool Executor](#4-tool-executor) | Error handling, retries, logging |
| 5 | [Function Calling](#5-function-calling) | OpenAI style + parallel calls |
| 6 | [Tool Decision Pipeline](#6-tool-decision-pipeline) | End-to-end pipeline |
| 7 | [Tool Composition](#7-tool-composition) | Chain & parallel tool calls |
| 8 | [Permission System](#8-permission-system) | RBAC for tools |
| 9 | [Rate Limiting](#9-rate-limiting) | Token/usage quotas |
| 10 | [Harness Integration](#10-harness-integration) | TypeScript interfaces |
| 11 | [Case Studies](#11-case-studies) | SWE-agent, Claude Code, Cursor |
| 12 | [Design Principles](#12-design-principles) | SOLID for tools |
| 13 | [Best Practices](#13-best-practices) | DO/DON'T in detail |
| 14 | [Testing](#14-testing) | Unit & integration tests |
| 15 | [Advanced Patterns](#15-advanced-patterns) | Tool learning, dynamic tools |
| 16 | [Future](#16-future) | Trends 2026-2028 |

> **One-line summary:** The document walks from picking tools (1–2), connecting to them (3–5), running them safely (6–10), to learning from real products (11) and hardening for production (12–17).

---

## 1. Tool Selection Patterns

> **📌 Core Concept**
>
> **Definition:** Tool Selection Patterns are the ways an AI Agent decides which tool to pick from a large set (tool registry, search, categories) to complete a specific task.
>
> **Metaphor:** Like a mechanic standing in front of a toolbox with hundreds of items: a skilled one doesn't need to read the manual for each wrench and still knows exactly which item to use for each bolt.
>
> **Why it matters:** Picking the right tool from the start saves tokens, avoids side effects, and increases the task completion rate.

### 1.1 Tool Registry

This section is the "phone book" of all tools in the system. `ToolDefinition` is the declaration record for a single tool (name, description, parameters, permissions, rate limit, timeout, cost) — think of it as the tool's ID card. `ToolRegistry` is the storage that lets you register, search, filter by category, detect deprecated tools (deprecated = old tools marked "retired, use the newer one instead"), and track metrics (success rate, latency). How to read it: look at the `ToolDefinition` record first, then read the `ToolRegistry` methods to see what the registry can do.

*Analogy:* Like a medicine cabinet with clear labels — each tool is a bottle labeled with its purpose (description), dosage (parameters), and expiration date (deprecation date); the registry is the cabinet manager who knows exactly which bottle is in which shelf.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-1-tool-registry.py`](examples/01-1-1-tool-registry.py)

</details>

> **One-line summary:** The registry is the labeled phone book of tools: each tool carries an ID card (definition), and the registry registers, finds, filters, and monitors them.

### 1.2 Example Tools — Extended Set

This section shows how to quickly build a default toolset: the `create_default_tools()` function registers each `ToolDefinition` into the `ToolRegistry` with name, description, parameters, category, and tags. While reading, note that some sensitive tools are marked `requires_permission="elevated"` (elevated = a higher permission level than normal, like a staff-only key) — those are `sql_query` (run database queries), `execute_python` (run code), and `write_file` (change files). This is the shared list of tools used by the following sections (intent classifier, executor, tests).

*Analogy:* Like a pre-packed toolbox for a newcomer: you don't need to buy each item separately, just open the case and you have the basics for most jobs.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-1-2-example-tools-extended-set.py`](examples/02-1-2-example-tools-extended-set.py)

</details>

> **One-line summary:** A ready-made toolbox: sensible defaults registered in one function, with dangerous tools flagged as needing elevated permission.

---

## 2. Intent Classification

> **📌 Core Concept**
>
> **Definition:** Intent Classification is the process of guessing what the user wants to do from their question (search, compute, write code, remember, etc.), then mapping it to the right group of tools — combining rule-based (fast, cheap) with embedding/LLM-based (more accurate, more expensive) to balance quality and cost.
>
> **Metaphor:** Like a hotel receptionist listening to the guest's first sentence to guess whether they need a room booking, a car, or the time, then handing them off to the right department.
>
> **Why it matters:** A wrong intent leads to the wrong tool call, wasted tokens, and meaningless results; correct classification is the mandatory stepping stone before tool selection.

### 2.1 Multi-Strategy Intent Classifier

This section is a three-tier intent classifier to read and reuse. Tier 1 is rule-based: scan keywords like "search", "compute", "read" in the question. Tier 2 is LLM-based: ask the model to analyze the intent. Tier 3 is auto: prefer rules when confidence is high (confidence = a 0-to-1 certainty score; 0.7 or above counts as sure), and only call the LLM when in doubt. The `classify_multi_intent()` function also splits a single sentence containing multiple intents, e.g. "Read the file and run the tests" into two intents [read, test].

*Analogy:* Like a front desk that has a script book (rules) to answer common questions quickly; it only needs to call the manager (the LLM) when it meets a difficult question.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-2-1-multi-strategy-intent-classifier.py`](examples/03-2-1-multi-strategy-intent-classifier.py)

</details>

> **One-line summary:** Classify intent in three tiers — cheap keyword rules first, the LLM only when unsure — and split multi-intent sentences before any tool is chosen.

---

## 3. MCP Protocol

> **📌 Core Concept**
>
> **Definition:** The MCP Protocol (Model Context Protocol) is a standard JSON-RPC 2.0-based protocol that lets any LLM discover (tools/list) and call (tools/call) tools provided by external MCP servers, along with resources and prompts — unified across all providers.
>
> **Metaphor:** Like the USB-C charging port: previously each device had its own cable type, now there is one shared standard for all devices. MCP is the "universal plug" that lets AI attach tools from any service without writing a separate integration for each type.
>
> **Why it matters:** It solves the integration problem of adding adapters one pair at a time (one adapter per LLM-tool pair); a standard protocol lets the tool ecosystem grow many times faster.

Plain glosses for the terms above:

- **JSON-RPC 2.0** = a standard message format for "please run this function, here are the arguments" calls over the network.
- **MCP server** = a small program that exposes tools (GitHub actions, database queries, file operations...) for an AI to call.
- **tools/list** = "what tools do you have?"; **tools/call** = "run this tool for me".

### 3.1 MCP Architecture Deep Dive

This section explains the diagram below: who talks to whom in MCP, and over what channel.

How to read this diagram? There are three clear layers. The top layer is the HOST (the client, where the LLM runs: Claude Desktop, GPT apps, your own agent); the bottom layer is the SERVERS (GitHub, Database, File, Web Search, Slack, etc.) that provide tools. In between is the JSON-RPC connection over stdio/SSE/HTTP — like a standard switchboard (stdio = plain input/output pipes of a local process; SSE and HTTP = network channels). The operating flow: the LLM asks the server "what tools do you have" (tools/list), then calls a specific tool (tools/call). The last strip of the diagram lists all protocol features: capabilities negotiation (client and server first agree on what each side supports), resource access, prompt templates, sampling, and logging.

*Analogy:* Like a taxi dispatch center: the operator (host) calls the drivers (servers) according to the switchboard standard (protocol), and whoever is free takes the job — instead of having to know each driver individually.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MCP (MODEL CONTEXT PROTOCOL)                     │
│                                                                  │
│  MCP is the standard protocol for LLMs to talk to external tools│
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    HOST (Client)                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ Claude   │  │ GPT-4    │  │ Custom   │              │   │
│  │  │ Desktop  │  │ App      │  │ Agent    │              │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘              │   │
│  │       └──────────────┼──────────────┘                    │   │
│  │                      ▼                                    │   │
│  │              MCP Client SDK                              │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                         │ JSON-RPC 2.0                           │
│                         │ (stdio/SSE/HTTP)                       │
│  ┌──────────────────────┴───────────────────────────────────┐   │
│  │                    SERVERS                                │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  GitHub     │  │  Database   │  │  File       │     │   │
│  │  │  Server     │  │  Server     │  │  Server     │     │   │
│  │  │  ─────────  │  │  ─────────  │  │  ─────────  │     │   │
│  │  │  - search   │  │  - query    │  │  - read     │     │   │
│  │  │  - create   │  │  - insert   │  │  - write    │     │   │
│  │  │  - update   │  │  - update   │  │  - delete   │     │   │
│  │  │  - delete   │  │  - schema   │  │  - list     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Web Search │  │  Slack      │  │  Custom     │     │   │
│  │  │  Server     │  │  Server     │  │  API Server │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Protocol Features:                                              │
│  ├── Capabilities negotiation                                   │
│  ├── Tool discovery (tools/list)                                │
│  ├── Tool execution (tools/call)                                │
│  ├── Resource access (resources/read)                           │
│  ├── Prompt templates (prompts/list, prompts/get)              │
│  ├── Sampling (sampling/createMessage)                          │
│  └── Logging (logging/setLevel)                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **One-line summary:** MCP is the universal plug between AI and tools: host asks the server for its tool list, calls what it needs, all over one standard JSON-RPC channel.

### 3.2 MCP Client Implementation

This section gives you a complete MCP client to try out: `connect()` connects to a server with capability negotiation, `list_tools()` fetches the tool list and caches it (cache = keep a local copy so you don't re-ask every time), `call_tool()` calls a tool with a timeout (a maximum wait time before giving up) and error handling, `read_resource()` reads a resource. The `format_tools_for_llm()` function converts MCP tools into the exact format of each provider (OpenAI's `type: function` or Anthropic's). The `MultiServerMCPManager` class at the end manages multiple servers: it gathers tools into one shared namespace and automatically fails over to another server when the primary one errors (failover = switch to the backup automatically). The key point to remember: caching, timeouts, routing, and fallback are the four must-haves of a production MCP client.

*Analogy:* Like a switchboard operator: knows which phone number can answer which request; when one line is busy, automatically transfers to the backup number (failover).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-3-2-mcp-client-implementation.py`](examples/04-3-2-mcp-client-implementation.py)

</details>

> **One-line summary:** A production MCP client must cache the tool list, time out every call, route to the right server, and fail over when a server dies.

---

## 4. Tool Executor

> **📌 Core Concept**
>
> **Definition:** The Tool Executor is the component responsible for calling tools safely: validating parameters, checking permissions and rate limits, running with a timeout, retrying with exponential backoff, and logging every call — sitting between the tool-selection decision and the returned result.
>
> **Metaphor:** Like a waiter with a checklist before taking an order: is the dish on the menu (does the tool exist), do we have enough ingredients (parameters), will the kitchen accept it (permissions, rate limit), and only then hand it to the kitchen and follow up until the dish comes out (timeout, retry).
>
> **Why it matters:** Most agent errors live in failed tool calls; the executor is where all of them are handled consistently, observably, and without breaking the task when something goes wrong.

Two terms from the definition worth unpacking:

- **Exponential backoff** = when a retry is needed, wait longer each time (1s, then 2s, then 4s...) instead of hammering a struggling service.
- **Logging every call** = writing down each tool call (who, what, when, result) so you can debug later.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-4-tool-executor.py`](examples/05-4-tool-executor.py)

</details>

> **One-line summary:** The executor is the safety-checked launcher for every tool call: validate → check permission → run with timeout → retry with growing waits → log.

---

## 5. Function Calling

> **📌 Core Concept**
>
> **Definition:** Function Calling is the mechanism that lets an LLM return not only text but also structured calls following a declared schema — e.g. calling `calculator` with `{"expression": "2+3"}` — while also supporting parallel calls to invoke multiple tools in a single turn, improving efficiency and reducing latency.
>
> **Metaphor:** Like a doctor writing a prescription instead of telling a story: the model "writes the prescription" (a tool call with JSON arguments) for the pharmacist (executor) to dispense the exact medicine at the exact dose, instead of brewing the medicine on its own.
>
> **Why it matters:** This is the standard communication language between the LLM and the code runtime — the foundation of every modern agent and the way an LLM manipulates the outside world.

Plain glosses:

- **Schema** = a declared form/template: which fields a call must have and their types. The model fills the form; code checks it.
- **Parallel calls** = asking for several tools in one turn, so they run at the same time instead of one after another.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/06-5-function-calling.py`](examples/06-5-function-calling.py)

</details>

> **One-line summary:** Function calling turns the LLM's words into filled-in forms (schema-valid JSON tool calls), letting it press buttons in the outside world — several at once if needed.

---

## 6. Tool Decision Pipeline

> **📌 Core Concept**
>
> **Definition:** The Tool Decision Pipeline is the end-to-end process from receiving the user query → intent classification → tool matching → parameter extraction and validation → execution → result validation, ensuring every step is controlled and logged.
>
> **Metaphor:** Like a factory assembly line: the first station sorts the raw material (intent classification), the middle stations pick the machine and load the material (tool matching + parameters), and the final station inspects the product before it leaves the plant (result validation).
>
> **Why it matters:** Fitting the whole tool decision into a single pipeline makes it easy to add guardrails, easier to debug, and easier to extend without breaking other parts.

In other words: instead of scattering tool logic across the codebase, one pipeline owns every step, in a fixed order. When something breaks, you know exactly which station failed.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-6-tool-decision-pipeline.py`](examples/07-6-tool-decision-pipeline.py)

</details>

> **One-line summary:** One assembly line for every tool call — intent → match → validate → execute → verify — so safety checks and debugging have a single home.

---

## 7. Tool Composition

> **📌 Core Concept**
>
> **Definition:** Tool Composition is the technique of combining multiple tool calls — sequential (chain), parallel, conditional, or fan-out/fan-in (pipeline) — to solve complex tasks that a single tool cannot handle.
>
> **Metaphor:** Like cooking a dish: several kitchen tools (chopping, boiling, stir-frying) must run in the right order, some steps run in parallel (boiling vegetables while making the sauce), and some steps branch based on a check.
>
> **Why it matters:** Most real tasks need two or more tools; knowing how to compose them into a workflow is the jump from an agent that calls tools individually to one that completes whole processes.

Plain glosses for the composition styles:

- **Chain** = tool B runs on tool A's output, one after another.
- **Parallel** = several tools run at the same time.
- **Conditional** = pick the next tool based on a check ("if the search found nothing, try the fallback").
- **Fan-out/fan-in** = fire many calls at once (fan-out), then collect and merge all results (fan-in).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-7-tool-composition.py`](examples/08-7-tool-composition.py)

</details>

> **One-line summary:** Complex jobs need tool recipes, not single tools: chain them in order, run some in parallel, branch on checks, and fan-out/fan-in for bulk work.

---

## 8. Permission System

> **📌 Core Concept**
>
> **Definition:** The Permission System is an RBAC (Role-Based Access Control) mechanism that controls which user may call which tool, based on role (guest/user/power_user/admin) and permission level (public/standard/elevated/admin), with an audit log for every allow/deny decision.
>
> **Metaphor:** Like company access cards: visitors can only enter the lobby, employees enter the office, and only managers reach the server room — every card swipe leaves a trace (audit log).
>
> **Why it matters:** Tools like `write_file` or `execute_python` can cause irreversible damage; a permission system is the barrier that stops unintended agent side effects.

Plain glosses:

- **RBAC** = permissions attach to roles, not to individuals. You get rights by being "an admin", not by being "Alice".
- **Audit log** = a permanent record of every allow/deny decision, so you can answer "who did this?" later.

> 🔑 **Policy / Permission highlight:** this section is the **policy & permission decision point** — RBAC role → permission level → allow/deny + audit. Enforcement lives in `12-sandbox-execution` (§6 policy matrix), human overrides in `15-approval-gates`, and pre-execution checks in `tools/guardrails`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/09-8-permission-system.py`](examples/09-8-permission-system.py)

</details>

> **One-line summary:** RBAC decides who may call which tool — role maps to permission level, every decision is logged — blocking dangerous tools like `write_file` from unauthorized hands.

---

## 9. Rate Limiting

> **📌 Core Concept**
>
> **Definition:** Rate Limiting is the mechanism that caps how many tool calls can happen in a time window (e.g. at most 60 calls per minute), using strategies such as fixed window, sliding window, or token bucket to control the token budget, block abuse, and keep the system stable.
>
> **Metaphor:** Like a pressure-reducing valve on a water tank: water still flows, but with a cap — preventing one pipe from draining the whole supply (abuse) and avoiding a burst pipe (overload).
>
> **Why it matters:** When an agent loop makes hundreds of tool calls in a minute, the rate limit is the life preserver that protects both the cost and the health of the system.

Plain glosses for the three strategies:

- **Fixed window** = a simple counter per time slot (e.g. "60 calls this minute", reset each minute).
- **Sliding window** = a rolling 60-second window, so bursts at slot boundaries can't sneak in double.
- **Token bucket** = a bucket that refills at a fixed rate; each call spends one token, so steady use flows but bursts are capped.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-9-rate-limiting.py`](examples/10-9-rate-limiting.py)

</details>

> **One-line summary:** Rate limiting caps calls per time window (fixed window, sliding window, or token bucket) so a runaway agent loop can't burn the token budget or crash the system.

---

## 10. Harness Integration

> **📌 Core Concept**
>
> **Definition:** Harness Integration is the layer that connects the Tool Decision module to the whole Harness Framework — Memory, Guardrails, Feedback, Permissions — through unified TypeScript interfaces.
>
> **Metaphor:** Like the standard connector on a multi-purpose vacuum cleaner: every attachment (brush, nozzle, hose) plugs into the same port — the TypeScript interface is that standard connector that lets harness modules snap together.
>
> **Why it matters:** A module is only valuable when it can plug into a real harness; unified interfaces make it fast to connect, easy to test each module in isolation, and safe when other modules change.

### 10.1 TypeScript Interfaces

This section is the TypeScript contract that defines what a tool decision system must look like for the harness to use it: register/get/list/search tools, `classifyIntent`, `executeTool`/`executeChain`/`executeParallel`, plus `checkPermission`/`checkRateLimit` and `getStats`. How to read it: the `interface` part describes the required data shape (an interface = a contract listing required functions and their types, like a job description the module must satisfy), and the `HarnessToolDecisionSystem` class is a reference implementation showing the order of a real tool call: check permission → check rate limit → execute → record metrics. If you write your own module, satisfying the interface is all the harness needs to use it.

*Analogy:* Like an office lease: the interface is the set of mandatory clauses, and the class is the concrete implementation each party writes on its own.

<details>
<summary><b>10.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/11-10-1-typescript-interfaces.ts`](examples/11-10-1-typescript-interfaces.ts)

</details>

> **One-line summary:** One TypeScript contract makes the tool module pluggable: satisfy the interface and the harness can wire you into Memory, Guardrails, Feedback, and Permissions.

---

## 11. Case Studies

> **📌 Core Concept**
>
> **Definition:** Real-World Case Studies are detailed analyses of tool-use architectures actually running in leading AI products (SWE-agent, Claude Code, Cursor IDE, DeepSeek Harness) from which you can extract immediately applicable design lessons.
>
> **Metaphor:** Like reading a famous chef's case study: not to copy the recipe verbatim, but to see the principles (sequence, safety, context) and adapt them to your own cooking.
>
> **Why it matters:** These products have been optimized with real money and real user data; learning from them keeps you from reinventing a broken wheel.

### 11.1. SWE-agent — Tool-Use for Software Engineering

This case shows that fewer, better-described tools beat a big messy pile.

**Tool strategy**: Simple, focused tools with clear descriptions.

```
Tools: read_file, search_code, edit_file, run_command

Key insight: "Read before edit" — SWE-agent always reads files first
to understand context before making changes.
```

**Result**: 20.5% success rate on SWE-bench (+64% over baseline). (SWE-bench = a benchmark of real GitHub bug-fixing tasks; baseline = the previous unimproved score.)

> **One-line summary:** SWE-agent wins with few, clearly described tools and one rule — always read a file before editing it — lifting its benchmark score 64%.

### 11.2. Claude Code — Hierarchical Tool Access

This case shows permissions arranged in layers: the higher the layer, the more damage the tools can do, and the more control they need. (Hierarchical = arranged in levels, like floors of a building.)

**Tool strategy**: Layered permissions, tool composition.

```
Layer 1 (always available): read_file, search_code
Layer 2 (standard): write_file, run_tests
Layer 3 (elevated): execute_command, delete_file
Layer 4 (admin): push_code, deploy
```

Reading the layers: Layer 1 tools only look, so they are always on. Layer 2 changes files but safely. Layer 3 runs commands and deletes — needs elevated permission. Layer 4 touches the outside world (push, deploy) — admin only.

> **One-line summary:** Claude Code gates tools by damage level in four layers — from read-only (always on) up to push/deploy (admin only) — so risk buys access.

### 11.3. Cursor IDE — Context-Aware Tool Selection

This case shows tool choice driven by editor context. (Context-aware = the agent looks at its current surroundings — which file is open, what text is selected — before deciding.)

**Tool strategy**: Select tools based on editor context.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/12-11-3-cursor-ide-context-aware-tool-selection.ts`](examples/12-11-3-cursor-ide-context-aware-tool-selection.ts)

</details>

> **One-line summary:** Cursor picks tools from what the user is looking at right now — the open file and selection steer which tool fits.

---

### 11.4. DeepSeek Harness — Code Mode SDK (`@deepseek-ai/dsh`)

**Context**: DeepSeek Harness provides **Code Mode** — a runtime mode optimized for single-turn coding tasks. It uses the `@deepseek-ai/dsh` SDK to execute code inside a Node.js `vm` sandbox (vm sandbox = an isolated jail where code runs with no network and no file access outside allowed paths) with batched tool operations, cutting **70-90% of latency and token costs** compared to a multi-turn agent loop.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/13-11-4-deepseek-harness-code-mode-sdk-deepseek.ts`](examples/13-11-4-deepseek-harness-code-mode-sdk-deepseek.ts)

</details>

**Key Innovations**:

1. ✅ **Single-turn Execution** — The entire task runs in one script, no multi-turn LLM loop needed
2. ✅ **Batched Tool Calls** — `batchTools([...])` groups many tool calls into a single execution, cutting **70-90% of latency**
3. ✅ **VM Sandbox Isolation** — Node.js `vm` context, no network, no filesystem outside allowed paths
4. ✅ **Deterministic Replay** — Same script + same input = same output. Easy to debug, test, and run in CI/CD (CI/CD = the automated build-and-test pipeline of a project)
5. ✅ **Token Cost Reduction** — No need to send tool results back to the LLM to decide the next step. The LLM is called only once (or zero times for pure code)
6. ✅ **Parallel by Default** — `batchTools` runs all tools in parallel automatically

**Code Mode vs Standard Mode**:

How to read it: each row compares one aspect (first column) between the usual multi-turn agent (middle column) and Code Mode (right column). For instance, the "Turns" row means Standard Mode needs 5–20+ LLM round trips while Code Mode needs exactly one.

| Aspect | Standard Mode | Code Mode (`@deepseek-ai/dsh`) |
|--------|---------------|-------------------------------|
| **Turns** | Multi-turn (5-20+) | Single-turn (1) |
| **Latency** | High (sequential LLM calls) | Low (batched, parallel) |
| **Token Cost** | High (full context each turn) | **70-90% less** |
| **Tools** | All tools | `bash`, `editor`, `llm_complete` only |
| **Isolation** | Process-level | VM sandbox (stronger) |
| **Determinism** | Non-deterministic | Deterministic (script-based) |
| **Use Case** | Open-ended tasks | Well-defined coding tasks |

**File Reference**: For implementation details, see [`code-mode-sdk.md`](code-mode-sdk.md)

> **One-line summary:** Code Mode runs the whole coding task as one sandboxed script with batched parallel tool calls, cutting 70-90% of latency and tokens versus a multi-turn loop.

---

## 12. Design Principles

> **📌 Core Concept**
>
> **Definition:** Design Principles are the set of software architecture guidelines — specifically applying the SOLID principles to a tool management and orchestration system.
>
> **Metaphor:** Like urban planning setting standards before issuing building permits: you don't need to know the details of every house, but everyone must follow the same code so the city doesn't become a mess.
>
> **Why it matters:** The tool ecosystem grows new tools every day; designing with SOLID lets you add new tools without breaking old ones.

(SOLID = five classic software design rules; the acronym letters stand for the five rules listed below.)

### 12.1 SOLID for Tools

**1. Single Responsibility**
- Each tool does one clear job, like one kitchen gadget per task
- Don't mash search + write into a single tool

**2. Open/Closed**
- Stay open to new tools: just register them
- Keep shipped tools steady instead of rewriting them

**3. Liskov Substitution**
- Every tool speaks the same shared interface
- So one tool can step in for another without surprises

**4. Interface Segregation**
- Keep tool definitions apart from running them
- Keep permission checks apart from the executor

**5. Dependency Inversion**
- Tools lean on the shared ToolRegistry idea
- Never hard-wire one tool's code into another

> **One-line summary:** SOLID for tools means: one job per tool, add without breaking, swap tools freely, split definition from execution, and depend on the registry contract — not on each other's internals.

---

## 13. Best Practices

> **📌 Core Concept**
>
> **Definition:** Best Practices are the collection of do's, don'ts, and optimization strategies distilled from hands-on experience building tool decision systems.
>
> **Metaphor:** Like a workplace safety handbook: it spells out the correct procedure (DO) and the warnings (DON'T) so newcomers don't have to learn the hard way by causing a breakdown.
>
> **Why it matters:** Most failures in tool systems come from avoidable mistakes; this list lets you inherit those lessons without paying the price yourself.

### 13.1 DO ✅

Healthy habits for a tool system that stays fast and safe:

- **Check parameters before running**: it stops silly errors early
- **Retry with exponential backoff**: don't pound a failing service
- **Write down every tool call**: logs make debugging and tuning possible
- **Always set a timeout**: so no call hangs forever
- **Check permissions first**: security comes before convenience
- **Watch the cost per call**: small fees add up without a budget
- **Describe each tool plainly**: the LLM can only pick what it understands
- **Keep both rule-based and LLM-based intent**: quick rules plus smart fallback is the best mix
- **Cache the tool list**: no need to re-fetch it on every call
- **Keep a backup tool in mind**: when the first choice fails, try the next

> **One-line summary:** Do the boring safety work every time: validate inputs, cap waits, log calls, check permissions, describe tools clearly, and always have a fallback.

### 13.2 DON'T ❌

Easy-to-make mistakes that break tool systems — dodge them from day one:

- **Don't skip parameter checks**: bad inputs mean crashes
- **Don't blow past rate limits**: API bans hurt
- **Don't hard-wire tool paths**: let the registry look them up
- **Don't assume calls always work**: every tool call can fail, so handle it
- **Don't write fuzzy tool blurbs**: the LLM can't guess what you meant
- **Don't retry forever**: always cap your retries
- **Don't run risky tools unchecked**: always confirm auth first
- **Don't leave old tools rotting**: migrate users off deprecated tools gently

> **One-line summary:** The classic failures — unvalidated inputs, ignored rate limits, hardcoded paths, endless retries, unguarded risky tools — are all preventable if you never assume a call will just work.

---

## 14. Testing

> **📌 Core Concept**
>
> **Definition:** Testing is the process of building unit tests and integration tests to evaluate the accuracy of each component — tool selection, intent classification, executor, permission, rate limiter — and of the pipeline as a whole.
>
> **Metaphor:** Like a dress rehearsal before showtime: each actor lines their own part (unit test), and the whole cast runs the script straight through (integration test) to catch errors before the real stage (production).
>
> **Why it matters:** A failed tool call is the most expensive error once you're live; testing early catches bugs at a point where the cost of fixing them is nearly zero.

Plain glosses:

- **Unit test** = tests one small piece in isolation (e.g. "does the intent classifier tag 'search the docs' as a search intent?").
- **Integration test** = tests the pieces connected together (e.g. "does a full query travel the whole pipeline and return the right answer?").

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/14-14-testing.py`](examples/14-14-testing.py)

</details>

> **One-line summary:** Unit-test each part, integration-test the whole pipeline — catching tool bugs in rehearsal costs almost nothing compared to a live failure.

---

## 15. Advanced Patterns

> **📌 Core Concept**
>
> **Definition:** Advanced Patterns cover deeper techniques such as Tool Learning — the ability of an agent to learn how to use new tools at runtime — along with dynamic tool registration (adding tools to the registry while the system is running, without a redeploy).
>
> **Metaphor:** Like a new sales employee: the first days they have to check the manual for everything, but after a few months they instinctively know which item sells fast and which step loses customers — the system absorbs the lessons over time instead of waiting for someone to fix the code.
>
> **Why it matters:** The longer a system runs, the more finely tuned it becomes — higher success rates and lower latency without manual intervention.

### 15.1 Tool Learning

What does this section give you? `ToolLearner` records every time the agent calls a tool: the task type, which tool, whether it succeeded, and the latency (the `record` function). When a tool needs to be picked for a task, `recommend()` ranks the candidates by success rate minus a latency penalty; a tool that has never been used gets a neutral score of 0.5. Simple idea, but it is the foundation of self-optimizing agents: the system learns from its own history instead of hand-patched code.

*Analogy:* Like a ride-hailing app that remembers which drivers are punctual and fast, so it prioritizes booking with them next time.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/15-15-1-tool-learning.py`](examples/15-15-1-tool-learning.py)

</details>

> **One-line summary:** Tool Learning keeps a scorecard per tool (success rate, latency) and recommends the best-ranked candidate — the agent improves from its own track record.

---

## 16. Future

> **📌 Core Concept**
>
> **Definition:** The Future reflects the prominent technology trends in tool decision and MCP for 2026-2028: protocol standardization, automatic tool discovery and wrapper generation for unfamiliar tools, plus multi-agent tool sharing.
>
> **Metaphor:** Like a weather forecast before a long trip: not 100% certain, but it helps you pack (design your architecture) in the right direction from today.
>
> **Why it matters:** Architecture decisions made today determine whether the system can keep up with the next 2-3 years of trends or has to be rebuilt from the ground up.

(Wrapper = a small adapter program that wraps an unfamiliar tool so it looks like a standard tool your system already knows how to call.)

### 16.1 Trends 2026-2028

**1. Auto Tool Discovery**
- Agents discover tools from MCP servers automatically
- Auto-generated wrappers for unknown tools
- Semantic tool matching (matching by meaning, not just by name)

**2. Tool Composition AI**
- Agents compose tools into workflows automatically
- Learned tool chains from execution history
- Self-optimizing pipelines

**3. Cross-Platform Tools**
- Tool portability across agents
- Standardized tool marketplace
- Universal tool interface

**4. Predictive Tool Use**
- Predict which tools will be needed
- Pre-warm connections
- Pre-fetch data

**5. Tool Security**
- Zero-trust tool execution (zero-trust = trust nothing by default; verify every call)
- Sandboxed tool environments
- Audit trail for all operations

> **One-line summary:** Expect agents that find, wrap, compose, and pre-warm tools on their own — with zero-trust security and full audit trails as the price of admission.

---

## 17. Production Hardening: MCP, Execution Boundaries, Memoization

> **Ownership note.** This section covers what the *tool layer* owns: the MCP client, the
> capability declarations a tool must publish, and memoization. The **isolation policy**
> (tiers, the five mandatory controls, the hardened runner) is owned by
> [`12-sandbox-execution`](../12-sandbox-execution/README.md); the **human verdict**
> (risk tiers, gate payload, timeout-deny) is owned by
> [`15-approval-gates`](../15-approval-gates/README.md). Both are cross-cutting modules that
> wrap every tool call. This module declares *what a tool needs*; 12 and 15 decide *whether it gets it*.

(Production hardening = making a system safe and stable for real users, not just demos.
Memoization = remember the result of an identical call and return the cached copy instead of re-running.)

### 17.1 Definitions

How to read it: each row defines one term. **Term** is the concept; **Definition** explains it in one line; **Owner** says which module is responsible for enforcing it. For instance, the "Sandbox" row means: running untrusted code is *not* this module's job — module `12-sandbox-execution` owns it.

| Term | Definition | Owner |
|------|------------|-------|
| Sandbox | Untrusted tool/code runs in Docker/microVM/gVisor with FS allowlist, no net (default), timeout+kill, no secret env | → `12-sandbox-execution` |
| MCP production client | Auth (OAuth/key rotation), `protocolVersion` pin + capability cache with TTL, `tools/list` ETag, result size caps + truncation | this module |
| Dangerous-op gate | Write/exec/network/publish requires explicit approval record (who, what, diff, expiry) | → `15-approval-gates` |
| Memoization | Identical `(tool, args_hash)` within TTL returns cached result; streaming yields partial chunks with cap | this module |

Plain-language glosses for the terms inside the table:

- **Docker/microVM/gVisor** = technologies that run code in an isolated jail, so a misbehaving tool can't touch the host machine.
- **FS allowlist** = only files/folders on an explicitly allowed list ("danh sách trắng") can be read or written; everything else is refused.
- **No secret env** = passwords and API keys are not passed into the sandbox as environment variables.
- **OAuth/key rotation** = sign in via a standard login protocol, and swap keys regularly so a leaked key dies fast.
- **`protocolVersion` pin** = fix which protocol version you speak, per request, so a server upgrade can't break you silently.
- **TTL** (time-to-live) = how long a cached item stays valid before it must be refreshed.
- **ETag** = a version stamp a server puts on data; if the stamp is unchanged, your cached copy is still fresh.
- **args_hash** = a fingerprint of the call's arguments; same fingerprint = same call = cache hit.
- **Approval record (who, what, diff, expiry)** = the human approval must state who approved, what exactly, what changed, and when the approval expires.

> **One-line summary:** This module owns the MCP client, capability declarations, and memoization; sandboxes belong to `12-sandbox-execution` and human approval to `15-approval-gates`.

### 17.2 Execution Boundaries — What This Module Owns

This section draws the line between *declaring* what a tool may do and *enforcing* it. The tool registry is where a tool *declares* its blast radius (blast radius = how far the damage can spread if the tool misbehaves); `12-sandbox-execution` is where
that declaration is *enforced*. This module's job is to keep the declaration honest:

1. **Every tool publishes its capabilities**, not just its parameters. Alongside `path`/`query`,
   a tool declares `net: ["api.example.com"]`, `allowWrite: ["src/**"]`, `secrets: ["EXAMPLE_API_KEY"]`,
   and `irreversible: boolean`. (net = which hosts it may contact; allowWrite = which file paths it may modify; secrets = which credentials it needs; irreversible = the action cannot be undone.) A tool that declares nothing gets the default-deny profile (default-deny = anything not explicitly allowed is refused).
2. **The declaration is versioned and reviewable.** Changing `irreversible: false → true` is a
   security-relevant diff and must go through the same review as a code change — the gate
   tiers in `15-approval-gates` are keyed off these fields.
3. **The executor refuses to widen.** If a tool's runtime asks for more than it declared
   (a write outside `allowWrite`, an egress host not in `net` — egress = outbound network access), the harness denies the call and
   emits a `tool_result` with `error: "capability-escalation"` — it does not silently allow.
4. **Rate limits and timeouts are per-tool declarations too** (`rate_limit_per_minute`,
   `timeout_seconds` in `ToolDefinition` above), and the sandbox deadline in `12` must be
   `≥` the tool timeout so the outer deadline never fires before the inner one reports.

The full rule set — isolation tiers, filesystem allowlist, network deny-by-default,
deadline + process-group kill, output caps, secret containment, per-role policy matrix,
and the hardened runner that pins images by digest (digest = an exact fingerprint of a container image, so nobody can swap it for a tampered version) — lives in
[`12-sandbox-execution`](../12-sandbox-execution/README.md). Read that module before writing
any code that spawns a subprocess.

> **One-line summary:** Every tool must honestly declare what it can touch (network, files, secrets, irreversibility); the executor refuses any attempt to exceed that declaration.

### 17.3 MCP Production Rules

> **Oct-2026:** the stateless spec `2026-07-28` is the latest.
> Step-by-step move in [`2026-07-28-migration.md`](./2026-07-28-migration.md).
> The old `initialize` handshake and `Mcp-Session-Id` are gone.

(Stateless = the server keeps no memory of the connection between calls; every request stands alone.)

1. Pin `protocolVersion` **per request** (`_meta` + `MCP-Protocol-Version` header, default `"2026-07-28"`, keep `"2025-06-18"` compat shim); cache `tools/list` per `ttlMs/cacheScope` (fallback 5–15 min); on `426`/unknown-tool/`UnsupportedProtocolVersionError` invalidate immediately. (Compat shim = a small compatibility layer so older versions still work. `426` = the HTTP "Upgrade Required" error.)
2. Auth: OAuth2 bearer with refresh + least-scope; rotate keys; never log tokens (redact `Bearer`). (Least-scope = request the minimum permissions possible; redact = mask the token before writing it to any log.)
3. Caps: `timeout 30s`, `result ≤128KB`, `args ≤32KB`, schema-validate args pre-send. (Caps = hard maximum sizes/times; anything bigger is cut off.)
4. Streaming: forward `content` chunks as they arrive, enforce total cap + idle timeout (10s); abort on client cancel. (Idle timeout = if nothing arrives for 10 seconds, give up.)

<details>
<summary>TypeScript Code — MCP Call + Memoization (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-17-3-mcp-production-rules.ts`](examples/16-17-3-mcp-production-rules.ts)

> The sandboxed subprocess runner that used to sit here has moved to
> [`12-sandbox-execution` §4.2](../12-sandbox-execution/README.md), which pins the image by
> digest, guards path traversal via `realpath`, enforces an idle timeout, and redacts
> secrets from output. Do not reintroduce a `:latest`-tagged runner here.

</details>

> **One-line summary:** In production, pin the protocol version per request, cache with TTLs, rotate auth, cap sizes and timeouts, and stream with an idle cutoff.

### 17.4 Dangerous-Op Approval UX

This section explains what the human sees when a dangerous operation asks for approval — the consent screen is part of the tool's design, not an afterthought.

The tier taxonomy, the mandatory-evidence gate payload, timeout-deny (fail closed), and the
`approval_request` / `approval_verdict` audit trail are all owned by
[`15-approval-gates`](../15-approval-gates/README.md). (Fail closed = if the approver doesn't answer in time, the call is *denied*, never allowed.) What stays here is the **tool-side
consent UX**, because a tool definition is where the approver learns what they are approving:

- **Render from the declaration, not from raw args.** The gate shows `command`, `cwd`, files
  touched, net egress, and the `irreversible` flag — all of which come from the tool's declared
  capabilities (§17.2), not from re-parsing `args` at approval time. (cwd = the working directory the command would run in.)
- **A tool with no declared capabilities renders as an unknown blast radius**, which forces the
  highest tier. Never let a tool appear safer than it is.
- **One-click for `write/exec`, typed confirm for `publish/delete/auth-change`** — but the
  expiry window and the two-person rule come from `15`, not from here. (Typed confirm = the approver must type a phrase, not just click OK.)
- **MCP tools get a server badge** in the consent prompt. Approving a call to a remote MCP
  server is a different trust decision from approving a local subprocess.

> **One-line summary:** The approval screen must show what the tool declared (command, files, network, irreversibility) — never parse raw args — and undeclared tools look maximally dangerous, on purpose.

### 17.5 Checklist

Run this list before shipping; each box is one safety property to confirm.

- [ ] Every tool declares `net` / `allowWrite` / `secrets` / `irreversible`? Undeclared = default-deny?
- [ ] Sandbox controls verified against `12-sandbox-execution` (net-off, FS allowlist, timeout+SIGKILL, output cap, no secret env, digest-pinned image)? (SIGKILL = the operating-system kill signal that terminates a process immediately.)
- [ ] MCP: version pinned, caps cached w/ TTL + invalidate, auth rotated, size/timeout caps?
- [ ] Dangerous ops gated with diff preview + expiring approval record, per `15-approval-gates`?
- [ ] Identical-call memo keyed on canonical args hash with TTL; streaming capped?

> **One-line summary:** Five boxes to tick before production: declarations published, sandbox verified, MCP hardened, dangerous ops gated, memoization capped.

---

## Reference Materials

This section lists the sources: research papers (for the theory) and frameworks (for the practice). Each entry has a link you can follow.

### Papers & Research

1. **Toolformer: Language Models Can Teach Themselves to Use Tools**
   - Schick et al., 2023
   - https://arxiv.org/abs/2302.04761

2. **Gorilla: Large Language Model Connected with Massive APIs**
   - Patil et al., 2023
   - https://arxiv.org/abs/2305.15334

3. **API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs**
   - Li et al., 2023
   - https://arxiv.org/abs/2304.08354

4. **NexusRaven: Function Calling for LLMs**
   - Nexusflow, 2023
   - https://arxiv.org/abs/2312.15933

### Frameworks & Tools

1. **MCP (Model Context Protocol)** - https://modelcontextprotocol.io
2. **OpenAI Function Calling** - https://platform.openai.com/docs
3. **Anthropic Tool Use** - https://docs.anthropic.com
4. **LangChain Tools** - https://langchain.com
5. **Semantic Kernel** - https://learn.microsoft.com/semantic-kernel

> **One-line summary:** The primary sources: four research papers that founded tool-using LLMs, and five frameworks you can build with today.

---

*Document: VI. Decide Tools / MCP Calls — HARNESS ENGINEERING EDITION*
*Last updated: 16/10/2026 (stateless 2026-07-28: see 2026-07-28-migration.md)*
*Author: AI Knowledge Repository*

*Updated: 10/2026 — MCP Ecosystem & Code Execution Pattern*

---

## October 2026 Update — MCP Ecosystem & Code Execution Pattern

> **📌 Summary**
>
> In October 2026, the MCP ecosystem has advanced remarkably: the `2026-07-28` spec is complete, a wide range of AI clients support it (Claude, ChatGPT, VS Code, Cursor, MCPJam...), and most importantly — the **code execution with MCP** pattern (Anthropic 11/2025) lets the agent write code to call MCP tools instead of exposing dozens of individual tools, significantly reducing tokens and latency.

This closing section is a dated snapshot: what changed in the MCP world recently and the one big new pattern worth adopting. Spec = the official protocol specification document.

### 1. MCP Ecosystem 2026 — "USB-C for AI"

How to read it: each row names one piece of the MCP ecosystem and what it is. For instance, the "MCP Apps" row means: full applications can now run *inside* AI clients, not just bare tools.

**MCP** (Model Context Protocol) is increasingly becoming the standard tool-connection protocol for AI agents. The `2026-07-28` spec finalizes many new features:

| Component | Description |
|---|---|
| **Spec** | `2026-07-28` — fully defines tools, resources, prompts, sampling |
| **MCP Apps** | Applications running inside AI clients (Cursor, VS Code, Claude Desktop...) |
| **Wide support** | Claude, ChatGPT, VS Code, Cursor, MCPJam, many others |
| **Original tagline** | MCP = "USB-C for AI" — unified connectivity instead of one style per vendor |

> **MCP vs A2A distinction:** Two complementary protocols:
> - **MCP** (Model Context Protocol): Agent → Tool (call tools/services)
> - **A2A** (Agent-to-Agent): Agent → Agent (communication between agents)
>
> A2A has been integrated into the [Agentic AI Foundation 08/2026](https://github.com/agentprotocol/A2A) — Layer 4. MCP and A2A coexist, serving two different needs.

(Complementary = they don't compete; each covers a different need. MCP is the agent's hand reaching for tools; A2A is agents talking to each other.)

> **One-line summary:** MCP is now the standard "USB-C for AI" — one spec, support in every major client, and it pairs with A2A (agent-to-agent talk) without competing with it.

### 2. Code Execution Pattern with MCP (Anthropic 11/2025)

This section explains the newest big idea: instead of showing the model 50 tool menus, let the model write one small script that calls the tools — and ship back only the summary.

**The old problem:** When the agent connects to many MCP servers (each server has 5–10 tools), the total can reach 50–100 tools. Every tool description must sit in the context of each LLM call → costly in **tokens + latency**.

**Solution — the agent writes code to call MCP tools:**

```
┌─────────────────────────────────────────────────────────────┐
│              CODE EXECUTION WITH MCP                        │
│                                                             │
│  Agent viết code:                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ # Agent viết code để gọi tool                       │   │
│  │ results = await mcp_batch([                          │   │
│  │   {"server": "filesystem", "tool": "read",           │   │
│  │    "args": {"path": "/data/a.txt"}},                │   │
│  │   {"server": "web", "tool": "search",                │   │
│  │    "args": {"query": "bug fixes"}},                 │   │
│  │   {"server": "db", "tool": "query",                 │   │
│  │    "args": {"sql": "SELECT * FROM logs"}},          │   │
│  │ ])                                                   │   │
│  └─────────────────────────────────────────────────────┘   │
│       │                                                    │
│       ▼                                                    │
│  Sandbox executor chạy code → gọi MCP servers              │
│       │                                                    │
│       ▼                                                    │
│  Chỉ TRẢ VỀ KẾT QUẢ TỔNG HỢP cho context                  │
│       (giảm token đáng kể so với expose 50+ tools)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

(Read the diagram top to bottom: the agent writes one script that batches several tool calls; a sandbox runs it; only the merged result returns to the model's context, not 50 tool menus.)

**Comparing the two approaches:**

How to read it: each row is one criterion; the middle column is the old "list every tool" approach; the right column is the new "agent writes code" approach. For instance, the "Tools in context" row means the old way stuffs 50–100 tool descriptions into every prompt, while the new way needs just one tool: `mcp_batch_execute`.

| Criteria | Expose each tool individually | Code execution pattern |
|---|---|---|
| Tools in context | 50–100 tool descriptions | 1 tool `mcp_batch_execute` |
| Token cost | High (each tool × each call) | Low (only aggregated results) |
| Latency | Grows with number of tools | Comparable to 1 tool call |
| Best for | < 20 tools | Many MCP servers, many tools |
| Code complexity | Low | Medium (needs sandbox executor) |

> **One-line summary:** With many MCP servers, let the agent write one sandboxed script that batches tool calls and return only the summary — this slashes tokens and latency versus listing every tool.

### 3. Tool Design — Action Centered Intelligence (ACI)

This section explains how to write tool descriptions the model can actually use. (ACI = designing tools centered on the *action* the model must take, with clarity as the top goal.)

Tool descriptions should be written like **docstrings for a junior developer** — clear, complete, unambiguous. (Docstring = the explanation comment attached to a function.)

> 📄 **Example code:** [`examples/17-3-tool-design-action-centered-intelligence-aci.py`](examples/17-3-tool-design-action-centered-intelligence-aci.py)

**4 ACI tool design principles:**

1. **Descriptions = docstrings for a junior dev** — describe input/output/error clearly, no abbreviations
2. **Format close to natural text** — tool names use underscores, descriptions in sentence form
3. **Poka-yoke params** — use absolute paths, enums instead of free-form strings, clear defaults (Poka-yoke = a Japanese manufacturing term for "mistake-proofing": design the input so errors are impossible, like a USB plug that only fits one way; enum = a fixed list of allowed values)
4. **Test tools with real inputs** — don't just write descriptions; actually run them, especially edge cases (edge cases = rare or extreme situations, like an empty file or a 10,000-character path)

**Avoid bloated toolsets:** 10 good tools beat 50 "decent" tools.

> **One-line summary:** Write tool descriptions like instructions for a junior dev, make parameters mistake-proof, test with real inputs — and prefer 10 sharp tools over 50 vague ones.

### 4. Python — Sandbox Executor Pattern

This section shows how to run the agent-written code safely: the sandbox executor pattern. (Sandbox executor = a runner that executes the agent's script inside an isolated jail — no network, limited files, capped time.)

> 📄 **Example code:** [`examples/18-4-python-sandbox-executor-pattern.py`](examples/18-4-python-sandbox-executor-pattern.py)

> **One-line summary:** Agent-written code must run in a sandbox executor — isolated, file-limited, time-capped — so the code-execution pattern stays safe.

### 5. Cross-links

This section points to related documents in the repo for the wider architecture picture.

- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)
- [agent-skills-spec.md](../05-prompt-builder/agent-skills-spec.md) — Agent Skills Open Standard (agentskills.io)

> **One-line summary:** For the whole-system view, read the architecture doc and the Agent Skills standard next.

*Author: AI Knowledge Repository*
