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

## Root Cause Analysis

[Explain what is causing the bug in the code, referencing files and lines]

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
- **Figma**: Available / Manual fallback — [reason]
- **Bitbucket**: Available / Manual fallback — [reason]

## Files Modified

- [File path 1 — line range]
- [File path 2 — line range]

## Verification & Validation Results

- **Automated Tests**: [Test command run and results]
- **Compilation Check**: [Build command run and results]
- **Manual Check**: [Screenshots or description of manual layout/functionality checks]

## Risks & Mitigation

[Detail any potential risks or edge cases remaining]

## Pull Request

- **Branch**: `fix/<ticket>`
- **Link**: [PR Link](url)
