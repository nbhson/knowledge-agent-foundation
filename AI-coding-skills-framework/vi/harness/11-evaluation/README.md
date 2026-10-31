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

Bạn mới xây xong một cây cầu. Nhìn bằng mắt thì *"trông ổn đấy"*, nhưng nếu chưa **cân tải trọng, kiểm chất liệu, cho xe tải nặng chạy thử** thì làm sao dám chắc cầu đứng được 10 năm chứ không phải sập sau 1 tháng?

**Code do AI sinh ra cũng thế.** Viết xong mà không evaluate thì chẳng khác nào **cho xe chạy qua cầu mà chưa kiểm định**.

Khi nhờ AI viết code, câu hỏi đáng giá không phải *"chạy được không?"* mà là cả chùm câu hỏi: *"có đúng không? có an toàn không? sau này có dễ sửa không? có hơn người viết tay không?"* — và bạn cần một **hệ thống evaluation tử tế** để trả lời từng câu một.

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

Nói một cách gần gũi: **Evaluation** trong AI coding là việc **chấm điểm xem AI agent làm ăn ra sao** khi nhận task coding. Chấm bằng cách cho làm bài thi chuẩn (benchmarking), gom điểm số (metrics collection), rồi lấy kết quả đó để cải tiến tiếp (continuous improvement).

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

Bảng dưới đây gom lại **9 chiều đánh giá** bạn nên ngó qua khi chấm AI agent — từ làm có đúng không (correctness) đến có đáng đồng tiền không (cost-effectiveness). Bạn cứ đọc như đọc phiếu khám sức khỏe tổng quát: mỗi dòng là một câu hỏi về "sức khỏe" của agent nhà mình.

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

Đoạn code này dựng sẵn **rubric chấm điểm** — tức là đáp án cho câu hỏi "thế nào là 5 điểm, thế nào là 3 điểm, thế nào là 1 điểm" ở từng chiều đánh giá. Giống như chấm bài thi có barem rõ ràng thì ai chấm cũng ra kết quả na ná nhau. Bạn chạy thử sẽ thấy từng điểm thành phần được nhân trọng số (weighted) rồi gom lại thành tổng điểm 0-100.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-evaluation-rubric.py`](examples/01-1-2-evaluation-rubric.py)

</details>

### 1.3 Weight Configuration — Tùy Theo Use Case

Code ở đây kể một chuyện rất đời: cùng một bộ tiêu chí, nhưng **tùy mục tiêu mà chấm nặng nhẹ khác nhau** — như thi đại học thì lệch môn tự nhiên, học nghề thì tay nghề mới là vua. Chỗ nào cần an toàn thì nâng `safety` lên, chỗ nào cần ra hàng nhanh thì nâng `completeness` lên. Bạn cứ chỉnh `WEIGHT_CONFIGS` cho khớp với use case nhà mình là được.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-1-3-weight-configuration-tuy-theo-use-case.py`](examples/02-1-3-weight-configuration-tuy-theo-use-case.py)

</details>

---

## 2. Quality Metrics

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Quality Metrics là các thước đo định lượng dùng để chấm chất lượng output của AI agent — accuracy, completeness, adherence, style — biến đánh giá cảm tính thành con số khách quan, so sánh được.
> **Ẩn dụ/so sánh:** Như thang điểm chấm món ăn: hương vị (correctness), trình bày (style), đủ khẩu phần (completeness). Điểm rõ ràng giúp người nấu biết món nào cần cải thiện.
> **Vì sao quan trọng:** Không có con số cụ thể thì "trông có vẻ ổn" sẽ thay thế đánh giá thật, và bạn không thể theo dõi tiến bộ theo thời gian.

### 2.1 Code Quality Metrics

Lớp `CodeQualityAnalyzer` đóng vai "cô giáo chấm bài tự động": nhận code đầu vào, soi độ phức tạp (cyclomatic complexity), khả năng bảo trì (maintainability index), cách đặt tên, xem có docstring không... rồi gom lại thành một điểm tổng 0-100 kèm bảng điểm chi tiết, thay vì chỉ phán một câu chung chung "code này ổn".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-1-code-quality-metrics.py`](examples/03-2-1-code-quality-metrics.py)

</details>

### 2.2 AI Agent Quality Metrics

Phần này chấm **cả quá trình làm việc của AI agent**, chứ không chỉ nhìn kết quả cuối: có đúng ngay lần đầu không, phải retry mấy lần, tốn bao nhiêu token, có làm vỡ chức năng cũ không. Agent giỏi cũng như nhân viên thạo việc — làm đúng sớm, ít phải hỏi lại, ít tốn tài nguyên.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-2-2-ai-agent-quality-metrics.py`](examples/04-2-2-ai-agent-quality-metrics.py)

</details>

### 2.3 Metrics Dashboard

Bảng điều khiển mẫu gom mọi metrics vào một màn hình duy nhất: mỗi chiều một thanh phần trăm, cuối cùng chốt bằng COMPOSITE SCORE. Cách đọc thì ai cũng hiểu — thanh dài là đang khỏe, thanh ngắn là chỗ cần bồi bổ. Cả đội chỉ cần liếc qua là biết agent đang yếu ở đâu.

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

`BenchmarkSuite` là "sân thi đấu" của agent: bạn thêm task vào, cho agent chạy từng task, rồi thống kê success rate, token đã dùng, thời gian chạy — thậm chí so sánh hai lượt chạy với nhau. Cứ hình dung như sân bóng có trọng tài bấm giờ và ghi biên bản: pha nào cũng được đo, không còn chuyện "tôi cảm giác mình đá tốt".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-3-1-benchmark-framework.py`](examples/05-3-1-benchmark-framework.py)

</details>

### 3.2 Standard Benchmark Tasks

Danh sách này là **bộ đề mẫu** xếp từ dễ đến khó: viết hello world, đảo chuỗi, sửa lỗi off-by-one, refactor cả class. Mỗi task đều có validator để chấm tự động. Bạn dùng như bộ đề ôn thi: cho làm câu dễ trước để xem agent có "vào phòng thi" được không, rồi nâng dần độ khó để đo thực lực.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-3-2-standard-benchmark-tasks.py`](examples/06-3-2-standard-benchmark-tasks.py)

</details>

### 3.3 Benchmark Comparison Table

Bảng này so điểm các model trên những benchmark phổ biến năm 2026. Bạn đọc theo cột sẽ thấy chuyện rất thường: một model đạt 92% trên HumanEval mà chỉ 53% trên SWE-bench — vì mỗi benchmark đo một kiểu năng lực khác nhau, viết một hàm lẻ khác hẳn sửa bug trong repo thật. Nhớ để ý dòng chú thích cuối: điểm số còn chạy theo phiên bản model và cách bạn viết prompt.

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

`EvaluationPipeline` biến việc đánh giá thành **cỗ máy chạy tự động**: bạn gắn vào pipeline các check như lint, test, security, cho chạy trên code rồi gom điểm theo trọng số. Mỗi check như một anh kiểm hàng đứng ở một công đoạn, mỗi người chấm một tiêu chí; con số cuối là kết luận chung của cả đội.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-4-1-auto-evaluation-pipeline.py`](examples/07-4-1-auto-evaluation-pipeline.py)

</details>

### 4.2 LLM-as-Judge Evaluation

Đây là cách **nhờ một LLM mạnh (GPT-4, Claude) đóng vai "giám khảo"** chấm code của LLM khác. Giống như nhờ anh senior nhiều kinh nghiệm đọc bài, cho điểm kèm lời nhận xét — mấy thứ trừu tượng như readability hay design thì người chấm kiểu này làm tốt hơn máy chấm tự động. Nhưng nhớ là giám khảo cũng có lúc thiên vị hay hallucinate, nên phải chấm kèm với test tự động chứ đừng tin tuyệt đối.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-4-2-llm-as-judge-evaluation.py`](examples/08-4-2-llm-as-judge-evaluation.py)

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

Regression testing trả lời một câu hỏi rất thực tế: **đổi prompt hay harness xong, agent có quên bài cũ không?** Cách làm là lưu lại "bài giải mẫu" (golden answer) cho từng task, mỗi lần đổi là cho chạy lại rồi so với baseline; điểm tụt quá 10% là réo REGRESSION. Giống ông thầy giữ lại bài kiểm tra cũ của học trò, thỉnh thoảng cho làm lại để chắc không bị "học trước quên sau".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-4-3-regression-testing-framework.py`](examples/09-4-3-regression-testing-framework.py)

</details>

---

## 5. Continuous Improvement

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Continuous Improvement là vòng lặp "đo → phân tích → chỉnh sửa → kiểm tra lại", dùng kết quả đánh giá để cải thiện prompt, tooling và kiến thức cho agent.
> **Ẩn dụ/so sánh:** Như việc tập gym: đo cân nặng (measure), xem vì sao chưa giảm (analyze), đổi bài tập (improve), rồi cân lại để biết có hiệu quả không (verify) — lặp đi lặp lại mỗi tuần.
> **Vì sao quan trọng:** AI agent chỉ tốt hơn qua từng bước chỉnh sửa có đo lường; thiếu vòng lặp này nó sẽ đứng yên mãi ở mức hiện tại.

### 5.1 Improvement Loop

Sơ đồ trên là **vòng lặp cải tiến 5 bước**: Đo (measure) → Phân tích (analyze) → Chốt vấn đề (identify) → Sửa (improve) → Kiểm tra lại (verify), rồi quay lại từ đầu. Bạn cứ coi như lịch bảo dưỡng định kỳ cho agent: mỗi tuần hay mỗi sprint lại chạy một vòng.

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

> 📄 **Code ví dụ:** [`examples/10-5-1-improvement-loop.py`](examples/10-5-1-improvement-loop.py)

</details>

### 5.2 A/B Testing Framework

`ABTestFramework` giúp so **hai phiên bản** — ví dụ prompt A đấu với prompt B — trên cùng một bộ benchmark để biết bản nào hơn. Giống như pha hai công thức cà phê cho hai nhóm khách uống thử rồi đếm xem ly nào được khen nhiều hơn; quyết định bằng số liệu chứ không bằng cảm tính.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/11-5-2-a-b-testing-framework.py`](examples/11-5-2-a-b-testing-framework.py)

</details>

---

## 6. Reporting & Dashboards

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Reporting & Dashboards là cách trình bày trực quan kết quả đánh giá — metrics theo thời gian, so sánh phiên bản, phát hiện suy giảm — để cả đội "nhìn một cái là hiểu" sức khỏe của agent.
> **Ẩn dụ/so sánh:** Như đồng hồ tốc độ trên xe: bạn không cần bấm giờ từng mét, chỉ cần nhìn kim là biết đang chạy nhanh hay chậm, cần đạp ga hay rà phanh.
> **Vì sao quan trọng:** Kết quả đánh giá nằm im trong file log chẳng giúp ai ra quyết định; phải hiển thị rõ thì đội mới phản ứng kịp khi chất lượng tụt dốc.

### 6.1 Evaluation Report Generator

`EvaluationReporter` lo việc "in biên bản" sau khi chấm: từ cùng một kết quả, nó xuất ra Markdown để dán lên PR, JSON cho máy đọc, và dữ liệu cho dashboard. Giống máy in báo cáo cuối ca của nhà máy — chỉ cần nạp số liệu vào là có ngay bảng tổng kết để gửi cả đội.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/12-6-1-evaluation-report-generator.py`](examples/12-6-1-evaluation-report-generator.py)

</details>

---

## 7. Case Studies

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies là những ví dụ đánh giá ngoài đời thật — SWE-bench, HumanEval, pipeline sản xuất — cho thấy cách người ta thiết lập metrics, chấm agent cụ thể và rút ra bài học cải thiện.
> **Ẩn dụ/so sánh:** Như đọc báo cáo sau trận bóng: xem đội này phối hợp ra sao, ghi bàn kiểu gì, thua ở khâu nào — để rút kinh nghiệm đưa vào trận sau thay vì chỉ dừng ở tỉ số.
> **Vì sao quan trọng:** Lý thuyết khô khan sẽ dễ hiểu hơn rất nhiều khi nhìn nó hoạt động trong bối cảnh thật.

### 7.1 SWE-bench — Benchmarking AI Code Agents

**Bối cảnh**: SWE-bench là benchmark chuẩn để xem AI agent sửa bug thật giỏi tới đâu trên các repo GitHub ngoài đời. Nói nôm na, người ta lấy bug thật từ dự án mã nguồn mở, đưa cho agent sửa, rồi chạy lại đúng bộ test của dự án đó để xem issue có được "đóng" không — như thi bằng đề thật chứ không phải đề tự ra.

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

Bảng này ghi lại hành trình tiến bộ của các model trên HumanEval — benchmark kinh điển của OpenAI toàn bài viết hàm Python lẻ — từ 2023 đến 2026, cột Improvement cho biết mỗi model tiến thêm bao nhiêu phần trăm. Điểm đáng để ý: các model lớn đã chạm trần quanh 90%, nên giới nghiên cứu phải tìm benchmark khó hơn như SWE-bench — bạn nhớ đọc kỹ dòng ⚠️ cuối bảng.

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

Đây là chuyện **một đội 20 dev xài pipeline đánh giá mỗi ngày trong production**: tối đến là chạy benchmark, kiểm regression, xuất report, chất lượng tụt là báo động ngay. Bạn đọc như xem "bản mẫu" để bê về đội mình — điểm hay là người ta giám sát liên tục chứ không chấm một lần rồi thôi.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/13-7-3-real-world-evaluation-pipeline-production-case.py`](examples/13-7-3-real-world-evaluation-pipeline-production-case.py)

</details>

---

## 8. Evaluation Tooling

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Evaluation Tooling là bộ công cụ hỗ trợ quy trình đánh giá — benchmark suites, framework chấm điểm, code quality tools, security scanners — giúp đánh giá tự động, lặp lại và đáng tin cậy.
> **Ẩn dụ/so sánh:** Như bộ dụng cụ sửa xe đầy đủ: mỗi loại chìa khóa, máy đo, máy chẩn đoán phục vụ một việc. Không có dụng cụ thì thợ phải mò bằng tay, vừa lâu vừa dễ sai.
> **Vì sao quan trọng:** Xây evaluation từ tay trắng rất tốn kém; tận dụng công cụ có sẵn để dồn sức vào việc chính là đo lường và cải thiện.

### 8.1 Popular Evaluation Tools

Sơ đồ này chia "chợ" công cụ evaluation thành 4 gian hàng: benchmark suites (gian bán đề thi), evaluation frameworks (gian bán khung chấm điểm), code quality tools (gian quét chất lượng code) và security scanners (gian quét lỗ hổng). Bạn không cần ôm hết cả chợ — gian nào hợp với giai đoạn của mình thì lấy.

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

Cấu hình YAML này giúp bạn chạy PromptFoo — công cụ test prompt phổ biến — trên agent coding: khai báo provider (model nào), prompt nào, và các assertion (điều kiện output phải thỏa). Bạn hình dung như viết "hợp đồng nghiệm thu": máy tự chấm xem model có đạt từng điều khoản không, kiểu `contains` hay `llm-rubric`.

<details>
<summary><b>8.2 PromptFoo Configuration Example (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/14-8-2-promptfoo-configuration-example.yaml`](examples/14-8-2-promptfoo-configuration-example.yaml)

</details>

---

## 9. Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là tập hợp các nguyên tắc đánh giá đã được chứng minh hiệu quả — test case chất lượng, tránh data leakage, cập nhật thường xuyên — giúp đo lường agent chính xác và đáng tin.
> **Ẩn dụ/so sánh:** Như quy tắc an toàn trong bếp chuyên nghiệp: tay rửa sạch, dao để riêng, kiểm tra hạn dùng — áp dụng đều đặn để tránh tai nạn và món ăn luôn đạt chuẩn.
> **Vì sao quan trọng:** Hầu hết sai lầm trong evaluation đều có người gặp trước; học theo kinh nghiệm để không tự đạp vào vết xe đổ.

### 9.1 DO và DON'T

Đây là tờ "nội quy" gọn nhất để chấm không trượt: **10 điều NÊN làm** (như automate mọi thứ, lưu baseline để so) và **8 điều KHÔNG nên làm** (như chỉ nhìn một metric duy nhất). Bạn cứ dùng như checklist mỗi khi dựng hệ thống evaluation.

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

Kim tự tháp này nói cho bạn biết **tầng nào chạy khi nào và tốn kém ra sao**: tầng dưới rẻ nên chạy liên tục (static analysis chạy theo từng phím gõ), tầng trên đắt nên chạy thưa (E2E mỗi tuần một lần). Ý tưởng cũng như lọc nước nhiều lớp: lớp rẻ lọc phần thô với số lượng lớn, lớp đắt chỉ xử lý phần tinh còn lại.

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

Case study này mổ xẻ SWE-bench — benchmark sửa bug thật từ 2294 GitHub issues. Nhìn bảng leaderboard bạn sẽ thấy tỷ lệ resolve, token và chi phí của từng hệ thống; điểm giật mình là **chất lượng ngang nhau mà chi phí chênh tới 10 lần**. Phần EVALUATION METHODOLOGY mô tả quy trình chấm 5 bước mà bạn có thể bê về xài cho benchmark nhà mình.

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

Case study này là bảng xếp hạng của dự án Aider, chấm LLM qua cách sửa file đúng edit-format và chất lượng diff có sạch không. Điểm đáng tiền nằm ở **phần COST-EFFECTIVENESS**: DeepSeek V3 đạt 92% chất lượng của GPT-4o mà chỉ tốn 11% chi phí — nghĩa là với task thường ngày, model rẻ có khi lại là lựa chọn khôn ngoan nhất.

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

LiveCodeBench ra đời để trị bệnh của benchmark tĩnh: model có thể đã "học tủ" đề cũ, hoặc bộ đề để lâu thành lỗi thời. Cách trị là **mỗi tuần nạp thêm đề mới từ các sân thi đấu lập trình**, kèm cơ chế phát hiện contamination. Sơ đồ Scrape → Dedupe → Validate → Run LLM chính là dây chuyền "ra đề liên tục" của họ.

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

Anthropic chấm theo **4 tầng**, từ máy (automated benchmarks) tới người (human evaluation) rồi tới đời thật (real user feedback, A/B testing) — vì chẳng tầng nào kể hết câu chuyện một mình. Chỉ số họ soi nhiều nhất là **Acceptance Rate** (dev gật đầu với bao nhiêu gợi ý của AI). Đây là kiểu "nghe nhiều tai" rất đáng học theo, thay vì bám vào một con số duy nhất.

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

> 📄 **Code ví dụ:** [`examples/15-10-5-deepseek-harness-minimal-benchmark-harness-for.ts`](examples/15-10-5-deepseek-harness-minimal-benchmark-harness-for.ts)

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

Khối TypeScript này là **cuốn từ điển kiểu dữ liệu của cả hệ evaluation**: BenchmarkConfig, EvaluationResult, QualityMetrics, ABTestConfig và nhiều kiểu nữa. Bạn đọc để biết mỗi cục dữ liệu phải có hình thù ra sao — ví dụ TaskResult thì buộc phải có status, score, duration, tokensUsed. Cứ coi như hợp đồng giữa các module: ai cũng theo đúng form, không ai tự chế cấu trúc riêng.

<details>
<summary><b>11.1 Core Evaluation Types (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/16-11-1-core-evaluation-types.ts`](examples/16-11-1-core-evaluation-types.ts)

</details>

---

## 12. Design Principles cho Evaluation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ nguyên tắc cốt lõi khi xây hệ thống evaluation — mỗi phần đảm nhiệm một việc, mở rộng được, đo được, phản hồi nhanh — để hệ thống bền vững lâu dài, không vỡ khi quy mô lớn lên.
> **Ẩn dụ/so sánh:** Như bản thiết kế ngôi nhà: móng vững, phòng nào chức năng đó, muốn đúc thêm tầng vẫn được mà không phải đập đi xây lại. Xây theo cảm hứng thì sớm muộn cũng phải sửa lớn.
> **Vì sao quan trọng:** Hệ thống evaluation thiếu nguyên tắc sẽ nhanh chóng thành mớ code khó bảo trì và cho kết quả không tin cậy.

### 12.1 SOLID cho Evaluation Systems

Sơ đồ này bê 5 nguyên tắc SOLID kinh điển vào hệ evaluation: mỗi evaluator chỉ đo một thứ (Single Responsibility), thêm metric mới thì cắm thêm chứ khỏi mổ code cũ (Open/Closed). Bạn đọc như đọc quy tắc xây nhà: làm đúng thì hệ thống ở bền nhiều năm, muốn cơi nới cũng dễ.

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

Đây là **10 điều răn** khi thiết kế evaluation, từ "đo cái quan trọng chứ đừng đo cái dễ đo" đến "nhớ đánh giá cả chính bộ đánh giá". Bạn đọc lướt như đọc hiến chương: mỗi điều là một cọc tiêu để hệ thống khỏi đi chệch đường.

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

Đây là bộ test **đem chính hệ thống đánh giá ra kiểm định**: metric có tính đúng không, benchmark chạy lại có ra kết quả cũ không, cost tracking có chuẩn không, chất lượng tụt có bị bắt không. Cách dùng: viết các case như `test_metric_accuracy` bên dưới, đăng ký vào harness rồi gọi `run_all()` lấy báo cáo pass/fail. Chỗ này mà chưa pass thì mọi con số bạn đo đều chưa đáng tin.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/17-13-1-evaluation-test-harness.py`](examples/17-13-1-evaluation-test-harness.py)

</details>

---

## 14. Future Trends trong Evaluation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Future Trends là những hướng phát triển đang định hình cách đánh giá AI trong 2024-2026 — tự động hóa, đánh giá real-time, tối ưu chi phí, benchmark chuyên ngành — giúp bạn chuẩn bị hệ thống trước, không bị tụt lại.
> **Ẩn dụ/so sánh:** Như người trồng trọt nghe dự báo thời tiết: biết sắp hạn, sắp mưa bão để chủ động canh tác thay vì bị động chờ trời đổi.
> **Vì sao quan trọng:** Evaluation đang dịch chuyển nhanh; ai xây hệ thống theo lối cũ sẽ phải đập đi làm lại rất tốn kém.

### 14.1 AI Evaluation Trends (2024-2026)

Bảng này điểm danh **6 xu hướng lớn** định hình cách chấm AI từ 2024 đến 2026: tự động hóa khâu chấm (meta-evaluation), chấm real-time, tối ưu chi phí, cho người và AI chấm cùng nhau, benchmark theo ngành, và đưa evaluation vào CI/CD như code. Mỗi gạch đầu dòng là một gợi ý bạn có thể thử bê về hệ thống nhà mình.

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

## 15. Trajectory, Contamination, Cost-per-Quality & Hiệu Chuẩn Với Con Người

Chỉ nhìn pass/fail thì không biết agent đã làm việc *ra sao*. Section này chấm thêm trajectory (đi có hiệu quả không, gọi tool có chuẩn không, vấp có tự đứng dậy không), dọn vệ sinh harness chống rò rỉ đề, tính $/pass-task để chọn model khôn ngoan, và hiệu chuẩn judge LLM với người thật. Bạn hình dung như chấm tay đua rally: về đích là quan trọng, nhưng rẽ nhầm chỗ nào (step), có đi đường vòng không (tool call), gặp sự cố có gượng lại được không (recovery), và có tập trước trên đường đua này không (contamination) cũng quan trọng không kém.

> **Ghi chú dedup:** §7 và §10 đều kể lại SWE-bench end-to-end. Quy ước: §7 = *định nghĩa benchmark* (SWE-bench/HumanEval đo gì); §10 = *kết quả case-study* (ai đạt bao nhiêu). §15 này chỉ bổ sung *phương pháp* (metric trajectory, isolation, chi phí, hiệu chuẩn).

### 15.1 Chấm Trajectory — Hiệu Quả Step, Độ Chính Xác, Khả Năng Phục Hồi

| Metric | Định Nghĩa | Mục Tiêu |
|---|---|---|
| `pass` | Task được giải (test + kiểm tra ẩn) | cổng chính |
| `steps_used / steps_p50` | Hiệu quả step = số step tham chiếu p50 ÷ số step thực tế (trần 1.0) | ≥ 0.7 |
| `tool_precision` | Số tool call hữu ích ÷ tổng tool call | ≥ 0.6 |
| `recovery_rate` | Số lỗi tự sửa không cần người ÷ tổng đợt lỗi | ≥ 0.5 |
| `wasted_edits` | Số lần ghi file bị hoàn tác trong cùng run ÷ tổng lần ghi | ≤ 0.2 |
| `trajectory_score` | `0.5·pass + 0.2·efficiency + 0.15·precision + 0.15·recovery` | cổng CI ≥ 0.65 |

Chấm trajectory chứ đừng chỉ nhìn kết quả: ghi log mọi span `(thought, tool, args, result, cost)`; vòng lặp retry kiểu brute-force mà may mắn pass cũng bị trừ điểm.

### 15.2 Vệ Sinh Contamination & Isolation

- **Rò rỉ (Leakage):** cách ly mọi task có lời giải/văn bản issue xuất hiện trong training cutoff; gắn thẻ `leak_risk: high` và loại khỏi con số chính (báo cáo riêng).
- **Seed:** cố định `seed` + `temperature=0` cho bộ regression; eval không đơn định chạy 3 lần và báo cáo mean ± std.
- **Cách ly flaky:** test lỗi <5% trong 50 run tự vào làn `flaky/`; không bao giờ chặn promotion, nhưng mở tracking issue.
- **Cô lập (Isolation):** container/FS mới cho mỗi task, không cache chung giữa các task, chặn mạng trừ mirror trong allow-list; hash dataset + ghi commit SHA vào báo cáo.

### 15.3 Cost-per-Quality — Metric Định Tuyến $/Pass-Task

Công thức `$/pass-task = total_eval_cost ÷ tasks_passed`. Bạn theo dõi theo từng model/route; task dễ thì đi model rẻ, hỏng mới leo thang (cascade). Báo cáo gọn trong bảng Pareto:

| Route | Pass % | $/1k task | $/pass-task | Kết Luận |
|---|---|---|---|---|
| small-only | 52% | $18 | $0.035 | baseline rẻ |
| small→large cascade | 71% | $46 | $0.065 | ✅ tradeoff tốt nhất |
| large-only | 74% | $210 | $0.284 | chỉ khi chất lượng là tối quan trọng |

Chỉ nâng cấp model khi đạt *cả hai*: Δpass ≥ +2pp *và* Δ$/pass-task ≤ +10%.

### 15.4 Hiệu Chuẩn Với Con Người — Judge-so-với-Người Có Đồng Thuận Không

- Lấy mẫu 100–200 task/quý để người chấm mù lại; tính κ của Cohen và tỉ lệ đồng thuận theo từng chiều (correctness/style/safety).
- Yêu cầu κ ≥ 0.7 trước khi judge được gác cổng promotion; thấp hơn → chỉnh rubric + few-shot, không bao giờ hạ chuẩn.
- **Kiểm tra bias:** bias độ dài (dài hơn ≠ hay hơn), tự thiên vị (judge chấm họ nhà mình cao hơn), bias vị trí (đảo thứ tự A/B); báo cáo độ lệch bias kèm điểm số.

<details>
<summary>Python Code — Trajectory Scorer (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/18-15-4-hieu-chuan-voi-con-nguoi-judge.py`](examples/18-15-4-hieu-chuan-voi-con-nguoi-judge.py)

</details>

### 15.5 Checklist

- [ ] Log đầy đủ trajectory + tính efficiency/precision/recovery
- [ ] Gác cổng bằng `trajectory_score`, không chỉ pass%
- [ ] Cách ly rò rỉ + ghim seed + chạy lại 3 lần cho eval ngẫu nhiên
- [ ] Làn flaky tách khỏi bộ blocking
- [ ] Báo cáo $/pass-task theo route + chính sách cascade
- [ ] Hiệu chuẩn với người hằng quý (κ ≥ 0.7) + kiểm tra bias độ dài/tự thiên vị/vị trí
- [ ] Hash dataset + SHA môi trường trong mọi báo cáo

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

---

> **Phụ lục Oct-2026:** evals nay bao cả automation (eval từng node + workflow, Custom Graders Library,
> generated graders). Ghép `minimal-benchmark-harness.md` với log trajectory (`13`) + trace OTel để chấm tái lập được.

---

## Cập nhật 10/2026 — LLM-as-Judge & End-State Evaluation (Anthropic 06/2025)

> **📌 Bối cảnh:** Tổng hợp từ bài *Demystifying Evals for AI Agents* (Anthropic, 06/2025). Thông điệp chính: **đừng đợi eval hoàn hảo mới bắt đầu** — bắt đầu nhỏ, chấm bằng LLM, và đánh giá trạng thái cuối thay vì từng bước.

### 1. Eval-First — Bắt Đầu Với ~20 Test Cases

Sai lầm phổ biến nhất: **hoãn xây eval** đến khi hệ thống "ổn định" — rồi khi cần đo lường thì không có baseline để so. Thực tế ngược lại:

> **Điểm mấu chốt:** Những thay đổi sớm nhất có **effect size lớn nhất** — khi cải thiện success rate từ **30% → 80%**, bạn **thấy được ngay với sample nhỏ** (~20 test cases). Còn khi hệ thống đã 85%, muốn thấy khác biệt 85% → 87% cần hàng nghìn cases.

| Giai đoạn | Số test cases | Lý do đủ dùng |
|---|---|---|
| Đầu dự án | ~20 | Effect size lớn (30%→80%), khác biệt thấy rõ ngay |
| Đang trưởng thành | 100–500 | Phát hiện regression theo feature mới |
| Ổn định | Hàng trăm–hàng nghìn | So model/version, tinh chỉnh nhỏ |

### 2. LLM-as-Judge Pattern

Đây là cách chấm **đơn giản nhất mà align nhất với human judgement**: 1 LLM call, 1 prompt, chấm theo rubric cố định:

| Tiêu chí | Câu hỏi chấm |
|---|---|
| **Factual accuracy** | Mỗi claim trong output có khớp với sources không? |
| **Citation accuracy** | Trích dẫn có trỏ đúng nguồn hỗ trợ claim đó không? |
| **Completeness** | Có bỏ sót phần nào của task không? |
| **Source quality** | Primary sources được ưu tiên hơn secondary không? |
| **Tool efficiency** | Agent dùng tool hợp lý hay lăng nhăng, dư thừa? |

**Output:** score `0.0–1.0` + nhãn `pass/fail`. Vì output có cấu trúc nên scale được cho **hàng trăm outputs** mà không cần đọc tay từng cái.

### 3. End-State Evaluation

Với agent **mutate state** (viết file, chạy lệnh, thay đổi DB), đừng chấm từng step — chấm **trạng thái cuối**:

> **Tại sao?** Cùng một đích, agent có thể đến bằng **nhiều path** khác nhau. Chấm từng step sẽ trừng phạt path khác thường dù kết quả đúng; chấm end-state thì công bằng và phản ánh đúng giá trị người dùng nhận được.

| Loại task | Đánh giá |
|---|---|
| Agent sửa code | ✅ Tests pass? Build thành công? Không phá chức năng cũ? |
| Agent deploy infra | ✅ Endpoint trả đúng kết quả? Trạng thái cluster đúng? |
| Agent research | ✅ Answer có đúng câu hỏi, có nguồn đáng tin? |

Với **workflow phức tạp**, chia tiến trình thành các **checkpoints** — mỗi checkpoint ứng với một **state change mong đợi** — để vừa chấm end-state vừa biết đứt gãy ở đoạn nào nếu fail.

### 4. Human Evaluation — Bắt Edge Cases

Tự động hóa không bắt hết — cần **người đọc hàng loạt output** (trong giai đoạn đầu) để bắt các class lỗi mà rubric chưa bao phủ:

- **Hallucinated answers:** agent khẳng định chắc nịch nhưng không có nguồn nào hỗ trợ.
- **System failures:** timeout, tool gọi sai, crash âm thầm không bị chấm là fail.
- **Source selection bias:** ví dụ kinh điển — agents **chọn SEO content farms thay vì academic PDFs**. Fix: thêm **source quality heuristics vào prompt** (ưu tiên `.edu`, `.gov`, domain uy tín; phạt content farm).

> Pattern: người tìm edge case → biến edge case thành test case mới → rubric/heuristics được cập nhật → LLM-judge tự chấm được class lỗi đó lần sau. **Human evaluation là nguồn nuôi dưỡng eval tự động, không phải thay thế nó.**

### 5. Production Reliability Eval

Sau khi lên production, evaluation chuyển vai trò từ "chấm bài" sang "canh gác":

| Hoạt động | Mục đích |
|---|---|
| **Regression test sau mỗi deploy** | Chạy lại bộ eval trước khi release — bắt sự cố do prompt/model/tool đổi |
| **Tracing decision patterns** | Log **decision patterns** (agent chọn tool nào, rẽ nhánh nào) — không log nội dung conversation (privacy) — để debug root cause khi quality tụt |

### 6. Code Python — LLM-Judge với Rubric Prompt

> 📄 **Code ví dụ:** [`examples/19-6-code-python-llm-judge-voi-rubric-prompt.py`](examples/19-6-code-python-llm-judge-voi-rubric-prompt.py)

**Điểm mấu chốt:** 1 call, 1 rubric, output JSON parse được, pass/fail theo threshold — đủ dùng cho CI chạy hàng trăm test cases mà không cần harness phức tạp.

### 7. Cross-Reference

> 📎 **Liên quan:** [`../../AGENT_SYSTEM_ARCHITECTURE.md`](../../AGENT_SYSTEM_ARCHITECTURE.md) — **Layer 8** (Evaluation). Xem thêm Section 4.2 (LLM-as-Judge Evaluation) ở trên cho pattern chấm code chi tiết hơn, và `07-workflow` cho checkpoint khi agent chạy dài.

---

**Ngày cập nhật:** 26/10/2026  
**Tác giả:** AI Knowledge Repository
