# Engineering Report

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | [feature / bug-fix / refactor / unit-test] |
| **Ticket/Feature** | [SP0168-XXXX or feature name]  |
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

## Summary of Changes

[High-level summary of the completed changes]

## Files Modified

- [File path 1]
- [File path 2]

## Verification & Validation Results

- **Automated Tests**: [Test command run and results]
- **Compilation Check**: [Build command run and results]
- **Manual Check**: [Screenshots or description of manual layout/functionality checks]

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

## Risks & Mitigation

[Detail any potential risks or edge cases remaining]

## Backward Compatibility

- [Assessment of breaking changes, if any]

## Pull Request

- **Branch**: `[feat/feature-name | fix/ticket | refactor/name]`
- **Link**: [PR Link](url)
