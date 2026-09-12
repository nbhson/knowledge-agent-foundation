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

Hãy tưởng tượng bạn là **quản lý một bệnh viện đa khoa**. Mỗi ngày, hàng trăm bệnh nhân đến: người đau bụng cấp tính, người cần khám định kỳ, người muốn tiêm vaccine. Nếu bạn **không phân loại** — bệnh nhân cấp cứu phải xếp sau người khám thường — hậu quả sẽ là **thảm họa**.

**AI Agent cũng gặp vấn đề tương tự khi không có Task Management.**

Khi user gửi một yêu cầu phức tạp như *"Refactor module auth, thêm test, update docs, rồi deploy"* — agent nhận **tất cả cùng lúc** nhưng không biết bắt đầu từ đâu, cái nào ưu tiên, cái nào có thể song song. Kết quả: làm lộn xộn, bỏ sót bước, hoặc worse — **deploy code chưa test**.

**Giải pháp**: Structured Task Management — một hệ thống phân loại, ưu tiên, phân nhỏ, và theo dõi tasks để agent **làm đúng việc, đúng lúc, đúng thứ tự**.

### Tại Sao Task Management Quan Trọng?

> *"Agent không quản lý task giống như đầu bếp nhận 100 món cùng lúc — nhận hết nhưng nấu không kịp, món nào cũng dở."*

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

**Analogies**: Task management giống quản lý bệnh viện — phân loại bệnh nhân (classify), ưu tiên cấp cứu (prioritize), kê toa (plan), theo dõi điều trị (track), và xuất viện (complete).

**Nếu bỏ qua**: Agent overwhelm bởi quá nhiều tasks, deliver sai thứ tự, lãng phí compute resources, và user frustration.

## Tổng Quan

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task Management trong AI coding là quá trình phân loại, chia nhỏ, ưu tiên và theo dõi các tác vụ lập trình để agent làm đúng việc, đúng lúc, đúng thứ tự.
>
> **Ẩn dụ/so sánh:** Giống quản lý một bệnh viện bận rộn — phải xếp ca cấp cứu trước, hẹn khám thường sau, phân kíp trực rõ ràng thì bệnh nhân mới không bị bỏ sót.
>
> **Vì sao quan trọng:** Không quản lý task, agent dễ bị quá tải, làm sai thứ tự và lãng phí tài nguyên.

**Task Management** trong AI coding là quá trình **phân tích, chia nhỏ, ưu tiên và theo dõi** các tác vụ coding. Task tốt giúp AI agent tập trung vào đúng việc, tránh overload, và deliver kết quả chất lượng.

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
> **Khái niệm:** Đây là mục lục của toàn module — mười chủ đề chính của Task Management được trình bày từ nhận diện task (phân loại, phân rã), điều hành (ưu tiên, trạng thái, phụ thuộc) đến quản lý nguồn lực (ước lượng, token budget).
>
> **Ẩn dụ/so sánh:** Giống bản đồ tuyến tàu điện ngầm — nhìn trước là biết có những ga nào và nên xuống ở đâu cho mục tiêu của bạn.
>
> **Vì sao quan trọng:** Mỗi chủ đề giải quyết một phần của cùng một bài toán, nên nắm tổng thể sẽ dễ định hướng việc cần học.

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
> **Khái niệm:** Task Classification là bước "chẩn đoán" task trước khi xử lý — đọc yêu cầu, nhận diện task thuộc loại nào (viết code mới, sửa bug, refactor, viết test v.v.) và độ phức tạp ra sao (1 file hay nguyên module), rồi chọn chiến lược phù hợp.
>
> **Ẩn dụ/so sánh:** Giống bác sĩ cấp cứu phân loại bệnh nhân (triage) trước khi điều trị — chẩn đoán đúng thì mới xử lý đúng, còn chẩn đoán sai thì mọi bước tiếp theo đều lệch.
>
> **Vì sao quan trọng:** Phân loại đúng giúp agent chọn đúng cách tiếp cận, tiết kiệm token và giảm sai sót ngay từ đầu.

### 1.1 Phân Loại Task Coding

Sơ đồ dưới tóm tắt hệ thống phân loại task coding theo 5 nhóm chính — mỗi nhóm là một "chuyên khoa" khác nhau (viết code mới, sửa code, phân tích code, tài liệu, test). Hãy đọc như một cây phân cấp: từ nhóm lớn ở trên, theo nhánh xuống loại task cụ thể, để biết task bạn đang gặp nằm ở đâu.

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

Đoạn code dưới là bộ máy phân loại thật sự: nó nhận vào mô tả task bằng ngôn ngữ tự nhiên, dò keyword patterns (ví dụ thấy chữ "fix" hay "bug" thì xếp vào nhóm MODIFICATION), rồi ước lượng độ phức tạp để trả về một đối tượng Task đầy đủ thông tin. Chạy thử với một câu mô tả bất kỳ để xem cách agent "hiểu" yêu cầu như thế nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
import re

class TaskCategory(Enum):
    GENERATION = "generation"
    MODIFICATION = "modification"
    ANALYSIS = "analysis"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    UNKNOWN = "unknown"

class TaskComplexity(Enum):
    TRIVIAL = 1     # 1 file, < 50 LOC
    SIMPLE = 2      # 1-2 files, < 200 LOC
    MODERATE = 3    # 3-5 files, 200-500 LOC
    COMPLEX = 4     # 5-15 files, 500-2000 LOC
    EPIC = 5        # 15+ files, 2000+ LOC


@dataclass
class Task:
    """Đại diện cho một coding task"""
    id: str
    title: str
    description: str
    category: TaskCategory = TaskCategory.UNKNOWN
    complexity: TaskComplexity = TaskComplexity.SIMPLE
    priority: int = 5                    # 1=highest, 10=lowest
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_tokens: int = 0
    files_involved: List[str] = field(default_factory=list)


class TaskClassifier:
    """
    Phân loại task tự động dựa trên keywords và patterns.
    
    Usage:
        classifier = TaskClassifier()
        task = classifier.classify(
            "Fix the authentication bug in login handler"
        )
        print(task.category)  # TaskCategory.MODIFICATION
        print(task.complexity)  # TaskComplexity.SIMPLE
    """
    
    PATTERNS = {
        TaskCategory.GENERATION: [
            r"tạo|create|generate|build|new|thêm|add",
            r"function|class|component|endpoint|api",
            r"from scratch|từ đầu|mới",
        ],
        TaskCategory.MODIFICATION: [
            r"sửa|fix|bug|error|broken",
            r"refactor|cải thiện|improve|optimize",
            r"thay đổi|change|update|migrate",
        ],
        TaskCategory.ANALYSIS: [
            r"kiểm tra|check|review|analyze|inspect",
            r"tìm|find|debug|trace|profile",
            r"security|audit|vulnerability",
        ],
        TaskCategory.DOCUMENTATION: [
            r"viết docs|write.*doc|readme|changelog",
            r"document|tài liệu|hướng dẫn|guide",
            r"comment|annotate",
        ],
        TaskCategory.TESTING: [
            r"test|viết test|write.*test|spec",
            r"mock|fixture|assert|coverage",
            r"integration|e2e|unit test",
        ],
    }
    
    COMPLEXITY_SIGNALS = {
        TaskComplexity.TRIVIAL: [
            r"1 dòng|one line|typo|formatting",
            r"rename|đổi tên|thay màu",
        ],
        TaskComplexity.SIMPLE: [
            r"fix.*bug|sửa lỗi đơn",
            r"thêm field|add field|add property",
            r"1 file|single file",
        ],
        TaskComplexity.MODERATE: [
            r"feature|tính năng|feature mới",
            r"refactor|cải trúc|restructure",
            r"multi.?file|nhiều file",
        ],
        TaskComplexity.COMPLEX: [
            r"module|system|hệ thống|architecture",
            r"migration|di chuyển|migrate",
            r"performance.*optimization|tối ưu lớn",
        ],
        TaskComplexity.EPIC: [
            r"redesign|thiết kế lại|rebuild",
            r"major.*overhaul|nâng cấp lớn",
            r"multiple.*module|nhiều module",
        ],
    }
    
    def classify(self, text: str) -> Task:
        text_lower = text.lower()
        
        # Classify category
        category_scores = {}
        for cat, patterns in self.PATTERNS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            category_scores[cat] = score
        
        category = max(category_scores, 
                      key=category_scores.get,
                      default=TaskCategory.UNKNOWN)
        if category_scores.get(category, 0) == 0:
            category = TaskCategory.UNKNOWN
        
        # Classify complexity
        complexity_scores = {}
        for comp, patterns in self.COMPLEXITY_SIGNALS.items():
            score = sum(
                1 for p in patterns 
                if re.search(p, text_lower)
            )
            complexity_scores[comp] = score
        
        complexity = max(complexity_scores,
                        key=complexity_scores.get,
                        default=TaskComplexity.SIMPLE)
        if complexity_scores.get(complexity, 0) == 0:
            complexity = TaskComplexity.SIMPLE
        
        return Task(
            id=f"task-{hash(text) % 10000:04d}",
            title=text[:100],
            description=text,
            category=category,
            complexity=complexity,
        )
```

</details>

### 1.3 Decision Tree: Chọn Strategy Xử Lý Task

Sơ đồ dưới mô tả luật ra quyết định khi một task được giao tới: nếu yêu cầu chưa rõ thì phải hỏi rõ trước, nếu nhỏ hơn 500 tokens thì làm luôn, còn nếu lớn thì phân rã thành sub-task rồi chọn chiến lược chạy tuần tự, song song hay theo TDD. Đi theo các mũi tên từ trên xuống để biết agent sẽ "đi cửa nào" cho từng loại task.

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
> **Khái niệm:** Task Decomposition là kỹ thuật chia một task lớn, khó nuốt thành nhiều subtask nhỏ, mỗi subtask có input/output gần như độc lập và có thể giao cho agent phù hợp xử lý riêng.
>
> **Ẩn dụ/so sánh:** Giống xây nhà — không ai đổ cả căn nhà một lần, mà phải làm móng, dựng khung, lợp mái theo từng giai đoạn; mỗi giai đoạn là một việc nhỏ dễ kiểm soát.
>
> **Vì sao quan trọng:** Task lớn dễ làm agent mất context và bỏ sót bước; chia nhỏ giúp giảm tải context và tăng xác suất hoàn thành.

### 2.1 Patterns Phân Rã Task

Sơ đồ dưới liệt kê 6 kiểu phân rã task phổ biến. Điểm khác nhau nằm ở cách các subtask liên hệ với nhau: chạy nối tiếp theo thứ tự bắt buộc (sequential), chạy song song rồi gộp kết quả (parallel, map-reduce), hay phân cấp cha-con (hierarchical). Nhìn các mũi tên trong hình để chọn pattern phù hợp với loại việc bạn đang làm.

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

Đây là code triển khai bộ phân rã: đối tượng TaskDecomposer nhận vào một Task và tự chọn chiến lược phân rã (feature, layer, file, TDD, vertical slice, spike) rồi trả về danh sách SubTask có thứ tự, dependency, token ước lượng và tiêu chí kiểm tra. Nếu không biết chọn gì, nó tự gợi ý dựa trên loại và độ phức tạp của task.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class SubTask:
    """Sub-task con trong task decomposition"""
    id: str
    title: str
    description: str
    order: int
    parallel: bool = False
    estimated_tokens: int = 0
    dependencies: List[str] = field(default_factory=list)
    files_to_modify: List[str] = field(default_factory=list)
    verification_criteria: str = ""


class TaskDecomposer:
    """
    Phân rã task lớn thành các sub-task có thể thực hiện riêng.
    
    Strategies:
    - feature-based: Chia theo tính năng
    - layer-based: Chia theo layer (UI, API, DB)
    - file-based: Chia theo file
    - test-driven: Viết test trước, rồi code
    - vertical-slice: Mỗi slice = full stack working increment
    - spike-then-execute: Research trước, rồi implement
    """
    
    def decompose(self, task: Task, strategy: str = "auto",
                  project_context: Dict = None) -> List[SubTask]:
        """Phân rã task thành sub-tasks"""
        
        if strategy == "auto":
            strategy = self._suggest_strategy(task, project_context)
        
        if strategy == "feature":
            return self._decompose_by_feature(task)
        elif strategy == "layer":
            return self._decompose_by_layer(task)
        elif strategy == "file":
            return self._decompose_by_file(task)
        elif strategy == "tdd":
            return self._decompose_tdd(task)
        elif strategy == "vertical_slice":
            return self._decompose_vertical_slice(task)
        elif strategy == "spike":
            return self._decompose_spike(task)
        else:
            return self._decompose_by_feature(task)
    
    def _suggest_strategy(self, task: Task, 
                          context: Dict = None) -> str:
        """Gợi ý strategy phù hợp dựa trên task characteristics"""
        context = context or {}
        
        # Trivial tasks - don't decompose
        if task.complexity.value <= 1:
            return "simple"
        
        # Test-related tasks
        if "test" in task.description.lower():
            return "tdd"
        
        # Generation tasks - feature-based
        if task.category == TaskCategory.GENERATION:
            if len(task.files_involved) > 3:
                return "vertical_slice"
            return "feature"
        
        # Modification tasks - file-based or layer-based
        if task.category == TaskCategory.MODIFICATION:
            if len(task.files_involved) > 5:
                return "layer"
            return "file"
        
        # Complex/uncertain tasks - spike first
        if task.complexity.value >= 4:
            if context.get("uncertain_approach", False):
                return "spike"
            return "layer"
        
        return "feature"
    
    def _decompose_by_feature(self, task: Task) -> List[SubTask]:
        """Chia theo tính năng — full workflow"""
        subtasks = []
        
        subtasks.append(SubTask(
            id=f"{task.id}-01",
            title="Phân tích yêu cầu",
            description=f"Đọc và hiểu yêu cầu: {task.description}",
            order=1,
            estimated_tokens=500,
            verification_criteria="Có danh sách requirements rõ ràng",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-02",
            title="Đọc code hiện tại",
            description="Xem codebase liên quan để hiểu context",
            order=2,
            dependencies=[f"{task.id}-01"],
            estimated_tokens=1500,
            verification_criteria="Đã identify affected files và patterns",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-03",
            title="Lên kế hoạch thay đổi",
            description="Xác định files cần sửa và cách tiếp cận",
            order=3,
            dependencies=[f"{task.id}-02"],
            estimated_tokens=800,
            verification_criteria="Có plan cụ thể với file list và approach",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-04",
            title="Triển khai code",
            description="Viết code theo kế hoạch",
            order=4,
            dependencies=[f"{task.id}-03"],
            estimated_tokens=task.estimated_tokens or 3000,
            verification_criteria="Code đã viết xong, không có syntax errors",
        ))
        
        subtasks.append(SubTask(
            id=f"{task.id}-05",
            title="Kiểm tra & validate",
            description="Chạy test, lint, review kết quả",
            order=5,
            dependencies=[f"{task.id}-04"],
            estimated_tokens=1000,
            verification_criteria="Tests pass, lint clean, no regressions",
        ))
        
        return subtasks
    
    def _decompose_by_layer(self, task: Task) -> List[SubTask]:
        """Chia theo layer: DB → Service → API → UI"""
        return [
            SubTask(f"{task.id}-db", "Database layer",
                    "Thay đổi schema, queries, migrations", 1,
                    estimated_tokens=1500,
                    verification_criteria="Schema updated, migrations run"),
            SubTask(f"{task.id}-svc", "Service layer",
                    "Business logic, validation", 2,
                    dependencies=[f"{task.id}-db"],
                    estimated_tokens=2000,
                    verification_criteria="Service logic complete, unit tests pass"),
            SubTask(f"{task.id}-api", "API layer",
                    "Endpoints, request/response, error handling", 3,
                    dependencies=[f"{task.id}-svc"],
                    estimated_tokens=1500,
                    verification_criteria="API endpoints working, OpenAPI spec updated"),
            SubTask(f"{task.id}-ui", "UI layer",
                    "Frontend components, forms, display", 4,
                    dependencies=[f"{task.id}-api"],
                    estimated_tokens=2000,
                    verification_criteria="UI renders correctly, forms submit"),
            SubTask(f"{task.id}-test", "Integration tests",
                    "End-to-end flow tests", 5,
                    dependencies=[f"{task.id}-ui"],
                    estimated_tokens=1500,
                    verification_criteria="All integration tests pass"),
        ]
    
    def _decompose_by_file(self, task: Task) -> List[SubTask]:
        """Chia theo file — mỗi file là 1 sub-task"""
        subtasks = []
        for i, filepath in enumerate(task.files_involved, 1):
            subtasks.append(SubTask(
                id=f"{task.id}-f{i:02d}",
                title=f"Modify {filepath}",
                description=f"Thay đổi file {filepath}",
                order=i,
                files_to_modify=[filepath],
                parallel=True,
                estimated_tokens=1000,
                verification_criteria=f"File {filepath} updated correctly",
            ))
        return subtasks
    
    def _decompose_tdd(self, task: Task) -> List[SubTask]:
        """Test-Driven Development decomposition"""
        return [
            SubTask(f"{task.id}-test-design", "Thiết kế test cases",
                    "Viết test cases dựa trên requirements", 1,
                    estimated_tokens=1000,
                    verification_criteria="Test cases cover all scenarios"),
            SubTask(f"{task.id}-test-write", "Viết tests",
                    "Viết test code (sẽ fail lúc đầu)", 2,
                    dependencies=[f"{task.id}-test-design"],
                    estimated_tokens=1500,
                    verification_criteria="Tests compile, run, and fail (RED)"),
            SubTask(f"{task.id}-impl", "Triển khai code",
                    "Viết code để pass tests", 3,
                    dependencies=[f"{task.id}-test-write"],
                    estimated_tokens=task.estimated_tokens or 2000,
                    verification_criteria="All tests pass (GREEN)"),
            SubTask(f"{task.id}-refactor", "Refactor",
                    "Cải thiện code quality", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1000,
                    verification_criteria="Code clean, tests still pass"),
        ]
    
    def _decompose_vertical_slice(self, task: Task) -> List[SubTask]:
        """Vertical slice — mỗi slice = full stack working feature"""
        return [
            SubTask(f"{task.id}-slice-core", "Core slice",
                    "Implement core logic + minimal API", 1,
                    estimated_tokens=3000,
                    verification_criteria="Core flow works end-to-end"),
            SubTask(f"{task.id}-slice-data", "Data slice",
                    "Database + repository layer", 2,
                    dependencies=[f"{task.id}-slice-core"],
                    estimated_tokens=2000,
                    verification_criteria="Data persistence working"),
            SubTask(f"{task.id}-slice-api", "API slice",
                    "Full API with validation + error handling", 3,
                    dependencies=[f"{task.id}-slice-data"],
                    estimated_tokens=2000,
                    verification_criteria="All API endpoints functional"),
            SubTask(f"{task.id}-slice-ui", "UI slice",
                    "Frontend integration", 4,
                    dependencies=[f"{task.id}-slice-api"],
                    estimated_tokens=2500,
                    verification_criteria="UI fully functional"),
            SubTask(f"{task.id}-slice-test", "Test slice",
                    "Integration + E2E tests", 5,
                    dependencies=[f"{task.id}-slice-ui"],
                    estimated_tokens=2000,
                    verification_criteria="Full test coverage"),
        ]
    
    def _decompose_spike(self, task: Task) -> List[SubTask]:
        """Spike-then-execute — research trước khi implement"""
        return [
            SubTask(f"{task.id}-spike", "Spike: Research & Decide",
                    "Timebox 1-2h research, compare approaches", 1,
                    estimated_tokens=3000,
                    verification_criteria="Chosen approach documented with rationale"),
            SubTask(f"{task.id}-poc", "Proof of Concept",
                    "Minimal implementation to validate approach", 2,
                    dependencies=[f"{task.id}-spike"],
                    estimated_tokens=2000,
                    verification_criteria="POC works, approach validated"),
            SubTask(f"{task.id}-impl", "Full Implementation",
                    "Implement complete solution", 3,
                    dependencies=[f"{task.id}-poc"],
                    estimated_tokens=task.estimated_tokens or 4000,
                    verification_criteria="Feature complete"),
            SubTask(f"{task.id}-validate", "Validation",
                    "Test, review, verify", 4,
                    dependencies=[f"{task.id}-impl"],
                    estimated_tokens=1500,
                    verification_criteria="All tests pass, code reviewed"),
        ]
```

</details>

---

## 3. Priority & Scheduling

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Priority & Scheduling là cơ chế quyết định task nào làm trước, task nào làm sau dựa trên mức khẩn cấp, tầm quan trọng, công sức cần bỏ ra và lượng token tiêu thụ.
>
> **Ẩn dụ/so sánh:** Giống xếp hàng ở bệnh viện — ca cấp cứu vào trước, ca khám thường chờ sau; việc nhỏ mà giá trị cao (quick win) cũng được ưu tiên như giải quyết món nợ nhỏ để giải phóng ngân quỹ.
>
> **Vì sao quan trọng:** Làm sai thứ tự sẽ khiến việc quan trọng bị trễ, tốn token và dễ bỏ sót yêu cầu của user.

### 3.1 Priority Model

Đoạn code dưới thể hiện cách tính điểm ưu tiên cho từng task bằng công thức kiểu Eisenhower Matrix: mỗi task được chấm urgency (khẩn cấp), importance (quan trọng), effort (công sức cần bỏ ra), rồi cộng thêm khoản bonus nếu đó là việc nhỏ dễ làm (quick win) hoặc nhiều task khác đang phụ thuộc nó. TaskScheduler sau đó xếp tasks vào từng batch vừa đúng thứ tự vừa không vượt ngân sách token mỗi phiên.

Nói nôm na, đây giống thang điểm xếp hàng: việc khẩn cấp và quan trọng thì điểm cao, việc to mà không gấp thì xếp sau, việc nho nhỏ dễ làm được ưu tiên để "quét bàn" cho nhanh.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class PriorityScore:
    """Score tính toán cho priority — Eisenhower Matrix + dependency bonus"""
    urgency: int        # 1-5: mức độ khẩn cấp
    importance: int     # 1-5: mức độ quan trọng
    effort: int         # 1-5: effort cần thiết (thấp = score cao)
    dependency_count: int  # Số tasks phụ thuộc vào task này
    
    @property
    def total(self) -> float:
        """Weighted score với quick-wins bonus"""
        base = self.urgency * 0.4 + self.importance * 0.4
        effort_bonus = (6 - self.effort) * 0.1   # Quick wins bonus
        dep_bonus = min(self.dependency_count * 0.1, 0.3)
        return base + effort_bonus + dep_bonus


class TaskScheduler:
    """
    Lên lịch tasks dựa trên priority, dependency, và token budget.
    
    Rules:
    1. Luôn làm task có dependency cao trước
    2. Quick wins (thấp effort, cao priority) nên làm trước
    3. Respect token budget per session
    """
    
    def __init__(self, max_tokens_per_session: int = 50000):
        self.max_tokens = max_tokens_per_session
    
    def schedule(self, tasks: List[Task]) -> List[List[Task]]:
        """
        Tạo lịch thực hiện — trả về list các batch.
        Mỗi batch là nhóm tasks có thể chạy cùng lúc.
        """
        # Sort by priority score descending
        scored = [(t, self._score(t)) for t in tasks]
        scored.sort(key=lambda x: x[1].total, reverse=True)
        
        batches = []
        current_batch = []
        current_tokens = 0
        
        for task, score in scored:
            task_tokens = task.estimated_tokens or 1000
            
            if current_tokens + task_tokens > self.max_tokens:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [task]
                current_tokens = task_tokens
            else:
                current_batch.append(task)
                current_tokens += task_tokens
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _score(self, task: Task) -> PriorityScore:
        """Tính priority score cho task"""
        effort = task.complexity.value
        urgency = max(1, 6 - task.priority)
        
        importance_map = {
            TaskCategory.MODIFICATION: 5,   # Bug fix = high
            TaskCategory.TESTING: 4,
            TaskCategory.GENERATION: 3,
            TaskCategory.ANALYSIS: 3,
            TaskCategory.DOCUMENTATION: 2,
        }
        importance = importance_map.get(task.category, 3)
        
        return PriorityScore(
            urgency=urgency,
            importance=importance,
            effort=effort,
            dependency_count=len(task.dependencies),
        )
```

</details>

---

## 4. Task State Management

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Task State Management là cách theo dõi vòng đời của từng task qua các trạng thái như pending, running, blocked, done — kèm cơ chế lưu lại và khôi phục trạng thái để lúc nào cũng biết "công việc đang dở đến đâu" khi bị gián đoạn.
>
> **Ẩn dụ/so sánh:** Giống cuốn sổ trực của bệnh viện — ca trực nào cũng đọc được tai nạn nói gì, bệnh nhân đang ở giai đoạn nào, rồi làm tiếp từ đó thay vì hỏi lại từ đầu.
>
> **Vì sao quan trọng:** Nếu không biết task đang ở trạng thái nào, agent không thể tiếp tục công việc sau khi gián đoạn và dễ làm lặp hoặc bỏ sót công đoạn.

### 4.1 Task Lifecycle

Sơ đồ dưới là bản đồ trạng thái của một task từ lúc sinh ra đến lúc kết thúc: PENDING → PLANNING → IN_PROGRESS → TESTING → REVIEW → DONE. Ngoài nhánh chính còn có các lối rẽ đặc biệt — BLOCKED (bị chặn thì quay về chờ), FAILED (thất bại thì làm lại), CANCELLED (hủy). Đọc theo mũi tên để hiểu task đi từ trạng thái nào sang trạng thái nào là hợp lệ.

Nói cho dễ hình dung, đây là "hành trình một task qua các khoa": vừa tạo là chờ khám (PENDING), được lên kế hoạch (PLANNING), đang điều trị (IN_PROGRESS), đang xét nghiệm (TESTING), đang hội chẩn (REVIEW), rồi xuất viện (DONE).

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

Đây là code quản lý trạng thái: TaskStateManager giữ "sổ theo dõi" cho mọi task, chỉ cho phép chuyển trạng thái khi hợp lệ (valid transitions), ghi lại thời gian bắt đầu, số lần thử, lỗi cuối cùng và phát sự kiện để phần khác của hệ thống biết mà phản hồi. Nếu bạn cố chuyển trạng thái trái phép (ví dụ TESTING → PENDING), code sẽ báo lỗi ngay — giống lệ phòng khám không cho làm liều.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    TESTING = "testing"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskState:
    """Trạng thái hiện tại của task"""
    task_id: str
    status: TaskStatus = TaskStatus.PENDING
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: float = 0.0        # 0.0 → 1.0
    attempts: int = 0
    last_error: Optional[str] = None
    notes: List[str] = field(default_factory=list)


class TaskStateManager:
    """
    Quản lý lifecycle của tasks — tracks status changes,
    enforces valid transitions, và emits events.
    """
    
    VALID_TRANSITIONS = {
        TaskStatus.PENDING: [
            TaskStatus.PLANNING, TaskStatus.CANCELLED
        ],
        TaskStatus.PLANNING: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED
        ],
        TaskStatus.IN_PROGRESS: [
            TaskStatus.TESTING, TaskStatus.BLOCKED,
            TaskStatus.FAILED, TaskStatus.DONE,
        ],
        TaskStatus.BLOCKED: [
            TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED,
            TaskStatus.PENDING,
        ],
        TaskStatus.TESTING: [
            TaskStatus.REVIEW, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.REVIEW: [
            TaskStatus.DONE, TaskStatus.IN_PROGRESS,
            TaskStatus.FAILED,
        ],
        TaskStatus.FAILED: [
            TaskStatus.PENDING, TaskStatus.CANCELLED,
        ],
    }
    
    def __init__(self):
        self.states: Dict[str, TaskState] = {}
        self.listeners: List[Callable] = []
    
    def create(self, task_id: str) -> TaskState:
        state = TaskState(task_id=task_id)
        self.states[task_id] = state
        return state
    
    def transition(self, task_id: str, new_status: TaskStatus,
                   note: str = "") -> TaskState:
        """Chuyển trạng thái task — kiểm tra validity"""
        state = self.states.get(task_id)
        if not state:
            raise ValueError(f"Task {task_id} not found")
        
        valid = self.VALID_TRANSITIONS.get(state.status, [])
        if new_status not in valid:
            raise InvalidTransitionError(
                f"Cannot transition from {state.status.value} "
                f"to {new_status.value}"
            )
        
        old_status = state.status
        state.status = new_status
        
        if new_status == TaskStatus.IN_PROGRESS and not state.started_at:
            state.started_at = datetime.now().isoformat()
            state.attempts += 1
        
        if new_status in (TaskStatus.DONE, TaskStatus.FAILED, 
                         TaskStatus.CANCELLED):
            state.completed_at = datetime.now().isoformat()
        
        if note:
            state.notes.append(
                f"[{datetime.now().isoformat()}] {note}"
            )
        
        # Notify listeners
        for listener in self.listeners:
            listener(task_id, old_status, new_status)
        
        return state
    
    def on_transition(self, callback: Callable):
        self.listeners.append(callback)


class InvalidTransitionError(Exception):
    pass
```

</details>

---

## 5. Dependency Management

> ## 📌 Khái Niệm Cơ Bản
>
> **Khái niệm:** Dependency Management là cách mô hình hóa quan hệ "task này phải xong trước task kia" bằng một đồ thị phụ thuộc (dependency graph), từ đó tính ra thứ tự thực thi đúng và phát hiện vòng lặp chết (deadlock).
>
> **Ẩn dụ/so sánh:** Giống thứ tự nấu một bữa ăn nhiều món — phải ninh canh trước, xào sau, vì món này cần nguyên liệu của món kia; làm ngược thứ tự thì bữa ăn vỡ trận.
>
> **Vì sao quan trọng:** Làm sai thứ tự hoặc để hai task chờ nhau vô hạn sẽ làm agent tắc nghẽn và không bao giờ hoàn thành.

### 5.1 Task Dependency Graph

Đoạn code dưới triển khai DAG (Directed Acyclic Graph) để quản lý dependency. Quy ước đọc rất đơn giản: "A → B" nghĩa là task A phải xong trước task B mới được bắt đầu. Lớp này hỗ trợ kiểm tra vòng lặp (cycle detection), sắp xếp thứ tự thực thi (topological sort) và tách các nhóm task chạy được song song (parallel groups).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from collections import defaultdict, deque
from typing import List, Dict, Set, Optional

class TaskDependencyGraph:
    """
    Directed Acyclic Graph (DAG) cho task dependencies.
    
    Features:
    - Thêm/bỏ dependencies
    - Topological sort (execution order)
    - Parallel groups (tasks chạy cùng lúc)
    - Cycle detection
    """
    
    def __init__(self):
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
        for dep_id in task.dependencies:
            self.adj[dep_id].add(task.id)
    
    def has_cycle(self) -> bool:
        """DFS-based cycle detection"""
        visited = set()
        in_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            in_stack.add(node)
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in in_stack:
                    return True
            in_stack.discard(node)
            return False
        
        return any(dfs(t) for t in self.tasks if t not in visited)
    
    def topological_sort(self) -> List[str]:
        """Trả về execution order (topological sort)"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        queue = deque([t for t, d in in_degree.items() if d == 0])
        order = []
        
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(order) != len(self.tasks):
            raise ValueError("Cycle detected in task dependencies")
        
        return order
    
    def parallel_groups(self) -> List[List[str]]:
        """Tách thành các nhóm có thể chạy song song"""
        in_degree = {t: 0 for t in self.tasks}
        for node in self.adj:
            for neighbor in self.adj[node]:
                in_degree[neighbor] += 1
        
        groups = []
        remaining = dict(in_degree)
        
        while remaining:
            ready = [t for t, d in remaining.items() if d == 0]
            if not ready:
                raise ValueError("Unresolvable dependency cycle")
            
            groups.append(ready)
            
            for task_id in ready:
                del remaining[task_id]
                for neighbor in self.adj[task_id]:
                    if neighbor in remaining:
                        remaining[neighbor] -= 1
        
        return groups
```

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

```python
TASK_TEMPLATES = {
    "bug_fix": {
        "title": "Fix: {bug_description}",
        "subtasks": [
            {"title": "Reproduce the bug", "tokens": 500},
            {"title": "Read and understand affected code", "tokens": 1000},
            {"title": "Identify root cause", "tokens": 800},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Write regression test", "tokens": 1000},
            {"title": "Verify fix in all scenarios", "tokens": 500},
        ],
        "estimated_total_tokens": 5300,
    },
    
    "new_feature": {
        "title": "Feature: {feature_name}",
        "subtasks": [
            {"title": "Analyze requirements", "tokens": 500},
            {"title": "Read existing code patterns", "tokens": 1000},
            {"title": "Design approach", "tokens": 800},
            {"title": "Implement core logic", "tokens": 3000},
            {"title": "Add error handling", "tokens": 800},
            {"title": "Write tests", "tokens": 1500},
            {"title": "Update documentation", "tokens": 500},
        ],
        "estimated_total_tokens": 8100,
    },
    
    "code_review": {
        "title": "Review: {target}",
        "subtasks": [
            {"title": "Read all changed files", "tokens": 2000},
            {"title": "Check code style & conventions", "tokens": 500},
            {"title": "Analyze logic & correctness", "tokens": 1500},
            {"title": "Review for security issues", "tokens": 1000},
            {"title": "Write review comments", "tokens": 1000},
        ],
        "estimated_total_tokens": 6000,
    },
    
    "refactor": {
        "title": "Refactor: {target_module}",
        "subtasks": [
            {"title": "Analyze current structure", "tokens": 1000},
            {"title": "Identify code smells", "tokens": 800},
            {"title": "Plan refactoring steps", "tokens": 500},
            {"title": "Extract functions/classes", "tokens": 2000},
            {"title": "Update imports & references", "tokens": 1000},
            {"title": "Run existing tests", "tokens": 500},
            {"title": "Verify behavior unchanged", "tokens": 500},
        ],
        "estimated_total_tokens": 6300,
    },
    
    "debug_investigation": {
        "title": "Debug: {issue_description}",
        "subtasks": [
            {"title": "Gather error info and logs", "tokens": 800},
            {"title": "Read stack trace and affected files", "tokens": 1500},
            {"title": "Add strategic logging/breakpoints", "tokens": 1000},
            {"title": "Reproduce with minimal test case", "tokens": 800},
            {"title": "Identify root cause", "tokens": 1000},
            {"title": "Implement fix", "tokens": 1500},
            {"title": "Add regression test", "tokens": 800},
        ],
        "estimated_total_tokens": 7400,
    },
    
    "performance_optimization": {
        "title": "Optimize: {target}",
        "subtasks": [
            {"title": "Profile current performance", "tokens": 1000},
            {"title": "Identify bottlenecks", "tokens": 800},
            {"title": "Research optimization strategies", "tokens": 1000},
            {"title": "Implement optimizations", "tokens": 2000},
            {"title": "Benchmark before/after", "tokens": 800},
            {"title": "Verify no regressions", "tokens": 500},
        ],
        "estimated_total_tokens": 6100,
    },
    
    "migration": {
        "title": "Migrate: {source} → {target}",
        "subtasks": [
            {"title": "Analyze source and target", "tokens": 1500},
            {"title": "Create migration plan", "tokens": 800},
            {"title": "Write migration scripts", "tokens": 2000},
            {"title": "Test migration on sample data", "tokens": 1000},
            {"title": "Run full migration", "tokens": 1500},
            {"title": "Verify and cleanup", "tokens": 800},
        ],
        "estimated_total_tokens": 7600,
    },
}


def create_task_from_template(template_name: str, **kwargs) -> Task:
    """Tạo task từ template"""
    template = TASK_TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")
    
    title = template["title"].format(**kwargs)
    
    return Task(
        id=f"task-{hash(title) % 10000:04d}",
        title=title,
        description=f"Task from template: {template_name}",
        category=TaskCategory.UNKNOWN,
        estimated_tokens=template["estimated_total_tokens"],
    )
```

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

```python
from enum import Enum
from typing import Dict, List, Tuple

class EffortEstimator:
    """
    ước lượng effort cho coding tasks dựa trên historical data
    và task characteristics.
    """
    
    # Base tokens per complexity level
    BASE_TOKENS = {
        TaskComplexity.TRIVIAL: 500,
        TaskComplexity.SIMPLE: 2000,
        TaskComplexity.MODERATE: 5000,
        TaskComplexity.COMPLEX: 12000,
        TaskComplexity.EPIC: 25000,
    }
    
    # Multipliers per category
    CATEGORY_MULTIPLIERS = {
        TaskCategory.GENERATION: 1.0,
        TaskCategory.MODIFICATION: 0.8,
        TaskCategory.ANALYSIS: 0.6,
        TaskCategory.DOCUMENTATION: 0.4,
        TaskCategory.TESTING: 0.7,
    }
    
    # File involvement bonus
    FILE_BONUS_PER_FILE = 500
    
    def estimate_tokens(self, task: Task) -> int:
        """Ước lượng số tokens cần thiết"""
        base = self.BASE_TOKENS.get(task.complexity, 2000)
        multiplier = self.CATEGORY_MULTIPLIERS.get(task.category, 1.0)
        file_bonus = len(task.files_involved) * self.FILE_BONUS_PER_FILE
        
        return int(base * multiplier + file_bonus)
    
    def estimate_duration(self, task: Task) -> Dict[str, float]:
        """
        ước lượng thời gian thực hiện (phút).
        Giả định: ~100 tokens/minute processing speed.
        """
        tokens = self.estimate_tokens(task)
        processing_minutes = tokens / 100
        
        # Add overhead for coordination, review
        overhead = 1.2 if len(task.dependencies) > 2 else 1.1
        
        total_minutes = processing_minutes * overhead
        
        return {
            "processing_minutes": processing_minutes,
            "overhead_factor": overhead,
            "total_minutes": total_minutes,
            "total_hours": total_minutes / 60,
        }
    
    def estimate_batch(self, tasks: List[Task]) -> Dict[str, float]:
        """Ước lượng cho cả batch tasks"""
        total_tokens = sum(self.estimate_tokens(t) for t in tasks)
        estimates = [self.estimate_duration(t) for t in tasks]
        
        return {
            "total_tokens": total_tokens,
            "total_minutes": sum(e["total_minutes"] for e in estimates),
            "task_count": len(tasks),
            "avg_tokens_per_task": total_tokens / len(tasks) if tasks else 0,
        }
```

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

```python
class AntiPatternDetector:
    """
    Phát hiện anti-patterns trong task management.
    """
    
    def detect(self, task: Task, context: Dict = None) -> List[Dict]:
        """Kiểm tra task và trả về list anti-patterns"""
        issues = []
        context = context or {}
        
        # Check 1: Killer Task
        if task.estimated_tokens > 20000:
            issues.append({
                "pattern": "KILLER_TASK",
                "severity": "HIGH",
                "message": f"Task estimated {task.estimated_tokens} tokens. "
                          f"Decompose into smaller tasks (< 5K each).",
                "suggestion": "Use TaskDecomposer with 'feature' or 'layer' strategy",
            })
        
        # Check 2: Ambiguous Task
        vague_keywords = [
            "improve", "optimize", "clean", "better",
            "refactor", "make it work", "fix it"
        ]
        if any(kw in task.description.lower() for kw in vague_keywords):
            if not task.verification_criteria:
                issues.append({
                    "pattern": "AMBIGUOUS_TASK",
                    "severity": "MEDIUM",
                    "message": "Task description is vague without clear criteria",
                    "suggestion": "Add specific acceptance criteria and expected outcomes",
                })
        
        # Check 3: Missing Token Estimate
        if task.estimated_tokens == 0:
            issues.append({
                "pattern": "MISSING_ESTIMATE",
                "severity": "LOW",
                "message": "No token estimate provided",
                "suggestion": "Use EffortEstimator to get initial estimate",
            })
        
        # Check 4: Too Many Dependencies
        if len(task.dependencies) > 5:
            issues.append({
                "pattern": "DEPENDENCY_OVERLOAD",
                "severity": "MEDIUM",
                "message": f"Task has {len(task.dependencies)} dependencies",
                "suggestion": "Consider reducing dependencies or splitting task",
            })
        
        # Check 5: No Files Involved (for modification tasks)
        if (task.category == TaskCategory.MODIFICATION 
            and len(task.files_involved) == 0):
            issues.append({
                "pattern": "MISSING_FILE_SCOPE",
                "severity": "MEDIUM",
                "message": "Modification task has no files identified",
                "suggestion": "Scan codebase to identify affected files",
            })
        
        return issues
```

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

```python
class TokenBudgetManager:
    """
    Quản lý ngân sách token cho task execution.
    Prevents context overflow và optimizes token usage.
    """
    
    def __init__(self, total_budget: int = 128000):
        self.total_budget = total_budget
        self.allocated = {
            "system": 5000,
            "project_context": 0,
            "task_context": 0,
            "working_memory": 0,
        }
        self.min_reserve = 20000
    
    @property
    def remaining(self) -> int:
        used = sum(self.allocated.values())
        return self.total_budget - used - self.min_reserve
    
    @property
    def usage_percent(self) -> float:
        used = sum(self.allocated.values())
        return (used / self.total_budget) * 100
    
    def can_fit(self, estimated_tokens: int) -> bool:
        """Kiểm tra có đủ budget cho task không"""
        return self.remaining >= estimated_tokens
    
    def allocate_for_task(self, task: Task) -> bool:
        """Cấp budget cho task — trả False nếu không đủ"""
        needed = task.estimated_tokens or 2000
        if not self.can_fit(needed):
            return False
        
        self.allocated["task_context"] += needed
        return True
    
    def add_to_working_memory(self, tokens: int):
        """Thêm tokens vào working memory"""
        self.allocated["working_memory"] += tokens
    
    def summarize_context(self) -> str:
        """Tóm tắt tình trạng budget"""
        lines = [
            "=== Token Budget Status ===",
            f"Total:     {self.total_budget:,}",
            f"System:    {self.allocated['system']:,}",
            f"Project:   {self.allocated['project_context']:,}",
            f"Task:      {self.allocated['task_context']:,}",
            f"Working:   {self.allocated['working_memory']:,}",
            f"Reserve:   {self.min_reserve:,}",
            f"Remaining: {self.remaining:,}",
            f"Usage:     {self.usage_percent:.1f}%",
        ]
        
        if self.usage_percent > 80:
            lines.append("⚠️ WARNING: High context usage!")
        if self.remaining < 5000:
            lines.append("🚨 CRITICAL: Very low remaining budget!")
        
        return "\n".join(lines)
    
    def suggest_compaction(self) -> List[str]:
        """Gợi ý cách giảm token usage"""
        suggestions = []
        
        if self.allocated["working_memory"] > 30000:
            suggestions.append(
                "Summarize older working memory entries"
            )
        
        if self.allocated["project_context"] > 20000:
            suggestions.append(
                "Remove non-essential project files from context"
            )
        
        if self.usage_percent > 85:
            suggestions.append(
                "Complete current sub-task and start new session"
            )
        
        return suggestions
```

</details>

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