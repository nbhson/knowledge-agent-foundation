# 🧪 Minimal Benchmark Harness — Môi Trường Đánh Giá Tối Giản Cho Raw LLM Reasoning

> **Pattern kế thừa từ DeepSeek Harness (Minimal Mode)**: Môi trường đánh giá tối giản nhằm cách ly khả năng suy luận gốc (Raw Reasoning) của LLM khỏi sự can thiệp của các tầng framework phức tạp (heavy prompts, multi-agent orchestration, complex memory pipelines).

---

## 📑 Mục Lục

- [🧪 Minimal Benchmark Harness — Môi Trường Đánh Giá Tối Giản Cho Raw LLM Reasoning](#-minimal-benchmark-harness--môi-trường-đánh-giá-tối-giản-cho-raw-llm-reasoning)
  - [📑 Mục Lục](#-mục-lục)
  - [1. Bối Cảnh \& Động Cơ](#1-bối-cảnh--động-cơ)
  - [2. Triết Lý Minimal Benchmark Harness](#2-triết-lý-minimal-benchmark-harness)
  - [3. Kiến Trúc Môi Trường Minimal Mode](#3-kiến-trúc-môi-trường-minimal-mode)
  - [4. Bộ Công Cụ Tối Giản (Minimal Tool Set: Bash + Editor)](#4-bộ-công-cụ-tối-giản-minimal-tool-set-bash--editor)
    - [1. `bash`](#1-bash)
    - [2. `editor`](#2-editor)
  - [5. Triển Khai Benchmark Runner (TypeScript Implementation)](#5-triển-khai-benchmark-runner-typescript-implementation)
  - [6. Tiêu Chí Đánh Giá \& Metrics (SWE-bench / HumanEval)](#6-tiêu-chí-đánh-giá--metrics-swe-bench--humaneval)
  - [7. Best Practices \& Isolation Guardrails](#7-best-practices--isolation-guardrails)
    - [✅ Best Practices](#-best-practices)
    - [❌ Anti-Patterns](#-anti-patterns)

---

## 1. Bối Cảnh & Động Cơ

Khi đánh giá hiệu năng của một AI Coding Agent trên các bộ Benchmark như **SWE-bench**, **HumanEval**, hoặc **MBPP**, kết quả đo lường thường bị nhiễu do:
- **System Prompt Overhead**: System Prompt quá dài (2,000+ tokens) định hướng hành vi của mô hình quá mức.
- **Framework Intervention**: Các tầng RAG, Memory Consolidation, hoặc Guardrail tự động chỉnh sửa câu trả lời của mô hình.
- **Tool Complexity**: Quá nhiều công cụ rườm rà làm suy giảm khả năng chọn công cụ chính xác (Tool Selection Overhead).

**Hệ quả**: Rất khó để trả lời câu hỏi: *"Mô hình LLM này thực sự giỏi suy luận lập trình, hay do Framework Harness che giấu điểm yếu của nó?"*

---

## 2. Triết Lý Minimal Benchmark Harness

Minimal Benchmark Harness giải quyết vấn đề này bằng nguyên tắc **Isolation Testing**:

```
Minimal Harness = Minimal System Prompt + Zero Framework Middleware + 2 Core Tools (Bash + Editor)
```

Bằng cách loại bỏ toàn bộ các thành phần phụ trợ, hệ thống đo lường chính xác **năng lực tự nhiên (native capability)** của LLM trong việc giải quyết vấn đề kỹ thuật.

---

## 3. Kiến Trúc Môi Trường Minimal Mode

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

## 4. Bộ Công Cụ Tối Giản (Minimal Tool Set: Bash + Editor)

Trong Minimal Mode, Agent chỉ được cung cấp đúng **2 công cụ chuẩn hóa**:

### 1. `bash`
Cho phép thi hành lệnh trong terminal của môi trường sandbox:
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
Cho phép xem và chỉnh sửa file tại các khoảng dòng chỉ định:
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

## 5. Triển Khai Benchmark Runner (TypeScript Implementation)

Dưới đây là mã nguồn của một **Minimal Benchmark Runner** cách ly hoàn toàn môi trường chạy:

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

    // System Prompt tối giản < 100 tokens
    const systemPrompt = `You are an expert software engineer. Solve the issue using bash and editor tools. When finished, output COMPLETE_TASK.`;

    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: task.problemStatement }
    ];

    const log: any[] = [];
    let turn = 0;

    while (turn < maxTurns) {
      turn++;
      // Gọi LLM trực tiếp không qua RAG hay Memory Middleware
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

    // Kiểm tra kết quả bằng test script khách quan
    const evalResult = await bash.execute({ command: task.testCommand });
    const solved = evalResult.exitCode === 0;

    return { solved, turns: turn, log };
  }
}
```

---

## 6. Tiêu Chí Đánh Giá & Metrics (SWE-bench / HumanEval)

Khi sử dụng Minimal Benchmark Harness, các chỉ số đo lường chính bao gồm:

| METRIC | Ý NGHĨA | MỤC TIÊU |
|---|---|---|
| **Pass@1 Rate** | Tỷ lệ sửa đúng bug ngay trong lần thử đầu tiên | Cao hơn (đánh giá suy luận chính xác) |
| **Average Turns per Task** | Số lượt đàm thoại trung bình để giải quyết 1 task | Thấp hơn (tiết kiệm chi phí & thời gian) |
| **Tool Error Rate** | Tỷ lệ gọi tool sai tham số / cú pháp | Thấp hơn (< 5%) |
| **Token Efficiency** | Số lượng token tổng cộng tiêu tốn per successful task | Thấp hơn |

---

## 7. Best Practices & Isolation Guardrails

### ✅ Best Practices
- **Clean Docker Container**: Reset môi trường Docker sang trạng thái gốc (git clean/reset) trước khi thực hiện từng task benchmark.
- **Zero Injected Memory**: Không nạp bất kỳ dữ liệu từ các session trước để đảm bảo tính khách quan tuyệt đối.
- **Timeouts & Deadlocks**: Đặt thời gian timeout nghiêm ngặt (vd: 5 phút/task) cho các lệnh bash để tránh treo tiến trình.

### ❌ Anti-Patterns
- **Prompt Leakage / Over-engineering**: Đưa thông tin giải đề hoặc hướng dẫn chi tiết vào System Prompt của Benchmark Harness.
- **Shared Workspace**: Cho phép các task dùng chung thư mục làm việc dẫn đến side-effect giữa các bài test.
