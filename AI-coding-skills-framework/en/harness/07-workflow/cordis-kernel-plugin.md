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

In the old generation of AI Agent engineering, the whole application was typically locked into a monolithic framework (for example: one large codebase file containing hardcoded prompts, hardcoded tools, and fixed execution loops).

DeepSeek Harness redefines this architecture through the formula:

$$\text{Agent} = \text{Model} + \text{Harness}$$

- **Model**: Reasoning, language, and general knowledge capabilities (LLM/SLM).
- **Harness**: The surrounding environment that provides Tools, Memory, Runtimes, Context, and Guardrails.

To ensure the Harness can evolve without having to rewrite the source code, the entire Harness follows the philosophy **"Everything is a Plugin"**:

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

---

## 2. Micro-Kernel Architecture (Cordis Pattern)

Cordis is an ultra-lightweight micro-kernel framework for TypeScript, using a **Context-based Dependency Injection** and **Service Locator** mechanism.

### The Kernel's role:
1. **Lifecycle management**: Initializing (`apply`), activating (`fork`), and disposing (`dispose`) plugins.
2. **Service Locator**: Allows plugins to register Services (e.g., `ctx.memory`, `ctx.tools`, `ctx.llm`) and safely access one another.
3. **Event Emitter & Middleware**: Allows a plugin to intervene before/after an LLM call or Tool Call.

---

## 3. The Plugin's Lifecycle (Lifecycle Management)

```typescript
export interface Plugin<C = any> {
  name: string;
  apply(ctx: Context, config?: C): void | Promise<void>;
}
```

A Plugin goes through 3 phases:
1. **Mount (`apply`)**: The Plugin is loaded into the Context, registering services or event listeners.
2. **Execute**: The Plugin listens to events from the Kernel (e.g., `on('before-tool-call')`) to process logic.
3. **Unmount (`dispose`)**: When the Plugin is removed, the Kernel automatically cleans up listeners and releases resources.

---

## 4. 4 Runtime Modes in DeepSeek Harness

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

### 4.1. Standard Mode (Standard Agent)
The default interactive environment. Provides the full toolset (File System, Search, Git, Web Browser, MCP) for multi-turn interaction.

### 4.2. Code Mode (SDK-Driven Execution)
Loads the `CodeExecutorPlugin` Plugin. Switches the tool-calling mechanism from JSON Schema to generating TypeScript/Python code executed through the `@deepseek-ai/dsh` SDK in a single round-trip.

### 4.3. Minimal Mode (Isolating Benchmark)
Loads the `MinimalEnvironmentPlugin` Plugin. Opens exactly 2 tools (`bash` and `editor`), and removes the entire complex system prompt to test the LLM's raw reasoning capability (Raw Reasoning) on benchmarks such as SWE-bench.

### 4.4. Creator Mode (Runtime Inspection & Preset Authoring)
Loads the `RuntimeInspectorPlugin` Plugin. Provides a visual interface for developers to inspect internal state, customize system prompts, and publish Agent Presets.

---

## 5. Illustrative Kernel Engine Implementation (TypeScript)

Below is a simplified version of the Cordis-style Micro-Kernel Engine:

```typescript
export class Context {
  public services: Map<string, any> = new Map();
  private events: Map<string, Function[]> = new Map();

  // Register a Service in the Kernel
  public provide(name: string, service: any) {
    this.services.set(name, service);
  }

  // Fetch a Service for use
  public inject<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) throw new Error(`Service ${name} not found in Kernel Context`);
    return service as T;
  }

  // Event System for Middleware
  public on(event: string, handler: Function) {
    const handlers = this.events.get(event) || [];
    handlers.push(handler);
    this.events.set(event, handlers);
  }

  public async emit(event: string, ...args: any[]) {
    const handlers = this.events.get(event) || [];
    for (const handler of handlers) {
      await handler(...args);
    }
  }

  // Load a Plugin
  public plugin(plugin: { name: string; apply: (ctx: Context) => void }) {
    console.log(`[Kernel] Mounting Plugin: ${plugin.name}`);
    plugin.apply(this);
  }
}
```

### Example of registering a Plugin:

```typescript
// Plugin 1: Register the Tool Service
const MCPToolPlugin = {
  name: 'mcp-tool-plugin',
  apply: (ctx: Context) => {
    ctx.provide('tools', {
      executeTool: async (name: string, args: any) => {
        console.log(`Executing MCP tool ${name}`, args);
        return { success: true };
      }
    });
  }
};

// Plugin 2: Log every Tool call (Middleware Plugin)
const LoggerPlugin = {
  name: 'logger-plugin',
  apply: (ctx: Context) => {
    ctx.on('before-tool-call', (toolName: string) => {
      console.log(`[Event Stream] About to call tool: ${toolName}`);
    });
  }
};

// Boot the Kernel
const kernel = new Context();
kernel.plugin(MCPToolPlugin);
kernel.plugin(LoggerPlugin);
```

---

## 6. DeepSeek Harness Monorepo & pnpm Workspace Structure

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

---

## 7. Best Practices & Design Principles

### ✅ Best Practices
- **Loose Coupling**: Plugins never import each other directly; they communicate through the Kernel Context (`ctx.inject('service_name')`).
- **Single Responsibility**: Each Plugin handles exactly one function (e.g., `GitPlugin`, `DockerSandboxPlugin`, `MemoryPlugin`).
- **Dynamic Loading**: Supports enabling/disabling Plugins at runtime based on user configuration (User Permission Policy).

### ❌ Anti-Patterns
- **Monolithic Kernel**: Packing too much business logic into the Kernel Core instead of moving it to Plugins.
- **Global State Pollution**: A Plugin overwrites global variables directly instead of using `ctx.provide()`.
