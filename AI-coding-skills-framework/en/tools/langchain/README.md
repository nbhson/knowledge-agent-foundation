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

You've read `HARNESS_ENGINEERING.md` — you understand the 7 components: retrieve memory, build context, update memory, plan, prompt builder, tool decision, workflow. You want to **write real code** for a harness, not just understand the theory.

You have two options: write all the orchestration from scratch (LLM calls, tool routing, memory, retry...), or use a professional framework that has already solved 80% of that problem.

> **Option 4 — LangChain / LlamaIndex (Professional framework)** — quoted from HARNESS_ENGINEERING.md

**LangChain / LangGraph** is the standard framework for materializing harness engineering: it provides tool-calling, memory, RAG, prompt templates out of the box, and — with LangGraph — the ability to model the harness flow as a **stateful graph** (retrieve → build → act → update → repeat).

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
| 1 | **Production-ready** | Tool calling, retries, streaming, tracing available out of the box |
| 2 | **Stateful graphs (LangGraph)** | Model the harness as a graph with state — exactly the loop philosophy |
| 3 | **Broad ecosystem** | 700+ integrations, from vector DBs to MCP |
| 4 | **Sample code ready** | HARNESS_ENGINEERING.md already has a TypeScript snippet |

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

The base library: LLM wrappers, chains, tools, memory, retrievers, prompts.

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

Adds the **stateful graph** layer — each node is a harness component, with conditional branching and loops.

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
graph.add_edge("tools", "agent")              # loop — like loop/
```

This is exactly the `loop/` philosophy — the agent doesn't end after one LLM call, it **repeats** until the task is complete.

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

```python
# Agent action loop — like loop/ but inside a graph
while True:
    action = agent.invoke(state)       # harness/04 plan
    if action.type == "finish": break  # answer the user
    result = execute_tool(action)      # harness/06 execute
    state = update_memory(result)      # harness/03 update
```

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

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — langchain*
