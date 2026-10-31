# 🧩 Micro-Kernel Architecture & Plugin Ecosystem — Triết Lý "Everything is a Plugin"

> **Pattern kế thừa từ DeepSeek Harness & Cordis**: Ý tưởng cốt lõi là **"Agent = Model + Harness"**. Toàn bộ Harness Engine dùng siêu kiến trúc **Micro-Kernel** — chỉ giữ lại một "hạt nhân" (kernel) thật nhỏ làm việc điều phối, viết dựa trên Cordis framework. Mọi tính năng từ Tools (công cụ), Runtimes (chế độ chạy), Memory Engine (bộ nhớ), Guardrails (rào chắn an toàn) cho đến UI Components (giao diện) đều là các **Plugins** — các "cục cắm ngoài" tháo/lắp được, giống cắm USB: cắm vào là có thêm tính năng, rút ra là mất, không phải sửa lại hạt nhân.

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

> Phần này giải thích ý tưởng nền của cả tài liệu: vì sao agent nên tách thành "model" và "bộ khung" riêng.

Trong kỹ nghệ AI Agent thế hệ cũ, toàn bộ ứng dụng thường bị khóa chặt vào một framework monolithic — nghĩa là **một khối code duy nhất**, mọi thứ cài cứng bên trong: prompt cứng, tool cứng, vòng lặp chạy cố định. Muốn đổi một chi tiết nhỏ là phải sửa lại cả khối.

DeepSeek Harness định nghĩa lại kiến trúc này thông qua công thức:

$$\text{Agent} = \text{Model} + \text{Harness}$$

- **Model (Mô hình)**: "Bộ não" — khả năng suy luận, ngôn ngữ, và kiến thức tổng quát (LLM = mô hình ngôn ngữ lớn; SLM = mô hình nhỏ gọn hơn).
- **Harness (Bộ khung)**: "Cơ thể" bao quanh — cung cấp Tools (công cụ), Memory (bộ nhớ), Runtimes (chế độ chạy), Context (ngữ cảnh), và Guardrails (rào chắn an toàn).

Để đảm bảo Harness có thể tiến hóa mà không phải viết lại mã nguồn, toàn bộ Harness tuân thủ triết lý **"Everything is a Plugin"** (mọi thứ đều là plugin cắm/rút được):

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

> **Tóm gọn 1 câu:** Model chỉ là bộ não; Harness là bộ khung bao quanh, và mọi bộ phận của Harness đều là plugin cắm/rút được — thay tính năng mới không cần viết lại hạt nhân.

---

## 2. Kiến Trúc Micro-Kernel (Cordis Pattern)

> Phần này giải thích "hạt nhân" của Harness làm những gì, và làm bằng thư viện nào.

Cordis là một framework micro-kernel siêu nhẹ dành cho TypeScript. **Micro-kernel** nghĩa là: phần lõi thật nhỏ, chỉ điều phối; tính năng thật nằm ngoài lõi, dạng plugin. Cordis dùng hai cơ chế: **Context-based Dependency Injection** (tiêm phụ thuộc qua "ngữ cảnh" — plugin không tự đi tìm dịch vụ mà nhận qua `ctx`, như chung một tủ đồ dùng được cấp phát) và **Service Locator** (danh bạ dịch vụ — cần gì thì tra qua `ctx`, ví dụ `ctx.memory`, `ctx.tools`).

### Vai trò của Kernel:
1. **Quản lý Lifecycle** (vòng đời): Khởi tạo (`apply` — cắm plugin vào), kích hoạt (`fork` — tạo nhánh ngữ cảnh mới), và hủy bỏ (`dispose` — tháo ra và dọn dẹp).
2. **Service Locator**: Cho phép các plugin đăng ký các Service (dịch vụ dùng chung — ví dụ `ctx.memory` là bộ nhớ, `ctx.tools` là danh sách công cụ, `ctx.llm` là kết nối tới model) và truy cập lẫn nhau một cách an toàn.
3. **Event Emitter & Middleware**: Cho phép plugin chen vào trước/sau khi gọi LLM hoặc Tool Call (bắt sự kiện + lớp can thiệp, như trạm kiểm soát đặt trước và sau cửa).

> **Tóm gọn 1 câu:** Kernel là "hạt nhân" nhỏ chỉ làm 3 việc — quản vòng đời plugin, làm danh bạ dịch vụ dùng chung, và đặt trạm kiểm soát trước/sau mỗi lần gọi model hay tool.

---

## 3. Vòng Đời Của Plugin (Lifecycle Management)

> Phần này giải thích một plugin sống và chết như thế nào trong kernel.

> 📄 **Code ví dụ:** [`examples/01-3-vong-oi-cua-plugin-lifecycle-management.ts`](examples/01-3-vong-oi-cua-plugin-lifecycle-management.ts)

Một Plugin trải qua 3 giai đoạn:
1. **Mount (`apply`)**: "Lắp vào" — Plugin được nạp vào Context, đăng ký các service hoặc event listeners (bộ lắng nghe sự kiện).
2. **Execute**: "Làm việc" — Plugin lắng nghe sự kiện từ Kernel (ví dụ: `on('before-tool-call')` — "ngay trước khi tool chạy") để xử lý logic.
3. **Unmount (`dispose`)**: "Tháo ra" — Khi Plugin bị gỡ bỏ, Kernel tự động dọn dẹp các listeners và giải phóng tài nguyên; bạn không phải dọn tay.

> **Tóm gọn 1 câu:** Plugin sống 3 nhịp — cắm vào (`apply`), lắng nghe và xử lý sự kiện khi chạy, rồi rút ra (`dispose`) khi kernel tự dọn dẹp.

---

## 4. 4 Runtime Modes Trong DeepSeek Harness

> Phần này giải thích 4 "chế độ chạy" của Harness — nhờ kiến trúc plugin, mỗi chế độ chỉ là một plugin khác nhau.

Nhờ kiến trúc Micro-Kernel, DeepSeek Harness có thể đóng gói 4 Runtime Modes (chế độ chạy) dưới dạng các Plugin khác nhau:

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
Môi trường tương tác mặc định — kiểu bạn chat trực tiếp với agent hằng ngày. Cung cấp đầy đủ tập công cụ (File System — đọc/ghi file, Search — tìm kiếm, Git, Web Browser — trình duyệt web, MCP — giao thức cắm công cụ ngoài) cho tương tác multi-turn (nhiều lượt hỏi–đáp).

> **Tóm gọn 1 câu:** Standard Mode là chế độ "đầy đủ công cụ", dùng cho làm việc nhiều lượt hằng ngày.

### 4.2. Code Mode (SDK-Driven Execution)
Nạp Plugin `CodeExecutorPlugin`. Đổi cơ chế gọi tool: thay vì mô tả từng tool bằng JSON Schema (bản mô tả cấu trúc dữ liệu) rồi gọi từng cái một, model viết luôn một đoạn mã TypeScript/Python chứa nhiều lời gọi và thực thi một lần qua `@deepseek-ai/dsh` SDK — trong 1 round-trip (một lượt đi–về với model, tiết kiệm nhiều lượt hỏi–đáp).

> **Tóm gọn 1 câu:** Code Mode cho model viết code gọi nhiều tool cùng lúc qua SDK, thay vì gọi từng tool một — nhanh hơn và tốn ít lượt hơn.

### 4.3. Minimal Mode (Isolating Benchmark)
Nạp Plugin `MinimalEnvironmentPlugin`. Chỉ mở đúng 2 công cụ (`bash` — chạy lệnh terminal, và `editor` — xem/sửa file), loại bỏ toàn bộ system prompt phức tạp (câu lệnh nền dài) để kiểm thử năng lực suy luận gốc (Raw Reasoning) của LLM trên các benchmark như SWE-bench (bộ đề vá lỗi thật trên repo thật).

> **Tóm gọn 1 câu:** Minimal Mode là "phòng thi trống": chỉ 2 công cụ, không prompt dài, để đo đúng năng lực gốc của model.

### 4.4. Creator Mode (Runtime Inspection & Preset Authoring)
Nạp Plugin `RuntimeInspectorPlugin`. Cung cấp giao diện trực quan để developer (người phát triển) kiểm tra state nội bộ (trạng thái bên trong của agent), tùy chỉnh system prompt, và xuất bản các Agent Presets (cấu hình agent dựng sẵn để dùng lại hoặc chia sẻ).

> **Tóm gọn 1 câu:** Creator Mode là "bàn lắp ráp" dành cho developer: soi trạng thái bên trong, chỉnh prompt, và đóng gói preset agent.

---

## 5. Triển Khai Minh Họa Kernel Engine (TypeScript)

> Phần này cho xem code: một kernel tối giản viết theo phong cách Cordis, để bạn hiểu cơ chế bên trong.

Dưới đây là phiên bản đơn giản hóa của Cordis-style Micro-Kernel Engine:

> 📄 **Code ví dụ:** [`examples/02-5-trien-khai-minh-hoa-kernel-engine-typescript.ts`](examples/02-5-trien-khai-minh-hoa-kernel-engine-typescript.ts)

### Ví dụ đăng ký Plugin:

Đây là cách cắm một plugin vào kernel: khai báo tên, các service nó cung cấp, và các sự kiện nó lắng nghe.

> 📄 **Code ví dụ:** [`examples/03-vi-du-ang-ky-plugin.ts`](examples/03-vi-du-ang-ky-plugin.ts)

> **Tóm gọn 1 câu:** Kernel không phải khái niệm trừu tượng — một engine kiểu Cordis viết được trong vài chục dòng TypeScript, và cắm plugin chỉ là gọi `apply` với một object khai báo.

---

## 6. DeepSeek Harness Monorepo & pnpm Workspace Structure

> Phần này cho thấy triết lý plugin hiện hình ngay trên cây thư mục dự án: mỗi plugin là một gói (package) riêng.

Kiến trúc "Everything is a Plugin" phản ánh trực tiếp trong cấu trúc thư mục dự án của DeepSeek Harness (`pnpm` monorepo — nhiều gói nằm chung một repo, quản phụ thuộc bằng trình quản lý gói pnpm):

Cách đọc cây: `packages/` chứa các gói riêng lẻ — mỗi gói là một plugin hoặc thành phần độc lập; dòng `#` phía sau là chú thích nghĩa của từng gói.

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

> **Tóm gọn 1 câu:** Cây thư mục chính là bản đồ kiến trúc: `core` là hạt nhân, còn lại mỗi package là một plugin (4 runtime, SDK, web UI) cắm quanh hạt nhân.

---

## 7. Best Practices & Design Principles

> Phần này tổng kết nên làm gì và tránh gì khi xây plugin cho kernel.

### ✅ Best Practices
- **Loose Coupling** (liên kết lỏng): Các Plugin không bao giờ import trực tiếp lẫn nhau mà giao tiếp qua Kernel Context (`ctx.inject('service_name')` — dùng dịch vụ qua `ctx`, như gọi qua tổng đài thay vì đục tường sang nhà người khác).
- **Single Responsibility** (mỗi plugin một việc): Mỗi Plugin chỉ đảm nhận một chức năng duy nhất (vd: `GitPlugin` chỉ lo Git, `DockerSandboxPlugin` chỉ lo sandbox, `MemoryPlugin` chỉ lo bộ nhớ).
- **Dynamic Loading** (nạp động): Hỗ trợ bật/tắt Plugin runtime (ngay khi đang chạy) dựa trên cấu hình người dùng (User Permission Policy — chính sách quyền của từng người dùng).

> **Tóm gọn 1 câu:** Plugin tốt là plugin lỏng lẻo: chỉ làm một việc, nói chuyện qua `ctx`, và bật/tắt được theo cấu hình.

### ❌ Anti-Patterns
- **Monolithic Kernel** (kernel khổng lồ): Đưa quá nhiều business logic (nghiệp vụ thực tế) vào Kernel Core thay vì chuyển sang Plugins — hạt nhân phình to, mất hết ý nghĩa "nhỏ gọn".
- **Global State Pollution** (làm bẩn biến toàn cục): Plugin ghi đè trực tiếp biến toàn cục thay vì dùng `ctx.provide()` (đăng ký dịch vụ qua ctx) — một plugin sửa biến chung thì mọi plugin khác bị lây, và lỗi khó truy vết.

> **Tóm gọn 1 câu:** Hai cách phá hỏng kiến trúc này: nhét nghiệp vụ vào hạt nhân, và ghi đè biến toàn cục thay vì đăng ký dịch vụ qua `ctx`.
