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

AutoGen xem multi-agent như một cuộc trò chuyện — nhưng nhiều lúc bạn muốn mọi thứ rõ vai rõ việc hơn: **mỗi agent một vai (role), mỗi vai một nhiệm vụ (task), rồi cả bọn phối hợp trong một crew**. Giống một công ty nhỏ: planner lên kế hoạch, executor xắn tay làm, reviewer ngồi duyệt — ai làm việc nấy, không ai nói leo.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** là framework multi-agent chia theo vai: bạn định nghĩa `Agent` (role, goal, backstory), `Task` (description, expected_output, agent), rồi gom lại thành `Crew` (agents, tasks, process). Tiện một chỗ là code mẫu đã có sẵn trong HARNESS_ENGINEERING.md section 9.1, bạn mở ra là thấy ngay.

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

> 📄 **Code ví dụ:** [`examples/01-code-mau-tu-harness-engineering-md.py`](examples/01-code-mau-tu-harness-engineering-md.py)

### Process: Sequential vs Hierarchical

> 📄 **Code ví dụ:** [`examples/02-process-sequential-vs-hierarchical.py`](examples/02-process-sequential-vs-hierarchical.py)

Hiểu đơn giản: `Process.hierarchical` chính là **harness/09-multi-agent** — có một manager đứng ra điều phối như harness orchestrator. Còn `Process.sequential` thì ứng với pipeline **harness/07-workflow**.

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

> 📄 **Code ví dụ:** [`examples/03-1-code-review-crew.py`](examples/03-1-code-review-crew.py)

### 2. Human-in-the-Loop

> 📄 **Code ví dụ:** [`examples/04-2-human-in-the-loop.py`](examples/04-2-human-in-the-loop.py)

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

## ⚠️ Cập nhật 10/2026: CrewAI v1.x — Phiên Bản Mới Nhất

CrewAI đã phát hành **v1.0.0 (10/2025)** và đạt **v1.15.x (2026)** — nhiều thay đổi đáng chú ý:

| Thay đổi | Chi tiết |
|----------|----------|
| **v1.0.0** | Knowledge & guardrail event handling trong Agent, response_format support |
| **v1.5.0** | Structured outputs, before/after tool call hooks |
| **v1.14+** | Inline skill definitions, Flow Definition authoring, dynamic LLM model pull |
| **crewAI CLI** | `crewai run` có cấu hình qua `crew.jsonc` |

**Lưu ý quan trọng:** CrewAI >= 1.0 yêu cầu **Python 3.10 – 3.13**.

> 📄 **Code ví dụ:** [`examples/05-cap-nhat-10-2026-crewai-v1-x-phien.sh`](examples/05-cap-nhat-10-2026-crewai-v1-x-phien.sh)

Ref: https://docs.crewai.com/

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — crewai*