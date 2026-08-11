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

Bạn đổi prompt system từ "bạn là assistant hữu ích" sang "bạn là senior engineer". Quality tăng — hay giảm? Bạn nói harness "tốt hơn", nhưng **bằng chứng đâu?** Bạn thêm RAG với top-5 chunks — có thật sự cải thiện answer accuracy hay chỉ tốn thêm token?

> *"If you ship prompt changes without evaluation, you're gambling — not engineering."*

**Evaluation (Eval)** là cách biến "cảm giác tốt hơn" thành **con số đo được**: chấm điểm response, so sánh giữa các phiên bản prompt/model, phát hiện regression trước khi nó tới production.

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
| **Ragas** | RAG-specific evaluation | Đo faithfulness, relevancy, context precision |

### PromptFoo — Config-Driven Eval

```yaml
# promptfooconfig.yaml
prompts:
  - "Summarize: {{input}}"
  - "Provide a concise summary: {{input}}"

providers:
  - openai:gpt-4
  - anthropic:claude-3-5-sonnet

tests:
  - vars:
      input: "Long technical document..."
    assert:
      - type: contains
        value: "key concept"
      - type: cost
        threshold: 0.05  # mỗi prompt ≤ $0.05
```

```bash
promptfoo eval   # chạy toàn bộ test suite
promptfoo view   # xem bảng so sánh providers + prompts
```

### Deepeval — Pytest-Style Eval

```python
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

def test_harness_answer():
    test_case = LLMTestCase(
        input="BHYT áp dụng cho đối tượng nào?",
        actual_output=harness.run("BHYT áp dụng cho đối tượng nào?"),
        retrieval_context=retrieved_chunks,
    )
    assert_test(test_case, [AnswerRelevancyMetric(), FaithfulnessMetric()])
```

### Ragas — RAG-Specific Metrics

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

dataset = load_your_qa_dataset()
results = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision])

# faithfulness        → câu trả lời có đúng với context không
# answer_relevancy    → câu trả lời có liên quan câu hỏi không
# context_precision   → chunks retrieved có đủ/đúng không
```

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

```yaml
# .github/workflows/evals.yml
steps:
  - run: promptfoo eval --share   # chạy eval suite
  - run: promptfoo regression-check  # so sánh với baseline
  # fail CI nếu accuracy giảm > 5%
```

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
- **Ragas**: https://docs.ragas.io
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