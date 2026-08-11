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

Bạn đã đọc `HARNESS_ENGINEERING.md` — hiểu 7 components: retrieve memory, build context, update memory, plan, prompt builder, tool decision, workflow. Bạn muốn **code thật** một harness, không chỉ hiểu lý thuyết.

Bạn có hai lựa chọn: viết từ đầu toàn bộ orchestration (LLM calls, tool routing, memory, retry...), hoặc dùng một framework chuyên nghiệp đã giải quyết 80% bài toán đó.

> **Cách 4 — LangChain / LlamaIndex (Framework chuyên nghiệp)** — trích từ HARNESS_ENGINEERING.md

**LangChain / LangGraph** là framework chuẩn để hiện thực hóa harness engineering: nó cung cấp sẵn tool-calling, memory, RAG, prompt templates, và — với LangGraph — khả năng mô hình hóa luồng harness như một **stateful graph** (retrieve → build → act → update → lặp lại).

### Tại Sao LangChain Quan Trọng?

> **"Every harness concept in this repo has a LangChain module that implements it."**

| Harness Concept | LangChain Module |
|-----------------|------------------|
| LLM abstraction | `ChatOpenAI`, `ChatAnthropic`... |
| Tool calling | `@langchain/core/tools`, `DynamicStructuredTool` |
| Memory (01/03) | `MemorySaver`, `InMemoryChatMessageHistory` |
| Context building (02) | `Retriever`, `DocumentCompressor`, `ContextualCompressionRetriever` |
| Prompt builder (05) | `PromptTemplate`, `ChatPromptTemplate` |
| Tool decision (06) | `create_tool_calling_agent`, `ToolNode` |
| Workflow (07) | `StateGraph`, `langgraph.prebuilt.ToolNode` |

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Production-ready** | Tool calling, retries, streaming, tracing có sẵn |
| 2 | **Stateful graphs (LangGraph)** | Mô hình harness như graph có state — đúng triết lý loop |
| 3 | **Ecosystem rộng** | 700+ integrations, từ vector DBs đến MCP |
| 4 | **Code mẫu sẵn** | HARNESS_ENGINEERING.md đã có TypeScript snippet |

### Quan Hệ Với Harness

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

## Tổng Quan

### LangChain (Core)

Thư viện nền: LLM wrappers, chains, tools, memory, retrievers, prompts.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { DynamicStructuredTool } from "@langchain/core/tools";

const harness = {
  llm: new ChatOpenAI({ model: "gpt-4" }),
  tools: [
    new DynamicStructuredTool({
      name: "search",
      description: "Search the web",
      func: async (input) => { /* ... */ }
    })
  ]
};
```

### LangGraph (Orchestration)

Thêm lớp **stateful graph** — mỗi node là một harness component, có điều kiện rẽ nhánh, có vòng lặp.

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

graph = StateGraph(State)
graph.add_node("retrieve", retrieve_memory)   # harness/01
graph.add_node("build", build_context)        # harness/02
graph.add_node("agent", call_model)           # harness/05 + 06
graph.add_node("tools", ToolNode(tools))      # harness/06

graph.add_edge("retrieve", "build")
graph.add_edge("build", "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")              # vòng lặp — giống loop/
```

Đây chính là triết lý `loop/` — agent không kết thúc sau một lần gọi LLM, mà **lặp lại** cho đến khi hoàn thành.

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
langchain/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Models, prompts, chains, agents, graph state
├── 02-setup/            ← (TODO) Cài đặt @langchain/langgraph, API keys
├── 03-patterns/         ← (TODO) RAG, agent loop, multi-agent supervisor
├── 04-savings/          ← (TODO) Token usage tracking, cost optimization
└── 05-troubleshooting/  ← (TODO) Graph cycles, tool errors, context overflow
```

### Lộ Trình Đề Xuất

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

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu 7 components harness | [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) |
| Tool design & MCP | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Vòng lặp agent | [loop/](../../loop/) |

## Case Studies Thực Tế

### 1. RAG Harness với LangChain

```
harness/01-retrieve → Chroma retriever (xem tools/vector-db/)
harness/02-build    → ContextualCompressionRetriever (nén context)
harness/05-prompt   → ChatPromptTemplate với retrieved docs
harness/06-tool     → ToolNode gọi web_search, query_db
```

### 2. Agent Loop (LangGraph)

```python
# Agent action loop — giống loop/ nhưng trong graph
while True:
    action = agent.invoke(state)       # harness/04 plan
    if action.type == "finish": break  # trả lời user
    result = execute_tool(action)      # harness/06 execute
    state = update_memory(result)      # harness/03 update
```

## Tài Liệu Tham Khảo

- **LangChain**: https://langchain.com
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Academy**: https://academy.langchain.com
- **Blog**: https://blog.langchain.dev
- **Discord**: https://langchain.ai/discord

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (code mẫu)
- [tools/vector-db](../vector-db/) — RAG retrievers
- [tools/observability](../observability/) — LangSmith tracing
- [tools/evaluation](../evaluation/) — LangSmith evals, Ragas

---

> **"A harness is just a graph — LangGraph gives you the nodes and edges."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — langchain*