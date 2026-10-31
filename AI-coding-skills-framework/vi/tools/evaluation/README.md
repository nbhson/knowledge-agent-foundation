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

*Phần này giải thích evaluation là gì và vì sao bạn cần nó. Evaluation (Eval) = đo chất lượng hệ thống AI bằng con số.*

Hãy thử thế này: bạn đổi prompt system từ "bạn là assistant hữu ích" sang "bạn là senior engineer". Chất lượng lên hay xuống? Bạn thấy harness "hình như ngon hơn rồi", nhưng **bằng chứng đâu?** Bạn thêm RAG lấy top-5 chunks (RAG = hệ trả lời có tra cứu tài liệu; top-5 chunks = lấy 5 đoạn văn khớp nhất để nhét vào context) — liệu accuracy có khá hơn thật, hay chỉ tốn thêm token?

> *"If you ship prompt changes without evaluation, you're gambling — not engineering."*

**Evaluation (Eval)** là cách biến cảm giác "hình như ngon hơn" thành **con số đo được**: chấm điểm response (câu trả lời), đặt các bản prompt/model cạnh nhau để so, và bắt regression từ sớm trước khi nó lọt ra production (regression = bản mới làm tính năng cũ xấu đi).

> **Tóm gọn 1 câu:** Evaluation biến "hình như tốt hơn" thành con số — đo điểm, so các bản cạnh nhau, và bắt lỗi trước khi tới tay người dùng.

### Tại Sao Evaluation Quan Trọng?

*Cách đọc bảng này: cột "Lý do" nêu lợi ích, cột "Giải thích" nói rõ lợi ích đó nghĩa là gì. Ví dụ, dòng 2: eval giúp phát hiện prompt mới làm giảm chất lượng trước khi deploy (deploy = đưa lên chạy thật cho người dùng).*

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Bằng chứng thay vì cảm giác** | Đo accuracy, faithfulness, relevance bằng con số |
| 2 | **Regression detection** | Phát hiện prompt mới làm giảm quality trước khi deploy |
| 3 | **So sánh được** | A/B giữa models, prompts, retrieval strategies |
| 4 | **Harness/11 đối tác thực thi** | Harness/11 dạy *cách* đánh giá — tools đây cho *công cụ* đánh giá |

*(Chú giải: accuracy = tỉ lệ trả lời đúng; faithfulness = độ trung thành với tài liệu đưa vào; relevance = độ liên quan câu hỏi; A/B = chạy hai bản song song để so; retrieval strategy = cách lấy tài liệu.)*

> **Tóm gọn 1 câu:** Evaluation cho bạn bằng chứng bằng số, bắt regression sớm, và so sánh được các phương án — thay vì đoán mò.

### Quan Hệ Với Harness

*Đoạn sau đối chiếu evaluation với các module harness (số như harness/11 là số thứ tự module). Đọc vế trái = khái niệm, vế phải = module liên quan.*

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

*(metrics = các con số đo lường; end-to-end = đo cả chuỗi từ đầu đến cuối.)*

> **Tóm gọn 1 câu:** harness/11 dạy *cách* đánh giá, còn nhánh tools/evaluation này cho bạn *công cụ* đánh giá — hai bên bổ sung nhau.

## Tổng Quan Các Công Cụ

*Phần này giới thiệu 5 công cụ eval. Chúng không thay thế nhau — mỗi cái phụ trách một câu hỏi khác nhau.*

*Cách đọc bảng này: cột "Mục đích chính" là việc công cụ sinh ra để làm; cột "Đặc điểm nổi bật" là cách nó hoạt động. Ví dụ, PromptFoo điều khiển bằng file cấu hình (config-driven), chạy ngay trên máy bạn nên không tốn tiền server.*

| Công cụ | Mục đích chính | Đặc điểm nổi bật |
|---------|---------------|------------------|
| **PromptFoo** | Eval LLM apps toàn diện | Config-driven, dataset + assertions, chạy local |
| **Deepeval** | Eval pipeline + unit tests | Pytest-style, LLM-as-judge metrics |
| **RAGAS** | RAG-specific evaluation | Đo faithfulness, relevancy, context precision |
| **LangSmith** | Production monitoring cho LLM | Tracing + evals + datasets, tích hợp LangChain/Anthropic/OpenAI |
| **Giskard** | Open-source ML/LLM testing | Phát hiện bias, hallucination, robustness của model |

*(Chú giải: dataset + assertions = bộ dữ liệu test + các điều kiện "phải đúng"; unit test = test từng phần nhỏ kiểu code; LLM-as-judge = dùng AI chấm bài; tracing = ghi lại từng bước chạy; robustness = chịu được tình huống bất thường.)*

> **2025-2026 note:** Ragas giờ gọi là **RAGAS** (v2+). LangSmith là lựa chọn hàng đầu cho monitoring production khi dùng Anthropic hoặc OpenAI SDK. Giskard đặc biệt hữu ích khi cần open-source và không muốn phụ thuộc vendor.

> **Tóm gọn 1 câu:** Năm công cụ năm câu hỏi: PromptFoo so prompt, Deepeval viết test, RAGAS đo RAG, LangSmith theo dõi production, Giskard scan rủi ro — chọn theo câu hỏi bạn cần trả lời.

### PromptFoo — Config-Driven Eval

*PromptFoo điều khiển bằng file cấu hình: bạn khai báo bộ prompt và bộ test, nó chạy và xuất bảng so sánh.*

> 📄 **Code ví dụ:** [`examples/01-promptfoo-config-driven-eval.yaml`](examples/01-promptfoo-config-driven-eval.yaml)

> 📄 **Code ví dụ:** [`examples/02-promptfoo-config-driven-eval.sh`](examples/02-promptfoo-config-driven-eval.sh)

> **Tóm gọn 1 câu:** PromptFoo = viết file cấu hình, chạy một lệnh, nhận bảng so sánh prompt/model — cách nhanh nhất để trả lời "prompt mới có tốt hơn không".

### Deepeval — Pytest-Style Eval

*Deepeval viết eval như viết test code: mỗi case là một hàm assert (assert = câu lệnh "điều kiện này phải đúng, sai là test fail").*

> 📄 **Code ví dụ:** [`examples/03-deepeval-pytest-style-eval.py`](examples/03-deepeval-pytest-style-eval.py)

> **Tóm gọn 1 câu:** Deepeval cho phép eval nằm chung bộ test tự động — chạy cùng `pytest`, fail cùng code hỏng.

### Ragas — RAG-Specific Metrics

*Ragas chuyên đo riêng phần truy xuất tài liệu của RAG (RAG = trả lời dựa trên tài liệu tra cứu được).*

> 📄 **Code ví dụ:** [`examples/04-ragas-rag-specific-metrics.py`](examples/04-ragas-rag-specific-metrics.py)

> **Tóm gọn 1 câu:** Ragas tách riêng lỗi "tìm sai tài liệu" khỏi lỗi "trả lời sai" — chỉ cần khi hệ thống có RAG.

## Lộ Trình Học (Cấu Trúc Thư Mục)

*Phần này cho biết thư mục có gì và nên học theo thứ tự nào. Chữ (TODO) nghĩa là mục còn bỏ trống.*

```
evaluation/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) LLM-as-judge, metrics types, datasets
├── 02-setup/            ← (TODO) Cài PromptFoo / Deepeval / Ragas
├── 03-patterns/         ← (TODO) Eval harness trong CI, regression testing
├── 04-savings/          ← (TODO) Chi phí eval, số lần phát hiện bug sớm
└── 05-troubleshooting/  ← (TODO) Judge bias, dataset drift, flaky eval
```

*(Chú giải: judge bias = AI chấm bài thiên vị; dataset drift = bộ test lệch khỏi dữ liệu thật; flaky eval = kết quả lúc đúng lúc sai không đáng tin.)*

### Lộ Trình Đề Xuất

*Năm bước đi từ lý thuyết tới eval chạy tự động trong CI.*

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

*Cách đọc bảng này: cột trái là điều bạn muốn làm, cột phải là tài liệu nên mở.*

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu evaluation component | [harness/11-evaluation](../../harness/11-evaluation/) |
| Prompt engineering | [harness/05-prompt-builder](../../harness/05-prompt-builder/) |
| Context building | [harness/02-build-context](../../harness/02-build-context/) |
| Observability metrics | [tools/observability](../observability/) |
| RAG retrieval | [tools/vector-db](../vector-db/) |

> **Tóm gọn 1 câu:** Đi theo 5 bước: hiểu metrics → dựng bộ test nhỏ → so sánh bằng PromptFoo → đo RAG bằng Ragas → cắm vào CI để tự chặn regression.

## Case Studies Thực Tế

*Hai tình huống thật: bắt regression trong CI và so sánh các thay đổi prompt.*

### 1. Regression Detection Trong CI

*Tình huống: mỗi lần đổi prompt, CI tự chạy eval; điểm tụt quá ngưỡng là chặn không cho merge.*

> 📄 **Code ví dụ:** [`examples/05-1-regression-detection-trong-ci.yaml`](examples/05-1-regression-detection-trong-ci.yaml)

> **Tóm gọn 1 câu:** Eval trong CI = máy chấm bài tự động đứng trước cửa merge, điểm tụt là không cho qua.

### 2. So Sánh Prompt Engineering Thay Đổi

*Đây là kết quả thật của một lần so ba prompt bằng PromptFoo — đọc để thấy con số quyết định thay cảm giác.*

```
Baseline:  "Bạn là assistant hữu ích" → accuracy 82%
New:       "Bạn là senior engineer, code production-ready" → accuracy 88% ✅
New2:      "Bạn luôn trả lời chi tiết nhất có thể" → accuracy 74% ❌ (verbose, lạc đề)

→ Quyết định dựa trên số liệu, không dựa trên cảm giác.
```

*(Chú giải: baseline = bản gốc làm chuẩn đối chiếu; verbose = dài dòng; production-ready = đủ chất lượng để chạy thật.)*

> **Tóm gọn 1 câu:** Ba prompt ba kết quả (82% / 88% / 74%) — chỉ bảng số này mới cho phép chọn đúng prompt thay vì chọn theo cảm tính.

## Tài Liệu Tham Khảo

*Link gốc của năm công cụ, mở khi cần tài liệu chi tiết.*

- **PromptFoo**: https://www.promptfoo.dev
- **Deepeval**: https://github.com/confident-ai/deepeval
- **RAGAS**: https://docs.ragas.io
- **LangSmith**: https://smith.langchain.com
- **Giskard**: https://www.giskard.ai
- **LLM-as-judge paper**: https://arxiv.org/abs/2306.05685

### Liên Kết Sang Nhánh Khác

*Cách đọc: mỗi dòng là tài liệu liên quan, sau gạch ngang là lý do nên mở nó.*

- [harness/11-evaluation](../../harness/11-evaluation/) — Evaluation component
- [harness/05-prompt-builder](../../harness/05-prompt-builder/) — Prompt variants để eval
- [tools/observability](../observability/) — Metrics runtime
- [tools/vector-db](../vector-db/) — RAG eval với Ragas
- [AI_AGENT_FRAMEWORK.md](../../AI_AGENT_FRAMEWORK.md) — Framework tổng

> **Tóm gọn 1 câu:** Tài liệu chi tiết nằm ở link gốc từng công cụ; cách đánh giá nằm ở harness/11; phần theo dõi runtime nằm ở tools/observability.

---

> **"The goal of evaluation is not to prove your harness is good — it's to catch when it gets worse."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — evaluation*