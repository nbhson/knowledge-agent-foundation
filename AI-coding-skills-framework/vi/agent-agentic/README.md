# AI Agent & Agentic AI – From Fundamentals to Implementation

> **Người mới bắt đầu** — hiểu từ số 0, đi dần lên production system.

Tutorial này bao phủ hai khía cạnh:
1. **Theoretical Foundation** — Hiểu Agent là gì, hoạt động ra sao, kiến trúc và khái niệm liên quan.
2. **Practical Implementation** — Tự xây dựng Agent bằng Python/Node.js, kết nối LLM, Tools, Memory, MCP và triển khai thực tế.

**Nguyên tắc: Hiểu cơ chế Agent trước, sau đó mới học framework.**

---

## 🗺️ Learning Path

```
PHẦN I ── Hiểu bản chất Agent
  Module 01: Giới thiệu AI Agent          ← BẮT ĐẦU Ở ĐÂY ✅
  Module 02: Agentic AI là gì?
  Module 03: Agent Lifecycle & Core Principles
  Module 04: Agent Architecture & Components

PHẦN II ── Công nghệ cốt lõi
  Module 05: LLM & Reasoning
  Module 06: Context Engineering
  Module 07: Memory Engineering
  Module 08: Tool Calling & External Integration

PHẦN III ── Thiết kế Agentic Workflow
  Module 09: Agent Workflow Patterns
  Module 10: Planning & Task Execution
  Module 11: Agent Decision Making
  Module 12: Single-Agent vs Multi-Agent

PHẦN IV ── Frameworks & Hệ sinh thái
  Module 13: Agent Frameworks (LangChain, CrewAI, AutoGen...)
  Module 14: MCP – Model Context Protocol
  Module 15: Agent Communication & Integration
```

> **Đọc theo thứ tự 01 → 15.** Mỗi module là bước kế tiếp của bước trước.


---

## 📚 Nội dung 15 Module

### PHẦN I – FUNDAMENTALS: UNDERSTANDING AI AGENTS

**Mục tiêu:** Hiểu bản chất của Agent và phân biệt các khái niệm thường bị nhầm lẫn.

#### Module 1. Introduction to AI Agent
`part-01-fundamentals/01-introduction-to-ai-agent/`

- AI là gì? — Artificial Intelligence, Machine Learning, Deep Learning.
- LLM là gì? — "bộ não" đằng sau mọi AI Agent hiện đại.
- AI Chatbot vs AI Assistant vs AI Agent — ba thuật ngữ hay bị dùng lẫn.
- Agent là gì? — từ Computer Science (Perceive → Decide → Act) đến LLM-based AI.
- AI Agent khác gì chương trình thông thường?
- Tại sao LLM không tự động trở thành Agent? — thiếu tools, memory, loop.
- Các ứng dụng thực tế của AI Agent.

#### Module 2. Understanding Agentic AI
`part-01-fundamentals/02-understanding-agentic-ai/`

- Agentic AI là gì? — Agent vs Agentic AI.
- Agentic Workflow là gì?
- Autonomous AI là gì?
- AI Automation vs Agentic Automation.
- Reactive vs Proactive Agent.
- Single-Agent vs Multi-Agent.
- Human-in-the-loop vs Human-out-of-the-loop.
- Mức độ tự chủ (Autonomy Levels).

#### Module 3. Agent Lifecycle & Core Principles
`part-01-fundamentals/03-agent-lifecycle-core-principles/`

- Perceive → Reason → Plan → Act → Observe.
- Feedback Loop & Iterative Execution.
- Goal-oriented Behavior & Decision Making.
- Stop Condition và Task Completion.

#### Module 4. Agent Architecture & Components
`part-01-fundamentals/04-agent-architecture-components/`

- Brain: LLM / Foundation Model.
- Agent Runtime / Orchestrator.
- Context Engineering, Planning Engine.
- Tool Registry, Tool Executor, Memory System.
- State Management, Environment, Feedback Mechanism.
- Guardrails và Permission System.

---

### PHẦN II – CORE TECHNOLOGIES: THE BUILDING BLOCKS

**Mục tiêu:** Hiểu những công nghệ giúp Agent có thể suy luận, ghi nhớ và hành động.

#### Module 5. LLM & Reasoning
`part-02-core-technologies/05-llm-reasoning/`

- Tokens & Context Window.
- System/User/Assistant messages.
- Inference & Generation.
- Temperature, Top-P, Max Tokens.
- Chain-of-Thought (CoT).
- Structured Output, JSON Mode.
- Function Calling / Tool Calling.
- Hallucination & Model limitations.

#### Module 6. Context Engineering
`part-02-core-technologies/06-context-engineering/`

- Prompt Engineering vs Context Engineering.
- Context Window Management, Assembly, Compression.
- Context Retrieval — Short-term / Long-term / Working Context.
- Context Overflow & Isolation.

#### Module 7. Memory Engineering
`part-02-core-technologies/07-memory-engineering/`

- Agent Memory là gì?
- Short-term / Long-term / Episodic / Semantic / Procedural Memory.
- Vector Database, Embeddings, RAG.
- Memory Retrieval, Update & Management.

#### Module 8. Tool Calling & External Integration
`part-02-core-technologies/08-tool-calling-external-integration/`

- Tool Definition (JSON Schema), Selection, Execution.
- Error Handling & Retry.
- Tool Permission.
- External API Integration.
- File System / Terminal / Browser / Database.
- MCP (tổng quan — chi tiết ở Module 14).

---

### PHẦN III – AGENTIC WORKFLOW & DESIGN PATTERNS

**Mục tiêu:** Hiểu cách thiết kế quy trình làm việc có tính Agentic.

#### Module 9. Agent Workflow Patterns
`part-03-agentic-workflow-design-patterns/09-agent-workflow-patterns/`

- Prompt Chaining, Routing, Parallelization.
- Orchestrator-Worker, Evaluator-Optimizer.
- Iterative Refinement, Tool-use Loop, Reflection Pattern.

#### Module 10. Planning & Task Execution
`part-03-agentic-workflow-design-patterns/10-planning-task-execution/`

- Task & Goal Decomposition, Planning Strategies.
- Sequential / Parallel / Dynamic Execution.
- Replanning, Dependency Management, Task Prioritization.
- Execution Budget & Stop Conditions.

#### Module 11. Agent Decision Making
`part-03-agentic-workflow-design-patterns/11-agent-decision-making/`

- Rule-based / LLM-based / State-based Decision Making.
- Action Selection & Observation Evaluation.
- Confidence & Uncertainty.
- Failure Recovery, Self-correction, Reflection.
- Human Approval.

#### Module 12. Single-Agent vs Multi-Agent
`part-03-agentic-workflow-design-patterns/12-single-agent-vs-multi-agent/`

- Single-Agent vs Multi-Agent Architecture.
- Collaboration, Delegation, Communication.
- Shared vs Independent Memory.
- Supervisor / Worker / Hierarchical Agents.
- Multi-Agent Coordination, Consensus & Conflict Resolution.

---

### PHẦN IV – AGENT FRAMEWORKS & ECOSYSTEM

**Mục tiêu:** Biết những framework và giao thức phổ biến, hiểu chúng giải quyết vấn đề gì.

#### Module 13. Agent Frameworks
`part-04-agent-frameworks-ecosystem/13-agent-frameworks/`

- Build Agent from Scratch.
- LangChain, LangGraph, CrewAI, AutoGen, OpenAI Agents SDK.
- Framework vs Runtime vs SDK.
- Khi nào nên dùng framework, khi nào nên tự xây dựng?

#### Module 14. MCP – Model Context Protocol
`part-04-agent-frameworks-ecosystem/14-mcp-model-context-protocol/`

- MCP là gì? Tại sao cần MCP?
- Architecture: Host / Client / Server.
- Tools, Resources, Prompts.
- Transport Mechanisms & MCP Lifecycle.
- Security & Permission.
- Tự xây dựng MCP Server.

#### Module 15. Agent Communication & Integration
`part-04-agent-frameworks-ecosystem/15-agent-communication-integration/`

- REST API, WebSocket, Event-driven Architecture, Message Queue.
- Agent-to-Agent Communication & A2A Protocol.
- External Services Integration.
- Authentication, Authorization, API Rate Limiting.

---

## 🚀 Đi Tiếp

- Hoàn thành Part I–IV (15 module) theo thứ tự 01 → 15.
- Sau mỗi module: làm `examples/` (code mẫu) để nắm chắc lý thuyết.
- Khi đủ nền tảng, bạn có thể mở rộng thêm phần thực hành xây dựng Agent hoàn chỉnh (Part V+).

> **Một câu để nhớ:** Hiểu cơ chế Agent trước, framework chỉ là phương tiện.
