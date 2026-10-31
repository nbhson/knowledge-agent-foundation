import { ulid } from 'ulid';

export class TrajectoryEngine {
  private events: Map<string, TrajectoryEvent[]> = new Map();

  // 1. Record a new Event (seq is gapless and monotonic per session)
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

  // 2. Replay the session to a desired step
  public replayToStep(sessionId: string, targetEventId: string): TrajectoryEvent[] {
    const sessionEvents = this.events.get(sessionId) || [];
    const index = sessionEvents.findIndex(e => e.id === targetEventId);
    if (index === -1) throw new Error(`Event ID ${targetEventId} not found in session ${sessionId}`);

    return sessionEvents.slice(0, index + 1);
  }

  // 3. Fork a session from a checkpoint
  public forkSession(sourceSessionId: string, checkpointEventId: string): { newSessionId: string; events: TrajectoryEvent[] } {
    const historicalEvents = this.replayToStep(sourceSessionId, checkpointEventId);
    const newSessionId = `session_fork_${ulid()}`;

    // Shared prefix: re-keyed into the fork session, sequence preserved
    const forkedEvents: TrajectoryEvent[] = historicalEvents.map((e, i) => ({
      ...e,
      id: `evt_${ulid()}`,
      sessionId: newSessionId,
      seq: i,
    }));

    // Register the prefix BEFORE appending, so append() derives the checkpoint's
    // seq from the real length. Appending first would mint seq 0 and collide
    // with the first copied event — exactly what findOrphans() would flag.
    this.events.set(newSessionId, forkedEvents);

    // Record the fork as a checkpoint event, not as an implicit copy
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

  // 4. Search Events (typed filter; see 13 §6.1 for the production SQL catalog)
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

  // 5. Gap detection — a missing seq means a lost write, not a lost thought (13 §4.3)
  public findOrphans(sessionId: string): number[] {
    const seqs = (this.events.get(sessionId) || []).map(e => e.seq);
    const gaps: number[] = [];
    for (let i = 0; i < seqs.length; i++) if (seqs[i] !== i) gaps.push(i);
    return gaps;
  }
}
