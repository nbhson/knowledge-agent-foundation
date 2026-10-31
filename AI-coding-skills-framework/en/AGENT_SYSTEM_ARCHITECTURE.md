# Building an Agent System Architecture — The Complete 2026 Guide

> **Purpose:** This document answers the single most important question — **"How do you build a complete agent system?"** — building on the foundational knowledge already in this repo (`HARNESS_ENGINEERING.md`, `AI_AGENT_FRAMEWORK.md`, `GRAPH_ENGINEERING.md`) and the latest official research and documentation as of **10/2026**.
>
> **Primary sources (directly verified 10/2026):**
> - [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) (12/2024, updated 2026)
> - [Effective Harnesses for Long-Running Agents — Anthropic](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) (11/2025)
> - [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (09/2025)
> - [How we built our multi-agent research system — Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) (06/2025)
> - [Agent Skills — Anthropic](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) (10/2025, open standard at [agentskills.io](https://agentskills.io) since 12/2025)
> - [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
> - [Model Context Protocol — MCP spec 2026-07-28](https://modelcontextprotocol.io/)
> - [A2A Protocol — Linux Foundation](https://a2a-protocol.org) (2026, joined the Agentic AI Foundation 08/2026)

**What this document explains:** how to assemble a complete agent system, layer by layer. This matters because architecture choices — not model choice — decide cost, speed, and safety.

---

## Table of Contents

- [1. The 2026 Big Picture](#1-the-2026-big-picture)
- [2. Workflow vs Agent vs Multi-Agent](#2-workflow-vs-agent-vs-multi-agent)
- [3. The Synthesized Architecture — 8 Layers](#3-the-synthesized-architecture--8-layers)
- [4. Production-Proven Architecture Patterns](#4-production-proven-architecture-patterns)
- [5. Comparing Agent Frameworks & SDKs](#5-comparing-agent-frameworks--sdks)
- [6. The Practical Build Process (Build Checklist)](#6-the-practical-build-process-build-checklist)
- [7. Connecting to the Existing Framework in This Repo](#7-connecting-to-the-existing-framework-in-this-repo)
- [8. References](#8-references)

> **One-line summary:** This guide shows how to build a full agent system in 8 layers — from picking models to safety and evaluation.

---

## 1. The 2026 Big Picture

**What this section explains:** the core idea everyone agrees on, and why architecture — not the model — is what you actually design.

All primary sources consistently affirm one critical insight:

> **Agent = LLM autonomously using tools in a loop.**
> This minimal definition is what the industry has converged on (Anthropic, Simon Willison):
> *"An agent is an LLM autonomously using tools in a loop."*

This means: **agent system architecture is NOT about choosing the best model**, but about designing the **loop + environment + controls** around the LLM (LLM = Large Language Model — the text model behind the agent, like Claude or GPT). Three pillars:

- **Loop** = the agent acts, checks the result, and acts again until the job is done — like a chef tasting and re-seasoning.
- **Environment** = the tools and files the agent can touch (its workshop).
- **Controls** = the rules and permissions that stop the agent from doing damage (its guardrails).

```
+------------------------------------------------------------------+
|                    AGENT = MODEL + HARNESS                        |
+------------------------------------------------------------------+
|                                                                   |
|   +---------------+           +-----------------------------+     |
|   |  MODEL (LLM)  |           |  HARNESS (you own this)       |  |
|   |  - thinking    |<-------->|  - tools                       |  |
|   |  - not        |           |  - context management          |  |
|   |    controllable|          |  - memory / persistence        |  |
|   +---------------+           |  - guardrails / permissions     |  |
|                                |  - orchestration / evaluation    |  |
|                                +------------------------------+     |
+------------------------------------------------------------------+
```

**Key research finding (Princeton NLP — SWE-agent):** Simply changing the ACI (Agent-Computer Interface — the "control panel" you hand the agent: how it lists files, reads errors, runs commands) boosted success rate by **+64%** without changing the model. As models become commoditized (2026: good models are everywhere and cheap), **the harness is the competitive moat** (moat = the lasting advantage competitors cannot easily copy — a well-tuned workshop vs a generic toolbox).

### Key Milestones (2024 -> 10/2026)

**What this table shows:** the key events that shaped how agents are built. How to read it: **Date** = when it happened; **Event** = what shipped or was published; **Architectural Significance** = why it matters for your design. For instance, "MCP launches" (12/2024) matters because it made connecting tools to agents a plug-and-play standard — like USB-C working with any device.

| Date | Event | Architectural Significance |
|------|-------|----------------------------|
| 12/2024 | Anthropic — *Building Effective Agents* | Standardized vocabulary: workflows vs agents, 5 workflow patterns |
| 12/2024 | MCP launches | Standardized agent-tool ("USB-C for AI") |
| 04/2025 | Google launches **A2A** protocol (50+ partners) + **Google ADK** (Agent Development Kit) | Standardized agent-agent; Google's open-source agent-building SDK |
| 06/2025 | Google donates A2A to Linux Foundation (IBM ACP merges into A2A 08/2025) | Standardized agent-agent |
| 06/2025 | Anthropic multi-agent research system | Orchestrator-worker production: +90.2% vs single agent (research eval) |
| 09/2025 | Context engineering becomes a core discipline | Compaction, note-taking, sub-agent = 3 context levers |
| 10/2025 | Agent Skills (open standard 12/2025) | Package expertise as SKILL.md — progressive disclosure |
| 11/2025 | Anthropic — long-running agent harness | Initializer agent + coding agent; feature-list JSON; incremental progress |
| 2025-2026 | OpenAI Agents SDK v2 (Swarm -> production) | Primitives: Agents, Handoffs, Guardrails, Sessions, Sandbox agents, Tracing |
| 07/2026 | MCP spec `2026-07-28` + MCP Apps | MCP ecosystem: build-once-integrate-everywhere |
| 08/2026 | A2A joins **Agentic AI Foundation** (Linux Foundation) | Standardized agent-agent: MCP (agent-tool) + A2A (agent-agent) are complementary |

> **One-line summary:** An agent = an LLM using tools in a loop — so your real work is designing the loop, the tools, and the controls, not picking a model.

---

## 2. Workflow vs Agent vs Multi-Agent

**What this section explains:** the first and most important choice — who steers the process, your code or the model.

This is the **#1 architectural decision** — getting it wrong here makes every layer below fail (Anthropic):

How to read this table: **Type** = the name of the pattern; **Definition** = what it is in one line; **Controlled by** = who makes the decisions; **When to use** = the situation that fits. For instance, a **Workflow** is like following a recipe — fixed steps written in code. An **Agent** is like a chef given a goal and free hands.

| Type | Definition | Controlled by | When to use |
|------|-----------|--------------|-------------|
| **Workflow** | LLM + tools running along a predefined code path | **Your code** | Fixed task, needs predictability and consistency |
| **Agent** | LLM **self-navigating** the process and tool usage in a loop | **The model** | Open-ended problem, unpredictable number of steps |
| **Multi-agent** | Multiple agents (each = LLM + tools in a loop) collaborating | Orchestrator + model | Breadth-first, parallelizable, exceeds 1 context window |

**Golden rules (don't skip these):**
1. Find the **simplest solution first** — many apps only need 1 optimized LLM call + retrieval (retrieval = looking up relevant documents before answering) + few-shot (few-shot = putting 2-3 worked examples in the prompt so the model copies the pattern).
2. Agentic systems **trade latency and cost for quality** — only add complexity when you can measure the benefit.
3. Workflow for well-defined tasks; agent for open-ended problems where the model needs to decide.

> **One-line summary:** Pick the simplest option that works — workflow when steps are fixed, agent when the model must decide, multi-agent only when one context window cannot hold the job.

---

## 3. The Synthesized Architecture — 8 Layers

**What this section explains:** the full blueprint. Imagine a building: the model is the ground floor, and each layer above adds one capability (tools, memory, safety, evaluation).

Synthesizing HARNESS_ENGINEERING (this repo) + 2025-2026 sources, a complete agent system consists of **8 stacked layers**:

```
+-------------------------------------------------------------------+
|  L8  EVALUATION & FEEDBACK   (evals, LLM-judge, regression)       |
+-------------------------------------------------------------------+
|  L7  SAFETY: Guardrails + Permissions + Approval + Sandbox        |
+-------------------------------------------------------------------+
|  L6  MEMORY: short-term / long-term / episodic / notes            |
+-------------------------------------------------------------------+
|  L5  ORCHESTRATION: single -> orchestrator-workers -> A2A mesh    |
+-------------------------------------------------------------------+
|  L4  TOOL ECOSYSTEM: MCP servers + Agent Skills + code execution  |
+-------------------------------------------------------------------+
|  L3  CONTEXT ENGINEERING: assembly, compaction, just-in-time      |
+-------------------------------------------------------------------+
|  L2  HARNESS: retrieval -> context -> plan -> prompt -> tools ->  |
|      workflow -> task -> eval -> memory write-back (+ 12-15)      |
+-------------------------------------------------------------------+
|  L1  MODEL: LLM (augmented: retrieval + tools + memory)           |
+-------------------------------------------------------------------+
```

> **One-line summary:** A complete agent system is 8 stacked layers, from the model at the bottom to evaluation at the top — the subsections below explain each layer.

### 3.1. Layer 1 — LLM with Augmentations

**What this section explains:** which model to use for which job. You don't need the "best" model — you need the right model for each task and budget.

This is the **physical foundation**. You don't need the "best" model — you need the right model:

How to read this table: **Model tier** = the model name; **Use case** = the job it fits; **Tradeoff** = what you gain and give up. For instance, Haiku 4.5 is the budget option for simple jobs like routing (routing = deciding which handler a request should go to), while Opus 4.5 is the expensive option for hard planning.

| Model tier | Use case | Tradeoff |
|------------|----------|----------|
| Haiku 4.5 | Routing, classification, guardrails | Cheap, fast, accurate for simple tasks |
| Sonnet 4.5 | Coding, multi-tool, mainstream agentic | Best cost/quality |
| Opus 4.5 | Orchestrator, complex reasoning, planning | Expensive but handles the hardest problems |
| o1/o3 (OpenAI) | Hard reasoning, eval judgment | Reasoning model, no CoT needed in prompt |

Note on the last row: **reasoning model** = a model that "thinks step by step" internally before answering, so you don't need to spell out the steps (CoT = Chain of Thought — asking the model to reason out loud in the prompt).

**Important note (Anthropic 09/2025):** The smarter the model -> the fewer "mandatory instructions" it needs -> the more autonomy it can handle. This changes harness design: weaker models need many hard-encoded rules and workflows; frontier models (frontier = the newest, most capable generation) only need good tools + guardrails.

**Augmentation = the model actively uses, not just passively receives input** (in other words, the model drives, not just reads):

- **Retrieval:** the model generates its own search queries -> calls retrieval -> uses the results
- **Tools:** the model decides which tool to use and when
- **Memory:** the model decides which information is worth keeping (write-back = saving results back to storage for later use)

> **One-line summary:** Match the model to the job and budget, and let the model actively drive retrieval, tools, and memory — smarter models need fewer handcuffs.

### 3.2. Layer 2 — Harness (7 components around the LLM)

**What this section explains:** the harness — the code you write around the model to feed it context, give it tools, and keep it safe. This is the part you own and control.

This is the most important part and is covered in detail in `HARNESS_ENGINEERING.md` (this repo). Here is only a summary mapping to 2025-2026 knowledge:

How to read this table: **Component** = one part of the harness; **New developments** = what changed in 2025-2026; **Related module** = the folder in this repo with the full details. For instance, "Tools" connects to `06-decide-tools-mcp/`, which explains how to pick and design tools.

| Component | New developments (2025-2026) | Related module |
|-----------|------------------------------|----------------|
| **Tools** | MCP standardization; Agent Skills for expertise; Tool descriptions = docstrings | `06-decide-tools-mcp/` |
| **Memory** | Note-taking (Claude Plays Pokemon); Memory tool (Anthropic Platform); Agent Skills | `01-retrieve`, `03-update`, `09-multi-agent` |
| **Context** | Compaction (tool-result clearing); 5 context levels; just-in-time vs pre-computed | `02-build-context/` |
| **Guardrails** | Guardrails run in parallel with execution (non-blocking); Risk tier at plan time; Tool guardrails | `05-prompt-builder/`, `15-approval-gates/` |
| **Feedback** | Eval-first development; LLM-judge with rubric; production tracing | `07-workflow/`, `11-evaluation/` |
| **Permissions** | Sandbox agents (OpenAI SDK); Manifest-defined files; RBAC + Approval gates | `06`, `12-sandbox`, `15-approval` |
| **Orchestration** | Orchestrator-worker; Handoffs; A2A; async vs sync tradeoffs | `07-workflow/`, `09-multi-agent/` |

> **One-line summary:** The harness is the 7-part frame around the model — tools, memory, context, guardrails, feedback, permissions, orchestration — and it is where most of your engineering time goes.

### 3.3. Layer 3 — Context Engineering

**What this section explains:** how to keep only useful information in the model's working memory. This matters because a cluttered memory makes the model dumber and slower.

**Context rot** is a fundamental phenomenon (Chroma research): the more tokens in the context window (context window = how much text the model can "hold in mind" at once, measured in tokens — tokens = word chunks), the lower the accurate-recall capability. In plain terms: the model's memory gets fuzzy as the conversation grows. LLMs have a finite **attention budget** (transformer structure: n^2 pairwise relationships for n tokens — doubling the text roughly quadruples the comparisons).

> Guiding principle: **"Find the smallest, highest-signal set of tokens that maximizes the odds of achieving the desired outcome."**

**Three levers for long-horizon tasks (Anthropic 09/2025)** — long-horizon = tasks that run so long they overflow the model's memory:

How to read this table: **Technique** = the name of the trick; **How it works** = what you actually do; **When to use** = the situation that fits. For instance, **Compaction** = summarizing the conversation and starting fresh with the summary — like replacing a full notebook with a one-page recap.

| Technique | How it works | When to use |
|-----------|-------------|-------------|
| **Compaction** | Summarize the conversation as it approaches the context limit -> restart with a fresh context carrying the summary | Tasks requiring lots of back-and-forth. Claude Code keeps architectural decisions + bugs + impl details, drops old tool outputs |
| **Structured note-taking** | The agent writes NOTES.md / todo-lists outside the context window -> reads them back later | Iterative development with clear milestones. Example: Claude Plays Pokemon maintains a map + strategy across thousands of steps |
| **Sub-agent architecture** | Sub-agents work deeply in their own clean context -> return a **1,000-2,000 token summary** | Complex research/analysis with parallelization. Lead agent synthesizes, sub-agents dig deep |

**Just-in-time vs Pre-computed retrieval:**

| Strategy | Pros | Cons |
|----------|------|------|
| Pre-computed (traditional RAG) | Fast, deterministic | Stale index, expensive to update, chunk-level link narrowing |
| Just-in-time (agentic search) | Fresh data, flexible, progressive disclosure | Slower, agent must know how to explore |
| **Hybrid (recommended)** | Fast + flexible. Claude Code: CLAUDE.md (static) + glob/grep (dynamic) | Requires well-designed tools so the agent doesn't wander |

Notes on the table: **Pre-computed** = you prepare an index of documents in advance, then search it (classic RAG — RAG = Retrieval-Augmented Generation, fetch documents first, then have the model answer from them). **Just-in-time** = the agent searches live, like a person opening files only when needed. **Hybrid** = load a small static briefing upfront (CLAUDE.md), then let the agent search for the rest with glob/grep (file-pattern search and text search).

> **One-line summary:** The model's attention is a limited budget — keep context small and high-signal with compaction, notes, and sub-agents, and prefer a hybrid retrieval strategy.

### 3.4. Layer 4 — Tool Ecosystem (MCP + Skills + Code Execution)

**What this section explains:** how to connect the agent to the outside world — data, APIs, and packaged expertise — without drowning it in tool descriptions.

#### MCP — "USB-C for AI" (spec `2026-07-28`)

MCP standardizes agent <-> external systems connection (data sources, tools, workflows). The nickname means one universal plug: like USB-C fits any device, any MCP-compatible agent can use any MCP server. Widely supported: Claude, ChatGPT, VS Code, Cursor, and many other clients.

```
Agent --MCP--> Tools / APIs / Resources
```

- MCP = standardization of **agent-to-tool**
- Client connects to MCP servers (local files, DB, search engines, APIs)
- Reduces repetitive development: build server once -> every MCP client can use it

#### Agent Skills (open standard since 12/2025)

**What this explains:** how to package expertise into files the agent can pick up on demand.

**Skill = directory with `SKILL.md`** (YAML frontmatter: `name` + `description` — a small header block listing the skill's name and what it's for) + accompanying resources. Think of it as a manual the agent opens only when relevant.

**Progressive disclosure at 3 levels** (progressive disclosure = show the table of contents first; open a chapter only when needed — this keeps the model's memory small):

1. Metadata (`name`, `description`) — pre-loaded into system prompt at startup, enough to know *when* to use the skill
2. Body of SKILL.md — only loaded when the agent decides the skill is relevant to the task
3. Additional files (`reference.md`, `forms.md`, scripts...) — agent navigates on demand

**Benefit:** context can be "unbounded" because the agent only loads what it needs. Skills can include **scripts** — agent runs code instead of generating tokens (sorting a list with code is much cheaper than using an LLM).

#### Code execution with MCP

Anthropic (11/2025): instead of exposing dozens of tools via MCP (each tool adds context + token overhead), give the agent the ability to **write code that calls MCP tools** — code runs in sandbox (sandbox = a sealed test environment where code can run without touching the real system), only the synthesized result comes back to context. In plain terms: instead of reading 10 manuals into memory, the agent reads them, does the work, and reports back one summary. Significantly reduces tokens + latency with multiple MCP servers.

#### Tool design (ACI — Agent-Computer Interface)

**What this explains:** how to design tools the agent uses reliably. Bad tool design is a top cause of agent failure.

Rules from Anthropic (SWE-bench):

- Invest in tool design **as much as HCI** (HCI = Human-Computer Interface design — designing for humans; here you design for the model with the same care) — tool descriptions are "docstrings for a junior dev"
- Format closer to natural text the model has been trained on (diff is harder than full-file rewrite; markdown is easier than JSON-escaped code)
- Enough tokens for the model to "think" before getting stuck by its own format
- **Poka-yoke** tools: design params to make mistakes hard (poka-yoke = mistake-proofing, like a SIM card that only fits one way; example: require absolute path after the agent changes directory)
- Test tools with many real inputs -> observe where the model makes mistakes -> iterate
- Avoid bloated toolset: if a human engineer can't decide which tool for scenario X, the agent can't either

> **One-line summary:** Give the agent few, well-described, mistake-proof tools — and let it run code to use MCP tools instead of loading every tool into memory.

### 3.5. Layer 5 — Agent Orchestration

**What this section explains:** how to arrange one or many agents to get work done — from a single agent to a team with a manager, to agents talking across companies.

#### Single agent -> Orchestrator-workers -> A2A

**Step 1 — Single agent:** LLM + tools in a loop, sufficient for the majority of use cases.

**Step 2 — Orchestrator-workers (most common multi-agent pattern):** one lead agent acts as a manager — it plans, spawns workers, and merges their results. "Spawn" = create and launch a subagent.

```
                  +-------------+
   User query --->| Lead agent  |---> plan + save plan to Memory
                  | (Opus)     |
                  +------+-----+
                         | spawn
          +--------------+---------------+
          v              v               v
      +--------+    +--------+    +--------+
      |Subagent|    |Subagent|    |Subagent|   <- parallel, own context
      |(Sonnet)|    |(Sonnet)|    |(Sonnet)|   <- interleaved thinking
      +----+---+    +----+---+    +----+---+
          +--------------+---------------+
                          v
                 Lead synthesizes
                          v
                 CitationAgent (if needed)
                          v
                 Answer + citations
```

**Real-world metrics (Anthropic 06/2025):** (eval = a standardized test set that measures whether the agent does its job well)
- Multi-agent (Opus lead + Sonnet subagents) **+90.2%** vs single-agent Opus 4 on research eval
- Token usage explains **80% of variance** in performance on BrowseComp (variance = the differences in results between runs; BrowseComp = a hard web-browsing benchmark)
- **Cost:** regular chat 1x; single agent ~4x; multi-agent ~15x tokens
- Multi-agent only worth it when: high-value task, parallelizable, exceeds 1 context window, many complex tools
- **NOT suitable:** coding (limited true parallelization), tasks needing tight shared context, real-time coordination (LLM still weak)

**Prompt engineering for multi-agent (8 Anthropic principles):**

1. **Think like your agents** — simulate each step, look at real failure modes
2. **Teach the orchestrator how to delegate** — each subtask needs: objective + output format + tool guidance + task boundaries. Vague instruction -> subagents duplicate work
3. **Scale effort to query complexity** — embed rules: fact-finding = 1 agent/3-10 tool calls; comparison = 2-4 subagents/10-15 calls; complex research = 10+ subagents
4. **Tool design and selection are critical** — clear heuristic: examine all tools first, match tool to intent, prefer specialized over generic
5. **Let agents improve themselves** — Claude 4 can rewrite tool descriptions; tool-testing agent helped reduce 40% task completion time
6. **Start wide, then narrow down** — prompt agents to resist the tendency to over-specify queries too early
7. **Guide the thinking process** — extended thinking = controllable scratchpad (the model gets extra "draft space" to reason before answering); interleaved thinking after each tool result (the model thinks between tool calls, not just once at the start)
8. **Parallel tool calling** — 3-5 subagents in parallel + 3+ tools in parallel per subagent -> up to 90% reduction in research time

**Step 3 — A2A Protocol (agent<->agent, Linux Foundation 2026):**

- **MCP** = agent->tool; **A2A** = agent->agent. Complementary, not competing. Plain terms: MCP is how the agent picks up its tools; A2A is how agents phone each other.
- A2A lets agents across **different frameworks/vendors** (LangGraph, CrewAI, ADK, custom) discover + delegate + share results — while **not sharing internal memory/tools/logic** (opaque, secure — like two companies collaborating through official channels, not by handing over their internal files).
- Official SDKs: Python, JS, Java, .NET, Go, Rust + A2A CLI (10/2026).
- A2A is **NOT**: a development kit, a sub-agent protocol (sub-agents in one system use native primitives), or a replacement for MCP.

**Sync vs async:** Anthropic currently runs subagents **synchronously** (lead waits for subagents — like a manager who waits for each report before moving on). Simple but creates bottleneck (lead can't steer subagent mid-way). Async enables higher parallelism but is far more complex in result coordination + state consistency + error propagation.

> **One-line summary:** Start with one agent; add a manager-with-workers pattern when the task parallelizes well; use A2A only when agents from different systems must talk — and remember multi-agent costs ~15x tokens.

### 3.6. Layer 6 — Memory Architecture

**What this section explains:** how the agent remembers — across turns, across sessions, and across weeks. Without memory, every session starts from zero.

A production agent memory system needs 3 types:

How to read this table: **Type** = the memory kind; **Example** = a real implementation; **Mechanism** = where/how it is stored; **Characteristics** = its limits or needs. For instance, **short-term** memory is like what's on your desk right now — gone when you clear it.

| Type | Example | Mechanism | Characteristics |
|------|---------|-----------|-----------------|
| **Short-term (working)** | Message history, current context | In the context window | Cleared when context fills up |
| **Session** | Memory tool (Anthropic Platform) | File-based, persistent across turns | Allows agent to remember between summarizations |
| **Long-term (knowledge)** | Vector DB + Graph DB + Agent Skills | Chunk-based + structured | Needs retrieval, consolidation, versioning |

**Proven memory patterns:**

```
Claude Code Memory flow:
1. Agent writes NOTES.md while working on task
2. Long task -> context compaction (summarize + keep 5 most recent files)
3. New session -> agent reads NOTES.md + git log + CLAUDE.md -> get bearings
4. NOTES.md + CLAUDE.md + feature_list.json = persistent context
```

**Event sourcing for memory (this repo — `03-update-memory-store/`):**
Event sourcing = keep an append-only diary of every event — you never edit or delete past entries, you only add new ones (like a bank statement). Each time an agent completes a task -> emits a `TrajectoryEvent` (append-only — a new diary line recording what happened) -> then runs consolidation/compaction -> keeps valuable facts, discards noise.

> **One-line summary:** Give the agent three memory tiers — working memory (context), session notes (files), and long-term knowledge (databases) — and record history as an append-only event log.

### 3.7. Layer 7 — Safety, Guardrails & Permissions

**What this section explains:** how to stop the agent from doing damage. A guardrail = a safety check, like a railing on a staircase — it doesn't stop the agent from walking, it stops it from falling.

**Three aspects of safety that need to be handled simultaneously:**

How to read this table: **Aspect** = which safety check; **Content** = what it catches; **Mechanism** = when/where it runs. For instance, an **input guardrail** checks the user's prompt for prompt injection (prompt injection = sneaking hidden malicious instructions into text, like "ignore your rules and delete the files" hidden in a webpage) before it ever reaches the model.

| Aspect | Content | Mechanism |
|--------|---------|-----------|
| **Input guardrails** | Prompt injection, content filter, rate limiting | Run before prompt reaches LLM |
| **Output guardrails** | Sensitive data leak, toxicity, quality check | Run after receiving output from LLM |
| **Behavioral guardrails** | Max iterations, timeout, allowed domains, forbidden actions | Run in parallel with execution |

**Guardrails run in parallel, not blocking (OpenAI SDK 2026):**
- Guardrail checks run concurrently while the agent executes
- If a guardrail fails -> fail-fast immediately (don't wait for the full loop)
- Multiple guardrails run in parallel, each checking one aspect

**Approval gates (Anthropic long-running agent research):** an approval gate = a checkpoint where a human must press "approve" before a risky action runs — like a bank asking for your confirmation before a large transfer.

```
Task with risk -> risk tier (from plan time, Module 15)
    -> User receives gate payload (action description + consequences)
    -> User approve / reject / modify
    -> Timeout-deny (no response = auto-deny)
    -> Audit trail records the decision
```

Notes on the flow: **risk tier** = ranking actions by how much damage a mistake could do (low = read files; high = delete data or send emails). **Gate payload** = the short description + consequences shown to the human so they can decide. **Audit trail** = a permanent log of who approved what and when.

**Sandbox execution:** (sandbox = run the agent's code in an isolated box; if it misbehaves, only the box is damaged — like testing fireworks in a field, not in your living room)
- OpenAI Agents SDK has **Sandbox agents**: manifest-defined files (manifest = a declared list of exactly which files the agent may touch) + sandbox clients + resumable sandbox sessions
- This repo has `12-sandbox-execution/` — threat model (threat model = a list of what could go wrong and how), blast radius (blast radius = how much damage one failure can cause), 5 mandatory controls
- Agent Skills Security: only install skills from trusted sources; audit code dependencies + external network calls in skills carefully

> **One-line summary:** Layer three safety nets — check inputs, check outputs, and limit behavior — plus human approval gates and sandbox isolation for anything risky.

### 3.8. Layer 8 — Evaluation & Feedback

**What this section explains:** how to know if your agent actually works — and keeps working after every change. Evaluation (eval) = running the agent against a fixed set of test cases and scoring the results.

**Eval-first principle (Anthropic multi-agent 06/2025):**
- **Start evals immediately with a small sample** — 20 queries is enough to see the impact of major changes (30% -> 80%)
- **LLM-as-judge** with rubric: factual accuracy, citation accuracy, completeness, source quality, tool efficiency (rubric = a fixed scoring checklist, like a grading sheet for essays). 1 LLM call, 1 prompt, score 0.0-1.0 + pass/fail — simplest and most aligned with human judgment
- **Human evaluation catches edge cases** that evals miss — e.g., SEO content farms being preferred over academic sources
- **End-state evaluation** for agents that mutate state: evaluate the **final state** rather than each step — because agents may reach the right result via different paths

**Production reliability (production lessons from Anthropic Research):**
- Agents are **stateful** — small errors compound into disaster. Don't restart from scratch; **resume from checkpoint**
- **Rainbow deployments** — gradually shift traffic from old -> new version, keep both running in parallel, because agents may be mid-execution when you deploy
- **Production tracing** — observe decision patterns + interaction structures (not conversation content) to debug root cause (tracing = logging the agent's steps so you can replay what it did)

> **One-line summary:** Build evals from day one (20 test cases is enough to start), score with an LLM judge plus human checks, and in production resume from checkpoints instead of restarting.

---

## 4. Production-Proven Architecture Patterns

**What this section explains:** five ready-made blueprints that teams already run in production. Pick the one closest to your problem instead of inventing from scratch.

### 4.1. Single Agent (Minimal) — "Enough for most use cases"

**What this pattern is:** one agent doing everything itself in a simple loop. Start here before considering anything fancier.

```
User -> [Retrieval -> Context -> Prompt -> LLM -> Tools (MCP) -> Result] -> User
        ^                                                  |
        +--------------------------------------------------+ (loop until stop condition)
```

**When it's enough:**
- Short task, well-defined steps
- Only 1-2 tools needed
- Low complexity

**Minimal stack:** LLM API + MCP servers + Session memory + basic guardrails. (In plain terms: one model, a few tools, a notepad, and a couple of safety checks.)

> **One-line summary:** A single agent in a simple loop with a few tools covers most use cases — build this first.

### 4.2. Orchestrator-Workers (Multi-Agent)

**What this pattern is:** one lead agent acts as manager, splitting work across worker subagents (see section 3.5, Step 2, for the diagram).

Most common in production, suited for:
- Coding products (edit many files, each with a different nature)
- Search/analysis (multiple independent sources)
- Customer support (qualify -> resolve -> escalate)

**Common anti-pattern:** (anti-pattern = a tempting approach that repeatedly causes trouble) spawning 50 subagents for a simple query. Fix: scale effort to query complexity (section 3.5 principle 3).

> **One-line summary:** Use one manager agent plus worker subagents for tasks that split cleanly — but size the team to the task, not to your enthusiasm.

### 4.3. Long-Running Agent (Initializer + Coding Agent)

**What this pattern is:** how to survive tasks too big for one memory window — split the work into sessions, and carry state forward in files (feature list, progress notes, git commits).

From Anthropic 11/2025, for tasks spanning multiple context windows:

```
+-----------------------------------------------------------------------+
|                  LONG-RUNNING AGENT ARCHITECTURE                     |
+-----------------------------------------------------------------------+
|                                                                       |
|  Session 1: Initializer Agent                                         |
|  ------------------------------------------------------------------   |
|  User prompt -> Analyze requirements                                  |
|           -> Write feature_list.json (200+ features, JSON, all       |
|             marked "passes: false")                                   |
|           -> Write init.sh (run dev server)                           |
|           -> Create git repo + initial commit                         |
|           -> Write claude-progress.txt (initial state)                |
|                                                                       |
|  Session N (N >= 2): Coding Agent (each session runs 1 feature)      |
|  ------------------------------------------------------------------   |
|  1. Run pwd (identify working directory)                              |
|  2. Read claude-progress.txt + git log (get bearings)                 |
|  3. Read feature_list.json -> pick a not-done feature                 |
|  4. Read init.sh -> run dev server                                    |
|  5. Test basic features (puppeteer MCP) -> verify no new bugs        |
|  6. Implement 1 feature                                               |
|  7. Test end-to-end (browser automation)                              |
|  8. Mark feature as "passes: true"                                    |
|  9. git commit + update claude-progress.txt                           |
|  10. Exit (context window reset)                                      |
|                                                                       |
+-----------------------------------------------------------------------+
```

**Lessons:** Claude has 2 main failure modes:
- "One-shot" app (trying to do everything at once) -> context overflow -> has to guess what happened
- "Declare victory prematurely" after seeing a few features done

**Fix = 3 mechanisms:**
- Feature list JSON (modifying/removing tests = unacceptable) — the list is the contract; the agent may check boxes, never rewrite the list
- Incremental progress (1 feature per session) — small steps, each verified, instead of one giant gamble
- Structured cleanup (git commit + progress notes at the end of each session) — every session ends with a save point, so the next session can pick up cleanly

> **One-line summary:** For multi-session tasks, keep a frozen feature list, do one feature per session, and always end with a git commit plus progress notes.

### 4.4. Multi-Agent Research System

**What this pattern is:** Anthropic's production research system — a lead researcher agent spawns subagents to explore many directions in parallel, then merges everything into one cited answer.

For open-ended, breadth-first problems with multiple independent directions:

```
User query -> LeadResearcher (Opus 4.5)
    |-- Thinking (extended) -> save plan to Memory
    |-- Spawn Subagent A (Sonnet) -> search "aspect 1"
    |-- Spawn Subagent B (Sonnet) -> search "aspect 2"
    |-- Spawn Subagent C (Sonnet) -> search "aspect 3"
    |   (each subagent: interleaved thinking after each tool result)
    |
    Lead synthesizes -> decide if more research needed
        |-- If yes -> spawn more subagents or refine
        +-- If no -> CitationAgent (process docs -> cite sources)
                         v
                   Final answer + citations
```

**Token economics:** multi-agent ~15x tokens vs regular chat. Only use when task value justifies the cost. (Plain terms: if a chat answer costs $1 of tokens, the multi-agent research might cost $15.)

> **One-line summary:** A lead researcher agent plus parallel subagents gives the best research quality — but at ~15x token cost, so reserve it for high-value questions.

### 4.5. Hybrid Retrieval -> Agent (RAG + Agent)

**What this pattern is:** combining pre-built search (RAG) with a live agent loop. The search gives the agent a head start; the loop lets it dig deeper when the head start isn't enough.

```
Query -> [Hybrid Search] -> [Context Assembly] -> [Agent Loop] -> Answer
              ^                     ^
         Vector DB          + Prompt + Memory
         + Graph DB         + Tools
```

**New in 2026:** instead of pre-computing all context upfront -> combine **just-in-time retrieval** (agent actively explores) + static CLAUDE.md. Claude Code uses this pattern: CLAUDE.md dropped into context upfront; glob/grep for progressive disclosure.

> **One-line summary:** Give the agent a static briefing plus the ability to search live — fast like pre-computed retrieval, fresh like manual exploration.

---

## 5. Comparing Agent Frameworks & SDKs

**What this section explains:** which off-the-shelf framework to pick, if any. An SDK (Software Development Kit) = a ready-made library that saves you from building the harness by hand.

How to read this table: each **row** is one capability; each **column** is one framework/SDK. For instance, the **Maturity** row tells you how battle-tested each option is, and **Primitives** lists the basic building blocks the SDK hands you (primitives = ready-made parts like "Agent", "Handoff" — a handoff = one agent passing the conversation to another, like passing a baton). "Via X" means you get that capability only through an add-on, not built in.

| Criteria | Claude Agent SDK | OpenAI Agents SDK | LangGraph | CrewAI | ADK (Google) | Strands (AWS) |
|----------|------------------|-------------------|-----------|--------|--------------|---------------|
| **Maturity** | Stable (Anthropic) | Production (OpenAI) | Very mature | Mature | GA (Google) | Stable (AWS) |
| **Primitives** | Agent + tools + MCP + memory | Agents + handoffs + guardrails + sessions + sandbox | Graph state machine + nodes/edges | Agent + crew + process | Agent + tool + task | Agent + tools |
| **Multi-agent** | Handoffs / sub-agents | Handoffs (primary); multi-agent orchestration | Native DAG/HSM | Native Crew (roles + sequential/parallel) | Native (TaskGraph) | Built-in |
| **Context management** | Compaction + memory tool | Sessions (SQLite, Redis, MongoDB, Dapr) | Manual | Manual | Manual | Manual |
| **MCP** | Native | Native MCP server manager | Native | Via LangChain MCP | Via extensions | Via integrations |
| **A2A** | Via custom | Via custom | Via LangGraph A2A nodes | Via custom | Via ADK A2A | Via custom |
| **Sandbox** | Via code execution | **Sandbox agents** (workspace isolation, manifest, resumable) | Via LangChain | Via custom | Via Vertex AI | Via AWS |
| **Tracing** | Console tracing | Built-in + OpenAI eval/fine-tune | LangSmith | Weights & Biases | Vertex AI | CloudWatch |
| **Guardrails** | Input/output validation | Guardrails (parallel, fast-fail) | Via LangChain LCEL | Via code | Via decorators | Via config |
| **Strengths** | Frontier model integration, Skills | Simple primitives, sandbox agents, 3 agent types (text/voice/realtime) | Full flexibility, production-tested | Fast prototyping | Google ecosystem | AWS ecosystem |
| **Weaknesses** | Vendor lock-in | Mostly OpenAI models | Overkill for simple tasks | Little low-level control | GCP only | AWS only |
| **Recommendation** | Use Claude model; need frontier quality | Use OpenAI; need sandbox + handoffs | Want full control; complex workflows | Fast prototyping; small team | Google Cloud; Vertex AI | AWS; Bedrock |

Notes on the rows: **Tracing** = built-in logging to see what the agent did; **Guardrails** = input/output safety checks; **Vendor lock-in** = getting stuck with one company's ecosystem because switching is painful. "GA" = Generally Available (finished, supported release, not a beta).

**Advice from Anthropic:** Start with the direct LLM API — many patterns only need a few lines of code. Use a framework only when you understand the underlying code; wrong assumptions about abstractions are the most common source of bugs.

**SDK naming notes (2025-2026):**
- **Claude Agent SDK** = **Claude Code SDK** renamed (Anthropic, 09/2025) — same SDK, used for both Claude Code (IDE) and custom agents.
- **OpenAI Agents SDK** = evolution of Swarm (experiment 2024) → production-grade SDK v2 (2025-2026).
- **Google ADK** (Agent Development Kit): open-source, GA 04/2025, used internally for Gemini Agentspace + Vertex AI Agent Builder.

**10/2026 Verification — new trends:**
- **LazyGraphRAG** (Microsoft, late 2024 → production 2025): LLM summarisation deferred to query time → indexing cost equal to vector RAG, query quality equal to full GraphRAG, ~700× lower query cost. Integrated into Microsoft Discovery (2025) and Azure Local.
- **Gartner 2026**: GraphRAG named in "Top Trends in D&A for 2026" as the path for complex cases where high-accuracy RAG fails.
- **Agent Control Planes**: IBM predicts 2026 will be the year agent control planes and multi-agent dashboards become production reality. (Control plane = a central cockpit where you watch and manage all your agents, like an air-traffic-control tower.)

**MCP + A2A = standardization combo (2026):**

```
Agent (any framework)
    |-- MCP client --> MCP servers (tools, data, APIs)
    +-- A2A client --> A2A servers (other agents)

A2A and MCP solve 2 DIFFERENT problems, complementing each other.
MCP: "what the agent needs to do" (tools/resources)
A2A: "who the agent needs to talk to" (collaboration, handoffs)
```

> **One-line summary:** Only adopt a framework when its abstractions make sense to you — otherwise the direct LLM API with a few hundred lines of code is safer and cheaper.

---

## 6. The Practical Build Process (Build Checklist)

**What this section explains:** the build order, as 7 phases of checklists. Work top to bottom: decide the shape first, then pick models and tools, then context, then orchestration, then safety, then evaluation, then monitoring.

### Phase 1: Define architectural requirements

**What this phase answers:** before writing code, decide the shape — workflow or agent, one model tier or several, one session or many.

- [ ] Does the task have well-defined steps? -> use a **workflow** (no agent needed)
- [ ] How many model tiers are needed? -> Sonnet is enough for regular tasks; use Opus for the orchestrator
- [ ] Does the token budget allow multi-agent? -> budget is enough -> multi-agent; otherwise -> single agent
- [ ] How long does the task run? -> < 1 session -> simple; multiple context windows -> long-running pattern

> **One-line summary:** Four questions — fixed steps? model tiers? token budget? task duration? — decide your whole architecture before you code.

### Phase 2: Design Layer 1-2 (Model + Tools)

**What this phase answers:** which models to use and which tools to give them — keep the tool list small and each description crystal clear.

- [ ] Choose model tiers matching task complexity
- [ ] Tool list — minimal but functionally complete (if a human can't distinguish tool X vs Y -> split them)
- [ ] Write tool descriptions like docstrings for a junior dev (name + description + examples + edge cases + boundaries)
- [ ] Implement MCP servers for external tools (build-once, use everywhere)
- [ ] Register tools with the MCP manager / registry

> **One-line summary:** Choose models per task difficulty and ship few but excellent tools — clear descriptions beat many tools.

### Phase 3: Design Layer 3 (Context Engineering)

**What this phase answers:** how to keep the model's memory small and useful — retrieval strategy, budget, compaction, and storage.

- [ ] Choose retrieval strategy: pre-computed (RAG), just-in-time, or hybrid
- [ ] Set a context budget (token limit per turn)
- [ ] Implement compaction (trigger at ~70% capacity, don't wait for 90%)
- [ ] Decide memory layer: file-based (NOTES.md), database (SQLite/Redis), or vector
- [ ] If using Agent Skills: design SKILL.md with progressive disclosure

> **One-line summary:** Set a context budget, compact at ~70% full, and pick one memory store — don't let context quietly overflow.

### Phase 4: Design Layer 4-5 (Orchestration + Multi-agent)

**What this phase answers:** whether you need more than one agent, and if so, how workers get tasks and report back.

- [ ] Is a single agent enough? -> implement a simple loop
- [ ] Need multi-agent? -> design the orchestrator-worker pattern:
  - [ ] Each subagent: specialized prompt + output format + task boundaries
  - [ ] Effort scaling rules in the prompt (fact-finding vs research vs complex)
  - [ ] Parallelization: 3-5 subagents + 3+ tools in parallel per subagent
  - [ ] Extended thinking for the lead; interleaved thinking for subagents
- [ ] Need A2A? -> design task handoff, shared results, no shared memory

> **One-line summary:** Default to a single agent; add workers only with clear task boundaries, effort-scaling rules, and parallelism.

### Phase 5: Safety & Guardrails

**What this phase answers:** what stops the agent from causing damage. Each checkbox is one safety net; note the isolation ladder on the sandbox line — a language-level sandbox is the weakest isolation, a container is stronger, and a syscall filter (blocking low-level OS calls) is strongest.

- [ ] Input guardrail: prompt injection detection + content filter
- [ ] Output guardrail: sensitive data + quality check
- [ ] Behavioral guardrail: max iterations + timeout + allowed domains
- [ ] Risk tier: assign at plan time (04), gate payload for humans, timeout-deny
- [ ] Sandbox: isolation tier (language -> container -> syscall filter)
- [ ] Rainbow deployment for production agents (keep both versions running in parallel)

> **One-line summary:** Install all three guardrail types, human approval for risky actions, sandbox isolation, and switch traffic gradually at deploy time.

### Phase 6: Evaluation

**What this phase answers:** how you will measure quality — before users find the problems for you.

- [ ] Start evals immediately with 20 small test cases
- [ ] LLM-as-judge with rubric: accuracy + completeness + tool efficiency + source quality
- [ ] Human evaluation to catch edge cases
- [ ] End-state eval for agents that mutate state (check final state, not each step)
- [ ] Regression test after every deploy (regression test = re-running old test cases after each change, to catch things the change broke)

> **One-line summary:** Twenty test cases from day one, an LLM judge plus human spot-checks, and a regression run after every deploy.

### Phase 7: Observability & Debugging

**What this phase answers:** how to see what the agent did and recover when it fails — you cannot fix what you cannot see.

- [ ] Production tracing: agent decision patterns, interaction structures (not content)
- [ ] Session-level event log (TrajectoryEvent: append-only)
- [ ] Error recovery: checkpoint + resume (don't restart from scratch)
- [ ] Metrics: success rate, avg response time, token usage, error types

> **One-line summary:** Log every step as append-only events, save checkpoints to resume from, and track a handful of core metrics.

---

## 7. Connecting to the Existing Framework in This Repo

This document is a **synthesis and update** — it does not replace but complements the existing materials:

How to read this table: **File in this repo** = the existing document or folder; **Role** = what that material covers; **Connection to this document** = which layer of the 8-layer architecture it feeds. For instance, `harness/11-evaluation/` provides the details behind Layer 8 (Evaluation).

| File in this repo | Role | Connection to this document |
|-------------------|------|----------------------------|
| `AI_AGENT_FRAMEWORK.md` | Global map of 15 modules + 6 phases | This is the "overview"; this architecture = the specific implementation |
| `HARNESS_ENGINEERING.md` | 7 harness components, 10 commandments, case studies | Layer 2 of this architecture = the implementation of the harness |
| `GRAPH_ENGINEERING.md` | Knowledge graph for AI agents | Supplements Layer 1 (RAG/Retrieval) — Graph doesn't replace Vector, they combine |
| `loop/01-concepts/` -> `loop/07-tools/` | Loop Engineering — self-sustaining loop patterns | Layer 5 (Orchestration) uses loop patterns for single + multi-agent |
| `harness/01-retrieve-memory-knowledge/` | Retrieve Memory | Layer 3 (Context) starts from retrieval |
| `harness/03-update-memory-store/` | Write-back + Event sourcing + Trajectory | Layer 6 (Memory) of this architecture |
| `harness/06-decide-tools-mcp/` | Tool selection + MCP + ACI design | Layer 4 (Tool Ecosystem) builds on this module |
| `harness/07-workflow/` | Pipeline design, state machine, error recovery | Layer 5 (Orchestration) uses workflow patterns |
| `harness/09-multi-agent/` | Agent roles, communication, shared memory | Layer 5 (Orchestration) + A2A section supplements the new protocol |
| `harness/11-evaluation/` | Rubric, benchmarks, LLM-judge | Layer 8 (Evaluation) of this architecture |
| `harness/12-sandbox-execution/` | Sandboxing + threat model | Layer 7 (Safety) uses these sandboxing mechanisms |
| `harness/13-trajectory-observability/` | Event stream, join keys, retention | Observability part of Phase 7 checklist |
| `harness/14-compaction-context/` | Compaction trigger, pin set, summarization | Layer 3 (Context Engineering) uses directly |
| `harness/15-approval-gates/` | Risk tier, gate payload, audit | Layer 7 (Safety) uses directly |

**Relationship diagram:**

```
AGENT_SYSTEM_ARCHITECTURE.md (synthesis + 2026 update)
    |
    +-- HARNESS_ENGINEERING.md --> Layer 2 (Harness 7 components)
    +-- GRAPH_ENGINEERING.md  --> Layer 1 supplement (Graph + Vector)
    +-- AI_AGENT_FRAMEWORK.md --> Phase map (01-15 modules)
    |
    +-- loop/ + harness/ + graph/
        -> Details for each module underneath
        -> 12-15 = cross-cutting (safety, obs, context, approvals)
```

> **One-line summary:** This document is the 2026 layer map; the other repo documents are the deep-dive manuals for each layer.

---

## 8. References

**What this section explains:** where every claim in this guide comes from — original research posts, repo documents, protocol specs, and SDK docs.

### Primary Official Research (2024-2026, directly verified)

How to read this table: **Source** = the article (clickable link); **Year** = when it was published; **Topic** = what it covers. For instance, the first row is the article that defined the workflow-vs-agent vocabulary used throughout this guide.

| Source | Year | Topic |
|--------|------|-------|
| [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | 12/2024 | Workflows vs agents, 5 workflow patterns, ACI design |
| [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 09/2025 | Context rot, compaction, note-taking, sub-agent architectures |
| [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 06/2025 | Orchestrator-worker production: +90.2% vs single agent, 8 prompting principles |
| [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | 11/2025 | Initializer + coding agent, feature list JSON, incremental progress |
| [Agent Skills](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) | 10/2025 | SKILL.md format, progressive disclosure 3 levels, open standard |
| [Code Execution with MCP](https://www.anthropic.com/research/code-execution-with-mcp) | 11/2025 | Instead of exposing many tools, agent writes code to call MCP |
| [Claude Managed Agents](https://www.anthropic.com/engineering/managed-agents) | 2026 | Production managed agent infrastructure |

> **One-line summary:** These seven Anthropic articles are the backbone of this guide — read them for the full original detail.

### Architecture Origins (in this repo)

- `HARNESS_ENGINEERING.md` — 7 components, SOLID, 10 commandments, case studies
- `GRAPH_ENGINEERING.md` — Knowledge graph for AI agents, GraphRAG, 9 modules
- `AI_AGENT_FRAMEWORK.md` — 15 modules, 6 phases, 27 project ideas
- `harness/ARCHITECTURE.md` — Overall harness architecture, 3 shared contracts
- `loop/` — Loop Engineering: concepts, patterns, safety, anti-patterns
- `harness/09-multi-agent/SUBAGENT.md` — Sub-agent spec: lifecycle, spawn, budget
- `harness/03-update-memory-store/trajectory-fork-replay.md` — Event stream, fork/replay/resume
- `harness/11-evaluation/minimal-benchmark-harness.md` — Eval harness isolation

> **One-line summary:** These are the in-repo source documents this guide synthesizes — each covers one layer in depth.

### Protocols & Standards

How to read this table: **Protocol** = the standard's name (with link); **Year** = when it emerged; **Purpose** = the connection it standardizes. For instance, MCP standardizes agent-to-tool connections, while A2A standardizes agent-to-agent ones.

| Protocol | Year | Purpose |
|---------|------|---------|
| [MCP spec 2026-07-28](https://modelcontextprotocol.io/) | 2024-2026 | Agent->tool: standardize tools, data, resources |
| [A2A Protocol](https://a2a-protocol.org) | 2026 | Agent->agent: handoff, delegation, collaboration |
| [Agent Skills (open standard)](https://agentskills.io/) | 12/2025 | SKILL.md: package expertise for agents |
| DeepLearning.AI — [Intro to A2A](https://goo.gle/dlai-a2a) | 2026 | Course introducing A2A protocol |

> **One-line summary:** MCP (agent-to-tool), A2A (agent-to-agent), and Agent Skills (packaged expertise) are the three open standards to know.

### SDKs & Frameworks

How to read this table: **SDK** = the framework (clickable link); **Strengths** = what it is best at. For instance, pick LangGraph when you want to design the workflow yourself as a state machine.

| SDK | Strengths |
|-----|-----------|
| [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) | Frontier models, Skills, long-running (formerly Claude Code SDK, renamed 09/2025) |
| [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | Sandbox agents, handoffs, sessions, guardrails, tracing |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Full flexibility, state machine, production |
| [CrewAI](https://docs.crewai.com/) | Fast prototyping, roles + processes |
| [Google ADK](https://adk.dev/) | Google ecosystem, Vertex AI (GA 04/2025, open-source) |
| [AWS Strands](https://strandsagents.com/latest/) | AWS + Bedrock ecosystem |

> **One-line summary:** Six main SDKs dominate in 2026 — match the choice to your cloud and your need for control.

### Blogs & Key Principles

- **"Agents" — Simon Willison** (2025): definition converging: *"LLMs autonomously using tools in a loop"*
- **"Context rot" — Chroma Research**: attention budget decreases as context grows
- **Harness Engineering quote — Mitchell Hashimoto**: *"Every time an agent makes a mistake, you don't pray — you build a systemic solution"*
- **Agentic AI Foundation (Linux Foundation)**: MCP + A2A governance + open standards

> **One-line summary:** The sources above are the primary evidence behind every recommendation in this guide.

---

*Part of the [AI Coding Skills Framework](./AI_AGENT_FRAMEWORK.md) — Agent System Architecture Track*

<!-- BUILD-DONE -->
