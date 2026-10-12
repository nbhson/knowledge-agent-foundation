---
name: bug-fix
description: Step-by-step workflow for reproducing, patching, formatting, testing, and creating bug reports in the Horizon 2 UI project.
argument-hint: '<Jira-key> <expected vs actual + repro>'
user-invocable: false
---

# Workflow: Bug Fix

This document outlines the systematic flow for reproducing, identifying, fixing, and validating bugs in the Horizon 2 UI application.

---

## Entry Criteria

- Bug report available: reproduction steps, expected vs actual behavior, environment (branch/commit, browser, route).
- Severity triaged (team default — adjust per project policy):

  | Severity | Meaning | Handling |
  |---|---|---|
  | Blocker | Crash, data loss/wrong data, auth bypass, or core flow unusable | Fix forward immediately; minimal review latency |
  | Major | Wrong behavior on a supported path, workaround painful or absent | Normal Phase 2 approval, no scope widening |
  | Minor | Cosmetic, typo-level, or edge-case with easy workaround | May ride the normal queue; still needs red→green proof |

- Target workflow confirmed as Bug Fix (not a hidden feature request or refactor).

## Required Steps & Phases

1. **Replicate & Document (Phase 1)**: Replicate the bug on the local development server (`npm run startdev`). No fix without a recorded reproduction artifact: numbered steps, expected vs actual per step, environment, and log/screenshot reference. Document the details using the Bug Report template (`.github/reports/templates/bug-report.md`).
2. **Fault Isolation (Phase 1)**: Narrow the layer before touching code — template, component, feature service, API transport, NgRx store/effects, route/guard, or styles. Record the evidence trail: stack trace or failing assertion → suspect layer → hypothesis list with each hypothesis ruled in/out and why. Common Angular 15 suspects to check first:
   - Unclosed subscription (missing `takeUntil`/`async` pipe) causing stale or duplicated state.
   - Computation method called from a template binding re-running every change-detection pass.
   - Race between parallel RxJS streams (no `switchMap`/ordering where user actions overlap).
   - Wrong provider scope (feature-provided service holding cross-route state) or missing module declaration/import.
   - Guard/route misconfiguration dropping context (params, resolved data).
3. **Fix Strategy (Phase 2)**: Choose forward-fix (targeted patch) vs revert (bad commit identified and revert is safe). Default to the smallest diff that removes the root cause — not the symptom. If the fix requires an API-shape, data-flow, or shared-service redesign, stop and split it into a New Feature / Refactor ticket instead of widening this fix.
4. **Draft Plan (Phase 2)**: Before implementation, provide a concise draft plan (root cause, fix approach, files, regression tests, validation) and wait for review/approval when the task is non-trivial. Apply the Phase 2 threshold table (`.github/phases/phase-2-planning.md`) to decide whether a design file (`implementation_plan.md`, lifecycle defined once in Phase 2) is needed; for simple/isolated fixes, proceed directly.
5. **Implement Fix (Phase 3)**: Make targeted changes following [Tech Stack](../../knowledge/tech-stack.md) and [Project Structure](../../knowledge/project-structure.md). Search existing constants, models, shared components, utils, pipes, and services before introducing new logic. Avoid unrelated code modifications. Bug fixes must not introduce new computation calls in templates to fix display logic — precompute in the service or use a pure pipe (see [Angular Architecture §6.5](../angular-architecture/SKILL.md)). If the fix touches styles, follow [Styling Standards](../styling-standards/SKILL.md); if it touches templates with interactive/viewable elements, keep `autoId` values stable per the [UI AutoId Skill](../ui-autoid/SKILL.md).
6. **Regression Tests (Phase 3)**: Add or update Jest unit tests in the corresponding `*.spec.ts` file. Prove red→green: the new test fails on the unfixed code for the right reason (red, recorded) and passes with the fix (green). Cover the exact reported scenario plus the nearest edge cases (empty/null/error adjacent to the fix). Re-run neighboring suites that touch the same service/store/component.
7. **Formatting & Quality Checks (Phase 3)**: Follow the [Post Code Change Skill](../post-code-change/SKILL.md) for canonical formatting, linting, and cleanup (mechanical template/line-count/`EMPTY_STRING` checks included).
8. **Validation (Phase 4)**:
   - Re-run the recorded reproduction steps against the fixed build: every step now matches expected behavior (`npm run startdev`).
   - Run unit tests to verify changes: `npm run test` (or the specific spec file first, then the affected suites).
   - Run production compilation check: `npm run build`.
   - If the bug corrupted or exposed data, state the data impact explicitly (who is affected, whether backfill/cleanup is needed) and file it as a follow-up ticket — never hide it in the fix.
9. **Report (Phase 5)**: File a Phase 5 report using the [Report Generation Skill](../report-generation/SKILL.md) (correct template + stable content-hash + `REPORTS.md` row). Phase 4 validates; Phase 5 files the report.

## Scope Boundaries

- Fix the root cause with the minimal targeted change; no unrelated cleanups or behavior changes.
- If the fix requires a design change (API shape, data flow, shared service), escalate to the New Feature / Refactor workflow instead of widening this fix.

---

## Deliverables

- **Severity & Blast Radius**: Severity, affected routes/users, and whether data was impacted.
- **Reproduction Artifact**: Numbered repro steps + expected/actual + environment, re-runnable after the fix.
- **Isolation Trail**: Suspect layers, hypotheses ruled in/out with evidence (`file:line`, stack, or assertion).
- **Clear Summary of the Root Cause**: Explanation of what caused the bug and how it was diagnosed.
- **Minimal Code Change**: Targeted, clean fix with no duplicate or redundant logic.
- **Validation Evidence**: Repro re-run result plus output/evidence from running lint, build, and test commands.
- **Regression Proof**: The new/updated test fails without the fix (red) and passes with it (green); affected existing suites re-run with no new failures.
- **Risk & Rollback Note**: Blast radius of the change and how to revert if the fix regresses.

## Exit Criteria

- Recorded reproduction passes on the fixed build; every step matches expected behavior.
- Red→green proof recorded; no new test failures in affected suites; build green.
- Data impact (if any) stated with a follow-up ticket; Phase 5 report filed.
