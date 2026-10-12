# Final Report

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

## Environment

- **Branch**: [working branch]
- **Base commit**: [commit hash the work started from]
- **Merge/target**: [target branch; merge SHA once merged]

## Files Modified

- [File path 1]
- [File path 2]

## Design Decisions (new-feature — omit for other workflows)

- **Component split**: [container vs presenters, state ownership]
- **Options rejected**: [option → one-line reason]
- **UI states covered**: [loading / error / empty / denied triggers + branches]

## Verification & Validation Results

- **Automated Tests**: [Test command run and results]
- **Compilation Check**: [Build command run and results]
- **Manual Check**: [Screenshots or description of manual layout/functionality checks]
- **Manual walkthrough**: [ACs walked × states × viewports, keyboard/focus notes for UI changes]

## Workflow Appendix (fill the block matching the workflow, delete the rest)

### Refactor — Move Log & Baseline Comparison

| Slice | Files moved/renamed | Wiring changes | Checkpoint |
|-------|--------------------|----------------|------------|
| 1 | [...] | [declarations/exports/routes/providers] | [green / blocked + reason] |

- **Baseline**: [test result before editing, pre-existing failures noted]
- **After**: [same suite result — diff must be empty; characterization tests unmodified + green]

### Unit Test — Red→Green Evidence

- **Red run**: [new test failed before fix — reason + ref]
- **Green run**: [passes after — ref]
- **Suites re-run**: [isolated spec + neighboring suites, no new failures]

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

## Risks & Mitigation

[Detail any potential risks or edge cases remaining]

## Backward Compatibility

- [Assessment of breaking changes, if any]

## Rollback

- [How to revert: revert commit / flag / follow-up ticket; migration reversal if any]

## Pull Request

- **Branch**: `[feat/feature-name | fix/ticket | refactor/name]`
- **Link**: [PR Link](url)
