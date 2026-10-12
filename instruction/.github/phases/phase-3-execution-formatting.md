# Phase 3 Hook - Execution and Formatting

## Goal

Implement approved changes, update tests, and perform formatting/linting checks.

## Trigger

Run this hook only after Phase 2 approval.

## Required Steps

1. Convert approved plan into a concrete task list.
   - Include contradiction-resolution decisions as implementation constraints.
2. Implement code changes in focused increments.
3. Add or update unit tests where behavior is changed.
   - Add coverage for behaviors that were ambiguous before contradiction resolution.
4. Execute linting and formatting:
   - `npm run lint`
   - `npm run format`
5. Generate a draft report using report templates from `.github/reports/templates/`.

## Related Detailed Hooks

- `.github/skills/post-code-change/SKILL.md`
- `.github/skills/report-generation/SKILL.md`

## Workflow Resources (single source of truth — do not duplicate here)

- Workflow → skill file: the ONE matching `skills/<workflow>/SKILL.md` per the
  Phase 1 routing decision (`session.json` → `workflow_phase_config`).
- Workflow → template + report filename: `skills/report-generation/SKILL.md` §1
  table (canonical). Supporting rules/knowledge per workflow: `knowledge/` +
  the technical skills named in each workflow skill.

## Exit Criteria

- Code and tests are updated.
- Frozen contradiction decisions are reflected in implementation and test intent.
- Lint/format are completed.
- Draft report is created.