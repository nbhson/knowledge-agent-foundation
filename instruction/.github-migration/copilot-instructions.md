---
name: 'Workspace Instructions'
description: 'Global 5-phase routing for Horizon 2 UI (strict mode default).'
---

# Workspace Custom Instructions: Horizon 2 UI

---

**Priority — Strict 5-phase routing (phase-gated loading)**

Strict mode is the DEFAULT. When handling developer requests, Copilot routes
the workflow type first (New Feature / Bug Fix / Refactor / Unit Test / Code Review /
Jira Ticket Investigate), then follows the phase matrix in `.github/phases/README.md`
(+ machine-readable mirror in `.github/phases/session.json`)
in order — full P1→P5 for code-delivery, P1+P5 for analysis-only.

Load ONLY what the current phase needs per the load index in
`.github/phases/README.md` (one skill + knowledge + one template at a time).
Path-scoped rules auto-attach from `.github/instructions/*.instructions.md`
(`angular15` for `**/*.{ts,html}`, `scss` for `**/*.scss`, `angular-tests` for
`**/*.spec.ts`) — do not repeat them here.
Strict means no skipped gates — not preloading every file upfront.
Every code change ends with a Phase 5 report (template + stable content-hash +
`REPORTS.md` row + Jira sync or manual steps).

> These are **conventions** (prompt guidance), not enforced gates: nothing here
> executes code or blocks tools by itself. Executable automation lives in
> `.github/hooks/`:
> - `phase-gates.json` (+ `phase-guard.sh`/`.ps1`) — real Copilot hooks
>   (`sessionStart` injects routing context, `preToolUse` enforces the Phase 2
>   approval gate, `postToolUse` reminds lint/format, `sessionEnd`/`errorOccurred`
>   point back to the phase index). `touch .github/PHASE2_APPROVED` after the
>   developer approves a non-trivial plan (file is gitignored, never committed).
> - `report-lifecycle.sh` — report archive/delete + manifest verify. Run
>   on demand (`bash .github/hooks/report-lifecycle.sh`). Not coupled
>   to npm lifecycle.
> Cloud-agent note: hooks run non-interactively in an ephemeral Linux sandbox
> (only `bash` honored, outbound network firewalled, files discarded at job end);
> a `preToolUse` decision of `ask` is treated as `deny`, and command-hook
> timeouts are fail-open — so the Jira fallback below must be
> manual steps, never interactive prompts.

---

## Developer Workflow Convention

Before making code changes, Copilot follows these workflow phases in order and
does not skip the planning/review step. (Full visual flowchart for humans:
`phases/DIAGRAM.md` — reference only, not loaded per phase.)

> **Routing source of truth:** `phases/session.json` → `workflow_phase_config`
> (machine-readable, authoritative). `phases/README.md` is its human-readable
> mirror. Do NOT copy the routing table elsewhere — link here instead.
> Summary: code-delivery workflows (new-feature, bug-fix, refactor, unit-test)
> run full P1→P5; analysis-only (code-review, jira-ticket-investigate) run
> P1+P5 only (`skip_phases` in session.json). Template + report filename mapping
> lives in exactly one place: `skills/libs/shared/report-generation/SKILL.md` §1.

Phase order: P1 Understanding → P2 Planning → P3 Execution & Formatting →
P4 Validation & PR → P5 Report Generation. Post-merge sync runs after merge.

Key conventions:

- **Approval gate** (non-trivial: ≥2 files, behavior change, or shared surface —
  threshold table in `phases/phase-2-planning.md`): present a draft plan and
  wait for developer approval before editing. Trivial/no-code queries present a
  brief plan and may proceed without a pause.
- **Contradiction gate** (before planning): list conflicts between ticket, design,
  and clarifications; obtain developer decisions; freeze the final interpretation
  before drafting implementation details. Blocked until resolved.
- **Phase 4 validation gate needs all four**: build passes, tests pass, every
  Jira Acceptance Criterion traced ✅, every frozen contradiction decision
  applied ✅ — each traced to implementation/tests. Build+test green alone is
  NOT sufficient.
- **Reviewer** (review code diffs) runs in Phase 4 for every code-delivery
  workflow — it is an in-place check, not a separate pass.
- Routing source of truth: `phases/session.json` → `workflow_phase_config`
  (authoritative). Real enforcement (where the harness supports it) is
  `.github/hooks/phase-gates.json`.

### MCP Availability & Degradation Mode

The Jira integration has an explicit `Available?` decision with a fallback. **No task ever blocks on a missing MCP connection.** The workflow degrades gracefully:

| Mode | Jira | Behavior |
| :--- | :--- | :--- |
| **Full** | ✅ | Fully automatic: fetch ticket, sync Jira |
| **Manual** | ❌ | Ask dev to paste ticket summary (AC, description) → run as pre-MCP workflow with manual info |

**General rules:**
1. When the Jira server is unreachable, ask the developer **once** for the ticket summary. Do not ask repeatedly.
2. Record in the report under `MCP Status` — whether Jira was usable or fell back to manual, and why.
3. Fallback **does not change the 5-phase order** — it only changes the context source.
4. When Jira is unreachable, Acceptance Criteria come from the dev-provided ticket summary; Phase 4 must still trace each AC to implementation/tests.

---

## Strict Mode (Default)

Strict mode is the default for all requests. The agent follows the full ordered
phases, the Phase 2 approval gate, and the contradiction gate before
implementation begins. The `h2-standard` agent is the default agent.

## Quick Mode (Express — Opt-In Light Mode)

Quick mode is NOT the default and has exactly ONE entry point:

| Entry | When |
|---|---|
| Select the `h2-express` **agent** in the agents dropdown | Ad-hoc small task in chat |

It uses the leanest valid workflow but must still respect repo rules, run
lint/format, and escalate to strict mode whenever the task becomes risky,
unclear, or cross-cutting. Trivial rule-6 changes log one `merge-log.md` line
only (no report file — see `phases/phase-2-planning.md` rule 6).

> Note: there is no `h2-express` skill/prompt entry — the `h2-express.agent.md`
> is the sole carrier of the light-mode policy. Quick mode is agent-only.

## Workflow Convention Summary

The routing convention is owned SOLELY by `.github/phases/session.json` →
`workflow_phase_config` (`.github/phases/README.md` is its human-readable
mirror), plus path-scoped rules in `.github/instructions/*.instructions.md`. This file is intentionally concise and should not repeat the full policy text.

- **Code-delivery workflows** follow the phase sequence in `.github/phases/README.md`.
- **Analysis-only review workflows** skip planning/execution/validation and move directly from Phase 1 to Phase 5.
- **Read relevant report context** from `.github/reports/<workflow-type>/` (or `archive/YYYY-MM/`) when it exists, especially for non-trivial or repeated work.
- **Blocking contradictions** must be resolved before implementation continues.
- **After code changes**, apply lint/format and validation, then generate the required report or PR notes when applicable.

The detailed phase references and specialized guidance remain in:

- `.github/phases/README.md`
- `.github/phases/DIAGRAM.md` (human reference only)
- `.github/phases/phase-1-understanding.md`
- `.github/phases/phase-2-planning.md`
- `.github/phases/phase-3-execution-formatting.md`
- `.github/phases/phase-4-validation-pr.md`
- `.github/phases/phase-5-report-generation.md`
- `.github/skills/libs/shared/post-code-change/SKILL.md`
- `.github/skills/libs/shared/report-generation/SKILL.md`
- `.github/skills/libs/shared/pre-pull-request/SKILL.md`
