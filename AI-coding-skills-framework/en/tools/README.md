# 🧰 Tools — Execution Tooling That Supports Harness & Loop

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Tools Matter?](#why-tools-matter)
> - [Overview (The Tools Group)](#overview-the-tools-group)
> - [Directory Structure Across 4 Groups](#directory-structure-across-4-groups)
> - [Learning Roadmap](#learning-roadmap)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

You've designed a complete harness — tools, memory, context, guardrails — and you've written loops that triage and verify on their own. But there's a quiet problem: **every time the agent runs `ls`, `cat`, `git status`, `cargo test`... it gets hundreds of lines of output back**, which gobbles up the context window, and in that pile of noise the agent easily misses the one most important error line.

> *"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."*

**Harness Engineering** teaches you to design the environment around AI. **Tools** is where the concrete execution tooling lives — the software you install and configure — that makes that theory work in a real environment.

This directory gathers the tooling that realizes **each component of the harness**, grouped by role: **Tool** (RTK, Loop CLI), **Framework** (LangChain, AutoGen, CrewAI), **Vector DBs** (memory/RAG), and **MCP Ecosystem** (connecting tools via MCP) — plus the **Security** (guardrails) and **Quality** (observability, evaluation) layers.

### Why Tools Matter?

> **"A great theoretical harness with no execution tooling is just slides."**

#### 3 Reasons a Tools Directory Is Needed

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **The harness needs "materialization"** | The modules in `harness/` teach *how to build* (context compression, tool design...). Tools like RTK are *ready-to-use things*, not code you write yourself. |
| 2 | **Immediate token savings** | Installing RTK once can cut 40-90% of tokens for repetitive bash commands — exactly the "Cut Costs 40-60%" goal in HARNESS_ENGINEERING.md. |
| 3 | **Separate knowledge from tooling** | Keep `harness/` purely knowledge (documentation, labs), `loop/` purely loops, and `tools/` for supporting binaries/CLIs/plugins — each branch with a clear role. |

## Overview (The Tools Group)

**Tools** is the third branch of the framework, parallel to `harness/` (knowledge) and `loop/` (loops). Each tool is a subdirectory with its own tutorial, following the same convention: an `README.md` overview + learning roadmap + numbered topics.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         AI CODING SKILLS FRAMEWORK                   │
│                                                                      │
│  harness/      → Knowledge: 7 components, 12 modules (01–12)         │
│  loop/         → Loops: concepts, patterns, safety, operating        │
│  tools/        → ❯ Execution tooling (binary/CLI/plugins)            │
└──────────────────────────────────────────────────────────────────────┘
```

## Directory Structure Across 4 Groups

The tools are grouped by **architectural role** — so you know exactly which tool solves which problem in the harness:

### 🔧 Group 1 — Tool (AI environment optimization tools)

> Directly installed binaries/CLIs that help optimize how the agent interacts with the environment.

```
tools/
├── rtk/           →   Rust Token Killer — cuts 90% of bash output from context
│   ├── README.md        ←   RTK overview: what it is, relationship to harness, learning roadmap
│   ├── 01-concepts/     ←   RTK architecture: hook system, 4 compression strategies, data flow
│   ├── 02-setup/        ←   Install + integration with each AI tool (Claude, Cline, Gemini...)
│   ├── 03-patterns/     ←   Usage patterns, one file per pattern
│   ├── 04-savings/      ←   Measurement: rtk gain, discover, session — tokens saved
│   └── 05-troubleshooting/ ← Troubleshooting, failure modes & mitigations
│
└── loop-cli/      →   The loop-* CLI suite: init, doctor, audit, gate, sandbox, worktree
    └── README.md        ←   Scaffold + orchestrate loops, Harness Runtime score
```

### 🏗️ Group 2 — Framework (Building harness orchestration)

> Programming frameworks to materialize the harness into real code.

```
tools/
├── langchain/     →   LangChain/LangGraph — graph-based harness framework
│   └── README.md        ←   StateGraph modeling the 7 components, ToolNode, RAG
│
├── autogen/       →   AutoGen (Microsoft) — multi-agent, conversation-based
│   └── README.md        ←   UserProxyAgent = harness, GroupChat orchestration
│
└── crewai/        →   CrewAI — multi-agent, role-based
    └── README.md        ←   Agent/Task/Crew, Process.sequential vs hierarchical
```

### 🗄️ Group 3 — Vector DBs (Memory & Retrieval)

> Storage and retrieval of semantic memory for harness/01-03.

```
tools/
└── vector-db/     →   Chroma, Pinecone, Qdrant, Weaviate — memory/RAG
    └── README.md        ←   Embeddings, semantic search, Tier 2 Warm Memory
```

### 🔌 Group 4 — MCP Ecosystem (Connecting Tools ↔ AI)

> The protocol that standardizes how AI apps connect to external tools & data (harness/06).

```
tools/
└── mcp-ecosystem/ →   MCP Protocol — server/client, tools/resources
    └── README.md        ←   GitHub MCP server, adding MCP servers, registry adapter
```

### 🛡️ Security Layer (Safe tool calls)

> The control layer before the agent acts — preventing unwanted side effects.

```
tools/
└── guardrails/    →   Guardrails AI, NeMo, LlamaGuard
    └── README.md        ←   Validators, rails, permissions + rate limits (harness/06)
```

### 📊 Quality Layer (Measurement & monitoring)

> Blocking regressions, tracking cost/latency, ensuring the harness runs correctly & cheaply.

```
tools/
├── observability/ →   LangSmith, Helicone, OpenLLMetry, W&B
│   └── README.md        ←   Traces, cost tracking, tool latency SLOs (harness/11)
│
└── evaluation/    →   PromptFoo, Deepeval, Ragas
    └── README.md        ←   Eval suites, regression detection, RAG metrics (harness/11)
```

---

### The Complete Directory Tree Summary

```
tools/
├── README.md              ← YOU ARE HERE — overview + roadmap + references
│
│  🔧 GROUP 1 — TOOL
├── rtk/                   ← Rust Token Killer — cuts 90% of bash output
│   ├── README.md
│   ├── 01-concepts/
│   ├── 02-setup/
│   ├── 03-patterns/
│   ├── 04-savings/
│   └── 05-troubleshooting/
├── loop-cli/              ← The loop-* CLI suite (init, audit, gate, sandbox)
│   └── README.md
│
│  🏗️ GROUP 2 — FRAMEWORK
├── langchain/             ← LangChain/LangGraph — graph harness
│   └── README.md
├── autogen/               ← AutoGen — multi-agent conversation
│   └── README.md
├── crewai/                ← CrewAI — multi-agent role-based
│   └── README.md
│
│  🗄️ GROUP 3 — VECTOR DBS
├── vector-db/             ← Chroma, Pinecone, Qdrant, Weaviate
│   └── README.md
│
│  🔌 GROUP 4 — MCP ECOSYSTEM
├── mcp-ecosystem/         ← MCP Protocol — connecting tools ↔ AI
│   └── README.md
│
│  🛡️ SECURITY LAYER
├── guardrails/            ← Guardrails AI, NeMo, LlamaGuard
│   └── README.md
│
│  📊 QUALITY LAYER
├── observability/         ← LangSmith, Helicone, OpenLLMetry
│   └── README.md
└── evaluation/            ← PromptFoo, Deepeval, Ragas
    └── README.md
```

> Each directory contains one `README.md` — consistent with the convention of `harness/` and `loop/`.

## Learning Roadmap

### By Group (The Stack By Need)

| Need | Group | Tool |
|------|-------|------|
| Cut bash token costs now | 🔧 Tool | [rtk](rtk/) |
| Automate loops safely | 🔧 Tool | [loop-cli](loop-cli/) |
| Build a harness with graphs | 🏗️ Framework | [langchain](langchain/) |
| Build a multi-agent harness | 🏗️ Framework | [autogen](autogen/) · [crewai](crewai/) |
| Memory + semantic retrieval | 🗄️ Vector DBs | [vector-db](vector-db/) |
| Connect tools via MCP | 🔌 MCP Ecosystem | [mcp-ecosystem](mcp-ecosystem/) |
| Safe tool calls | 🛡️ Security | [guardrails](guardrails/) |
| Monitor cost/latency | 📊 Quality | [observability](observability/) |
| Measure response quality | 📊 Quality | [evaluation](evaluation/) |

### Recommended Roadmap (6 Stages)

```
Stage 1 — Cut costs immediately:
   rtk/ → install RTK → apply the git-speedup pattern
   ↓
Stage 2 — Materialize the harness:
   Choose a framework: langchain/ (graph) OR autogen/crewai (multi-agent)
   Add vector-db/ for memory + RAG retrieval
   ↓
Stage 3 — Connect tools:
   mcp-ecosystem/ → register MCP servers into the harness/06 registry
   ↓
Stage 4 — Make it safe:
   guardrails/ → validate tool calls, permissions, rate limits
   ↓
Stage 5 — Measure & monitor:
   observability/ → cost tracking + latency SLOs
   evaluation/ → eval suites that block regressions
   ↓
Stage 6 — Automate:
   loop-cli/ → scaffold loops, loop gate in CI, worktree isolation
```

---

## Real-World Case Studies

### 1. RTK — Eating Its Own Dogfood

The `rtk-ai/rtk` repo itself is a harness engineering case study: it supports **16 AI coding tools** through different hook/plugin mechanisms:

| AI Tool | Integration method | Level |
|---------|-------------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

### 2. A Complete Stack for a Production Harness (By Group)

```
🔧 TOOL
rtk/           → cuts 90% of bash output before it enters context (harness/02)

🗄️ VECTOR DBS
vector-db/     → memory tiers + RAG retrieval (harness/01, 02, 03)

🏗️ FRAMEWORK
langchain/     → StateGraph orchestrates the 7 components (harness/07)

🔌 MCP ECOSYSTEM
mcp-ecosystem/ → GitHub MCP + custom MCP servers into the registry (harness/06)

🛡️ SECURITY
guardrails/    → validates every tool call before execution (harness/06)

📊 QUALITY
observability/ → LangSmith tracing + Helicone cost (harness/11)
evaluation/    → PromptFoo regression-check in CI (harness/11)

🔧 TOOL (automation)
loop-cli/      → loop gate + worktree isolation for automation (harness/10)
```

### 3. Measured RTK Results

| Command | Raw output | RTK output | Reduction |
|---------|-----------|------------|-----------|
| `ls -la` (45 lines) | 45 lines | 12 lines (tree + file counts) | ~73% |
| `git push` (15 lines) | 15 lines | `ok main` (1 line) | ~93% |
| `cargo test` (200+ lines failing) | 200+ | `FAILED: 2/15 tests` + details | ~90% |
| `docker ps` | Many columns | Essential fields only | ~70%+ |
| `ruff check` | Many lines | Grouped by rule/file | ~80% |

---

## Reference Materials

### Across the 4 Groups

#### 🔧 Tool

| Tool | Role | Link |
|------|------|------|
| **RTK — Rust Token Killer** | CLI proxy that compresses bash output before it enters LLM context | [rtk/](rtk/) · https://github.com/rtk-ai/rtk · https://www.rtk-ai.app |
| **Loop CLI** | The loop-* CLI suite: init, doctor, audit, gate, sandbox, worktree | [loop-cli/](loop-cli/) · https://github.com/cobusgreyling/loop-engineering |

#### 🏗️ Framework

| Framework | Role | Link |
|-----------|------|------|
| **LangChain / LangGraph** | Framework for building a stateful-graph harness | [langchain/](langchain/) · https://langchain.com |
| **AutoGen (Microsoft)** | Conversation-based multi-agent harness | [autogen/](autogen/) · https://microsoft.github.io/autogen/ |
| **CrewAI** | Role-based multi-agent harness | [crewai/](crewai/) · https://docs.crewai.com |

#### 🗄️ Vector DBs

| Vector DB | Role | Link |
|-----------|------|------|
| **Chroma / Pinecone / Qdrant / Weaviate** | Store + retrieve semantic memory for RAG | [vector-db/](vector-db/) |

#### 🔌 MCP Ecosystem

| Component | Role | Link |
|-----------|------|------|
| **MCP Protocol** | Standard for connecting AI ↔ tools/data | [mcp-ecosystem](mcp-ecosystem/) · https://modelcontextprotocol.io |
| **GitHub MCP Server** | GitHub integration (pre-configured in the repo) | [MCP_SETUP.md](../../../MCP_SETUP.md) |

#### 🛡️ Security & 📊 Quality

| Layer | Tool | Role | Link |
|-------|------|------|------|
| 🛡️ Security | **Guardrails** (AI, NeMo, LlamaGuard) | Safe tool calls | [guardrails/](guardrails/) |
| 📊 Quality | **Observability** (LangSmith, Helicone, OpenLLMetry, W&B) | Monitor cost + latency | [observability/](observability/) |
| 📊 Quality | **Evaluation** (PromptFoo, Deepeval, Ragas) | Measure response quality | [evaluation/](evaluation/) |

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../HARNESS_ENGINEERING.md) — the 7 components of the harness
- [harness/01-retrieve-memory-knowledge](../harness/01-retrieve-memory-knowledge/) — Retrieval (vector-db)
- [harness/02-build-context](../harness/02-build-context/) — Context Management (where RTK plays its role)
- [harness/06-decide-tools-mcp](../harness/06-decide-tools-mcp/) — Tool design & permissions (guardrails, MCP)
- [harness/09-multi-agent](../harness/09-multi-agent/) — Multi-agent (autogen, crewai)
- [harness/11-evaluation](../harness/11-evaluation/) — Measuring effectiveness (evaluation, observability)
- [loop/](../loop/) — Self-maintaining loops (loop-cli)
- [MCP_SETUP.md](../../../MCP_SETUP.md) — MCP ecosystem (harness/06, repo root)

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch*
