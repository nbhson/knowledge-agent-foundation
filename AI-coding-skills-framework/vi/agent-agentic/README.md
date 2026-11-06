# AI Agent & Agentic AI – From Fundamentals to Implementation

> Cấu trúc khung (placeholder). Nội dung sẽ được thêm sau.

Tutorial này bao phủ hai khía cạnh:
1. **Theoretical Foundation** – Hiểu Agent là gì, hoạt động ra sao, kiến trúc và khái niệm liên quan.
2. **Practical Implementation** – Tự xây dựng Agent bằng Python/Node.js, kết nối LLM, Tools, Memory, MCP và triển khai thực tế.

Nguyên tắc: **Hiểu cơ chế Agent trước, sau đó mới học framework.**

Mục tiêu tổng thể: đi từ nền tảng đến kiến trúc production, chia thành **8 phần lớn, 24 module**.

---

## PHẦN I – FUNDAMENTALS: UNDERSTANDING AI AGENTS

Mục tiêu: Hiểu bản chất của Agent và phân biệt các khái niệm thường bị nhầm lẫn.

### Module 1. Introduction to AI Agent
`part-01-fundamentals/01-introduction-to-ai-agent/`

- AI là gì?
- Artificial Intelligence, Machine Learning, Deep Learning.
- LLM là gì?
- AI Chatbot vs AI Assistant vs AI Agent.
- Agent là gì?
- Agent trong Computer Science và Agent trong LLM-based AI.
- AI Agent khác gì một chương trình thông thường?
- Tại sao LLM không tự động trở thành Agent?
- Các ứng dụng thực tế của AI Agent.

### Module 2. Understanding Agentic AI
`part-01-fundamentals/02-understanding-agentic-ai/`

- Agentic AI là gì?
- Agent vs Agentic AI.
- Agentic Workflow là gì?
- Autonomous AI là gì?
- AI Automation vs Agentic Automation.
- Reactive vs Proactive Agent.
- Single-Agent vs Multi-Agent.
- Human-in-the-loop vs Human-out-of-the-loop.
- Mức độ tự chủ (Autonomy Levels).

### Module 3. Agent Lifecycle & Core Principles
`part-01-fundamentals/03-agent-lifecycle-core-principles/`

- Perceive – Nhận biết.
- Reason – Suy luận.
- Plan – Lập kế hoạch.
- Act – Hành động.
- Observe – Quan sát.
- Feedback Loop.
- Iterative Execution.
- Goal-oriented Behavior.
- Decision Making.
- Stop Condition và Task Completion.

### Module 4. Agent Architecture & Components
`part-01-fundamentals/04-agent-architecture-components/`

- LLM / Foundation Model – Brain.
- Agent Runtime / Orchestrator.
- System Instructions / Prompt.
- Context Engineering.
- Planning Engine.
- Tool Registry.
- Tool Executor.
- Memory System.
- State Management.
- Environment.
- Feedback Mechanism.
- Guardrails và Permission System.

> Kết quả cần đạt: Có thể giải thích một Agent từ góc nhìn Software Architecture và phân chia trách nhiệm thành các module code.

---

## PHẦN II – CORE TECHNOLOGIES: THE BUILDING BLOCKS

Mục tiêu: Hiểu những công nghệ giúp Agent có thể suy luận, ghi nhớ và hành động.

### Module 5. LLM & Reasoning
`part-02-core-technologies/05-llm-reasoning/`

- LLM hoạt động như thế nào?
- Tokens và Context Window.
- System Prompt, User Prompt, Assistant Message.
- Inference và Generation.
- Temperature, Top-P, Max Tokens.
- Reasoning và Chain-of-Thought ở góc độ khái niệm.
- Structured Output.
- JSON Mode.
- Function Calling / Tool Calling.
- Model limitations và hallucination.

### Module 6. Context Engineering
`part-02-core-technologies/06-context-engineering/`

- Prompt Engineering vs Context Engineering.
- Context Window Management.
- Context Assembly.
- Context Compression.
- Context Retrieval.
- Short-term Context.
- Long-term Context.
- Working Context.
- Context Overflow.
- Context Isolation.

### Module 7. Memory Engineering
`part-02-core-technologies/07-memory-engineering/`

- Agent Memory là gì?
- Short-term Memory.
- Long-term Memory.
- Episodic Memory.
- Semantic Memory.
- Procedural Memory.
- Conversation History.
- Vector Database.
- Embeddings.
- RAG (Retrieval-Augmented Generation).
- Memory Retrieval và Memory Update.
- Memory Management.

### Module 8. Tool Calling & External Integration
`part-02-core-technologies/08-tool-calling-external-integration/`

- Tool là gì?
- Function Calling vs Tool Calling.
- Tool Definition / JSON Schema.
- Tool Selection.
- Tool Execution.
- Tool Result.
- Error Handling.
- Retry Mechanism.
- Tool Permission.
- External API Integration.
- File System / Terminal / Browser / Database.
- MCP (Model Context Protocol).

---

## PHẦN III – AGENTIC WORKFLOW & DESIGN PATTERNS

Mục tiêu: Hiểu cách thiết kế quy trình làm việc có tính Agentic.

### Module 9. Agent Workflow Patterns
`part-03-agentic-workflow-design-patterns/09-agent-workflow-patterns/`

- Prompt Chaining.
- Routing.
- Parallelization.
- Orchestrator-Worker.
- Evaluator-Optimizer.
- Iterative Refinement.
- Tool-use Loop.
- Reflection Pattern.

### Module 10. Planning & Task Execution
`part-03-agentic-workflow-design-patterns/10-planning-task-execution/`

- Task Decomposition.
- Goal Decomposition.
- Planning Strategies.
- Sequential Execution.
- Parallel Execution.
- Dynamic Planning.
- Replanning.
- Dependency Management.
- Task Prioritization.
- Execution Budget.
- Stop Conditions.

### Module 11. Agent Decision Making
`part-03-agentic-workflow-design-patterns/11-agent-decision-making/`

- Rule-based Decision Making.
- LLM-based Decision Making.
- State-based Decision Making.
- Action Selection.
- Observation Evaluation.
- Confidence and Uncertainty.
- Failure Recovery.
- Self-correction.
- Reflection.
- Human Approval.

### Module 12. Single-Agent vs Multi-Agent
`part-03-agentic-workflow-design-patterns/12-single-agent-vs-multi-agent/`

- Single-Agent Architecture.
- Multi-Agent Architecture.
- Agent Collaboration.
- Agent Delegation.
- Agent Communication.
- Shared Memory.
- Independent Memory.
- Agent Roles.
- Supervisor Agent.
- Worker Agent.
- Hierarchical Agents.
- Multi-Agent Coordination.
- Consensus và Conflict Resolution.

---

## PHẦN IV – AGENT FRAMEWORKS & ECOSYSTEM

Mục tiêu: Biết những framework và giao thức phổ biến, hiểu chúng giải quyết vấn đề gì.

### Module 13. Agent Frameworks
`part-04-agent-frameworks-ecosystem/13-agent-frameworks/`

- Build Agent from Scratch.
- LangChain.
- LangGraph.
- CrewAI.
- AutoGen.
- OpenAI Agents SDK.
- Framework vs Runtime vs SDK.
- Khi nào nên dùng framework, khi nào nên tự xây dựng?

### Module 14. MCP – Model Context Protocol
`part-04-agent-frameworks-ecosystem/14-mcp-model-context-protocol/`

- MCP là gì?
- Tại sao cần MCP?
- MCP Architecture.
- MCP Host.
- MCP Client.
- MCP Server.
- Tools.
- Resources.
- Prompts.
- Transport Mechanisms.
- MCP Lifecycle.
- Security và Permission.
- Tự xây dựng MCP Server.

### Module 15. Agent Communication & Integration
`part-04-agent-frameworks-ecosystem/15-agent-communication-integration/`

- REST API.
- WebSocket.
- Event-driven Architecture.
- Message Queue.
- Agent-to-Agent Communication.
- A2A Protocol.
- External Services Integration.
- Authentication.
- Authorization.
- API Rate Limiting.

---

### Ghi chú
- Mỗi module có `README.md` placeholder với danh sách nội dung dự kiến.
- Mỗi module có thư mục `examples/` để bạn thêm code mẫu khi viết nội dung.
- Bạn có thể thêm `code/`, `assets/` trong từng module nếu cần.
- Nếu sau này bạn có outline cho phần V–VIII, tôi sẽ tạo thêm các part/module tương ứng.