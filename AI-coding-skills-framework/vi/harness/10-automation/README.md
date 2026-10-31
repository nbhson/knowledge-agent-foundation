# ⚙️ X. Automation

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Automation Patterns](#1-automation-patterns)
>   - [1.1 Pattern Taxonomy](#11-pattern-taxonomy)
>   - [1.2 Automation Framework](#12-automation-framework)
> - [2. CI/CD Pipelines](#2-cicd-pipelines)
>   - [2.1 CI/CD Pipeline Architecture](#21-cicd-pipeline-architecture)
>   - [2.2 GitHub Actions Templates](#22-github-actions-templates)
>   - [2.3 Pipeline Configuration](#23-pipeline-configuration)
> - [3. Code Generation Automation](#3-code-generation-automation)
>   - [3.1 Automated Code Generation](#31-automated-code-generation)
> - [4. Testing Automation](#4-testing-automation)
>   - [4.1 Test Automation Strategy](#41-test-automation-strategy)
>   - [4.2 Automated Test Runner](#42-automated-test-runner)
> - [5. Monitoring & Alerting](#5-monitoring-alerting)
>   - [5.1 Monitoring Architecture](#51-monitoring-architecture)
>   - [5.2 Monitoring System](#52-monitoring-system)
> - [6. Self-Healing Systems](#6-self-healing-systems)
>   - [6.1 Self-Healing Patterns](#61-self-healing-patterns)
>   - [6.2 Self-Healing Implementation](#62-self-healing-implementation)
> - [7. Scheduled Tasks](#7-scheduled-tasks)
>   - [7.1 Task Scheduler](#71-task-scheduler)
> - [8. Workflow Templates](#8-workflow-templates)
>   - [8.1 Common Automation Workflows](#81-common-automation-workflows)
> - [9. Anti-Patterns & Solutions](#9-anti-patterns-solutions)
>   - [9.1 Common Anti-Patterns](#91-common-anti-patterns)
> - [10. Production Automation](#10-production-automation)
>   - [10.1 Production Checklist](#101-production-checklist)
> - [Best Practices](#best-practices)
> - [11. Case Studies Thực Tế](#11-case-studies-thực-tế)
>   - [11.1 SWE-agent: Automated Software Engineering](#111-swe-agent-automated-software-engineering)
>   - [11.2 Anthropic's Claude Code Automation](#112-anthropics-claude-code-automation)
>   - [11.3 Cursor IDE: AI-Native Development](#113-cursor-ide-ai-native-development)
>   - [11.4 GitHub Copilot: Enterprise Automation](#114-github-copilot-enterprise-automation)
>   - [11.5 Vercel v0: Full-Stack Automation](#115-vercel-v0-full-stack-automation)
> - [12. TypeScript Interfaces cho Automation](#12-typescript-interfaces-cho-automation)
>   - [12.1 Core Automation Types](#121-core-automation-types)
> - [13. Design Principles cho Automation](#13-design-principles-cho-automation)
>   - [13.1 SOLID cho Automation Systems](#131-solid-cho-automation-systems)
>   - [13.2 Automation Design Principles](#132-automation-design-principles)
> - [14. Testing Automation Harness](#14-testing-automation-harness)
>   - [14.1 Testing Automation Systems](#141-testing-automation-systems)
> - [15. Anti-Patterns & Solutions Chi Tiết](#15-anti-patterns-solutions-chi-tiết)
>   - [15.1 Common Anti-Patterns](#151-common-anti-patterns)
>   - [15.2 DO vs DON'T Summary](#152-do-vs-dont-summary)
> - [16. Future Trends trong Automation](#16-future-trends-trong-automation)
>   - [16.1 AI-Powered Automation (2024-2026)](#161-ai-powered-automation-2024-2026)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
---

### Câu Chuyện Mở Đầu

Hãy hình dung một ngày của bạn: sáng `git pull`, sửa code, chạy test, chiều build, tối deploy rồi lại ngồi dò log. Ngày nào cũng y chang như vậy. Lần đầu bạn còn làm cẩn thận từng bước. Đến lần thứ mười, bạn bắt đầu làm tắt. Đến lần thứ năm mươi, chỉ cần quên một bước nhỏ là production lăn ra lỗi.

**Automation sinh ra để cắt cái vòng lặp mệt mỏi đó.**

Trong AI coding, automation không chỉ là CI/CD pipeline. Nó là mọi việc lặp đi lặp lại: viết boilerplate, chạy test, review code, deploy, monitor, thậm chí tự sửa lỗi khi có sự cố. Làm đúng, cả team bớt việc tay chân để dành sức cho việc khó hơn — suy nghĩ, thiết kế, sáng tạo.

**Cách làm**: dựng Automation Pipeline đi từ manual → scripted → triggered → self-healing → predictive, để team có thể **deploy hàng trăm lần mỗi ngày** thay vì mỗi tuần một lần hồi hộp.

### Tại Sao Automation Quan Trọng?

> *"Automation không thay thế con người — nó thay thế những việc con người KHÔNG PHẢI làm."*

#### 3 Bằng Chứng Khoa Học

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **GitHub (2025)** | Repositories với CI/CD automation giảm **60% deployment failures** và **44% time-to-merge** |
| 2 | **DORA Report (2025)** | Top-performing teams automate **95%+ deployments** — deploy hàng trăm lần/ngày thay vì hàng tuần |
| 3 | **Stripe Engineering (2024)** | Automated code review pipelines phát hiện **38% more bugs** trước khi reaches human reviewers |

#### Triết lý cốt lõi:

```
Automation = Repetition → Rule → Script → Self-Healing Pipeline
```

**Automation Maturity Model**:
- **Level 0**: Manual (mỗi lần làm tay)
- **Level 1**: Scripted (có script chạy lại được)
- **Level 2**: Triggered (tự chạy khi event xảy ra)
- **Level 3**: Self-healing (tự detect + fix issues)
- **Level 4**: Predictive (tự predict vấn đề trước khi xảy ra)

**Analogies**: Automation giống dây chuyền sản xuất — ban đầu từng bước làm tay, dần dần conveyor belt tự chạy, robot tự lắp ráp, và cuối cùng nhà máy tự hoạt động 24/7.

**Nếu bỏ qua**: Manual steps = bottlenecks, human errors mỗi lần lặp lại, team dành 40% thời gian cho repetitive tasks thay vì innovation.

## Tổng Quan

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Automation trong AI coding là việc để máy (kèm AI Agent) tự làm những quy trình lặp lại — sinh code, chạy test, deploy, giám sát — thay vì con người làm tay từng lần.
>
> **Ẩn dụ/so sánh:** Như dây chuyền sản xuất: ban đầu từng bước làm tay, dần dần băng tải tự chạy, robot tự lắp ráp, rồi cả nhà máy tự hoạt động 24/7.
>
> **Vì sao quan trọng:** Team hết bớt "việc tay chân" để dành sức cho việc suy nghĩ và sáng tạo.

Nói ngắn gọn: **Automation** trong AI coding là để máy lo những việc lặp đi lặp lại — từ sinh code, chạy test, deploy cho đến monitor. Mục tiêu cũng rất đời thường: con người can thiệp ít lại, làm nhanh hơn, và lần nào kết quả cũng đều tay như lần nào.

```
┌──────────────────────────────────────────────────────────────────┐
│                     AUTOMATION PIPELINE                           │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Trigger  │───►│  Process │───►│ Validate │───►│  Deploy  │ │
│  │           │    │  & Build │    │  & Test  │    │  & Ship  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │         │
│  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    │
│  │ • Git   │    │ • AI    │    │ • Tests │    │ • CI/CD │    │
│  │ • Cron  │    │ • Build │    │ • Lint  │    │ • Docker│    │
│  │ • Event │    │ • Format│    │ • Type  │    │ • K8s   │    │
│  │ • Manual│    │ • Gen   │    │ • Audit │    │ • Notify│    │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Automation Patterns](#1-automation-patterns) | Các pattern tự động hóa phổ biến |
| 2 | [CI/CD Pipelines](#2-cicd-pipelines) | Pipeline tích hợp liên tục |
| 3 | [Code Generation Automation](#3-code-generation-automation) | Tự động generate code |
| 4 | [Testing Automation](#4-testing-automation) | Tự động test |
| 5 | [Monitoring & Alerting](#5-monitoring--alerting) | Theo dõi và cảnh báo |
| 6 | [Self-Healing Systems](#6-self-healing-systems) | Hệ thống tự sửa chữa |
| 7 | [Scheduled Tasks](#7-scheduled-tasks) | Tác vụ định kỳ |
| 8 | [Workflow Templates](#8-workflow-templates) | Mẫu quy trình tự động |
| 9 | [Anti-Patterns & Solutions](#9-anti-patterns--solutions) | Các lỗi thường gặp |
| 10 | [Production Automation](#10-production-automation) | Tự động hóa sản phẩm |

---

## 1. Automation Patterns

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Automation Patterns là các khuôn mẫu thiết kế chuẩn hóa cho quy trình chạy tự động — theo sự kiện (event-driven), theo lịch (scheduled) hay theo điều kiện (conditional) — giúp AI Agent làm các việc lặp lại mà không cần người can thiệp.
>
> **Ẩn dụ/so sánh:** Giống công thức nấu ăn chuẩn hóa: cùng một món, ai vào bếp cũng làm y hệt nhau, không ai nêm sai liều.
>
> **Vì sao quan trọng:** Có pattern tốt, cả đội không phải "phát minh lại" quy trình mỗi lần — automation chạy ổn định và dễ sửa khi cần.

### 1.1 Pattern Taxonomy

Bạn cứ đọc bảng phân loại này như đọc sơ đồ một xưởng nhỏ, chia làm 4 nhóm cho dễ nhớ: **Trigger Patterns** là "ai bấm nút khởi động" — sự kiện, lịch hẹn, điều kiện hay làm tay; **Process Patterns** là "máy chạy kiểu gì" — chạy nối tiếp, chia ra chạy song song rồi gom lại, kiểu saga hay tự thử lại; **Quality Patterns** là "cửa kiểm hàng" — gate, canary, blue-green, feature flag; còn **Feedback Patterns** là "xong rồi thì sao" — báo tin, tự rollback, rút kinh nghiệm, tự chỉnh thông số.

```
┌──────────────────────────────────────────────────────────────────┐
│                 AUTOMATION PATTERN TAXONOMY                       │
│                                                                  │
│  TRIGGER PATTERNS                                                │
│  ├── Event-driven    → Git push, webhook, API call              │
│  ├── Scheduled       → Cron, interval, time-based               │
│  ├── Conditional     → Threshold, anomaly, state change         │
│  └── Manual          → On-demand trigger                        │
│                                                                  │
│  PROCESS PATTERNS                                                │
│  ├── Pipeline        → Sequential steps with gates              │
│  ├── Fan-out/Fan-in  → Parallel processing + merge              │
│  ├── Saga            → Distributed transaction with rollback    │
│  └── Retry           → Automatic retry on failure               │
│                                                                  │
│  QUALITY PATTERNS                                                │
│  ├── Gate            → Must pass before proceeding               │
│  ├── Canary          → Deploy to small % first                  │
│  ├── Blue-Green      → Two environments, switch                 │
│  └── Feature Flag    → Toggle features without deploy           │
│                                                                  │
│  FEEDBACK PATTERNS                                               │
│  ├── Notification    → Alert humans when needed                 │
│  ├── Auto-rollback   → Revert on failure                        │
│  ├── Learning        → Improve from past results                │
│  └── Adaptive        → Adjust parameters dynamically            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Automation Framework

Đoạn code dưới đây là một **`AutomationPipeline`** — bạn hình dung nó như anh quản đốc trông cả dây chuyền: cho từng bước chạy nối tiếp nhau, bước nào gắn `gate=True` thì bắt buộc phải đạt mới được đi tiếp, lỗi thì tự thử lại vài lần (có giãn thời gian `backoff` cho đỡ dồn), còn bước gate mà hỏng hẳn thì tự rollback — gỡ lại những gì đã lắp. Muốn thử, bạn chỉ cần tạo pipeline, thêm vài step bằng `add_step()` hay `step()`, gắn hook `before()`/`after()` rồi gọi `execute()` là xong.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-automation-framework.py`](examples/01-1-2-automation-framework.py)

</details>

---

## 2. CI/CD Pipelines

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** CI/CD (Continuous Integration / Continuous Delivery) là đường ống tự động chạy mỗi khi code thay đổi — kiểm tra lỗi, build, chạy test rồi đưa lên production — để code mới luôn an toàn khi đến tay người dùng.
>
> **Ẩn dụ/so sánh:** Như dây chuyền kiểm tra chất lượng xe trước khi xuất xưởng: máy tự kiểm phanh, tự test thử đường, ngon thì mới giao đi.
>
> **Vì sao quan trọng:** Biến việc "deploy tay đầy rủi ro" thành quy trình lặp lại an toàn, bắt lỗi sớm trước khi khách hàng thấy.

### 2.1 CI/CD Pipeline Architecture

Hình dưới bạn đọc từ trên xuống như ba tầng của một dây chuyền: tầng **CI** kiểm hàng nhanh mỗi lần push — soi lint, check type, chạy unit test, build thử; tầng **CD** đưa hàng lên staging, chạy test tích hợp với E2E rồi mới cho lên production; tầng **Continuous Monitoring** thì ngồi canh metrics, thấy lạ là báo động và phản hồi ngược lại. Nguyên tắc nằm lòng: chỉ cần một bước hỏng là dừng cả line (`FAIL=stop`) — như thanh chắn không cho hàng lỗi trôi xuống công đoạn sau.

```
┌──────────────────────────────────────────────────────────────────┐
│                  CI/CD PIPELINE ARCHITECTURE                      │
│                                                                  │
│  CONTINUOUS INTEGRATION                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐       │   │
│  │  │  Lint  │─►│  Type  │─►│  Unit  │─►│ Build  │       │   │
│  │  │  Check │  │ Check  │  │ Tests  │  │        │       │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘       │   │
│  │      │           │           │            │              │   │
│  │    FAIL=stop    FAIL=stop   FAIL=stop    FAIL=stop      │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  CONTINUOUS DELIVERY                                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐       │   │
│  │  │Deploy  │─►│Integr. │─►│ E2E    │─►│Deploy  │       │   │
│  │  │Staging │  │ Tests  │  │ Tests  │  │Prod    │       │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘       │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                          │                                       │
│                          ▼                                       │
│  CONTINUOUS MONITORING                                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐       │   │
│  │  │Metrics │─►│Alerts  │─►│Log     │─►│Feedback│       │   │
│  │  │Collect │  │Check   │  │Analyze │  │Loop    │       │   │
│  │  └────────┘  └────────┘  └────────┘  └────────┘       │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 GitHub Actions Templates

File YAML dưới đây là một **workflow GitHub Actions làm sẵn** cho dự án Python — bạn copy vào `.github/workflows/ci.yml` là chạy được ngay. Nó chia việc thành 5 chặng: Validate → Test → Build → Security → Deploy, mỗi chặng là một `job` và nối nhau bằng `needs:` — việc sau chờ việc trước xong mới làm. Gặp dòng `if: github.ref == 'refs/heads/main'` thì bạn hiểu là "cửa này chỉ mở trên nhánh `main`", như cổng kho chỉ nhận đúng loại kiện hàng.

<details>
<summary><b>2.2 GitHub Actions Templates (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-github-actions-templates.yaml`](examples/02-2-2-github-actions-templates.yaml)

</details>

### 2.3 Pipeline Configuration

Class `CIPipelineConfig` trong đoạn code giống một tờ "phiếu gọi món" cho pipeline: bạn tick vào ngôn ngữ nào, cần quality gate nào, có quét bảo mật không, build và deploy ra sao... rồi gọi `to_github_actions()` là máy tự in ra file workflow YAML. Mỗi thuộc tính là một cái công tắc bật/tắt — khai đúng thì khỏi phải viết tay từng dòng YAML.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-2-3-pipeline-configuration.py`](examples/03-2-3-pipeline-configuration.py)

</details>

---

## 3. Code Generation Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Code Generation Automation là dùng AI để sinh mã theo yêu cầu — scaffold project, boilerplate, CRUD, API — kèm cơ chế kiểm tra chất lượng để con người duyệt trước khi dùng.
>
> **Ẩn dụ/so sánh:** Như nhà máy đúc khuôn: ra sản phẩm nhanh với số lượng lớn, nhưng mỗi sản phẩm vẫn phải qua khâu kiểm tra bằng tay.
>
> **Vì sao quan trọng:** Tiết kiệm hàng giờ viết "mã nhàm chán" lặp lại, để developer tập trung vào logic khó và đáng giá hơn.

### 3.1 Automated Code Generation

Class `CodeGenerator` dưới đây như một chiếc máy đúc "nhà tiền chế" cho CRUD: bạn đưa tên model và danh sách fields kiểu `{"name": "str", "age": "int"}` rồi gọi `generate_crud(model_name, fields)` một cái, máy tự đúc ra đủ bộ — model SQLAlchemy, schema Pydantic, service, router FastAPI đến test pytest — nằm gọn trong `output_dir`, khỏi ngồi gõ từng file.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-3-1-automated-code-generation.py`](examples/04-3-1-automated-code-generation.py)

</details>

---

## 4. Testing Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing Automation là để AI (và pipeline) tự viết test, chạy test suite rồi phân tích kết quả — bắt lỗi sớm trước khi code được merge, không cần làm tay.
>
> **Ẩn dụ/so sánh:** Như đội kiểm phẩm tự động trong xưởng may: máy tự căng chỉ, sờ đường may, sản phẩm nào lỗi là kéo ra khỏi dây chuyền ngay.
>
> **Vì sao quan trọng:** Bắt lỗi ngay lúc viết code (chi phí thấp nhất) thay vì để khách hàng gặp lỗi ngoài production.

### 4.1 Test Automation Strategy

Hình trên là **kim tự tháp test** quen thuộc: đáy to là unit test — rẻ, chạy nhanh nên viết nhiều; giữa là integration test — vừa vừa; đỉnh nhỏ là E2E — đắt, chậm nên chỉ chọn đường quan trọng mà test. Kèm theo là mức tự động hóa gợi ý cho từng tầng và cửa CI (ví dụ muốn merge PR phải đạt >80% coverage). Nếu test suite nhà bạn đang "trồng cây chuối" — toàn E2E chậm rì — thì nhìn vào hình này là biết cần dời bớt xuống đáy.

```
┌──────────────────────────────────────────────────────────────────┐
│               TEST AUTOMATION PYRAMID                             │
│                                                                  │
│                        /\                                        │
│                       /  \         E2E Tests                     │
│                      / E2E\       (Few, slow, expensive)        │
│                     /──────\                                     │
│                    /        \     Integration Tests              │
│                   / Integr.  \   (Some, moderate speed)          │
│                  /────────────\                                  │
│                 /              \  Unit Tests                     │
│                /   Unit Tests   \ (Many, fast, cheap)            │
│               /──────────────────\                               │
│                                                                  │
│  AUTOMATION TARGETS:                                             │
│  ├── Unit tests:     100% automated (fast feedback)             │
│  ├── Integration:    90% automated (API + DB)                    │
│  ├── E2E tests:      70% automated (critical paths only)        │
│  └── Performance:    50% automated (periodic runs)               │
│                                                                  │
│  CI GATES:                                                       │
│  ├── PR merge:    Unit + Integration pass, >80% coverage        │
│  ├── Staging:     All tests pass                                │
│  └── Production:  Smoke tests pass after deploy                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 Automated Test Runner

`AutomatedTestRunner` giống một thầy giám thị cần mẫn: bạn đăng ký các `TestCase` vào (có chia loại unit/integration/E2E/performance/security, gắn `tags` và `timeout` đàng hoàng), gọi `run()` là thầy tự lọc theo category/tag, cho chạy lần lượt rồi gom điểm trả về báo cáo có `gate_passed`. Muốn thử, bạn cứ tạo vài test giả, `register()` vào rồi in kết quả `run()` ra — nhìn bảng điểm là biết ngay môn nào đậu, môn nào rớt.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-4-2-automated-test-runner.py`](examples/05-4-2-automated-test-runner.py)

</details>

---

## 5. Monitoring & Alerting

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Monitoring & Alerting là hệ thống theo dõi liên tục sức khỏe ứng dụng — metrics, logs, errors — và tự báo động khi có bất thường để AI xử lý hoặc thông báo người trực.
>
> **Ẩn dụ/so sánh:** Như bảng đồng hồ taplo ô tô: kim nhiệt độ và đèn cảnh báo sáng lên để bạn xử lý trước khi xe chết máy giữa đường.
>
> **Vì sao quan trọng:** Phát hiện "vừa mới hỏng" còn cứu được — phát hiện khi "đã sập tiếng rồi" thì thành sự cố lớn.

### 5.1 Monitoring Architecture

Kiến trúc này bạn đọc xuôi theo mũi tên là ra ba tầng: **Data Collection** lo thu thập — metrics từ Prometheus, log từ ELK/Loki, trace từ Jaeger; **Processing** lo gom lại, vẽ dashboard, soi xem có gì bất thường; rồi **Alerting** lo hú còi qua Slack/Email/PagerDuty. Cứ hình dung như hệ cảm biến trong gara ô tô: phải gắn cảm biến trước, mới có bảng đồng hồ để nhìn, rồi chuông mới kêu khi xe có sự cố.

```
┌──────────────────────────────────────────────────────────────────┐
│              MONITORING & ALERTING ARCHITECTURE                    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    DATA COLLECTION                        │   │
│  │                                                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │   │
│  │  │ Metrics  │  │   Logs   │  │  Traces  │  │ Events │ │   │
│  │  │(Promethe)│  │(ELK/Loki)│  │(Jaeger)  │  │(custom)│ │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘ │   │
│  │       └──────────────┴──────────────┴────────────┘      │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    PROCESSING                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │   Aggregate  │  │  Analyze &   │  │    Detect     │  │   │
│  │  │   & Store    │  │  Dashboard   │  │   Anomalies   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    ALERTING                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Slack   │  │  Email   │  │  PagerDuty│              │   │
│  │  │  Alert   │  │  Alert   │  │  Alert    │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Monitoring System

`MonitoringSystem` là một hệ giám sát gọn nhẹ, đọc code là hiểu ngay: `record_metric()` để ghi từng điểm số, `add_alert_rule()` để đặt luật (kiểu "CPU > 90% thì báo"), `on_alert()` để gắn người xử lý khi luật bị chạm, `get_metric_stats()` để tính min, max, mean, p95, còn `generate_dashboard()` thì vẽ bảng tổng hợp dạng chữ. Bạn cứ thử record vài metric, thêm một rule "gt 80" rồi chạy — thấy alert tự bắn là hiểu cơ chế. Nói vui thì đây là cuốn sổ khám sức khỏe của hệ thống, mở ra là biết đang khỏe hay sắp phải đi cấp cứu.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/06-5-2-monitoring-system.py`](examples/06-5-2-monitoring-system.py)

</details>

---

## 6. Self-Healing Systems

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Self-Healing là kiến trúc để hệ thống tự phát hiện lỗi, tự chẩn đoán và tự khôi phục — restart service, rollback, sửa config — mà không cần người làm tay.
>
> **Ẩn dụ/so sánh:** Như cơ thể tự cầm máu khi trầy da hay tự hạ sốt khi nhiễm khuẩn — không cần "đợi bác sĩ" mỗi lần.
>
> **Vì sao quan trọng:** Rút thời gian chết từ "hàng giờ" xuống "hàng giây" và giảm áp lực cho người trực.

### 6.1 Self-Healing Patterns

Năm pattern dưới đây là "bộ kỹ năng tự cứu" của hệ thống, bạn cứ nhớ theo kiểu đời thường: **auto-restart** là ngã thì tự đứng dậy, **auto-rollback** là đi sai thì quay lại bản cũ cho lành, **auto-scale** là quán đông thì kê thêm bàn, **retry + backoff** là đường kẹt thì chờ bớt kẹt rồi đi tiếp, còn **circuit breaker** là thấy bên kia đang sập thì tạm ngưng gọi, đợi khỏe lại mới thử từng ít một. Mỗi pattern đều ghi rõ Trigger (khi nào kích hoạt) và Action (làm gì) — đọc như tờ hướng dẫn xử lý sự cố dán ngay cạnh tủ điện.

```
┌──────────────────────────────────────────────────────────────────┐
│              SELF-HEALING PATTERNS                                │
│                                                                  │
│  PATTERN 1: AUTO-RESTART                                         │
│  ┌──────────┐  fail  ┌──────────┐  restart  ┌──────────┐      │
│  │  Service │───────►│  Detect  │──────────►│  Restart │      │
│  │  Running │        │  Failure │           │  Service │      │
│  └──────────┘        └──────────┘           └──────────┘      │
│  Trigger: Process exit, health check fail                       │
│  Action: Restart process/service                                │
│                                                                  │
│  PATTERN 2: AUTO-ROLLBACK                                        │
│  ┌──────────┐  error  ┌──────────┐  revert  ┌──────────┐     │
│  │  Deploy  │────────►│  Monitor │─────────►│ Rollback │     │
│  │  v2.0    │         │  Metrics │          │  to v1.9 │     │
│  └──────────┘         └──────────┘          └──────────┘     │
│  Trigger: Error rate > threshold, latency spike                │
│  Action: Revert to last known good version                     │
│                                                                  │
│  PATTERN 3: AUTO-SCALE                                          │
│  ┌──────────┐  load   ┌──────────┐  scale  ┌──────────┐      │
│  │  Traffic │───────►│  Monitor │────────►│ Add/Remove│      │
│  │  Spike   │        │  Load    │         │ Instances │      │
│  └──────────┘        └──────────┘         └──────────┘      │
│  Trigger: CPU > 80%, queue depth > threshold                   │
│  Action: Add/remove instances                                  │
│                                                                  │
│  PATTERN 4: AUTO-RETRY WITH BACKOFF                             │
│  ┌──────────┐  fail   ┌──────────┐  wait   ┌──────────┐      │
│  │  API     │───────►│  Failure │───────►│  Retry   │      │
│  │  Call    │         │  Detected│        │  (exp)   │      │
│  └──────────┘         └──────────┘        └──────────┘      │
│  Trigger: Transient error (network, timeout)                   │
│  Action: Retry with exponential backoff                        │
│                                                                  │
│  PATTERN 5: CIRCUIT BREAKER                                    │
│  ┌──────────┐  fail>5 ┌──────────┐  wait   ┌──────────┐      │
│  │  Service │───────►│  Circuit │───────►│ Half-Open│      │
│  │  Call    │         │  OPEN    │        │  Test    │      │
│  └──────────┘         └──────────┘        └──────────┘      │
│  Trigger: Consecutive failures > threshold                     │
│  Action: Stop calling, periodically test recovery              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Self-Healing Implementation

`SelfHealingSystem` là hiện thân bằng code của mấy pattern trên: bạn đăng ký các `health_checks` để khám sức khỏe định kỳ, hệ thống đếm số lần fail liên tiếp — đủ ngưỡng (mặc định 5 lần) là mở `circuit breaker` và gọi `recovery_handler` đến "cấp cứu". Hàm `allow_request()` thì như người gác cổng, nhìn trạng thái circuit (`CLOSED`/`OPEN`/`HALF_OPEN`) để quyết cho request vào hay không. Muốn thử, bạn đăng ký một check hay vấp lỗi, để nó fail tới ngưỡng rồi ngồi xem hệ thống tự gọi xe cứu thương và hồi phục.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-6-2-self-healing-implementation.py`](examples/07-6-2-self-healing-implementation.py)

</details>

---

## 7. Scheduled Tasks

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Scheduled Tasks là các công việc chạy tự động đúng giờ định sẵn — dọn log, backup DB, tạo báo cáo, cập nhật dependency — theo lịch (cron/interval).
>
> **Ẩn dụ/so sánh:** Như chiếc đồng hồ báo thức của hệ thống: đến giờ tự làm mà không cần ai nhắc.
>
> **Vì sao quan trọng:** Các việc vận hành đều đặn không bao giờ bị quên, team không phải canh chừng.

### 7.1 Task Scheduler

`TaskScheduler` giống cái đồng hồ hẹn giờ trong bếp: `schedule()` là đặt lịch cho một task (kiểu `interval`/`daily`/`weekly`), `run_pending()` là đi một vòng xem món nào đến giờ thì "ting" lên chạy, rồi tự tính `next_run` bằng `_calculate_next()` và ghi log lại. Bạn thử schedule một hàm in chữ với interval 1 giây rồi gọi `run_pending()` vài lần sẽ thấy — chưa đến giờ thì nó nằm yên, đến giờ mới chạy, khỏi cần ai ngồi canh.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-7-1-task-scheduler.py`](examples/08-7-1-task-scheduler.py)

</details>

---

## 8. Workflow Templates

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Workflow Templates là các khuôn mẫu quy trình tự động dùng lại được — pipeline cho feature, hotfix, bảo trì ban đêm, đánh giá PR — giúp thiết lập automation nhanh và đồng bộ.
>
> **Ẩn dụ/so sánh:** Như bộ "mẫu hợp đồng" soạn sẵn: mỗi lần dùng chỉ điền vài ô là xong, không phải viết lại từ đầu.
>
> **Vì sao quan trọng:** Mọi dự án mới đều có sẵn "đường ray" đã được kiểm chứng, giảm rủi ro thiết lập sai.

### 8.1 Common Automation Workflows

Từ điển `WORKFLOW_TEMPLATES` dưới đây dọn sẵn 4 "mâm" quy trình cho bạn chọn: `feature_pipeline` để làm tính năng mới bài bản, `hotfix_pipeline` để vá gấp khi production đang cháy, `nightly_maintenance` để dọn dẹp ban đêm, và `pr_quality_check` để soi chất lượng PR. Mỗi mẫu chỉ là danh sách steps kèm `command` và cờ `gate` — `gate: True` nghĩa là bước này tạch là cả mâm dừng. Cách dùng cũng như chọn slide mẫu thuyết trình: lấy mẫu hợp nhu cầu rồi sửa lại commands cho vừa nhà mình.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/09-8-1-common-automation-workflows.py`](examples/09-8-1-common-automation-workflows.py)

</details>

---

## 9. Anti-Patterns & Solutions

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Anti-Patterns là những cách làm automation tưởng đúng mà hóa sai — pipeline mỏng manh, lỗi âm thầm (silent failures), secrets nằm trong code, không có rollback — kèm giải pháp khắc phục.
>
> **Ẩn dụ/so sánh:** Như danh sách "cạm bẫy" của thợ lặn: biết trước chỗ nào nguy hiểm để tránh, thay vì học mót sau khi gặp nạn.
>
> **Vì sao quan trọng:** Đa số sự cố automation đều đến từ một nhóm nhỏ lỗi lặp lại — nhận diện được là chữa được ngay.

### 9.1 Common Anti-Patterns

Danh sách 8 mục dưới đây toàn là "bệnh kinh niên" của automation: pipeline mong manh đụng nhẹ là gãy, lỗi âm thầm kiểu báo pass mà deploy thì hỏng, secret nhét thẳng trong code, deploy hỏng không có đường lui, pipeline dài lê thê, test lúc đậu lúc rớt, chạy mà không ai ngó, và vẫn còn bước deploy phải làm tay. Mỗi mục đều viết theo kiểu **Vấn đề → Giải pháp**. Bạn đọc như đọc biên bản điều tra tai nạn: thấy team mình có triệu chứng nào thì chữa ngay chỗ đó.

```
┌──────────────────────────────────────────────────────────────────┐
│           AUTOMATION ANTI-PATTERNS                                │
│                                                                  │
│  ❌ ANTI-PATTERN 1: FRAGILE PIPELINES                            │
│     Pipeline fails on minor config changes                       │
│     → SOLUTION: Version control pipeline configs, test changes  │
│                                                                  │
│  ❌ ANTI-PATTERN 2: SILENT FAILURES                              │
│     Pipeline reports success but deploy is broken                │
│     → SOLUTION: Add post-deploy verification, smoke tests       │
│                                                                  │
│  ❌ ANTI-PATTERN 3: CREDENTIALS IN CODE                          │
│     Hardcoded secrets in pipeline configs                        │
│     → SOLUTION: Use secret managers (Vault, GitHub Secrets)     │
│                                                                  │
│  ❌ ANTI-PATTERN 4: NO ROLLBACK PLAN                             │
│     Deploy fails, no way to revert                               │
│     → SOLUTION: Blue-green deploys, auto-rollback on failure    │
│                                                                  │
│  ❌ ANTI-PATTERN 5: TOO LONG PIPELINES                           │
│     CI takes 30+ minutes → developers ignore results            │
│     → SOLUTION: Parallelize, split into stages, cache deps      │
│                                                                  │
│  ❌ ANTI-PATTERN 6: FLAKY TESTS                                  │
│     Tests randomly fail → developers skip them                   │
│     → SOLUTION: Fix flaky tests, quarantine unreliable tests    │
│                                                                  │
│  ❌ ANTI-PATTERN 7: NO MONITORING                                │
│     Deploy succeeds but service is degraded                      │
│     → SOLUTION: Health checks, metrics, alerting                │
│                                                                  │
│  ❌ ANTI-PATTERN 8: MANUAL DEPLOY STEPS                          │
│     "Just click this button" → human error                       │
│     → SOLUTION: Fully automated deploy pipeline                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Production Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Production Automation là đưa automation vào môi trường thật một cách an toàn — canary rollout, auto-rollback, giám sát chặt — để hệ thống tự vận hành ổn định với rủi ro được kiểm soát.
>
> **Ẩn dụ/so sánh:** Như lái thử xe: chạy thử quãng ngắn trước, nếu trục trặc tự phanh về điểm xuất phát, không ai phải lao ra sửa giữa đường.
>
> **Vì sao quan trọng:** Ở production, để lỗi xảy ra là mất tiền và uy tín — automation phải an toàn trước đã.

### 10.1 Production Checklist

Checklist này là tờ "khám tổng quát" trước khi cho automation ra chạy thật, chia làm 5 nhóm: CI/CD pipeline, monitoring, self-healing, scheduled tasks và security. Bạn cứ tick từng ô một — ô nào chưa tick nghĩa là rủi ro vẫn còn nằm đó. Cứ hình dung như phi công check máy bay trước khi cất cánh: thiếu một mục là chưa được rời đường băng.

```
┌──────────────────────────────────────────────────────────────────┐
│            PRODUCTION AUTOMATION CHECKLIST                        │
│                                                                  │
│  CI/CD PIPELINE:                                                 │
│  □ Lint + type check on every PR                                │
│  □ Unit tests with >80% coverage gate                           │
│  □ Integration tests on staging                                 │
│  □ Automated build + push to registry                           │
│  □ Canary deploy before full rollout                            │
│  □ Auto-rollback on health check failure                        │
│                                                                  │
│  MONITORING:                                                     │
│  □ Application metrics (latency, errors, throughput)            │
│  □ Infrastructure metrics (CPU, memory, disk)                   │
│  □ Log aggregation (structured logging)                         │
│  □ Distributed tracing                                          │
│  □ Alert rules for critical metrics                             │
│                                                                  │
│  SELF-HEALING:                                                   │
│  □ Health checks (liveness + readiness)                         │
│  □ Auto-restart on crash                                        │
│  □ Circuit breakers for external dependencies                   │
│  □ Rate limiting                                                │
│  □ Graceful degradation                                         │
│                                                                  │
│  SCHEDULED TASKS:                                                │
│  □ Database backups (daily)                                     │
│  □ Log cleanup (weekly)                                         │
│  □ Security scans (weekly)                                      │
│  □ Dependency updates (monthly)                                 │
│  □ Performance benchmarks (nightly)                             │
│                                                                  │
│  SECURITY:                                                       │
│  □ Secrets in secret manager (not in code)                      │
│  □ Dependency vulnerability scanning                            │
│  □ SAST/DAST scanning in pipeline                               │
│  □ Access controls for deploy                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Best Practices là bộ 10 nguyên tắc vàng đúc kết từ thực tế — automate việc lặp lại, fail fast, luôn có rollback, giám sát mọi thứ — để automation đáng tin cậy.
>
> **Ẩn dụ/so sánh:** Như cuốn sổ "kinh nghiệm xương máu" của đội vận hành: theo thì đỡ đau, bỏ qua thì nhận hậu quả.
>
> **Vì sao quan trọng:** Đây là danh sách kiểm tra nhanh để biết hệ thống automation của bạn đang sắp "vỡ" ở chỗ nào.

```
┌──────────────────────────────────────────────────────────────────┐
│              AUTOMATION BEST PRACTICES                            │
│                                                                  │
│  1. AUTOMATE THE REPEATABLE                                      │
│     If you do it more than twice → automate it                  │
│     Focus on high-value, high-frequency tasks                    │
│                                                                  │
│  2. FAIL FAST                                                    │
│     Run cheapest checks first (lint → test → build)             │
│     Gate critical steps (no deploy without tests passing)       │
│                                                                  │
│  3. MAKE IT REVERSIBLE                                           │
│     Every deploy must have a rollback plan                      │
│     Blue-green or canary deployments                            │
│                                                                  │
│  4. OBSERVE EVERYTHING                                           │
│     If it's not monitored, it's not production-ready            │
│     Log, measure, alert on everything important                 │
│                                                                  │
│  5. KEEP PIPELINES FAST                                          │
│     Target: <10 min for CI, <30 min for CD                      │
│     Parallelize, cache dependencies, skip unnecessary steps     │
│                                                                  │
│  6. VERSION CONTROL EVERYTHING                                   │
│     Pipeline configs in repo (IaC)                              │
│     Infrastructure as Code (Terraform, Pulumi)                  │
│                                                                  │
│  7. TEST THE AUTOMATION                                          │
│     Test pipeline configs before merging                         │
│     Chaos testing for self-healing                               │
│                                                                  │
│  8. NOTIFICATION WITHOUT NOISE                                   │
│     Alert on actionable items only                               │
│     Different channels for different severity                   │
│                                                                  │
│  9. DOCUMENT RUNBOOKS                                            │
│     Every alert should have a runbook                            │
│     Automate the runbook if possible                             │
│                                                                  │
│  10. ITERATE AND IMPROVE                                         │
│      Review pipeline metrics weekly                             │
│      Remove bottlenecks, add value                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

---

## 11. Case Studies Thực Tế

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Case Studies Thực Tế là các ví dụ automation đã chạy thật trong sản xuất — SWE-agent, Claude Code, Cursor, GitHub Copilot, Vercel v0 — để rút bài học từ người đi trước.
>
> **Ẩn dụ/so sánh:** Như xem phim tài liệu về các nhà máy thành công: không cần tự lặp lại sai lầm của họ.
>
> **Vì sao quan trọng:** "Người ta đã làm được rồi" là bằng chứng mạnh nhất trước khi bạn đầu tư công sức.

### 11.1 SWE-agent: Automated Software Engineering

Hình trên kể chuyện **SWE-agent** — một AI agent nhận GitHub issue rồi tự lục codebase (Search) và tự sửa file (Edit) để ra bản vá. Bí quyết nằm ở **autonomy loop**: agent cứ lặp đi lặp lại vòng Quan sát → Suy nghĩ → Hành động → Quan sát cho tới khi xong. Nói theo kiểu đời thường, đây là anh thợ "giao việc là tự lo": không cần ai khui thùng đồ hay chỉ tay từng bước, chỉ cần đưa con bug là tự xoay xở từ đầu tới cuối.

```
┌──────────────────────────────────────────────────────────────────┐
│                    SWE-AGENT ARCHITECTURE                         │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  GitHub Issue │───►│  SWE-agent   │───►│  Patch File  │       │
│  │  (Problem)    │    │  (LLM Agent) │    │  (Solution)  │       │
│  └──────────────┘    └──────┬───────┘    └──────────────┘       │
│                             │                                     │
│                    ┌────────┴────────┐                            │
│                    │                 │                             │
│              ┌─────▼─────┐   ┌─────▼─────┐                     │
│              │  Search    │   │  Edit      │                     │
│              │  Codebase  │   │  Files     │                     │
│              │  (Read)    │   │  (Write)   │                     │
│              └───────────┘   └───────────┘                     │
│                                                                  │
│  KEY INSIGHT: Agent cần ability để navigate codebase,           │
│  không chỉ là generate code. Autonomy loop:                       │
│  Observe → Think → Act → Observe → ...                          │
│                                                                  │
│  PERFORMANCE (SWE-bench):                                        │
│  ├── Resolved: 12.47% (full) → 24.07% (with LSP)              │
│  ├── Median steps: 6-8 edits per issue                          │
│  └── Average tokens: 15K-25K per issue                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 11.2 Anthropic's Claude Code Automation

Bức hình trên tóm triết lý automation của Claude Code, nghe ngược đời mà lại hiệu quả: **đừng gồng xây khung sườn phức tạp, cứ tin model** — để model tự quyết đọc file nào, sửa file nào, tự đẻ sub-agent khi cần, bí quá mới nâng cấp công cụ (graceful degradation). Kết quả là một model duy nhất mà đi được hết 200K dòng source code. Bài học ở đây cũng mộc mạc: nhiều khi prompt tốt cộng vòng lặp ngắn lại thắng cả hệ thống phức tạp.

```
┌──────────────────────────────────────────────────────────────────┐
│                CLAUDE CODE AUTOMATION STRATEGY                    │
│                                                                  │
│  PRINCIPLE 1: "Model is 99% of the solution"                    │
│  → Focus on prompt engineering, not complex tooling             │
│  → Simple agent loop beats complex orchestrations               │
│                                                                  │
│  PRINCIPLE 2: "Let the model do the work"                       │
│  → Model decides what files to read/edit                         │
│  → Model writes its own sub-agents (Task tool)                  │
│  → Model uses grep/ripgrep to navigate codebase                 │
│                                                                  │
│  PRINCIPLE 3: "Graceful degradation"                            │
│  → Try without MCP → Add MCP if stuck                          │
│  → Try single agent → Escalate to sub-agents                    │
│  → Try local context → Fetch from remote if needed             │
│                                                                  │
│  AUTOMATION DECISIONS:                                           │
│  ├── Which files to read → Model decides (not rules)           │
│  ├── When to stop reading → Model decides (not timeout)        │
│  ├── When to ask user → Model decides (not always)             │
│  └── When to give up → Model decides (not hardcoded)           │
│                                                                  │
│  RESULT: 200K+ lines of source code navigated by single model  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 11.3 Cursor IDE: AI-Native Development

Bức hình mổ xẻ 3 kiểu automation của Cursor cho dễ chọn: **Tab completion** là gợi ý theo từng phím gõ, trả lời dưới 100ms; **Inline edit** (Cmd+K) là khoanh vùng code rồi ra lệnh bằng tiếng người để sửa tại chỗ, có xem trước diff; còn **Chat** (Cmd+L) là hỏi đáp với cả repo làm bối cảnh. Điểm hay là Cursor không đoán từ tiếp theo mà đoán **lần sửa tiếp theo**. Bạn nhớ mẹo dùng: gõ nhanh thì Tab, sửa đoạn ngắn thì Cmd+K, thắc mắc lớn thì Cmd+L.

```
┌──────────────────────────────────────────────────────────────────┐
│                  CURSOR AUTOMATION PIPELINE                       │
│                                                                  │
│  TAB COMPLETION (Autocomplete):                                  │
│  ├── Trigger: Every keystroke                                   │
│  ├── Speed: <100ms response time                               │
│  ├── Context: Current file + imports + open files               │
│  └── Pattern: Predict next edit, not next token                │
│                                                                  │
│  INLINE EDIT (Cmd+K):                                           │
│  ├── Trigger: User selection + natural language instruction     │
│  ├── Context: Selected code + surrounding context               │
│  ├── Pattern: Edit-in-place with diff preview                   │
│  └── Quality: One-shot generation, minimal iteration           │
│                                                                  │
│  CHAT (Cmd+L):                                                  │
│  ├── Trigger: User question with codebase context               │
│  ├── Context: @-mentioned files + chat history                  │
│  ├── Pattern: Multi-turn conversation with file references      │
│  └── Scope: Can span multiple files and files                  │
│                                                                  │
│  AUTOMATION HIGHLIGHT:                                           │
│  → Predict edits (not just tokens) for autocomplete            │
│  → Small, focused context windows per feature                   │
│  → Local indexing + remote LLM hybrid approach                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 11.4 GitHub Copilot: Enterprise Automation

Hình trên xếp Copilot thành 4 nấc theo độ "tự lo" tăng dần: gợi ý từng dòng (inline completion), chat ngay trong IDE, **PR automation** (tự viết mô tả PR, AI review, tự vá lỗ hổng bảo mật) rồi tới **Copilot Workspaces** (agent tự sửa nhiều file và dọn sẵn PR cho người duyệt). Bạn đọc từ dưới lên là thấy hành trình từ gợi ý nhỏ đến làm trọn gói một task. Con số đáng nhớ: 77% Fortune 100 dùng Copilot, làm nhanh hơn 55% và xong nhiều code hơn 46%.

```
┌──────────────────────────────────────────────────────────────────┐
│               GITHUB COPILOT AUTOMATION LAYERS                    │
│                                                                  │
│  LAYER 1: INLINE COMPLETION                                      │
│  ├── Context: Current file + nearby files                       │
│  ├── Model: GPT-4o / Codex                                     │
│  ├── Latency: <500ms                                            │
│  └── Automation: Real-time suggestion on every line            │
│                                                                  │
│  LAYER 2: CHAT IN IDE                                           │
│  ├── Context: Entire workspace (via indexing)                   │
│  ├── Pattern: Natural language → Code generation               │
│  └── Automation: @workspace for full codebase access           │
│                                                                  │
│  LAYER 3: PULL REQUEST AUTOMATION                               │
│  ├── Copilot for PRs: Auto-generate PR descriptions            │
│  ├── Copilot Code Review: AI reviewer for PRs                  │
│  ├── Copilot Autofix: Auto-fix security vulnerabilities        │
│  └── Automation: CI/CD integration with GitHub Actions         │
│                                                                  │
│  LAYER 4: COPILOT WORKSPACES (Beta)                             │
│  ├── Task assignment to AI agent                                │
│  ├── Autonomous code changes with PR creation                   │
│  ├── Multi-file refactoring capabilities                        │
│  └── Human-in-the-loop review before merge                     │
│                                                                  │
│  SCALE: 77% of Fortune 100 uses Copilot                        │
│  IMPACT: 55% faster task completion, 46% more code completed   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 11.5 Vercel v0: Full-Stack Automation

Sơ đồ này kể mô hình "nói một câu ra cả app" của Vercel v0: bạn đưa mô tả (text, ảnh, Figma) → máy sinh code (React, SQL, API) → bạn xem trước live qua URL → ưng hay chưa thì chat để sửa tiếp. Điểm ăn tiền là vòng xem-trước-sửa cực nhanh, dựng xong khung app chưa tới 5 phút. Nói theo kiểu quán ăn: bạn gọi món theo thực đơn, được ngó món trước khi ăn, muốn đổi vị thì nói một câu là bếp làm lại ngay.

```
┌──────────────────────────────────────────────────────────────────┐
│                    V0 AUTOMATION PATTERN                          │
│                                                                  │
│  INPUT: Natural language → FULL-STACK APP                        │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Prompt   │───►│ Generate │───►│  Preview │───►│ Iterate  │ │
│  │  (NL)     │    │  Code    │    │  (Live)  │    │ (Edit)   │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │         │
│  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    │
│  │ • Text  │    │ • React │    │ • URL   │    │ • Chat  │    │
│  │ • Image │    │ • SQL   │    │ • Code  │    │ • Ref   │    │
│  │ • Figma │    │ • API   │    │ • Diff  │    │ • Undo  │    │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│                                                                  │
│  AUTOMATION HIGHLIGHTS:                                          │
│  → Scaffolding to production-ready in <5 min                   │
│  → Automatic: Component gen → Styling → DB schema → API       │
│  → Real-time streaming preview during generation               │
│  → Iterative refinement via natural language                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 12. TypeScript Interfaces cho Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** TypeScript Interfaces là định nghĩa kiểu dữ liệu cho toàn bộ hệ automation — pipeline config, trigger, quality gate, self-healing — để mô tả và kiểm tra hệ thống bằng ngôn ngữ có kiểu tĩnh.
>
> **Ẩn dụ/so sánh:** Như bản vẽ kỹ thuật trước khi đổ bê tông: kích thước rõ ràng từ đầu, sai lệch bị bắt ngay trên bản vẽ.
>
> **Vì sao quan trọng:** Compiler gánh một nửa công việc kiểm tra — lỗi cấu hình bị chặn lúc viết, không phải lúc deploy.

### 12.1 Core Automation Types

Đây là bộ **interface TypeScript** vẽ lại cả hệ automation dưới dạng dữ liệu: `PipelineConfig` (cấu hình pipeline, trigger, gates), `PipelineRun`/`StepRun` (sổ theo dõi từng lần chạy), `MetricDefinition`/`AlertConfig` (phần giám sát), `SelfHealingConfig` (phần tự phục hồi) và nhóm `GuardrailConfig` (hàng rào an toàn — giới hạn số file, số lần retry, khi nào phải duyệt mới được deploy). Bạn đọc mỗi interface như một cái khuôn có ghi chú từng ô — dữ liệu cứ đúng khuôn thì các bộ phận mới hiểu nhau.

<details>
<summary><b>12.1 Core Automation Types (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/10-12-1-core-automation-types.ts`](examples/10-12-1-core-automation-types.ts)

</details>

---

## 13. Design Principles cho Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Design Principles là bộ nguyên tắc thiết kế cốt lõi — đơn giản, tái sử dụng được, giám sát được, an toàn — giúp hệ thống tự động bền và dễ bảo trì về lâu dài.
>
> **Ẩn dụ/so sánh:** Như luật giao thông cho nhà máy: không thú vị, nhưng thiếu nó thì tắc nghẽn và xảy ra tai nạn.
>
> **Vì sao quan trọng:** Hệ thống automation càng lớn, thiếu nguyên tắc thiết kế càng nhanh sập.

### 13.1 SOLID cho Automation Systems

Hình trên dịch **5 nguyên tắc SOLID** ra tiếng automation cho dễ soi: mỗi step chỉ làm một việc (S), muốn thêm thì cắm plugin chứ đừng mổ lõi (O), step nào cũng nói chung một interface (L), interface nào cũng nhỏ gọn tách biệt (I), và chỉ bắt tay với abstraction chứ không ôm cứng implementation (D). Mỗi mục đều có ví dụ ✅/❌. Bạn đọc xong tự chấm pipeline nhà mình: nếu thấy một step vừa lint vừa test vừa deploy thì biết ngay nên tách ra.

```
┌──────────────────────────────────────────────────────────────────┐
│            SOLID PRINCIPLES IN AUTOMATION                         │
│                                                                  │
│  S — SINGLE RESPONSIBILITY                                       │
│  Each automation step does ONE thing well                        │
│  ✅ Lint step → only lint                                        │
│  ✅ Test step → only test                                        │
│  ❌ "Lint-Test-Deploy" step → too many responsibilities          │
│                                                                  │
│  O — OPEN/CLOSED                                                 │
│  Open for extension, closed for modification                    │
│  ✅ Plugin-based steps (add new steps without changing core)    │
│  ❌ Hardcoded step list (requires code change to add steps)     │
│                                                                  │
│  L — LISKOV SUBSTITUTION                                         │
│  Any step implementation should work in any pipeline             │
│  ✅ All steps implement StepHandler interface                    │
│  ❌ Different step types with incompatible APIs                  │
│                                                                  │
│  I — INTERFACE SEGREGATION                                       │
│  Small, focused interfaces for automation                       │
│  ✅ Separate: TriggerHandler, StepHandler, Notifier             │
│  ❌ One giant AutomationInterface with 20 methods               │
│                                                                  │
│  D — DEPENDENCY INVERSION                                        │
│  Depend on abstractions, not implementations                    │
│  ✅ Step depends on ILogger, not ConsoleLogger                   │
│  ❌ Step directly uses fs.writeFile()                           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 13.2 Automation Design Principles

Danh sách "10 điều răn" này là những luật nằm lòng khi thiết kế automation: việc lặp thì phải automate, hỏng thì hỏng sớm, lúc nào cũng có đường lui, cái gì cũng phải ngó được, giữ pipeline chạy nhanh, tất cả cho vào version control, chính automation cũng phải được test, báo động ít mà chất, viết runbook đàng hoàng và cải tiến liên tục. Bạn đọc như đọc nội quy phòng cháy: cách chữa cháy tốt nhất là đừng để cháy.

```
┌──────────────────────────────────────────────────────────────────┐
│         AUTOMATION DESIGN PRINCIPLES (10 Commandments)            │
│                                                                  │
│  1. THOU SHALL AUTOMATE THE REPEATABLE                          │
│     → If done >2 times → automate it                            │
│     → Focus on high-value, high-frequency tasks                 │
│                                                                  │
│  2. THOU SHALL FAIL FAST                                         │
│     → Run cheapest checks first (lint → test → build)           │
│     → Gate critical steps (no deploy without tests)             │
│                                                                  │
│  3. THOU SHALL MAKE IT REVERSIBLE                               │
│     → Every deploy must have rollback plan                      │
│     → Blue-green or canary deployments                          │
│                                                                  │
│  4. THOU SHALL OBSERVE EVERYTHING                               │
│     → If not monitored, not production-ready                    │
│     → Log, measure, alert on everything important               │
│                                                                  │
│  5. THOU SHALL KEEP PIPELINES FAST                              │
│     → Target: <10 min CI, <30 min CD                            │
│     → Parallelize, cache, skip unnecessary steps                │
│                                                                  │
│  6. THOU SHALL VERSION CONTROL EVERYTHING                       │
│     → Pipeline configs in repo (IaC)                            │
│     → Infrastructure as Code (Terraform, Pulumi)                │
│                                                                  │
│  7. THOU SHALL TEST THE AUTOMATION                              │
│     → Test pipeline configs before merging                      │
│     → Chaos testing for self-healing systems                    │
│                                                                  │
│  8. THOU SHALL NOT NOISE                                        │
│     → Alert on actionable items only                            │
│     → Different channels for different severity                 │
│                                                                  │
│  9. THOU SHALL DOCUMENT RUNBOOKS                                │
│     → Every alert should have a runbook                         │
│     → Automate the runbook if possible                          │
│                                                                  │
│  10. THOU SHALL ITERATE AND IMPROVE                             │
│      → Review pipeline metrics weekly                           │
│      → Remove bottlenecks, add value                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 14. Testing Automation Harness

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Testing Automation Harness là "phòng thí nghiệm" kiểm chứng automation trước khi chạy thật — validate pipeline config, test từng bước, mô phỏng rollback, chaos test.
>
> **Ẩn dụ/so sánh:** Như phòng mô phỏng bay cho phi công: tập dượt đủ tình huống nguy hiểm mà không gặp rủi ro thật.
>
> **Vì sao quan trọng:** Nhìn "có vẻ chạy" là không đủ — phải chứng minh automation chịu được lỗi mới dám tin tưởng.

### 14.1 Testing Automation Systems

`AutomationTestHarness` là phòng thí nghiệm để kiểm chứng chính automation: bạn đăng ký các `AutomationTest` theo từng kiểu (`PIPELINE_CONFIG`, `STEP_EXECUTION`, `ROLLBACK`, `CIRCUIT_BREAKER`, `INTEGRATION`, `CHAOS`, `PERFORMANCE`), mỗi test có `setup`/`teardown` và `expected_result`; gọi `run_all()` hay `run_by_type()` là có báo cáo kèm `gate_passed`. Cuối đoạn còn có 3 ví dụ thật: CI workflow có tồn tại không, circuit breaker có mở sau 3 lần fail không, rollback có về đúng bản cũ không. Cứ hình dung như phòng thử va đập của hãng xe — cho đâm thử ở nơi an toàn để xe thật ra đường không gặp chuyện.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/11-14-1-testing-automation-systems.py`](examples/11-14-1-testing-automation-systems.py)

</details>

---

## 15. Anti-Patterns & Solutions Chi Tiết

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Phần này phân tích sâu các lỗi automation nâng cao — flaky tests, monolithic pipeline, silent failures, alert fatigue — kèm chiến lược phát hiện và khắc phục cụ thể từng bước.
>
> **Ẩn dụ/so sánh:** Như bác sĩ chẩn bệnh: không chỉ kê thuốc mà chỉ rõ triệu chứng, xét nghiệm và liệu trình.
>
> **Vì sao quan trọng:** Lỗi nhỏ nếu không nhận diện sẽ leo thang thành sự cố hệ thống đắt đỏ.

### 15.1 Common Anti-Patterns

Phần này mổ sâu **6 bệnh nặng** hay gặp: test lúc đậu lúc rớt (flaky tests), pipeline khổng lồ ôm hết mọi thứ (monolithic pipeline), lỗi âm thầm, không có đường rollback, vẫn sót bước làm tay, và cảnh báo nhiều tới mức chẳng ai buồn đọc (alert fatigue). Mỗi mục đều theo cấu trúc **Problem → Solution** với cách xử lý từng bước. Bạn đọc như đi khám bệnh: thấy team mình có triệu chứng nào thì lấy đúng toa đó mà chữa.

```
┌──────────────────────────────────────────────────────────────────┐
│              AUTOMATION ANTI-PATTERNS                             │
│                                                                  │
│  ❌ ANTI-PATTERN: Flaky Tests                                   │
│     Problem: Tests that pass/fail randomly                      │
│     Solution:                                                 │
│     → Isolate external dependencies (mock, stub)               │
│     → Use deterministic test data                              │
│     → Implement retry with jitter for network tests            │
│                                                                  │
│  ❌ ANTI-PATTERN: Monolithic Pipeline                           │
│     Problem: One giant pipeline for everything                 │
│     Solution:                                                 │
│     → Split into focused, composable pipelines                 │
│     → Use pipeline templates for reuse                         │
│     → Separate CI (validate) from CD (deploy)                 │
│                                                                  │
│  ❌ ANTI-PATTERN: Silent Failures                               │
│     Problem: Pipeline succeeds but output is broken            │
│     Solution:                                                 │
│     → Add post-deploy smoke tests                              │
│     → Implement health check gates                             │
│     → Monitor error rates after deploy                        │
│                                                                  │
│  ❌ ANTI-PATTERN: No Rollback Plan                              │
│     Problem: Deploy broken code with no way to revert          │
│     Solution:                                                 │
│     → Blue-green deployments                                    │
│     → Database migration backward compatibility                │
│     → Feature flags for quick disable                          │
│                                                                  │
│  ❌ ANTI-PATTERN: Manual Steps in Automation                   │
│     Problem: Human clicks required in the middle               │
│     Solution:                                                 │
│     → Fully automate the pipeline (no manual gates)           │
│     → Use chatops for approval (Slack/Teams integration)       │
│     → Implement auto-rollback instead of manual intervention   │
│                                                                  │
│  ❌ ANTI-PATTERN: Alert Fatigue                                 │
│     Problem: Too many alerts, everyone ignores them            │
│     Solution:                                                 │
│     → Tune alert thresholds based on historical data           │
│     → Implement severity levels (info/warn/critical)           │
│     → Add context and runbook links to every alert            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 15.2 DO vs DON'T Summary

Bảng hai cột này là tờ "nên — không nên" gọn nhất của cả module — 15 cặp đối nhau: việc lặp thì automate ↔ việc một lần thì thôi, pipeline phải có người ngó ↔ đừng kiểu "cài xong bỏ đấy"... Bạn in ra rồi dò từng dòng với hệ thống nhà mình; dòng nào đang rơi vào cột ❌ thì đó chính là việc cần sửa tiếp theo. Nhìn nhanh như tờ nội quy dán trong bếp: liếc qua là biết nên làm gì, nên tránh gì.

```
┌──────────────────────────────────────────────────────────────────┐
│              AUTOMATION DO vs DON'T                               │
│                                                                  │
│  ✅ DO:                          ❌ DON'T:                      │
│  Automate repeatable tasks       Automate one-off tasks         │
│  Test automation itself          Trust automation blindly       │
│  Version control configs         Store configs in UI only       │
│  Monitor all pipelines           "Set and forget" pipelines    │
│  Implement rollback              Deploy without rollback plan  │
│  Use quality gates               Skip tests to go faster       │
│  Parallelize when possible       Run everything sequentially   │
│  Cache dependencies              Reinstall every time          │
│  Notify on failures only         Spam notifications            │
│  Document runbooks               Assume everyone knows         │
│  Start simple, iterate           Build complex from day 1      │
│  Use canary deployments          Big bang deployments           │
│  Implement circuit breakers      Let failures cascade          │
│  Log everything                  Debug without logs            │
│  Review pipeline metrics weekly  Ignore pipeline performance   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 16. Future Trends trong Automation

> **📌 Khái Niệm Cơ Bản**
>
> **Khái niệm:** Future Trends là những hướng đi sắp tới của automation — agent tự chủ, AI sinh CI/CD, deploy tiên đoán, ra lệnh bằng ngôn ngữ tự nhiên.
>
> **Ẩn dụ/so sánh:** Như nhìn trước 5 phút trên xa lộ: biết hướng đi của cả đoàn xe để không bị tụt lại phía sau.
>
> **Vì sao quan trọng:** Hướng xây dựng hôm nay quyết định hệ thống của bạn "lỗi thời" trong 2 năm nữa hay không.

### 16.1 AI-Powered Automation (2024-2026)

Hình này điểm qua **6 xu hướng automation do AI dẫn dắt**: AI tự vẽ CI/CD, tự debug (tìm root cause, gợi ý fix, pipeline tự chữa lành), đoán trước rủi ro rồi mới deploy, ra lệnh bằng tiếng người kiểu "deploy main lên staging", platform engineering, và automation chạy ngay tại edge. Bạn đọc để trả lời một câu rất thực tế: "2 năm tới đội mình nên bỏ sức vào đâu?". Cứ coi như bản tin dự báo thời tiết — không trúng 100% nhưng đủ để bạn mang áo mưa đúng hôm cần.

```
┌──────────────────────────────────────────────────────────────────┐
│              FUTURE AUTOMATION TRENDS                             │
│                                                                  │
│  TREND 1: AI-GENERATED CI/CD                                     │
│  ├── AI generates CI/CD pipeline từ project structure           │
│  ├── Automatic test generation và coverage optimization        │
│  ├── Smart caching decisions dựa trên code analysis            │
│  └── Self-optimizing pipeline configurations                   │
│                                                                  │
│  TREND 2: AUTONOMOUS DEBUGGING                                   │
│  ├── AI agent tự động tìm root cause                          │
│  ├── Automatic fix suggestions cho test failures                │
│  ├── Self-healing CI/CD pipelines                              │
│  └── Smart retry với intelligent failure classification        │
│                                                                  │
│  TREND 3: PREDICTIVE DEPLOYMENT                                  │
│  ├── Predict deployment rủi ro trước khi xảy ra                 │
│  ├── Suggest optimal deployment windows                        │
│  ├── Auto-adjust canary percentage dựa on risk                │
│  └── Intelligent rollback timing                               │
│                                                                  │
│  TREND 4: NATURAL LANGUAGE AUTOMATION                            │
│  ├── "Deploy main to staging" → Full pipeline execution        │
│  ├── "Add a test for UserService" → Auto-generate test         │
│  ├── "Fix the failing CI" → Auto-diagnose và fix              │
│  └── "Monitor API latency" → Auto-setup monitoring            │
│                                                                  │
│  TREND 5: PLATFORM ENGINEERING                                   │
│  ├── Internal developer platforms (IDP)                         │
│  ├── Self-service infrastructure                               │
│  ├── Golden paths cho common workflows                         │
│  └── Automated compliance và governance                        │
│                                                                  │
│  TREND 6: EDGE AUTOMATION                                        │
│  ├── Run CI/CD at edge locations                                │
│  ├── Distributed testing across regions                        │
│  ├── Local-first automation (no cloud dependency)              │
│  └── Offline-capable automation pipelines                      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 17. An Toàn Deploy, Secret & Guard Cho Vòng Lặp Tự Động

Automation mà thiếu an toàn thì lỗi cũng lan đi với tốc độ máy. Section này vá đúng chỗ hổng đó: cổng canary kèm auto-rollback gắn với metric, secret cất trong vault, guard cứng cho vòng lặp tự động, và task định kỳ phải idempotent. Bạn hình dung như chế độ lái tự động của máy bay — nó tự bay được, nhưng vẫn bắt buộc có giới hạn G, trần nhiên liệu và cơ chế tự ngắt khi động cơ có dấu hiệu lạ.

> **Ghi chú dedup:** §9 "Common Anti-Patterns" và §15 "Anti-Patterns in Detail" trùng lặp ~70%. Quy ước: giữ §9 làm bảng tóm tắt 1 trang; §15 làm playbook chi tiết. Nội dung dưới đây mang tính chuẩn (normative) và liên kết chéo cả hai thay vì diễn đạt lại.

### 17.1 An Toàn Deploy — Cổng Canary + Auto-Rollback Gắn Metric

```
STAGES: 5% (10m) → 25% (30m) → 50% (30m) → 100%
PROMOTE GATE (all must pass at each stage):
 • error_rate_delta < +0.5pp vs baseline  • p95_latency_delta < +10%
 • smoke tests 100% pass                  • no Sev0/1 alerts firing
AUTO-ROLLBACK TRIGGERS (any fires → halt + revert):
 • error_rate > 2% for 3m  • p99_latency > SLO for 5m
 • smoke/canary job fail   • manual `halt` label on deploy PR
MECHANISM: blue-green or Argo Rollouts; DB migrations always
 backward-compatible (expand → migrate → contract)
```

Quy tắc: rollback tự động và được diễn tập hằng tháng (game day); mỗi deploy phát ra `deploy_id` nối vào metric/log để trigger đối chiếu được.

### 17.2 Quản Lý Secret & Cấu Hình

| Mối Quan Tâm | Tiêu Chuẩn |
|---|---|
| Lưu trữ | Chỉ dùng Vault / cloud secret manager; không bao giờ để trong repo, cấu hình chỉ-UI, hay transcript của agent |
| Phạm vi | Theo môi trường (`dev/staging/prod`) + theo service; agent chỉ nhận cred ngắn hạn, không bao giờ cầm key prod dài hạn |
| Nạp vào | Env lúc runtime hoặc file mount; `${SECRET:arn…}` do deployer resolve, không phải LLM |
| Xoay vòng | Tự động 30–90 ngày + ngay khi có sự cố; có phiên bản (`vN`) với cửa sổ hỗ trợ kép |
| Kiểm tra | Mọi lần đọc đều log (`who/what/when`); che trong log CI bằng masking filter |

### 17.3 Guard Vòng Lặp Tự Động — Giới Hạn Lặp / Chi Phí / Latency SLO

Mỗi vòng lặp tự phục hồi / agent mang `LoopBudget { maxIterations=10, maxCostUSD=5, maxLatencyMs=300_000, maxToolCalls=50 }`. Vòng lặp thoát khi gặp điều đầu tiên: thành công, cạn budget, hoặc confidence đi ngang (3 vòng không cải thiện). Khi cạn → đóng băng + mở incident kèm full trace, không bao giờ retry lặng lẽ. Hiển thị bộ đếm trực tiếp (`iteration/cost/latency`) trong log và tóm tắt CI.

### 17.4 Idempotency Task Định Kỳ + Chính Sách Chồng Lấn

- **Idempotency key:** `task_name + window_start` (ví dụ `nightly-e2e#2026-09-28`); handler kiểm tra dedup store trước khi hành động; tác dụng phụ dùng cùng key.
- **Chồng lấn (Overlap):** `concurrencyPolicy: Forbid` (bỏ qua nếu lần chạy trước còn đang chạy) cho deploy/migration; `Replace` chỉ cho sync đọc rẻ tiền. Đặt `activeDeadlineSeconds` + `startingDeadlineSeconds` để cron kẹt không dồn đống.
- **Bắt kịp (Catch-up):** `failedJobsHistoryLimit=3`; window bị lỡ chỉ backfill nếu được đánh dấu rõ `backfill: true`.

<details>
<summary>YAML + Python — Canary with Metric Rollback (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/12-17-4-idempotency-task-inh-ky-chinh-sach.yaml`](examples/12-17-4-idempotency-task-inh-ky-chinh-sach.yaml)

> 📄 **Code ví dụ:** [`examples/13-17-4-idempotency-task-inh-ky-chinh-sach.py`](examples/13-17-4-idempotency-task-inh-ky-chinh-sach.py)

</details>

### 17.5 Checklist

- [ ] Các stage canary + cổng promote được định nghĩa bằng code
- [ ] Trigger rollback gắn với metric (không thủ công) + đã diễn tập game-day
- [ ] Migration tương thích ngược
- [ ] Secret trong vault, theo phạm vi môi trường, tự xoay vòng, che trong log
- [ ] Budget vòng lặp (lặp/chi phí/latency/số tool-call) được thực thi + khi cạn sẽ mở incident
- [ ] Idempotency key cho cron + chồng lấn `Forbid` + trần deadline

---

## Tài Liệu Tham Khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Kubernetes Health Checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Circuit Breaker Pattern](https://microservices.io/patterns/reliability/circuit-breaker.html)
- [The Twelve-Factor App](https://12factor.net/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [SWE-agent](https://github.com/princeton-nlp/SWE-agent)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Cursor IDE](https://cursor.sh)
- [GitHub Copilot](https://docs.github.com/en/copilot)
- [Vercel v0](https://v0.dev)
- [Platform Engineering](https://internaldeveloperplatform.org/)
