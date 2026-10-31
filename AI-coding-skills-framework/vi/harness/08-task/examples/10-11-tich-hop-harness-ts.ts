export type TaskStatus = "pending"|"planning"|"in_progress"|"waiting_approval"|"testing"|"review"|"done"|"failed"|"cancelled";
export interface TaskNode { id: string; title: string; trajectoryId: string; idempotencyKey: string;
  permissions: "read"|"write"|"elevated"; budgetTokens: number; timeoutMs: number; maxRetries: number;
  deps: string[]; status: TaskStatus; resultRef?: string; }
export interface TaskEngine { submit(t: Omit<TaskNode,"trajectoryId"|"idempotencyKey"|"status">): TaskNode;
  transition(id: string, to: TaskStatus, note?: string): void; on(evt: string, fn: (e: any) => void): void; }
export function makeTaskEngine(): TaskEngine {
  const tasks = new Map<string, TaskNode>(); const ls: Record<string, Function[]> = {};
  const emit = (e: string, d: any) => (ls[e] ?? []).forEach(f => f(d));
  const VALID: Record<string, TaskStatus[]> = { pending: ["planning","cancelled"], planning: ["in_progress","cancelled"],
    in_progress: ["testing","waiting_approval","failed","done"], waiting_approval: ["in_progress","cancelled"],
    testing: ["review","in_progress","failed"], review: ["done","in_progress","failed"] };
  return {
    submit(t) { const n: TaskNode = { ...t, trajectoryId: `traj_${Date.now().toString(36)}_${t.id}`, idempotencyKey: `${t.id}:${t.title.length}`, status: "pending" };
      tasks.set(n.id, n); emit("task.created", n); return n; },
    transition(id, to, note) { const cur = tasks.get(id)!; if (!VALID[cur.status]?.includes(to)) throw new Error(`invalid ${cur.status}→${to}`);
      cur.status = to; emit("task.transition", { id, to, note, trajectoryId: cur.trajectoryId }); },
    on(e, f) { (ls[e] ??= []).push(f); },
  };
}
