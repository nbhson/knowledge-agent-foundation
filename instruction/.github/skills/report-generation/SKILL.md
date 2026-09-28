---
name: report-generation
description: Guide for selecting, completing, and saving structured reports to the .github/reports directory in the Horizon 2 UI project.
---

# Skill: Report Generation Guide

After completing any development workflow (Bug Fix, Feature Delivery, Refactor, Unit Test, Code Review, Jira Ticket Review), generate a structured report based on the workflow type and save it to the `.github/reports` directory. This skill is the single owner of draft (Phase 3) and final (Phase 5) reports — `post-code-change` covers lint/format/cleanup only and must not generate reports.

---

## Report Generation Steps

### 1. Select the Appropriate Template

Based on your workflow type, select the corresponding template from `.github/report-templates/`:

| Workflow Type | Template File | Report File Name |
| :--- | :--- | :--- |
| **Bug Fix** | `bug-report.md` | `BUG-REPORT-[TICKET-ID]-[DATE]-[TIME].ctx.md` |
| **Feature Delivery** | `engineering-report.md` | `ENGINEERING-REPORT-[FEATURE-NAME]-[DATE]-[TIME].ctx.md` |
| **Refactor** | `technical-design.md` (planning phase) + `engineering-report.md` (completion) | `REFACTOR-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` |
| **Unit Test** | `engineering-report.md` | `TEST-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` |
| **Code Review** | `pull-request.md` | `CODE-REVIEW-[PR-ID]-[DATE]-[TIME].ctx.md` |
| **Jira Ticket Review** | `jira-ticket-review.md` | `JIRA-REVIEW-[TICKET-ID]-[DATE]-[TIME].ctx.md` |

### 2. Fill in the Template

Complete all sections of the selected template with:
- Specific details from your work
- File paths and line numbers referencing modified code
- Test results and validation evidence
- Screenshots or execution logs where relevant
- Clear summary of changes and their impact
- **Jira Ticket URL** — always fill the full URL (e.g. `https://jira.example.com/browse/SP0168-XXXX`)

### 3. Compute SHA-256 Hash (stable content-hash)

After writing the report content, compute the stable content-hash — sha256 over
the file EXCLUDING the `SHA-256 Hash` row itself (so the stored value stays
valid after insertion):

```bash
grep -v 'SHA-256 Hash' .github/reports/YOUR-REPORT-file.md | sha256sum | cut -c1-12
# macOS fallback: grep -v 'SHA-256 Hash' <file> | shasum -a 256 | cut -c1-12
```

Insert the truncated hash (first 12 hex chars) into the `SHA-256 Hash` field in the report's `## Meta` section.

### 4. Save the Report

Save the completed report to `.github/reports/` with the naming convention above. Include:
- A descriptive timestamp (YYYYMMDD-HHMM format)
- The ticket ID or component name
- The workflow type
- The `.ctx.md` extension (marks the file as report context for later phases)

Example file names:
- `BUG-REPORT-SP0168-1234-20260630-1430.ctx.md`
- `ENGINEERING-REPORT-CustomViewFiltering-20260630-1415.ctx.md`
- `REFACTOR-REPORT-SharedComponentModule-20260630-1400.ctx.md`

### 5. Update the Report Index (REPORTS.md)

After saving the report, update `.github/reports/REPORTS.md` by appending a new row to the manifest table:

```markdown
| N+1 | [Workflow Type] | [Ticket/Feature] | [YYYY-MM-DD] | [Report Filename](REPORT_FILENAME) | [TRUNCATED_HASH] | active |
```

If the report is an update to an existing one (same ticket), replace that row instead of adding a new one.

### 6. Link to Pull Request (if applicable)

If creating a Pull Request, update the report template with the PR link for easy reference.

---

## Integration with Workflows

Reports are generated **after** each workflow phase is complete:
- **Phase 3 Completion** (Code Formatting & Linting): Generate draft report with current implementation status.
- **Phase 4 Completion** (Validation & PR): Finalize report with test results, PR link, and updated manifest row.

---

## Report Format

All reports should follow this structure:
1. **Header**: Workflow type, ticket/component ID, and date
2. **Meta Section**: Table with Workflow Type, Ticket/Feature, Date, Report File, and SHA-256 Hash
3. **Jira Ticket Section**: Ticket Key, Ticket URL (required), Status, Assignee, Priority, Components
4. **Summary Section**: High-level overview of work completed
5. **Details Section**: In-depth information about files, changes, and logic
6. **Verification Section**: Test results, build verification, manual checks
7. **References**: Links to PR, tickets, related documentation

---

## Archiving Old Reports

Lifecycle (see `CHARTER.md`): `active` on creation → `archived` when moved to `.github/reports/archive/YYYY-MM/` (by post-merge hook for merged PRs, or by the monthly scheduled `cleanup-reports` job for reports older than 30 days) → row removed only when an archived report older than 90 days is deleted. Archive flips the `REPORTS.md` row to `archived`; delete removes the row.
