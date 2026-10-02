# Knowledge: Multi-Agent Coordination (Opt-In)

> Theory: `AI-coding-skills-framework/vi/harness/09-multi-agent/` (+ `SUBAGENT.md` for
> sub-agent lifecycle/spawn/budget). This file is the **repo implementation contract**.
> Status was ❌ MISSING in `README.md` — this file + `agents/coordinator.agent.md` close the
> minimal gap without changing the strict 5-phase flow.

## When to use (and when NOT to)

Use only when Phase 2 plan explicitly marks `multi-agent: true` AND developer approves:

- 3+ independent workstreams (e.g. parallel bug fixes, feature + tests + docs), or
- a change requiring **independent verification** (maker/checker split), or
- explicit developer request for fan-out.

Do NOT use for: single-file/trivial edits, analysis-only reviews, anything that fits one
agent in P3. Default stays single-agent strict mode.

## Roles (minimal team)

| Role | Job | Must not |
|---|---|---|
| `coordinator` | Fan-out/fan-in, owns lease/deadline/quorum, aggregates report | Edit code directly |
| `implementer` | Implements ONE assigned scope in its worktree | Verify its own output as final |
| `verifier` | Runs build/test/gates, default stance REJECT until evidence | Edit code (comments only) |
| `reviewer` | Reviews diff, severity Blocker/Major/Minor | Run shell |

Cap: **max 3 sub-agents/run** (`loop/04-operating`). Empty/actionable-negative triage → no spawn.

## Spawn contract (per sub-agent)

```text
role + taskId + narrow goal + definition of done
+ files allow-list + parent summary (trimmed, never raw log)
+ tools allow-list (reviewer: read-only, no shell; implementer: sandboxed shell, no net)
+ worktree (REQUIRED for code edits) + budget {maxTokens, maxSteps, timeoutMs}
+ lease {leaseId, deadlineMs default 300s, maxAttempts 3}
```

Faults: heartbeat 5s; DEAD (>15s lost) / TIMED_OUT / SUSPECT (>60s no progress) →
freeze lease (fencing token++), requeue with prior transcript, `attempts > 3` → escalate
to developer / fail closed.

## Shared-memory / blackboard rules

- Private scratchpad by default (`agent_id/task_id/*`); publish only diffs/facts.
- **Single-writer per file/section** (coordinator assigns; reviewer never edits code).
- Cross-agent reads via allow-listed projections only; never leak raw prompts/secrets.
- Blackboard storage = `.github/reports/` (`*.ctx.md` per agent + one aggregated report in P5).
- Concurrency: `isolation: worktree` for every code-editing sub-agent + lock/queue in state
  (`"PR #1234 — worktree in progress"`); two sub-agents never edit the same files.
- Secrets: short lease (5–15 min, scoped), redact `sk-*, ghp_*, AWS_*` before logging;
  one agent's secret never appears in another agent's context.

## Mapping to the 5 phases (phase-gated, no preload)

- **P1 Understanding**: coordinator routes workflow, loads knowledge + ONE matching skill,
  pulls Jira/Figma context once. No fan-out yet.
- **P2 Planning**: plan lists scopes, owners, worktrees, budgets, quorum (default 2-of-3 for
  votes). `multi-agent: true` requires explicit developer approval + frozen decisions.
- **P3 Execution**: implementers work isolated in worktrees; run `lint + format` per scope.
- **P4 Validation**: verifier runs `build + test` + AC trace per scope; coordinator aggregates;
  fail → targeted retry (idempotent), not full-pipeline retry.
- **P5 Report**: ONE aggregated report (template + content-hash + `REPORTS.md` row + Jira sync)
  plus per-agent `*.ctx.md` for future context. No report = incomplete.

## Forbidden

- Same agent implements AND verifies (confirmation bias).
- Full sub-agent chain on empty/noisy triage (cost spike).
- Preloading all phases/skills "just in case" (violates phase-gated loading).
- Retrying irreversible side effects without outbox + fencing guard.
