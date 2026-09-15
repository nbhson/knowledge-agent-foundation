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

Hãy tưởng tượng bạn nhờ một người thợ xây dựng **căn nhà 3 tầng**. Anh ta chẳng vẽ bản vẽ, chẳng chia giai đoạn, cứ thế bắt tay vào — đập nền, xây tường, lắp cửa... cùng lúc. Kết quả? Tường lệch, cửa hỏng, phải đập bỏ làm lại.

**Đó chính xác là vấn đề của AI Agent khi không có Planning & Decomposition.**

LLM rất giỏi "nói" — nhưng khi đối mặt task phức tạp như *"triển khai hệ thống BHYT cho công ty 100 người"*, chúng thường mắc **lỗi Oversimplification** (nhảy thẳng vào code mà không plan) hoặc **Analysis Paralysis** (phân tích quá nhiều mà không bao giờ bắt tay). Cả hai đều dẫn đến kết quả tồi.

**Giải pháp**: Structured Planning — cho agent **nghĩ trước khi làm**, nhưng vẫn **bắt tay vào làm trong thời gian hợp lý**.

### Tại Sao Plan & Decompose Task Quan Trọng?

> *"Một mục tiêu không có kế hoạch chỉ là một mong ước. Và một AI không có khả năng phân chia tác vụ (decomposition) chỉ là một chatbot."*

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

**Analogies**: Plan & Decompose giống GPS navigation — không chỉ cho biết đích đến (goal), mà còn phân tích đường đi (decompose), chọn tuyến tối ưu (prioritize), tính thời gian (estimate), và reroute khi có traffic (replan). Without GPS, bạn có thể lái xe cả ngày mà không đến nơi.

**Nếu bỏ qua**: Agent cố gắng làm mọi thứ cùng lúc → context overload, hallucinate khi không có cấu trúc rõ ràng, tạo code không nhất quán, và cuối cùng tốn gấp 3-5 lần token so với planned approach.

## Tổng Quan

> 📌 **Khái Niệm Cơ Bản**
>
> **Khái niệm:** Tổng Quan là bức tranh bao quát về Planning & Decomposition — quá trình biến một công việc lớn, mơ hồ thành chuỗi các bước nhỏ, rõ ràng và thực thi được, giống như chia một con voi lớn thành nhiều miếng nhỏ dễ nuốt.
>
> **Ẩn dụ/so sánh:** Giống đầu bếp trước một bữa tiệc lớn: thay vì nấu "một món khổng lồ", anh ta chia thành nhiều món nhỏ, mỗi món một khâu, rồi mới bắt tay vào bếp.
>
> **Vì sao quan trọng:** Vì không có kế hoạch, AI dễ nhảy lung tung, làm sai thứ tự hoặc bỏ sót bước — phần này giúp bạn hiểu khung tổng thể trước khi đi vào chi tiết.

Khi đối mặt task phức tạp, AI Agent cần **phân tích → lập kế hoạch → chia nhỏ → thực hiện tuần tự**. Đây là kỹ năng cốt lõi biến LLM từ "chatbot" thành "agent".

Trong hệ thống Harness Engineering, Planning & Decomposition là **"bộ não điều khiển"** — quyết định tất cả các thành phần khác (tools, memory, guardrails) được sử dụng như thế nào.

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

> *"Một agent không có planning giống như một người lái xe không có bản đồ — có thể di chuyển, nhưng chắc chắn sẽ lạc đường."*

### Triết Lý Cốt Lõi

LLMs có khả năng "nói" rất giỏi, nhưng khi đối mặt task phức tạp như **"triển khai hệ thống BHYT cho công ty 100 người"**, chúng thường mắc một trong hai lỗi phổ biến:

**Lỗi 1: Oversimplification** — Agent nhảy thẳng vào code mà không plan → Implement sai requirements → Phải làm lại từ đầu.

**Lỗi 2: Analysis Paralysis** — Agent phân tích quá nhiều mà không bao giờ bắt tay vào làm → User chờ đợi vô tận.

**Giải pháp**: Structured Planning — một hệ thống có framework rõ ràng cho phép agent **nghĩ trước khi làm**, nhưng vẫn **bắt tay vào làm trong thời gian hợp lý**.

### Bằng Chứng Nghiên Cûu

#### LangChain (2025): "ReAct vs Plan-and-Execute"
> Agents sử dụng **Plan-and-Execute pattern** hoàn thành tasks phức tạp với **40% ít hơn retries** so với ReAct (reactive) pattern.

Nguyên nhân: Plan trước → biết cần tool nào → giảm false starts → ít hơn một nửa số tool calls không cần thiết.

#### Microsoft Research (2024): "Task Decomposition in LLM Agents"
> Khi task được chia thành sub-tasks có kích thước **3-7 items** mỗi nhóm, accuracy tăng **52%** so với monolithic task.

**Quy tắc 7±2**: Tương tự Miller's Law trong tâm lý học — con người (và cả LLM) xử lý hiệu quả nhất khi có 5-9 items trong working memory.

#### Devin AI & OpenHands (2025)
> Top coding agents đều sử dụng **hierarchical decomposition**: Task → Epic → Story → Sub-task. Tốc độ hoàn thành **2.8x** so với flat task list.

### Phân Tích Chi Phí & Lợi Ích (Cost-Benefit Analysis)

| Chi Phí / Giá Trị | Không Có Planning | Có Planning + Decomposition |
|---|---|---|
| **Retry Rate** | 40-60% tasks cần retry | 10-15% tasks cần retry |
| **Tool Calls** | 3-5x redundant calls | Gần như minimal calls |
| **Token Usage** | Cao (phải re-process context) | Thấp hơn 30-50% |
| **Time to Complete** | Unpredictable, thường chậm | Predictable, typically faster |
| **User Trust** | Thấp vì kết quả bất ngờ | Cao vì có visibility vào plan |

**ROI**: Đầu tư 15-30 giây ban đầu cho planning → Tiết kiệm 5-15 phút retry. Tỷ lệ **1:20**.

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

**1. Infinite Loop (Vòng Lặp Vô Tận)**
- Agent thực hiện task A → B → A → B → ... không bao giờ hoàn thành
- Thiếu termination conditions rõ ràng trong plan

**2. Scope Creep (Mở Rộng Phạm Vi)**
- Agent thêm tính năng không cần thiết → Token waste, time waste
- Ví dụ: "Viết hello world" → Agent thêm authentication, logging, i18n...

**3. Chọn Sai Tool (Wrong Tool Selection)**
- Không plan trước → Chọn sai tool cho mỗi step → Phải undo và làm lại
- Ví dụ: Dùng search khi cần write, dùng write khi cần verify

**4. Bỏ Sót Bước (Missing Steps)**
- Agent quên steps quan trọng → Kết quả incomplete
- Ví dụ: Deploy code mà không test, không lint, không commit

**5. Lỗi Dây Chuyền (Cascading Errors)**
- Sub-task 1 sai → Sub-task 2-5 đều sai theo → Phải làm lại toàn bộ
- Thiếu validation checkpoints giữa các sub-tasks

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

Mục này chỉ ra **các cách khác nhau để cắt một task thành nhiều phần**: làm tuần tự, làm song song, rẽ nhánh theo điều kiện, phân cấp cha-con, lặp lại, hoặc kết hợp theo đồ thị. Mỗi pattern là một "kiểu bố trí" luồng chạy khác nhau — nhìn vào các ô ASCII bên dưới để hiểu hình dạng của từng kiểu rồi mới chọn cái phù hợp với bài toán.

> Giống cách sếp phân việc cho đội: chia người làm tuần tự, chia nhiều người làm cùng lúc (song song), hoặc giao có điều kiện "nếu xong A thì mới làm B".

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

Code bên dưới là bộ cài đặt Python hoàn chỉnh cho các pattern ở mục 1.1: lớp `Task` định nghĩa "một mảnh công việc" (loại, trạng thái, dependency, retry...), còn lớp `TaskPlanner` là "bộ não chia việc" dùng LLM để phân tích task lớn thành subtask, phát hiện dependency và ước tính độ phức tạp. Bạn có thể bấm mở để đọc theo thứ tự: khai báo `Task` trước, rồi đến phương thức `decompose()` và `estimate_complexity()`.

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

Bảng dưới là "bảng tổng hợp điểm" so sánh 6 pattern theo 4 tiêu chí: tốc độ (Speed), chất lượng (Quality), chi phí token (Token Cost) và trường hợp dùng tốt nhất (Best For). Đọc theo hàng để chọn: cần nhanh → Sequential/Parallel; cần chất lượng cao, chấp nhận chậm → Hierarchical/Iterative.

> Giống bảng so sánh điện thoại khi đi mua: nhìn một bảng là thấy ngay loại nào hợp với nhu cầu của mình, không cần thử từng cái.

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

Cách tiếp cận này giống hệt việc bạn lên "to-do list" trước khi bắt tay làm: AI viết ra các bước chi tiết trước, thực hiện từng bước, kiểm tra lại kết quả, và nếu bước nào thất bại thì **lập kế hoạch mới** (re-plan) thay vì thử lại y nguyên. Code bên dưới mô phỏng đúng vòng đời đó qua các phương thức `plan()` → `solve_step()` → `verify()` → `replan()`.

> Giống nấu ăn theo công thức: ghi sẵn các bước → làm từng bước → nếm thử (verify) → nếu mặn quá thì điều chỉnh công thức thay vì nấu lại y hệt từ đầu.

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

Thay vì suy luận theo một đường thẳng như Plan-and-Solve, ToT **rẽ nhiều nhánh suy nghĩ cùng lúc**, chấm điểm từng nhánh, rồi tập trung đào sâu nhánh nào hứa hẹn nhất. Code bên dưới dùng BFS (duyệt theo từng tầng) kèm cắt tỉa (pruning) để tránh số nhánh bùng nổ: mỗi tầng chỉ giữ lại top-k nhánh tốt nhất.

> Giống bác sĩ đề xuất 3 phác đồ điều trị, chấm điểm từng phác đồ theo rủi ro và triển vọng, rồi chọn phác đồ tốt nhất để theo đuổi.

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

Ý tưởng chính là **tách việc suy nghĩ và việc chạy tool thành hai giai đoạn riêng**: AI lập toàn bộ kế hoạch ngay từ đầu (bước nào dùng tool gì, query gì), chạy hết một lượt, rồi mới dùng kết quả để tổng hợp câu trả lời. Ưu điểm là gọi LLM ít lần hơn nên rẻ hơn; nhược điểm là kém thích ứng khi một bước thất bại giữa chừng. Code trong `ReWOOPlanner` minh họa đúng chu trình plan-all → execute → synthesize.

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

Đây là bản đồ mô tả **6 kiểu tổ chức agent phổ biến nhất**, từ đơn giản đến phức tạp: ReAct (suy nghĩ – hành động xen kẽ), Plan-and-Execute (lập kế hoạch trước rồi chạy), Reflective (làm rồi rút kinh nghiệm), Multi-Agent (nhiều vai cùng phối hợp), LangGraph-style (máy trạng thái với các node rẽ nhánh), và Hierarchical (cấp trên giao việc cho cấp dưới). Nhìn vào các ô ASCII để thấy luồng gọi giữa các thành phần — đây là hình ảnh trực quan nhất của cả module.

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

Code dưới đây hiện thực hóa 2 kiểu workflow nói trên: lớp `SimpleAgent` là agent đơn lẻ chạy vòng lặp Think → Act → Observe kèm guardrail (validate tool trước và sau khi gọi), còn lớp `MultiAgent` là hệ nhiều agent chuyên biệt được điều phối bởi một coordinator — chia việc, nhận kết quả, đánh giá, rồi tổng hợp. Bấm mở để xem từng phương thức theo thứ tự tương ứng.

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
> **Ẩn dụ/so sánh:** Giống trò chơi điện tử có điểm lưu (save point): trước trận boss bạn lưu game, chết thì load lại điểm đó thay vì chơi lại từ đầu.
>
> **Vì sao quan trọng:** Vì agent chạy lâu hoặc gặp lỗi giữa chừng rất dễ mất sạch tiến trình — có state management thì tiếp tục ngay được, không phải làm lại từ con số 0.

Code dưới đây là lớp `AgentState` — bộ quản lý trạng thái hoàn chỉnh: lưu giá trị kèm lịch sử phiên bản (`history`), chụp ảnh trạng thái (`checkpoint`), quay lại mốc cũ (`rollback`), và xuất ra chuỗi context để đưa cho LLM (`to_context`). Bấm mở để đọc từng phương thức theo tên mô tả.

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
> **Khái niệm:** ReAct (Reasoning + Acting) là vòng lặp "suy nghĩ → hành động → nhìn lại kết quả" lặp đi lặp lại: AI tự độc thoại về bước tiếp theo (Thought), gọi công cụ (Action), rồi đọc kết quả phản hồi (Observation) trước khi quyết định bước sau.
>
> **Ẩn dụ/so sánh:** Giống người nấu ăn nếm thử từng lần: nêm → nếm → điều chỉnh, cứ lặp cho đến khi vừa miệng — không làm một phát rồi xong luôn.
>
> **Vì sao quan trọng:** Vì môi trường thực tế hay thay đổi, agent cần đọc lại kết quả thật để tự hiệu chỉnh thay vì bám cứng vào kế hoạch cũ (static planning).

Code bên dưới là lớp `ReActAgent` — bản cài đặt nguyên mẫu của vòng lặp Thought → Action → Observation kèm guardrail `max_steps`, validate tool trước khi gọi và đếm token. Bấm mở để xem cách parse phản hồi của LLM và cách luân chuyển giữa các bước cho tới khi đạt "Final Answer".

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
> **Khái niệm:** Harness-Integrated Planning là cách "cắm" bộ lập kế hoạch vào khung nền (Harness) của hệ thống: đến đây bộ planner không hoạt động đơn độc mà được giám sát bởi Guardrails, trợ giúp bởi Memory và hưởng lợi từ vòng phản hồi (Feedback).
>
> **Ẩn dụ/so sánh:** Giống dự án xây nhà có ban giám sát: thợ (planner) vẫn chia giai đoạn và thi công, nhưng mọi bản vẽ phải qua kiểm duyệt (guardrails), có kho hồ sơ cũ để tham khảo (memory), và có biên bản nghiệm thu mỗi giai đoạn (feedback).
>
> **Vì sao quan trọng:** Vì một kế hoạch tự do, không ai kiểm soát dễ vượt quyền hạn hoặc lặp lại sai lầm cũ — tích hợp vào Harness giúp kế hoạch an toàn và tự thích nghi hơn.


### 6.1 TypeScript Interface (Harness Architecture)

Mục này mô tả **giao diện (interface) khai báo cấu trúc Harness**: liệt kê các năng lực mà một Planning System phải có (decompose, replan, estimateComplexity...) và cách nó kết nối với tools, memory, guardrails, feedback. Trong TypeScript, `interface` giống "bản hợp đồng" — dòng nào khai báo trong interface là bạn cam kết lớp triển khai phải có năng lực đó. Phần `HarnessPlanner` bên dưới là ví dụ triển khai thực sự theo đúng hợp đồng này.

> Giống danh sách hạng mục trong hợp đồng giao khoán: ai nhận thầu bắt buộc phải có đủ các hạng mục được liệt kê, không được thiếu sót.

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
> **Khái niệm:** Case Studies là những "ca điển hình" phân tích thật về cách 4 sản phẩm AI nổi tiếng (SWE-agent, Anthropic Multi-Agent, Claude Code, Cursor) xây dựng hệ thống lập kế hoạch trong sản xuất thực tế.
>
> **Ẩn dụ/so sánh:** Giống xem "bài văn mẫu điểm 10" của học sinh giỏi: bạn học được cách họ trình bày, đặt câu hỏi và sửa lỗi — rồi áp dụng lại cho bài của mình.
>
> **Vì sao quan trọng:** Vì lý thuyết sách vở dễ xa rời thực tế — xem sản phẩm đang chạy tốt giúp bạn rút ra các mẫu thiết kế đã được kiểm chứng (production-proven) để tái sử dụng.


### 7.1. SWE-agent (Princeton NLP) — Planning-First Approach

**Bối cảnh**: SWE-agent sử dụng planning để agent không "lạc lối" trong codebase.

**Vấn đề ban đầu**:
- Agent không có kế hoạch rõ ràng → thực hiện lộn xộn
- Phải đọc toàn bộ codebase trước khi bắt đầu → tốn token
- Không biết khi nào dừng lại

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
- Success rate: 12.5% → 20.5% (+64%)
- Token usage giảm 30%
- Thời gian giải quyết giảm 40%

**Bài học**: **"Lập kế hoạch trước khi hành động — sơ đồ hóa codebase giúp giảm lãng phí thời gian khám phá"**

---

### 7.2. Anthropic Multi-Agent Architecture

**Bối cảnh**: Claude Code cần tạo ứng dụng phức tạp (games, DAW).

**Giải pháp — 3-Agent Planning System**:

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
- Tạo được games, DAW hoàn chỉnh
- Success rate cao hơn 80% so với single-agent
- Code quality tốt hơn nhờ evaluation loop

**Bài học**: **"Phân chia tác vụ → Song song hóa → Đánh giá (Decompose → Parallelize → Evaluate) — công thức 3 bước"**

---

### 7.3. Claude Code — Hierarchical Planning System

**Bối cảnh**: Claude Code leak reveals advanced planning architecture.

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

Bối cảnh: Cursor phải lập kế hoạch sửa code **dựa trên ngữ cảnh hiện tại của lập trình viên** — file đang mở, đoạn code đang chọn, dòng con trỏ, các chỉnh sửa gần đây. Code bên dưới minh họa cách nó thu thập ngữ cảnh, lập kế hoạch thay đổi, rồi tự thu hẹp phạm vi để không đụng vào những file không liên quan.

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
> **Khái niệm:** Design Principles là tập hợp các nguyên tắc thiết kế phần mềm (nguyên lý SOLID và "10 Điều răn" riêng cho lập kế hoạch) giúp bạn xây dựng một module planner sạch, gọn và dễ mở rộng.
>
> **Ẩn dụ/so sánh:** Giống bộ quy tắc xây nhà: tường chịu lực đặt ở đâu, dây điện đi chỗ nào — tuân thủ thì nhà bền và dễ sửa chữa; vi phạm thì về sau phải đập phá, tốn kém.
>
> **Vì sao quan trọng:** Vì một planner phát triển một thời gian rất dễ thành "mớ spaghetti" khó bảo trì — áp đúng nguyên tắc giúp hệ thống sống lâu và mở rộng dễ dàng.


### 8.1 SOLID Cho Planning System

**1. Single Responsibility (Đơn Trách Nhiệm)**
- Mỗi planner chỉ phân 1 loại task (code, research, deploy)
- Mỗi decomposition strategy xử lý 1 pattern cụ thể

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

Đây là 10 "điều răn" gói gọn toàn bộ kinh nghiệm của module thành những câu ngắn dễ nhớ. Mỗi dòng gồm quy tắc tiếng Anh (thuật ngữ chuẩn) kèm câu giải thích tiếng Việt. Bạn cứ đọc tuần tự và đối chiếu với các ví dụ phía trên — phần lớn những lỗi agent mắc phải đều vi phạm một trong các điều này.

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
> **Khái niệm:** Best Practices ("các thói quen tốt") gom lại những việc nên làm (DO), không nên làm (DON'T) và cách quản lý ngân sách token — rút ra từ kinh nghiệm chạy agent thực tế.
>
> **Ẩn dụ/so sánh:** Giống danh sách "kinh nghiệm của người đi trước": nên mang áo mưa khi dự báo mưa, đừng xuất phát khi bình xăng gần cạn — nghe theo sẽ đỡ tốn kém.
>
> **Vì sao quan trọng:** Vì những lỗi như vòng lặp vô hạn hay cạn token xảy ra rất dễ và rất tốn kém — biết trước để tránh là cách rẻ nhất.


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

Mỗi task nên có một "hạn mức tiêu dùng" token rõ ràng, giống hạn mức thẻ tín dụng. Code bên dưới là lớp `TokenBudgetManager`: phân bổ ngân sách cho từng task (`allocate`), ghi nhận số token đã dùng (`report`), kiểm tra còn đủ hạn mức để chạy tiếp không (`canContinue`), và xuất báo cáo hiệu suất cuối kỳ (`getReport`).

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
> **Khái niệm:** Testing Planning Systems là việc viết các bài kiểm thử tự động (unit test) để chắc chắn bộ lập kế hoạch hoạt động đúng: chia được task, tôn trọng dependency và quản lý token hợp lý.
>
> **Ẩn dụ/so sánh:** Giống bài kiểm tra định kỳ trước khi nộp bài lớn: kiểm tra lẻ từng phần (unit test) giúp bắt lỗi sớm, tránh để tới lúc ra sản xuất mới vỡ.
>
> **Vì sao quan trọng:** Vì một planner không được kiểm thử giống một quả bom nổ chậm — phát hiện lỗi sớm rẻ hơn nhiều so với sửa khi hệ thống đã chạy production.

Code bên dưới là bộ kiểm thử mẫu cho `TaskPlanner`, `TokenBudgetManager` và `AgentState`: bạn có thể chạy trực tiếp để xem từng hành vi (chia task, giới hạn độ sâu, retry, checkpoint/rollback) có đúng như mong đợi không.

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
> **Khái niệm:** Advanced Patterns là những kỹ thuật lập kế hoạch nâng cao dành cho task cực phức tạp: HTN (chia theo tầng bằng "công thức" đã cài sẵn cho từng loại việc) và Self-Reflective Planning (tự nhìn lại rồi sửa kế hoạch của chính mình).
>
> **Ẩn dụ/so sánh:** Giống đầu bếp bậc thầy: HTN như có sẵn tủ sách công thức để chia món; Self-Reflective giống việc sau mỗi lần nấu tự ngẫm "lần sau nêm ít muối hơn".
>
> **Vì sao quan trọng:** Vì những task cực khó sẽ đánh bại kế hoạch tuyến tính đơn giản — kỹ thuật này cho phép agent phân tích đa tầng và tự sửa sai ngay khi phát hiện vấn đề.


### 11.1 Hierarchical Task Network (HTN)

HTN mở rộng ý tưởng chia nhỏ ở mục 1 bằng cách dùng sẵn **các "công thức chia việc" (methods)**: với mỗi loại task có sẵn cách chia thành các mảnh nhỏ hơn, và cứ bóc tách đến khi gặp tác vụ nguyên thủy (primitive) có thể chạy trực tiếp. Code dưới đây cho thấy cách đăng ký method, điều kiện áp dụng (precondition), rồi lần lượt đệ quy chia nhỏ theo tầng.

> Giống tủ đựng mẫu biên bản sẵn: gặp loại việc nào thì rút mẫu đó ra chia — nhanh và chuẩn hơn là tự nghĩ ra cách chia mỗi lần.

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

Ý tưởng: agent làm kế hoạch rồi **tự chấm điểm chất lượng kế hoạch đó** (tính đầy đủ, khả thi, rủi ro); nếu điểm thấp thì tự sửa theo gợi ý của chính nó rồi lặp lại vài vòng. Class `SelfReflectivePlanner` bên dưới triển khai đúng vòng lặp Plan → Reflect → Improve, đồng thời ghi lại lịch sử kế hoạch để học từ kết quả thực tế.

> Giống bạn viết nháp bài văn: viết xong đọc lại, thấy chỗ nào yếu thì sửa, rồi mới nộp bản cuối cùng.

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
> **Khái niệm:** Tools & Frameworks là các thư viện mã nguồn mở sẵn có giúp bạn xây hệ thống planning/agent nhanh chóng thay vì tự viết từ con số 0 — tiêu biểu là LangGraph, CrewAI và AutoGen.
>
> **Ẩn dụ/so sánh:** Giống chọn mua nhà tiền chế thay vì tự xây gạch: có khung sẵn (state machine, agent orchestration), bạn chỉ việc lắp ráp và tùy biến theo nhu cầu.
>
> **Vì sao quan trọng:** Vì tự viết lại mọi thứ vừa chậm vừa dễ sai — dùng framework đã được cộng đồng kiểm chứng giúp rút ngắn thời gian phát triển và chuẩn hóa kiến trúc.


### 12.1 LangGraph (Recommended for Planning)

LangGraph cho phép bạn mô tả workflow như một **máy trạng thái (state machine)** bằng đồ thị: mỗi node là một công đoạn, mỗi edge là đường đi, và có thể rẽ nhánh tùy điều kiện. Code dưới đây dựng một vòng lặp planning hoàn chỉnh: analyze → plan → validate → execute — nếu validate fail thì rẽ sang replan, còn thành công thì kết thúc.

> Giống sơ đồ tuyến tàu điện: vẽ sẵn các ga (node) và đường ray (edge), tàu chạy đúng lộ trình, có nhánh rẽ khi cần đổi hướng.

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

CrewAI tổ chức các agent như một **đội ngũ (crew)**: bạn định nghĩa từng vai (Agent) với mục tiêu và công cụ riêng, giao các task (nhiệm vụ), rồi để chúng phối hợp hoàn thành. Code dưới đây tạo ra ba vai điển hình: Planner (lập kế hoạch), Executor (thực thi) và Reviewer (kiểm duyệt).

> Giống dựng một công ty thu nhỏ với ba phòng ban, mỗi phòng có sứ mệnh riêng, cùng làm xong một dự án.

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

AutoGen của Microsoft cho phép các agent **trò chuyện với nhau** để phối hợp — mỗi agent là một "đầu óc" có thể gửi tin cho agent khác. Code mẫu bên dưới định nghĩa planner bày kế hoạch, executor thực thi, và user proxy đại diện cho người thật để duyệt kết quả cuối.

> Giống nhóm chat thảo luận công việc: người này đề xuất, người kia làm, có người chốt duyệt trước khi nộp.

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
> **Khái niệm:** Tương Lai là phần nhìn xa về các xu hướng lập kế hoạch của AI Agent giai đoạn 2026-2028: tự lập kế hoạch, lập kế hoạch hiệp tác, dự đoán rủi ro trước khi xảy ra, và giao diện lập kế hoạch trực quan.
>
> **Ẩn dụ/so sánh:** Giống đọc dự báo thị trường trước khi đầu tư: hiểu xu hướng để chuẩn bị từ sớm thay vì chạy theo khi mọi người đã đổ về.
>
> **Vì sao quan trọng:** Vì kiến trúc bạn xây hôm nay sẽ quyết định bạn có đón đầu được 3 năm tới hay không — đọc để đầu tư đúng hướng.


### 13.1 Xu Hướng 2026-2028

**1. AI Tự Lập Kế Hoạch (AI Self-Planning)**
- Agent tự động tạo kế hoạch không cần human input
- Adaptive planning dựa trên real-time feedback
- Cross-task learning (học từ planning history)

**2. Lập Kế Hoạch Hiệp Tác (Collaborative Planning)**
- Nhiều agents cùng plan và vote
- Lập kế hoạch phân tán giữa các đội ngũ
- Chia sẻ cơ sở tri thức lập kế hoạch

**3. Lập Kế Hoạch Dự Đoán (Predictive Planning)**
- Dự đoán thất bại trước khi xảy ra
- Chủ động lập lại kế hoạch (Re-planning)
- Phân bổ tác vụ nhận biết rủi ro

**4. Lập Kế Hoạch Nhận Biết Context (Context-Aware Planning)**
- Kế hoạch thích ứng với Context khả dụng
- Phân bổ tài nguyên động
- Quản lý ngân sách Token thông minh

**5. Giao Diện Lập Kế Hoạch Trực Quan (Visual Planning Interfaces)**
- Trình dựng kế hoạch kéo thả
- Trực quan hóa kế hoạch theo thời gian thực
- Chỉnh sửa kế hoạch tương tác

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
*Ngày cập nhật: 13/07/2026*
*Tác giả: AI Knowledge Repository*