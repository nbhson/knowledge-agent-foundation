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
