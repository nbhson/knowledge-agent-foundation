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

This section explains why this folder exists: even a perfect harness fails if every shell command dumps hundreds of lines into the model's memory.

You have built a full harness — tools, memory, context, guardrails — and you have loops that check work on their own. But one quiet problem remains: **every time the agent runs `ls`, `cat`, `git status`, or `cargo test`... it gets back hundreds of lines**, which fill up the context window (*context window = the model's short-term memory; everything in it costs tokens and attention*), and the one error line that matters gets lost in the noise.

> *"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."*

**Harness Engineering** teaches you how to shape the environment around AI. **Tools** is where the hands-on tooling lives — the apps and helpers you install and set up — that make those ideas work in real life.

This folder gathers the tooling behind **each part of the harness**, grouped by role: **Tool** (RTK, Loop CLI), **Framework** (LangChain, AutoGen, CrewAI), **Vector DBs** (memory/RAG), and **MCP Ecosystem** (linking tools through MCP) — plus the **Security** (guardrails) and **Quality** (observability, evaluation) layers.

> **One-line summary:** This folder holds the ready-to-install tools that turn harness ideas into working software — starting with cutting bash noise.

### Why Tools Matter?

> **"A great theoretical harness with no execution tooling is just slides."**

#### 3 Reasons a Tools Directory Is Needed

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **The harness needs "materialization"** | The `harness/` guides teach *how to build* (context sizing, tool design...). Tools like RTK are *ready to use* — you install them instead of writing them. |
| 2 | **Immediate token savings** | Installing RTK once can cut 40-90% of tokens from repeated bash commands — a direct win toward the "Cut Costs 40-60%" goal in HARNESS_ENGINEERING.md. |
| 3 | **Separate knowledge from tooling** | Keep `harness/` for ideas and guides, `loop/` for loops, and `tools/` for ready-made binaries, CLIs, and plugins — each folder with a clear job. |

> **How to read this table:** each row is one reason this folder exists. For example, row 2: a *token* is the unit of text the model reads and writes (you pay per token); RTK cuts 40-90% of the tokens spent on shell output — savings from day one, not after a rewrite.

> **One-line summary:** Ideas alone don't run — this folder is the installable software that makes the harness real.

## Overview (The Tools Group)

This section shows where `tools/` sits in the framework: it is the third branch, the one you install and run.

**Tools** is the third branch of the framework, next to `harness/` (ideas) and `loop/` (loops). Each tool has its own folder with a guide, following the same style: an `README.md` overview plus a learning path with numbered topics.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         AI CODING SKILLS FRAMEWORK                   │
│                                                                      │
│  harness/      → Knowledge: 7 components, 15 modules (01–15)         │
│  loop/         → Loops: concepts, patterns, safety, operating        │
│  tools/        → ❯ Execution tooling (binary/CLI/plugins)            │
└──────────────────────────────────────────────────────────────────────┘
```

> **One-line summary:** `harness/` teaches, `loop/` orchestrates, `tools/` installs — this branch is the software you actually run.

## Directory Structure Across 4 Groups

The tools are grouped by **what job they do** — so you can quickly see which tool solves which harness problem:

### 🔧 Group 1 — Tool (AI environment optimization tools)

> Ready-to-install binaries and CLIs that help the agent work better with its environment.

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

> **How to read this tree:** `rtk/` = a tool that shortens shell output before the model sees it (a *hook* = a trigger the agent runs before/after each command). `loop-cli/` = the command suite that creates and guards loops. The numbered folders (`01-` to `05-`) are the learning path, in order.

> **One-line summary:** Group 1 is install-and-go software: RTK (cut bash noise) and loop-cli (create and guard loops).

### 🏗️ Group 2 — Framework (Building harness orchestration)

> Coding frameworks that turn harness ideas into real working code.

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

> **How to read this tree:** these three are rival frameworks — pick one. LangGraph thinks in graphs (*StateGraph = your workflow drawn as boxes and arrows*), AutoGen thinks in conversations, CrewAI thinks in named roles with a task list.

> **One-line summary:** Three alternative ways to code the same harness — graph, conversation, or roles.

### 🗄️ Group 3 — Vector DBs (Memory & Retrieval)

> Storage and lookup for long-term memory in harness/01-03.

```
tools/
└── vector-db/     →   Chroma, Pinecone, Qdrant, Weaviate — memory/RAG
    └── README.md        ←   Embeddings, semantic search, Tier 2 Warm Memory
```

> **How to read this tree:** a *vector DB* stores text as embeddings (*embedding = text turned into a list of numbers that captures meaning*) and finds it again by meaning, not exact keywords. *RAG = the model answers using documents fetched from this store.*

> **One-line summary:** Vector DBs are the agent's long-term memory — search by meaning, not keywords.

### 🔌 Group 4 — MCP Ecosystem (Connecting Tools ↔ AI)

> The shared standard that links AI apps with outside tools and data (harness/06).

```
tools/
└── mcp-ecosystem/ →   MCP Protocol — server/client, tools/resources
    └── README.md        ←   GitHub MCP server, adding MCP servers, registry adapter
```

> **How to read this tree:** *MCP (Model Context Protocol)* = a standard plug format between AI apps and external tools — like USB for agent tools. A tool server that speaks MCP plugs in without custom glue code.

> **One-line summary:** MCP is the standard socket that lets any tool plug into any agent — no custom wiring per tool.

### 🛡️ Security Layer (Safe tool calls)

> The safety check before the agent acts — so it avoids harmful side effects.

```
tools/
└── guardrails/    →   Guardrails AI, NeMo, LlamaGuard
    └── README.md        ←   Validators, rails, permissions + rate limits (harness/06)
```

> **How to read this tree:** *guardrails* = automatic checks that run before every tool call — a call that breaks a rule (wrong file, too many requests) is refused before it does damage.

> **One-line summary:** Guardrails check every tool call before it executes — the seatbelt for agent actions.

### 📊 Quality Layer (Measurement & monitoring)

> Tools that block regressions, track cost and speed, and keep the harness healthy and cheap.

```
tools/
├── observability/ →   LangSmith, Helicone, OpenLLMetry, W&B
│   └── README.md        ←   Traces, cost tracking, tool latency SLOs (harness/11)
│
└── evaluation/    →   PromptFoo, Deepeval, Ragas
    └── README.md        ←   Eval suites, regression detection, RAG metrics (harness/11)
```

> **How to read this tree:** *observability* = recording what happened in every run (traces, cost, latency) so you can diagnose it; *SLO = a service-level objective, a target like "answers in under 2 seconds"*. *evaluation* = fixed test suites that catch regressions (*regression = something that worked gets worse after a change*).

> **One-line summary:** Observability records what happened; evaluation blocks things getting worse — together they keep the harness honest.

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

> **How to read this tree:** the same ten directories as above, in one view. The emoji headers are the group names; each `←` comment is the one-line job of that folder. Only `rtk/` has all its numbered topics filled in today — the rest ship an overview README.

> Each directory contains one `README.md` — consistent with the convention of `harness/` and `loop/`.

> **One-line summary:** Ten directories, four groups plus two layers — this tree is the whole map at a glance.

## Learning Roadmap

This section tells you what to install in what order, so you get value early instead of boiling the ocean.

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

> **How to read this table:** start from your problem, in your words, in the **Need** column ("cut bash token costs now"). The **Group** column tells you the category, and **Tool** links to the exact folder. For example, if your bill is too high, go straight to `rtk/`.

> **One-line summary:** Find your tool by problem, not by name — nine needs, nine folders.

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

> **How to read this roadmap:** install in this order — each stage builds on the last. Stage 1 pays for itself the same day; automation (Stage 6) comes last because automating an unsafe, unmeasured harness just breaks things faster.

> **One-line summary:** Six stages, cheapest payoff first: compress tokens, pick a framework, connect tools, add safety, measure, then automate.

---

## Real-World Case Studies

This section shows the tools working on real repos: RTK plugged into 16 AI tools, a complete production stack, and measured numbers.

### 1. RTK — Eating Its Own Dogfood

The `rtk-ai/rtk` repo itself shows harness ideas in action (*dogfood = a project uses its own product on itself, for real*): it supports **16 AI coding tools** through different hook and plugin setups:

| AI Tool | Integration method | Level |
|---------|-------------------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

> **How to read this table:** **AI Tool** = the coding assistant. **Integration method** = how RTK attaches to it — a *PreToolUse hook* = a trigger that rewrites the command before it runs, so the agent never sees raw output. **Level** = how deep the integration goes: "Transparent rewrite" means the agent cannot tell RTK is there; "Instruction-based" means the agent is politely asked to use RTK.

> **One-line summary:** RTK plugs into 16 AI tools — transparently via hooks where possible, via instruction files elsewhere.

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

> **How to read this stack:** each block is one layer of a full production setup, with the harness module it serves in brackets — for example, `rtk/` serves context management (harness/02) by cutting 90% of shell output before the model sees it. Read it top to bottom as "what to assemble for a serious harness".

> **One-line summary:** A full production stack in eight blocks — each mapped to the harness module it serves.

### 3. Measured RTK Results

| Command | Raw output | RTK output | Reduction |
|---------|-----------|------------|-----------|
| `ls -la` (45 lines) | 45 lines | 12 lines (tree + file counts) | ~73% |
| `git push` (15 lines) | 15 lines | `ok main` (1 line) | ~93% |
| `cargo test` (200+ lines failing) | 200+ | `FAILED: 2/15 tests` + details | ~90% |
| `docker ps` | Many columns | Essential fields only | ~70%+ |
| `ruff check` | Many lines | Grouped by rule/file | ~80% |

> **How to read this table:** **Command** = a common shell command. **Raw output** = the lines the model would receive without RTK. **RTK output** = what the model receives after compression — for example, 200+ failing test lines become one summary line plus details. **Reduction** = the share of tokens removed.

> **One-line summary:** Measured on real commands, RTK removes 70–93% of shell output — the model sees the answer, not the noise.

---

## Reference Materials

This section lists every tool with its role and link, plus pointers into the other framework branches.

> **One-line summary:** Every tool with its job and link, plus pointers into harness/ and loop/.

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
| **GitHub MCP Server** | GitHub integration (pre-configured in the repo) | [MCP_SETUP.md](../../../instruction/MCP_SETUP.md) |

#### 🛡️ Security & 📊 Quality

| Layer | Tool | Role | Link |
|-------|------|------|------|
| 🛡️ Security | **Guardrails** (AI, NeMo, LlamaGuard) | Safe tool calls | [guardrails/](guardrails/) |
| 📊 Quality | **Observability** (LangSmith, Helicone, OpenLLMetry, W&B) | Monitor cost + latency | [observability](observability/) |
| 📊 Quality | **Evaluation** (PromptFoo, Deepeval, Ragas) | Measure response quality | [evaluation](evaluation/) |

> **How to read these tables:** each row = one tool with its job (**Role**) and where to get it (**Link** — a local folder plus an external URL). They repeat the directory structure above in reference form, so you can look a tool up by name.

> **One-line summary:** The same ten tools in reference form — name, job, and where to get it.

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../HARNESS_ENGINEERING.md) — the 7 components of the harness
- [harness/01-retrieve-memory-knowledge](../harness/01-retrieve-memory-knowledge/) — Retrieval (vector-db)
- [harness/02-build-context](../harness/02-build-context/) — Context Management (where RTK plays its role)
- [harness/06-decide-tools-mcp](../harness/06-decide-tools-mcp/) — Tool design & permissions (guardrails, MCP)
- [harness/09-multi-agent](../harness/09-multi-agent/) — Multi-agent (autogen, crewai)
- [harness/11-evaluation](../harness/11-evaluation/) — Measuring effectiveness (evaluation, observability)
- [loop/](../loop/) — Self-maintaining loops (loop-cli)
- [MCP_SETUP.md](../../../instruction/MCP_SETUP.md) — MCP ecosystem (harness/06, instruction/)

> **One-line summary:** Eight links connecting each tool back to the harness module it supports.

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

## ⚠️ Update 10/2026: New Frameworks in the Agent Ecosystem

This section tracks the newer frameworks and protocols that appeared after this guide was written, so you don't adopt something already being replaced.

> **One-line summary:** Four new frameworks/protocols since 2025 — and AutoGen itself is now archived.

Beyond the 3 frameworks already listed in Group 2 (LangChain, AutoGen, CrewAI), the agent ecosystem has gained new frameworks/protocols since 2025 worth tracking:

| Framework/Protocol | Publisher | Highlights | Link |
|--------------------|-----------|------------|------|
| **Microsoft Agent Framework (MAF)** | Microsoft | Unification of AutoGen + Semantic Kernel — **replaces AutoGen** (now archived) | https://github.com/microsoft/agent-framework |
| **OpenAI Agents SDK** | OpenAI | OpenAI's official agent SDK — tool calling, handoffs, guardrails, tracing | https://openai.github.io/openai-agents-python/ |
| **Google ADK (Agent Development Kit)** | Google | Framework for building agents compatible with Gemini + Vertex AI, multi-agent support | https://google.github.io/adk-docs/ |
| **A2A Protocol (Agent2Agent)** | Google → Linux Foundation | Standard protocol for agent-to-agent communication across different frameworks | https://a2a-protocol.org |

> **How to read this table:** **Framework/Protocol** = the new name. **Publisher** = who maintains it. **Highlights** = what it does, in one line — for example, MAF = Microsoft merging its two older agent libraries into one; A2A = a shared language that lets agents from different frameworks talk to each other. **Link** = the official page.

**Important note on AutoGen:** The AutoGen repo has been **archived** — Microsoft no longer maintains it. If you are using AutoGen, plan a migration to **Microsoft Agent Framework (MAF)**. See details in [tools/autogen/](autogen/).

### Version Updates for Existing Frameworks

- **LangChain 1.0** (10/2025): `create_agent` is the primary API, LangGraph integrated natively — see [tools/langchain/](langchain/)
- **CrewAI v1.x** (10/2025+): v1.0.0 released 10/2025, currently v1.15.x — see [tools/crewai/](crewai/)
- **MCP Spec 2026-07-28**: Streamable HTTP replaces SSE, elicitation, sampling, registry — see [tools/mcp-ecosystem/](mcp-ecosystem/)
- **Guardrails AI**: validators moved to standard PyPI (7/2026) — see [tools/guardrails/](guardrails/)

> **One-line summary:** AutoGen is archived (migrate to MAF); LangChain, CrewAI, MCP and Guardrails all shipped major updates in 2025–2026 — check the linked folders before building.

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch*
