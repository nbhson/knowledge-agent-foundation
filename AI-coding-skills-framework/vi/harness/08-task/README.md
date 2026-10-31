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

> **Tóm gọn 1 câu:** Task Management cho agent cũng như phân loại bệnh nhân ở bệnh viện: phân loại, xếp ưu tiên, chẻ nhỏ và theo dõi từng việc — agent mới làm đúng việc, đúng lúc, đúng thứ tự.

### Tại Sao Task Management Quan Trọng?

> *"Agent mà không quản lý task thì giống anh đầu bếp ôm một lúc 100 món — món nào cũng nhận mà món nào cũng nấu không tới."*

#### 3 Bằng Chứng Khoa Học

Bảng dưới là 3 nghiên cứu nổi tiếng chứng minh "xếp việc tử tế" có thật sự giúp agent nhanh hơn, ít sai hơn. Cách đọc: cột **Nghiên Cứu** là ai đã nghiên cứu (ví dụ dòng 1: Anthropic — công ty làm Claude), cột **Phát Hiện Quan Trọng** là họ đo được gì.

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

> **Tóm gọn 1 câu:** Task Management là kỹ năng bắt buộc chứ không phải tùy chọn — nghiên cứu của 3 phòng lab lớn đều xác nhận: chia nhỏ, xếp ưu tiên và theo dõi giúp agent nhanh hơn, chính xác hơn và ít phí tài nguyên hơn.

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

Sơ đồ trên đọc từ trái sang phải như một dây chuyền: yêu cầu của bạn vào cửa (**Input Request**), được đọc và phân loại (**Parse & Classify**), xếp vào hàng đợi chờ (**Task Queue**), rồi lên kế hoạch và giao việc (**Plan & Assign**), agent bắt tay làm và được theo dõi (**Execute & Track**), cuối cùng là kiểm tra rồi chốt sổ (**Validate & Close**).

> **Tóm gọn 1 câu:** Task Management là một dây chuyền 6 bước: nhận yêu cầu → phân loại → xếp hàng đợi → lên kế hoạch → thực thi có theo dõi → kiểm tra rồi chốt.

## Nội Dung

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Đây là tấm bản đồ của cả module — mười chủ đề chính của Task Management, từ lúc nhận diện việc (phân loại, phân rã) tới lúc điều hành (ưu tiên, trạng thái, phụ thuộc) rồi tới chuyện cân đối nguồn lực (ước lượng, token budget).
>
> **Ẩn dụ/so sánh:** Cứ coi như bản đồ tuyến tàu điện ngầm — liếc qua là biết có những ga nào, mình cần xuống ở ga nào cho đúng việc mình đang cần.
>
> **Vì sao quan trọng:** Mỗi chủ đề gỡ một nút thắt trong cùng một bài toán, nên nắm được toàn cảnh thì bạn sẽ dễ định hướng hơn hẳn.

Cách đọc bảng này: cột **Chủ đề** là tên mục (bấm vào sẽ nhảy tới đúng chỗ), cột **Mô tả** là một câu giải thích chủ đề đó làm gì. Ví dụ dòng 1: Task Classification = phân loại task theo kiểu, như bệnh viện phân loại bệnh nhân.

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

> **Tóm gọn 1 câu:** Mục lục gồm 10 chủ đề theo thứ tự xử lý một task: phân loại → chẻ nhỏ → xếp ưu tiên → quản lý trạng thái và phụ thuộc → dùng mẫu và ước lượng → tránh lỗi → quy trình thực tế → cân đối ngân sách token.

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

Đọc cụ thể cho dễ hiểu: nhánh **Code Generation** là các task "tạo ra code mới" — ví dụ New Feature là làm tính năng mới, Boilerplate là tạo khung mẫu có sẵn; nhánh **Code Analysis** là các task "đọc code để đánh giá" — ví dụ Debugging là đi tìm nguyên nhân lỗi, Security Audit là kiểm tra lỗ hổng bảo mật.

> **Tóm gọn 1 câu:** Task coding rơi vào 1 trong 5 nhóm: tạo code mới, sửa code, phân tích code, viết tài liệu, viết test — biết task thuộc nhóm nào là chọn được cách xử lý hợp lý.

### 1.2 Task Classification Engine

Đoạn code dưới đây chính là bộ máy phân loại chạy thật: nó đọc mô tả task bằng ngôn ngữ thường ngày, soi keyword (ví dụ thấy chữ "fix" hay "bug" thì xếp vào nhóm MODIFICATION), rồi áng chừng độ phức tạp để nhả ra một đối tượng Task đầy đủ thông tin. Bạn cứ thử quăng vào một câu mô tả bất kỳ là thấy ngay cách agent "hiểu" yêu cầu ra sao.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-task-classification-engine.py`](examples/01-1-2-task-classification-engine.py)

</details>

> **Tóm gọn 1 câu:** Bộ phân loại đọc mô tả task bằng tiếng thường, soi keyword và áng độ khó, rồi nhả ra đối tượng Task đầy đủ thông tin — đúng kiểu bác sĩ khám xong ghi chẩn đoán vào phiếu.

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

Đọc ví dụ cụ thể: task mơ hồ như "làm đẹp code lại đi" → đi nhánh NO (Clarify requirements first) là agent phải hỏi lại cho rõ; task gọn như "sửa chính tả trong README" → đi nhánh YES là làm luôn một lèo (Execute directly); task to như "thêm tính năng đăng nhập" → chẻ thành sub-task, rồi chọn chạy nối tiếp (Sequential Pipeline = làm từng bước lần lượt), chạy song song (Parallel Fan-out = mấy việc không phụ thuộc nhau thì làm cùng lúc), hay viết test trước (TDD = Test-Driven Development, viết test trước rồi mới viết code).

> **Tóm gọn 1 câu:** Cây quyết định 3 nhánh: mờ thì hỏi lại, nhỏ thì làm luôn, to thì chẻ nhỏ rồi chọn chạy nối tiếp, song song hay TDD.

> **Tóm gọn 1 câu (cả mục 1):** Task Classification là bước "bắt bệnh" trước khi chữa — phân đúng loại task và chọn đúng strategy thì agent làm nhanh hơn, rẻ token hơn và ít sai hơn.

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

Đọc ví dụ cụ thể: **Pattern 1 (Sequential)** là làm nối đuôi — xây móng xong mới dựng tường; **Pattern 2 (Parallel)** là 3 thợ phụ phụ trách 3 phòng khác nhau rồi thợ chính gom kết quả lại (Merge Results); **Pattern 5 (Spike)** là hẹn giờ 1-2 tiếng nghiên cứu thử xem đường nào khả thi trước khi làm thật (spike = buổi thí nghiệm có giới hạn thời gian); **Pattern 6 (Vertical Slice)** là làm một lát mỏng xuyên suốt từ database tới giao diện, sao cho mỗi lát đều chạy được hẳn hoi chứ không phải nửa vời.

> **Tóm gọn 1 câu:** 6 pattern chẻ việc khác nhau ở kiểu quan hệ giữa các subtask — nối tiếp, song song, cây cha-con, map-reduce, thử nghiệm trước rồi làm, và lát mỏng xuyên suốt.

### 2.2 Task Decomposer

Đây là code của bộ chẻ việc: đối tượng TaskDecomposer ôm một Task rồi tự chọn kiểu chẻ cho hợp (theo feature, theo tầng, theo file, theo TDD, vertical slice, spike), sau đó nhả ra danh sách SubTask có thứ tự, dependency, token dự kiến và tiêu chí kiểm tra. Bí quá không biết chọn kiểu nào thì nó cũng tự gợi ý dựa trên loại và độ khó của task.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-task-decomposer.py`](examples/02-2-2-task-decomposer.py)

</details>

> **Tóm gọn 1 câu:** TaskDecomposer là bộ chẻ việc tự động: nhận task lớn, tự chọn kiểu chẻ hợp lý và nhả ra danh sách subtask có thứ tự, phụ thuộc, token dự kiến và tiêu chí nghiệm thu.

> **Tóm gọn 1 câu (cả mục 2):** Chẻ việc to thành subtask nhỏ là cách giúp agent không ngợp — 6 pattern cho đủ kiểu tình huống, và code decomposer tự chọn pattern giúp bạn.

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

Giải thích thêm mấy thuật ngữ trong đoạn trên: **Eisenhower Matrix** = bảng 4 ô chia việc theo hai trục "gấp hay không" và "quan trọng hay không" (đặt theo tổng thống Mỹ Eisenhower); **quick win** = việc nhỏ mà lợi ích cao, làm vèo cái xong; **batch** = một "đợt làm việc" gom nhiều task chạy cùng lúc.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-3-1-priority-model.py`](examples/03-3-1-priority-model.py)

</details>

> **Tóm gọn 1 câu:** Điểm ưu tiên = độ gấp + độ quan trọng − độ tốn công + điểm thưởng (quick win, có người chờ); scheduler rồi xếp task thành các đợt sao cho không lố ngân sách token.

> **Tóm gọn 1 câu (cả mục 3):** Xếp ưu tiên kiểu Eisenhower Matrix giúp việc quan trọng không bị việc vặt nhấn chìm, đồng thời giữ token trong ngân sách của phiên.

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

Giải thích vài trạng thái dễ nhầm: **BLOCKED** là task bị kẹt vì chờ thứ khác (thiếu file, thiếu phê duyệt), không phải là hỏng; **PENDING (retry)** ở nhánh rẽ là kẹt xong thì quay về hàng chờ để thử lại; **FAILED** khác **CANCELLED** ở chỗ FAILED là làm mà hỏng, CANCELLED là chủ động bỏ không làm nữa.

> **Tóm gọn 1 câu:** Vòng đời task là chuỗi trạng thái từ chờ → lập kế hoạch → làm → test → duyệt → xong, kèm 3 lối rẽ: kẹt thì quay về chờ thử lại, hỏng thì ghi thất bại, không làm nữa thì hủy.

### 4.2 Task State Manager

Đây là code giữ "cuốn sổ theo dõi" cho mọi task: TaskStateManager chỉ cho chuyển trạng thái khi đúng luật (valid transitions), ghi lại giờ bắt đầu, số lần thử, lỗi gần nhất rồi bắn sự kiện cho các phần khác trong hệ thống cùng biết. Bạn mà cố chuyển ẩu (ví dụ từ TESTING nhảy về PENDING), code sẽ chặn lại ngay — cũng nghiêm như quy định ở phòng khám, không cho làm liều.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-4-2-task-state-manager.py`](examples/04-4-2-task-state-manager.py)

</details>

> **Tóm gọn 1 câu:** TaskStateManager là cuốn sổ trực của hệ thống: chỉ cho chuyển trạng thái đúng luật, ghi giờ và lỗi lại, bắn sự kiện báo cho mọi người — nên mất điện giữa chừng vẫn làm tiếp được đúng chỗ dở.

> **Tóm gọn 1 câu (cả mục 4):** Quản lý trạng thái giúp task "chết giữa đường" vẫn phục hồi được đúng chỗ dở, nhờ sổ trạng thái chặt chẽ và luật chuyển trạng thái không cho làm liều.

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

Giải thích nhanh mấy thuật ngữ: **DAG (Directed Acyclic Graph)** = đồ thị có hướng, không vòng lặp — "hướng" nghĩa là mũi tên chỉ chiều "phải làm trước", "không vòng lặp" nghĩa là không có trường hợp A đợi B mà B lại đợi A; **topological sort** = xếp thứ tự các task sao cho task nào được nhắc tới trước thì được làm trước; **cycle detection** = dò xem sơ đồ có vòng chờ nhau chết cứng (deadlock) hay không.

> **Tóm gọn 1 câu:** Dependency graph vẽ quan hệ "việc này xong trước thì việc kia mới làm" bằng DAG, rồi tự tính thứ tự làm đúng và bắt ra vòng chờ nhau chết cứng.

> **Tóm gọn 1 câu (cả mục 5):** Vẽ dependency graph kiểu DAG là cách đảm bảo agent không làm ngược thứ tự và không để hai task đứng chờ nhau mãi.

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

> **Tóm gọn 1 câu:** Mỗi loại task quen thuộc có sẵn một khuôn mẫu ghi rõ các bước con và token ước lượng — gọi tên mẫu ra, điền thông tin cụ thể vào là có ngay task hoàn chỉnh.

> **Tóm gọn 1 câu (cả mục 6):** Task template giống form mẫu phòng khám: dùng lại cái đã chuẩn hóa cho việc giống nhau thì nhanh hơn, nhất quán hơn và ít sót bước hơn.

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

Cách đọc bảng trên: tra theo **loại task** (cột trái, ví dụ "Bug Fix (simple)" = sửa lỗi chỉ đụng một file) để lấy khoảng token dự trù ở cột giữa. Phần **Context Window Budget** chia một cửa sổ context 128K tokens (128,000 tokens ≈ khoảng 90-100 trang văn bản) thành các khoản: lời dặn hệ thống ~5K, bối cảnh dự án ~30K, bối cảnh task ~20K, bộ nhớ làm việc ~50K, và chừa ~23K dự phòng. Phần **Rules of Thumb** là quy tắc ngón tay: 1 LOC (line of code = một dòng code) tốn khoảng 5-10 tokens.

> **Tóm gọn 1 câu:** Tra "bảng giá" token theo loại task và độ khó để dự trù chi phí, nhớ quy tắc 1 dòng code ≈ 5-10 tokens, và luôn chừa ~23K tokens dự phòng trong cửa sổ 128K.

### 7.2 Effort Estimation Algorithm

Đây là code ước lượng tự động: EffortEstimator nhận một Task, dựa trên độ phức tạp để chọn con số gốc (BASE_TOKENS), nhân thêm hệ số theo loại task (ví dụ viết tài liệu rẻ hơn code mới), cộng thêm "phí" cho mỗi file đụng tới, rồi trả về token, thời gian ước lượng (giả định khoảng 100 token mỗi phút) và bản tổng kết cho cả batch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-7-2-effort-estimation-algorithm.py`](examples/07-7-2-effort-estimation-algorithm.py)

</details>

> **Tóm gọn 1 câu:** EffortEstimator tự ước lượng chi phí bằng công thức: token gốc theo độ khó × hệ số theo loại task + phí cho từng file đụng tới — cho ra số token, thời gian dự kiến ngay từ đầu.

> **Tóm gọn 1 câu (cả mục 7):** Ước lượng token trước khi làm (tra bảng kinh nghiệm hoặc dùng công cụ tính tự động) giúp lên kế hoạch tài nguyên và cảnh báo sớm trước khi context window bị nhồi đầy.

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

Đọc ví dụ cụ thể: **Anti-pattern 1 (Killer Task)** là task ôm đồm quá to — hơn 20K tokens, đụng tới nhiều tính năng một lượt — chữa bằng cách chẻ thành các subtask dưới 5K tokens mỗi cái; **Anti-pattern 4 (Dependency Deadlock)** là A chờ B xong mà B lại chờ A xong, không task nào chạy nổi — chữa bằng dò vòng lặp (cycle detection) rồi chủ động cắt một mũi tên; **Anti-pattern 8 (Ignoring Token Budget)** là task cần 5K tokens mà cửa sổ context chỉ còn 3K — chữa bằng cách kiểm tra ngân sách trước khi bắt đầu.

> **Tóm gọn 1 câu:** 8 lỗi hay gặp nhất — task quá to, mơ hồ, đổi scope giữa chừng, chờ nhau chết cứng, quên ý định ban đầu, thiếu tiêu chí nghiệm thu, chẻ quá nhỏ, phớt lờ ngân sách token — đều có cách chữa rõ ràng trong bảng.

### 8.2 Anti-Pattern Detector

Đây là bộ máy phát hiện anti-pattern tự động: AntiPatternDetector nhận vào một Task, chạy lần lượt các kiểm tra (task quá lớn hơn 20K token, mô tả mơ hồ, thiếu ước lượng, quá nhiều dependencies, thiếu phạm vi file) rồi trả về danh sách vấn đề kèm mức nghiêm trọng và gợi ý khắc phục. Hãy chạy nó trước khi bắt đầu task để "khám bệnh" từ lúc còn sớm.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-8-2-anti-pattern-detector.py`](examples/08-8-2-anti-pattern-detector.py)

</details>

> **Tóm gọn 1 câu:** AntiPatternDetector "khám bệnh" task trước khi chạy: soi lần lượt 5 kiểu lỗi (quá to, mơ hồ, thiếu ước lượng, phụ thuộc quá nhiều, thiếu phạm vi file) rồi báo kèm mức nghiêm trọng và gợi ý sửa.

> **Tóm gọn 1 câu (cả mục 8):** Nhận ra 8 anti-pattern sớm (bằng bảng tra cứu hoặc bộ phát hiện tự động) là cách rẻ nhất để tránh những hỏng hóc tốn kém nhất khi agent chạy task.

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

Giải thích mấy công cụ trong Phase 4: **linter** (flake8, ruff) = phần mềm rà lỗi phong cách code; **mypy** = trình kiểm tra kiểu dữ liệu (type checker); **pytest** = framework chạy test của Python; **regressions** = lỗi cũ quay lại do thay đổi mới.

> **Tóm gọn 1 câu:** Thêm tính năng mới theo đúng 4 pha: hiểu yêu cầu → lập kế hoạch → hiện thực từ model tới logic tới test → xác nhận bằng linter, type checker và test.

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

Giải thích vài chi tiết kỹ thuật trong sơ đồ: **stack trace** = bản in ra đường đi của lỗi, từng dòng một hàm gọi hàm nào; **git log --oneline -20** = lệnh xem 20 commit gần nhất, mỗi commit một dòng tóm tắt — giúp biết gần đây ai sửa gì; **minimal fix** = sửa đúng phần hỏng thôi, không lợi thế "sản xuất thêm" code phức tạp; **regression test** = test mới ghi lại lỗi này, để sau này chạy lại là biết lỗi không tái diễn.

> **Tóm gọn 1 câu:** Sửa lỗi đúng quy trình 5 bước: tái hiện → điều tra → đặt giả thuyết rồi kiểm chứng → sửa tối thiểu kèm regression test → phòng ngừa lỗi tương tự.

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

Giải thích mấy thuật ngữ trong sơ đồ: **characterization tests** = test ghi lại hành vi hiện tại (dù hành vi đó sai) làm "ảnh chụp chuẩn" để so sánh sau khi refactor; **code smells** = dấu hiệu code có vấn đề, ví dụ hàm quá dài (> 30 dòng), class "thần tài" (God object) ôm đủ thứ; **feature envy** = hàm này lại quan tâm dữ liệu của class khác nhiều hơn của chính nó — dấu hiệu nên chuyển nó sang class kia; **Extract Method** = tách một đoạn code thành hàm riêng có tên rõ nghĩa.

> **Tóm gọn 1 câu:** Refactor an toàn là: chụp lại hành vi hiện tại bằng test trước, nhận diện code smells, sửa từng bước nhỏ có commit và chạy test sau mỗi bước, cuối cùng xác nhận hành vi không đổi.

> **Tóm gọn 1 câu (cả mục 9):** Ba quy trình chuẩn (thêm tính năng, điều tra bug, refactor) là checklist bay của agent: theo đúng thứ tự các bước thì không sót việc nào và không phá hỏng thứ có sẵn.

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

Đọc ví dụ cụ thể: hộp **Project Context ~30,000 tokens** là "sách giáo khoa" về dự án nạp sẵn — trong đó cấu trúc file tốn ~2K, các file code chính ~20K, file cấu hình ~3K, tài liệu ~5K; hộp **Working Memory ~50,000 tokens** là "bàn làm việc" chứa những gì agent vừa làm — code vừa sinh ra, kết quả trung gian, output từ tool. Hộp **Reserve ~23,000 tokens** là khoản dự phòng: ~15K cho phần trả lời của model, ~8K để không "đổ vỡ" nếu phát sinh.

> **Tóm gọn 1 câu:** Chia cửa sổ context 128K thành 4 hộp có hạn mức (system prompt, bối cảnh dự án, bối cảnh task, bộ nhớ làm việc) cộng khoản dự phòng 23K — còn dưới 20% là phải dọn bớt ngay.

### 10.2 Token Budget Manager

Đây là code quản lý ngân sách: TokenBudgetManager giữ tổng hạn mức, cấp token cho task qua allocate_for_task (trả False nếu không đủ tiền), theo dõi tỷ lệ dùng (usage_percent), in bản tóm tắt tình trạng "ví tiền" bằng summarize_context và gợi ý cách dọn dẹp khi context gần đầy. Nói ngắn gọn, đây chính là thủ quỹ của hệ thống agent.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-10-2-token-budget-manager.py`](examples/09-10-2-token-budget-manager.py)

</details>

> **Tóm gọn 1 câu:** TokenBudgetManager là thủ quỹ của agent: giữ tổng hạn mức, cấp token cho từng task (không đủ thì từ chối), theo dõi phần trăm đã dùng và gợi ý dọn dẹp khi ví sắp vơi.

> **Tóm gọn 1 câu (cả mục 10):** Tràn context window là một trong những lỗi chết người nhất — chia ngân sách token thành các hộp có hạn mức và có thủ quỹ theo dõi là cách phòng trước.

---

## 11. Tích Hợp Harness (TS)

Cứ hình dung mỗi task như một kiện hàng gửi đi — trên nhãn phải ghi rõ mã vận đơn (`trajectoryId`), mã chống trùng (`idempotencyKey`), quyền được mở (`permissions`) và cước phí (`budget`). Đoạn code dưới là "băng chuyền" gom các kiện hàng (`TaskNode`) vào trục thực thi, rồi phát ra event để các tầng workflow/observability cùng nghe thấy.

Giải thích nhanh mấy cái nhãn trên kiện hàng: **trajectoryId** = mã "vận đơn" nối tất cả log (prompt, gọi tool, workflow) của cùng một lần chạy task — cần nó để truy vết một task đi qua đâu; **idempotencyKey** = mã chống làm trùng: nếu retry (chạy lại sau khi lỗi) bằng đúng mã này, hệ thống nhận ra và không làm lại việc đã làm rồi — ví dụ không chạy migration database hai lần; **permissions** = quyền ghi/xóa file được cấp cho task này; **budget** = hạn mức token tối đa task được đốt. Còn **TaskNode** là đối tượng mô tả một task trong engine TypeScript, và **event** là tín hiệu phát ra cho các bộ phận khác "nghe" được.

<details>
<summary>TypeScript Code — Task Engine (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-11-tich-hop-harness-ts.ts`](examples/10-11-tich-hop-harness-ts.ts)

</details>

Mấy luật chơi nhớ giùm nhé: task nào gắn mác `elevated` thì phải xin phê duyệt mới được chạy tiếp; `trajectoryId` là sợi dây nối các log prompt/tool/workflow lại với nhau; còn `idempotencyKey` giúp khử trùng lặp khi bạn retry.

> **Tóm gọn 1 câu:** Trong harness TypeScript, mỗi task là một kiện hàng có nhãn đầy đủ (truy vết, chống trùng, quyền, ngân sách) đi qua băng chuyền Task Engine — việc nhạy cảm (`elevated`) phải chờ phê duyệt.

## 12. Ngữ Nghĩa Thực Thi

Cứ coi mỗi task như một món ăn đặt giờ trên bếp — bạn hẹn `timeoutMs` (mặc định 60s), hết giờ mà chưa chín thì tắt bếp và ghi `failed:timeout`. Gặp món hỏng thì xem lại công thức `maxRetries` với backoff mũ + jitter, nhưng chỉ retry khi task idempotent hoặc đã checkpoint. Bấm `cancel()` là dọn bếp ngay: task thành `cancelled`, còn task con trông chờ vào nó thì chuyển thành `blocked`. Còn pipeline xử lỗi thì đi theo đường này: `failed → classify(transient|perm|budget) → transient: retry | perm: park + emit task.failed | budget: compact + re-estimate → continue DAG`. Nhớ một điều cấm kỵ: không bao giờ tự retry thao tác ghi non-idempotent.

Giải thích từng thuật ngữ khó: **backoff mũ (exponential backoff)** = chờ lâu gấp đôi sau mỗi lần thử lại (1s, 2s, 4s...); **jitter** = cộng thêm chút nhiễu ngẫu nhiên vào thời gian chờ, để nhiều task không "đập" server cùng một nhịp; **idempotent** = làm lại nhiều lần cho cùng kết quả (như phép cộng, không như thao tác trừ tiền); **checkpoint** = điểm lưu tiến độ để chạy lại từ đó chứ không làm lại từ đầu; **transient** = lỗi tạm thời (mạng chập chờn, timeout) — retry được; **perm** = lỗi vĩnh viễn (quyền không đủ, code sai cú pháp) — retry vô ích, nên "park" (để sang một bên) và phát event `task.failed`; **budget** = hết hạn mức token — phải "compact" (nén gọn context) rồi ước lượng lại; **non-idempotent** = làm lại là tệ thêm (ví dụ trừ tiền hai lần, xóa file hai lần).

> **Tóm gọn 1 câu:** Mỗi task có hẹn giờ (timeout), quy tắc thử lại (chỉ retry khi lỗi tạm thời và việc đó lặp lại được), và đường xử lỗi tách 3 loại: lỗi tạm thì retry, lỗi hẳn thì ghi thua, hết ngân sách thì nén context rồi ước lượng lại.

## 13. Đồng Thời (Concurrency)

Đoạn này giống chuyện xếp xe qua cầu: Scheduler chia xe thành từng batch theo topo (xe nào mà mọi xe đi trước đều `done` thì mới được lăn bánh), rồi dựng trạm gác semaphore (4–8) kèm cổng token-budget (batch nào mà `sum(budgetTokens) > remaining` thì mời đứng chờ). Muốn nhanh với thao tác đọc nhạy latency thì dùng `race([primary, fallback])`, còn muốn gom kết quả fan-in thì dùng `join(all)`. Để khỏi kẹt cầu, mình giới hạn tài nguyên: tối đa task/run (ví dụ 50), tối đa token/session, độ sâu hàng đợi 1 cho mỗi task. Còn chống deadlock thì cứ thẳng tay: batch nào 2 vòng liền không tiến triển (do thiếu dep/vòng lặp) là cho fail.

Giải thích từng khái niệm: **batch theo topo** = chia đợt theo thứ tự phụ thuộc đã tính trước (topological order) — đợt sau chỉ chạy khi mọi việc của đợt trước đã `done`; **semaphore (4–8)** = "trạm gác" giới hạn số task chạy đồng thời, ví dụ tối đa 4-8 task cùng lúc; **latency** = thời gian chờ phản hồi; **`race([primary, fallback])`** = chạy hai nhánh cùng lúc, nhánh nào trả lời trước thì lấy nhánh đó (ví dụ so kết quả cache với gọi trực tiếp); **fan-in / `join(all)`** = chờ tất cả các task con chạy xong rồi gom hết kết quả về một chỗ; **deadlock** = hai task đứng chờ nhau mãi, không ai nhúc nhích.

> **Tóm gọn 1 câu:** Chạy nhiều task song song an toàn nhờ 4 lớp: xếp đợt theo thứ tự phụ thuộc, trạm gác giới hạn chạy đồng thời, cổng ngân sách token, và quy tắc hạnh phúc — kẹt 2 vòng liền là cho fail ngay thay vì để treo.

## 14. Case Studies

Kể hai câu chuyện đi ca thực tế cho dễ hình dung:

1. **Refactor auth (12 file, 4 tầng):** ca này khám xong xếp loại MODIFICATION/COMPLEX, nên bác sĩ cho mổ theo tầng (db→svc→api→ui→test). Kíp 1 (db) phải xong thì kíp svc/api mới được vào; cổng budget thì mời phần tài liệu UI dời sang session 2 cho khỏi quá tải. Giữa ca có một lệnh `write_file:elevated` phải dừng chờ phê duyệt kèm xem trước diff; nhờ idempotency key mà lần retry sau timeout không bị chạy migration hai lần. Kết quả: 1 lần retry, 0 lần ghi trùng.
2. **Phân loại E2E flaky (30 test):** ca này đông bệnh nhân nên chia theo kiểu map-reduce — 30 shard `run_tests` chạy song song (sem=6), mỗi shard hẹn timeout 90s, chỗ nào nhạy thì cho `race(unit-shard, cached-baseline)` để nhánh nào xanh thì đi tiếp. Có 3 lỗi transient được retry qua idempotency cache; 1 lỗi perm thì ghi `failed` gọn gàng chứ không chặn báo cáo merge. Cuối ca dùng join gom kết quả pass/fail + gắn liên kết trajectory.

Giải thích vài từ trong hai ca trên: **flaky test** = test "hên xui", đôi lúc pass đôi lúc fail dù code không đổi; **shard** = một phần nhỏ của khối việc (ở đây mỗi shard chạy một nhóm test); **E2E test** = end-to-end, test toàn bộ luồng từ đầu tới cuối như người dùng thật; **diff** = bảng so sánh thay đổi trước/sau của code, xem trước để duyệt; **migration** = script chuyển đổi dữ liệu/cấu trúc database — chạy hai lần là hỏng dữ liệu, nên mới cần chống trùng.

> **Tóm gọn 1 câu:** Hai ca thực tế cho thấy cả bài học trong module dùng được ra sao: refactor lớn thì chia tầng + chặn phê duyệt + chống trùng retry, còn 30 test hên xui thì chia shard chạy song song, retry lỗi tạm thời và gom kết quả cuối.

## 15. Thực Hành (Hands-On Lab)

Tới giờ thực tập rồi — coi như ca trực 30 phút của bạn:

**Bài tập (30 phút):** thử làm bác sĩ trực với `schedule + execute` cho 6 ca bệnh (A→B, A→C, B+D→E, C→F), trong đó budget là `[2k,3k,3k,5k,2k,2k]`, trần session 10k, `D: elevated`, `E: timeout 5s`.
1. Chia các batch theo topo; chỉ ra batch nào phải đứng chờ phê duyệt và batch nào bị hoãn vì cạn budget.
2. Giả vờ E timeout một lần — hãy retry bằng idempotency-key, rồi ghi lại event `trajectoryId` + `transition`.
3. Gắn thêm `race()` cho C (so kèo cache với live) và `join()` cho E/F. Nộp bài gồm: bảng batch + event log + 1 đoạn văn ngắn kể lại điều gì phải dời sang session 2 và vì sao.

Giải thích đề bài: **A→B, A→C** nghĩa là B và C chỉ được làm khi A xong; **B+D→E** nghĩa là E phải đợi cả B lẫn D; **trần session 10k** = tổng ngân sách token cả phiên chỉ 10,000; **D: elevated** = D là việc nhạy cảm, phải chờ phê duyệt; **E: timeout 5s** = E hẹn giờ 5 giây, quá giờ là coi như hỏng.

> **Tóm gọn 1 câu:** Bài lab 30 phút cho bạn tự tay xếp đợt theo topo, xử lý phê duyệt, cạn ngân sách, timeout và retry — làm xong là hiểu hết toàn bộ cơ chế task engine.

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

Đọc ví dụ cụ thể: quy tắc **1 (ONE TASK = ONE RESPONSIBILITY)** là một task chỉ làm đúng một việc — dễ đo chi phí, dễ theo dõi, dễ duyệt; quy tắc **2 (SIZE MATTERS)** là task lý tưởng tốn 100-5,000 tokens — nhỏ hơn thế thì phí giấy mực quản lý, to hơn thế thì dễ hỏng; quy tắc **7 (FAIL GRACEFULLY)** là task hỏng thì ghi rõ lý do rồi retry hoặc bỏ qua, tuyệt đối không để một task hỏng chặn đứng cả dây chuyền.

> **Tóm gọn 1 câu:** 12 nguyên tắc vàng của task management — một việc một task, kích thước vừa phải, trạng thái nhìn thấy được, phụ thuộc ghi rõ, đếm token, có tiêu chí nghiệm thu và phát hiện lỗi sớm — làm theo là phần lớn rủi ro tự tan.

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

Từng nguồn để làm gì, giải thích ngắn: **LangGraph** là thư viện dựng workflow cho agent của LangChain — tham khảo cách quản lý trạng thái; **CrewAI** là framework chia việc cho nhiều agent — tham khảo cách giao task; **Eisenhower Matrix** là phương pháp xếp ưu tiên nổi tiếng — nền tảng của Priority Model ở mục 3; **Refactoring của Martin Fowler** là cuốn sách kinh điển về cải thiện code — nền tảng của Refactoring Workflow; **Google Engineering Practices** là bộ chuẩn code review của Google — tham khảo tiêu chí chất lượng; **tiktoken** là thư viện đếm token của OpenAI — dùng để ước lượng token chính xác hơn bảng kinh nghiệm ở mục 7.

> **Tóm gọn 1 câu:** Danh sách 6 nguồn tham khảo gốc — muốn đào sâu phần nào (ưu tiên, refactor, đếm token) thì mở đúng nguồn tương ứng.