# 🤖 IX. Multi-Agent

> ## 📑 Table of Contents
>
> - [Overview](#overview)
> - [Contents](#contents)
> - [1. Agent Roles](#1-agent-roles)
>   - [1.1 Agent Role Taxonomy](#11-agent-role-taxonomy)
>   - [1.2 Detailed Agent Definitions](#12-detailed-agent-definitions)
> - [2. Communication Patterns](#2-communication-patterns)
>   - [2.1 Communication Patterns Overview](#21-communication-patterns-overview)
>   - [2.2 Message Protocol](#22-message-protocol)
> - [3. Orchestration Strategies](#3-orchestration-strategies)
>   - [3.1 Strategy Comparison](#31-strategy-comparison)
>   - [3.2 Orchestrator Implementation](#32-orchestrator-implementation)
> - [4. Shared Memory](#4-shared-memory)
>   - [4.1 Memory Architecture](#41-memory-architecture)
>   - [4.2 Shared Memory Manager](#42-shared-memory-manager)
> - [5. Conflict Resolution](#5-conflict-resolution)
>   - [5.1 Conflict Types & Resolution](#51-conflict-types-resolution)
>   - [5.2 Conflict Resolution Manager](#52-conflict-resolution-manager)
> - [6. Agent Selection Guide](#6-agent-selection-guide)
>   - [6.1 When to Use Multi-Agent](#61-when-to-use-multi-agent)
> - [7. Real-World Implementations](#7-real-world-implementations)
>   - [7.1 Code Review Pipeline](#71-code-review-pipeline)
>   - [7.2 Feature Development Team](#72-feature-development-team)
>   - [7.3 Debug Squad](#73-debug-squad)
> - [8. Debugging Multi-Agent Systems](#8-debugging-multi-agent-systems)
>   - [8.1 Debug Strategy](#81-debug-strategy)
>   - [8.2 Debug Logger](#82-debug-logger)
> - [9. Performance Optimization](#9-performance-optimization)
>   - [9.1 Optimization Strategies](#91-optimization-strategies)
>   - [9.2 Cost Estimation](#92-cost-estimation)
> - [10. Anti-Patterns & Solutions](#10-anti-patterns-solutions)
>   - [10.1 Common Anti-Patterns](#101-common-anti-patterns)
> - [11. Production Deployment](#11-production-deployment)
>   - [11.1 Deployment Checklist](#111-deployment-checklist)
> - [Best Practices](#best-practices)
> - [12. Case Studies — Real-World Multi-Agent Architectures](#12-case-studies-real-world-multi-agent-architectures)
>   - [12.1 Claude Code — Anthropic's Multi-Agent Architecture](#121-claude-code-anthropics-multi-agent-architecture)
>   - [12.2 Devin — Autonomous Software Engineering Agent](#122-devin-autonomous-software-engineering-agent)
>   - [12.3 OpenHands (OpenDevin) — Open-Source Multi-Agent](#123-openhands-opendevin-open-source-multi-agent)
> - [13. Advanced Multi-Agent Patterns](#13-advanced-multi-agent-patterns)
>   - [13.1 MapReduce Pattern for Code Generation](#131-mapreduce-pattern-for-code-generation)
>   - [13.2 Debate Pattern — Multi-Agent Discussion](#132-debate-pattern-multi-agent-discussion)
>   - [13.3 Critique-Revision Pattern](#133-critique-revision-pattern)
>   - [13.4 Ensemble Pattern — Multiple Agents, Best Output](#134-ensemble-pattern-multiple-agents-best-output)
> - [14. Multi-Agent Testing Strategies](#14-multi-agent-testing-strategies)
>   - [14.1 Testing Multi-Agent Systems](#141-testing-multi-agent-systems)
>   - [14.2 Test Implementation](#142-test-implementation)
> - [15. Cost-Benefit Analysis](#15-cost-benefit-analysis)
>   - [15.1 When Multi-Agent Is Worth It](#151-when-multi-agent-is-worth-it)
>   - [15.2 Token Cost Comparison](#152-token-cost-comparison)
> - [References](#references)
>   - [Frameworks](#frameworks)
>   - [Research & Papers](#research-papers)
>   - [Production Systems](#production-systems)
>   - [Architecture Patterns](#architecture-patterns)
>
---

### Opening Story

Have you ever watched a **heist** movie like *Ocean's Eleven*? The crew of 11, each with a specialty: one person makes the plan (Danny Ocean), one picks locks (Basher), one does disguises (Saul), one drives (Terry). None of them could have **pulled it off alone** — but together, they executed the perfect heist.

**AI Multi-Agent works exactly the same way.**

A single AI agent can be good at many things, but when a task gets complex enough — like *"Implement a payment system with tests, docs, and a security review"* — one agent will **overload**. The context window gets wasted having to hold knowledge for every domain, there's no peer review to catch mistakes, and worst case: **the agent confirms its own mistakes**.

**The solution**: Multi-Agent Architecture — each agent is a **specialist in one domain**, coordinated through a communication protocol, with checks & balances to guarantee quality.

### Why Is Multi-Agent Important?

> *"A single agent is like one person doing everything — capable but slow, easily overloaded, and without checks & balances."*

#### 3 Scientific Pieces of Evidence

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **AutoGen (Microsoft, 2025)** | Multi-agent architecture solved **68% of complex coding tasks** successfully, compared to **41%** for single-agent |
| 2 | **CrewAI Research (2025)** | Agent teams with role specialization improved **code quality by 52%** (measured by review scores) |
| 3 | **Google DeepMind (2025)** | The multi-agent debate pattern reduced the **hallucination rate by 35%** in code generation |

#### Core philosophy:

```
Multi-Agent = Specialization + Communication + Coordination + Checks & Balances
```

Each agent = **a specialist in one domain**. Like a multi-specialty hospital — the general practitioner (Orchestrator), the cardiologist (Backend Agent), the surgeon (Frontend Agent), the pharmacist (Testing Agent). They don't do everything — they do their own part **best in class**.

**If you skip it**: the single agent overloads, there is no peer review, wrong code is produced without anyone catching it, and the context window is wasted by having to hold knowledge for every domain.

## Overview

> **📌 Core Concept**
>
> - **Concept:** A Multi-Agent System is an architecture in which **multiple AI agents work together**, each taking on a specialized role (writing code, reviewing, testing...) to complete tasks that are too complex for a single agent.
> - **Analogy/comparison:** Like a hospital — the general practitioner does the initial exam, the cardiology specialist handles heart issues, the pharmacist prescribes medication. No one does everything, but the coordination produces the correct outcome.
> - **Why it matters:** A single agent easily overloads and "confirms its own mistakes" on complex tasks — multi-agent adds cross-checks (checks & balances).

**Multi-Agent Systems** in AI coding are an architecture of **multiple AI agents working together**, where each agent has a specialized role and they cooperate to complete complex tasks that a single agent would struggle to handle.

```
┌──────────────────────────────────────────────────────────────────┐
│                      MULTI-AGENT SYSTEM                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │ Planner  │───►│ Coder    │───►│ Reviewer │            │  │
│  │  │ Agent    │    │ Agent    │    │ Agent    │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │       │               │               │                   │  │
│  │       └───────────────┴───────────────┘                   │  │
│  │                       │                                    │  │
│  │              ┌────────┴────────┐                          │  │
│  │              │  Coordinator    │                          │  │
│  │              │  / Orchestrator │                          │  │
│  │              └────────┬────────┘                          │  │
│  │                       │                                    │  │
│  │         ┌─────────────┼─────────────┐                    │  │
│  │         ▼             ▼             ▼                     │  │
│  │    ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │    │ Tester   │  │ Debugger │  │ DevOps   │             │  │
│  │    │ Agent    │  │ Agent    │  │ Agent    │             │  │
│  │    └──────────┘  └──────────┘  └──────────┘             │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Contents

| # | Topic | Description |
|---|--------|-------|
| 1 | [Agent Roles](#1-agent-roles) | Common agent roles |
| 2 | [Communication Patterns](#2-communication-patterns) | Communication patterns between agents |
| 3 | [Orchestration Strategies](#3-orchestration-strategies) | Orchestration strategies |
| 4 | [Shared Memory](#4-shared-memory) | Shared memory among agents |
| 5 | [Conflict Resolution](#5-conflict-resolution) | Resolving conflicts |
| 6 | [Agent Selection Guide](#6-agent-selection-guide) | Choosing the right structure |
| 7 | [Real-World Implementations](#7-real-world-implementations) | Real-world examples |
| 8 | [Debugging Multi-Agent Systems](#8-debugging-multi-agent-systems) | Debug & troubleshoot |
| 9 | [Performance Optimization](#9-performance-optimization) | Optimizing performance |
| 10 | [Anti-Patterns & Solutions](#10-anti-patterns--solutions) | Common mistakes |
| 11 | [Production Deployment](#11-production-deployment) | Real-world deployment |

---

## 1. Agent Roles

> **📌 Core Concept**
>
> - **Concept:** Agent Roles are the way expertise is divided up — each agent (orchestrator, coder, reviewer, tester...) owns a single responsibility and a set of skills so they can cooperate on complex work.
> - **Analogy/comparison:** Like a soccer team: the goalkeeper specializes in catching the ball, the striker in scoring goals. Clear roles keep the whole team in sync.
> - **Why it matters:** Without clearly assigned roles, agents duplicate each other's work, drop the ball, and no one is fully accountable.

### 1.1 Agent Role Taxonomy

Here is a complete map of agent roles, organized into 4 tiers: **Coordination**, **Execution** (doing the work), **Quality** (quality control) and **Support**. Read it like a company org chart — the top tier makes decisions, the lower tiers do the work and cross-check each other. The metaphor: this is the team's "job description board" — everyone knows what they are supposed to do.

```
┌──────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ROLE TAXONOMY                      │
│                                                                  │
│  COORDINATION LAYER                                              │
│  ├── Orchestrator     → Overall orchestration, routing tasks     │
│  ├── Planner          → Analyze, decompose, plan                │
│  └── Supervisor       → Monitor progress, quality gates         │
│                                                                  │
│  EXECUTION LAYER                                                 │
│  ├── Coder            → Write code to spec                      │
│  ├── Architect        → Design the system, choose patterns      │
│  ├── Refactorer       → Improve code quality                    │
│  └── Integrator       → Integrate modules and APIs              │
│                                                                  │
│  QUALITY LAYER                                                   │
│  ├── Code Reviewer    → Assess code quality                     │
│  ├── Tester           → Write & run tests                       │
│  ├── Security Auditor → Check for vulnerabilities               │
│  └── Performance Analyst → Analyze & optimize performance       │
│                                                                  │
│  SUPPORT LAYER                                                   │
│  ├── Debugger         → Find & fix bugs                         │
│  ├── Doc Writer       → Write documentation                     │
│  ├── DevOps           → CI/CD, deployment, monitoring           │
│  └── Git Manager      → Branching, commits, PRs                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Detailed Agent Definitions

This code defines each agent role in Python: every role has its **own system prompt** (behavioral instructions), a **limit on the number of agents that can run concurrently**, **average token usage**, and the **list of tools** it is allowed to use. The code block is large, but it is essentially a "job card" listing who does what and what they are allowed to use. The goal: standardize things so agents don't work outside their scope.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum

class AgentRole(Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    CODER = "coder"
    ARCHITECT = "architect"
    REFACTORER = "refactorer"
    CODE_REVIEWER = "code_reviewer"
    TESTER = "tester"
    DEBUGGER = "debugger"
    SECURITY_AUDITOR = "security_auditor"
    DOC_WRITER = "doc_writer"
    DEVOPS = "devops"
    GIT_MANAGER = "git_manager"
    PERFORMANCE_ANALYST = "performance_analyst"
    INTEGRATOR = "integrator"


AGENT_DEFINITIONS = {
    AgentRole.ORCHESTRATOR: {
        "name": "Orchestrator",
        "responsibility": "Overall orchestration, task assignment, workflow management",
        "system_prompt_addon": """
            You are the ORCHESTRATOR. Your job:
            1. Analyze incoming requests
            2. Break into sub-tasks
            3. Route to appropriate specialist agents
            4. Monitor progress and handle failures
            5. Coordinate handoffs between agents
            6. Final quality gate before delivery
            
            You do NOT write code directly. You delegate.
        """,
        "max_concurrent": 1,
        "typical_tokens": 2000,
        "tools": ["task_decomposer", "agent_router", "progress_tracker"],
    },
    
    AgentRole.CODER: {
        "name": "Coder",
        "responsibility": "Write code according to specifications and requirements",
        "system_prompt_addon": """
            You are the CODER. Your job:
            1. Read specifications carefully
            2. Implement clean, working code
            3. Follow project conventions and patterns
            4. Handle error cases
            5. Write self-documenting code
            6. Report completion with summary of changes
            
            Focus on CORRECTNESS first, then CLARITY.
        """,
        "max_concurrent": 3,
        "typical_tokens": 5000,
        "tools": ["read_file", "write_to_file", "search_files", "execute_command"],
    },
    
    AgentRole.ARCHITECT: {
        "name": "Architect",
        "responsibility": "Design system architecture and make technical decisions",
        "system_prompt_addon": """
            You are the ARCHITECT. Your job:
            1. Analyze requirements for system-level implications
            2. Design module boundaries and interfaces
            3. Choose appropriate patterns and technologies
            4. Identify risks and trade-offs
            5. Create technical specifications
            6. Review code for architectural compliance
            
            Think in systems, not just code.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "search_files", "list_code_definition_names"],
    },
    
    AgentRole.CODE_REVIEWER: {
        "name": "Code Reviewer",
        "responsibility": "Evaluate code quality, correctness, and security",
        "system_prompt_addon": """
            You are the CODE REVIEWER. Your job:
            1. Read all changed files thoroughly
            2. Check for correctness and logic errors
            3. Verify adherence to coding standards
            4. Identify potential security issues
            5. Suggest improvements with specific examples
            6. Provide actionable feedback (not vague comments)
            
            Be constructive but thorough. Every comment should help.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "search_files", "execute_command"],
    },
    
    AgentRole.TESTER: {
        "name": "Tester",
        "responsibility": "Write tests, run tests, and report coverage",
        "system_prompt_addon": """
            You are the TESTER. Your job:
            1. Write comprehensive unit tests
            2. Create integration tests for critical paths
            3. Test edge cases and error scenarios
            4. Run test suites and report results
            5. Identify coverage gaps
            6. Suggest test improvements
            
            Think about what could go WRONG.
        """,
        "max_concurrent": 2,
        "typical_tokens": 4000,
        "tools": ["read_file", "write_to_file", "execute_command", "search_files"],
    },
    
    AgentRole.DEBUGGER: {
        "name": "Debugger",
        "responsibility": "Find root causes and fix bugs",
        "system_prompt_addon": """
            You are the DEBUGGER. Your job:
            1. Analyze error messages and stack traces
            2. Form hypotheses about root cause
            3. Read relevant code to validate hypotheses
            4. Implement minimal fix (not over-engineer)
            5. Add regression tests
            6. Document root cause
            
            Be systematic. Track what you've tried.
        """,
        "max_concurrent": 1,
        "typical_tokens": 4000,
        "tools": ["read_file", "search_files", "execute_command", "write_to_file"],
    },
    
    AgentRole.DEVOPS: {
        "name": "DevOps",
        "responsibility": "CI/CD, deployment, infrastructure, monitoring",
        "system_prompt_addon": """
            You are the DEVOPS agent. Your job:
            1. Manage CI/CD pipelines
            2. Handle deployments
            3. Configure monitoring and alerting
            4. Manage Docker/container configs
            5. Handle environment configurations
            6. Ensure reproducibility
            
            Automate everything. Document what can't be automated.
        """,
        "max_concurrent": 1,
        "typical_tokens": 3000,
        "tools": ["read_file", "write_to_file", "execute_command"],
    },
}
```

</details>

---

## 2. Communication Patterns

> **📌 Core Concept**
>
> - **Concept:** Communication Patterns are the information-exchange structures between agents — sequential passing, parallel fan-out, via a message bus... — plus a standard message protocol so data is transmitted reliably and stays in sync.
> - **Analogy/comparison:** Like a company: a few people pass documents down an assembly line (pipeline), or everyone reads from the same shared notice board (blackboard).
> - **Why it matters:** If agents don't communicate to a standard ⟶ information gets lost, agents work on stale data and produce wrong results.

### 2.1 Communication Patterns Overview

This section compares 6 ways agents "talk" to each other: sequential passing (pipeline), splitting work in parallel (fan-out), sharing a common state board (blackboard), direct question-answer (request-reply), work assignment management (hierarchical), and publishing events through a bus (pub/sub). Each has its own pros (✓) and cons (✗) — you read them to pick the right style for your problem. The metaphor: a pipeline is an assembly line, a blackboard is the company's shared bulletin board.
```
┌──────────────────────────────────────────────────────────────────┐
│              AGENT COMMUNICATION PATTERNS                         │
│                                                                  │
│  PATTERN 1: SEQUENTIAL PIPELINE                                  │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐            │
│  │Agent A │──►│Agent B │──►│Agent C │──►│Agent D │            │
│  │Planner │   │Coder   │   │Reviewer│   │Tester  │            │
│  └────────┘   └────────┘   └────────┘   └────────┘            │
│  Output of A → Input of B → Output of C → Input of D           │
│  ✓ Simple, predictable  ✗ Slow (no parallelism)                │
│                                                                  │
│  PATTERN 2: FAN-OUT / FAN-IN                                    │
│                    ┌────────┐                                   │
│               ┌───►│Agent A │───┐                              │
│  ┌────────┐  │    └────────┘   │    ┌────────┐                │
│  │Router  │──┤    ┌────────┐   ├───►│Merger  │                │
│  └────────┘  ├───►│Agent B │──┤    └────────┘                │
│               │    └────────┘   │                               │
│               └───►│Agent C │──┘                               │
│                    └────────┘                                   │
│  ✓ Parallel execution  ✓ Throughput  ✗ Merge conflicts          │
│                                                                  │
│  PATTERN 3: BLACKBOARD (Shared State)                            │
│  ┌─────────────────────────────────────┐                       │
│  │           BLACKBOARD                │                       │
│  │  ┌─────────────────────────────┐   │                       │
│  │  │  Shared State / Knowledge   │   │                       │
│  │  └─────────────────────────────┘   │                       │
│  └──────┬──────┬──────┬──────┬────────┘                       │
│         │      │      │      │                                  │
│    ┌────┴─┐┌───┴──┐┌──┴───┐┌─┴─────┐                         │
│    │Agent ││Agent ││Agent ││Agent  │                          │
│    │  A   ││  B   ││  C   ││  D    │                          │
│    └──────┘└──────┘└──────┘└───────┘                          │
│  Agents read/write shared state independently                    │
│  ✓ Decoupled  ✓ Flexible  ✗ Race conditions, consistency       │
│                                                                  │
│  PATTERN 4: REQUEST-REPLY (Conversation)                        │
│  ┌────────┐         ┌────────┐                                  │
│  │Agent A │◄───────►│Agent B │                                  │
│  └────────┘ Request │        │                                  │
│       │   ┌────────►└────────┘                                  │
│       │   │    Reply                                            │
│       ▼   ▼                                                     │
│  Multi-turn conversation until consensus                        │
│  ✓ Negotiation  ✓ Rich  ✗ Token-heavy, can loop                │
│                                                                  │
│  PATTERN 5: HIERARCHICAL (Manager → Workers)                    │
│  ┌──────────────┐                                               │
│  │   Manager    │                                               │
│  │   Agent      │                                               │
│  └──┬───┬───┬──┘                                               │
│     │   │   │                                                   │
│  ┌──┴┐┌─┴─┐┌┴──┐                                               │
│  │W1 ││W2 ││W3 │   Workers process sub-tasks in parallel       │
│  └───┘└───┘└───┘                                               │
│  ✓ Scalable  ✓ Clear authority  ✗ Single point of failure       │
│                                                                  │
│  PATTERN 6: EVENT-DRIVEN (Pub/Sub)                              │
│  ┌────────┐  event   ┌──────────────────┐  event   ┌────────┐ │
│  │Agent A │─────────►│  Event Bus       │─────────►│Agent B │ │
│  └────────┘          │  (pub/sub)       │          └────────┘ │
│                       │  ┌────────────┐ │                       │
│                       │  │ subscribers│ │                       │
│                       │  └────────────┘ │                       │
│                       └──────────────────┘                       │
│  ✓ Decoupled  ✓ Scalable  ✗ Hard to debug, eventual consistency │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Message Protocol

This code standardizes the "letter envelope" that agents exchange: every message has a **sender, a recipient, a message type** (task handoff, completion report, information request...), a **payload** (content), a timestamp, a priority, and a time-to-live. The `MessageRouter` function acts as the post office: it receives letters, queues them per agent, and broadcasts when needed. The metaphor: without a standard format, if agent A "writes by hand" while agent B "reads numbers", the information will fall apart.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
import uuid

class MessageType(Enum):
    TASK_ASSIGN = "task_assign"
    TASK_COMPLETE = "task_complete"
    TASK_FAILED = "task_failed"
    REQUEST_INFO = "request_info"
    PROVIDE_INFO = "provide_info"
    FEEDBACK = "feedback"
    HEARTBEAT = "heartbeat"
    ESCALATE = "escalate"


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    from_agent: str = ""
    to_agent: str = ""
    message_type: MessageType = MessageType.TASK_ASSIGN
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    reply_to: Optional[str] = None
    priority: int = 5       # 1=highest
    ttl_seconds: int = 300   # Time to live
    
    def to_prompt_context(self) -> str:
        """Convert message to readable prompt context"""
        lines = [
            f"From: {self.from_agent}",
            f"Type: {self.message_type.value}",
            f"Time: {self.timestamp}",
            "---",
        ]
        for key, value in self.payload.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)


class MessageRouter:
    """
    Routes messages between agents — manages message queues
    and delivery.
    """
    
    def __init__(self):
        self.queues: Dict[str, List[AgentMessage]] = {}
        self.message_log: List[AgentMessage] = []
        self.handlers: Dict[str, Callable] = {}
    
    def register_agent(self, agent_id: str, 
                       handler: Callable = None):
        """Register an agent with the message router"""
        self.queues[agent_id] = []
        if handler:
            self.handlers[agent_id] = handler
    
    def send(self, message: AgentMessage) -> bool:
        """Send a message to an agent"""
        if message.to_agent not in self.queues:
            return False
        
        self.queues[message.to_agent].append(message)
        self.message_log.append(message)
        
        # Auto-deliver if handler registered
        if message.to_agent in self.handlers:
            handler = self.handlers[message.to_agent]
            handler(message)
        
        return True
    
    def receive(self, agent_id: str) -> List[AgentMessage]:
        """Receive messages for an agent"""
        messages = self.queues.get(agent_id, [])
        self.queues[agent_id] = []
        return messages
    
    def peek(self, agent_id: str) -> List[AgentMessage]:
        """View messages without removing them"""
        return self.queues.get(agent_id, [])
    
    def broadcast(self, sender: str, message_type: MessageType,
                  payload: Dict[str, Any]):
        """Send a message to all agents"""
        for agent_id in self.queues:
            if agent_id != sender:
                msg = AgentMessage(
                    from_agent=sender,
                    to_agent=agent_id,
                    message_type=message_type,
                    payload=payload,
                )
                self.send(msg)
    
    def get_metrics(self) -> Dict[str, int]:
        """Metrics about message activity"""
        return {
            "total_sent": len(self.message_log),
            "by_type": {
                mt.value: sum(
                    1 for m in self.message_log 
                    if m.message_type == mt
                )
                for mt in MessageType
            },
            "pending": {
                aid: len(q) for aid, q in self.queues.items()
            },
        }
```

</details>

---

## 3. Orchestration Strategies

> **📌 Core Concept**
>
> - **Concept:** Orchestration Strategies are the way a multi-agent workflow is organized — running sequentially, in parallel, in a manager/worker hierarchy, or by discussion until a decision is reached — deciding which agent starts, how they coordinate, and how results are synthesized.
> - **Analogy/comparison:** Like a film director: shoot scenes one at a time in sequence (sequential), let multiple crews shoot in parallel (parallel), or have the on-set manager delegate the work (hierarchical).
> - **Why it matters:** Picking the wrong strategy ⟶ the whole system runs slowly, burns tokens, or produces inconsistent results.

### 3.1 Strategy Comparison

A table comparing 6 orchestration strategies, with columns for **when to use** and the **pros/cons** of each type. How to read it: identify the characteristics of your task (independent? dependent? needs debate?) and find the matching row. The metaphor: like choosing how to organize work — clearly defined work gets a sequential assembly line, independent work gets split among several people at once.

```
┌──────────────────────────────────────────────────────────────────┐
│              ORCHESTRATION STRATEGIES                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ STRATEGY        │ WHEN TO USE         │ PROS/CONS       │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Sequential      │ Simple workflows    │ ✓ Predictable   │    │
│  │ Pipeline        │ Clear dependencies  │ ✗ No parallel   │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Parallel        │ Independent tasks   │ ✓ Fast          │    │
│  │ Fan-out         │ No dependencies     │ ✗ Merge issues  │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Hierarchical    │ Complex projects    │ ✓ Scalable      │    │
│  │ (Manager/Worker)│ Need coordination   │ ✗ Bottleneck    │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Blackboard      │ Research/creative   │ ✓ Flexible      │    │
│  │ (Shared state)  │ Emergent solutions  │ ✗ Race cond.    │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Negotiation     │ Design decisions    │ ✓ Rich dialogue │    │
│  │ (Conversation)  │ Need consensus      │ ✗ Token-heavy   │    │
│  ├─────────────────┼─────────────────────┼─────────────────┤    │
│  │ Event-driven    │ Loosely coupled     │ ✓ Decoupled     │    │
│  │ (Pub/Sub)       │ Scalable systems    │ ✗ Hard to trace │    │
│  └─────────────────┴─────────────────────┴─────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Orchestrator Implementation

This code is a working implementation of an orchestrator: it **takes a task list and orders them by their dependencies** (which task must wait for which), **routes to the right agent** by task type, **retries on failure**, and tracks token consumption. The `_resolve_execution_order` function is like an automated "work schedule" that figures out which job goes first. The metaphor: an orchestrator is a project manager — scheduling, delegating, checking off each item.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

class OrchestrationMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    NEGOTIATION = "negotiation"
    EVENT_DRIVEN = "event_driven"


class AgentOrchestrator:
    """
    Central orchestrator manages agent lifecycle, routing,
    and coordination.
    
    Modes:
    - sequential: Agents execute one after another
    - parallel: Independent agents run simultaneously
    - hierarchical: Manager delegates to workers
    - negotiation: Agents discuss to reach consensus
    """
    
    def __init__(self, mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL):
        self.mode = mode
        self.agents: Dict[str, Any] = {}
        self.router = MessageRouter()
        self.execution_log: List[Dict] = []
        self.max_retries = 2
        self.token_budget = 100000
        self.tokens_used = 0
    
    def register_agent(self, agent_id: str, role: AgentRole,
                       agent_instance: Any = None):
        """Register an agent with the orchestrator"""
        self.agents[agent_id] = {
            "role": role,
            "instance": agent_instance,
            "status": "idle",
            "tasks_completed": 0,
            "errors": 0,
            "avg_tokens": 0,
        }
        self.router.register_agent(agent_id)
    
    def execute_pipeline(self, tasks: List[Dict[str, Any]]) -> Dict:
        """
        Execute tasks through the agent pipeline.
        
        Each task: {
            "id": str,
            "type": str,          # maps to AgentRole
            "input": Dict,
            "depends_on": [str],  # task IDs
        }
        """
        results = {}
        executed = set()
        
        # Topological sort based on dependencies
        execution_order = self._resolve_execution_order(tasks)
        
        for task in execution_order:
            task_id = task["id"]
            
            # Check dependencies
            deps_met = all(
                dep in executed 
                for dep in task.get("depends_on", [])
            )
            if not deps_met:
                results[task_id] = {
                    "status": "skipped",
                    "reason": "Dependencies not met"
                }
                continue
            
            # Route to appropriate agent
            agent_id = self._route_task(task)
            if not agent_id:
                results[task_id] = {
                    "status": "failed",
                    "reason": "No available agent for task type"
                }
                continue
            
            # Execute with retry
            result = self._execute_with_retry(
                agent_id, task, 
                context=results
            )
            results[task_id] = result
            executed.add(task_id)
            
            # Track token usage
            self.tokens_used += result.get("tokens_used", 0)
            if self.tokens_used > self.token_budget:
                break
        
        return {
            "results": results,
            "tokens_used": self.tokens_used,
            "tasks_completed": len(executed),
            "execution_log": self.execution_log,
        }
    
    def _route_task(self, task: Dict) -> Optional[str]:
        """Route task to best available agent"""
        task_type = task.get("type", "")
        
        # Map task type to agent role
        role_map = {
            "plan": AgentRole.PLANNER,
            "architect": AgentRole.ARCHITECT,
            "code": AgentRole.CODER,
            "review": AgentRole.CODE_REVIEWER,
            "test": AgentRole.TESTER,
            "debug": AgentRole.DEBUGGER,
            "deploy": AgentRole.DEVOPS,
            "docs": AgentRole.DOC_WRITER,
            "refactor": AgentRole.REFACTORER,
            "security": AgentRole.SECURITY_AUDITOR,
        }
        
        target_role = role_map.get(task_type)
        if not target_role:
            return None
        
        # Find available agent with matching role
        for agent_id, info in self.agents.items():
            if (info["role"] == target_role 
                and info["status"] == "idle"):
                return agent_id
        
        return None
    
    def _execute_with_retry(self, agent_id: str, task: Dict,
                            context: Dict = None) -> Dict:
        """Execute a task with retry logic"""
        agent = self.agents[agent_id]
        agent["status"] = "busy"
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # Simulate agent execution
                result = {
                    "status": "success",
                    "output": f"Task {task['id']} completed by {agent_id}",
                    "tokens_used": task.get("estimated_tokens", 1000),
                    "attempt": attempt + 1,
                }
                
                agent["tasks_completed"] += 1
                agent["status"] = "idle"
                
                self.execution_log.append({
                    "task_id": task["id"],
                    "agent_id": agent_id,
                    "attempt": attempt + 1,
                    "status": "success",
                })
                
                return result
                
            except Exception as e:
                last_error = str(e)
                agent["errors"] += 1
                
                self.execution_log.append({
                    "task_id": task["id"],
                    "agent_id": agent_id,
                    "attempt": attempt + 1,
                    "status": "error",
                    "error": last_error,
                })
        
        agent["status"] = "idle"
        return {
            "status": "failed",
            "error": last_error,
            "attempts": self.max_retries + 1,
        }
    
    def _resolve_execution_order(self, tasks: List[Dict]) -> List[Dict]:
        """Topological sort tasks by dependencies"""
        task_map = {t["id"]: t for t in tasks}
        in_degree = {t["id"]: 0 for t in tasks}
        
        for task in tasks:
            for dep in task.get("depends_on", []):
                if dep in in_degree:
                    in_degree[task["id"]] += 1
        
        from collections import deque
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            task_id = queue.popleft()
            order.append(task_map[task_id])
            
            for task in tasks:
                if task_id in task.get("depends_on", []):
                    in_degree[task["id"]] -= 1
                    if in_degree[task["id"]] == 0:
                        queue.append(task_id)
        
        return order
    
    def get_status_report(self) -> str:
        """Report the orchestrator's status"""
        lines = [
            "=== Orchestrator Status ===",
            f"Mode: {self.mode.value}",
            f"Tokens used: {self.tokens_used:,} / {self.token_budget:,}",
            f"Agents: {len(self.agents)}",
            "",
            "Agent Status:",
        ]
        for aid, info in self.agents.items():
            lines.append(
                f"  {aid}: {info['role'].value} "
                f"[{info['status']}] "
                f"tasks={info['tasks_completed']} "
                f"errors={info['errors']}"
            )
        
        return "\n".join(lines)
```

</details>

---

## 4. Shared Memory

> **📌 Core Concept**
>
> - **Concept:** Shared Memory is a centralized data store that many agents read/write together — project context, task queue, finalized decisions — so agents can share understanding without retransmitting all the information.
> - **Analogy/comparison:** Like the whiteboard in a meeting room: everyone can see it and add to it, instead of each person keeping a private notebook and reading it aloud to the others.
> - **Why it matters:** Without shared memory, each agent "remembers things differently" ⟶ they work on stale context and the results are inconsistent.

### 4.1 Memory Architecture

The diagram shows two memory tiers: **Global Memory** (the shared whiteboard: project context, task queue, state, decision log) and each agent's **Agent Memory** (private context + its own working memory). The idea: anything that needs to be shared goes on the common board; anything private stays in your own drawer. The metaphor: like an office that shares a work board, while each person still has a personal notebook.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT SHARED MEMORY                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   GLOBAL MEMORY                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │ Project Context (codebase, config, docs)         │   │   │
│  │  │ Task Queue (pending, in-progress, done)          │   │   │
│  │  │ Shared State (variables, results, artifacts)     │   │   │
│  │  │ Decision Log (choices made and reasoning)        │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│  │ Agent Memory │ │ Agent Memory │ │ Agent Memory │              │
│  │   Agent A    │ │   Agent B    │ │   Agent C    │              │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │              │
│  │ │Private  │ │ │ │Private  │ │ │ │Private  │ │              │
│  │ │Context  │ │ │ │Context  │ │ │ │Context  │ │              │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │              │
│  │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │              │
│  │ │Working  │ │ │ │Working  │ │ │ │Working  │ │              │
│  │ │Memory   │ │ │ │Memory   │ │ │ │Memory   │ │              │
│  │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │              │
│  └─────────────┘ └─────────────┘ └─────────────┘              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Shared Memory Manager

This code implements a safe "whiteboard" for many agents to read/write at the same time without stepping on each other — thanks to a `Lock` (synchronization lock), no write operation can be interrupted mid-write by another agent. Besides global memory, it also stores **artifacts** (files, test results) and a **change log** recording who changed what. The metaphor: like a bank vault — every open/close must happen in order, and every transaction is written in the ledger.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from threading import Lock
from typing import Any, Dict, List, Optional
from datetime import datetime

class SharedMemoryManager:
    """
    Thread-safe shared memory for multi-agent systems.
    
    Layers:
    - Global: Project-wide state, accessible by all agents
    - Agent-private: Each agent's own context
    - Artifact store: Files, code, test results
    """
    
    def __init__(self):
        self._lock = Lock()
        self.global_state: Dict[str, Any] = {
            "project_files": [],
            "task_queue": [],
            "completed_tasks": [],
            "decisions": [],
        }
        self.agent_memory: Dict[str, Dict[str, Any]] = {}
        self.artifacts: Dict[str, Any] = {}
        self.change_log: List[Dict] = []
    
    def read_global(self, key: str) -> Any:
        """Read from global memory"""
        with self._lock:
            return self.global_state.get(key)
    
    def write_global(self, key: str, value: Any, 
                     agent_id: str = "system"):
        """Write to global memory"""
        with self._lock:
            old_value = self.global_state.get(key)
            self.global_state[key] = value
            
            self.change_log.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent_id,
                "key": key,
                "action": "write",
                "old": str(old_value)[:200],
                "new": str(value)[:200],
            })
    
    def update_global(self, key: str, updater: Callable,
                      agent_id: str = "system"):
        """Atomic update — read-modify-write inside the lock"""
        with self._lock:
            current = self.global_state.get(key, {})
            new_value = updater(current)
            self.global_state[key] = new_value
            
            self.change_log.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent_id,
                "key": key,
                "action": "update",
            })
    
    def get_agent_memory(self, agent_id: str) -> Dict[str, Any]:
        """Get an agent's private memory"""
        with self._lock:
            if agent_id not in self.agent_memory:
                self.agent_memory[agent_id] = {
                    "context": "",
                    "working_set": [],
                    "notes": [],
                }
            return self.agent_memory[agent_id]
    
    def store_artifact(self, name: str, content: Any,
                       agent_id: str = "system"):
        """Store an artifact (file content, test result, etc.)"""
        with self._lock:
            self.artifacts[name] = {
                "content": content,
                "stored_by": agent_id,
                "timestamp": datetime.now().isoformat(),
            }
    
    def get_artifact(self, name: str) -> Optional[Any]:
        """Get an artifact"""
        artifact = self.artifacts.get(name)
        return artifact["content"] if artifact else None
    
    def log_decision(self, decision: str, rationale: str,
                     agent_id: str):
        """Log a technical decision"""
        with self._lock:
            self.global_state["decisions"].append({
                "decision": decision,
                "rationale": rationale,
                "agent": agent_id,
                "timestamp": datetime.now().isoformat(),
            })
    
    def get_summary(self) -> str:
        """Summarize shared memory status"""
        return (
            f"Global keys: {len(self.global_state)}\n"
            f"Agents: {len(self.agent_memory)}\n"
            f"Artifacts: {len(self.artifacts)}\n"
            f"Decisions: {len(self.global_state['decisions'])}\n"
            f"Changes logged: {len(self.change_log)}"
        )
```

</details>

---

## 5. Conflict Resolution

> **📌 Core Concept**
>
> - **Concept:** Conflict Resolution is the mechanism for handling disagreements between agents — two agents editing the same file, opposing viewpoints, resource contention — by classifying the conflict and applying a controlled reconciliation strategy.
> - **Analogy/comparison:** Like two coworkers editing the same report: the risk of overwriting each other. With rules about "who locks the file, who gets the final call", neither person's work gets broken.
> - **Why it matters:** Without a conflict resolution mechanism, agents can overwrite and "break" each other's results.

### 5.1 Conflict Types & Resolution

The diagram lists 5 common conflict types between agents — same-file edits, opposing approaches, resource contention, reading inconsistent state, contradictory outputs — along with the resolution strategy for each type. How to read it: identify which type your conflict is and apply the ready-made solution. The metaphor: like traffic rules — with rules in place, two cars that meet each other instantly know who has priority.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT CONFLICT RESOLUTION                      │
│                                                                  │
│  CONFLICT TYPE 1: CODE CONFLICT                                  │
│  Agent A and Agent B are editing the same file                   │
│  → SOLUTION: File locking + merge strategy                       │
│    - Last-write-wins (simple but risky)                          │
│    - Three-way merge (safe)                                      │
│    - Agent negotiation (discuss changes)                         │
│                                                                  │
│  CONFLICT TYPE 2: APPROACH CONFLICT                              │
│  Agent A and Agent B disagree on approach                        │
│  → SOLUTION: Debate protocol                                     │
│    - Each agent presents rationale (max 3 points)               │
│    - Orchestrator evaluates evidence                             │
│    - Majority vote or authority decision                         │
│                                                                  │
│  CONFLICT TYPE 3: RESOURCE CONFLICT                              │
│  Multiple agents need same tool/API at same time                 │
│  → SOLUTION: Resource scheduling                                 │
│    - Priority-based access                                       │
│    - Time-sliced access                                          │
│    - Queue with fair scheduling                                  │
│                                                                  │
│  CONFLICT TYPE 4: STATE CONFLICT                                 │
│  Agents read inconsistent shared state                            │
│  → SOLUTION: Consistency protocol                                │
│    - Optimistic locking (retry on conflict)                     │
│    - Pessimistic locking (acquire lock first)                   │
│    - Event sourcing (replay from events)                        │
│                                                                  │
│  CONFLICT TYPE 5: OUTPUT CONFLICT                                │
│  Multiple agents produce contradictory results                    │
│  → SOLUTION: Validation protocol                                 │
│    - Cross-validation (agent B validates agent A)               │
│    - Authority agent has final say                               │
│    - Quality metrics decide                                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Conflict Resolution Manager

This code implements the "peacekeeping" mechanism between agents: file locking (no other agent may edit while one is in use), scoring approaches when two agents disagree, and logging every conflict that is resolved. The `_score_approach` function grades the arguments — the more specific a rationale is (contains "because", "trade-off", "tested"), the more likely it wins. The metaphor: like a referee who scores debate entries to pick the more persuasive speaker.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Dict, List, Tuple
from enum import Enum

class ConflictType(Enum):
    CODE_CONFLICT = "code_conflict"
    APPROACH_CONFLICT = "approach_conflict"
    RESOURCE_CONFLICT = "resource_conflict"
    STATE_CONFLICT = "state_conflict"
    OUTPUT_CONFLICT = "output_conflict"


class ConflictResolutionManager:
    """
    Detects and resolves conflicts between agents.
    """
    
    def __init__(self):
        self.file_locks: Dict[str, str] = {}  # file -> agent_id
        self.conflict_log: List[Dict] = []
    
    def acquire_file_lock(self, file_path: str, 
                          agent_id: str) -> bool:
        """Agent requests a lock on a file before modifying it"""
        if file_path in self.file_locks:
            current_holder = self.file_locks[file_path]
            if current_holder != agent_id:
                self.conflict_log.append({
                    "type": ConflictType.CODE_CONFLICT,
                    "file": file_path,
                    "agents": [current_holder, agent_id],
                    "resolution": "blocked",
                })
                return False
        
        self.file_locks[file_path] = agent_id
        return True
    
    def release_file_lock(self, file_path: str, agent_id: str):
        """Agent releases a file lock when done"""
        if self.file_locks.get(file_path) == agent_id:
            del self.file_locks[file_path]
    
    def resolve_approach_conflict(
        self,
        agent_a: Dict,   # {"id": str, "approach": str, "rationale": str}
        agent_b: Dict,
        authority: str = "orchestrator",
    ) -> Dict:
        """
        Resolve a disagreement between 2 agents on approach.
        Uses structured debate with evidence.
        """
        # Score each approach
        score_a = self._score_approach(agent_a)
        score_b = self._score_approach(agent_b)
        
        winner = agent_a if score_a >= score_b else agent_b
        loser = agent_b if score_a >= score_b else agent_a
        
        resolution = {
            "type": ConflictType.APPROACH_CONFLICT,
            "agents": [agent_a["id"], agent_b["id"]],
            "winner": winner["id"],
            "chosen_approach": winner["approach"],
            "scores": {agent_a["id"]: score_a, agent_b["id"]: score_b},
            "resolved_by": authority,
        }
        
        self.conflict_log.append(resolution)
        return resolution
    
    def _score_approach(self, agent: Dict) -> float:
        """Score approach based on rationale quality"""
        rationale = agent.get("rationale", "")
        score = 0.0
        
        # More specific rationale = higher score
        if "because" in rationale.lower():
            score += 0.3
        if "trade-off" in rationale.lower():
            score += 0.2
        if "tested" in rationale.lower() or "proven" in rationale.lower():
            score += 0.3
        if len(rationale) > 100:
            score += 0.2
        
        return min(score, 1.0)
    
    def get_conflict_report(self) -> str:
        """Report conflicts that have occurred"""
        if not self.conflict_log:
            return "No conflicts recorded."
        
        lines = ["=== Conflict Report ==="]
        for i, conflict in enumerate(self.conflict_log, 1):
            lines.append(
                f"\n#{i} [{conflict['type'].value}] "
                f"Agents: {conflict['agents']} "
                f"→ Resolution: {conflict.get('resolution', conflict.get('winner', 'N/A'))}"
            )
        
        return "\n".join(lines)
```

</details>

---

## 6. Agent Selection Guide

> **📌 Core Concept**
>
> - **Concept:** The Agent Selection Guide is a set of criteria for deciding when to use multi-agent and when a single agent is enough, based on task complexity, token cost, and specialization requirements.
> - **Analogy/comparison:** Like choosing transportation: walk for short distances (single-agent), hire a team only for far-and-many jobs (multi-agent). Driving 100 meters just to save effort is a pointless expense.
> - **Why it matters:** Using multi-agent for a simple task only wastes tokens and adds slowness — the guide helps you avoid over-engineering.

### 6.1 When to Use Multi-Agent

This is a question-branch decision diagram: start from the task, answer each question (can a single agent handle it? are the jobs independent? is there a clear pipeline? is discussion needed? many sub-tasks?), and every "Yes" leads to a suitable architecture. At the bottom of the diagram is a token estimation table for each system type. The metaphor: like a "which exit to take" quiz — each answer sends you down the right turn.

```
┌──────────────────────────────────────────────────────────────────┐
│           MULTI-AGENT DECISION GUIDE                              │
│                                                                  │
│  Task arrives                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Single agent can │──────────►│ USE SINGLE AGENT  │           │
│  │ handle it?       │          │ (simpler, cheaper) │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Tasks are        │──────────►│ PARALLEL FAN-OUT  │           │
│  │ independent?     │          │ (max throughput)   │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Clear pipeline?  │──────────►│ SEQUENTIAL        │           │
│  │ (Plan→Code→Test) │          │ PIPELINE          │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Need multi-turn  │──────────►│ NEGOTIATION       │           │
│  │ discussion?      │          │ PATTERN           │           │
│  └────────┬─────────┘          └──────────────────┘           │
│           │ NO                                                  │
│           ▼                                                      │
│  ┌──────────────────┐     YES    ┌──────────────────┐           │
│  │ Complex, many    │──────────►│ HIERARCHICAL      │           │
│  │ sub-tasks?       │          │ (Manager/Workers)  │           │
│  └──────────────────┘          └──────────────────┘           │
│                                                                  │
│  COST COMPARISON:                                                │
│  • Single agent:     ~5K-20K tokens per task                    │
│  • 2 agents:         ~10K-40K tokens (2x base)                 │
│  • Pipeline:         ~15K-60K tokens (3x base)                 │
│  • Hierarchical:     ~20K-80K tokens (4x base)                 │
│  • But: Quality may improve 20-40% with specialist agents      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Real-World Implementations

> **📌 Core Concept**
>
> - **Concept:** Real-World Implementations are multi-agent examples applied in production — a code review pipeline, a feature development team, a debug squad — showing how roles are assigned and communication flows set up concretely.
> - **Analogy/comparison:** Like watching a software company's actual workflow: who reviews, who writes code, who tests — instead of just reading dry theory.
> - **Why it matters:** Real examples give you a battle-tested design to "copy" and adapt, so you don't have to fumble your way from scratch.

### 7.1 Code Review Pipeline

This code builds an automated review pipeline the way a software company would: collect changed files → review code → security review → performance review → merge feedback. How to "read" it: each task in the `tasks` list has a `depends_on` field that decides which job must wait for which. The metaphor: like a real merge-request workflow where 2-3 reviewers have to click Approve before the merge.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class CodeReviewPipeline:
    """
    Multi-agent code review pipeline:
    1. Git Manager collects changed files
    2. Coder provides context
    3. Reviewer analyzes code
    4. Security Auditor checks vulnerabilities
    5. Orchestrator merges feedback
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.SEQUENTIAL
        )
        
        # Register agents
        self.orchestrator.register_agent(
            "git-mgr", AgentRole.GIT_MANAGER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
        self.orchestrator.register_agent(
            "security", AgentRole.SECURITY_AUDITOR
        )
        self.orchestrator.register_agent(
            "perf", AgentRole.PERFORMANCE_ANALYST
        )
    
    def review(self, pr_description: str, 
               changed_files: List[str]) -> Dict:
        """Execute full code review pipeline"""
        tasks = [
            {
                "id": "collect-context",
                "type": "code",
                "input": {
                    "action": "read_files",
                    "files": changed_files,
                },
                "depends_on": [],
            },
            {
                "id": "code-review",
                "type": "review",
                "input": {"description": pr_description},
                "depends_on": ["collect-context"],
            },
            {
                "id": "security-review",
                "type": "security",
                "input": {"files": changed_files},
                "depends_on": ["collect-context"],
            },
            {
                "id": "perf-review",
                "type": "review",
                "input": {"target": "performance"},
                "depends_on": ["collect-context"],
            },
            {
                "id": "merge-feedback",
                "type": "plan",
                "input": {
                    "combine": [
                        "code-review",
                        "security-review",
                        "perf-review"
                    ]
                },
                "depends_on": [
                    "code-review", 
                    "security-review", 
                    "perf-review"
                ],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
```

</details>

### 7.2 Feature Development Team

This code simulates a complete feature development team in **hierarchical** style: the Architect designs first → multiple Coders work on independent modules in parallel → the Tester writes tests → the Reviewer finalizes quality. Notable point: `implement-core` and `implement-api` both depend on `design` but not on each other, so they can run in parallel. The metaphor: like a house-building crew — the electrician and the plumber work at the same time, but both wait for the blueprints.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class FeatureDevTeam:
    """
    Multi-agent feature development:
    1. Architect designs the approach
    2. Coder implements (parallel for independent modules)
    3. Tester writes & runs tests
    4. Reviewer validates quality
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.HIERARCHICAL
        )
        
        self.orchestrator.register_agent(
            "architect", AgentRole.ARCHITECT
        )
        self.orchestrator.register_agent(
            "coder-1", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "coder-2", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "tester", AgentRole.TESTER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
    
    def develop_feature(self, feature_spec: str) -> Dict:
        """Develop a feature with a multi-agent team"""
        tasks = [
            {
                "id": "design",
                "type": "architect",
                "input": {"spec": feature_spec},
                "depends_on": [],
            },
            {
                "id": "implement-core",
                "type": "code",
                "input": {"module": "core"},
                "depends_on": ["design"],
            },
            {
                "id": "implement-api",
                "type": "code",
                "input": {"module": "api"},
                "depends_on": ["design"],
            },
            {
                "id": "write-tests",
                "type": "test",
                "input": {"target": "all"},
                "depends_on": ["implement-core", "implement-api"],
            },
            {
                "id": "review",
                "type": "review",
                "input": {},
                "depends_on": ["write-tests"],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
```

</details>

### 7.3 Debug Squad

This code assembles a 4-step sequential "incident response team": the Debugger finds the root cause → the Coder fixes it → the Tester runs regression tests → the Reviewer rechecks quality. Each step depends on the previous one (via `depends_on`), so the flow runs in the correct order: catch the bug, patch it, verify, approve. The metaphor: like an incident-handling process in a company — support diagnoses, the engineer fixes, QA confirms, the lead approves.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class DebugSquad:
    """
    Multi-agent debugging:
    1. Debugger reproduces and investigates
    2. Coder implements fix
    3. Tester verifies fix + regression tests
    4. Reviewer ensures fix quality
    """
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator(
            mode=OrchestrationMode.SEQUENTIAL
        )
        
        self.orchestrator.register_agent(
            "debugger", AgentRole.DEBUGGER
        )
        self.orchestrator.register_agent(
            "coder", AgentRole.CODER
        )
        self.orchestrator.register_agent(
            "tester", AgentRole.TESTER
        )
        self.orchestrator.register_agent(
            "reviewer", AgentRole.CODE_REVIEWER
        )
    
    def debug_and_fix(self, error_report: str) -> Dict:
        """Debug and fix an issue"""
        tasks = [
            {
                "id": "investigate",
                "type": "debug",
                "input": {"error": error_report},
                "depends_on": [],
            },
            {
                "id": "fix",
                "type": "code",
                "input": {"action": "implement_fix"},
                "depends_on": ["investigate"],
            },
            {
                "id": "test-fix",
                "type": "test",
                "input": {"action": "regression_test"},
                "depends_on": ["fix"],
            },
            {
                "id": "review-fix",
                "type": "review",
                "input": {"action": "review_fix"},
                "depends_on": ["test-fix"],
            },
        ]
        
        return self.orchestrator.execute_pipeline(tasks)
```

</details>

---

## 8. Debugging Multi-Agent Systems

> **📌 Core Concept**
>
> - **Concept:** Debugging Multi-Agent Systems is the process of tracing fault causes in a system of interacting agents — communication errors, out-of-sync state, conflicting results — using logging, tracing, and isolating individual components.
> - **Analogy/comparison:** Like finding a leak in a multi-story building: you must inspect each pipe (message log), each floor (agent state), and each timer (timeline) instead of just guessing.
> - **Why it matters:** Multi-agent faults rarely sit inside one agent — they usually live "between" agents, so dedicated tracing tools are needed.

### 8.1 Debug Strategy

This diagram is a multi-agent "diagnostic manual": for each symptom (agent not responding, task routed to the wrong agent, infinite loop, conflicting results, poor quality) it lists the steps to check ("Check") and then points to the remedy ("Fix"). How to use it: match the symptom you're seeing, follow the check branch until you find the root cause. The metaphor: like a mechanic diagnosing a car — out of oil? Out of gas? Bad spark plug? Eliminate possibilities one by one.

```
┌──────────────────────────────────────────────────────────────────┐
│          DEBUGGING MULTI-AGENT SYSTEMS                            │
│                                                                  │
│  SYMPTOM 1: Agent not responding                                 │
│  ├── Check: Message queue empty?                                 │
│  ├── Check: Agent registered with router?                        │
│  ├── Check: Token budget exhausted?                              │
│  └── Fix: Restart agent, check message format                    │
│                                                                  │
│  SYMPTOM 2: Wrong agent handling task                            │
│  ├── Check: Task type → role mapping correct?                    │
│  ├── Check: Agent role definition matches?                       │
│  └── Fix: Update routing logic, verify role assignments          │
│                                                                  │
│  SYMPTOM 3: Infinite loop between agents                         │
│  ├── Check: Circular dependencies in pipeline?                   │
│  ├── Check: Negotiation without convergence?                     │
│  ├── Check: Missing termination condition?                       │
│  └── Fix: Add max iterations, timeout, convergence check         │
│                                                                  │
│  SYMPTOM 4: Conflicting outputs                                  │
│  ├── Check: Shared state consistency?                            │
│  ├── Check: File lock contention?                                │
│  └── Fix: Add conflict resolution, merge strategy                │
│                                                                  │
│  SYMPTOM 5: Poor quality output                                  │
│  ├── Check: System prompts clear enough?                         │
│  ├── Check: Context passed between agents complete?              │
│  ├── Check: Right agent for the task?                            │
│  └── Fix: Improve prompts, add validation step                   │
│                                                                  │
│  DEBUGGING TOOLS:                                                │
│  • Message log analysis (trace message flow)                     │
│  • Agent state inspection (what each agent knows)                │
│  • Execution timeline (what happened when)                       │
│  • Token usage per agent (identify bottlenecks)                  │
│  • Conflict report (what conflicts occurred)                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Debug Logger

This code is the "replay the game footage" toolkit for multi-agent: `trace_message_flow` replays every message between agents over time, `inspect_agent_state` shows what a single agent currently knows, and `generate_timeline` reconstructs the sequence of events. When the system misbehaves, this is where you see "who said what, did what, when". The metaphor: like checking the security camera to find out who bumped into whom.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class MultiAgentDebugger:
    """Debug utilities for multi-agent systems"""
    
    def __init__(self, orchestrator: AgentOrchestrator):
        self.orchestrator = orchestrator
        self.trace_log: List[Dict] = []
    
    def trace_message_flow(self) -> str:
        """Trace the entire message flow between agents"""
        messages = self.orchestrator.router.message_log
        
        lines = ["=== Message Flow Trace ==="]
        for msg in messages:
            direction = "→" if msg.message_type in [
                MessageType.TASK_ASSIGN, MessageType.REQUEST_INFO
            ] else "←"
            lines.append(
                f"  {msg.from_agent} {direction} {msg.to_agent} "
                f"[{msg.message_type.value}] "
                f"at {msg.timestamp}"
            )
        
        return "\n".join(lines)
    
    def inspect_agent_state(self, agent_id: str) -> str:
        """Inspect the state of one agent"""
        agent = self.orchestrator.agents.get(agent_id, {})
        memory = self.orchestrator.router.peek(agent_id)
        
        lines = [
            f"=== Agent: {agent_id} ===",
            f"Role: {agent.get('role', 'unknown')}",
            f"Status: {agent.get('status', 'unknown')}",
            f"Tasks completed: {agent.get('tasks_completed', 0)}",
            f"Errors: {agent.get('errors', 0)}",
            f"Pending messages: {len(memory)}",
        ]
        
        return "\n".join(lines)
    
    def generate_timeline(self) -> str:
        """Create an execution timeline"""
        log = self.orchestrator.execution_log
        
        lines = ["=== Execution Timeline ==="]
        for entry in log:
            status_icon = "✓" if entry["status"] == "success" else "✗"
            lines.append(
                f"  [{entry.get('attempt', 1)}] {status_icon} "
                f"{entry['task_id']} → {entry['agent_id']}"
            )
        
        return "\n".join(lines)
```

</details>

---

## 9. Performance Optimization

> **📌 Core Concept**
>
> - **Concept:** Performance Optimization is the set of techniques that reduce latency and cost for a multi-agent system — more parallelism, fewer redundant messages, caching, token estimation — so the system responds faster and costs less.
> - **Analogy/comparison:** Like optimizing a factory: cut unnecessary middle stages, let independent production lines run in parallel instead of one after another.
> - **Why it matters:** Multi-agent already costs 2-5× the tokens — without optimization, operating costs climb very quickly.

### 9.1 Optimization Strategies

A list of 5 optimization strategies for multi-agent systems: reduce tokens, maximize parallelism, reduce communication, keep the team just big enough, and cache for reuse. Each strategy is a "practical trick" you can apply right away, without any complex tooling. The metaphor: like cleaning out a warehouse — remove the excess (tokens), arrange things so people can work in parallel, and keep frequently used items where they're easy to grab (cache).

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT PERFORMANCE OPTIMIZATION                      │
│                                                                  │
│  1. REDUCE TOKEN USAGE                                           │
│     • Pass summaries between agents, not full context            │
│     • Use structured messages (JSON), not prose                  │
│     • Cache common context (project structure, conventions)      │
│     • Limit agent memory to relevant information                 │
│                                                                  │
│  2. MAXIMIZE PARALLELISM                                         │
│     • Identify independent tasks early                           │
│     • Fan-out independent work to multiple agents                │
│     • Use async message passing                                  │
│     • Don't serialize what can be parallel                       │
│                                                                  │
│  3. MINIMIZE COMMUNICATION                                       │
│     • Batch messages instead of many small ones                  │
│     • Use shared memory for frequently accessed data             │
│     • Define clear interfaces between agents                     │
│     • Avoid unnecessary back-and-forth                            │
│                                                                  │
│  4. RIGHT-SIZE AGENTS                                            │
│     • Don't over-specialize (too many agents = overhead)         │
│     • Match agent capability to task complexity                  │
│     • Use single agent for simple tasks                          │
│     • Reserve multi-agent for genuinely complex work             │
│                                                                  │
│  5. CACHE AND REUSE                                              │
│     • Cache file reads across agents                             │
│     • Reuse analysis results                                     │
│     • Share test fixtures                                        │
│     • Persist decisions (don't re-derive)                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Cost Estimation

A "token budget" estimation table for multi-agent: cost = cost per agent × number of agents × communication cost. It prices out each role (orchestrator ~2K, coder ~5K tokens...), adds the "post office fee" (messages, handoffs, conflicts), then gives you typical scenarios. The metaphor: like estimating a project's cost — once you know the price of each line item, you can predict the total spend.

```
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-AGENT COST ESTIMATION                          │
│                                                                  │
│  Cost = Base Agent Cost × Number of Agents × Communication      │
│                                                                  │
│  Base Cost per Agent (avg tokens per task):                      │
│  ├── Orchestrator:  2,000 tokens (planning + routing)           │
│  ├── Coder:         5,000 tokens (reading + writing code)       │
│  ├── Reviewer:      3,000 tokens (reading + feedback)           │
│  ├── Tester:        4,000 tokens (writing + running tests)      │
│  ├── Debugger:      4,000 tokens (investigating + fixing)       │
│  └── DevOps:        3,000 tokens (config + deployment)          │
│                                                                  │
│  Communication Overhead:                                         │
│  ├── Message passing:  200-500 tokens per message               │
│  ├── Context transfer: 1,000-3,000 tokens per handoff           │
│  └── Conflict resolution: 1,000-2,000 tokens per conflict       │
│                                                                  │
│  Typical Scenarios:                                              │
│  ├── Simple feature (1 agent):     5,000 tokens                 │
│  ├── Code review (2 agents):       8,000 tokens                 │
│  ├── Feature dev (3 agents):      20,000 tokens                 │
│  ├── Complex project (5 agents):  50,000 tokens                 │
│  └── Full team (7 agents):        80,000 tokens                 │
│                                                                  │
│  ROI Consideration:                                              │
│  • Multi-agent costs 2-5x more in tokens                         │
│  • But may produce 20-40% better quality                         │
│  • Best ROI: Code review, security audit, testing                │
│  • Worst ROI: Simple tasks, documentation                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Anti-Patterns & Solutions

> **📌 Core Concept**
>
> - **Concept:** Anti-Patterns & Solutions is a collection of common design mistakes in multi-agent systems — overlapping roles, agents that "chat" too much, single points of dependency — together with how to avoid and fix them.
> - **Analogy/comparison:** Like a distilled "don'ts" list from experience: knowing the traps other people fall into means you won't repeat them.
> - **Why it matters:** Most multi-agent systems fail because of these anti-patterns, not because the model is weak.

### 10.1 Common Anti-Patterns

A list of 8 "traps" that almost everyone who builds multi-agent systems has stepped in — too many agents, agents talking too much, single points of dependency, unclear roles... — each trap comes with its solution right on the "→ SOLUTION" line. How to use it: check your project against each trap, and if you hit one, apply the fix. The metaphor: like a "check before confirming the order" list — knowing where things go wrong beats patching things later.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT ANTI-PATTERNS                                 │
│                                                                  │
│  ❌ ANTI-PATTERN 1: OVER-ENGINEERING                             │
│     Using 5 agents for a task that needs 1                      │
│     → SOLUTION: Start with single agent, add only if needed     │
│                                                                  │
│  ❌ ANTI-PATTERN 2: CHATTY AGENTS                                │
│     Agents exchange 20+ messages for simple coordination         │
│     → SOLUTION: Batch communication, use shared memory          │
│                                                                  │
│  ❌ ANTI-PATTERN 3: SINGLE POINT OF FAILURE                      │
│     All agents depend on one orchestrator                        │
│     → SOLUTION: Add fallback routing, health checks             │
│                                                                  │
│  ❌ ANTI-PATTERN 4: UNCLEAR RESPONSIBILITIES                     │
│     Multiple agents try to do the same thing                    │
│     → SOLUTION: Strict role definitions, task routing           │
│                                                                  │
│  ❌ ANTI-PATTERN 5: NO CONFLICT RESOLUTION                       │
│     Agents modify same file, corrupt each other's work          │
│     → SOLUTION: File locking, conflict resolution manager       │
│                                                                  │
│  ❌ ANTI-PATTERN 6: TOKEN BOMB                                   │
│     Communication overhead exceeds task execution cost          │
│     → SOLUTION: Monitor token ratio, simplify messages          │
│                                                                  │
│  ❌ ANTI-PATTERN 7: INFINITE NEGOTIATION                         │
│     Agents debate forever without reaching consensus            │
│     → SOLUTION: Max rounds limit, authority fallback            │
│                                                                  │
│  ❌ ANTI-PATTERN 8: LOST CONTEXT                                 │
│     Agent B doesn't know what Agent A decided                   │
│     → SOLUTION: Shared decision log, context handoff protocol   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 11. Production Deployment

> **📌 Core Concept**
>
> - **Concept:** Production Deployment is the process of putting a multi-agent system into real operation — ensuring readiness, monitoring, security, and scalability — with a checklist to run before going live.
> - **Analogy/comparison:** Like putting a building into use: before opening, you must check the electrical and water systems, fire alarms, and who does what when something fails — you can't just hand over the keys and start living there.
> - **Why it matters:** A system that works fine in the lab can fall over the moment it hits production without monitoring and failure-handling procedures.

### 11.1 Deployment Checklist

This checklist splits into 3 phases before a multi-agent system goes to production: **preparation** (clear roles, tested routing, conflict handling, token limits...), **monitoring** (tokens, latency, conflicts...) and **continuous optimization**. How to use it: check each box; any box that stays unchecked means the system is not yet ready to run for real. The metaphor: like the pre-flight checklist — missing one small item can lead to a big incident.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT PRODUCTION CHECKLIST                          │
│                                                                  │
│  BEFORE DEPLOYMENT:                                              │
│  □ All agents have clear role definitions                        │
│  □ Message routing is tested                                     │
│  □ Conflict resolution is implemented                            │
│  □ Token budget limits are set                                   │
│  □ Error handling and retry logic in place                       │
│  □ Logging and monitoring configured                             │
│  □ Cost estimation reviewed                                      │
│                                                                  │
│  MONITORING:                                                     │
│  □ Token usage per agent (track anomalies)                       │
│  □ Message latency (detect bottlenecks)                          │
│  □ Conflict frequency (identify problematic pairs)               │
│  □ Task completion rate (measure effectiveness)                  │
│  □ Error rates per agent (find weak links)                       │
│                                                                  │
│  OPTIMIZATION:                                                   │
│  □ Review token usage weekly                                     │
│  □ Identify unnecessary agent communication                      │
│  □ Cache frequently accessed context                              │
│  □ Right-size team (remove underperforming agents)               │
│  □ Update prompts based on failure analysis                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

> **📌 Core Concept**
>
> - **Concept:** Best Practices are the foundational principles distilled from building multi-agent systems — start simple, keep roles clear, communicate in a structured way, design defensively, and track cost.
> - **Analogy/comparison:** Like a veteran team's code of conduct — they know what makes a project succeed because they've stumbled a great many times.
> - **Why it matters:** Applying them from the start costs far less than repairing a system after it has grown big.

```
┌──────────────────────────────────────────────────────────────────┐
│           MULTI-AGENT BEST PRACTICES                              │
│                                                                  │
│  1. START SIMPLE                                                 │
│     Single agent first → add agents only when needed            │
│     Each new agent must justify its overhead                     │
│                                                                  │
│  2. CLEAR ROLES                                                  │
│     Every agent has ONE primary responsibility                   │
│     Document what each agent does and doesn't do                │
│                                                                  │
│  3. STRUCTURED COMMUNICATION                                     │
│     Use standard message format (not free-form)                  │
│     Pass summaries, not raw data between agents                  │
│                                                                  │
│  4. EXPLICIT HANDOFFS                                            │
│     Clear contract: what sender provides, receiver expects      │
│     Validate inputs before processing                            │
│                                                                  │
│  5. DEFENSIVE DESIGN                                             │
│     Handle agent failures gracefully                             │
│     Never assume another agent's output is correct              │
│                                                                  │
│  6. MONITOR TOKEN COST                                           │
│     Track tokens per agent, per task                             │
│     Set budgets, alert on overruns                               │
│                                                                  │
│  7. LOG EVERYTHING                                               │
│     Message flow, decisions, conflicts                           │
│     Enables debugging and optimization                           │
│                                                                  │
│  8. TEST THE SYSTEM                                              │
│     Unit test individual agents                                  │
│     Integration test agent interactions                          │
│     Chaos test agent failures                                    │
│                                                                  │
│  9. ITERATE AND IMPROVE                                          │
│     Review failure cases regularly                               │
│     Tune prompts based on output quality                         │
│     Add/remove agents based on actual needs                      │
│                                                                  │
│  10. KNOW WHEN NOT TO                                           │
│      Multi-agent is NOT always better                            │
│      Simple tasks → single agent                                 │
│      Complex coordination → multi-agent                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 12. Case Studies — Real-World Multi-Agent Architectures

> **📌 Core Concept**
>
> - **Concept:** Case Studies are analyses of the multi-agent architectures of famous real systems — Claude Code, Devin, OpenHands — to extract lessons on role design, workflows, and how to pick an architecture.
> - **Analogy/comparison:** Like studying the tactical diagrams of top football teams before building your own lineup.
> - **Why it matters:** Learning from systems that already run in production means you don't have to "reinvent the wheel".

### 12.1 Claude Code — Anthropic's Multi-Agent Architecture

Claude Code uses a complex multi-agent pattern with planner, coder, and reviewer agents that coordinate through shared context.

```
┌──────────────────────────────────────────────────────────────────┐
│         CLAUDE CODE MULTI-AGENT ARCHITECTURE                      │
│                                                                  │
│  User Request                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────────┐                                            │
│  │  PLANNER AGENT   │  Analyzes task, creates plan              │
│  │  (Claude 3.5)    │  Outputs: ordered subtask list            │
│  └────────┬─────────┘  Max tokens: ~2K                          │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  CODING AGENT    │  Executes each subtask                    │
│  │  (Claude 3.5)    │  Tools: read_file, write_to_file          │
│  │                  │  Tool: search_files, execute_command       │
│  │  ┌────────────┐  │  Iterates until task complete             │
│  │  │ Edit Loop  │  │  Max iterations: 20-50                    │
│  │  │ Read→Edit  │  │  Token budget: ~100K per task             │
│  │  │ →Verify    │  │                                           │
│  │  └────────────┘  │                                           │
│  └────────┬─────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  REVIEW AGENT    │  Validates output quality                 │
│  │  (Same model)    │  Checks: correctness, style, safety       │
│  │                  │  Can reject and send back for fix          │
│  └────────┬─────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                            │
│  │  COORDINATOR     │  Manages state, handles errors            │
│  │  (System code)   │  Tracks progress, manages context         │
│  │                  │  Handles tool permissions & safety         │
│  └──────────────────┘                                            │
│                                                                  │
│  Key Insight: Multiple agents share SAME model but              │
│  different system prompts → different behaviors                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.2 Devin — Autonomous Software Engineering Agent

Devin (Cognition AI) uses a multi-agent pattern with specialized modules:

```
┌──────────────────────────────────────────────────────────────────┐
│              DEVIN AGENT ARCHITECTURE                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CORE BRAIN (LLM)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │ Planning   │  │ Reasoning  │  │ Reflection │         │   │
│  │  │ Module     │  │ Module     │  │ Module     │         │   │
│  │  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘         │   │
│  └─────────┼───────────────┼───────────────┼────────────────┘   │
│            │               │               │                     │
│  ┌─────────▼───────────────▼───────────────▼────────────────┐   │
│  │                 TOOL USE LAYER                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │ Code     │ │ Browser  │ │ Terminal │ │ Planner  │   │   │
│  │  │ Editor   │ │          │ │          │ │          │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 ENVIRONMENT (Sandbox)                     │   │
│  │  Full VM with: codebase, browser, terminal               │   │
│  │  Agent has full autonomy to read, write, test, deploy    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.3 OpenHands (OpenDevin) — Open-Source Multi-Agent

This code simulates the OpenHands/Devin-style architecture: a **central brain (LLM)** decides actions in a **observe → decide → act → observe again** loop (visible in `run_agent_loop`), living in a safe **sandbox** and automatically retrying on errors. How to read it: focus on the `run_agent_loop` function — that is the heart of the whole pattern. The metaphor: like a chess player who looks at the board between moves, evaluating the result before each next move.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# OpenHands architecture pattern — simplified implementation
# Based on open-source OpenHands (formerly OpenDevin) architecture

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field

@dataclass
class AgentConfig:
    """Configuration for one agent in a multi-agent system"""
    name: str
    model: str
    system_prompt: str
    tools: List[str]
    max_iterations: int = 20
    max_tokens: int = 100000
    temperature: float = 0.0


class OpenHandsStyleOrchestrator:
    """
    Multi-agent orchestrator in the OpenHands/Devin style.
    
    Key patterns:
    - Central brain (LLM) decides actions
    - Sandbox environment for safe execution
    - Iterative read→act→observe cycle
    - Conversation memory across iterations
    - Automatic retry on failure
    """
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.sandbox_state: Dict = {
            "files": {},
            "env_vars": {},
            "processes": [],
        }
        self.tool_registry: Dict[str, Callable] = {}
        self.metrics = {
            "total_tokens": 0,
            "total_actions": 0,
            "files_modified": set(),
            "errors": 0,
        }
    
    def register_tool(self, name: str, func: Callable):
        """Register a tool for the agent to use"""
        self.tool_registry[name] = func
    
    def run_agent_loop(self, task: str, config: AgentConfig,
                       llm_func: Callable) -> Dict:
        """
        Main agent loop — core execution cycle:
        1. LLM observes state
        2. LLM decides action
        3. System executes action
        4. System observes result
        5. Repeat until done or max iterations
        """
        self.conversation_history.append({
            "role": "user",
            "content": task,
        })
        
        for iteration in range(config.max_iterations):
            # 1. Build context for LLM
            context = self._build_context(config)
            
            # 2. Get LLM action
            action = llm_func(context)
            self.metrics["total_actions"] += 1
            
            # 3. Parse action
            parsed = self._parse_action(action)
            
            # 4. Execute action
            if parsed["type"] == "finish":
                return {
                    "status": "completed",
                    "iterations": iteration + 1,
                    "metrics": self.metrics,
                    "result": parsed.get("output", ""),
                }
            
            if parsed["type"] == "error":
                self.metrics["errors"] += 1
                if self.metrics["errors"] > 3:
                    return {
                        "status": "failed",
                        "reason": "Too many errors",
                        "iterations": iteration + 1,
                        "metrics": self.metrics,
                    }
                continue
            
            # Execute tool
            result = self._execute_tool(parsed)
            
            # 5. Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": action,
            })
            self.conversation_history.append({
                "role": "environment",
                "content": f"Tool result: {result}",
            })
        
        return {
            "status": "max_iterations",
            "iterations": config.max_iterations,
            "metrics": self.metrics,
        }
    
    def _build_context(self, config: AgentConfig) -> str:
        """Build context for the LLM call"""
        parts = [config.system_prompt]
        
        # Add sandbox state summary
        parts.append(f"\nSandbox state: {len(self.sandbox_state['files'])} files")
        
        # Add conversation history (limited)
        recent = self.conversation_history[-20:]  # Last 20 messages
        for msg in recent:
            parts.append(f"{msg['role']}: {msg['content'][:500]}")
        
        # Add available tools
        parts.append(f"\nAvailable tools: {list(self.tool_registry.keys())}")
        
        return "\n".join(parts)
    
    def _parse_action(self, action: str) -> Dict:
        """Parse LLM action output"""
        if "FINISH" in action.upper():
            return {"type": "finish", "output": action}
        elif "ERROR" in action.upper():
            return {"type": "error", "message": action}
        else:
            return {"type": "tool_use", "tool": "default", "args": action}
    
    def _execute_tool(self, parsed: Dict) -> str:
        """Execute tool call"""
        tool_name = parsed.get("tool", "default")
        if tool_name in self.tool_registry:
            try:
                result = self.tool_registry[tool_name](parsed.get("args", ""))
                return str(result)[:2000]  # Limit output size
            except Exception as e:
                return f"Tool error: {str(e)}"
        return f"Unknown tool: {tool_name}"
```

</details>

---

## 13. Advanced Multi-Agent Patterns

> **📌 Core Concept**
>
> - **Concept:** Advanced Multi-Agent Patterns are refined architectural patterns — MapReduce, Debate, Critique-Revision, Ensemble — that use multiple agents in parallel to push quality far beyond what a single agent can achieve.
> - **Analogy/comparison:** Like organizing a competition round: give several people the same job and pick the best entry (ensemble), or have them critique each other before settling on an approach (debate).
> - **Why it matters:** This is the family of patterns that reduces hallucination and increases reliability when quality is the top priority.

### 13.1 MapReduce Pattern for Code Generation

MapReduce is the "divide and conquer" pattern: **MAP** splits a big task into independent sub-tasks that multiple agents process in parallel, and **REDUCE** merges the results into a final output. In the code, `parallel_code_generation` is an example of generating code for many modules at once and then merging them. How to read it: if your task splits into independent parts — map-reduce fits; if the parts depend on each other — it does not. The metaphor: like cooking a feast — many chefs cook many dishes in parallel, then everything lands on the same table.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Dict, List, Callable

class MapReduceCodeGenerator:
    """
    MapReduce pattern applied to code generation.
    
    MAP: Split the task into sub-tasks → each agent processes one sub-task
    REDUCE: Merge results from all agents into a final output
    
    Pros:
    - Speed: sub-tasks run in parallel
    - Scalability: more agents = more throughput
    - Quality: each agent focuses on one part
    
    Cons:
    - Merging results can be complex
    - Not suitable for tasks with high dependency
    """
    
    def __init__(self):
        self.mapper_agents: List[Dict] = []
        self.reducer_agent: Dict = {}
        self.merge_strategy: str = "concatenate"
    
    def map_reduce(self, task: Dict, 
                   map_func: Callable,
                   reduce_func: Callable) -> Dict:
        """
        Execute the MapReduce pattern.
        
        task: {
            "description": str,
            "subtasks": [{"id": str, "input": Dict}],
        }
        """
        # MAP PHASE
        map_results = []
        for subtask in task["subtasks"]:
            result = map_func(subtask)
            map_results.append({
                "subtask_id": subtask["id"],
                "result": result,
            })
        
        # REDUCE PHASE
        reduced = reduce_func(map_results)
        
        return {
            "map_results": map_results,
            "final_output": reduced,
            "subtasks_completed": len(map_results),
        }
    
    def parallel_code_generation(self, modules: List[Dict],
                                  coder_func: Callable) -> Dict:
        """
        Generate code for multiple modules in parallel.
        
        modules: [{"name": "auth", "spec": "..."}, 
                  {"name": "api", "spec": "..."},
                  {"name": "db", "spec": "..."}]
        """
        # MAP: Each coder generates one module
        results = []
        for module in modules:
            code = coder_func(module)
            results.append({
                "module": module["name"],
                "code": code,
                "lines": len(code.split("\n")),
            })
        
        # REDUCE: Merge all modules
        merged_code = self._merge_modules(results)
        
        # Generate imports/connectors
        imports = self._generate_imports(results)
        
        return {
            "modules": results,
            "merged_code": merged_code,
            "imports": imports,
            "total_lines": sum(r["lines"] for r in results),
        }
    
    def _merge_modules(self, results: List[Dict]) -> str:
        """Merge code from multiple modules"""
        parts = []
        for r in results:
            parts.append(f"# === Module: {r['module']} ===")
            parts.append(r["code"])
            parts.append("")
        return "\n".join(parts)
    
    def _generate_imports(self, results: List[Dict]) -> str:
        """Automatically generate import statements"""
        module_names = [r["module"] for r in results]
        imports = []
        for name in module_names:
            imports.append(f"from .{name} import *")
        return "\n".join(imports)
```

</details>

### 13.2 Debate Pattern — Multi-Agent Discussion

The debate pattern lets multiple agents "argue" their way to a more reliable decision: round 1 each agent states its position, round 2 they rebut the opponents, round 3 they wrap up, and then a **judge agent** scores who was most persuasive. How to read it: `_judge_decision` scores based on the number of arguments and content length — a simple simulation of the principle that "a good argument wins". The metaphor: like a review committee before approving a loan — listen to all sides, then decide.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class DebateProtocol:
    """
    Debate pattern — multiple agents debate to reach consensus.
    
    Each agent presents its own position,
    then the agents rebut one another,
    and finally a judge agent decides.
    
    Use when:
    - An important design decision is needed
    - No clear best approach exists
    - Diverse perspectives are required
    """
    
    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds
        self.debate_history: List[Dict] = []
        self.positions: Dict[str, str] = {}
    
    def conduct_debate(self, topic: str, 
                       agents: List[Dict],
                       judge: Dict) -> Dict:
        """
        Conduct a debate on one topic.
        
        agents: [{"id": str, "position": str, "arguments": [str]}]
        judge: {"id": str, "criteria": [str]}
        """
        # Round 1: Opening statements
        for agent in agents:
            self.positions[agent["id"]] = agent["position"]
            self.debate_history.append({
                "round": 1,
                "agent": agent["id"],
                "type": "opening",
                "content": agent["position"],
                "arguments": agent.get("arguments", []),
            })
        
        # Round 2: Rebuttals
        for i, agent in enumerate(agents):
            other_agents = [a for a in agents if a["id"] != agent["id"]]
            rebuttal_targets = [a["id"] for a in other_agents]
            
            self.debate_history.append({
                "round": 2,
                "agent": agent["id"],
                "type": "rebuttal",
                "targets": rebuttal_targets,
                "content": f"Rebutting arguments from {rebuttal_targets}",
            })
        
        # Round 3: Closing
        for agent in agents:
            self.debate_history.append({
                "round": 3,
                "agent": agent["id"],
                "type": "closing",
                "content": f"Final position: {agent['position']}",
            })
        
        # Judge decision
        decision = self._judge_decision(judge, agents)
        
        return {
            "topic": topic,
            "rounds": 3,
            "positions": self.positions,
            "winner": decision["winner"],
            "reasoning": decision["reasoning"],
            "full_debate": self.debate_history,
        }
    
    def _judge_decision(self, judge: Dict, 
                        agents: List[Dict]) -> Dict:
        """Judge decides the winner based on criteria"""
        # Simplified scoring
        scores = {}
        for agent in agents:
            score = 0
            # Count arguments as proxy for depth
            history_entries = [
                h for h in self.debate_history 
                if h["agent"] == agent["id"]
            ]
            for entry in history_entries:
                score += len(entry.get("arguments", []))
                score += len(entry.get("content", "")) / 100
            
            scores[agent["id"]] = score
        
        winner_id = max(scores, key=scores.get)
        
        return {
            "winner": winner_id,
            "scores": scores,
            "reasoning": f"Agent {winner_id} presented the most "
                        f"compelling case with strongest arguments.",
        }
```

</details>

### 13.3 Critique-Revision Pattern

This pattern simulates the exact "write - grade - fix" loop: the **Writer** writes code, the **Critic** gives feedback, the **Writer** revises based on it, repeating until quality reaches the threshold (`quality_threshold`) or the rounds run out. How to read it: the `iterate` loop is the learn-from-feedback mechanism — whichever round scores higher is the one that gets kept. The metaphor: like submitting a draft to an editor for feedback and revising it — a few rounds produce a better result than the first raw draft.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class CritiqueRevisionLoop:
    """
    Critique-Revision pattern — one agent writes, one agent gives
    feedback, repeated until a quality threshold is met.
    
    Iterative improvement loop:
    1. Writer generates code
    2. Critic reviews code
    3. Writer revises based on feedback
    4. Repeat until quality threshold met or max iterations
    
    Use when:
    - Code quality matters more than speed
    - Multiple perspectives are needed
    - Complex tasks need refinement
    """
    
    def __init__(self, max_iterations: int = 3,
                 quality_threshold: float = 0.8):
        self.max_iterations = max_iterations
        self.quality_threshold = quality_threshold
        self.history: List[Dict] = []
    
    def iterate(self, task: str, 
                writer_func: Callable,
                critic_func: Callable,
                quality_func: Callable) -> Dict:
        """
        Run the critique-revision loop.
        
        writer_func: function(task, feedback) -> code
        critic_func: function(code, task) -> feedback
        quality_func: function(code, task) -> float (0-1)
        """
        best_code = ""
        best_score = 0.0
        all_iterations = []
        
        feedback = ""  # No feedback for first iteration
        
        for i in range(self.max_iterations):
            # WRITE
            code = writer_func(task, feedback)
            
            # CRITIQUE
            critique = critic_func(code, task)
            
            # EVALUATE
            score = quality_func(code, task)
            
            iteration_data = {
                "iteration": i + 1,
                "code_preview": code[:200],
                "critique": critique[:200],
                "score": score,
            }
            all_iterations.append(iteration_data)
            self.history.append(iteration_data)
            
            # Track best
            if score > best_score:
                best_score = score
                best_code = code
            
            # Check threshold
            if score >= self.quality_threshold:
                return {
                    "status": "threshold_met",
                    "iterations": i + 1,
                    "final_code": code,
                    "final_score": score,
                    "all_iterations": all_iterations,
                }
            
            # Build feedback for next iteration
            feedback = f"Previous score: {score:.2f}. Critique: {critique}"
        
        return {
            "status": "max_iterations",
            "iterations": self.max_iterations,
            "final_code": best_code,
            "final_score": best_score,
            "all_iterations": all_iterations,
        }
```

</details>

### 13.4 Ensemble Pattern — Multiple Agents, Best Output

The ensemble pattern runs **multiple agents on the same task at the same time**, each producing its own result; a judge scores them all and picks the best output. It is like "ensembles" in machine learning — combining many different opinions to reduce risk. How to read it: note `_generate_recommendation` — if the agents agree (low variance), the result is trustworthy; if they strongly disagree, a closer review is needed. The metaphor: like drafting several versions before finalizing the last one — take the one done best.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class EnsemblePattern:
    """
    Ensemble pattern — run N agents in parallel,
    pick the best output.
    
    Like ensembles in ML:
    - Multiple diverse agents → diverse outputs
    - Judge/voting system → pick best
    - Reduces risk of single-agent failure
    
    Pros:
    - Higher quality ceiling
    - More robust (one agent fails, others compensate)
    - Diverse solutions → better exploration
    
    Cons:
    - N× cost
    - Need a good judge/voting mechanism
    """
    
    def __init__(self, n_agents: int = 3):
        self.n_agents = n_agents
    
    def run_ensemble(self, task: str,
                     agent_func: Callable,
                     judge_func: Callable) -> Dict:
        """
        Run N agents and pick the best output.
        
        agent_func: function(task) -> code
        judge_func: function(code, task) -> float
        """
        outputs = []
        
        for i in range(self.n_agents):
            output = agent_func(task)
            score = judge_func(output, task)
            
            outputs.append({
                "agent_index": i,
                "output": output,
                "score": score,
                "lines": len(output.split("\n")) if isinstance(output, str) else 0,
            })
        
        # Sort by score
        outputs.sort(key=lambda x: x["score"], reverse=True)
        
        best = outputs[0]
        worst = outputs[-1]
        
        return {
            "best_output": best["output"],
            "best_score": best["score"],
            "best_agent": best["agent_index"],
            "worst_score": worst["score"],
            "score_variance": self._variance([o["score"] for o in outputs]),
            "all_outputs": outputs,
            "recommendation": self._generate_recommendation(outputs),
        }
    
    def _variance(self, scores: List[float]) -> float:
        """Calculate the variance of the scores"""
        if len(scores) < 2:
            return 0.0
        mean = sum(scores) / len(scores)
        return sum((s - mean) ** 2 for s in scores) / len(scores)
    
    def _generate_recommendation(self, outputs: List[Dict]) -> str:
        """Recommend based on ensemble results"""
        scores = [o["score"] for o in outputs]
        variance = self._variance(scores)
        
        if variance < 0.01:
            return "Low variance: All agents agree. High confidence."
        elif variance < 0.05:
            return "Moderate variance: Minor differences. Best output likely reliable."
        else:
            return "High variance: Agents disagree significantly. Consider reviewing all outputs."
```

</details>

---

## 14. Multi-Agent Testing Strategies

> **📌 Core Concept**
>
> - **Concept:** Multi-Agent Testing Strategies are the methods for verifying a multi-agent system — routing tests, message tests, per-agent tests, interaction tests, chaos tests — to make sure the system behaves correctly and stays stable.
> - **Analogy/comparison:** Like testing a production line: test each machine (agent), test the whole line, even deliberately break one machine to see if the system stops.
> - **Why it matters:** Multi-agent systems often have "no individual fault but a systemic fault" — you need to test at several different levels.

### 14.1 Testing Multi-Agent Systems

This triangle shows that multi-agent testing happens at **many levels**, bottom-up: routing tests (does the task go to the right agent?), message tests (is the protocol standard?), per-agent tests, interaction tests between agents, and finally **chaos tests** — deliberately killing an agent to see if the system survives. How to read it: the lower levels are the foundation; do them well before moving up. The metaphor: like inspecting a building — check each brick, then test the whole structure before subjecting it to an earthquake.

```
┌──────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT TESTING PYRAMID                               │
│                                                                  │
│                        ┌──────────┐                              │
│                        │  Chaos   │  ← Kill agents mid-task     │
│                        │  Tests   │  ← Corrupt shared state     │
│                       ┌┴──────────┴┐                            │
│                       │ Integration │  ← Agent interactions     │
│                       │    Tests    │  ← Full pipeline runs     │
│                      ┌┴─────────────┴┐                         │
│                      │  Agent Tests   │  ← Individual agent     │
│                      │  (Unit equiv.) │  ← with mock tools      │
│                     ┌┴───────────────┴┐                        │
│                     │  Message Tests   │  ← Protocol correctness│
│                     │  (Contract)      │  ← Format validation   │
│                    ┌┴─────────────────┴┐                       │
│                    │  Routing Tests     │  ← Task → Agent mapping│
│                    │  (Logic)           │  ← Edge cases          │
│                    └───────────────────┘                        │
│                                                                  │
│  Each level tests different aspects:                             │
│  - Routing: Does the right agent get the right task?             │
│  - Messages: Are messages formatted correctly?                   │
│  - Agents: Does each agent produce quality output?               │
│  - Integration: Do agents work together?                         │
│  - Chaos: Does the system survive failures?                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 14.2 Test Implementation

This code comes with ready-made example tests: `test_routing_accuracy` checks whether tasks land on the correct agent, `test_agent_failure_recovery` "kills" one agent to see if the system keeps running, `test_token_budget_enforcement` checks the token limit, `test_conflict_resolution` checks file locking and reconciliation. How to use it: you can extend this very test suite for your own system. The metaphor: like the driving-test questions before you're allowed on the road — if any item FAILs, you're not ready yet.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class MultiAgentTestSuite:
    """
    Test suite for multi-agent systems.
    
    Categories:
    1. Unit tests for individual agents
    2. Integration tests for agent interactions
    3. Chaos tests for failure scenarios
    4. Performance tests for token/cost efficiency
    """
    
    def __init__(self):
        self.test_results: List[Dict] = []
    
    # === ROUTING TESTS ===
    
    def test_routing_accuracy(self, orchestrator: 'AgentOrchestrator',
                               test_cases: List[Dict]) -> Dict:
        """
        Test: task types route to the correct agents.
        
        test_cases: [{"task_type": str, "expected_role": AgentRole}]
        """
        correct = 0
        total = len(test_cases)
        
        for case in test_cases:
            task = {"id": "test", "type": case["task_type"]}
            agent_id = orchestrator._route_task(task)
            
            if agent_id:
                agent_role = orchestrator.agents[agent_id]["role"]
                if agent_role == case["expected_role"]:
                    correct += 1
                else:
                    self.test_results.append({
                        "test": "routing_accuracy",
                        "task_type": case["task_type"],
                        "expected": case["expected_role"].value,
                        "got": agent_role.value,
                        "status": "FAIL",
                    })
            else:
                self.test_results.append({
                    "test": "routing_accuracy",
                    "task_type": case["task_type"],
                    "expected": case["expected_role"].value,
                    "got": "no_agent",
                    "status": "FAIL",
                })
        
        return {
            "test": "routing_accuracy",
            "passed": correct,
            "total": total,
            "accuracy": correct / total if total else 0,
        }
    
    # === CHAOS TESTS ===
    
    def test_agent_failure_recovery(self, 
                                     orchestrator: 'AgentOrchestrator',
                                     failing_agent: str) -> Dict:
        """
        Test: the system still operates when one agent fails.
        """
        # Execute pipeline with failing agent
        tasks = [
            {"id": "task-1", "type": "code", "input": {}},
            {"id": "task-2", "type": "review", "input": {},
             "depends_on": ["task-1"]},
        ]
        
        # Simulate failure for specific agent
        original_status = orchestrator.agents.get(failing_agent, {}).get("status")
        if failing_agent in orchestrator.agents:
            orchestrator.agents[failing_agent]["status"] = "failed"
        
        result = orchestrator.execute_pipeline(tasks)
        
        # Restore
        if failing_agent in orchestrator.agents:
            orchestrator.agents[failing_agent]["status"] = original_status
        
        return {
            "test": "agent_failure_recovery",
            "failing_agent": failing_agent,
            "tasks_completed": result["tasks_completed"],
            "has_graceful_degradation": result["tasks_completed"] > 0,
            "status": "PASS" if result["tasks_completed"] > 0 else "FAIL",
        }
    
    def test_token_budget_enforcement(self, 
                                       orchestrator: 'AgentOrchestrator',
                                       budget: int = 10000) -> Dict:
        """
        Test: the token budget is enforced correctly.
        """
        orchestrator.token_budget = budget
        orchestrator.tokens_used = 0
        
        # Create tasks that would exceed budget
        tasks = [
            {"id": f"task-{i}", "type": "code", 
             "input": {}, "estimated_tokens": budget // 2}
            for i in range(5)
        ]
        
        result = orchestrator.execute_pipeline(tasks)
        
        budget_respected = result["tokens_used"] <= budget
        
        return {
            "test": "token_budget_enforcement",
            "budget": budget,
            "tokens_used": result["tokens_used"],
            "budget_respected": budget_respected,
            "status": "PASS" if budget_respected else "FAIL",
        }
    
    def test_conflict_resolution(self, 
                                  conflict_mgr: 'ConflictResolutionManager') -> Dict:
        """
        Test: conflicts are resolved correctly.
        """
        # Test file locking
        acquired1 = conflict_mgr.acquire_file_lock("main.py", "agent-a")
        acquired2 = conflict_mgr.acquire_file_lock("main.py", "agent-b")
        
        # Test approach conflict
        resolution = conflict_mgr.resolve_approach_conflict(
            {"id": "agent-a", "approach": "Use ORM", 
             "rationale": "Because it's tested and proven in production"},
            {"id": "agent-b", "approach": "Raw SQL",
             "rationale": "Because trade-off: better performance"},
        )
        
        return {
            "test": "conflict_resolution",
            "file_locking": {
                "first_acquired": acquired1,
                "second_blocked": not acquired2,
                "status": "PASS" if acquired1 and not acquired2 else "FAIL",
            },
            "approach_conflict": {
                "resolved": "winner" in resolution,
                "winner": resolution.get("winner"),
                "status": "PASS" if "winner" in resolution else "FAIL",
            },
        }
    
    def get_summary(self) -> Dict:
        """Summarize test results"""
        passed = sum(1 for t in self.test_results if t.get("status") == "PASS")
        failed = sum(1 for t in self.test_results if t.get("status") == "FAIL")
        
        return {
            "total": len(self.test_results),
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / len(self.test_results) if self.test_results else 0,
            "failures": [t for t in self.test_results if t.get("status") == "FAIL"],
        }
```

</details>

---

## 15. Cost-Benefit Analysis

> **📌 Core Concept**
>
> - **Concept:** Cost-Benefit Analysis is a comparison between the extra token cost of multi-agent and the quality improvement, so you know when multi-agent is actually worth it versus single-agent.
> - **Analogy/comparison:** Like weighing whether to hire a specialist team: it costs more, but if product quality improves enough, it's still a profit.
> - **Why it matters:** Multi-agent isn't always better — this analysis helps you spend money where it pays off.

### 15.1 When Multi-Agent Is Worth It

A "worth it or not" decision table per task type: comparing single vs multi fit, the quality improvement percentage, the cost multiplier, and the final verdict (SINGLE / MULTI / DEPENDS). How to read it: look at the `Cost` and `Quality` columns — tasks where quality improves a lot while cost only rises a little are good multi-agent candidates. The metaphor: like an outsourcing decision table — do simple work yourself, hire a specialist for hard work.

```
┌────────────────────────────────────────────────────────────────────┐
│         MULTI-AGENT COST-BENEFIT ANALYSIS                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Task Type          │ Single │ Multi │ Quality │ Cost │ Verdict   │
│  ───────────────────┼────────┼───────┼─────────┼──────┼──────────│
│  Simple bug fix     │  ★★★★★ │ ★★☆☆☆ │ +10%    │ 3×   │ SINGLE   │
│  Code review        │  ★★★☆☆ │ ★★★★★ │ +35%    │ 2×   │ MULTI ✓  │
│  Feature dev        │  ★★★☆☆ │ ★★★★☆ │ +25%    │ 3×   │ MULTI ✓  │
│  Security audit     │  ★★☆☆☆ │ ★★★★★ │ +40%    │ 2×   │ MULTI ✓  │
│  Refactoring        │  ★★★☆☆ │ ★★★★☆ │ +20%    │ 3×   │ DEPENDS  │
│  Documentation      │  ★★★★★ │ ★★☆☆☆ │ +5%     │ 4×   │ SINGLE   │
│  Complex debugging  │  ★★☆☆☆ │ ★★★★★ │ +45%    │ 3×   │ MULTI ✓  │
│  Performance tuning │  ★★★☆☆ │ ★★★★☆ │ +30%    │ 2×   │ MULTI ✓  │
│  Multi-file refactor│  ★★☆☆☆ │ ★★★★★ │ +35%    │ 3×   │ MULTI ✓  │
│                                                                    │
│  ROI Formula:                                                      │
│  ROI = (Quality Improvement × Business Value) /                   │
│        (Additional Token Cost + Overhead)                          │
│                                                                    │
│  Break-even: When quality improvement > 20% AND task complexity   │
│  warrants specialization (code review, security, testing)         │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 15.2 Token Cost Comparison

This code writes a Python ROI calculator for multi-agent: each `CostEstimate` holds the single vs multi token counts plus the quality improvement percentage, from which it automatically computes `cost_ratio`, `roi`, and issues a `RECOMMEND` / `CONSIDER` / `AVOID` recommendation. How to run it: the final `print()` section prints a comparison table for each task type. The metaphor: like a pocket calculator for spending decisions — put in the numbers and it tells you right away whether it's a good idea.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CostEstimate:
    """Cost estimate for multi-agent execution"""
    task_name: str
    single_agent_tokens: int
    multi_agent_tokens: int
    quality_improvement_pct: float  # Estimated quality gain
    
    @property
    def cost_ratio(self) -> float:
        """Multi/single cost ratio"""
        return self.multi_agent_tokens / max(self.single_agent_tokens, 1)
    
    @property
    def roi(self) -> float:
        """
        ROI estimate.
        Positive = multi-agent is worth the cost.
        """
        quality_value = self.quality_improvement_pct * 100
        cost_increase = (self.cost_ratio - 1) * 100
        return quality_value - cost_increase
    
    def recommendation(self) -> str:
        if self.roi > 20:
            return "✅ RECOMMEND: Multi-agent (strong ROI)"
        elif self.roi > 0:
            return "💡 CONSIDER: Multi-agent (marginal ROI)"
        else:
            return "❌ AVOID: Single agent is more cost-effective"


# Example cost estimates
COST_ESTIMATES = [
    CostEstimate("Simple bug fix", 5000, 15000, 10),
    CostEstimate("Code review", 8000, 16000, 35),
    CostEstimate("Feature development", 15000, 45000, 25),
    CostEstimate("Security audit", 10000, 20000, 40),
    CostEstimate("Multi-file refactor", 20000, 60000, 35),
    CostEstimate("Documentation", 5000, 20000, 5),
]

print("Multi-Agent Cost-Benefit Analysis:")
print("=" * 60)
for est in COST_ESTIMATES:
    print(f"\n{est.task_name}:")
    print(f"  Single agent: {est.single_agent_tokens:,} tokens")
    print(f"  Multi agent:  {est.multi_agent_tokens:,} tokens")
    print(f"  Cost ratio:   {est.cost_ratio:.1f}×")
    print(f"  Quality gain: +{est.quality_improvement_pct:.0f}%")
    print(f"  ROI:          {est.roi:+.0f}")
    print(f"  → {est.recommendation()}")
```

</details>

---

## References

### Frameworks
- [LangGraph Multi-Agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) — LangChain multi-agent orchestration
- [CrewAI Framework](https://docs.crewai.com/) — Role-based multi-agent framework
- [AutoGen by Microsoft](https://microsoft.github.io/autogen/) — Multi-agent conversation framework
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) — Open-source AI coding agent (formerly OpenDevin)
- [Swarm by OpenAI](https://github.com/openai/swarm) — Lightweight multi-agent orchestration

### Research & Papers
- [Multi-Agent Systems - MIT](https://ocw.mit.edu/courses/6-825-techniques-in-artificial-intelligence-sma-5504-fall-2002/) — MIT course on MAS
- [Blackboard Architecture Pattern](https://wwwPatterns.com/catalog/patterns/view/Blackboard) — Classic coordination pattern
- [Actor Model - Erlang/OTP](https://www.erlang.org/doc/design_principles/actors) — Message-passing concurrency model
- [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629) — Reasoning + Action in LLMs
- [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) — Tool use in language models

### Production Systems
- [Devin by Cognition AI](https://www.cognition.ai/) — Autonomous software engineer
- [Claude Code by Anthropic](https://docs.anthropic.com/en/docs/claude-code) — CLI coding agent
- [GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace) — Multi-agent dev environment
- [Cursor Agent Mode](https://cursor.sh/) — AI-first code editor with agent capabilities

### Architecture Patterns
- [Saga Pattern](https://microservices.io/patterns/data/saga.html) — Distributed transactions
- [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cQRS) — Command Query Responsibility Segregation
- [Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing) — State via events
