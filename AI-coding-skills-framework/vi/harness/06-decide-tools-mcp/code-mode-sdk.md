# 💻 Code Mode SDK — Multi-Step Tool Orchestration via Code Execution

> **Pattern kế thừa từ DeepSeek Harness**: Thay vì bắt LLM thực hiện hàng chục lượt đàm thoại (multi-turn round-trips) để gọi lần lượt từng công cụ qua JSON schema, **Code Mode SDK** cho phép LLM viết một chương trình duy nhất (TypeScript/Python) tương tác với Harness SDK. Chương trình này thực thi toàn bộ luồng xử lý phức tạp trong một vòng lặp runtime đơn duy nhất.

> **Đọc trang này để làm gì:** tài liệu giải thích cách cho model "viết code gọi công cụ" thay vì trả lời JSON từng bước — nhanh hơn, rẻ hơn — và các luồng an toàn bắt buộc khi chạy code đó.
>
> **Từ khóa nhanh:** *SDK* = bộ thư viện có sẵn để code gọi thẳng vào hệ thống; *runtime* = môi trường chạy code; *sandbox* = "lồng kính" cô lập code chạy trong đó.

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

> Phần này so sánh cách gọi công cụ "kiểu cũ" (nhiều lượt qua lại) với cách "kiểu mới" (một chương trình duy nhất) để thấy vì sao code mode nhanh hơn.

### Standard Tool Calling (Multi-turn Round-trips)
Trong các framework AI Agent tiêu chuẩn, khi cần hoàn thành một task gồm 5 bước (ví dụ: tìm file `*.ts`, đọc file, lọc hàm `fetch`, sửa code, chạy linter — linter = công cụ kiểm tra lỗi phong cách code), LLM phải thực hiện **5 turn tương tác** độc lập với hệ thống:

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

> **Tóm gọn 1 câu:** Kiểu cũ gọi từng tool một qua JSON nên chậm, đốt token và không viết được vòng lặp/điều kiện — đó là lý do cần code mode.

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
3. **Deterministic Output**: Giảm hiện tượng hallucination (model bịa ra dữ liệu không có thật) khi ghép nối dữ liệu giữa các công cụ.

> **Tóm gọn 1 câu:** Code mode gộp N lượt gọi thành 1, cho phép dùng vòng lặp/xử lý lỗi thật, và giảm bịa đặt khi nối dữ liệu giữa các công cụ.

---

## 3. Kiến Trúc SDK (`@deepseek-ai/dsh` Pattern)

> Phần này mô tả SDK đóng gói công cụ thành một đối tượng có sẵn trong sandbox.

Harness SDK đóng gói toàn bộ công cụ của hệ thống (Search, File System, MCP Tools, Shell execution) thành một đối tượng TypeScript có type-definition rõ ràng (type-definition = bản mô tả "hàm nào nhận gì, trả về gì" giúp viết code không sai):

> 📄 **Code ví dụ:** [`examples/02-3-kien-truc-sdk-deepseek-ai-dsh-pattern.ts`](examples/02-3-kien-truc-sdk-deepseek-ai-dsh-pattern.ts)

> **Tóm gọn 1 câu:** Mọi công cụ nằm gọn trong một đối tượng SDK có định dạng kiểu đầy đủ — model nhìn bản mô tả là viết code đúng ngay.

---

## 4. Luồng Thực Thi Programmatic Tool Pipeline

> Phần này mô tả 4 bước từ lúc model nhận việc đến lúc nhận lại kết quả.

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

*(Đọc sơ đồ trên: 1. model sinh ra file `solution.ts` → 2. engine sandbox bơm SDK vào, khoá quyền mạng/file, đặt giới hạn thời gian và RAM → 3. chạy script, bắt mọi `console.log` và sự kiện → 4. trả kết quả tổng hợp kèm vết thực thi cho model.)*

> **Tóm gọn 1 câu:** Model chỉ viết code; sandbox lo inject SDK, khoá quyền, giới hạn tài nguyên, chạy và trả kết quả kèm vết thực thi.

---

## 5. Triển Khai Minh Họa (TypeScript Execution Sandbox)

> Phần này cho code minh họa của bộ thực thi sandbox.

Dưới đây là mã nguồn đơn giản hóa của một **Code Mode Sandbox Executor** (bộ thực thi code trong lồng kính) chạy mã TypeScript do LLM tạo ra:

> 📄 **Code ví dụ:** [`examples/03-5-trien-khai-minh-hoa-typescript-execution-sandbox.ts`](examples/03-5-trien-khai-minh-hoa-typescript-execution-sandbox.ts)

> **Tóm gọn 1 câu:** Code minh họa cho thấy sandbox executor chặn quyền, giới hạn tài nguyên và chạy script của model một cách kiểm soát.

---

## 6. So Sánh Chi Tiết (Standard vs Code Mode)

> Phần này so sánh hai cách tiếp cận theo 6 tiêu chí.

Cách đọc bảng này: cột **TIÊU CHÍ** là mặt so sánh; cột **STANDARD TOOL CALLING** là cách kiểu cũ (gọi từng tool qua JSON); cột **CODE MODE SDK** là cách mới (model viết một chương trình). Ví dụ, dòng "Cấu trúc điều khiển": kiểu cũ không có vòng lặp, kiểu mới dùng thoải mái `for`, `while`, `try/catch`.

| TIÊU CHÍ | STANDARD TOOL CALLING | CODE MODE SDK |
|---|---|---|
| **Cơ chế thực thi** | LLM trả về JSON Schema → Server chạy tool → Trả kết quả cho LLM | LLM viết mã TypeScript/Python → Run trong Sandbox |
| **Số lượt tương tác (Turns)** | Multi-turn ($N$ turns cho $N$ bước) | Single turn (1 turn cho cả chuỗi $N$ bước) |
| **Độ trễ (Latency)** | Cao (phụ thuộc nhiều lần gọi LLM API) | Thấp (chỉ tốn thời gian chạy script thực tế) |
| **Xử lý dữ liệu trung gian** | Truyền qua lại qua Context Window của LLM | Xử lý trực tiếp trong RAM của Code Runtime |
| **Cấu trúc điều khiển** | Không có (do LLM suy luận theo chuỗi) | Rất mạnh (`for`, `while`, `try/catch`, `map/filter`) |
| **Phù hợp cho task** | Phân tích từng bước, hỏi đáp tương tác | Batch processing, refactoring mã nguồn, data migration |

Giải nghĩa thêm: *batch processing* = xử lý một loạt việc cùng lúc; *refactoring* = sắp xếp lại code mà không đổi hành vi; *data migration* = chuyển dữ liệu từ nơi này sang nơi khác.

> **Tóm gọn 1 câu:** Kiểu cũ hợp hỏi-đáp từng bước; code mode hợp việc hàng loạt nhiều bước (refactor, migrate) — nhanh hơn và có logic điều khiển thật.

---

## 7. Best Practices & Security Guardrails

> Phần này tổng hợp việc nên làm và rào chắn an toàn bắt buộc khi chạy code do model sinh ra.

### ✅ Best Practices
- **Strict Typing for SDK**: Cung cấp file định nghĩa `@types/dsh` đầy đủ trong System Prompt để LLM tự động viết code chính xác 100%.
- **Dry-run First**: Thực hiện kiểm tra cú pháp (static analysis/TypeScript compilation — phân tích code mà không chạy nó) trước khi thực thi mã nguồn.
- **Detailed Logging**: Yêu cầu LLM dùng `console.log()` tại các mốc xử lý quan trọng để dễ dàng truy vết trong Event Stream.

> **Tóm gọn 1 câu:** Đưa cho model định nghĩa kiểu đầy đủ, kiểm tra cú pháp trước khi chạy, và bắt log rõ ràng ở các mốc quan trọng.

### 🛡️ Security Guardrails
- **Sandbox Isolation**: Luôn chạy mã trong môi trường cô lập (Docker Container, Worker Threads, hoặc V8 Isolate). Không bao giờ dùng `eval()` hoặc `vm.runInThisContext()`. Taxonomy tier, các control bắt buộc, và runner đã harden được đặc tả trong [`12-sandbox-execution`](../12-sandbox-execution/README.md) — mục này chỉ ghi nhận rằng script Code Mode kế thừa chúng.
- **Resource Constraints**: Thiết lập giới hạn thời gian chạy (`timeoutMs`), dung lượng bộ nhớ (`maxMemory`), và số câu lệnh Shell tối đa. Đây là các giới hạn tài nguyên ở `12` §3 áp cho sandbox Code Mode; hãy đổi ở đó, không đổi ở đây.
- **Permission Approval**: Nếu script thực hiện các thao tác nguy hiểm (vd: `rm -rf` = xóa sạch thư mục, `git push --force` = ghi đè lịch sử commit trên repo remote), Sandbox phải tạm dừng và yêu cầu xác nhận từ phía User. Cơ chế tạm dừng là giao thức `PAUSED:` ở [`15-approval-gates`](../15-approval-gates/README.md) §5 — lưu ý rằng "tạm dừng và hỏi" không giống "từ chối khi hết hạn", và `15` là nơi quyết định cái nào áp dụng.

> **Tóm gọn 1 câu:** Luôn chạy code trong sandbox cô lập với giới hạn tài nguyên, và mọi thao tác nguy hiểm như `rm -rf` hay `git push --force` phải dừng chờ người dùng duyệt.
