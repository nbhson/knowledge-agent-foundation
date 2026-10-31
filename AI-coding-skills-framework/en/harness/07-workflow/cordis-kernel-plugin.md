# 🧩 Micro-Kernel Architecture & Plugin Ecosystem — The "Everything is a Plugin" Philosophy

> **Pattern inherited from DeepSeek Harness & Cordis**: The core concept is **"Agent = Model + Harness"**. The entire Harness Engine is designed around the **Micro-Kernel** super-architecture (a micro-kernel based on the Cordis framework). Every feature — from Tools, Runtimes, and the Memory Engine to Guardrails and UI Components — is a **Plugin** that can be plugged in/removed and extended flexibly.

---

## 📑 Table of Contents

- [🧩 Micro-Kernel Architecture \& Plugin Ecosystem — The "Everything is a Plugin" Philosophy](#-micro-kernel-architecture--plugin-ecosystem--the-everything-is-a-plugin-philosophy)
  - [📑 Table of Contents](#-table-of-contents)
  - [1. Core Philosophy: Agent = Model + Harness](#1-core-philosophy-agent--model--harness)
  - [2. Micro-Kernel Architecture (Cordis Pattern)](#2-micro-kernel-architecture-cordis-pattern)
    - [The Kernel's role:](#the-kernels-role)
  - [3. The Plugin's Lifecycle (Lifecycle Management)](#3-the-plugins-lifecycle-lifecycle-management)
  - [4. 4 Runtime Modes in DeepSeek Harness](#4-4-runtime-modes-in-deepseek-harness)
    - [4.1. Standard Mode (Standard Agent)](#41-standard-mode-standard-agent)
    - [4.2. Code Mode (SDK-Driven Execution)](#42-code-mode-sdk-driven-execution)
    - [4.3. Minimal Mode (Isolating Benchmark)](#43-minimal-mode-isolating-benchmark)
    - [4.4. Creator Mode (Runtime Inspection \& Preset Authoring)](#44-creator-mode-runtime-inspection-&-preset-authoring)
  - [5. Illustrative Kernel Engine Implementation (TypeScript)](#5-illustrative-kernel-engine-implementation-typescript)
    - [Example of registering a Plugin:](#example-of-registering-a-plugin)
  - [6. DeepSeek Harness Monorepo \& pnpm Workspace Structure](#6-deepseek-harness-monorepo-&-pnpm-workspace-structure)
  - [7. Best Practices \& Design Principles](#7-best-practices-&-design-principles)
    - [✅ Best Practices](#-best-practices)
    - [❌ Anti-Patterns](#-anti-patterns)

---

## 1. Core Philosophy: Agent = Model + Harness

This section explains the founding idea: the "brain" and the "workshop" are two separate things.

In the old generation of AI Agent engineering, the whole application was typically locked into a monolithic framework (for example: one large codebase file containing hardcoded prompts, hardcoded tools, and fixed execution loops — monolithic = one big block you cannot take apart).

DeepSeek Harness redefines this architecture through the formula:

$$\text{Agent} = \text{Model} + \text{Harness}$$

- **Model**: Reasoning, language, and general knowledge capabilities (LLM/SLM — the AI itself).
- **Harness**: The surrounding environment that provides Tools, Memory, Runtimes, Context, and Guardrails (guardrails = safety checks).

To ensure the Harness can evolve without having to rewrite the source code, the entire Harness follows the philosophy **"Everything is a Plugin"** (plugin = a module that plugs in and out without changing the core):

```
                       ┌────────────────────────────────┐
                       │      CORDIS MICRO-KERNEL       │
                       │ (Lifecycle, Service Registry) │
                       └───────────────┬────────────────┘
                                       │
       ┌────────────────┬───────────────┼───────────────┬────────────────┐
       ▼                ▼               ▼               ▼                ▼
 ┌───────────┐    ┌───────────┐   ┌───────────┐   ┌───────────┐    ┌───────────┐
 │ Tool      │    │ Runtime   │   │ Memory    │   │ Guardrail │    │ UI        │
 │ Plugin    │    │ Plugin    │   │ Plugin    │   │ Plugin    │    │ Plugin    │
 │ (MCP)     │    │ (4 Modes) │   │ (Vector)  │   │ (Linter)  │    │ (Web UI)  │
 └───────────┘    └───────────┘   └───────────┘   └───────────┘    └───────────┘
```

Read it as: the small kernel in the middle only manages lifecycle and services; every capability around it is a plugin you can add, remove, or replace.

> **One-line summary:** Agent = Model + Harness, and the Harness is built so every capability is a swappable plugin around a tiny core.

---

## 2. Micro-Kernel Architecture (Cordis Pattern)

This section explains the three jobs the kernel itself is allowed to do.

Cordis is an ultra-lightweight micro-kernel framework for TypeScript, using a **Context-based Dependency Injection** (dependency injection = the kernel hands you what you need, instead of you importing it yourself) and **Service Locator** (a directory where plugins register and look up services) mechanism.

### The Kernel's role:
1. **Lifecycle management**: Initializing (`apply`), activating (`fork`), and disposing (`dispose`) plugins — i.e. start, branch, and clean up.
2. **Service Locator**: Allows plugins to register Services (e.g., `ctx.memory`, `ctx.tools`, `ctx.llm`) and safely access one another.
3. **Event Emitter & Middleware**: Allows a plugin to intervene before/after an LLM call or Tool Call (middleware = a hook that sits between two steps).

> **One-line summary:** The kernel does only three things — start/stop plugins, run a service directory, and route events between them.

---

## 3. The Plugin's Lifecycle (Lifecycle Management)

This section explains the three phases every plugin goes through, from load to removal.

> 📄 **Example code:** [`examples/01-3-the-plugin-s-lifecycle-lifecycle-management.ts`](examples/01-3-the-plugin-s-lifecycle-lifecycle-management.ts)

A Plugin goes through 3 phases:
1. **Mount (`apply`)**: The Plugin is loaded into the Context, registering services or event listeners (listener = a function that runs when an event fires).
2. **Execute**: The Plugin listens to events from the Kernel (e.g., `on('before-tool-call')`) to process logic.
3. **Unmount (`dispose`)**: When the Plugin is removed, the Kernel automatically cleans up listeners and releases resources.

> **One-line summary:** A plugin mounts (registers its services), runs (listens to events), and unmounts (gets cleaned up) — all managed by the kernel.

---

## 4. 4 Runtime Modes in DeepSeek Harness

This section explains the four pre-built "personalities" the same harness can take, each just a different plugin set.

Thanks to the Micro-Kernel architecture, DeepSeek Harness can package the 4 Runtime Modes as different Plugins:

```
                  ┌─────────────────────────────────────────┐
                  │          DEEPSEEK HARNESS ENGINE        │
                  └────────────────────┬────────────────────┘
                                       │
     ┌───────────────────┬─────────────┴─────┬───────────────────┐
     ▼                   ▼                   ▼                   ▼
 ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │  STANDARD    │  │  CODE MODE   │  │   MINIMAL    │  │   CREATOR    │
 │    MODE      │  │    MODE      │  │    MODE      │  │    MODE      │
 ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
 │ Interactive  │  │ Single turn  │  │ Benchmark    │  │ Preset &     │
 │ Full Agent   │  │ SDK Script   │  │ Bash+Editor  │  │ Inspection   │
 └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

Read it as: same engine, four plugin combinations — pick the row that matches your job.

### 4.1. Standard Mode (Standard Agent)
The default interactive environment. Provides the full toolset (File System, Search, Git, Web Browser, MCP) for multi-turn interaction.

### 4.2. Code Mode (SDK-Driven Execution)
Loads the `CodeExecutorPlugin` Plugin. Switches the tool-calling mechanism from JSON Schema to generating TypeScript/Python code executed through the `@deepseek-ai/dsh` SDK in a single round-trip (round-trip = one send-to-model-and-wait cycle).

### 4.3. Minimal Mode (Isolating Benchmark)
Loads the `MinimalEnvironmentPlugin` Plugin. Opens exactly 2 tools (`bash` = the shell, and `editor` = file editing), and removes the entire complex system prompt to test the LLM's raw reasoning capability (Raw Reasoning) on benchmarks such as SWE-bench (a public benchmark of real software bugs).

### 4.4. Creator Mode (Runtime Inspection & Preset Authoring)
Loads the `RuntimeInspectorPlugin` Plugin. Provides a visual interface for developers to inspect internal state, customize system prompts, and publish Agent Presets (preset = a saved bundle of prompt + tools for reuse).

> **One-line summary:** Four modes, four plugin sets: full agent, single-turn code execution, stripped-down benchmark, and a developer's inspection bench.

---

## 5. Illustrative Kernel Engine Implementation (TypeScript)

This section points to runnable code for the kernel and for plugin registration.

Below is a simplified version of the Cordis-style Micro-Kernel Engine:

> 📄 **Example code:** [`examples/02-5-illustrative-kernel-engine-implementation-typescript.ts`](examples/02-5-illustrative-kernel-engine-implementation-typescript.ts)

### Example of registering a Plugin:

> 📄 **Example code:** [`examples/03-example-of-registering-a-plugin.ts`](examples/03-example-of-registering-a-plugin.ts)

> **One-line summary:** The example files show the tiny kernel engine in code, plus how a plugin gets registered onto it.

---

## 6. DeepSeek Harness Monorepo & pnpm Workspace Structure

This section maps the "everything is a plugin" idea onto the project's folder layout (monorepo = one repository holding many packages; pnpm = a package manager that links them).

The "Everything is a Plugin" architecture is reflected directly in the DeepSeek Harness project's directory structure (`pnpm` monorepo):

```
deepseek-harness/
├── packages/
│   ├── core/               # Cordis Micro-Kernel core & types
│   ├── dsh/                # @deepseek-ai/dsh Code Mode SDK
│   ├── runtime-standard/   # Standard Agent Runtime Plugin
│   ├── runtime-code/       # Code Mode Execution Plugin
│   ├── runtime-minimal/    # Minimal Benchmark Plugin
│   └── web-ui/             # React/Next.js Web UI & Trajectory Viewer (Port 3080)
├── presets/                # Community & Official Agent Presets
└── pnpm-workspace.yaml
```

How to read it: each folder under `packages/` is one plugin or the kernel itself — so "remove a plugin" in theory means "delete a folder".

> **One-line summary:** The folder layout mirrors the architecture: one small `core` and one folder per plugin.

---

## 7. Best Practices & Design Principles

This section closes with the habits to follow and the traps to avoid.

### ✅ Best Practices
- **Loose Coupling**: Plugins never import each other directly; they communicate through the Kernel Context (`ctx.inject('service_name')`) — so any plugin can be replaced without touching others.
- **Single Responsibility**: Each Plugin handles exactly one function (e.g., `GitPlugin`, `DockerSandboxPlugin`, `MemoryPlugin`).
- **Dynamic Loading**: Supports enabling/disabling Plugins at runtime based on user configuration (User Permission Policy).

> **One-line summary:** Keep plugins loosely coupled, one job each, and switchable at runtime.

### ❌ Anti-Patterns
- **Monolithic Kernel**: Packing too much business logic into the Kernel Core instead of moving it to Plugins — the core grows unkillable and untestable.
- **Global State Pollution**: A Plugin overwrites global variables directly instead of using `ctx.provide()` — so nothing is tracked, cleaned up, or visible to other plugins.

> **One-line summary:** Never grow the core with business logic and never stash state in globals — provide it through the kernel instead.
