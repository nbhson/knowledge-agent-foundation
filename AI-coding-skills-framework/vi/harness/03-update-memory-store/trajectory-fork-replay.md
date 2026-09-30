# 🔄 Trajectory Traceability Engine — Session Event Stream, Fork, Replay & Resume

> **Pattern kế thừa từ DeepSeek Harness**: Hệ thống quản lý toàn bộ vết thực thi (trajectory) dưới dạng **Session Event Stream**, hỗ trợ truy vết 100%, Replay để audit/debug, và Fork/Resume để thử nghiệm nhiều nhánh giải quyết vấn đề mà không làm hỏng lịch sử gốc.

> **⚠️ Schema chuẩn nằm ở `13-trajectory-observability`.** Shape `TrajectoryEvent`, danh mục
> `EventKind`, retention/redaction, và các câu truy vấn metric được đặc tả ở
> [`13-trajectory-observability`](../13-trajectory-observability/README.md) — module đó là hợp
> đồng mà mọi bên sinh và bên tiêu thụ đều viết code theo. **File này là engine**: store cụ thể,
> và bốn thao tác (append / replay / fork / resume) hiện thực trên schema của `13`.
> Nếu hai bên mâu thuẫn, `13` thắng — hãy sửa file này.
>
> Chia vậy là vì ghi vào bộ nhớ và quan sát run là hai việc khác nhau.
> `03-update-memory-store` quyết định *cái gì đáng giữ*; `13` quyết định *cái gì bắt buộc phải
> được ghi*. Cùng một event log phục vụ cả hai, đó là lý do schema được chia sẻ chứ không nhân bản.

---

## 📑 Mục Lục

- [1. Bối Cảnh \& Động Cơ](#1-bối-cảnh--động-cơ)
- [2. Triết Lý Trajectory Traceability Engine](#2-triết-lý-trajectory-traceability-engine)
- [3. Kiến Trúc Session Event Stream](#3-kiến-trúc-session-event-stream)
- [4. Các Thao Tác Cốt Lõi: Replay, Fork, Resume \& Search](#4-các-thao-tác-cốt-lõi-replay-fork-resume--search)
  - [4.1. Replay (Phát lại Trajectory)](#41-replay-phát-lại-trajectory)
  - [4.2. Fork (Tách Nhánh Session)](#42-fork-tách-nhánh-session)
  - [4.3. Resume (Tiếp Tục Phiên Làm Việc)](#43-resume-tiếp-tục-phiên-làm-việc)
  - [4.4. Event Search (Tìm Kiếm Vết Thực Thi)](#44-event-search-tìm-kiếm-vết-thực-thi)
- [5. Triển Khai Minh Họa (TypeScript Implementation)](#5-triển-khai-minh-họa-typescript-implementation)
- [6. DeepSeek Harness Case Study: Trajectory Viewer & Event Inspector](#6-deepseek-harness-case-study-trajectory-viewer--event-inspector)
- [7. Best Practices \& Anti-Patterns](#7-best-practices--anti-patterns)

---

## 1. Bối Cảnh & Động Cơ

Trong các hệ thống AI Agent phức tạp (đặc biệt là AI Coding Agents), một phiên tương tác có thể kéo dài hàng chục turn, gọi hàng trăm công cụ (file search, edit, terminal, git), và tạo ra lượng ngữ cảnh khổng lồ.

**Các vấn đề thường gặp ở Agent truyền thống:**
- **Black-box Execution**: Khi Agent mắc lỗi ở bước 15, người dùng không thể biết lỗi phát sinh từ bước nào (prompt sai, tool trả kết quả lỗi, hay LLM suy luận sai).
- **Không Thể Đảo Nược State (No Undo/Branching)**: Nếu Agent thực thi sai hướng ở bước 10, cách duy nhất là xóa toàn bộ session và bắt đầu lại từ đầu.
- **Khó khăn trong Debug & Evaluation**: Không thể phát lại chính xác chuỗi sự kiện đã xảy ra để reproduce bug hoặc benchmark mô hình.

---

## 2. Triết Lý Trajectory Traceability Engine

DeepSeek Harness giải quyết các vấn đề trên bằng triết lý **Full Traceability**:

```
Agent Execution = Sequence of State-Changing Events (Event Stream)
```

Thay vì lưu trữ cuộc trò chuyện dưới dạng danh sách tin nhắn phẳng (flat list of messages `[{role, content}]`), hệ thống lưu dưới dạng **Append-Only Event Stream**. Mọi hành động, kết quả công cụ, sự thay đổi state, và prompt injection đều được ghi lại dưới dạng Event có mốc thời gian (timestamp) và ID duy nhất.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SESSION EVENT STREAM                            │
├────────────────────────────────────────────────────────────────────────┤
│  [Evt 1: User Prompt] ──► [Evt 2: System Context Inject]              │
│       │                                                                │
│       ▼                                                                │
│  [Evt 3: Reasoning Step] ──► [Evt 4: Tool Call (search_file)]          │
│       │                                                                │
│       ▼                                                                │
│  [Evt 5: Tool Result] ──► [Evt 6: Checkpoint Alpha]                    │
│                                   │                                    │
│                 ┌─────────────────┴─────────────────┐                  │
│                 ▼                                   ▼                  │
│       [Main Branch: Evt 7a...]            [Fork Branch: Evt 7b...]     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Kiến Trúc Session Event Stream

Mọi Event dùng hợp đồng `TrajectoryEvent` định nghĩa ở `13-trajectory-observability` §1.1.
File này không lặp lại nó — điều duy nhất đáng bổ sung ở đây là cách các tên event cũ của
engine DeepSeek ánh xạ sang danh mục `EventKind` chuẩn, vì một store có trước `13` sẽ chứa các
bản ghi `user_prompt` / `agent_reasoning` / `state_change` vốn phải truy vấn được bằng kind mới:

```typescript
// Hợp đồng chuẩn — định nghĩa đúng một lần, ở 13-trajectory-observability §1.1
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
  id: string;             // evt_01HZX… — sắp xếp được theo thứ tự chuỗi (ULID/KSUID)
  seq: number;            // 0-based, không lỗ hổng, đơn điệu trong một session
  sessionId: string;
  parentTaskId?: string;  // → 08-task TaskNode.id
  runId?: string;         // một lần gọi engine; một session có thể có nhiều lần
  ts: number;             // ms epoch
  kind: EventKind;
  actor: string;          // "agent:coder" | "human:alice" | "system" | "judge"
  payload: unknown;       // đã redact; ≤64KB; vượt → { ref }
  tokens?: { in: number; out: number; cached?: number };
  latencyMs?: number;
  model?: string;
  costUsd?: number;
  error?: { code: string; retryable: boolean };
  fingerprint?: string;
}
```

**Bản đồ migrate cho store có trước `13`.** Ba field và ba kind đã đổi. `timestamp` → `ts`,
`type` → `kind`, `parentId` → `parentTaskId`, và `metadata.tokensUsed` (một số đơn) →
`tokens: { in, out }`. Lưu ý `parentId` trỏ tới *event liền trước trong luồng* còn
`parentTaskId` trỏ tới *node của kế hoạch* — đây là hai quan hệ khác nhau, nên khi migrate phải
suy ra `parentTaskId` từ đồ thị plan chứ không được đổi tên field:

| Cũ (engine `03`) | Chuẩn (hợp đồng `13`) | Ghi chú |
|----------------------|--------------------------|------|
| `user_prompt` | `prompt` (kèm `actor: "human:*"`) | |
| `system_injection` | `context_assembly` | |
| `agent_reasoning` | `message` (kèm `actor: "agent:*"`) | suy luận là một message, không phải kind riêng |
| `state_change` | `plan` / `plan_revision` / `compaction` | một kind cũ, ba kind chuẩn — tách theo payload |
| `timestamp` | `ts` | đổi tên |
| `type` | `kind` | đổi tên |
| `parentId` (event trước) | `parentTaskId` (node plan) | **tính lại, không đổi tên** |
| `metadata.tokensUsed: number` | `tokens: { in, out }` | tách; không rõ thì đưa hết vào `in` |
| *(không có)* | `seq`, `actor`, `model`, `costUsd`, `fingerprint` | backfill: `seq` theo vị trí, `actor` theo nguồn, còn lại nullable |

Engine bên dưới phát trực tiếp shape chuẩn. Nếu bạn đang migrate một store sẵn có, hãy chạy
backfill một lần rồi **xoá** nhánh cũ đi — hai schema cùng sống trong một store chính là cách
mà event mồ côi và audit không nối được bắt đầu.

---

## 4. Các Thao Tác Cốt Lõi: Replay, Fork, Resume & Search

### 4.1. Replay (Phát lại Trajectory)
Replay cho phép tải lại toàn bộ danh sách Event từ bước 1 đến bước $N$ và tái tạo trạng thái (state) chính xác của Agent tại bất kỳ mốc thời gian nào.
- **Deterministic Replay**: Tái tạo chính xác các câu trả lời và kết quả công cụ đã lưu trong quá khứ mà không cần gọi lại LLM hay execute lại command thực tế.
- **Live Replay (Dry-run)**: Giữ nguyên lịch sử Tool Execution nhưng gọi lại LLM thế hệ mới hơn để so sánh kết quả.

*Độ trung thực của replay* — bước nào an toàn để thực thi lại, bước nào phải phục vụ từ kết quả
đã ghi, và cách phát hiện sai lệch khi replay trực tiếp — được đặc tả ở
`13-trajectory-observability` §3.3. Luật ngắn: một `tool_call` trong replay có `fingerprint`
khớp với kết quả đã ghi thì tái dùng kết quả đã ghi; bất kỳ bước nào tạo side effect phải
được bảo vệ bằng idempotency key từ `07-workflow` §13.3.

### 4.2. Fork (Tách Nhánh Session)
Nếu người dùng thấy Agent đi sai hướng tại Event thứ $K$, người dùng có thể **Fork** tại Event $K$:
- Tạo một Session con (`parentSessionId`) chia sẻ lịch sử Event từ $1 \to K$.
- Mọi Event mới từ bước $K+1$ trở đi của Fork Session sẽ nằm ở một nhánh độc lập.
- Giúp người dùng thử nghiệm lời gọi prompt khác, chọn công cụ khác mà không ảnh hưởng tới Session ban đầu.

Bản ghi fork được lưu thành một event `checkpoint` mang `forkedFrom: { atSeq, by }` — xem
`13` §3.2. Về mặt logic, fork **không phải** là một bản sao: phần tiền tố là lịch sử bất biến,
nên fork *rẽ nhánh* từ nó chứ không thay thế hay chạy lại nó. Ví dụ bên dưới đánh số lại tiền tố
vào session mới cho dễ hình dung — đó là minh hoạ, không phải chiến lược lưu trữ. Hiện thực
thật chia sẻ tiền tố theo tham chiếu (hoặc qua con trỏ chuỗi cha–con) để một session 10.000
event không biến thành 20.000 event; quy tắc dedup đó được đặc tả ở `13` §2.2, không phải ở đây.

### 4.3. Resume (Tiếp Tục Phiên Làm Việc)
Tất cả trạng thái Session đều được persisted trên đĩa (disk/DB) theo cơ chế Event Sourcing. Khi hệ thống bị gián đoạn (crash, restart, network timeout), Agent có thể **Resume** lập tức từ Event cuối cùng mà không mất bất kỳ context nào.

Resume không được thực thi lại side effect đã commit. Engine nạp `checkpoint` cuối cùng, rồi
đọc các event ghi sau thời điểm crash và suy ra tập bước đã hoàn thành
(`stepsToSkip()` ở `13` §3.2); `07-workflow` §13.3 cung cấp idempotency key làm cho thao tác
bỏ qua đó an toàn, và `08-task` §11 là nơi trạng thái task được đối soát.

### 4.4. Event Search (Tìm Kiếm Vết Thực Thi)
Cho phép tìm kiếm chi tiết trong Trajectory Log:
- Tìm tất cả các Tool Call bị lỗi (`error.retryable === false`, hoặc `kind === "error"`).
- Tìm các dòng lệnh bash đã chạy thành công chứa từ khóa `pnpm build`.
- Lọc theo lượng token mỗi turn (`tokens.in + tokens.out`).

Catalog truy vấn production cho các truy vấn này — cộng phát hiện `tool_call` không khớp,
quy chiếu chi phí, và sức khoẻ compaction — nằm ở `13-trajectory-observability` §6.1. Engine
ở đây giữ một bộ lọc có kiểu cho unit test; SQL mới là chỗ đúng cho store.

---

## 5. Triển Khai Minh Họa (TypeScript Implementation)

Dưới đây là implementation mô phỏng Engine quản lý Trajectory Event Stream, phát đúng shape
chuẩn của `13`. Các tầng độ bền, live tailing, và cam kết append-only được đặc tả ở `13` §2.2;
`inMemory` ở đây đóng vai một sink JSONL.

```typescript
import { ulid } from 'ulid';

export class TrajectoryEngine {
  private events: Map<string, TrajectoryEvent[]> = new Map();

  // 1. Ghi nhận Event mới (seq không lỗ hổng và đơn điệu theo session)
  public append(e: Partial<TrajectoryEvent> & { sessionId: string; kind: EventKind; actor: string }): TrajectoryEvent {
    const sessionEvents = this.events.get(e.sessionId) || [];
    const evt: TrajectoryEvent = {
      id: `evt_${ulid()}`,
      seq: sessionEvents.length,
      sessionId: e.sessionId,
      parentTaskId: e.parentTaskId,
      runId: e.runId,
      ts: Date.now(),
      kind: e.kind,
      actor: e.actor,
      payload: e.payload ?? {},
      tokens: e.tokens,
      latencyMs: e.latencyMs,
      model: e.model,
      costUsd: e.costUsd,
      error: e.error,
      fingerprint: e.fingerprint,
    };
    sessionEvents.push(evt);
    this.events.set(e.sessionId, sessionEvents);
    return evt;
  }

  // 2. Replay Session đến bước mong muốn
  public replayToStep(sessionId: string, targetEventId: string): TrajectoryEvent[] {
    const sessionEvents = this.events.get(sessionId) || [];
    const index = sessionEvents.findIndex(e => e.id === targetEventId);
    if (index === -1) throw new Error(`Event ID ${targetEventId} not found in session ${sessionId}`);
    
    return sessionEvents.slice(0, index + 1);
  }

  // 3. Fork Session từ một checkpoint
  public forkSession(sourceSessionId: string, checkpointEventId: string): { newSessionId: string; events: TrajectoryEvent[] } {
    const historicalEvents = this.replayToStep(sourceSessionId, checkpointEventId);
    const newSessionId = `session_fork_${ulid()}`;

    // Tiền tố dùng chung: đánh số lại vào session fork, giữ nguyên thứ tự
    const forkedEvents: TrajectoryEvent[] = historicalEvents.map((e, i) => ({
      ...e,
      id: `evt_${ulid()}`,
      sessionId: newSessionId,
      seq: i,
    }));

    // Đăng ký tiền tố TRƯỚC khi append, để append() suy ra seq của checkpoint
    // từ độ dài thật. Append trước sẽ tạo seq 0 và đụng event đầu tiên được
    // sao chép — đúng thứ mà findOrphans() sẽ phát hiện.
    this.events.set(newSessionId, forkedEvents);

    // Ghi lại fork thành event checkpoint, không phải một bản sao ngầm
    this.append({
      sessionId: newSessionId,
      kind: "checkpoint",
      actor: "human:ui",
      payload: {
        message: `Forked from session ${sourceSessionId} at event ${checkpointEventId}`,
        forkedFrom: { sessionId: sourceSessionId, atSeq: historicalEvents.length - 1, by: "human:ui" },
      },
    });

    return { newSessionId, events: this.events.get(newSessionId)! };
  }

  // 4. Tìm kiếm Event (bộ lọc có kiểu; xem 13 §6.1 cho catalog SQL production)
  public searchEvents(sessionId: string, query: { kind?: EventKind; keyword?: string; failedOnly?: boolean }): TrajectoryEvent[] {
    const sessionEvents = this.events.get(sessionId) || [];
    return sessionEvents.filter(e => {
      if (query.kind && e.kind !== query.kind) return false;
      if (query.failedOnly && !e.error) return false;
      if (query.keyword) {
        const jsonStr = JSON.stringify(e.payload).toLowerCase();
        if (!jsonStr.includes(query.keyword.toLowerCase())) return false;
      }
      return true;
    });
  }

  // 5. Phát hiện lỗ hổng — seq thiếu nghĩa là mất một lần ghi, không phải mất một suy nghĩ (13 §4.3)
  public findOrphans(sessionId: string): number[] {
    const seqs = (this.events.get(sessionId) || []).map(e => e.seq);
    const gaps: number[] = [];
    for (let i = 0; i < seqs.length; i++) if (seqs[i] !== i) gaps.push(i);
    return gaps;
  }
}
```

---

## 6. DeepSeek Harness Case Study: Trajectory Viewer & Event Inspector

Trong Web UI của DeepSeek Harness (chạy tại port `3080`), tính năng **Trajectory View** cung cấp một giao diện trực quan cho phép kỹ sư:
1. **Visual Timeline**: Xem trục thời gian của phiên làm việc với các khối màu tương ứng cho Reasoning, Tool Call (Bash/Edit), và Execution Result.
2. **One-Click Replay**: Nhấn vào bất kỳ node nào trong timeline để phát lại chính xác câu thoại và ngữ cảnh lúc đó.
3. **Fork & Branch**: Nút "Fork Session from here" cho phép rẽ nhánh lập tức từ giao diện web, tạo môi trường thử nghiệm an toàn.

---

## 7. Best Practices & Anti-Patterns

### ✅ Best Practices
- **Append-Only Immutability**: Không bao giờ chỉnh sửa trực tiếp các Event đã ghi. Nếu muốn rollback hay sửa đổi, hãy fork session hoặc ghi một Event bù trừ thuộc kind chuẩn — `plan_revision` cho thay đổi plan, `compaction` cho việc thu nhỏ context window. (`state_change` là tên *legacy*; xem bảng migrate ở §1, đừng ghi kind này.)
- **Compact Payload**: Với các Tool Result trả về dữ liệu cực lớn (vd: log 10,000 dòng), hãy lưu payload ngắn gọn và trích xuất reference sang file blob để tránh làm đầy RAM/DB. Hợp đồng `13` giới hạn payload inline ở 64KB và bắt buộc `{ ref }` vượt ngưỡng đó.
- **Regular Checkpointing**: Ghi event `checkpoint` sau mỗi mốc hoàn thành task quan trọng (vd: xong phase planning, xong phase refactoring) để dễ dàng Fork.
- **Luôn gán `actor`**: Một `tool_call` không có `actor` là không truy vết được — đó là thứ audit không thể sửa lại sau.
- **Luôn gán `parentTaskId`**: Một event không có nó là orphan — không nối được vào plan, và vì vậy vô hình với mọi truy vấn xuyên module ở `13` §4.1.

### ❌ Anti-Patterns
- **Incomplete Logging**: Chỉ lưu câu thoại chat giữa User và Agent mà không lưu các sự kiện ngầm (Context Injection, Internal Tool Calls, System Errors). Chat log không phải là trajectory — xem `13` §14.
- **Non-deterministic Events**: Lưu kết quả Tool Call nhưng không lưu cấu hình môi trường/tham số, làm hỏng Replay về sau.
- **Hai schema cùng sống**: Chạy song song shape cũ `type`/`timestamp`/`parentId` của engine này với hợp đồng `13`. Hãy chọn một, migrate, xoá cái kia.
