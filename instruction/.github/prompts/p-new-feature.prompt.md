---
name: 'P-New-Feature'
description: 'Strict P1→P5 new feature with approval gate and Phase 5 report.'
argument-hint: '<Jira-key> <mô tả ngắn + AC>'
agent: 'p-standard'
---

# P-New-Feature

Inputs: $ARGUMENTS (Jira key or dev summary with testable AC).

Follow [.github/copilot-instructions.md](../copilot-instructions.md)
and [.github/phases/README.md](../phases/README.md) — full P1→P5.

- P1: Load `knowledge/tech-stack.md` + `knowledge/project-structure.md` + `skills/new-feature/SKILL.md`. Jira MCP: fetch ticket, else ask dev once for summary. Load at most one relevant report from `.github/reports/`. Survey reusable services/constants/models/utils/pipes/components. List contradictions/blockers.
- P2: Apply `phases/phase-2-planning.md` threshold. Present draft plan, freeze contradictions, wait for approval (`PHASE2_APPROVED`).
- P3: Create task list, then implement approved plan only per `skills/new-feature/SKILL.md` + `skills/post-code-change/SKILL.md`. Write/update unit tests per AC. No template computation calls, `autoId` on touched elements.
- P4: All four required — build OK, tests OK, every AC traced, every frozen decision applied. Prepare the PR description per `skills/pre-pull-request/SKILL.md` and propose opening the PR. Run Reviewer diff check.
- P5: File report via `skills/report-generation/SKILL.md` (final-report template + hash + `REPORTS.md` row + Jira sync or manual steps).
