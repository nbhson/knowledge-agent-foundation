# 💻 Code Mode SDK — Multi-Step Tool Orchestration via Code Execution

> **Pattern kế thừa từ DeepSeek Harness**: Thay vì bắt LLM thực hiện hàng chục lượt đàm thoại (multi-turn round-trips) để gọi lần lượt từng công cụ qua JSON schema, **Code Mode SDK** cho phép LLM viết một chương trình duy nhất (TypeScript/Python) tương tác với Harness SDK. Chương trình này thực thi toàn bộ luồng xử lý phức tạp trong một vòng lặp runtime đơn duy nhất.

---

## 📑 Mục Lục

- [💻 Code Mode SDK — Multi-Step Tool Orchestration via Code Execution](#-code-mode-sdk--multi-step-tool-orchestration-via-code-execution)
  - [📑 Mục Lục](#-mục-lục)
  - [1. Bối Cảnh: Standard Tool Calling vs Code Mode SDK](#1-bối-cảnh-standard-tool-calling-vs-code-mode-sdk)
    - [Standard Tool Calling (Multi-turn Round-trips)](#standard-tool-calling-multi-turn-round-trips)
  - [2. Lợi Ích Cốt Lõi Của Code Mode SDK](#2-lợi-ích-cốt-lõi-của-code-mode-sdk)
    - [Ưu điểm vượt trội:](#ưu-điểm-vượt-trội)
  - [3. Kiến Trúc SDK (`@deepseek-ai/dsh` Pattern)](#3-kiến-trúc-sdk-deepseek-aidsh-pattern)
  - [4. Luồng Thực Thi Programmatic Tool Pipeline](#4-luồng-thực-thi-programmatic-tool-pipeline)
  - [5. Triển Khai Minh Họa (TypeScript Execution Sandbox)](#5-triển-khai-minh-họa-typescript-execution-sandbox)
  - [6. So Sánh Chi Tiết (Standard vs Code Mode)](#6-so-sánh-chi-tiết-standard-vs-code-mode)
  - [7. Best Practices \& Security Guardrails](#7-best-practices--security-guardrails)
    - [✅ Best Practices](#-best-practices)
    - [🛡️ Security Guardrails](#️-security-guardrails)

---

## 1. Bối Cảnh: Standard Tool Calling vs Code Mode SDK

### Standard Tool Calling (Multi-turn Round-trips)
Trong các framework AI Agent tiêu chuẩn, khi cần hoàn thành một task gồm 5 bước (ví dụ: tìm file `*.ts`, đọc file, lọc hàm `fetch`, sửa code, chạy linter), LLM phải thực hiện **5 turn tương tác** độc lập với hệ thống:

```
Turn 1: LLM ──[JSON: search_files]──► Harness ──[Exec]──► LLM (Trả về 20 files)
Turn 2: LLM ──[JSON: read_file_1]───► Harness ──[Exec]──► LLM (Trả về content 1)
Turn 3: LLM ──[JSON: read_file_2]───► Harness ──[Exec]──► LLM (Trả về content 2)
Turn 4: LLM ──[JSON: edit_file]─────► Harness ──[Exec]──► LLM (Sửa xong)
Turn 5: LLM ──[JSON: run_linter]────► Harness ──[Exec]──► LLM (Thành công)
```

**Nhược điểm:**
- **Độ trễ cao (High Latency)**: Mỗi turn mất 1-3 giây gọi LLM API. 5 turn tốn 10-15 giây.
- **Tiêu tốn Token**: Lịch sử trò chuyện phải phình to qua mỗi turn (gửi lại toàn bộ context cũ).
- **Thiếu logic điều khiển phức tạp**: LLM không thể viết vòng lặp (`for`), câu lệnh điều kiện (`if/else`), hoặc xử lý lỗi (`try/catch`) trực tiếp giữa các công cụ mà phải dựa hoàn toàn vào khả năng suy luận từng bước.

---

## 2. Lợi Ích Cốt Lõi Của Code Mode SDK

DeepSeek Harness giới thiệu **Code Mode** cùng với SDK chuẩn hóa (`@deepseek-ai/dsh`). Thay vì gọi tool qua JSON, LLM sinh ra một đoạn mã TypeScript/JavaScript thực thi trong Sandboxing Runtime:

> 📄 **Code ví dụ:** [`examples/01-2-loi-ich-cot-loi-cua-code-mode.ts`](examples/01-2-loi-ich-cot-loi-cua-code-mode.ts)

```
Single Turn: LLM ──[TypeScript Code]──► Code Runtime Engine ──[Exec All Steps]──► LLM (Kết quả cuối)
```

### Ưu điểm vượt trội:
1. **Giảm 80% Latency & Token Cost**: Gộp $N$ lượt gọi API xuống thành **1 turn duy nhất**.
2. **Logic Control Mạnh Mẽ**: Tận dụng đầy đủ cấu trúc điều khiển của ngôn ngữ lập trình (loops, async/await, error boundaries, data filtering).
3. **Deterministic Output**: Giảm hiện tượng hallucination khi ghép nối dữ liệu giữa các công cụ.

---

## 3. Kiến Trúc SDK (`@deepseek-ai/dsh` Pattern)

Harness SDK đóng gói toàn bộ công cụ của hệ thống (Search, File System, MCP Tools, Shell execution) thành một đối tượng TypeScript có type-definition rõ ràng:

> 📄 **Code ví dụ:** [`examples/02-3-kien-truc-sdk-deepseek-ai-dsh-pattern.ts`](examples/02-3-kien-truc-sdk-deepseek-ai-dsh-pattern.ts)

---

## 4. Luồng Thực Thi Programmatic Tool Pipeline

```
┌────────────────────────────────────────────────────────────────────────┐
│                      CODE MODE EXECUTION ENGINE                        │
├────────────────────────────────────────────────────────────────────────┤
│  1. LLM nhận task ──► Sinh ra Script: `solution.ts`                    │
│                                                                        │
│  2. Sandboxing Engine (Node.js/V8 Isolate):                            │
│     ├── Inject `dsh` SDK object                                        │
│     ├── Giới hạn quyền truy cập Network / File System                  │
│     └── Đặt Timeout & Resource Limits (RAM / CPU)                     │
│                                                                        │
│  3. Execute Script ──► Bắt các console.log / Trajectory Events        │
│                                                                        │
│  4. Trả về kết quả tổng hợp + Trajectory trace cho LLM                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Triển Khai Minh Họa (TypeScript Execution Sandbox)

Dưới đây là mã nguồn đơn giản hóa của một **Code Mode Sandbox Executor** chạy mã TypeScript do LLM tạo ra:

> 📄 **Code ví dụ:** [`examples/03-5-trien-khai-minh-hoa-typescript-execution-sandbox.ts`](examples/03-5-trien-khai-minh-hoa-typescript-execution-sandbox.ts)

---

## 6. So Sánh Chi Tiết (Standard vs Code Mode)

| TIÊU CHÍ | STANDARD TOOL CALLING | CODE MODE SDK |
|---|---|---|
| **Cơ chế thực thi** | LLM trả về JSON Schema → Server chạy tool → Trả kết quả cho LLM | LLM viết mã TypeScript/Python → Run trong Sandbox |
| **Số lượt tương tác (Turns)** | Multi-turn ($N$ turns cho $N$ bước) | Single turn (1 turn cho cả chuỗi $N$ bước) |
| **Độ trễ (Latency)** | Cao (phụ thuộc nhiều lần gọi LLM API) | Thấp (chỉ tốn thời gian chạy script thực tế) |
| **Xử lý dữ liệu trung gian** | Truyền qua lại qua Context Window của LLM | Xử lý trực tiếp trong RAM của Code Runtime |
| **Cấu trúc điều khiển** | Không có (do LLM suy luận theo chuỗi) | Rất mạnh (`for`, `while`, `try/catch`, `map/filter`) |
| **Phù hợp cho task** | Phân tích từng bước, hỏi đáp tương tác | Batch processing, refactoring mã nguồn, data migration |

---

## 7. Best Practices & Security Guardrails

### ✅ Best Practices
- **Strict Typing for SDK**: Cung cấp file định nghĩa `@types/dsh` đầy đủ trong System Prompt để LLM tự động viết code chính xác 100%.
- **Dry-run First**: Thực hiện kiểm tra cú pháp (static analysis/TypeScript compilation) trước khi thực thi mã nguồn.
- **Detailed Logging**: Yêu cầu LLM dùng `console.log()` tại các mốc xử lý quan trọng để dễ dàng truy vết trong Event Stream.

### 🛡️ Security Guardrails
- **Sandbox Isolation**: Luôn chạy mã trong môi trường cô lập (Docker Container, Worker Threads, hoặc V8 Isolate). Không bao giờ dùng `eval()` hoặc `vm.runInThisContext()`. Taxonomy tier, các control bắt buộc, và runner đã harden được đặc tả trong [`12-sandbox-execution`](../12-sandbox-execution/README.md) — mục này chỉ ghi nhận rằng script Code Mode kế thừa chúng.
- **Resource Constraints**: Thiết lập giới hạn thời gian chạy (`timeoutMs`), dung lượng bộ nhớ (`maxMemory`), và số câu lệnh Shell tối đa. Đây là các giới hạn tài nguyên ở `12` §3 áp cho sandbox Code Mode; hãy đổi ở đó, không đổi ở đây.
- **Permission Approval**: Nếu script thực hiện các thao tác nguy hiểm (vd: `rm -rf`, `git push --force`), Sandbox phải tạm dừng và yêu cầu xác nhận từ phía User. Cơ chế tạm dừng là giao thức `PAUSED:` ở [`15-approval-gates`](../15-approval-gates/README.md) §5 — lưu ý rằng "tạm dừng và hỏi" không giống "từ chối khi hết hạn", và `15` là nơi quyết định cái nào áp dụng.
