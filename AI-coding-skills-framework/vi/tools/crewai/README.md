# 🚢 CrewAI — Multi-Agent Harness (Role-Based)

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao CrewAI Quan Trọng?](#tại-sao-crewai-quan-trọng)
> - [Quan Hệ Với Harness](#quan-hệ-với-harness)
> - [Tổng Quan](#tổng-quan)
> - [Lộ Trình Học (Cấu Trúc Thư Mục)](#lộ-trình-học-cấu-trúc-thư-mục)
> - [Case Studies Thực Tế](#case-studies-thực-tế)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Phần này kể lý do CrewAI ra đời: nó giải bài toán gì mà AutoGen chưa giải xong. AutoGen xem multi-agent như một cuộc trò chuyện — các agent nói chuyện với nhau tự do. Nhưng nhiều lúc bạn muốn mọi thứ rõ vai rõ việc hơn: **mỗi agent một vai (role — tức "vai diễn", ví dụ "người lên kế hoạch"), mỗi vai một nhiệm vụ (task), rồi cả bọn phối hợp trong một crew (crew = "đội kịch", tức nhóm agent làm chung một việc)**. Giống một công ty nhỏ: planner (bộ phận lập kế hoạch) lên kế hoạch, executor (bộ phận thi hành) xắn tay làm, reviewer (bộ phận soát xét) ngồi duyệt — ai làm việc nấy, không ai nói leo.

> *"CrewAI is the org chart for your harness — roles, tasks, and a crew that ships."*

**CrewAI** là framework multi-agent chia theo vai (framework = bộ khung code có sẵn, bạn lắp vào thay vì tự viết từ đầu). Ba viên gạch chính:
- `Agent` = một nhân viên AI, khai báo bằng role (vai), goal (mục tiêu), backstory (lý lịch — giúp agent hiểu mình là ai).
- `Task` = một đơn vị công việc, khai báo bằng description (làm gì), expected_output (kết quả mong đợi trông ra sao), agent (giao cho ai).
- `Crew` = cả đội, gồm agents (danh sách nhân viên), tasks (danh sách việc), process (cách phối hợp — chạy lần lượt hay theo cấp bậc).

Tiện một chỗ là code mẫu đã có sẵn trong HARNESS_ENGINEERING.md section 9.1, bạn mở ra là thấy ngay.

> **Tóm gọn 1 câu:** CrewAI chia đội agent theo đúng vai — như sơ đồ tổ chức: mỗi agent một chức danh, mỗi chức danh một việc, cả đội chạy dưới một crews chỉ huy chung.

### Tại Sao CrewAI Quan Trọng?

*Cách đọc bảng này: cột "Lý do" nêu điểm mạnh của CrewAI; cột "Giải thích" nói rõ điểm đó nghĩa là gì. Ví dụ, dòng 1 nói CrewAI gán vai cho mỗi agent, nên dễ ghép vào các thành phần harness.*

| # | Lý do | Giải thích |
|---|-------|------------|
| 1 | **Role-based rõ ràng** | Mỗi agent có role/goal/backstory — dễ map sang harness components |
| 2 | **Task-first** | `Task` là đơn vị công việc — đúng triết lý harness/04 (task decomposition) |
| 3 | **Process orchestrates** | `Process.sequential` / `Process.hierarchical` — kiểm soát thứ tự thực thi |
| 4 | **Human-in-the-loop** | `human_input` flag cho phép interjection giữa các bước |

*Chú giải thuật ngữ: task decomposition = bẻ việc lớn thành việc nhỏ; `Process.sequential` = chạy lần lượt từng việc; `Process.hierarchical` = có "quản lý" đứng phân công; `human_input` flag = công tắc cho phép con người xen lời vào giữa các bước (interjection = chen ngang để sửa hướng).*

> **Tóm gọn 1 câu:** CrewAI đáng học vì nó có sẵn đúng bốn thứ harness cần: vai rõ ràng, việc bẻ nhỏ, thứ tự chạy có kiểm soát, và chỗ cho người dùng xen tay.

### Quan Hệ Với Harness

*Đoạn sau đây giải thích CrewAI "khớp" vào bộ harness ở đâu. Đọc như bảng đối chiếu: vế trái là khái niệm của CrewAI, vế phải là module harness tương đương (harness/04, harness/06... là số thứ tự các module trong bộ harness).*

```
┌────────────────────────────────────────────────────────────┐
│  CREWAI MAP VS HARNESS COMPONENTS                          │
│                                                            │
│  Agent(role="Planner")   → harness/04 (plan/decompose)     │
│  Agent(role="Executor")  → harness/06 (tool execution)     │
│  Agent(role="Reviewer")  → harness/11 (evaluation)         │
│  Task + expected_output  → harness/08 (task)               │
│  Crew(process=...)       → harness/07 (workflow)           │
│  Crew + agents           → harness/09 (multi-agent)        │
└────────────────────────────────────────────────────────────┘
```

*Đọc ví dụ: dòng đầu nghĩa là "Agent đóng vai Planner trong CrewAI ≈ module harness/04, vốn phụ trách lập kế hoạch và bẻ nhỏ việc".*

> **Tóm gọn 1 câu:** Mỗi khái niệm CrewAI có một module harness tương đương — biết bản đồ này là bạn biết tra cứu chỗ nào khi cần đi sâu.

## Tổng Quan

*Phần này giới thiệu ba khái niệm nền của CrewAI. Nắm được ba chữ dưới đây là đọc được mọi code mẫu CrewAI.*

### Ba Khái Niệm Cốt Lõi

*Đọc như công thức: mỗi dòng là một đối tượng trong code, mũi tên chỉ ra nó là gì.*

```
Agent  →  AI worker với role/goal/backstory + tools
Task   →  Công việc cụ thể, expected output, giao cho agent nào
Crew   →  Tập hợp agents + tasks + process (cách chúng phối hợp)
```

*Ví dụ đời thường: Agent = "nhân viên named Long, chuyên review code"; Task = "review file main.py, mong đợi ra danh sách lỗi"; Crew = cả phòng Long + hai nhân viên kia + quy trình chạy việc.*

> **Tóm gọn 1 câu:** CrewAI có đúng ba khối lắp ghép — Agent (nhân viên), Task (việc), Crew (đội) — mọi hệ thống phức tạp đều ghép từ ba khối này.

### Code Mẫu Từ HARNESS_ENGINEERING.md

*Đây là code mẫu đầu tiên bạn nên mở: một crew hoàn chỉnh chạy được.*

> 📄 **Code ví dụ:** [`examples/01-code-mau-tu-harness-engineering-md.py`](examples/01-code-mau-tu-harness-engineering-md.py)

> **Tóm gọn 1 câu:** Đừng tự viết từ đầu — file ví dụ này đã có sẵn một crew hoàn chỉnh để bạn đọc và sửa.

### Process: Sequential vs Hierarchical

*Phần này giải thích hai cách xếp lịch chạy việc trong CrewAI — chọn sai cách là crew chạy sai thứ tự.*

> 📄 **Code ví dụ:** [`examples/02-process-sequential-vs-hierarchical.py`](examples/02-process-sequential-vs-hierarchical.py)

Hiểu đơn giản: `Process.hierarchical` chính là **harness/09-multi-agent** — có một manager đứng ra điều phối như harness orchestrator. Còn `Process.sequential` thì ứng với pipeline **harness/07-workflow**.

*Chú giải: sequential = "tuần tự" — việc 1 xong tới việc 2, như dây chuyền. hierarchical = "theo cấp bậc" — một agent quản lý nhận yêu cầu rồi tự phân công cho các agent dưới, như trưởng phòng giao việc cho nhân viên.*

> **Tóm gọn 1 câu:** Sequential chạy việc lần lượt như dây chuyền; hierarchical có một "trưởng phòng" agent đứng phân công — tương ứng với harness/07 và harness/09.

## Lộ Trình Học (Cấu Trúc Thư Mục)

*Phần này cho bạn biết thư mục này có gì và nên học theo thứ tự nào. Cây dưới đây là bản đồ thư mục — chữ (TODO) nghĩa là mục đó còn bỏ trống chờ viết.*

```
crewai/
├── README.md            ← BẠN ĐANG Ở ĐÂY — tổng quan + lộ trình
├── 01-concepts/         ← (TODO) Agent, Task, Crew, Process, Flows
├── 02-setup/            ← (TODO) Cài đặt crewai, cấu hình LLM, tools
├── 03-patterns/         ← (TODO) Sequential pipeline, hierarchical, flows
├── 04-savings/          ← (TODO) Token usage + cost per crew run
└── 05-troubleshooting/  ← (TODO) Agent misalignment, task delegation, memory
```

*Chú giải: token usage = lượng chữ AI tiêu thụ (căn cứ tính tiền); misalignment = agent hiểu sai ý, làm lệch mục tiêu; task delegation = agent giao việc hộ cho agent khác.*

### Lộ Trình Đề Xuất

*Đây là 5 bước đi từ không biết gì đến có crew chạy thật. Làm theo thứ tự, mỗi bước chỉ cần kết quả của bước trước.*

```
Bước 1: Đọc HARNESS_ENGINEERING.md section 9.1 — code mẫu CrewAI có sẵn
   ↓
Bước 2: Tạo Crew đơn giản: planner → executor → reviewer (sequential)
   ↓
Bước 3: Thêm tools cho executor (search, code, db) — harness/06
   ↓
Bước 4: Nâng lên Process.hierarchical với manager — harness/09
   ↓
Bước 5: Kết nối evaluation + observability (tools/evaluation, tools/observability)
```

*Chú giải: evaluation = bộ đo điểm chất lượng; observability = bộ theo dõi runtime (thấy agent đang làm gì, tốn bao nhiêu).*

*Cách đọc bảng này: cột trái là điều bạn muốn làm, cột phải là tài liệu nên mở ra. Ví dụ, muốn học cách bẻ nhỏ việc thì mở harness/04.*

| Bạn muốn... | Đọc |
|-------------|-----|
| Hiểu task decomposition | [harness/04-plan-decompose-task](../../harness/04-plan-decompose-task/) |
| Workflow orchestration | [harness/07-workflow](../../harness/07-workflow/) |
| Multi-agent concepts | [harness/09-multi-agent](../../harness/09-multi-agent/) |
| Task lifecycle | [harness/08-task](../../harness/08-task/) |

> **Tóm gọn 1 câu:** Đi theo 5 bước: đọc code mẫu → dựng crew tuần tự đơn giản → thêm tools → nâng lên cấp bậc có manager → nối thêm đo lường.

## Case Studies Thực Tế

*Phần này cho thấy hai tình huống thật hay gặp nhất khi dùng CrewAI, mỗi tình huống kèm code chạy được.*

### 1. Code Review Crew

*Tình huống: bạn muốn một đội agent tự soát code — một agent đọc diff, một agent nêu vấn đề. Code mẫu dưới đây dựng đúng đội đó.*

> 📄 **Code ví dụ:** [`examples/03-1-code-review-crew.py`](examples/03-1-code-review-crew.py)

> **Tóm gọn 1 câu:** Crew review code là ví dụ nhỏ nhất cho thấy ba khối Agent/Task/Crew ghép thành hệ thống thật.

### 2. Human-in-the-Loop

*Tình huống: bạn muốn con người duyệt trước khi agent làm việc quan trọng. human_input flag chính là nút dừng đó.*

> 📄 **Code ví dụ:** [`examples/04-2-human-in-the-loop.py`](examples/04-2-human-in-the-loop.py)

> **Tóm gọn 1 câu:** Bật human_input là bạn chèn một "trạm duyệt của người" vào giữa các bước của crew.

## Tài Liệu Tham Khảo

*Danh sách link gốc của CrewAI và các nhánh liên quan trong repo này.*

- **CrewAI**: https://docs.crewai.com/
- **GitHub**: https://github.com/crewAIInc/crewAI
- **Blog**: https://blog.crewai.com

### Liên Kết Sang Nhánh Khác

*Cách đọc: mỗi dòng là một tài liệu liên quan, sau dấu gạch ngang là lý do nên mở nó.*

- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.1 (code mẫu CrewAI)
- [harness/07-workflow](../../harness/07-workflow/) — Workflow orchestration
- [harness/09-multi-agent](../../harness/09-multi-agent/) — Multi-agent patterns
- [tools/autogen](../autogen/) — Multi-agent tương đương (conversation-based)
- [tools/langchain](../langchain/) — Graph-based orchestration

> **Tóm gọn 1 câu:** Muốn code mẫu mở HARNESS_ENGINEERING.md mục 9.1; muốn so cách tiếp cận khác thì xem autogen (kiểu hội thoại) và langchain (kiểu đồ thị).

---

> **"CrewAI gives your harness an org chart — roles, tasks, and a crew that ships."**

---

## ⚠️ Cập nhật 10/2026: CrewAI v1.x — Phiên Bản Mới Nhất

*Phần này tóm tắt thay đổi gần nhất của CrewAI để bạn không dùng thông tin lỗi thời.*

CrewAI đã phát hành **v1.0.0 (10/2025)** và đạt **v1.15.x (2026)** — nhiều thay đổi đáng chú ý:

*Cách đọc bảng này: cột trái là mốc phiên bản, cột phải là tính năng mới tại mốc đó. Ví dụ, từ v1.5.0 trở đi bạn viết được output theo cấu trúc (structured output = kết quả trả về theo format cố định, ví dụ JSON có schema, không phải text tự do).*

| Thay đổi | Chi tiết |
|----------|----------|
| **v1.0.0** | Knowledge & guardrail event handling trong Agent, response_format support |
| **v1.5.0** | Structured outputs, before/after tool call hooks |
| **v1.14+** | Inline skill definitions, Flow Definition authoring, dynamic LLM model pull |
| **crewAI CLI** | `crewai run` có cấu hình qua `crew.jsonc` |

*Chú giải: hook = móc code chạy tự động trước/sau một sự kiện; guardrail event handling = agent tự xử lý sự kiện bị chặn bởi lớp an toàn; `crew.jsonc` = file cấu hình dạng JSON cho phép ghi chú (c).*

**Lưu ý quan trọng:** CrewAI >= 1.0 yêu cầu **Python 3.10 – 3.13** — tức là phiên bản Python cũ hơn sẽ không cài được.

> 📄 **Code ví dụ:** [`examples/05-cap-nhat-10-2026-crewai-v1-x-phien.sh`](examples/05-cap-nhat-10-2026-crewai-v1-x-phien.sh)

Ref: https://docs.crewai.com/

> **Tóm gọn 1 câu:** CrewAI đã lên 1.x với structured output, hooks và CLI cấu hình qua crew.jsonc — nhưng nhớ nó đòi Python 3.10–3.13.

*Bài viết thuộc [AI Coding Skills Framework](../..) — nhánh Tools — crewai*