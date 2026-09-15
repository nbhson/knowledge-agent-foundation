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

Harness của bạn ngày càng phức tạp: một agent duy nhất làm mọi thứ — retrieve, plan, code, review. Khi task đủ lớn, agent đơn lẻ trở thành **nút thắt**: context quá tải, một lỗi nhỏ phá hỏng cả chuỗi, và không có sự phân công chuyên môn hóa.

> *"One agent doing everything is a monolith. A harness of specialized agents is a microservices architecture for cognition."*

**AutoGen (Microsoft)** giải quyết bằng mô hình **conversation-based multi-agent**: nhiều agent (assistant, user proxy, critic, planner...) trò chuyện với nhau thông qua một `ConversableAgent` abstraction. Mỗi agent có vai trò, hệ thống prompt, và khả năng riêng — như các node chuyên biệt trong harness.

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

AutoGen dùng kiến trúc **agent-to-agent conversation**. Thay vì một pipeline tuyến tính, các agent trao đổi:

```
User → UserProxyAgent → AssistantAgent (gọi tool) → UserProxyAgent (chạy code)
     → AssistantAgent (nhận kết quả, tiếp tục) → ... → trả lời User
```

### Code Mẫu Từ HARNESS_ENGINEERING.md

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"},
    system_message="You are a helpful assistant"
)

# UserProxyAgent đóng vai harness — điều phối, chạy code, kiểm soát
harness = UserProxyAgent(
    name="harness",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"}
)
```

`human_input_mode="NEVER"` biến UserProxyAgent thành **harness tự điều hành**: tự gọi tools, tự nhận kết quả, tự tiếp tục cho tới khi hoàn thành hoặc chạm giới hạn `max_consecutive_auto_reply`.

### GroupChat — Nhiều Agent

```python
from autogen import GroupChat, GroupChatManager

agents = [planner, assistant, critic, executor]
group_chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=20,
    speaker_selection_method="auto"  # hoặc "round_robin", "vote"
)
manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

Đây chính là **harness/09-multi-agent** dưới dạng code — một manager điều phối ai nói khi nào, như một harness orchestrating các workers.

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

```python
planner  = AssistantAgent(name="planner",  system_message="Tạo kế hoạch chi tiết")
coder    = AssistantAgent(name="coder",    system_message="Viết code theo plan")
critic   = AssistantAgent(name="critic",   system_message="Review lỗi logic & an toàn")

group_chat = GroupChat(agents=[planner, coder, critic], max_round=15)
manager = GroupChatManager(groupchat=group_chat)

# Harness khởi động hội đồng
result = manager.run(task="Implement login API with rate limiting")
```

Luồng: planner đề xuất → coder implement → critic phát hiện lỗi → quay lại coder sửa → ... cho đến khi critic hài lòng — một **loop/05-multi-loop** code-based.

### 2. Human-in-the-Loop Cho Phép Thay Đổi Nhạy Cảm

```python
sensitive_harness = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",  # chỉ dừng khi cần xác nhận
    code_execution_config=False
)
```

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

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — autogen*