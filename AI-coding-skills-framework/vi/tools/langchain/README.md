# 🦜️🔗 LangChain / LangGraph — Framework Xây Dựng Harness

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao LangChain Quan Trọng?](#tại-sao-langchain-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

*Phần này giải vì sao nên dùng framework thay vì tự viết mọi thứ. Framework = bộ khung code có sẵn.*

Giả sử bạn đã đọc `HARNESS_ENGINEERING.md` — đã nắm 7 components (component = một bộ phận chức năng, như bộ nhớ hay bộ chọn tool): retrieve memory, build context, update memory, plan, prompt builder, tool decision, workflow. Giờ bạn muốn **code thật** một harness, chứ không dừng ở lý thuyết.

Tới đây thường chỉ có hai hướng: tự viết lại toàn bộ orchestration từ đầu (LLM calls, tool routing, memory, retry... — orchestration = điều phối, retry = thử lại khi lỗi), hoặc mượn một framework đã làm hộ mình 80% việc đó.

> **Cách 4 — LangChain / LlamaIndex (Framework chuyên nghiệp)** — trích từ HARNESS_ENGINEERING.md

**LangChain / LangGraph** là framework quen thuộc để biến harness engineering thành code thật: có sẵn tool-calling (cơ chế model gọi công cụ), memory, RAG (trả lời dựa trên tài liệu tra cứu), prompt templates (khung prompt có chỗ điền), và — với LangGraph — bạn vẽ luôn luồng harness thành một **stateful graph** (đồ thị có trạng thái: nhớ được kết quả các bước trước) (retrieve → build → act → update → lặp lại).

> **Tóm gọn 1 câu:** LangChain/LangGraph cho bạn sẵn 80% khối ghép của harness — thay vì tự viết lại điều phối, memory, tool-calling từ đầu.

### Tại Sao LangChain Quan Trọng?

*Phần này chứng minh nhận định: mỗi khái niệm harness đều có module LangChain tương đương.*

> **"Every harness concept in this repo has a LangChain module that implements it."**

*Cách đọc bảng này: cột trái là khái niệm harness (số như 01, 05 là số module), cột phải là module LangChain hiện thực nó. Ví dụ, dòng "Prompt builder (05)" nghĩa là module harness/05 tương đương `ChatPromptTemplate`.*

| Harness Concept | LangChain Module |
|-----------------|------------------|
| LLM abstraction | `ChatOpenAI`, `ChatAnthropic`... |
| Tool calling | `@langchain/core/tools`, `DynamicStructuredTool` |
| Memory (01/03) | `MemorySaver`, `InMemoryChatMessageHistory` |
| Context building (02) | `Retriever`, `DocumentCompressor`, `ContextualCompressionRetriever` |
| Prompt builder (05) | `PromptTemplate`, `ChatPromptTemplate` |
| Tool decision (06) | `create_tool_calling_agent`, `ToolNode` |
| Workflow (07) | `StateGraph`, `langgraph.prebuilt.ToolNode` |

*(Chú giải: LLM abstraction = lớp bọc gọi model; Retriever = bộ tra cứu tài liệu; DocumentCompressor = bộ nén văn bản.)*

*Cách đọc bảng dưới đây: cột "Lý do" là lợi ích, cột "Giải thích" là ý nghĩa cụ thể.*

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Production-ready** | Tool calling, retries, streaming, tracing có sẵn |
| 2 | **Stateful graphs (LangGraph)** | Mô hình harness như graph có state — đúng triết lý loop |
| 3 | **Ecosystem rộng** | 700+ integrations, từ vector DBs đến MCP |
| 4 | **Code mẫu sẵn** | HARNESS_ENGINEERING.md đã có TypeScript snippet |

*(Chú giải: streaming = in kết quả ra dần dần; tracing = ghi lại từng bước chạy; integration = phần kết nối dịch vụ ngoài; snippet = đoạn code mẫu.)*

> **Tóm gọn 1 câu:** Mỗi khái niệm harness có một module LangChain tương đương, đã sản xuất được — dùng nó thay vì viết lại từ đầu.

### Quan Hệ Với Harness

*Bản đồ đối chiếu: vế trái là module harness (số thứ tự 01–07), vế phải là bộ phận LangChain phục vụ module đó.*

```
┌────────────────────────────────────────────────────────────┐
│  LANGCHAIN MAP VS HARNESS COMPONENTS                       │
│                                                            │
│  harness/01-retrieve-memory-knowledge → Retrievers, Memory │
│  harness/02-build-context            → DocumentCompressor │
│  harness/03-update-memory-store      → MemorySaver/Store  │
│  harness/04-plan-decompose-task      → Planner nodes      │
│  harness/05-prompt-builder           → PromptTemplates    │
│  harness/06-decide-tools-mcp         → ToolNode, DynamicTools│
│  harness/07-workflow                 → StateGraph          │
└────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Đọc bảng trên theo hàng: mỗi module harness có đúng một bộ phận LangChain tương đương — đó là bản đồ tra cứu khi bắt tay code.

## Tổng Quan

*Phần này tách hai tầng của framework: LangChain (nền) và LangGraph (điều phối).*

### LangChain (Core)

Thư viện nền: gồm LLM wrappers (lớp bọc gọi model), chains, tools, memory, retrievers, prompts.

> 📄 **Code ví dụ:** [`examples/01-langchain-core.ts`](examples/01-langchain-core.ts)

> **Tóm gọn 1 câu:** LangChain Core = hộp đồ nghề nền: gọi model, định nghĩa tool, giữ memory, dựng prompt.

### LangGraph (Orchestration)

LangGraph đắp thêm một lớp **stateful graph** — mỗi node là một harness component (node = một điểm làm một việc trong đồ thị), muốn rẽ nhánh có điều kiện cũng được, muốn cho lặp lại cũng xong.

> 📄 **Code ví dụ:** [`examples/02-langgraph-orchestration.py`](examples/02-langgraph-orchestration.py)

Đây đúng là tinh thần của `loop/` — agent không gọi LLM một phát rồi thôi, mà **lặp lại** cho tới khi xong việc.

> **Tóm gọn 1 câu:** LangGraph = LangChain + vòng lặp: vẽ harness thành đồ thị, agent lặp lại bước nào cần lặp cho tới khi xong.

## Lộ Trình Học (Cấu Trúc Thư Mục)

*Bản đồ thư mục và thứ tự học. Chữ (TODO) nghĩa là mục còn bỏ trống.*

```
langchain/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Models, prompts, chains, agents, graph state
├── 02-setup/            ← (TODO) Cài đặt @langchain/langgraph, API keys
├── 03-patterns/         ← (TODO) RAG, agent loop, multi-agent supervisor
├── 04-savings/          ← (TODO) Token usage tracking, cost optimization
└── 05-troubleshooting/  ← (TODO) Graph cycles, tool errors, context overflow
```

*(Chú giải: API key = khoá xác thực gọi dịch vụ; supervisor = agent quản lý các agent khác; graph cycle = vòng lặp trong đồ thị; context overflow = context quá dài vượt giới hạn model.)*

### Lộ Trình Đề Xuất

*Năm bước từ đọc code mẫu tới hệ thống có theo dõi. Làm theo thứ tự.*

```
Bước 1: Đọc HARNESS_ENGINEERING.md section 9.1 — code mẫu TS có sẵn
   ↓
Bước 2: Code harness đơn giản bằng LangChain core (llm + tools + memory)
   ↓
Bước 3: Chuyển sang LangGraph — StateGraph mô hình 7 components
   ↓
Bước 4: Thêm ToolNode + MCP adapters (harness/06)
   ↓
Bước 5: Thêm tracing bằng LangSmith (xem tools/observability/)
```

*(Chú giải: MCP adapter = cầu nối tới MCP server, chuẩn kết nối công cụ; tracing = ghi lại từng bước chạy.)*

*Cách đọc bảng này: cột trái là điều bạn muốn làm, cột phải là tài liệu nên mở.*

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu 7 components harness | [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) |
| Tool design & MCP | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Vòng lặp agent | [loop/](../../loop/) |

> **Tóm gọn 1 câu:** Bắt đầu từ code mẫu có sẵn, dựng harness nền (llm + tools + memory), rồi mới lên đồ thị LangGraph và cắm thêm tool, tracing.

## Case Studies Thực Tế

*Hai cách lắp phổ biến: RAG và agent loop.*

### 1. RAG Harness với LangChain

*Bảng gắn module vào từng bước harness — đọc vế trái = bước, vế phải = module dùng.*

```
harness/01-retrieve → Chroma retriever (xem tools/vector-db/)
harness/02-build    → ContextualCompressionRetriever (nén context)
harness/05-prompt   → ChatPromptTemplate với retrieved docs
harness/06-tool     → ToolNode gọi web_search, query_db
```

> **Tóm gọn 1 câu:** RAG harness = tra tài liệu (Chroma), nén cho gọn (ContextualCompressionRetriever), dán vào prompt, cho agent gọi tool khi cần.

### 2. Agent Loop (LangGraph)

*Tình huống: agent tự lặp vòng nghĩ → gọi tool → đọc kết quả → nghĩ tiếp cho tới khi xong.*

> 📄 **Code ví dụ:** [`examples/03-2-agent-loop-langgraph.py`](examples/03-2-agent-loop-langgraph.py)

> **Tóm gọn 1 câu:** Agent loop = đồ thị có cạnh quay về node model — agent tự lặp cho tới khi quyết định dừng.

## Tài Liệu Tham Khảo

*Link gốc của LangChain và các nhánh liên quan trong repo.*

- **LangChain**: https://langchain.com
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Academy**: https://academy.langchain.com
- **Blog**: https://blog.langchain.dev
- **Discord**: https://langchain.ai/discord

### Liên Kết Sang Nhánh Khác

*Cách đọc: mỗi dòng là tài liệu liên quan, sau gạch ngang là lý do nên mở nó.*

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (code mẫu)
- [tools/vector-db](../vector-db/) — RAG retrievers
- [tools/observability](../observability/) — LangSmith tracing
- [tools/evaluation](../evaluation/) — LangSmith evals, Ragas

> **Tóm gọn 1 câu:** Code mẫu nằm ở HARNESS_ENGINEERING.md mục 9.1; tài liệu RAG và theo dõi nằm ở tools/vector-db và tools/observability.

---

> **"A harness is just a graph — LangGraph gives you the nodes and edges."**

---

## ⚠️ Cập nhật 10/2026: LangChain 1.0 (10/2025)

*Phần này tóm tắt các thay đổi lớn của LangChain 1.0 để bạn không đọc tài liệu lỗi thời.*

LangChain 1.0 phát hành 10/2025 với thay đổi lớn:
- `create_agent` là API chính (thay nhiều chain utilities — chain utilities = các hàm ghép bước cũ)
- LangGraph tích hợp sẵn cho stateful workflows (workflow = luồng công việc nhiều bước)
- LCEL vẫn hoạt động nhưng được khuyến nghị dùng qua agents (LCEL = cú pháp ghép các bước bằng dấu `|`)
- Package mới: `langchain` core tách khỏi `langchain-community` (tách = cài riêng phần lõi khỏi phần cộng đồng)
- Python 3.10+ bắt buộc (3.9 EOL tháng 10/2025 — EOL = hết thời gian hỗ trợ)

Migration: https://docs.langchain.com/oss/python/langchain/migration

> **Tóm gọn 1 câu:** LangChain 1.0 dùng `create_agent` làm API chính, tích hợp LangGraph sẵn, và đòi Python 3.10 trở lên — xem link migration trước khi nâng cấp.

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — langchain*