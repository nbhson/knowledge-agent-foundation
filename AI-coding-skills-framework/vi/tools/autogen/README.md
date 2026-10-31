# 🤖 AutoGen — Multi-Agent Harness (Microsoft)

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao AutoGen Quan Trọng?](#tại-sao-autogen-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Hãy hình dung thế này: harness của bạn ngày càng phình ra — lúc đầu chỉ một agent lo hết mọi việc: retrieve, plan, code, review. Nhưng khi task lớn dần, agent đơn lẻ đó dễ thành **nút thắt**: context quá tải, chỉ một lỗi nhỏ là hỏng cả chuỗi, mà cũng chẳng có ai thật sự chuyên sâu việc nào.

> *"One agent doing everything is a monolith. A harness of specialized agents is a microservices architecture for cognition."*

**AutoGen (Microsoft)** gỡ điểm nghẽn này bằng mô hình **conversation-based multi-agent**: nhiều agent (assistant, user proxy, critic, planner...) trò chuyện qua lại với nhau thông qua một `ConversableAgent` abstraction. Mỗi agent giữ một vai, một hệ prompt và một khả năng riêng — giống như các node chuyên biệt cắm vào harness vậy.

### Tại Sao AutoGen Quan Trọng?

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Multi-agent tự nhiên** | Conversation-based — agents trao đổi qua messages, ai cũng có thể gọi tools |
| 2 | **UserProxyAgent = harness** | Code mẫu trong HARNESS_ENGINEERING.md cho thấy UserProxyAgent đóng vai harness điều phối |
| 3 | **Code execution tích hợp** | Agents có thể chạy code trong sandbox, nhận kết quả, tự sửa |
| 4 | **GroupChat cho orchestration** | Nhiều agents + manager = hội đồng ra quyết định |

### Quan Hệ Với Harness

```
┌────────────────────────────────────────────────────────────┐
│  AUTOGEN MAP VS HARNESS COMPONENTS                         │
│                                                            │
│  PlannerAgent            → harness/04 (plan/decompose)     │
│  AssistantAgent          → harness/05 (prompt/response)    │
│  UserProxyAgent (harness)→ harness/06 (tool execution)     │
│  CriticAgent             → harness/11 (evaluation)         │
│  GroupChat + Manager     → harness/09 (multi-agent)        │
│  Memory (ConversableMemory)→ harness/01, 03 (memory)      │
└────────────────────────────────────────────────────────────┘
```

## Tổng Quan

### Conversation-Based Multi-Agent

AutoGen dùng kiến trúc **agent-to-agent conversation**. Thay vì xếp thành một pipeline thẳng đuột, các agent cứ trao đổi qua lại với nhau như thế này:

```
User → UserProxyAgent → AssistantAgent (gọi tool) → UserProxyAgent (chạy code)
     → AssistantAgent (nhận kết quả, tiếp tục) → ... → trả lời User
```

### Code Mẫu Từ HARNESS_ENGINEERING.md

> 📄 **Code ví dụ:** [`examples/01-code-mau-tu-harness-engineering-md.py`](examples/01-code-mau-tu-harness-engineering-md.py)

Để `human_input_mode="NEVER"` là UserProxyAgent trở thành một **harness tự chạy**: tự gọi tools, tự đón kết quả, tự đi tiếp cho tới khi xong việc hoặc chạm trần `max_consecutive_auto_reply`.

### GroupChat — Nhiều Agent

> 📄 **Code ví dụ:** [`examples/02-groupchat-nhieu-agent.py`](examples/02-groupchat-nhieu-agent.py)

Nói ngắn gọn, đây chính là **harness/09-multi-agent** viết thành code — một manager đứng ra chia lượt xem ai nói khi nào, giống như harness điều phối mấy worker vậy.

## Lộ Trình Học (Cấu Trúc Thư Mục)

```
autogen/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) ConversableAgent, UserProxyAgent, GroupChat
├── 02-setup/            ← (TODO) Cài đặt pyautogen, cấu hình LLM
├── 03-patterns/         ← (TODO) Two-agent, group chat, nested chats
├── 04-savings/          ← (TODO) Token cost per conversation round
└── 05-troubleshooting/  ← (TODO) Infinite loops, agent deadlock, termination
```

### Lộ Trình Đề Xuất

```
Bước 1: Đọc HARNESS_ENGINEERING.md section 9.1 — code mẫu AutoGen có sẵn
   ↓
Bước 2: Chạy mô hình 2-agent: UserProxyAgent + AssistantAgent
   ↓
Bước 3: Thêm Planner + Critic — tương ứng harness/04 + harness/11
   ↓
Bước 4: Nâng lên GroupChat với manager (harness/09 multi-agent)
   ↓
Bước 5: Kết nối memory + evaluation (xem tools/observability, tools/evaluation)
```

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu multi-agent harness | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Planning/decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Evaluation/review | [harness/11-evaluation](../../harness/11-evaluation/) |
| Vòng lặp agents | [loop/05-multi-loop](../../loop/05-multi-loop/) |

## Case Studies Thực Tế

### 1. Code Review Pipeline (Planner → Coder → Critic)

> 📄 **Code ví dụ:** [`examples/03-1-code-review-pipeline-planner-coder-critic.py`](examples/03-1-code-review-pipeline-planner-coder-critic.py)

Luồng chạy cũng dễ hình dung: planner lên ý tưởng → coder viết theo → critic soi lỗi → quay lại coder sửa → ... cứ thế cho tới khi critic gật đầu — đúng kiểu **loop/05-multi-loop** nhưng viết thành code.

### 2. Human-in-the-Loop Cho Phép Thay Đổi Nhạy Cảm

> 📄 **Code ví dụ:** [`examples/04-2-human-in-the-loop-cho-phep-thay.py`](examples/04-2-human-in-the-loop-cho-phep-thay.py)

## Tài Liệu Tham Khảo

- **AutoGen (Microsoft)**: https://microsoft.github.io/autogen/
- **AutoGen Studio**: https://microsoft.github.io/autogen/studio/
- **GitHub**: https://github.com/microsoft/autogen

### Liên Kết Sang Nhánh Khác

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (code mẫu AutoGen)
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent concepts
- [tools/loop-cli](../loop-cli/) — Orchestration layer
- [tools/langchain](../langchain/) — Framework thay thế (graph-based)

---

> **"AutoGen doesn't give you agents — it gives you a conversation where intelligence emerges."**

---

## ⚠️ Cập nhật 10/2026: AutoGen → Microsoft Agent Framework (MAF)

AutoGen đã được **archive** và thay thế bởi **Microsoft Agent Framework (MAF)**:
- Repo AutoGen archived — không phát triển thêm
- MAF = sự hợp nhất AutoGen + Semantic Kernel
- API hoàn toàn mới: `agents/`, không còn `ConversableAgent`

> 📄 **Code ví dụ:** [`examples/05-cap-nhat-10-2026-autogen-microsoft-agent-framework.py`](examples/05-cap-nhat-10-2026-autogen-microsoft-agent-framework.py)

**Di chuyển project cũ:** https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/
**MAF mới:** https://github.com/microsoft/agent-framework

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — autogen*