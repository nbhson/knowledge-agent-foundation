# 🧩 Micro-Kernel Architecture & Plugin Ecosystem — Triết Lý "Everything is a Plugin"

> **Pattern kế thừa từ DeepSeek Harness & Cordis**: Khái niệm cốt lõi **"Agent = Model + Harness"**. Toàn bộ Harness Engine được thiết kế theo siêu kiến trúc **Micro-Kernel** (hạt nhân vi mô dựa trên Cordis framework). Mọi tính năng từ Tools, Runtimes, Memory Engine, Guardrails cho đến UI Components đều là các **Plugins** có thể cắm/rút và mở rộng linh hoạt.

---

## 📑 Mục Lục

- [🧩 Micro-Kernel Architecture \& Plugin Ecosystem — Triết Lý "Everything is a Plugin"](#-micro-kernel-architecture--plugin-ecosystem--triết-lý-everything-is-a-plugin)
  - [📑 Mục Lục](#-mục-lục)
  - [1. Triết Lý Cốt Lõi: Agent = Model + Harness](#1-triết-lý-cốt-lõi-agent--model--harness)
  - [2. Kiến Trúc Micro-Kernel (Cordis Pattern)](#2-kiến-trúc-micro-kernel-cordis-pattern)
    - [Vai trò của Kernel:](#vai-trò-của-kernel)
  - [3. Vòng Đời Của Plugin (Lifecycle Management)](#3-vòng-đời-của-plugin-lifecycle-management)
  - [4. 4 Runtime Modes Trong DeepSeek Harness](#4-4-runtime-modes-trong-deepseek-harness)
    - [4.1. Standard Mode (Standard Agent)](#41-standard-mode-standard-agent)
    - [4.2. Code Mode (SDK-Driven Execution)](#42-code-mode-sdk-driven-execution)
    - [4.3. Minimal Mode (Isolating Benchmark)](#43-minimal-mode-isolating-benchmark)
    - [4.4. Creator Mode (Runtime Inspection \& Preset Authoring)](#44-creator-mode-runtime-inspection--preset-authoring)
  - [5. Triển Khai Minh Họa Kernel Engine (TypeScript)](#5-triển-khai-minh-họa-kernel-engine-typescript)
    - [Ví dụ đăng ký Plugin:](#ví-dụ-đăng-ký-plugin)
  - [6. DeepSeek Harness Monorepo \& pnpm Workspace Structure](#6-deepseek-harness-monorepo--pnpm-workspace-structure)
  - [7. Best Practices \& Design Principles](#7-best-practices--design-principles)
    - [✅ Best Practices](#-best-practices)
    - [❌ Anti-Patterns](#-anti-patterns)

---

## 1. Triết Lý Cốt Lõi: Agent = Model + Harness

Trong kỹ nghệ AI Agent thế hệ cũ, toàn bộ ứng dụng thường bị khóa chặt vào một framework monolithic (ví dụ: một file codebase lớn chứa hardcoded prompts, hardcoded tools, và fixed execution loops).

DeepSeek Harness định nghĩa lại kiến trúc này thông qua công thức:

$$\text{Agent} = \text{Model} + \text{Harness}$$

- **Model (Mô hình)**: Khả năng suy luận, ngôn ngữ, và kiến thức tổng quát (LLM/SLM).
- **Harness (Bộ khung)**: Môi trường xung quanh cung cấp Tools, Memory, Runtimes, Context, và Guardrails.

Để đảm bảo Harness có thể tiến hóa mà không phải viết lại mã nguồn, toàn bộ Harness tuân thủ triết lý **"Everything is a Plugin"**:

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

## 2. Kiến Trúc Micro-Kernel (Cordis Pattern)

Cordis là một framework micro-kernel siêu nhẹ dành cho TypeScript, sử dụng cơ chế **Context-based Dependency Injection** và **Service Locator**.

### Vai trò của Kernel:
1. **Quản lý Lifecycle**: Khởi tạo (`apply`), kích hoạt (`fork`), và hủy bỏ (`dispose`) các plugins.
2. **Service Locator**: Cho phép các plugin đăng ký các Service (ví dụ: `ctx.memory`, `ctx.tools`, `ctx.llm`) và truy cập lẫn nhau một cách an toàn.
3. **Event Emitter & Middleware**: Cho phép plugin can thiệp vào trước/sau khi gọi LLM hoặc Tool Call.

---

## 3. Vòng Đời Của Plugin (Lifecycle Management)

```typescript
export interface Plugin<C = any> {
  name: string;
  apply(ctx: Context, config?: C): void | Promise<void>;
}
```

Một Plugin trải qua 3 giai đoạn:
1. **Mount (`apply`)**: Plugin được nạp vào Context, đăng ký các service hoặc event listeners.
2. **Execute**: Plugin lắng nghe sự kiện từ Kernel (ví dụ: `on('before-tool-call')`) để xử lý logic.
3. **Unmount (`dispose`)**: Khi Plugin bị gỡ bỏ, Kernel tự động dọn dẹp các listeners và giải phóng tài nguyên.

---

## 4. 4 Runtime Modes Trong DeepSeek Harness

Nhờ kiến trúc Micro-Kernel, DeepSeek Harness có thể đóng gói 4 Runtime Modes dưới dạng các Plugin khác nhau:

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
Môi trường tương tác mặc định. Cung cấp đầy đủ tập công cụ (File System, Search, Git, Web Browser, MCP) cho tương tác multi-turn.

### 4.2. Code Mode (SDK-Driven Execution)
Nạp Plugin `CodeExecutorPlugin`. Đổi cơ chế gọi tool từ JSON Schema sang sinh mã TypeScript/Python thực thi qua `@deepseek-ai/dsh` SDK trong 1 round-trip.

### 4.3. Minimal Mode (Isolating Benchmark)
Nạp Plugin `MinimalEnvironmentPlugin`. Chỉ mở đúng 2 công cụ (`bash` và `editor`), loại bỏ toàn bộ system prompt phức tạp để kiểm thử năng lực suy luận gốc (Raw Reasoning) của LLM trên các benchmark như SWE-bench.

### 4.4. Creator Mode (Runtime Inspection & Preset Authoring)
Nạp Plugin `RuntimeInspectorPlugin`. Cung cấp giao diện trực quan để developer kiểm tra state nội bộ, tùy chỉnh system prompt, và xuất bản các Agent Presets.

---

## 5. Triển Khai Minh Họa Kernel Engine (TypeScript)

Dưới đây là phiên bản đơn giản hóa của Cordis-style Micro-Kernel Engine:

```typescript
export class Context {
  public services: Map<string, any> = new Map();
  private events: Map<string, Function[]> = new Map();

  // Đăng ký Service vào Kernel
  public provide(name: string, service: any) {
    this.services.set(name, service);
  }

  // Lấy Service ra dùng
  public inject<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) throw new Error(`Service ${name} not found in Kernel Context`);
    return service as T;
  }

  // Event System cho Middleware
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

  // Nạp Plugin
  public plugin(plugin: { name: string; apply: (ctx: Context) => void }) {
    console.log(`[Kernel] Mounting Plugin: ${plugin.name}`);
    plugin.apply(this);
  }
}
```

### Ví dụ đăng ký Plugin:

```typescript
// Plugin 1: Đăng ký Tool Service
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

// Plugin 2: Log lại mọi lượt gọi Tool (Middleware Plugin)
const LoggerPlugin = {
  name: 'logger-plugin',
  apply: (ctx: Context) => {
    ctx.on('before-tool-call', (toolName: string) => {
      console.log(`[Event Stream] About to call tool: ${toolName}`);
    });
  }
};

// Khởi chạy Kernel
const kernel = new Context();
kernel.plugin(MCPToolPlugin);
kernel.plugin(LoggerPlugin);
```

---

## 6. DeepSeek Harness Monorepo & pnpm Workspace Structure

Kiến trúc "Everything is a Plugin" phản ánh trực tiếp trong cấu trúc thư mục dự án của DeepSeek Harness (`pnpm` monorepo):

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
- **Loose Coupling**: Các Plugin không bao giờ import trực tiếp lẫn nhau mà giao tiếp qua Kernel Context (`ctx.inject('service_name')`).
- **Single Responsibility**: Mỗi Plugin chỉ đảm nhận một chức năng duy nhất (vd: `GitPlugin`, `DockerSandboxPlugin`, `MemoryPlugin`).
- **Dynamic Loading**: Hỗ trợ bật/tắt Plugin runtime dựa trên cấu hình người dùng (User Permission Policy).

### ❌ Anti-Patterns
- **Monolithic Kernel**: Đưa quá nhiều business logic vào Kernel Core thay vì chuyển sang Plugins.
- **Global State Pollution**: Plugin ghi đè trực tiếp biến toàn cục thay vì dùng `ctx.provide()`.
