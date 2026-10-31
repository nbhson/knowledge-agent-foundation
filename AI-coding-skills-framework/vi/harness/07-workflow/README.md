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

Hãy tưởng tượng một **xưởng làm bánh mì** vào giờ cao điểm buổi sáng. Bột phải nhào rồi mới ủ, ủ đủ giờ mới nướng, nướng xong mới đóng gói đem bán. Nếu mỗi người thợ tự làm theo ý mình — người nướng khi bột chưa ủ, người đóng gói khi bánh còn sống — thì cả mẻ bánh hôm đó coi như bỏ.

**AI Agent không có Workflow cũng rối y như vậy.**

Nhiều bạn viết agent chỉ là **một chuỗi function gọi nối tiếp nhau** — không lưu trạng thái đang làm tới đâu, không có cách chữa cháy khi lỗi, không có điểm lưu để chạy tiếp. Task nhỏ thì còn chạy được. Nhưng task càng lớn — **chỉ cần lỗi một bước là phải chạy lại từ đầu, vừa mất thời gian vừa tốn tiền**.

**Giải pháp** chính là Workflow có cấu trúc — một cách tổ chức để quản lý **cả vòng đời** của task, từ lúc bắt đầu (trigger) tới lúc xong và rút kinh nghiệm (feedback), mà bước nào cũng **lưu vết được, lỗi có đường lui, và nhìn thấy đang chạy tới đâu**.

### Tại Sao Workflow Quan Trọng?

> *"Agent không có workflow giống như đầu bếp không có thực đơn — có nguyên liệu, có dụng cụ, nhưng món ra tùy hứng."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Google DeepMind (2025)** | Structured workflows giảm **45% task failure rate** trong multi-step coding agents |
| 2 | **Anthropic (2025)** | Workflow engine với retry + checkpoint giảm **70% data loss** khi agent gặp lỗi |
| 3 | **LangGraph Benchmark (2025)** | State machine workflows xử lý **3× complex tasks** tốt hơn simple sequential chains |

#### Triết lý cốt lõi:

```
Workflow = Trigger → Plan → Execute → Validate → Deploy → Feedback
```

Mỗi bước trong chuỗi đó đều phải có **quản lý trạng thái (state management)**, **cách xử lý khi lỗi (error recovery)**, và **cách theo dõi (observability)**. Workflow không chỉ là "xếp thứ tự các bước" — mà là cách lo cho **cả vòng đời** của một task.

**Hình dung cho dễ**: Workflow giống hệ thống giao thông trong thành phố — có đèn tín hiệu (guardrails), có tuyến đường vẽ sẵn (steps), có trung tâm điều phối (orchestrator), và có camera theo dõi (logging).

**Nếu bỏ qua Workflow**: agent làm việc lộn xộn, đang chạy mà lỗi là chịu chết không cứu được, không biết tiến độ tới đâu, và mỗi lần debug là một lần đau đầu.

## Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow là cách sắp xếp các bước thực hiện của AI Agent thành một kế hoạch rõ ràng — bước nào trước, bước nào sau, lỗi xử lý ra sao — để một tác vụ phức tạp được hoàn thành đúng trình tự và an toàn.
> - **Ẩn dụ/so sánh:** Giống bếp nhà hàng: đầu bếp (agent) có nguyên liệu tốt vẫn cần thực đơn và quy trình trực (workflow) để ra món đúng giờ, đúng chất lượng mỗi lần.
> - **Vì sao quan trọng:** Không có workflow, agent làm việc theo cảm hứng — vừa chậm, vừa khó lặp lại kết quả, và hỏng giữa chừng là phải làm lại từ đầu.

**Workflow** là cách **sắp xếp các bước làm việc** để hoàn thành một task coding phức tạp. Trong Harness Engineering, Workflow Engine đóng vai trò **"người điều phối chính"** — lo toàn bộ hành trình từ trigger → plan → execute → validate → deploy, kèm theo theo dõi (observability), xử lý lỗi (error recovery), và quản lý trạng thái (state management).

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

---

## 1. Workflow Patterns

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Patterns là các "khuôn mẫu" tổ chức chuỗi hoạt động của AI Agent — chạy tuần tự (sequential), chạy song song (parallel), rẽ nhánh theo điều kiện (conditional branching) — nhằm đạt mục tiêu nhiệm vụ một cách có kiểm soát.
> - **Ẩn dụ/so sánh:** Giống đường đi trong thành phố: một con đường thẳng (sequential), nhiều làn chạy đồng thời (parallel), hay giao lộ rẽ hướng tuỳ biển báo (conditional branching).
> - **Vì sao quan trọng:** Chọn đúng pattern quyết định tốc độ, độ phức tạp và khả năng chịu lỗi của cả workflow.

### 1.1 Sequential Workflow (Tuần Tự)

Giống nấu một món ăn theo công thức: làm xong bước 1 mới sang bước 2, không được bỏ qua, không lộn thứ tự. Đây là pattern đơn giản nhất — dễ viết, dễ debug, nhưng hơi chậm vì mọi bước nối đuôi nhau. Dùng khi bước sau bắt buộc phải phụ thuộc vào kết quả bước trước. Diagram dưới đây minh hoạ luồng 5 bước Parse → Analyze → Build → Test → Deploy:

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

### 1.2 Parallel Workflow (Song Song)

Giống nấu bữa tiệc với nhiều trợ lý: cùng lúc người rửa rau, người nấu cơm, người chiên thịt — xong tất cả mới gom lại dọn bàn. Pattern này chạy nhanh vì nhiều bước cùng lúc, nhưng phần khó nằm ở chỗ gộp (fan-in) kết quả về. Dùng khi các bước độc lập với nhau, không cần chờ nhau:

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

### 1.3 DAG Workflow (Directed Acyclic Graph)

Giống lịch thi đấu giải thể thao: trận bán kết phải chờ đủ hai trận tứ kết, nhưng hai trận tứ kết lại diễn ra song song. DAG là pattern linh hoạt nhất — mỗi node chỉ chạy sau khi các node nó phụ thuộc (dependency) hoàn thành, hết "tầng" này rồi mới sang "tầng" kia, và tuyệt đối không có vòng lặp. Ví dụ dưới đây: A và B chạy song song → C chờ A, D chờ B → E chờ C, F chờ D:

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

### 1.4 Event-Driven Workflow

Giống trung tâm báo cháy: chuông reo (event) ở đâu thì đội ứng trực (handler) phản hồi ở đó, và mỗi phản hồi có thể kích ra một báo động mới. Khác với các pattern trên, luồng không được định sẵn từ đầu — workflow phản ứng theo từng sự kiện nảy sinh, nên rất linh hoạt với hệ thống bất định:

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

---

## 2. Pipeline Design

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Pipeline Design là cách chia một tác vụ lớn thành nhiều giai đoạn (stages) nối tiếp nhau; mỗi giai đoạn nhận dữ liệu từ giai đoạn trước, xử lý rồi chuyển tiếp cho giai đoạn sau, kèm khả năng rẽ nhánh (branching) và fan-out/fan-in.
> - **Ẩn dụ/so sánh:** Giống dây chuyền nhà máy bia: nghiền → nấu → lọc → lên men → đóng chai; mỗi công đoạn nhận đầu ra của công đoạn trước, và có ngã rẽ nếu khách đặt loại bia khác.
> - **Vì sao quan trọng:** Pipeline giúp xử lý dữ liệu lớn gọn gàng, kiểm tra được từng khâu và dễ đổi mới khi nghiệp vụ thay đổi.

### 2.1 Data Pipeline với Branching

Đây là "dây chuyền làm việc" cho dữ liệu: mỗi khâu là một stage (transform, filter, branch, fan_out, validator, sink), dữ liệu chảy qua từng khâu như sản phẩm qua từng công đoạn. Điểm đặc biệt là branching — một khâu kiểm tra điều kiện rồi rẽ dữ liệu sang hai nhánh khác nhau, như băng chuyền có chốt chuyển hướng hàng. Code bên dưới cho thấy cách ráp và chạy một pipeline đầy đủ:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-2-1-data-pipeline-voi-branching.py`](examples/05-2-1-data-pipeline-voi-branching.py)

</details>

---

## 3. State Machine

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** State Machine là "máy trạng thái" — mô hình ghi lại Agent đang ở trạng thái nào (đang đọc code, đang viết code, đang test) và chỉ cho phép chuyển sang trạng thái tiếp theo khi thoả điều kiện nhất định.
> - **Ẩn dụ/so sánh:** Giống đèn giao thông ba màu: xe chỉ được đi khi đèn xanh, chuỗi xanh → vàng → đỏ luôn đúng tuần tự và không bao giờ vọt thẳng từ đỏ sang xanh.
> - **Vì sao quan trọng:** Nó ngăn Agent nhảy loạn giữa các bước, giữ cho luồng thực thi lúc nào cũng hợp lệ và có thể dự đoán được.

### 3.1 Hierarchical State Machine

Đây là bản "nâng cấp" của state machine: ngoài chuyển trạng thái có điều kiện, nó còn hỗ trợ trạng thái cha/con (hierarchical), guard chặn chuyển bất hợp lệ, timeout tự động và giới hạn số lần lặp — đủ an toàn để điều khiển cả một AI coding agent. Code dưới đây mô phỏng agent đi qua chuỗi trạng thái IDLE → THINKING → PLANNING → READING_CODE → WRITING_CODE → RUNNING_TESTS → DONE:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-3-1-hierarchical-state-machine.py`](examples/06-3-1-hierarchical-state-machine.py)

</details>

---

## 4. Error Recovery

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Error Recovery là bộ chiến lược xử lý khi workflow gặp lỗi — thử lại với thời gian chờ tăng dần (retry/backoff), fallback sang phương án khác, hoặc cắt mạch bảo vệ (circuit breaker) — để hệ thống chạy ổn định thay vì sập cả tiến trình.
> - **Ẩn dụ/so sánh:** Giống gọi điện thoại khi máy bận: thử lại sau 1 phút (retry), chưa được thì chờ lâu hơn (backoff), hoặc quay sang gọi người thứ hai (fallback).
> - **Vì sao quan trọng:** Lỗi chắc chắn sẽ xảy ra; có chiến lược khôi phục thì workflow không bị chết đứng giữa chừng.

### 4.1 Retry Strategies

Giống nhấn "gửi lại" email khi mạng chập chờn — nhưng làm có khoa học: thử lại với khoảng chờ tăng dần (1s → 2s → 4s) để không dồn tải lên service, và thêm jitter (độ nhiễu ngẫu nhiên) để các client không cùng lúc "dồn đàn" như bầy trâu tháo chạy (thundering herd). Code dưới đây là decorator retry dùng cho cả hàm đồng bộ lẫn async:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-4-1-retry-strategies.py`](examples/07-4-1-retry-strategies.py)

</details>

### 4.2 Circuit Breaker Pattern

Giống cầu chì điện trong nhà: dòng lỗi quá dày thì cầu chì đứt, ngắt luôn dòng điện để bảo vệ toàn hệ thống. Ở đây, khi một service lỗi liên tục vượt ngưỡng, mạch chuyển từ CLOSED (đóng, vẫn gọi) sang OPEN (mở, chặn gọi); sau một khoảng thời gian hồi phục, nó thử lại ở trạng thái HALF_OPEN để xem service đã khoẻ chưa:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-4-2-circuit-breaker-pattern.py`](examples/08-4-2-circuit-breaker-pattern.py)

</details>

### 4.3 Saga Pattern

Giống làm thủ tục đặt tour trọn gói: nếu hỏng giữa chừng ở bước "đặt vé máy bay" thì phải huỷ ngược lại các bước đã thành công — trả tiền phòng, trả tiền bảo hiểm. Saga dùng cho nghiệp vụ trải qua nhiều services: mỗi bước đều có một compensation (bước bù) để cuộn ngược khi có bước nào đó fail:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-4-3-saga-pattern.py`](examples/09-4-3-saga-pattern.py)

</details>

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

Giống "lệnh truy vết" xuyên suốt hành trình: mỗi yêu cầu được gán một trace_id duy nhất, đi qua bao nhiêu service thì mỗi bước đều ghi lại thành spans (span cha, span con) — nhờ đó bạn dựng lại toàn bộ hành trình của một request và tìm ra chính xác khâu nào chậm hay lỗi:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-5-1-distributed-tracing.py`](examples/10-5-1-distributed-tracing.py)

</details>

### 5.2 Structured Logging + Metrics

Giống nhiệt kế + sổ ghi chép của máy móc: một bên (structured logging) ghi lại từng sự kiện dưới dạng JSON có cấu trúc để dễ lọc tìm, một bên (metrics) đếm và thống kê số liệu — số lần chạy, tỷ lệ thành công, độ trễ p50/p95/p99. Code dưới đây gồm hai lớp WorkflowLogger và MetricsCollector:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/11-5-2-structured-logging-metrics.py`](examples/11-5-2-structured-logging-metrics.py)

</details>

---

## 6. Workflow Orchestration Engine

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Orchestration Engine là "trái tim" của hệ thống — thành phần trung tâm chịu trách nhiệm khởi tạo, điều phối, giám sát và hủy bỏ workflow, đồng thời quản lý scheduling, trạng thái từng bước, retry và dependency giữa các bước.
> - **Ẩn dụ/so sánh:** Giống đài kiểm soát không lưu tại sân bay: điều phối từng chuyến bay (tác vụ) cất hạ cánh đúng đường băng, đúng thứ tự, và biết chính xác máy bay nào đang ở đâu.
> - **Vì sao quan trọng:** Đây là nơi gom toàn bộ kiến thức của các phần trước — patterns, pipeline, state machine, error recovery, observability — thành một engine dùng được trong thực tế.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/12-6-workflow-orchestration-engine.py`](examples/12-6-workflow-orchestration-engine.py)

</details>

---

## 7. Workflow Testing

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Workflow Testing là quy trình kiểm thử workflow trước khi chạy thật — unit test cho từng bước, integration test cho cả chuỗi, end-to-end test cho toàn bộ luồng — để chắc chắn các bước nối nhau đúng và lỗi được xử lý như mong đợi.
> - **Ẩn dụ/so sánh:** Giống chạy thử dây chuyền sản xuất bằng hàng giả: chỉ cần một khâu kẹt là biết ngay chỗ nào hỏng, mà không tốn tiền hàng thật.
> - **Vì sao quan trọng:** Workflow càng phức tạp thì lỗi nối các bước càng khó tìm; kiểm thử đàng hoàng giúp phát hiện lỗi trước khi nó làm hỏng hệ thống thật.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/13-7-workflow-testing.py`](examples/13-7-workflow-testing.py)

</details>

---

## 8. Harness Integration

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Harness Integration là lớp kết nối Workflow module với toàn bộ Harness Framework — Memory, Guardrails, Tool Execution, Feedback — thông qua các interface thống nhất để các module trao đổi với nhau bằng một "ngôn ngữ" chung.
> - **Ẩn dụ/so sánh:** Giống ổ cắm điện chuẩn quốc tế: bất kỳ thiết bị (module) nào cắm vào cũng vừa khớp và hoạt động, miễn là tuân theo chuẩn interface.
> - **Vì sao quan trọng:** Không có interface chuẩn, mỗi module tự bịa cách gọi riêng — tích hợp thành mớ dây nhợ rối và khó bảo trì.

### 8.1 TypeScript Interfaces

Đây là "hợp đồng" giữa Workflow module và phần còn lại của Harness framework — khai báo các method chuẩn như createWorkflow, execute, pause, resume, cancel, getTrace, getMetrics để ai cũng biết engine cung cấp gì và dùng như thế nào:

<details>
<summary><b>8.1 TypeScript Interfaces (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/14-8-1-typescript-interfaces.ts`](examples/14-8-1-typescript-interfaces.ts)

</details>

---

## 9. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Case Studies là những phân tích thực tế về cách các hệ thống lớn (GitHub Actions, Apache Airflow, Temporal, DeepSeek Harness) thiết kế workflow, để rút ra bài học áp dụng vào dự án của bạn.
> - **Ẩn dụ/so sánh:** Giống xem phim tài liệu rồi rút kinh nghiệm: thay vì tự lăn vào vết xe đổ, bạn học ngay từ cách người đi trước đã giải quyết vấn đề.
> - **Vì sao quan trọng:** Lý thuyết suông khó hình dung; học từ hệ thống thật giúp bạn biết pattern nào hiệu quả trong điều kiện sản xuất.

### 9.1. GitHub Actions — Event-Driven CI/CD

Ví dụ gần gũi với hầu hết developer: một file YAML mô tả CI/CD chạy khi có push hoặc pull request. Bạn sẽ thấy ngay event-driven trigger (on:) kết hợp dependency giữa các job — deploy phải chờ build, build phải chờ lint và test:

<details>
<summary><b>9.1. GitHub Actions — Event-Driven CI/CD (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/15-9-1-github-actions-event-driven-ci-cd.yaml`](examples/15-9-1-github-actions-event-driven-ci-cd.yaml)

</details>

**Bài học rút ra**: GitHub Actions chạy workflow theo kiểu DAG — việc nào phụ thuộc việc nào được giải quyết rõ ràng, và mọi thứ bắt đầu từ sự kiện (event triggers).

### 9.2. Apache Airflow — Data Pipeline Orchestration

Airflow nổi tiếng với cách khai báo pipeline bằng DAG trong Python chỉ vài dòng: khai báo các task (extract, transform, load, validate) rồi dùng toán tử >> để nối thứ tự. Cách này khiến toàn bộ quy trình hiện rõ như một bản đồ và dễ đổi thứ tự:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/16-9-2-apache-airflow-data-pipeline-orchestration.py`](examples/16-9-2-apache-airflow-data-pipeline-orchestration.py)

</details>

**Bài học rút ra**: Airflow chứng minh rằng workflow kiểu DAG — task nào phụ thuộc task nào viết ra thật rõ — là chuẩn vàng cho data pipeline.

### 9.3. Temporal — Durable Workflow Execution

Điểm mấu chốt của Temporal: workflow phải "sống sót" ngay cả khi server crash — trạng thái được lưu bền vững (durable) và tự động retry, kèm compensation. Ví dụ dưới đây là flow đặt hàng theo kiểu Saga: giữ hàng → thu tiền → gửi hàng; nếu bước gửi hàng fail thì huỷ ngược lại:

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

---

### 9.4. DeepSeek Harness — Cordis Micro-Kernel Plugin Architecture

**Bối cảnh**: DeepSeek Harness dùng **Cordis** — một micro-kernel cắm plugin được xây theo triết lý **"Agent = Model + Harness"** và **"cái gì cũng là plugin"**. Cordis là một kernel rất nhẹ (core nén lại chỉ ~2KB), lo toàn bộ vòng đời của agent thông qua hệ plugin, còn việc tìm nhau giữa các plugin thì nhờ Context — một chỗ đăng ký service chung (service registry) để inject dependency.

Nói cho dễ hình dung: kernel giống một hệ điều hành tí hon, còn các plugin giống những app cài thêm vào đó — mỗi app chỉ cần khai báo "tôi cần xài dịch vụ gì" (consumes) và "tôi cung cấp dịch vụ gì" (provides), hệ điều hành sẽ tự lo phần nối dây để các app chạy đúng thứ tự.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts`](examples/17-9-4-deepseek-harness-cordis-micro-kernel-plugin.ts)

</details>

**Những điểm hay nhất trong kiến trúc này**:

1. ✅ **Thiết kế micro-kernel** — kernel chỉ ~2KB, mọi chức năng đều là plugin. Cần gì load nấy, thay nóng (hot-reload) được.

2. ✅ **Quản lý vòng đời rõ ràng** — 4 chặng: `init` → `attach` → `ready` → `detach`. Khởi động và tắt máy theo trình tự cố định, đoán được.

3. ✅ **Chỗ đăng ký service qua Context** — muốn chia sẻ thì `ctx.provide()`, muốn xài thì `ctx.inject()` / `ctx.get()`. Plugin khai báo `provides`/`consumes` là tự nối dây (auto-wiring).

4. ✅ **Event bus** — các plugin nói chuyện với nhau kiểu pub/sub. Nhờ vậy plugin này không cần biết plugin kia, muốn mở rộng cũng dễ.

4. ✅ **4 chế độ chạy (runtime modes)** (do plugin `runtime-mode` cung cấp):
   - **Standard** — agent đầy đủ, xài mọi tool, cách ly ở mức process
   - **Code** — SDK `@deepseek-ai/dsh`, chạy script gói gọn trong một lượt, gom batch, sandbox kiểu VM, giảm độ trễ 70-90%
   - **Benchmark** — gọn nhẹ (chỉ có bash + editor), cách ly bằng container, chạy ổn định để chấm SWE-bench
   - **Creator** — có timeline trực quan, preset sẵn, debug kiểu du hành thời gian (time-travel), fork/replay

5. ✅ **Ghi vết hành trình (trajectory)** (do plugin `trajectory-recorder` lo):
   - Luồng event của session, chỉ ghi thêm (append-only)
   - Có `replayToStep()`, `forkSession()`, `resumeSession()`
   - Tìm event theo loại, theo thời gian, theo bước

6. ✅ **Ráp harness bằng cách ghép plugin** — DeepSeek Harness thực chất là nhiều plugin ghép lại. Muốn thay, muốn thêm, muốn test riêng từng mảnh đều dễ.

**So sánh Cordis với framework truyền thống**:

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

**Đọc thêm code chi tiết**: xem [`cordis-kernel-plugin.md`](cordis-kernel-plugin.md)

---

## 10. Design Principles

> **📌 Khái Niệm Cơ Bản**
>
> - **Khái niệm:** Design Principles là bộ chỉ dẫn kiến trúc (gồm nguyên lý SOLID) áp dụng riêng cho workflow — giúp bạn quyết định cách chia bước, tổ chức dependency và đặt biên giới trách nhiệm trong hệ thống.
> - **Ẩn dụ/so sánh:** Giống luật xây nhà: không ai cấm xây, nhưng tuân theo quy chuẩn thì nhà an toàn, dễ sửa và không phải đập đi xây lại.
> - **Vì sao quan trọng:** Nguyên tắc tốt khiến workflow dễ mở rộng, dễ test và ít nợ kỹ thuật khi hệ thống lớn dần.

### 10.1 SOLID Cho Workflows

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
- Đầu vào/đầu ra của từng step tách bạch, theo schema riêng
- Đừng xài chung một cục state mà bước nào cũng sửa được

**5. Dependency Inversion (phụ thuộc vào trừu tượng)**
- Workflow engine chỉ biết tới cái khung chung (Step abstraction)
- Đừng viết cứng (hardcode) cách làm cụ thể của từng step vào engine

### 10.2 6 Design Principles

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

### 11.2 DON'T ❌

- **Đừng xài chung state sửa được (mutable) giữa các bước**: truyền dữ liệu kiểu bất biến (immutable) từ bước này sang bước kia
- **Đừng bỏ qua xử lý lỗi**: bước nào cũng có thể fail, nên chừa đường lui
- **Đừng để vòng lặp vô hạn**: lúc nào cũng đặt số lần lặp tối đa (max iterations)
- **Đừng bơ timeout**: một bước treo là cả workflow đứng hình
- **Đừng viết cứng quan hệ phụ thuộc giữa các bước**: khai báo bằng cấu hình DAG cho dễ đổi
- **Đừng bỏ qua testing**: test riêng từng bước một cách độc lập
- **Đừng gọi blocking trong các bước chạy song song**: dùng async/executor để không nghẽn nhau
- **Đừng quên logic bù (compensation)**: việc nào tiến tới được thì cũng phải có đường lui (rollback)

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

---

## 13. Độ Bền Production: Checkpoint-Resume, Idempotency, Backpressure, Approvals

### 13.1 Định Nghĩa

| Thuật Ngữ | Định Nghĩa |
|------|------------|
| Durable execution | Mỗi step hoàn thành đều được checkpoint (event log + snapshot); khởi động lại sẽ tiếp tục từ checkpoint cuối cùng, không bao giờ chạy lại từ đầu |
| Idempotency key | `stepId + inputHash (+ attempt ceiling)`; thực thi lại với cùng key trả về kết quả đã lưu, không gây tác dụng phụ kép |
| Backpressure | Hàng đợi giới hạn + semaphore (`maxParallel`), deadline của mỗi run được lan truyền qua `AbortSignal`/ctx; giảm tải hoặc hoãn lại thay vì OOM |
| Approval node | Step có trạng thái `WAITING_APPROVAL`; engine tạm dừng, lưu trạng thái, tiếp tục khi được phê duyệt/từ chối/hết thời gian |

### 13.2 Checkpoint-Resume (Tiếp Tục Sau Khi Khởi Động Lại)

Hãy hình dung mỗi step làm xong là mình "chốt sổ" một dòng: ghi log trước đã (`append({seq, stepId, inputHash, status, outputRef})` — gọi là write-ahead log), rồi cứ mỗi N step lại chụp một tấm snapshot nguyên tử. Khi khởi động lại, engine làm đúng 4 việc theo thứ tự: `load snapshot → replay log tail → skip completed (idempotent) → resume pending` — tức nạp snapshot, chạy lại phần đuôi log, step nào xong rồi thì bỏ qua (nhờ idempotent), step nào còn dở thì chạy tiếp. Snapshot cất ở JSON/SQLite ngay trên máy; output nào to hơn 64KB thì không nhét vào log mà gửi ra artifact store, trong log chỉ giữ ref. Và nhớ giữ `runId` cố định qua mọi lần khởi động lại, đừng đổi.

### 13.3 Idempotency + Backpressure + Deadline Theo Từng Step

Về idempotency: có một kho `Map<idempotencyKey, resultRef>` kèm TTL — cứ thao tác ghi (mutation) là bắt buộc phải có key, còn thao tác đọc thì khỏi cần. Về backpressure (chống quá tải): đặt một `Semaphore(maxParallel=4–8)` chung cho toàn engine, mỗi step giới hạn độ dài hàng đợi (ví dụ 100); khi hàng đợi đầy, `enqueue` sẽ ném `BackpressureError` — bên gọi cứ retry kèm jitter là được. Về deadline: mỗi run chỉ có một `deadlineAt` duy nhất; step nào cũng nhận `remaining = deadlineAt - now()` (đã trừ buffer hao hụt), rồi lan truyền xuống qua `AbortSignal.timeout(remaining)`. Nguyên tắc sắt: không bao giờ âm thầm nới deadline.

### 13.4 Node Phê Duyệt / Tạm Dừng-Tiếp Tục Của Con Người

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

Muốn chạy tiếp (resume): gọi lại `run()` với đúng `runId` cũ — key nào đã xong (trúng `done()`/store) sẽ tự được bỏ qua. Muốn tạm dừng (pause): bắt lỗi `PAUSED:*`, lưu trạng thái lên UI, đợi phê duyệt xong rồi chạy lại.

### 13.5 Checklist

- [ ] Đã checkpoint sau mỗi step (log + snapshot) chưa; đã thử kill -9 giữa run rồi chạy lại mà vẫn đạt chưa?
- [ ] Step nào ghi dữ liệu cũng có idempotency key chưa; chạy trùng hai lần cũng không gây tác dụng phụ chứ?
- [ ] Đã đặt `maxParallel` + giới hạn độ dài hàng đợi chưa; deadline đã lan truyền tới signal của mọi step chưa?
- [ ] Node phê duyệt đã lưu trạng thái `WAITING_APPROVAL` chưa; các nhánh approve/reject/timeout đều chạy tiếp đúng chứ?

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

| Thành phần | Vai trò |
|---|---|
| **Checkpoint** | Mỗi step hoàn thành lưu state (outputs, biến, tiến độ) vào storage bền vững (file JSON, S3, DB) |
| **Resume** | Crash/timeout → load checkpoint gần nhất → bỏ qua step đã xong → chạy tiếp |
| **Retry/backoff deterministic** | Lỗi tạm thời (network, rate limit) → exponential backoff, giới hạn số lần |
| **Model adaptation** | Lỗi logic → **báo tool fail cho agent** để nó tự adapt (đổi approach) thay vì retry y nguyên |

Nguyên tắc phân loại: **deterministic problems dùng retry/backoff; những gì cần phán đoán thì đưa về cho model** — agent thấy được lỗi sẽ tự sửa chiến lược, máy móc retry mù quáng thì không.

### 2. Rainbow Deployments

Agents có thể **đang chạy giữa chừng** khi bạn deploy version mới — cắt ngang giữa chừng là mất trạng thái, hỏng task đang dở. Giải pháp: **chuyển traffic dần** từ version cũ sang version mới, giữ cả 2 chạy song song:

| Giai đoạn | Version cũ | Version mới | Ghi chú |
|---|---|---|---|
| 1. Deploy song song | 100% | 0% | Version mới đứng chờ, sẵn sàng nhận task |
| 2. Chuyển dần | 80% → 50% → 20% | 20% → 50% → 80% | Task mới vào version mới; task cũ chạy hết lifecycle trên version cũ |
| 3. Hoàn tất | 0% | 100% | Tắt version cũ khi không còn task nào đang chạy trên nó |

Điểm mấu chốt: **không kill version cũ ngay** — agent đang chạy giữa chừng trên đó cần được hoàn thành trọn vẹn (drain). Tham khảo: **rainbow deploys trong Kubernetes** (Argo Rollouts, Flagger) — weighted routing giữa các version.

### 3. Sync Bottleneck trong Orchestration

Chạy subagents **sync** (lead đợi từng subagent xong rồi mới giao việc tiếp) là mô hình đơn giản nhất — nhưng tạo bottleneck nghiêm trọng:

- Lead **không steer được** subagent giữa chừng: subagent đi lạc hướng thì cũng phải đợi nó chạy xong mới sửa được.
- Lead **blocked** khi 1 subagent chậm: cả hệ thống dừng theo subagent chậm nhất (waterfall effect).

**Async orchestration** giải quyết được throughput, nhưng phải trả lời 3 câu hỏi khó:

| Vấn đề | Câu hỏi | Hướng giải |
|---|---|---|
| **Result coordination** | Kết quả từ nhiều subagent về khi nào, gom thế nào? | Completion queue, callback, hoặc barrier sync |
| **State consistency** | Nhiều subagent viết chung state thì conflict thế nào? | Versioning, optimistic locking, hoặc tách vùng ghi |
| **Error propagation** | 1 subagent fail thì các subagent phụ thuộc biết không? | Cancellation tree + shared error bus |

Quy tắc thực dụng: **sync khi số subagent ít và task ngắn** (dễ debug); **async khi task dài, độc lập nhiều** (nhưng phải đầu tư vào 3 vấn đề trên ngay từ đầu, đừng để thành nợ kỹ thuật).

### 4. Code Python — Workflow Runner với Checkpoint/Resume

Code dưới đây minh họa pattern: mỗi step hoàn thành lưu checkpoint (JSON), crash → resume từ checkpoint cuối, retry với exponential backoff, tối đa 3 lần:

> 📄 **Code ví dụ:** [`examples/19-4-code-python-workflow-runner-voi-checkpoint-resume.py`](examples/19-4-code-python-workflow-runner-voi-checkpoint-resume.py)

**Điểm mấu chốt trong code:**
- `_save()` chạy **ngay sau khi** mỗi step xong — checkpoint luôn mới nhất, crash ở bước nào thì lần sau chỉ lặp lại đúng bước đó.
- `run_id` cố định giúp nhiều lần chạy lại cùng một task **gộp chung checkpoint** — đây chính là resume.
- Retry **deterministic** (backoff cố định công thức) cho lỗi tạm thời; khi hết lượt, ném exception lên để **agent nhận biết và adapt** (đổi cách làm) chứ không retry vô hạn.

### 5. Cross-Reference

> 📎 **Liên quan:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 2** (Orchestration) + **Section 4.3** (Long-Running Agent Pattern). Xem thêm Section 4 (Error Recovery) ở trên cho retry/circuit breaker/saga — checkpoint/resume là lớp bổ sung, không thay thế.

---

*Tài liệu: VII. Workflow — HARNESS ENGINEERING EDITION*
*Ngày cập nhật: 26/10/2026*
*Tác giả: AI Knowledge Repository*