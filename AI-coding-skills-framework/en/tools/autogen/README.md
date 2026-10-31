# 🤖 AutoGen — Multi-Agent Harness (Microsoft)

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why AutoGen Matters?](#why-autogen-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview](#overview)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section explains why one big agent stops being enough, and what AutoGen does about it.

Your harness is getting bigger. At first, one agent does everything — it looks things up, makes a plan, writes code, and reviews the result. But when tasks grow, that single agent runs into trouble: its context gets too full (*context = everything the model can "hold in mind" at once*), one small mistake can break the whole chain, and there is no teamwork to share the load.

> *"One agent doing everything is a monolith. A harness of specialized agents is a microservices architecture for cognition."*

**AutoGen (Microsoft)** fixes this with a **conversation-based multi-agent** setup: several agents (assistant, user proxy, critic, planner...) talk to each other through a `ConversableAgent` idea (*ConversableAgent = any agent that can send and receive messages — the base class every AutoGen agent is built on*). Each agent has its own role, its own instructions, and its own skills — a bit like small expert helpers inside one bigger harness.

> **One-line summary:** AutoGen splits one overloaded agent into several specialists that talk to each other by message.

### Why AutoGen Matters?

This section lists the four concrete things AutoGen gives you that a single agent cannot.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Multi-agent is natural** | Agents talk through messages, and any agent can call tools |
| 2 | **UserProxyAgent = harness** | The example in HARNESS_ENGINEERING.md uses UserProxyAgent as the main organizer |
| 3 | **Integrated code execution** | Agents can run code in a safe sandbox (*sandbox = an isolated, throwaway environment where mistakes can't hurt anything real*), read the result, and fix problems by themselves |
| 4 | **GroupChat for orchestration** | Many agents plus a manager work together like a small team that makes decisions |

> **How to read this table:** each row = one built-in capability. For example, row 2: the *UserProxyAgent* is the "hands" agent — it runs tools and code on behalf of the group, which is exactly the harness role, so it doubles as your orchestrator.

> **One-line summary:** Four built-ins — message-based agents, a proxy that acts as the harness, sandboxed code execution, and a managed GroupChat.

### Relationship to the Harness

This section maps each AutoGen piece onto the seven harness components, so you can translate between the two vocabularies.

```
┌────────────────────────────────────────────────────────────┐
│  AUTOGEN MAP VS HARNESS COMPONENTS                         │
│                                                            │
│  PlannerAgent            → harness/04 (plan/decompose)     │
│  AssistantAgent          → harness/05 (prompt/response)    │
│  UserProxyAgent (harness)→ harness/06 (tool execution)     │
│  CriticAgent             → harness/11 (evaluation)         │
│  GroupChat + Manager     → harness/09 (multi-agent)        │
│  Memory (ConversableMemory)→ harness/01, 03 (memory)       │
└────────────────────────────────────────────────────────────┘
```

> **How to read this diagram:** the left side names the AutoGen agent; the right side names the harness concept it plays. For example, the *CriticAgent* (the agent that finds faults) is AutoGen's version of harness/11 evaluation.

> **One-line summary:** Every AutoGen agent type plays one harness role — planner, executor, critic, or orchestrator.

## Overview

### Conversation-Based Multi-Agent

AutoGen uses **agents talking to each other**. Instead of one straight line of steps, the agents send messages back and forth:

```
User → UserProxyAgent → AssistantAgent (calls tool) → UserProxyAgent (runs code)
     → AssistantAgent (gets result, continues) → ... → replies to User
```

(*In plain words: you ask, the proxy fetches and runs things, the assistant thinks and calls tools, and they pass messages until someone answers you.*)

> **One-line summary:** Agents coordinate by passing messages, not by a fixed script.

### Sample Code From HARNESS_ENGINEERING.md

> 📄 **Example code:** [`examples/01-sample-code-from-harness-engineering-md.py`](examples/01-sample-code-from-harness-engineering-md.py)

With `human_input_mode="NEVER"` (*the agent never pauses to ask a human — see the FAQ for why that needs care*), the UserProxyAgent turns into a **harness that runs by itself**: it calls tools on its own, gathers the results on its own, and keeps going until the job is done or it reaches the `max_consecutive_auto_reply` limit (*the maximum number of replies one agent may give in a row without a human*).

> **One-line summary:** With no human input, the proxy becomes a self-running harness — bounded by a hard reply limit.

### GroupChat — Multiple Agents

> 📄 **Example code:** [`examples/02-groupchat-multiple-agents.py`](examples/02-groupchat-multiple-agents.py)

This is **harness/09-multi-agent** written as code — a manager decides who speaks next, much like a harness guides its workers.

> **One-line summary:** AutoGen's model is agents passing messages — one pair for simple work, a managed GroupChat when several specialists must cooperate.

## Learning Roadmap (Directory Structure)

```
autogen/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) ConversableAgent, UserProxyAgent, GroupChat
├── 02-setup/            ← (TODO) Installing pyautogen, configuring the LLM
├── 03-patterns/         ← (TODO) Two-agent, group chat, nested chats
├── 04-savings/          ← (TODO) Token cost per conversation round
└── 05-troubleshooting/  ← (TODO) Infinite loops, agent deadlock, termination
```

### Recommended Roadmap

```
Step 1: Read the section 9.1 of HARNESS_ENGINEERING.md — sample AutoGen code is provided
   ↓
Step 2: Run a 2-agent model: UserProxyAgent + AssistantAgent
   ↓
Step 3: Add a Planner + Critic — corresponding to harness/04 + harness/11
   ↓
Step 4: Scale up to a GroupChat with a manager (harness/09 multi-agent)
   ↓
Step 5: Connect memory + evaluation (see tools/observability, tools/evaluation)
```

| If you want to... | Read |
|-------------------|------|
| Understand a multi-agent harness | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Planning/decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Evaluation/review | [harness/11-evaluation](../../harness/11-evaluation/) |
| Loops of agents | [loop/05-multi-loop](../../loop/05-multi-loop/) |

> **How to read this table:** the left column is your goal ("I want to plan and split tasks"); the right column is the document that teaches it. Start with harness/09 if the multi-agent idea itself is new to you.

> **One-line summary:** Start from the sample code in harness/09.1, run two agents, then grow to a managed GroupChat.

## Real-World Case Studies

### 1. Code Review Pipeline (Planner → Coder → Critic)

> 📄 **Example code:** [`examples/03-1-code-review-pipeline-planner-coder-critic.py`](examples/03-1-code-review-pipeline-planner-coder-critic.py)

How it runs: the planner suggests a plan → the coder writes the code → the critic spots bugs → the coder fixes them → this repeats until the critic is happy — a code version of **loop/05-multi-loop**.

> **One-line summary:** Planner → coder → critic, repeated until the critic approves — a review loop in code.

### 2. Human-in-the-Loop for Sensitive Changes

> 📄 **Example code:** [`examples/04-2-human-in-the-loop-for-sensitive-changes.py`](examples/04-2-human-in-the-loop-for-sensitive-changes.py)

(*Human-in-the-loop = the agent must stop and get a person's approval before risky steps, like a sign-off before a payment.*)

> **One-line summary:** Two ready-made flows: a plan→code→review loop, and a version that stops for human approval on risky changes.

## Reference Materials

This section lists the official docs and the related modules in this framework.

> **One-line summary:** Official docs, AutoGen Studio, the GitHub repo, and links to related modules.

- **AutoGen (Microsoft)**: https://microsoft.github.io/autogen/
- **AutoGen Studio**: https://microsoft.github.io/autogen/studio/
- **GitHub**: https://github.com/microsoft/autogen

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (AutoGen sample code)
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent concepts
- [tools/loop-cli](../loop-cli/) — Orchestration layer
- [tools/langchain](../langchain/) — Alternative framework (graph-based)

> **One-line summary:** Four links: the sample code, multi-agent concepts, orchestration tools, and the rival graph framework.

---

> **"AutoGen doesn't give you agents — it gives you a conversation where intelligence emerges."**

---

## ⚠️ Update 10/2026: AutoGen → Microsoft Agent Framework (MAF)

This section is the headline news for AutoGen users: the library described above has been retired and replaced.

AutoGen has been **archived** (*archived = frozen by Microsoft; no bug fixes, no new features*) and replaced by **Microsoft Agent Framework (MAF)**:
- AutoGen repo archived — no further development
- MAF = unification of AutoGen + Semantic Kernel
- Completely new API: `agents/`, no more `ConversableAgent`

> 📄 **Example code:** [`examples/05-update-10-2026-autogen-microsoft-agent-framework-maf.py`](examples/05-update-10-2026-autogen-microsoft-agent-framework-maf.py)

**Migrate your project:** https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
**MAF new:** https://github.com/microsoft/agent-framework

> **One-line summary:** AutoGen is frozen forever — use Microsoft Agent Framework (MAF) for new work and plan a migration for existing code.

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — autogen*
