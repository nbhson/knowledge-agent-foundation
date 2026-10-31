# 🧪 Evaluation — Đo Lường Chất Lượng Harness

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Evaluation Quan Trọng?](#tại-sao-evaluation-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan Các Công Cụ](#tổng-quan-các-công-cụ)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Hãy thử thế này: bạn đổi prompt system từ "bạn là assistant hữu ích" sang "bạn là senior engineer". Chất lượng lên hay xuống? Bạn thấy harness "hình như ngon hơn rồi", nhưng **bằng chứng đâu?** Bạn thêm RAG lấy top-5 chunks — liệu accuracy có khá hơn thật, hay chỉ tốn thêm token?

> *"If you ship prompt changes without evaluation, you're gambling — not engineering."*

**Evaluation (Eval)** là cách biến cảm giác "hình như ngon hơn" thành **con số đo được**: chấm điểm response, đặt các bản prompt/model cạnh nhau để so, và bắt regression từ sớm trước khi nó lọt ra production.

### Tại Sao Evaluation Quan Trọng?

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Bằng chứng thay vì cảm giác** | Đo accuracy, faithfulness, relevance bằng con số |
| 2 | **Regression detection** | Phát hiện prompt mới làm giảm quality trước khi deploy |
| 3 | **So sánh được** | A/B giữa models, prompts, retrieval strategies |
| 4 | **Harness/11 đối tác thực thi** | Harness/11 dạy *cách* đánh giá — tools đây cho *công cụ* đánh giá |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  EVALUATION MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  harness/11-evaluation     → component chính (metrics)     │
│  harness/05-prompt-builder → eval prompts khác nhau       │
│  harness/02-build-context  → eval retrieval quality (RAGAS)│
│  harness/07-workflow       → eval end-to-end pipeline      │
└────────────────────────────────────────────────────────────┘
```

## Tổng Quan Các Công Cụ

| Công cụ | Mục đích chính | Đặc điểm nổi bật |
|---------|---------------|------------------|
| **PromptFoo** | Eval LLM apps toàn diện | Config-driven, dataset + assertions, chạy local |
| **Deepeval** | Eval pipeline + unit tests | Pytest-style, LLM-as-judge metrics |
| **RAGAS** | RAG-specific evaluation | Đo faithfulness, relevancy, context precision |
| **LangSmith** | Production monitoring cho LLM | Tracing + evals + datasets, tích hợp LangChain/Anthropic/OpenAI |
| **Giskard** | Open-source ML/LLM testing | Phát hiện bias, hallucination, robustness của model |

> **2025-2026 note:** Ragas giờ gọi là **RAGAS** (v2+). LangSmith là lựa chọn hàng đầu cho monitoring production khi dùng Anthropic hoặc OpenAI SDK. Giskard đặc biệt hữu ích khi cần open-source và không muốn phụ thuộc vendor.

### PromptFoo — Config-Driven Eval

> 📄 **Code ví dụ:** [`examples/01-promptfoo-config-driven-eval.yaml`](examples/01-promptfoo-config-driven-eval.yaml)

> 📄 **Code ví dụ:** [`examples/02-promptfoo-config-driven-eval.sh`](examples/02-promptfoo-config-driven-eval.sh)

### Deepeval — Pytest-Style Eval

> 📄 **Code ví dụ:** [`examples/03-deepeval-pytest-style-eval.py`](examples/03-deepeval-pytest-style-eval.py)

### Ragas — RAG-Specific Metrics

> 📄 **Code ví dụ:** [`examples/04-ragas-rag-specific-metrics.py`](examples/04-ragas-rag-specific-metrics.py)

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
evaluation/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) LLM-as-judge, metrics types, datasets
├── 02-setup/            ← (TODO) Cài PromptFoo / Deepeval / Ragas
├── 03-patterns/         ← (TODO) Eval harness trong CI, regression testing
├── 04-savings/          ← (TODO) Chi phí eval, số lần phát hiện bug sớm
└── 05-troubleshooting/  ← (TODO) Judge bias, dataset drift, flaky eval
```

### Lộ Trình Đề Xuất

```
Bước 1: Hiểu harness/11-evaluation — metrics nào phù hợp
   ↓
Bước 2: Tạo dataset test nhỏ (20-50 case) cho task chính (02-setup)
   ↓
Bước 3: PromptFoo — so sánh prompt cũ vs mới, model A vs B (03-patterns)
   ↓
Bước 4: Nếu dùng RAG → Ragas đo retrieval quality (03-patterns)
   ↓
Bước 5: Tích hợp eval vào CI — chặn regression mỗi lần đổi prompt (03-patterns)
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu evaluation component | [harness/11-evaluation](../../harness/11-evaluation/) |
| Prompt engineering | [harness/05-prompt-builder](../../harness/05-prompt-builder/) |
| Context building | [harness/02-build-context](../../harness/02-build-context/) |
| Observability metrics | [tools/observability](../observability/) |
| RAG retrieval | [tools/vector-db](../vector-db/) |

## Case Studies Thực Tế

### 1. Regression Detection Trong CI

> 📄 **Code ví dụ:** [`examples/05-1-regression-detection-trong-ci.yaml`](examples/05-1-regression-detection-trong-ci.yaml)

### 2. So Sánh Prompt Engineering Thay Đổi

```
Baseline:  "Bạn là assistant hữu ích" → accuracy 82%
New:       "Bạn là senior engineer, code production-ready" → accuracy 88% ✅
New2:      "Bạn luôn trả lời chi tiết nhất có thể" → accuracy 74% ❌ (verbose, lạc đề)

→ Quyết định dựa trên số liệu, không dựa trên cảm giác.
```

## Tài Liệu Tham Khảo

- **PromptFoo**: https://www.promptfoo.dev
- **Deepeval**: https://github.com/confident-ai/deepeval
- **RAGAS**: https://docs.ragas.io
- **LangSmith**: https://smith.langchain.com
- **Giskard**: https://www.giskard.ai
- **LLM-as-judge paper**: https://arxiv.org/abs/2306.05685

### Liên Kết Sang Nhánh Khác

- [harness/11-evaluation](../../harness/11-evaluation/) — Evaluation component
- [harness/05-prompt-builder](../../harness/05-prompt-builder/) — Prompt variants để eval
- [tools/observability](../observability/) — Metrics runtime
- [tools/vector-db](../vector-db/) — RAG eval với Ragas
- [AI_AGENT_FRAMEWORK.md](../../AI_AGENT_FRAMEWORK.md) — Framework tổng

---

> **"The goal of evaluation is not to prove your harness is good — it's to catch when it gets worse."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — evaluation*