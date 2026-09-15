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

When evaluating the performance of an AI Coding Agent on benchmarks such as **SWE-bench**, **HumanEval**, or **MBPP**, the measured results are often noisy because of:
- **System Prompt Overhead**: A system prompt that is too long (2,000+ tokens) steers the model's behavior excessively.
- **Framework Intervention**: RAG layers, Memory Consolidation, or Guardrails automatically modify the model's answers.
- **Tool Complexity**: Too many unwieldy tools degrade the ability to pick the correct tool (Tool Selection Overhead).

**The consequence**: It becomes very hard to answer the question: *"Is this LLM actually good at programming reasoning, or is the framework harness hiding its weaknesses?"*

---

## 2. The Philosophy of the Minimal Benchmark Harness

The Minimal Benchmark Harness solves this problem with the principle of **Isolation Testing**:

```
Minimal Harness = Minimal System Prompt + Zero Framework Middleware + 2 Core Tools (Bash + Editor)
```

By removing every auxiliary component, the system measures precisely the **native capability** of the LLM in solving technical problems.

---

## 3. Architecture of the Minimal Mode Environment

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

---

## 4. The Minimal Tool Set (Minimal Tool Set: Bash + Editor)

In Minimal Mode, the agent is given exactly **2 standardized tools**:

### 1. `bash`
Allows running commands in the sandbox environment's terminal:
```json
{
  "name": "bash",
  "description": "Execute bash command in sandbox terminal",
  "parameters": {
    "command": { "type": "string", "description": "Command to run" }
  }
}
```

### 2. `editor`
Allows viewing and editing files at specified line ranges:
```json
{
  "name": "editor",
  "description": "View or edit file content",
  "parameters": {
    "command": { "type": "string", "enum": ["view", "create", "str_replace"] },
    "path": { "type": "string" },
    "file_text": { "type": "string" },
    "old_str": { "type": "string" },
    "new_str": { "type": "string" }
  }
}
```

---

## 5. Implementing the Benchmark Runner (TypeScript Implementation)

Below is the source code of a **Minimal Benchmark Runner** that fully isolates the execution environment:

```typescript
import { MinimalBashTool, MinimalEditorTool } from './minimal-tools';

export interface BenchmarkTask {
  id: string;
  problemStatement: string;
  repoPath: string;
  testCommand: string;
}

export class MinimalBenchmarkRunner {
  constructor(private llmClient: any) {}

  public async runTask(task: BenchmarkTask, maxTurns: number = 20): Promise<{ solved: boolean; turns: number; log: any[] }> {
    const bash = new MinimalBashTool(task.repoPath);
    const editor = new MinimalEditorTool(task.repoPath);

    // Minimal system prompt < 100 tokens
    const systemPrompt = `You are an expert software engineer. Solve the issue using bash and editor tools. When finished, output COMPLETE_TASK.`;

    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: task.problemStatement }
    ];

    const log: any[] = [];
    let turn = 0;

    while (turn < maxTurns) {
      turn++;
      // Call the LLM directly, without going through RAG or Memory Middleware
      const response = await this.llmClient.chat({
        messages,
        tools: [bash.definition, editor.definition]
      });

      log.push({ turn, response });

      if (response.content?.includes('COMPLETE_TASK')) {
        break;
      }

      if (response.toolCalls) {
        for (const call of response.toolCalls) {
          let toolResult: any;
          if (call.name === 'bash') {
            toolResult = await bash.execute(call.args);
          } else if (call.name === 'editor') {
            toolResult = await editor.execute(call.args);
          }

          messages.push({
            role: 'tool',
            tool_call_id: call.id,
            content: JSON.stringify(toolResult)
          });
        }
      }
    }

    // Verify the result with an objective test script
    const evalResult = await bash.execute({ command: task.testCommand });
    const solved = evalResult.exitCode === 0;

    return { solved, turns: turn, log };
  }
}
```

---

## 6. Evaluation Criteria & Metrics (SWE-bench / HumanEval)

When using the Minimal Benchmark Harness, the key measured metrics include:

| METRIC | MEANING | GOAL |
|---|---|---|
| **Pass@1 Rate** | The rate of fixing the bug correctly on the first attempt | Higher (measures precise reasoning) |
| **Average Turns per Task** | The average number of conversation turns to resolve one task | Lower (saves cost & time) |
| **Tool Error Rate** | The rate of tool calls with wrong parameters / syntax | Lower (< 5%) |
| **Token Efficiency** | Total tokens consumed per successful task | Lower |

---

## 7. Best Practices & Isolation Guardrails

### ✅ Best Practices
- **Clean Docker Container**: Reset the Docker environment to its pristine state (git clean/reset) before running each benchmark task.
- **Zero Injected Memory**: Do not load any data from previous sessions, guaranteeing absolute objectivity.
- **Timeouts & Deadlocks**: Set strict timeouts (e.g., 5 minutes/task) on bash commands to avoid hung processes.

### ❌ Anti-Patterns
- **Prompt Leakage / Over-engineering**: Putting problem-solution information or detailed instructions into the Benchmark Harness's system prompt.
- **Shared Workspace**: Letting tasks share a working directory, which causes side-effects between tests.
