---
name: p-bug-fix
description: Strict P1→P5 bug fix with repro, red-green proof and bug report.
disable-model-invocation: true
argument-hint: '<Jira-key> <expected vs actual + repro steps>'
---
# P-Bug-Fix

Inputs: $ARGUMENTS (bug report: repro steps, expected vs actual, env).

Follow [.github/copilot-instructions.md](../../copilot-instructions.md)
and [.github/phases/README.md](../../phases/README.md) — full P1→P5.

- P1: Load `skills/libs/workflows/bug-fix/SKILL.md`. Jira MCP: fetch ticket, else ask dev once. Load at most one relevant report. Record repro artifact first (`npm run startdev`). Isolate layer with evidence trail. No fix without repro.
- P2: Forward-fix vs revert decision, minimal diff. Draft plan + approval when non-trivial per `phases/phase-2-planning.md`.
- P3: Create task list, then targeted fix per `skills/libs/workflows/bug-fix/SKILL.md` + `skills/libs/shared/post-code-change/SKILL.md`. Prove red→green in owning `*.spec.ts`. Keep `autoId` stable.
- P4: Re-run repro steps green + `npm run test` + `npm run build` + AC/contradiction trace. Prepare the PR description and propose opening the PR. Run Reviewer diff check. State data impact explicitly if any.
- P5: File report via `skills/libs/shared/report-generation/SKILL.md` (bug-report template + hash + `REPORTS.md` row + Jira sync or manual steps).
