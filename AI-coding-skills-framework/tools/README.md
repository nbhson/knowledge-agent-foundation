# 🧰 Tools — Công Cụ Thực Thi Hỗ Trợ Harness & Loop

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Tools Quan Trọng?](#tại-sao-tools-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã thiết kế một harness hoàn chỉnh — tools, memory, context, guardrails — và bạn đã viết những vòng lặp (loops) tự triage, tự verify. Nhưng có một vấn đề âm thầm: **mỗi lần agent chạy `ls`, `cat`, `git status`, `cargo test`... nó nhận về hàng trăm dòng output**, ngốn hết context window, và trong đống noise đó agent dễ bỏ lỡ chính dòng lỗi quan trọng nhất.

> *"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."*

**Harness Engineering** dạy bạn thiết kế môi trường xung quanh AI. **Tools** là nơi chứa những công cụ thực thi cụ thể — phần mềm bạn cài đặt và cấu hình — để hiện thực hóa lý thuyết đó trong môi trường thật.

Thư mục này không chỉ có **RTK (Rust Token Killer)** — CLI proxy cắt tới 90% bash output — mà còn là nơi tập hợp các công cụ hiện thực hóa **từng component của harness**: framework orchestration, vector databases cho memory, guardrails, observability, và evaluation.

### Tại Sao Tools Quan Trọng?

> **"Một harness lý thuyết hay mà không có công cụ thực thi thì chỉ là slide."**

#### 3 Lý Do Phải Có Tools Directory

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Harness cần "hiện thực hóa"** | Các module trong `harness/` dạy *cách xây dựng* (context compression, tool design...). Tools như RTK là *thứ có sẵn để dùng ngay*, không phải tự code. |
| 2 | **Tiết kiệm token tức thì** | Một lần cài RTK có thể giảm 40-90% token cho các lệnh bash lặp lại — đúng mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md. |
| 3 | **Tách kiến thức khỏi công cụ** | Giữ `harness/` thuần kiến thức (documentation, labs), `loop/` thuần vòng lặp, và `tools/` cho các binary/CLI/plugins hỗ trợ — mỗi nhánh một vai trò rõ ràng. |

## Tổng Quan

**Tools** là nhánh thứ ba của framework, song song với `harness/` (kiến thức) và `loop/` (vòng lặp). Mỗi công cụ là một thư mục con với tutorial riêng, bắt chước cùng convention: `README.md` tổng quan + lộ trình học + các chuyên đề đánh số.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI CODING SKILLS FRAMEWORK                   │
│                                                                     │
│  harness/      → Kiến thức: 7 components, 12 modules (01–12)       │
│  loop/         → Vòng lặp: concepts, patterns, safety, operating   │
│  tools/        → ❯ Công cụ thực thi (binary/CLI/plugins)           │
│     ├── rtk/           →   Rust Token Killer — cắt 90% bash output │
│     ├── loop-cli/      →   Bộ CLI loop-* — scaffold + gate + audit │
│     ├── langchain/     →   LangChain/LangGraph — graph harness     │
│     ├── autogen/       →   AutoGen — multi-agent conversation      │
│     ├── crewai/        →   CrewAI — multi-agent role-based         │
│     ├── vector-db/     →   Vector DBs — memory/RAG retrieval       │
│     ├── guardrails/    →   Lớp an toàn cho tool calls              │
│     ├── observability/ →   Giám sát + logging + cost tracking      │
│     └── evaluation/    →   Đo chất lượng harness response          │
└─────────────────────────────────────────────────────────────────────┘
```

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
tools/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + references
├── rtk/                 ← Tutorial RTK (Rust Token Killer)
│   ├── README.md        ←   Tổng quan RTK: là gì, quan hệ với harness, lộ trình học
│   ├── 01-concepts/     ←   Kiến trúc RTK: hook system, 4 chiến lược nén, luồng dữ liệu
│   ├── 02-setup/        ←   Cài đặt + tích hợp từng AI tool (Claude, Cline, Gemini...)
│   ├── 03-patterns/     ←   Các pattern sử dụng, mỗi pattern một file
│   ├── 04-savings/      ←   Đo lường: rtk gain, discover, session — token saved
│   └── 05-troubleshooting/ ← Xử lý sự cố, failure modes & mitigations
│
├── loop-cli/            ← Bộ CLI `@cobusgreyling/loop-*` (init, audit, gate, sandbox)
│   └── README.md        ←   Scaffold + điều phối loop, Harness Runtime score
│
├── langchain/           ← LangChain/LangGraph — framework xây harness có state
│   └── README.md        ←   StateGraph mô hình 7 components, ToolNode, RAG
│
├── autogen/             ← AutoGen (Microsoft) — multi-agent conversation-based
│   └── README.md        ←   UserProxyAgent = harness, GroupChat orchestration
│
├── crewai/              ← CrewAI — multi-agent role-based
│   └── README.md        ←   Agent/Task/Crew, Process.sequential vs hierarchical
│
├── vector-db/           ← Chroma, Pinecone, Qdrant, Weaviate — memory retrieval
│   └── README.md        ←   Embedding, semantic search, Tier 2 Warm Memory
│
├── guardrails/          ← Guardrails AI, NeMo, LlamaGuard — an toàn tool calls
│   └── README.md        ←   Validators, rails, permission + rate limit
│
├── observability/       ← LangSmith, Helicone, OpenLLMetry, W&B — monitoring
│   └── README.md        ←   Traces, cost tracking, tool latency SLO
│
└── evaluation/          ← PromptFoo, Deepeval, Ragas — đo chất lượng
    └── README.md        ←   Eval suite, regression detection, RAG metrics
```

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/` và `loop/`.

### Lộ Trình Đề Xuất

```
Giai đoạn 1 — Giảm chi phí ngay lập tức:
   Đọc tools/rtk/README.md → cài RTK → áp dụng pattern git-speedup
   ↓
Giai đoạn 2 — Hiện thực hóa harness:
   Chọn framework: langchain/ (graph) HOẶC autogen/crewai (multi-agent)
   Thêm vector-db/ cho memory + RAG retrieval
   ↓
Giai đoạn 3 — Làm an toàn:
   guardrails/ → validate tool calls, permission, rate limit
   ↓
Giai đoạn 4 — Đo lường & giám sát:
   observability/ → cost tracking + latency SLO
   evaluation/ → eval suite chặn regression
   ↓
Giai đoạn 5 — Tự động hóa:
   loop-cli/ → scaffold loops, loop gate trong CI, worktree isolation
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Giảm token bash output | [rtk](rtk/) |
| Hiểu RTK hoạt động thế nào | [rtk/01-concepts](rtk/01-concepts/) |
| Cài đặt + tích hợp RTK vào AI tool | [rtk/02-setup](rtk/02-setup/) |
| Chọn pattern RTK nào dùng trước | [rtk/03-patterns](rtk/03-patterns/) — pattern picker |
| Scaffold + điều phối loops | [loop-cli](loop-cli/) |
| Xây harness bằng graph | [langchain](langchain/) |
| Xây multi-agent harness | [autogen](autogen/) hoặc [crewai](crewai/) |
| Memory + RAG retrieval | [vector-db](vector-db/) |
| An toàn tool calls | [guardrails](guardrails/) |
| Giám sát cost + latency | [observability](observability/) |
| Đo chất lượng response | [evaluation](evaluation/) |

---

## Case Studies Thực Tế

### 1. RTK — Eat Its Own Dogfood

Repo `rtk-ai/rtk` chính là một harness engineering case study: nó hỗ trợ **16 AI coding tools** thông qua cơ chế hook/plugin khác nhau:

| AI Tool | Phương thức tích hợp | Level |
|---------|---------------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

### 2. Stack Hoàn Chỉnh Cho Một Harness Production

```
rtk/           → cắt 90% bash output trước khi vào context
vector-db/     → memory tiers + RAG retrieval (harness/01, 02, 03)
langchain/     → StateGraph orchestrate 7 components (harness/07)
guardrails/    → validate mọi tool call trước khi execute (harness/06)
observability/ → LangSmith trace + Helicone cost (harness/11)
evaluation/    → PromptFoo regression-check trong CI (harness/11)
loop-cli/      → loop gate + worktree isolation cho tự động hóa (harness/10)
```

### 3. Kết Quả Đo Lường RTK

| Command | Output thô | Output RTK | Giảm |
|---------|-----------|------------|------|
| `ls -la` (45 lines) | 45 lines | 12 lines (tree + file counts) | ~73% |
| `git push` (15 lines) | 15 lines | `ok main` (1 line) | ~93% |
| `cargo test` (200+ lines fail) | 200+ | `FAILED: 2/15 tests` + details | ~90% |
| `docker ps` | Nhiều cột | Essential fields only | ~70%+ |
| `ruff check` | Nhiều dòng | Grouped by rule/file | ~80% |

---

## Tài Liệu Tham Khảo

### Công Cụ Trong Nhánh Này

| Tool | Vai trò | Liên kết |
|------|---------|----------|
| **RTK — Rust Token Killer** | CLI proxy nén bash output trước khi vào LLM context | [rtk/](rtk/) · https://github.com/rtk-ai/rtk · https://www.rtk-ai.app |
| **Loop CLI** | Bộ CLI loop-*: init, doctor, audit, gate, sandbox, worktree | [loop-cli/](loop-cli/) · https://github.com/cobusgreyling/loop-engineering |
| **LangChain / LangGraph** | Framework xây harness dạng stateful graph | [langchain/](langchain/) · https://langchain.com |
| **AutoGen (Microsoft)** | Multi-agent harness conversation-based | [autogen/](autogen/) · https://microsoft.github.io/autogen/ |
| **CrewAI** | Multi-agent harness role-based | [crewai/](crewai/) · https://docs.crewai.com |
| **Vector DBs** | Chroma, Pinecone, Qdrant, Weaviate — memory/RAG | [vector-db/](vector-db/) |
| **Guardrails** | Guardrails AI, NeMo, LlamaGuard — an toàn tool calls | [guardrails/](guardrails/) |
| **Observability** | LangSmith, Helicone, OpenLLMetry, W&B | [observability/](observability/) |
| **Evaluation** | PromptFoo, Deepeval, Ragas | [evaluation/](evaluation/) |

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../HARNESS_ENGINEERING.md) — 7 components của harness
- [harness/01-retrieve-memory-knowledge](../harness/01-retrieve-memory-knowledge/) — Retrieval (vector-db)
- [harness/02-build-context](../harness/02-build-context/) — Context Management (nơi RTK đóng vai trò)
- [harness/06-decide-tools-mcp](../harness/06-decide-tools-mcp/) — Tool design & permissions (guardrails)
- [harness/09-multi-agent](../harness/09-multi-agent/) — Multi-agent (autogen, crewai)
- [harness/11-evaluation](../harness/11-evaluation/) — Đo lường hiệu quả (evaluation, observability)
- [loop/](../loop/) — Vòng lặp tự duy trì (loop-cli)
- [MCP_SETUP.md](../MCP_SETUP.md) — MCP ecosystem (harness/06)

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools*