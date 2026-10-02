# Knowledge: Multi-Agent Coordination (Opt-In)

> Theory: `AI-coding-skills-framework/vi/harness/09-multi-agent/` (+ `SUBAGENT.md`).
> Repo contract for the `.agents` (Cline/general) flavor. Strict 5-phase flow is unchanged.

## When to use (and when NOT to)

Use only when the Phase 2 plan sets `multi-agent: true` AND the developer approves it:

- 3+ independent workstreams, or independent verification needed (maker/checker), or
- developer explicitly asks for fan-out.

Otherwise stay single-agent. Trivial/single-file/analysis-only work never fans out.

## Roles

`coordinator` (fan-out/fan-in, owns lease/quorum, no direct edits) ·
`implementer` (one scope, own worktree) · `verifier` (build/test/gates, stance REJECT,
comments only) · `reviewer` (diff review, no shell). Cap **max 3 sub-agents/run**.

## Spawn contract

`role + taskId + narrow goal + definition of done + files allow-list + trimmed parent
summary + tools allow-list + worktree (required for code edits) + budget
{maxTokens, maxSteps, timeoutMs} + lease {leaseId, deadlineMs 300s default, maxAttempts 3}`.
Heartbeat 5s; DEAD (>15s)/TIMED_OUT/SUSPECT (>60s stall) → fencing token++, requeue with
transcript, `attempts > 3` → escalate / fail closed.

## Shared memory

Private scratchpad (`agent_id/task_id/*`); publish diffs/facts only; single-writer per
file/section; cross-agent reads via allow-listed projections. Blackboard =
`.agents/reports/` (per-agent `*.ctx.md` + ONE aggregated P5 report). Worktree isolation +
lock/queue (`"PR #1234 — worktree in progress"`). Secrets: 5–15 min scoped lease, redact
`sk-*, ghp_*, AWS_*`, never cross-leak; deny-by-default egress with per-agent allow-list.

## Phase mapping

P1 route (no fan-out) → P2 plan with scopes/owners/worktrees/budgets/quorum (default 2-of-3)
+ approval gate → P3 isolated execution (`lint + format` per scope) → P4 aggregated
validation (`build + test` + AC trace; targeted retry only) → P5 one aggregated report +
per-agent `*.ctx.md`. No report = incomplete.

## Forbidden

Same agent implements AND verifies; full chain on empty triage; preloading future phases;
retrying irreversible effects without outbox + fencing guard.
