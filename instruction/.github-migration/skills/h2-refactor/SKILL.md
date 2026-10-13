---
name: h2-refactor
description: Strict P1→P5 refactor with smell inventory and no-behavior-change proof.
disable-model-invocation: true
argument-hint: '<target modules/files> <smell/motivation>'
---
# H2-Refactor

Inputs: $ARGUMENTS (target + motivation, affected modules).

Follow [.github/copilot-instructions.md](../../copilot-instructions.md)
and [.github/phases/README.md](../../phases/README.md) — full P1→P5.

- P1: Load `skills/libs/workflows/refactor/SKILL.md`. Jira MCP: fetch ticket, else ask dev once. Load at most one relevant report. Build smell inventory table with `file:line` evidence. Map blast radius (imports, routes, store, `autoId`) before planning.
- P2: Slice order + per-increment checkpoints. Approval required per `phases/phase-2-planning.md`; vague plans are not approvable.
- P3: Record baseline `npm run test` first. Create task list, then one slice = one move + green checkpoint per `skills/libs/workflows/refactor/SKILL.md` + `skills/libs/shared/post-code-change/SKILL.md`.
- P4: Behavior preserved, `npm run test` + `npm run build` green, no scope creep. Prepare the PR description and propose opening the PR. Run Reviewer diff check.
- P5: File report via `skills/libs/shared/report-generation/SKILL.md` (final-report template + hash + `REPORTS.md` row + Jira sync or manual steps).
