---
name: pre-pull-request
description: Quality checklist, git branch verification, commits, and PR descriptions to run before pulling and pushing code in the Horizon 2 UI project.
user-invocable: false
---

# Skill: Pre Pull Request (Pre-PR)

Before creating a commit, pushing code, or submitting a Pull Request, execute the following verification steps:

---

## Required Steps

1. **Build Check**: Run the relevant build command to ensure no compilation errors:
   - `npm run build` (for production build)
   - Or verify that your local development build completes without errors.

2. **Test Verification**: Run unit tests to confirm all changes are covered and pass:
   - `npm run test`
   - Include the red→green evidence for new regression tests (failed before, passes after) in the PR description or linked report.

3. **Branch & Commit Clarity**:
   - Checkout a clean branch from the main target using the ticket-based convention: `feat/<ticket>-<short-slug>` (feature) or `fix/<ticket>-<short-slug>` (bug fix), e.g. `feat/SP0168-3417-budget-request-loading`.
   - Use this mandatory commit message format for all PR commits: `SP0168-<ticket number>: <short summary>`.
   - Example: `SP0168-3417: fix loading issue in create IPG budget request`.
   - One ticket per branch. Stacked follow-ups reference each other (`Follow-up to #…` / `Stacked on #…`) instead of piling unrelated commits.

4. **Diff Review**:
   - Review all file changes for redundant edits, accidental modifications, or missing documentation.
   - Verify that no unrelated or temporary code/logs are included.
   - Verify new/modified templates comply with the `ui-autoid` naming convention (see [UI AutoId Skill](../ui-autoid/SKILL.md)); no accidental renames of stable `autoId` values.

5. **Alignment Check**:
   - Ensure the implementation follows [Tech Stack](../../../../knowledge/tech-stack.md) and [Project Structure](../../../../knowledge/project-structure.md).

6. **Finalize Report**:
   - Complete and review the generated report file in `.github/reports/<workflow-type>/`.
   - Update with final test results and build validation.
   - Confirm the Phase 4 validation gate (see `.github/phases/phase-4-validation-pr.md`): build OK, tests OK, every Jira AC traced, every frozen contradiction decision applied. Build+test green alone is not enough to open the PR.
   - Add the PR link once created.
   - Refer to the [Report Generation Skill](../report-generation/SKILL.md).

7. **Submit PR**:
   - Push the branch to the remote git repository.
   - Propose opening a Pull Request. Fill out the description using the PR description template (`.github/reports/templates/pr-description.md`).

---

## PR Description Field Guide

Fill every field of the template — an empty section is a review blocker, not a time-saver:

- **Summary**: what changed and why in 3–5 sentences; link the ticket. State behavior/UI-contract changes explicitly (reviewers should not discover them in the diff).
- **AC status**: one row per acceptance criterion — ✅ Met (evidence `file:line`/test) / ❌ Not met (must not happen at PR time) / ⚠️ Partial (what remains + follow-up ticket).
- **Validation**: build + test commands with outputs (or explicit skip reason for docs-only); manual walkthrough notes for UI changes.
- **Risk & impact**: affected modules/consumers, migration/backfill needs, rollback path (revert commit).
- **Scope note**: anything deliberately excluded + its ticket, so "missing" scope reads as a decision, not an oversight.

## PR Readiness Gates (enterprise)

- **Size**: keep PRs reviewable (guideline: ≤500 lines of product change; split by ticket if larger, with stacked/follow-up PRs noted).
- **Hygiene**: `git diff --check` clean; no debug logs, commented blocks, or accidental files.
- **Traceability**: PR description links ticket, lists AC status (✅/❌/⚠️ with evidence), and calls out behavior/UI-contract changes explicitly.
- **Risk note**: affected modules, migration/backfill needs, and rollback path stated up front for reviewers.
- **State**: open as draft while CI or the report is incomplete; mark ready only when gates above + Phase 4 gate all hold.

---

## Templates Reference

- **PR Description**: `.github/reports/templates/pr-description.md`
- **Final Report**: `.github/reports/templates/final-report.md` (for non-bug workflows)
- **Bug Report**: `.github/reports/templates/bug-report.md` (for bug fix workflows)
- **Jira Ticket Investigate**: `.github/reports/templates/jira-ticket-investigate.md` (for ticket review workflows)
