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

```python
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    HIERARCHICAL = "hierarchical"
    ITERATIVE = "iterative"
    DAG = "dag"

@dataclass
class Task:
    id: str
    name: str
    description: str
    task_type: TaskType = TaskType.SEQUENTIAL
    status: TaskStatus = TaskStatus.PENDING
    subtasks: List['Task'] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    result: Any = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    max_retries: int = 3
    retry_count: int = 0
    timeout_seconds: int = 300
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    token_budget: Optional[int] = None  # Token limit cho task này
    tools_allowed: List[str] = field(default_factory=list)  # Tools được phép dùng
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "type": self.task_type.value,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "dependencies": self.dependencies,
            "retry_count": self.retry_count,
            "token_budget": self.token_budget,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }
    
    def mark_completed(self, result):
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now().isoformat()
    
    def mark_failed(self, error):
        self.status = TaskStatus.FAILED
        self.error = error
    
    def can_retry(self):
        return self.retry_count < self.max_retries
    
    def can_execute(self, completed_tasks: set):
        """Check if all dependencies are satisfied"""
        return all(dep in completed_tasks for dep in self.dependencies)

class TaskPlanner:
    """
    LLM-based task planner
    
    Phân tích task lớn và chia thành sub-tasks
    Hỗ trợ: hierarchical decomposition, dependency detection, complexity estimation
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def decompose(self, task_description, max_depth=3, current_depth=0):
        """
        Phân tích task và chia thành sub-tasks
        
        Strategy:
        - depth 0-1: Broad decomposition (major phases)
        - depth 2+: Fine-grained decomposition (specific actions)
        """
        if current_depth >= max_depth:
            return [Task(
                id=f"leaf_{current_depth}",
                name=task_description[:50],
                description=task_description,
            )]
        
        if self.llm:
            prompt = f"""Phân tích task sau và chia thành các sub-tasks:

Task: {task_description}
Depth: {current_depth}/{max_depth}

Quy tắc:
- Mỗi sub-task phải cụ thể, có thể thực hiện được
- Xác định dependencies giữa các sub-tasks
- Đánh giá loại (sequential/parallel/conditional)
- Ước tính token budget cho mỗi sub-task
- Liệt kê tools cần thiết cho mỗi sub-task

Output JSON:
{{
  "analysis": "Phân tích task",
  "subtasks": [
    {{
      "name": "...",
      "description": "...",
      "type": "sequential|parallel|conditional",
      "dependencies": [],
      "estimated_tokens": 5000,
      "required_tools": ["tool1", "tool2"]
    }}
  ],
  "estimated_steps": 3
}}"""
            
            response = self.llm(prompt)
            try:
                import json
                data = json.loads(response)
                tasks = []
                for i, st in enumerate(data.get("subtasks", [])):
                    task_type_map = {
                        "sequential": TaskType.SEQUENTIAL,
                        "parallel": TaskType.PARALLEL,
                        "conditional": TaskType.CONDITIONAL,
                    }
                    task = Task(
                        id=f"task_{current_depth}_{i}",
                        name=st["name"],
                        description=st["description"],
                        task_type=task_type_map.get(st.get("type", "sequential"), TaskType.SEQUENTIAL),
                        dependencies=st.get("dependencies", []),
                        token_budget=st.get("estimated_tokens"),
                        tools_allowed=st.get("required_tools", []),
                    )
                    tasks.append(task)
                return tasks
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Phản ứng dự phòng: phân chia tác vụ đơn giản
        return [Task(
            id=f"task_{current_depth}_0",
            name=task_description[:50],
            description=task_description,
        )]
    
    def create_execution_plan(self, root_task):
        """
        Tạo execution plan từ task tree
        
        Returns: Ordered list of tasks to execute with dependency info
        """
        plan = []
        self._traverse(root_task, plan)
        return plan
    
    def _traverse(self, task, plan):
        """DFS traversal to create execution order"""
        if task.task_type == TaskType.SEQUENTIAL:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.PARALLEL:
            plan.append(task)  # Dấu hiệu song song
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        elif task.task_type == TaskType.ITERATIVE:
            task.metadata["max_iterations"] = 5
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
        
        else:
            plan.append(task)
            for subtask in task.subtasks:
                self._traverse(subtask, plan)
    
    def estimate_complexity(self, task):
        """
        Đánh giá độ phức tạp của task
        
        Returns: Score 1-10 with detailed breakdown
        """
        depth = self._get_depth(task)
        breadth = self._get_breadth(task)
        
        # Chấm điểm nâng cao
        score = min(10, depth * 2 + breadth)
        
        # Ước tính Token
        estimated_tokens = self._estimate_tokens(task)
        
        # Chiến lược đề xuất
        if score <= 3:
            strategy = "direct"
            reasoning = "Task đơn giản, execute trực tiếp"
        elif score <= 6:
            strategy = "sequential"
            reasoning = "Task trung bình, chia theo thứ tự"
        else:
            strategy = "hierarchical"
            reasoning = "Task phức tạp, cần phân cấp nhiều tầng"
        
        return {
            "score": score,
            "depth": depth,
            "total_subtasks": breadth,
            "complexity": "simple" if score <= 3 else "medium" if score <= 6 else "complex",
            "estimated_tokens": estimated_tokens,
            "recommended_strategy": strategy,
            "reasoning": reasoning,
        }
    
    def _get_depth(self, task, current=0):
        if not task.subtasks:
            return current
        return max(self._get_depth(s, current + 1) for s in task.subtasks)
    
    def _get_breadth(self, task):
        count = 1
        for sub in task.subtasks:
            count += self._get_breadth(sub)
        return count
    
    def _estimate_tokens(self, task):
        """Ước tính số token cần thiết"""
        base_tokens = len(task.description.split()) * 2  # Ước tính thô
        for sub in task.subtasks:
            base_tokens += self._estimate_tokens(sub)
        return base_tokens
```

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

```python
class PlanAndSolve:
    """
    Plan-and-Solve prompting strategy
    
    Based on paper: "Plan-and-Solve Prompting" (Wang et al., 2023)
    
    1. Plan: Break down the problem into sub-problems
    2. Solve: Execute each sub-problem
    3. Verify: Check results against original problem
    4. Re-plan: If verification fails, create new plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.max_replan_attempts = 3
    
    def plan(self, problem):
        """Step 1: Create a plan"""
        prompt = f"""Hãy lập kế hoạch giải quyết vấn đề sau. 
Đưa ra các bước cụ thể, rõ ràng.

Vấn đề: {problem}

Kế hoạch (mỗi bước trên 1 dòng, bắt đầu bằng số):
1. ...
2. ...
3. ..."""
        
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Bước 1: Phân tích {problem}", "Bước 2: Thực hiện"]
    
    def solve_step(self, step, context=""):
        """Step 2: Solve a single step"""
        prompt = f"""Thực hiện bước sau:

Bước: {step}
Context: {context}

Kết quả:"""
        
        if self.llm:
            return self.llm(prompt)
        return f"Kết quả cho: {step}"
    
    def verify(self, problem, solution):
        """Step 3: Verify solution"""
        prompt = f"""Kiểm tra giải pháp cho vấn đề:

Vấn đề: {problem}
Giải pháp: {solution}

Đánh giá (JSON):
{{
  "complete": true/false,
  "correct": true/false,
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1"]
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"complete": True, "correct": True, "issues": [], "suggestions": []}
    
    def replan(self, problem, original_plan, failed_step, error):
        """Create a new plan based on failure"""
        prompt = f"""Kế hoạch ban đầu thất bại. Hãy tạo kế hoạch mới.

Vấn đề: {problem}
Kế hoạch cũ: {original_plan}
Bước thất bại: {failed_step}
Lỗi: {error}

Kế hoạch mới (mỗi bước trên 1 dòng):
"""
        if self.llm:
            response = self.llm(prompt)
            steps = [line.strip() for line in response.split('\n') 
                    if line.strip() and line.strip()[0].isdigit()]
            return steps
        
        return [f"Fix: {failed_step}"]
    
    def run(self, problem):
        """Execute full plan-and-solve cycle with re-planning"""
        plan = self.plan(problem)
        
        for attempt in range(self.max_replan_attempts):
            results = []
            context = ""
            all_succeeded = True
            
            for i, step in enumerate(plan):
                result = self.solve_step(step, context)
                results.append({"step": step, "result": result})
                context += f"\nBước {i+1} đã hoàn thành: {result[:200]}"
            
            # Xác minh
            verification = self.verify(problem, "\n".join(
                f"{r['step']}: {r['result']}" for r in results
            ))
            
            if verification.get("complete", True) and verification.get("correct", True):
                return {
                    "plan": plan,
                    "results": results,
                    "verification": verification,
                    "attempts": attempt + 1,
                }
            
            # Lập lại kế hoạch dựa trên các vấn đề
            if verification.get("issues"):
                plan = self.replan(
                    problem, plan, 
                    verification["issues"][0],
                    str(verification.get("suggestions", []))
                )
        
        return {
            "plan": plan,
            "results": results,
            "verification": verification,
            "attempts": self.max_replan_attempts,
            "status": "max_attempts_reached",
        }
```

</details>

### 2.2 Tree of Thoughts (ToT)

Khác với kiểu suy nghĩ một đường thẳng như Plan-and-Solve, ToT **bung ra nhiều nhánh suy nghĩ cùng lúc**, chấm điểm từng nhánh, rồi dồn sức đào sâu nhánh nào ngon ăn nhất. Code bên dưới dùng BFS (đi theo từng tầng) kèm tỉa cành (pruning) cho đỡ nổ số nhánh: mỗi tầng chỉ giữ lại top-k nhánh điểm cao nhất.

> Như hội chẩn của bác sĩ: đưa ra 3 phác đồ, chấm từng phác đồ theo rủi ro và triển vọng, rồi chọn phác đồ sáng cửa nhất để theo.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class TreeOfThoughts:
    """
    Tree of Thoughts: Explore multiple reasoning paths
    
    Better than linear chain-of-thought for complex problems
    Based on paper: "Tree of Thoughts" (Yao et al., 2023)
    
    Key insight: Not all reasoning paths are equal.
    ToT explores multiple branches and evaluates which path is most promising.
    """
    
    def __init__(self, llm_func=None, branching_factor=3, max_depth=3):
        self.llm = llm_func
        self.branching_factor = branching_factor
        self.max_depth = max_depth
    
    def generate_thoughts(self, state, n=None):
        """Generate multiple candidate thoughts"""
        n = n or self.branching_factor
        
        prompt = f"""Từ trạng thái hiện tại, hãy nghĩ ra {n} hướng giải quyết khác nhau.

Trạng thái: {state}

Hướng 1: 
Hướng 2: 
Hướng 3: """
        
        if self.llm:
            response = self.llm(prompt)
            thoughts = [t.strip() for t in response.split('\n') 
                       if t.strip().startswith("Hướng")]
            return thoughts[:n]
        
        return [f"Thought {i+1}" for i in range(n)]
    
    def evaluate_thought(self, state, thought):
        """Evaluate how promising a thought is"""
        prompt = f"""Đánh giá hướng giải quyết này (1-10):

Trạng thái: {state}
Hướng: {thought}

Tiêu chí:
- Tính khả thi (0-3)
- Tốc độ giải quyết (0-3)
- Chất lượng kết quả (0-4)

Điểm số (1-10):"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                score = int(''.join(c for c in response if c.isdigit())[:2])
                return min(max(score, 1), 10)
            except (ValueError, IndexError):
                pass
        
        return 5  # Điểm mặc định
    
    def solve(self, problem):
        """
        Tree search: explore best paths
        
        Uses BFS with pruning to avoid exponential explosion
        """
        root_state = {"problem": problem, "path": [], "score": 0}
        
        frontier = [root_state]
        best_solution = None
        best_score = -1
        
        for depth in range(self.max_depth):
            next_frontier = []
            
            for state in frontier:
                thoughts = self.generate_thoughts(
                    f"{state['problem']} | Path: {' → '.join(state['path'])}"
                )
                
                for thought in thoughts:
                    score = self.evaluate_thought(state['problem'], thought)
                    
                    new_state = {
                        "problem": state["problem"],
                        "path": state["path"] + [thought],
                        "score": state["score"] + score,
                    }
                    
                    if new_state["score"] > best_score:
                        best_score = new_state["score"]
                        best_solution = new_state
                    
                    next_frontier.append(new_state)
            
            # Cắt tỉa: chỉ giữ lại top-k đường dẫn tốt nhất
            frontier = sorted(next_frontier, key=lambda x: x["score"], reverse=True)
            frontier = frontier[:self.branching_factor]
        
        return {
            "solution": best_solution["path"] if best_solution else [],
            "total_score": best_score,
            "paths_explored": self.branching_factor ** self.max_depth,
        }
```

</details>

### 2.3 ReWOO (Reasoning Without Observation)

Chiêu chính là **tách bạch lúc nghĩ và lúc chạy tool ra làm hai ca riêng**: AI vẽ trọn bộ kế hoạch ngay từ đầu (bước nào xài tool gì, câu query ra sao), cho chạy một lèo hết, rồi mới gom kết quả về viết câu trả lời. Được cái gọi LLM ít lần nên rẻ hơn; dở cái là giữa đường có biến thì xoay hơi chậm. Class `ReWOOPlanner` trong code minh họa đúng vòng plan-all → execute → synthesize đó.

> Như đặt trọn tour du lịch từ A tới Z trước giờ lên xe: đi giữa đường khỏi phải gọi điện hỏi lại, nhưng lỡ một điểm dừng bị đóng cửa thì phải xử lý dồn một cục.

> Giống đặt trọn một tour du lịch từ A đến Z trước khi đi: không cần gọi điện hỏi lại giữa chừng, nhưng nếu một điểm dừng bị đóng cửa thì phải xử lý dồn dập sau.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ReWOOPlanner:
    """
    ReWOO: Decouple planning from execution
    
    1. PLAN all steps upfront (no observation between steps)
    2. EXECUTE all steps
    3. USE evidence to synthesize answer
    
    Advantage: Fewer LLM calls (batch planning)
    Disadvantage: Less adaptive to failures
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def plan_all(self, task, tools):
        """Generate all plan steps at once"""
        prompt = f"""Tạo kế hoạch hoàn chỉnh cho task sau.

Task: {task}
Tools có sẵn: {list(tools.keys())}

Output JSON:
{{
  "plan": [
    {{"step_id": "e1", "tool": "tool_name", "query": "query for tool"}},
    {{"step_id": "e2", "tool": "tool_name", "query": "query using #e1"}},
    ...
  ],
  "synthesis_prompt": "Dựa trên #e1, #e2, ..., trả lời: {task}"
}}"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"plan": [], "synthesis_prompt": task}
    
    def execute_plan(self, plan, tools):
        """Execute all plan steps, collecting evidence"""
        evidence = {}
        
        for step in plan.get("plan", []):
            tool_name = step.get("tool", "")
            query = step.get("query", "")
            
            # Thay thế tham chiếu bằng bằng chứng trước đó
            for ref_id, ref_val in evidence.items():
                query = query.replace(f"#{ref_id}", str(ref_val))
            
            if tool_name in tools:
                try:
                    result = tools[tool_name](query)
                    evidence[step["step_id"]] = result
                except Exception as e:
                    evidence[step["step_id"]] = f"Error: {e}"
        
        return evidence
```

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

```python
class SimpleAgent:
    """
    Simple agent with tool-calling loop
    
    Pattern: Think → Act → Observe → Repeat
    
    Harness integration:
    - Respects max_iterations (guardrail)
    - Logs all steps (feedback loop)
    - Validates tool permissions
    """
    
    def __init__(self, tools, llm_func, max_iterations=10):
        self.tools = {tool["name"]: tool for tool in tools}
        self.llm = llm_func
        self.max_iterations = max_iterations
        self.memory = []
        self.metrics = {
            "total_iterations": 0,
            "tools_used": {},
            "errors": 0,
            "total_tokens": 0,
        }
    
    def run(self, task):
        """Execute task with tool calls"""
        self.memory = []
        context = f"Task: {task}\n\nAvailable tools: {list(self.tools.keys())}"
        
        for i in range(self.max_iterations):
            # Suy luận (Think): quyết định bước tiếp theo
            thought = self._think(context)
            
            # Kiểm tra nếu đã hoàn thành
            if thought.get("done"):
                return {
                    "answer": thought.get("answer", ""),
                    "steps": self.memory,
                    "iterations": i + 1,
                    "metrics": self.metrics,
                }
            
            # Hành động (Act): thực thi tool với kiểm tra hợp lệ
            tool_name = thought.get("tool")
            tool_input = thought.get("input", {})
            
            if tool_name and tool_name in self.tools:
                # Kiểm tra hợp lệ trước khi thực thi
                if not self._validate_tool_call(tool_name, tool_input):
                    context += f"\n\nStep {i+1}: Tool validation failed for '{tool_name}'. Try different approach."
                    continue
                
                result = self._execute_tool(tool_name, tool_input)
                
                # Kiểm tra hợp lệ sau khi thực thi
                if not self._validate_result(result):
                    self.metrics["errors"] += 1
                    context += f"\n\nStep {i+1}: Result validation failed. Retry with different parameters."
                    continue
                
                # Quan sát (Observe): thêm kết quả vào Context
                observation = f"Tool '{tool_name}' returned: {result}"
                context += f"\n\nStep {i+1}: {thought.get('reasoning', '')}"
                context += f"\n→ Used {tool_name}({tool_input})"
                context += f"\n→ Result: {result}"
                
                self.memory.append({
                    "step": i + 1,
                    "thought": thought,
                    "action": tool_name,
                    "result": result,
                })
                
                self.metrics["tools_used"][tool_name] = self.metrics["tools_used"].get(tool_name, 0) + 1
            else:
                context += f"\n\nStep {i+1}: Invalid tool '{tool_name}'. Try again."
            
            self.metrics["total_iterations"] = i + 1
        
        return {
            "answer": "Max iterations reached",
            "steps": self.memory,
            "iterations": self.max_iterations,
            "metrics": self.metrics,
        }
    
    def _think(self, context):
        """LLM decides next action"""
        prompt = f"""{context}

Based on the information above, decide your next action.

Output JSON:
{{
  "reasoning": "Why I'm doing this",
  "tool": "tool_name" or null if done,
  "input": {{"param": "value"}},
  "done": false,
  "answer": null
}}

If you have enough information to answer, set "done": true and provide "answer"."""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                import json
                return json.loads(response)
            except json.JSONDecodeError:
                pass
        
        return {"done": True, "answer": "No LLM available"}
    
    def _validate_tool_call(self, tool_name, tool_input):
        """Pre-execution validation (Harness guardrail)"""
        # Kiểm tra tool có tồn tại không
        if tool_name not in self.tools:
            return False
        
        # Kiểm tra các tham số bắt buộc
        tool = self.tools[tool_name]
        required = tool.get("required_params", [])
        for param in required:
            if param not in tool_input:
                return False
        
        return True
    
    def _validate_result(self, result):
        """Post-execution validation (Harness guardrail)"""
        if result is None:
            return False
        if isinstance(result, str) and result.startswith("Error:"):
            return False
        return True
    
    def _execute_tool(self, tool_name, tool_input):
        """Execute a tool"""
        tool = self.tools.get(tool_name)
        if tool and "function" in tool:
            try:
                return tool["function"](**tool_input)
            except Exception as e:
                return f"Error: {str(e)}"
        return f"Tool '{tool_name}' not found"


class MultiAgent:
    """
    Multi-agent system with specialized agents
    
    Based on Anthropic's multi-agent architecture pattern:
    - Planner Agent: Creates the plan
    - Generator Agent: Executes each step
    - Evaluator Agent: Validates results
    """
    
    def __init__(self, agents, coordinator_llm=None):
        self.agents = agents  # {tên: agent}
        self.coordinator = coordinator_llm
    
    def run(self, task):
        """Coordinate multiple agents"""
        plan = self._create_plan(task)
        
        results = {}
        for step in plan:
            agent_name = step["agent"]
            subtask = step["task"]
            
            if agent_name in self.agents:
                result = self.agents[agent_name].run(subtask)
                results[agent_name] = result
                
                # Kiểm tra xem kết quả có đạt yêu cầu không
                if not self._evaluate_result(result, subtask):
                    # Thử lại với phản hồi (feedback)
                    retry_result = self.agents[agent_name].run(
                        f"{subtask}\n\nLần trước thất bại vì: {result.get('answer', 'unknown error')}"
                    )
                    results[agent_name] = retry_result
        
        return self._synthesize(results, task)
    
    def _create_plan(self, task):
        """Decompose task across agents"""
        agent_names = list(self.agents.keys())
        
        if self.coordinator:
            prompt = f"""Assign subtasks to available agents.

Task: {task}
Available agents: {agent_names}

Output JSON:
{{"steps": [{{"agent": "...", "task": "...", "dependencies": []}}]}}"""
            
            response = self.coordinator(prompt)
            try:
                import json
                return json.loads(response).get("steps", [])
            except json.JSONDecodeError:
                pass
        
        return [{"agent": agent_names[0], "task": task}]
    
    def _evaluate_result(self, result, original_task):
        """Evaluate if result meets requirements"""
        if result.get("iterations", 0) >= 10:
            return False
        if not result.get("answer"):
            return False
        return True
    
    def _synthesize(self, results, original_task):
        """Combine results from all agents"""
        combined = "\n".join(
            f"Agent {name}: {r.get('answer', 'N/A')}"
            for name, r in results.items()
        )
        
        if self.coordinator:
            prompt = f"""Tổng hợp kết quả từ nhiều agents:

Task gốc: {original_task}

Kết quả:
{combined}

Tổng hợp:"""
            return self.coordinator(prompt)
        
        return combined
```

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

```python
class AgentState:
    """
    Manage state across agent execution steps
    
    Supports: state persistence, checkpointing, rollback, versioning
    """
    
    def __init__(self):
        self.state = {}
        self.history = []
        self.checkpoints = []
        self.version = 0
    
    def set(self, key, value):
        """Set state value with versioning"""
        old_value = self.state.get(key)
        self.state[key] = value
        self.version += 1
        
        self.history.append({
            "action": "set",
            "key": key,
            "old": old_value,
            "new": value,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get(self, key, default=None):
        """Get state value"""
        return self.state.get(key, default)
    
    def checkpoint(self):
        """Save current state snapshot"""
        self.checkpoints.append({
            "state": dict(self.state),
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
        })
        return len(self.checkpoints) - 1
    
    def rollback(self, checkpoint_id=None):
        """Rollback to checkpoint"""
        if checkpoint_id is None:
            checkpoint_id = len(self.checkpoints) - 1
        
        if 0 <= checkpoint_id < len(self.checkpoints):
            self.state = dict(self.checkpoints[checkpoint_id]["state"])
            self.version = self.checkpoints[checkpoint_id]["version"]
            return True
        return False
    
    def to_context(self):
        """Convert state to context string for LLM"""
        lines = [f"{k}: {v}" for k, v in self.state.items()]
        return "\n".join(lines)
    
    def diff(self, checkpoint_id):
        """Compare current state with checkpoint"""
        if 0 <= checkpoint_id < len(self.checkpoints):
            old = self.checkpoints[checkpoint_id]["state"]
            current = self.state
            
            changes = {
                "added": {k: v for k, v in current.items() if k not in old},
                "removed": {k: v for k, v in old.items() if k not in current},
                "modified": {k: (old.get(k), current.get(k)) 
                           for k in current if k in old and current[k] != old[k]},
            }
            return changes
        return {}
    
    def reset(self):
        """Clear all state"""
        self.state = {}
        self.version = 0
```

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

```python
class ReActAgent:
    """
    ReAct: Reasoning + Acting
    
    Thought → Action → Observation → Thought → ...
    
    Based on paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
    (Yao et al., 2022)
    
    Harness integration:
    - max_steps as guardrail
    - tool validation before execution
    - metrics tracking
    - error recovery
    """
    
    def __init__(self, tools, llm_func, max_steps=10):
        self.tools = tools
        self.llm = llm_func
        self.max_steps = max_steps
        self.trace = []
        self.token_usage = 0
    
    def run(self, query):
        """Execute ReAct loop"""
        prompt = f"""Solve this step by step using Thought/Action/Observation.

Question: {query}

Available actions:
{self._format_tools()}

Use this format:
Thought: [your reasoning about what to do next]
Action: [tool_name(input)]
Observation: [result of action]
... (repeat Thought/Action/Observation as needed)
Thought: [final reasoning]
Final Answer: [your answer]"""
        
        history = prompt
        
        for step in range(self.max_steps):
            response = self._llm_call(history)
            
            # Phân tích cú pháp phản hồi
            parsed = self._parse_response(response)
            
            if parsed.get("final_answer"):
                return {
                    "answer": parsed["final_answer"],
                    "steps": step + 1,
                    "trace": self.trace,
                    "token_usage": self.token_usage,
                }
            
            # Thực thi hành động
            if parsed.get("action"):
                tool_name, tool_input = self._parse_action(parsed["action"])
                
                # Kiểm tra hợp lệ lệnh gọi tool
                if not self._validate_tool(tool_name):
                    history += f"\n{response}"
                    history += f"\nObservation: Invalid tool '{tool_name}'. Use available tools only."
                    continue
                
                observation = self._execute_tool(tool_name, tool_input)
                
                self.trace.append({
                    "step": step + 1,
                    "thought": parsed.get("thought", ""),
                    "action": parsed["action"],
                    "observation": observation,
                })
                
                history += f"\n{response}"
                history += f"\nObservation: {observation}"
            else:
                history += f"\n{response}"
        
        return {
            "answer": "Max steps reached without final answer",
            "steps": self.max_steps,
            "trace": self.trace,
            "token_usage": self.token_usage,
        }
    
    def _format_tools(self):
        lines = []
        for name, tool in self.tools.items():
            params = tool.get("params", [])
            lines.append(f"- {name}({', '.join(params)})")
        return "\n".join(lines)
    
    def _parse_response(self, response):
        """Parse Thought/Action/Observation from response"""
        result = {}
        
        if "Final Answer:" in response:
            result["final_answer"] = response.split("Final Answer:")[-1].strip()
        
        if "Thought:" in response:
            thought_lines = [l for l in response.split('\n') if l.strip().startswith('Thought:')]
            if thought_lines:
                result["thought"] = thought_lines[-1].replace('Thought:', '').strip()
        
        if "Action:" in response:
            action_line = [l for l in response.split('\n') if l.strip().startswith('Action:')]
            if action_line:
                result["action"] = action_line[0].replace('Action:', '').strip()
        
        return result
    
    def _parse_action(self, action_str):
        """Parse tool_name(input) format"""
        import re
        match = re.match(r'(\w+)\((.+)\)', action_str)
        if match:
            return match.group(1), match.group(2)
        return action_str, ""
    
    def _validate_tool(self, tool_name):
        """Check if tool exists in available tools"""
        return tool_name in self.tools
    
    def _execute_tool(self, tool_name, tool_input):
        if tool_name in self.tools:
            try:
                func = self.tools[tool_name].get("function")
                if func:
                    return func(tool_input)
            except Exception as e:
                return f"Error: {e}"
        return f"Unknown tool: {tool_name}"
    
    def _llm_call(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "Thought: I don't know\nFinal Answer: N/A"
```

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

```typescript
// Planning System Interface — Tích hợp hoàn chỉnh với Harness
interface PlanningSystem {
  // Các năng lực lập kế hoạch cốt lõi
  decompose: (task: Task) => Promise<DecomposedPlan>;
  replan: (task: Task, failure: FailureInfo) => Promise<DecomposedPlan>;
  estimateComplexity: (task: Task) => ComplexityEstimate;
  
  // Quản lý trạng thái (State management)
  getState: () => AgentState;
  checkpoint: () => number;
  rollback: (checkpointId: number) => boolean;
  
  // Các điểm tích hợp
  tools: ToolRegistry;
  memory: MemorySystem;
  guardrails: GuardrailSystem;
  feedback: FeedbackSystem;
}

interface DecomposedPlan {
  rootTask: Task;
  subtasks: Task[];
  executionOrder: ExecutionStep[];
  estimatedTokens: number;
  estimatedTime: number;
  requiredTools: string[];
}

interface ExecutionStep {
  taskId: string;
  agentId: string;
  dependencies: string[];
  timeoutMs: number;
  tokenBudget: number;
  requiredPermissions: string[];
}

// Bộ lập kế hoạch tích hợp Harness hoàn chỉnh
class HarnessPlanner implements PlanningSystem {
  private tools: ToolRegistry;
  private memory: MemorySystem;
  private guardrails: GuardrailSystem;
  private feedback: FeedbackSystem;
  private state: AgentState;
  
  async decompose(task: Task): Promise<DecomposedPlan> {
    // 1. Kiểm tra tính hợp lệ của đầu vào
    const inputCheck = await this.guardrails.validateInput(task);
    if (!inputCheck.valid) {
      throw new Error(`Task validation failed: ${inputCheck.reason}`);
    }
    
    // 2. Kiểm tra Memory cho các tác vụ tương tự trong quá khứ
    const similarTasks = await this.memory.longTerm.search(
      `task: ${task.description}`,
      { limit: 3 }
    );
    
    // 3. Phân chia tác vụ với Context từ kinh nghiệm quá khứ
    const plan = await this.decomposeWithMemory(task, similarTasks);
    
    // 4. Kiểm tra kế hoạch đối chiếu với Guardrails
    const planValidation = await this.guardrails.validatePlan(plan);
    if (!planValidation.valid) {
      throw new Error(`Plan validation failed: ${planValidation.reason}`);
    }
    
    // 5. Ghi log phục vụ phản hồi
    await this.feedback.logPlan(task, plan);
    
    return plan;
  }
  
  async replan(task: Task, failure: FailureInfo): Promise<DecomposedPlan> {
    // Học hỏi từ thất bại
    await this.memory.longTerm.add(
      `Failed task: ${task.name}, Error: ${failure.error}`,
      { type: 'failure_pattern', task: task.name }
    );
    
    // Lập lại kế hoạch với Context thất bại
    const plan = await this.decompose(task);
    
    // Điều chỉnh dựa trên thất bại
    plan.executionOrder = plan.executionOrder.map(step => ({
      ...step,
      timeoutMs: step.timeoutMs * 1.5, // Tăng thời gian chờ (timeout)
      tokenBudget: step.tokenBudget * 1.2, // Tăng ngân sách Token
    }));
    
    return plan;
  }
  
  estimateComplexity(task: Task): ComplexityEstimate {
    const depth = this.getDepth(task);
    const breadth = this.getBreadth(task);
    
    return {
      score: Math.min(10, depth * 2 + breadth),
      depth,
      totalSubtasks: breadth,
      complexity: depth <= 1 ? 'simple' : depth <= 2 ? 'medium' : 'complex',
      recommendedApproach: breadth > 10 ? 'multi-agent' : 'single-agent',
    };
  }
  
  getState(): AgentState { return this.state; }
  checkpoint(): number { return this.state.checkpoint(); }
  rollback(id: number): boolean { return this.state.rollback(id); }
  
  private async decomposeWithMemory(task: Task, memories: any[]): Promise<DecomposedPlan> {
    // Triển khai sử dụng Memory của các tác vụ quá khứ
    // để nâng cao chất lượng phân chia tác vụ
    return { /* ... */ } as DecomposedPlan;
  }
  
  private getDepth(task: Task): number { /* ... */ return 0; }
  private getBreadth(task: Task): number { /* ... */ return 0; }
}
```

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

```typescript
// Lập kế hoạch Harness cho SWE-agent
const swePlanner = {
  async plan(issue: string, codebase: CodebaseInfo) {
    // 1. Phân tích issue
    const analysis = await analyzeIssue(issue);
    
    // 2. Tìm files liên quan (KHÔNG đọc toàn bộ)
    const relevantFiles = await findRelevantFiles(analysis, codebase);
    
    // 3. Lập kế hoạch thực thi
    return {
      steps: [
        { action: "read_file", path: relevantFiles[0], reason: "understand context" },
        { action: "search_code", pattern: analysis.functionName, reason: "find implementation" },
        { action: "edit_file", path: relevantFiles[0], changes: analysis.suggestedFix },
        { action: "run_tests", suite: "relevant", reason: "verify fix" },
      ],
      estimatedTokens: 15000,
      maxRetries: 2,
    };
  }
};
```

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

```typescript
// Bộ lập kế hoạch → Bộ tạo → Bộ đánh giá (Planner → Generator → Evaluator)
class AnthropicPlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  async plan(task: string): Promise<Plan> {
    // 1. Phân tích độ phức tạp của tác vụ
    const complexity = await this.estimateComplexity(task);
    
    // 2. Tạo kế hoạch theo từng bước
    const steps = await this.generateSteps(task, complexity);
    
    // 3. Thêm đồ thị phụ thuộc (dependency graph)
    const graphedSteps = this.addDependencies(steps);
    
    return {
      steps: graphedSteps,
      estimatedComplexity: complexity,
      parallelizableGroups: this.findParallelGroups(graphedSteps),
    };
  }
  
  private findParallelGroups(steps: Step[]): Step[][] {
    // Tìm các bước có thể chạy song song (không có phụ thuộc lẫn nhau)
    const groups: Step[][] = [];
    const remaining = [...steps];
    
    while (remaining.length > 0) {
      const group = remaining.filter(s => 
        s.dependencies.every(dep => 
          groups.some(g => g.some(gs => gs.id === dep))
        )
      );
      groups.push(group);
      remaining.splice(0, group.length);
    }
    
    return groups;
  }
}
```

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

```typescript
// Hierarchical Planning — 3 cấp độ
class ClaudePlanningSystem {
  // Cấp độ 1: Lập kế hoạch chiến lược (Strategic Planning - cấp độ tác vụ)
  async strategicPlan(goal: string): Promise<StrategicPlan> {
    return {
      approach: await this.selectApproach(goal),
      phases: await this.definePhases(goal),
      estimatedTime: await this.estimateTime(goal),
      checkpoints: await this.defineCheckpoints(goal),
    };
  }
  
  // Cấp độ 2: Lập kế hoạch chiến thuật (Tactical Planning - cấp độ giai đoạn)
  async tacticalPlan(phase: Phase): Promise<TacticalPlan> {
    return {
      steps: await this.breakDownPhase(phase),
      tools: await this.selectTools(phase),
      parallelizable: await this.findParallelSteps(phase),
      rollbackPoints: await this.identifyRollbackPoints(phase),
    };
  }
  
  // Cấp độ 3: Lập kế hoạch vận hành (Operational Planning - cấp độ bước)
  async operationalPlan(step: Step): Promise<OperationalPlan> {
    return {
      action: await this.defineAction(step),
      parameters: await this.extractParameters(step),
      validation: await this.defineValidation(step),
      errorHandling: await this.defineErrorHandling(step),
    };
  }
}
```

</details>

**Tính năng cốt lõi — Dynamic Re-planning**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// Claude Code tự động re-plan khi gặp vấn đề
class DynamicReplanner {
  async handleFailure(
    failedStep: Step, 
    error: Error, 
    currentPlan: Plan
  ): Promise<Plan> {
    // 1. Phân tích lỗi
    const analysis = await this.analyzeFailure(failedStep, error);
    
    // 2. Thử sửa lỗi trong phạm vi kế hoạch hiện tại
    if (analysis.canFixInPlace) {
      return this.adjustStep(failedStep, analysis.fix);
    }
    
    // 3. Lập lại kế hoạch từ điểm này
    const remainingSteps = currentPlan.steps.filter(
      s => !s.dependencies.includes(failedStep.id)
    );
    
    return this.replan(remainingSteps, analysis.context);
  }
}
```

</details>

---

### 7.4. Cursor IDE — Context-Aware Planning

Bối cảnh: Cursor phải lên kế hoạch sửa code **nương theo đúng chỗ bạn đang làm** — file nào đang mở, bôi đen đoạn nào, con trỏ đang đặt ở dòng mấy, vừa sửa gì gần đây. Đoạn code bên dưới cho thấy nó gom ngữ cảnh ra sao, vẽ kế hoạch thay đổi thế nào, rồi tự thu hẹp phạm vi để khỏi đụng lung tung sang mấy file chẳng liên quan.

<details>
<summary><b>7.4. Cursor IDE — Context-Aware Planning (Click to expand/collapse)</b></summary>

```typescript
class CursorPlanner {
  async plan(codeChange: string): Promise<Plan> {
    // 1. Thấu hiểu Context hiện tại
    const context = {
      currentFile: editor.getCurrentFile(),
      selectedCode: editor.getSelection(),
      cursorLine: editor.getCursorLine(),
      recentEdits: this.getRecentEdits(5),
      relatedFiles: await this.findRelatedFiles(),
      gitContext: await git.getContext(),
    };
    
    // 2. Lập kế hoạch thay đổi
    const plan = await this.planChanges(codeChange, context);
    
    // 3. Tối thiểu hóa phạm vi (không thay đổi các file không liên quan)
    const scopedPlan = this.minimizeScope(plan, context.currentFile);
    
    return scopedPlan;
  }
  
  private minimizeScope(plan: Plan, currentFile: string): Plan {
    return {
      ...plan,
      steps: plan.steps.filter(step => 
        this.isRelated(step.file, currentFile) || step.essential
      ),
    };
  }
}
```

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

```typescript
class TokenBudgetManager {
  private totalBudget: number;
  private allocated: Map<string, number>;
  private used: Map<string, number>;
  
  constructor(totalBudget: number = 100000) {
    this.totalBudget = totalBudget;
    this.allocated = new Map();
    this.used = new Map();
  }
  
  allocate(taskId: string, budget: number): boolean {
    const totalAllocated = Array.from(this.allocated.values()).reduce((a, b) => a + b, 0);
    
    if (totalAllocated + budget > this.totalBudget) {
      return false; // Không đủ ngân sách Token
    }
    
    this.allocated.set(taskId, budget);
    return true;
  }
  
  report(taskId: string, tokens: number): void {
    this.used.set(taskId, (this.used.get(taskId) || 0) + tokens);
  }
  
  canContinue(taskId: string): boolean {
    const allocated = this.allocated.get(taskId) || 0;
    const used = this.used.get(taskId) || 0;
    return used < allocated * 0.9; // Cho phép sử dụng tối đa 90%
  }
  
  getRemaining(): number {
    const totalUsed = Array.from(this.used.values()).reduce((a, b) => a + b, 0);
    return this.totalBudget - totalUsed;
  }
  
  getReport(): TokenReport {
    return {
      totalBudget: this.totalBudget,
      allocated: Object.fromEntries(this.allocated),
      used: Object.fromEntries(this.used),
      remaining: this.getRemaining(),
      efficiency: Array.from(this.used.values()).reduce((a, b) => a + b, 0) / 
                  Array.from(this.allocated.values()).reduce((a, b) => a + b, 1),
    };
  }
}
```

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

```python
import unittest

class TestTaskPlanner(unittest.TestCase):
    def setUp(self):
        self.planner = TaskPlanner()
    
    def test_simple_decomposition(self):
        """Simple task → 1-3 subtasks"""
        task = Task(id="t1", name="Fix typo", description="Fix typo in README")
        plan = self.planner.decompose("Fix typo in README")
        self.assertLessEqual(len(plan), 3)
    
    def test_complex_decomposition(self):
        """Complex task → multiple subtasks"""
        plan = self.planner.decompose(
            "Build a complete RAG system with vector search, "
            "chunking, embedding, and query processing"
        )
        self.assertGreater(len(plan), 3)
    
    def test_complexity_estimation(self):
        """Estimate complexity correctly"""
        task = Task(id="t1", name="Simple", description="Simple task")
        estimate = self.planner.estimate_complexity(task)
        self.assertIn(estimate["complexity"], ["simple", "medium", "complex"])
    
    def test_dependency_detection(self):
        """Verify dependency-based execution order"""
        t1 = Task(id="t1", name="Setup DB", dependencies=[])
        t2 = Task(id="t2", name="Create schema", dependencies=["t1"])
        t3 = Task(id="t3", name="Insert data", dependencies=["t2"])
        
        completed = set()
        # t1 phải có thể thực thi trước
        self.assertTrue(t1.can_execute(completed))
        
        # t2 CHƯA ĐƯỢC thực thi
        self.assertFalse(t2.can_execute(completed))
        
        # Sau khi t1 hoàn thành
        completed.add("t1")
        self.assertTrue(t2.can_execute(completed))
    
    def test_max_depth_limit(self):
        """Verify decomposition respects max depth"""
        plan = self.planner.decompose(
            "Build: a → b → c → d → e → f",
            max_depth=2
        )
        depth = self.planner._get_depth(
            Task(id="root", subtasks=plan)
        )
        self.assertLessEqual(depth, 2)
    
    def test_retry_logic(self):
        """Test task retry on failure"""
        task = Task(id="t1", name="Flaky task", max_retries=3)
        
        # Thất bại lần đầu
        task.mark_failed("timeout")
        self.assertTrue(task.can_retry())
        
        # Sau 3 lần thử lại (retries)
        task.retry_count = 3
        self.assertFalse(task.can_retry())

class TestTokenBudget(unittest.TestCase):
    def setUp(self):
        self.budget_manager = TokenBudgetManager(totalBudget=50000)
    
    def test_allocation_within_budget(self):
        """Allocate within budget"""
        result = self.budget_manager.allocate("task1", 20000)
        self.assertTrue(result)
    
    def test_allocation_exceeds_budget(self):
        """Allocation exceeds budget"""
        self.budget_manager.allocate("task1", 30000)
        result = self.budget_manager.allocate("task2", 25000)
        self.assertFalse(result)
    
    def test_usage_tracking(self):
        """Track token usage per task"""
        self.budget_manager.allocate("task1", 10000)
        self.budget_manager.report("task1", 5000)
        
        self.assertTrue(self.budget_manager.canContinue("task1"))
        
        self.budget_manager.report("task1", 4500)
        self.assertFalse(self.budget_manager.canContinue("task1"))

class TestAgentState(unittest.TestCase):
    def setUp(self):
        self.state = AgentState()
    
    def test_set_and_get(self):
        self.state.set("key1", "value1")
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_checkpoint_and_rollback(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.assertEqual(self.state.get("key1"), "value2")
        
        self.state.rollback(cp)
        self.assertEqual(self.state.get("key1"), "value1")
    
    def test_diff(self):
        self.state.set("key1", "value1")
        cp = self.state.checkpoint()
        self.state.set("key1", "value2")
        self.state.set("key2", "value3")
        
        changes = self.state.diff(cp)
        self.assertIn("key2", changes["added"])
        self.assertIn("key1", changes["modified"])

if __name__ == "__main__":
    unittest.main()
```

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

```python
class HTNPlanner:
    """
    Hierarchical Task Network planning
    
    Unlike simple decomposition, HTN uses:
    - Primitive tasks (can be executed directly)
    - Compound tasks (need further decomposition)
    - Methods (ways to decompose compound tasks)
    """
    
    def __init__(self):
        self.methods = {}  # task_type -> danh sách phương pháp phân chia tác vụ
        self.primitive_actions = {}  # action_name -> phần triển khai
    
    def add_method(self, task_type, method):
        if task_type not in self.methods:
            self.methods[task_type] = []
        self.methods[task_type].append(method)
    
    def decompose(self, task, depth=0, max_depth=5):
        if depth >= max_depth:
            return [task]
        
        if task["type"] in self.methods:
            for method in self.methods[task["type"]]:
                if method["precondition"](task):
                    subtasks = method["decompose"](task)
                    result = []
                    for subtask in subtasks:
                        result.extend(self.decompose(subtask, depth + 1, max_depth))
                    return result
        
        return [task]  # Tác vụ nguyên thủy (primitive task)
    
    def execute_plan(self, plan):
        results = []
        for task in plan:
            if task["name"] in self.primitive_actions:
                result = self.primitive_actions[task["name"]](task)
                results.append({"task": task, "result": result})
        return results
```

</details>

### 11.2 Self-Reflective Planning

Chiêu này là: agent vẽ kế hoạch xong thì **tự làm giám khảo chấm bài của mình** (đủ chưa, làm nổi không, rủi ro chỗ nào); điểm thấp thì tự sửa theo góp ý của chính mình rồi chấm lại vài vòng. Class `SelfReflectivePlanner` bên dưới code đúng vòng Plan → Reflect → Improve đó, lại còn lưu sổ lịch sử để học từ kết quả thật.

> Như hồi đi học viết nháp văn: viết xong đọc lại, thấy đoạn nào sượng thì sửa, ổn rồi mới nộp bản sạch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class SelfReflectivePlanner:
    """
    Planner that improves by reflecting on its own plans
    
    Pattern: Plan → Execute → Reflect → Improve Plan
    """
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
        self.plan_history = []  # Lịch sử kế hoạch và kết quả
    
    def plan_with_reflection(self, task, max_reflections=3):
        """Plan with self-reflection"""
        plan = self._initial_plan(task)
        
        for reflection_round in range(max_reflections):
            # Tự ngẫm (Reflect) về chất lượng kế hoạch
            reflection = self._reflect_on_plan(task, plan)
            
            if reflection["quality_score"] >= 8:
                break  # Dừng lại nếu kế hoạch đã đủ tốt
            
            # Cải thiện kế hoạch dựa trên tự ngẫm
            plan = self._improve_plan(plan, reflection["suggestions"])
        
        return plan
    
    def _initial_plan(self, task):
        return {
            "steps": [],
            "estimated_complexity": 0,
            "risks": [],
        }
    
    def _reflect_on_plan(self, task, plan):
        if self.llm:
            prompt = f"""Phân tích kế hoạch sau:

Task: {task}
Plan: {plan}

Đánh giá:
1. Tính đầy đủ (1-10)
2. Tính khả thi (1-10)
3. Rủi ro (list)
4. Cải tiến (suggestions)"""
            
            response = self.llm(prompt)
            return {"quality_score": 7, "suggestions": [], "risks": []}
        
        return {"quality_score": 5, "suggestions": ["Add more detail"], "risks": []}
    
    def _improve_plan(self, plan, suggestions):
        plan["improvements"] = suggestions
        return plan
    
    def learn_from_outcome(self, task, plan, outcome):
        """Store plan outcome for future learning"""
        self.plan_history.append({
            "task": task,
            "plan": plan,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat(),
        })
```

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

```python
from langgraph.graph import StateGraph, END

# Định nghĩa State Machine lập kế hoạch
def create_planning_graph():
    graph = StateGraph(dict)
    
    # Thêm các Node
    graph.add_node("analyze", analyze_task)
    graph.add_node("plan", create_plan)
    graph.add_node("validate", validate_plan)
    graph.add_node("execute", execute_step)
    graph.add_node("replan", replan_on_failure)
    
    # Thêm các Edge
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "validate")
    graph.add_conditional_edges("validate", decide_next, {
        "pass": "execute",
        "fail": "replan",
        "done": END,
    })
    graph.add_edge("execute", "validate")
    graph.add_edge("replan", "validate")
    
    return graph.compile()
```

</details>

### 12.2 CrewAI (Multi-Agent Planning)

CrewAI xếp các agent thành hẳn một **đội (crew)**: bạn cắt vai cho từng người (Agent) kèm mục tiêu và đồ nghề riêng, phát task cho từng vai, rồi để cả đội phối hợp "đá" cho xong. Đoạn code dựng ba vai quen thuộc: Planner (ông vẽ đường), Executor (ông xắn tay làm) và Reviewer (ông soi lỗi).

> Như mở công ty mini ba phòng ban, mỗi phòng một sứ mệnh, hợp sức làm xong một dự án.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from crewai import Agent, Task, Crew

# Tạo các Agent lập kế hoạch chuyên biệt
planner = Agent(
    role="Task Planner",
    goal="Break down complex tasks into actionable steps",
    backstory="Expert at task decomposition and dependency analysis",
    tools=[analysis_tool, research_tool],
)

executor = Agent(
    role="Task Executor", 
    goal="Execute planned tasks efficiently",
    backstory="Expert at implementation and testing",
    tools=[code_tool, test_tool],
)

reviewer = Agent(
    role="Plan Reviewer",
    goal="Review and validate task plans",
    backstory="Expert at quality assurance and risk assessment",
)

# Tạo các tác vụ (tasks)
planning_task = Task(
    description="Create execution plan for: {task}",
    agent=planner,
)

execution_task = Task(
    description="Execute the plan created by planner",
    agent=executor,
)

# Tập hợp Crew
crew = Crew(
    agents=[planner, executor, reviewer],
    tasks=[planning_task, execution_task],
    verbose=True,
)
```

</details>

### 12.3 AutoGen (Microsoft)

AutoGen của Microsoft cho các agent **ngồi "chat" với nhau** để phối hợp — mỗi agent là một cái đầu biết nhắn tin qua lại. Code mẫu dựng ba nhân vật: planner chuyên bày kế hoạch, executor chuyên xắn tay làm, và user proxy đóng vai người thật ngồi duyệt kết quả cuối.

> Như nhóm chat công việc: một người đề xuất, một người làm, một người chốt "ok" trước khi nộp.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from autogen import AssistantAgent, UserProxyAgent

planner = AssistantAgent(
    name="planner",
    llm_config={"model": "gpt-4"},
    system_message="""You are a planning specialist.
    Break down tasks into clear steps with dependencies.
    Always output JSON format."""
)

executor = AssistantAgent(
    name="executor",
    llm_config={"model": "gpt-4"},
    system_message="""You execute tasks based on the plan.
    Report completion status for each step."""
)

user = UserProxyAgent(
    name="user",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
)
```

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

```python
import hashlib
MAX_RETRY, MAX_REPLAN = 3, 2
MAX_DEPTH, MAX_FANOUT, MAX_TOKENS = 4, 5, 100_000

def idem_key(plan: str, sub: str, inputs: dict) -> str:
    h = hashlib.sha1(repr(sorted(inputs.items())).encode()).hexdigest()[:12]
    return f"{plan}:{sub}:{h}"

store: dict = {}
def run_subtask(plan: str, sub: str, inputs: dict, fn, *, risk="low"):
    k = idem_key(plan, sub, inputs)
    if k in store: return store[k]  # replay idempotent
    if risk in ("high", "irreversible") and not approved(plan, sub, inputs):
        return {"status": "blocked", "reason": "approval-denied"}
    try:
        out = fn(inputs); store[k] = {"status": "ok", "out": out}
    except Exception as e:
        store[k] = {"status": "failed", "err": str(e), "transient": is_transient(e)}
    return store[k]

def decide(state: dict) -> str:  # retry | replan | escalate | done
    if state.get("risk_gate"): return "escalate"
    if state.get("tokens", 0) > MAX_TOKENS * 0.8: return "escalate"
    if state.get("replans", 0) >= MAX_REPLAN: return "escalate"
    if state.get("transient") and state.get("attempts", 0) < MAX_RETRY: return "retry"
    if state.get("status") == "failed": return "replan"
    return "done"

def approved(plan, sub, inputs) -> bool:
    print(f"[GATE] approve {plan}/{sub} {inputs} ? (y/n, timeout -> deny)")
    return input().strip().lower() == "y"

def is_transient(e: Exception) -> bool:
    return any(s in str(e).lower() for s in ("timeout", "429", "econnreset"))
```

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