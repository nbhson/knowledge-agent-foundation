# 📊 Observability — Giám Sát & Logging Cho Harness

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Observability Quan Trọng?](#tại-sao-observability-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Công Cụ](#tổng-quan-các-công-cụ)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Harness của bạn đang chạy loop tự động nightly. Một loop bắt đầu tốn 50,000 token mỗi lần thay vì 10,000. Một agent khác gọi tool lặp 10 lần trước khi finish. Một prompt mới làm quality giảm nhưng bạn không biết vì sao.

Không có observability, bạn đang **bay trong đêm tối không đèn**. Không biết cost, không biết attempt nào thành công, không biết tool nào chậm, không biết context nào bị cắt.

> *"You can't optimize what you can't measure. You can't fix what you can't see."*

**Observability cho AI systems** = trace từng LLM call, từng tool call, từng token, từng latency, từng cost — giống như APM cho microservices, nhưng cho agent pipes.

### Tại Sao Observability Quan Trọng?

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Cost tracking** | Biết chính xác mỗi session tốn bao nhiêu token/dollar |
| 2 | **Debug nhanh hơn** | Trace từng tool call, thấy được chain nào fail |
| 3 | **Quality monitoring** | Theo dõi feedback, accuracy, làm regression detection |
| 4 | **Harness/11 evaluation đối tác** | Eval không ý nghĩa nếu không quan sát runtime |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  OBSERVABILITY MAP VS HARNESS COMPONENTS                   │
│                                                            │
│  harness/06-decide-tools-mcp → log tool calls + outcomes   │
│  harness/07-workflow         → trace flow qua components   │
│  harness/11-evaluation       → metrics thu thập được      │
│  harness/10-automation       → monitor automation health   │
└────────────────────────────────────────────────────────────┘
```

```
ToolDefinition đã có sẵn metrics tracking (harness/06):
  avg_latency_ms  → theo dõi tốc độ tool
  success_rate    → theo dõi tỷ lệ thành công
  total_calls     → đếm lượt gọi
```

## Tổng Quan Các Công Cụ

| Công cụ | Nhà phát hành | Đặc điểm nổi bật | Best for |
|---------|--------------|------------------|----------|
| **LangSmith** | LangChain | Tracing + evals + monitoring, tích hợp LangChain tự nhiên | LangChain stack, full lifecycle |
| **Helicone** | Helicone | Proxy LLM API, cost tracking, analytics | Đa framework, không cần sửa code |
| **OpenLLMetry** | Traceloop | OpenTelemetry-based, vendor-neutral | Standardized, multi-provider |
| **Weights & Biases** | W&B | Experiment tracking, LLM evals | ML nghiên cứu, experiment log |

### LangSmith — Trace Từng Bước

```python
from langsmith import Client
from langchain_openai import ChatOpenAI

# Auto-trace mọi LLM call khi dùng LangChain
llm = ChatOpenAI(model="gpt-4", callbacks=[tracing_callback])

# Xem trong LangSmith UI:
#   - Chain steps: retrieve → build → agent → tools
#   - Token usage mỗi call
#   - Latency từng node
#   - Feedback/review của user
```

### Helicone — Proxy Không Cần Sửa Code

```bash
# Cấu hình proxy: thay API base URL
export OPENAI_API_BASE="https://oai.helicone.ai/v1"
export HELICONE_API_KEY="sk-helicone-..."

# Tất cả LLM calls tự động được log + metrics
# → Dashboard: cost, latency, số request, error rate
```

### OpenLLMetry — OpenTelemetry Standard

```python
# OpenTelemetry-compatible — trace chuẩn OTLP
from traceloop.sdk import Traceloop

Traceloop.init(app_name="my_harness")

# Mọi framework (LangChain, LlamaIndex, OpenAI SDK...) tự động trace
# → Export sang Jaeger, Grafana, Datadog, ...
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
observability/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Traces, spans, metrics, token accounting
├── 02-setup/            ← (TODO) Cài Helicone proxy / LangSmith / OpenLLMetry
├── 03-patterns/         ← (TODO) Cost alerts, tool latency SLO, session replay
├── 04-savings/          ← (TODO) Phát hiện token leak, tối ưu prompt qua metrics
└── 05-troubleshooting/  ← (TODO) Trace bị thiếu, context truncation, cost spike
```

### Lộ Trình Đề Xuất

```
Bước 1: Hiểu kết quả đo lường cần thiết cho harness (harness/11)
   ↓
Bước 2: Cài Helicone proxy — nhanh nhất, không cần sửa code (02-setup)
   ↓
Bước 3: Add tracing metadata: session_id, user_id, tool_name (03-patterns)
   ↓
Bước 4: Thiết lập cost alerts + latency SLO cho từng tool (03-patterns)
   ↓
Bước 5: Nếu dùng LangChain → chuyển LangSmith cho deep tracing
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Evaluation metrics | [harness/11-evaluation](../../harness/11-evaluation/) |
| Tool metrics tracking | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Automation health | [harness/10-automation](../../harness/10-automation/) |
| Eval công cụ | [tools/evaluation](../evaluation/) |
| Token bị tốn do bash output | [tools/rtk](../rtk/) |

## Case Studies Thực Tế

### 1. Phát Hiện Token Leak Trong Loop

```
Với observability:
  Loop "ci-sweeper" chạy 5 lần/ngày
  → Thấy: attempt #3 luôn gọi `read_file` 15 lần cùng 1 file
  → Debug: prompt thiếu instruction về caching kết quả
  → Fix: thêm "reuse file contents if already in context" → giảm 40% token
```

### 2. Tool Latency SLO

```python
# ToolDefinition metrics (từ harness/06)
tool.update_metrics(latency_ms=1200, success=True)  # ghi nhận khi gọi

# Dashboard alert:
#   Nếu vector_search.avg_latency_ms > 2000 → cảnh báo
#   Nếu execute_python.success_rate < 0.95 → cảnh báo
```

## Tài Liệu Tham Khảo

- **LangSmith**: https://smith.langchain.com
- **Helicone**: https://www.helicone.ai
- **OpenLLMetry**: https://github.com/traceloop/openllmetry
- **Weights & Biases**: https://wandb.ai

### Liên Kết Sang Nhánh Khác

- [harness/11-evaluation](../../harness/11-evaluation/) — Đo lường hiệu quả harness
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool metrics in registry
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (danh sách monitoring)
- [tools/evaluation](../evaluation/) — Công cụ đánh giá quality
- [tools/rtk](../rtk/) — Giảm token (đối trọng: đo + cắt)

---

> **"Observability turns your harness from a black box into a dashboard."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — observability*