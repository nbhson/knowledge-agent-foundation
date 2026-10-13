# Bug Fix Report

## Meta

| Field | Value |
|---|---|
| **Workflow Type** | Bug Fix |
| **Ticket/Feature** | Studies tracker runtime errors after component extraction |
| **Date** | 2026-09-21 |
| **Report File** | `BUG-REPORT-StudiesTracker-Runtime-20260921-0745.ctx.md` |
| **SHA-256 Hash** | 3e26e0d3e5e1 |

## Jira Ticket

- **Ticket Key**: Not provided
- **Ticket URL**: N/A — no ticket (local component-extraction fix, AC sourced from dev summary)
- **Status**: Fixed locally
- **Components**: `src/app/tracker/studies`

## Root Cause

1. `StudiesOversightComponent` was wrapped by `StudiesOversightTabComponent`, but `StudiesComponent` still dereferenced the old direct `@ViewChild`; the value was undefined during header rendering and tab changes.
2. `mat-header-cell` templates were nested inside `StudiesFilterHeaderComponent` under `matColumnDef`. Angular Material content queries could not resolve the nested `TemplateRef`, producing `MatColumnDef.template` undefined during tracker rendering.
3. Table callbacks such as `checkAdminRoles()` were passed as unbound methods, so child rendering invoked them without the `StudiesComponent` context.

## Fix

- Forward oversight download state and refresh through `StudiesOversightTabComponent`, while retaining compatibility with existing direct component tests/export payload construction.
- Keep filter header cell templates directly under `matColumnDef` in `StudiesTrackerTableComponent`; retain event forwarding and filter behavior without hiding the `th` templates behind a child component.
- Resolve filter data-list typing through the existing normalization pattern.
- Bind callback methods passed to the table so service-backed permission and form methods retain their owner context.

## Files Modified

- `src/app/tracker/studies/components/studies-oversight-tab/studies-oversight-tab.component.ts`
- `src/app/tracker/studies/components/studies-tracker-table/studies-tracker-table.component.html`
- `src/app/tracker/studies/components/studies-tracker-table/studies-tracker-table.component.ts`
- `src/app/tracker/studies/studies.component.html`
- `src/app/tracker/studies/studies.component.ts`

## Verification

- Focused tests: 3 suites, 9 tests passed.
- Callback regression tests: Studies tracker focused suite remains green at 8/8 tests.
- Development build: passed; browser bundle generation completed successfully.
- Type diagnostics: no errors in changed files.
- Prettier: passed on changed files.
- `git diff --check`: passed.
- Full Jest: repository has unrelated baseline failures; focused Studies tracker tests pass.
- Unrelated existing worktree change in `study-health-top-priority.component.ts` was not included.

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Studies tracker no longer throws `Cannot read properties of undefined (reading 'template')`. | ✅ Met | Direct `mat-header-cell` templates restored; focused table and StudiesComponent tests plus build pass. |
| 2 | Studies oversight no longer dereferences an undefined `isDisableDownloadButton`. | ✅ Met | Wrapper forwards state with safe fallback; focused StudiesComponent and oversight wrapper tests pass. |
| 3 | Existing filter, pagination, export, refresh, and review flows remain wired. | ✅ Met | Existing StudiesComponent focused suite passes 6/6. |

## Contradiction Resolution

No blocking contradictions. The fix preserves the extracted component boundaries where Angular Material supports them and keeps `matColumnDef` template ownership in the table component where Angular Material requires direct content templates.

## MCP Status

- **Jira**: Manual fallback (no ticket supplied; AC sourced from dev summary).
- **Bitbucket**: Manual fallback; no PR created.

## Backward Compatibility

No route, API, payload, or user-facing behavior changes were introduced. Existing direct test-facing oversight property compatibility was retained.

## Residual Risk

A browser-level manual verification should still exercise switching between Studies Tracker and Studies Oversight after a hard reload. Development compilation and focused component tests pass.
