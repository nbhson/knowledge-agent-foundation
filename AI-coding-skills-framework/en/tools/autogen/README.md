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

Your harness keeps getting more complex: a single agent doing everything — retrieve, plan, code, review. Once the task gets big enough, the single agent becomes the **bottleneck**: overloaded context, one small error breaks the whole chain, and no division of specialized labor.

> *"One agent doing everything is a monolith. A harness of specialized agents is a microservices architecture for cognition."*

**AutoGen (Microsoft)** solves this with a **conversation-based multi-agent** model: multiple agents (assistant, user proxy, critic, planner...) talk to each other through a `ConversableAgent` abstraction. Each agent has a role, a system prompt, and its own capabilities — like specialized nodes in a harness.

### Why AutoGen Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Multi-agent is natural** | Conversation-based — agents exchange messages, and any of them can call tools |
| 2 | **UserProxyAgent = harness** | The sample code in HARNESS_ENGINEERING.md shows the UserProxyAgent playing the orchestrating-harness role |
| 3 | **Integrated code execution** | Agents can run code in a sandbox, receive results, and fix things themselves |
| 4 | **GroupChat for orchestration** | Multiple agents + a manager = a decision-making council |

### Relationship to the Harness

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

## Overview

### Conversation-Based Multi-Agent

AutoGen uses an **agent-to-agent conversation** architecture. Instead of a linear pipeline, the agents exchange messages:

```
User → UserProxyAgent → AssistantAgent (calls tool) → UserProxyAgent (runs code)
     → AssistantAgent (gets result, continues) → ... → replies to User
```

### Sample Code From HARNESS_ENGINEERING.md

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"},
    system_message="You are a helpful assistant"
)

# UserProxyAgent plays the harness role — orchestration, code execution, control
harness = UserProxyAgent(
    name="harness",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"}
)
```

`human_input_mode="NEVER"` turns the UserProxyAgent into a **self-operating harness**: it calls tools on its own, collects results on its own, and keeps going until it's done or hits the `max_consecutive_auto_reply` limit.

### GroupChat — Multiple Agents

```python
from autogen import GroupChat, GroupChatManager

agents = [planner, assistant, critic, executor]
group_chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=20,
    speaker_selection_method="auto"  # or "round_robin", "vote"
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

This is exactly **harness/09-multi-agent** in code form — a manager orchestrating who speaks when, like a harness orchestrating its workers.

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

## Real-World Case Studies

### 1. Code Review Pipeline (Planner → Coder → Critic)

```python
planner  = AssistantAgent(name="planner",  system_message="Create a detailed plan")
coder    = AssistantAgent(name="coder",    system_message="Write code following the plan")
critic   = AssistantAgent(name="critic",   system_message="Review logic & safety errors")

group_chat = GroupChat(agents=[planner, coder, critic], max_round=15)
manager = GroupChatManager(groupchat=group_chat)

# The harness starts the council
result = manager.run(task="Implement login API with rate limiting")
```

Flow: the planner proposes → the coder implements → the critic finds bugs → back to the coder to fix → ... until the critic is satisfied — a code-based **loop/05-multi-loop**.

### 2. Human-in-the-Loop for Sensitive Changes

```python
sensitive_harness = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",  # only stops when confirmation is needed
    code_execution_config=False
)
```

## Reference Materials

- **AutoGen (Microsoft)**: https://microsoft.github.io/autogen/
- **AutoGen Studio**: https://microsoft.github.io/autogen/studio/
- **GitHub**: https://github.com/microsoft/autogen

### Links to Other Branches

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (AutoGen sample code)
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent concepts
- [tools/loop-cli](../loop-cli/) — Orchestration layer
- [tools/langchain](../langchain/) — Alternative framework (graph-based)

---

> **"AutoGen doesn't give you agents — it gives you a conversation where intelligence emerges."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — autogen*
