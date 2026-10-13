# Phase 5 Hook - Report Generation & Jira Sync (w/ Fallback)

## Goal

Generate comprehensive structured reports documenting all work completed, validation results, and evidence for archival and audit purposes. Sync the Jira ticket to reflect delivery status when possible.

## Trigger

Run this hook after Phase 4 (Validation & PR Preparation) is complete. For analysis-only workflows (Jira Ticket Investigate, Code Review) run it directly after Phase 1.

## Required Steps

1. **Select Report Template**: per the canonical table in
   `skills/libs/shared/report-generation/SKILL.md` §1 (workflow → template + report filename).
   Do not duplicate that table here.

2. **Complete Report Content**:
   - High-level summary of completed work
   - List of all files modified with line references
   - Test results and validation outputs
   - Build verification evidence (hash, time, size)
   - Type checking and linting results
   - Manual verification steps (if applicable)
   - Risk assessment and backward compatibility notes
   - PR link (once created)

3. **Include Acceptance Criteria Traceability** (required for code-delivery workflows; **skip for Jira Ticket Investigate** — no implementation occurs, so ACs are not validated against delivered code):
   - Copy the AC list from the Jira ticket (or dev-provided summary when Jira is down).
   - For each AC, record: ✅ Met / ❌ Not met / ⚠️ Partial, with evidence (file/line or test name) from Phase 4.
   - All AC must be ✅ before the report is archived. Any ❌/⚠️ means the workflow returns to Phase 3/4.

4. **Include Contradiction Resolution Traceability** (required when contradictions were identified; **skip for Code Review** — no Phase 2 planning occurred, so there are no frozen decisions to trace):
   - Copy the contradiction list and frozen decisions from Phase 2.
   - For each decision, record: ✅ Applied / ❌ Violated / ⚠️ Partial, with evidence (file/line or test name) from Phase 4.
   - Any ❌/⚠️ means the workflow returns to Phase 3/4.

5. **Generate Report File**:
   - Save to `.github/reports/<workflow-type>/` with the filename pattern from
     the canonical table (`skills/libs/shared/report-generation/SKILL.md` §1):
     `[WORKFLOW-TYPE]-REPORT-[COMPONENT/TICKET]-[DATE]-[TIME].ctx.md`.
   - Examples:
     - `refactor/REFACTOR-REPORT-ValidatorSupportUtil-20260701-1531.ctx.md`
     - `bug-fix/BUG-REPORT-SP0168-1234-20260630-1430.ctx.md`
     - `new-feature/NEW-FEATURE-REPORT-CustomViewFiltering-20260630-1415.ctx.md`
   - Compute the stable content-hash (excludes the hash row itself so it stays valid after insertion):
     ```bash
     grep -v 'SHA-256 Hash' .github/reports/<workflow-type>/<report-file> | sha256sum | cut -c1-12
     # macOS fallback: grep -v 'SHA-256 Hash' <file> | shasum -a 256 | cut -c1-12
     ```
   - Insert the first 12 hex characters into the `## Meta` → `SHA-256 Hash` field of the report.

6. **Update Report Index (REPORTS.md)**:
   - Append a new row to `.github/reports/REPORTS.md` with the report filename, truncated content-hash, and metadata.
   - If updating an existing report for the same ticket, replace that row instead.
   - Status is `active` on creation; post-merge or the on-demand cleanup (`bash .github/hooks/report-lifecycle.sh`, e.g. monthly or after merging to main) flips it to `archived` when the file moves from `.github/reports/<workflow-type>/` to `.github/reports/archive/YYYY-MM/`. Age is measured from the file's **last git commit date**, falling back to filesystem mtime outside git. Rows are removed only when archived files older than 90 days are deleted (same script, `--retention-days 90`; preview with `--dry-run`, integrity check with `--check`).

7. **Include Evidence**:
   - Build log excerpts with hash and duration
   - Test output summaries
   - ESLint/TypeScript validation results
   - Screenshots or execution logs (if relevant)
   - Performance metrics (if applicable)

8. **Add PR Reference**:
   - Once the PR is opened by the developer, update the report with the PR link
   - Include PR URL for traceability

9. **Add MCP Status Section** (required in all reports):
   - Required line: Jira (`Available` / `Manual fallback` + reason
     + replacement). Optional servers only when probed, prefixed `Optional:`.
   - Example:
     ```
     ## MCP Status
     - Jira: Available (auto-fetched ticket SP0168-1234, synced status)
     ```
   - When no ticket exists: `Ticket URL: N/A — no ticket (reason)` and
     `Jira: Manual fallback (no ticket supplied; AC sourced from dev summary)`.

10. **Sync Jira Ticket with explicit availability check**:
   - **Jira MCP available?** → Yes:
     - Update the ticket status to reflect delivery (e.g., In Review / Ready for QA).
     - Add a completion comment summarizing the change, AC status, validation evidence, and the PR link.
     - Link the PR to the ticket for traceability.
   - **Jira MCP available?** → No:
     - Provide the developer with the exact Jira update steps to apply manually: status transition + comment text (change summary, AC status, validation evidence, PR link).
     - Never block the workflow on a missing Jira MCP connection.
   - Skip Jira sync entirely for analysis-only Jira Ticket Investigate workflows (no code change delivered).
11. **Post-Merge Sync (runs only after the PR is confirmed merged — via MCP notification or developer confirmation; otherwise stop at step 10)**:
    - Follow the [Post-Merge Skill](../skills/libs/shared/post-merge/SKILL.md): sync the Jira ticket to Done/Closed (or give manual steps), archive the report from `.github/reports/<workflow-type>/` to `.github/reports/archive/YYYY-MM/` (flip the `REPORTS.md` row to archived + repoint its link), delete `implementation_plan.md` at repo root if present, and append the merge row to `.github/reports/merge-log.md`.
    - Skip for analysis-only Jira Ticket Investigate workflows (no code change delivered).


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

- [Report Generation Skill](../skills/libs/shared/report-generation/SKILL.md)
- [Post-Merge Skill](../skills/libs/shared/post-merge/SKILL.md) (step 11 only, after merge confirmation)

## Exit Criteria

- Report file generated and saved to `.github/reports/<workflow-type>/`
  (EXCEPT trivial Phase-2-rule-6 changes → `merge-log.md` one-liner only, no report file)
- `## Meta` section filled with Workflow Type, Ticket/Feature, Date, Report File, and SHA-256 Hash (stable content-hash, excludes hash row)
- `## Jira Ticket` section filled with Ticket Key and full Ticket URL *(required)*
- All required sections completed with specific details, including `MCP Status`, `Acceptance Criteria Traceability`, and `Contradiction Resolution`
- Evidence links and references included
- `.github/reports/REPORTS.md` updated with the new/updated row
- Report is accessible and archive-ready
- PR link added once PR is created
- Jira ticket synced via MCP (or exact manual update steps provided) for code-delivery workflows
- Post-merge (only when merge confirmed): Jira closed, report archived, merge logged per the Post-Merge Skill
