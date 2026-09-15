# 🧠 Memory & Context in AI — A Learning Guide

> **This framework teaches you how to BUILD AN AI AGENT** — from memory design, context handling, planning, multi-agent coordination, to automation and evaluation. This is NOT a guide on how to use AI the ordinary way.

---

## 🎯 Audience

| Group | Purpose |
|------|----------|
| **AI Engineers** | Design and implement AI Agent systems |
| **Backend Developers** | Integrate LLM + RAG into applications |
| **DevOps / SRE** | Deploy and monitor AI pipelines |
| **Tech Leads** | Evaluate and select the right AI architecture |
| **Researchers** | Reference patterns and best practices |

## 📋 Prerequisites

| Knowledge | Level | Notes |
|-----------|--------|---------|
| Python | Basic → Intermediate | The framework's main language |
| LLM Concepts | Basic | Transformer, Token, Prompt |
| REST API | Basic | Communicating with Ollama, MCP servers |
| Git | Basic | Managing code and automation |

## 🛠️ How to Use

### Step 1: Set up the environment

<details>
<summary><b>Step 1: Set up the environment (Click to expand/collapse)</b></summary>

```bash
# Install Ollama (run LLM & Embedding locally)
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull gemma3:12b        # Main LLM
ollama pull nomic-embed-text  # Embedding model
```

</details>

### Step 2: Learn along the roadmap
Start with **Phase 1** (Core Skills) and progress to **Phase 6** (Evaluation). Each module has a detailed README.md with code examples.

### Step 3: Practice
- Clone the repo and try the code examples in each module
- Change parameters to observe results
- Combine modules to build a complete pipeline

## ⚡ Quick Reference

| You want to... | Learn module |
|-------------|------------|
| Search information from docs/database | [01 - Retrieve Memory](#part-i-retrieve-memory-&-knowledge) |
| Manage the LLM's context window | [02 - Build Context](#part-ii-build-context) |
| Store new knowledge | [03 - Update Memory Store](#part-iii-update-memory-&-knowledge-store) |
| Break down tasks and plan | [04 - Plan & Decompose](#part-iv-plan-&-decompose-task) |
| Write effective prompts | [05 - Prompt Builder](#part-v-prompt-builder) |
| Choose and call tools (MCP) | [06 - Decide Tools / MCP](#part-vi-decide-tools--mcp-calls) |
| Organize automated workflows | [07 - Workflow](#part-vii-workflow) |
| Manage task tracking | [08 - Task Management](#part-viii-task-management) |
| Coordinate multiple agents | [09 - Multi-Agent](#part-ix-multi-agent-systems) |
| Automate CI/CD, Git | [10 - Automation](#part-x-automation) |
| Evaluate effectiveness | [11 - Evaluation](#part-xi-evaluation) |

---

## Learning Structure

```
AI/
├── AI_AGENT_FRAMEWORK.md                   ← HOMEPAGE
├── HARNESS_ENGINEERING.md                  ← HARNESS ARCHITECTURE
├── GRAPH_ENGINEERING.md                    ← GRAPH ARCHITECTURE
│
├── harness/                                ← HARNESS (7 Components)
│  │
│  │  ── CORE SKILLS ──
│  ├── 01-retrieve-memory-knowledge/         ← READ
│  ├── 02-build-context/                     ← PROCESS
│  ├── 03-update-memory-store/               ← WRITE
│  ├── 04-plan-decompose-task/               ← PLAN
│  ├── 05-prompt-builder/                    ← BUILD PROMPT
│  ├── 06-decide-tools-mcp/                  ← DECIDE TOOLS
│  │
│  │  ── ADVANCED SKILLS ──
│  ├── 07-workflow/                          ← WORKFLOWS
│  ├── 08-task/                              ← TASK MANAGEMENT
│  ├── 09-multi-agent/                       ← MULTI-AGENT SYSTEMS
│  ├── 10-automation/                        ← AUTOMATION
│  └── 11-evaluation/                        ← EVALUATION
│
├── loop/                                    ← LOOP ENGINEERING
│  └── 12-loop-engineering/                  ← IMPROVEMENT LOOP
│
└── graph/                                   ← GRAPH ENGINEERING (Knowledge Substrate)
   ├── 01-foundations/                       ← GRAPH FOUNDATIONS
   ├── 02-knowledge-graph/                   ← BUILD KG
   ├── 03-graph-storage/                     ← STORAGE & QUERY
   ├── 04-graph-embeddings/                  ← EMBEDDINGS
   ├── 05-graph-rag/                         ← GRAPH RAG
   ├── 06-graph-reasoning/                   ← REASONING
   ├── 07-gnn/                               ← GRAPH NEURAL NETWORKS
   ├── 08-graph-workflow/                    ← WORKFLOW & OPERATIONS
   └── 09-evaluation/                        ← EVALUATION
```

## Learning Path

```
┌──────────────────────────────────────────────────────────────────────┐
│                    AI AGENT LEARNING PATH                             │
│                                                                      │
│  ── CORE SKILLS ────────────────────────────────────────            │
│                                                                      │
│  Phase 1: GATHER INFORMATION                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 01 Retrieve Memory   │───►│ 02 Build Context     │                │
│  │ & Knowledge          │    │                      │                │
│  └─────────────────────┘    └──────────┬───────────┘                │
│                                         │                            │
│  Phase 2: PROCESS & ANSWER              │                            │
│                                         ▼                            │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 05 Prompt Builder    │◄───│ 06 Decide Tools /    │                │
│  └─────────────────────┘    └──────────────────────┘                │
│                                                                      │
│  Phase 3: STORE & MANAGE                                            │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 03 Update Memory     │───►│ 04 Plan & Decompose  │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  ── ADVANCED SKILLS ───────────────────────────────────            │
│                                                                      │
│  Phase 4: ORGANIZE & OPERATE                                        │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 07 Workflow          │───►│ 08 Task Management   │                │
│  │ ─ Pipeline Design    │    │ ─ Classification     │                │
│  │ ─ State Machine      │    │ ─ Decomposition      │                │
│  │ ─ Error Recovery     │    │ ─ Priority/Schedule  │                │
│  │ ─ Observability      │    │ ─ Dependency Graph   │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  Phase 5: COORDINATE & AUTOMATE                                      │
│  ┌─────────────────────┐    ┌─────────────────────┐                 │
│  │ 09 Multi-Agent       │───►│ 10 Automation        │                │
│  │ ─ Agent Roles        │    │ ─ CI/CD Pipelines    │                │
│  │ ─ Communication      │    │ ─ Code Generation    │                │
│  │ ─ Orchestration      │    │ ─ Git Automation     │                │
│  │ ─ Shared Memory      │    │ ─ Monitoring/Alerts  │                │
│  └─────────────────────┘    └─────────────────────┘                │
│                                                                      │
│  Phase 6: EVALUATE & IMPROVE                                        │
│  ┌──────────────────────────────────────────────────────┐          │
│  │ 11 Evaluation                                            │          │
│  │ ─ Quality Metrics  ─ Benchmarks  ─ Continuous Improve  │          │
│  └──────────────────────────────────────────────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Hands-on Environment

| Component | Model / Tool | Runs |
|-----------|-------------|------|
| LLM | `gemma3:12b` | Local via Ollama |
| Embedding | `nomic-embed-text` (768D) | Local via Ollama |
| Vector Store | FAISS / ChromaDB | Local |
| Graph Store | Neo4j / Kuzu / NetworkX | Local (Docker or embedded) |
| GNN | PyG / DGL | Local (Python) |
| BM25 | Custom Python | Local |
| MCP Server | GitHub MCP, Custom tools | Local |

## Details for Each Part

### Part I: Retrieve Memory & Knowledge
> How do you find the right information?

| # | Topic | Description |
|---|-------|-------|
| 1.1 | [Vector Search](harness/01-retrieve-memory-knowledge/README.md#1-vector-search) | Semantic similarity with embeddings |
| 1.2 | [BM25 Search](harness/01-retrieve-memory-knowledge/README.md#2-bm25-search) | Keyword matching, term frequency |
| 1.3 | [Hybrid Search](harness/01-retrieve-memory-knowledge/README.md#3-hybrid-search) | Combine Vector + BM25 |
| 1.4 | [Knowledge Graph](harness/01-retrieve-memory-knowledge/README.md#4-knowledge-graph) | Entity relationships, graph traversal |
| 1.5 | [Multi-Source Retrieval](harness/01-retrieve-memory-knowledge/README.md#5-multi-source-retrieval) | Fusing results from many sources |

### Part II: Build Context
> How do you organize information effectively?

| # | Topic | Description |
|---|-------|-------|
| 2.1 | [Context Window Management](harness/02-build-context/README.md#1-context-window-management) | Token limits, sliding window |
| 2.2 | [Context Compression](harness/02-build-context/README.md#2-context-compression) | Summarize, extract key info |
| 2.3 | [Prompt Templates](harness/02-build-context/README.md#3-prompt-templates) | System/user/assistant roles |
| 2.4 | [Hierarchical Context](harness/02-build-context/README.md#4-hierarchical-context) | Summary → Detail structure |
| 2.5 | [Multi-turn Context](harness/02-build-context/README.md#5-multi-turn-context) | Conversation memory management |

### Part III: Update Memory & Knowledge Store
> How do you store new information?

| # | Topic | Description |
|---|-------|-------|
| 3.1 | [Write-back Memory](harness/03-update-memory-store/README.md#1-write-back-memory) | Write new events into memory |
| 3.2 | [Memory Consolidation](harness/03-update-memory-store/README.md#2-memory-consolidation) | Merge, dedupe facts |
| 3.3 | [Report Generation](harness/03-update-memory-store/README.md#3-report-generation) | Create structured output |
| 3.4 | [KB Maintenance](harness/03-update-memory-store/README.md#4-kb-maintenance) | CRUD the knowledge base |
| 3.5 | [Event Sourcing](harness/03-update-memory-store/README.md#5-event-sourcing-pattern) | Full audit trail |

### Part IV: Plan & Decompose Task
> How do you break down complex tasks?

| # | Topic | Description |
|---|-------|-------|
| 4.1 | [Task Decomposition](harness/04-plan-decompose-task/README.md#1-task-decomposition-patterns) | Sequential, parallel, hierarchical |
| 4.2 | [Planning Algorithms](harness/04-plan-decompose-task/README.md#2-planning-algorithms) | Plan-and-Solve, ToT |
| 4.3 | [Agent Workflows](harness/04-plan-decompose-task/README.md#3-agent-workflows) | ReAct, Multi-agent, State Machine |
| 4.4 | [State Management](harness/04-plan-decompose-task/README.md#4-state-management) | Checkpoint, rollback |
| 4.5 | [ReAct Pattern](harness/04-plan-decompose-task/README.md#5-react-pattern) | Thought → Action → Observation |

### Part V: Prompt Builder
> How do you write the best prompts?

| # | Topic | Description |
|---|-------|-------|
| 5.1 | [Prompt Templates](harness/05-prompt-builder/README.md#1-prompt-templates) | Reusable templates with variables |
| 5.2 | [Few-shot Examples](harness/05-prompt-builder/README.md#2-few-shot-examples) | Dynamic example selection |
| 5.3 | [Chain-of-Thought](harness/05-prompt-builder/README.md#3-chain-of-thought-cot) | CoT variants |
| 5.4 | [Guardrails](harness/05-prompt-builder/README.md#4-guardrails) | Safety filters, validation |
| 5.5 | [Output Format](harness/05-prompt-builder/README.md#5-output-format-control) | JSON, Markdown, Table |

### Part VI: Decide Tools / MCP Calls
> Which tool to use when?

| # | Topic | Description |
|---|-------|-------|
| 6.1 | [Tool Selection](harness/06-decide-tools-mcp/README.md#1-tool-selection-patterns) | Registry, search, categories |
| 6.2 | [Intent Classification](harness/06-decide-tools-mcp/README.md#2-intent-classification) | Rule-based & LLM-based |
| 6.3 | [MCP Protocol](harness/06-decide-tools-mcp/README.md#3-mcp-model-context-protocol) | Model Context Protocol |
| 6.4 | [Tool Executor](harness/06-decide-tools-mcp/README.md#4-tool-executor-with-error-handling) | Error handling & retry |

---

### Part VII: Workflow
> How do you organize execution processes?

| # | Topic | Description |
|---|-------|-------|
| 7.1 | [Workflow Patterns](harness/07-workflow/README.md#1-workflow-patterns) | Sequential, parallel, conditional |
| 7.2 | [Pipeline Design](harness/07-workflow/README.md#2-pipeline-design) | Transform, filter, sink |
| 7.3 | [State Machine](harness/07-workflow/README.md#3-state-machine) | FSM for agents |
| 7.4 | [Error Recovery](harness/07-workflow/README.md#4-error-recovery) | Retry, circuit breaker |
| 7.5 | [Observability](harness/07-workflow/README.md#5-observability) | Logging, metrics |

### Part VIII: Task Management
> How do you manage and track tasks?

| # | Topic | Description |
|---|-------|-------|
| 8.1 | [Task Classification](harness/08-task/README.md#1-task-classification) | Classify by category & complexity |
| 8.2 | [Task Decomposition](harness/08-task/README.md#2-task-decomposition) | Feature, layer, file, TDD |
| 8.3 | [Priority & Scheduling](harness/08-task/README.md#3-priority--scheduling) | Eisenhower matrix, token budget |
| 8.4 | [Task State Management](harness/08-task/README.md#4-task-state-management) | Lifecycle, valid transitions |
| 8.5 | [Dependency Management](harness/08-task/README.md#5-dependency-management) | DAG, topological sort |

### Part IX: Multi-Agent Systems
> How do you coordinate multiple agents?

| # | Topic | Description |
|---|-------|-------|
| 9.1 | [Agent Roles](harness/09-multi-agent/README.md#1-agent-roles) | Planner, Coder, Reviewer, Tester |
| 9.2 | [Communication Patterns](harness/09-multi-agent/README.md#2-communication-patterns) | Hierarchical, P2P, pipeline |
| 9.3 | [Orchestration](harness/09-multi-agent/README.md#3-orchestration-strategies) | Sequential, parallel, debate, voting |
| 9.4 | [Shared Memory](harness/09-multi-agent/README.md#4-shared-memory) | Versioned, tagged, locked |
| 9.5 | [Conflict Resolution](harness/09-multi-agent/README.md#5-conflict-resolution) | File lock, voting, deadlock detection |

### Part X: Automation
> How do you automate repetitive tasks?

| # | Topic | Description |
|---|-------|-------|
| 10.1 | [Automation Patterns](harness/10-automation/README.md#1-automation-patterns) | Event, scheduled, reactive, self-healing |
| 10.2 | [CI/CD Pipelines](harness/10-automation/README.md#2-cicd-pipelines) | GitHub Actions, deploy pipeline |
| 10.3 | [Code Generation](harness/10-automation/README.md#3-code-generation-automation) | Scaffolding, templates |
| 10.4 | [Scheduled Tasks](harness/10-automation/README.md#4-scheduled-tasks) | Cron, interval, daily |
| 10.5 | [Git Automation](harness/10-automation/README.md#5-git-automation) | Hooks, commit conventions |
| 10.6 | [Monitoring & Alerts](harness/10-automation/README.md#6-monitoring--alerts) | Thresholds, dashboards |

### Part XI: Evaluation
> How do you evaluate AI coding effectiveness?

| # | Topic | Description |
|---|-------|-------|
| 11.1 | [Evaluation Dimensions](harness/11-evaluation/README.md#1-evaluation-dimensions) | Correctness, quality, safety, speed |
| 11.2 | [Quality Metrics](harness/11-evaluation/README.md#2-quality-metrics) | Complexity, maintainability |
| 11.3 | [Performance Benchmarks](harness/11-evaluation/README.md#3-performance-benchmarks) | Benchmark suite, compare |
| 11.4 | [Evaluation Framework](harness/11-evaluation/README.md#4-evaluation-framework) | Auto-eval pipeline |
| 11.5 | [Continuous Improvement](harness/11-evaluation/README.md#5-continuous-improvement) | Trend analysis, suggestions |
| 11.6 | [Reporting & Dashboards](harness/11-evaluation/README.md#6-reporting--dashboards) | Markdown/JSON reports |

### Part XII: Loop Engineering
> How do you design self-sustaining loops for AI agents?

| # | Topic | Description |
|---|-------|-------|
| 12.1 | [Concepts](loop/01-concepts/README.md) | 5 building blocks + memory, anatomy, L1-L3, taxonomy |
| 12.2 | [Patterns](loop/02-patterns/README.md) | 7 production patterns (daily-triage, pr-babysitter, ci-sweeper...) |
| 12.3 | [Safety](loop/03-safety/README.md) | Loop Design Checklist, denylist, human gates |
| 12.4 | [Operating](loop/04-operating/README.md) | Budget, logging, metrics, pause/kill |
| 12.5 | [Multi-Loop](loop/05-multi-loop/README.md) | Coordinate when running multiple loops |
| 12.6 | [Anti-Patterns](loop/06-anti-patterns/README.md) | 10 anti-patterns + failure mode catalog |
| 12.7 | [Tools](loop/07-tools/README.md) | loop-init, loop-audit, loop-cost, ecosystem |

### Part XIII: Graph Engineering
> How do you build graph-based knowledge systems for AI agents?

| # | Topic | Description |
|---|-------|-------|
| 13.1 | [Foundations](graph/01-foundations/README.md) | Graph theory, types, representations, metrics |
| 13.2 | [Knowledge Graph](graph/02-knowledge-graph/README.md) | Entity/relation extraction, ontology, deduplication |
| 13.3 | [Graph Storage](graph/03-graph-storage/README.md) | Neo4j, Cypher, indexing, transactions |
| 13.4 | [Graph Embeddings](graph/04-graph-embeddings/README.md) | Node2Vec, GraphSAGE, hybrid vector+graph search |
| 13.5 | [GraphRAG](graph/05-graph-rag/README.md) | Subgraph retrieval, community summaries, Microsoft pattern |
| 13.6 | [Graph Reasoning](graph/06-graph-reasoning/README.md) | Traversal, path finding, inference rules, temporal reasoning |
| 13.7 | [GNN](graph/07-gnn/README.md) | GNN, link prediction, KG completion, R-GCN |
| 13.8 | [Graph Workflow](graph/08-graph-workflow/README.md) | Pipeline ETL, incremental updates, versioning, orchestration |
| 13.9 | [Evaluation](graph/09-evaluation/README.md) | Coverage, hallucination, path precision, benchmarks |

---

## 🧠 Understanding This Framework

> **This framework is the "orchestration brain" — the AI model is the "reasoning brain".**

The framework teaches you **how to assemble the pieces** — the model is just one piece of the puzzle. You can use **Ollama running locally for free** or a **paid API** depending on your budget.

### Illustrative flow: What does a RAG chatbot need?

```
Your documents (PDF, docs, DB)
        ↓
   [Module 01] Retrieve — find relevant passages
        ↓
   [Module 02] Build Context — arrange the information
        ↓
   [Module 05] Prompt Builder — craft the prompt
        ↓
        ↓
   ══════════════════════════════
   ║   AI MODEL (Ollama/GPT)   ║  ← THE MODEL-NEEDED PART
   ║   Read context + answer   ║
   ══════════════════════════════
        ↓
      The answer
```

### Illustrative flow: What does GraphRAG need?

```
Your documents (PDF, docs, DB)
        ↓
   [Graph 02] Knowledge Graph — extract entities/relations (LLM)
        ↓
   [Graph 03] Graph Storage — store in Neo4j/Kuzu (Cypher)
        ↓
   [Graph 05] GraphRAG — subgraph retrieval + community summaries
        ↓
   [Harness 02] Build Context — merge graph context + vector context
        ↓
   ══════════════════════════════
   ║   AI MODEL (Ollama/GPT)   ║  ← THE MODEL-NEEDED PART
   ║   Read graph context + answer with a citation path ║
   ══════════════════════════════
        ↓
      Answer + proof path
```

### Clear distinction: Which parts need a model?

| Part | Needs a model? | Description |
|------|-----------|-------|
| **Vector Search** (Module 01) | ✅ Needs an **embedding model** | Turns text into vectors for comparison |
| **BM25 Search** (Module 01) | ❌ Not needed | Pure math, counts keywords |
| **Generate Answer** (Module 05) | ✅ Needs an **LLM** | gemma3:12b, GPT-4o, Claude... |
| **Prompt Building** (Module 05) | ❌ Not needed | Just text arrangement |
| **Workflow** (Module 07) | ❌ Not needed | Just orchestration logic |
| **CI/CD Automation** (Module 10) | ❌ Not needed | GitHub Actions, scripts |

### The 2 model types you need

| Type | Role | Local (free) | API (paid) |
|------|---------|-------------------|---------------|
| **Embedding model** | Turns text into vectors (used for search) | `nomic-embed-text` via Ollama | OpenAI text-embedding-3-small |
| **LLM** (Large Language Model) | Generates answers | `gemma3:12b`, `llama3`, `qwen2.5` via Ollama | GPT-4o, Claude, Gemini |

### In short

- **~60% of the framework** = pure code, no model needed (search, workflow, orchestration)
- **~40% of the framework** = needs a model (embedding + generation)

The framework teaches you **how to assemble the pieces** — the model is just one piece of the puzzle. You can use **Ollama running locally for free** or a **paid API** depending on your budget.

---

## 🚀 After You Finish — Real Projects

With **11 modules** covering everything from Retrieval, Context, Memory, Planning, Prompting, Tooling, Workflow, Task Management, Multi-Agent, and Automation to Evaluation — you can build **dozens of real projects**. Below are **20 projects** organized by level and domain.

---

### 🟢 Beginner Level — Start Right Away (Modules 01-05)

#### 1. 📚 Personal Knowledge Base (PKB)

- **Description**: A system to store and search personal knowledge from notes, bookmarks, and code snippets
- **Tech Stack**: ChromaDB + nomic-embed-text + Python CLI
- **⏱️ Build time**: 2-3 days (basic CLI), 1 week (with a Web UI)
- **Modules applied**:
  - Module 01 — Vector Search + Hybrid Search (BM25 + Semantic)
  - Module 03 — Write-back Memory, KB Maintenance (CRUD)
  - Module 06 — Tool Selection (CLI tool, search tool)
- **Features**: Import markdown/notes → Chunk → Embed → Semantic search CLI
- **Result**: `pkb search "how to deploy Docker"` → finds the right hit among 1000+ notes

#### 2. 📄 Document Q&A Chatbot

- **Description**: A chatbot that answers questions from your own documents (PDF, docs, wiki)
- **Tech Stack**: Ollama (gemma3:12b + nomic-embed-text) + FAISS/ChromaDB + FastAPI
- **⏱️ Build time**: 3-5 days (basic endpoint), 1-2 weeks (chat UI + multi-format)
- **Modules applied**:
  - Module 01 — Document Processing, Chunking, Vector Search
  - Module 02 — Context Window Management, Prompt Templates
  - Module 05 — Prompt Builder, Output Format Control
- **Features**: Upload PDF → Auto-chunk → Embed → Chat with the document
- **Result**: A chatbot that answers correctly from internal documents, reducing hallucination

#### 3. 🔍 Hybrid Search Engine

- **Description**: A search engine combining semantic + keyword search with re-ranking
- **Tech Stack**: BM25 (Python) + FAISS + Cross-encoder reranker
- **⏱️ Build time**: 3-5 days (BM25 + Vector), 1 week (add reranking + optimization)
- **Modules applied**:
  - Module 01 — Vector Search, BM25, Hybrid Search, Re-ranking
  - Module 02 — Context Compression (summarizing results)
- **Features**: Query → Parallel BM25 + Vector → Merge → Rerank → Top-K
- **Result**: 40% more accurate search than using BM25 or Vector alone

#### 4. 📊 Markdown to Structured Data

- **Description**: Automatically convert Markdown documents into a structured database
- **Tech Stack**: LLM (gemma3:12b) + SQLite + Python
- **⏱️ Build time**: 1-2 days
- **Modules applied**:
  - Module 05 — Prompt Builder, Output Format Control (JSON/Table)
  - Module 03 — Report Generation, Write-back Memory
- **Features**: Input Markdown docs → LLM extracts entities/relations → Store as structured data
- **Result**: Automatically create a database from docs, supporting structured queries

#### 5. 🧪 AI Code Review Bot (Simple)

- **Description**: A bot that reviews code when you push to GitHub and suggests improvements
- **Tech Stack**: GitHub Webhooks + LLM + Python
- **⏱️ Build time**: 2-3 days
- **Modules applied**:
  - Module 05 — Prompt Builder (review prompts), Guardrails (safety)
  - Module 10 — Git Automation (hooks, webhooks)
- **Features**: PR created → Bot reviews → Comments suggestions on the PR
- **Result**: Automated code review, catch bugs early, suggest best practices

---

### 🟢 Daily-Use Level — Useful Every Day (Modules 01-10)

> **These are small projects that can be built in 1-3 days, but are used EVERY DAY at work.**

#### 6. 📋 Auto Daily Work Log

- **Description**: Automatically record daily work from git commits, Slack messages, and calendar — creates a daily report
- **Tech Stack**: LLM + Git API + Calendar API + Markdown/JSON output
- **Modules applied**:
  - Module 01 — Multi-Source Retrieval (git, calendar, Slack, Jira)
  - Module 03 — Write-back Memory (store the daily log), Report Generation
  - Module 05 — Prompt Builder (report template), Output Format (Markdown table)
  - Module 10 — Scheduled Tasks (cron at the end of each day)
- **Flow**:
  ```
  6:00 PM → Cron trigger
    → Git: List today's commits (git log --since="today")
    → Calendar: List meetings attended
    → Jira/Trello: Tasks updated
    → Slack: Summary of key messages (optional)
    → LLM: Synthesize into a daily report
    → Output: Markdown daily log + Send to Slack/Email
  ```
- **Result**: Never forget to log your work at the end of the day. Reports are automatic and professional.
- **Sample output**:
  ```markdown
  ## Daily Report — 2025-01-15
  
  ### ✅ Completed
  - [PROJ-123] Fix login bug — 3 commits, merged PR #456
  - [PROJ-124] Implement user search API — 2 commits, PR #457 pending review
  
  ### 📅 Meetings
  - Sprint Planning (10:00-10:30)
  - Code Review with Team (14:00-14:30)
  
  ### 🔄 In Progress
  - [PROJ-125] Dashboard redesign — 60% complete
  
  ### 📌 Blockers
  - Waiting for API credentials from DevOps team
  ```

#### 7. 📝 Smart Standup Bot

- **Description**: Automatically generate standup answers (What did you do? What will you do? Blockers?) from real data
- **Tech Stack**: LLM + Git + Jira API + Calendar
- **Modules applied**:
  - Module 01 — Retrieve yesterday's activities from multiple sources
  - Module 05 — Prompt Builder (standup template), Chain-of-Thought (summarization)
  - Module 10 — Scheduled Tasks (cron at 9:00 AM every day)
- **Flow**:
  ```
  09:00 AM → Bot sends a message:
    "🌅 Good morning! Here's your standup for today:"
    
    What I did yesterday:
    - Fixed auth bug (commit abc123)
    - Reviewed PR #456
    
    What I'll do today:
    - Continue dashboard redesign (from Jira backlog)
    - Pair programming with @dev2 on API migration
    
    Blockers: None
  ```
- **Result**: Standups in 30 seconds instead of 15 minutes of thinking.

#### 8. 📧 AI Email/Message Drafter

- **Description**: Create email drafts from bullet points — professional, with an appropriate tone, multilingual
- **Tech Stack**: LLM + Gmail API / Slack API
- **Modules applied**:
  - Module 05 — Prompt Builder (email templates, tone control), Few-shot Examples
  - Module 02 — Context Window (preserve email thread context)
- **Flow**:
  ```
  User: "draft email to boss: project delayed 2 weeks, need more resources, will update timeline"
    → LLM generates a professional email with:
      - Appropriate greeting/closing
      - Structured paragraphs
      - Action items highlighted
      - Diplomatic tone
  ```
- **Result**: Write professional emails from a few keywords, saving 10-15 minutes per email.

#### 9. 🔍 Codebase Q&A (Ask Your Code)

- **Description**: Q&A with your codebase — "what does function X do?", "why does this bug exist?", "where is function Y called from?"
- **Tech Stack**: LLM + AST Parser + Embedding + Code indexing
- **Modules applied**:
  - Module 01 — Vector Search (code chunks), Knowledge Graph (call graph)
  - Module 02 — Build Context (code + comments + git history)
  - Module 06 — Tool Selection (read_file, search_code, grep)
- **Flow**:
  ```
  User: "what does the handlePayment() function do and where is it called?"
    → Search: Find the handlePayment definition
    → Search: Find all callers
    → Context: Build with code + tests + comments
    → LLM: Explain the logic + list callers + potential issues
  ```
- **Result**: Understand a codebase 5x faster, especially when onboarding to a new project.

#### 10. 📊 PR Summary & Changelog Generator

- **Description**: Summarize PRs into changelog entries, automated release notes
- **Tech Stack**: LLM + Git diff + GitHub API
- **Modules applied**:
  - Module 01 — Retrieve PR context, linked issues
  - Module 05 — Prompt Builder (changelog template), Output Format
  - Module 10 — Git Automation (auto-generate on merge)
- **Flow**:
  ```
  PR merged → Webhook trigger
    → LLM analyzes the diff + PR description + linked issues
    → Generates a changelog entry:
    
    ### Added
    - User search API with fuzzy matching (#457)
    
    ### Fixed  
    - Login timeout on slow networks (#456)
    
    ### Changed
    - Upgraded auth library to v2.1
  ```
- **Result**: Automatic release notes, nobody has to type changelogs by hand.

#### 11. 🗓️ Meeting Notes → Action Items

- **Description**: Automatically extract action items from meeting notes/recordings
- **Tech Stack**: LLM + Speech-to-Text (optional) + Task Manager API
- **Modules applied**:
  - Module 02 — Context Compression (summarize the meeting)
  - Module 05 — Prompt Builder (action item extraction), Output Format (JSON)
  - Module 08 — Task Classification, Priority
- **Flow**:
  ```
  Meeting notes / transcript input
    → LLM extracts:
      - Action items with assignees
      - Decisions made
      - Follow-up topics
      - Deadlines
    → Auto-create tasks in Jira/Trello/Notion
  ```
- **Result**: No missed action items, every meeting has clear outcomes.

#### 12. 💡 Git Commit Message AI

- **Description**: Automatically create standard commit messages from the git diff
- **Tech Stack**: LLM + Git hooks (commit-msg)
- **Modules applied**:
  - Module 05 — Prompt Builder (Conventional Commits template)
  - Module 10 — Git Automation (pre-commit hooks)
- **Flow**:
  ```
  git commit → pre-commit hook
    → Analyze staged changes (git diff --cached)
    → LLM generates:
      feat(auth): add OAuth2 login with Google
    
      - Add Google OAuth2 provider
      - Store refresh token in session
      - Handle token refresh on expiry
    
      Closes #123
  ```
- **Result**: Standard, consistent commit messages with linked issues.

#### 13. 📖 Code Review Checklist Generator

- **Description**: Automatically generate review checklists tailored to the type of change (API change, DB migration, UI...)
- **Tech Stack**: LLM + Git diff analysis
- **Modules applied**:
  - Module 01 — Retrieve past review patterns, team conventions
  - Module 04 — Task Decomposition (break the review into checklist items)
  - Module 05 — Prompt Builder (checklist templates)
- **Flow**:
  ```
  PR opened → Analyze changed files
    → Detect: "This PR modifies the database schema"
    → Generate a targeted checklist:
      ☐ Is the migration reversible?
      ☐ Is it backward compatible?
      ☐ Are indexes added for the new queries?
      ☐ Is the seed data updated?
      ☐ Is the documentation updated?
  ```
- **Result**: More thorough code reviews, no missed edge cases.

---

### 📊 Daily-Use Projects Summary

| # | Project | Usage frequency | Build time | Time saved |
|---|-------|---------------|-----------------|------------|
| 6 | Auto Daily Work Log | **Every day** | 2-3 days | 15-20 min/day |
| 7 | Smart Standup Bot | **Every day** | 1-2 days | 10-15 min/day |
| 8 | AI Email Drafter | **3-5 times/day** | 1 day | 10-15 min/each |
| 9 | Codebase Q&A | **5-10 times/day** | 2-3 days | 5-10 min/each |
| 10 | PR Changelog Generator | **Every PR merge** | 1 day | 10-15 min/PR |
| 11 | Meeting Notes → Actions | **After each meeting** | 1-2 days | 15-20 min/meeting |
| 12 | Git Commit Message AI | **Every commit** | 0.5 day | 2-3 min/commit |
| 13 | Code Review Checklist | **Every PR** | 1 day | 5-10 min/PR |

> **💰 Estimated total time saved: 1-2 HOURS/day** — about 20-40 hours per month!
> 
> At least 1-2 of these projects will **pay for the course** within the first week of use.

---

### 🟡 Intermediate Level — Needs More Modules (Modules 01-08)

#### 14. 🏗️ Enterprise RAG Platform

- **Description**: A production-grade RAG system with multi-source retrieval, caching, and monitoring
- **Tech Stack**: Ollama + Qdrant + FastAPI + Redis (cache) + Prometheus
- **⏱️ Build time**: 2-3 weeks (MVP), 4-6 weeks (production-ready with monitoring)
- **Modules applied**:
  - Module 01 — Hybrid Search, Multi-Source Retrieval, Knowledge Graph
  - Module 02 — Hierarchical Context, Context Compression, Multi-turn
  - Module 03 — Memory Consolidation, Event Sourcing
  - Module 05 — Prompt Templates, Few-shot Examples, Guardrails
  - Module 07 — Pipeline Design, Error Recovery, Observability
- **Features**: Multi-source ingestion → Hybrid search → Context assembly → Cached responses → Monitored pipeline
- **Result**: A production RAG system handling 10K+ documents, <200ms latency

#### 15. 💬 Customer Support AI Agent

- **Description**: A customer support agent with the ability to look up the knowledge base, ticket system, and escalation
- **Tech Stack**: LLM + Vector DB + Ticket API + WebSocket
- **⏱️ Build time**: 2-3 weeks (basic chat + KB), 4-6 weeks (multi-turn + escalation + ticketing)
- **Modules applied**:
  - Module 01 — Retrieve from KB + order history + FAQ
  - Module 02 — Multi-turn Context, Context Window Management
  - Module 04 — Plan & Decompose (analyze the problem → find a solution)
  - Module 05 — Prompt Builder (customer-facing prompts), Guardrails
  - Module 07 — Workflow (qualification → resolution → follow-up)
- **Features**: Chat → Classify intent → Retrieve relevant docs → Resolve or Escalate
- **Result**: Resolve 80% of tickets automatically, with smart escalation

#### 16. 📝 Smart Documentation Generator

- **Description**: Automatically generate documentation for a codebase from source code + comments
- **Tech Stack**: LLM + AST Parser + Git + Markdown
- **⏱️ Build time**: 1-2 weeks (single language), 3-4 weeks (multi-language + auto-commit)
- **Modules applied**:
  - Module 01 — Retrieve code context, existing docs
  - Module 02 — Build Context (code + comments + usage examples)
  - Module 05 — Prompt Builder (doc generation templates), Output Format
  - Module 10 — Git Automation (auto-commit docs), Code Generation
- **Features**: Scan codebase → Extract API signatures → Generate docs → Auto-commit
- **Result**: Documentation that stays up to date, cutting doc-writing time by 90%

#### 17. 🗓️ AI Task Manager

- **Description**: An intelligent task management system — classification, prioritization, decomposition, scheduling
- **Tech Stack**: LLM + SQLite + CLI/Web UI + Calendar API
- **⏱️ Build time**: 1-2 weeks (CLI), 3-4 weeks (Web UI + calendar integration)
- **Modules applied**:
  - Module 04 — Task Decomposition, Planning Algorithms (Plan-and-Solve)
  - Module 05 — Prompt Builder (classification prompts)
  - Module 08 — Task Classification, Priority & Scheduling, Dependency Management
- **Features**: Input task description → Auto-classify → Decompose → Prioritize → Schedule → Track
- **Result**: Complex tasks are automatically broken down and scheduled intelligently

#### 18. 🔄 Memory-Augmented Chatbot

- **Description**: A chatbot with long-term memory — remembers preferences, conversation history, and facts about the user
- **Tech Stack**: LLM + Vector DB + SQLite (fact store) + Session management
- **⏱️ Build time**: 2-3 weeks (basic memory), 4-6 weeks (consolidation + multi-session)
- **Modules applied**:
  - Module 02 — Multi-turn Context, Hierarchical Context
  - Module 03 — Write-back Memory, Memory Consolidation (merge/dedupe facts)
  - Module 05 — Prompt Builder (system prompt with remembered context)
- **Features**: Chat → Extract facts → Store → Recall in future conversations
- **Result**: The bot remembers user preferences and personalizes responses over time

---

### 🔴 Advanced Level — Complex Systems (Modules 04-11)

#### 19. 🤖 AI Coding Agent (Build It Yourself)

- **Description**: Build your own agent similar to Cline/Cursor — reads code, plans tasks, writes code, reviews, tests, commits
- **Tech Stack**: LLM + MCP Servers + Git + File System + Terminal
- **⏱️ Build time**: 4-6 weeks (MVP: read + write code), 2-3 months (full pipeline: review + test + commit)
- **Modules applied**:
  - Module 04 — ReAct Pattern (Thought → Action → Observation loop), Agent Workflows
  - Module 06 — Tool Selection, MCP Protocol, Tool Executor with Error Handling
  - Module 07 — State Machine (idle → planning → coding → reviewing → testing)
  - Module 08 — Task Decomposition, Dependency Management
- **Features**: User request → Plan → Read files → Write code → Run tests → Fix errors → Commit
- **Result**: An agent that completes coding tasks from a description automatically

#### 20. 🏢 Multi-Agent Development Team

- **Description**: A system of cooperating agents: Planner → Architect → Coder → Reviewer → Tester → Deployer
- **Tech Stack**: LLM + MCP + Message Queue (Redis/RabbitMQ) + Shared Memory
- **⏱️ Build time**: 2-3 months (2 basic agents), 4-6 months (full 6-agent pipeline)
- **Modules applied**:
  - Module 08 — Task Classification, Decomposition, Priority & Scheduling, Dependency DAG
  - Module 09 — Agent Roles, Communication Patterns, Orchestration, Shared Memory, Conflict Resolution
  - Module 07 — Workflow Patterns, Pipeline Design, Error Recovery
- **Features**: Feature request → Planner decomposes → Architect designs → Coder implements → Reviewer reviews → Tester tests → Deployer deploys
- **Result**: A fully automated development pipeline, each agent being a specialist

#### 21. 🔄 Self-Healing CI/CD Pipeline

- **Description**: A CI/CD pipeline that auto-builds, tests, reviews, and deploys — and automatically fixes errors when it fails
- **Tech Stack**: GitHub Actions + LLM + Docker + Kubernetes + Prometheus + Grafana
- **⏱️ Build time**: 2-3 weeks (basic auto-fix), 4-6 weeks (full self-healing + monitoring)
- **Modules applied**:
  - Module 07 — Error Recovery (retry, circuit breaker), Observability (logging, metrics)
  - Module 10 — CI/CD Pipelines, Git Automation, Monitoring & Alerts, Code Generation
  - Module 11 — Performance Benchmarks, Continuous Improvement
- **Features**: Push → Build → Test → AI Review → Auto-fix failures → Deploy → Monitor → Rollback if needed
- **Result**: The pipeline self-repairs 90% of failures, reducing downtime

#### 22. 📈 AI-Powered Analytics Dashboard

- **Description**: A dashboard that automatically analyzes data, generates insights, and alerts on anomalies
- **Tech Stack**: LLM + Pandas/SQL + Chart Library + Scheduler
- **⏱️ Build time**: 2-3 weeks (single data source), 4-6 weeks (multi-source + anomaly detection)
- **Modules applied**:
  - Module 01 — Multi-Source Retrieval (data from multiple DBs/APIs)
  - Module 03 — Report Generation, Event Sourcing
  - Module 05 — Prompt Builder (analysis prompts), Output Format (charts, tables)
  - Module 10 — Scheduled Tasks, Monitoring & Alerts
  - Module 11 — Quality Metrics, Reporting & Dashboards
- **Features**: Scheduled analysis → Query data → AI generates insights → Dashboard update → Alert on anomalies
- **Result**: Automated business intelligence, proactive anomaly detection

#### 23. 🏥 Domain-Specific Research Assistant (Medical/Legal/Finance)

- **Description**: A domain-specific research assistant — answers questions from papers, regulations, and financial reports
- **Tech Stack**: LLM + Vector DB + Knowledge Graph + Citation tracking
- **⏱️ Build time**: 3-4 weeks (basic Q&A), 6-8 weeks (CoT reasoning + citation tracking)
- **Modules applied**:
  - Module 01 — Knowledge Graph (entity relationships), Multi-Source Retrieval
  - Module 02 — Hierarchical Context (summary → detail), Context Compression
  - Module 04 — Planning Algorithms (research decomposition)
  - Module 05 — Guardrails (safety filters), Chain-of-Thought (reasoning)
  - Module 11 — Evaluation Dimensions (correctness, safety, faithfulness)
- **Features**: Research question → Decompose into sub-questions → Retrieve from papers/docs → Reason with CoT → Answer with citations
- **Result**: Expert-level research assistance with verifiable sources

---

### 🟣 Expert Level — Integrated Systems (All Modules)

#### 24. 🌐 Autonomous AI Development Platform

- **Description**: A platform that lets users describe a feature in natural language and the AI develops it automatically
- **Tech Stack**: Full stack — LLM + MCP + Docker + CI/CD + Monitoring
- **⏱️ Build time**: 3-6 months (MVP), 6-12 months (production-grade)
- **Modules applied**: **ALL modules 01-11**
  - 01-03: Knowledge retrieval & memory management
  - 04-05: Planning & prompt engineering
  - 06-07: Tool selection & workflow orchestration
  - 08-09: Task management & multi-agent coordination
  - 10-11: Automation & continuous evaluation
- **Features**: "Build a blog app with auth, posts, comments" → Auto-plan → Auto-code → Auto-test → Auto-deploy
- **Result**: A low-code/no-code platform with an AI agent backbone

#### 25. 🧠 Adaptive Learning System

- **Description**: An adaptive learning system — tracks knowledge gaps, suggests content, and uses spaced repetition
- **Tech Stack**: LLM + Vector DB + Scheduler + Analytics
- **⏱️ Build time**: 2-3 months (basic tracking), 4-6 months (full adaptive + spaced repetition)
- **Modules applied**:
  - Module 01 — Retrieve learning materials, knowledge graph
  - Module 02 — Build personalized context for each learner
  - Module 03 — Write-back Memory (track what the user learned/forgot)
  - Module 04 — Plan learning paths (adaptive difficulty)
  - Module 08 — Task Management (learning tasks, scheduling)
  - Module 11 — Evaluation (track progress, identify gaps)
- **Features**: User learns → Track mastery → Identify gaps → Suggest next topics → Spaced repetition schedule
- **Result**: A personalized learning path, optimized for retention

#### 26. 🔐 AI Security Audit System

- **Description**: An automated security audit system — scans code, detects vulnerabilities, and suggests fixes
- **Tech Stack**: LLM + SAST tools + Knowledge Graph + CI/CD
- **⏱️ Build time**: 3-4 weeks (single scanner), 2-3 months (multi-agent + auto-fix + compliance)
- **Modules applied**:
  - Module 01 — Retrieve the CVE database, security knowledge
  - Module 05 — Guardrails (safety, prompt injection prevention)
  - Module 07 — Workflow (scan → analyze → report → fix → verify)
  - Module 09 — Multi-agent (Scanner agent + Analyzer agent + Fixer agent)
  - Module 10 — CI/CD integration, Git Automation
  - Module 11 — Evaluation (security metrics, compliance)
- **Features**: Code push → Security scan → AI analysis → Fix suggestions → Auto-PR fixes
- **Result**: An automated security pipeline, with compliance reporting

#### 27. 📱 Cross-Platform App Generator

- **Description**: Create multi-platform apps from a spec — Web + Mobile + API from a single specification
- **Tech Stack**: LLM + Code generation templates + MCP + Multi-repo management
- **⏱️ Build time**: 2-3 months (single platform), 4-6 months (multi-platform parallel generation)
- **Modules applied**:
  - Module 04 — Plan & Decompose (feature → frontend + backend + API)
  - Module 06 — Tool Selection (choose frameworks, libraries)
  - Module 07 — Workflow (parallel generation for each platform)
  - Module 09 — Multi-agent (Frontend agent + Backend agent + API agent)
  - Module 10 — Code Generation Automation, Git Automation
- **Features**: App spec → Architect designs the API → Parallel code gen → Cross-platform build → Unified test
- **Result**: Create MVPs for 3 platforms from 1 spec in a few hours

#### 28. 🏗️ Infrastructure-as-Code AI Assistant

- **Description**: An AI assistant for DevOps — automatically generates Terraform/Docker/K8s configs from requirements
- **Tech Stack**: LLM + MCP (Docker, K8s, Cloud APIs) + Git + Terraform
- **⏱️ Build time**: 2-3 months (single cloud), 4-6 months (multi-cloud + validation + apply)
- **Modules applied**:
  - Module 01 — Retrieve infrastructure docs, best practices
  - Module 04 — Plan the infrastructure (networking → compute → storage → monitoring)
  - Module 05 — Prompt Builder (IaC templates), Guardrails (security policies)
  - Module 06 — Tool Selection (Docker, K8s, AWS/GCP/Azure MCP tools)
  - Module 07 — Workflow (plan → generate → validate → apply → verify)
  - Module 10 — CI/CD for infrastructure, Monitoring
- **Features**: "Deploy a scalable web app" → Generates Terraform + Docker + K8s + CI/CD configs
- **Result**: Automated infrastructure provisioning, following best practices

---

### 📊 Projects & Modules Overview

| # | Project | Level | Modules applied | Complexity |
|---|-------|--------|-----------------|-------------|
| 1 | Personal Knowledge Base | 🟢 Basic | 01, 03, 06 | ⭐⭐ |
| 2 | Document Q&A Chatbot | 🟢 Basic | 01, 02, 05 | ⭐⭐ |
| 3 | Hybrid Search Engine | 🟢 Basic | 01, 02 | ⭐⭐⭐ |
| 4 | Markdown to Structured Data | 🟢 Basic | 03, 05 | ⭐⭐ |
| 5 | AI Code Review Bot | 🟢 Basic | 05, 10 | ⭐⭐ |
| 6 | Enterprise RAG Platform | 🟡 Intermediate | 01, 02, 03, 05, 07 | ⭐⭐⭐⭐ |
| 7 | Customer Support AI Agent | 🟡 Intermediate | 01, 02, 04, 05, 07 | ⭐⭐⭐⭐ |
| 8 | Smart Documentation Generator | 🟡 Intermediate | 01, 02, 05, 10 | ⭐⭐⭐ |
| 9 | AI Task Manager | 🟡 Intermediate | 04, 05, 08 | ⭐⭐⭐ |
| 10 | Memory-Augmented Chatbot | 🟡 Intermediate | 02, 03, 05 | ⭐⭐⭐ |
| 11 | AI Coding Agent | 🔴 Advanced | 04, 06, 07, 08 | ⭐⭐⭐⭐⭐ |
| 12 | Multi-Agent Dev Team | 🔴 Advanced | 07, 08, 09 | ⭐⭐⭐⭐⭐ |
| 13 | Self-Healing CI/CD | 🔴 Advanced | 07, 10, 11 | ⭐⭐⭐⭐ |
| 14 | AI Analytics Dashboard | 🔴 Advanced | 01, 03, 05, 10, 11 | ⭐⭐⭐⭐ |
| 15 | Domain Research Assistant | 🔴 Advanced | 01, 02, 04, 05, 11 | ⭐⭐⭐⭐ |
| 16 | Autonomous Dev Platform | 🟣 Expert | 01-11 (all) | ⭐⭐⭐⭐⭐ |
| 17 | Adaptive Learning System | 🟣 Expert | 01, 02, 03, 04, 08, 11 | ⭐⭐⭐⭐⭐ |
| 18 | AI Security Audit System | 🟣 Expert | 01, 05, 07, 09, 10, 11 | ⭐⭐⭐⭐⭐ |
| 19 | Cross-Platform App Generator | 🟣 Expert | 04, 06, 07, 09, 10 | ⭐⭐⭐⭐⭐ |
| 20 | Infrastructure-as-Code AI | 🟣 Expert | 01, 04, 05, 06, 07, 10 | ⭐⭐⭐⭐⭐ |

---

### 🗺️ Module → Project Matrix

> How many projects each module serves — showing the value of each knowledge area.

| Module | Module Name | # of projects using it | Representative projects |
|--------|-----------|------------------|-----------------|
| **01** | Retrieve Memory & Knowledge | **15/20** | Enterprise RAG, Research Assistant |
| **02** | Build Context | **12/20** | Customer Support Agent, Memory Chatbot |
| **03** | Update Memory Store | **10/20** | PKB, Memory Chatbot, Analytics Dashboard |
| **04** | Plan & Decompose | **10/20** | AI Coding Agent, Research Assistant |
| **05** | Prompt Builder | **15/20** | Almost all projects |
| **06** | Decide Tools / MCP | **7/20** | AI Coding Agent, IaC Assistant |
| **07** | Workflow | **10/20** | Enterprise RAG, Multi-Agent, CI/CD |
| **08** | Task Management | **5/20** | AI Task Manager, Multi-Agent Dev Team |
| **09** | Multi-Agent | **5/20** | Multi-Agent Dev Team, Security Audit |
| **10** | Automation | **9/20** | CI/CD, Code Gen, Git Automation |
| **11** | Evaluation | **6/20** | Self-Healing CI/CD, Research Assistant |

---

### 📈 Hands-on Roadmap by Level

```
🟢 BASIC LEVEL (1-2 weeks per project)
═══════════════════════════════════════
Weeks 1-2:  #1 Personal Knowledge Base
           → Learn: Vector Search, Hybrid Search, KB Maintenance
           
Weeks 3-4:  #2 Document Q&A Chatbot
           → Learn: Chunking, Embedding, Context Building, Prompt Templates
           
Weeks 5-6:  #3 Hybrid Search Engine
           → Learn: BM25 + Vector fusion, Re-ranking, Context Compression

───────────────────────────────────────

🟡 INTERMEDIATE LEVEL (2-3 weeks per project)
═══════════════════════════════════════
Weeks 7-9:  #6 Enterprise RAG Platform
           → Learn: Pipeline Design, Error Recovery, Observability
           
Weeks 10-12: #7 Customer Support AI Agent
           → Learn: Multi-turn Context, Planning, Workflow

───────────────────────────────────────

🔴 ADVANCED LEVEL (3-4 weeks per project)
═══════════════════════════════════════
Weeks 13-16: #11 AI Coding Agent
            → Learn: ReAct Pattern, MCP Protocol, State Machine
           
Weeks 17-20: #12 Multi-Agent Development Team
            → Learn: Agent Roles, Orchestration, Shared Memory

───────────────────────────────────────

🟣 EXPERT LEVEL (4-6 weeks per project)
═══════════════════════════════════════
Weeks 21-26: #16 Autonomous AI Development Platform
            → Learn: Integrate ALL modules into a complete system
```

---

### 💼 Career Opportunities & Salary

| Role | Core skills from the framework | VN salary (2025) | Global salary |
|---------|------------------------------|--------------------|--------------------|
| **AI Engineer** | Modules 01-07: RAG, Agent, Workflow | 30-80M/month | $100K-200K/year |
| **MLOps / AI Platform Engineer** | Modules 07, 10, 11: Pipeline, CI/CD, Monitoring | 25-60M/month | $120K-180K/year |
| **Backend Developer (AI-focused)** | Modules 01-06: RAG integration, API design | 20-50M/month | $80K-150K/year |
| **DevOps/SRE with AI** | Modules 07, 10, 11: Self-healing, Automation | 25-60M/month | $100K-160K/year |
| **Tech Lead (AI Products)** | Modules 04, 08, 09: Planning, Multi-agent orchestration | 40-100M/month | $150K-250K/year |
| **AI Freelancer / Consultant** | The whole framework: Build custom AI solutions | 50-200M/month (project-based) | $100-300/hour |

---

### 💡 Tips to Get Started

```
1. START SMALL
   ├── Don't try to build an "Autonomous Dev Platform" right away
   ├── Start with #1 (PKB) or #2 (Document Q&A)
   └── Master the fundamentals before making things complex

2. BUILD IN PUBLIC
   ├── Write a blog post about building each project
   ├── Share on GitHub to get feedback
   └── Build an impressive portfolio for employers

3. ITERATE & COMBINE
   ├── Start simple → add features module by module
   ├── Combine 2-3 small projects into a bigger one
   └── E.g.: PKB (#1) + Doc Q&A (#2) = Enterprise RAG (#6)

4. FOCUS ON REAL PROBLEMS
   ├── Build something that solves a REAL problem of yours
   ├── E.g.: Automate docs for your company's codebase
   ├── E.g.: A chatbot answering questions from SRS/PRD
   └── Real problems = Real portfolio = Real job opportunities
```

---

## 💡 Real Examples

### Example 1: Building a simple RAG Pipeline

<details>
<summary><b>Example 1: Building a simple RAG Pipeline (Click to expand/collapse)</b></summary>

```python
# Step 1: Chunk documents
from pathlib import Path

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start = start + chunk_size - overlap
    return chunks

# Step 2: Embed chunks with Ollama
import requests

def embed_text(text):
    response = requests.post("http://localhost:11434/api/embed", json={
        "model": "nomic-embed-text",
        "input": text
    })
    return response.json()["embeddings"][0]

# Step 3: Create a simple vector store
import numpy as np

class SimpleVectorStore:
    def __init__(self):
        self.vectors = []
        self.documents = []
    
    def add(self, doc, vector):
        self.documents.append(doc)
        self.vectors.append(vector)
    
    def search(self, query_vec, top_k=3):
        scores = []
        q = np.array(query_vec)
        for i, v in enumerate(self.vectors):
            score = np.dot(q, np.array(v)) / (np.linalg.norm(q) * np.linalg.norm(np.array(v)))
            scores.append((i, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return [(self.documents[i], s) for i, s in scores[:top_k]]

# Step 4: Generate the answer
def generate_answer(query, context_docs):
    context = "\\n".join([f"- {doc}" for doc in context_docs])
    prompt = f"""Based on the information below, answer the question.

Information:
{context}

Question: {query}

Answer:"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
```

</details>

### Example 2: Multi-Agent Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                  MULTI-AGENT CODING WORKFLOW                      │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Planner      │───►│  Coder        │───►│  Reviewer    │       │
│  │  (Analyze)    │    │  (Write code) │    │  (Review)    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                    │                │
│         │                   │                    ▼                │
│         │                   │            ┌──────────────┐        │
│         │                   │            │  Tester       │        │
│         │                   │            │  (Test code)  │        │
│         │                   │            └──────────────┘        │
│         │                   │                    │                │
│         │                   │                    ▼                │
│         │                   │            ┌──────────────┐        │
│         └───────────────────┴───────────►│  Deployer     │        │
│                                         │  (Deploy)     │        │
│                                         └──────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📊 Knowledge Summary

| Skill | Level 1 (Basic) | Level 2 (Intermediate) | Level 3 (Advanced) |
|---------|-------------------|----------------------|---------------------|
| **Search** | Keyword search (BM25) | Vector search | Hybrid + Re-ranking |
| **Context** | Simple concatenation | Sliding window | Hierarchical + Compression |
| **Memory** | File-based | Vector store | Event sourcing + Consolidation |
| **Planning** | Sequential tasks | Parallel + Dependencies | Tree of Thought |
| **Tools** | Manual tool call | Rule-based selection | Intent classification + MCP |
| **Workflow** | Linear pipeline | State machine | Error recovery + Observability |
| **Multi-Agent** | Two agents | Orchestrated team | Shared memory + Conflict resolution |
| **Automation** | Simple scripts | CI/CD pipelines | Self-healing systems |
| **Evaluation** | Manual testing | Automated metrics | Continuous improvement loop |

---

## 🔗 Useful Links

| Source | Description |
|-------|-------|
| [Ollama](https://ollama.com) | Run LLM & Embedding locally |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector search library |
| [ChromaDB](https://www.trychroma.com) | Embedded vector database |
| [MCP Protocol](https://modelcontextprotocol.io) | Model Context Protocol |
| [LangChain](https://langchain.com) | Framework for LLM applications |
| [LlamaIndex](https://www.llamaindex.ai) | Data framework for LLMs |

---

> **Note**: Each module in the framework has a detailed README.md with code examples. You can read each module individually or learn along the roadmap from Phase 1 to Phase 6.
