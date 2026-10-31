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

You have read `HARNESS_ENGINEERING.md` — you know the 7 parts: fetch memory, build context, update memory, make a plan, build prompts, pick tools, run the workflow. Now you want to **write real code** for a harness, not just learn the ideas.

You have two choices: write all the setup yourself (LLM calls, tool routing, memory, retries...), or use a ready-made framework that has already solved most of it for you.

> **Option 4 — LangChain / LlamaIndex (Professional framework)** — quoted from HARNESS_ENGINEERING.md

**LangChain / LangGraph** is the standard toolkit for turning harness ideas into code: it gives you tool-calling, memory, RAG, and prompt templates right away, and — with LangGraph — lets you shape the harness flow as a **stateful graph** (fetch → build → act → update → repeat).

### Why LangChain Matters?

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

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Production-ready** | Tool calling, retries, streaming, and tracing work out of the box |
| 2 | **Stateful graphs (LangGraph)** | Shape the harness as a graph with state — much like the loop idea |
| 3 | **Broad ecosystem** | 700+ ready integrations, from vector DBs to MCP |
| 4 | **Sample code ready** | HARNESS_ENGINEERING.md already includes a TypeScript example |

### Relationship to the Harness

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

## Overview

### LangChain (Core)

The base library: LLM wrappers, chains, tools, memory, retrievers, and prompts.

> 📄 **Example code:** [`examples/01-langchain-core.ts`](examples/01-langchain-core.ts)

### LangGraph (Orchestration)

Adds the **stateful graph** layer — each step is a harness part, with branches and loops when needed.

> 📄 **Example code:** [`examples/02-langgraph-orchestration.py`](examples/02-langgraph-orchestration.py)

This follows the `loop/` idea closely — the agent does not stop after one LLM call, it **keeps going** until the task is finished.

## Learning Roadmap (Directory Structure)

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

| If you want to... | Read |
|-------------------|------|
| Understand the 7 harness components | [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) |
| Tool design & MCP | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Agent loops | [loop/](../../loop/) |

## Real-World Case Studies

### 1. RAG Harness with LangChain

```
harness/01-retrieve → Chroma retriever (see tools/vector-db/)
harness/02-build    → ContextualCompressionRetriever (compresses context)
harness/05-prompt   → ChatPromptTemplate with the retrieved docs
harness/06-tool     → ToolNode calls web_search, query_db
```

### 2. Agent Loop (LangGraph)

> 📄 **Example code:** [`examples/03-2-agent-loop-langgraph.py`](examples/03-2-agent-loop-langgraph.py)

## Reference Materials

- **LangChain**: https://langchain.com
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Academy**: https://academy.langchain.com
- **Blog**: https://blog.langchain.dev
- **Discord**: https://langchain.ai/discord

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (sample code)
- [tools/vector-db](../vector-db/) — RAG retrievers
- [tools/observability](../observability/) — LangSmith tracing
- [tools/evaluation](../evaluation/) — LangSmith evals, Ragas

---

> **"A harness is just a graph — LangGraph gives you the nodes and edges."**

---

## ⚠️ Update 10/2026: LangChain 1.0 (10/2025)

LangChain 1.0 released 10/2025 with major breaking changes:
- `create_agent` is the primary API (replaces many chain utilities)
- LangGraph integrated natively for stateful workflows
- LCEL still works but now recommended via the agents layer
- New package structure: `langchain` core separated from `langchain-community`
- Python 3.10+ required (3.9 EOL October 2025)

Migration: https://docs.langchain.com/oss/python/langchain/migration

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — langchain*
