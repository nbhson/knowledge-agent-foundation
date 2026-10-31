# 🧠 Memory & Context in AI — A Learning Guide

> **This guide teaches you how to BUILD AN AI AGENT** — from memory design, handling context, planning, teamwork between agents, to automation and checking results. This is NOT a guide on using AI the everyday way.

In plain words: an **AI agent** = a program where an **LLM** (Large Language Model — a text model like GPT or Claude that generates answers) is the "brain", and this framework is the "body" — the tools, memory, and rules that let the brain actually get work done. **Memory** = what the agent saves and can look up later, like notes on a desk. **Context** = the text the model can read *right now*, in one request.

---

## 🎯 Audience

This section tells you who this guide is for, so you know if it fits you before reading on.

| Group | Purpose |
|------|----------|
| **AI Engineers** | Design and implement AI Agent systems |
| **Backend Developers** | Integrate LLM + RAG into applications |
| **DevOps / SRE** | Deploy and monitor AI pipelines |
| **Tech Leads** | Evaluate and select the right AI architecture |
| **Researchers** | Reference patterns and best practices |

How to read it: each row = a reader type and what they will get. For example, a **Backend Developer** will learn to plug an **LLM** (the text-generating model) + **RAG** (Retrieval-Augmented Generation — first search your own documents, then make the model answer using what was found, so it invents less) into an existing app. **SRE** = Site Reliability Engineer — the person keeping production systems up and running.

> **One-line summary:** This guide is for engineers, developers, DevOps, leads, and researchers who want to *build* agents, not just chat with AI.

## 📋 Prerequisites

This section lists what you should already know, so you don't get stuck mid-way.

| Knowledge | Level | Notes |
|-----------|--------|---------|
| Python | Basic → Intermediate | The framework's main language |
| LLM Concepts | Basic | Transformer, Token, Prompt |
| REST API | Basic | Communicating with Ollama, MCP servers |
| Git | Basic | Managing code and automation |

How to read it: each row = a topic, how deep you must know it, and why. Glossary: **Transformer** = the neural-network design behind every modern LLM. **Token** = the chunk of text (about a short word, or 3-4 characters) that models actually read — they never see raw letters. **Prompt** = the text you send the model: instructions + context + your question. **REST API** = how programs talk to each other over HTTP, e.g. your code calling Ollama. **Ollama** = a free tool that runs LLMs on your own machine. **MCP server** = a service that exposes tools (search, files, GitHub…) to an agent through a standard plug. **Git** = the version-control system that records every change to your code.

> **One-line summary:** You need basic Python, LLM vocabulary (Transformer/Token/Prompt), REST APIs, and Git before starting.

## 🛠️ How to Use

This section gives you the 3 steps to work through the guide, from setup to practice.

### Step 1: Set up the environment

First, install the tools: Ollama (runs LLMs on your machine, free) and Python. The script below does the setup for you.

<details>
<summary><b>Step 1: Set up the environment (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/01-step-1-set-up-the-environment.sh`](examples/01-step-1-set-up-the-environment.sh)

> **Oct-2026 note.** The two `ollama pull` lines are just Jul-2026 examples —
> swap in any newer model, the pattern stays the same. Fresh picks:
> `qwen3.6`, `deepseek-v4-flash/pro (up to 1M ctx)`, `gemma4 26B-A4B`, `gpt-oss:20b/120b (light via MXFP4)`,
> `muse-glimmer 30b`, `minimax-m3`, `glm-5.2`, `granite4.2`. Use Ollama >=0.6.

</details>

Glossary for the note above: `ollama pull qwen3.6` = download that model to your machine (like `git clone`, but for models). **1M ctx** = a context window of 1 million tokens — the model can read roughly a whole book in one request. **MXFP4** = a compact 4-bit number format that shrinks the model so it fits in less RAM.

> **One-line summary:** Install Ollama + Python with the provided script; any recent model name works, the pattern never changes.

### Step 2: Learn along the roadmap
Start with **Phase 1** (Core Skills) and progress to **Phase 6** (Evaluation). Each module has a detailed README.md with code examples.

In plain words: each "Phase" is a group of modules (a module = one skill folder with its own README). Learn in order — finding information (Phase 1) before storing it (Phase 3) — because later modules reuse earlier ones.

> **One-line summary:** Follow the phases in order, 01 → 11; each module folder has its own README with runnable examples.

### Step 3: Practice
- Clone the repo and try the code examples in each module
- Change parameters to observe results
- Combine modules to build a complete pipeline

Glossary: **clone the repo** = download a full copy of this code repository with `git clone`. **Parameters** = the adjustable settings in the code (e.g., how many search results to return). **Pipeline** = a chain of steps where one step's output feeds the next.

> **One-line summary:** Don't just read — run the examples, tweak the settings, and chain modules into one working pipeline.

## ⚡ Quick Reference

This table is the map of the whole guide: find your goal in the left column, then jump to the module that teaches it.

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
| Isolate untrusted code execution | [12 - Sandbox Execution](#control-plane-harness-modules-1215) |
| Debug/replay a run after the fact | [13 - Trajectory & Observability](#control-plane-harness-modules-1215) |
| Keep the context window bounded | [14 - Compaction & Context](#control-plane-harness-modules-1215) |
| Gate an irreversible action on a human | [15 - Approval Gates](#control-plane-harness-modules-1215) |
| **Build a complete agent system architecture (8 Layers)** | [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md) |

How to read it: left column = a goal you might have; right column = the module to read, as a clickable link. For example, "Isolate untrusted code execution" → module 12, which runs agent-written code in a **sandbox** (a sealed, isolated environment so buggy or malicious code cannot touch your real system). **Context window** = how much text the model can read at once, measured in tokens. **CI/CD** = Continuous Integration/Continuous Delivery — automatically build, test, and ship code on every push.

> **Numbering note.** Harness modules are `01`–`15`. The `Part` labels below
> (`Part I` … `Part XIII`) number *framework parts*, a different namespace —
> which is why `Part XII` is Loop Engineering and `Part XIII` is Graph
> Engineering, while harness module `12` is Sandbox Execution. Loop Engineering
> lives in the top-level `loop/` directory, not in `harness/`.

In plain words: there are two numbering systems that don't match. "Harness module 12" = the folder `harness/12-sandbox-execution/`; "Part XII" = the 12th framework part, which is Loop Engineering. Always check which one is meant.

### Standard Protocols & SDKs (2026)

Signpost: this section names the industry-standard protocols and code libraries for agents in 2026 — knowing which layer each one covers saves weeks of confusion.

> **Summary (details in [AGENT_SYSTEM_ARCHITECTURE.md](AGENT_SYSTEM_ARCHITECTURE.md)):**
> - **MCP** (Model Context Protocol, spec `2026-07-28`) — agent↔tool. Every tool-calling module should go through MCP.
> - **A2A** (Agent-to-Agent, Linux Foundation — launched by Google 04/2025, donated 06/2025) — agent↔agent handoffs and collaboration.
> - **Agent Skills** (open standard at [agentskills.io](https://agentskills.io) since 12/2025) — package expertise as SKILL.md.
> - **Mainstream SDKs**: Claude Agent SDK (formerly Claude Code SDK), OpenAI Agents SDK, Google ADK (GA 04/2025), LangGraph, CrewAI, AWS Strands.
> - **GraphRAG 2026**: LazyGraphRAG + LightRAG cut costs by ~700× vs original GraphRAG (details in [GRAPH_ENGINEERING.md](GRAPH_ENGINEERING.md) and `graph/05-graph-rag/`).

Plain-language glosses: **MCP** = an open-standard "plug" that connects one agent to many tools (files, GitHub, databases) without custom wiring per tool. **A2A** = a standard for two agents to hand work to each other. **Agent Skills** = a standard file format (SKILL.md) for packaging "how to do X" know-how. **SDK** = Software Development Kit — a ready-made code library. **GraphRAG** = retrieval that walks a knowledge graph (things + relationships) instead of only matching text; LazyGraphRAG/LightRAG are much cheaper ways to do it.

> **One-line summary:** MCP connects an agent to tools, A2A connects agent to agent, Agent Skills packages know-how, and the listed SDKs implement all of this for you.

## Learning Structure

Signpost: this tree shows every folder in the framework and what it teaches, so you always know where you are.

```
AI/
├── AI_AGENT_FRAMEWORK.md                   ← HOMEPAGE
├── AGENT_SYSTEM_ARCHITECTURE.md            ← AGENT SYSTEM ARCHITECTURE (8 Layers, updated 2026)
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
│  ├── 11-evaluation/                        ← EVALUATION
│  │
│  │  ── CROSS-CUTTING CONTROL PLANE ──
│  │  (substrate every module above depends on)
│  ├── 12-sandbox-execution/                 ← SANDBOX / ISOLATION
│  ├── 13-trajectory-observability/          ← TRAJECTORY / AUDIT
│  ├── 14-compaction-context/                ← CONTEXT COMPACTION
│  └── 15-approval-gates/                    ← HUMAN-IN-THE-LOOP
│
├── loop/                                    ← LOOP ENGINEERING
│  ├── 01-concepts/  02-patterns/  03-safety/
│  ├── 04-operating/  05-multi-loop/  06-anti-patterns/
│  └── 07-tools/                            ← THE IMPROVEMENT LOOP
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

How to read the tree: each line = a file or folder; `├──` and `└──` mean "this folder contains". Three big areas: **harness/** = the 15 core modules — modules 01-11 are skills, modules 12-15 are the control plane. **loop/** = Loop Engineering — designing self-sustaining agent loops (an agent that keeps working on its own: pick task → do it → check → repeat). **graph/** = Graph Engineering — storing knowledge as a graph of entities (things, like `Alice`) and relations (links, like `—works_at→ Acme`). **Control plane** (line "CROSS-CUTTING CONTROL PLANE") = the shared foundation — isolation, audit trail, context limits, human approval — that every skill module sits on. **Audit** = a recorded history you can inspect later.

> **One-line summary:** The framework = 15 harness modules (11 skills + 4 control-plane modules), plus `loop/` for self-running loops and `graph/` for knowledge stored as a graph.

## Learning Path

Signpost: this diagram shows the recommended order to learn the modules, phase by phase, and what each phase covers.

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

How to read it: each box = a module; arrows (`───►`) = "learn this before that"; Phases group modules by job. Phase 1 gathers information, Phase 2 turns it into an answer, Phase 3 stores and plans, Phases 4-5 organize and automate, Phase 6 measures quality. Glossary from the diagram: **State Machine** = a design where the system is in exactly one state at a time with defined moves between states (e.g., `idle → planning → coding`). **Decomposition** = splitting one big task into small ones. **Dependency Graph** = a chart of which tasks must finish before others start. **Orchestration** = coordinating who does what, and when. **Benchmarks** = standardized tests to compare systems.

> **One-line summary:** Learn in 6 phases — gather → answer → store & plan → organize → automate → evaluate — each phase builds on the previous one.

## Hands-on Environment

Signpost: this table lists every tool the examples run on — all free and local, so you can reproduce everything on your own laptop.

| Component | Model / Tool | Runs |
|-----------|-------------|------|
| LLM | `gemma3:12b` | Local via Ollama |
| Embedding | `nomic-embed-text` (768D) | Local via Ollama |
| Vector Store | FAISS / ChromaDB | Local |
| Graph Store | Neo4j / Kuzu / NetworkX | Local (Docker or embedded) |
| GNN | PyG / DGL | Local (Python) |
| BM25 | Custom Python | Local |
| MCP Server | GitHub MCP, Custom tools | Local |

How to read it: each row = one job, the tool that does it, and where it runs. Glossary: **Embedding** = turning text into a list of numbers (a **vector**); `768D` = each list has 768 numbers, so "similar meaning" becomes "nearby numbers". **Vector Store** = a database that stores those lists and finds the nearest ones fast (FAISS and ChromaDB are libraries for this). **Graph Store** = a database storing nodes and links (Neo4j, Kuzu), or plain Python objects (NetworkX). **GNN** = Graph Neural Network — a model that learns from a graph's shape; PyG/DGL are Python libraries for it. **BM25** = a classic formula that scores documents by how often your search words appear, favoring rare words. **Docker** = packaging software into isolated containers. **Embedded** = runs inside your Python process, no separate server needed.

> **One-line summary:** Everything runs locally and free — Ollama for models, FAISS/ChromaDB for vector search, Neo4j/Kuzu for graphs — so you can follow along offline.

## Details for Each Part

Signpost: this is the catalog of all skill modules, the control plane, and the loop/graph parts. Each part answers one question and links into the module READMEs.

### Part I: Retrieve Memory & Knowledge
> How do you find the right information?

Signpost: this part teaches 5 ways to search stored knowledge, from keyword math to graphs. "Retrieval" = fetching the few relevant pieces from a big pile, before the model answers.

| # | Topic | Description |
|---|-------|-------|
| 1.1 | [Vector Search](harness/01-retrieve-memory-knowledge/README.md#1-vector-search) | Semantic similarity with embeddings |
| 1.2 | [BM25 Search](harness/01-retrieve-memory-knowledge/README.md#2-bm25-search) | Keyword matching, term frequency |
| 1.3 | [Hybrid Search](harness/01-retrieve-memory-knowledge/README.md#3-hybrid-search) | Combine Vector + BM25 |
| 1.4 | [Knowledge Graph](harness/01-retrieve-memory-knowledge/README.md#4-knowledge-graph) | Entity relationships, graph traversal |
| 1.5 | [Multi-Source Retrieval](harness/01-retrieve-memory-knowledge/README.md#5-multi-source-retrieval) | Fusing results from many sources |

How to read it: each row = one search technique. Glossary: **Vector Search** (1.1) = match by meaning using embeddings — a question about "cheap flights" matches a note saying "low-cost airfare" even with no shared words. **BM25** (1.2) = match by exact words and frequency — good for names and codes. **Hybrid Search** (1.3) = run both and merge the results. **Knowledge Graph** (1.4) = search by following entity links ("who reviewed this PR?" → person → PR). **Multi-Source** (1.5) = search several stores at once and combine the hits.

> **One-line summary:** Retrieval finds the right few pieces before the model answers — vector search matches meaning, BM25 matches words, and hybrid search does both.

### Part II: Build Context
> How do you organize information effectively?

Signpost: this part teaches how to fit the right information into the model's limited reading space (the context window).

| # | Topic | Description |
|---|-------|-------|
| 2.1 | [Context Window Management](harness/02-build-context/README.md#1-context-window-management) | Token limits, sliding window |
| 2.2 | [Context Compression](harness/02-build-context/README.md#2-context-compression) | Summarize, extract key info |
| 2.3 | [Prompt Templates](harness/02-build-context/README.md#3-prompt-templates) | System/user/assistant roles |
| 2.4 | [Hierarchical Context](harness/02-build-context/README.md#4-hierarchical-context) | Summary → Detail structure |
| 2.5 | [Multi-turn Context](harness/02-build-context/README.md#5-multi-turn-context) | Conversation memory management |

How to read it: each row = one way to organize what the model reads. Glossary: **Sliding window** (2.1) = keep only the most recent N tokens, like a rolling camera view. **Compression** (2.2) = replace long text with a short summary. **System/user/assistant roles** (2.3) = the three standard voices in a prompt — rules from the system, question from the user, prior replies from the assistant. **Hierarchical** (2.4) = a summary first, details only where needed. **Multi-turn** (2.5) = remembering earlier exchanges across a conversation without overloading the window.

> **One-line summary:** The context window is small and expensive — build context by trimming, compressing, and structuring exactly what the model needs to see.

### Part III: Update Memory & Knowledge Store
> How do you store new information?

Signpost: this part teaches how an agent saves what it learned, so future runs can use it instead of starting from zero.

| # | Topic | Description |
|---|-------|-------|
| 3.1 | [Write-back Memory](harness/03-update-memory-store/README.md#1-write-back-memory) | Write new events into memory |
| 3.2 | [Memory Consolidation](harness/03-update-memory-store/README.md#2-memory-consolidation) | Merge, dedupe facts |
| 3.3 | [Report Generation](harness/03-update-memory-store/README.md#3-report-generation) | Create structured output |
| 3.4 | [KB Maintenance](harness/03-update-memory-store/README.md#4-kb-maintenance) | CRUD the knowledge base |
| 3.5 | [Event Sourcing](harness/03-update-memory-store/README.md#5-event-sourcing-pattern) | Full audit trail |

How to read it: each row = one memory-keeping job. Glossary: **Write-back** (3.1) = after a run, save the new events/facts into the store. **Consolidation** (3.2) = merge duplicates and drop contradictions, like tidying notes. **Report Generation** (3.3) = output structured documents (Markdown/JSON) from raw data. **KB** = knowledge base; **CRUD** (3.4) = Create, Read, Update, Delete — the four basic data operations. **Event Sourcing** (3.5) = store every change as an append-only event (you may only add, never edit old entries), so you can replay and audit the full history.

> **One-line summary:** Memory must be written back, tidied (dedupe/merge), and kept as an append-only event log so history stays auditable.

### Part IV: Plan & Decompose Task
> How do you break down complex tasks?

Signpost: this part teaches how an agent turns "build feature X" into small ordered steps it can actually execute.

| # | Topic | Description |
|---|-------|-------|
| 4.1 | [Task Decomposition](harness/04-plan-decompose-task/README.md#1-task-decomposition-patterns) | Sequential, parallel, hierarchical |
| 4.2 | [Planning Algorithms](harness/04-plan-decompose-task/README.md#2-planning-algorithms) | Plan-and-Solve, ToT |
| 4.3 | [Agent Workflows](harness/04-plan-decompose-task/README.md#3-agent-workflows) | ReAct, Multi-agent, State Machine |
| 4.4 | [State Management](harness/04-plan-decompose-task/README.md#4-state-management) | Checkpoint, rollback |
| 4.5 | [ReAct Pattern](harness/04-plan-decompose-task/README.md#5-react-pattern) | Thought → Action → Observation |

How to read it: each row = one planning technique. Glossary: **Sequential/parallel/hierarchical** (4.1) = steps one after another, steps at the same time, or steps in a tree (big task → subtasks). **Plan-and-Solve** (4.2) = a prompt pattern: "first write the plan, then execute each step". **ToT** = Tree of Thoughts — explore several reasoning branches and keep the best one, instead of one fixed line of thinking. **Checkpoint/rollback** (4.4) = save progress so you can undo to a good state, like a save point in a game. **ReAct** (4.5) = Reason + Act — the loop: think ("Thought") → use a tool ("Action") → look at the result ("Observation") → think again.

> **One-line summary:** Planning = split the task into small steps, order them, and run a think-act-observe loop (ReAct) with checkpoints to undo mistakes.

### Part V: Prompt Builder
> How do you write the best prompts?

Signpost: this part teaches prompt construction as engineering — templates, examples, reasoning steps, safety filters, and output formats.

| # | Topic | Description |
|---|-------|-------|
| 5.1 | [Prompt Templates](harness/05-prompt-builder/README.md#1-prompt-templates) | Reusable templates with variables |
| 5.2 | [Few-shot Examples](harness/05-prompt-builder/README.md#2-few-shot-examples) | Dynamic example selection |
| 5.3 | [Chain-of-Thought](harness/05-prompt-builder/README.md#3-chain-of-thought-cot) | CoT variants |
| 5.4 | [Guardrails](harness/05-prompt-builder/README.md#4-guardrails) | Safety filters, validation |
| 5.5 | [Output Format](harness/05-prompt-builder/README.md#5-output-format-control) | JSON, Markdown, Table |

How to read it: each row = one prompt technique. Glossary: **Template** (5.1) = a prompt with blanks (`{user_name}`) filled in at runtime. **Few-shot** (5.2) = include 2-3 solved examples in the prompt so the model imitates the pattern ("few-shot" = a few examples). **CoT** = Chain-of-Thought (5.3) = ask the model to reason step by step before answering. **Guardrails** (5.4) = filters that block unsafe inputs/outputs — e.g., stop a **prompt injection** (a hidden instruction smuggled into data, like "ignore previous rules" planted in a web page the agent reads). **Output format** (5.5) = demand a machine-readable shape, e.g. `JSON` (a strict key-value text format programs can parse).

> **One-line summary:** Good prompts are engineered: reusable templates, a few examples, step-by-step reasoning, safety filters, and a strict output format.

### Part VI: Decide Tools / MCP Calls
> Which tool to use when?

Signpost: this part teaches how an agent picks the right tool from a menu and calls it safely — the "hands" of the agent.

| # | Topic | Description |
|---|-------|-------|
| 6.1 | [Tool Selection](harness/06-decide-tools-mcp/README.md#1-tool-selection-patterns) | Registry, search, categories |
| 6.2 | [Intent Classification](harness/06-decide-tools-mcp/README.md#2-intent-classification) | Rule-based & LLM-based |
| 6.3 | [MCP Protocol](harness/06-decide-tools-mcp/README.md#3-mcp-model-context-protocol) | Model Context Protocol |
| 6.4 | [Tool Executor](harness/06-decide-tools-mcp/README.md#4-tool-executor-with-error-handling) | Error handling & retry |

How to read it: each row = one step of tool use. Glossary: **Registry** (6.1) = a catalog of available tools with descriptions the agent can browse. **Intent Classification** (6.2) = decide what the user actually wants — by fixed rules or by asking an LLM. **MCP** (6.3) = the standard protocol (see above) that connects the agent to tools. **Tool Executor** (6.4) = the runner that actually calls the tool and handles failure — **retry** = try again on a temporary error (e.g., network timeout), usually with backoff (wait longer between tries).

> **One-line summary:** Tool use = classify the intent, pick the tool from the registry via MCP, and call it through an executor that retries and handles errors.

---

### Part VII: Workflow
> How do you organize execution processes?

Signpost: this part teaches how to arrange many steps into reliable automated flows.

| # | Topic | Description |
|---|-------|-------|
| 7.1 | [Workflow Patterns](harness/07-workflow/README.md#1-workflow-patterns) | Sequential, parallel, conditional |
| 7.2 | [Pipeline Design](harness/07-workflow/README.md#2-pipeline-design) | Transform, filter, sink |
| 7.3 | [State Machine](harness/07-workflow/README.md#3-state-machine) | FSM for agents |
| 7.4 | [Error Recovery](harness/07-workflow/README.md#4-error-recovery) | Retry, circuit breaker |
| 7.5 | [Observability](harness/07-workflow/README.md#5-observability) | Logging, metrics |

How to read it: each row = one workflow-building tool. Glossary: **Conditional** (7.1) = "if X then do A, else B" branching. **Transform/filter/sink** (7.2) = pipeline stages — change the data, drop what you don't need, then write it to its final destination ("sink" = where data ends up, e.g., a database). **FSM** (7.3) = Finite State Machine — same as state machine above. **Circuit breaker** (7.4) = after N failures in a row, stop calling the failing service for a while, like flipping a breaker off before it burns. **Metrics** (7.5) = measured numbers over time (requests/sec, error rate).

> **One-line summary:** Workflows = arrange steps (sequential/parallel/branching), survive failures with retries and circuit breakers, and log everything you can inspect later.

### Part VIII: Task Management
> How do you manage and track tasks?

Signpost: this part teaches how an agent keeps a to-do list: sorting, splitting, ordering, and tracking state of tasks.

| # | Topic | Description |
|---|-------|-------|
| 8.1 | [Task Classification](harness/08-task/README.md#1-task-classification) | Classify by category & complexity |
| 8.2 | [Task Decomposition](harness/08-task/README.md#2-task-decomposition) | Feature, layer, file, TDD |
| 8.3 | [Priority & Scheduling](harness/08-task/README.md#3-priority--scheduling) | Eisenhower matrix, token budget |
| 8.4 | [Task State Management](harness/08-task/README.md#4-task-state-management) | Lifecycle, valid transitions |
| 8.5 | [Dependency Management](harness/08-task/README.md#5-dependency-management) | DAG, topological sort |

How to read it: each row = one task-tracking skill. Glossary: **TDD** (8.2) = Test-Driven Development — write the failing test first, then the code. **Eisenhower matrix** (8.3) = sort tasks by urgent/not-urgent × important/not-important. **Token budget** (8.3) = a cap on how many tokens (cost) a task may spend. **Lifecycle/transitions** (8.4) = the legal moves between states (`todo → doing → done`), so a task can't jump from `done` back to `doing` by accident. **DAG** (8.5) = Directed Acyclic Graph — a one-way dependency chart with no loops (A before B, B before C, never C back to A). **Topological sort** = ordering DAG tasks so every task comes after its prerequisites.

> **One-line summary:** Task management = classify, split, prioritize (Eisenhower + token budget), track legal state transitions, and order work by its dependency DAG.

### Part IX: Multi-Agent Systems
> How do you coordinate multiple agents?

Signpost: this part teaches running several specialized agents as a team — and handling the conflicts that come with teamwork.

| # | Topic | Description |
|---|-------|-------|
| 9.1 | [Agent Roles](harness/09-multi-agent/README.md#1-agent-roles) | Planner, Coder, Reviewer, Tester |
| 9.2 | [Communication Patterns](harness/09-multi-agent/README.md#2-communication-patterns) | Hierarchical, P2P, pipeline |
| 9.3 | [Orchestration](harness/09-multi-agent/README.md#3-orchestration-strategies) | Sequential, parallel, debate, voting |
| 9.4 | [Shared Memory](harness/09-multi-agent/README.md#4-shared-memory) | Versioned, tagged, locked |
| 9.5 | [Conflict Resolution](harness/09-multi-agent/README.md#5-conflict-resolution) | File lock, voting, deadlock detection |

How to read it: each row = one teamwork mechanism. Glossary: **Roles** (9.1) = each agent gets one specialty, like a job title. **Hierarchical** (9.2) = a boss agent delegates to workers; **P2P** = peer-to-peer, all agents talk directly; **pipeline** = each agent passes work to the next. **Debate/voting** (9.3) = agents argue for different answers, then vote — cheaper than a perfect single agent. **Versioned/locked memory** (9.4) = shared notes carry version numbers and locks so two agents can't overwrite each other. **Deadlock** (9.5) = two agents each wait forever for the other's lock — like two people in a hallway each politely waiting for the other to pass.

> **One-line summary:** Multi-agent = assign roles, pick a communication shape, coordinate via orchestration, and protect shared memory with versions, locks, and deadlock detection.

### Part X: Automation
> How do you automate repetitive tasks?

Signpost: this part teaches making the agent run on triggers — timers, events, failures — instead of a human pressing a button each time.

| # | Topic | Description |
|---|-------|-------|
| 10.1 | [Automation Patterns](harness/10-automation/README.md#1-automation-patterns) | Event, scheduled, reactive, self-healing |
| 10.2 | [CI/CD Pipelines](harness/10-automation/README.md#2-cicd-pipelines) | GitHub Actions, deploy pipeline |
| 10.3 | [Code Generation](harness/10-automation/README.md#3-code-generation-automation) | Scaffolding, templates |
| 10.4 | [Scheduled Tasks](harness/10-automation/README.md#4-scheduled-tasks) | Cron, interval, daily |
| 10.5 | [Git Automation](harness/10-automation/README.md#5-git-automation) | Hooks, commit conventions |
| 10.6 | [Monitoring & Alerts](harness/10-automation/README.md#6-monitoring--alerts) | Thresholds, dashboards |

How to read it: each row = one automation pattern. Glossary: **Event-driven** (10.1) = run when something happens (a PR opens); **scheduled** = run at fixed times; **reactive** = respond to alerts; **self-healing** = detect and fix your own failures. **GitHub Actions** (10.2) = GitHub's built-in runner that executes workflows on push/PR. **Scaffolding** (10.3) = generating starter code structure (folders, empty files, boilerplate). **Cron** (10.4) = the classic time scheduler (e.g., "run daily at 6 PM"). **Hooks** (10.5) = scripts Git runs automatically at moments like `pre-commit` (just before a commit is created). **Threshold** (10.6) = a limit that, once crossed, fires an alert (e.g., error rate > 5%).

> **One-line summary:** Automation = trigger the agent by events, schedules, or failures — and watch it with dashboards and thresholds so silent breakage can't happen.

### Part XI: Evaluation
> How do you evaluate AI coding effectiveness?

Signpost: this part teaches measuring whether the agent's work is actually good — the only way to improve anything on purpose.

| # | Topic | Description |
|---|-------|-------|
| 11.1 | [Evaluation Dimensions](harness/11-evaluation/README.md#1-evaluation-dimensions) | Correctness, quality, safety, speed |
| 11.2 | [Quality Metrics](harness/11-evaluation/README.md#2-quality-metrics) | Complexity, maintainability |
| 11.3 | [Performance Benchmarks](harness/11-evaluation/README.md#3-performance-benchmarks) | Benchmark suite, compare |
| 11.4 | [Evaluation Framework](harness/11-evaluation/README.md#4-evaluation-framework) | Auto-eval pipeline |
| 11.5 | [Continuous Improvement](harness/11-evaluation/README.md#5-continuous-improvement) | Trend analysis, suggestions |
| 11.6 | [Reporting & Dashboards](harness/11-evaluation/README.md#6-reporting--dashboards) | Markdown/JSON reports |

How to read it: each row = one measuring tool. Glossary: **Correctness** (11.1) = does the code do what it should; **safety** = does it break or expose anything. **Maintainability** (11.2) = how easy the code is to change later — low complexity, clear names. **Benchmark suite** (11.3) = a fixed set of tasks with known good answers, so you can compare runs fairly. **Auto-eval pipeline** (11.4) = a workflow that grades every run automatically. **Trend analysis** (11.5) = comparing scores over time ("are we getting better or worse?").

> **One-line summary:** Evaluation = grade every agent run on correctness, quality, safety, and speed — automatically — and track the trend to improve on purpose.

### Control Plane (Harness Modules 12–15)
> How do you run, observe, bound, and authorize untrusted agent work?

Signpost: modules 12-15 answer the safety questions every skill module depends on: where does the code run, what happened, what got cut from context, and who approves dangerous actions.

Modules `12`–`15` are **not pipeline stages**. They are the cross-cutting substrate every
module above depends on. Each is authoritative for its own question; other modules
reference it rather than restating it.

| # | Topic | Description |
|---|-------|-------------|
| 12 | [Sandbox Execution](harness/12-sandbox-execution/README.md) | Isolation tiers, threat model, hardened runner, per-role policy matrix |
| 13 | [Trajectory & Observability](harness/13-trajectory-observability/README.md) | Append-only `TrajectoryEvent` stream, join keys, retention, redaction |
| 14 | [Compaction & Context](harness/14-compaction-context/README.md) | Compaction trigger, pin set, pruning, resume block |
| 15 | [Approval Gates](harness/15-approval-gates/README.md) | Risk tiers, gate payload, timeout-deny, human verdict, audit trail |

How to read it: each row = one safety module. Glossary: **Isolation tiers** (12) = levels of separation, from "run in-process" to "run in a throwaway container with no network"; a **threat model** = the list of what could go wrong and who would exploit it. **Trajectory** (13) = the full step-by-step record of a run; **append-only stream** = you can only add events, never edit or delete old ones; **redaction** = scrubbing secrets (passwords, tokens) from the record. **Compaction** (14) = summarizing/dropping older context to keep the window bounded; **pin set** = items marked "keep" that compaction may never drop; **pruning** = cutting out the rest. **Approval gate** (15) = a checkpoint where a human must approve before a risky, irreversible action runs (e.g., `git push --force` = overwriting the shared remote history — no undo); **timeout-deny** = if the human doesn't answer in time, the answer is automatically "no".

> **One-line summary:** Modules 12-15 are the safety chassis: run risky code in sandboxes, record everything append-only, keep context bounded with compaction, and require human approval for irreversible actions.

> The Roman `Part XII`/`XIII` labels that follow belong to the framework-part namespace
> (Loop, Graph). They are unrelated to harness module numbering.

### Part XII: Loop Engineering
> How do you design self-sustaining loops for AI agents?

Signpost: this part teaches agent loops that keep running on their own — and how to stop them becoming expensive or runaway.

| # | Topic | Description |
|---|-------|-------|
| 12.1 | [Concepts](loop/01-concepts/README.md) | 5 building blocks + memory, anatomy, L1-L3, taxonomy |
| 12.2 | [Patterns](loop/02-patterns/README.md) | 7 production patterns (daily-triage, pr-babysitter, ci-sweeper...) |
| 12.3 | [Safety](loop/03-safety/README.md) | Loop Design Checklist, denylist, human gates |
| 12.4 | [Operating](loop/04-operating/README.md) | Budget, logging, metrics, pause/kill |
| 12.5 | [Multi-Loop](loop/05-multi-loop/README.md) | Coordinate when running multiple loops |
| 12.6 | [Anti-Patterns](loop/06-anti-patterns/README.md) | 10 anti-patterns + failure mode catalog |
| 12.7 | [Tools](loop/07-tools/README.md) | loop-init, loop-audit, loop-cost, ecosystem |

How to read it: each row = one aspect of building agent loops. Glossary: a **loop** = an agent cycle that repeats without a human in each cycle (e.g., `pr-babysitter` = an agent that keeps checking a pull request, fixes review comments, re-tests, until merged). **L1-L3** (12.1) = three levels of loop autonomy, from single-task to multi-day. **Taxonomy** = a named classification of loop types. **Denylist** (12.3) = "danh sách đen" — a list of forbidden actions/paths the loop must never touch. **Human gates** = approval checkpoints inside the loop. **Pause/kill** (12.4) = switches to stop the loop immediately; **budget** = a spending/step cap so a stuck loop can't burn money forever. **Anti-patterns** (12.6) = named common mistakes (e.g., a loop that keeps "fixing" its own failed fix, forever).

> **One-line summary:** Loops let agents run unattended — but always with a budget, a denylist, human gates, and a kill switch, or they repeat their own mistakes forever.

### Part XIII: Graph Engineering
> How do you build graph-based knowledge systems for AI agents?

Signpost: this part teaches storing knowledge as a graph (things + relationships) so agents can answer "connected" questions that plain text search cannot.

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

How to read it: each row = one stage of building a graph system, from theory to evaluation. Glossary: **Entity/relation extraction** (13.2) = the LLM reads text and pulls out things and links ("Gemma —made_by→ Google"); **ontology** = the agreed vocabulary of node and link types. **Cypher** (13.3) = Neo4j's query language for graphs (like SQL, but for nodes and edges). **Node2Vec/GraphSAGE** (13.4) = methods to turn a node's graph position into a vector. **Subgraph retrieval** (13.5) = fetch a small connected piece of the graph as context. **Traversal/path finding** (13.6) = walking links between nodes ("who connects A to B?"). **Link prediction** (13.7) = the GNN guesses a missing connection. **ETL** (13.8) = Extract-Transform-Load — pull data from sources, reshape it, store it. **Path precision** (13.9) = how often the answer's cited path through the graph is actually correct.

> **One-line summary:** Graph engineering turns scattered text into a queryable web of entities and relations — so agents can answer multi-hop, connected questions with a checkable proof path.

> **One-line summary (whole section):** The parts catalog maps every question an agent builder has — find, organize, store, plan, prompt, tool, orchestrate, automate, measure — plus the safety chassis (12-15) and the two specialty tracks (loop, graph).

---

## 🧠 Understanding This Framework

> **This framework is the "orchestration brain" — the AI model is the "reasoning brain".**

In plain words: the framework decides *what happens* (what to fetch, when to call which tool, who approves), while the model only decides *what to say*. You can use **Ollama running locally for free** or a **paid API** depending on your budget.

### Illustrative flow: What does a RAG chatbot need?

Signpost: this diagram traces one user question through a RAG chatbot, so you can see which framework modules do the work and where the model itself is needed.

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

How to read it: an arrow (`↓`) = "hand this to the next step"; the double-line box = the only step that needs the actual AI model. Everything above the box is plain code: search your documents, arrange what was found, assemble the prompt.

> **One-line summary:** A RAG chatbot = search your documents, arrange the hits into a prompt, and only then hand it to the model to write the answer.

### Illustrative flow: What does GraphRAG need?

Signpost: this diagram shows the same question answered through a knowledge graph — slower to build, but the answer comes with a checkable proof path.

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

How to read it: same arrow notation as above. The difference from plain RAG: first an LLM extracts entities and relations from your documents, they are stored as a graph, and retrieval fetches a connected **subgraph** (a small piece of the graph). **Community summaries** = short digests of clusters of related nodes. The final answer includes a **proof path** = the chain of graph links that led to it, so you can verify instead of trusting.

> **One-line summary:** GraphRAG = extract entities/relations into a graph, retrieve the relevant subgraph, and answer with a citation path you can verify.

### Clear distinction: Which parts need a model?

Signpost: this table shows which framework parts need an AI model and which are plain code — that decides your cost and infrastructure.

| Part | Needs a model? | Description |
|------|-----------|-------|
| **Vector Search** (Module 01) | ✅ Needs an **embedding model** | Turns text into vectors for comparison |
| **BM25 Search** (Module 01) | ❌ Not needed | Pure math, counts keywords |
| **Generate Answer** (Module 05) | ✅ Needs an **LLM** | gemma3:12b, GPT-4o, Claude... |
| **Prompt Building** (Module 05) | ❌ Not needed | Just text arrangement |
| **Workflow** (Module 07) | ❌ Not needed | Just orchestration logic |
| **CI/CD Automation** (Module 10) | ❌ Not needed | GitHub Actions, scripts |

How to read it: ✅ = you pay for (or host) a model; ❌ = plain code, runs free. For example, Vector Search needs an **embedding model** (a smaller, cheaper model that converts text to vectors); BM25 is just a formula.

### The 2 model types you need

Signpost: you only ever need two kinds of models — one to search with, one to answer with.

| Type | Role | Local (free) | API (paid) |
|------|---------|-------------------|---------------|
| **Embedding model** | Turns text into vectors (used for search) | `nomic-embed-text` via Ollama | OpenAI text-embedding-3-small |
| **LLM** (Large Language Model) | Generates answers | `gemma3:12b`, `llama3`, `qwen2.5` via Ollama | GPT-4o, Claude, Gemini |

How to read it: each row = one model type, its job, and where to get it. "Local (free)" = runs on your machine via Ollama; "API (paid)" = you pay per use to a provider.

### In short

- **~60% of the framework** = pure code, no model needed (search, workflow, orchestration)
- **~40% of the framework** = needs a model (embedding + generation)

The framework teaches you **how to assemble the pieces** — the model is just one piece of the puzzle. You can use **Ollama running locally for free** or a **paid API** depending on your budget.

> **One-line summary:** The model is one replaceable piece — most of the framework is free plain code, and you only need two model types: one embedding (search) and one LLM (answer).

---

## 🚀 After You Finish — Real Projects

Signpost: this section lists 20 concrete projects you can build with the framework, grouped by difficulty — so you turn theory into a portfolio.

With **11 modules** covering everything from Retrieval, Context, Memory, Planning, Prompting, Tooling, Workflow, Task Management, Multi-Agent, and Automation to Evaluation — you can build **dozens of real projects**. Below are **20 projects** organized by level and domain.

How to read each project card: **Description** = what it is; **Tech Stack** = the tools used; **Build time** = realistic effort; **Modules applied** = which framework modules teach the needed skills; **Features** = how it works; **Result** = what you get at the end.

---

### 🟢 Beginner Level — Start Right Away (Modules 01-05)

Signpost: five small projects using only the first five modules. Jargon used in this level: **CLI** = command-line interface — you type commands in a terminal, no graphical UI. **Chunking** = splitting long documents into small pieces before storing, because embeddings work best on small text. **FastAPI** = a Python framework for building web APIs quickly. **Webhook** = a URL that a service calls when something happens (e.g., GitHub calls your server when a PR opens). **Re-ranking** = a second-pass model reorders search hits by true relevance.

> **One-line summary:** Five starter projects — a personal knowledge base, a document chatbot, hybrid search, structured data, and a code review bot — all buildable in days with modules 01-05.

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

In plain words: **PKB** = your private searchable second brain. The flow line means: import notes → cut them into chunks → convert each chunk to a vector → search by meaning from the terminal.

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

Glossary: **hallucination** = the model confidently making things up; grounding answers in your documents is the main fix.

#### 3. 🔍 Hybrid Search Engine

- **Description**: A search engine combining semantic + keyword search with re-ranking
- **Tech Stack**: BM25 (Python) + FAISS + Cross-encoder reranker
- **⏱️ Build time**: 3-5 days (BM25 + Vector), 1 week (add reranking + optimization)
- **Modules applied**:
  - Module 01 — Vector Search, BM25, Hybrid Search, Re-ranking
  - Module 02 — Context Compression (summarizing results)
- **Features**: Query → Parallel BM25 + Vector → Merge → Rerank → Top-K
- **Result**: 40% more accurate search than using BM25 or Vector alone

Glossary: **Cross-encoder reranker** = a slower but smarter model that re-reads the top results and re-scores them against your query. **Top-K** = keep the K best hits (e.g., top 10).

#### 4. 📊 Markdown to Structured Data

- **Description**: Automatically convert Markdown documents into a structured database
- **Tech Stack**: LLM (gemma3:12b) + SQLite + Python
- **⏱️ Build time**: 1-2 days
- **Modules applied**:
  - Module 05 — Prompt Builder, Output Format Control (JSON/Table)
  - Module 03 — Report Generation, Write-back Memory
- **Features**: Input Markdown docs → LLM extracts entities/relations → Store as structured data
- **Result**: Automatically create a database from docs, supporting structured queries

Glossary: **SQLite** = a small self-contained database stored in one file. **Structured queries** = asking the data in a precise way, e.g., `SELECT` in SQL.

#### 5. 🧪 AI Code Review Bot (Simple)

- **Description**: A bot that reviews code when you push to GitHub and suggests improvements
- **Tech Stack**: GitHub Webhooks + LLM + Python
- **⏱️ Build time**: 2-3 days
- **Modules applied**:
  - Module 05 — Prompt Builder (review prompts), Guardrails (safety)
  - Module 10 — Git Automation (hooks, webhooks)
- **Features**: PR created → Bot reviews → Comments suggestions on the PR
- **Result**: Automated code review, catch bugs early, suggest best practices

Glossary: **PR** = Pull Request — a proposed change waiting to be merged into the main code. **Push** = send your commits to the shared remote repo.

---

### 🟢 Daily-Use Level — Useful Every Day (Modules 01-10)

> **These are small projects that can be built in 1-3 days, but are used EVERY DAY at work.**

Signpost: eight small helpers that pay back daily. Jargon in this level: **cron** = the classic time scheduler ("run daily at 9 AM"). **git log --since="today"** = list only today's commits. **Jira/Trello/Notion** = popular task-tracking apps. **diff** = the line-by-line list of code changes. **git diff --cached** = show exactly what's staged for the next commit. **git hook** = a script Git runs automatically at moments like commit time. **AST parser** = a tool that reads code into a structural tree (AST = Abstract Syntax Tree), so the agent understands code shape, not just text. **WebSocket** = a connection that stays open for live two-way messaging.

> **One-line summary:** Eight small tools (work log, standup, email drafter, code Q&A, changelog, meeting notes, commit messages, review checklists) that together save 1-2 hours a day.

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

How to read the flow: each `→` = the next step, triggered by **cron** at 6 PM. **Slack** = the team chat app; **Sprint Planning** = the meeting where the team picks work for the next sprint (a 1-2 week work cycle); **blocker** = something stopping progress.

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

Glossary: **standup** = the short daily team status meeting; **backlog** = the pool of not-yet-started tasks; **pair programming** = two developers coding together at one screen.

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

Glossary: **action items** = concrete things someone must do next; **email thread** = the whole back-and-forth conversation kept as context.

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

Glossary: **codebase** = all the source code of a project; **call graph** = a map of "who calls whom" between functions; **onboarding** = getting up to speed on a new project/job.

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

Glossary: **merged** = the PR's changes are now part of the main branch; **changelog** = the user-facing list of what changed in each release; **fuzzy matching** = matching even with typos or partial words.

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

Glossary: **transcript** = the written text of a recording; **assignee** = the person responsible for a task; **deadline** = the due date.

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

Glossary: **commit** = a saved snapshot of changes; **staged** = marked to be included in the next commit. **Conventional Commits** = the standard format `type(scope): summary`, e.g., `feat(auth): ...` where `feat` = new feature. **OAuth2** = the standard "login with Google/GitHub" protocol; **refresh token** = the credential used to renew access without re-login.

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

Glossary: **DB migration** = a script that changes the database structure (add a table/column); **reversible** = it can be undone cleanly; **backward compatible** = old code/users keep working; **index** = a database structure that makes lookups fast; **seed data** = the initial sample data a fresh database is filled with.

---

### 📊 Daily-Use Projects Summary

How to read it: each row = one daily-use project, how often you'd use it, effort to build, and time it gives back. For example, #6 (Auto Daily Work Log) = used every day, 2-3 days to build, saves 15-20 minutes daily.

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

> **One-line summary:** Eight small daily-use tools take 1-2 weeks total to build and give back 1-2 hours every day.

### 🟡 Intermediate Level — Needs More Modules (Modules 01-08)

Signpost: five bigger, production-grade systems. Jargon in this level: **production-grade** = reliable enough for real users, not a demo. **MVP** = Minimum Viable Product — the smallest version that works. **Cache** = keep a copy of an expensive result to reuse (Redis = a very fast in-memory store often used for this). **Prometheus** = collects system metrics; **Grafana** = draws them as dashboards. **Escalation** = handing a case to a human when the bot can't solve it. **Ticket** = a tracked support request. **AST Parser** = reads code into a structure tree (see above). **Session** = one user's ongoing interaction, with its own memory.

> **One-line summary:** Five mid-size systems — enterprise RAG, support agent, doc generator, task manager, memory chatbot — combining 4-5 modules each and taking 2-6 weeks.

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

Glossary: **Qdrant** = a dedicated vector database (like ChromaDB but built to scale). **Ingestion** = pulling documents in and preparing them (chunk, embed, store). **Latency** = the delay before the answer arrives; `<200ms` = under a fifth of a second.

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

Glossary: **FAQ** = Frequently Asked Questions list; **qualification** = figuring out what category/severity the problem is; **resolution** = solving it.

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

Glossary: **API signature** = a function's public shape — name, parameters, return type.

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

Glossary: **fact store** = a table of small factual statements ("user prefers Vietnamese"), separate from chat history.

---

### 🔴 Advanced Level — Complex Systems (Modules 04-11)

Signpost: five systems where agents write code, run infrastructure, or do multi-agent work — these carry real risk, so safety modules matter. Jargon in this level: **MCP Servers** = tool services the agent calls via the MCP protocol (see above). **Message Queue** (Redis/RabbitMQ) = a post-office buffer: agents drop messages in, others pick them up later. **Kubernetes (K8s)** = an orchestrator that runs containers across many machines. **Rollback** = revert to the previous working version. **Anomaly** = a value that deviates sharply from normal (e.g., traffic 10x at 3 AM). **CVE** = a published ID for a known security vulnerability (CVE-2024-1234); the CVE database = the public list of these.

> **One-line summary:** Five advanced systems — a coding agent, an agent team, self-healing CI/CD, analytics, and a research assistant — where error recovery, evaluation, and safety modules become mandatory.

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

Glossary: **Cline/Cursor** = existing AI coding assistants — this project builds your own equivalent. **Terminal** = the command-line shell where commands run.

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

Glossary: **Architect** = the agent that decides the technical design (what components, what patterns).

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

Glossary: **deploy** = release the new version to users; **downtime** = time the system is unavailable.

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

Glossary: **Pandas** = the standard Python library for data tables; **insight** = a finding worth acting on ("sales drop every Friday").

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

Glossary: **citation tracking** = recording exactly which source each claim came from; **faithfulness** = the answer says only what the sources actually support.

---

### 🟣 Expert Level — Integrated Systems (All Modules)

Signpost: four moonshot systems that combine nearly everything. Jargon in this level: **low-code/no-code** = building software with little or no hand-written code. **Spaced repetition** = reviewing material at growing intervals (1 day, 3 days, 1 week…) to lock it into memory. **SAST** = Static Application Security Testing — scanning source code for vulnerabilities without running it. **Compliance** = meeting legal/industry rules (e.g., GDPR). **Terraform** = the main Infrastructure-as-Code tool: you describe servers in config files and it creates them. **MVP** = smallest working version (see above).

> **One-line summary:** Four expert systems — an autonomous dev platform, adaptive learning, security audit, and cross-platform app generation — integrating all 11 modules.

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

Glossary: **auth** = the login/permission part of an app. "Full stack" = everything from web UI to servers to deployment.

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

Glossary: **mastery** = how well a topic is learned; **gap** = a topic not yet understood; **retention** = how much stays in memory over time.

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

Glossary: **vulnerability** = a weakness an attacker could exploit (e.g., SQL injection = slipping database commands through user input); **audit** = a systematic check.

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

Glossary: **spec** = specification — the written description of what to build; **frontend** = the user-facing part; **backend** = the server part; **API** = the interface the two talk through.

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

Glossary: **IaC** = Infrastructure-as-Code — describing servers/config as reviewable code files instead of clicking in a console. **Provisioning** = creating the infrastructure. **Multi-cloud** = works across AWS, GCP, and Azure (the three big cloud providers).

---

### 📊 Projects & Modules Overview

How to read it: each row = one project, its difficulty level, the modules it uses, and a star rating for complexity. For example, #1 (Personal Knowledge Base) = beginner level, uses modules 01/03/06, complexity 2 stars.

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

Note: project numbers here (1-20) are renumbered from the detailed sections above (which run 1-28 including daily-use tools) — match by project name, not number.

> **One-line summary:** All 20 projects at a glance — difficulty, modules used, and complexity stars — to pick your next build.

### 🗺️ Module → Project Matrix

> How many projects each module serves — showing the value of each knowledge area.

How to read it: each row = one module, how many of the 20 projects use it, and two example projects. For example, module 01 (Retrieve Memory & Knowledge) appears in 15 of 20 projects — it's the most reused skill.

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

> **One-line summary:** Modules 01 (retrieval), 02 (context), and 05 (prompting) are used by nearly every project — master those first for the highest return.

---

### 📈 Hands-on Roadmap by Level

Signpost: this schedule puts the projects on a ~6-month calendar, level by level.

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

How to read it: each block = a level; `Weeks X-Y` = when to build which project (numbers match the Projects & Modules Overview table above); `→ Learn:` = the skills that project exercises. **Fusion** = merging results from two search methods into one ranked list.

> **One-line summary:** A realistic 6-month schedule: 6 weeks of basics, 6 weeks of intermediate, 8 weeks of advanced, then one big expert capstone.

---

### 💼 Career Opportunities & Salary

Signpost: this table maps framework skills to job titles and pay, so you know what each module is worth on the market.

| Role | Core skills from the framework | VN salary (2025) | Global salary |
|---------|------------------------------|--------------------|--------------------|
| **AI Engineer** | Modules 01-07: RAG, Agent, Workflow | 30-80M/month | $100K-200K/year |
| **MLOps / AI Platform Engineer** | Modules 07, 10, 11: Pipeline, CI/CD, Monitoring | 25-60M/month | $120K-180K/year |
| **Backend Developer (AI-focused)** | Modules 01-06: RAG integration, API design | 20-50M/month | $80K-150K/year |
| **DevOps/SRE with AI** | Modules 07, 10, 11: Self-healing, Automation | 25-60M/month | $100K-160K/year |
| **Tech Lead (AI Products)** | Modules 04, 08, 09: Planning, Multi-agent orchestration | 40-100M/month | $150K-250K/year |
| **AI Freelancer / Consultant** | The whole framework: Build custom AI solutions | 50-200M/month (project-based) | $100-300/hour |

How to read it: each row = a job title, the framework modules that prepare you for it, and salary ranges (VN = Vietnam, in millions of VND per month; Global = USD). Glossary: **MLOps** = Machine Learning Operations — deploying and monitoring models in production. **DevOps** = engineering the build/deploy pipeline itself.

> **One-line summary:** Retrieval + context + prompting (01-05) already open backend/AI roles; adding workflow, automation, and evaluation (07/10/11) unlocks MLOps and lead-level pay.

---

### 💡 Tips to Get Started

Signpost: four practical habits for starting without drowning — order matters more than speed.

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

How to read it: `├──` and `└──` = bullet points under each tip. Glossary: **portfolio** = a public collection of your work employers can see; **SRS/PRD** = Software Requirements Specification / Product Requirements Document — the written specs of what to build.

> **One-line summary:** Start with one small real problem, build it publicly, then combine small wins into bigger systems.

---

## 💡 Real Examples

Signpost: two fully worked examples — one RAG pipeline with runnable code, one multi-agent flow as a diagram.

### Example 1: Building a simple RAG Pipeline

<details>
<summary><b>Example 1: Building a simple RAG Pipeline (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/02-example-1-building-a-simple-rag-pipeline.py`](examples/02-example-1-building-a-simple-rag-pipeline.py)

</details>

In plain words: this script shows the full RAG loop end-to-end — chunk documents, embed each chunk, store vectors, embed the question, fetch the nearest chunks, and hand them to the LLM with the question. Read it alongside modules 01, 02, and 05.

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

How to read it: each box = one agent with its job in parentheses; `───►` = "hands work to". The Planner analyzes the request, the Coder writes code, the Reviewer checks it, the Tester verifies, and the Deployer releases. All three left-side agents eventually hand off to the Deployer.

> **One-line summary:** A multi-agent workflow is an assembly line: Planner → Coder → Reviewer → Tester → Deployer, each doing one job and passing work on.

---

## 📊 Knowledge Summary

Signpost: this final table compresses the whole framework into one skill ladder — read a row left to right to see how one skill matures from basic to advanced.

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

How to read it: each row = one skill; the three columns = growing mastery. For example, **Search**: level 1 = count keywords (BM25); level 2 = match meaning with vectors; level 3 = merge both and re-rank. **Concatenation** = simply gluing text together end to end.

> **One-line summary:** Every skill in this framework matures through 3 levels — from manual/basic, to structured, to self-correcting and automated.

---

## 🔗 Useful Links

Signpost: the six tools most referenced in this guide, with what each one is for.

| Source | Description |
|-------|-------|
| [Ollama](https://ollama.com) | Run LLM & Embedding locally |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector search library |
| [ChromaDB](https://www.trychroma.com) | Embedded vector database |
| [MCP Protocol](https://modelcontextprotocol.io) | Model Context Protocol |
| [LangChain](https://langchain.com) | Framework for LLM applications |
| [LlamaIndex](https://www.llamaindex.ai) | Data framework for LLMs |

How to read it: each row = a tool and its one-line job. Ollama runs the models; FAISS/ChromaDB store and search vectors; MCP is the agent↔tool protocol; LangChain/LlamaIndex are higher-level libraries that wrap many of these pieces for you.

> **One-line summary:** Six tools cover the whole stack: Ollama for models, FAISS/ChromaDB for vectors, MCP for tools, LangChain/LlamaIndex for glue.

---

> **Note**: Each module in the framework has a detailed README.md with code examples. You can read each module individually or learn along the roadmap from Phase 1 to Phase 6.
