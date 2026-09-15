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

### Standard Tool Calling (Multi-turn Round-trips)
In standard AI Agent frameworks, when completing a task consisting of 5 steps (e.g.: find `*.ts` files, read the files, filter `fetch` functions, fix the code, run the linter), the LLM must perform **5 independent interaction turns** with the system:

```
Turn 1: LLM ──[JSON: search_files]──► Harness ──[Exec]──► LLM (Returns 20 files)
Turn 2: LLM ──[JSON: read_file_1]───► Harness ──[Exec]──► LLM (Returns content 1)
Turn 3: LLM ──[JSON: read_file_2]───► Harness ──[Exec]──► LLM (Returns content 2)
Turn 4: LLM ──[JSON: edit_file]─────► Harness ──[Exec]──► LLM (Edit done)
Turn 5: LLM ──[JSON: run_linter]────► Harness ──[Exec]──► LLM (Success)
```

**Drawbacks:**
- **High Latency**: Each turn takes 1-3 seconds to call the LLM API. 5 turns take 10-15 seconds.
- **Token Consumption**: The conversation history must balloon with every turn (the entire old context is re-sent).
- **Lack of complex control flow**: The LLM cannot write loops (`for`), conditional statements (`if/else`), or handle errors (`try/catch`) directly between tools — it must rely entirely on step-by-step reasoning.

---

## 2. Core Benefits of Code Mode SDK

The DeepSeek Harness introduces **Code Mode** together with a standardized SDK (`@deepseek-ai/dsh`). Instead of calling tools via JSON, the LLM generates a TypeScript/JavaScript code snippet that executes inside a Sandboxing Runtime:

```typescript
// A single round-trip only! The LLM writes code that orchestrates the SDK:
import { tools } from '@deepseek-ai/dsh';

const files = await tools.findFiles('src/**/*.ts');
for (const file of files) {
  const content = await tools.readFile(file);
  if (content.includes('legacyFetch')) {
    const updated = content.replace(/legacyFetch/g, 'modernFetch');
    await tools.writeFile(file, updated);
  }
}
await tools.bash('pnpm lint');
```

```
Single Turn: LLM ──[TypeScript Code]──► Code Runtime Engine ──[Exec All Steps]──► LLM (Final result)
```

### Outstanding advantages:
1. **80% Latency & Token Cost Reduction**: Merges $N$ API calls into **a single turn only**.
2. **Powerful Control Flow**: Fully leverages the control structures of programming languages (loops, async/await, error boundaries, data filtering).
3. **Deterministic Output**: Reduces hallucination when stitching data together across tools.

---

## 3. SDK Architecture (`@deepseek-ai/dsh` Pattern)

The Harness SDK packages all system tools (Search, File System, MCP Tools, Shell execution) into a single TypeScript object with clear type definitions:

```typescript
export interface HarnessSDK {
  fs: {
    readFile(path: string): Promise<string>;
    writeFile(path: string, content: string): Promise<void>;
    searchFiles(pattern: string): Promise<string[]>;
  };
  bash: {
    exec(command: string, options?: { timeoutMs?: number }): Promise<{ stdout: string; stderr: string; exitCode: number }>;
  };
  mcp: {
    callTool(serverName: string, toolName: string, args: Record<string, any>): Promise<any>;
  };
  logger: {
    info(msg: string): void;
    warn(msg: string): void;
    error(msg: string): void;
  };
}
```

---

## 4. Programmatic Tool Pipeline Execution Flow

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

---

## 5. Illustrative Implementation (TypeScript Execution Sandbox)

Below is simplified source code for a **Code Mode Sandbox Executor** that runs LLM-generated TypeScript code:

```typescript
import * as vm from 'vm';
import { HarnessSDK } from './sdk-types';

export class CodeModeExecutor {
  constructor(private sdk: HarnessSDK) {}

  public async executeScript(code: string, timeoutMs: number = 30000): Promise<{ success: boolean; result?: any; logs: string[]; error?: string }> {
    const logs: string[] = [];

    // 1. Create a safe Context with the approved APIs
    const sandboxContext = {
      dsh: this.sdk,
      console: {
        log: (...args: any[]) => logs.push(args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')),
        error: (...args: any[]) => logs.push(`[ERROR] ${args.join(' ')}`),
      },
      setTimeout,
      clearTimeout,
    };

    // 2. Wrap the source code in an Async IIFE
    const wrappedCode = `
      (async () => {
        ${code}
      })();
    `;

    try {
      const vmContext = vm.createContext(sandboxContext);
      const script = new vm.Script(wrappedCode);

      // 3. Execute the source code in the sandbox with a timeout
      const result = await script.runInContext(vmContext, { timeout: timeoutMs });

      return { success: true, result, logs };
    } catch (err: any) {
      return {
        success: false,
        logs,
        error: err.message || String(err)
      };
    }
  }
}
```

---

## 6. Detailed Comparison (Standard vs Code Mode)

| CRITERION | STANDARD TOOL CALLING | CODE MODE SDK |
|---|---|---|
| **Execution mechanism** | LLM returns a JSON Schema → the server runs the tool → returns the result to the LLM | LLM writes TypeScript/Python code → runs it in a Sandbox |
| **Number of interactions (Turns)** | Multi-turn ($N$ turns for $N$ steps) | Single turn (1 turn for the whole chain of $N$ steps) |
| **Latency** | High (depends on many LLM API calls) | Low (only the actual script runtime) |
| **Intermediate data handling** | Shuttled back and forth through the LLM's Context Window | Processed directly in the Code Runtime's RAM |
| **Control structures** | None (the LLM reasons step by step) | Very strong (`for`, `while`, `try/catch`, `map/filter`) |
| **Best suited tasks** | Step-by-step analysis, interactive Q&A | Batch processing, code refactoring, data migration |

---

## 7. Best Practices & Security Guardrails

### ✅ Best Practices
- **Strict Typing for the SDK**: Provide the complete `@types/dsh` definition file inside the System Prompt so the LLM can automatically write 100% correct code.
- **Dry-run First**: Perform a syntax check (static analysis/TypeScript compilation) before executing the source code.
- **Detailed Logging**: Require the LLM to use `console.log()` at key processing milestones for easy tracing in the Event Stream.

### 🛡️ Security Guardrails
- **Sandbox Isolation**: Always run code in an isolated environment (Docker Container, Worker Threads, or V8 Isolate). Never use `eval()` or `vm.runInThisContext()`.
- **Resource Constraints**: Set execution time limits (`timeoutMs`), memory limits (`maxMemory`), and a maximum number of Shell commands.
- **Permission Approval**: If the script performs dangerous operations (e.g.: `rm -rf`, `git push --force`), the Sandbox must pause and request confirmation from the User.
