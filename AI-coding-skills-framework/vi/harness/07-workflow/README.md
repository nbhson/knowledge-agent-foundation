# ⚙️ VII. Workflow

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Workflow Patterns](#1-workflow-patterns)
>   - [1.1 Sequential Workflow (Tuần Tự)](#11-sequential-workflow-tuần-tự)
>   - [1.2 Parallel Workflow (Song Song)](#12-parallel-workflow-song-song)
>   - [1.3 DAG Workflow (Directed Acyclic Graph)](#13-dag-workflow-directed-acyclic-graph)
>   - [1.4 Event-Driven Workflow](#14-event-driven-workflow)
> - [2. Pipeline Design](#2-pipeline-design)
>   - [2.1 Data Pipeline với Branching](#21-data-pipeline-với-branching)
> - [3. State Machine](#3-state-machine)
>   - [3.1 Hierarchical State Machine](#31-hierarchical-state-machine)
> - [4. Error Recovery](#4-error-recovery)
>   - [4.1 Retry Strategies](#41-retry-strategies)
>   - [4.2 Circuit Breaker Pattern](#42-circuit-breaker-pattern)
>   - [4.3 Saga Pattern](#43-saga-pattern)
> - [5. Observability](#5-observability)
>   - [5.1 Distributed Tracing](#51-distributed-tracing)
>   - [5.2 Structured Logging + Metrics](#52-structured-logging-metrics)
> - [6. Workflow Orchestration Engine](#6-workflow-orchestration-engine)
> - [7. Workflow Testing](#7-workflow-testing)
> - [8. Harness Integration](#8-harness-integration)
>   - [8.1 TypeScript Interfaces](#81-typescript-interfaces)
> - [9. Case Studies](#9-case-studies)
>   - [9.1. GitHub Actions — Event-Driven CI/CD](#91-github-actions-event-driven-cicd)
>   - [9.2. Apache Airflow — Data Pipeline Orchestration](#92-apache-airflow-data-pipeline-orchestration)
>   - [9.3. Temporal — Durable Workflow Execution](#93-temporal-durable-workflow-execution)
> - [10. Design Principles](#10-design-principles)
>   - [10.1 SOLID Cho Workflows](#101-solid-cho-workflows)
>   - [10.2 6 Design Principles](#102-6-design-principles)
> - [11. Best Practices](#11-best-practices)
>   - [11.1 DO ✅](#111-do)
>   - [11.2 DON'T ❌](#112-dont)
> - [12. Tương Lai](#12-tương-lai)
>   - [12.1 Xu Hướng 2026-2028](#121-xu-hướng-2026-2028)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks](#frameworks)
>
---

### Câu Chuyện Mở Đầu

**Phần này giải thích workflow là gì, và vì sao agent không có nó thì dễ hỏng.**

Hãy tưởng tượng một **xưởng làm bánh mì** vào giờ cao điểm buổi sáng. Bột phải nhào rồi mới ủ, ủ đủ giờ mới nướng, nướng xong mới đóng gói đem bán. Nếu mỗi người thợ tự làm theo ý mình — người nướng khi bột chưa ủ, người đóng gói khi bánh còn sống — thì cả mẻ bánh hôm đó coi như bỏ.

**AI Agent không có Workflow cũng rối y như vậy.**

Nhiều bạn viết agent chỉ là **một chuỗi function gọi nối tiếp nhau** — không lưu trạng thái đang làm tới đâu, không có cách chữa cháy khi lỗi, không có điểm lưu để chạy tiếp. Task nhỏ thì còn chạy được. Nhưng task càng lớn — **chỉ cần lỗi một bước là phải chạy lại từ đầu, vừa mất thời gian vừa tốn tiền**.

**Giải pháp** chính là Workflow có cấu trúc — một cách tổ chức để quản lý **cả vòng đời** của task, từ lúc bắt đầu (trigger = sự kiện kích hoạt, ví dụ một file được đổi hoặc lịch hẹn tới giờ) tới lúc xong và rút kinh nghiệm (feedback), mà bước nào cũng **lưu vết được, lỗi có đường lui, và nhìn thấy đang chạy tới đâu**.

> **Tóm gọn 1 câu:** Workflow là bộ khung quản lý toàn bộ hành trình của task, để lỗi một bước không phải làm lại từ đầu.

### Tại Sao Workflow Quan Trọng?

> *"Agent không có workflow giống như đầu bếp không có thực đơn — có nguyên liệu, có dụng cụ, nhưng món ra tùy hứng."*

#### 3 Bằng Chứng Khoa Học

*Cách đọc bảng này: mỗi dòng là một nghiên cứu; cột "Phát Hiện Quan Trọng" nêu con số chứng minh workflow có tác dụng thật. Ví dụ dòng 1: chia các bước thành khuôn mẫu có cấu trúc giúp giảm gần một nửa số task thất bại.*

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Google DeepMind (2025)** | Structured workflows giảm **45% task failure rate** trong multi-step coding agents |
| 2 | **Anthropic (2025)** | Workflow engine với retry + checkpoint giảm **70% data loss** khi agent gặp lỗi |
| 3 | **LangGraph Benchmark (2025)** | State machine workflows xử lý **3× complex tasks** tốt hơn simple sequential chains |

*Giải nghĩa thuật ngữ trong bảng:* **task failure rate** = tỷ lệ task thất bại; **retry** = tự thử lại khi lỗi; **checkpoint** = điểm lưu tiến độ để chạy tiếp mà không phải làm lại từ đầu; **state machine** = mô hình máy trạng thái, chỉ cho agent bước sang giai đoạn kế tiếp khi đủ điều kiện (giải thích kỹ ở mục 3).

#### Triết lý cốt lõi:

```
Workflow = Trigger → Plan → Execute → Validate → Deploy → Feedback
```

*Đọc dòng trên thế này:* Trigger = sự kiện kích hoạt (ví dụ có commit mới) → Plan = lập kế hoạch các bước → Execute = chạy từng bước → Validate = kiểm tra kết quả → Deploy = đưa vào dùng thật → Feedback = rút kinh nghiệm cho lần sau.

Mỗi bước trong chuỗi đó đều phải có **quản lý trạng thái (state management = nhớ đang làm tới đâu)**, **cách xử lý khi lỗi (error recovery)**, và **cách theo dõi (observability)**. Workflow không chỉ là "xếp thứ tự các bước" — mà là cách lo cho **cả vòng đời** của một task.

**Hình dung cho dễ**: Workflow giống hệ thống giao thông trong thành phố — có đèn tín hiệu (guardrails = thanh chắn an toàn chặn hành động nguy hiểm), có tuyến đường vẽ sẵn (steps = các bước), có trung tâm điều phối (orchestrator = bộ điều phối trung tâm), và có camera theo dõi (logging = ghi nhật ký mọi việc đã xảy ra).

**Nếu bỏ qua Workflow**: agent làm việc lộn xộn, đang chạy mà lỗi là chịu chết không cứu được, không biết tiến độ tới đâu, và mỗi lần debug là một lần đau đầu.

> **Tóm gọn 1 câu:** Nghiên cứu thật chứng minh workflow có cấu trúc giúp agent ít lỗi hơn nhiều, vì nó lo trọn vòng đời: kích hoạt, chạy, kiểm tra, và rút kinh nghiệm.

## Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow là cách sắp xếp các bước thực hiện của AI Agent thành một kế hoạch rõ ràng — bước nào trước, bước nào sau, lỗi xử lý ra sao — để một tác vụ phức tạp được hoàn thành đúng trình tự và an toàn.
> - **Ẩn dụ/so sánh:** Giống bếp nhà hàng: đầu bếp (agent) có nguyên liệu tốt vẫn cần thực đơn và quy trình trực (workflow) để ra món đúng giờ, đúng chất lượng mỗi lần.
> - **Vì sao quan trọng:** Không có workflow, agent làm việc theo cảm hứng — vừa chậm, vừa khó lặp lại kết quả, và hỏng giữa chừng là phải làm lại từ đầu.

**Workflow** là cách **sắp xếp các bước làm việc** để hoàn thành một task coding phức tạp. Trong Harness Engineering, Workflow Engine đóng vai trò **"người điều phối chính"** — lo toàn bộ hành trình từ trigger → plan → execute → validate → deploy, kèm theo theo dõi (observability), xử lý lỗi (error recovery), và quản lý trạng thái (state management).

*Giải nghĩa sơ đồ dưới đây, đọc từ trên xuống:* **Trigger** = thứ khởi động workflow (sự kiện / lịch hẹn / webhook — tức tín hiệu tự động gửi từ hệ thống khác). **Orchestrator** = bộ điều phối trung tâm, gồm 4 mảnh: **State Machine** (máy trạng thái — nhớ agent đang ở giai đoạn nào), **Task Queue** (hàng đợi — các tác vụ chờ đến lượt), **Guard Rails** (thanh chắn — chặn hành động nguy hiểm), **Retry Engine** (bộ tự thử lại khi lỗi). **Execution Engine** = nơi chạy thật, chọn cách chạy: tuần tự (Sequential) / song song (Parallel) / theo đồ thị phụ thuộc (DAG) / có điều kiện. **Observability & Recovery** = quan sát và tự chữa: Tracing (truy vết từng request), Metrics (số đo), Circuit Breaker (cầu chì ngắt khi lỗi dồn dập), Saga (cuộn ngược nhiều bước khi có lỗi). Cuối cùng xuất ra **kết quả + log + số đo + sản phẩm phụ (artifacts)**, và module này nối với các module khác của harness qua **HARNESS INTEGRATION**.

```
┌──────────────────────────────────────────────────────────────────┐
│                         WORKFLOW ENGINE                           │
│                                                                  │
│  Trigger (Event/Schedule/Webhook)                                │
│       │                                                          │
│       ▼                                                          │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  WORKFLOW ORCHESTRATOR                                     │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  State   │  │  Task    │  │  Guard   │  │  Retry   │  │  │
│  │  │  Machine │  │  Queue   │  │  Rails   │  │  Engine  │  │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │  │
│  │       └──────────────┼──────────────┼──────────────┘        │  │
│  │                      ▼                                       │  │
│  │  ┌──────────────────────────────────────────────────┐      │  │
│  │  │              EXECUTION ENGINE                     │      │  │
│  │  │  Sequential | Parallel | DAG | Conditional       │      │  │
│  │  └──────────────────────┬───────────────────────────┘      │  │
│  │                         │                                    │  │
│  │  ┌──────────────────────┼───────────────────────────┐      │  │
│  │  │        OBSERVABILITY & RECOVERY                   │      │  │
│  │  │  Tracing | Metrics | Circuit Breaker | Saga      │      │  │
│  │  └──────────────────────────────────────────────────┘      │  │
│  └────────────────────────────────────────────────────────────┘  │
│       │                                                          │
│       ▼                                                          │
│  Result + Logs + Metrics + Artifacts                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  HARNESS INTEGRATION                                       │  │
│  │  Memory ←→ Guardrails ←→ Feedback ←→ Observability       │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Nội Dung

*Cách đọc bảng này: mỗi dòng là một chủ đề trong tài liệu; bấm vào tên chủ đề ở cột giữa để nhảy tới. Ví dụ dòng 4: mục "Error Recovery" dạy cách tự thử lại (retry), ngắt mạch khi lỗi dồn dập (circuit breaker), và cuộn ngược nhiều bước (saga).*

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Workflow Patterns](#1-workflow-patterns) | Sequential, Parallel, DAG, Event-driven |
| 2 | [Pipeline Design](#2-pipeline-design) | Transform, Branching, Fan-out/Fan-in |
| 3 | [State Machine](#3-state-machine) | FSM nâng cao, hierarchical states |
| 4 | [Error Recovery](#4-error-recovery) | Retry, Circuit Breaker, Saga pattern |
| 5 | [Observability](#5-observability) | Structured logging, distributed tracing |
| 6 | [Workflow Orchestration](#6-workflow-orchestration) | Engine tổng hợp |
| 7 | [Workflow Testing](#7-workflow-testing) | Unit, integration, chaos testing |
| 8 | [Harness Integration](#8-harness-integration) | TypeScript interfaces |
| 9 | [Case Studies](#9-case-studies) | GitHub Actions, Airflow, Temporal |
| 10 | [Design Principles](#10-design-principles) | SOLID cho workflows |
| 11 | [Best Practices](#11-best-practices) | DO/DON'T chi tiết |
| 12 | [Tương Lai](#12-tương-lai) | Xu hướng 2026-2028 |

*Giải nghĩa nhanh các từ khóa trong cột "Mô tả":* **Transform** = biến đổi dữ liệu (ví dụ đổi JSON thành bảng); **Fan-out/Fan-in** = chia việc cho nhiều nhánh chạy cùng lúc rồi gộp kết quả về; **FSM** = Finite State Machine, máy trạng thái hữu hạn; **chaos testing** = cố tình gây lỗi để test khả năng chịu đựng.

> **Tóm gọn 1 câu:** Tài liệu đi từ 4 khuôn mẫu chạy cơ bản, qua xử lý lỗi và quan sát, tới engine hoàn chỉnh và bài học từ hệ thống thật.

---

## 1. Workflow Patterns

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Patterns là các "khuôn mẫu" tổ chức chuỗi hoạt động của AI Agent — chạy tuần tự (sequential), chạy song song (parallel), rẽ nhánh theo điều kiện (conditional branching) — nhằm đạt mục tiêu nhiệm vụ một cách có kiểm soát.
> - **Ẩn dụ/so sánh:** Giống đường đi trong thành phố: một con đường thẳng (sequential), nhiều làn chạy đồng thời (parallel), hay giao lộ rẽ hướng tuỳ biển báo (conditional branching).
> - **Vì sao quan trọng:** Chọn đúng pattern quyết định tốc độ, độ phức tạp và khả năng chịu lỗi của cả workflow.

### 1.1 Sequential Workflow (Tuần Tự)

Giống nấu một món ăn theo công thức: làm xong bước 1 mới sang bước 2, không được bỏ qua, không lộn thứ tự. Đây là pattern đơn giản nhất — dễ viết, dễ debug, nhưng hơi chậm vì mọi bước nối đuôi nhau. Dùng khi bước sau bắt buộc phải phụ thuộc vào kết quả bước trước. Diagram dưới đây minh hoạ luồng 5 bước Parse (đọc và tách dữ liệu) → Analyze (phân tích) → Build (build code) → Test (chạy kiểm thử) → Deploy (đưa lên chạy thật):

```
┌──────────────────────────────────────────────────────────────────┐
│                   SEQUENTIAL WORKFLOW                             │
│                                                                  │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐     │
│  │Step 1│───►│Step 2│───►│Step 3│───►│Step 4│───►│Step 5│     │
│  │Parse │    │Analyze│   │Build │    │Test  │    │Deploy│     │
│  └──────┘    └──────┘    └──────┘    └──────┘    └──────┘     │
│                                                                  │
│  Mỗi bước chỉ chạy SAU khi bước trước hoàn thành              │
│  → Đơn giản, dễ debug, nhưng chậm                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-1-sequential-workflow-tuan-tu.py`](examples/01-1-1-sequential-workflow-tuan-tu.py)

</details>

> **Tóm gọn 1 câu:** Chạy tuần tự = bước nào xong mới tới bước sau; đơn giản, dễ sửa lỗi, nhưng chậm.

### 1.2 Parallel Workflow (Song Song)

Giống nấu bữa tiệc với nhiều trợ lý: cùng lúc người rửa rau, người nấu cơm, người chiên thịt — xong tất cả mới gom lại dọn bàn. Pattern này chạy nhanh vì nhiều bước cùng lúc, nhưng phần khó nằm ở chỗ gộp (fan-in) kết quả về. Dùng khi các bước độc lập với nhau, không cần chờ nhau. *Đọc sơ đồ:* **Fan-Out (chia)** = bơm việc đi nhiều nhánh cùng lúc; **Fan-In (gộp)** = đợi cả 4 nhánh xong rồi gom kết quả về một đầu ra duy nhất:

```
┌──────────────────────────────────────────────────────────────────┐
│                    PARALLEL WORKFLOW (Song Song)                  │
│                                                                  │
│                        ┌──────────┐                              │
│                        │  Input   │                              │
│                        └────┬─────┘                              │
│                             │                                    │
│                             ▼                                    │
│                  ┌─────────────────────┐                         │
│                  │   Fan-Out (chia)    │                         │
│                  └───┬────┬────┬────┬──┘                         │
│                      │    │    │    │                            │
│                      ▼    ▼    ▼    ▼                            │
│              ┌──────┐┌──────┐┌──────┐┌──────┐                    │
│              │Task A││Task B││Task C││Task D│                    │
│              │Parse ││Analyze││Build ││Test  │                    │
│              └──────┘└──────┘└──────┘└──────┘                    │
│                      │    │    │    │                            │
│                      ▼    ▼    ▼    ▼                            │
│                  ┌─────────────────────┐                         │
│                  │   Fan-In (gộp)      │                         │
│                  └─────────┬───────────┘                         │
│                            │                                     │
│                            ▼                                     │
│                        ┌──────────┐                              │
│                        │  Output  │                              │
│                        └──────────┘                              │
│                                                                  │
│  Nhiều bước chạy ĐỒNG THỜI, chờ tất cả hoàn thành             │
│  → Nhanh, nhưng phức tạp khi gộp kết quả                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-1-2-parallel-workflow-song-song.py`](examples/02-1-2-parallel-workflow-song-song.py)

</details>

> **Tóm gọn 1 câu:** Chạy song song = chia việc cho nhiều nhánh làm cùng lúc (fan-out) rồi đợi gộp kết quả (fan-in); nhanh hơn nhưng phần gộp là chỗ dễ sai.

### 1.3 DAG Workflow (Directed Acyclic Graph)

Giống lịch thi đấu giải thể thao: trận bán kết phải chờ đủ hai trận tứ kết, nhưng hai trận tứ kết lại diễn ra song song. DAG là pattern linh hoạt nhất — mỗi node (nút = một bước trong workflow) chỉ chạy sau khi các node nó phụ thuộc (dependency = quan hệ "cần kết quả của bước kia") hoàn thành, hết "tầng" này rồi mới sang "tầng" kia, và tuyệt đối không có vòng lặp. *Giải nghĩa tên gọi:* **Directed** = mũi tên một chiều (A làm xong mới tới C); **Acyclic** = không có vòng lặp (không bao giờ A quay lại chính nó). Ví dụ dưới đây: A và B chạy song song → C chờ A, D chờ B → E chờ C, F chờ D:

```
┌──────────────────────────────────────────────────────────────────┐
│                    DAG WORKFLOW (Directed Acyclic Graph)          │
│                                                                  │
│   Level 1          Level 2          Level 3                      │
│                                                                  │
│   ┌──────┐         ┌──────┐         ┌──────┐                     │
│   │Node A│────────►│Node C│────────►│Node E│                     │
│   └──────┘         └──────┘         └──────┘                     │
│                                                                  │
│   ┌──────┐         ┌──────┐         ┌──────┐                     │
│   │Node B│────────►│Node D│────────►│Node F│                     │
│   └──────┘         └──────┘         └──────┘                     │
│                                                                  │
│   A, B chạy song song → C chờ A, D chờ B → E chờ C, F chờ D    │
│   → Tối ưu dependency, không vòng lặp (acyclic)                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-1-3-dag-workflow-directed-acyclic-graph.py`](examples/03-1-3-dag-workflow-directed-acyclic-graph.py)

</details>

> **Tóm gọn 1 câu:** DAG = biểu đồ phụ thuộc có hướng, không vòng lặp; bước nào đủ điều kiện là chạy, nên vừa linh hoạt vừa không bao giờ mắc kẹt.

### 1.4 Event-Driven Workflow

Giống trung tâm báo cháy: chuông reo (event) ở đâu thì đội ứng trực (handler = hàm đảm nhận xử lý sự kiện đó) phản hồi ở đó, và mỗi phản hồi có thể kích ra một báo động mới. Khác với các pattern trên, luồng không được định sẵn từ đầu — workflow phản ứng theo từng sự kiện nảy sinh, nên rất linh hoạt với hệ thống bất định:

```
┌──────────────────────────────────────────────────────────────────┐
│                    EVENT-DRIVEN WORKFLOW                          │
│                                                                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                 │
│   │  Event   │────►│  Event   │────►│  Event   │                 │
│   │  A       │     │  B       │     │  C       │                 │
│   └────┬─────┘     └────┬─────┘     └────┬─────┘                 │
│        │                │                │                       │
│        ▼                ▼                ▼                       │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                 │
│   │ Handler  │     │ Handler  │     │ Handler  │                 │
│   │  1       │     │  2       │     │  3       │                 │
│   └──────────┘     └──────────┘     └──────────┘                 │
│                                                                  │
│   Workflow phản ứng theo sự kiện; handler có thể phát sinh      │
│   sự kiện mới → chuỗi phản ứng linh hoạt, không cần định        │
│   trước thứ tự                                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-1-4-event-driven-workflow.py`](examples/04-1-4-event-driven-workflow.py)

</details>

> **Tóm gọn 1 câu:** Event-driven = không vẽ sẵn luồng đi, mà cứ có sự kiện là hàm xử lý tương ứng nhảy vào, có thể kích chuỗi phản ứng mới.

---

## 2. Pipeline Design

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Pipeline Design là cách chia một tác vụ lớn thành nhiều giai đoạn (stages) nối tiếp nhau; mỗi giai đoạn nhận dữ liệu từ giai đoạn trước, xử lý rồi chuyển tiếp cho giai đoạn sau, kèm khả năng rẽ nhánh (branching) và fan-out/fan-in.
> - **Ẩn dụ/so sánh:** Giống dây chuyền nhà máy bia: nghiền → nấu → lọc → lên men → đóng chai; mỗi công đoạn nhận đầu ra của công đoạn trước, và có ngã rẽ nếu khách đặt loại bia khác.
> - **Vì sao quan trọng:** Pipeline giúp xử lý dữ liệu lớn gọn gàng, kiểm tra được từng khâu và dễ đổi mới khi nghiệp vụ thay đổi.

### 2.1 Data Pipeline với Branching

**Mục này giải thích cách chia một tác vụ dữ liệu lớn thành các khâu nối dây chuyền, có chỗ rẽ nhánh theo điều kiện.**

Đây là "dây chuyền làm việc" cho dữ liệu: mỗi khâu là một stage (transform = biến đổi, filter = lọc, branch = rẽ nhánh, fan_out = chia ra nhiều nhánh, validator = kiểm tra dữ liệu, sink = điểm đích cuối cùng), dữ liệu chảy qua từng khâu như sản phẩm qua từng công đoạn. Điểm đặc biệt là branching — một khâu kiểm tra điều kiện rồi rẽ dữ liệu sang hai nhánh khác nhau, như băng chuyền có chốt chuyển hướng hàng. Code bên dưới cho thấy cách ráp và chạy một pipeline đầy đủ:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-2-1-data-pipeline-voi-branching.py`](examples/05-2-1-data-pipeline-voi-branching.py)

</details>

> **Tóm gọn 1 câu:** Pipeline = dây chuyền các khâu xử lý nối tiếp nhau, có chốt rẽ nhánh để dữ liệu đi đúng đường theo điều kiện.

---

## 3. State Machine

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** State Machine là "máy trạng thái" — mô hình ghi lại Agent đang ở trạng thái nào (đang đọc code, đang viết code, đang test) và chỉ cho phép chuyển sang trạng thái tiếp theo khi thoả điều kiện nhất định.
> - **Ẩn dụ/so sánh:** Giống đèn giao thông ba màu: xe chỉ được đi khi đèn xanh, chuỗi xanh → vàng → đỏ luôn đúng tuần tự và không bao giờ vọt thẳng từ đỏ sang xanh.
> - **Vì sao quan trọng:** Nó ngăn Agent nhảy loạn giữa các bước, giữ cho luồng thực thi lúc nào cũng hợp lệ và có thể dự đoán được.

### 3.1 Hierarchical State Machine

**Mục này giải thích bản nâng cấp của máy trạng thái, đủ an toàn để điều khiển agent thật.**

Đây là bản "nâng cấp" của state machine: ngoài chuyển trạng thái có điều kiện, nó còn hỗ trợ trạng thái cha/con (hierarchical = trạng thái lớn chứa các trạng thái nhỏ, ví dụ "đang làm việc" chia thành "đang đọc code" và "đang viết code"), guard chặn chuyển bất hợp lệ (guard = điều kiện bảo vệ, không thoả thì không cho chuyển), timeout tự động (quá giờ thì nhảy trạng thái) và giới hạn số lần lặp — đủ an toàn để điều khiển cả một AI coding agent. Code dưới đây mô phỏng agent đi qua chuỗi trạng thái IDLE (rảnh) → THINKING (đang suy nghĩ) → PLANNING (đang lập kế hoạch) → READING_CODE (đang đọc code) → WRITING_CODE (đang viết code) → RUNNING_TESTS (đang chạy test) → DONE (xong):

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-3-1-hierarchical-state-machine.py`](examples/06-3-1-hierarchical-state-machine.py)

</details>

> **Tóm gọn 1 câu:** State machine = chỉ cho agent chuyển giai đoạn khi đủ điều kiện, nên luồng làm việc luôn hợp lệ và đoán được.

---

## 4. Error Recovery

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Error Recovery là bộ chiến lược xử lý khi workflow gặp lỗi — thử lại với thời gian chờ tăng dần (retry/backoff), fallback sang phương án khác, hoặc cắt mạch bảo vệ (circuit breaker) — để hệ thống chạy ổn định thay vì sập cả tiến trình.
> - **Ẩn dụ/so sánh:** Giống gọi điện thoại khi máy bận: thử lại sau 1 phút (retry), chưa được thì chờ lâu hơn (backoff), hoặc quay sang gọi người thứ hai (fallback).
> - **Vì sao quan trọng:** Lỗi chắc chắn sẽ xảy ra; có chiến lược khôi phục thì workflow không bị chết đứng giữa chừng.

### 4.1 Retry Strategies

Giống nhấn "gửi lại" email khi mạng chập chờn — nhưng làm có khoa học: thử lại với khoảng chờ tăng dần (1s → 2s → 4s) để không dồn tải lên service, và thêm jitter (độ nhiễu ngẫu nhiên — mỗi máy chờ lệch nhau một chút) để các client không cùng lúc "dồn đàn" như bầy trâu tháo chạy (thundering herd = hàng nghìn request dồn về service cùng một khoảnh khắc, làm service gục luôn). Code dưới đây là decorator retry (decorator = hàm bọc ngoài hàm khác để tự động thêm hành vi thử lại) dùng cho cả hàm đồng bộ lẫn async:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-4-1-retry-strategies.py`](examples/07-4-1-retry-strategies.py)

</details>

> **Tóm gọn 1 câu:** Retry có kỷ luật = thử lại với khoảng chờ tăng dần và ngẫu nhiên, để lỗi thoáng qua tự lành mà không đè sập service.

### 4.2 Circuit Breaker Pattern

Giống cầu chì điện trong nhà: dòng lỗi quá dày thì cầu chì đứt, ngắt luôn dòng điện để bảo vệ toàn hệ thống. Ở đây, khi một service lỗi liên tục vượt ngưỡng, mạch chuyển từ CLOSED (đóng = bình thường, vẫn gọi) sang OPEN (mở = chặn hẳn gọi, khỏi mất công gọi tới service đang gục); sau một khoảng thời gian hồi phục, nó thử lại ở trạng thái HALF_OPEN (nửa mở = cho phép một vài lượt gọi thử, nếu thông thì trả về CLOSED):

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-4-2-circuit-breaker-pattern.py`](examples/08-4-2-circuit-breaker-pattern.py)

</details>

> **Tóm gọn 1 câu:** Circuit breaker = cầu chì cho service: lỗi dày thì ngắt hẳn, hồi sức xong mới thả gọi lại, để một chỗ hỏng không kéo sập cả dây chuyền.

### 4.3 Saga Pattern

Giống làm thủ tục đặt tour trọn gói: nếu hỏng giữa chừng ở bước "đặt vé máy bay" thì phải huỷ ngược lại các bước đã thành công — trả tiền phòng, trả tiền bảo hiểm. Saga dùng cho nghiệp vụ trải qua nhiều services (nhiều hệ thống nhỏ hợp tác, không thể "commit tất cả một lúc" như một giao dịch database duy nhất): mỗi bước đều có một compensation (bước bù = thao tác đảo ngược bước đó, ví dụ hoàn tiền) để cuộn ngược khi có bước nào đó fail:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-4-3-saga-pattern.py`](examples/09-4-3-saga-pattern.py)

</details>

> **Tóm gọn 1 câu:** Saga = mọi bước đều có sẵn bước bù, nên hỏng ở bước nào cũng cuộn ngược được toàn bộ những gì đã làm.

---

## 5. Observability

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Observability là khả năng "nhìn thấy bên trong" workflow bằng ba loại dữ liệu — logs (nhật ký sự kiện), metrics (số đo), traces (dấu vết của từng request) — để biết chính xác chuyện gì xảy ra ở từng bước.
> - **Ẩn dụ/so sánh:** Giống camera hành trình + đồng hồ công tơ mét + bản đồ GPS của một chiếc taxi: biết xe đang đi đâu, chạy nhanh chậm thế nào, và đang bị kẹt ở đoạn nào.
> - **Vì sao quan trọng:** Không quan sát được thì khi workflow chậm hay sai, bạn không thể tìm ra nguyên nhân và phải mò từng bước một để debug.

> **Ghi chú để khỏi nhầm — hai tầng khác nhau, đừng gộp làm một.** Mục này chỉ lo **theo dõi cho một
> lượt chạy (run)**: một `trace_id` đi xuyên suốt các bước của *lần chạy đó*, các span chia theo quan hệ cha–con,
> một logger, và một bộ gom metrics. Đó là bộ đồ nghề tracing phân tán kinh điển, và
> nó trả lời câu hỏi "vì sao *lần chạy này* bị chậm".
>
> **Hợp đồng event dùng chung giữa các module** — luồng `TrajectoryEvent` dạng append-only mà mọi module trong
> harness đều ghi vào và mọi công cụ debug đều đọc từ đó, với join key, fork/replay, retention, và
> redaction — là phần của
> [`13-trajectory-observability`](../13-trajectory-observability/README.md). Một `trace_id`
> không phải là `sessionId`, và một span không phải là một `TrajectoryEvent`; hai thứ gặp nhau
> ở `runId`. Nếu bạn đang dựng khung xương cho harness thì đọc thêm `13`. Còn nếu bạn chỉ đang
> ráp một workflow chạy được, phần dưới đây là đủ dùng.

### 5.1 Distributed Tracing

Giống "lệnh truy vết" xuyên suốt hành trình: mỗi yêu cầu được gán một trace_id (mã định danh duy nhất cho cả lượt chạy) đi qua bao nhiêu service thì mỗi bước đều ghi lại thành spans (span = đoạn ghi thời gian của một bước; span cha chứa span con như chuỗi khoá móc) — nhờ đó bạn dựng lại toàn bộ hành trình của một request và tìm ra chính xác khâu nào chậm hay lỗi:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-5-1-distributed-tracing.py`](examples/10-5-1-distributed-tracing.py)

</details>

> **Tóm gọn 1 câu:** Distributed tracing = mỗi request mang một mã vạch (trace_id) xuyên suốt, nên bạn dựng lại được hành trình và chỉ ra đúng khâu chậm hay lỗi.

### 5.2 Structured Logging + Metrics

Giống nhiệt kế + sổ ghi chép của máy móc: một bên (structured logging = ghi log có cấu trúc) ghi lại từng sự kiện dưới dạng JSON (định dạng dữ liệu có sẵn cột tên-giá trị, nên lọc tìm được, khác với log dòng chữ tự do) để dễ lọc tìm, một bên (metrics = số đo thống kê) đếm và thống kê số liệu — số lần chạy, tỷ lệ thành công, độ trễ p50/p95/p99 (p50 = nửa số request nhanh hơn con số này, p95 = 95% nhanh hơn, p99 = 99% nhanh hơn — tức con số mà trường hợp xấu nhất phải chịu). Code dưới đây gồm hai lớp WorkflowLogger và MetricsCollector:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/11-5-2-structured-logging-metrics.py`](examples/11-5-2-structured-logging-metrics.py)

</details>

> **Tóm gọn 1 câu:** Logging có cấu trúc + metrics = vừa ghi lại từng sự kiện dạng JSON lọc được, vừa có số đo sức khoẻ (tỷ lệ thành công, độ trễ) của workflow.

---

## 6. Workflow Orchestration Engine

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Orchestration Engine là "trái tim" của hệ thống — thành phần trung tâm chịu trách nhiệm khởi tạo, điều phối, giám sát và hủy bỏ workflow, đồng thời quản lý scheduling, trạng thái từng bước, retry và dependency giữa các bước.
> - **Ẩn dụ/so sánh:** Giống đài kiểm soát không lưu tại sân bay: điều phối từng chuyến bay (tác vụ) cất hạ cánh đúng đường băng, đúng thứ tự, và biết chính xác máy bay nào đang ở đâu.
> - **Vì sao quan trọng:** Đây là nơi gom toàn bộ kiến thức của các phần trước — patterns, pipeline, state machine, error recovery, observability — thành một engine dùng được trong thực tế.

Code dưới đây là một engine hoàn chỉnh ráp từ những mảnh đã học: nó nhận job, xếp hàng đợi, chọn cách chạy (tuần tự/song song/DAG), tự thử lại khi lỗi, và ghi số đo ở từng bước. Đây là chỗ các khái niệm ở trên đi vào hoạt động chung:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/12-6-workflow-orchestration-engine.py`](examples/12-6-workflow-orchestration-engine.py)

</details>

> **Tóm gọn 1 câu:** Orchestration engine = đài kiểm soát không lưu của workflow: khởi tạo, xếp lịch, giám sát và thử lại mọi tác vụ ở một nơi duy nhất.

---

## 7. Workflow Testing

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Testing là quy trình kiểm thử workflow trước khi chạy thật — unit test cho từng bước, integration test cho cả chuỗi, end-to-end test cho toàn bộ luồng — để chắc chắn các bước nối nhau đúng và lỗi được xử lý như mong đợi.
> - **Ẩn dụ/so sánh:** Giống chạy thử dây chuyền sản xuất bằng hàng giả: chỉ cần một khâu kẹt là biết ngay chỗ nào hỏng, mà không tốn tiền hàng thật.
> - **Vì sao quan trọng:** Workflow càng phức tạp thì lỗi nối các bước càng khó tìm; kiểm thử đàng hoàng giúp phát hiện lỗi trước khi nó làm hỏng hệ thống thật.

*Giải nghĩa các loại test:* **unit test** = test riêng từng bước nhỏ; **integration test** = test mấy bước nối nhau có ăn khớp không; **end-to-end test** = chạy trọn vẹn cả luồng từ đầu tới cuối; **chaos testing** = cố tình phá (ngắt mạng, kill process) để xem workflow có đứng vững không. Code dưới đây minh họa cách test workflow ở cả ba mức đầu:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/13-7-workflow-testing.py`](examples/13-7-workflow-testing.py)

</details>

> **Tóm gọn 1 câu:** Test workflow theo ba tầng — từng bước, chuỗi bước, cả luồng — để bắt lỗi nối bước trước khi nó đánh sập hệ thống thật.

---

## 8. Harness Integration

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Harness Integration là lớp kết nối Workflow module với toàn bộ Harness Framework — Memory, Guardrails, Tool Execution, Feedback — thông qua các interface thống nhất để các module trao đổi với nhau bằng một "ngôn ngữ" chung.
> - **Ẩn dụ/so sánh:** Giống ổ cắm điện chuẩn quốc tế: bất kỳ thiết bị (module) nào cắm vào cũng vừa khớp và hoạt động, miễn là tuân theo chuẩn interface.
> - **Vì sao quan trọng:** Không có interface chuẩn, mỗi module tự bịa cách gọi riêng — tích hợp thành mớ dây nhợ rối và khó bảo trì.

### 8.1 TypeScript Interfaces

**Mục này giải thích "hợp đồng" giữa workflow engine và các module khác của harness.**

Đây là "hợp đồng" giữa Workflow module và phần còn lại của Harness framework — khai báo các method chuẩn như createWorkflow (tạo workflow mới), execute (chạy), pause (tạm dừng), resume (chạy tiếp), cancel (huỷ), getTrace (lấy dấu vết chạy), getMetrics (lấy số đo) để ai cũng biết engine cung cấp gì và dùng như thế nào:

<details>
<summary><b>8.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/14-8-1-typescript-interfaces.ts`](examples/14-8-1-typescript-interfaces.ts)

</details>

> **Tóm gọn 1 câu:** Interface TypeScript = hợp đồng công khai các lệnh tạo/chạy/dừng/doi lược của engine, để mọi module cắm vào đều khớp.

---

## 9. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Case Studies là những phân tích thực tế về cách các hệ thống lớn (GitHub Actions, Apache Airflow, Temporal, DeepSeek Harness) thiết kế workflow, để rút ra bài học áp dụng vào dự án của bạn.
> - **Ẩn dụ/so sánh:** Giống xem phim tài liệu rồi rút kinh nghiệm: thay vì tự lăn vào vết xe đổ, bạn học ngay từ cách người đi trước đã giải quyết vấn đề.
> - **Vì sao quan trọng:** Lý thuyết suông khó hình dung; học từ hệ thống thật giúp bạn biết pattern nào hiệu quả trong điều kiện sản xuất.

### 9.1. GitHub Actions — Event-Driven CI/CD

**Mục này phân tích một hệ thống thật bạn dùng hằng ngày để xem event-driven + DAG ra sao.**

Ví dụ gần gũi với hầu hết developer: một file YAML (định dạng file cấu hình viết bằng thụt dòng) mô tả CI/CD (Continuous Integration/Continuous Deployment = tự động build, test, và triển khai mỗi khi có code mới) chạy khi có push hoặc pull request. Bạn sẽ thấy ngay event-driven trigger (dòng `on:` = khai báo sự kiện nào kích hoạt pipeline) kết hợp dependency giữa các job — deploy phải chờ build, build phải chờ lint (kiểm tra style code) và test:

<details>
<summary><b>9.1. GitHub Actions — Event-Driven CI/CD (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/15-9-1-github-actions-event-driven-ci-cd.yaml`](examples/15-9-1-github-actions-event-driven-ci-cd.yaml)

</details>

**Bài học rút ra**: GitHub Actions chạy workflow theo kiểu DAG — việc nào phụ thuộc việc nào được giải quyết rõ ràng, và mọi thứ bắt đầu từ sự kiện (event triggers).

### 9.2. Apache Airflow — Data Pipeline Orchestration

Airflow nổi tiếng với cách khai báo pipeline bằng DAG trong Python chỉ vài dòng: khai báo các task (extract = lấy dữ liệu từ nguồn, transform = biến đổi, load = nạp vào đích, validate = kiểm tra chất lượng) rồi dùng toán tử >> để nối thứ tự (extract >> transform >> load = làm xong extract mới tới transform). Cách này khiến toàn bộ quy trình hiện rõ như một bản đồ và dễ đổi thứ tự:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/16-9-2-apache-airflow-data-pipeline-orchestration.py`](examples/16-9-2-apache-airflow-data-pipeline-orchestration.py)

</details>

**Bài học rút ra**: Airflow chứng minh rằng workflow kiểu DAG — task nào phụ thuộc task nào viết ra thật rõ — là chuẩn vàng cho data pipeline.

> **Tóm gọn 1 câu:** Airflow = khai báo pipeline thành DAG vài dòng Python, bản đồ phụ thuộc hiện rõ và dễ đổi thứ tự.

### 9.3. Temporal — Durable Workflow Execution

Điểm mấu chốt của Temporal: workflow phải "sống sót" ngay cả khi server crash — trạng thái được lưu bền vững (durable = cất xuống đĩa, không mất khi process chết) và tự động retry, kèm compensation. Ví dụ dưới đây là flow đặt hàng theo kiểu Saga: giữ hàng → thu tiền → gửi hàng; nếu bước gửi hàng fail thì huỷ ngược lại. *Đọc pseudo-code:* bước 3 fail → chạy ngược từ 2 về 1: hoàn tiền (RefundPayment) rồi trả hàng kho (ReleaseInventory):

```
Temporal pattern: Saga with compensating transactions

Workflow:
  1. ReserveInventory() → success
  2. ChargePayment() → success
  3. ShipOrder() → FAIL
  
Compensation (reverse):
  2. RefundPayment()
  1. ReleaseInventory()
```

**Bài học rút ra**: ý tưởng cốt lõi của Temporal là workflow phải sống sót qua cả crash — nhờ lưu trạng thái bền vững (durable state), tự động thử lại, và có bước bù (compensation) khi cần.

> **Tóm gọn 1 câu:** Temporal = workflow sống sót qua crash nhờ lưu trạng thái ra đĩa, tự retry, và có bước bù khi cần cuộn ngược.

---

### 9.4. DeepSeek Harness — Cordis Micro-Kernel Plugin Architecture

**Mục này phân tích một kiến trúc khác biệt: thay vì một framework to, mọi thứ đều là plugin cắm vào kernel nhỏ.**

**Bối cảnh**: DeepSeek Harness dùng **Cordis** — một micro-kernel cắm plugin được xây theo triết lý **"Agent = Model + Harness"** và **"cái gì cũng là plugin"**. Cordis là một kernel rất nhẹ (core nén lại chỉ ~2KB), lo toàn bộ vòng đời của agent thông qua hệ plugin, còn việc tìm nhau giữa các plugin thì nhờ Context — một chỗ đăng ký service chung (service registry) để inject dependency.

Nói cho dễ hình dung: kernel giống một hệ điều hành tí hon, còn các plugin giống những app cài thêm vào đó — mỗi app chỉ cần khai báo "tôi cần xài dịch vụ gì" (consumes) và "tôi cung cấp dịch vụ gì" (provides), hệ điều hành sẽ tự lo phần nối dây để các app chạy đúng thứ tự.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts`](examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts)

</details>

**Những điểm hay nhất trong kiến trúc này**:

1. ✅ **Thiết kế micro-kernel** — kernel chỉ ~2KB (lõi hệ thống siêu nhẹ), mọi chức năng đều là plugin. Cần gì load nấy, thay nóng (hot-reload = thay plugin khi hệ thống vẫn đang chạy) được.

2. ✅ **Quản lý vòng đời rõ ràng** — 4 chặng: `init` → `attach` → `ready` → `detach` (khởi tạo → cắm vào hệ thống → sẵn sàng chạy → rút ra). Khởi động và tắt máy theo trình tự cố định, đoán được.

3. ✅ **Chỗ đăng ký service qua Context** — muốn chia sẻ thì `ctx.provide()` (đăng ký "tôi cung cấp dịch vụ này"), muốn xài thì `ctx.inject()` / `ctx.get()` (xin dùng dịch vụ đó). Plugin khai báo `provides`/`consumes` (cung cấp/tiêu thụ) là tự nối dây (auto-wiring), khỏi tự tay trỏ vào nhau.

4. ✅ **Event bus** (bus sự kiện = đường phát tin chung) — các plugin nói chuyện với nhau kiểu pub/sub (publish/subscribe = ai phát tin không cần biết ai nghe). Nhờ vậy plugin này không cần biết plugin kia, muốn mở rộng cũng dễ.

4. ✅ **4 chế độ chạy (runtime modes)** (do plugin `runtime-mode` cung cấp):
   - **Standard** — agent đầy đủ, xài mọi tool, cách ly ở mức process
   - **Code** — SDK `@deepseek-ai/dsh`, chạy script gói gọn trong một lượt, gom batch, sandbox kiểu VM, giảm độ trễ 70-90%
   - **Benchmark** — gọn nhẹ (chỉ có bash + editor), cách ly bằng container, chạy ổn định để chấm SWE-bench
   - **Creator** — có timeline trực quan, preset sẵn, debug kiểu du hành thời gian (time-travel = xem lại đúng trạng thái từng thời điểm trong quá khứ), fork/replay

5. ✅ **Ghi vết hành trình (trajectory)** (do plugin `trajectory-recorder` lo):
   - Luồng event của session, chỉ ghi thêm (append-only = chỉ được ghi vào cuối, không sửa không xoá)
   - Có `replayToStep()` (xem lại tới một bước), `forkSession()` (nhân đôi session thành nhánh mới), `resumeSession()` (chạy tiếp session cũ)
   - Tìm event theo loại, theo thời gian, theo bước

6. ✅ **Ráp harness bằng cách ghép plugin** — DeepSeek Harness thực chất là nhiều plugin ghép lại. Muốn thay, muốn thêm, muốn test riêng từng mảnh đều dễ.

**So sánh Cordis với framework truyền thống**:

*Cách đọc bảng này: mỗi dòng so sánh một khía cạnh giữa cách làm của LangGraph/AutoGen (framework truyền thống) và Cordis. Ví dụ dòng "Hot Reload": framework cũ khó thay nóng, còn Cordis làm được nhờ rút plugin ra rồi cắm lại.*

| Aspect | LangGraph / AutoGen | Cordis (DeepSeek Harness) |
|--------|---------------------|---------------------------|
| **Architecture** | Framework-specific | Micro-kernel + Plugins |
| **Extensibility** | Subclass/override | Register plugin |
| **Dependency Injection** | Manual/prop drilling | `ctx.provide` / `ctx.inject` |
| **Lifecycle** | Implicit | Explicit: init→attach→ready→detach |
| **Hot Reload** | Difficult | Native (detach + attach) |
| **Size** | Heavy (~MB) | ~2KB kernel |
| **Runtime Modes** | Single | 4 distinct modes |
| **Trajectory** | External logging | Built-in plugin |

*Giải nghĩa từng dòng:* **Extensibility** = mức độ dễ mở rộng — framework cũ phải kế thừa (subclass) rồi ghi đè, Cordis chỉ cần đăng ký plugin. **Dependency Injection** = cách ném đối tượng cần vào cho module dùng — framework cũ phải truyền tay từng tầng (prop drilling), Cordis có `ctx` chung. **Lifecycle** = vòng đời — framework cũ ngầm định (implicit), Cordis công bố rõ 4 chặng. **Trajectory** = vết ghi hành trình agent.

**Đọc thêm code chi tiết**: xem [`cordis-kernel-plugin.md`](cordis-kernel-plugin.md)

> **Tóm gọn 1 câu:** Cordis cho thấy agent harness có thể là kernel 2KB cộng nhiều plugin tự nối dây — thay gì, thêm gì cũng dễ, vòng đời rõ ràng.

---

## 10. Design Principles

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Design Principles là bộ chỉ dẫn kiến trúc (gồm nguyên lý SOLID) áp dụng riêng cho workflow — giúp bạn quyết định cách chia bước, tổ chức dependency và đặt biên giới trách nhiệm trong hệ thống.
> - **Ẩn dụ/so sánh:** Giống luật xây nhà: không ai cấm xây, nhưng tuân theo quy chuẩn thì nhà an toàn, dễ sửa và không phải đập đi xây lại.
> - **Vì sao quan trọng:** Nguyên tắc tốt khiến workflow dễ mở rộng, dễ test và ít nợ kỹ thuật khi hệ thống lớn dần.

### 10.1 SOLID Cho Workflows

**Mục này giải thích 5 nguyên lý SOLID — bộ luật kinh điển cho code dễ mở rộng — áp vào từng bước workflow.**

**1. Single Responsibility (mỗi bước một việc)**
- Mỗi step chỉ làm đúng một việc, tên gọi là hiểu ngay
- Đừng nhét cả parse + validate + transform vào chung một step

**2. Open/Closed (dễ thêm, ngại sửa)**
- Muốn thêm step mới thì cứ thêm vào, workflow vẫn chạy
- Hạn chế đụng chạm logic cũ đang chạy ổn

**3. Liskov Substitution (thay được cho nhau)**
- Step A thay bằng step B vẫn chạy, miễn là cùng interface (đầu vào/đầu ra giống nhau)
- Các nhánh rẽ (conditional branches) cũng đổi qua lại được

**4. Interface Segregation (ai cần gì cho nấy)**
- Đầu vào/đầu ra của từng step tách bạch, theo schema riêng (schema = bản mô tả dữ liệu có những cột gì, kiểu gì)
- Đừng xài chung một cục state mà bước nào cũng sửa được

**5. Dependency Inversion (phụ thuộc vào trừu tượng)**
- Workflow engine chỉ biết tới cái khung chung (Step abstraction = "khuôn" chung định nghĩa mọi step đều có input/output)
- Đừng viết cứng (hardcode = chôn luôn trong code, đổi là phải sửa engine) cách làm cụ thể của từng step vào engine

### 10.2 6 Design Principles

**Mục này là 6 nguyên tắc "kim chỉ nam" khi thiết kế bất kỳ workflow nào.**

Sáu nguyên tắc dưới đây là "kim chỉ nam" khi thiết kế bất kỳ workflow nào — từ việc chạy lại an toàn (idempotency) đến lưu trạng thái ra ngoài bộ nhớ (state externalization) để có thể resume từ checkpoint:

```
┌──────────────────────────────────────────────────────────────────┐
│                 WORKFLOW DESIGN PRINCIPLES                        │
│                                                                  │
│  1. IDEMPOTENCY                                                  │
│     Mỗi bước phải an toàn khi chạy lại nhiều lần              │
│     → Dùng UUID/idempotency key cho mutations                   │
│                                                                  │
│  2. OBSERVABILITY                                                │
│     Mọi bước phải log input/output + metrics                    │
│     → Dùng structured logging + distributed tracing             │
│                                                                  │
│  3. SEPARATION OF CONCERNS                                       │
│     Mỗi bước làm 1 việc duy nhất                               │
│     → Dễ test, dễ thay thế, dễ debug                           │
│                                                                  │
│  4. PROGRESSIVE DISCLOSURE                                       │
│     Bắt đầu đơn giản, thêm complexity khi cần                  │
│     → Sequential trước, Parallel khi bottleneck                  │
│                                                                  │
│  5. FAIL-FAST + RECOVER                                          │
│     Phát hiện lỗi sớm, có strategy recovery                     │
│     → Retry + Circuit Breaker + Saga pattern                     │
│                                                                  │
│  6. STATE EXTERNALIZATION                                        │
│     Lưu state ra ngoài memory                                   │
│     → Có thể resume từ checkpoint                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

*Giải nghĩa các nguyên tắc trong sơ đồ:* **Idempotency** = chạy lại nhiều lần vẫn cho kết quả như chạy một lần (ví dụ gắn UUID — mã định danh duy nhất — cho mỗi lượt ghi, ghi trùng thì bỏ qua). **Fail-fast** = lỗi thì báo ngay chứ không để trôi tới bước sau. **State externalization** = cất trạng thái ra ngoài bộ nhớ của process (file, database), nên process chết cũng không mất.

---

## 11. Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Best Practices là danh sách việc nên làm (DO) và không nên làm (DON'T) được đúc kết từ kinh nghiệm thực tiễn khi xây dựng workflow cho AI Agent.
> - **Ẩn dụ/so sánh:** Giống checklist của phi công trước khi cất cánh: ai cũng thuộc lòng, nhưng cứ ghi ra để kiểm tra tuần tự mới chắc ăn, tránh quên việc nhỏ gây hậu quả lớn.
> - **Vì sao quan trọng:** Đây là "bản đồ tránh bẫy" — làm đúng thì ít đau đầu, làm sai thì tự chuốc lỗi khó debug.

### 11.1 DO ✅

- **Viết rõ đầu vào/đầu ra cho từng bước**: test và debug đỡ cực hẳn
- **Ghi log có cấu trúc ở mọi bước**: log dạng JSON kèm thời gian để dễ lọc
- **Thử lại với backoff tăng dần**: lỗi thoáng qua (transient failures) thì chờ rồi thử lại, đừng bỏ cuộc ngay
- **Dùng circuit breaker cho service bên ngoài**: một chỗ sập thì ngắt ra, đừng để sập cả dây chuyền
- **Thiết kế sao cho chạy lại an toàn (idempotency)**: chạy lại bước nào cũng không gây tác dụng phụ
- **Đặt timeout cho mọi bước**: bước nào cũng phải có giới hạn thời gian, tránh treo
- **Giao dịch phân tán thì dùng saga**: bước nào fail thì có bước bù (compensate) để cuộn ngược
- **Theo dõi metrics**: độ trễ, tỷ lệ thành công, tỷ lệ lỗi — tính theo từng bước
- **Kiểm tra cấu trúc DAG trước khi chạy**: phát hiện vòng lặp (cycle) từ sớm
- **Có checkpoint**: lưu điểm đã xong để lỗi thì chạy tiếp từ đó, khỏi chạy lại từ đầu

> **Tóm gọn 1 câu:** Nên làm: mỗi bước một việc, log JSON, retry có backoff, timeout, checkpoint, và saga cho giao dịch nhiều bước.

### 11.2 DON'T ❌

- **Đừng xài chung state sửa được (mutable) giữa các bước**: truyền dữ liệu kiểu bất biến (immutable) từ bước này sang bước kia
- **Đừng bỏ qua xử lý lỗi**: bước nào cũng có thể fail, nên chừa đường lui
- **Đừng để vòng lặp vô hạn**: lúc nào cũng đặt số lần lặp tối đa (max iterations)
- **Đừng bơ timeout**: một bước treo là cả workflow đứng hình
- **Đừng viết cứng quan hệ phụ thuộc giữa các bước**: khai báo bằng cấu hình DAG cho dễ đổi
- **Đừng bỏ qua testing**: test riêng từng bước một cách độc lập
- **Đừng gọi blocking trong các bước chạy song song**: dùng async/executor để không nghẽn nhau
- **Đừng quên logic bù (compensation)**: việc nào tiến tới được thì cũng phải có đường lui (rollback = hoàn tác về trạng thái trước đó)

> **Tóm gọn 1 câu:** Không nên làm: chia sẻ state sửa được, bỏ xử lý lỗi, thiếu timeout, và viết cứng phụ thuộc — bốn thói quen sinh lỗi khó debug nhất.

---

## 12. Tương Lai

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Phần Tương Lai phác thảo các xu hướng workflow orchestration và agent pipelines giai đoạn 2026-2028 — workflow tự sinh bởi AI, serverless engines, chạy đa nền tảng, và workflows thích ứng theo thời gian thực.
> - **Ẩn dụ/so sánh:** Giống xem dự báo thời tiết tuần tới: không chắc 100%, nhưng đủ định hướng để bạn chọn kiến trúc không lỗi thời sau hai năm nữa.
> - **Vì sao quan trọng:** Nắm xu hướng giúp bạn đầu tư đúng công nghệ, tránh xây thứ sắp bị thay thế.

### 12.1 Xu Hướng 2026-2028

**1. Workflow do AI tự sinh**
- Agent đọc mô tả task rồi tự vẽ ra workflow
- Tự tối ưu cấu trúc workflow dựa trên lịch sử chạy trước đó
- Workflow tự chữa (self-healing) khi gặp lỗi quen thuộc

**2. Engine chạy kiểu serverless**
- Viết workflow như viết code (workflow-as-code), khỏi lo hạ tầng
- Mỗi bước tự co giãn (auto-scaling) theo tải
- Trả tiền theo lượt chạy (pay-per-execution)

**3. Workflow mang đi đâu cũng chạy**
- Có định dạng workflow chuẩn chung (kiểu CNCF WASM?)
- Mang qua lại giữa Temporal, Airflow, Step Functions đều được
- Có chợ (marketplace) chia sẻ workflow dùng chung

**4. Workflow tự thích ứng theo thời gian thực**
- Tự chỉnh bước đi dựa trên metrics lúc đang chạy
- Dùng ML để đoán trước chỗ nghẽn (bottleneck)
- Tự tách bước nặng ra chạy song song (auto-parallelization)

**5. Quan sát workflow kiểu 2.0**
- AI tự tìm nguyên nhân gốc (root cause) khi có lỗi
- Cảnh báo trước khi sự cố xảy ra (predictive alerting)
- Tự xử lý sự cố thường gặp (automated incident response)

> **Tóm gọn 1 câu:** Workflow tương lai sẽ tự sinh, tự chữa, chạy kiểu serverless và mang đi đâu cũng được — thiết kế lỏng lẻo hôm nay để đỡ phải xây lại.

---

## 13. Độ Bền Production: Checkpoint-Resume, Idempotency, Backpressure, Approvals

**Mục này nói về cách giữ workflow sống sót khi chạy thật ở quy mô lớn: có điểm lưu để chạy tiếp, không bị trùng lặp khi chạy lại, không quá tải, và có bước xin người duyệt khi cần.**

### 13.1 Định Nghĩa

*Cách đọc bảng này: mỗi dòng là một thuật ngữ cốt lõi của "workflow bền" kèm ý nghĩa của nó. Ví dụ dòng 2: idempotency key là "chìa khoá chống trùng" — chạy lại bước đã chạy vẫn không gây tác dụng phụ kép.*

| Thuật Ngữ | Định Nghĩa |
|------|------------|
| Durable execution | Mỗi step hoàn thành đều được checkpoint (event log + snapshot); khởi động lại sẽ tiếp tục từ checkpoint cuối cùng, không bao giờ chạy lại từ đầu |
| Idempotency key | `stepId + inputHash (+ attempt ceiling)`; thực thi lại với cùng key trả về kết quả đã lưu, không gây tác dụng phụ kép |
| Backpressure | Hàng đợi giới hạn + semaphore (`maxParallel`), deadline của mỗi run được lan truyền qua `AbortSignal`/ctx; giảm tải hoặc hoãn lại thay vì OOM |
| Approval node | Step có trạng thái `WAITING_APPROVAL`; engine tạm dừng, lưu trạng thái, tiếp tục khi được phê duyệt/từ chối/hết thời gian |

*Giải nghĩa các ký hiệu trong bảng:* `stepId` = tên định danh của bước; `inputHash` = "vân tay" của dữ liệu đầu vào (hash = dãy ký tự sinh ra từ dữ liệu, dữ liệu đổi một chữ là vân tay đổi); `semaphore` = đồng hồ đếm giới hạn số việc chạy đồng thời; `OOM` = Out Of Memory, hết RAM mà gục; `AbortSignal` = tín hiệu hủy — bước nào cầm nó sẽ tự dừng khi hết hạn.

### 13.2 Checkpoint-Resume (Tiếp Tục Sau Khi Khởi Động Lại)

**Mục này giải thích cơ chế "chốt sổ" để workflow chết giữa chừng vẫn chạy tiếp từ chỗ dở, không làm lại từ đầu.**

Hãy hình dung mỗi step làm xong là mình "chốt sổ" một dòng: ghi log trước đã (`append({seq, stepId, inputHash, status, outputRef})` — gọi là write-ahead log), rồi cứ mỗi N step lại chụp một tấm snapshot nguyên tử. Khi khởi động lại, engine làm đúng 4 việc theo thứ tự: `load snapshot → replay log tail → skip completed (idempotent) → resume pending` — tức nạp snapshot, chạy lại phần đuôi log, step nào xong rồi thì bỏ qua (nhờ idempotent), step nào còn dở thì chạy tiếp. Snapshot cất ở JSON/SQLite ngay trên máy; output nào to hơn 64KB thì không nhét vào log mà gửi ra artifact store, trong log chỉ giữ ref. Và nhớ giữ `runId` cố định qua mọi lần khởi động lại, đừng đổi.

### 13.3 Idempotency + Backpressure + Deadline Theo Từng Step

**Mục này là "bộ ba sống còn" khi chạy thật: chống trùng lặp, chống quá tải, và chống treo vô hạn.**

Về idempotency: có một kho `Map<idempotencyKey, resultRef>` kèm TTL — cứ thao tác ghi (mutation) là bắt buộc phải có key, còn thao tác đọc thì khỏi cần. Về backpressure (chống quá tải): đặt một `Semaphore(maxParallel=4–8)` chung cho toàn engine, mỗi step giới hạn độ dài hàng đợi (ví dụ 100); khi hàng đợi đầy, `enqueue` sẽ ném `BackpressureError` — bên gọi cứ retry kèm jitter là được. Về deadline: mỗi run chỉ có một `deadlineAt` duy nhất; step nào cũng nhận `remaining = deadlineAt - now()` (đã trừ buffer hao hụt), rồi lan truyền xuống qua `AbortSignal.timeout(remaining)`. Nguyên tắc sắt: không bao giờ âm thầm nới deadline.

### 13.4 Node Phê Duyệt / Tạm Dừng-Tiếp Tục Của Con Người

**Mục này giải thích cách dừng workflow để xin con người phê duyệt, rồi chạy tiếp mà không mất trạng thái.**

**Mục này sở hữu *cơ chế* checkpoint; chính sách cổng thuộc
[`15-approval-gates`](../15-approval-gates/README.md).** Engine bên dưới cung cấp
*cơ chế*: một lệnh `PAUSED:` có kiểu được ném sau khi đã ghi checkpoint bền, một write-ahead
log, một idempotency store, và trạng thái `WAITING_APPROVAL` sống sót qua cái chết của
process. Nó **không** quyết định bước nào *cần* con người, hay người duyệt được thấy những
gì. Những thứ đó nằm ở `15`: taxonomy risk tier và TTL, payload bắt buộc có bằng chứng,
timeout-deny (fail closed), luật hai-người, và audit trail `approval_request` /
`approval_verdict`. Hợp đồng thứ tự của giao thức — checkpoint trước, ném sau; "duyệt" của
con người là *truyền phán quyết*, không phải khởi động lại — được viết ra ở `15` §5.2.

Hãy hiểu `needsApproval?: boolean` bên dưới là đường ghép: `07` đưa run sang
`WAITING_APPROVAL` rồi ném; `15` quyết định ai giải quyết nó và chuyện gì xảy ra khi hết hạn.
Một `true` ở đây không có nghĩa là "hỏi ai đó", mà là "hỏi Gatekeeper".

<details>
<summary>TypeScript Code — Durable Engine (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/18-13-4-node-phe-duyet-tam-dung-tiep.ts`](examples/18-13-4-node-phe-duyet-tam-dung-tiep.ts)

</details>

Muốn chạy tiếp (resume): gọi lại `run()` với đúng `runId` cũ (mã định danh của lượt chạy) — key nào đã xong (trúng `done()`/store) sẽ tự được bỏ qua. Muốn tạm dừng (pause): bắt lỗi `PAUSED:*`, lưu trạng thái lên UI, đợi phê duyệt xong rồi chạy lại.

> **Tóm gọn 1 câu:** Node phê duyệt = dừng lại có lưu trạng thái: xin xong thì chạy tiếp từ đúng chỗ, không mất gì và không chạy lại phần đã xong.

### 13.5 Checklist

- [ ] Đã checkpoint sau mỗi step (log + snapshot) chưa; đã thử kill -9 giữa run rồi chạy lại mà vẫn đạt chưa?
- [ ] Step nào ghi dữ liệu cũng có idempotency key chưa; chạy trùng hai lần cũng không gây tác dụng phụ chứ?
- [ ] Đã đặt `maxParallel` + giới hạn độ dài hàng đợi chưa; deadline đã lan truyền tới signal của mọi step chưa?
- [ ] Node phê duyệt đã lưu trạng thái `WAITING_APPROVAL` chưa; các nhánh approve/reject/timeout đều chạy tiếp đúng chứ?

> **Tóm gọn 1 câu:** Workflow production bền = checkpoint sau mỗi bước, chạy lại không trùng lặp, giới hạn tải và deadline rõ, và dừng xin duyệt khi cần mà không mất trạng thái.

---

## Tài Liệu Tham Khảo

### Papers & Research

1. **Temporal: Durable Execution**
   - https://docs.temporal.io
   - Durable workflow execution with automatic retry and compensation

2. **Apache Airflow Documentation**
   - https://airflow.apache.org/docs/
   - DAG-based workflow orchestration

3. **Microservices Patterns**
   - Chris Richardson, 2018
   - Saga pattern, CQRS, Event Sourcing

4. **Designing Data-Intensive Applications**
   - Martin Kleppmann, 2017
   - Pipeline design, distributed systems patterns

### Frameworks

1. **Temporal** - https://temporal.io
2. **Apache Airflow** - https://airflow.apache.org
3. **Prefect** - https://www.prefect.io
4. **GitHub Actions** - https://docs.github.com/en/actions
5. **AWS Step Functions** - https://aws.amazon.com/step-functions/

---

> **Phụ lục Oct-2026:** muốn đặt "bảo vệ ở các cửa" cho agent thì đọc
> [`hooks-standard.md`](./hooks-standard.md) nhé. Nôm na là mỗi mốc vòng đời
> (`preToolUse`, `postToolUse`...) gắn một script kiểm tra: cho qua, hỏi người, hay cấm hẳn.

---

## Cập nhật 10/2026 — Production Reliability Patterns (Anthropic 2025)

> **📌 Bối cảnh:** Ba pattern dưới đây tổng hợp từ bài *Effective Harnesses for Long-Running Agents* (Anthropic, 2025) — dành cho lúc agent không còn là demo 5 phút mà là hệ thống production chạy hàng giờ, deploy liên tục, và lỗi là chuyện đương nhiên.

### 1. Checkpoint & Resume (không restart)

Agents là **stateful** — trạng thái tích lũy qua từng bước, nên lỗi nhỏ có xu hướng **compounding**: một trượt nhỏ ở bước 3 tạo ra lỗi lớn ở bước 7. Khi lỗi xảy ra, đừng chạy lại từ đầu — **resume từ checkpoint gần nhất**:

*Cách đọc bảng này: mỗi dòng là một thành phần của cơ chế checkpoint-resume và vai trò của nó. Ví dụ dòng 1: checkpoint = điểm lưu trọn bộ trạng thái (kết quả, biến, tiến độ) sau mỗi bước xong.*

| Thành phần | Vai trò |
|---|---|
| **Checkpoint** | Mỗi step hoàn thành lưu state (outputs, biến, tiến độ) vào storage bền vững (file JSON, S3, DB) |
| **Resume** | Crash/timeout → load checkpoint gần nhất → bỏ qua step đã xong → chạy tiếp |
| **Retry/backoff deterministic** | Lỗi tạm thời (network, rate limit) → exponential backoff, giới hạn số lần |
| **Model adaptation** | Lỗi logic → **báo tool fail cho agent** để nó tự adapt (đổi approach) thay vì retry y nguyên |

*Giải nghĩa:* **rate limit** = service chặn vì gọi quá nhiều; **exponential backoff** = chờ gấp đôi mỗi lần thử lại (1s → 2s → 4s); **deterministic** = theo công thức cố định, đoán trước được.

Nguyên tắc phân loại: **deterministic problems dùng retry/backoff; những gì cần phán đoán thì đưa về cho model** — agent thấy được lỗi sẽ tự sửa chiến lược, máy móc retry mù quáng thì không.

> **Tóm gọn 1 câu:** Lỗi tạm thời thì máy tự retry với backoff; lỗi logic thì báo cho agent tự đổi cách làm — và luôn resume từ checkpoint chứ không chạy lại từ đầu.

### 2. Rainbow Deployments

**Mục này giải thích cách deploy version mới mà không cắt đứt agent đang chạy dở.**

Agents có thể **đang chạy giữa chừng** khi bạn deploy version mới — cắt ngang giữa chừng là mất trạng thái, hỏng task đang dở. Giải pháp: **chuyển traffic dần** từ version cũ sang version mới, giữ cả 2 chạy song song:

*Cách đọc bảng này: mỗi dòng là một giai đoạn chuyển đổi, các cột cho biết phần trăm task mới được giao cho version nào. Ví dụ giai đoạn 2: dần dần nới 20% → 80% task mới cho version mới, trong khi task cũ được chạy hết trên version cũ.*

| Giai đoạn | Version cũ | Version mới | Ghi chú |
|---|---|---|---|
| 1. Deploy song song | 100% | 0% | Version mới đứng chờ, sẵn sàng nhận task |
| 2. Chuyển dần | 80% → 50% → 20% | 20% → 50% → 80% | Task mới vào version mới; task cũ chạy hết lifecycle trên version cũ |
| 3. Hoàn tất | 0% | 100% | Tắt version cũ khi không còn task nào đang chạy trên nó |

Điểm mấu chốt: **không kill version cũ ngay** — agent đang chạy giữa chừng trên đó cần được hoàn thành trọn vẹn (drain = "rút cạn": đợi hết task đang chạy mới tắt). Tham khảo: **rainbow deploys trong Kubernetes** (Argo Rollouts, Flagger) — weighted routing giữa các version (phân % traffic theo trọng số).

> **Tóm gọn 1 câu:** Rainbow deploy = chuyển traffic dần dần sang version mới, đợi version cũ rút cạn task đang chạy rồi mới tắt.

### 3. Sync Bottleneck trong Orchestration

**Mục này so sánh hai cách điều phối subagent — đợi từng đứa (sync) hay giao xong là quên (async) — và cái giá phải trả của async.**

Chạy subagents **sync** (lead đợi từng subagent xong rồi mới giao việc tiếp) là mô hình đơn giản nhất — nhưng tạo bottleneck nghiêm trọng:

- Lead **không steer được** subagent giữa chừng: subagent đi lạc hướng thì cũng phải đợi nó chạy xong mới sửa được.
- Lead **blocked** khi 1 subagent chậm: cả hệ thống dừng theo subagent chậm nhất (waterfall effect).

**Async orchestration** giải quyết được throughput (lưu lượng xử lý được trong một đơn vị thời gian), nhưng phải trả lời 3 câu hỏi khó:

*Cách đọc bảng này: mỗi dòng là một vấn đề khi chạy subagent song song, câu hỏi cụ thể của nó, và hướng giải phổ biến. Ví dụ dòng 3: một subagent gục thì phải thông báo cho những subagent đang đợi nó, để chúng dừng đúng lúc.*

| Vấn đề | Câu hỏi | Hướng giải |
|---|---|---|
| **Result coordination** | Kết quả từ nhiều subagent về khi nào, gom thế nào? | Completion queue, callback, hoặc barrier sync |
| **State consistency** | Nhiều subagent viết chung state thì conflict thế nào? | Versioning, optimistic locking, hoặc tách vùng ghi |
| **Error propagation** | 1 subagent fail thì các subagent phụ thuộc biết không? | Cancellation tree + shared error bus |

*Giải nghĩa các hướng giải:* **completion queue** = hàng đợi gom kết quả, xong cái nào vào cái đó; **callback** = hàm được gọi ngược khi xong; **barrier sync** = rào chắn, đợi đủ tất cả mới đi tiếp; **optimistic locking** = cứ ghi, nếu phát hiện người khác ghi trước thì làm lại; **cancellation tree** = cây huỷ — huỷ một nhánh thì những gì phụ thuộc nó tự huỷ theo; **shared error bus** = đường phát lỗi chung cho mọi subagent nghe.

Quy tắc thực dụng: **sync khi số subagent ít và task ngắn** (dễ debug); **async khi task dài, độc lập nhiều** (nhưng phải đầu tư vào 3 vấn đề trên ngay từ đầu, đừng để thành nợ kỹ thuật).

> **Tóm gọn 1 câu:** Sync dễ debug nhưng chậm vì đợi đứa chậm nhất; async nhanh nhưng phải tự lo gom kết quả, giữ state nhất quán và lan truyền lỗi.

### 4. Code Python — Workflow Runner với Checkpoint/Resume

Code dưới đây minh họa pattern: mỗi step hoàn thành lưu checkpoint (JSON), crash → resume từ checkpoint cuối, retry với exponential backoff, tối đa 3 lần:

> 📄 **Code ví dụ:** [`examples/19-4-code-python-workflow-runner-voi-checkpoint-resume.py`](examples/19-4-code-python-workflow-runner-voi-checkpoint-resume.py)

**Điểm mấu chốt trong code:**
- `_save()` chạy **ngay sau khi** mỗi step xong — checkpoint luôn mới nhất, crash ở bước nào thì lần sau chỉ lặp lại đúng bước đó.
- `run_id` cố định giúp nhiều lần chạy lại cùng một task **gộp chung checkpoint** — đây chính là resume.
- Retry **deterministic** (backoff cố định công thức) cho lỗi tạm thời; khi hết lượt, ném exception lên để **agent nhận biết và adapt** (đổi cách làm) chứ không retry vô hạn.

### 5. Cross-Reference

> 📎 **Liên quan:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 2** (Orchestration) + **Section 4.3** (Long-Running Agent Pattern). Xem thêm Section 4 (Error Recovery) ở trên cho retry/circuit breaker/saga — checkpoint/resume là lớp bổ sung, không thay thế.

> **Tóm gọn 1 câu:** Ba pattern trên — checkpoint/resume, rainbow deploy, async orchestration — là bộ ba sống còn khi agent chạy thật hàng giờ, không phải demo 5 phút.

---

*Tài liệu: VII. Workflow — HARNESS ENGINEERING EDITION*
*Ngày cập nhật: 26/10/2026*
*Tác giả: AI Knowledge Repository*