# 🔄 Trajectory Traceability Engine — Session Event Stream, Fork, Replay & Resume

> **Pattern kế thừa từ DeepSeek Harness**: Hệ thống quản lý toàn bộ vết thực thi (trajectory) dưới dạng **Session Event Stream**, hỗ trợ truy vết 100%, Replay để audit/debug, và Fork/Resume để thử nghiệm nhiều nhánh giải quyết vấn đề mà không làm hỏng lịch sử gốc.

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

Mỗi Event trong Trajectory bao gồm các thông tin chuẩn hóa:

```typescript
export type EventType = 
  | 'user_prompt' 
  | 'system_injection' 
  | 'agent_reasoning' 
  | 'tool_call' 
  | 'tool_result' 
  | 'state_change' 
  | 'checkpoint'
  | 'error';

export interface TrajectoryEvent {
  id: string;               // Unique ID (UUIDv4)
  sessionId: string;        // ID của Session
  parentId?: string;        // ID của Event liền trước (để dựng Event Tree khi Fork)
  timestamp: number;        // Unix Epoch timestamp (ms)
  type: EventType;
  payload: Record<string, any>;
  metadata: {
    tokensUsed?: number;
    latencyMs?: number;
    mode: 'standard' | 'code' | 'minimal' | 'creator';
  };
}
```

---

## 4. Các Thao Tác Cốt Lõi: Replay, Fork, Resume & Search

### 4.1. Replay (Phát lại Trajectory)
Replay cho phép tải lại toàn bộ danh sách Event từ bước 1 đến bước $N$ và tái tạo trạng thái (state) chính xác của Agent tại bất kỳ mốc thời gian nào.
- **Deterministic Replay**: Tái tạo chính xác các câu trả lời và kết quả công cụ đã lưu trong quá khứ mà không cần gọi lại LLM hay execute lại command thực tế.
- **Live Replay (Dry-run)**: Giữ nguyên lịch sử Tool Execution nhưng gọi lại LLM thế hệ mới hơn để so sánh kết quả.

### 4.2. Fork (Tách Nhánh Session)
Nếu người dùng thấy Agent đi sai hướng tại Event thứ $K$, người dùng có thể **Fork** tại Event $K$:
- Tạo một Session con (`parentSessionId`) chia sẻ lịch sử Event từ $1 \to K$.
- Mọi Event mới từ bước $K+1$ trở đi của Fork Session sẽ nằm ở một nhánh độc lập.
- Giúp người dùng thử nghiệm lời gọi prompt khác, chọn công cụ khác mà không ảnh hưởng tới Session ban đầu.

### 4.3. Resume (Tiếp Tục Phiên Làm Việc)
Tất cả trạng thái Session đều được persisted trên đĩa (disk/DB) theo cơ chế Event Sourcing. Khi hệ thống bị gián đoạn (crash, restart, network timeout), Agent có thể **Resume** lập tức từ Event cuối cùng mà không mất bất kỳ context nào.

### 4.4. Event Search (Tìm Kiếm Vết Thực Thi)
Cho phép tìm kiếm chi tiết trong Trajectory Log:
- Tìm tất cả các Tool Call bị lỗi (`status === 'error'`).
- Tìm các dòng lệnh bash đã chạy thành công chứa từ khóa `pnpm build`.
- Lọc theo lượng token sử dụng ở từng turn.

---

## 5. Triển Khai Minh Họa (TypeScript Implementation)

Dưới đây là implementation mô phỏng Engine quản lý Trajectory Event Stream:

```typescript
import { v4 as uuidv4 } from 'uuid';

export class TrajectoryEngine {
  private events: Map<string, TrajectoryEvent[]> = new Map();

  // 1. Ghi nhận Event mới
  public appendEvent(sessionId: string, type: EventType, payload: any, parentId?: string): TrajectoryEvent {
    const sessionEvents = this.events.get(sessionId) || [];
    const lastEvent = sessionEvents[sessionEvents.length - 1];

    const newEvent: TrajectoryEvent = {
      id: uuidv4(),
      sessionId,
      parentId: parentId || lastEvent?.id,
      timestamp: Date.now(),
      type,
      payload,
      metadata: { mode: 'standard' }
    };

    sessionEvents.push(newEvent);
    this.events.set(sessionId, sessionEvents);
    return newEvent;
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
    const newSessionId = `session_fork_${uuidv4().substring(0, 8)}`;

    // Tạo bản sao Event Stream cho Session mới
    const forkedEvents: TrajectoryEvent[] = historicalEvents.map(e => ({
      ...e,
      id: uuidv4(),
      sessionId: newSessionId
    }));

    // Đánh dấu checkpoint event
    const forkNotice: TrajectoryEvent = {
      id: uuidv4(),
      sessionId: newSessionId,
      parentId: forkedEvents[forkedEvents.length - 1].id,
      timestamp: Date.now(),
      type: 'checkpoint',
      payload: { message: `Forked from session ${sourceSessionId} at event ${checkpointEventId}` },
      metadata: { mode: 'standard' }
    };
    forkedEvents.push(forkNotice);

    this.events.set(newSessionId, forkedEvents);
    return { newSessionId, events: forkedEvents };
  }

  // 4. Tìm kiếm Event
  public searchEvents(sessionId: string, query: { type?: EventType; keyword?: string }): TrajectoryEvent[] {
    const sessionEvents = this.events.get(sessionId) || [];
    return sessionEvents.filter(e => {
      if (query.type && e.type !== query.type) return false;
      if (query.keyword) {
        const jsonStr = JSON.stringify(e.payload).toLowerCase();
        if (!jsonStr.includes(query.keyword.toLowerCase())) return false;
      }
      return true;
    });
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
- **Append-Only Immutability**: Không bao giờ chỉnh sửa trực tiếp các Event đã ghi. Nếu muốn rollback hay sửa đổi, hãy tạo Fork Session hoặc ghi một Event `state_change` mới.
- **Compact Payload**: Với các Tool Result trả về dữ liệu cực lớn (vd: log 10,000 dòng), hãy lưu payload ngắn gọn và trích xuất reference sang file blob để tránh làm đầy RAM/DB.
- **Regular Checkpointing**: Ghi Event type `checkpoint` sau mỗi mốc hoàn thành task quan trọng (vd: xong phase planning, xong phase refactoring) để dễ dàng Fork.

### ❌ Anti-Patterns
- **Incomplete Logging**: Chỉ lưu câu thoại chat giữa User và Agent mà không lưu các sự kiện ngầm (Context Injection, Internal Tool Calls, System Errors).
- **Non-deterministic Events**: Lưu kết quả Tool Call nhưng không lưu cấu hình environment/parameters khiến việc Replay sau này bị đứt gãy.
