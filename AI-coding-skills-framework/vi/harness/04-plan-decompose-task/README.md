# 📋 IV. Lập Kế Hoạch & Chia Nhỏ Tác Vụ

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Tại Sao Lập Kế Hoạch & Chia Nhỏ Tác Vụ Quan Trọng?](#tại-sao-lập-kế-hoạch-chia-nhỏ-tác-vụ-quan-trọng)
> - [Nội Dung](#nội-dung)
> - [1. Các Mô Hình Chia Nhỏ Tác Vụ](#1-các-mô-hình-chia-nhỏ-tác-vụ)
>   - [1.1 Các Mô Hình Phân Chia](#11-các-mô-hình-phân-chia)
>   - [1.2 Implementation](#12-implementation)
>   - [1.3 So Sánh Các Pattern](#13-so-sánh-các-pattern)
> - [2. Planning Algorithms](#2-planning-algorithms)
>   - [2.1 LLM-Based Planning (Plan-and-Solve)](#21-llm-based-planning-plan-and-solve)
>   - [2.2 Tree of Thoughts (ToT)](#22-tree-of-thoughts-tot)
>   - [2.3 ReWOO (Reasoning Without Observation)](#23-rewoo-reasoning-without-observation)
> - [3. Agent Workflows](#3-agent-workflows)
>   - [3.1 Các Kiểu Agent](#31-các-kiểu-agent)
>   - [3.2 Agent Implementation](#32-agent-implementation)
> - [4. State Management](#4-state-management)
> - [5. ReAct Pattern](#5-react-pattern)
> - [6. Harness-Integrated Planning](#6-harness-integrated-planning)
>   - [6.1 TypeScript Interface (Harness Architecture)](#61-typescript-interface-harness-architecture)
> - [7. Case Studies Thực Tế](#7-case-studies-thực-tế)
>   - [7.1. SWE-agent (Princeton NLP) — Planning-First Approach](#71-swe-agent-princeton-nlp-planning-first-approach)
>   - [7.2. Anthropic Multi-Agent Architecture](#72-anthropic-multi-agent-architecture)
>   - [7.3. Claude Code — Hierarchical Planning System](#73-claude-code-hierarchical-planning-system)
>   - [7.4. Cursor IDE — Context-Aware Planning](#74-cursor-ide-context-aware-planning)
> - [8. Design Principles](#8-design-principles)
>   - [8.1 SOLID Cho Planning System](#81-solid-cho-planning-system)
>   - [8.2 The 10 Commandments of Task Planning](#82-the-10-commandments-of-task-planning)
> - [9. Best Practices](#9-best-practices)
>   - [9.1 DO ✅](#91-do)
>   - [9.2 DON'T ❌](#92-dont)
>   - [9.3 Token Budget Management](#93-token-budget-management)
> - [10. Testing Planning Systems](#10-testing-planning-systems)
> - [11. Advanced Patterns](#11-advanced-patterns)
>   - [11.1 Hierarchical Task Network (HTN)](#111-hierarchical-task-network-htn)
>   - [11.2 Self-Reflective Planning](#112-self-reflective-planning)
> - [12. Tools & Frameworks](#12-tools-frameworks)
>   - [12.1 LangGraph (Recommended for Planning)](#121-langgraph-recommended-for-planning)
>   - [12.2 CrewAI (Multi-Agent Planning)](#122-crewai-multi-agent-planning)
>   - [12.3 AutoGen (Microsoft)](#123-autogen-microsoft)
> - [13. Tương Lai](#13-tương-lai)
>   - [13.1 Xu Hướng 2026-2028](#131-xu-hướng-2026-2028)
>   - [13.2 Lời Khuyên](#132-lời-khuyên)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks](#frameworks)
>
---

### Câu Chuyện Mở Đầu

Hãy tưởng tượng bạn thuê một bác thợ xây **căn nhà 3 tầng**. Bác ấy không vẽ bản vẽ, không chia giai đoạn, cứ thế bắt tay vào làm luôn — vừa đổ móng vừa xây tường vừa lắp cửa một lúc. Kết quả thế nào? Tường lệch, cửa vênh, cuối cùng phải đập đi làm lại từ đầu.

**AI Agent không có Planning & Decomposition cũng y hệt như vậy.**

LLM nói rất hay — nhưng khi gặp việc khó kiểu *"triển khai hệ thống BHYT cho công ty 100 người"*, chúng hay mắc một trong hai lỗi: **Oversimplification** (nhảy vào code ngay mà không plan gì cả) hoặc **Analysis Paralysis** (mổ xẻ mãi mà chẳng chịu bắt tay làm). Kiểu nào cũng cho ra kết quả dở.

**Cách gỡ**: Structured Planning — dạy agent **nghĩ trước khi làm**, nhưng vẫn **làm đúng lúc, không chần chừ**.

### Tại Sao Plan & Decompose Task Quan Trọng?

> *"Mục tiêu mà không có kế hoạch thì chỉ là mong ước. Còn AI mà không biết chia việc thì cũng chỉ là chatbot mà thôi."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Microsoft Research (2025)** | Agent **without planning** chỉ đạt **32% success rate**, có **structured decomposition** đạt **78%** — improvement 2.4× |
| 2 | **Stanford HAI (2024)** | Task decomposition giảm **60% token usage** cho complex tasks — agent không "lạc đề" giữa subtask |
| 3 | **Anthropic (2025)** | Claude Code với task planning resolve **44% more SWE-bench issues** — planning là difference giữa "agent" và "chatbot" |

1. **Microsoft Research (2025)**: AI agents thực hiện complex tasks **without planning** chỉ đạt **32% success rate**, trong khi agents có **structured decomposition** đạt **78%** — improvement 2.4×.
2. **Stanford HAI (2024)**: Task decomposition giảm **60% token usage** cho complex tasks vì agent không "lạc đề" giữa các subtask.
3. **Anthropic (2025)**: Claude Code với task planning resolve **44% more SWE-bench issues** so với prompt-only approach — planning là difference giữa "agent" và "chatbot".

#### Triết lý cốt lõi:

```
Plan & Decompose = Analyze → Prioritize → Sequence → Execute → Validate
```

**5 Levels của Task Planning**:
- **Level 1**: Chia nhỏ tác vụ thành các subtask (decomposition)
- **Level 2**: Sắp xếp thứ tự subtask theo phụ thuộc (ordering)
- **Level 3**: Estimate effort cho mỗi subtask (estimation)
- **Level 4**: Identify risks và fallback plans (risk assessment)
- **Level 5**: Monitor progress và replan khi cần (adaptive planning)

**Analogies**: Plan & Decompose giống như chạy xe có GPS — không chỉ biết điểm đến (goal), mà còn được chia chặng (decompose), gợi ý đường ngon nhất (prioritize), áng chừng thời gian tới nơi (estimate), và tự tìm đường khác khi kẹt xe (replan). Không có GPS, bạn có thể chạy cả ngày mà vẫn chẳng tới nơi.

**Nếu bỏ qua bước này**: agent ôm mọi thứ làm cùng lúc → quá tải context, bịa bừa vì thiếu cấu trúc rõ ràng, code chỗ nọ đá chỗ kia, cuối cùng tốn token gấp 3-5 lần so với khi có kế hoạch tử tế.

## Tổng Quan

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tổng Quan là bức tranh bao quát về Planning & Decomposition — quá trình biến một công việc lớn, mơ hồ thành chuỗi các bước nhỏ, rõ ràng và thực thi được, giống như chia một con voi lớn thành nhiều miếng nhỏ dễ nuốt.
>
> **Ẩn dụ/so sánh:** Giống đầu bếp trước một bữa tiệc lớn: thay vì nấu "một món khổng lồ", anh ta chia thành nhiều món nhỏ, mỗi món một khâu, rồi mới bắt tay vào bếp.
>
> **Vì sao quan trọng:** Vì không có kế hoạch, AI dễ nhảy lung tung, làm sai thứ tự hoặc bỏ sót bước — phần này giúp bạn hiểu khung tổng thể trước khi đi vào chi tiết.

Khi gặp việc khó, AI Agent cần đi theo đúng bài: **phân tích → lên kế hoạch → chia nhỏ → làm từng bước**. Đây chính là kỹ năng biến LLM từ "anh chàng chỉ biết chém gió" thành "người làm được việc".

Trong Harness Engineering, Planning & Decomposition đóng vai **"bộ não tổng chỉ huy"** — quyết định mọi món khác (tools, memory, guardrails) được dùng lúc nào, ở đâu, thế nào.

```
┌──────────────────────────────────────────────────────────────────┐
│                  PLAN & DECOMPOSE TASK                            │
│                                                                  │
│  Complex Task                                                    │
│  "Triển khai hệ thống BHYT cho công ty 100 người"              │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────────┐                                               │
│  │  PLANNING    │  Phân tích → Chia task → Đánh giá thứ tự     │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ DECOMPOSE    │  Task lớn → Sub-tasks → Sub-sub-tasks        │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  EXECUTE     │  Sub-task 1 → 2 → 3 → ... → Done            │
│  └──────┬───────┘                                               │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │  VALIDATE    │  Kiểm tra kết quả → Re-plan nếu cần         │
│  └──────────────┘                                               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Tools ←→ Memory ←→ Guardrails ←→ Feedback ←→ Permissions │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Tại Sao Planning & Decomposition Quan Trọng?

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Đây là phần lý giải vì sao lập kế hoạch được xem là "bộ não điều khiển" của AI Agent: nó biến LLM từ công cụ chỉ biết trả lời câu hỏi thành tác nhân biết hành động từng bước có chủ đích.
>
> **Ẩn dụ/so sánh:** Giống người lái xe có bản đồ so với người lái xe không bản đồ: cả hai đều biết chạy, nhưng người có bản đồ sẽ đến đích còn người kia thì lạc đường.
>
> **Vì sao quan trọng:** Vì thiếu planning, agent làm lộn xộn, tốn token và dễ kẹt trong vòng lặp — phần này đưa bằng chứng khoa học để bạn đầu tư vào structured planning ngay từ đầu.

> *"Agent mà không có planning thì giống bác tài ôm vô-lăng mà không có bản đồ — xe vẫn chạy, nhưng lạc đường là cái chắc."*

### Triết Lý Cốt Lõi

LLM "chém gió" thì giỏi, nhưng gặp việc khó kiểu **"triển khai hệ thống BHYT cho công ty 100 người"** là hay trượt vào một trong hai cái hố quen thuộc:

**Lỗi 1: Oversimplification** — Agent hùng hục nhảy vào code mà không plan gì → làm sai yêu cầu → cuối cùng đập đi làm lại từ đầu.

**Lỗi 2: Analysis Paralysis** — Agent mổ xẻ đủ kiểu mà mãi không chịu bắt tay vào làm, người dùng ngồi chờ dài cổ.

**Cách gỡ**: Structured Planning — một khung rõ ràng giúp agent **nghĩ kỹ trước khi làm**, mà vẫn **ra tay đúng lúc**.

### Bằng Chứng Nghiên Cûu

#### LangChain (2025): "ReAct vs Plan-and-Execute"
> Agents sử dụng **Plan-and-Execute pattern** hoàn thành tasks phức tạp với **40% ít hơn retries** so với ReAct (reactive) pattern.

Nguyên nhân: lên plan trước nên biết cần tool nào → đỡ đi nhầm đường → bớt hẳn một nửa số lần gọi tool thừa.

#### Microsoft Research (2024): "Task Decomposition in LLM Agents"
> Task mà được chẻ thành từng cụm **3-7 việc** nhỏ thì độ chính xác tăng **52%** so với để nguyên một cục to đùng.

**Quy tắc 7±2**: cũng giống tâm lý học nói về trí nhớ con người (Miller's Law) — não mình (và cả LLM) làm việc ngon nhất khi trong đầu chỉ giữ tầm 5-9 món một lúc.

#### Devin AI & OpenHands (2025)
> Các coding agent xịn nhất hiện nay đều chơi kiểu **chia tầng**: Task → Epic → Story → Sub-task. Nhờ vậy làm nhanh **gấp 2.8 lần** so với liệt kê task kiểu danh sách phẳng.

### Phân Tích Chi Phí & Lợi Ích (Cost-Benefit Analysis)

| Chi Phí / Giá Trị | Không Có Planning | Có Planning + Decomposition |
|---|---|---|
| **Retry Rate** | 40-60% tasks cần retry | 10-15% tasks cần retry |
| **Tool Calls** | 3-5x redundant calls | Gần như minimal calls |
| **Token Usage** | Cao (phải re-process context) | Thấp hơn 30-50% |
| **Time to Complete** | Unpredictable, thường chậm | Predictable, typically faster |
| **User Trust** | Thấp vì kết quả bất ngờ | Cao vì có visibility vào plan |

**ROI**: bỏ ra 15-30 giây đầu để lên kế hoạch → tiết kiệm 5-15 phút sửa sai về sau. Tỉ lệ lời **1:20**.

### Analogies Minh Họa

**Analogies 1: Thợ Xây và Bản Vẽ**
- **Không planning** = Thợ xây bắt tay ngay vào tường → Cột lệch, mái nghiêng → Phải đập bỏ làm lại
- **Có planning** = Thợ xây đo đạc, vẽ bản vẽ, kiểm tra nền → Xây đúng lần đầu
- **Decomposition** = Bản vẽ lớn → Bản vẽ chi tiết từng tầng → Bản vẽ từng phòng

**Analogies 2: Bếp and Menu**
- **Không planning** = Đầu bếp nấu ngẫu nhiên từ nguyên liệu có sẵn → Món ăn hỗn tạp
- **Có planning** = Đầu bếp lên menu → Phân công: người rửa, người cắt, người nấu → Món ra đúng giờ
- **Decomposition** = Menu lớn → Courses → Dishes → Ingredients + Steps

**Analogies 3: Dự án Software**
- **Không planning** = Developer code ngay không cần spec → Feature creep, bugs
- **Có planning** = Sprint planning → User stories → Tasks → Code
- **Decomposition** = Epic → Feature → Story → Sub-task → Code

### Bối Cảnh Tiến Hóa (Evolutionary Context)

```
┌──────────────────────────────────────────────────────────────────┐
│              EVOLUTION OF AGENT PLANNING                          │
│                                                                  │
│  2022-2023: No Planning (Pure ReAct)                            │
│  └── Agent: Think → Act → Observe → Think → Act...              │
│      Vấn đề: Không biết tổng thể, hay lạc hướng                 │
│                                                                  │
│  2023-2024: Chain-of-Thought (CoT)                              │
│  └── Agent: Think step-by-step before acting                    │
│      Vấn đề: CoT linear, không branch/replan                    │
│                                                                  │
│  2024-2025: Plan-and-Execute                                    │
│  └── Agent: Create full plan → Execute step-by-step             │
│      Vấn đề: Plan cứng nhắc, không adapt khi thay đổi          │
│                                                                  │
│  2026+: Adaptive Hierarchical Planning                          │
│  └── Agent: Plan → Execute → Monitor → Re-plan dynamically      │
│      + Hierarchical decomposition (Task → Epic → Story)         │
│      + Dependency graph + Priority ordering                     │
│      + Automatic replanning when subtask fails                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Nếu Bạn Bỏ Qua Planning...

**1. Vòng lặp vô tận (Infinite Loop)**
- Agent làm A → B → A → B… xoay vòng mãi không xong
- Vì ngay từ đầu không chốt trong plan: "khi nào thì được coi là xong"

**2. Việc đẻ thêm việc (Scope Creep)**
- Agent tự "vẽ" thêm tính năng chẳng ai nhờ → vừa tốn token vừa tốn thời gian
- Ví dụ kinh điển: nhờ "viết hello world" mà agent tiện tay gắn thêm authentication, logging, i18n…

**3. Cầm nhầm "đồ nghề" (Wrong Tool Selection)**
- Không plan trước nên mỗi bước vớ nhầm tool → làm xong lại phải undo, làm lại
- Ví dụ: chỗ cần đọc (search) thì lại đi ghi (write), chỗ cần kiểm tra (verify) thì lại đi viết mới

**4. Quên bước (Missing Steps)**
- Agent quên mất mấy khâu quan trọng → kết quả dở dang
- Ví dụ: deploy code mà quên test, quên lint, quên commit

**5. Sai một ly, đi luôn cả dặm (Cascading Errors)**
- Bước 1 sai → các bước 2-3-4-5 sai theo dây chuyền → cuối cùng phải làm lại cả cụm
- Vì thiếu điểm kiểm tra (validation checkpoint) chặn giữa các bước

### Best Practices (Và Tại Sao)

| Quy tắc | Lý do |
|---|---|
| Luôn decompose task > 3 steps thành sub-tasks |LLM context window hạn chế, 1 task quá lớn dễ lose focus |
| Đặt termination condition cho mỗi sub-task | Ngăn infinite loops, biết khi nào "done" |
| Thêm validation checkpoint sau mỗi major step | Catch errors early, không để cascade |
| Đánh giá dependency trước khi execute | Task A cần hoàn thành trước Task B → execute tuần tự |
| Limit plan depth ≤ 4 levels | Quá sâu dễ lose context tổng thể |
| Re-plan khi sub-task fail | Thay vì retry một cách mù quáng, phân tích root cause và adjust plan |

---

## Nội Dung

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Đây là bảng mục lục của module: 13 chủ đề lớn từ chia nhỏ tác vụ, thuật toán lập kế hoạch, kiểu agent, đến case study thực tế và các công cụ hỗ trợ.
>
> **Ẩn dụ/so sánh:** Giống bản đồ tuyến tàu điện — nhìn qua các trạm để biết mình nên xuống ở đâu; đọc theo thứ tự 1 đến 13 là lộ trình hợp lý nhất.
>
> **Vì sao quan trọng:** Vì nhìn bao quát trước giúp bạn biết mình đang đứng ở đâu và nên đi sâu vào phần nào.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Task Decomposition Patterns](#1-task-decomposition-patterns) | Các mô hình chia task |
| 2 | [Planning Algorithms](#2-planning-algorithms) | Thuật toán lập kế hoạch |
| 3 | [Agent Workflows](#3-agent-workflows) | Các kiểu workflow của agent |
| 4 | [State Management](#4-state-management) | Quản lý trạng thái |
| 5 | [ReAct Pattern](#5-react-pattern) | Reasoning + Acting |
| 6 | [Harness-Integrated Planning](#6-harness-integrated-planning) | Tích hợp planning với harness |
| 7 | [Case Studies Thực Tế](#7-case-studies-thực-tế) | SWE-agent, Anthropic, Claude Code |
| 8 | [Design Principles](#8-design-principles) | Nguyên tắc thiết kế |
| 9 | [Best Practices](#9-best-practices) | DO/DON'T chi tiết |
| 10 | [Testing Planning Systems](#10-testing-planning-systems) | Kiểm thử hệ thống planning |
| 11 | [Advanced Patterns](#11-advanced-patterns) | Hierarchical, Self-reflective |
| 12 | [Tools & Frameworks](#12-tools--frameworks) | LangGraph, AutoGen, CrewAI |
| 13 | [Tương Lai](#13-tương-lai) | Xu hướng 2026-2028 |

---

## 1. Task Decomposition Patterns

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Task Decomposition (phân chia tác vụ) là cách chia một mục tiêu lớn thành nhiều mảnh nhỏ gọi là subtask, mỗi mảnh đủ nhỏ để AI xử lý gọn gàng và dễ kiểm soát.
>
> **Ẩn dụ/so sánh:** Giống chia một công trình lớn thành các hạng mục: đổ móng → xây tường → lợp mái → hoàn thiện. Không thể đổ cả tòa nhà làm một lần.
>
> **Vì sao quan trọng:** Vì một task quá to làm LLM dễ lạc đề, ngốn context window và hallucinate — chia nhỏ giúp agent thực hiện chắc chắn từng bước và kiểm soát tiến độ dễ dàng.


### 1.1 Các Mô Hình Phân Chia

Mục này chỉ ra **đủ kiểu cắt việc lớn thành việc nhỏ**: làm nối đuôi nhau, làm song song, rẽ nhánh theo điều kiện, chia cha-con theo tầng, làm đi làm lại tới khi đạt, hoặc đan xen theo đồ thị. Mỗi kiểu là một "thế trận" chạy việc khác nhau — bạn cứ nhìn mấy ô hình ASCII bên dưới là thấy ngay dáng dấp từng kiểu, rồi hẵng chọn kiểu hợp với bài toán của mình.

> Cứ hình dung như sếp chia việc cho đội: có việc phải làm nối tiếp nhau, có việc chia cho mấy người cùng làm một lúc (song song), có việc thì "làm xong A mới được đụng vào B".

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK DECOMPOSITION PATTERNS                          │
│                                                                  │
│  1. SEQUENTIAL (Tuần tự)                                        │
│  ┌────┐   ┌────┐   ┌────┐   ┌────┐                            │
│  │ T1 │──►│ T2 │──►│ T3 │──►│ T4 │                            │
│  └────┘   └────┘   └────┘   └────┘                            │
│  Input T2 = Output T1                                          │
│                                                                  │
│  2. PARALLEL (Song song)                                        │
│  ┌────┐                                                        │
│  │ T1 │──┐                                                     │
│  └────┘  │  ┌────┐   ┌────┐                                   │
│  ┌────┐  ├─►│Merge│──►│Final│                                  │
│  │ T2 │──┤  └────┘   └────┘                                   │
│  └────┘  │                                                     │
│  ┌────┐  │                                                     │
│  │ T3 │──┘                                                     │
│  └────┘                                                        │
│                                                                  │
│  3. CONDITIONAL (Có điều kiện)                                  │
│  ┌────┐                                                        │
│  │ Q  │──┐                                                     │
│  └────┘  │                                                     │
│          ├── YES ──►┌─────┐                                    │
│          │          │ T_A │                                    │
│          │          └─────┘                                    │
│          └── NO  ──►┌─────┐                                    │
│                     │ T_B │                                    │
│                     └─────┘                                    │
│                                                                  │
│  4. HIERARCHICAL (Phân cấp)                                    │
│           ┌────────┐                                            │
│           │ Task   │                                            │
│           └───┬────┘                                            │
│          ┌────┼────┐                                            │
│       ┌──┴──┐ ┌──┴──┐ ┌──┴──┐                                 │
│       │Sub1 │ │Sub2 │ │Sub3 │                                 │
│       └──┬──┘ └─────┘ └─────┘                                 │
│       ┌──┴──┐                                                   │
│       │Sub1a│                                                   │
│       └─────┘                                                   │
│                                                                  │
│  5. ITERATIVE (Lặp lại)                                        │
│  ┌────────┐                                                    │
│  │Implement│◄──┐                                               │
│  └────┬───┘   │                                               │
│       ▼       │                                               │
│  ┌────────┐   │                                               │
│  │Evaluate │──►│  Until: pass criteria                         │
│  └────────┘   │                                               │
│       │       │                                               │
│       └───────┘                                               │
│                                                                  │
│  6. DAG (Directed Acyclic Graph)                                │
│       ┌────┐                                                    │
│       │ T1 │──┐                                                 │
│       └────┘  │  ┌────┐                                        │
│               ├──│ T3 │──┐                                     │
│       ┌────┐  │  └────┘  │  ┌────┐                            │
│       │ T2 │──┘           ├─│ T5 │──►Done                      │
│       └────┘              │  └────┘                            │
│       ┌────┐  │  ┌────┐  │                                     │
│       │ T4 │──┘  │ T6 │──┘                                     │
│       └────┘     └────┘                                        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Implementation

Code bên dưới là bộ cài đặt Python đầy đủ cho các pattern ở mục 1.1: lớp `Task` định nghĩa "một mảnh việc" gồm những gì (loại, trạng thái, dependency, số lần retry…), còn lớp `TaskPlanner` là "ông não" chuyên chẻ việc lớn thành việc nhỏ bằng LLM, tự đoán dependency và áng chừng độ khó. Bạn cứ đọc từ trên xuống: xem "mảnh việc" được khai báo ra sao trước, rồi mới ngó cách "ông não" chẻ việc (`decompose()`) và chấm độ khó (`estimate_complexity()`).

> Cứ như đọc bản vẽ chi tiết: coi "một viên gạch" trông thế nào đã, rồi mới xem "thợ cả" định xây cả bức tường bằng gạch đó ra sao.

> Giống đọc bản thiết kế chi tiết: xem cách "khai báo một mảnh việc" ra sao, rồi mới xem cách "bộ não" cắt công việc đó thành các mảnh nhỏ.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-implementation.py`](examples/01-1-2-implementation.py)

</details>

### 1.3 So Sánh Các Pattern

Bảng dưới là "bảng tổng kết" so điểm 6 pattern theo 4 tiêu chí: chạy nhanh không (Speed), hàng có đẹp không (Quality), tốn token ra sao (Token Cost) và hợp với ca nào (Best For). Đọc theo hàng mà chọn: cần nhanh gọn → Sequential/Parallel; cần hàng xịn, chậm tí cũng được → Hierarchical/Iterative.

> Như đi mua điện thoại: ngó một bảng so sánh là biết ngay con nào hợp túi tiền, khỏi phải mượn từng con về xài thử.

```
┌──────────────────┬──────────┬──────────┬────────────────┬──────────────┐
│ Pattern          │ Speed    │ Quality  │ Token Cost     │ Best For     │
├──────────────────┼──────────┼──────────┼────────────────┼──────────────┤
│ Sequential       │ ⭐⭐⭐⭐⭐  │ ⭐⭐⭐      │ Low            │ Simple tasks │
│ Parallel         │ ⭐⭐⭐⭐   │ ⭐⭐⭐      │ Medium (gộp)   │ Independent  │
│ Conditional      │ ⭐⭐⭐    │ ⭐⭐⭐⭐    │ Low-Medium     │ Dynamic      │
│ Hierarchical     │ ⭐⭐      │ ⭐⭐⭐⭐⭐  │ Medium-High    │ Complex      │
│ Iterative        │ ⭐       │ ⭐⭐⭐⭐⭐  │ High (lặp)     │ Quality-first│
│ DAG              │ ⭐⭐⭐    │ ⭐⭐⭐⭐⭐  │ Medium         │ Dependencies │
└──────────────────┴──────────┴──────────┴────────────────┴──────────────┘
```

---

## 2. Planning Algorithms

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Planning Algorithms là những "cách suy nghĩ" có cấu trúc giúp AI quyết định thực hiện công việc theo trình tự nào, cân nhắc nhiều phương án và chọn đường đi tối ưu trước hoặc trong khi làm.
>
> **Ẩn dụ/so sánh:** Giống người đi du lịch dùng GPS: người chỉ lên kế hoạch một lần rồi đi (Plan-and-Solve), người thử nhiều tuyến rồi chọn tuyến tốt nhất (Tree of Thoughts), người vẽ hết cả hành trình rồi giao cho ai đó chạy (ReWOO).
>
> **Vì sao quan trọng:** Vì chọn sai thứ tự hành động khiến agent lãng phí token và kẹt trong những bước không cần thiết — đúng thuật toán giúp làm ít mà đạt hiệu quả cao.


### 2.1 LLM-Based Planning (Plan-and-Solve)

Cách này đúng kiểu bạn lên "to-do list" trước khi xắn tay áo: AI viết các bước ra giấy trước, làm từng bước một, xong bước nào ngó lại bước đó, bước nào hỏng thì **vẽ lại đường đi** (re-plan) chứ không cắm đầu thử lại y chang. Code bên dưới mô phỏng đúng vòng đời đó qua các hàm `plan()` → `solve_step()` → `verify()` → `replan()`.

> Y như nấu ăn theo công thức mẹ cho: ghi sẵn các bước → làm từng bước → nếm thử (verify) → mặn quá thì tự bớt muối ở lần sau, chứ không nấu lại y hệt nồi cũ.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-1-llm-based-planning-plan-and-solve.py`](examples/02-2-1-llm-based-planning-plan-and-solve.py)

</details>

### 2.2 Tree of Thoughts (ToT)

Khác với kiểu suy nghĩ một đường thẳng như Plan-and-Solve, ToT **bung ra nhiều nhánh suy nghĩ cùng lúc**, chấm điểm từng nhánh, rồi dồn sức đào sâu nhánh nào ngon ăn nhất. Code bên dưới dùng BFS (đi theo từng tầng) kèm tỉa cành (pruning) cho đỡ nổ số nhánh: mỗi tầng chỉ giữ lại top-k nhánh điểm cao nhất.

> Như hội chẩn của bác sĩ: đưa ra 3 phác đồ, chấm từng phác đồ theo rủi ro và triển vọng, rồi chọn phác đồ sáng cửa nhất để theo.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-2-tree-of-thoughts-tot.py`](examples/03-2-2-tree-of-thoughts-tot.py)

</details>

### 2.3 ReWOO (Reasoning Without Observation)

Chiêu chính là **tách bạch lúc nghĩ và lúc chạy tool ra làm hai ca riêng**: AI vẽ trọn bộ kế hoạch ngay từ đầu (bước nào xài tool gì, câu query ra sao), cho chạy một lèo hết, rồi mới gom kết quả về viết câu trả lời. Được cái gọi LLM ít lần nên rẻ hơn; dở cái là giữa đường có biến thì xoay hơi chậm. Class `ReWOOPlanner` trong code minh họa đúng vòng plan-all → execute → synthesize đó.

> Như đặt trọn tour du lịch từ A tới Z trước giờ lên xe: đi giữa đường khỏi phải gọi điện hỏi lại, nhưng lỡ một điểm dừng bị đóng cửa thì phải xử lý dồn một cục.

> Giống đặt trọn một tour du lịch từ A đến Z trước khi đi: không cần gọi điện hỏi lại giữa chừng, nhưng nếu một điểm dừng bị đóng cửa thì phải xử lý dồn dập sau.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-2-3-rewoo-reasoning-without-observation.py`](examples/04-2-3-rewoo-reasoning-without-observation.py)

</details>

---

## 3. Agent Workflows

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Agent Workflows là các "kịch bản vận hành" mô tả trình tự AI suy nghĩ (reasoning), hành động (action) và nhìn lại kết quả (observation) để hoàn thành mục tiêu.
>
> **Ẩn dụ/so sánh:** Giống cách một đoàn phim tổ chức làm việc: đội một người tự lo mọi thứ (single agent), đội chia vai như đạo diễn – biên kịch – diễn viên (multi-agent), hay đội chạy theo quy trình cố định (state machine).
>
> **Vì sao quan trọng:** Vì kịch bản vận hành quyết định agent phản ứng linh hoạt hay máy móc — chọn đúng kiểu workflow giúp công việc hoàn thành mịn và đúng hạn.


### 3.1 Các Kiểu Agent

Đây là bản đồ gọi tên **6 kiểu tổ chức agent hay gặp nhất**, từ đơn giản tới phức tạp: ReAct (vừa nghĩ vừa làm xen kẽ), Plan-and-Execute (vẽ hết đường rồi mới chạy), Reflective (làm xong ngồi ngẫm rồi làm tốt hơn), Multi-Agent (mỗi người một vai cùng phối hợp), LangGraph-style (chạy theo máy trạng thái, tới ngã ba thì rẽ theo điều kiện), và Hierarchical (sếp trên giao việc cho lính dưới). Mấy ô hình ASCII bên dưới vẽ rõ luồng gọi giữa các bên — đây là tấm hình đáng giá nhất để bạn hình dung cả module.

> Như cách một công ty vận hành: có lúc một nhân viên cân hết, có lúc phòng kế hoạch chia việc cho mấy phòng ban cùng làm.

> Giống một công ty: có thể một nhân viên xử lý tất cả, hoặc phòng kế hoạch chia việc cho nhiều phòng ban phối hợp.

```
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT WORKFLOW TYPES                            │
│                                                                  │
│  1. REACT (Reasoning + Acting)                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Think → Act → Observe → Think → Act → ... → Answer     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  2. PLAN-AND-EXECUTE                                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Plan all steps → Execute step 1 → 2 → 3 → Report      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  3. REFLECTIVE                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Act → Reflect → Improve → Act → Reflect → ...          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. MULTI-AGENT (Anthropic Pattern)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Planner Agent ─┬─► Coder Agent                         │   │
│  │                 ├─► Researcher Agent                     │   │
│  │                 └─► Reviewer Agent ──► Final Output     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  5. LANGGRAPH-STYLE (State Machine)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  [Start] → [Router] → [Tool_A] or [Tool_B] → [End]     │   │
│  │                         ↑               │                │   │
│  │                         └───────────────┘                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  6. HIERARCHICAL (Claude Code Pattern)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Supervisor → Sub-Agent 1 (parallel)                     │   │
│  │           → Sub-Agent 2 (parallel)                       │   │
│  │           → Sub-Agent 3 (sequential) → Merge → Output   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent Implementation

Code dưới đây dựng 2 kiểu workflow vừa kể thành hàng thật: lớp `SimpleAgent` là anh nhân viên một mình cân hết, chạy vòng Think → Act → Observe kèm chốt an toàn (kiểm tra tool trước và sau khi gọi), còn lớp `MultiAgent` là cả team mỗi người một nghề, có một điều phối viên (coordinator) chia việc — gom kết quả — chấm điểm — ráp lại. Bạn cứ bấm mở và đọc từng hàm theo tên là hiểu.

> Một bên như anh xe ôm công nghệ tự chạy cuốc (SimpleAgent), một bên như đội trưởng công trình chia việc rồi gom báo cáo về (MultiAgent).

> Giống một nhân viên tự quản (SimpleAgent) so với một team leader chia việc rồi gom kết quả về (MultiAgent).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-3-2-agent-implementation.py`](examples/05-3-2-agent-implementation.py)

</details>

---

## 4. State Management

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** State Management là cơ chế "ghi sổ" toàn bộ trạng thái của agent trong lúc làm việc: biến số nào đã đổi, tiến trình đang ở đâu, và có thể quay về mốc nào nếu xảy ra lỗi.
>
> **Ẩn dụ/so sánh:** Giống chơi game có điểm lưu (save point): sắp đánh boss thì lưu game lại, lỡ thua thì load đúng chỗ đó chứ khỏi cày lại từ đầu.
>
> **Vì sao quan trọng:** Vì agent chạy lâu mà sập giữa chừng thì dễ mất trắng — có state management là đứng lên chạy tiếp ngay, khỏi làm lại từ con số 0.

Cuốn "sổ cái" bên dưới là lớp `AgentState`: lưu giá trị kèm lịch sử phiên bản (`history`), chụp ảnh thời điểm (`checkpoint`), quay về mốc cũ (`rollback`), rồi xuất ra chuỗi context cho LLM đọc (`to_context`). Bạn cứ bấm mở và đọc từng hàm theo tên là rõ.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-4-state-management.py`](examples/06-4-state-management.py)

</details>

---

## 5. ReAct Pattern

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** ReAct (Reasoning + Acting) là vòng lặp "nghĩ → làm → ngó kết quả" quay đi quay lại: AI tự lẩm bẩm tính bước tiếp theo (Thought), xài công cụ (Action), rồi đọc kết quả dội về (Observation) trước khi chốt bước kế tiếp.
>
> **Ẩn dụ/so sánh:** Như người nấu ăn vừa nêm vừa nếm: nêm một tí → nếm thử → chỉnh tiếp, lặp tới khi vừa miệng mới thôi — chứ không đổ gia vị một phát rồi cầu may.
>
> **Vì sao quan trọng:** Vì đời thực nay thế này mai thế khác, agent phải biết nhìn kết quả thật mà tự bẻ lái, thay vì ôm khư khư kế hoạch cũ.

Lớp `ReActAgent` bên dưới là bản dựng chuẩn của vòng lặp Thought → Action → Observation, có kèm chốt an toàn `max_steps`, kiểm tra tool trước khi gọi và đếm token. Bạn cứ bấm mở, xem cách nó bóc tách câu trả lời của LLM rồi xoay vòng các bước cho tới khi ra được "Final Answer".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-5-react-pattern.py`](examples/07-5-react-pattern.py)

</details>

---

## 6. Harness-Integrated Planning

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Harness-Integrated Planning là cách "cắm" bộ lập kế hoạch vào khung sườn (Harness) của cả hệ thống: từ đây planner không đánh lẻ nữa mà có Guardrails đứng sau lưng giám sát, có Memory nhắc bài, lại thêm vòng Feedback góp ý sau mỗi chặng.
>
> **Ẩn dụ/so sánh:** Như công trình có ban giám sát: thợ (planner) vẫn chia giai đoạn và thi công, nhưng bản vẽ nào cũng phải qua kiểm duyệt (guardrails), có kho hồ sơ công trình cũ để tra (memory), và mỗi giai đoạn đều có biên bản nghiệm thu (feedback).
>
> **Vì sao quan trọng:** Vì kế hoạch mà thả rông, không ai coi chừng thì dễ lộng quyền hoặc ngã lại đúng cái hố cũ — cắm vào Harness là để kế hoạch vừa an toàn vừa biết tự thích nghi.


### 6.1 TypeScript Interface (Harness Architecture)

Mục này diễn giải **tờ "hợp đồng" (interface) của Harness**: một Planning System chuẩn thì phải có những năng lực nào (decompose, replan, estimateComplexity…) và bắt tay với tools, memory, guardrails, feedback ra sao. Trong TypeScript, `interface` đúng nghĩa là bản cam kết — đã ghi vào là lớp triển khai phải có đủ. Class `HarnessPlanner` bên dưới là bản làm thật theo đúng hợp đồng đó.

> Như hợp đồng giao khoán xây nhà: đã nhận thầu là phải đủ các hạng mục ghi trong hợp đồng, thiếu một gạch đầu dòng cũng không xong.

<details>
<summary><b>6.1 TypeScript Interface (Harness Architecture) (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/08-6-1-typescript-interface-harness-architecture.ts`](examples/08-6-1-typescript-interface-harness-architecture.ts)

</details>

---

## 7. Case Studies Thực Tế

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies là mấy "ca người thật việc thật", mổ xẻ cách 4 sản phẩm AI có tiếng (SWE-agent, Anthropic Multi-Agent, Claude Code, Cursor) dựng hệ thống lập kế hoạch ngoài đời thực.
>
> **Ẩn dụ/so sánh:** Như đi xem "bài văn 10 điểm" của bạn học giỏi: coi người ta mở bài, đặt câu hỏi, chữa lỗi ra sao — rồi đem mánh đó về áp cho bài của mình.
>
> **Vì sao quan trọng:** Vì lý thuyết trong sách hay bị "trên trời" — ngó hàng đang chạy ngon ngoài production giúp bạn lượm được mấy mẫu thiết kế đã có người kiểm chứng.


### 7.1. SWE-agent (Princeton NLP) — Planning-First Approach

**Bối cảnh**: SWE-agent xài planning để agent đỡ "đi lạc" trong rừng codebase.

**Vấn đề ban đầu**:
- Agent không có kế hoạch rõ ràng → làm lung tung, đụng đâu sửa đó
- Cứ phải đọc hết cả codebase mới dám bắt đầu → ngốn token
- Làm hoài không biết lúc nào nên dừng

**Giải pháp**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/09-7-1-swe-agent-princeton-nlp-planning-first.ts`](examples/09-7-1-swe-agent-princeton-nlp-planning-first.ts)

</details>

**Kết quả**:
- Tỉ lệ thành công: 12.5% → 20.5% (+64%)
- Token tiêu thụ giảm 30%
- Thời gian xử lý nhanh hơn 40%

**Bài học**: **"Cứ vẽ bản đồ codebase trước rồi hẵng xắn tay — đỡ mất công đi lòng vòng khám phá"**

---

### 7.2. Anthropic Multi-Agent Architecture

**Bối cảnh**: Claude Code phải "đẻ" ra hẳn ứng dụng phức tạp (games, DAW).

**Giải pháp — hệ 3 agent chia vai lập kế hoạch**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/10-7-2-anthropic-multi-agent-architecture.ts`](examples/10-7-2-anthropic-multi-agent-architecture.ts)

</details>

**Kết quả**:
- Dựng được hẳn games, DAW hoàn chỉnh
- Tỉ lệ thành công cao hơn 80% so với chơi single-agent
- Code sạch đẹp hơn nhờ có vòng kiểm duyệt (evaluation loop)

**Bài học**: **"Chia việc → chạy song song → chấm lại (Decompose → Parallelize → Evaluate) — công thức 3 bước cứ thế mà làm"**

**Bài học**: **"Phân chia tác vụ → Song song hóa → Đánh giá (Decompose → Parallelize → Evaluate) — công thức 3 bước"**

---

### 7.3. Claude Code — Hierarchical Planning System

**Bối cảnh**: Bản rò rỉ của Claude Code hé lộ một kiến trúc planning khá cao tay, chia hẳn 3 tầng.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/11-7-3-claude-code-hierarchical-planning-system.ts`](examples/11-7-3-claude-code-hierarchical-planning-system.ts)

</details>

**Tính năng cốt lõi — Dynamic Re-planning**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/12-7-3-claude-code-hierarchical-planning-system.ts`](examples/12-7-3-claude-code-hierarchical-planning-system.ts)

</details>

---

### 7.4. Cursor IDE — Context-Aware Planning

Bối cảnh: Cursor phải lên kế hoạch sửa code **nương theo đúng chỗ bạn đang làm** — file nào đang mở, bôi đen đoạn nào, con trỏ đang đặt ở dòng mấy, vừa sửa gì gần đây. Đoạn code bên dưới cho thấy nó gom ngữ cảnh ra sao, vẽ kế hoạch thay đổi thế nào, rồi tự thu hẹp phạm vi để khỏi đụng lung tung sang mấy file chẳng liên quan.

<details>
<summary><b>7.4. Cursor IDE — Context-Aware Planning (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/13-7-4-cursor-ide-context-aware-planning.ts`](examples/13-7-4-cursor-ide-context-aware-planning.ts)

</details>

**Bài học từ Case Studies**:

| Bài học | SWE-agent | Anthropic | Claude Code | Cursor |
|--------|-----------|-----------|-------------|--------|
| **Plan before act** | ✅ File mapping | ✅ Step decomposition | ✅ 3-level planning | ✅ Context-aware |
| **Limit scope** | ✅ 50 results max | ✅ Step-level | ✅ Hierarchical | ✅ File-scoped |
| **Re-plan on failure** | - | ✅ Evaluation loop | ✅ Dynamic replan | - |
| **Parallel execution** | - | ✅ Group steps | ✅ Sub-agents | - |
| **Use memory** | - | - | ✅ Past patterns | ✅ Recent edits |

---

## 8. Design Principles

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ nguyên tắc "xây cho khéo" (gồm SOLID quen thuộc và "10 điều răn" riêng của nghề planning) giúp bạn dựng module planner gọn gàng, mai mốt muốn nới gì cũng dễ.
>
> **Ẩn dụ/so sánh:** Như bộ quy tắc xây nhà: tường chịu lực đặt đâu, dây điện đi đường nào — làm đúng thì nhà bền, hư chỗ nào sửa chỗ đó; làm ẩu thì sau này đục phá khắp nơi, tốn tiền.
>
> **Vì sao quan trọng:** Vì planner mà cứ đắp thêm tính năng vô tội vạ thì sớm muộn cũng thành "mớ mì spaghetti" rối nùi — giữ đúng nguyên tắc thì hệ sống lâu, nới rộng nhẹ nhàng.


### 8.1 SOLID Cho Planning System

**1. Single Responsibility (Một người một việc)**
- Mỗi planner chỉ lo 1 loại việc (code, research, deploy)
- Mỗi chiêu chia việc (strategy) chỉ xử 1 pattern cụ thể

**2. Open/Closed (Mở để Mở rộng, Đóng để Sửa đổi)**
- Mở cho thêm planning strategies mới
- Đóng cho sửa đổi core decomposition logic

**3. Liskov Substitution (Thay thế Liskov)**
- Các planner có thể thay thế cho nhau
- Cùng interface, khác implementation (ToT, Plan-and-Solve, ReWOO)

**4. Interface Segregation (Phân tách Interface)**
- Không ép planner phải handle tất cả types
- Tách planner theo domain

**5. Dependency Inversion (Đảo ngược Phụ thuộc)**
- Planner phụ thuộc vào Task abstraction, không phụ thuộc vào implementation cụ thể
- Dễ dàng swap decomposition strategy

### 8.2 The 10 Commandments of Task Planning

Đây là 10 "điều răn" rút gọn cả module thành mấy câu ngắn dễ thuộc. Mỗi dòng giữ nguyên câu tiếng Anh chuẩn kèm lời diễn giải tiếng Việt. Bạn cứ đọc lần lượt rồi ngẫm lại mấy ví dụ phía trên — hầu hết pha "toang" của agent đều do phạm vào một trong mười điều này.

```
1. Thou shall DECOMPOSE before EXECUTE
   → Phân task trước khi chạy, đừng nhảy vào code ngay

2. Thou shall RESPECT dependencies
   → Tôn trọng thứ tự, đừng chạy parallel khi cần sequential

3. Thou shall SET token budgets
   → Giới hạn token mỗi task, tránh việc token bùng nổ

4. Thou shall CHECKPOINT regularly
   → Lưu state thường xuyên, để rollback khi cần

5. Thou shall RE-PLAN on failure
   → Tạo kế hoạch mới khi thất bại, đừng thử lại y hệt

6. Thou shall LOG every decision
   → Ghi lại mọi quyết định planning, để debug và improve

7. Thou shall VALIDATE each step
   → Kiểm tra kết quả mỗi bước, đừng chờ cuối mới check

8. Thou shall PARALLELIZE when possible
   → Chạy song song khi được, để tiết kiệm thời gian

9. Thou shall ESTIMATE before starting
   → Ước tính độ phức tạp trước, để chọn strategy phù hợp

10. Thou shall LEARN from past plans
    → Học từ kế hoạch cũ, để cải thiện kế hoạch mới
```

---

## 9. Best Practices

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là cuốn "sổ tay kinh nghiệm" đúc từ lúc chạy agent thật: việc nào nên làm (DO), việc nào nên chừa (DON'T), và cách giữ hầu bao token cho khỏi lủng.
>
> **Ẩn dụ/so sánh:** Như lời dặn của người đi trước: trời báo mưa thì nhớ mang áo mưa, bình xăng gần cạn thì đừng cố chạy — nghe theo đỡ tốn tiền oan.
>
> **Vì sao quan trọng:** Vì mấy lỗi như kẹt vòng lặp hay cháy token rất dễ gặp mà sửa thì đắt — biết trước để né vẫn là cách rẻ nhất.


### 9.1 DO ✅

- **Phân task theo granularities**: broad → medium → fine-grained
- **Xác định dependencies trước khi execute**: Dùng DAG để represent
- **Set timeout và retry cho mỗi task**: Prevent infinite loops
- **Checkpoint trước mỗi operation quan trọng**: Để rollback
- **Re-plan khi gặp failure**: Không retry y hệt
- **Track token usage per task**: Để optimize cost
- **Validate kết quả mỗi step**: Fail fast
- **Parallelize independent tasks**: Tiết kiệm thời gian

### 9.2 DON'T ❌

- **Đừng execute toàn bộ task 1 lần**: Quá rủi ro
- **Đừng ignore failures**: Phân tích nguyên nhân
- **Đừng over-decompose**: Task quá nhỏ = overhead lớn
- **Đừng forget to update state**: State sync rất quan trọng
- **Đừng hardcode task order**: Nên compute từ dependencies
- **Đừng skip validation**: Output chưa verify = chưa hoàn thành
- **Đừng allocate token budget quá lớn**: Prevent waste
- **Đừng use single agent cho complex tasks**: Multi-agent tốt hơn

### 9.3 Token Budget Management

Mỗi task nên có một "hạn mức chi tiêu" token cho riêng mình, y như hạn mức thẻ tín dụng vậy. Class `TokenBudgetManager` bên dưới làm đúng việc đó: chia hạn mức cho từng task (`allocate`), ghi sổ số token đã xài (`report`), coi còn đủ room để chạy tiếp không (`canContinue`), rồi xuất báo cáo tổng kết (`getReport`).

<details>
<summary><b>9.3 Token Budget Management (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/14-9-3-token-budget-management.ts`](examples/14-9-3-token-budget-management.ts)

</details>

---

## 10. Testing Planning Systems

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing Planning Systems đơn giản là viết sẵn mấy bài test tự động (unit test) để coi bộ lập kế hoạch có làm ăn đàng hoàng không: chia task có ngọt không, có tôn trọng dependency không, xài token có chừng mực không.
>
> **Ẩn dụ/so sánh:** Như làm bài kiểm tra 15 phút trước khi thi học kỳ: test lẻ từng phần giúp lòi lỗi sớm, chứ để tới lúc "ra trận" production mới vỡ thì mệt.
>
> **Vì sao quan trọng:** Vì planner mà không test chẳng khác gì ôm bom nổ chậm — bắt bệnh sớm luôn rẻ hơn nhiều so với đợi cháy rồi mới chữa.

Bộ test mẫu bên dưới cover cả `TaskPlanner`, `TokenBudgetManager` lẫn `AgentState`: bạn chạy thẳng tay để coi từng trò (chia task, chặn độ sâu, retry, checkpoint/rollback) có chạy đúng như quảng cáo không.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/15-10-testing-planning-systems.py`](examples/15-10-testing-planning-systems.py)

</details>

---

## 11. Advanced Patterns

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Advanced Patterns là mấy chiêu planning "nâng cao" dành cho ca cực khoai: HTN (chia tầng theo "công thức có sẵn" cho từng loại việc) và Self-Reflective Planning (tự soi gương, tự sửa kế hoạch của mình).
>
> **Ẩn dụ/so sánh:** Như bác đầu bếp lão làng: HTN là có sẵn cả tủ sách công thức để chẻ món; Self-Reflective là sau mỗi lần nấu tự ngẫm "lần sau bớt muối lại".
>
> **Vì sao quan trọng:** Vì ca cực khó thì kế hoạch thẳng một đường đỡ không nổi — mấy chiêu này cho agent vừa chẻ đa tầng vừa tự chữa sai ngay khi thấy mùi khét.


### 11.1 Hierarchical Task Network (HTN)

HTN nối dài ý tưởng chia nhỏ ở mục 1 bằng cách thủ sẵn **mấy "công thức chẻ việc" (methods)**: mỗi loại việc đã có sẵn cách chẻ thành mảnh nhỏ hơn, cứ bóc dần tới khi gặp việc nguyên thủy (primitive) làm được ngay thì dừng. Đoạn code cho thấy cách đăng ký method, ghi điều kiện xài được (precondition), rồi đệ quy chẻ dần theo từng tầng.

> Như tủ đựng mẫu đơn sẵn ở phường: gặp việc gì thì rút đúng mẫu đó ra xài — vừa nhanh vừa chuẩn, khỏi ngồi nghĩ lại từ đầu mỗi lần.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/16-11-1-hierarchical-task-network-htn.py`](examples/16-11-1-hierarchical-task-network-htn.py)

</details>

### 11.2 Self-Reflective Planning

Chiêu này là: agent vẽ kế hoạch xong thì **tự làm giám khảo chấm bài của mình** (đủ chưa, làm nổi không, rủi ro chỗ nào); điểm thấp thì tự sửa theo góp ý của chính mình rồi chấm lại vài vòng. Class `SelfReflectivePlanner` bên dưới code đúng vòng Plan → Reflect → Improve đó, lại còn lưu sổ lịch sử để học từ kết quả thật.

> Như hồi đi học viết nháp văn: viết xong đọc lại, thấy đoạn nào sượng thì sửa, ổn rồi mới nộp bản sạch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/17-11-2-self-reflective-planning.py`](examples/17-11-2-self-reflective-planning.py)

</details>

---

## 12. Tools & Frameworks

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tools & Frameworks là mấy bộ đồ nghề mã nguồn mở có sẵn, giúp bạn dựng hệ planning/agent cho lẹ thay vì ngồi đẽo lại từ khúc gỗ — điển hình là LangGraph, CrewAI và AutoGen.
>
> **Ẩn dụ/so sánh:** Như mua nhà lắp ghép thay vì tự trộn hồ xây gạch: khung sườn (state machine, agent orchestration) có sẵn rồi, bạn chỉ việc ráp và sơn phết theo ý mình.
>
> **Vì sao quan trọng:** Vì ôm đồm viết lại từ đầu vừa lâu vừa dễ toang — xài framework đã có cộng đồng kiểm chứng vừa nhanh vừa chuẩn bài.


### 12.1 LangGraph (Recommended for Planning)

LangGraph cho bạn vẽ workflow như một **máy trạng thái (state machine)** bằng đồ thị: mỗi node là một chặng, mỗi edge là con đường, tới ngã ba thì rẽ theo điều kiện. Đoạn code dựng hẳn một vòng planning khép kín: analyze → plan → validate → execute — validate rớt thì quẹo sang replan, đậu thì đi tiếp tới đích.

> Như sơ đồ tuyến metro: vẽ sẵn các ga (node) với đường ray (edge), tàu cứ thế chạy, tới chỗ rẽ thì bẻ ghi theo tín hiệu.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/18-12-1-langgraph-recommended-for-planning.py`](examples/18-12-1-langgraph-recommended-for-planning.py)

</details>

### 12.2 CrewAI (Multi-Agent Planning)

CrewAI xếp các agent thành hẳn một **đội (crew)**: bạn cắt vai cho từng người (Agent) kèm mục tiêu và đồ nghề riêng, phát task cho từng vai, rồi để cả đội phối hợp "đá" cho xong. Đoạn code dựng ba vai quen thuộc: Planner (ông vẽ đường), Executor (ông xắn tay làm) và Reviewer (ông soi lỗi).

> Như mở công ty mini ba phòng ban, mỗi phòng một sứ mệnh, hợp sức làm xong một dự án.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/19-12-2-crewai-multi-agent-planning.py`](examples/19-12-2-crewai-multi-agent-planning.py)

</details>

### 12.3 AutoGen (Microsoft)

AutoGen của Microsoft cho các agent **ngồi "chat" với nhau** để phối hợp — mỗi agent là một cái đầu biết nhắn tin qua lại. Code mẫu dựng ba nhân vật: planner chuyên bày kế hoạch, executor chuyên xắn tay làm, và user proxy đóng vai người thật ngồi duyệt kết quả cuối.

> Như nhóm chat công việc: một người đề xuất, một người làm, một người chốt "ok" trước khi nộp.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/20-12-3-autogen-microsoft.py`](examples/20-12-3-autogen-microsoft.py)

</details>

---

## 13. Tương Lai

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tương Lai là chương "ngó trước" xem nghề planning cho AI Agent giai đoạn 2026-2028 sẽ đi về đâu: agent tự vẽ kế hoạch, nhiều agent rủ nhau cùng plan, đoán trước rủi ro, và giao diện kéo-thả trực quan.
>
> **Ẩn dụ/so sánh:** Như đọc dự báo thời tiết trước chuyến đi xa: biết trước gió máy ra sao để chuẩn bị áo ấm từ sớm, chứ đừng đợi người ta đi hết rồi mới chạy theo.
>
> **Vì sao quan trọng:** Vì móng nhà bạn đổ hôm nay quyết định 3 năm nữa có cơi thêm tầng được không — ngó trước để đặt tiền đúng chỗ.


### 13.1 Xu Hướng 2026-2028

**1. AI Tự Vẽ Kế Hoạch (AI Self-Planning)**
- Agent tự lên kế hoạch, khỏi cần người mớm tay
- Vừa làm vừa chỉnh theo phản hồi thực tế (real-time feedback)
- Học chéo từ những lần plan trước (planning history)

**2. Rủ Nhau Cùng Plan (Collaborative Planning)**
- Nhiều agents cùng đề xuất rồi bỏ phiếu chọn
- Mỗi đội plan một mảng rồi ráp lại
- Xài chung kho kinh nghiệm lập kế hoạch

**3. Đoán Trước Rủi Ro (Predictive Planning)**
- Ngửi thấy mùi hỏng trước khi nó nổ ra
- Chủ động vẽ lại đường (re-planning) từ sớm
- Chia việc có né chỗ rủi ro cao

**4. Plan Nương Theo Context (Context-Aware Planning)**
- Có bao nhiêu context thì liệu cơm gắp mắm bấy nhiêu
- Chia tài nguyên linh hoạt theo tình hình
- Giữ hầu bao token cho khéo, đừng xài hoang

**5. Vẽ Plan Bằng Kéo-Thả (Visual Planning Interfaces)**
- Trình dựng kế hoạch kéo thả như xếp hình
- Nhìn thấy plan chạy trực tiếp theo thời gian thực
- Thò tay chỉnh plan ngay trên giao diện

### 13.2 Lời Khuyên

```
1. Start with simple patterns
   → Sequential → Parallel → Conditional → Hierarchical

2. Add complexity gradually
   → Đừng implement ToT ngay từ đầu

3. Always validate
   → Check kết quả mỗi bước

4. Learn from failures
   → Store failure patterns

5. Measure everything
   → Track tokens, time, success rate
```

## 14. Bổ Sung Production: Replanning, Cổng Approval, Idempotency & Chặn Bùng Nổ

> Nốt chặn an toàn để plan từ §1–§13 chạy tự động ngoài production mà không "bung".

### 14.1 Định nghĩa

| Thuật ngữ | Định nghĩa |
|------|------------|
| Replanning động | Chọn lúc runtime giữa retry / replan / escalate dựa trên loại lỗi, chi phí đã dùng và độ tin cậy |
| Cổng approval | Checkpoint human-in-loop trước subtask không thể đảo ngược / bán kính ảnh hưởng lớn |
| Idempotency key | `plan_id:subtask_id:input_hash` ổn định để retry không áp dụng side effect hai lần |
| Chặn bùng nổ (explosion guard) | Trần cứng cho độ sâu, fan-out và nhánh ToT × chi phí để chặn planning chạy mất kiểm soát |

### 14.2 Bảng Quyết Định Replanning Động

| Tín hiệu | Retry (giữ plan) | Replan (phân rã mới) | Escalate (con người) |
|--------|-------------------|----------------------------|------------------|
| Lỗi tool thoáng qua (timeout, 429), lần thử <3 | ✅ | — | — |
| Cùng subtask hỏng 3x / lớp lỗi mới | — | ✅ phân rã khác hoặc đổi tool | — |
| Độ tin cậy plan thấp (<0.4), intent mơ hồ | — | ✅ subtask hỏi-làm-rõ trước | — |
| Hành động không đảo ngược (deploy, xóa, thanh toán) | — | — | ✅ cổng approval |
| Đã dùng >80% ngân sách hoặc chạm trần chi phí ToT | — | — (đóng băng) | ✅ kèm tóm tắt |
| Kết quả con mâu thuẫn / vi phạm policy | — | — | ✅ |

Luật chung: mỗi lần đổi hướng đều ghi log `attempt, error_class, decision, reason`; tối đa 3 lần auto-retry, 2 lần auto-replan, quá số đó là phải gọi người vào (escalate).

### 14.3 Cổng Approval Human-in-Loop

**Việc của planner ở cái cổng này.** Mức risk được dán nhãn *ngay lúc vẽ plan* — một subtask
gắn `risk ∈ {high, irreversible}` là ứng viên đi qua cổng, và chính tag đó là khoá mà
`15-approval-gates` dùng để tra phán quyết. Ba việc thuộc module này:

1. **Gán tag, không gắn cổng.** Gắn `db.migrate, prod.deploy, user.delete, external.send`
   là `risk ∈ {high, irreversible}` ngay khi phân rã. Subtask không có tag là `low` và không
   bao giờ chặn.
2. **Liệt kê bán kính ảnh hưởng từ registry policy.** Lấy đúng tập tài nguyên mà subtask
   chạm tới từ registry sandbox/policy ở
   [`12-sandbox-execution` §6](../12-sandbox-execution/README.md) — không phải từ một phỏng
   đoán trong plan.
3. **Từ chối → replan, không retry.** Một lần từ chối ghi lại `reason` và kích hoạt replan
   *loại nhánh bị từ chối* (xem bảng quyết định ở §14.2). Retry lại chính subtask bị từ chối
   sẽ lặp vô hạn.

**Nửa còn lại của cổng thuộc [`15-approval-gates`](../15-approval-gates/README.md)**:
taxonomy tier và TTL, payload bắt buộc có bằng chứng (`diff plan + bán kính ảnh hưởng + output
dry-run + lệnh rollback`), timeout-deny (fail closed), giao thức checkpoint `PAUSED:`, luật
hai-người, và audit trail `approval_request` / `approval_verdict`. Đừng lặp lại những hằng số
đó ở đây — một planner và một gatekeeper bất đồng về cửa sổ hết hạn là một cổng hoặc treo
vĩnh viễn, hoặc tự kích hoạt mà không ai canh.

Mọi approval đều được ghi audit-log `(who, when, diff_hash)` rồi lưu vào trajectory store
(`13-trajectory-observability` §6), để câu "người chưa từng thấy nó" nói ra là có bằng chứng kiểm được, chứ không phải lời chống chế suông.

### 14.4 Idempotency Subtask + Lỗi Một Phần

Key là `f"{plan_id}:{subtask_id}:{sha1(canonical_inputs)}"`. Executor ngó vào result-store trước; lỡ crash giữa chừng thì replay sẽ trả ngay kết quả cache. Gặp lỗi một phần: đánh dấu từng node DAG là `ok/failed/skipped`; nhánh độc lập cứ chạy tiếp, node nào ăn theo node hỏng thì bỏ qua, cuối cùng trả `partial:true + completed[] + failed[]`. Mấy side effect đã làm xong mà phải abort thì bù lại qua `rollback()` đã đăng ký sẵn cho từng subtask.

### 14.5 Chặn Bùng Nổ (Độ Sâu / Fan-out / Chi Phí ToT)

- `MAX_DEPTH=4, MAX_FANOUT=5, MAX_SUBTASKS=25`. Lệnh decompose nào lố độ sâu thì trả về task nguyên tử, khỏi chẻ nữa.
- ToT: `MAX_BRANCHES=3, MAX_ROLLOUTS=9`; mỗi rollout có hạn mức token/thời gian riêng; nhánh nào điểm <0.3 sau 2 bước thì tỉa bỏ.
- Trần chi phí toàn cục: `MAX_TOKENS_PER_PLAN` (ví dụ 100k) + `MAX_TOOL_CALLS=50`; xài tới 80% thì bắn subtask cảnh báo, chạm 100% thì đóng băng và escalate kèm bản tóm tắt `best-so-far`.

<details>
<summary>Python Code — Subtask Idempotent + Quyết Định Replan (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/21-14-5-chan-bung-no-o-sau-fan.py`](examples/21-14-5-chan-bung-no-o-sau-fan.py)

</details>

### 14.6 Checklist

| # | Quy tắc |
|---|------|
| 1 | Phân loại mọi lỗi → retry / replan / escalate theo bảng; log quyết định + lý do |
| 2 | Giới hạn retry (3) và replan (2), rồi escalate — không vòng lặp vô hạn |
| 3 | Chặn mọi subtask không đảo ngược bằng diff + dry-run + rollback + timeout-deny |
| 4 | Idempotency key trên mọi subtask có side effect; cache kết quả để replay |
| 5 | Theo dõi trạng thái DAG một phần; bù khi abort; trả `partial` tường minh |
| 6 | Thực thi `depth ≤4, fan-out ≤5, nhánh ToT ≤3`, trần token/tool toàn cục với cảnh báo 80% |

---

## Tài Liệu Tham Khảo

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Danh sách các bài nghiên cứu (papers) và framework là nguồn gốc của toàn bộ kiến thức trong module — nếu muốn đào sâu học thuật thì bắt đầu từ đây.
>
> **Ẩn dụ/so sánh:** Giống mục "nguồn gốc" cuối bài viết: ghi nơi lấy ý tưởng, đồng thời cho bạn đường về bản gốc nếu muốn tìm hiểu chi tiết hơn.
>
> **Vì sao quan trọng:** Vì các số liệu và mô hình trong module đều bắt nguồn từ những nghiên cứu này — tra đúng gốc giúp bạn tự tin khi trình bày lại.

### Papers & Research

1. **ReAct: Synergizing Reasoning and Acting in Language Models**
   - Yao et al., 2022
   - https://arxiv.org/abs/2210.03629

2. **Tree of Thoughts: Deliberate Problem Solving with Large Language Models**
   - Yao et al., 2023
   - https://arxiv.org/abs/2305.10601

3. **Plan-and-Solve Prompting**
   - Wang et al., 2023
   - https://arxiv.org/abs/2305.04091

4. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
   - Princeton NLP Lab, 2024
   - https://arxiv.org/abs/2405.15793

5. **ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models**
   - Xu et al., 2023
   - https://arxiv.org/abs/2305.18323

### Frameworks

1. **LangGraph** - https://langchain-ai.github.io/langgraph/
2. **CrewAI** - https://www.crewai.com
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **LangChain** - https://langchain.com

---

*Tài liệu: IV. Plan & Decompose Task — HARNESS ENGINEERING EDITION*
*Ngày cập nhật: 16/10/2026*
*Tác giả: AI Knowledge Repository*