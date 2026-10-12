---
name: 'H2-Express'
description: 'Light mode for trivial, low-risk tasks. Minimal plan, targeted change, focused validation.'
argument-hint: '<small task description>'
agent: 'h2-express'
---

# H2-Express

Inputs: $ARGUMENTS (one small, low-risk task).

Follow [.github/copilot-instructions.md](../copilot-instructions.md)
Quick Mode and the `h2-express` agent — NOT the strict 5-phase flow.

- Keep it minimal: brief understanding → tiny plan (chat only, no
  `implementation_plan.md`) → targeted change → focused validation
  (`npm run lint` + relevant tests for touched files).
- Respect repo rules (`knowledge/tech-stack.md`, `knowledge/project-structure.md`,
  `angular-architecture` conventions): no `any`, no template method calls,
  `EMPTY_STRING`, `autoId` on touched interactive elements.
- Trivial rule-6 changes (≤3 lines, no behavior change): P5 = one-line
  `merge-log.md` entry only — no report file, no hash, no `REPORTS.md` row
  (see `phases/phase-2-planning.md` rule 6).
- Escalate to strict mode immediately when: ≥2 files, behavior/UI-contract
  change, shared surface (`src/shared/`, `@services/*`, store, guards,
  routing), contradictions, or security sensitivity. Say so explicitly and
  switch to the matching `h2-*` strict prompt.
