type AgentState = "IDLE" | "RUNNING" | "SUSPECT" | "DEAD";
interface TaskLease { taskId: string; leaseId: number; deadlineMs: number; attempts: number; }

const HEARTBEAT_TTL_MS = 15_000, PROGRESS_STALL_MS = 60_000, MAX_ATTEMPTS = 3;
const heartbeats = new Map<string, { ts: number; progressTs: number; state: AgentState }>();

export function heartbeat(agentId: string, progressed: boolean): void {
  const h = heartbeats.get(agentId) ?? { ts: 0, progressTs: Date.now(), state: "IDLE" as AgentState };
  h.ts = Date.now(); if (progressed) h.progressTs = h.ts;
  h.state = "RUNNING"; heartbeats.set(agentId, h);
}

export async function supervise(agentId: string, lease: TaskLease,
  requeue: (l: TaskLease) => Promise<void>, escalate: (l: TaskLease) => Promise<void>): Promise<void> {
  const h = heartbeats.get(agentId); const now = Date.now();
  if (!h || now - h.ts > HEARTBEAT_TTL_MS) return handleFault(agentId, lease, "DEAD", requeue, escalate);
  if (now > lease.deadlineMs) return handleFault(agentId, lease, "TIMED_OUT", requeue, escalate);
  if (now - h.progressTs > PROGRESS_STALL_MS) return handleFault(agentId, lease, "SUSPECT", requeue, escalate);
}

async function handleFault(agentId: string, lease: TaskLease, reason: string,
  requeue: (l: TaskLease) => Promise<void>, escalate: (l: TaskLease) => Promise<void>) {
  console.warn(`[supervisor] ${agentId} fault=${reason} task=${lease.taskId} attempt=${lease.attempts}`);
  heartbeats.set(agentId, { ts: 0, progressTs: 0, state: "DEAD" });
  const next: TaskLease = { ...lease, leaseId: lease.leaseId + 1, attempts: lease.attempts + 1,
    deadlineMs: Date.now() + 300_000 };
  if (next.attempts > MAX_ATTEMPTS) return escalate(next);
  return requeue(next); // đính kèm transcript trước đó tại nơi gọi để giữ liên tục
}
