/**
 * DeepSeek Harness - Trajectory Traceability Engine
 * 
 * Core philosophy: "Agent = Model + Harness"
 * Everything is traceable, replayable, and forkable.
 */

// ═══════════════════════════════════════════════
// 1. SESSION EVENT STREAM (Append-only log)
// ═══════════════════════════════════════════════

interface SessionEvent {
  id: string;              // UUID
  step: number;            // Monotonically increasing
  timestamp: number;       // Unix ms
  type: EventType;
  payload: EventPayload;
  metadata: EventMetadata;
}

type EventType = 
  | "user_prompt"          // User input
  | "model_thought"        // LLM reasoning (hidden)
  | "tool_call"            // Tool invocation
  | "tool_result"          // Tool output
  | "model_output"         // Final LLM response
  | "state_change"         // Harness state mutation
  | "checkpoint";          // Manual/auto checkpoint

interface EventPayload {
  // user_prompt
  text?: string;
  attachments?: Attachment[];
  
  // model_thought
  reasoning?: string;
  confidence?: number;
  
  // tool_call
  tool_name?: string;
  args?: Record<string, any>;
  call_id?: string;
  
  // tool_result
  result?: any;
  error?: string;
  duration_ms?: number;
  
  // model_output
  content?: string;
  finish_reason?: string;
  
  // state_change
  path?: string;           // JSON path in state
  old_value?: any;
  new_value?: any;
  
  // checkpoint
  label?: string;
  description?: string;
}

interface EventMetadata {
  session_id: string;
  parent_step?: number;    // For forked sessions
  fork_id?: string;        // Fork identifier
  tags?: string[];         // e.g., ["debug", "critical"]
  cost_usd?: number;       // Token cost estimate
}

// ═══════════════════════════════════════════════
// 2. TRAJECTORY STORE (Persistence layer)
// ═══════════════════════════════════════════════

class TrajectoryStore {
  private events: SessionEvent[] = [];
  private checkpoints: Map<string, number> = new Map(); // label -> step
  
  append(event: SessionEvent): void {
    this.events.push(event);
  }
  
  getEvents(sessionId: string, fromStep?: number): SessionEvent[] {
    return this.events.filter(e => 
      e.metadata.session_id === sessionId && 
      (fromStep === undefined || e.step >= fromStep)
    );
  }
  
  getEventByStep(sessionId: string, step: number): SessionEvent | undefined {
    return this.events.find(e => 
      e.metadata.session_id === sessionId && e.step === step
    );
  }
  
  createCheckpoint(sessionId: string, label: string): void {
    const latestStep = this.getLatestStep(sessionId);
    this.checkpoints.set(`${sessionId}:${label}`, latestStep);
  }
  
  getCheckpoint(sessionId: string, label: string): number | undefined {
    return this.checkpoints.get(`${sessionId}:${label}`);
  }
  
  private getLatestStep(sessionId: string): number {
    const sessionEvents = this.events.filter(
      e => e.metadata.session_id === sessionId
    );
    return sessionEvents.length > 0 
      ? Math.max(...sessionEvents.map(e => e.step)) 
      : 0;
  }
}

// ═══════════════════════════════════════════════
// 3. REPLAY ENGINE (Core innovation)
// ═══════════════════════════════════════════════

class ReplayEngine {
  constructor(
    private store: TrajectoryStore,
    private model: ModelProvider,
    private toolRegistry: ToolRegistry
  ) {}
  
  /**
   * Replay session from beginning up to a specific step.
   * Returns the state at that step.
   */
  async replayToStep(sessionId: string, targetStep: number): Promise<AgentState> {
    const events = this.store.getEvents(sessionId);
    let state = this.initialState();
    
    for (const event of events) {
      if (event.step > targetStep) break;
      state = await this.applyEvent(state, event);
    }
    
    return state;
  }
  
  /**
   * Fork a session at a specific step.
   * Creates a new session that shares history up to fork point.
   */
  async forkSession(
    sessionId: string, 
    forkStep: number, 
    newPrompt?: string
  ): Promise<string> {
    const newSessionId = `fork_${sessionId}_${forkStep}_${Date.now()}`;
    
    // Copy events up to fork step
    const history = this.store.getEvents(sessionId, 0, forkStep);
    for (const event of history) {
      const forkedEvent = {
        ...event,
        id: uuid(),
        metadata: {
          ...event.metadata,
          session_id: newSessionId,
          parent_step: forkStep,
          fork_id: newSessionId
        }
      };
      this.store.append(forkedEvent);
    }
    
    // Optionally add new prompt to continue from fork
    if (newPrompt) {
      this.store.append({
        id: uuid(),
        step: forkStep + 1,
        timestamp: Date.now(),
        type: "user_prompt",
        payload: { text: newPrompt },
        metadata: { session_id: newSessionId, fork_id: newSessionId }
      });
    }
    
    return newSessionId;
  }
  
  /**
   * Resume a session from a checkpoint or step.
   * Continues execution from that point.
   */
  async resumeSession(
    sessionId: string, 
    fromStep: number,
    newInput?: string
  ): Promise<AgentState> {
    // Get state at resume point
    const state = await this.replayToStep(sessionId, fromStep);
    
    // If new input provided, continue from there
    if (newInput) {
      return this.continueFromState(sessionId, state, newInput);
    }
    
    return state;
  }
  
  private async applyEvent(state: AgentState, event: SessionEvent): Promise<AgentState> {
    switch (event.type) {
      case "tool_call":
        return await this.executeTool(state, event);
      case "model_thought":
        return { ...state, lastThought: event.payload.reasoning };
      case "state_change":
        return this.applyStateChange(state, event);
      default:
        return state;
    }
  }
  
  private async continueFromState(
    sessionId: string, 
    state: AgentState, 
    input: string
  ): Promise<AgentState> {
    // Continue agent loop from restored state
    // ... implementation
    return state;
  }
  
  private initialState(): AgentState {
    return { history: [], tools: {}, memory: {} };
  }
}

// ═══════════════════════════════════════════════
// 4. EVENT SEARCH & ANALYTICS
// ═══════════════════════════════════════════════

class TrajectoryAnalytics {
  constructor(private store: TrajectoryStore) {}
  
  /**
   * Search events across all sessions.
   * Supports: full-text, type filter, time range, cost range.
   */
  searchEvents(query: SearchQuery): SessionEvent[] {
    let results = this.store.events;
    
    if (query.session_id) {
      results = results.filter(e => e.metadata.session_id === query.session_id);
    }
    if (query.type) {
      results = results.filter(e => e.type === query.type);
    }
    if (query.text) {
      const text = query.text.toLowerCase();
      results = results.filter(e => 
        JSON.stringify(e.payload).toLowerCase().includes(text)
      );
    }
    if (query.from_step !== undefined) {
      results = results.filter(e => e.step >= query.from_step!);
    }
    if (query.to_step !== undefined) {
      results = results.filter(e => e.step <= query.to_step!);
    }
    if (query.max_cost !== undefined) {
      results = results.filter(e => 
        (e.metadata.cost_usd ?? 0) <= query.max_cost!
      );
    }
    
    return results;
  }
  
  /**
   * Get cost breakdown by event type.
   */
  getCostBreakdown(sessionId: string): Record<string, number> {
    const events = this.store.getEvents(sessionId);
    const breakdown: Record<string, number> = {};
    
    for (const event of events) {
      const cost = event.metadata.cost_usd ?? 0;
      breakdown[event.type] = (breakdown[event.type] ?? 0) + cost;
    }
    
    return breakdown;
  }
  
  /**
   * Find common failure patterns.
   */
  findFailurePatterns(): FailurePattern[] {
    const toolErrors = this.store.events.filter(
      e => e.type === "tool_result" && e.payload.error
    );
    
    // Group by tool + error type
    const groups = new Map<string, SessionEvent[]>();
    for (const event of toolErrors) {
      const key = `${event.payload.tool_name}:${event.payload.error}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(event);
    }
    
    return Array.from(groups.entries())
      .map(([pattern, events]) => ({
        pattern,
        count: events.length,
        sessions: [...new Set(events.map(e => e.metadata.session_id))],
        first_seen: Math.min(...events.map(e => e.timestamp)),
        last_seen: Math.max(...events.map(e => e.timestamp))
      }))
      .sort((a, b) => b.count - a.count);
  }
}

interface SearchQuery {
  session_id?: string;
  type?: EventType;
  text?: string;
  from_step?: number;
  to_step?: number;
  max_cost?: number;
}

interface FailurePattern {
  pattern: string;
  count: number;
  sessions: string[];
  first_seen: number;
  last_seen: number;
}
