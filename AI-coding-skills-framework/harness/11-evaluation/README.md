# 📊 XI. Evaluation

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Evaluation Dimensions](#1-evaluation-dimensions)
>   - [1.1 Các Chiều Đánh Giá](#11-các-chiều-đánh-giá)
>   - [1.2 Evaluation Rubric](#12-evaluation-rubric)
>   - [1.3 Weight Configuration — Tùy Theo Use Case](#13-weight-configuration-tùy-theo-use-case)
> - [2. Quality Metrics](#2-quality-metrics)
>   - [2.1 Code Quality Metrics](#21-code-quality-metrics)
>   - [2.2 AI Agent Quality Metrics](#22-ai-agent-quality-metrics)
>   - [2.3 Metrics Dashboard](#23-metrics-dashboard)
> - [3. Performance Benchmarks](#3-performance-benchmarks)
>   - [3.1 Benchmark Framework](#31-benchmark-framework)
>   - [3.2 Standard Benchmark Tasks](#32-standard-benchmark-tasks)
>   - [3.3 Benchmark Comparison Table](#33-benchmark-comparison-table)
> - [4. Evaluation Framework](#4-evaluation-framework)
>   - [4.1 Auto-Evaluation Pipeline](#41-auto-evaluation-pipeline)
>   - [4.2 LLM-as-Judge Evaluation](#42-llm-as-judge-evaluation)
>   - [4.3 Regression Testing Framework](#43-regression-testing-framework)
> - [5. Continuous Improvement](#5-continuous-improvement)
>   - [5.1 Improvement Loop](#51-improvement-loop)
>   - [5.2 A/B Testing Framework](#52-ab-testing-framework)
> - [6. Reporting & Dashboards](#6-reporting-dashboards)
>   - [6.1 Evaluation Report Generator](#61-evaluation-report-generator)
> - [7. Case Studies](#7-case-studies)
>   - [7.1 SWE-bench — Benchmarking AI Code Agents](#71-swe-bench-benchmarking-ai-code-agents)
>   - [7.2 HumanEval — Classic Code Generation](#72-humaneval-classic-code-generation)
>   - [7.3 Real-World Evaluation Pipeline — Production Case](#73-real-world-evaluation-pipeline-production-case)
> - [8. Evaluation Tooling](#8-evaluation-tooling)
>   - [8.1 Popular Evaluation Tools](#81-popular-evaluation-tools)
>   - [8.2 PromptFoo Configuration Example](#82-promptfoo-configuration-example)
> - [9. Best Practices](#9-best-practices)
>   - [9.1 DO và DON'T](#91-do-và-dont)
>   - [9.2 Evaluation Strategy](#92-evaluation-strategy)
> - [10. Case Studies Thực Tế](#10-case-studies-thực-tế)
>   - [10.1 Princeton NLP SWE-bench: Benchmarking Real-World Code](#101-princeton-nlp-swe-bench-benchmarking-real-world-code)
>   - [10.2 Aider: LLM Leaderboard for Coding](#102-aider-llm-leaderboard-for-coding)
>   - [10.3 LiveCodeBench: Dynamic Evaluation](#103-livecodebench-dynamic-evaluation)
>   - [10.4 Anthropic's Evaluation Methodology](#104-anthropics-evaluation-methodology)
> - [11. TypeScript Interfaces cho Evaluation](#11-typescript-interfaces-cho-evaluation)
>   - [11.1 Core Evaluation Types](#111-core-evaluation-types)
> - [12. Design Principles cho Evaluation](#12-design-principles-cho-evaluation)
>   - [12.1 SOLID cho Evaluation Systems](#121-solid-cho-evaluation-systems)
>   - [12.2 Evaluation Design Principles](#122-evaluation-design-principles)
> - [13. Testing Evaluation Harness](#13-testing-evaluation-harness)
>   - [13.1 Evaluation Test Harness](#131-evaluation-test-harness)
> - [14. Future Trends trong Evaluation](#14-future-trends-trong-evaluation)
>   - [14.1 AI Evaluation Trends (2024-2026)](#141-ai-evaluation-trends-2024-2026)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks & Tools](#frameworks-tools)
>   - [Benchmarks](#benchmarks)
>   - [Case Study References](#case-study-references)
>
---

### Câu Chuyện Mở Đầu

Bạn xây một chiếc cầu mới. Bạn có thể nói *"Trông nó ổn"*, nhưng nếu không **đo tải trọng, kiểm tra chất liệu, stress-test với xe tải nặng** — bạn sẽ không biết cây cầu có chịu được 10 năm sử dụng hay sẽ sập sau 1 tháng.

**AI code cũng vậy.** Viết code xong mà không evaluate = **ship cầu mà không kiểm tra**.

Khi bạn sử dụng AI để generate code, câu hỏi quan trọng nhất không phải *"Code chạy được không?"* mà là: *"Code có đúng không? Có an toàn không? Có maintain được không? Có tốt hơn cách viết tay không?"* — và bạn cần **hệ thống evaluation bài bản** để trả lời.

**Giải pháp**: Multi-level Evaluation Framework — từ functional correctness đến business value, đảm bảo mỗi dòng code AI-generated đều **đạt chuẩn trước khi đến tay người dùng**.

### Tại Sao Evaluation Quan Trọng?

> *"Nếu bạn không đo lường được, bạn không thể cải thiện được. Và nếu bạn không cải thiện được, bạn đang tụt hậu."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **SWE-bench (Princeton, 2025)** | Top models resolve **44% real GitHub issues** — nhưng **chỉ khi được evaluate đúng cách** mới biết model nào thực sự tốt cho use case cụ thể |
| 2 | **Google Research (2024)** | Teams với systematic evaluation pipelines phát hiện **3× more regressions** trước khi reaching production |
| 3 | **Microsoft (2025)** | AI code generation without evaluation tăng **28% technical debt** trong 6 tháng |

#### Triết lý cốt lõi:

```
Evaluation = What You Measure → What You Improve → What You Ship
```

**5 Levels của Evaluation**:
- **Level 1**: Code works (functional correctness)
- **Level 2**: Code is correct (edge cases, error handling)
- **Level 3**: Code is good (readability, maintainability)
- **Level 4**: Code is safe (security, performance)
- **Level 5**: Code adds value (business impact, user satisfaction)

**Analogies**: Evaluation giống hệ thống kiểm soát chất lượng trong nhà máy — không chỉ kiểm tra sản phẩm có hỏng không (Level 1), mà còn kiểm tra finish có đẹp không (Level 3), vật liệu có an toàn không (Level 4), và khách hàng có hài lòng không (Level 5).

**Nếu bỏ qua**: Ship code không biết quality ra sao, không biết regression khi nào xuất hiện, không biết model nào tốt hơn model nào, và cuối cùng technical debt tích tụ đến mức refactor tốn 10× chi phí.

## Tổng Quan

**Evaluation** trong AI coding là quá trình **đánh giá hiệu quả và chất lượng** của AI agent khi thực hiện các tác vụ coding. Evaluation bao gồm benchmarking, metrics collection, và continuous improvement dựa trên kết quả đánh giá.

> **"You can't improve what you can't measure"** — Peter Drucker

```
┌──────────────────────────────────────────────────────────────────┐
│                      EVALUATION FRAMEWORK                         │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │  Input   │    │  Agent   │    │  Output  │            │  │
│  │  │  Tasks   │───►│  Execute │───►│  Code    │            │  │
│  │  └──────────┘    └──────────┘    └────┬─────┘            │  │
│  │                                        │                   │  │
│  │                                        ▼                   │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐            │  │
│  │  │ Improve  │◄───│ Analyze  │◄───│ Evaluate │            │  │
│  │  │ Action   │    │ Results  │    │ Metrics  │            │  │
│  │  └──────────┘    └──────────┘    └──────────┘            │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Evaluation Dimensions](#1-evaluation-dimensions) | Các chiều đánh giá |
| 2 | [Quality Metrics](#2-quality-metrics) | Metrics chất lượng code |
| 3 | [Performance Benchmarks](#3-performance-benchmarks) | Benchmark hiệu suất |
| 4 | [Evaluation Framework](#4-evaluation-framework) | Framework đánh giá tự động |
| 5 | [Continuous Improvement](#5-continuous-improvement) | Cải tiến liên tục |
| 6 | [Reporting & Dashboards](#6-reporting--dashboards) | Báo cáo và dashboard |
| 7 | [Case Studies](#7-case-studies) | Case studies thực tế |
| 8 | [Evaluation Tooling](#8-evaluation-tooling) | Tools và frameworks |
| 9 | [Best Practices](#9-best-practices) | Nguyên tắc đánh giá |

---

## 1. Evaluation Dimensions

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Evaluation Dimensions là các "khía cạnh" riêng biệt để đo chất lượng AI agent — correctness (độ đúng), efficiency (độ nhanh), safety (độ an toàn), reliability (độ ổn định) và nhiều nữa. Mỗi khía cạnh là một chiếc cân riêng, gom lại cho bạn bức tranh toàn diện thay vì chỉ một con số duy nhất.
> **Ẩn dụ/so sánh:** Giống phiếu điểm ở trường — không chỉ có điểm toán, mà còn điểm văn, điểm anh, điểm hạnh kiểm. Chấm nhiều môn mới thấy được học sinh giỏi nét nào, yếu chỗ nào.
> **Vì sao quan trọng:** Chất lượng AI rất trừu tượng, cần tách thành các chiều đo rõ ràng thì mới biết phải cải thiện phần nào.

### 1.1 Các Chiều Đánh Giá

Bảng dưới đây tổng hợp **9 chiều đánh giá** mà bạn nên xem xét khi chấm AI agent — từ độ đúng (correctness) đến chi phí (cost-effectiveness). Hãy đọc như một "bảng kiểm tra sức khỏe": mỗi dòng là một câu hỏi bạn cần trả lời cho agent của mình.

```
┌──────────────────────────────────────────────────────────────────┐
│                EVALUATION DIMENSIONS                              │
│                                                                  │
│  1. CORRECTNESS (Đúng)                                          │
│     Code có chạy đúng không?                                    │
│     → Functional correctness, edge cases                       │
│                                                                  │
│  2. QUALITY (Tốt)                                               │
│     Code có sạch không?                                         │
│     → Readability, maintainability, complexity                  │
│                                                                  │
│  3. EFFICIENCY (Nhanh)                                          │
│     Code có tối ưu không?                                       │
│     → Time complexity, memory usage, I/O                       │
│                                                                  │
│  4. SAFETY (An toàn)                                            │
│     Code có an toàn không?                                      │
│     → Security, error handling, edge cases                     │
│                                                                  │
│  5. COMPLETENESS (Đầy đủ)                                       │
│     Task có được hoàn thành hết không?                         │
│     → Coverage, missing features                                │
│                                                                  │
│  6. SPEED (Tốc độ)                                              │
│     Agent có nhanh không?                                       │
│     → Tokens used, time to completion                           │
│                                                                  │
│  7. USABILITY (Dễ dùng)                                         │
│     Output có dễ dùng không?                                    │
│     → Documentation, API design, examples                      │
│                                                                  │
│  8. COST-EFFECTIVENESS (Hiệu quả chi phí)                       │
│     Chi phí có hợp lý không?                                    │
│     → Token cost vs value delivered                             │
│                                                                  │
│  9. RELIABILITY (Đáng tin cậy)                                  │
│     Kết quả có ổn định không?                                   │
│     → Consistency across runs, reproducibility                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Evaluation Rubric

Đoạn code này định nghĩa **rubric chấm điểm** — bộ tiêu chuẩn nói rõ thế nào là điểm 5, điểm 3, điểm 1 cho từng chiều đánh giá. Giống tiêu chí chấm bài thi: có mô tả rõ ràng thì chấm mới công bằng và thống nhất giữa các lần. Bạn có thể chạy thử để thấy một kết quả được cộng điểm trọng số (weighted) thành tổng điểm 0-100.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class Rating(Enum):
    EXCELLENT = 5
    GOOD = 4
    ACCEPTABLE = 3
    POOR = 2
    FAILED = 1


@dataclass
class EvaluationDimension:
    """Một chiều đánh giá"""
    name: str
    weight: float              # 0.0 - 1.0
    description: str
    criteria: Dict[Rating, str] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    """Kết quả đánh giá cho một task"""
    task_id: str
    scores: Dict[str, float] = field(default_factory=dict)
    notes: Dict[str, str] = field(default_factory=dict)
    total_score: float = 0.0
    
    def add_score(self, dimension: str, score: float, 
                  note: str = ""):
        self.scores[dimension] = score
        if note:
            self.notes[dimension] = note
    
    def calculate_total(self, weights: Dict[str, float]) -> float:
        """Tính tổng điểm weighted"""
        total = 0.0
        total_weight = 0.0
        
        for dim, weight in weights.items():
            if dim in self.scores:
                total += self.scores[dim] * weight
                total_weight += weight
        
        self.total_score = total / total_weight if total_weight else 0
        return self.total_score


# Define standard rubric
STANDARD_RUBRIC = [
    EvaluationDimension(
        name="correctness",
        weight=0.25,
        description="Code runs correctly, handles edge cases",
        criteria={
            Rating.EXCELLENT: "All tests pass, edge cases handled",
            Rating.GOOD: "Most tests pass, minor edge case missed",
            Rating.ACCEPTABLE: "Core functionality works, some gaps",
            Rating.POOR: "Partially working, key issues remain",
            Rating.FAILED: "Does not work or breaks existing code",
        }
    ),
    EvaluationDimension(
        name="quality",
        weight=0.20,
        description="Code is clean, readable, maintainable",
        criteria={
            Rating.EXCELLENT: "Follows all conventions, self-documenting",
            Rating.GOOD: "Clean code, minor style issues",
            Rating.ACCEPTABLE: "Readable but could be improved",
            Rating.POOR: "Messy but understandable",
            Rating.FAILED: "Unreadable or extremely messy",
        }
    ),
    EvaluationDimension(
        name="efficiency",
        weight=0.15,
        description="Performance is appropriate for the use case",
        criteria={
            Rating.EXCELLENT: "Optimal complexity, minimal resources",
            Rating.GOOD: "Good performance, minor optimizations possible",
            Rating.ACCEPTABLE: "Acceptable for most cases",
            Rating.POOR: "Performance concerns for scale",
            Rating.FAILED: "Severe performance issues",
        }
    ),
    EvaluationDimension(
        name="safety",
        weight=0.15,
        description="Code handles errors and is secure",
        criteria={
            Rating.EXCELLENT: "Comprehensive error handling, no vulnerabilities",
            Rating.GOOD: "Good error handling, minor security notes",
            Rating.ACCEPTABLE: "Basic error handling present",
            Rating.POOR: "Minimal error handling",
            Rating.FAILED: "No error handling, security risks",
        }
    ),
    EvaluationDimension(
        name="completeness",
        weight=0.15,
        description="All requirements are addressed",
        criteria={
            Rating.EXCELLENT: "All requirements + bonus improvements",
            Rating.GOOD: "All requirements met",
            Rating.ACCEPTABLE: "Core requirements met, some missing",
            Rating.POOR: "Partially completed",
            Rating.FAILED: "Major requirements missing",
        }
    ),
    EvaluationDimension(
        name="speed",
        weight=0.10,
        description="Token efficiency and time to completion",
        criteria={
            Rating.EXCELLENT: "Minimal tokens, fast completion",
            Rating.GOOD: "Reasonable token usage",
            Rating.ACCEPTABLE: "Average token usage",
            Rating.POOR: "High token usage, slow",
            Rating.FAILED: "Extremely inefficient",
        }
    ),
]
```

</details>

### 1.3 Weight Configuration — Tùy Theo Use Case

Code ở đây cho thấy cùng một bộ chiều đánh giá, nhưng **trọng số đổi theo mục tiêu** — giống phòng thi đại học điểm lệch môn tự nhiên, trường nghề lại nặng tay nghề. Nơi cần sự an toàn thì nâng trọng số `safety`, nơi cần ra sản phẩm nhanh thì nâng `completeness`. Bạn tùy chỉnh `WEIGHT_CONFIGS` sao cho khớp use case của mình.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Different weight configurations for different scenarios
WEIGHT_CONFIGS = {
    "production_code": {
        "correctness": 0.30,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.20,
        "completeness": 0.10,
        "speed": 0.05,
    },
    
    "prototype_hackathon": {
        "correctness": 0.35,
        "quality": 0.05,
        "efficiency": 0.05,
        "safety": 0.05,
        "completeness": 0.40,
        "speed": 0.10,
    },
    
    "library_framework": {
        "correctness": 0.25,
        "quality": 0.25,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.10,
        "speed": 0.10,
    },
    
    "ai_agent_harness": {
        "correctness": 0.20,
        "quality": 0.15,
        "efficiency": 0.10,
        "safety": 0.25,
        "completeness": 0.15,
        "speed": 0.15,
    },
}
```

</details>

---

## 2. Quality Metrics

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Quality Metrics là các thước đo định lượng dùng để chấm chất lượng output của AI agent — accuracy, completeness, adherence, style — biến đánh giá cảm tính thành con số khách quan, so sánh được.
> **Ẩn dụ/so sánh:** Như thang điểm chấm món ăn: hương vị (correctness), trình bày (style), đủ khẩu phần (completeness). Điểm rõ ràng giúp người nấu biết món nào cần cải thiện.
> **Vì sao quan trọng:** Không có con số cụ thể thì "trông có vẻ ổn" sẽ thay thế đánh giá thật, và bạn không thể theo dõi tiến bộ theo thời gian.

### 2.1 Code Quality Metrics

Lớp `CodeQualityAnalyzer` tự động chấm chất lượng code — độ phức tạp (cyclomatic complexity), khả năng bảo trì (maintainability index), cách đặt tên, mức độ có docstring — rồi gộp thành điểm tổng 0-100. Như một "giáo viên chấm bài tự động": nhận code đầu vào, trả bảng điểm kèm từng chỉ số cụ thể thay vì chỉ nói "code này ổn".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import ast
import math
from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path

@dataclass
class CodeQualityReport:
    """Báo cáo chất lượng code"""
    file_path: str
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 0.0
    duplication_ratio: float = 0.0
    naming_score: float = 0.0
    documentation_score: float = 0.0
    overall_score: float = 0.0


class CodeQualityAnalyzer:
    """
    Phân tích chất lượng code — tính metrics tự động.
    
    Metrics:
    - Lines of Code (LOC)
    - Cyclomatic Complexity
    - Maintainability Index
    - Code Duplication
    - Naming Conventions
    - Documentation Coverage
    """
    
    def analyze(self, code: str, file_path: str = "") -> CodeQualityReport:
        report = CodeQualityReport(file_path=file_path)
        
        lines = code.strip().split("\n")
        report.lines_of_code = len(lines)
        report.cyclomatic_complexity = self._calc_complexity(code)
        report.maintainability_index = self._calc_maintainability(
            code, report.cyclomatic_complexity, report.lines_of_code
        )
        report.naming_score = self._calc_naming_score(code)
        report.documentation_score = self._calc_doc_score(code)
        
        # Overall score (weighted average)
        scores = [
            report.maintainability_index * 0.3,
            report.naming_score * 0.25,
            report.documentation_score * 0.25,
            max(0, 100 - report.cyclomatic_complexity * 10) * 0.2,
        ]
        report.overall_score = sum(scores)
        
        return report
    
    def _calc_complexity(self, code: str) -> float:
        """Tính cyclomatic complexity"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 10.0  # High complexity for unparseable code
        
        complexity = 1
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For,
                                ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calc_maintainability(self, code: str, 
                               complexity: float, loc: int) -> float:
        """Tính maintainability index (0-100)"""
        if loc == 0:
            return 100.0
        
        # Simplified MI formula
        mi = 171 - 5.2 * math.log(max(loc, 1)) - 0.23 * complexity - 16.2 * math.log(max(loc, 1))
        return max(0, min(100, mi))
    
    def _calc_naming_score(self, code: str) -> float:
        """Đánh giá naming conventions"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        good_names = 0
        total_names = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_names += 1
                if (node.name.islower() and 
                    "_" in node.name or 
                    node.name.startswith("_")):
                    good_names += 1
            elif isinstance(node, ast.ClassDef):
                total_names += 1
                if node.name[0].isupper():
                    good_names += 1
        
        return (good_names / total_names * 100) if total_names else 100.0
    
    def _calc_doc_score(self, code: str) -> float:
        """Đánh giá documentation coverage"""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0.0
        
        documented = 0
        total = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total += 1
                if (ast.get_docstring(node)):
                    documented += 1
        
        return (documented / total * 100) if total else 100.0
```

</details>

### 2.2 AI Agent Quality Metrics

Phần này đo **cả quá trình generate của AI agent**, không chỉ kết quả: tỷ lệ đúng ngay lần đầu, số lần retry, token tiêu thụ, tỷ lệ không làm vỡ chức năng cũ. Một agent tốt thường đúng sớm, ít retry và ít tốn token — như nhân viên biết việc, không cần hỏi sếp nhiều lần.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AgentQualityMetrics:
    """
    Metrics đặc thù cho AI coding agent.
    
    Khác với code quality thông thường,
    agent metrics đo cả QUÁ TRÌNH generate,
    không chỉ kết quả cuối cùng.
    """
    
    # === PROCESS METRICS ===
    
    # 1. First-Attempt Success Rate
    # Tỷ lệ code đúng ngay lần đầu (không cần retry)
    first_attempt_success: float = 0.0
    
    # 2. Iteration Efficiency
    # Số lần retry trung bình để hoàn thành task
    avg_iterations: float = 0.0
    
    # 3. Token Efficiency
    # Token sử dụng so với optimal (thấp hơn = tốt hơn)
    token_efficiency: float = 0.0
    
    # 4. Time to First Good Output
    # Thời gian từ prompt đến output hợp lệ đầu tiên
    time_to_first_output: float = 0.0
    
    # === OUTPUT METRICS ===
    
    # 5. Code Correctness
    # Tỷ lệ tests pass
    test_pass_rate: float = 0.0
    
    # 6. Edit Precision
    # Tỷ lệ edits thực sự cần thiết / total edits
    edit_precision: float = 0.0
    
    # 7. Context Relevance
    # Có dùng đúng context không (không hallucinate)
    context_relevance: float = 0.0
    
    # 8. Instruction Following
    # Có làm đúng theo yêu cầu không
    instruction_following: float = 0.0
    
    # === SAFETY METRICS ===
    
    # 9. No Regressions
    # Không phá vỡ existing functionality
    regression_free_rate: float = 0.0
    
    # 10. Security Compliance
    # Không introduce vulnerabilities
    security_compliance: float = 0.0
    
    def calculate_composite_score(self) -> float:
        """Tính composite score từ tất cả metrics"""
        weights = {
            "first_attempt_success": 0.15,
            "test_pass_rate": 0.25,
            "edit_precision": 0.10,
            "context_relevance": 0.10,
            "instruction_following": 0.15,
            "regression_free_rate": 0.15,
            "token_efficiency": 0.10,
        }
        
        total = 0.0
        for metric, weight in weights.items():
            value = getattr(self, metric, 0.0)
            total += value * weight
        
        return total * 100  # Scale to 0-100
```

</details>

### 2.3 Metrics Dashboard

Bảng điều khiển mẫu gộp mọi metrics vào một màn hình duy nhất: mỗi chiều một thanh phần trăm, cuối cùng là COMPOSITE SCORE. Cách đọc rất đơn giản — thanh dài là tốt, thanh ngắn là chỗ cần cải thiện. Dashboard kiểu này giúp cả đội "nhìn là biết" agent đang khỏe hay yếu ở đâu.

```
┌──────────────────────────────────────────────────────────────────┐
│                AI AGENT QUALITY DASHBOARD                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ CORRECTNESS                           ████████░░ 82%    │   │
│  │ └─ Test Pass Rate                     ████████░░ 85%    │   │
│  │ └─ Edge Case Handling                 ███████░░░ 72%    │   │
│  │ └─ Regression Free                    █████████░ 90%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ QUALITY                               ███████░░░ 75%    │   │
│  │ └─ Maintainability                    ███████░░░ 70%    │   │
│  │ └─ Naming Conventions                 █████████░ 88%    │   │
│  │ └─ Documentation                      ███████░░░ 68%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ EFFICIENCY                            ████████░░ 80%    │   │
│  │ └─ Token Efficiency                   ████████░░ 82%    │   │
│  │ └─ Time to Completion                 ███████░░░ 75%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ SAFETY                                █████████░ 88%    │   │
│  │ └─ No Vulnerabilities                 ██████████ 95%    │   │
│  │ └─ Error Handling                     ████████░░ 82%    │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ COMPOSITE SCORE                       ████████░░ 81/100 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Performance Benchmarks

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Performance Benchmarks là những bài kiểm chuẩn hóa — SWE-bench, HumanEval, LiveCodeBench — dùng bộ câu hỏi cố định để đo năng lực agent, cho phép so sánh công bằng giữa các model và phiên bản.
> **Ẩn dụ/so sánh:** Giống kỳ thi tuyển sinh chung: mọi thí sinh cùng một đề, cùng thang điểm, để trường dễ nhận xét học sinh nào giỏi hơn. Ai cũng tự ra đề riêng thì không bao giờ so được.
> **Vì sao quan trọng:** Thiếu bộ đề chung thì mỗi người tự chấm kiểu riêng, không thể biết model A thực sự có hơn model B hay không.

### 3.1 Benchmark Framework

`BenchmarkSuite` là "sân thi đấu" cho agent: bạn thêm các task vào, chạy agent trên từng task, rồi thống kê success rate, token dùng, thời gian — thậm chí so sánh hai lần chạy với nhau. Như sân bóng có trọng tài bấm giờ và ghi biên bản: mọi pha bóng đều được đo, không có chuyện "tôi cảm giác mình chơi tốt".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List
from datetime import datetime

@dataclass
class BenchmarkResult:
    """Kết quả benchmark cho một task"""
    task_id: str
    task_description: str
    tokens_used: int = 0
    execution_time_s: float = 0.0
    success: bool = False
    quality_score: float = 0.0
    attempts: int = 0
    error_message: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


class BenchmarkSuite:
    """
    Benchmark suite cho AI coding agent.
    
    Chạy nhiều tasks, collect metrics, và so sánh
    giữa các runs/models/configurations.
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.results: List[BenchmarkResult] = []
        self.tasks: List[Dict] = []
    
    def add_task(self, task_id: str, description: str,
                 input_data: Any = None,
                 expected_output: Any = None,
                 validator: Callable = None):
        """Thêm task vào benchmark suite"""
        self.tasks.append({
            "id": task_id,
            "description": description,
            "input": input_data,
            "expected": expected_output,
            "validator": validator,
        })
    
    def run(self, agent_func: Callable, max_retries: int = 3):
        """
        Chạy benchmark — chạy agent trên mỗi task.
        
        agent_func: function(task) -> (output, tokens_used)
        """
        for task in self.tasks:
            result = BenchmarkResult(
                task_id=task["id"],
                task_description=task["description"],
            )
            
            start_time = time.time()
            
            for attempt in range(max_retries):
                try:
                    output, tokens = agent_func(task)
                    result.execution_time_s = time.time() - start_time
                    result.tokens_used = tokens
                    result.attempts = attempt + 1
                    
                    # Validate
                    if task.get("validator"):
                        result.success = task["validator"](output)
                    elif task.get("expected"):
                        result.success = output == task["expected"]
                    else:
                        result.success = True
                    
                    if result.success:
                        break
                        
                except Exception as e:
                    result.error_message = str(e)
                    result.attempts = attempt + 1
            
            self.results.append(result)
        
        return self.get_summary()
    
    def get_summary(self) -> Dict:
        """Tổng hợp kết quả benchmark"""
        if not self.results:
            return {"total": 0}
        
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        total_tokens = sum(r.tokens_used for r in self.results)
        total_time = sum(r.execution_time_s for r in self.results)
        
        return {
            "suite": self.name,
            "total_tasks": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(self.results),
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens / len(self.results),
            "total_time_s": total_time,
            "avg_time_s": total_time / len(self.results),
            "avg_attempts": sum(
                r.attempts for r in self.results
            ) / len(self.results),
        }
    
    def compare_with(self, other_suite: "BenchmarkSuite") -> Dict:
        """So sánh hai benchmark suites"""
        s1 = self.get_summary()
        s2 = other_suite.get_summary()
        
        return {
            self.name: s1,
            other_suite.name: s2,
            "improvements": {
                "success_rate": (
                    s1["success_rate"] - s2["success_rate"]
                ),
                "avg_tokens": (
                    s2["avg_tokens"] - s1["avg_tokens"]
                ),
                "avg_time": (
                    s2["avg_time_s"] - s1["avg_time_s"]
                ),
            },
        }
```

</details>

### 3.2 Standard Benchmark Tasks

Danh sách này là **bộ đề mẫu** chia theo độ khó từ trivial đến complex: viết hello world, đảo chuỗi, sửa lỗi off-by-one, refactor class. Mỗi task đi kèm validator để chấm tự động. Dùng như bộ đề ôn thi: bắt đầu dễ để kiểm tra agent có chạy được không, rồi tăng dần độ khó để đo năng lực thực sự.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
BENCHMARK_TASKS = {
    # === TRIVIAL (Difficulty: 1/5) ===
    "hello_world": {
        "id": "basic-001",
        "description": "Create a hello world function",
        "difficulty": "trivial",
        "expected": "Hello, World!",
    },
    
    "string_reverse": {
        "id": "basic-002",
        "description": "Reverse a string without built-in",
        "difficulty": "trivial",
        "validator": lambda out: out("hello") == "olleh",
    },
    
    # === EASY (Difficulty: 2/5) ===
    "fibonacci": {
        "id": "algo-001",
        "description": "Implement fibonacci with memoization",
        "difficulty": "easy",
        "validator": lambda out: out(10) == 55,
    },
    
    "binary_search": {
        "id": "algo-002",
        "description": "Implement binary search",
        "difficulty": "easy",
        "validator": lambda out: out([1,2,3,4,5], 3) == 2,
    },
    
    # === MODERATE (Difficulty: 3/5) ===
    "api_endpoint": {
        "id": "web-001",
        "description": "Create a REST API endpoint for CRUD",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "bug_fix": {
        "id": "debug-001",
        "description": "Fix off-by-one error in loop",
        "difficulty": "easy",
        "validator": lambda out: True,
    },
    
    # === COMPLEX (Difficulty: 4/5) ===
    "refactor_class": {
        "id": "refactor-001",
        "description": "Refactor God class into smaller classes",
        "difficulty": "complex",
        "validator": lambda out: True,
    },
    
    "write_tests": {
        "id": "test-001",
        "description": "Write comprehensive unit tests",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    # === HARD (Difficulty: 5/5) ===
    "security_audit": {
        "id": "security-001",
        "description": "Find and fix SQL injection vulnerabilities",
        "difficulty": "moderate",
        "validator": lambda out: True,
    },
    
    "multi_file_refactor": {
        "id": "complex-001",
        "description": "Refactor across 5+ files with dependency updates",
        "difficulty": "hard",
        "validator": lambda out: True,
    },
}
```

</details>

### 3.3 Benchmark Comparison Table

Bảng so sánh điểm của các model trên các benchmark phổ biến năm 2026. Đọc theo cột: một model đạt 92% trên HumanEval nhưng chỉ 53% trên SWE-bench là chuyện bình thường — vì mỗi benchmark đo năng lực khác nhau (viết hàm đơn lẻ khác với sửa bug trong repo thật). Nhớ dòng chú thích cuối: điểm số thay đổi theo phiên bản model và cách viết prompt.

```
┌────────────────────────────────────────────────────────────────────┐
│           BENCHMARK SCORES COMPARISON (2026)                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Benchmark         │ Metric              │ Human │ Claude │ GPT-4 │
│  ──────────────────┼─────────────────────┼───────┼───────┼───────│
│  HumanEval         │ Pass@1              │ -     │ 92%   │ 86%   │
│  HumanEval         │ Pass@10             │ -     │ 96%   │ 92%   │
│  SWE-bench Lite    │ Resolved            │ -     │ 48%   │ 33%   │
│  SWE-bench Verified│ Resolved            │ -     │ 53%   │ 38%   │
│  MBPP+             │ Pass@1              │ -     │ 89%   │ 82%   │
│  LiveCodeBench     │ Pass@1              │ -     │ 45%   │ 38%   │
│  Aider Polyglot    │ % Correct           │ 95%   │ 72%   │ 61%   │
│                                                                    │
│  ──────────────────┼─────────────────────┼───────┼───────┼───────│
│  COMPOSITE SCORE   │ Overall             │ -     │ ~78%  │ ~65%  │
│                                                                    │
│  ⚠️  Note: Scores vary by model version and prompting strategy  │
│     Claude 3.5 Sonnet with good harness can outperform GPT-4o    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Evaluation Framework

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Evaluation Framework là "bộ khung" tổ chức cả quy trình đánh giá — thiết kế test case, chạy thử, thu thập kết quả, phân tích — để việc đánh giá lặp lại được nhất quán và dễ hành động.
> **Ẩn dụ/so sánh:** Như dây chuyền kiểm tra chất lượng trong nhà máy: sản phẩm lần lượt qua bàn cân, trạm kiểm an toàn, trạm đóng gói — mỗi trạm một việc, quy trình lặp lại y hệt mỗi lần.
> **Vì sao quan trọng:** Không có khung chuẩn thì mỗi lần đánh giá lại làm kiểu khác nhau, kết quả không đáng tin để so sánh.

### 4.1 Auto-Evaluation Pipeline

`EvaluationPipeline` biến quá trình đánh giá thành **cỗ máy chạy tự động**: bạn thêm các check như lint, test, security vào pipeline, chạy trên code rồi gom điểm theo trọng số và xuất tổng hợp. Mỗi check như một người kiểm tra viên trong dây chuyền, mỗi người chấm một tiêu chí; con số cuối là kết luận chung của cả đội kiểm tra.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Callable, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class EvalConfig:
    """Cấu hình evaluation"""
    dimensions: List[str] = field(default_factory=lambda: [
        "correctness", "quality", "efficiency", 
        "safety", "completeness"
    ])
    weights: Dict[str, float] = field(default_factory=lambda: {
        "correctness": 0.25,
        "quality": 0.20,
        "efficiency": 0.15,
        "safety": 0.15,
        "completeness": 0.15,
        "speed": 0.10,
    })
    auto_evaluate: bool = True
    human_review: bool = False


class EvaluationPipeline:
    """
    Pipeline đánh giá tự động cho AI coding output.
    
    Steps:
    1. Static Analysis (lint, complexity, naming)
    2. Dynamic Testing (run tests, check output)
    3. Security Scan (vulnerability check)
    4. Quality Scoring (weighted dimensions)
    5. Report Generation
    """
    
    def __init__(self, config: EvalConfig = None):
        self.config = config or EvalConfig()
        self.checks: List[Callable] = []
        self.results: List[EvaluationResult] = []
    
    def add_check(self, name: str, check_func: Callable,
                  dimension: str, weight: float = 1.0):
        """Thêm một check vào pipeline"""
        self.checks.append({
            "name": name,
            "func": check_func,
            "dimension": dimension,
            "weight": weight,
        })
    
    def evaluate(self, task_id: str, code: str, 
                 context: Dict = None) -> EvaluationResult:
        """Chạy evaluation trên code"""
        result = EvaluationResult(task_id=task_id)
        
        for check in self.checks:
            try:
                score = check["func"](code, context or {})
                result.add_score(
                    check["name"],
                    score * check["weight"],
                    f"Auto-evaluated by {check['name']}"
                )
            except Exception as e:
                result.add_score(
                    check["name"], 0.0,
                    f"Evaluation failed: {str(e)}"
                )
        
        result.calculate_total(self.config.weights)
        self.results.append(result)
        return result
    
    def get_average_scores(self) -> Dict[str, float]:
        """Tính average scores qua tất cả evaluations"""
        if not self.results:
            return {}
        
        dim_scores = {}
        for result in self.results:
            for dim, score in result.scores.items():
                if dim not in dim_scores:
                    dim_scores[dim] = []
                dim_scores[dim].append(score)
        
        return {
            dim: sum(scores) / len(scores)
            for dim, scores in dim_scores.items()
        }


# Standard checks
def check_test_passes(code: str, context: Dict) -> float:
    """Kiểm tra code có chạy qua tests không"""
    tests = context.get("tests", [])
    if not tests:
        return 50.0  # No tests = neutral score
    # Would execute tests and return pass rate
    return 80.0

def check_no_lint_errors(code: str, context: Dict) -> float:
    """Kiểm tra lint"""
    return 90.0  # Simplified

def check_complexity(code: str, context: Dict) -> float:
    """Kiểm tra complexity"""
    analyzer = CodeQualityAnalyzer()
    report = analyzer.analyze(code)
    return min(100, max(0, 100 - report.cyclomatic_complexity * 5))
```

</details>

### 4.2 LLM-as-Judge Evaluation

Đây là cách **dùng một LLM mạnh (GPT-4, Claude) làm "giám khảo"** để chấm code của một LLM khác. Giống nhờ senior engineer có kinh nghiệm đọc code, chấm điểm và nêu lý do — xử lý tốt các thứ mơ hồ như readability, design mà máy chấm tự động khó làm. Nhưng hãy nhớ: giám khảo cũng có lúc chủ quan và hallucinate, nên dùng phối hợp với test tự động, đừng tin tuyệt đối.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class LLMJudge:
    """
    Dùng LLM để đánh giá output của AI agent.
    
    Leverage: GPT-4, Claude, hoặc model lớn khác
    làm "judge" để đánh giá code quality.
    
    Ưu điểm:
    - Có thể đánh giá nuanced qualities (readability, design)
    - Không cần viết test cases cho mọi edge case
    - Có thể hiểu intent và context
    
    Nhược điểm:
    - Chi phí (cần thêm 1 LLM call)
    - Có thể không consistent 100%
    - Judge cũng có thể hallucinate
    """
    
    def __init__(self, judge_model_func):
        self.judge = judge_model_func
    
    def evaluate_code(self, code: str, task: str, 
                      context: str = "") -> Dict:
        """Đánh giá code bằng LLM judge"""
        
        prompt = f"""You are a senior code reviewer. Evaluate the following code.

TASK: {task}

CODE:
```

</details>
{code}
```

CONTEXT: {context}

Rate the code on these dimensions (1-10):
1. Correctness - Does it solve the task correctly?
2. Code Quality - Is it clean, readable, well-structured?
3. Efficiency - Is it performant?
4. Robustness - Does it handle edge cases?
5. Completeness - Does it address all requirements?

For each dimension, provide:
- Score (1-10)
- Brief justification (1 sentence)

Output as JSON:
{{
  "correctness": {{"score": N, "reason": "..."}},
  "quality": {{"score": N, "reason": "..."}},
  "efficiency": {{"score": N, "reason": "..."}},
  "robustness": {{"score": N, "reason": "..."}},
  "completeness": {{"score": N, "reason": "..."}},
  "overall": N,
  "suggestions": ["suggestion1", "suggestion2"]
}}"""
        
        response = self.judge(prompt)
        return self._parse_judgment(response)
    
    def compare_outputs(self, task: str, 
                        output_a: str, output_b: str) -> Dict:
        """So sánh hai outputs"""
        
        prompt = f"""Compare these two implementations for the same task.

TASK: {task}

IMPLEMENTATION A:
```
{output_a}
```

IMPLEMENTATION B:
```
{output_b}
```

Which is better and why? Rate each (1-10) and pick a winner.
Output as JSON:
{{
  "implementation_a": {{"score": N, "strengths": [...], "weaknesses": [...]}},
  "implementation_b": {{"score": N, "strengths": [...], "weaknesses": [...]}},
  "winner": "A" or "B",
  "reasoning": "..."
}}"""
        
        response = self.judge(prompt)
        return self._parse_comparison(response)
    
    def _parse_judgment(self, response: str) -> Dict:
        """Parse JSON response từ LLM judge"""
        import json
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except json.JSONDecodeError:
            return {"error": "Failed to parse judgment"}
```

### 4.3 Regression Testing Framework

Regression testing trả lời câu hỏi: **sau khi đổi prompt hoặc harness, agent có quên cách làm đúng không?** Cách làm: lưu "bài giải mẫu" (golden answer) cho từng task, chạy lại rồi so với baseline; điểm tụt quá 10% là báo REGRESSION. Giống ông thầy giữ bài kiểm tra cũ của học sinh, lâu lâu cho làm lại để chắc chắn học sinh không "học trước quên sau".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class RegressionTestSuite:
    """
    Framework regression testing cho AI coding agent.
    
    Mục đích: Đảm bảo agent không "quên" cách làm đúng
    sau khi được update/prompt mới.
    
    Concept:
    - Mỗi task có "golden answer" đã được verify
    - Khi update agent, chạy lại tất cả tasks
    - Nếu score giảm → REGRESSION
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.test_cases: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def add_test_case(self, task_id: str, prompt: str,
                      golden_output: str, 
                      validator: Callable = None,
                      category: str = "general"):
        """Thêm test case với golden output"""
        self.test_cases.append({
            "id": task_id,
            "prompt": prompt,
            "golden": golden_output,
            "validator": validator,
            "category": category,
        })
    
    def set_baseline(self, results: Dict[str, float]):
        """Đặt baseline score cho mỗi test case"""
        self.baselines = results
    
    def run_and_check(self, agent_func: Callable) -> Dict:
        """
        Chạy agent và check regression.
        
        agent_func: function(prompt) -> output
        
        Returns:
        {
            "total": N,
            "passed": N,
            "regressions": [...],
            "improvements": [...],
            "score_delta": float,
        }
        """
        results = {}
        regressions = []
        improvements = []
        
        for test in self.test_cases:
            output = agent_func(test["prompt"])
            
            # Score against golden
            if test["validator"]:
                score = 100.0 if test["validator"](output) else 0.0
            else:
                score = self._similarity_score(output, test["golden"])
            
            results[test["id"]] = score
            
            # Check regression
            baseline = self.baselines.get(test["id"], 50.0)
            if score < baseline - 10:  # 10% threshold
                regressions.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
            elif score > baseline + 10:
                improvements.append({
                    "id": test["id"],
                    "baseline": baseline,
                    "current": score,
                    "delta": score - baseline,
                })
        
        # Calculate overall
        avg_score = sum(results.values()) / len(results) if results else 0
        avg_baseline = sum(self.baselines.values()) / len(self.baselines) if self.baselines else 50
        
        return {
            "total": len(self.test_cases),
            "passed": sum(1 for s in results.values() if s >= 70),
            "regressions": regressions,
            "improvements": improvements,
            "avg_score": avg_score,
            "score_delta": avg_score - avg_baseline,
            "has_regression": len(regressions) > 0,
        }
    
    def _similarity_score(self, actual: str, expected: str) -> float:
        """Simple text similarity score"""
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        
        if not expected_words:
            return 100.0
        
        intersection = actual_words & expected_words
        return (len(intersection) / len(expected_words)) * 100
```

</details>

---

## 5. Continuous Improvement

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Continuous Improvement là vòng lặp "đo → phân tích → chỉnh sửa → kiểm tra lại", dùng kết quả đánh giá để cải thiện prompt, tooling và kiến thức cho agent.
> **Ẩn dụ/so sánh:** Như việc tập gym: đo cân nặng (measure), xem vì sao chưa giảm (analyze), đổi bài tập (improve), rồi cân lại để biết có hiệu quả không (verify) — lặp đi lặp lại mỗi tuần.
> **Vì sao quan trọng:** AI agent chỉ tốt hơn qua từng bước chỉnh sửa có đo lường; thiếu vòng lặp này nó sẽ đứng yên mãi ở mức hiện tại.

### 5.1 Improvement Loop

Sơ đồ trên là **vòng lặp cải tiến 5 bước**: Đo (measure) → Phân tích (analyze) → Xác định vấn đề (identify) → Sửa (improve) → Kiểm tra lại (verify) rồi quay lại từ đầu. Hãy đọc như công thức chạy một vòng "bảo dưỡng" cho agent; mỗi tuần hoặc mỗi sprint lặp một lần.

```
┌──────────────────────────────────────────────────────────────────┐
│              CONTINUOUS IMPROVEMENT LOOP                          │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  1. MEASURE│   │ 2. ANALYZE│   │ 3. IDENTIFY│               │
│  │  Collect   │──►│ Find     │──►│ Top 3    │                  │
│  │  metrics   │   │ patterns │   │ issues   │                  │
│  └──────────┘    └──────────┘    └────┬─────┘                  │
│                                       │                          │
│                                       ▼                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │  5. VERIFY│   │ 4. IMPROVE│   │  Plan    │                  │
│  │  Re-run   │◄──│ Update   │◄──│ Fix     │                   │
│  │  benchmark│   │ prompts  │   │ strategy│                    │
│  └─────┬────┘    └──────────┘    └──────────┘                  │
│        │                                                        │
│        └───► Back to 1. MEASURE                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Dict, List, Tuple

class ImprovementTracker:
    """
    Theo dõi improvement qua mỗi iteration.
    
    Tracks:
    - Benchmark scores over time
    - Regression detection
    - Improvement suggestions
    """
    
    def __init__(self):
        self.iterations: List[Dict] = []
        self.baselines: Dict[str, float] = {}
    
    def set_baseline(self, benchmark_name: str, scores: Dict):
        """Đặt baseline cho benchmark"""
        self.baselines[benchmark_name] = scores
    
    def record_iteration(self, iteration_id: str,
                         benchmark_name: str,
                         scores: Dict[str, float]):
        """Ghi kết quả iteration"""
        self.iterations.append({
            "id": iteration_id,
            "benchmark": benchmark_name,
            "scores": scores,
            "timestamp": datetime.now().isoformat(),
        })
    
    def analyze_trend(self, benchmark_name: str) -> Dict:
        """Phân tích trend qua các iterations"""
        relevant = [
            i for i in self.iterations 
            if i["benchmark"] == benchmark_name
        ]
        
        if len(relevant) < 2:
            return {"trend": "insufficient_data"}
        
        # Compare first and last
        first = relevant[0]["scores"]
        last = relevant[-1]["scores"]
        
        improvements = {}
        regressions = {}
        
        for metric in last:
            if metric in first:
                change = last[metric] - first[metric]
                if change > 0:
                    improvements[metric] = change
                elif change < 0:
                    regressions[metric] = abs(change)
        
        return {
            "iterations": len(relevant),
            "improvements": improvements,
            "regressions": regressions,
            "overall_trend": "improving" if not regressions else "mixed",
        }
    
    def suggest_improvements(self, 
                              eval_results: List[EvaluationResult]
                              ) -> List[str]:
        """Gợi ý cải tiến dựa trên evaluation results"""
        suggestions = []
        
        # Find consistently low scores
        dim_avgs = {}
        for result in eval_results:
            for dim, score in result.scores.items():
                if dim not in dim_avgs:
                    dim_avgs[dim] = []
                dim_avgs[dim].append(score)
        
        for dim, scores in dim_avgs.items():
            avg = sum(scores) / len(scores)
            if avg < 60:
                suggestions.append(
                    f"⚠️ {dim}: Average score {avg:.1f}/100. "
                    f"Consider improving prompts or adding "
                    f"specific rules for {dim}."
                )
            elif avg < 80:
                suggestions.append(
                    f"💡 {dim}: Score {avg:.1f}/100. "
                    f"Room for improvement with "
                    f"better context or examples."
                )
        
        return suggestions
```

</details>

### 5.2 A/B Testing Framework

`ABTestFramework` so sánh **hai phiên bản** — ví dụ prompt A và prompt B — trên cùng một bộ benchmark để biết bản nào tốt hơn. Như thử hai công thức pha cà phê cho khách thử theo nhóm rồi đếm ly nào được khen nhiều hơn; quyết định dựa trên dữ liệu, không dựa trên "cảm giác".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ABTestFramework:
    """
    A/B testing cho prompt engineering.
    
    So sánh 2 versions của prompt/harness
    trên cùng một benchmark suite.
    
    Giống như A/B testing cho web,
    nhưng áp dụng cho AI agent configuration.
    """
    
    def __init__(self, benchmark_suite: BenchmarkSuite):
        self.suite = benchmark_suite
        self.results = {"A": None, "B": None}
    
    def run_variant(self, variant: str, 
                    agent_func: Callable) -> Dict:
        """Chạy một variant"""
        self.results[variant] = self.suite.run(agent_func)
        return self.results[variant]
    
    def analyze(self) -> Dict:
        """
        Phân tích kết quả A/B test.
        
        Dùng statistical significance test
        để quyết định variant nào tốt hơn.
        """
        if not all(self.results.values()):
            return {"error": "Both variants must be run first"}
        
        a_summary = self.results["A"]
        b_summary = self.results["B"]
        
        # Simple comparison
        metrics = {}
        for key in a_summary:
            if isinstance(a_summary[key], (int, float)):
                a_val = a_summary[key]
                b_val = b_summary.get(key, 0)
                metrics[key] = {
                    "A": a_val,
                    "B": b_val,
                    "delta": b_val - a_val,
                    "winner": "A" if a_val > b_val else "B",
                }
        
        # Overall winner (by success rate)
        a_rate = a_summary.get("success_rate", 0)
        b_rate = b_summary.get("success_rate", 0)
        
        return {
            "metrics": metrics,
            "overall_winner": "A" if a_rate >= b_rate else "B",
            "confidence": "high" if abs(a_rate - b_rate) > 0.1 else "low",
        }
```

</details>

---

## 6. Reporting & Dashboards

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Reporting & Dashboards là cách trình bày trực quan kết quả đánh giá — metrics theo thời gian, so sánh phiên bản, phát hiện suy giảm — để cả đội "nhìn một cái là hiểu" sức khỏe của agent.
> **Ẩn dụ/so sánh:** Như đồng hồ tốc độ trên xe: bạn không cần bấm giờ từng mét, chỉ cần nhìn kim là biết đang chạy nhanh hay chậm, cần đạp ga hay rà phanh.
> **Vì sao quan trọng:** Kết quả đánh giá nằm im trong file log chẳng giúp ai ra quyết định; phải hiển thị rõ thì đội mới phản ứng kịp khi chất lượng tụt dốc.

### 6.1 Evaluation Report Generator

`EvaluationReporter` tự tạo báo cáo từ kết quả đánh giá ở nhiều định dạng: Markdown để đăng lên PR, JSON cho máy đọc, và dữ liệu cho dashboard trực quan. Như chiếc máy in biên bản cuối ngày của nhà máy: chỉ cần nạp số liệu, nó in ra bảng tổng kết sẵn sàng gửi cho đội ngũ.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from datetime import datetime
from typing import Dict, List

class EvaluationReporter:
    """
    Tạo báo cáo evaluation — markdown, JSON, hoặc dashboard.
    """
    
    def generate_markdown_report(self, 
                                  results: List[EvaluationResult],
                                  summary: Dict) -> str:
        """Tạo báo cáo Markdown"""
        report = []
        report.append("# 📊 Evaluation Report")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Tasks Evaluated:** {len(results)}")
        
        # Summary
        report.append("\n## Summary\n")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Total Tasks | {summary.get('total', 0)} |")
        report.append(f"| Success Rate | {summary.get('success_rate', 0):.1%} |")
        report.append(f"| Avg Quality Score | {summary.get('avg_quality', 0):.1f} |")
        report.append(f"| Total Tokens | {summary.get('total_tokens', 0):,} |")
        
        # Per-dimension scores
        report.append("\n## Dimension Scores\n")
        report.append("| Dimension | Avg Score | Status |")
        report.append("|-----------|-----------|--------|")
        
        for dim, score in summary.get("dimension_scores", {}).items():
            status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
            report.append(f"| {dim} | {score:.1f} | {status} |")
        
        # Top issues
        report.append("\n## Top Issues\n")
        for i, issue in enumerate(summary.get("top_issues", []), 1):
            report.append(f"{i}. {issue}")
        
        # Individual results
        report.append("\n## Task Results\n")
        for result in results:
            status = "✅" if result.total_score >= 70 else "❌"
            report.append(
                f"### {status} {result.task_id}\n"
            )
            report.append(f"**Score:** {result.total_score:.1f}/100\n")
            
            for dim, score in result.scores.items():
                bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
                note = result.notes.get(dim, "")
                report.append(
                    f"- `{dim}`: {bar} {score:.0f}/100"
                    f"{f' — {note}' if note else ''}"
                )
            report.append("")
        
        return "\n".join(report)
    
    def generate_json_report(self,
                              results: List[EvaluationResult],
                              summary: Dict) -> Dict:
        """Tạo báo cáo JSON"""
        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_tasks": len(results),
            },
            "summary": summary,
            "results": [
                {
                    "task_id": r.task_id,
                    "total_score": r.total_score,
                    "scores": r.scores,
                    "notes": r.notes,
                }
                for r in results
            ],
        }
    
    def generate_dashboard_data(self, 
                                 results: List[EvaluationResult]) -> Dict:
        """Generate data cho visual dashboard"""
        return {
            "timeline": self._build_timeline(results),
            "distribution": self._build_distribution(results),
            "heatmap": self._build_heatmap(results),
        }
    
    def _build_timeline(self, results: List) -> List:
        """Build timeline data cho chart"""
        return [
            {
                "date": r.timestamp,
                "score": r.total_score,
                "task": r.task_id,
            }
            for r in results
        ]
    
    def _build_distribution(self, results: List) -> Dict:
        """Build score distribution"""
        ranges = {
            "0-20": 0, "20-40": 0, "40-60": 0,
            "60-80": 0, "80-100": 0
        }
        
        for r in results:
            score = r.total_score
            if score < 20:
                ranges["0-20"] += 1
            elif score < 40:
                ranges["20-40"] += 1
            elif score < 60:
                ranges["40-60"] += 1
            elif score < 80:
                ranges["60-80"] += 1
            else:
                ranges["80-100"] += 1
        
        return ranges
    
    def _build_heatmap(self, results: List) -> List:
        """Build heatmap data (task x dimension)"""
        dimensions = set()
        for r in results:
            dimensions.update(r.scores.keys())
        
        heatmap = []
        for r in results:
            row = {"task": r.task_id}
            for dim in sorted(dimensions):
                row[dim] = r.scores.get(dim, 0)
            heatmap.append(row)
        
        return heatmap
```

</details>

---

## 7. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies là những ví dụ đánh giá ngoài đời thật — SWE-bench, HumanEval, pipeline sản xuất — cho thấy cách người ta thiết lập metrics, chấm agent cụ thể và rút ra bài học cải thiện.
> **Ẩn dụ/so sánh:** Như đọc báo cáo sau trận bóng: xem đội này phối hợp ra sao, ghi bàn kiểu gì, thua ở khâu nào — để rút kinh nghiệm đưa vào trận sau thay vì chỉ dừng ở tỉ số.
> **Vì sao quan trọng:** Lý thuyết khô khan sẽ dễ hiểu hơn rất nhiều khi nhìn nó hoạt động trong bối cảnh thật.

### 7.1 SWE-bench — Benchmarking AI Code Agents

**Bối cảnh**: SWE-bench là benchmark tiêu chuẩn đánh giá khả năng sửa lỗi real-world của AI agents trên các GitHub repositories thực tế. Nói đơn giản, nó lấy các bug thật từ những dự án mã nguồn mở, đưa cho agent sửa, rồi chạy lại đúng bộ test của dự án đó để xem agent có "đóng" được issue hay không — như trả bài bằng đúng đề thi thật thay vì câu hỏi tự chế.

**Kết quả thực tế**:

```
┌────────────────────────────────────────────────────────────────┐
│                 SWE-BENCH RESULTS 2026                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Agent              │ Verified │ Lite  │ Full  │ Cost/Task     │
│  ───────────────────┼──────────┼───────┼───────┼──────────────│
│  Claude Code+Harness│ 53%      │ 48%   │ 42%   │ ~$2.50       │
│  Devin              │ 48%      │ 44%   │ 38%   │ ~$8.00       │
│  OpenHands+SWE      │ 45%      │ 42%   │ 35%   │ ~$3.00       │
│  Cursor (agent)     │ 42%      │ 38%   │ 32%   │ ~$1.50       │
│  GitHub Copilot     │ 35%      │ 33%   │ 28%   │ ~$0.50       │
│  SWE-agent (base)   │ 20%      │ 20%   │ 15%   │ ~$1.00       │
│                                                                │
│  Key Insight: Harness design accounts for 30%+ of             │
│  the performance difference between agents!                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Key Learnings:**
1. Harness design impact > model choice
2. Tool permissions affect safety significantly
3. Context management affects token cost
4. Multi-agent improves complex task handling

### 7.2 HumanEval — Classic Code Generation

Bảng này theo dõi sự tiến bộ của các model trên HumanEval — benchmark kinh điển của OpenAI với các bài viết hàm Python đơn lẻ — từ 2023 đến 2026. Cột Improvement cho thấy model tăng bao nhiêu phần trăm. Điểm đáng chú ý: các model lớn đã chạm trần khoảng 90%, nên giới nghiên cứu phải chuyển sang benchmark khó hơn như SWE-bench — hãy đọc kỹ chú thích ⚠️ ở cuối bảng.

```
┌────────────────────────────────────────────────────────────────┐
│                 HUMANEVAL EVOLUTION                             │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Model            │ Pass@1 (2023) │ Pass@1 (2026) │ Improvement│
│  ─────────────────┼───────────────┼───────────────┼───────────│
│  GPT-3.5 Turbo    │ 48%           │ 72%           │ +50%      │
│  GPT-4            │ 67%           │ 86%           │ +28%      │
│  Claude 3.5 Sonnet│ -             │ 92%           │ -         │
│  Gemini 2.5 Pro   │ -             │ 88%           │ -         │
│  DeepSeek-V3      │ -             │ 90%           │ -         │
│                                                                │
│  ⚠️ HumanEval reaching ceiling — need harder benchmarks      │
│     → SWE-bench, LiveCodeBench becoming more relevant         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 7.3 Real-World Evaluation Pipeline — Production Case

Đây là ví dụ **một đội 20 dev dùng pipeline đánh giá hàng ngày trong sản xuất**: chạy benchmark vào ban đêm, kiểm tra regression, sinh report và cảnh báo tức thì nếu chất lượng tụt. Đọc như "bản thiết kế mẫu" cho pipeline của riêng bạn — học cách team thật tổ chức giám sát liên tục chứ không chỉ đánh giá một lần.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# Real-world example: How a team evaluates their AI coding agent

class ProductionEvaluator:
    """
    Production evaluation pipeline được dùng hàng ngày.
    
    Context: Team 20 developers sử dụng AI coding agent
    daily. Pipeline chạy mỗi đêm để monitor quality.
    """
    
    def __init__(self):
        self.benchmark_suite = BenchmarkSuite("daily")
        self.regression_suite = RegressionTestSuite("production")
        self.reporter = EvaluationReporter()
    
    def setup_daily_benchmarks(self):
        """Setup benchmark tasks cho daily run"""
        
        # 10 representative tasks cho team's domain
        self.benchmark_suite.add_task(
            "fix-001", "Fix null pointer in UserService.getProfile",
            validator=lambda out: "null check" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "feat-001", "Add pagination to ProductController.list",
            validator=lambda out: "offset" in str(out).lower() or 
                                   "limit" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "test-001", "Write unit tests for PaymentService.charge",
            validator=lambda out: "assert" in str(out).lower()
        )
        
        self.benchmark_suite.add_task(
            "refactor-001", "Extract database queries to repository pattern",
            validator=lambda out: "Repository" in str(out)
        )
        
        self.benchmark_suite.add_task(
            "security-001", "Fix SQL injection in UserDAO.findByEmail",
            validator=lambda out: "parameterized" in str(out).lower() or
                                   "prepared" in str(out).lower()
        )
    
    def run_daily_evaluation(self, agent_func: Callable) -> Dict:
        """Chạy evaluation hàng ngày"""
        
        # 1. Run benchmarks
        summary = self.benchmark_suite.run(agent_func)
        
        # 2. Check regression
        reg_result = self.regression_suite.run_and_check(agent_func)
        
        # 3. Generate report
        report = self.reporter.generate_markdown_report(
            [],  # Would pass actual results
            summary
        )
        
        # 4. Alert if regression detected
        if reg_result["has_regression"]:
            self._send_alert(reg_result)
        
        # 5. Track trend
        return {
            "summary": summary,
            "regression": reg_result,
            "report": report,
        }
    
    def _send_alert(self, reg_result: Dict):
        """Gửi alert khi regression detected"""
        regressions = reg_result["regressions"]
        message = f"⚠️ REGRESSION DETECTED!\n"
        message += f"Score delta: {reg_result['score_delta']:.1f}%\n"
        for reg in regressions:
            message += f"  - {reg['id']}: {reg['baseline']:.0f} → {reg['current']:.0f}\n"
        
        # Would send to Slack, email, etc.
        print(message)
```

</details>

---

## 8. Evaluation Tooling

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Evaluation Tooling là bộ công cụ hỗ trợ quy trình đánh giá — benchmark suites, framework chấm điểm, code quality tools, security scanners — giúp đánh giá tự động, lặp lại và đáng tin cậy.
> **Ẩn dụ/so sánh:** Như bộ dụng cụ sửa xe đầy đủ: mỗi loại chìa khóa, máy đo, máy chẩn đoán phục vụ một việc. Không có dụng cụ thì thợ phải mò bằng tay, vừa lâu vừa dễ sai.
> **Vì sao quan trọng:** Xây evaluation từ tay trắng rất tốn kém; tận dụng công cụ có sẵn để dồn sức vào việc chính là đo lường và cải thiện.

### 8.1 Popular Evaluation Tools

Sơ đồ này chia hệ sinh thái công cụ evaluation thành 4 nhóm: benchmark suites (bộ đề), evaluation frameworks (bộ khung chấm điểm), code quality tools (quét chất lượng code) và security scanners (quét lỗ hổng bảo mật). Chọn công cụ theo đúng vai trò từng nhóm — bạn không cần dùng hết, chỉ lấy cái phù hợp với giai đoạn mình đang ở.

```
┌──────────────────────────────────────────────────────────────────┐
│                 EVALUATION TOOLS ECOSYSTEM                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BENCHMARK SUITES:                                               │
│  ├── HumanEval (OpenAI) — Classic code gen benchmark           │
│  ├── SWE-bench (Princeton) — Real-world bug fix                │
│  ├── MBPP (Google) — Mostly Basic Python Problems              │
│  ├── LiveCodeBench — Live competition-style tasks               │
│  └── BigCodeBench — Complex function-level tasks               │
│                                                                  │
│  EVALUATION FRAMEWORKS:                                          │
│  ├── PromptFoo — Prompt testing & evaluation                    │
│  ├── DeepEval — LLM evaluation framework                        │
│  ├── RAGAS — RAG-specific evaluation                            │
│  ├── LangSmith — Tracing & evaluation                           │
│  └── Weights & Biases — Experiment tracking                     │
│                                                                  │
│  CODE QUALITY TOOLS:                                             │
│  ├── SonarQube — Code quality & security                        │
│  ├── ESLint/Prettier — Style checking                           │
│  ├── Pylint/Ruff — Python linting                                │
│  ├── pytest — Test runner                                        │
│  └── Coverage.py — Test coverage                                 │
│                                                                  │
│  SECURITY SCANNERS:                                              │
│  ├── Bandit — Python security                                   │
│  ├── Semgrep — Multi-language security                           │
│  ├── npm audit — Node.js vulnerabilities                        │
│  └── Snyk — Dependency scanning                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 PromptFoo Configuration Example

Cấu hình YAML này giúp bạn chạy PromptFoo — công cụ test prompt phổ biến — trên agent coding: khai báo provider (model nào), prompt nào, và các assertion (điều kiện output phải thỏa). Giống viết "hợp đồng kiểm tra": máy sẽ tự chấm xem model có đạt từng điều kiện đề ra hay không (ví dụ `contains` hoặc `llm-rubric`).

<details>
<summary><b>8.2 PromptFoo Configuration Example (Click to expand/collapse)</b></summary>

```yaml
# promptfooconfig.yaml
# Configuration cho PromptFoo evaluation

description: "AI Coding Agent Evaluation"

providers:
  - id: "openai:gpt-4o"
    config:
      temperature: 0
  - id: "anthropic:messages:claude-3.5-sonnet"
    config:
      temperature: 0

prompts:
  - file://prompts/v1.txt
  - file://prompts/v2.txt

tests:
  - description: "Fix null pointer bug"
    vars:
      task: "Fix the null pointer in UserService.getProfile"
      file_content: "{{fixture.userservice}}"
    assert:
      - type: contains
        value: "null check"
      - type: llm-rubric
        value: "Code handles null case properly, no runtime errors"
  
  - description: "Add pagination"
    vars:
      task: "Add pagination to ProductController.list"
      file_content: "{{fixture.productcontroller}}"
    assert:
      - type: contains
        value: "offset"
      - type: contains
        value: "limit"
      - type: llm-rubric
        value: "Pagination is correctly implemented with proper defaults"

  - description: "Security fix"
    vars:
      task: "Fix SQL injection in UserDAO.findByEmail"
      file_content: "{{fixture.userdao}}"
    assert:
      - type: llm-rubric
        value: "Uses parameterized queries, no string concatenation for SQL"

metrics:
  correctness:
    weight: 0.3
  quality:
    weight: 0.25
  safety:
    weight: 0.25
  efficiency:
    weight: 0.2
```

</details>

---

## 9. Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là tập hợp các nguyên tắc đánh giá đã được chứng minh hiệu quả — test case chất lượng, tránh data leakage, cập nhật thường xuyên — giúp đo lường agent chính xác và đáng tin.
> **Ẩn dụ/so sánh:** Như quy tắc an toàn trong bếp chuyên nghiệp: tay rửa sạch, dao để riêng, kiểm tra hạn dùng — áp dụng đều đặn để tránh tai nạn và món ăn luôn đạt chuẩn.
> **Vì sao quan trọng:** Hầu hết sai lầm trong evaluation đều có người gặp trước; học theo kinh nghiệm để không tự đạp vào vết xe đổ.

### 9.1 DO và DON'T

Đây là "bảng điều luật" gọn nhất để không đánh giá sai: **10 điều NÊN làm** (chẳng hạn tự động hóa mọi thứ, theo dõi baseline) và **8 điều KHÔNG nên làm** (chẳng hạn chỉ dùng một metric duy nhất). Hãy dùng như checklist khi xây hệ thống evaluation.

```
┌──────────────────────────────────────────────────────────────────┐
│              EVALUATION BEST PRACTICES                           │
│                                                                  │
│  ✅ DO:                                                          │
│                                                                  │
│  1. AUTOMATE EVERYTHING                                         │
│     Evaluation phải tự động, không manual                      │
│     → Consistent, repeatable, scalable                         │
│                                                                  │
│  2. MULTIPLE DIMENSIONS                                         │
│     Không chỉ check "đúng/sai"                                 │
│     → Quality + Correctness + Efficiency + Safety               │
│                                                                  │
│  3. REGULAR BENCHMARKS                                          │
│     Chạy benchmark định kỳ (mỗi PR, mỗi week)                │
│     → Catch regressions early                                   │
│                                                                  │
│  4. BASELINE TRACKING                                           │
│     Lưu baseline để so sánh                                    │
│     → Know if you're improving or regressing                   │
│                                                                  │
│  5. ACTIONABLE FEEDBACK                                          │
│     Kết quả phải gợi ý hành động cụ thể                       │
│     → "Fix X" not just "Score is low"                          │
│                                                                  │
│  6. BALANCED METRICS                                             │
│     Đừng optimize 1 metric mà sacrifice metric khác            │
│     → Trade-offs are real                                       │
│                                                                  │
│  7. HUMAN CALIBRATION                                            │
│     Định kỳ đối chiếu auto-eval với human review              │
│     → Ensure evaluation quality                                 │
│                                                                  │
│  8. TEST EDGE CASES                                              │
│     Benchmark phải có diverse difficulty levels                │
│     → Don't just test the easy stuff                            │
│                                                                  │
│  9. MONITOR COST                                                  │
│     Track token cost per evaluation                              │
│     → Evaluation shouldn't cost more than the value             │
│                                                                  │
│  10. SHARE RESULTS                                                │
│      Publish evaluation results for team transparency           │
│      → Build trust in AI coding tools                           │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ DON'T:                                                       │
│                                                                  │
│  1. Don't use a single metric                                    │
│  2. Don't ignore regressions                                     │
│  3. Don't benchmark on trivial tasks only                       │
│  4. Don't trust auto-eval without human calibration            │
│  5. Don't optimize for benchmark at expense of real usage      │
│  6. Don't forget to evaluate cost/efficiency                   │
│  7. Don't skip evaluation after prompt changes                  │
│  8. Don't compare across different benchmark setups            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 9.2 Evaluation Strategy

Kim tự tháp này cho bạn **tần suất và độ đắt đỏ của từng tầng kiểm tra**: tầng dưới rẻ và chạy liên tục (static analysis mỗi lần gõ phím), tầng trên đắt hơn và chạy thưa hơn (E2E test mỗi tuần). Ý tưởng: dùng tầng nhanh và rẻ để bắt lỗi sớm với khối lượng lớn, để tầng chậm và đắt chỉ xử lý phần tinh túy còn lại.

```
┌──────────────────────────────────────────────────────────────────┐
│              EVALUATION STRATEGY PYRAMID                         │
│                                                                  │
│                        ┌──────────┐                              │
│                        │ E2E Test │ ← Real user scenarios       │
│                        │ (Weekly) │    Slow, expensive           │
│                       ┌┴──────────┴┐                            │
│                       │ Integration │ ← Multi-component tests  │
│                       │   (Daily)   │    Medium speed           │
│                      ┌┴─────────────┴┐                         │
│                      │ Unit Tests     │ ← Individual functions │
│                      │   (Per Commit) │    Fast, cheap          │
│                     ┌┴───────────────┴┐                        │
│                     │ Static Analysis  │ ← Lint, type check    │
│                     │   (Continuous)   │    Instant             │
│                    ┌┴─────────────────┴┐                       │
│                    │ Code Review        │ ← Human + AI review  │
│                    │   (Continuous)     │    Quality gate        │
│                    └───────────────────┘                        │
│                                                                  │
│  Strategy:                                                      │
│  - Static analysis: Every keystroke (IDE)                       │
│  - Unit tests: Every commit                                     │
│  - Integration: Daily                                           │
│  - E2E: Weekly                                                  │
│  - Regression: Every prompt change                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Case Studies Thực Tế

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies Thực Tế là những ví dụ evaluation đã triển khai ngoài sản xuất — SWE-bench, Aider, LiveCodeBench, Anthropic — minh họa cách thiết kế benchmark, chấm điểm agent cụ thể và rút ra bài học cải thiện.
> **Ẩn dụ/so sánh:** Như xem phim tài liệu về cách các công ty lớn vận hành: không chỉ lý thuyết suông, mà nhìn trực tiếp họ ra quyết định, sai chỗ nào, hay chỗ nào để áp dụng cho mình.
> **Vì sao quan trọng:** Mỗi case study là một bài học đã được người khác trả phí; học từ đó giúp bạn chọn đúng benchmark và tránh lặp lại sai lầm.

### 10.1 Princeton NLP SWE-bench: Benchmarking Real-World Code

Case study này phân tích SWE-bench — benchmark sửa bug thật từ 2294 GitHub issues. Bảng leaderboard cho thấy tỷ lệ resolve, token và chi phí của từng hệ thống; điểm đáng chú ý là **chi phí chênh nhau tới 10 lần giữa các hệ thống có chất lượng tương đương**. Phần EVALUATION METHODOLOGY mô tả quy trình chấm 5 bước mà bạn có thể áp dụng lại cho benchmark của riêng mình.

```
┌──────────────────────────────────────────────────────────────────┐
│                    SWE-BENCH EVALUATION                           │
│                                                                  │
│  WHAT: Benchmark từ 2294 GitHub issues với ground-truth patches │
│  HOW: Agent phải reproduce bug fix từ issue description         │
│  METRIC: % issues resolved (pass unit tests)                    │
│                                                                  │
│  LEADERBOARD (2024-2025):                                        │
│  ┌────────────────────┬──────────┬───────────┬───────────────┐  │
│  │ System             │ Resolve  │ Token Use │ Cost/Issue    │  │
│  ├────────────────────┼──────────┼───────────┼───────────────┤  │
│  │ Amazon Q           │ 26.0%    │ ~20K      │ ~$0.50        │  │
│  │ Agentless          │ 24.0%    │ ~15K      │ ~$0.30        │  │
│  │ SWE-agent+GPT-4    │ 22.7%    │ ~25K      │ ~$0.50        │  │
│  │ AutoCodeRover      │ 19.0%    │ ~18K      │ ~$0.40        │  │
│  │ Aider+GPT-4o       │ 18.5%    │ ~20K      │ ~$0.40        │  │
│  │ OpenHands+CodeAct  │ 17.0%    │ ~30K      │ ~$0.60        │  │
│  └────────────────────┴──────────┴───────────┴───────────────┘  │
│                                                                  │
│  KEY INSIGHTS:                                                   │
│  → LLM + Agent loop ≠ always better than simple retrieval      │
│  → Agentless approaches (no LLM in loop) often competitive      │
│  → Search/retrieval quality matters more than model size        │
│  → Cost varies 10x across systems for same quality              │
│                                                                  │
│  EVALUATION METHODOLOGY:                                         │
│  1. Run agent on each issue (with timeout + token budget)       │
│  2. Apply generated patch to codebase                           │
│  3. Run existing test suite                                     │
│  4. Check if failing tests now pass                             │
│  5. Check if passing tests still pass (regression)              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.2 Aider: LLM Leaderboard for Coding

Case study này là bảng xếp hạng của dự án Aider, chấm LLM qua cách chúng sửa file theo edit-format và chất lượng diff. Điểm mấu chốt nằm ở **phần COST-EFFECTIVENESS**: DeepSeek V3 đạt 92% chất lượng của GPT-4o nhưng chỉ tốn 11% chi phí — minh họa rằng model rẻ có thể là lựa chọn tối ưu cho task thường.

```
┌──────────────────────────────────────────────────────────────────┐
│                 AIDER LLM LEADERBOARD                             │
│                                                                  │
│  BENCHMARK: Edit-format compliance + code quality               │
│  METHODOLOGY: LLM edits whole files, judge by diff quality     │
│                                                                  │
│  TOP MODELS (2024-2025):                                        │
│  ┌────────────────────┬──────────┬───────────┬───────────────┐  │
│  │ Model              │ Score    │ Cost/1M   │ Best For      │  │
│  ├────────────────────┼──────────┼───────────┼───────────────┤  │
│  │ Claude 3.5 Sonnet  │ 74%      │ $3/$15    │ Complex tasks  │  │
│  │ GPT-4o             │ 70%      │ $2.5/$10  │ General code   │  │
│  │ DeepSeek V3        │ 68%      │ $0.27/$1.1│ Budget tasks   │  │
│  │ Gemini 1.5 Pro     │ 66%      │ $1.25/$5  │ Long context   │  │
│  │ Claude 3 Haiku     │ 58%      │ $0.25/$1.2│ Fast/cheap     │  │
│  └────────────────────┴──────────┴───────────┴───────────────┘  │
│                                                                  │
│  COST-EFFECTIVENESS RANKING:                                     │
│  1. DeepSeek V3: 68% score at $0.27/1M tokens (best value)    │
│  2. Claude 3.5 Sonnet: 74% score at $3/1M tokens (best quality)│
│  3. GPT-4o: 70% score at $2.5/1M tokens (balanced)             │
│                                                                  │
│  INSIGHT: DeepSeek V3 achieves 92% of GPT-4o quality at 11%   │
│  of the cost — making it the best choice for routine tasks.     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.3 LiveCodeBench: Dynamic Evaluation

LiveCodeBench giải quyết điểm yếu của benchmark tĩnh: model có thể đã "học lậu" dữ liệu cũ hoặc bộ đề dần lỗi thời. Vì vậy đề thi được **cập nhật hàng tuần bằng bài mới từ các nền tảng thi đấu lập trình**, kèm phát hiện contamination. Sơ đồ pipeline Scrape → Dedupe → Validate → Run LLM là quy trình "sản xuất đề thi" liên tục.

```
┌──────────────────────────────────────────────────────────────────┐
│              LIVECODEBENCH DYNAMIC BENCHMARK                      │
│                                                                  │
│  PROBLEM WITH STATIC BENCHMARKS:                                 │
│  → Models may have been trained on benchmark data               │
│  → Static benchmarks become stale over time                     │
│  → Leaderboard gaming possible                                  │
│                                                                  │
│  SOLUTION: Continuously updated benchmark                       │
│  → New problems added weekly from contest platforms             │
│  → Temporal awareness (problems after training cutoff)          │
│  → Contamination detection built-in                             │
│                                                                  │
│  EVALUATION PIPELINE:                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Scrape   │───►│  Dedupe  │───►│ Validate │───►│  Run LLM │ │
│  │ Problems │    │  & Clean │    │  Tests   │    │  (temp)  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │         │
│  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    │
│  │ Contest │    │ Remove  │    │ Generate │    │ Pass/Fail│   │
│  │ Platforms│   │ duplicates│   │ test cases│   │ + Time   │   │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│                                                                  │
│  METRICS TRACKED:                                                │
│  → Pass@1: Does the first solution work?                       │
│  → Pass@10: Does any of 10 solutions work?                     │
│  → Time-to-solution: How fast?                                  │
│  → Token efficiency: Tokens per correct solution                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.4 Anthropic's Evaluation Methodology

Anthropic đánh giá theo **4 tầng**, từ máy (automated benchmarks) đến người (human evaluation) rồi đến thực tế (real user feedback, A/B testing) — vì không tầng nào đơn lẻ kể trọn câu chuyện. Chuẩn họ dùng nhiều là **Acceptance Rate** (tỷ lệ dev chấp nhận gợi ý của AI). Đây là mô hình "đánh giá nhiều nguồn" đáng bắt chước thay vì chỉ dựa một con số.

```
┌──────────────────────────────────────────────────────────────────┐
│            ANTHROPIC EVALUATION METHODOLOGY                       │
│                                                                  │
│  PRINCIPLE: "Eval what matters, not what's easy to measure"     │
│                                                                  │
│  EVALUATION LAYERS:                                              │
│                                                                  │
│  LAYER 1: AUTOMATED BENCHMARKS                                  │
│  → HumanEval, SWE-bench, internal benchmarks                   │
│  → Fast, scalable, objective                                    │
│  → Limitation: May not reflect real-world usage                │
│                                                                  │
│  LAYER 2: HUMAN EVALUATION                                       │
│  → Expert reviewers rate code quality                          │
│  → Assess: Readability, maintainability, correctness           │
│  → Limitation: Slow, expensive, subjective                     │
│                                                                  │
│  LAYER 3: REAL USER FEEDBACK                                     │
│  → Track acceptance rate of suggestions                        │
│  → Measure time saved vs manual coding                         │
│  → Limitation: Noisy signal, many confounders                  │
│                                                                  │
│  LAYER 4: A/B TESTING                                            │
│  → Compare model versions on real tasks                        │
│  → Statistical significance testing                             │
│  → Limitation: Requires large sample sizes                     │
│                                                                  │
│  KEY METRIC: "Acceptance Rate" (% of AI suggestions accepted)   │
│  → High acceptance = AI is useful                               │
│  → Low acceptance = Need to improve                            │
│  → Tracked across: task type, complexity, user experience      │
│                                                                  │
│  COST AWARENESS:                                                 │
│  → Track $ per quality point                                    │
│  → Optimize model routing (cheap model for easy tasks)          │
│  → Set token budgets per task type                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

### 10.5 DeepSeek Harness — Minimal Benchmark Harness for Unbiased Evaluation

**Bối cảnh**: DeepSeek Harness cung cấp **Minimal Benchmark Harness** — một chế độ đánh giá tối giản chỉ với **2 tools: `bash` và `editor`**, được thiết kế để loại bỏ bias từ tool selection và cung cấp môi trường cách ly sạch cho SWE-bench evaluation.

<details>
<summary><b>Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * Minimal Benchmark Harness
 * 
 * Core Philosophy:
 * - "Less is More" — Chỉ 2 tools: bash + editor
 * - Clean isolation — No LLM-powered tools, no search, no memory
 * - Deterministic — Container-based isolation for reproducibility
 * - Unbiased — LLM không thể "cheat" bằng cách dùng tools nâng cao
 * 
 * Repo: DeepSeek Harness (internal)
 * Used for: SWE-bench, LiveCodeBench, custom benchmarks
 */

// ═══════════════════════════════════════════════
// 1. HARNESS ARCHITECTURE
// ═══════════════════════════════════════════════

interface MinimalHarnessConfig {
  // Isolation settings
  isolation: 'container' | 'vm' | 'process';
  containerImage?: string;      // e.g., 'ubuntu:22.04' with dev tools
  workingDir: string;           // Project directory
  
  // Tool restrictions — ONLY these 2
  allowedTools: ['bash', 'editor'];
  
  // Resource limits
  limits: {
    cpuCores: number;
    memoryMB: number;
    diskMB: number;
    timeoutSeconds: number;
    networkAccess: boolean;
  };
  
  // Evaluation settings
  evaluation: {
    suite: string;              // 'swe-bench', 'livecodebench', 'custom'
    dataset: string;            // Path to dataset
    split: 'train' | 'test' | 'dev';
    maxInstances?: number;
  };
  
  // LLM settings (agent under test)
  llm: {
    model: string;
    temperature: number;
    maxTokens: number;
    systemPrompt: string;
  };
}

interface BenchmarkInstance {
  id: string;                   // e.g., 'django__django-12345'
  repo: string;                 // Repository name
  baseCommit: string;           // Commit to start from
  problemStatement: string;     // Issue description
  hints?: string;               // Optional hints
  testPatch: string;            // Tests that should pass after fix
  envSetup?: string;            // Setup commands
}

interface BenchmarkResult {
  instanceId: string;
  status: 'resolved' | 'failed' | 'error' | 'timeout';
  patch?: string;               // Generated patch/diff
  testsPassed: number;
  testsTotal: number;
  executionTimeMs: number;
  tokensUsed: number;
  toolsUsed: string[];          // Should only be ['bash', 'editor']
  errorMessage?: string;
  trajectory: TrajectoryEvent[]; // For debugging
}

// ═══════════════════════════════════════════════
// 2. TWO TOOLS ONLY
// ═══════════════════════════════════════════════

/**
 * Tool 1: BASH
 * Execute shell commands in the container
 */
interface BashTool {
  type: 'bash';
  command: string;              // Shell command to execute
  timeout?: number;             // Override default timeout
  workdir?: string;             // Working directory
}

// Returns:
interface BashResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  durationMs: number;
}

/**
 * Tool 2: EDITOR
 * File operations: read, write, edit
 */
interface EditorTool {
  type: 'editor';
  action: 'read' | 'write' | 'edit' | 'list' | 'grep';
  path: string;                 // File or directory path
  content?: string;             // For write/edit
  oldString?: string;           // For edit
  newString?: string;           // For edit
  pattern?: string;             // For grep
}

// Returns:
interface EditorResult {
  success: boolean;
  content?: string;             // For read
  files?: string[];             // For list
  matches?: GrepMatch[];        // For grep
  error?: string;
}

interface GrepMatch {
  file: string;
  line: number;
  content: string;
}

// ═══════════════════════════════════════════════
// 3. EXECUTION LOOP
// ═══════════════════════════════════════════════

class MinimalBenchmarkHarness {
  private config: MinimalHarnessConfig;
  private container: ContainerRuntime;
  private trajectory: TrajectoryEvent[] = [];
  
  constructor(config: MinimalHarnessConfig) {
    this.config = config;
    this.container = this.createContainer();
  }
  
  async runInstance(instance: BenchmarkInstance): Promise<BenchmarkResult> {
    const startTime = Date.now();
    const tokensUsed = 0;
    const toolsUsed: string[] = [];
    
    try {
      // 1. Setup environment
      await this.setupEnvironment(instance);
      
      // 2. Run agent loop
      const patch = await this.runAgentLoop(instance);
      
      // 3. Apply patch and run tests
      const testResult = await this.runTests(instance, patch);
      
      return {
        instanceId: instance.id,
        status: testResult.allPassed ? 'resolved' : 'failed',
        patch,
        testsPassed: testResult.passed,
        testsTotal: testResult.total,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        trajectory: this.trajectory,
      };
      
    } catch (error) {
      return {
        instanceId: instance.id,
        status: 'error',
        testsPassed: 0,
        testsTotal: 0,
        executionTimeMs: Date.now() - startTime,
        tokensUsed,
        toolsUsed,
        errorMessage: error.message,
        trajectory: this.trajectory,
      };
    }
  }
  
  private async runAgentLoop(instance: BenchmarkInstance): Promise<string> {
    const messages = [
      { role: 'system', content: this.config.llm.systemPrompt },
      { role: 'user', content: this.formatProblem(instance) },
    ];
    
    let patch = '';
    const maxTurns = 20;
    
    for (let turn = 0; turn < maxTurns; turn++) {
      // Call LLM
      const response = await this.callLLM(messages);
      messages.push({ role: 'assistant', content: response });
      
      // Parse tool calls
      const toolCalls = this.parseToolCalls(response);
      
      if (toolCalls.length === 0) {
        // No tool calls = agent thinks it's done
        patch = this.extractPatch(response);
        break;
      }
      
      // Execute tools (ONLY bash or editor)
      for (const call of toolCalls) {
        if (!['bash', 'editor'].includes(call.type)) {
          throw new Error(`Tool ${call.type} not allowed in minimal harness`);
        }
        
        toolsUsed.push(call.type);
        
        const result = await this.executeTool(call);
        
        // Record trajectory
        this.trajectory.push({
          turn,
          type: 'tool-call',
          tool: call.type,
          input: call,
          output: result,
          timestamp: Date.now(),
        });
        
        // Add result to messages
        messages.push({
          role: 'tool',
          tool_call_id: call.id,
          content: JSON.stringify(result),
        });
      }
    }
    
    return patch;
  }
  
  private async executeTool(call: ToolCall): Promise<any> {
    switch (call.type) {
      case 'bash':
        return await this.container.exec(call.command, {
          timeout: call.timeout || this.config.limits.timeoutSeconds * 1000,
          workdir: call.workdir || this.config.workingDir,
        });
      
      case 'editor':
        return await this.container.fileOp(call);
      
      default:
        throw new Error(`Unknown tool: ${call.type}`);
    }
  }
  
  private formatProblem(instance: BenchmarkInstance): string {
    return `## Repository: ${instance.repo}
## Base Commit: ${instance.baseCommit}

## Problem Statement:
${instance.problemStatement}

${instance.hints ? `## Hints:\n${instance.hints}` : ''}

## Task:
Fix the issue described above. You have access to ONLY two tools:
1. **bash** - Execute shell commands
2. **editor** - Read, write, edit, list, or grep files

Your goal is to produce a patch that makes the tests pass.
Explore the codebase first, then implement the fix.

Output format:
1. Use tools to explore and fix
2. When done, provide the final patch in unified diff format`;
  }
}

// ═══════════════════════════════════════════════
// 4. CONTAINER RUNTIME
// ═══════════════════════════════════════════════

interface ContainerRuntime {
  // Lifecycle
  start(): Promise<void>;
  stop(): Promise<void>;
  snapshot(): Promise<string>;    // For fork/resume
  restore(snapshotId: string): Promise<void>;
  
  // Execution
  exec(command: string, options: ExecOptions): Promise<BashResult>;
  fileOp(op: EditorTool): Promise<EditorResult>;
  
  // State
  getFiles(pattern?: string): Promise<string[]>;
  readFile(path: string): Promise<string>;
  writeFile(path: string, content: string): Promise<void>;
}

// Implementation using Docker/Podman
class DockerContainerRuntime implements ContainerRuntime {
  private containerId: string;
  private image: string;
  
  constructor(image: string = 'ubuntu:22.04') {
    this.image = image;
  }
  
  async start(): Promise<void> {
    // docker run -d --cpus=2 --memory=4g --network=none \
    //   -v ${workspace}:/workspace -w /workspace \
    //   ${image} sleep infinity
    this.containerId = await this.dockerRun();
  }
  
  async exec(command: string, options: ExecOptions): Promise<BashResult> {
    const start = Date.now();
    const result = await this.dockerExec(this.containerId, command, options);
    return {
      ...result,
      durationMs: Date.now() - start,
    };
  }
  
  async fileOp(op: EditorTool): Promise<EditorResult> {
    switch (op.action) {
      case 'read':
        return { success: true, content: await this.readFile(op.path) };
      case 'write':
        await this.writeFile(op.path, op.content || '');
        return { success: true };
      case 'edit':
        // Use sed or similar for in-place edit
        const content = await this.readFile(op.path);
        const newContent = content.replace(op.oldString!, op.newString!);
        await this.writeFile(op.path, newContent);
        return { success: true };
      case 'list':
        const files = await this.getFiles(op.path);
        return { success: true, files };
      case 'grep':
        const matches = await this.grep(op.pattern!, op.path);
        return { success: true, matches };
    }
  }
}

// ═══════════════════════════════════════════════
// 5. TRAJECTORY TRACKING
// ═══════════════════════════════════════════════

interface TrajectoryEvent {
  turn: number;
  type: 'tool-call' | 'llm-response' | 'error' | 'test-run';
  tool?: string;
  input?: any;
  output?: any;
  timestamp: number;
}

interface TestResult {
  allPassed: boolean;
  passed: number;
  total: number;
  details: TestDetail[];
}

interface TestDetail {
  name: string;
  status: 'passed' | 'failed' | 'skipped';
  durationMs: number;
  output?: string;
}

// ═══════════════════════════════════════════════
// 6. SWE-BENCH INTEGRATION
// ═══════════════════════════════════════════════

async function runSWEBenchEvaluation(config: {
  model: string;
  dataset: 'lite' | 'verified' | 'full';
  split: 'test' | 'dev';
  maxInstances?: number;
  parallel?: number;
}): Promise<{
  resolved: number;
  total: number;
  resolveRate: number;
  results: BenchmarkResult[];
}> {
  // Load SWE-bench dataset
  const instances = await loadSWEBenchDataset(config.dataset, config.split);
  const limited = config.maxInstances 
    ? instances.slice(0, config.maxInstances) 
    : instances;
  
  const harness = new MinimalBenchmarkHarness({
    isolation: 'container',
    containerImage: 'swebench/ubuntu:22.04',  // Pre-built with Python, etc.
    workingDir: '/workspace',
    allowedTools: ['bash', 'editor'],
    limits: { cpuCores: 2, memoryMB: 4096, diskMB: 10240, timeoutSeconds: 300, networkAccess: false },
    evaluation: { suite: 'swe-bench', dataset: config.dataset, split: config.split },
    llm: { model: config.model, temperature: 0.0, maxTokens: 8192, systemPrompt: SYSTEM_PROMPT },
  });
  
  // Run in parallel
  const results: BenchmarkResult[] = [];
  const semaphore = new Semaphore(config.parallel || 4);
  
  await Promise.all(limited.map(async (instance) => {
    await semaphore.acquire();
    try {
      const result = await harness.runInstance(instance);
      results.push(result);
    } finally {
      semaphore.release();
    }
  }));
  
  const resolved = results.filter(r => r.status === 'resolved').length;
  
  return {
    resolved,
    total: results.length,
    resolveRate: resolved / results.length,
    results,
  };
}

// System prompt for minimal benchmark
const SYSTEM_PROMPT = `You are an expert software engineer. Your task is to fix bugs in a codebase.

You have access to ONLY two tools:
1. **bash** - Execute shell commands (ls, grep, cat, python, pytest, etc.)
2. **editor** - Read, write, edit, list, or grep files

You do NOT have access to:
- Web search
- Code search across repositories
- LLM-powered tools
- Memory/knowledge bases
- Git operations (except via bash)

Workflow:
1. Explore the codebase to understand the problem
2. Find the relevant files
3. Implement the fix
4. Run tests to verify
5. Output the final patch in unified diff format

Be concise. Use tools efficiently.`;
```

</details>

**Key Innovations**:

| Feature | Traditional Harness | Minimal Benchmark Harness |
|---------|-------------------|---------------------------|
| **Tools** | 10-20+ (search, read, write, execute, LLM, memory, etc.) | **2 only** (bash + editor) |
| **Isolation** | Process-level | **Container-level** |
| **Determinism** | Variable (LLM tools) | **High** (no LLM tools) |
| **Bias** | Tool selection bias | **Minimal** (equal footing) |
| **Reproducibility** | Hard | **Native** (container snapshots) |
| **SWE-bench Score** | Varies | **Baseline for comparison** |

**Why Only 2 Tools?**:
1. **Scientific Control** — Eliminates "tool selection bias" where models with better tool-use appear smarter
2. **Reproducibility** — Container + fixed toolset = deterministic environment
3. **Focus on Reasoning** — Forces model to demonstrate actual code understanding, not tool mastery
4. **Cost Control** — Fewer tool calls = lower token usage, predictable costs
5. **Fair Comparison** — All models evaluated on same minimal interface

**File Reference**: Chi tiết implementation xem [`minimal-benchmark-harness.md`](minimal-benchmark-harness.md)

---

## 11. TypeScript Interfaces cho Evaluation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeScript Interfaces là các "bản vẽ kiểu dữ liệu" cho evaluation — metric, test case, report, configuration — giúp chuẩn hóa hình dạng dữ liệu đánh giá và bắt lỗi sai ngay từ lúc code (compile time).
> **Ẩn dụ/so sánh:** Như phiếu nhập hàng có sẵn các ô: tên, số lượng, đơn giá. Người nhập chỉ điền đúng ô, không thể sáng tạo kiểu dữ liệu khác — công đoạn kiểm đếm sau đó mới chính xác được.
> **Vì sao quan trọng:** Dữ liệu evaluation nhiều loại, dễ lẫn lộn; kiểu tĩnh giúp hệ thống không âm thầm tạo ra dữ liệu sai lệch.

### 11.1 Core Evaluation Types

Khối TypeScript này là **từ điển kiểu dữ liệu của cả hệ thống evaluation**: BenchmarkConfig, EvaluationResult, QualityMetrics, ABTestConfig và nhiều kiểu khác. Đọc để biết mỗi dữ liệu phải có hình dạng ra sao — chẳng hạn TaskResult buộc có status, score, duration, tokensUsed. Dùng như bản hợp đồng giữa các module: ai cũng đúng format, không ai tự bịa cấu trúc riêng.

<details>
<summary><b>11.1 Core Evaluation Types (Click to expand/collapse)</b></summary>

```typescript
// ═══════════════════════════════════════════════════════════════
// EVALUATION TYPES — Production-grade interfaces cho evaluation systems
// ═══════════════════════════════════════════════════════════════

/**
 * Benchmark definition — How to structure an evaluation benchmark
 */
interface BenchmarkConfig {
  name: string;
  description: string;
  version: string;
  tasks: BenchmarkTask[];
  metrics: MetricDefinition[];
  settings: BenchmarkSettings;
}

interface BenchmarkTask {
  id: string;
  name: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  category: string;
  input: TaskInput;
  expectedOutput?: TaskOutput;
  testCases: TestCase[];
  timeout: number;        // ms
  tokenBudget?: number;   // max tokens
}

interface TaskInput {
  prompt: string;
  context?: string;
  files?: FileReference[];
  language?: string;
}

interface TaskOutput {
  code: string;
  explanation?: string;
  filesModified?: string[];
}

interface TestCase {
  id: string;
  name: string;
  input: any;
  expectedOutput: any;
  type: 'unit' | 'integration' | 'e2e' | 'edge_case';
  weight: number;  // 0-1, importance in scoring
}

interface BenchmarkSettings {
  maxRetries: number;
  timeoutPerTask: number;       // ms
  tokenBudgetPerTask: number;
  parallelism: number;
  temperature: number;
  randomSeed?: number;
  modelConfig: ModelConfig;
}

interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'ollama' | 'custom';
  model: string;
  maxTokens: number;
  temperature: number;
  topP?: number;
}

/**
 * Evaluation results
 */
interface EvaluationResult {
  benchmarkName: string;
  model: string;
  timestamp: string;
  summary: EvaluationSummary;
  taskResults: TaskResult[];
  metrics: Record<string, number>;
  cost: CostBreakdown;
}

interface EvaluationSummary {
  totalTasks: number;
  passed: number;
  failed: number;
  errored: number;
  passRate: number;
  avgScore: number;
  avgDuration: number;
  avgTokens: number;
  totalTokens: number;
  totalCost: number;
}

interface TaskResult {
  taskId: string;
  status: 'passed' | 'failed' | 'error' | 'timeout';
  score: number;           // 0-1
  duration: number;        // ms
  tokensUsed: number;
  output?: string;
  error?: string;
  testResults: TestCaseResult[];
}

interface TestCaseResult {
  testCaseId: string;
  passed: boolean;
  actual: any;
  expected: any;
  duration: number;
}

interface CostBreakdown {
  inputTokens: number;
  outputTokens: number;
  inputCost: number;
  outputCost: number;
  totalCost: number;
  costPerTask: number;
  costPerPassingTask: number;
}

/**
 * Quality metrics
 */
interface QualityMetrics {
  correctness: CorrectnessMetrics;
  efficiency: EfficiencyMetrics;
  safety: SafetyMetrics;
  maintainability: MaintainabilityMetrics;
}

interface CorrectnessMetrics {
  passRate: number;
  edgeCaseHandling: number;
  errorHandling: number;
  regressionRate: number;
}

interface EfficiencyMetrics {
  timeComplexity: string;      // e.g., "O(n log n)"
  memoryUsage: number;         // bytes
  tokenEfficiency: number;     // tokens per correct answer
  responseTime: number;        // ms
}

interface SafetyMetrics {
  securityScore: number;       // 0-100
  vulnerabilityCount: number;
  inputValidationScore: number;
  dataLeakage: boolean;
}

interface MaintainabilityMetrics {
  codeComplexity: number;      // cyclomatic complexity
  documentationCoverage: number;  // %
  testCoverage: number;        // %
  duplicationRatio: number;    // 0-1
}

/**
 * Continuous improvement tracking
 */
interface ImprovementTracking {
  version: string;
  timestamp: string;
  previousVersion?: string;
  metrics: Record<string, number>;
  regressions: Regression[];
  improvements: Improvement[];
}

interface Regression {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

interface Improvement {
  metric: string;
  previousValue: number;
  currentValue: number;
  percentChange: number;
  taskCategory?: string;
}

/**
 * A/B Testing
 */
interface ABTestConfig {
  name: string;
  variants: Variant[];
  sampleSize: number;
  significanceLevel: number;  // typically 0.05
  metrics: string[];
}

interface Variant {
  id: string;
  name: string;
  description: string;
  config: ModelConfig;
  promptTemplate?: string;
  weight: number;  // traffic split (0-1)
}

interface ABTestResult {
  config: ABTestConfig;
  results: VariantResult[];
  winner?: string;
  pValue: number;
  significant: boolean;
}

interface VariantResult {
  variantId: string;
  sampleSize: number;
  metrics: Record<string, number>;
  confidenceInterval: [number, number];
}

/**
 * Harness quality evaluation — Evaluating the evaluation itself
 */
interface HarnessQualityMetrics {
  /** How well does the benchmark correlate with human judgment? */
  humanCorrelation: number;  // 0-1, Pearson correlation
  /** Are benchmark scores stable across runs? */
  testRetestReliability: number;  // 0-1
  /** Does the benchmark discriminate between good and bad? */
  discriminativePower: number;  // 0-1
  /** How much does it cost to run? */
  costPerRun: number;
  /** How long does a full evaluation take? */
  durationMinutes: number;
  /** Coverage of task types and difficulties */
  coverageScore: number;  // 0-1
}
```

</details>

---

## 12. Design Principles cho Evaluation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ nguyên tắc cốt lõi khi xây hệ thống evaluation — mỗi phần đảm nhiệm một việc, mở rộng được, đo được, phản hồi nhanh — để hệ thống bền vững lâu dài, không vỡ khi quy mô lớn lên.
> **Ẩn dụ/so sánh:** Như bản thiết kế ngôi nhà: móng vững, phòng nào chức năng đó, muốn đúc thêm tầng vẫn được mà không phải đập đi xây lại. Xây theo cảm hứng thì sớm muộn cũng phải sửa lớn.
> **Vì sao quan trọng:** Hệ thống evaluation thiếu nguyên tắc sẽ nhanh chóng thành mớ code khó bảo trì và cho kết quả không tin cậy.

### 12.1 SOLID cho Evaluation Systems

Sơ đồ này áp dụng 5 nguyên tắc SOLID kinh điển vào hệ thống evaluation: mỗi evaluator chỉ đo một thứ (Single Responsibility), thêm metric mới không cần sửa code cũ (Open/Closed). Đọc như "quy tắc xây nhà cho code": tuân thủ thì hệ thống dễ bảo trì và mở rộng trong nhiều năm.

```
┌──────────────────────────────────────────────────────────────────┐
│          SOLID PRINCIPLES IN EVALUATION SYSTEMS                   │
│                                                                  │
│  S — SINGLE RESPONSIBILITY                                       │
│  Each evaluator measures ONE thing                               │
│  ✅ CorrectnessEvaluator → only correctness                     │
│  ✅ PerformanceEvaluator → only performance                     │
│  ❌ "EverythingEvaluator" → too broad, unmaintainable           │
│                                                                  │
│  O — OPEN/CLOSED                                                 │
│  Open for new metrics, closed for modification                  │
│  ✅ Plugin architecture (add new metric without changing core)  │
│  ❌ Hardcoded metric list (requires code change to add metrics) │
│                                                                  │
│  L — LISKOV SUBSTITUTION                                         │
│  Any evaluator should work in any benchmark                     │
│  ✅ All evaluators implement Evaluator interface                │
│  ❌ Different evaluator types with incompatible APIs            │
│                                                                  │
│  I — INTERFACE SEGREGATION                                       │
│  Small, focused evaluation interfaces                           │
│  ✅ Separate: MetricCollector, ResultAggregator, Reporter       │
│  ❌ One giant EvaluationInterface with 30 methods               │
│                                                                  │
│  D — DEPENDENCY INVERSION                                        │
│  Depend on abstractions, not implementations                    │
│  ✅ Evaluator depends on IModelProvider, not OpenAI directly    │
│  ❌ Evaluator directly calls openai.completions()              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 12.2 Evaluation Design Principles

Đây là **10 điều răn** khi thiết kế evaluation, từ "đo thứ quan trọng, không đo thứ dễ đo" đến "đánh giá chính bộ đánh giá". Đọc nhanh như đọc hiến chương: mỗi điều là một cột mốc giúp hệ thống của bạn không đi lệch đường.

```
┌──────────────────────────────────────────────────────────────────┐
│         EVALUATION DESIGN PRINCIPLES (10 Commandments)            │
│                                                                  │
│  1. THOU SHALL EVALUATE WHAT MATTERS                            │
│     → Don't measure easy things, measure important things       │
│     → Correctness > Token count > Response time                 │
│                                                                  │
│  2. THOU SHALL USE MULTIPLE METRICS                             │
│     → Single metric is always misleading                        │
│     → Balance: quality, speed, cost, safety                     │
│                                                                  │
│  3. THOU SHALL BENCHMARK REALISTICALLY                          │
│     → Use real-world tasks, not synthetic examples              │
│     → Include easy, medium, and hard tasks                      │
│                                                                  │
│  4. THOU SHALL CALIBRATE WITH HUMANS                            │
│     → Auto-eval must align with human judgment                  │
│     → Regular calibration checks (weekly/monthly)               │
│                                                                  │
│  5. THOU SHALL TRACK REGRESSIONS                                │
│     → Every evaluation run should compare to previous           │
│     → Alert on metric drops > threshold                         │
│                                                                  │
│  6. THOU SHALL MAKE IT REPRODUCIBLE                             │
│     → Fixed random seeds for deterministic results              │
│     → Version-controlled benchmark data                         │
│                                                                  │
│  7. THOU SHALL TRACK COST                                       │
│     → Token cost per quality point                              │
│     → ROI of model upgrades                                     │
│                                                                  │
│  8. THOU SHALL ITERATE                                          │
│     → Update benchmarks as codebase evolves                     │
│     → Add new test cases from production failures               │
│                                                                  │
│  9. THOU SHALL SHARE RESULTS                                    │
│     → Team visibility into evaluation outcomes                  │
│     → Build trust through transparency                          │
│                                                                  │
│  10. THOU SHALL EVALUATE THE EVALUATOR                          │
│      → Does your benchmark actually measure quality?            │
│      → Cross-validate with multiple evaluation approaches       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 13. Testing Evaluation Harness

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing Evaluation Harness là việc "test lại chính bộ test" — kiểm tra metric tính đúng không, benchmark lặp lại có ổn định không, cost tracking có chính xác không — trước khi dùng nó để chấm agent.
> **Ẩn dụ/so sánh:** Như kiểm định cái cân trước khi cân hàng: lái buôn phải chắc chắn cái cân đúng, nếu cân sai thì mọi phiếu hàng sau đó đều sai theo.
> **Vì sao quan trọng:** Cái cân sai còn nguy hiểm hơn không có cân — nó khiến bạn tin vào những con số dối trá.

### 13.1 Evaluation Test Harness

Đây là bộ test **kiểm tra chính hệ thống đánh giá**: metric có tính đúng không, benchmark có lặp lại giống nhau không, cost tracking có chính xác không, regression có được phát hiện không. Cách dùng: viết các trường hợp kiểm thử như `test_metric_accuracy` bên dưới, đăng ký vào harness rồi chạy `run_all()` để nhận báo cáo pass/fail. Nếu phần này không pass thì mọi con số bạn đo đều chưa đáng tin.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import time
import json
import statistics
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from enum import Enum


class EvalHarnessTestType(Enum):
    """Các loại test cho evaluation harness"""
    METRIC_ACCURACY = "metric_accuracy"       # Metric outputs correct values
    BENCHMARK_VALIDITY = "benchmark_validity"  # Benchmark has expected structure
    REPRODUCIBILITY = "reproducibility"        # Same input → same output
    COST_TRACKING = "cost_tracking"           # Costs are accurate
    REGRESSION_DETECTION = "regression_detection"  # Detects quality drops
    HUMAN_CALIBRATION = "human_calibration"    # Aligns with human judgment
    EDGE_CASE_HANDLING = "edge_case_handling"  # Handles edge cases


@dataclass
class EvalHarnessTest:
    """Một test case cho evaluation harness"""
    name: str
    test_type: EvalHarnessTestType
    description: str
    handler: Callable
    setup: Optional[Callable] = None
    teardown: Optional[Callable] = None
    timeout: int = 120
    tags: List[str] = field(default_factory=list)
    expected_result: Optional[Any] = None


class EvaluationTestHarness:
    """
    Harness để test evaluation systems itself.
    
    Features:
    - Metric accuracy verification
    - Benchmark validity checks
    - Reproducibility testing
    - Cost tracking validation
    - Regression detection testing
    - Human calibration checks
    """
    
    def __init__(self):
        self.tests: List[EvalHarnessTest] = []
        self.results: List[Dict] = []
    
    def register(self, test: EvalHarnessTest):
        """Register một eval harness test"""
        self.tests.append(test)
    
    def run_all(self) -> Dict:
        """Chạy toàn bộ eval harness tests"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            result = self._run_single(test)
            self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def run_by_type(self, test_type: EvalHarnessTestType) -> Dict:
        """Chạy tests theo type"""
        self.results = []
        start_time = time.time()
        
        for test in self.tests:
            if test.test_type == test_type:
                result = self._run_single(test)
                self.results.append(result)
        
        total_time = time.time() - start_time
        return self._generate_report(total_time)
    
    def _run_single(self, test: EvalHarnessTest) -> Dict:
        """Chạy một test case"""
        if test.setup:
            try:
                test.setup()
            except Exception as e:
                return {
                    "name": test.name,
                    "type": test.test_type.value,
                    "status": "setup_error",
                    "error": str(e),
                    "duration": 0,
                }
        
        start = time.time()
        try:
            result = test.handler()
            duration = time.time() - start
            
            passed = True
            if test.expected_result is not None:
                passed = result == test.expected_result
            
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "passed" if passed else "failed",
                "duration": duration,
                "output": result,
                "expected": test.expected_result,
                "tags": test.tags,
            }
        except AssertionError as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "failed",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        except Exception as e:
            return {
                "name": test.name,
                "type": test.test_type.value,
                "status": "error",
                "duration": time.time() - start,
                "error": str(e),
                "tags": test.tags,
            }
        finally:
            if test.teardown:
                try:
                    test.teardown()
                except Exception:
                    pass
    
    def _generate_report(self, total_time: float) -> Dict:
        """Tạo test report"""
        passed = sum(1 for r in self.results if r["status"] == "passed")
        failed = sum(1 for r in self.results if r["status"] == "failed")
        errors = sum(1 for r in self.results if r["status"] == "error")
        
        return {
            "summary": {
                "total": len(self.results),
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "pass_rate": f"{(passed / len(self.results) * 100):.1f}%",
                "total_duration": f"{total_time:.2f}s",
            },
            "by_type": self._group_by_type(),
            "results": self.results,
            "gate_passed": failed == 0 and errors == 0,
        }
    
    def _group_by_type(self) -> Dict:
        """Group results by test type"""
        groups: Dict[str, List] = {}
        for result in self.results:
            t = result["type"]
            if t not in groups:
                groups[t] = []
            groups[t].append(result)
        
        return {
            t: {
                "total": len(results),
                "passed": sum(1 for r in results if r["status"] == "passed"),
            }
            for t, results in groups.items()
        }


# ═══════════════════════════════════════════════════════════════
# Usage Example
# ═══════════════════════════════════════════════════════════════

def test_metric_accuracy():
    """Test that pass@k metric computes correctly"""
    evaluator = PassAtKEvaluator()
    # 3 correct out of 5 → pass@1 should be 0.6
    result = evaluator.compute(k=1, total=5, correct=3)
    assert abs(result - 0.6) < 0.01, f"Expected 0.6, got {result}"

def test_benchmark_reproducibility():
    """Test that running same benchmark twice gives same results"""
    bench = SimpleBenchmark(seed=42)
    result1 = bench.run(tasks=["task1", "task2"])
    result2 = bench.run(tasks=["task1", "task2"])
    assert result1 == result2, "Benchmark results not reproducible"

def test_cost_tracking():
    """Test that cost tracking is accurate"""
    tracker = CostTracker(model="gpt-4o")
    tracker.record(input_tokens=1000, output_tokens=500)
    assert tracker.total_cost > 0
    assert tracker.total_cost < 0.01  # Should be very small for this usage


# Register tests
harness = EvaluationTestHarness()

harness.register(EvalHarnessTest(
    name="Pass@K Accuracy",
    test_type=EvalHarnessTestType.METRIC_ACCURACY,
    description="Verify pass@k metric computation",
    handler=test_metric_accuracy,
    tags=["metric", "correctness"],
))

harness.register(EvalHarnessTest(
    name="Benchmark Reproducibility",
    test_type=EvalHarnessTestType.REPRODUCIBILITY,
    description="Verify benchmark produces consistent results",
    handler=test_benchmark_reproducibility,
    tags=["benchmark", "reliability"],
))

harness.register(EvalHarnessTest(
    name="Cost Tracking Accuracy",
    test_type=EvalHarnessTestType.COST_TRACKING,
    description="Verify cost tracking is accurate",
    handler=test_cost_tracking,
    tags=["cost", "tracking"],
))

# Run
# report = harness.run_all()
# print(json.dumps(report, indent=2))
```

</details>

---

## 14. Future Trends trong Evaluation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Future Trends là những hướng phát triển đang định hình cách đánh giá AI trong 2024-2026 — tự động hóa, đánh giá real-time, tối ưu chi phí, benchmark chuyên ngành — giúp bạn chuẩn bị hệ thống trước, không bị tụt lại.
> **Ẩn dụ/so sánh:** Như người trồng trọt nghe dự báo thời tiết: biết sắp hạn, sắp mưa bão để chủ động canh tác thay vì bị động chờ trời đổi.
> **Vì sao quan trọng:** Evaluation đang dịch chuyển nhanh; ai xây hệ thống theo lối cũ sẽ phải đập đi làm lại rất tốn kém.

### 14.1 AI Evaluation Trends (2024-2026)

Bảng này tóm tắt **6 xu hướng lớn** định hình cách đánh giá AI từ 2024 đến 2026: tự động hóa khâu đánh giá (meta-evaluation), đánh giá real-time, tối ưu chi phí, kết hợp con người với AI, benchmark chuyên ngành, và biến evaluation thành code trong CI/CD. Mỗi mục nhỏ là một gợi ý bạn có thể thử đưa vào hệ thống của mình.

```
┌──────────────────────────────────────────────────────────────────┐
│              FUTURE EVALUATION TRENDS                             │
│                                                                  │
│  TREND 1: AUTOMATED HARNESS EVALUATION                          │
│  ├── Meta-evaluation: AI evaluates the evaluator                │
│  ├── Self-improving benchmarks that evolve with models          │
│  ├── Automatic detection of benchmark contamination             │
│  └── Quality signals from production usage data                 │
│                                                                  │
│  TREND 2: REAL-TIME EVALUATION                                   │
│  ├── Live evaluation during coding (not just post-hoc)          │
│  ├── Instant feedback loops on code quality                     │
│  ├── Predictive evaluation (estimate quality before running)    │
│  └── Continuous evaluation dashboards                           │
│                                                                  │
│  TREND 3: COST-AWARE EVALUATION                                 │
│  ├── Quality-per-dollar as primary metric                       │
│  ├── Model routing based on task difficulty                     │
│  ├── Token budget optimization                                  │
│  └── ROI measurement for AI tooling investments                │
│                                                                  │
│  TREND 4: HUMAN-AI CALIBRATED EVALUATION                        │
│  ├── LLM-as-judge calibrated against human experts              │
│  ├── Multi-rater consensus systems                              │
│  ├── Bias detection in automated evaluation                     │
│  └── Fair comparison across model families                      │
│                                                                  │
│  TREND 5: DOMAIN-SPECIFIC BENCHMARKS                            │
│  ├── Security-focused evaluation (OWASP patterns)               │
│  ├── Performance-focused evaluation (latency, memory)           │
│  ├── Accessibility-focused evaluation (WCAG compliance)         │
│  └── Industry-specific benchmarks (healthcare, finance)         │
│                                                                  │
│  TREND 6: EVALUATION-AS-CODE                                     │
│  ├── Version-controlled evaluation suites                       │
│  ├── CI/CD integrated evaluation pipelines                      │
│  ├── Evaluation results as PR comments                          │
│  └── Automated evaluation gates for model upgrades              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tài Liệu Tham Khảo

### Papers & Research
- [HumanEval Benchmark](https://github.com/openai/human-eval) — OpenAI code generation benchmark
- [SWE-bench](https://www.swebench.com/) — Princeton NLP real-world bug fix benchmark
- [CodeBLEU](https://github.com/microsoft/CodeXGLUE) — Microsoft code evaluation metric
- [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) — Codex paper

### Frameworks & Tools
- [PromptFoo](https://www.promptfoo.dev) — Prompt testing & evaluation
- [DeepEval](https://docs.confident-ai.com) — LLM evaluation framework
- [RAGAS](https://docs.ragas.io) — RAG evaluation
- [LangSmith](https://smith.langchain.com) — Tracing & evaluation
- [Weights & Biases](https://wandb.ai) — Experiment tracking

### Benchmarks
- [SWE-bench Leaderboard](https://www.swebench.com/)
- [LiveCodeBench](https://livecodebench.github.io/)
- [BigCodeBench](https://bigcode-benchmark.github.io/)
- [Aider LLM Leaderboard](https://aider.chat/docs/leaderboards/)

### Case Study References
- [SWE-agent](https://github.com/princeton-nlp/SWE-agent)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [Aider](https://aider.chat)
- [Anthropic Claude Code](https://docs.anthropic.com/en/docs/claude-code)

---

**Ngày cập nhật:** 19/07/2026  
**Tác giả:** AI Knowledge Repository
