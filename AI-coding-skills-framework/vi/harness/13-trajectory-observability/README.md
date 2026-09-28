# 📈 XIII. Trajectory & Observability

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

Ticket: *"Agent xoá `src/auth/middleware.ts` và user báo lại sau 40 phút. Tại sao?"*

Không có trajectory, câu hỏi này không trả lời được. Bạn có một chat log (lời model,
không phải hành động của nó), một phần CI log, và cảm giác ("nó đang refactor auth").
Bạn không nói được lệnh xoá nằm ở lượt nào, tool trả về gì trước đó, file lúc đó có
thực sự nằm trên nhánh hiện tại không, hay agent đang nghĩ là mình đang làm gì. Bạn
viết một post-mortem mà thực chất chỉ là phỏng đoán.

Có trajectory, cùng câu hỏi đó mất mười một giây và một query:

```sql
SELECT seq, kind, payload->>'tool' AS tool, payload->>'path' AS path
FROM trajectory
WHERE session_id = 'ses_44a' AND payload->>'path' LIKE '%middleware%'
ORDER BY seq;
-- seq 31: read_file  src/auth/middleware.ts  → 4.1KB
-- seq 32: edit_file  (patch applied)
-- seq 33: write_file  ← lệnh xoá
-- seq 34: eval        "tests pass" (thật — không còn gì import nó)
```

**Và các câu hỏi tiếp theo tự trả lời lấy nhau.** Tại sao nó xoá? `seq 29: prompt` —
các export không ai dùng, và mô hình chọn xoá thay vì để lại code chết. Có hoàn tác
được không? `seq 33` ghi `git worktree`, nên có, và patch cuối nằm ở `seq 51`. Chuyện
này có nên qua gate không? Blast radius là một file — dưới ngưỡng `write` — nhưng file
đó được **3 file khác import mà agent chưa từng đọc**. Đó là một câu hỏi chính sách, và
giờ nó có câu trả lời.

**Đây là thứ một trajectory mua được: khác biệt giữa "nó hỏng" và "đây chính xác là
gì đã xảy ra, đây là lý do, và đây là điều chúng ta nên đổi".**

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

Góc chi phí đáng nhấn mạnh. Không có tokens và model tier ở từng step, bạn không trả
lời được *"vì sao tháng trước hóa đơn tăng gấp ba?"* — chỉ biết là nó tăng. Có
trajectory thì đó là `SELECT SUM(tokens) WHERE model='frontier' GROUP BY session`, và
câu trả lời thường là "vòng retry trên 3% số run" hoặc "compaction ngừng chạy" — cả hai
đều sửa được trong một buổi chiều.

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

**Trajectory & Observability** biến một run agent mờ đục thành một đối tượng truy vấn
được, replay được, audit được. Đó là khác biệt giữa một agent bạn *vận hành* và một
agent bạn *hy vọng*.

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

**Hai bất biến làm nên nó:** (1) *chỉ-append* — không event nào bị sửa, nên lịch sử đáng
tin; (2) *mọi event mang `sessionId` + `parentTaskId`* — nên không event nào mồ côi và
mọi câu hỏi đều có đường join.

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

Một shape, mọi module emit, mọi công cụ đọc. Đây là artifact quan trọng nhất trong
tầng observability của một harness.

```typescript
export type EventKind =
  | "session_start" | "session_end"
  | "context_assembly" | "prompt"
  | "plan" | "plan_revision"
  | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write"
  | "delegate" | "message"
  | "approval_request" | "approval_verdict"
  | "compaction" | "checkpoint" | "eval" | "error";

export interface TrajectoryEvent {
  id: string;             // evt_01HZX… — sắp xếp được theo lexicographic (ULID/KSUID)
  seq: number;            // 0-based, liền mạch, tăng đơn điệu trong session
  sessionId: string;      // một user request = một session
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // một lần engine chạy; một session có thể có nhiều lần
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: EventPayload;  // đã redact; ≤64KB; quá lớn → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;         // tier nào phục vụ step này → quy chi phí
  costUsd?: number;       // tính lúc emit, không tính lại lúc query
  error?: { code: string; retryable: boolean };
  fingerprint?: string;   // hash prompt → dedupe replay, audit compaction
}
```

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

**Quy tắc:** nếu một module tạo ra một sự thật mà sớm nay sẽ có người muốn tương
quan, nó phải emit một event. Một sự thật chỉ nằm trong memory là một sự thật bạn
không thể debug bằng.

### 1.3 Validate & Phiên Bản Hoá

```typescript
import { z } from "zod";

export const TrajectoryEventSchema = z.object({
  id: z.string().regex(/^evt_[0-9A-HJKMNP-TV-Z]{26}$/),  // ULID
  seq: z.number().int().nonnegative(),
  sessionId: z.string().min(1),
  parentTaskId: z.string().optional(),
  runId: z.string().optional(),
  ts: z.number().int(),
  kind: z.enum([/* … */]),
  actor: z.string().min(1),
  payload: z.unknown(),
  tokens: z.object({ in: z.number(), out: z.number(), cached: z.number().optional() }).optional(),
  latencyMs: z.number().nonnegative().optional(),
  model: z.string().optional(),
  costUsd: z.number().nonnegative().optional(),
  error: z.object({ code: z.string(), retryable: z.boolean() }).optional(),
  fingerprint: z.string().optional(),
}).superRefine((e, ctx) => {
  if (e.kind !== "session_start" && !e.parentTaskId)
    ctx.addIssue({ code: "custom", message: "orphan event: parentTaskId required" });
});
```

**Phiên bản hoá schema, đừng phiên bản từng trường.** Thêm `v: 2` và giữ lại reader
xử lý được cả hai. Một trajectory viết sáu tháng trước phải vẫn đọc được — đó là
chính lý do giữ nó. Đổi tên trường trong im lặng phá hủy bản sao duy nhất của sự thật.

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

Các điểm xen kẽ quan trọng:

- **`tool_call` rồi `tool_result`, luôn đi cặp.** Một `tool_call` không có `tool_result` là một step bị treo — và chính query tìm ra chúng là công cụ phát hiện treo của bạn (→ `09` §16.1).
- **`plan_revision` xen giữa với các tool call đã sinh nó.** Dựng lại câu chuyện đòi nguyên nhân và hệ quả nằm cạnh nhau.
- **`compaction` nằm giữa prompt nó rút gọn và prompt kế tiếp.** Nếu không, bạn không giải thích được vì sao mô hình quên mất thứ gì.

### 2.2 Đường Ghi — Các Tầng Bền Vững

Không phải event nào cũng xứng đáng `fsync`. Xếp theo cái giá khi mất:

| Event | Bền vững | Lý do |
|-------|----------|-------|
| `approval_verdict` | **fsync** | Bản ghi pháp lý; mất là mất chuỗi audit |
| `memory_write` | **fsync** | Mất fact bền = bug đúng-sai lặng lẽ |
| `session_start` / `session_end` | **fsync** | Neo của báo cáo cost và thời lượng |
| `eval` | **fsync** | Phát hiện hồi quy phụ thuộc tính đầy đủ |
| `tool_call` / `tool_result` | flush ≤100 ms | Cần để debug, chấp nhận mất 100 ms cuối |
| `prompt` / `context_assembly` | buffered | Dựng lại được từ chính run |

```bash
# Mỗi session một file. Chỉ-append, JSON newline-delimited.
./trajectories/ses_44a.jsonl
./trajectories/ses_44b.jsonl
```

**Tại sao JSONL chứ không phải bảng?** Ghi chỉ-append, không cần khoá trong trường hợp
thường, `grep` được, dễ mang váo, replay được. Index là vấn đề *dẫn xuất*; nạp vào
DuckDB/SQLite để phân tích. Lưu log dạng bảng trước nghĩa là mọi event là một giao
dịch trong hot path — thuế độ trễ lên vòng lặp agent, đổi lấy một câu query bạn chạy
một tuần một lần.

### 2.3 Đường Đọc & Tail Trực Tiếp

```bash
# 1. Điều gì đã xảy ra, theo thứ tự?
jq -r '[.seq, .kind, .actor, (.payload.tool // "-")] | @tsv' ses_44a.jsonl

# 2. Tìm step đắt nhất
jq -s 'sort_by(-(.latencyMs // 0))[:10] | .[] | {seq, kind, latencyMs, model}' ses_44a.jsonl

# 3. Tìm tool_call không có tool_result (phát hiện treo)
jq -s '[.[] | select(.kind=="tool_call") | .seq] as $c
       | [.[] | select(.kind=="tool_result") | .seq] as $r
       | ($c - $r)' ses_44a.jsonl

# 4. Tail trực tiếp
tail -f ses_44a.jsonl | jq -c '{seq, kind, tool: .payload.tool}'
```

Nạp vào DuckDB cho mọi thứ nặng hơn:

```sql
INSTALL httpfs; LOAD httpfs;
SELECT model, COUNT(*) AS steps, SUM(tokens.in + tokens.out) AS total_tokens,
       SUM(costUsd) AS usd
FROM read_json_auto('trajectories/*.jsonl')
GROUP BY model ORDER BY usd DESC;
```

---

## 3. Fork, Replay, Resume

### 3.1 Ngữ Nghĩa Từng Thao Tác

| Thao tác | Làm gì | Khi nào cần | Yêu cầu trung thực |
|----------|--------|-------------|---------------------|
| **Replay** | Chạy lại event `0..N` với cùng input; assert output khớp | Tái hiện chính xác một bug report | Step tất định phải giống byte |
| **Fork** | Clone session tại event `K`, đi tiếp với prompt/model/policy khác | "Nếu chỗ này dùng model lớn thì sao?" | Tiền tố giống nhau; hậu tố có thể phân kỳ tuỳ ý |
| **Resume** | Nạp checkpoint cuối + phần event ghi sau crash | Workflow bền vững (→ 07 §13) | Không được chạy lại side effect đã commit |

Đây là ba công cụ khác nhau với ba bảo đảm khác nhau. Lẫn lộn chúng là cách các đội
biến một "replay" thành công cụ gửi lại email production.

### 3.2 Implementation

<details>
<summary>TypeScript Code — fork / replay / resume (Click để mở rộng/thu gọn)</summary>

```typescript
import { createHash } from "node:crypto";
import { createInterface } from "node:readline";
import { createReadStream } from "node:fs";
import { ulid } from "ulid";

export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}

export async function loadSession(path: string): Promise<TrajectoryEvent[]> {
  const out: TrajectoryEvent[] = [];
  const rl = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of rl) if (line.trim()) out.push(JSON.parse(line));
  return assertGapless(out);
}

/** seq liền mạch chứng minh không mất lần ghi nào. Có lỗ hổng nghĩa là log
 *  không đầy đủ — mọi kết luận suy ra (cost, replay) khi đó đáng ngờ. */
function assertGapless(evts: TrajectoryEvent[]): TrajectoryEvent[] {
  evts.sort((a, b) => a.seq - b.seq);
  for (let i = 1; i < evts.length; i++)
    if (evts[i].seq !== evts[i - 1].seq + 1)
      throw new Error(`trajectory gap: seq ${evts[i - 1].seq} → ${evts[i].seq}`);
  return evts;
}

/** FORK — clone tiền tố, tạo danh tính mới, đi tiếp theo hướng khác. */
export function fork(src: Session, atSeq: number, by: string): Session {
  const prefix = src.events.filter(e => e.seq <= atSeq);
  const clone: Session = {
    sessionId: `ses_${ulid()}`,
    forkedFrom: { sessionId: src.sessionId, atSeq, by },
    events: prefix.map(e => ({ ...e })),      // id mới khi ghi, seq giữ nguyên
  };
  return clone;
}

export interface ReplayDiff { step: number; kind: string; drift: "none" | "output" | "error" | "latency" }

/** REPLAY — so một lần chạy mới với lần đã ghi. */
export function diffRun(recorded: TrajectoryEvent[], fresh: TrajectoryEvent[]): ReplayDiff[] {
  const diffs: ReplayDiff[] = [];
  const n = Math.max(recorded.length, fresh.length);
  for (let i = 0; i < n; i++) {
    const a = recorded[i], b = fresh[i];
    if (!a || !b) { diffs.push({ step: i, kind: a?.kind ?? b?.kind ?? "?", drift: "output" }); continue; }
    if (a.kind !== b.kind) { diffs.push({ step: i, kind: a.kind, drift: "output" }); continue; }
    if (hash(a.payload) !== hash(b.payload)) diffs.push({ step: i, kind: a.kind, drift: "output" });
    else if ((a.latencyMs ?? 0) > (b.latencyMs ?? 0) * 3 + 500) diffs.push({ step: i, kind: a.kind, drift: "latency" });
  }
  return diffs;
}
const hash = (o: unknown) => createHash("sha256").update(JSON.stringify(o)).digest("hex").slice(0, 16);

/** RESUME — idempotency key làm cho chạy lại sau crash an toàn. */
export function stepsToSkip(events: TrajectoryEvent[], done: Set<string>): string[] {
  return events.filter(e => e.kind === "tool_call" && done.has(idempotencyKeyOf(e)))
               .map(e => e.payload.callId as string);
}
export function idempotencyKeyOf(e: TrajectoryEvent): string {
  return `${e.parentTaskId}:${e.payload.tool}:${e.payload.argvHash}`;  // → 07 §13.3
}
```

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

**Quy tắc ngăn thảm hoạ:** replay không bao giờ kích hoạt lại một side effect không
thể hoàn tác. `idempotencyKeyOf()` = `(taskId, tool, argvHash)`; khi replay, key đã
hoàn tất bị bỏ qua và `tool_result` đã ghi được thay thế. Đây chính là lý do
`07-workflow/README.md` §13.3 yêu cầu idempotency key trên mọi step — replay không
phải thứ "có thì hay", nó là *lý do* những key đó tồn tại.

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

Mỗi dòng là một câu hỏi mà người dùng sẽ hỏi trong vòng một tuần sau khi ship. Mỗi
dòng là một query SQL. Mỗi dòng là bất khả thi nếu thiếu key.

### 4.2 Năm Câu Hỏi Một Query Trả Lời

```sql
-- "Sao retrieval được trích dẫn mà không dùng?" — join context_assembly → prompt → eval
SELECT c.session_id,
       c.payload->>'chunkIds'    AS retrieved,
       p.payload->>'chunkIds'    AS used,
       e.payload->>'score'       AS judge_score
FROM trajectory c
JOIN trajectory p ON p.session_id = c.session_id AND p.kind='prompt'
JOIN trajectory e ON e.session_id = c.session_id AND e.kind='eval'
WHERE c.kind='context_assembly';
```

Join key biến "mô hình trả lời sai" thành "nó lấy 12 chunk, dùng 4, và 3 chunk điểm
cao nhất đã cũ" — một kết luận có chủ sở hữu và có cách sửa.

### 4.3 Phát Hiện Event Mồ Côi

Một event không có `parentTaskId` (hoặc task không tồn tại) là lỗi đấu nối. Chạy
liên tục:

```sql
SELECT kind, COUNT(*) AS orphans, MIN(ts) AS first_seen
FROM trajectory
WHERE parent_task_id IS NULL AND kind NOT IN ('session_start','session_end')
GROUP BY kind;
```

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

Redaction diễn ra **lúc ghi**, không phải lúc đọc. Redact lúc đọc thất bại ngay khi bất
kỳ thứ gì đọc bảng thô — và bảng thô luôn bị đọc bởi các query ad-hoc.

```typescript
const PII = [
  /sk-[A-Za-z0-9_-]{20,}/g,                 // API key
  /gh[pousr]_\w{20,}/g,                     // GitHub token
  /AKIA[0-9A-Z]{16}/g,                      // AWS access key id
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/g,     // private key
  /[\w.+-]+@[\w-]+\.[\w.]{2,}/g,             // email
  /\b(?:\d[ -]?){13,19}\b/g,                 // số thẻ
];

export function redactPayload<T>(payload: T): { payload: T; redactions: number } {
  let s = JSON.stringify(payload), n = 0;
  for (const re of PII) s = s.replace(re, () => { n++; return "[REDACTED]"; });
  return { payload: JSON.parse(s), redactions: n };
}
```

Lưu `redactions` thành một trường của event. Rồi:

```sql
-- Kiểm chứng hàng quý: không còn chuỗi hình dạng secret trong warm store
SELECT COUNT(*) FROM read_json_auto('trajectories-warm/*.jsonl')
WHERE payload::TEXT ~ 'sk-[A-Za-z0-9]{20}';
-- phải bằng 0. Khác 0 = incident.
```

### 5.3 Cô Lập Tenant & Receipt Xoá

- **`tenantId` trên mọi event, ép lúc ghi.** Thiếu `tenantId` là từ chối ghi, không phải cảnh báo.
- **Row-level security hoặc bucket riêng cho từng tenant.** Rò rỉ chéo tenant trong trajectory store là một sự cố dữ liệu theo nghĩa đen.
- **Xoá theo GDPR** gỡ: event trajectory, aggregate cold, báo cáo dẫn xuất, và mọi projection đã cache — rồi phát một receipt:

```json
{ "kind": "deletion_receipt", "tenantId": "acme",
  "sessionsDeleted": 1841, "eventsDeleted": 214883, "coldAggregatesPurged": true,
  "ref": "receipts/acme-2026-07-19.json", "at": 1752900000000 }
```

Bản receipt cũng được lưu bất biến. "Chúng tôi đã xoá nó" phải kiểm chứng được mà
không cần tin vào chính hệ thống đã xoá.

---

## 6. Metrics Có Sẵn Miễn Phí

### 6.1 Catalog Query

Mọi metric là một query trên cùng một bảng. Đây là phần thưởng cho công sức thiết kế
schema.

```sql
-- Hiệu quả step (→ 11 §15.1)
SELECT AVG(steps) AS avg_steps, AVG(tokens_out) AS avg_out
FROM (SELECT session_id, COUNT(*) AS steps, MAX(tokens_out) AS tokens_out
      FROM trajectory WHERE kind IN ('tool_call','prompt') GROUP BY session_id);

-- Tool precision: hữu ích ÷ tổng (gắn nhãn hữu ích ở tầng tool)
SELECT payload->>'tool' AS tool,
       COUNT(*) AS calls,
       AVG(CASE WHEN payload->>'useful'='true' THEN 1.0 ELSE 0.0 END) AS precision
FROM trajectory WHERE kind='tool_call' GROUP BY tool ORDER BY calls DESC;

-- Recovery rate: những run gặp lỗi nhưng vẫn hoàn thành
SELECT COUNT(*) FILTER (WHERE err THEN 1)/COUNT(*)::float AS recovered
FROM (SELECT session_id, BOOL_OR(kind='error') AS err
      FROM trajectory GROUP BY session_id);

-- Phát hiện lặp: cùng argvHash 3+ lần trong một session
SELECT session_id, payload->>'argvHash' AS h, COUNT(*) AS n
FROM trajectory WHERE kind='tool_call'
GROUP BY session_id, h HAVING COUNT(*) >= 3 ORDER BY n DESC;

-- Sức khoẻ compaction (→ 14)
SELECT AVG((payload->>'ratio')::float) AS avg_ratio,
       AVG((payload->>'dropped')::int)  AS avg_dropped
FROM trajectory WHERE kind='compaction';

-- Tỉ lệ fallback (→ 01): các đường retrieval bị suy giảm
SELECT AVG(CASE WHEN payload->>'degraded'='true' THEN 1.0 ELSE 0.0 END)
FROM trajectory WHERE kind='context_assembly';
```

### 6.2 Quy Kết Chi Phí

```sql
-- Cost theo task, theo model, theo tenant — ba câu hỏi finance hay hỏi
SELECT t.session_id, e.model,
       SUM(e.cost_usd) AS usd, SUM(e.tokens_out) AS out_tok
FROM trajectory e JOIN trajectory t ON t.session_id = e.session_id AND t.kind='session_start'
WHERE e.cost_usd IS NOT NULL
GROUP BY t.session_id, e.model
ORDER BY usd DESC LIMIT 20;
```

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

Trả lời 2 và 3 trước 4 là kỷ luật. Phần lớn ticket kiểu "mô hình làm cái gì đó ngu
ngốc" thực chất là lỗi ở câu 2: mô hình thiếu thông tin, và câu 3 phản ánh đúng điều
đó.

### 7.2 So Sánh Hai Run

```typescript
export function diffSessions(a: TrajectoryEvent[], b: TrajectoryEvent[]): string {
  const A = new Map(a.map(e => [e.seq, e])), B = new Map(b.map(e => [e.seq, e]));
  const lines: string[] = [];
  for (const seq of new Set([...A.keys(), ...B.keys()]).values()) {
    const x = A.get(seq), y = B.get(seq);
    if (!x) { lines.push(`+${seq} ${y!.kind} ${y!.payload.tool ?? ""}`); continue; }
    if (!y) { lines.push(`-${seq} ${x.kind} ${x.payload.tool ?? ""}`); continue; }
    if (JSON.stringify(x.payload) !== JSON.stringify(y.payload))
      lines.push(`~${seq} ${x.kind} ${x.payload.tool ?? ""} (${x.latencyMs}ms → ${y.latencyMs}ms)`);
  }
  return lines.join("\n");
}
```

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

```typescript
import { appendFile, open, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { ulid } from "ulid";
import { redactPayload, TrajectoryEventSchema } from "./schema";

const FSYNC_KINDS = new Set(["approval_verdict", "memory_write", "eval", "session_start", "session_end"]);
const MAX_PAYLOAD = 64_000;

export class TrajectoryStore {
  private seq = 0;
  private buffer: string[] = [];
  private timer?: NodeJS.Timeout;
  dropped = 0; lastError?: unknown; currentSession = "";

  constructor(private root: string) {}

  /** Mọi module gọi hàm này. Không bao giờ throw vào vòng lặp agent —
   *  một lỗi telemetry không được làm hỏng task. Lỗi được đếm và báo. */
  async append(e: Omit<TrajectoryEvent, "id" | "seq">): Promise<void> {
    try {
      const { payload, redactions } = redactPayload(e.payload);
      const ev = TrajectoryEventSchema.parse({
        ...e, id: `evt_${ulid()}`, seq: this.seq++, redactions,
        payload: JSON.stringify(payload).length > MAX_PAYLOAD ? { ref: blobRef(payload) } : payload,
      });
      const line = JSON.stringify(ev) + "\n";
      if (FSYNC_KINDS.has(ev.kind)) {
        await this.flush();
        const fh = await open(this.path(ev.sessionId), "a");
        await fh.appendFile(line); await fh.sync(); await fh.close();
      } else {
        this.buffer.push(line);
        this.timer ??= setTimeout(() => void this.flush(), 100);
      }
    } catch (err) { this.dropped++; this.lastError = err; }
  }

  async flush(): Promise<void> {
    clearTimeout(this.timer); this.timer = undefined;
    if (!this.buffer.length) return;
    const b = this.buffer; this.buffer = [];
    await mkdir(this.root, { recursive: true });
    await appendFile(this.path(this.currentSession), b.join(""), "utf8");
  }

  async close(): Promise<void> { await this.flush(); }
  path(sessionId: string) { return join(this.root, `${sessionId}.jsonl`); }
}
```

</details>

### 8.2 Projector Tiến Độ Trực Tiếp

```typescript
/** Chiếu event stream thành trạng thái UI sống. Cùng một stream, khác cái nhìn —
 *  UI là một phép gấp trên trajectory, không phải nguồn sự thật thứ hai. */
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string; status: "running" | "waiting" | "done" | "failed";
}

export function project(e: TrajectoryEvent, prev: RunProgress): RunProgress {
  const next = { ...prev, stepsDone: prev.stepsDone + (e.kind === "tool_result" ? 1 : 0) };
  if (e.tokens) next.tokens += e.tokens.in + e.tokens.out;
  next.costUsd += e.costUsd ?? 0;
  if (e.kind === "plan") next.currentTask = (e.payload as any).firstPendingTask;
  if (e.kind === "approval_request") next.status = "waiting";
  if (e.kind === "approval_verdict") next.status = "running";
  if (e.kind === "error") next.lastError = e.error?.code;
  if (e.kind === "session_end")
    next.status = (e.payload as any).tasksDone === (e.payload as any).tasksTotal ? "done" : "failed";
  return next;
}
```

### 8.3 Debug Logger Adapter

```typescript
/** Một dòng dễ đọc cho các run có DEBUG=agent. Cùng event, chỉ khác định dạng. */
export function formatEvent(e: TrajectoryEvent): string {
  const t = `${String(e.seq).padStart(3, "0")} ${e.kind.padEnd(16)} ${e.actor.padEnd(12)}`;
  const detail = e.kind === "tool_call" ? `${e.payload.tool} ${JSON.stringify(e.payload.args).slice(0, 60)}`
    : e.kind === "tool_result" ? `exit=${e.payload.exitCode} ${e.latencyMs}ms ${e.payload.bytes}B`
    : e.kind === "eval" ? `score=${e.payload.score}`
    : e.kind === "compaction" ? `ratio=${e.payload.ratio} dropped=${e.payload.dropped}`
    : "";
  const cost = e.costUsd ? ` $${e.costUsd.toFixed(4)}` : "";
  return `${t} ${detail}${cost}`;
}
```

---

## 9. Kiểm Thử Trajectory

### 9.1 Contract Test

Chạy trong CI. Đây là bắt lớp bug khi một module mới emit một event phá vỡ mọi query
phía dưới.

```typescript
import { TrajectoryEventSchema } from "./schema";

export function validateEmitter(name: string, evts: unknown[]): void {
  for (const e of evts) {
    const r = TrajectoryEventSchema.safeParse(e);
    if (!r.success) throw new Error(`${name} emitted invalid event: ${r.error.message}`);
  }
  const seqs = evts.map((e: any) => e.seq).sort((a: number, b: number) => a - b);
  seqs.forEach((s, i) => { if (s !== i) throw new Error(`${name} produced a seq gap at ${i}`); });
}
```

Cũng assert: mọi `tool_call` có `tool_result` tương ứng; mọi `tool_result.parentTaskId`
tồn tại trong plan; không payload nào chứa pattern secret.

### 9.2 Bộ Test Replay

```typescript
/** Step tất định phải giống byte. Step LLM so bằng fingerprint + dung sai score.
 *  Bất cứ thứ gì khác là bug của harness. */
export async function replayTest(cases: ReplayCase[]): Promise<{ name: string; drift: ReplayDiff[] }[]> {
  const out: { name: string; drift: ReplayDiff[] }[] = [];
  for (const c of cases) {
    const recorded = await loadSession(c.path);
    const fresh = await c.run();
    out.push({ name: c.name, drift: diffRun(recorded, fresh) });
  }
  return out;
}
```

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

Bài học thiết kế: **làm trajectory trở thành artifact đánh giá, không phải output
cuối.** Eval chỉ dựa trên output cuối cho bạn biết *nó* fail. Eval dựa trên trajectory
cho bạn biết nó fail vì không tìm ra bug (vấn đề retrieval), vì viết sai patch (vấn
đề suy luận), hay vì patch đúng mà test harness flaky (vấn đề hạ tầng). Ba thứ đó
đòi hỏi cách sửa hoàn toàn khác nhau.

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

```typescript
span.setAttributes({
  "gen_ai.system": "anthropic",
  "gen_ai.request.model": "claude-sonnet-4-5",
  "gen_ai.usage.input_tokens": 12_480,
  "gen_ai.usage.output_tokens": 1_120,
  "gen_ai.agent.id": "agent:coder",
  "gen_ai.trajectory.session_id": "ses_44a",
});
```

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

```typescript
// ── Event ─────────────────────────────────────────────────────────────────
export type EventKind =
  | "session_start" | "session_end" | "context_assembly" | "prompt"
  | "plan" | "plan_revision" | "tool_call" | "tool_result" | "sandbox"
  | "memory_read" | "memory_write" | "delegate" | "message"
  | "approval_request" | "approval_verdict" | "compaction" | "checkpoint"
  | "eval" | "error";

export interface TrajectoryEvent {
  id: string; seq: number; sessionId: string; parentTaskId?: string; runId?: string;
  ts: number; kind: EventKind; actor: string; payload: unknown;
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number; model?: string; costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string; redactions?: number; tenantId: string;
}

export type NewEvent = Omit<TrajectoryEvent, "id" | "seq" | "redactions">;

// ── Store ──────────────────────────────────────────────────────────────────
export interface TrajectoryStore {
  append(e: NewEvent): Promise<void>;
  flush(): Promise<void>;
  load(sessionId: string): Promise<TrajectoryEvent[]>;
  tail(sessionId: string, fromSeq: number): AsyncIterable<TrajectoryEvent>;
}

// ── Derived views ──────────────────────────────────────────────────────────
export interface RunProgress {
  sessionId: string; currentTask?: string; stepsDone: number;
  tokens: number; costUsd: number; lastError?: string;
  status: "running" | "waiting" | "done" | "failed";
}

// ── Fork / replay ──────────────────────────────────────────────────────────
export interface Session {
  sessionId: string;
  forkedFrom?: { sessionId: string; atSeq: number; by: string };
  events: TrajectoryEvent[];
}
export type ReplayDrift = "none" | "output" | "error" | "latency";
export interface ReplayDiff { step: number; kind: EventKind | string; drift: ReplayDrift }

// ── Redaction ──────────────────────────────────────────────────────────────
export interface RedactionResult<T> { payload: T; redactions: number }
export interface Redactor { redact(s: string): RedactionResult<string> }

// ── Retention ──────────────────────────────────────────────────────────────
export type RetentionTier = "hot" | "warm" | "cold" | "purged";
export interface RetentionPolicy {
  hotDays: number; warmDays: number; coldDays: number;
  inlineMaxBytes: number;             // > ngưỡng này → { ref } ở tầng warm
  tenantTtlDays?: number;             // GDPR
}

// ── Test surface ───────────────────────────────────────────────────────────
export interface ReplayCase {
  name: string; path: string;
  run(): Promise<TrajectoryEvent[]>;
  expectDeterministic: EventKind[];
}
```

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
- `08-task/README.md` §11 — bên sinh task (nguồn của `parentTaskId`)
- `11-evaluation/README.md` §15 — bên tiêu thụ eval (trajectory eval, hiệu chuẩn người)
- `12-sandbox-execution/README.md` §9 — bên sinh event `sandbox`
- `14-compaction-context/README.md` — bên sinh event `compaction`
- `15-approval-gates/README.md` §6 — bên tiêu thụ audit (`approval_verdict`)

---

*Tài liệu: XIII. Trajectory & Observability — HARNESS ENGINEERING EDITION*
*Module cross-cutting · cột sống của observability harness*
*Cập nhật: 19/07/2026*
*Tác giả: AI Knowledge Repository*
