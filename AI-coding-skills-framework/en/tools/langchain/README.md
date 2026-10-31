# 🦜️🔗 LangChain / LangGraph — Framework for Building a Harness

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why LangChain Matters?](#why-langchain-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview](#overview)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section explains the problem LangChain solves: turning harness ideas into working code without writing every piece yourself.

You have read `HARNESS_ENGINEERING.md` — you know the 7 parts: fetch memory, build context, update memory, make a plan, build prompts, pick tools, run the workflow. Now you want to **write real code** for a harness, not just learn the ideas.

You have two choices: write all the setup yourself (LLM calls, tool routing, memory, retries...), or use a ready-made framework that has already solved most of it for you. An LLM call = one request to a language model; tool routing = deciding which tool handles which request; retries = re-running a failed call automatically.

> **Option 4 — LangChain / LlamaIndex (Professional framework)** — quoted from HARNESS_ENGINEERING.md

**LangChain / LangGraph** is the standard toolkit for turning harness ideas into code: it gives you tool-calling, memory, RAG, and prompt templates right away, and — with LangGraph — lets you shape the harness flow as a **stateful graph** (fetch → build → act → update → repeat). Plain glosses: RAG = retrieval-augmented generation, i.e. searching your documents and feeding the results to the model. Prompt template = a fill-in-the-blanks prompt. Stateful graph = a flowchart whose nodes remember shared data between steps.

> **One-line summary:** LangChain hands you pre-built pieces (tools, memory, prompts) so you code a harness instead of a framework.

### Why LangChain Matters?

This section maps harness ideas to concrete LangChain modules — proof the two vocabularies match up.

> **"Every harness concept in this repo has a LangChain module that implements it."**

How to read this table: the left column is a harness concept (an idea from this repo's docs); the right column is the LangChain name for the code that implements it. For example, "LLM abstraction" means one interface for calling any model — `ChatOpenAI` for OpenAI models, `ChatAnthropic` for Anthropic's.

| Harness Concept | LangChain Module |
|-----------------|------------------|
| LLM abstraction | `ChatOpenAI`, `ChatAnthropic`... |
| Tool calling | `@langchain/core/tools`, `DynamicStructuredTool` |
| Memory (01/03) | `MemorySaver`, `InMemoryChatMessageHistory` |
| Context building (02) | `Retriever`, `DocumentCompressor`, `ContextualCompressionRetriever` |
| Prompt builder (05) | `PromptTemplate`, `ChatPromptTemplate` |
| Tool decision (06) | `create_tool_calling_agent`, `ToolNode` |
| Workflow (07) | `StateGraph`, `langgraph.prebuilt.ToolNode` |

Plain glosses: `DynamicStructuredTool` = a tool you define with typed inputs (like a function signature). `Retriever` = a component that fetches relevant documents. `DocumentCompressor` = shrinks the fetched documents to only the useful parts. `StateGraph` = the LangGraph flowchart with shared state.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Production-ready** | Tool calling, retries, streaming, and tracing work out of the box |
| 2 | **Stateful graphs (LangGraph)** | Shape the harness as a graph with state — much like the loop idea |
| 3 | **Broad ecosystem** | 700+ ready integrations, from vector DBs to MCP |
| 4 | **Sample code ready** | HARNESS_ENGINEERING.md already includes a TypeScript example |

How to read it: **#** is a row number; **Reason** is the label; **Explanation** says why in one line. For example, "700+ integrations" = ready-made connectors to 700+ external systems, including vector databases (searchable embedding storage) and MCP (the Model Context Protocol for tools).

> **One-line summary:** LangChain matters because each harness idea already has a battle-tested module you can import.

### Relationship to the Harness

This diagram shows which harness component each LangChain piece replaces. Read `→` as "is implemented by".

```
┌──────────────────────────────────────────────────────────────┐
│  LANGCHAIN MAP VS HARNESS COMPONENTS                         │
│                                                              │
│  harness/01-retrieve-memory-knowledge → Retrievers, Memory   │
│  harness/02-build-context            → DocumentCompressor    │
│  harness/03-update-memory-store      → MemorySaver/Store     │
│  harness/04-plan-decompose-task      → Planner nodes         │
│  harness/05-prompt-builder           → PromptTemplates       │
│  harness/06-decide-tools-mcp         → ToolNode, DynamicTools│
│  harness/07-workflow                 → StateGraph            │
└──────────────────────────────────────────────────────────────┘
```

> **One-line summary:** Each of the 7 harness components has a LangChain equivalent — the diagram is your translation dictionary.

## Overview

> **One-line summary:** Two layers: LangChain core (the pieces) and LangGraph (the graph that wires them together).

### LangChain (Core)

This subsection describes the base library — what you get before adding LangGraph.

The base library: LLM wrappers, chains, tools, memory, retrievers, and prompts. "Chains" = pipelines that pass output from one step to the next, like an assembly line.

> 📄 **Example code:** [`examples/01-langchain-core.ts`](examples/01-langchain-core.ts)

> **One-line summary:** LangChain core = the toolbox: models, chains, tools, memory, retrievers, prompts.

### LangGraph (Orchestration)

This subsection describes the layer that turns steps into a graph with loops and branches.

Adds the **stateful graph** layer — each step is a harness part, with branches and loops when needed. "Stateful" = the graph keeps shared data (the state) as it moves from node to node.

> 📄 **Example code:** [`examples/02-langgraph-orchestration.py`](examples/02-langgraph-orchestration.py)

This follows the `loop/` idea closely — the agent does not stop after one LLM call, it **keeps going** until the task is finished.

> **One-line summary:** LangGraph = the loop: the graph keeps calling tools and updating state until the job is done.

## Learning Roadmap (Directory Structure)

> **One-line summary:** This section maps the folder layout and a step-by-step learning path.

This tree shows the folder layout; `(TODO)` means not written yet.

```
langchain/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Models, prompts, chains, agents, graph state
├── 02-setup/            ← (TODO) Installing @langchain/langgraph, API keys
├── 03-patterns/         ← (TODO) RAG, agent loop, multi-agent supervisor
├── 04-savings/          ← (TODO) Token usage tracking, cost optimization
└── 05-troubleshooting/  ← (TODO) Graph cycles, tool errors, context overflow
```

### Recommended Roadmap

A suggested learning order; read `↓` as "then do this next". "MCP adapters" = connectors to MCP servers (external tool providers via the Model Context Protocol).

```
Step 1: Read HARNESS_ENGINEERING.md section 9.1 — sample TS code is provided
   ↓
Step 2: Code a simple harness with LangChain core (llm + tools + memory)
   ↓
Step 3: Move to LangGraph — StateGraph modeling the 7 components
   ↓
Step 4: Add ToolNode + MCP adapters (harness/06)
   ↓
Step 5: Add tracing with LangSmith (see tools/observability/)
```

This table maps goals to docs. How to read it: left column = what you want to learn; right column = where to read it.

| If you want to... | Read |
|-------------------|------|
| Understand the 7 harness components | [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) |
| Tool design & MCP | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Agent loops | [loop/](../../loop/) |

> **One-line summary:** Learn in this order: sample code → core pieces → StateGraph → tools/MCP → tracing.

## Real-World Case Studies

Two worked scenarios showing the pieces assembled into a working harness.

> **One-line summary:** Two assemblies — a RAG pipeline and an agent loop — each mapped to harness slots.

### 1. RAG Harness with LangChain

This example shows which LangChain piece fills each harness slot in a RAG pipeline. Read `→` as "is handled by". For example, `ContextualCompressionRetriever` = a retriever that also trims fetched documents down to the relevant sentences.

```
harness/01-retrieve → Chroma retriever (see tools/vector-db/)
harness/02-build    → ContextualCompressionRetriever (compresses context)
harness/05-prompt   → ChatPromptTemplate with the retrieved docs
harness/06-tool     → ToolNode calls web_search, query_db
```

> **One-line summary:** A RAG harness in LangChain = retriever + compressor + prompt template + tool node, one per harness slot.

### 2. Agent Loop (LangGraph)

What this shows: an agent that loops through think → call tool → observe until the task is done — the LangGraph version of the loop idea.

> 📄 **Example code:** [`examples/03-2-agent-loop-langgraph.py`](examples/03-2-agent-loop-langgraph.py)

> **One-line summary:** LangGraph's agent loop is the "keep going until done" pattern, expressed as a graph.

## Reference Materials

Official LangChain/LangGraph resources for deeper reading.

> **One-line summary:** Official site, LangGraph docs, academy, blog, and community chat.

- **LangChain**: https://langchain.com
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Academy**: https://academy.langchain.com
- **Blog**: https://blog.langchain.dev
- **Discord**: https://langchain.ai/discord

### Links to Other Branches

Related pages in this repo — follow them for the neighboring topic.

> **One-line summary:** Neighboring topics: the harness doc itself, plus retrievers, tracing, and evaluation tools.

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (sample code)
- [tools/vector-db](../vector-db/) — RAG retrievers
- [tools/observability](../observability/) — LangSmith tracing
- [tools/evaluation](../evaluation/) — LangSmith evals, Ragas

---

> **"A harness is just a graph — LangGraph gives you the nodes and edges."**

---

## ⚠️ Update 10/2026: LangChain 1.0 (10/2025)

This section lists the breaking changes in LangChain 1.0, so old tutorials don't mislead you. "Breaking changes" = changes that make old code stop working.

LangChain 1.0 released 10/2025 with major breaking changes:
- `create_agent` is the primary API (replaces many chain utilities) — one function that builds a full agent for you
- LangGraph integrated natively for stateful workflows — no separate install wiring needed
- LCEL still works but now recommended via the agents layer — LCEL = LangChain Expression Language, the `|` pipe syntax for chaining steps
- New package structure: `langchain` core separated from `langchain-community` — stable pieces split from third-party ones
- Python 3.10+ required (3.9 EOL October 2025) — EOL = end of life, no more security fixes

> **One-line summary:** LangChain 1.0 makes `create_agent` the main API and requires Python 3.10+; follow the migration guide before upgrading.

Migration: https://docs.langchain.com/oss/python/langchain/migration

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — langchain*
