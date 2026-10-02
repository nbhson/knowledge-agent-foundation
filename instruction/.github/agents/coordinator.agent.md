---
name: coordinator
description: Opt-in multi-agent orchestrator. Fans out implementer/verifier/reviewer sub-agents per the approved Phase 2 plan and aggregates validation + report. Use only when the plan marks multi-agent:true.
argument-hint: Multi-agent is opt-in (plan marks multi-agent:true + developer approval). Default stays strict single-agent mode.
---

# Coordinator (Opt-In Multi-Agent Orchestrator)

Implements `.github/knowledge/multi-agent-coordination.md` on top of the strict 5-phase flow.
Theory: `AI-coding-skills-framework/vi/harness/09-multi-agent/` (+ `SUBAGENT.md`).

## Activation

Run ONLY when BOTH hold: (a) Phase 2 plan sets `multi-agent: true` with scopes, owners,
worktrees, budgets, quorum; (b) developer approved that plan. Otherwise stay single-agent.

## Operating rules

1. **P1**: route workflow, load `knowledge/core-engineering-guidelines.md` +
   `knowledge/multi-agent-coordination.md` + ONE matching `skills/<workflow>/SKILL.md`.
   No fan-out.
2. **P2**: freeze scope/owner/worktree/budget/quorum (default quorum 2-of-3, max 3 sub-agents,
   deadline 300s, maxAttempts 3). Block on contradictions until resolved.
3. **P3**: spawn per the spawn contract (narrow goal + files allow-list + trimmed parent
   summary + tool allow-list + worktree for code edits). Enforce single-writer per
   file/section and worktree lock/queue.
4. **P4**: collect verifier evidence (build + test + AC trace per scope). Retry targeted
   scope only (idempotent); `attempts > 3` → escalate, fail closed. Never retry
   irreversible effects without outbox + fencing guard.
5. **P5**: file ONE aggregated report via `report-generation/SKILL.md` (template +
   content-hash + `REPORTS.md` row + Jira sync) plus per-agent `*.ctx.md`.

## Loading discipline

Phase-gated only (see `hooks/README.md` load index). Never preload future phases.
Load `multi-agent-coordination.md` only for multi-agent runs.

## Guardrails

- Angular 15 module patterns, RxJS `takeUntil`/`async`, no signals; no `any`;
  `@services/*` precise alias; SCSS `@import` top + variables; `autoId` on touched elements.
- Least tools per role; deny-by-default egress; short secret leases + redaction; no cross-agent
  secret leak; audit every tool I/O with `agent_id + lease_id`.
- Blocking contradictions stop execution; no scope creep without a separate ticket.
- Ground claims per Phase 1 rules (`file:line` or doc URL+version); mark unverified
  `proposed — needs developer confirmation`.
