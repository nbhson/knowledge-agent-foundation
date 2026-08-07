# Phase 5 Hook - Report Generation & Jira Sync (w/ Fallback)

## Goal

Generate comprehensive structured reports documenting all work completed, validation results, and evidence for archival and audit purposes. Sync the Jira ticket to reflect delivery status when possible.

## Trigger

Run this hook after Phase 4 (Validation & PR Preparation) is complete.

## Required Steps

1. **Select Report Template**: Choose the appropriate template based on workflow type:
   - **Bug Fix** → `bug-report.md`
   - **Feature Delivery** → `engineering-report.md` (final artifact; `technical-design.md` was used at planning phase and `pull-request.md` for the PR)
   - **Refactor** → `engineering-report.md` (with planning context from `technical-design.md`)
   - **Unit Test** → `engineering-report.md`
   - **Code Review** → `pull-request.md`
   - **Jira Ticket Review** → `jira-ticket-review.md`

2. **Complete Report Content**:
   - High-level summary of completed work
   - List of all files modified with line references
   - Test results and validation outputs
   - Build verification evidence (hash, time, size)
   - Type checking and linting results
   - Manual verification steps (if applicable)
   - Risk assessment and backward compatibility notes
   - PR link (once created)

3. **Include Acceptance Criteria Traceability** (required for code-delivery workflows):
   - Copy the AC list from the Jira ticket (or dev-provided summary when Jira is down).
   - For each AC, record: ✅ Met / ❌ Not met / ⚠️ Partial, with evidence (file/line or test name) from Phase 4.
   - All AC must be ✅ before the report is archived. Any ❌/⚠️ means the workflow returns to Phase 3/4.

4. **Generate Report File**:
   - Save to `.agents/reports/` directory
   - Use naming convention: `[WORKFLOW-TYPE]-REPORT-[COMPONENT/TICKET]-[DATE]-[TIME].ctx.md`
   - Examples:
     - `REFACTOR-REPORT-ValidatorSupportUtil-20260701-1531.ctx.md`
     - `BUG-REPORT-SP0168-1234-20260630-1430.ctx.md`
     - `ENGINEERING-REPORT-CustomViewFiltering-20260630-1415.ctx.md`

5. **Include Evidence**:
   - Build log excerpts with hash and duration
   - Test output summaries
   - ESLint/TypeScript validation results
   - Screenshots or execution logs (if relevant)
   - Performance metrics (if applicable)

6. **Add PR Reference**:
   - Once PR is created (via MCP or manually by the developer), update report with PR link
   - Include PR URL for traceability

7. **Add MCP Status Section** (required in all reports):
   - For each server (Jira / Figma / Bitbucket): `Available` / `Manual fallback` + reason
   - Example:
     ```
     ## MCP Status
     - Jira: Available (auto-fetched ticket SP0168-1234, synced status)
     - Figma: Manual fallback (server not reachable; verified via developer screenshot)
     - Bitbucket: Manual fallback (server not reachable; PR created manually by developer)
     ```

8. **Sync Jira Ticket with explicit availability check**:
   - **Jira MCP available?** → Yes:
     - Update the ticket status to reflect delivery (e.g., In Review / Ready for QA).
     - Add a completion comment summarizing the change, AC status, validation evidence, and the Bitbucket PR link.
     - Link the PR to the ticket for traceability.
   - **Jira MCP available?** → No:
     - Provide the developer with the exact Jira update steps to apply manually: status transition + comment text (change summary, AC status, validation evidence, PR link).
     - Never block the workflow on a missing Jira MCP connection.
   - Skip Jira sync entirely for analysis-only Jira Ticket Review workflows (no code change delivered).

## Report Template Structure

All reports should follow:
1. **Header**: Workflow type, component/ticket ID, and timestamp
2. **Summary Section**: High-level overview of changes
3. **Files Modified**: Workspace-relative paths with line numbers
4. **Verification Section**: Test results, build verification, type checking
5. **Acceptance Criteria Traceability**: AC list with ✅/❌/⚠️ and evidence (code-delivery only)
6. **Quality Metrics**: Code changes impact analysis
7. **Backward Compatibility**: Breaking changes assessment
8. **Risks & Mitigation**: Potential issues and how addressed
9. **Evidence & References**: Links to files and PR
10. **MCP Status**: Per-server availability and fallback notes

## Related Skills

- [Report Generation Skill](../../skills/report-generation/SKILL.md)

## Exit Criteria

- Report file generated and saved to `.agents/reports/`
- All required sections completed with specific details, including `MCP Status` and `Acceptance Criteria Traceability`
- Evidence links and references included
- Report is accessible and archive-ready
- PR link added once PR is created
- Jira ticket synced via MCP (or exact manual update steps provided) for code-delivery workflows