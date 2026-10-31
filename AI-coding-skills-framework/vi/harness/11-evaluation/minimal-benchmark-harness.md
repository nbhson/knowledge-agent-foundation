# 🧪 Minimal Benchmark Harness — Môi Trường Đánh Giá Tối Giản Cho Raw LLM Reasoning

> **Pattern kế thừa từ DeepSeek Harness (Minimal Mode)**: Môi trường đánh giá tối giản nhằm cách ly khả năng suy luận gốc (Raw Reasoning) của LLM khỏi sự can thiệp của các tầng framework phức tạp (heavy prompts, multi-agent orchestration, complex memory pipelines). Hiểu đơn giản: cho model "thi trong phòng trống" — không prompt dài, không trợ giúp ngoài — để đo đúng trí thông minh thật của nó, không phải của hệ thống bao quanh.

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

> Phần này giải thích vì sao cần một môi trường đánh giá "tối giản": kết quả đo thường bị bẩn bởi chính framework bao quanh.

Khi đánh giá hiệu năng của một AI Coding Agent trên các bộ Benchmark như **SWE-bench**, **HumanEval**, hoặc **MBPP**, kết quả đo lường thường bị nhiễu do:
- **System Prompt Overhead**: System Prompt quá dài (2,000+ tokens) định hướng hành vi của mô hình quá mức. (System Prompt = câu lệnh nền chỉ dẫn agent phải làm gì.)
- **Framework Intervention**: Các tầng RAG, Memory Consolidation, hoặc Guardrail tự động chỉnh sửa câu trả lời của mô hình. (RAG = truy xuất tài liệu ngoài; Memory Consolidation = gộp nhớ các phiên cũ; Guardrail = rào chắn an toàn.)
- **Tool Complexity**: Quá nhiều công cụ rườm rà làm suy giảm khả năng chọn công cụ chính xác (Tool Selection Overhead).

**Hệ quả**: Rất khó để trả lời câu hỏi: *"Mô hình LLM này thực sự giỏi suy luận lập trình, hay do Framework Harness che giấu điểm yếu của nó?"*

> **Tóm gọn 1 câu:** Điểm benchmark thường bị nhiễu bởi prompt dài, tầng trung gian và quá nhiều tool — nên cần một môi trường "thi trống" để đo đúng năng lực model.

---

## 2. Triết Lý Minimal Benchmark Harness

> Phần này nêu nguyên tắc cốt lõi: loại bỏ tối đa các thành phần phụ trợ để đo năng lực gốc.

Minimal Benchmark Harness giải quyết vấn đề này bằng nguyên tắc **Isolation Testing** (kiểm thử cách ly — tách đối tượng cần đo khỏi mọi yếu tố gây nhiễu):

```
Minimal Harness = Minimal System Prompt + Zero Framework Middleware + 2 Core Tools (Bash + Editor)
```

Bằng cách loại bỏ toàn bộ các thành phần phụ trợ, hệ thống đo lường chính xác **năng lực tự nhiên (native capability)** của LLM trong việc giải quyết vấn đề kỹ thuật.

> **Tóm gọn 1 câu:** Công thức chỉ có 3 thành phần: prompt ngắn nhất có thể, không tầng trung gian nào, và đúng 2 công cụ — tất cả để đo năng lực "thuần" của model.

---

## 3. Kiến Trúc Môi Trường Minimal Mode

> Phần này cho xem sơ đồ toàn cảnh: bài test đi qua prompt tối giản tới model, model chỉ có 2 công cụ để làm bài.

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

Đọc sơ đồ: từ trái sang phải — bộ test (SWE-bench) nạp đề qua system prompt tối giản "You are a coder..."; model đang kiểm tra chỉ nhận đúng 2 công cụ: `bash` (chạy lệnh, test, git) và `editor` (xem/sửa code).

> **Tóm gọn 1 câu:** Kiến trúc chỉ là một đường thẳng: đề → prompt ngắn → model → 2 công cụ — không có nhánh phụ nào can thiệp.

---

## 4. Bộ Công Cụ Tối Giản (Minimal Tool Set: Bash + Editor)

> Phần này mô tả đúng 2 công cụ model được phép dùng — mỗi tool một định dạng JSON rõ ràng.

Trong Minimal Mode, Agent chỉ được cung cấp đúng **2 công cụ chuẩn hóa**:

### 1. `bash`
Cho phép thi hành lệnh trong terminal của môi trường sandbox:
> 📄 **Code ví dụ:** [`examples/01-1-bash.json`](examples/01-1-bash.json)

> **Tóm gọn 1 câu:** `bash` là "cặp tay" của model — nhận đúng một tham số `command` rồi chạy lệnh trong sandbox.

### 2. `editor`
Cho phép xem và chỉnh sửa file tại các khoảng dòng chỉ định:
> 📄 **Code ví dụ:** [`examples/02-2-editor.json`](examples/02-2-editor.json)

> **Tóm gọn 1 câu:** `editor` là "cặp mắt + bút chì" của model — xem, tạo, và thay file bằng 3 lệnh: `view`, `create`, `str_replace`.

---

## 5. Triển Khai Benchmark Runner (TypeScript Implementation)

> Phần này cho xem code runner — bộ máy điều phối chạy từng bài test trong môi trường cách ly hoàn toàn.

Dưới đây là mã nguồn của một **Minimal Benchmark Runner** cách ly hoàn toàn môi trường chạy:

> 📄 **Code ví dụ:** [`examples/03-5-trien-khai-benchmark-runner-typescript-implementation.ts`](examples/03-5-trien-khai-benchmark-runner-typescript-implementation.ts)

> **Tóm gọn 1 câu:** Runner là "giám thị": nạp bài, cấp 2 công cụ, chạy đủ số lượt, chấm bằng test, và dọn sạch môi trường sau mỗi bài.

---

## 6. Tiêu Chí Đánh Giá & Metrics (SWE-bench / HumanEval)

> Phần này liệt kê 4 chỉ số cần đo khi chạy harness tối giản.

Cách đọc bảng này: cột **METRIC** là tên chỉ số; cột **Ý NGHĨA** giải thích nó đo cái gì; cột **MỤC TIÊU** cho biết nên cao hay thấp (và ngưỡng nếu có). Ví dụ: Tool Error Rate dưới 5% nghĩa là trên 100 lần gọi tool chỉ được dưới 5 lần sai tham số.

| METRIC | Ý NGHĨA | MỤC TIÊU |
|---|---|---|
| **Pass@1 Rate** | Tỷ lệ sửa đúng bug ngay trong lần thử đầu tiên | Cao hơn (đánh giá suy luận chính xác) |
| **Average Turns per Task** | Số lượt đàm thoại trung bình để giải quyết 1 task | Thấp hơn (tiết kiệm chi phí & thời gian) |
| **Tool Error Rate** | Tỷ lệ gọi tool sai tham số / cú pháp | Thấp hơn (< 5%) |
| **Token Efficiency** | Số lượng token tổng cộng tiêu tốn per successful task | Thấp hơn |

> **Tóm gọn 1 câu:** Đo 4 thứ — giải đúng ngay lần đầu (Pass@1), ít lượt thoại, ít gọi tool sai, ít token — đủ để so sánh các model công bằng.

---

## 7. Best Practices & Isolation Guardrails

> Phần này tổng kết luật cách ly: nên làm gì và tránh gì để kết quả không bị bẩn.

### ✅ Best Practices
- **Clean Docker Container**: Reset môi trường Docker sang trạng thái gốc (git clean/reset) trước khi thực hiện từng task benchmark. (Nghĩa là mỗi bài thi đều nhận một "phòng thi" sạch bong.)
- **Zero Injected Memory**: Không nạp bất kỳ dữ liệu từ các session trước để đảm bảo tính khách quan tuyệt đối. (Model không được "nhớ" bài nào khác.)
- **Timeouts & Deadlocks**: Đặt thời gian timeout nghiêm ngặt (vd: 5 phút/task) cho các lệnh bash để tránh treo tiến trình.

> **Tóm gọn 1 câu:** Ba luật nên làm: mỗi bài một container sạch, không nhớ phiên cũ, và có timeout chặt.

### ❌ Anti-Patterns
- **Prompt Leakage / Over-engineering**: Đưa thông tin giải đề hoặc hướng dẫn chi tiết vào System Prompt của Benchmark Harness. (Là "thuộc bài trước khi thi" — điểm không còn đo năng lực thật.)
- **Shared Workspace**: Cho phép các task dùng chung thư mục làm việc dẫn đến side-effect giữa các bài test. (Bài trước để lại rác, bài sau "ăn theo" — kết quả sai.)

> **Tóm gọn 1 câu:** Hai điều cấm: không đưa gợi ý giải đề vào prompt, và không cho các bài dùng chung thư mục — vi phạm một trong hai là toàn bộ kết quả vô giá trị.
