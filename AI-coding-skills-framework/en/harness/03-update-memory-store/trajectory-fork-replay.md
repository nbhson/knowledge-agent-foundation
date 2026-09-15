# 🔄 Trajectory Traceability Engine — Session Event Stream, Fork, Replay & Resume

> **Pattern inherited from DeepSeek Harness**: The system manages the entire execution trace (trajectory) as a **Session Event Stream**, supporting 100% traceability, Replay for audit/debug, and Fork/Resume to experiment with multiple solution branches without corrupting the original history.

---

## 📑 Contents

- [1. Context & Motivation](#1-context-&-motivation)
- [2. Trajectory Traceability Engine Philosophy](#2-trajectory-traceability-engine-philosophy)
- [3. Session Event Stream Architecture](#3-session-event-stream-architecture)
- [4. Core Operations: Replay, Fork, Resume & Search](#4-core-operations-replay-fork-resume-&-search)
  - [4.1. Replay (Replaying a Trajectory)](#41-replay-replaying-a-trajectory)
  - [4.2. Fork (Branching a Session)](#42-fork-branching-a-session)
  - [4.3. Resume (Continuing a Work Session)](#43-resume-continuing-a-work-session)
  - [4.4. Event Search (Searching Execution Traces)](#44-event-search-searching-execution-traces)
- [5. Illustrative Implementation (TypeScript Implementation)](#5-illustrative-implementation-typescript-implementation)
- [6. DeepSeek Harness Case Study: Trajectory Viewer & Event Inspector](#6-deepseek-harness-case-study-trajectory-viewer-&-event-inspector)
- [7. Best Practices & Anti-Patterns](#7-best-practices-&-anti-patterns)

---

## 1. Context & Motivation

In complex AI agent systems (especially AI Coding Agents), a single interaction session can span dozens of turns, call hundreds of tools (file search, edit, terminal, git), and generate a huge amount of context.

**Common problems with traditional agents:**
- **Black-box Execution**: When an agent fails at step 15, the user cannot tell which step the error came from (a bad prompt, a tool returning a faulty result, or an LLM reasoning error).
- **No State Undo/Branching**: If the agent goes down the wrong path at step 10, the only option is to delete the entire session and start over from scratch.
- **Hard Debugging & Evaluation**: You cannot replay the exact sequence of events that occurred to reproduce a bug or benchmark a model.

---

## 2. Trajectory Traceability Engine Philosophy

DeepSeek Harness solves the problems above with the **Full Traceability** philosophy:

```
Agent Execution = Sequence of State-Changing Events (Event Stream)
```

Instead of storing a conversation as a flat list of messages (`[{role, content}]`), the system stores it as an **Append-Only Event Stream**. Every action, tool result, state change, and prompt injection is recorded as an Event with a timestamp and a unique ID.

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

## 3. Session Event Stream Architecture

Every Event in the Trajectory contains standardized information:

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
  sessionId: string;        // The session ID
  parentId?: string;        // ID of the immediately preceding Event (to build the Event Tree when forking)
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

## 4. Core Operations: Replay, Fork, Resume & Search

### 4.1. Replay (Replaying a Trajectory)
Replay loads back the full list of Events from step 1 to step $N$ and reconstructs the exact state of the agent at any point in time.
- **Deterministic Replay**: Exactly reproduces answers and tool results stored in the past without calling the LLM again or re-executing real commands.
- **Live Replay (Dry-run)**: Keeps the tool execution history but calls a newer-generation LLM to compare results.

### 4.2. Fork (Branching a Session)
If the user sees the agent going down the wrong path at Event $K$, the user can **Fork** at Event $K$:
- Create a child session (`parentSessionId`) that shares the Event history from $1 \to K$.
- All new Events in the fork session from step $K+1$ onward live on an independent branch.
- Lets the user experiment with different prompt calls or different tools without affecting the original session.

### 4.3. Resume (Continuing a Work Session)
All session state is persisted to disk/DB using an Event Sourcing mechanism. When the system is interrupted (crash, restart, network timeout), the agent can **Resume** immediately from the last event without losing any context.

### 4.4. Event Search (Searching Execution Traces)
Allows searching inside the Trajectory Log:
- Find all failed Tool Calls (`status === 'error'`).
- Find bash commands that ran successfully and contain the keyword `pnpm build`.
- Filter by the amount of tokens used per turn.

---

## 5. Illustrative Implementation (TypeScript Implementation)

Below is a simulated implementation of an engine that manages the Trajectory Event Stream:

```typescript
import { v4 as uuidv4 } from 'uuid';

export class TrajectoryEngine {
  private events: Map<string, TrajectoryEvent[]> = new Map();

  // 1. Record a new Event
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
    const newSessionId = `session_fork_${uuidv4().substring(0, 8)}`;

    // Create a copy of the Event Stream for the new session
    const forkedEvents: TrajectoryEvent[] = historicalEvents.map(e => ({
      ...e,
      id: uuidv4(),
      sessionId: newSessionId
    }));

    // Mark the checkpoint event
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

  // 4. Search Events
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

In the DeepSeek Harness Web UI (running on port `3080`), the **Trajectory View** feature provides an intuitive interface that lets engineers:
1. **Visual Timeline**: View the session's timeline with color blocks corresponding to Reasoning, Tool Calls (Bash/Edit), and Execution Results.
2. **One-Click Replay**: Click any node in the timeline to replay the exact dialogue and context at that point.
3. **Fork & Branch**: The "Fork Session from here" button branches immediately from the web interface, creating a safe experimentation environment.

---

## 7. Best Practices & Anti-Patterns

### ✅ Best Practices
- **Append-Only Immutability**: Never directly edit Events that have already been recorded. If you want to roll back or modify, create a Fork Session or record a new `state_change` Event.
- **Compact Payloads**: For Tool Results that return huge amounts of data (e.g. a 10,000-line log), store a compact payload and extract a reference to a blob file to avoid filling up RAM/DB.
- **Regular Checkpointing**: Record Events of type `checkpoint` after each completion of an important task milestone (e.g. end of the planning phase, end of the refactoring phase) to make forking easy.

### ❌ Anti-Patterns
- **Incomplete Logging**: Only storing the chat dialogue between user and agent while failing to record background events (Context Injection, Internal Tool Calls, System Errors).
- **Non-deterministic Events**: Storing Tool Call results but not storing the environment/parameters configuration, which breaks future Replay.
