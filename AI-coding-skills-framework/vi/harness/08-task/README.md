# 📋 VIII. Task

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Task Classification](#1-task-classification)
>   - [1.1 Phân Loại Task Coding](#11-phân-loại-task-coding)
>   - [1.2 Task Classification Engine](#12-task-classification-engine)
>   - [1.3 Decision Tree: Chọn Strategy Xử Lý Task](#13-decision-tree-chọn-strategy-xử-lý-task)
> - [2. Task Decomposition](#2-task-decomposition)
>   - [2.1 Patterns Phân Rã Task](#21-patterns-phân-rã-task)
>   - [2.2 Task Decomposer](#22-task-decomposer)
> - [3. Priority & Scheduling](#3-priority-scheduling)
>   - [3.1 Priority Model](#31-priority-model)
> - [4. Task State Management](#4-task-state-management)
>   - [4.1 Task Lifecycle](#41-task-lifecycle)
>   - [4.2 Task State Manager](#42-task-state-manager)
> - [5. Dependency Management](#5-dependency-management)
>   - [5.1 Task Dependency Graph](#51-task-dependency-graph)
> - [6. Task Templates](#6-task-templates)
>   - [6.1 Common Task Templates](#61-common-task-templates)
> - [7. Estimation Techniques](#7-estimation-techniques)
>   - [7.1 Token Estimation Model](#71-token-estimation-model)
>   - [7.2 Effort Estimation Algorithm](#72-effort-estimation-algorithm)
> - [8. Anti-Patterns & Solutions](#8-anti-patterns-solutions)
>   - [8.1 Common Anti-Patterns](#81-common-anti-patterns)
>   - [8.2 Anti-Pattern Detector](#82-anti-pattern-detector)
> - [9. Real-World Workflows](#9-real-world-workflows)
>   - [9.1 Feature Implementation Workflow](#91-feature-implementation-workflow)
>   - [9.2 Debug Investigation Workflow](#92-debug-investigation-workflow)
>   - [9.3 Refactoring Workflow](#93-refactoring-workflow)
> - [10. Token Budget Management](#10-token-budget-management)
>   - [10.1 Context Window Budget Allocation](#101-context-window-budget-allocation)
>   - [10.2 Token Budget Manager](#102-token-budget-manager)
> - [Best Practices](#best-practices)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
---

### Câu Chuyện Mở Đầu

Hãy thử tưởng tượng một buổi sáng bạn làm **quản lý ở một bệnh viện đông nghẹt**. Ngoài cổng thì có người đau bụng cấp tính đang ôm bụng chờ, trong sảnh có bác tới khám định kỳ, góc bên kia lại có bạn nhỏ tới tiêm vaccine. Nếu mình cứ ai tới trước khám trước, không chịu **phân loại xem ai cần cứu ngay**, thì ca cấp cứu kẹt cứng sau ca khám thường — nghe thôi đã thấy toát mồ hôi, đúng không?

**AI Agent mà thiếu Task Management thì cũng rối y như vậy.**

Bạn thử nhờ agent một câu kiểu *"Refactor giùm module auth, viết thêm test, cập nhật docs, rồi deploy luôn nhé"* — agent nghe một lèo hết mọi việc mà chẳng biết nên bắt đầu từ đâu, việc nào gấp, việc nào làm song song được. Thế là dễ làm lộn xộn, quên mất một bước, tệ nhất là **mang code chưa test đi deploy**.

**Cách gỡ rối** chính là Structured Task Management — tức là mình chịu khó phân loại, xếp thứ tự ưu tiên, chẻ nhỏ việc ra rồi theo dõi từng việc một, để agent cứ **làm đúng việc, đúng lúc, đúng thứ tự**.

### Tại Sao Task Management Quan Trọng?

> *"Agent mà không quản lý task thì giống anh đầu bếp ôm một lúc 100 món — món nào cũng nhận mà món nào cũng nấu không tới."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Anthropic (2025)** | Task decomposition giảm **40% completion time** và **55% error rate** trong complex coding tasks |
| 2 | **OpenAI (2025)** | Structured task tracking tăng **35% accuracy** trong multi-step reasoning compared to unstructured approaches |
| 3 | **Microsoft Research (2024)** | Task prioritization framework giảm **30% resource waste** trong AI-assisted development workflows |

#### Triết lý cốt lõi:

```
Task = Analyze → Classify → Prioritize → Decompose → Execute → Track → Report
```

**Nói cho dễ nhớ:** task management cũng giống cách bệnh viện vận hành — tiếp nhận rồi phân loại bệnh nhân (classify), ca nặng cho vào trước (prioritize), bác sĩ kê toa (plan), theo dõi điều trị mỗi ngày (track), khỏi thì cho xuất viện (complete).

**Còn nếu mình bỏ qua bước này thì sao?** Agent sẽ ngợp vì quá nhiều việc dồn một lúc, làm sai thứ tự, đốt tài nguyên vô ích, và cuối cùng là bạn bực mình vì việc chẳng tới đâu.

## Tổng Quan

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task Management trong AI coding là cách mình phân loại, chẻ nhỏ, xếp thứ tự ưu tiên rồi theo dõi các việc lập trình, để agent cứ đúng việc, đúng lúc, đúng thứ tự mà làm.
>
> **Ẩn dụ/so sánh:** Cứ hình dung bạn điều hành một bệnh viện giờ cao điểm — ca cấp cứu phải cho vào trước, lịch khám thường xếp sau, kíp trực chia rõ ràng thì mới không bỏ sót bệnh nhân nào.
>
> **Vì sao quan trọng:** Không có người điều phối, agent rất dễ bị ngợp, làm lộn thứ tự và đốt tài nguyên vô ích.

**Task Management** trong AI coding chính là việc **phân tích, chẻ nhỏ, xếp ưu tiên rồi theo dõi** các tác vụ coding. Task được sắp xếp gọn gàng thì AI agent mới tập trung đúng chỗ, không bị quá tải, và trả về kết quả đàng hoàng.

```
┌──────────────────────────────────────────────────────────────────┐
│                         TASK MANAGEMENT                           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Input   │    │  Parse & │    │  Task    │            │  │
│  │  │  Request │───►│  Classify│───►│  Queue   │            │  │
│  │  └──────────┘    └──────────┘    └────┬─────┘            │  │
│  │                                        │                   │  │
│  │       ┌────────────────────────────────┘                   │  │
│  │       ▼                                                    │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Plan &  │    │  Execute │    │  Validate│            │  │
│  │  │  Assign  │───►│  & Track │───►│  & Close │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Nội Dung

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Đây là tấm bản đồ của cả module — mười chủ đề chính của Task Management, từ lúc nhận diện việc (phân loại, phân rã) tới lúc điều hành (ưu tiên, trạng thái, phụ thuộc) rồi tới chuyện cân đối nguồn lực (ước lượng, token budget).
>
> **Ẩn dụ/so sánh:** Cứ coi như bản đồ tuyến tàu điện ngầm — liếc qua là biết có những ga nào, mình cần xuống ở ga nào cho đúng việc mình đang cần.
>
> **Vì sao quan trọng:** Mỗi chủ đề gỡ một nút thắt trong cùng một bài toán, nên nắm được toàn cảnh thì bạn sẽ dễ định hướng hơn hẳn.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Task Classification](#1-task-classification) | Phân loại task theo kiểu |
| 2 | [Task Decomposition](#2-task-decomposition) | Phân rã task lớn thành nhỏ |
| 3 | [Priority & Scheduling](#3-priority--scheduling) | Ưu tiên và lên lịch |
| 4 | [Task State Management](#4-task-state-management) | Quản lý trạng thái task |
| 5 | [Dependency Management](#5-dependency-management) | Quản lý phụ thuộc giữa tasks |
| 6 | [Task Templates](#6-task-templates) | Mẫu task phổ biến |
| 7 | [Estimation Techniques](#7-estimation-techniques) | Kỹ thuật ước lượng task |
| 8 | [Anti-Patterns & Solutions](#8-anti-patterns--solutions) | Các lỗi thường gặp |
| 9 | [Real-World Workflows](#9-real-world-workflows) | Quy trình thực tế |
| 10 | [Token Budget Management](#10-token-budget-management) | Quản lý ngân sách token |

---

## 1. Task Classification

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task Classification là bước "bắt bệnh" trước khi chữa — đọc kỹ yêu cầu, xem task này thuộc loại nào (viết code mới, sửa bug, refactor, viết test...) và nặng nhẹ cỡ nào (vài dòng hay cả module), rồi mới chọn cách xử lý cho hợp.
>
> **Ẩn dụ/so sánh:** Y như bác sĩ trực cấp cứu phân loại bệnh nhân (triage) trước khi đưa vào phòng mổ — chẩn đoán đúng thì các bước sau mới suôn sẻ, chẩn đoán sai là cả dây chuyền trật theo.
>
> **Vì sao quan trọng:** Phân loại trúng ngay từ đầu thì agent chọn đúng cách làm, đỡ tốn token mà cũng ít sai vặt hơn.

### 1.1 Phân Loại Task Coding

Sơ đồ dưới đây gom các kiểu task coding thành 5 nhóm lớn — mỗi nhóm như một "chuyên khoa" riêng (viết code mới, sửa code, mổ xẻ code, viết tài liệu, viết test). Bạn cứ đọc như cây gia phả: từ nhóm lớn ở trên, lần theo nhánh xuống loại task cụ thể, là biết việc mình đang cầm thuộc họ nào.

```
┌──────────────────────────────────────────────────────────────────┐
│                    TASK TYPE HIERARCHY                            │
│                                                                  │
│  Code Generation                                                 │
│  ├── New Feature        → Tạo tính năng mới                    │
│  ├── Code Snippet       → Tạo đoạn code ngắn                   │
│  ├── Boilerplate        → Tạo template/mẫu                     │
│  └── API Endpoint       → Tạo REST/GraphQL endpoint             │
│                                                                  │
│  Code Modification                                                │
│  ├── Refactor            → Cải thiện cấu trúc code             │
│  ├── Bug Fix             → Sửa lỗi                              │
│  ├── Optimization        → Tối ưu performance                   │
│  └── Migration           → Di chuyển code/platform              │
│                                                                  │
│  Code Analysis                                                    │
│  ├── Code Review         → Đánh giá code quality                │
│  ├── Debugging           → Tìm nguyên nhân lỗi                  │
│  ├── Profiling           → Phân tích performance                 │
│  └── Security Audit      → Kiểm tra bảo mật                     │
│                                                                  │
│  Documentation                                                    │
│  ├── README              → Tài liệu dự án                       │
│  ├── API Docs            → Tài liệu API                         │
│  ├── Comments            → Inline comments                      │
│  └── Changelog           → Nhật ký thay đổi                     │
│                                                                  │
│  Testing                                                          │
│  ├── Unit Test           → Test đơn vị                          │
│  ├── Integration Test    → Test tích hợp                         │
│  ├── E2E Test            → Test đầu cuối                        │
│  └── Test Fixtures       → Dữ liệu test                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Task Classification Engine

Đoạn code dưới đây chính là bộ máy phân loại chạy thật: nó đọc mô tả task bằng ngôn ngữ thường ngày, soi keyword (ví dụ thấy chữ "fix" hay "bug" thì xếp vào nhóm MODIFICATION), rồi áng chừng độ phức tạp để nhả ra một đối tượng Task đầy đủ thông tin. Bạn cứ thử quăng vào một câu mô tả bất kỳ là thấy ngay cách agent "hiểu" yêu cầu ra sao.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-task-classification-engine.py`](examples/01-1-2-task-classification-engine.py)

</details>

### 1.3 Decision Tree: Chọn Strategy Xử Lý Task

Sơ đồ này là luật ra quyết định khi có task mới gõ cửa: nếu yêu cầu còn mù mờ thì phải hỏi lại cho rõ trước, nếu việc gọn dưới 500 tokens thì làm luôn một lèo, còn việc to thì chẻ thành sub-task rồi chọn kiểu chạy nối tiếp, song song hay theo TDD. Bạn cứ đi theo mũi tên từ trên xuống là biết agent sẽ "rẽ cửa nào" cho từng kiểu task.

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK HANDLING DECISION TREE                          │
│                                                                  │
│  Task arrived                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────┐     YES    ┌──────────────────┐                │
│  │ Is it clear? │──────────►│ Can be done in   │                │
│  │ (clear scope)│          │ < 500 tokens?     │                │
│  └──────┬──────┘          └────────┬─────────┘                  │
│         │ NO                       │ YES        NO               │
│         ▼                          ▼            ▼                │
│  ┌──────────────┐         ┌────────────┐  ┌──────────────┐     │
│  │  Clarify     │         │  Execute   │  │  Decompose   │     │
│  │  requirements│         │  directly  │  │  into sub-   │     │
│  │  first       │         │  (1 shot)  │  │  tasks       │     │
│  └──────────────┘         └────────────┘  └──────┬───────┘     │
│                                                   │              │
│                                    ┌──────────────┼──────────┐  │
│                                    ▼              ▼          ▼  │
│                             ┌──────────┐  ┌──────────┐ ┌────┐ │
│                             │Sequential│  │ Parallel │ │TDD │ │
│                             │ Pipeline │  │ Fan-out  │ │    │ │
│                             └──────────┘  └──────────┘ └────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Task Decomposition

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task Decomposition là mẹo chẻ một việc to đùng, khó nuốt thành nhiều subtask nhỏ — mỗi subtask có đầu vào, đầu ra gần như độc lập nên dễ giao cho agent xử lý riêng từng miếng.
>
> **Ẩn dụ/so sánh:** Y như xây nhà — chẳng ai đổ cả căn nhà trong một buổi, mà phải làm móng, dựng khung rồi mới lợp mái; mỗi giai đoạn là một việc nhỏ dễ kiểm soát.
>
> **Vì sao quan trọng:** Việc to dễ làm agent rối trí, quên trước quên sau; chẻ nhỏ ra thì nhẹ đầu hơn hẳn mà tỉ lệ xong việc cũng cao hơn.

### 2.1 Patterns Phân Rã Task

Sơ đồ dưới đây liệt kê 6 kiểu chẻ task hay gặp nhất. Khác nhau cốt ở chỗ các subtask liên hệ với nhau ra sao: chạy nối đuôi theo thứ tự bắt buộc (sequential), chạy song song rồi gom kết quả lại (parallel, map-reduce), hay xếp theo cây cha-con (hierarchical). Bạn cứ nhìn các mũi tên trong hình là biết kiểu nào hợp với việc mình đang làm.

```
┌──────────────────────────────────────────────────────────────────┐
│               TASK DECOMPOSITION PATTERNS                         │
│                                                                  │
│  Pattern 1: SEQUENTIAL DECOMPOSITION                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ Parent   │───►│ Sub 1    │───►│ Sub 2    │───► ...          │
│  │ Task     │    │ (must    │    │ (needs   │                   │
│  │          │    │  finish) │    │  sub 1)  │                   │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                                                  │
│  Pattern 2: PARALLEL DECOMPOSITION                              │
│  ┌──────────┐    ┌──────────┐                                  │
│  │ Parent   │───►│ Sub A    │ ─┐                                │
│  │ Task     │    │ (indep.) │   │    ┌──────────┐              │
│  │          │    ├──────────┤   ├───►│  Merge   │              │
│  │          │───►│ Sub B    │ ─┤    │  Results │              │
│  │          │    │ (indep.) │   │    └──────────┘              │
│  │          │    ├──────────┤   │                               │
│  │          │───►│ Sub C    │ ─┘                                │
│  │          │    │ (indep.) │                                   │
│  └──────────┘    └──────────┘                                  │
│                                                                  │
│  Pattern 3: HIERARCHICAL DECOMPOSITION                          │
│  ┌──────────┐                                                   │
│  │ Epic     │                                                   │
│  └────┬─────┘                                                   │
│       ├── Feature 1                                             │
│       │    ├── Sub-task 1.1                                     │
│       │    └── Sub-task 1.2                                     │
│       └── Feature 2                                             │
│            ├── Sub-task 2.1                                     │
│            ├── Sub-task 2.2                                     │
│            └── Sub-task 2.3                                     │
│                                                                  │
│  Pattern 4: MAP-REDUCE DECOMPOSITION                            │
│  ┌──────────┐    ┌──────────────────────────────┐              │
│  │ Input    │───►│ MAP: Process each item in    │              │
│  │ Data     │    │       parallel                │              │
│  │          │    ├──────────────────────────────┤              │
│  │          │    │ REDUCE: Combine results       │──► Output    │
│  └──────────┘    └──────────────────────────────┘              │
│                                                                  │
│  Pattern 5: SPIKE-THEN-EXECUTE                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  Spike   │───►│ Research │───►│ Execute  │                 │
│  │ (timebox)│    │ & Decide │    │ with     │                  │
│  │ 1-2 hrs  │    │ approach │    │ confidence│                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│                                                                  │
│  Pattern 6: VERTICAL SLICE                                      │
│  ┌──────────────────────────────────────────┐                  │
│  │  Full Stack Feature (thin slice)         │                  │
│  │  DB → API → Service → UI → Test          │                  │
│  │  Each slice = working increment          │                  │
│  └──────────────────────────────────────────┘                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Task Decomposer

Đây là code của bộ chẻ việc: đối tượng TaskDecomposer ôm một Task rồi tự chọn kiểu chẻ cho hợp (theo feature, theo tầng, theo file, theo TDD, vertical slice, spike), sau đó nhả ra danh sách SubTask có thứ tự, dependency, token dự kiến và tiêu chí kiểm tra. Bí quá không biết chọn kiểu nào thì nó cũng tự gợi ý dựa trên loại và độ khó của task.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-task-decomposer.py`](examples/02-2-2-task-decomposer.py)

</details>

---

## 3. Priority & Scheduling

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Priority & Scheduling là cách mình quyết định việc nào làm trước, việc nào xếp sau — dựa trên độ gấp, độ quan trọng, công sức phải bỏ ra và lượng token sẽ tốn.
>
> **Ẩn dụ/so sánh:** Y như xếp hàng ở bệnh viện — ca cấp cứu cho vào trước, ca khám thường chịu khó chờ; còn mấy việc nhỏ mà giá trị cao (quick win) thì tranh thủ làm sớm cho gọn, kiểu trả món nợ nhỏ để nhẹ ví.
>
> **Vì sao quan trọng:** Xếp sai thứ tự là việc quan trọng bị trễ, token thì đội lên, mà bạn lại phải đi nhắc agent từng chút một.

### 3.1 Priority Model

Đoạn code dưới đây cho thấy cách chấm điểm ưu tiên cho từng task theo kiểu Eisenhower Matrix: mỗi task được chấm urgency (độ gấp), importance (độ quan trọng), effort (độ tốn công), rồi cộng thêm điểm bonus nếu đó là việc nhỏ dễ xơi (quick win) hoặc đang có nhiều task khác trông chờ vào nó. TaskScheduler sau đó xếp task vào từng batch sao cho vừa đúng thứ tự vừa không lố ngân sách token của phiên.

Nói nôm na, đây là thang điểm xếp hàng: việc vừa gấp vừa quan trọng thì lên top, việc to mà chưa gấp thì xếp sau, còn mấy việc be bé làm vèo cái xong thì ưu tiên "quét" sớm cho gọn bàn.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-3-1-priority-model.py`](examples/03-3-1-priority-model.py)

</details>

---

## 4. Task State Management

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task State Management là cách mình dõi theo vòng đời của từng task qua các trạng thái như pending, running, blocked, done — kèm cơ chế lưu lại để lúc bị gián đoạn vẫn biết "việc đang dở tới đâu" mà làm tiếp.
>
> **Ẩn dụ/so sánh:** Y như cuốn sổ trực ở bệnh viện — kíp sau đọc là biết kíp trước đã làm gì, bệnh nhân đang ở giai đoạn nào, rồi cứ thế làm tiếp chứ không phải hỏi lại từ đầu.
>
> **Vì sao quan trọng:** Không nắm được task đang ở đâu thì agent khó mà làm tiếp sau khi bị ngắt, rất dễ làm trùng hoặc sót bước.

### 4.1 Task Lifecycle

Sơ đồ dưới đây là tấm bản đồ trạng thái của một task, từ lúc mới sinh ra tới lúc kết thúc: PENDING → PLANNING → IN_PROGRESS → TESTING → REVIEW → DONE. Ngoài đường chính còn có mấy lối rẽ đặc biệt — BLOCKED (kẹt thì quay về chờ), FAILED (hỏng thì làm lại), CANCELLED (hủy). Bạn cứ lần theo mũi tên là biết task được đi từ trạng thái nào sang trạng thái nào.

Nói cho vui thì đây là "hành trình một task đi khám bệnh": mới tạo là ngồi chờ khám (PENDING), được lên phác đồ (PLANNING), vào điều trị (IN_PROGRESS), đi xét nghiệm (TESTING), đem ra hội chẩn (REVIEW), rồi khỏe thì xuất viện (DONE).

```
┌──────────────────────────────────────────────────────────────────┐
│                    TASK LIFECYCLE                                 │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ PENDING  │───►│ PLANNING │───►│IN_PROGRESS│                │
│  │          │    │          │    │          │                   │
│  │ Chưa bắt │    │ Đang lên │    │ Đang làm │                   │
│  │ đầu      │    │ kế hoạch │    │          │                   │
│  └──────────┘    └──────────┘    └────┬─────┘                 │
│                                       │                         │
│                    ┌──────────────────┤                         │
│                    ▼                  ▼                         │
│              ┌──────────┐    ┌──────────┐                     │
│              │BLOCKED   │    │ TESTING  │                      │
│              │          │    │          │                      │
│              │ Bị chặn  │    │ Đang test│                      │
│              └────┬─────┘    └────┬─────┘                      │
│                   │              │                              │
│                   ▼              ▼                              │
│              ┌──────────┐    ┌──────────┐                     │
│              │PENDING   │    │ REVIEW   │                     │
│              │(retry)   │    │          │                      │
│              └──────────┘    └────┬─────┘                      │
│                                  │                              │
│                    ┌─────────────┼─────────────┐               │
│                    ▼             ▼             ▼               │
│              ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│              │  DONE    │  │  FAILED  │  │CANCELLED │        │
│              │          │  │          │  │          │         │
│              │ Hoàn thành│ │ Thất bại │  │ Bị hủy   │        │
│              └──────────┘  └──────────┘  └──────────┘        │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Task State Manager

Đây là code giữ "cuốn sổ theo dõi" cho mọi task: TaskStateManager chỉ cho chuyển trạng thái khi đúng luật (valid transitions), ghi lại giờ bắt đầu, số lần thử, lỗi gần nhất rồi bắn sự kiện cho các phần khác trong hệ thống cùng biết. Bạn mà cố chuyển ẩu (ví dụ từ TESTING nhảy về PENDING), code sẽ chặn lại ngay — cũng nghiêm như quy định ở phòng khám, không cho làm liều.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-4-2-task-state-manager.py`](examples/04-4-2-task-state-manager.py)

</details>

---

## 5. Dependency Management

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Dependency Management là cách mình vẽ ra quan hệ "việc này phải xong trước thì việc kia mới làm được" bằng một đồ thị phụ thuộc (dependency graph), rồi từ đó tính ra thứ tự làm cho đúng và bắt mấy vòng chờ nhau chết cứng (deadlock).
>
> **Ẩn dụ/so sánh:** Y như nấu một bữa cơm nhiều món — canh phải ninh trước rồi mới rảnh tay đi xào, vì món này mượn nguyên liệu của món kia; nấu ngược thứ tự là bữa cơm vỡ trận.
>
> **Vì sao quan trọng:** Xếp sai thứ tự hoặc để hai task đứng chờ nhau mãi thì agent kẹt cứng, việc chẳng bao giờ xong.

### 5.1 Task Dependency Graph

Đoạn code dưới đây dựng một DAG (Directed Acyclic Graph) để trông coi dependency. Cách đọc rất đơn giản: "A → B" nghĩa là task A phải xong trước thì task B mới được bắt đầu. Lớp này lo mấy việc khó nhằn giùm bạn: soi xem có vòng lặp luẩn quẩn không (cycle detection), xếp thứ tự làm cho đúng (topological sort) và tách ra các nhóm task chạy song song được (parallel groups).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-5-1-task-dependency-graph.py`](examples/05-5-1-task-dependency-graph.py)

</details>

---

## 6. Task Templates

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task Templates là các khuôn mẫu có sẵn cho từng loại task quen thuộc (fix bug, thêm feature, refactor v.v.) gồm danh sách bước, token ước lượng và tiêu chí hoàn thành, để agent không phải nghĩ lại từ đầu mỗi lần gặp việc giống nhau.
>
> **Ẩn dụ/so sánh:** Giống form mẫu điền sẵn trong phòng khám — các ô cần thiết đã có sẵn, chỉ cần đổ dữ liệu vào là dùng được, khỏi lo thiếu mục.
>
> **Vì sao quan trọng:** Dùng template giúp agent xử lý nhanh, nhất quán và ít quên bước hơn so với làm tự do.

### 6.1 Common Task Templates

Đoạn code dưới định nghĩa các mẫu task phổ biến dưới dạng dictionary: mỗi mẫu (bug_fix, new_feature, code_review, refactor, debug_investigation, performance_optimization, migration) chứa tiêu đề, danh sách subtask với token riêng rẽ và tổng token ước lượng. Hàm create_task_from_template chỉ cần nhận tên mẫu rồi điền thông tin cụ thể để tạo ra một Task hoàn chỉnh ngay lập tức.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-6-1-common-task-templates.py`](examples/06-6-1-common-task-templates.py)

</details>

---

## 7. Estimation Techniques

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Estimation Techniques là các phương pháp dự đoán trước chi phí thực thi một task — cần bao nhiêu token, bao nhiêu thời gian — dựa trên độ phức tạp, loại task và kinh nghiệm từ những lần trước.
>
> **Ẩn dụ/so sánh:** Giống thợ xây báo giá trước khi nhận thầu — nhìn bản vẽ (task) là ước lượng ngay cần bao nhiêu vật liệu và mấy ngày mới xong, để chủ nhà không lo hụt ngân sách giữa chừng.
>
> **Vì sao quan trọng:** Ước lượng đúng giúp lên kế hoạch tài nguyên và cảnh báo sớm trước khi context window tràn ngập.

### 7.1 Token Estimation Model

Bảng dưới là "bảng giá" kinh nghiệm để ước lượng token cho từng loại task: dò theo loại task (bug fix, new feature, migration v.v.) và độ phức tạp, tra cột Estimated Tokens là biết nên dự trù bao nhiêu. Phần dưới cùng cho biết các con số ước lượng nhanh (ví dụ 1 dòng code rơi vào 5-10 tokens) và cách phân bổ một context window 128K.

```
┌──────────────────────────────────────────────────────────────────┐
│              TOKEN ESTIMATION GUIDE                               │
│                                                                  │
│  Task Type              │ Estimated Tokens │ Notes              │
│  ───────────────────────┼──────────────────┼───────────────────│
│  Bug Fix (simple)       │ 1,000 - 3,000    │ Single file       │
│  Bug Fix (complex)      │ 3,000 - 8,000    │ Multi-file        │
│  New Feature (small)    │ 3,000 - 6,000    │ 1-2 files         │
│  New Feature (large)    │ 6,000 - 15,000   │ 3-5 files         │
│  Refactor (simple)      │ 2,000 - 5,000    │ Rename, extract   │
│  Refactor (complex)     │ 5,000 - 12,000   │ Restructure       │
│  Code Review            │ 2,000 - 5,000    │ Per PR            │
│  Write Tests            │ 2,000 - 6,000    │ Unit + edge cases │
│  Documentation          │ 1,000 - 3,000    │ README, API docs  │
│  Debug Investigation    │ 3,000 - 10,000   │ Investigation     │
│  Migration              │ 5,000 - 20,000   │ Data + code       │
│                                                                  │
│  Context Window Budget (128K model):                             │
│  ├── System prompt:     ~5K tokens                              │
│  ├── Project context:   ~30K tokens                             │
│  ├── Task context:      ~20K tokens                             │
│  ├── Working memory:    ~50K tokens                             │
│  └── Reserve:           ~23K tokens (safety buffer)             │
│                                                                  │
│  Rules of Thumb:                                                 │
│  • 1 LOC ≈ 5-10 tokens (code)                                   │
│  • 1 line of comment ≈ 8-12 tokens                              │
│  • 1 function definition ≈ 20-50 tokens                         │
│  • 1 class definition ≈ 50-100 tokens                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 7.2 Effort Estimation Algorithm

Đây là code ước lượng tự động: EffortEstimator nhận một Task, dựa trên độ phức tạp để chọn con số gốc (BASE_TOKENS), nhân thêm hệ số theo loại task (ví dụ viết tài liệu rẻ hơn code mới), cộng thêm "phí" cho mỗi file đụng tới, rồi trả về token, thời gian ước lượng (giả định khoảng 100 token mỗi phút) và bản tổng kết cho cả batch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-7-2-effort-estimation-algorithm.py`](examples/07-7-2-effort-estimation-algorithm.py)

</details>

---

## 8. Anti-Patterns & Solutions

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Anti-Patterns là những thói quen xử lý task sai mà rất dễ gặp — ví dụ task quá to, mô tả mơ hồ, task đổi scope giữa chừng — kèm giải pháp khắc phục và bộ phát hiện tự động.
>
> **Ẩn dụ/so sánh:** Giống danh sách "bệnh thường gặp" của phòng khám — mỗi bệnh có triệu chứng nhận diện và đơn thuốc điều trị, để biết mình đang mắc bệnh nào mà chữa cho đúng.
>
> **Vì sao quan trọng:** Nhận ra anti-pattern sớm sẽ tránh được phần lớn những hỏng hóc tốn kém nhất khi chạy agent.

### 8.1 Common Anti-Patterns

Sơ đồ dưới liệt kê 8 lỗi task management thường gặp nhất. Mỗi lỗi được đánh dấu bằng "❌ ANTI-PATTERN", kèm triệu chứng nhận diện và mũi tên "→ SOLUTION" là cách chữa. Hãy đọc như một bảng tra cứu: thấy task của mình có triệu chứng nào thì áp dụng giải pháp tương ứng ngay.

```
┌──────────────────────────────────────────────────────────────────┐
│              TASK MANAGEMENT ANTI-PATTERNS                        │
│                                                                  │
│  ❌ ANTI-PATTERN 1: KILLER TASK                                  │
│     Task quá lớn (> 20K tokens), bao trùm nhiều features       │
│     → SOLUTION: Decompose thành sub-tasks < 5K tokens mỗi cái  │
│                                                                  │
│  ❌ ANTI-PATTERN 2: AMBIGUOUS TASK                               │
│     Task description mơ hồ: "improve the code"                  │
│     → SOLUTION: Thêm acceptance criteria cụ thể                │
│                                                                  │
│  ❌ ANTI-PATTERN 3: TASK CHURN                                    │
│     Task liên tục thay đổi scope mid-execution                  │
│     → SOLUTION: Lock scope, tạo task mới cho changes            │
│                                                                  │
│  ❌ ANTI-PATTERN 4: DEPENDENCY DEADLOCK                          │
│     Task A chờ B, B chờ A → không bao giờ finish               │
│     → SOLUTION: Cycle detection + forced break                   │
│                                                                  │
│  ❌ ANTI-PATTERN 5: CONTEXT DRIFT                                │
│     Task chạy quá lâu → agent forgets original intent           │
│     → SOLUTION: Timebox tasks, refresh context periodically     │
│                                                                  │
│  ❌ ANTI-PATTERN 6: MISSING ACCEPTANCE CRITERIA                  │
│     Task done nhưng không biết có đúng yêu cầu không           │
│     → SOLUTION: Mỗi task phải có "definition of done"           │
│                                                                  │
│  ❌ ANTI-PATTERN 7: OVER-DECOMPOSITION                           │
│     Chia quá nhỏ → overhead > benefit                           │
│     → SOLUTION: Minimum 500 tokens per sub-task                 │
│                                                                  │
│  ❌ ANTI-PATTERN 8: IGNORING TOKEN BUDGET                        │
│     Task ước lượng 5K tokens nhưng context window chỉ còn 3K   │
│     → SOLUTION: Always check token budget before starting       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Anti-Pattern Detector

Đây là bộ máy phát hiện anti-pattern tự động: AntiPatternDetector nhận vào một Task, chạy lần lượt các kiểm tra (task quá lớn hơn 20K token, mô tả mơ hồ, thiếu ước lượng, quá nhiều dependencies, thiếu phạm vi file) rồi trả về danh sách vấn đề kèm mức nghiêm trọng và gợi ý khắc phục. Hãy chạy nó trước khi bắt đầu task để "khám bệnh" từ lúc còn sớm.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-8-2-anti-pattern-detector.py`](examples/08-8-2-anti-pattern-detector.py)

</details>

---

## 9. Real-World Workflows

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Real-World Workflows là các quy trình chuẩn hóa cho những tình huống coding thực tế — thêm tính năng, điều tra bug, refactor — gộp toàn bộ bài học task management ở trên thành các bước có thứ tự rõ ràng.
>
> **Ẩn dụ/so sánh:** Giống checklist bay của phi công — không cần nghĩ từng bước trong lúc gấp, cứ theo đúng danh sách là không sót việc nào.
>
> **Vì sao quan trọng:** Có sẵn workflow giúp agent xử lý việc thật một cách có kỷ luật, ít quên và dễ kiểm soát chất lượng.

### 9.1 Feature Implementation Workflow

Sơ đồ dưới mô tả quy trình thêm tính năng mới qua 4 phase: UNDERSTAND → PLAN → IMPLEMENT → VERIFY. Mỗi phase là một hộp chứa các công việc cụ thể (đọc requirement, tìm code tương tự, ước lượng token v.v.). Hãy theo đúng thứ tự phase, giống đi theo công thức nấu ăn — chuẩn bị nguyên liệu xong mới bắt đầu nấu.

```
┌──────────────────────────────────────────────────────────────────┐
│           FEATURE IMPLEMENTATION WORKFLOW                         │
│                                                                  │
│  Phase 1: UNDERSTAND (5-10 min)                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Read requirements/spec                              │     │
│  │ 2. Search existing code for similar features           │     │
│  │ 3. Identify affected files and modules                 │     │
│  │ 4. Check for existing patterns to follow               │     │
│  │ 5. Ask clarifying questions if needed                  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 2: PLAN (5-10 min)                                        │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Design the approach (which files to change)         │     │
│  │ 2. Identify risks and edge cases                       │     │
│  │ 3. Estimate token budget                               │     │
│  │ 4. Create sub-task list with dependencies              │     │
│  │ 5. Choose decomposition strategy                       │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 3: IMPLEMENT (variable)                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Start with data models / types                      │     │
│  │ 2. Implement core business logic                       │     │
│  │ 3. Add API/interface layer                             │     │
│  │ 4. Add error handling                                  │     │
│  │ 5. Write tests (TDD if complex)                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Phase 4: VERIFY (5-10 min)                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ 1. Run linter (flake8, ruff)                           │     │
│  │ 2. Run type checker (mypy)                             │     │
│  │ 3. Run tests (pytest)                                  │     │
│  │ 4. Check for regressions                               │     │
│  │ 5. Verify acceptance criteria met                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Debug Investigation Workflow

Sơ đồ dưới là quy trình điều tra và sửa lỗi gồm 5 bước: REPRODUCE (tái hiện lỗi) → INVESTIGATE (điều tra) → HYPOTHESIZE (đưa giả thuyết) → FIX (sửa) → PREVENT (ngừa tái phát). Điểm mấu chốt là dừng lại để kiểm tra giả thuyết trước khi vội sửa — tránh tình trạng sửa lụi nhưng lỗi vẫn còn.

```
┌──────────────────────────────────────────────────────────────────┐
│             DEBUG INVESTIGATION WORKFLOW                          │
│                                                                  │
│  Step 1: REPRODUCE                                                │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Get exact error message and stack trace              │     │
│  │ • Find minimal reproduction steps                      │     │
│  │ • Note environment details (OS, versions, config)      │     │
│  │ • Check if intermittent or consistent                  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 2: INVESTIGATE                                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Read stack trace → identify entry point              │     │
│  │ • Search for error message in codebase                 │     │
│  │ • Read affected code top-to-bottom                     │     │
│  │ • Check recent git changes (git log --oneline -20)     │     │
│  │ • Add debug logging if needed                          │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 3: HYPOTHESIZE                                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Form hypothesis: "The bug is in X because Y"        │     │
│  │ • Test hypothesis with minimal code change             │     │
│  │ • If wrong, form new hypothesis and repeat             │     │
│  │ • Track hypotheses tried (avoid cycling)               │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 4: FIX                                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Implement minimal fix (not over-engineer)            │     │
│  │ • Verify fix resolves the original issue               │     │
│  │ • Check fix doesn't break other functionality          │     │
│  │ • Add regression test                                  │     │
│  │ • Document root cause in commit message                │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 5: PREVENT                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Add type hints to prevent similar type errors        │     │
│  │ • Add input validation if applicable                   │     │
│  │ • Consider if similar bugs exist elsewhere             │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.3 Refactoring Workflow

Sơ đồ dưới là quy trình refactor an toàn gồm 5 bước: characterize hành vi hiện tại, nhận diện code smells, lập kế hoạch từng bước nhỏ, áp dụng refactor rồi verify lại. Quy tắc vàng được ghi ngay đầu sơ đồ: đừng refactor và thêm feature cùng lúc, và phải chạy test sau mỗi bước để đảm bảo hành vi không đổi.

```
┌──────────────────────────────────────────────────────────────────┐
│              REFACTORING WORKFLOW                                  │
│                                                                  │
│  ⚠️ RULE: Never refactor AND add features at the same time      │
│                                                                  │
│  Step 1: CHARACTERIZE CURRENT BEHAVIOR                           │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Ensure existing tests pass                           │     │
│  │ • If no tests → write characterization tests first     │     │
│  │ • Document current behavior (even if wrong)            │     │
│  │ • Take "before" snapshots (metrics, benchmarks)        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 2: IDENTIFY CODE SMELLS                                    │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Long methods (> 30 lines)                            │     │
│  │ • Large classes (> 300 lines)                          │     │
│  │ • Duplicate code (> 3 similar blocks)                  │     │
│  │ • Deep nesting (> 3 levels)                            │     │
│  │ • God objects (doing too many things)                  │     │
│  │ • Feature envy (method uses other class's data more)   │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 3: PLAN REFACTORING STEPS                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Order refactoring steps from least to most risky     │     │
│  │ • Each step should be small and testable               │     │
│  │ • Run tests after EACH step                            │     │
│  │ • Commit after each successful step                    │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 4: APPLY REFACTORING (Small Steps)                         │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • Extract Method / Extract Class                       │     │
│  │ • Rename for clarity                                   │     │
│  │ • Move methods to correct classes                      │     │
│  │ • Replace conditional with polymorphism                │     │
│  │ • Remove dead code                                     │     │
│  │ • Simplify conditional expressions                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 5: VERIFY                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ • All tests still pass?                                │     │
│  │ • Behavior unchanged? (characterization tests)         │     │
│  │ • Metrics improved? (LOC, complexity, readability)     │     │
│  │ • No performance regression?                           │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Token Budget Management

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Token Budget Management là chiến lược chia và kiểm soát ngân sách token trong context window — bao nhiêu cho system prompt, project context, task context, working memory — để không bao giờ đụng trần và hết chỗ trả lời.
>
> **Ẩn dụ/so sánh:** Giống ví tiền đi chợ — biết tổng tiền đang có, chi khoản nào bao nhiêu, luôn chừa một khoản dự phòng để không phải dừng giữa chừng vì hết tiền đột xuất.
>
> **Vì sao quan trọng:** Tràn context window là một trong những lỗi chết người nhất khi chạy agent — token budget giúp phòng trước.

### 10.1 Context Window Budget Allocation

Sơ đồ dưới cho thấy ngân sách token của một context window 128K được chia làm 4 hộp: System Prompt (cố định), Project Context, Task Context và Working Memory, cộng thêm khoản Reserve để dự phòng. Đọc cột tokens bên phải để biết mỗi hộp chiếm bao nhiêu. Đặc biệt chú ý phần cảnh báo cuối sơ đồ: khi budget còn dưới 20% thì phải tóm tắt hoặc dọn bớt context ngay.

```
┌──────────────────────────────────────────────────────────────────┐
│           TOKEN BUDGET ALLOCATION (128K context window)          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  System Prompt (fixed)              │  ~5,000 tokens  │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Project Context (dynamic)          │  ~30,000 tokens │     │
│  │  • File structure                   │  ~2,000         │     │
│  │  • Key code files                   │  ~20,000        │     │
│  │  • Config files                     │  ~3,000         │     │
│  │  • Documentation                    │  ~5,000         │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Task Context (dynamic)             │  ~20,000 tokens │     │
│  │  • Task description                 │  ~1,000         │     │
│  │  • Related code                     │  ~15,000        │     │
│  │  • Error logs                       │  ~4,000         │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Working Memory (growing)           │  ~50,000 tokens │     │
│  │  • Generated code                   │  ~30,000        │     │
│  │  • Intermediate results             │  ~10,000        │     │
│  │  • Tool outputs                     │  ~10,000        │     │
│  │  ───────────────────────────────────┤                  │     │
│  │  Reserve (safety buffer)            │  ~23,000 tokens │     │
│  │  • Response generation              │  ~15,000        │     │
│  │  • Overflow protection              │  ~8,000         │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ⚠️ When budget < 20% remaining:                                │
│     1. Summarize older context                                  │
│     2. Remove non-essential files from context                  │
│     3. Complete current sub-task, then start fresh               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.2 Token Budget Manager

Đây là code quản lý ngân sách: TokenBudgetManager giữ tổng hạn mức, cấp token cho task qua allocate_for_task (trả False nếu không đủ tiền), theo dõi tỷ lệ dùng (usage_percent), in bản tóm tắt tình trạng "ví tiền" bằng summarize_context và gợi ý cách dọn dẹp khi context gần đầy. Nói ngắn gọn, đây chính là thủ quỹ của hệ thống agent.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-10-2-token-budget-manager.py`](examples/09-10-2-token-budget-manager.py)

</details>

---

## 11. Tích Hợp Harness (TS)

Cứ hình dung mỗi task như một kiện hàng gửi đi — trên nhãn phải ghi rõ mã vận đơn (`trajectoryId`), mã chống trùng (`idempotencyKey`), quyền được mở (`permissions`) và cước phí (`budget`). Đoạn code dưới là "băng chuyền" gom các kiện hàng (`TaskNode`) vào trục thực thi, rồi phát ra event để các tầng workflow/observability cùng nghe thấy.

<details>
<summary>TypeScript Code — Task Engine (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-11-tich-hop-harness-ts.ts`](examples/10-11-tich-hop-harness-ts.ts)

</details>

Mấy luật chơi nhớ giùm nhé: task nào gắn mác `elevated` thì phải xin phê duyệt mới được chạy tiếp; `trajectoryId` là sợi dây nối các log prompt/tool/workflow lại với nhau; còn `idempotencyKey` giúp khử trùng lặp khi bạn retry.

## 12. Ngữ Nghĩa Thực Thi

Cứ coi mỗi task như một món ăn đặt giờ trên bếp — bạn hẹn `timeoutMs` (mặc định 60s), hết giờ mà chưa chín thì tắt bếp và ghi `failed:timeout`. Gặp món hỏng thì xem lại công thức `maxRetries` với backoff mũ + jitter, nhưng chỉ retry khi task idempotent hoặc đã checkpoint. Bấm `cancel()` là dọn bếp ngay: task thành `cancelled`, còn task con trông chờ vào nó thì chuyển thành `blocked`. Còn pipeline xử lỗi thì đi theo đường này: `failed → classify(transient|perm|budget) → transient: retry | perm: park + emit task.failed | budget: compact + re-estimate → continue DAG`. Nhớ một điều cấm kỵ: không bao giờ tự retry thao tác ghi non-idempotent.

## 13. Đồng Thời (Concurrency)

Đoạn này giống chuyện xếp xe qua cầu: Scheduler chia xe thành từng batch theo topo (xe nào mà mọi xe đi trước đều `done` thì mới được lăn bánh), rồi dựng trạm gác semaphore (4–8) kèm cổng token-budget (batch nào mà `sum(budgetTokens) > remaining` thì mời đứng chờ). Muốn nhanh với thao tác đọc nhạy latency thì dùng `race([primary, fallback])`, còn muốn gom kết quả fan-in thì dùng `join(all)`. Để khỏi kẹt cầu, mình giới hạn tài nguyên: tối đa task/run (ví dụ 50), tối đa token/session, độ sâu hàng đợi 1 cho mỗi task. Còn chống deadlock thì cứ thẳng tay: batch nào 2 vòng liền không tiến triển (do thiếu dep/vòng lặp) là cho fail.

## 14. Case Studies

Kể hai câu chuyện đi ca thực tế cho dễ hình dung:

1. **Refactor auth (12 file, 4 tầng):** ca này khám xong xếp loại MODIFICATION/COMPLEX, nên bác sĩ cho mổ theo tầng (db→svc→api→ui→test). Kíp 1 (db) phải xong thì kíp svc/api mới được vào; cổng budget thì mời phần tài liệu UI dời sang session 2 cho khỏi quá tải. Giữa ca có một lệnh `write_file:elevated` phải dừng chờ phê duyệt kèm xem trước diff; nhờ idempotency key mà lần retry sau timeout không bị chạy migration hai lần. Kết quả: 1 lần retry, 0 lần ghi trùng.
2. **Phân loại E2E flaky (30 test):** ca này đông bệnh nhân nên chia theo kiểu map-reduce — 30 shard `run_tests` chạy song song (sem=6), mỗi shard hẹn timeout 90s, chỗ nào nhạy thì cho `race(unit-shard, cached-baseline)` để nhánh nào xanh thì đi tiếp. Có 3 lỗi transient được retry qua idempotency cache; 1 lỗi perm thì ghi `failed` gọn gàng chứ không chặn báo cáo merge. Cuối ca dùng join gom kết quả pass/fail + gắn liên kết trajectory.

## 15. Thực Hành (Hands-On Lab)

Tới giờ thực tập rồi — coi như ca trực 30 phút của bạn:

**Bài tập (30 phút):** thử làm bác sĩ trực với `schedule + execute` cho 6 ca bệnh (A→B, A→C, B+D→E, C→F), trong đó budget là `[2k,3k,3k,5k,2k,2k]`, trần session 10k, `D: elevated`, `E: timeout 5s`.
1. Chia các batch theo topo; chỉ ra batch nào phải đứng chờ phê duyệt và batch nào bị hoãn vì cạn budget.
2. Giả vờ E timeout một lần — hãy retry bằng idempotency-key, rồi ghi lại event `trajectoryId` + `transition`.
3. Gắn thêm `race()` cho C (so kèo cache với live) và `join()` cho E/F. Nộp bài gồm: bảng batch + event log + 1 đoạn văn ngắn kể lại điều gì phải dời sang session 2 và vì sao.

---

## Best Practices

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Best Practices là tập hợp 12 nguyên tắc vàng rút ra từ kinh nghiệm thực tế khi xây dựng task management cho AI agent — từ "một task chỉ làm một việc" đến "quản lý token budget".
>
> **Ẩn dụ/so sánh:** Giống bộ nội quy an toàn lao động — không cần nhớ tại sao từng điều lại đúng, chỉ cần làm theo thì phần lớn rủi ro tự động biến mất.
>
> **Vì sao quan trọng:** Section này gói gọn toàn bộ module thành các quy tắc thực hành dễ dùng hằng ngày.

```
┌──────────────────────────────────────────────────────────────────┐
│                TASK MANAGEMENT BEST PRACTICES                     │
│                                                                  │
│  1. ONE TASK = ONE RESPONSIBILITY                                │
│     Mỗi task chỉ làm 1 việc rõ ràng                           │
│     → Dễ estimate, dễ track, dễ review                         │
│                                                                  │
│  2. SIZE MATTERS                                                  │
│     Task 100-5000 tokens là lý tưởng                            │
│     Quá nhỏ → overhead, quá lớn → dễ fail                      │
│                                                                  │
│  3. VISIBLE STATE                                                 │
│     Luôn biết task đang ở trạng thái gì                         │
│     → State machine + logging                                    │
│                                                                  │
│  4. EXPLICIT DEPENDENCIES                                        │
│     Ghi rõ task nào phụ thuộc task nào                         │
│     → DAG + topological sort                                     │
│                                                                  │
│  5. ESTIMATE & TRACK TOKENS                                      │
│     Theo dõi token usage per task                                │
│     → Budget awareness, avoid context overflow                   │
│                                                                  │
│  6. TEMPLATE COMMON PATTERNS                                     │
│     Tạo template cho task type thường gặp                       │
│     → Tiết kiệm thời gian, đảm bảo consistency                  │
│                                                                  │
│  7. FAIL GRACEFULLY                                               │
│     Task fail → log rõ lý do, retry hoặc skip                  │
│     → Không block toàn bộ pipeline                              │
│                                                                  │
│  8. USE VERIFICATION CRITERIA                                    │
│     Mỗi sub-task phải có "definition of done"                   │
│     → Rõ ràng khi task hoàn thành                               │
│                                                                  │
│  9. DETECT ANTI-PATTERNS EARLY                                   │
│     Check killer tasks, ambiguous tasks, dependency overload    │
│     → Fix before starting execution                              │
│                                                                  │
│  10. CHOOSE RIGHT DECOMPOSITION STRATEGY                         │
│      Auto-detect based on task type and complexity              │
│      → Feature, Layer, File, TDD, Vertical Slice, Spike         │
│                                                                  │
│  11. MANAGE TOKEN BUDGET                                         │
│      Check remaining budget before each sub-task                │
│      → Prevent context overflow, plan session breaks            │
│                                                                  │
│  12. FOLLOW WORKFLOW PATTERNS                                     │
│      Feature → Understand, Plan, Implement, Verify              │
│      Debug → Reproduce, Investigate, Hypothesize, Fix           │
│      Refactor → Characterize, Identify, Plan, Apply, Verify     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tài Liệu Tham Khảo

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Đây là danh sách nguồn tài liệu gốc mà module dựa trên ý tưởng và kỹ thuật — từ LangGraph, CrewAI đến Eisenhower Matrix, cuốn Refactoring của Martin Fowler và bộ chuẩn engineering của Google.
>
> **Ẩn dụ/so sánh:** Giống danh sách sách tham khảo cuối giáo trình — muốn đào sâu hay xem nguồn gốc thì mở đúng cuốn.
>
> **Vì sao quan trọng:** Khi cần chi tiết kỹ thuật đầy đủ hơn, bạn có nơi đáng tin cậy để tra cứu tiếp.

- [LangGraph State Management](https://langchain-ai.github.io/langgraph/)
- [CrewAI Task Management](https://docs.crewai.com/)
- [Eisenhower Matrix](https://www.mindtools.com/pages/article/newHTE_H.htm)
- [Martin Fowler - Refactoring](https://refactoring.com/)
- [Google Engineering Practices](https://google.github.io/eng-practices/review/)
- [Token Estimation - tiktoken](https://github.com/openai/tiktoken)