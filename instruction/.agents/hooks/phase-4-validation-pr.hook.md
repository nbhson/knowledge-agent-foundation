# Phase 4 Hook - Validation and PR Preparation (AC + Build + Tests + Bitbucket w/ Fallback)

## Goal

Validate final quality against the Jira ticket requirements and prepare for pull request.

## Trigger

Run this hook after Phase 3 outputs are available.

## Required Steps

1. Run compile/build validation:
   - `npm run build` (or `npm run build-prod` when needed)
2. Run unit tests:
   - `npm run test`
3. Verify Acceptance Criteria (AC) against the Jira ticket:
   - Retrieve the list of Acceptance Criteria from Phase 1 context (Jira MCP fetch, or dev-provided ticket summary when Jira is down).
   - For **each AC**, explicitly trace it to implementation and/or tests. Record the result as:
     - ✅ Met — evidence: file/line or test name
     - ❌ Not met — gap item → return to Phase 3
     - ⚠️ Partial — list what remains
   - Build+Test green alone is NOT sufficient to pass the Validation Gate.
4. Validation Gate — all three must hold:
   - Build OK
   - Tests OK
   - All Acceptance Criteria Met
   - If any fails, return to Phase 3 (Execution and Formatting) for fixes, then re-run Phase 4.
5. Prepare Bitbucket branch & PR with explicit availability check:
   - **Bitbucket MCP available?** → Yes:
     - Create branch: `feat/<ticket>` (feature), `fix/<ticket>` (bug fix).
     - Confirm all commits in the branch follow format: `SP0168-<ticket number>: <short summary>`.
     - Create the Bitbucket Pull Request via MCP with summary, AC status, risk/impact notes, and related ticket.
   - **Bitbucket MCP available?** → No:
     - Prepare the full PR description manually using `.agents/report-templates/pull-request.md` (summary, AC status, risk/impact, related ticket, commit list).
     - Instruct the developer to create the PR in Bitbucket with the prepared description.
     - Never block the workflow on a missing Bitbucket MCP connection; the developer creates the PR manually.
6. Review diffs for unintended changes before PR submission.

## Related Detailed Hooks

- `.agents/skills/pre-pull-request/SKILL.md`
- `.agents/hooks/phase-5-report-generation.hook.md` (for report generation)

## Exit Criteria

- Build and test validations are completed and passing.
- Every Acceptance Criteria from the Jira ticket is traced to implementation/tests (✅/❌/⚠️ recorded).
- All Acceptance Criteria are Met before proceeding to PR.
- Bitbucket branch/PR created via MCP (when available) OR PR description prepared and handed to the developer for manual creation.
- PR commit messages follow `SP0168-<ticket number>: <short summary>`.
- All code diffs reviewed.

## Failure Handling

- If any Phase 4 validation step fails (build, test, AC traceability, or diff review), return to Phase 3 (Execution and Formatting) to apply fixes, then re-run Phase 4 until all exit criteria pass.