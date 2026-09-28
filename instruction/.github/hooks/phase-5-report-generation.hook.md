# Phase 5 Hook - Report Generation & Jira Sync (w/ Fallback)

## Goal

Generate comprehensive structured reports documenting all work completed, validation results, and evidence for archival and audit purposes. Sync the Jira ticket to reflect delivery status when possible.

## Trigger

Run this hook after Phase 4 (Validation & PR Preparation) is complete. For analysis-only workflows (Jira Ticket Review, Code Review) run it directly after Phase 1.

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

3. **Include Acceptance Criteria Traceability** (required for code-delivery workflows; **skip for Jira Ticket Review** — no implementation occurs, so ACs are not validated against delivered code):
   - Copy the AC list from the Jira ticket (or dev-provided summary when Jira is down).
   - For each AC, record: ✅ Met / ❌ Not met / ⚠️ Partial, with evidence (file/line or test name) from Phase 4.
   - All AC must be ✅ before the report is archived. Any ❌/⚠️ means the workflow returns to Phase 3/4.

4. **Include Contradiction Resolution Traceability** (required when contradictions were identified; **skip for Code Review** — no Phase 2 planning occurred, so there are no frozen decisions to trace):
   - Copy the contradiction list and frozen decisions from Phase 2.
   - For each decision, record: ✅ Applied / ❌ Violated / ⚠️ Partial, with evidence (file/line or test name) from Phase 4.
   - Any ❌/⚠️ means the workflow returns to Phase 3/4.

5. **Generate Report File**:
   - Save to `.github/reports/` directory
   - Use naming convention: `[WORKFLOW-TYPE]-REPORT-[COMPONENT/TICKET]-[DATE]-[TIME].ctx.md`
   - Examples:
     - `REFACTOR-REPORT-ValidatorSupportUtil-20260701-1531.ctx.md`
     - `BUG-REPORT-SP0168-1234-20260630-1430.ctx.md`
     - `ENGINEERING-REPORT-CustomViewFiltering-20260630-1415.ctx.md`
   - Compute the stable content-hash (excludes the hash row itself so it stays valid after insertion):
     ```bash
     grep -v 'SHA-256 Hash' .github/reports/<report-file> | sha256sum | cut -c1-12
     # macOS fallback: grep -v 'SHA-256 Hash' <file> | shasum -a 256 | cut -c1-12
     ```
   - Insert the first 12 hex characters into the `## Meta` → `SHA-256 Hash` field of the report.

6. **Update Report Index (REPORTS.md)**:
   - Append a new row to `.github/reports/REPORTS.md` with the report filename, truncated content-hash, and metadata.
   - If updating an existing report for the same ticket, replace that row instead.
   - Status is `active` on creation; post-merge or the monthly cleanup job flips it to `archived` when the file moves to `.github/reports/archive/YYYY-MM/`. Rows are removed only when archived files older than 90 days are deleted.

7. **Include Evidence**:
   - Build log excerpts with hash and duration
   - Test output summaries
   - ESLint/TypeScript validation results
   - Screenshots or execution logs (if relevant)
   - Performance metrics (if applicable)

8. **Add PR Reference**:
   - Once PR is created (via MCP or manually by the developer), update report with PR link
   - Include PR URL for traceability

9. **Add MCP Status Section** (required in all reports):
   - For each server (Jira / Figma / Bitbucket): `Available` / `Manual fallback` + reason
   - Example:
     ```
     ## MCP Status
     - Jira: Available (auto-fetched ticket SP0168-1234, synced status)
     - Figma: Manual fallback (server not reachable; verified via developer screenshot)
     - Bitbucket: Manual fallback (server not reachable; PR created manually by developer)
     ```

10. **Sync Jira Ticket with explicit availability check**:
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
6. **Contradiction Resolution**: contradiction list + frozen decisions + ✅/❌/⚠️ implementation status
7. **Quality Metrics**: Code changes impact analysis
8. **Backward Compatibility**: Breaking changes assessment
9. **Risks & Mitigation**: Potential issues and how addressed
10. **Evidence & References**: Links to files and PR
11. **MCP Status**: Per-server availability and fallback notes

## Related Skills

- [Report Generation Skill](../skills/report-generation/SKILL.md)

## Exit Criteria

- Report file generated and saved to `.github/reports/`
- `## Meta` section filled with Workflow Type, Ticket/Feature, Date, Report File, and SHA-256 Hash (stable content-hash, excludes hash row)
- `## Jira Ticket` section filled with Ticket Key and full Ticket URL *(required)*
- All required sections completed with specific details, including `MCP Status`, `Acceptance Criteria Traceability`, and `Contradiction Resolution`
- Evidence links and references included
- `.github/reports/REPORTS.md` updated with the new/updated row
- Report is accessible and archive-ready
- PR link added once PR is created
- Jira ticket synced via MCP (or exact manual update steps provided) for code-delivery workflows
