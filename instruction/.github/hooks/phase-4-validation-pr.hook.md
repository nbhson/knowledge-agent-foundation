# Phase 4 Hook - Validation and PR Preparation (AC + Contradictions + Build + Tests + Bitbucket w/ Fallback)

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
4. Verify contradiction-resolution compliance:
   - Re-check each frozen contradiction decision from Phase 2 against implementation/tests.
   - Record as:
    - ✅ Applied
    - ❌ Violated (return to Phase 3)
    - ⚠️ Partial (list remaining work)
5. Validation Gate — all four must hold:
   - Build OK
   - Tests OK
   - All Acceptance Criteria Met
   - Contradiction Decisions Applied
   - If any fails, return to Phase 3 (Execution and Formatting) for fixes, then re-run Phase 4.
6. Prepare Bitbucket branch & PR with explicit availability check:
   - **Bitbucket MCP available?** → Yes:
     - Create branch: `feat/<ticket>` (feature), `fix/<ticket>` (bug fix).
     - Confirm all commits in the branch follow format: `SP0168-<ticket number>: <short summary>`.
     - Create the Bitbucket Pull Request via MCP with summary, AC status, risk/impact notes, and related ticket.
   - **Bitbucket MCP available?** → No:
     - Prepare the full PR description manually using `.github/report-templates/pull-request.md` (summary, AC status, risk/impact, related ticket, commit list).
     - Instruct the developer to create the PR in Bitbucket with the prepared description.
     - Never block the workflow on a missing Bitbucket MCP connection; the developer creates the PR manually.
7. Review diffs for unintended changes before PR submission.

## Related Detailed Hooks

- `.github/skills/pre-pull-request/SKILL.md`
- `.github/hooks/phase-5-report-generation.hook.md` (for report generation)

## Exit Criteria

- Build and test validations are completed and passing.
- Every Acceptance Criteria from the Jira ticket is traced to implementation/tests (✅/❌/⚠️ recorded).
- Every contradiction-resolution decision from Phase 2 is traced to implementation/tests (✅/❌/⚠️ recorded).
- All Acceptance Criteria are Met before proceeding to PR.
- Bitbucket branch/PR created via MCP (when available) OR PR description prepared and handed to the developer for manual creation.
- PR commit messages follow `SP0168-<ticket number>: <short summary>`.
- All code diffs reviewed.

## Failure Handling & Recovery Table

| Failure | Return to | Carry (artifacts) | Retry limit → escalate |
|---------|-----------|-------------------|------------------------|
| Build fails (`npm run build`) | Phase 3 | Full compiler output + failing `file:line` + last green commit | 3 attempts → escalate to senior/architect with log excerpt |
| Test fails (`npm run test`) | Phase 3 | Failing spec + assertion diff + seed/order if flaky (rerun once isolated before counting) | 3 attempts (1 extra rerun if proven flaky) → escalate |
| AC not met / partial | Phase 3 (or Phase 2 if AC itself is wrong) | AC row ❌/⚠️ + evidence gap; if the AC text is ambiguous, reopen Phase 2 contradiction gate instead | 2 implementation rounds → return to Phase 2 for rescoping |
| Frozen decision violated | Phase 3 | Decision row ❌ + Phase 2 source | 2 rounds → return to Phase 2 to amend the decision with developer sign-off |
| Diff review finds unintended changes | Phase 3 | Diff hunks + reason each hunk stays or goes | 2 rounds → split PR (>500 lines → multiple tickets) |
| Plan rejected repeatedly | Phase 2 | Rejection reasons + revised options (see technical-design §5) | 3 rejections → escalate to senior/architect for decision, documented |

- Every return carries specific context (file/line/error message/test name) — never a generic "fix and retry".
- Counts reset only when the failing gate passes cleanly.