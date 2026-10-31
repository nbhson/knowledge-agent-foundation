# 🛡️ Guardrails — Lớp An Toàn Cho Harness Tool Calls

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Guardrails Quan Trọng?](#tại-sao-guardrails-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Guardrails](#tổng-quan-các-guardrails)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Hãy hình dung thế này: harness của bạn đang cầm trong tay cả `write_file`, `execute_python`, `send_notification`, `sql_query`. Chỉ cần agent hiểu sai prompt một chút là có thể gọi nhầm `write_file` vào chỗ như... `/etc/passwd`. Hoặc bắn `send_notification` tới cả trăm lần. Hoặc cho `execute_python` chạy lệnh xóa sạch dữ liệu.

LLM vốn không có khái niệm "lỡ tay là toi" — nó chỉ sinh text. **Guardrails là lớp kiểm soát đứng trước đó**, chặn harness làm điều không nên làm ngay trước khi hành động diễn ra.

> *"The model proposes. The guardrail disposes."*

### Tại Sao Guardrails Quan Trọng?

> Trong harness/06-decide-tools-mcp — mọi tool call đều phải đi qua `GUARDRAILS CHECK`: *"Validate permission, safety, rate limit"*.

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Chặn side effects** | Ngăn `write_file` vào vùng cấm, `execute_python` lệnh nguy hiểm |
| 2 | **Permission enforcement** | Tool có `requires_permission="elevated"` → cần approve |
| 3 | **Rate limiting** | `rate_limit_per_minute=60` — chặn agent gọi tool spam |
| 4 | **Output validation** | Kiểm tra output phạm quy trước khi trả vào context |

### Quan Hệ Với Harness

> **Thư mục này là catalog sản phẩm, không phải policy của harness.**
> Mỗi mục bên dưới là một *thư viện cụ thể* mà bạn có thể chọn dùng. Policy **chuẩn về uỷ
> quyền và cách ly** — risk tier, payload bắt buộc cho cổng, timeout-deny (fail closed),
> luật hai-người, giao thức `PAUSED:` — thuộc sở hữu của
> [`harness/15-approval-gates`](../../harness/15-approval-gates/README.md), còn **cơ chế
> cách ly** thuộc về
> [`harness/12-sandbox-execution`](../../harness/12-sandbox-execution/README.md).
> Một thư viện guardrail *kiểm tra*; nó không quyết định cái gì được phép. Nếu bạn đang nghĩ
> ra một risk tier ở đây, nó thuộc về `15`.

```
┌────────────────────────────────────────────────────────────┐
│  GUARDRAILS MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  harness/15-approval-gates    → POLICY chuẩn + giao thức   │
│                                  PAUSED: (giữ policy)      │
│  harness/12-sandbox-execution → tier cách ly chuẩn         │
│                                                            │
│  Guardrails AI            → harness/06 (tool input/output) │
│  NeMo Guardrails (NVIDIA) → harness/07 (workflow rails)    │
│  LlamaGuard (Meta)        → harness/05 (prompt safety)     │
│  Permission/rate limit    → harness/06 (decide tools)      │
└────────────────────────────────────────────────────────────┘
```

```
Tool Decision Pipeline (từ harness/06):
  User Query → Intent → Tool Selector → Parameter Extractor
      → ❯ GUARDRAILS CHECK (validate permission, safety, rate limit)
      → Tool Executor → Result Processor
```

## Tổng Quan Các Guardrails

| Guardrail | Nhà phát hành | Loại | Đặc điểm nổi bật |
|-----------|--------------|------|------------------|
| **Guardrails AI** | Guardrails AI | Open-source | Validators cho input/output, can thiệp structured |
| **NeMo Guardrails** | NVIDIA | Open-source | Rails: input, dialog, retrieval, execution |
| **LlamaGuard** | Meta | Model-based | LLM classifier chuyên phát hiện prompt/response nguy hiểm |

### Guardrails AI — Validate Input/Output

> 📄 **Code ví dụ:** [`examples/01-guardrails-ai-validate-input-output.py`](examples/01-guardrails-ai-validate-input-output.py)

### NeMo Guardrails — Rails Mô Hình Hóa Luồng

> 📄 **Code ví dụ:** [`examples/02-nemo-guardrails-rails-mo-hinh-hoa-luong.py`](examples/02-nemo-guardrails-rails-mo-hinh-hoa-luong.py)

### LlamaGuard — Model-Based Safety Classifier

> 📄 **Code ví dụ:** [`examples/03-llamaguard-model-based-safety-classifier.py`](examples/03-llamaguard-model-based-safety-classifier.py)

### Permission & Rate Limit Trong Harness (harness/06)

> 📄 **Code ví dụ:** [`examples/04-permission-rate-limit-trong-harness-harness-06.py`](examples/04-permission-rate-limit-trong-harness-harness-06.py)

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
guardrails/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Validators, rails, prompt safety, permission checks
├── 02-setup/            ← (TODO) Cài Guardrails AI / NeMo / LlamaGuard
├── 03-patterns/         ← (TODO) Tool-level guard, workflow rails, PII filtering
├── 04-savings/          ← (TODO) Giảm thiểu chi phí do hành động sai
└── 05-troubleshooting/  ← (TODO) False positive, override, bypass
```

### Lộ Trình Đề Xuất

```
Bước 1: Hiểu tool decision pipeline + guardrail position (harness/06)
   ↓
Bước 2: Cài Guardrails AI — validate tool parameters (02-setup)
   ↓
Bước 3: Thêm permission + rate limit cho ToolDefinition (03-patterns)
   ↓
Bước 4: Nâng cấp NeMo Rails cho workflow-level (03-patterns)
   ↓
Bước 5: LlamaGuard cho prompt safety (04-savings đo lường)
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Tool decision pipeline | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Permission system | [harness/08-task](../../harness/08-task/) |
| Safe automation | [harness/10-automation](../../harness/10-automation/) |
| Loop safety | [loop/03-safety](../../loop/03-safety/) |
| Loop gate (cơ học) | [tools/loop-cli](../loop-cli/) |

## Case Studies Thực Tế

### 1. Chặn Tool Damage

> 📄 **Code ví dụ:** [`examples/05-1-chan-tool-damage.py`](examples/05-1-chan-tool-damage.py)

### 2. Rate Limit + Elevated Permission

> 📄 **Code ví dụ:** [`examples/06-2-rate-limit-elevated-permission.py`](examples/06-2-rate-limit-elevated-permission.py)

## Tài Liệu Tham Khảo

- **Guardrails AI**: https://www.guardrailsai.com
- **NeMo Guardrails (NVIDIA)**: https://github.com/NVIDIA/NeMo-Guardrails
- **LlamaGuard (Meta)**: https://ai.meta.com/research/publications/llama-guard

### Liên Kết Sang Nhánh Khác

- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Guardrails check trong pipeline
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (danh sách guardrails)
- [tools/loop-cli](../loop-cli/) — `loop gate` enforce cơ học
- [tools/langchain](../langchain/) — Guardrails trong agent loops

---

> **"A harness without guardrails is a loaded weapon pointed at production."**

---

## ⚠️ Cập nhật 10/2026: Guardrails AI Hub — Thay Đổi Lớn 2026

**Guardrails AI** vẫn phát triển tích cực, nhưng có 2 thay đổi quan trọng:

1. **Validators chuyển sang PyPI chuẩn (7/2026):**Validators không còn qua Guardrails Hub hosted nữa — giờ cài trực tiếp bằng `pip`. Remote inferencing đã ngừng.

> 📄 **Code ví dụ:** [`examples/07-cap-nhat-10-2026-guardrails-ai-hub-thay.py`](examples/07-cap-nhat-10-2026-guardrails-ai-hub-thay.py)

2. **PyPI 0.6.x vẫn active** — framework core vẫn dùng được. Nếu cần thay thế nhẹ hơn:

| Thay thế | Lý do | Link |
|----------|-------|------|
| **Pydantic Validators** | Nhẹ, built-in Python, không cần thêm dependency | https://docs.pydantic.dev/ |
| **NeMo Guardrails** | NVIDIA, open-source, active development | https://github.com/NVIDIA/NeMo-Guardrails |
| **Llama Guard** | Meta, model-based classifier, chạy local | https://ai.meta.com/research/llama-guard |

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — guardrails*