# 📈 Harness 13. Trajectory & Observability

> ## 📑 Mục Lục
>
> - [Opening Story](#opening-story)
> - [Vì Sao Trajectory Là Bắt Buộc?](#vì-sao-trajectory-là-bắt-buộc)
> - [Overview](#overview)
> - [Mục Lục Chi Tiết](#mục-lục-chi-tiết)
> - [1. Contract TrajectoryEvent](#1-contract-trajectoryevent)
>   - [1.1 Schema Cốt Lõi](#11-schema-cốt-lõi)
>   - [1.2 Danh Mục Event Kind](#12-danh-mục-event-kind)
>   - [1.3 Validate & Phiên Bản Hoá](#13-validate--phiên-bản-hoá)
> - [2. Vòng Đời Session Event Stream](#2-vòng-đời-session-event-stream)
>   - [2.1 Hình Dạng Một Run](#21-hình-dạng-một-run)
>   - [2.2 Đường Ghi — Các Tầng Bền Vững](#22-đường-ghi--các-tầng-bền-vững)
>   - [2.3 Đường Đọc & Tail Trực Tiếp](#23-đường-đọc--tail-trực-tiếp)
> - [3. Fork, Replay, Resume](#3-fork-replay-resume)
>   - [3.1 Ngữ Nghĩa Từng Thao Tác](#31-ngữ-nghĩa-từng-thao-tác)
>   - [3.2 Implementation](#32-implementation)
>   - [3.3 Độ Trung Thực Replay & Idempotency](#33-độ-trung-thực-replay--idempotency)
> - [4. Join Key Xuyên Module](#4-join-key-xuyên-module)
>   - [4.1 Bảng Join](#41-bảng-join)
>   - [4.2 Năm Câu Hỏi Một Query Trả Lời](#42-năm-câu-hỏi-một-query-trả-lời)
>   - [4.3 Phát Hiện Event Mồ Côi](#43-phát-hiện-event-mồ-côi)
> - [5. Retention, Redaction & GDPR](#5-retention-redaction--gdpr)
>   - [5.1 Các Tầng Hot / Warm / Cold](#51-các-tầng-hot--warm--cold)
>   - [5.2 Redaction Lúc Emit](#52-redaction-lúc-emit)
>   - [5.3 Cô Lập Tenant & Receipt Xoá](#53-cô-lập-tenant--receipt-xoá)
> - [6. Metrics Có Sẵn Miễn Phí](#6-metrics-có-sẵn-miễn-phí)
>   - [6.1 Catalog Query](#61-catalog-query)
>   - [6.2 Quy Kết Chi Phí](#62-quy-kết-chi-phí)
> - [7. Quy Trình Debug](#7-quy-trình-debug)
>   - [7.1 Năm Câu Hỏi Debug](#71-năm-câu-hỏi-debug)
>   - [7.2 So Sánh Hai Run](#72-so-sánh-hai-run)
>   - [7.3 Chiến Lược Sampling](#73-chiến-lược-sampling)
> - [8. Implementation TypeScript](#8-implementation-typescript)
>   - [8.1 TrajectoryStore](#81-trajectorystore)
>   - [8.2 Projector Tiến Độ Trực Tiếp](#82-projector-tiến-độ-trực-tiếp)
>   - [8.3 Debug Logger Adapter](#83-debug-logger-adapter)
> - [9. Kiểm Thử Trajectory](#9-kiểm-thử-trajectory)
>   - [9.1 Contract Test](#91-contract-test)
>   - [9.2 Bộ Test Replay](#92-bộ-test-replay)
> - [10. Case Study Thực Tế](#10-case-study-thực-tế)
>   - [10.1 Harness SWE-bench — Trajectory Có Cấu Trúc](#101-harness-swe-bench--trajectory-có-cấu-trúc)
>   - [10.2 LangSmith / Langfuse — Trace Là Sản Phẩm](#102-langsmith--langfuse--trace-là-sản-phẩm)
>   - [10.3 OpenTelemetry GenAI Conventions](#103-opentelemetry-genai-conventions)
>   - [10.4 OpenHands — Runtime Event Stream](#104-openhands--runtime-event-stream)
>   - [10.5 Claude Code — Session Replay Cho Support](#105-claude-code--session-replay-cho-support)
> - [11. TypeScript Interfaces Cho Observability](#11-typescript-interfaces-cho-observability)
> - [12. Nguyên Tắc Thiết Kế Cho Observability](#12-nguyên-tắc-thiết-kế-cho-observability)
>   - [12.1 SOLID cho hệ trace](#121-solid-cho-hệ-trace)
>   - [12.2 Sáu nguyên tắc thiết kế](#122-sáu-nguyên-tắc-thiết-kế)
> - [13. Best Practices](#13-best-practices)
>   - [13.1 NÊN ✅](#131-nên-)
>   - [13.2 KHÔNG NÊN ❌](#132-không-nên-)
> - [14. Anti-Patterns & Cách Khắc Phục](#14-anti-patterns--cách-khắc-phục)
> - [15. Production Checklist](#15-production-checklist)
> - [16. Xu Hướng Tương Lai](#16-xu-hướng-tương-lai)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)
>
> **Module cross-cutting.** Trajectory là cột sống của toàn bộ harness. Mọi stage
> đều emit vào đó; mọi buổi debug đều đọc từ đó. Module này là bản đồ;
> `03-update-memory-store/trajectory-fork-replay.md` giữ implementation engine.

---

### Opening Story

Hãy tưởng tượng sáng thứ Hai bạn nhận ticket: *"Agent xoá mất `src/auth/middleware.ts`, user phát hiện sau 40 phút. Vì sao vậy?"*

Nếu không có trajectory, coi như bạn đang mò mẫm trong bóng tối. Trong tay chỉ có đoạn chat của model (toàn lời nó *nói*, chứ không phải việc nó *làm*), thêm vài dòng log CI rời rạc, cộng với cảm giác mơ hồ kiểu "hình như nó đang refactor auth". Bạn chịu chết, không chỉ ra được lệnh xoá nằm ở lượt nào, ngay trước đó tool trả về cái gì, lúc ấy file có thật sự nằm trên nhánh hiện tại không, hay trong đầu agent đang nghĩ gì. Cuối cùng đành viết post-mortem mà thực ra là... đoán mò.

Có trajectory, cùng câu hỏi đó mất mười một giây và một query:

> 📄 **Code ví dụ:** [`examples/01-opening-story.sql`](examples/01-opening-story.sql)

**Và cái hay là các câu hỏi tiếp theo tự trả lời lẫn nhau.** Tại sao nó lại xoá? Nhìn `seq 29: prompt` là thấy ngay — mô hình thấy mấy export không ai dùng nên chọn cách xoá thay vì để lại code chết. Có cứu được không? `seq 33` có ghi `git worktree`, nên cứu được, bản patch cuối nằm ở `seq 51`. Chuyện này có đáng phải qua cổng duyệt không? Blast radius chỉ là một file — dưới ngưỡng `write` — nhưng khổ nỗi file đó được **3 file khác import mà agent chưa từng mở ra đọc**. Thế là từ một câu hỏi kỹ thuật, ta có luôn câu trả lời cho chính sách.

**Nói ngắn gọn: trajectory giúp bạn thoát khỏi cảnh "nó hỏng rồi", để nói được "chính xác chuyện gì đã xảy ra, vì sao, và giờ mình nên sửa chỗ nào".**

### Vì Sao Trajectory Là Bắt Buộc?

> *"Một hệ agent không có trajectory log là hệ mà mọi incident đều không tái hiện
> được, mọi khoản chi phí đều không quy được nguồn, và mọi hồi quy đều vô hình."*

#### Bốn năng lực sụp đổ khi thiếu nó

| Năng lực | Không có trajectory | Có trajectory |
|-----------|---------------------|---------------|
| **Debug** | Đoán từ chat transcript | `SELECT` đúng lượt cần xem |
| **Eval** (→ 11) | Chỉ output cuối; không thấy hiệu quả từng step | Step precision, recovery rate, phát hiện lặp |
| **Chi phí** | Hoá đơn ÷ số run; không phân bổ được | `GROUP BY task_id` kèm tokens + model tier |
| **Audit** (→ 15) | "Ai duyệt deploy?" → cuộn lại Slack | Một bản ghi bất biến, nối bằng hash |

Chuyện tiền nong rất đáng để kể kỹ một chút. Nếu mỗi step không ghi lại tokens và model tier đã dùng, bạn sẽ bó tay trước câu hỏi *"vì sao tháng trước hoá đơn tăng gấp ba?"* — chỉ biết là nó tăng, thế thôi. Còn khi đã có trajectory, bạn chỉ cần chạy `SELECT SUM(tokens) WHERE model='frontier' GROUP BY session`, và đáp án thường rất đời thường: "do vòng retry ở 3% số run" hoặc "do compaction ngừng chạy" — cả hai đều sửa gọn trong một buổi chiều.

#### Triết lý cốt lõi

```
Trajectory    = bằng chứng bền vững duy nhất về việc agent đã thực sự làm gì
Observability = kỷ luật truy vấn bằng chứng đó trước khi hình thành ý kiến
```

## Overview

> **📌 Khái Niệm Cốt Lõi**
>
> - **Khái niệm:** Trajectory là **event log chỉ-append** của một run: mọi prompt, tool call, tool result, plan revision, eval verdict, memory write, approval và compaction — mỗi cái đều có timestamp, actor và join key. **Observability** là thực hành truy vấn log đó để debug, replay, quy chi phí và cải tiến hệ thống.
> - **So sánh:** Như hộp đen máy bay. Chuyến hạ cánh bình thường không ai nhìn; một sự cố thì điều tra toàn bộ từ hộp đen, và chính dữ liệu đó phát lại đúng lộ trình.
> - **Vì sao quan trọng:** Không có nó, bạn không trả lời được "sao nó sửa nhầm file?", "chunk retrieval nào đầu độc câu trả lời?", hay "run này tốn bao nhiêu?". Có nó, debug là một query, eval là SQL, và incident tái hiện được.

**Trajectory & Observability** biến một run agent đang mờ mịt như "nồi lẩu thập cẩm" thành thứ bạn có thể truy vấn, phát lại và audit đàng hoàng. Nói dân dã: đó là khác biệt giữa một agent bạn *thật sự vận hành* và một agent bạn chỉ biết *cầu may*.

```
┌────────────────────── HARNESS EMITTERS ──────────────────────┐
│                                                              │
│  01 retrieve ┐  02 context ┐  04 plan  ┐  06 tools ┐  11 eval│
│  03 memory  ─┤  05 prompt ─┤  07 flow ─┤  09 agents┤  14 compact
│  12 sandbox ─┤  13 self   ─┘  15 gate  ─┘  10 auto ─┘        │
└──────────────────────────────┬───────────────────────────────┘
                               │  append(event)  ← một shape, một sink
                               ▼
                 ┌─────────────────────────────┐
                 │   TrajectoryStore           │
                 │   ses_44a.jsonl (append)    │
                 │   ┌───────────────────────┐ │
                 │   │ evt_01  prompt        │ │
                 │   │ evt_02  plan          │ │
                 │   │ evt_03  tool_call     │ │  ← seq, ts, taskId,
                 │   │ evt_04  tool_result   │ │    tokens, latency,
                 │   │ evt_05  eval          │ │    payload đã redact
                 │   │ evt_06  memory_write  │ │
                 │   └───────────────────────┘ │
                 └──────┬───────────────┬───────┘
                        │               │
          ┌─────────────┴──┐      ┌─────┴──────────────┐
          │ Replay / Fork /│      │ SQL / dashboard    │
          │ Resume (→ 3)   │      │ metrics (→ 6)      │
          └────────────────┘      └────────────────────┘
```

**Hai nguyên tắc vàng làm nên tất cả:** (1) *chỉ-append* — event đã ghi thì không bao giờ sửa, nên lịch sử luôn đáng tin như sổ cái; (2) *mọi event đều mang `sessionId` + `parentTaskId`* — nhờ đó không event nào bị mồ côi, câu hỏi nào cũng có đường để lần theo.

## Mục Lục Chi Tiết

| # | Chủ đề | Mô tả |
|---|-------|-------|
| 1 | [Contract TrajectoryEvent](#1-contract-trajectoryevent) | Schema duy nhất mọi module emit |
| 2 | [Session Event Stream](#2-vòng-đời-session-event-stream) | Vòng đời, bền vững, tailing |
| 3 | [Fork / Replay / Resume](#3-fork-replay-resume) | Tất định, A/B, khôi phục crash |
| 4 | [Join xuyên module](#4-join-key-xuyên-module) | Task ↔ Context ↔ Eval ↔ Gate |
| 5 | [Retention & Redaction](#5-retention-redaction--gdpr) | Hot/warm/cold, receipt GDPR |
| 6 | [Metrics miễn phí](#6-metrics-có-sẵn-miễn-phí) | Catalog query |
| 7 | [Debug](#7-quy-trình-debug) | Năm câu hỏi, diff run, sampling |
| 8 | [Implementation](#8-implementation-typescript) | Store, projector, logger |
| 9 | [Kiểm thử](#9-kiểm-thử-trajectory) | Contract + replay test |
| 10 | [Case study](#10-case-study-thực-tế) | SWE-bench, LangSmith, OTel, OpenHands, Claude Code |
| 11 | [TypeScript Interfaces](#11-typescript-interfaces-cho-observability) | Toàn bộ bề mặt kiểu |
| 12 | [Nguyên tắc thiết kế](#12-nguyên-tắc-thiết-kế-cho-observability) | SOLID cho trace |
| 13 | [Best practices](#13-best-practices) | NÊN / KHÔNG NÊN |
| 14 | [Anti-patterns](#14-anti-patterns--cách-khắc-phục) | Lỗi thường gặp |
| 15 | [Production checklist](#15-production-checklist) | Cổng ship |
| 16 | [Xu hướng tương lai](#16-xu-hướng-tương-lai) | 2026-2028 |

---

## 1. Contract TrajectoryEvent

### 1.1 Schema Cốt Lõi

Một shape duy nhất, mọi module cùng emit, mọi công cụ cùng đọc. Đây là món "hợp đồng" quan trọng nhất trong cả tầng observability — cả nhà dùng chung một khuôn thì mới nói chuyện được với nhau.

> 📄 **Code ví dụ:** [`examples/02-1-1-schema-cot-loi.ts`](examples/02-1-1-schema-cot-loi.ts)

**Mỗi trường đều có việc để làm:**

| Trường | Mở khoá điều gì mà không có trường khác làm được |
|--------|--------------------------------------------------|
| `id` (ULID) | Thứ tự chèn sắp xếp được không phụ thuộc đồng hồ; dedupe giữa các store |
| `seq` | Phát hiện lỗ hổng — thiếu `seq` nghĩa là mất một lần ghi, không phải mất một suy nghĩ |
| `parentTaskId` | Đường join tới plan (→ 08); thiếu nó thì mọi event đều mồ côi |
| `actor` | Phân biệt "mô hình làm cái này" với "con người làm cái này" — cốt lõi của audit |
| `model` + `costUsd` | Chi phí từng step; cách duy nhất tìm ra run đã nuốt ngân sách |
| `fingerprint` | Phát hiện một prompt đã lệch dưới tay bạn; làm compaction truy vết được |
| `error.retryable` | Cho phép replay và eval suy luận về *lớp* lỗi, không chỉ về text |

### 1.2 Danh Mục Event Kind

| Kind | Do ai emit | Payload chính | Ai tiêu thụ |
|------|-----------|---------------|-------------|
| `session_start` | supervisor | user request, tenant, config hash | replay, cost |
| `context_assembly` | 02 | id + điểm của chunk đã lấy, số token | attribution (→ 01) |
| `prompt` | 05 | fingerprint, tier, template id, token ước tính | replay, thống kê cache (→ 06) |
| `plan` / `plan_revision` | 04 | task graph, lý do sửa kế hoạch | phân tích recovery |
| `tool_call` | 06 | tool, argvHash, policyHash, tier | metric precision |
| `tool_result` | 06/12 | exit code, số byte, truncated, redactions | phân tích lỗi |
| `sandbox` | 12 | runtime, image digest, allowlist | audit bảo mật (→ 12) |
| `memory_read` / `memory_write` | 03 | fact id, scope, hit/miss | phân tích grounding (→ 03) |
| `approval_request` / `approval_verdict` | 15 | tier, approver, diffHash, expiresAt | audit (→ 15) |
| `compaction` | 14 | keptIds, evictedIds, ratio, hash resume | sức khoẻ context (→ 14) |
| `eval` | 11 | judge, score, rubric, humanSampleId | phát hiện hồi quy (→ 11) |
| `error` | bất kỳ | code, retryable, tham chiếu stack | SLO, cảnh báo |

**Nguyên tắc nằm lòng:** nếu một module tạo ra sự thật nào mà nay mai có người muốn lần theo, nó phải emit một event. Một sự thật chỉ nằm trong memory mà không lên log thì lúc cần debug, bạn chịu thua.

### 1.3 Validate & Phiên Bản Hoá

> 📄 **Code ví dụ:** [`examples/03-1-3-validate-phien-ban-hoa.ts`](examples/03-1-3-validate-phien-ban-hoa.ts)

**Hãy version cả schema, đừng version từng trường riêng lẻ.** Thêm `v: 2` và giữ reader đọc được cả bản cũ lẫn mới. Một trajectory viết từ sáu tháng trước vẫn phải đọc được — giữ được lịch sử đọc được chính là lý do ta lưu nó. Đổi tên trường trong im lặng chẳng khác nào xé mất trang duy nhất ghi lại sự thật.

---

## 2. Vòng Đời Session Event Stream

### 2.1 Hình Dạng Một Run

```
session_start
  → context_assembly   (lấy 12 chunk, 8.1k token)
  → prompt             (fingerprint a3f9, tier=standard)
  → plan               (5 task: t1..t5, t2,t3 song song)
  → tool_call/tool_result × N   (đã sandbox; mỗi lời gọi emit cả hai)
  → compaction         (dùng 74% → giữ 41, bỏ 63)
  → eval               (judge score 0.82)
  → memory_write       (3 fact được lưu)
  → session_end        (task xong: 5/5, cost $0.41, 214s)
```

Mấy chỗ xen kẽ này rất đáng để ý, kiểu như "cặp đôi" lúc nào cũng phải đi cùng nhau:

- **`tool_call` rồi `tool_result`, lúc nào cũng đi cặp.** Một `tool_call` mà không thấy `tool_result` đâu chính là một step bị treo — và query tìm ra chúng cũng là "máy báo treo" của bạn (→ `09` §16.1).
- **`plan_revision` nằm xen giữa các tool call đã sinh ra nó.** Muốn kể lại câu chuyện cho ra đầu đuôi thì nguyên nhân và hệ quả phải nằm cạnh nhau.
- **`compaction` nằm giữa prompt nó rút gọn và prompt kế tiếp.** Nếu không, bạn sẽ không bao giờ giải thích nổi vì sao mô hình tự dưng "quên" mất thứ gì.

### 2.2 Đường Ghi — Các Tầng Bền Vững

Không phải event nào cũng đáng để `fsync` ngay. Hãy xếp hạng theo kiểu "mất nó thì đau tới đâu":

| Event | Bền vững | Lý do |
|-------|----------|-------|
| `approval_verdict` | **fsync** | Bản ghi pháp lý; mất là mất chuỗi audit |
| `memory_write` | **fsync** | Mất fact bền = bug đúng-sai lặng lẽ |
| `session_start` / `session_end` | **fsync** | Neo của báo cáo cost và thời lượng |
| `eval` | **fsync** | Phát hiện hồi quy phụ thuộc tính đầy đủ |
| `tool_call` / `tool_result` | flush ≤100 ms | Cần để debug, chấp nhận mất 100 ms cuối |
| `prompt` / `context_assembly` | buffered | Dựng lại được từ chính run |

> 📄 **Code ví dụ:** [`examples/04-2-2-uong-ghi-cac-tang-ben-vung.sh`](examples/04-2-2-uong-ghi-cac-tang-ben-vung.sh)

**Sao lại là JSONL mà không phải bảng SQL?** Vì ghi kiểu nối đuôi thì khỏi cần khoá trong trường hợp thường, `grep` phát ăn ngay, mang đi đâu cũng tiện, replay cũng dễ. Còn index là chuyện *tính sau*; cần phân tích thì nạp vào DuckDB/SQLite. Nếu ngay từ đầu đã lưu dạng bảng, mỗi event thành một giao dịch nằm ngay trên đường chạy nóng — bạn phải trả "thuế độ trễ" cho vòng lặp agent, chỉ để đổi lấy một câu query mỗi tuần mới chạy một lần.

### 2.3 Đường Đọc & Tail Trực Tiếp

> 📄 **Code ví dụ:** [`examples/05-2-3-uong-oc-tail-truc-tiep.sh`](examples/05-2-3-uong-oc-tail-truc-tiep.sh)

Nạp vào DuckDB cho mọi thứ nặng hơn:

> 📄 **Code ví dụ:** [`examples/06-2-3-uong-oc-tail-truc-tiep.sql`](examples/06-2-3-uong-oc-tail-truc-tiep.sql)

---

## 3. Fork, Replay, Resume

### 3.1 Ngữ Nghĩa Từng Thao Tác

| Thao tác | Làm gì | Khi nào cần | Yêu cầu trung thực |
|----------|--------|-------------|---------------------|
| **Replay** | Chạy lại event `0..N` với cùng input; assert output khớp | Tái hiện chính xác một bug report | Step tất định phải giống byte |
| **Fork** | Clone session tại event `K`, đi tiếp với prompt/model/policy khác | "Nếu chỗ này dùng model lớn thì sao?" | Tiền tố giống nhau; hậu tố có thể phân kỳ tuỳ ý |
| **Resume** | Nạp checkpoint cuối + phần event ghi sau crash | Workflow bền vững (→ 07 §13) | Không được chạy lại side effect đã commit |

Đây là ba món khác nhau với ba lời hứa khác nhau. Nhầm lẫn chúng là cách nhanh nhất để biến một buổi "replay" vô hại thành cú gửi lại email production cho khách hàng.

### 3.2 Implementation

<details>
<summary>TypeScript Code — fork / replay / resume (Click để mở rộng/thu gọn)</summary>

> 📄 **Code ví dụ:** [`examples/07-3-2-implementation.ts`](examples/07-3-2-implementation.ts)

</details>

### 3.3 Độ Trung Thực Replay & Idempotency

**Không phải step nào cũng tất định.** Phân loại từng kind trước khi hứa replay:

| Kind | Tất định? | Hợp đồng trung thực |
|------|----------|---------------------|
| `memory_read` | ✅ (với cùng trạng thái index) | giống byte |
| `tool_call` tới lệnh trong sandbox | ⚠️ (phụ thuộc filesystem/thời gian) | cùng exit code; stdout có thể khác ở timestamp |
| `tool_call` tới API sống | ❌ | ghi lại response; replay gọi lại và so hình dạng |
| `prompt` | ❌ (có sampling) | cùng `fingerprint` (template + context hash), không phải cùng token |
| `eval` (LLM judge) | ❌ | cùng rubric + cùng input; kỳ vọng score trong ±0.1 |

**Quy tắc chống thảm hoạ:** replay không bao giờ được kích hoạt lại một side effect không thể hoàn tác. `idempotencyKeyOf()` = `(taskId, tool, argvHash)`; khi replay, key nào đã xong thì bỏ qua và lấy lại `tool_result` đã ghi. Đây cũng chính là lý do `07-workflow/README.md` §13.3 đòi mọi step phải có idempotency key — replay không phải món "có thì vui", nó là *lý do* những chiếc key đó tồn tại.

`fingerprint` đáng được chú ý: nó hash `(template, id chunk đã lấy, id memory, hash
policy)`. Nếu một lần replay cho fingerprint khác, *input* đã đổi — và dù có so sánh
output bao nhiêu cũng không cho bạn biết vì sao. Hãy kiểm tra fingerprint trước.

---

## 4. Join Key Xuyên Module

### 4.1 Bảng Join

| Câu hỏi | Đường join |
|----------|-----------|
| Tool call này thuộc task nào? | `tool_call.parentTaskId → TaskNode.id` (→ 08) |
| Chunk retrieval nào nuôi câu trả lời này? | `prompt.payload.chunkIds[] → chunk.id` (→ 01) |
| Compaction giữ gì, bỏ gì? | `compaction.payload.{keptIds, evictedIds, ratio}` (→ 14) |
| Ai duyệt lệnh deploy này? | `approval_verdict.{approver, diffHash, expiresAt}` (→ 15) |
| Judge có đồng ý với con người không? | `eval.{judge, score, humanSampleId}` (→ 11 §15.4) |
| Step này có được sandbox đúng không? | `sandbox.policyHash` ↔ `tool_call.policyHash` (→ 12) |

Mỗi dòng trên là một câu hỏi mà kiểu gì người dùng cũng sẽ hỏi bạn trong tuần đầu sau khi ship. Mỗi dòng là một query SQL. Và mỗi dòng đều bất khả thi nếu hôm đó bạn quên gắn key.

### 4.2 Năm Câu Hỏi Một Query Trả Lời

> 📄 **Code ví dụ:** [`examples/08-4-2-nam-cau-hoi-mot-query-tra.sql`](examples/08-4-2-nam-cau-hoi-mot-query-tra.sql)

Join key biến "mô hình trả lời sai" thành "nó lấy 12 chunk, dùng 4, và 3 chunk điểm
cao nhất đã cũ" — một kết luận có chủ sở hữu và có cách sửa.

### 4.3 Phát Hiện Event Mồ Côi

Một event không có `parentTaskId` (hoặc task không tồn tại) là lỗi đấu nối. Chạy
liên tục:

> 📄 **Code ví dụ:** [`examples/09-4-3-phat-hien-event-mo-coi.sql`](examples/09-4-3-phat-hien-event-mo-coi.sql)

Khác 0 là phải page. Event mồ côi là cách một harness kết thúc với một dashboard
âm thầm thiếu 12% chi phí trong tám tháng.

---

## 5. Retention, Redaction & GDPR

### 5.1 Các Tầng Hot / Warm / Cold

| Tầng | Tuổi | Nội dung | Lưu trữ | Mẫu truy vấn |
|------|------|----------|---------|--------------|
| **Hot** | 0–7 ngày | payload đầy đủ | SSD nhanh / trong bộ nhớ | tail trực tiếp, debug trực tiếp |
| **Warm** | 7–90 ngày | payload >4KB thay bằng `ref`; phần còn lại inline | object storage | review incident |
| **Cold** | 90 ngày – 1 năm | chỉ aggregate (`steps`, `tokens`, `costUsd`, `latencyMs`, verdict) | dạng cột | xu hướng, SLO, báo cáo cost |
| **Purged** | theo TTL của tenant | đã xoá | — | xoá theo GDPR |

**Quy tắc 4KB:** ở tầng warm, payload vượt 4KB bị thay bằng một con trỏ. Tool output
lớn chiếm phần lớn dung lượng byte và ít giá trị nhất sáu tuần sau; một `ref` cộng
`stdoutHash` giữ được khả năng audit mà không tốn hoá đơn lưu trữ.

### 5.2 Redaction Lúc Emit

Redaction phải làm **ngay lúc ghi**, đừng để tới lúc đọc. Redact lúc đọc là thua chắc, vì kiểu gì cũng có query ad-hoc chọc thẳng vào bảng thô — mà bảng thô thì lúc nào cũng bị người ta lôi ra soi.

> 📄 **Code ví dụ:** [`examples/10-5-2-redaction-luc-emit.ts`](examples/10-5-2-redaction-luc-emit.ts)

Lưu `redactions` thành một trường của event. Rồi:

> 📄 **Code ví dụ:** [`examples/11-5-2-redaction-luc-emit.sql`](examples/11-5-2-redaction-luc-emit.sql)

### 5.3 Cô Lập Tenant & Receipt Xoá

- **`tenantId` trên mọi event, ép lúc ghi.** Thiếu `tenantId` là từ chối ghi, không phải cảnh báo.
- **Row-level security hoặc bucket riêng cho từng tenant.** Rò rỉ chéo tenant trong trajectory store là một sự cố dữ liệu theo nghĩa đen.
- **Xoá theo GDPR** gỡ: event trajectory, aggregate cold, báo cáo dẫn xuất, và mọi projection đã cache — rồi phát một receipt:

> 📄 **Code ví dụ:** [`examples/12-5-3-co-lap-tenant-receipt-xoa.json`](examples/12-5-3-co-lap-tenant-receipt-xoa.json)

Bản receipt cũng được lưu bất biến. "Chúng tôi đã xoá nó" phải kiểm chứng được mà
không cần tin vào chính hệ thống đã xoá.

---

## 6. Metrics Có Sẵn Miễn Phí

### 6.1 Catalog Query

Mọi metric đều là một query trên cùng một bảng. Đây chính là phần thưởng xứng đáng cho công sức thiết kế schema tử tế từ đầu.

> 📄 **Code ví dụ:** [`examples/13-6-1-catalog-query.sql`](examples/13-6-1-catalog-query.sql)

### 6.2 Quy Kết Chi Phí

> 📄 **Code ví dụ:** [`examples/14-6-2-quy-ket-chi-phi.sql`](examples/14-6-2-quy-ket-chi-phi.sql)

Phát hiện phổ biến nhất: **chi phí không nằm ở prompt, mà ở vòng retry và các step
dùng frontier tier mà không cần thiết.** Một dashboard cost dựa trên query này
thường tìm ra 15–30% tiết kiệm trong tuần đầu mà không đổi chất lượng.

---

## 7. Quy Trình Debug

### 7.1 Năm Câu Hỏi Debug

| # | Câu hỏi | Query |
|---|----------|-------|
| 1 | Agent **làm** gì? | `SELECT kind, payload ORDER BY seq` |
| 2 | Nó **thấy** gì? | `context_assembly` + `prompt.payload` |
| 3 | Nó **tin** gì? | `plan` + `plan_revision.reason` |
| 4 | Nó **hỏng** ở đâu? | `tool_result.exit_code != 0` + `error` |
| 5 | **Judge** nói gì? | `eval.payload` |

Trả lời câu 2 và 3 trước câu 4 — đó là kỷ luật. Rất nhiều ticket kiểu "mô hình làm cái gì ngớ ngẩn quá" thực ra lại hỏng ở câu 2: mô hình bị thiếu thông tin đầu vào, và câu 3 chỉ đang phản ánh trung thực cái thiếu đó mà thôi.

### 7.2 So Sánh Hai Run

> 📄 **Code ví dụ:** [`examples/15-7-2-so-sanh-hai-run.ts`](examples/15-7-2-so-sanh-hai-run.ts)

Dùng cho A/B test prompt, nâng cấp model, và các report kiểu "hôm qua còn chạy". Dòng
`~` đầu tiên gần như luôn là dòng thú vị.

### 7.3 Chiến Lược Sampling

Full fidelity cho tất cả là không t afford được và cũng không cần thiết.

| Lớp tín hiệu | Sampling | Lý do |
|---------------|-----------|-------|
| Lỗi, approval, prod-auth | 100% | Lượng ít, giá trị cao |
| `eval.score < 0.6` | 100% | Thất bại chính là dữ liệu huấn luyện |
| Tool `read` thành công | 5% | Lượng lớn, thông tin ít |
| Ghi thành công | 20% | Giá trị trung bình, cần độ phủ |
| Prompt happy-path ở frontier | 1% | Kiểm soát chi phí |

Luôn giữ **counter ở 100%** kể cả khi bỏ payload. Log đã sample nhưng aggregate đầy
đủ trả lời được câu hỏi SLO; log đã sample mà không có aggregate thì không trả lời
được gì.

---

## 8. Implementation TypeScript

### 8.1 TrajectoryStore

<details>
<summary>TypeScript Code — store chỉ-append với các tầng bền vững (Click để mở rộng/thu gọn)</summary>

> 📄 **Code ví dụ:** [`examples/16-8-1-trajectorystore.ts`](examples/16-8-1-trajectorystore.ts)

</details>

### 8.2 Projector Tiến Độ Trực Tiếp

> 📄 **Code ví dụ:** [`examples/17-8-2-projector-tien-o-truc-tiep.ts`](examples/17-8-2-projector-tien-o-truc-tiep.ts)

### 8.3 Debug Logger Adapter

> 📄 **Code ví dụ:** [`examples/18-8-3-debug-logger-adapter.ts`](examples/18-8-3-debug-logger-adapter.ts)

---

## 9. Kiểm Thử Trajectory

### 9.1 Contract Test

Chạy trong CI. Đây là bắt lớp bug khi một module mới emit một event phá vỡ mọi query
phía dưới.

> 📄 **Code ví dụ:** [`examples/19-9-1-contract-test.ts`](examples/19-9-1-contract-test.ts)

Cũng assert: mọi `tool_call` có `tool_result` tương ứng; mọi `tool_result.parentTaskId`
tồn tại trong plan; không payload nào chứa pattern secret.

### 9.2 Bộ Test Replay

> 📄 **Code ví dụ:** [`examples/20-9-2-bo-test-replay.ts`](examples/20-9-2-bo-test-replay.ts)

**Lịch:** mỗi đêm replay 20 trajectory production hàng đầu với một model đã ghim. Drift
ở step tất định là fail cứng. Drift ở step LLM vượt ±0.1 score là tín hiệu cần điều
tra — đó là cách bạn phát hiện nhà cung cấp đổi hành vi trước khi người dùng của bạn.

---

## 10. Case Study Thực Tế

### 10.1 Harness SWE-bench — Trajectory Có Cấu Trúc

Đánh giá SWE-bench ghi lại, cho mỗi instance: trajectory của mô hình (patch, kết quả
test), trạng thái resolve, và chi phí token. Vì trajectory có cấu trúc giống nhau cho
mọi bài nộp, nó đóng vai trò kép: (a) đầu vào đánh giá (→ 11), (b) bề mặt
contamination (→ 11 §15.2), và (c) artifact debug khi một bài từng pass bắt đầu fail.

Bài học thiết kế rút ra: **hãy biến trajectory thành món chính của buổi đánh giá, đừng chỉ nộp output cuối.** Eval chỉ nhìn output cuối thì chỉ biết *nó fail*. Eval nhìn cả trajectory mới biết nó fail vì không tìm ra bug (lỗi retrieval), vì viết patch sai (lỗi suy luận), hay vì patch đúng mà hạ tầng test chập chờn. Ba kiểu hỏng này cần ba toa thuốc hoàn toàn khác nhau.

### 10.2 LangSmith / Langfuse — Trace Là Sản Phẩm

Các nhà cung cấp observability biến trajectory thành sản phẩm: waterfall trace, prompt
versioning, curation dataset từ trace, và chạy eval trên trace đã lưu. Insight khái
quát hoá: **trace không chỉ là log, chúng là nguyên liệu thô cho dataset đánh giá.**
Mỗi run thất bại là một case eval đã curate sẵn, đúng hình dạng, với đúng context
thật đã sinh ra nó.

Cách thất bại cần tránh: xây một trace UI mà không ai truy vấn. Phần thưởng nằm ở
SQL, không nằm ở waterfall. Các đội đầu tư vào *query* trên một store JSONL ngu ngốc
kiểu thu được nhiều giá trị hơn các đội có dashboard đẹp nhưng không cách nào đặt
câu hỏi cho nó.

### 10.3 OpenTelemetry GenAI Conventions

OpenTelemetry GenAI semantic conventions chuẩn hoá tên span và thuộc tính cho các
lời gọi LLM: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`,
`gen_ai.usage.output_tokens`. Conventions dành riêng cho agent bổ sung span cho tool
call, retrieval, và từng bước của chain.

Vì sao quan trọng: nếu bạn emit thuộc tính `gen_ai.*`, trace của bạn sáng lên trong
đúng backend observability mà công ty đã trả tiền, và dashboard cost/latency đến kèm
miễn phí. Cái giá của việc không chấp nhận conventions là phải tự xây dashboard mãi
mãi.

> 📄 **Code ví dụ:** [`examples/21-10-3-opentelemetry-genai-conventions.ts`](examples/21-10-3-opentelemetry-genai-conventions.ts)

### 10.4 OpenHands — Runtime Event Stream

OpenHands làm cho event stream trở thành interface của runtime: agent phát ra các cặp
`Action`/`Observation`, và mọi action được ghi lại *khi nó thực thi* chứ không phải
sau đó. Hệ quả thiết kế:

1. **Ghi log không phải side effect — nó là vòng lặp.** Không thể "quên log" vì log *là* cách vòng lặp giao tiếp.
2. **Observation là event bậc nhất**, không phải giá trị trả về ngầm. Khác biệt này quan trọng: một tool result bị cắt là event có `truncated: true`, không phải một chuỗi bị cắt âm thầm.
3. **Replay gần như miễn phí** vì event stream chính là mô hình thực thi.

### 10.5 Claude Code — Session Replay Cho Support

Các coding agent dùng ở quy mô lớn dựa vào session replay cho bộ phận hỗ trợ: khi user
báo "nó đã đổi config của tôi", support đọc trajectory thay vì bắt user kể lại. Hai
thực hành đáng học:

1. **Transcript của chính user là UI chính.** Một trace hiển thị được, cuộn được, là
   một cơ chế tạo niềm tin — user tự thấy chuyện gì xảy ra mà không phải hỏi.
2. **Redact giá trị nhạy cảm diễn ra lúc emit.** Các file như `.env`, file khoá, và
   pattern credential được redact trong transcript user thấy, không chỉ trong log bạn
   lưu.

---

## 11. TypeScript Interfaces Cho Observability

> 📄 **Code ví dụ:** [`examples/22-11-typescript-interfaces-cho-observability.ts`](examples/22-11-typescript-interfaces-cho-observability.ts)

---

## 12. Nguyên Tắc Thiết Kế Cho Observability

### 12.1 SOLID cho hệ trace

| Nguyên tắc | Áp dụng |
|------------|---------|
| **S**ingle responsibility | `TrajectoryStore` ghi lại. Nó không diễn giải, không cảnh báo, không quyết định sampling. |
| **O**pen/closed | Event kind mới là *dữ liệu*, không phải code — thêm `delegation` không cần sửa store. |
| **L**iskov substitution | Mọi store (file, Postgres, OTel) thoả `TrajectoryStore`; engine không quan tâm. |
| **I**nterface segregation | UI sống cần `tail()`; debugger cần `load()`. Đừng bắt debugger phụ thuộc streaming. |
| **D**ependency inversion | Module phụ thuộc interface `EventSink`, nên test harness có thể capture trong bộ nhớ. |

### 12.2 Sáu nguyên tắc thiết kế

1. **Chỉ-append.** Event là sự thật; sự thật không bị sửa. Cách đính chính là event mới (`plan_revision`), không phải mutation.
2. **Mọi event đều quy được nguồn.** `actor` và `parentTaskId` là bắt buộc. Không mồ côi, không bao giờ.
3. **Redact lúc ghi.** Redact lúc đọc thì đã thua rồi.
4. **Telemetry không bao giờ làm hỏng task.** Lỗi append được đếm, không throw vào vòng lặp agent. Một agent ngừng hoạt động vì log hỏng còn tệ hơn một agent bị giám sát mù.
5. **Tất định trước, sample sau.** Full fidelity cho lỗi, approval và score thấp; chỉ sample happy path.
6. **Idempotency key là một phần của schema.** Không có chúng, replay là gánh nặng chứ không phải tính năng.

---

## 13. Best Practices

### 13.1 NÊN ✅

- Emit từ *mọi* module, kể cả những cái tưởng tượng là tầm thường (context assembly, compaction).
- `fsync` approval, memory write và biên session; phần còn lại buffer.
- Lưu `seq` liền mạch và cảnh báo khi có lỗ hổng — lỗ hổng nghĩa là mất bằng chứng.
- Xây attribution chi phí từ `model` + `tokens` từng step, không phải từ hoá đơn tổng.
- Biến mỗi run thất bại thành một case eval đã curate; nó đã đúng hình dạng sẵn.
- Replay 20 trajectory production hàng đầu mỗi đêm với model đã ghim.
- Emit thuộc tính `gen_ai.*` của OpenTelemetry để trace nằm trong backend sẵn có.

### 13.2 KHÔNG NÊN ❌

- ❌ Không log tool output đầy đủ kèm secret. Cap, redact, giữ một `ref`.
- ❌ Không dùng chat transcript làm trajectory — nó ghi lại điều mô hình *nói*, không phải điều nó *làm*.
- ❌ Không `UPDATE` event cũ để "sửa" nó. Hãy append một event đính chính.
- ❌ Không để exception telemetry lan vào vòng lặp agent.
- ❌ Không xây dashboard trước khi diễn đạt được câu hỏi bằng SQL.
- ❌ Không hứa replay giống byte cho step LLM. Hãy phân loại tất định theo từng event kind.
- ❌ Không lưu trajectory mà không có `tenantId` rồi coi việc lọc tenant là việc của query.

---

## 14. Anti-Patterns & Cách Khắc Phục

| Anti-pattern | Triệu chứng | Cách sửa |
|--------------|------------|---------|
| **Chat log ≠ trajectory** | Bạn thấy câu trả lời, không thấy hành động | Emit `tool_call`/`tool_result` cho mọi hành động |
| **Event mồ côi** | Dashboard thiếu cost 10% | Bắt buộc `parentTaskId`; validate trong CI |
| **Log tất cả ở full fidelity** | Hoá đơn lưu trữ đắt hơn hoá đơn suy luận | Tầng hot/warm/cold; quy tắc 4KB; sampling |
| **Redact lúc đọc** | Một query ad-hoc rò PII vào notebook | Redact lúc emit; audit warm store hàng quý |
| **Replay kích hoạt lại side effect** | Một lần replay gửi email cho khách | Idempotency key + thay bằng kết quả đã ghi (→ 07 §13.3) |
| **Log bất biến, nghĩa có thể đổi** | Đội "sửa" event tại chỗ, lịch sử mất | Chỉ-append + event `*_revision` |
| **Sample mà không có counter** | Metric mất ý nghĩa thống kê | Aggregate 100%, payload đã sample |
| **Không phát hiện lỗ hổng** | Mất một lần ghi, phát hiện lúc incident | `seq` liền mạch + assert trong CI + cảnh báo |
| **UI là nguồn sự thật** | Trạng thái tiến độ lệch với event log | UI là phép gấp trên event (`project()`) |

---

## 15. Production Checklist

- [ ] **Schema** — một shape `TrajectoryEvent`, validate bằng zod, có phiên bản, `seq` liền mạch
- [ ] **Quy kết** — `sessionId` + `parentTaskId` + `actor` + `tenantId` bắt buộc mọi event
- [ ] **Bền vững** — fsync approval/memory/eval/biên session; flush ≤100 ms phần còn lại
- [ ] **Redaction** — lúc emit; PII + pattern secret; lưu và audit số lần redact
- [ ] **Cap** — payload ≤64 KB, quá lớn → `ref`; stdout đã cap ở sandbox
- [ ] **Chi phí** — `model` + `tokens` + `costUsd` cấp step; attribution theo task và theo tenant chạy được
- [ ] **Retention** — hot 7 ngày / warm 90 ngày / cold 1 năm; quy tắc 4KB; tôn trọng TTL tenant
- [ ] **Cô lập** — RLS hoặc bucket riêng từng tenant; query chéo tenant trả về rỗng
- [ ] **GDPR** — đường xoá phủ event, aggregate, projection; receipt lưu bất biến
- [ ] **Fork/replay/resume** — cả ba đã hiện thực và có test; idempotency key trên mọi step
- [ ] **Phát hiện treo** — query tool_call không có tool_result đã nối vào cảnh báo
- [ ] **Sampling** — 100% cho lỗi/approval/score thấp; 5–20% cho happy path
- [ ] **Replay CI** — replay 20 trajectory hàng đầu mỗi đêm với model đã ghim
- [ ] **Chuẩn** — phát thuộc tính `gen_ai.*` của OTel

---

## 16. Xu Hướng Tương Lai

### 16.1 Agent-Native Tracing (2026-2028)

- **Eval nhận thức trajectory.** Rubric chấm *đường đi* — nó có kiểm tra test trước khi nói "thành công" không? — thay vì chấm câu trả lời cuối. Dữ liệu đã có sẵn; đây là bài toán query.
- **Phát hiện drift tự động.** Một bộ nhúng trajectory đánh dấu những run có cấu trúc khác dân số "tốt đã biết" trước khi con người kịp nhìn.
- **Quy kết nhân quả.** Với một kết quả xấu, xác định quyết định sớm nhất đã gây ra nó. Đây là vùng tiền tuyến: không phải "đã xảy ra gì" mà là "lượt nào tôi cần đổi".

### 16.2 Telemetry Bảo Mật Quyền Riêng Tư

- **Redaction tại thiết bị kèm aggregate differential privacy** cho metric bạn giữ toàn cục, trong khi payload vẫn nằm ở tenant.
- **Sink trace chạy trong confidential compute** để cả nhà cung cấp observability cũng không đọc được trajectory — cùng mẫu SEV-SNP/TDX như `12-sandbox-execution` §16.3.

### 16.3 Trajectory Tự Mô Tả

Event mang theo *lý do* ở dạng máy đọc được — không chỉ "tôi chạy `pytest`" mà là "tôi
chạy `pytest` vì lần trước fail ở `test_auth_refresh`" — làm post-mortem tự động trở nên
khả thi. Hãy kỳ vọng lý do `plan_revision` của chính mô hình trở thành một trường
bậc nhất thay vì nằm chôn trong văn xuôi.

### 16.4 Observability Như Một Primitive Bảo Mật

Trajectory là đầu vào của phát hiện bất thường cho prompt injection: một cụm
`path-escape` bất ngờ, egress tới host lạ, hoặc đợt redact tăng vọt ở một tenant đều
là mẫu phát hiện được. Hộp đen là cách bạn tìm ra chuyến bay đã bị điều khiển.

---

## Tài Liệu Tham Khảo

### Papers & Research

- **Event Sourcing** — Martin Fowler · https://martinfowler.com/eaaDev/EventSourcing.html
- **The Tail at Scale** — Dean & Barroso, CACM 2013 · https://cacm.acm.org/research/the-tail-at-scale/
- **DORA: Accelerate State of DevOps** — nghiên cứu về tần suất triển khai và tỉ lệ thất bại
- **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Jimenez et al., 2024 · https://arxiv.org/abs/2310.06770
- **A Survey on LLM-based Software Engineering Agents** · https://arxiv.org/abs/2402.06530

### Frameworks & Tools

1. **OpenTelemetry GenAI semantic conventions** — https://opentelemetry.io/docs/specs/semconv/gen-ai/
2. **LangSmith** — https://docs.smith.langchain.com/ — nền tảng trace + eval
3. **Langfuse** — https://langfuse.com/docs — observability mã nguồn mở
4. **Arize Phoenix** — https://arize.com/docs/phoenix — tracing + eval mã nguồn mở
5. **DuckDB** — https://duckdb.org/docs/stable/data/json/loading_json.html — query JSONL trực tiếp
6. **Zod** — https://zod.dev — validate schema lúc emit
7. **ULID / KSUID** — https://github.com/ulid/spec — event id sắp xếp được
8. **Claude Code** — https://docs.anthropic.com/en/docs/claude-code

### Production Systems

- **SWE-bench harness** — https://github.com/SWE-bench/SWE-bench — trajectory có cấu trúc cho eval
- **OpenHands** — https://github.com/All-Hands-AI/OpenHands — runtime event-stream
- **Langfuse** — https://langfuse.com — trace store tự host
- **Phoenix** — https://github.com/Arize-ai/phoenix — vòng lặp trace + eval

### Module Liên Quan

- `03-update-memory-store/trajectory-fork-replay.md` — implementation engine (fork/replay/resume)
- `07-workflow/README.md` §13 — bên tiêu thụ resume (checkpoint-resume, idempotency)
- `07-workflow/README.md` §5 — *liền kề, không trùng lặp*: distributed tracing cho một run (`trace_id`/spans/logs/metrics) của một workflow. Nối với module này qua `runId`; một span không phải một `TrajectoryEvent`.
- `08-task/README.md` §11 — bên sinh task (nguồn của `parentTaskId`)
- `11-evaluation/README.md` §15 — bên tiêu thụ eval (trajectory eval, hiệu chuẩn người)
- `12-sandbox-execution/README.md` §9 — bên sinh event `sandbox`
- `14-compaction-context/README.md` — bên sinh event `compaction`
- `15-approval-gates/README.md` §6 — bên tiêu thụ audit (`approval_verdict`)

---

*Tài liệu: Harness 13. Trajectory & Observability — HARNESS ENGINEERING EDITION*
*Module cross-cutting · cột sống của observability harness*
*Cập nhật: 16/10/2026*
*Tác giả: AI Knowledge Repository*

---

## Cập nhật 10/2026 — Python Trajectory & Cost-per-Run

> Bổ sung bản Python tương đương TrajectoryStore TypeScript ở §8.1, kèm phân tích
> **cost-per-run** — thứ biến trajectory từ "log để debug" thành "log để quản trị chi phí".

### 1. TrajectoryEvent + JSONL Append-Only (Python)

> 📄 **Code ví dụ:** [`examples/23-1-trajectoryevent-jsonl-append-only-python.py`](examples/23-1-trajectoryevent-jsonl-append-only-python.py)

Hai bất biến giữ nguyên như bản TypeScript: **chỉ-append** (sổ cái không xóa) và
**mỗi event mang `session_id`** (không event mồ côi — §4.3).

### 2. Cost-per-Run: Phát Hiện Run Đắt Bất Thường

> 📄 **Code ví dụ:** [`examples/24-2-cost-per-run-phat-hien-run-at.py`](examples/24-2-cost-per-run-phat-hien-run-at.py)

Vì sao metric này đáng xây đầu tiên: phân tích của Anthropic (06/2025) cho thấy
**token usage giải thích ~80% variance hiệu năng** giữa các run agent — run chậm,
run fail thường là run nuốt token nhiều nhất, và nguyên nhân hầu như luôn truy ra
được (vòng retry, retrieval lặp, compaction ngừng chạy — §6.2). Đo cost-per-run
theo task type là cách rẻ nhất thấy đuôi phân phối đó **trước** khi hoá đơn thấy.

Known gap: hiện chưa có **SLO cost-per-task** — ngưỡng "run này đắt bất thường"
vẫn là con số kinh nghiệm, chưa được chuẩn hoá thành SLO đo được. Gap này đã được
ghi nhận ở [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (§8);
cho tới khi có SLO, hãy lưu phân phối cost per task type để có dữ liệu hiệu chuẩn.

### 3. Trace Quyết Định — Không Trace Nội Dung Hội Thoại

Ranh giới privacy giữ nguyên trong bản Python: emit **pattern quyết định** (kind,
tool, tier, exit code, số token, latency), **không** emit nội dung prompt/response
của conversation. Lý do là bài học production của Anthropic Research: log hội thoại
nguyên văn biến trajectory store thành một bản copy dữ liệu nhạy cảm thứ hai —
mỗi query ad-hoc, mỗi dashboard, mỗi lần export đều là một đường rò rỉ tiềm năng
(→ §5.2: redact lúc emit, không redact lúc đọc). Payload cần truy vết → lưu `{ref}`
trỏ tới blob có ACL riêng, không inline vào event.

### 4. Liên Kết Kiến Trúc

Trajectory là **Layer 8 (Observability & Feedback)** — mọi layer khác emit vào đó,
mọi buổi debug đọc từ đó. Xem
[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) (Layer 8).
