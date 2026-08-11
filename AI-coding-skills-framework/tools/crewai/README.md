# 🚢 CrewAI — Multi-Agent Harness (Role-Based)

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao CrewAI Quan Trọng?](#tại-sao-crewai-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

AutoGen mô hình hóa multi-agent như một cuộc trò chuyện — nhưng đôi khi bạn muốn cấu trúc rõ ràng hơn: **mỗi agent một vai (role), mỗi vai một nhiệm vụ (task), và agents phối hợp trong một crew**. Giống một công ty nơi planner lên kế hoạch, executor thực thi, reviewer kiểm duyệt — mỗi người một việc, không ai nói leo.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** là framework role-based multi-agent: bạn định nghĩa `Agent` (role, goal, backstory), `Task` (description, expected_output, agent), và `Crew` (agents, tasks, process). Crucially, code mẫu đã có trong HARNESS_ENGINEERING.md section 9.1.

### Tại Sao CrewAI Quan Trọng?

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Role-based rõ ràng** | Mỗi agent có role/goal/backstory — dễ map sang harness components |
| 2 | **Task-first** | `Task` là đơn vị công việc — đúng triết lý harness/04 (task decomposition) |
| 3 | **Process orchestrates** | `Process.sequential` / `Process.hierarchical` — kiểm soát thứ tự thực thi |
| 4 | **Human-in-the-loop** | `human_input` flag cho phép interjection giữa các bước |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  CREWAI MAP VS HARNESS COMPONENTS                          │
│                                                            │
│  Agent(role="Planner")   → harness/04 (plan/decompose)     │
│  Agent(role="Executor")  → harness/06 (tool execution)     │
│  Agent(role="Reviewer")  → harness/11 (evaluation)         │
│  Task + expected_output  → harness/08 (task)               │
│  Crew(process=...)       → harness/07 (workflow)           │
│  Crew + agents           → harness/09 (multi-agent)        │
└────────────────────────────────────────────────────────────┘
```

## Tổng Quan

### Ba Khái Niệm Cốt Lõi

```
Agent  →  AI worker với role/goal/backstory + tools
Task   →  Công việc cụ thể, expected output, giao cho agent nào
Crew   →  Tập hợp agents + tasks + process (cách chúng phối hợp)
```

### Code Mẫu Từ HARNESS_ENGINEERING.md

```python
from crewai import Agent, Task, Crew

# Multi-agent harness
planner = Agent(role='Planner', goal='Create plan')
executor = Agent(role='Executor', goal='Execute plan')
reviewer = Agent(role='Reviewer', goal='Review output')

harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task]
)
```

### Process: Sequential vs Hierarchical

```python
# Sequential — pipeline tuyến tính: plan → execute → review
harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task],
    process=Process.sequential
)

# Hierarchical — manager agent điều phối, assign tasks
harness = Crew(
    agents=[executor, reviewer],
    tasks=[execute_task, review_task],
    process=Process.hierarchical,
    manager_agent=manager,  # bổ sung "harness manager"
    manager_llm=llm
)
```

`Process.hierarchical` chính là **harness/09-multi-agent** — một manager điều phối like harness orchestrator. `Process.sequential` map với **harness/07-workflow** pipeline.

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
crewai/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Agent, Task, Crew, Process, Flows
├── 02-setup/            ← (TODO) Cài đặt crewai, cấu hình LLM, tools
├── 03-patterns/         ← (TODO) Sequential pipeline, hierarchical, flows
├── 04-savings/          ← (TODO) Token usage + cost per crew run
└── 05-troubleshooting/  ← (TODO) Agent misalignment, task delegation, memory
```

### Lộ Trình Đề Xuất

```
Bước 1: Đọc HARNESS_ENGINEERING.md section 9.1 — code mẫu CrewAI có sẵn
   ↓
Bước 2: Tạo Crew đơn giản: planner → executor → reviewer (sequential)
   ↓
Bước 3: Thêm tools cho executor (search, code, db) — harness/06
   ↓
Bước 4: Nâng lên Process.hierarchical với manager — harness/09
   ↓
Bước 5: Kết nối evaluation + observability (tools/evaluation, tools/observability)
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu task decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Multi-agent concepts | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Task lifecycle | [harness/08-task](../../harness/08-task/) |

## Case Studies Thực Tế

### 1. Code Review Crew

```python
planner = Agent(role='Planner', goal='Break down feature into tasks')
coder = Agent(role='Coder', goal='Implement tasks', tools=[code_editor])
reviewer = Agent(role='Reviewer', goal='Find bugs and security issues')

plan_task = Task(description='Plan the login API', expected_output='Task list')
code_task = Task(description='Implement per plan', expected_output='Working code')
review_task = Task(description='Review code', expected_output='Review report')

crew = Crew(
    agents=[planner, coder, reviewer],
    tasks=[plan_task, code_task, review_task],
    process=Process.sequential  # plan → code → review → (reviewer feedback loop)
)
```

### 2. Human-in-the-Loop

```python
task = Task(
    description="Deploy to production",
    expected_output="Deployment confirmation",
    human_input=True  # dừng lại chờ xác nhận trước khi deploy
)
```

## Tài Liệu Tham Khảo

- **CrewAI**: https://docs.crewai.com/
- **GitHub**: https://github.com/crewAIInc/crewAI
- **Blog**: https://blog.crewai.com

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (code mẫu CrewAI)
- [harness/07-workflow](../../harness/07-workflow/) — Workflow orchestration
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent patterns
- [tools/autogen](../autogen/) — Multi-agent tương đương (conversation-based)
- [tools/langchain](../langchain/) — Graph-based orchestration

---

> **"CrewAI gives your harness an org chart — roles, tasks, and a crew that ships."**

---

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — crewai*