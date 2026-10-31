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

Phần này giải thích observability là gì, bằng ba sự cố thật. Đọc xong bạn biết vì sao cần giám sát trước khi chọn công cụ.

Hãy hình dung thế này: harness của bạn đang chạy loop tự động mỗi đêm. Bỗng một loop ngốn tới 50.000 token mỗi lần thay vì 10.000 như trước. Một agent khác gọi tool lặp đi lặp lại tới 10 lần mới chịu finish. Một prompt mới làm chất lượng tụt mà bạn chẳng hiểu vì sao. Harness = bộ khung điều khiển agent; loop = vòng lặp agent chạy tự động; token = đơn vị văn bản mà mô hình tính tiền và tính ngữ cảnh.

Không có observability thì đúng là **lái đêm mà tắt đèn**: không biết tốn bao nhiêu cost, attempt nào thành công, tool nào ì ạch, đoạn context nào bị cắt mất. Attempt = một lượt chạy; context = phần thông tin agent nhìn thấy khi quyết định.

> *"You can't optimize what you can't measure. You can't fix what you can't see."*

Dịch ý: không đo được thì không tối ưu được; không nhìn thấy thì không sửa được.

**Observability cho AI systems** nghĩa là trace từng LLM call, từng tool call, từng token, từng latency, từng cost — giống như APM cho microservices, nhưng là bản dành cho agent pipes. Trace = bản ghi từng bước của một lần chạy, như video hành trình của request; LLM call = một lời gọi tới mô hình ngôn ngữ; latency = thời gian chờ kết quả; APM = phần mềm giám sát hiệu năng; microservices = hệ thống tách thành nhiều dịch vụ nhỏ; agent pipe = chuỗi các bước agent chạy nối tiếp nhau.

> **Tóm gọn 1 câu:** Observability là việc ghi lại từng lời gọi, token và độ trễ của agent — không có nó thì bạn sửa hệ thống bằng đoán mò.

### Tại Sao Observability Quan Trọng?

Cách đọc bảng này: cột # là số thứ tự, cột "Lý do" nêu lợi ích, cột "Giải thích" nói rõ lợi ích đó nghĩa là gì.

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Cost tracking** | Biết chính xác mỗi session tốn bao nhiêu token/dollar |
| 2 | **Debug nhanh hơn** | Trace từng tool call, thấy được chain nào fail |
| 3 | **Quality monitoring** | Theo dõi feedback, accuracy, làm regression detection |
| 4 | **Harness/11 evaluation đối tác** | Eval không ý nghĩa nếu không quan sát runtime |

Giải nghĩa các dòng: session = một phiên làm việc của agent; chain = chuỗi bước gọi nối nhau; regression detection = phát hiện chất lượng tụt so với trước; eval = đánh giá chất lượng bằng bộ đề bài; runtime = lúc hệ thống đang chạy thật.

> **Tóm gọn 1 câu:** Observability quan trọng vì nó cho bạn thấy tiền, lỗi và chất lượng — thứ mà eval (harness/11) cần để có ý nghĩa.

### Quan Hệ Với Harness

Phần này vạch ranh giới trách nhiệm: thư mục này chọn công cụ, còn hợp đồng dữ liệu chuẩn nằm ở harness/13.

> **Thư mục này là catalog sản phẩm/công cụ, không phải hợp đồng của harness.**
> Mọi thứ bên dưới là một *vendor hay thư viện cụ thể* mà bạn có thể chọn dùng. Hợp đồng
> event **chuẩn** — harness phát ra điều gì, schema `TrajectoryEvent`, join key, retention,
> redaction — thuộc sở hữu của
> [`harness/13-trajectory-observability`](../../harness/13-trajectory-observability/README.md).
> Chọn công cụ ở đây; tuân thủ hợp đồng ở kia. Nếu bạn thấy mình đang định nghĩa shape của
> event ở đây, nó thuộc về `13`.

Hiểu đoạn trên: catalog = danh mục để chọn; vendor = nhà cung cấp; schema `TrajectoryEvent` = cấu trúc bản ghi một bước của agent; join key = trường chung giúp nối các bản ghi (như số hóa đơn); retention = thời gian giữ dữ liệu; redaction = che dữ liệu nhạy cảm trước khi ghi.

```
┌────────────────────────────────────────────────────────────┐
│  OBSERVABILITY MAP VS HARNESS COMPONENTS                   │
│                                                            │
│  harness/13-trajectory-obser → HỢP ĐỒNG event chuẩn       │
│                              (giữ schema, không phải đây) │
│  harness/06-decide-tools-mcp → log tool calls + outcomes   │
│  harness/07-workflow         → trace flow qua components   │
│  harness/11-evaluation       → metrics thu thập được      │
│  harness/10-automation       → monitor automation health   │
└────────────────────────────────────────────────────────────┘
```

Sơ đồ trên: mỗi dòng là một thành phần harness và phần giám sát tương ứng. Outcome = kết quả của một lần gọi tool; metrics = các con số đo lường.

```
ToolDefinition đã có sẵn metrics tracking (harness/06):
  avg_latency_ms  → theo dõi tốc độ tool
  success_rate    → theo dõi tỷ lệ thành công
  total_calls     → đếm lượt gọi
```

Ba chỉ số này đã có sẵn trong định nghĩa tool (ToolDefinition): độ trễ trung bình tính mili giây, tỉ lệ thành công, tổng lượt gọi. Việc của bạn là đặt ngưỡng cảnh báo lên trên chúng.

> **Tóm gọn 1 câu:** Thư mục này chỉ là danh mục công cụ để bạn chọn; luật về dữ liệu log (schema, thời gian lưu, lọc nhạy cảm) thuộc về harness/13.

## Tổng Quan Các Công Cụ

Phần này so sánh 5 công cụ giám sát để bạn chọn nhanh theo nhu cầu.

Cách đọc bảng này: cột "Công cụ" là tên sản phẩm; "Đặc điểm nổi bật" là nó làm tốt gì; "Best for" là tình huống nên chọn nó. Ví dụ, nếu dữ liệu không được rời khỏi máy thì chọn Langfuse vì nó self-host được.

| Công cụ | Nhà phát hành | Đặc điểm nổi bật | Best for |
|---------|--------------|------------------|----------|
| **LangSmith** | LangChain | Tracing + evals + monitoring, tích hợp LangChain tự nhiên | LangChain stack, full lifecycle |
| **Langfuse** | Langfuse (open source) | Open-source tracing + agent graphs, OTel export, self-host được | Self-host, privacy-sensitive, đa framework |
| **Helicone** | Helicone | Proxy LLM API, cost tracking, analytics | Đa framework, không cần sửa code |
| **OpenLLMetry** | Traceloop | OpenTelemetry-based, vendor-neutral | Standardized, multi-provider |
| **Weights & Biases** | W&B | Experiment tracking, LLM evals | ML nghiên cứu, experiment log |

Giải nghĩa: tracing = ghi vết từng bước; evals = đánh giá chất lượng; proxy = server đứng giữa bạn và API; open source = mã nguồn công khai, tự host được; vendor-neutral = không phụ thuộc nhà cung cấp nào; multi-provider = dùng với nhiều hãng mô hình.

### LangSmith — Trace Từng Bước

Công cụ của LangChain, thấy được cả chuỗi bước `retrieve → build → agent → tools`. Phù hợp khi dự án đã dùng LangChain.

> 📄 **Code ví dụ:** [`examples/01-langsmith-trace-tung-buoc.py`](examples/01-langsmith-trace-tung-buoc.py)

Retrieve = bước tìm kiếm dữ liệu; build = bước dựng prompt; mỗi mũi tên là một bước trong chuỗi xử lý.

> **Tóm gọn 1 câu:** LangSmith cho bạn video từng bước của agent — mạnh nhất khi dự án đã dùng LangChain.

### Helicone — Proxy Không Cần Sửa Code

Đứng giữa bạn và API mô hình: chỉ đổi địa chỉ API là đo được tiền, độ trễ, tỉ lệ lỗi.

> 📄 **Code ví dụ:** [`examples/02-helicone-proxy-khong-can-sua-code.sh`](examples/02-helicone-proxy-khong-can-sua-code.sh)

Đổi lại: nó chỉ thấy lời gọi mô hình, không thấy bên trong chuỗi xử lý.

> **Tóm gọn 1 câu:** Helicone đo được chi phí và độ trễ mà không sửa code — chỉ đổi địa chỉ API sang proxy của nó.

### OpenLLMetry — OpenTelemetry Standard

Công cụ theo chuẩn OpenTelemetry (chuẩn ghi vết mở, dùng chung nhiều backend) — đẩy dữ liệu sang Jaeger, Grafana hay Datadog đều đọc được.

> 📄 **Code ví dụ:** [`examples/03-openllmetry-opentelemetry-standard.py`](examples/03-openllmetry-opentelemetry-standard.py)

> **Tóm gọn 1 câu:** OpenLLMetry phù hợp khi bạn muốn dữ liệu giám sát theo chuẩn mở, đọc được ở nhiều hệ dashboard.

## OpenTelemetry GenAI Semantic Conventions (2025)

Phần này giải thích một chuẩn đặt tên dữ liệu — vì sao nó giúp trace không bị "khóa" vào một nhà cung cấp.

OTel GenAI spec chuẩn hóa traces cho LLM calls:
- span.name: "genai.*"
- genai.* attributes (genai.prompt_tokens, genai.completion_tokens, genai.model)
- Langfuse hỗ trợ OTel export từ LangChain/LangGraph

Ref: https://opentelemetry.io/docs/specs/semconv/gen-ai/

Giải nghĩa: span = một đoạn trong trace (một bước, ví dụ một lời gọi LLM); attribute = trường thông tin gắn vào span. Ví dụ `genai.prompt_tokens` là số token của phần hỏi; `genai.model` là tên mô hình.

Vì sao quan trọng: trước 2025, mỗi vendor tự đặt tên span/attribute riêng nên trace không portable giữa các backend. Với GenAI semantic conventions, cùng một trace đọc được ở Jaeger, Grafana, Datadog hay Langfuse — đổi backend quan sát không phải viết lại instrumentation. OpenLLMetry và Langfuse đều phát thẳng theo chuẩn này. Portable = mang đi dùng ở nơi khác; instrumentation = mã cài đặt để ghi dữ liệu đo.

> **Tóm gọn 1 câu:** Chuẩn OTel GenAI quy định tên thống nhất cho dữ liệu trace, nên bạn đổi bảng điều khiển mà không phải cài lại mã ghi đo.

## Lộ Trình Học (Cấu Trúc Thư Mục)

Phần này vẽ bản đồ thư mục và gợi ý thứ tự đọc.

```
observability/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Traces, spans, metrics, token accounting
├── 02-setup/            ← (TODO) Cài Helicone proxy / LangSmith / OpenLLMetry
├── 03-patterns/         ← (TODO) Cost alerts, tool latency SLO, session replay
├── 04-savings/          ← (TODO) Phát hiện token leak, tối ưu prompt qua metrics
└── 05-troubleshooting/  ← (TODO) Trace bị thiếu, context truncation, cost spike
```

Mỗi thư mục con là một chủ đề; TODO nghĩa là chưa viết xong. Token accounting = sổ kế toán token; session replay = xem lại diễn biến một phiên; context truncation = ngữ cảnh bị cắt bớt; cost spike = chi phí vọt lên đột ngột.

### Lộ Trình Đề Xuất

Thứ tự đọc từng bước: từ hiểu cái cần đo, tới cài công cụ, tới đặt cảnh báo.

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

Metadata = thông tin mô tả gắn kèm bản ghi; ví dụ `session_id` là mã phiên, giúp nối mọi bản ghi của cùng một lượt chạy.

Cách đọc bảng này: cột "Bạn muốn..." là nhu cầu, cột "Đọc" là file nên mở.

| Bạn muốn... | Đọc |
|-------------|-----|
| Evaluation metrics | [harness/11-evaluation](../../harness/11-evaluation/) |
| Tool metrics tracking | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Automation health | [harness/10-automation](../../harness/10-automation/) |
| Eval công cụ | [tools/evaluation](../evaluation/) |
| Token bị tốn do bash output | [tools/rtk](../rtk/) |

> **Tóm gọn 1 câu:** Đi theo 5 bước — hiểu cái cần đo, cài Helicone, gắn metadata, đặt cảnh báo, nâng cấp lên LangSmith nếu dùng LangChain.

## Case Studies Thực Tế

Phần này kể hai ca sửa lỗi thật nhờ có số liệu.

### 1. Phát Hiện Token Leak Trong Loop

```
Với observability:
  Loop "ci-sweeper" chạy 5 lần/ngày
  → Thấy: attempt #3 luôn gọi `read_file` 15 lần cùng 1 file
  → Debug: prompt thiếu instruction về caching kết quả
  → Fix: thêm "reuse file contents if already in context" → giảm 40% token
```

Đọc từ trên xuống: nhờ ghi trace, người ta thấy lượt chạy thứ 3 đọc cùng một file 15 lần; nguyên nhân là prompt thiếu chỉ dẫn tái dùng kết quả; sửa bằng một câu chỉ dẫn và token giảm 40%.

> **Tóm gọn 1 câu:** Không có trace thì không bao giờ biết agent đọc lại cùng một file 15 lần — observability biến đoán mò thành con số.

### 2. Tool Latency SLO

Case này đặt ngưỡng cảnh báo cho độ trễ từng tool.

> 📄 **Code ví dụ:** [`examples/04-2-tool-latency-slo.py`](examples/04-2-tool-latency-slo.py)

> **Tóm gọn 1 câu:** Đặt ngưỡng SLO cho từng tool (ví dụ vector search quá 2 giây thì báo động) để con số đo trở thành hành động.

## Tài Liệu Tham Khảo

Phần này liệt kê trang chủ của các công cụ đã nêu.

- **LangSmith**: https://smith.langchain.com
- **Langfuse**: https://langfuse.com
- **Helicone**: https://www.helicone.ai
- **OpenLLMetry**: https://github.com/traceloop/openllmetry
- **Weights & Biases**: https://wandb.ai
- **OTel GenAI Semantic Conventions**: https://opentelemetry.io/docs/specs/semconv/gen-ai/

> **Tóm gọn 1 câu:** Mỗi dòng là trang chủ của một công cụ đã so sánh ở trên — vào đây để đọc chi tiết cài đặt.

### Liên Kết Sang Nhánh Khác

Cách đọc: mỗi dòng là file liên quan và nó giải quyết việc gì.

- [harness/11-evaluation](../../harness/11-evaluation/) — Đo lường hiệu quả harness
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool metrics in registry
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (danh sách monitoring)
- [tools/evaluation](../evaluation/) — Công cụ đánh giá quality
- [tools/rtk](../rtk/) — Giảm token (đối trọng: đo + cắt)

> **Tóm gọn 1 câu:** Các link này nối giám sát với các mảnh khác: đo chất lượng (harness/11), chỉ số tool (harness/06), và cắt token (tools/rtk).

---

> **"Observability turns your harness from a black box into a dashboard."**

Dịch ý: observability biến harness từ cái hộp đen (không thấy gì bên trong) thành bảng điều khiển (mọi số liệu hiển thị rõ).

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — observability*
