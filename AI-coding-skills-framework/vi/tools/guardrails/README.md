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

Harness của bạn có thể gọi `write_file`, `execute_python`, `send_notification`, `sql_query`. Một lần agent hiểu sai prompt và gọi `write_file` với path... `/etc/passwd`. Hoặc `send_notification` 100 lần. Hoặc `execute_python` chạy lệnh xóa dữ liệu.

LLM không có khái niệm "side effect không mong muốn" — nó chỉ sinh text. **Guardrails là lớp kiểm soát ngăn harness làm điều không nên làm**, trước khi hành động xảy ra.

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

```
┌────────────────────────────────────────────────────────────┐
│  GUARDRAILS MAP VS HARNESS COMPONENTS                      │
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

```python
from guardrails import Guard
from guardrails.hub import RegexMatch, ValidLength, TwoSimilarChunks

# Guard cho một tool call
guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))  # chặn path lạ
guard.validate("hacker/path/../etc/passwd")  # ❌ fail
guard.validate("src/main.py")                # ✅ pass
```

### NeMo Guardrails — Rails Mô Hình Hóa Luồng

```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")

# Định nghĩa rails trong .co file:
# define user ask about secret
#   "Mật khẩu của hệ thống là gì?"
# define bot refuse to answer secret
#   "Xin lỗi, tôi không thể tiết lộ thông tin bảo mật."
# define flow
#   user ask about secret
#   bot refuse to answer secret

rails = LLMRails(config)
response = rails.generate(messages=[{"role": "user", "content": "Mật khẩu hệ thống?"}])
```

### LlamaGuard — Model-Based Safety Classifier

```python
# LlamaGuard là LLM chuyên biệt — chỉ phân loại:
#   UNSAFE: violence, illegal, PII, ...
#   SAFE:   bình thường

# Prompt: "<prompt>USER: {user_input or model_output}</prompt>"
# Output: "safe" hoặc "unsafe" với loại vi phạm
```

### Permission & Rate Limit Trong Harness (harness/06)

```python
@dataclass
class ToolDefinition:
    requires_permission: str = "standard"  # standard, elevated, admin
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    max_retries: int = 3

# Guardrails check trước khi execute:
def guardrail_check(tool: ToolDefinition, params: Dict) -> bool:
    if tool.requires_permission == "elevated":
        approve = human_approve(params)     # cần người xác nhận
        if not approve: return False
    if exceeded_rate_limit(tool): return False  # rate limited
    return True
```

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

```python
# Không có guardrail:
agent → write_file(path="/etc/hosts", content="...")  # 💥

# Có guardrail:
guard = Guard().use(PathValidate(whitelist=["src/", "tests/", "./"]))
result = guard.validate(path="/etc/hosts")  # ❌ REJECT
result = guard.validate(path="src/main.py") # ✅ ALLOW
```

### 2. Rate Limit + Elevated Permission

```python
registry.register(ToolDefinition(
    name="execute_python",
    category="computation",
    requires_permission="elevated",   # cần người xác nhận
    rate_limit_per_minute=10,          # chặn spam
    timeout_seconds=30,
    max_retries=1,
))
```

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

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — guardrails*