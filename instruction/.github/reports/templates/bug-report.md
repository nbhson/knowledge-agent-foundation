# Bug Report

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | bug-fix                        |
| **Ticket/Feature** | [SP0168-XXXX]                  |
| **Date**           | [YYYY-MM-DD]                   |
| **Report File**    | `[filename].ctx.md`            |
| **SHA-256 Hash**   | `[auto-generated on save]`     |

## Jira Ticket

- **Ticket Key**: [SP0168-XXXX]
- **Ticket URL**: [https://jira.example.com/browse/SP0168-XXXX] *(required — must be filled)*
- **Status**: [Current Jira status]
- **Assignee**: [Assignee name]
- **Priority**: [P0/P1/P2/P3]
- **Components**: [Affected modules]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]

## Expected vs. Actual Result

- **Expected**: [Description of expected behavior]
- **Actual**: [Description of actual buggy behavior]

## Severity & Blast Radius

- **Severity**: [Blocker / Major / Minor — per bug-fix skill triage]
- **Affected routes/users**: [Who and where is impacted]
- **Environment**: [Branch/commit, browser, route where observed]

## Root Cause Analysis

[Explain what is causing the bug in the code, referencing files and lines]

## Isolation Trail

| # | Suspect layer | Hypothesis | Ruled in/out + evidence |
|---|---------------|------------|-------------------------|
| 1 | [template / component / service / API / store / route-guard / styles] | [...] | [in/out — stack trace, assertion, or `file:line`] |

## Proposed Fix

[Detail the changes required to resolve the issue]

## Acceptance Criteria Traceability

| # | Acceptance Criterion | Status | Evidence (file/line or test name) |
|---|----------------------|--------|-----------------------------------|
| 1 | [AC from Jira ticket or dev-provided summary] | ✅ Met / ❌ Not met / ⚠️ Partial | [file path:line or test name] |
| 2 | [...] | [...] | [...] |

> **Rule**: All AC must be ✅ before the report is archived. Any ❌/⚠️ requires returning to Phase 3 for fixes.

## Contradiction Resolution

| # | Contradiction / Ambiguity | Frozen Decision | Applied Status | Evidence |
|---|--------------------------|-----------------|----------------|----------|
| 1 | [Describe the conflict identified in Phase 1] | [Decision made with developer] | ✅ Applied / ❌ Violated / ⚠️ Partial | [file path:line or test name] |

> **Rule**: Any ❌/⚠️ in contradiction resolution requires returning to Phase 3/4 for fixes.

## MCP Status

- **Jira**: Available / Manual fallback — [reason]

## Files Modified

- [File path 1 — line range]
- [File path 2 — line range]

## Verification & Validation Results

- **Reproduction re-run**: [Each recorded repro step re-run on the fixed build — pass/fail per step]
- **Regression proof (red→green)**: [New test failed before fix (red run ref) / passes after (green run ref)]
- **Neighboring suites**: [Suites re-run + result, no new failures]
- **Automated Tests**: [Test command run and results]
- **Compilation Check**: [Build command run and results]
- **Manual Check**: [Screenshots or description of manual layout/functionality checks]

## Risks & Mitigation

[Detail any potential risks or edge cases remaining]

## Data Impact

- [None — or: who is affected, whether backfill/cleanup is needed + follow-up ticket]

## Rollback

- [How to revert if the fix regresses: revert commit / flag / follow-up]

## Pull Request

- **Branch**: `fix/<ticket>`
- **Link**: [PR Link](url)
