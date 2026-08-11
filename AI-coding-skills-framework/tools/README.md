# 🧰 Tools — Công Cụ Thực Thi Hỗ Trợ Harness & Loop

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Tools Quan Trọng?](#tại-sao-tools-quan-trọng)
> - [Tổng Quan (Nhóm Tools)](#tổng-quan-nhóm-tools)
> - [Cấu Trúc Thư Mục Theo 4 Nhóm](#cấu-trúc-thư-mục-theo-4-nhóm)
> - [Lộ Trình Học](#lộ-trình-học)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã thiết kế một harness hoàn chỉnh — tools, memory, context, guardrails — và bạn đã viết những vòng lặp (loops) tự triage, tự verify. Nhưng có một vấn đề âm thầm: **mỗi lần agent chạy `ls`, `cat`, `git status`, `cargo test`... nó nhận về hàng trăm dòng output**, ngốn hết context window, và trong đống noise đó agent dễ bỏ lỡ chính dòng lỗi quan trọng nhất.

> *"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."*

**Harness Engineering** dạy bạn thiết kế môi trường xung quanh AI. **Tools** là nơi chứa những công cụ thực thi cụ thể — phần mềm bạn cài đặt và cấu hình — để hiện thực hóa lý thuyết đó trong môi trường thật.

Thư mục này tập hợp các công cụ hiện thực hóa **từng component của harness**, được phân nhóm theo vai trò: **Tool** (RTK, Loop CLI), **Framework** (LangChain, AutoGen, CrewAI), **Vector DBs** (memory/RAG), và **MCP Ecosystem** (kết nối tools qua MCP) — cùng các tầng **Security** (guardrails) và **Quality** (observability, evaluation).

### Tại Sao Tools Quan Trọng?

> **"Một harness lý thuyết hay mà không có công cụ thực thi thì chỉ là slide."**

#### 3 Lý Do Phải Có Tools Directory

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Harness cần "hiện thực hóa"** | Các module trong `harness/` dạy *cách xây dựng* (context compression, tool design...). Tools như RTK là *thứ có sẵn để dùng ngay*, không phải tự code. |
| 2 | **Tiết kiệm token tức thì** | Một lần cài RTK có thể giảm 40-90% token cho các lệnh bash lặp lại — đúng mục tiêu "Giảm Chi Phí 40-60%" trong HARNESS_ENGINEERING.md. |
| 3 | **Tách kiến thức khỏi công cụ** | Giữ `harness/` thuần kiến thức (documentation, labs), `loop/` thuần vòng lặp, và `tools/` cho các binary/CLI/plugins hỗ trợ — mỗi nhánh một vai trò rõ ràng. |

## Tổng Quan (Nhóm Tools)

**Tools** là nhánh thứ ba của framework, song song với `harness/` (kiến thức) và `loop/` (vòng lặp). Mỗi công cụ là một thư mục con với tutorial riêng, bắt chước cùng convention: `README.md` tổng quan + lộ trình học + các chuyên đề đánh số.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI CODING SKILLS FRAMEWORK                   │
│                                                                     │
│  harness/      → Kiến thức: 7 components, 12 modules (01–12)       │
│  loop/         → Vòng lặp: concepts, patterns, safety, operating   │
│  tools/        → ❯ Công cụ thực thi (binary/CLI/plugins)           │
└─────────────────────────────────────────────────────────────────────┘
```

## Cấu Trúc Thư Mục Theo 4 Nhóm

Các công cụ được nhóm theo **vai trò kiến trúc** — giúp bạn biết chính xác công cụ nào giải quyết vấn đề nào trong harness:

### 🔧 Nhóm 1 — Tool (Công cụ tối ưu môi trường AI)

> Các binary/CLI cài trực tiếp, giúp tối ưu cách agent tương tác với môi trường.

```
tools/
├── rtk/           →   Rust Token Killer — cắt 90% bash output khỏi context
│   ├── README.md        ←   Tổng quan RTK: là gì, quan hệ với harness, lộ trình học
│   ├── 01-concepts/     ←   Kiến trúc RTK: hook system, 4 chiến lược nén, luồng dữ liệu
│   ├── 02-setup/        ←   Cài đặt + tích hợp từng AI tool (Claude, Cline, Gemini...)
│   ├── 03-patterns/     ←   Các pattern sử dụng, mỗi pattern một file
│   ├── 04-savings/      ←   Đo lường: rtk gain, discover, session — token saved
│   └── 05-troubleshooting/ ← Xử lý sự cố, failure modes & mitigations
│
└── loop-cli/      →   Bộ CLI loop-*: init, doctor, audit, gate, sandbox, worktree
    └── README.md        ←   Scaffold + điều phối loop, Harness Runtime score
```

### 🏗️ Nhóm 2 — Framework (Xây dựng harness orchestration)

> Các framework lập trình để hiện thực hóa harness thành code thật.

```
tools/
├── langchain/     →   LangChain/LangGraph — graph-based harness framework
│   └── README.md        ←   StateGraph mô hình 7 components, ToolNode, RAG
│
├── autogen/       →   AutoGen (Microsoft) — multi-agent conversation-based
│   └── README.md        ←   UserProxyAgent = harness, GroupChat orchestration
│
└── crewai/        →   CrewAI — multi-agent role-based
    └── README.md        ←   Agent/Task/Crew, Process.sequential vs hierarchical
```

### 🗄️ Nhóm 3 — Vector DBs (Memory & Retrieval)

> Lưu trữ và truy xuất memory ngữ nghĩa cho harness/01-03.

```
tools/
└── vector-db/     →   Chroma, Pinecone, Qdrant, Weaviate — memory/RAG
    └── README.md        ←   Embedding, semantic search, Tier 2 Warm Memory
```

### 🔌 Nhóm 4 — MCP Ecosystem (Kết nối Tools ↔ AI)

> Giao thức chuẩn hóa cách AI apps kết nối external tools & data (harness/06).

```
tools/
└── mcp-ecosystem/ →   MCP Protocol — server/client, tools/resources
    └── README.md        ←   GitHub MCP server, thêm MCP servers, registry adapter
```

### 🛡️ Tầng Security (An toàn tool calls)

> Lớp kiểm soát trước khi agent hành động — ngăn side effects không mong muốn.

```
tools/
└── guardrails/    →   Guardrails AI, NeMo, LlamaGuard
    └── README.md        ←   Validators, rails, permission + rate limit (harness/06)
```

### 📊 Tầng Quality (Đo lường & giám sát)

> Chặn regression, theo dõi cost/latency, đảm bảo harness chạy đúng & rẻ.

```
tools/
├── observability/ →   LangSmith, Helicone, OpenLLMetry, W&B
│   └── README.md        ←   Traces, cost tracking, tool latency SLO (harness/11)
│
└── evaluation/    →   PromptFoo, Deepeval, Ragas
    └── README.md        ←   Eval suite, regression detection, RAG metrics (harness/11)
```

---

### Tổng Kết Cây Thư Mục Đầy Đủ

```
tools/
├── README.md              ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình + references
│
│  🔧 NHÓM 1 — TOOL
├── rtk/                   ← Rust Token Killer — cắt 90% bash output
│   ├── README.md
│   ├── 01-concepts/
│   ├── 02-setup/
│   ├── 03-patterns/
│   ├── 04-savings/
│   └── 05-troubleshooting/
├── loop-cli/              ← Bộ CLI loop-* (init, audit, gate, sandbox)
│   └── README.md
│
│  🏗️ NHÓM 2 — FRAMEWORK
├── langchain/             ← LangChain/LangGraph — graph harness
│   └── README.md
├── autogen/               ← AutoGen — multi-agent conversation
│   └── README.md
├── crewai/                ← CrewAI — multi-agent role-based
│   └── README.md
│
│  🗄️ NHÓM 3 — VECTOR DBS
├── vector-db/             ← Chroma, Pinecone, Qdrant, Weaviate
│   └── README.md
│
│  🔌 NHÓM 4 — MCP ECOSYSTEM
├── mcp-ecosystem/         ← MCP Protocol — kết nối tools ↔ AI
│   └── README.md
│
│  🛡️ TẦNG SECURITY
├── guardrails/            ← Guardrails AI, NeMo, LlamaGuard
│   └── README.md
│
│  📊 TẦNG QUALITY
├── observability/         ← LangSmith, Helicone, OpenLLMetry
│   └── README.md
└── evaluation/            ← PromptFoo, Deepeval, Ragas
    └── README.md
```

> Mỗi thư mục chứa một `README.md` — đồng nhất với convention của `harness/` và `loop/`.

## Lộ Trình Học

### Theo Nhóm (Stack Theo Nhu Cầu)

| Nhu cầu | Nhóm | Công cụ |
|---------|------|---------|
| Giảm ngay chi phí token bash | 🔧 Tool | [rtk](rtk/) |
| Tự động hóa loop an toàn | 🔧 Tool | [loop-cli](loop-cli/) |
| Xây harness bằng graph | 🏗️ Framework | [langchain](langchain/) |
| Xây multi-agent harness | 🏗️ Framework | [autogen](autogen/) · [crewai](crewai/) |
| Memory + semantic retrieval | 🗄️ Vector DBs | [vector-db](vector-db/) |
| Kết nối tools qua MCP | 🔌 MCP Ecosystem | [mcp-ecosystem](mcp-ecosystem/) |
| An toàn tool calls | 🛡️ Security | [guardrails](guardrails/) |
| Giám sát cost/latency | 📊 Quality | [observability](observability/) |
| Đo chất lượng response | 📊 Quality | [evaluation](evaluation/) |

### Lộ Trình Đề Xuất (6 Giai Đoạn)

```
Giai đoạn 1 — Giảm chi phí ngay lập tức:
   rtk/ → cài RTK → áp dụng pattern git-speedup
   ↓
Giai đoạn 2 — Hiện thực hóa harness:
   Chọn framework: langchain/ (graph) HOẶC autogen/crewai (multi-agent)
   Thêm vector-db/ cho memory + RAG retrieval
   ↓
Giai đoạn 3 — Kết nối tools:
   mcp-ecosystem/ → đăng ký MCP servers vào harness/06 registry
   ↓
Giai đoạn 4 — Làm an toàn:
   guardrails/ → validate tool calls, permission, rate limit
   ↓
Giai đoạn 5 — Đo lường & giám sát:
   observability/ → cost tracking + latency SLO
   evaluation/ → eval suite chặn regression
   ↓
Giai đoạn 6 — Tự động hóa:
   loop-cli/ → scaffold loops, loop gate trong CI, worktree isolation
```

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

### 2. Stack Hoàn Chỉnh Cho Một Harness Production (Theo Nhóm)

```
🔧 TOOL
rtk/           → cắt 90% bash output trước khi vào context (harness/02)

🗄️ VECTOR DBS
vector-db/     → memory tiers + RAG retrieval (harness/01, 02, 03)

🏗️ FRAMEWORK
langchain/     → StateGraph orchestrate 7 components (harness/07)

🔌 MCP ECOSYSTEM
mcp-ecosystem/ → GitHub MCP + custom MCP servers vào registry (harness/06)

🛡️ SECURITY
guardrails/    → validate mọi tool call trước khi execute (harness/06)

📊 QUALITY
observability/ → LangSmith trace + Helicone cost (harness/11)
evaluation/    → PromptFoo regression-check trong CI (harness/11)

🔧 TOOL (tự động hóa)
loop-cli/      → loop gate + worktree isolation cho automation (harness/10)
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

### Theo 4 Nhóm

#### 🔧 Tool

| Công cụ | Vai trò | Liên kết |
|---------|---------|----------|
| **RTK — Rust Token Killer** | CLI proxy nén bash output trước khi vào LLM context | [rtk/](rtk/) · https://github.com/rtk-ai/rtk · https://www.rtk-ai.app |
| **Loop CLI** | Bộ CLI loop-*: init, doctor, audit, gate, sandbox, worktree | [loop-cli/](loop-cli/) · https://github.com/cobusgreyling/loop-engineering |

#### 🏗️ Framework

| Framework | Vai trò | Liên kết |
|-----------|---------|----------|
| **LangChain / LangGraph** | Framework xây harness dạng stateful graph | [langchain/](langchain/) · https://langchain.com |
| **AutoGen (Microsoft)** | Multi-agent harness conversation-based | [autogen/](autogen/) · https://microsoft.github.io/autogen/ |
| **CrewAI** | Multi-agent harness role-based | [crewai/](crewai/) · https://docs.crewai.com |

#### 🗄️ Vector DBs

| Vector DB | Vai trò | Liên kết |
|-----------|---------|----------|
| **Chroma / Pinecone / Qdrant / Weaviate** | Lưu trữ + truy xuất memory ngữ nghĩa cho RAG | [vector-db/](vector-db/) |

#### 🔌 MCP Ecosystem

| Thành phần | Vai trò | Liên kết |
|-----------|---------|----------|
| **MCP Protocol** | Chuẩn kết nối AI ↔ tools/data | [mcp-ecosystem/](mcp-ecosystem/) · https://modelcontextprotocol.io |
| **GitHub MCP Server** | GitHub integration (cấu hình sẵn trong repo) | [MCP_SETUP.md](../../../MCP_SETUP.md) |

#### 🛡️ Security & 📊 Quality

| Tầng | Công cụ | Vai trò | Liên kết |
|------|---------|---------|----------|
| 🛡️ Security | **Guardrails** (AI, NeMo, LlamaGuard) | An toàn tool calls | [guardrails/](guardrails/) |
| 📊 Quality | **Observability** (LangSmith, Helicone, OpenLLMetry, W&B) | Giám sát cost + latency | [observability/](observability/) |
| 📊 Quality | **Evaluation** (PromptFoo, Deepeval, Ragas) | Đo chất lượng response | [evaluation/](evaluation/) |

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../HARNESS_ENGINEERING.md) — 7 components của harness
- [harness/01-retrieve-memory-knowledge](../harness/01-retrieve-memory-knowledge/) — Retrieval (vector-db)
- [harness/02-build-context](../harness/02-build-context/) — Context Management (nơi RTK đóng vai trò)
- [harness/06-decide-tools-mcp](../harness/06-decide-tools-mcp/) — Tool design & permissions (guardrails, MCP)
- [harness/09-multi-agent](../harness/09-multi-agent/) — Multi-agent (autogen, crewai)
- [harness/11-evaluation](../harness/11-evaluation/) — Đo lường hiệu quả (evaluation, observability)
- [loop/](../loop/) — Vòng lặp tự duy trì (loop-cli)
- [MCP_SETUP.md](../../../MCP_SETUP.md) — MCP ecosystem (harness/06, repo root)

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools*