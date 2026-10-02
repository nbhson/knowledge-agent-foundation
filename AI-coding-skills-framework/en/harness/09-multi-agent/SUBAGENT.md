# Sub-Agent — Lifecycle, Spawn, Permissions and Budget Spec

> Companion to `README.md` (especially §16 Fault tolerance/Messaging/Isolation).
> Consolidates sub-agent conventions scattered across `loop/01-concepts` (§2.5 Maker/Checker),
> `loop/02-patterns/*` (verifier/reviewer), `loop/04-operating` (cost guards),
> `loop/06-anti-patterns`, and the Claude Code example in `README.md §16.5`.

## 1. Definitions

* **Agent**: entity running the full harness loop (01→11), owning a task and memory.
* **Sub-agent**: child agent spawned by a parent (or orchestrator) for **one narrow task**,
  running the same harness but with **trimmed context + narrowed tools + own budget + lease**.
* **Loop**: scheduled loop (cron) that may spawn sub-agents on each run (`loop/05-multi-loop`).

Rule: without a lease + deadline + own budget + own tool allow-list, it is not a
sub-agent — just a function call.

## 2. Role taxonomy

| Role | Does | Must not |
|---|---|---|
| `implementer` / `maker` | Writes code in the assigned worktree | Self-merge, final self-verify |
| `verifier` / `checker` | Runs tests, gates, rubric (default stance REJECT) | Edit code directly (comments only) |
| `reviewer` | Reviews diffs, severity Blocker/Major/Minor | Run shell, write files outside comments |
| `researcher` / `triage` | Reads code/docs, returns facts + `file:line` citations | Change behavior, write long-term memory |

Forbidden anti-pattern (`loop/06-anti-patterns`): same agent implements AND verifies
→ confirmation bias, weak tests get rubber-stamped.

## 3. Lifecycle

```text
spawn (with §4 spec) → 5s heartbeat → progress stream
  → done (artifact + trimmed transcript)
  → fault: DEAD (heartbeat lost >15s) / TIMED_OUT (deadline exceeded) / SUSPECT (alive, no progress >60s)
  → requeue (fencing token++, attempt++, prior transcript attached) → >3 attempts → escalate / fail closed
```

* Every task has `lease_id + deadlineMs + max_attempts` (default 300s deadline, max 3).
* Stateless supervisor backed by a queue (Redis/BullMQ); workers must be idempotent
  for safe requeue retries. Judge/voter quorum: 2f+1 tolerates f faults, majority required (e.g. 2/3).
* Implementation: `README.md §16.1–16.2` (heartbeat + reassignment sample).

## 4. Spawn API (minimum contract)

```typescript
interface SubAgentSpec {
  role: "implementer" | "verifier" | "reviewer" | "researcher";
  taskId: string;
  goal: string;              // narrow, single job, with definition of done
  context: {                 // NEVER dump the full parent context
    files: string[];
    artifactRefs: { path: string; hash: string }[];
    parentSummary: string;   // trimmed parent transcript, not raw log
  };
  tools: string[];           // narrowed allow-list from the role matrix in 12-sandbox §6
  worktree?: string;         // REQUIRED for code-editing sub-agents
  budget: { maxTokens: number; maxSteps: number; timeoutMs: number };
  lease: { leaseId: number; deadlineMs: number; maxAttempts: number };
  secrets?: { scope: string; ttlMinutes: number }; // 5–15m, env injection, redact before logging
}
```

Spawn rules (`loop/04-operating`): cheap triage first, spawn only when state reports
actionable work; empty watchlist → exit <5k tokens, no spawn. **Max 3 sub-agents/run** by default.

## 5. Context and memory

* **Private by default:** each sub-agent has its own scratchpad; publishes only diffs/facts
  to the shared blackboard via `blackboard.write(key, value, expectedVersion)` (CAS semantics).
* **Single-writer:** orchestrator assigns file/section ownership (e.g. only `coder` writes `auth.ts`).
* **Namespaced:** keys under `agent_id/task_id/*`; cross-agent reads via allow-listed
  projections only (`README.md §16.3`).

## 6. Isolation and secrets

* Tiers/controls/runners belong to `12-sandbox-execution` §2–§6; the multi/sub-agent
  addition is: **least tools per role** (reviewer: read-only FS, no shell; coder: sandboxed
  shell, no net), resolved from the same role matrix so solo and swarm runs resolve to the
  same policy for the same role.
* Secrets are **per-agent leases** (short-lived scoped tokens), supervisor redacts
  `sk-*, ghp_*, AWS_*` from logs/transcripts; one agent's secret never appears in another
  agent's context (`README.md §16.4`).
* Deny-by-default egress with per-agent domain allow-list; every tool I/O audited with
  `agent_id + lease_id`.
* Code-editing sub-agents: `isolation: worktree` + lock/queue in state
  (`"PR #1234 — worktree in progress"`) so two sub-agents never edit the same files.

## 7. Result aggregation

* Maker/checker: implementer finishes → independent verifier runs tests/gates; default
  verdict REJECT until evidence is sufficient (build OK, tests OK, AC traced).
* Quorum: reviewers vote 2-of-3; one crashed voter never blocks merge.
* Payload: 64KB header + 512KB body caps; larger → artifact ref. Messages carry `msg_id`
  (dedupe), per-task FIFO (reject out-of-order `seq`), 30s request/reply timeout.

## 8. Checklist

[ ] Full §4 spec (narrow role, trimmed context, tool allow-list, worktree for code edits,
budget/timeout/lease) [ ] heartbeat + deadline + hang detector [ ] fencing token on requeue
[ ] max 3 attempts + escalation path [ ] CAS + single-writer + namespacing [ ] short secret
leases + redaction + no cross-leak [ ] max 3 spawns/run + cost kill switch [ ] independent
verifier, never self-verify.
