---
name: report-generation
description: Guide for selecting, completing, and saving structured reports to the .github/reports directory in the Horizon 2 UI project.
user-invocable: false
---

# Skill: Report Generation Guide

After completing any development workflow (Bug Fix, New Feature, Refactor, Unit Test, Code Review, Jira Ticket Investigate), generate a structured report based on the workflow type and save it to the `.github/reports` directory. This skill is the single owner of draft (Phase 3) and final (Phase 5) reports — `post-code-change` covers lint/format/cleanup only and must not generate reports.

---

## Report Generation Steps

### 1. Select the Appropriate Template

Based on your workflow type, select the corresponding template from `.github/reports/templates/`:

| Workflow Type | Template File | Report File Name |
| :--- | :--- | :--- |
| **Bug Fix** | `bug-report.md` | `bug-fix/BUG-REPORT-[TICKET-ID]-[DATE]-[TIME].ctx.md` |
| **New Feature** | `final-report.md` | `new-feature/NEW-FEATURE-REPORT-[FEATURE-NAME]-[DATE]-[TIME].ctx.md` |
| **Refactor** | `implementation-plan.md` (planning phase) + `final-report.md` (completion) | `refactor/REFACTOR-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` |
| **Unit Test** | `final-report.md` | `unit-test/TEST-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` |
| **Code Review** | `pr-description.md` | `code-review/CODE-REVIEW-[PR-ID]-[DATE]-[TIME].ctx.md` |
| **Jira Ticket Investigate** | `jira-ticket-investigate.md` | `jira-ticket-investigate/JIRA-INVESTIGATE-[TICKET-ID]-[DATE]-[TIME].ctx.md` |

### 2. Fill in the Template

Complete all sections of the selected template with:
- Specific details from your work
- File paths and line numbers referencing modified code
- Test results and validation evidence
- Screenshots or execution logs where relevant
- Clear summary of changes and their impact
- **Jira Ticket URL** — always fill the full URL (e.g. `https://icon-software.atlassian.net/browse/SP0168-XXXX`)

### 3. Compute SHA-256 Hash (stable content-hash)

After writing the report content, compute the stable content-hash — sha256 over
the file EXCLUDING the `SHA-256 Hash` row itself (so the stored value stays
valid after insertion):

```bash
grep -v 'SHA-256 Hash' .github/reports/<workflow-type>/YOUR-REPORT-file.md | sha256sum | cut -c1-12
# macOS fallback: grep -v 'SHA-256 Hash' <file> | shasum -a 256 | cut -c1-12
```

Insert the truncated hash (first 12 hex chars) into the `SHA-256 Hash` field in the report's `## Meta` section.

### 4. Save the Report

Save the completed report to `.github/reports/<workflow-type>/` (folder matches the skill name: `bug-fix/`, `new-feature/`, `refactor/`, `unit-test/`, `code-review/`, `jira-ticket-investigate/`) with the naming convention above. Include:
- A descriptive timestamp (YYYYMMDD-HHMM format)
- The ticket ID or component name
- The workflow type
- The `.ctx.md` extension (marks the file as report context for later phases)

Example file names:
- `bug-fix/BUG-REPORT-SP0168-1234-20260630-1430.ctx.md`
- `new-feature/NEW-FEATURE-REPORT-CustomViewFiltering-20260630-1415.ctx.md`
- `refactor/REFACTOR-REPORT-SharedComponentModule-20260630-1400.ctx.md`

### 5. Update the Report Index (REPORTS.md)

After saving the report, update `.github/reports/REPORTS.md` by appending a new row to the manifest table:

```markdown
| N+1 | [Workflow Type] | [Ticket/Feature] | [YYYY-MM-DD] | [Report Filename](<workflow-type>/REPORT_FILENAME) | [TRUNCATED_HASH] | active |
```

If the report is an update to an existing one (same ticket), replace that row instead of adding a new one — never leave two rows for the same file (duplicate rows broke the manifest sync before).

**Trivial exemption (Phase 2 rule 6):** typo/comment/whitespace-only changes (≤3 lines,
one file, no behavior change) SKIP steps 1–7 entirely — no report file, no hash,
no `REPORTS.md` row. Log one line in `.github/reports/merge-log.md` instead
(format in `phase-2-planning.md` trivial-log rule). This skill does not apply to trivial changes.

### 6. Link to Pull Request (if applicable)

Add the PR link to the report content BEFORE step 3 (hash computation) whenever the PR already exists. If the PR is created after the hash was inserted, any content edit — including adding the PR link — invalidates the stored hash: recompute with the step-3 command and update the `REPORTS.md` row to the new value. Post-hash edits without recompute are the documented cause of mass `HASH_MISMATCH` failures — never do them.

### 7. Integrity Rules (enterprise)

- One report file → exactly one `REPORTS.md` row; updating a report replaces its row, never appends a duplicate.
- Active rows link to `<workflow-type>/<file>`; archived rows link to `archive/YYYY-MM/<file>` with status flipped — never mix.
- Required Meta fields (`Workflow Type`, `Ticket/Feature`, `Date`, `Report File`, `SHA-256 Hash`) plus the full Jira ticket URL must be filled before archiving; incomplete reports stay unarchived with the gap recorded.
- Verify with `npm run reports:check` (link/status integrity) after every manifest change.

---

## Integration with Workflows

Reports are generated **after** each workflow phase is complete:
- **Phase 3 Completion** (Code Formatting & Linting): Generate the draft report with current implementation status (`phase-3-execution-formatting.md` step 6 — load this skill here too, not only in Phase 5).
- **Phase 5 Completion** (after Phase 4 Validation & PR): Finalize the report with test results, PR link, hash, and updated manifest row (`phase-5-report-generation.md`).

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

## Field Fill Guide (what "done" looks like per section)

- **Header/Meta**: filename matches `[TYPE]-REPORT-[SUBJECT]-[YYYYMMDD]-[HHMM].ctx.md` and the `Report File` field matches the actual path; date is the completion date, not the ticket date.
- **Jira section**: Ticket Key always filled. Ticket URL: full URL when a ticket
  exists (e.g. `https://icon-software.atlassian.net/browse/SP0168-XXXX`); when
  there is genuinely no ticket (local refactor, automation, docs-only), write
  `N/A — no ticket (reason)` — never leave the field free-text ambiguous.
  Status reflects reality at report time (In Review / Done); unresolved items
  listed, never omitted.
- **Summary**: 3–5 sentences a stranger can understand — what, why, and outcome. No implementation detail here.
- **Details**: every touched file with `file:line` ranges; behavior changes called out explicitly; rejected alternatives noted with one-line reasons.
- **Verification**: commands + outputs (build, tests, lint), manual walkthrough notes, red→green evidence for fixes; skips carry explicit reasons.
- **MCP Status**: Jira line only (`Available` + what was done, or
  `Manual fallback` + reason + replacement). Optional servers (Figma, etc.)
  only when probed — prefix `Optional` and never let them affect the workflow verdict.
- **Traceability**: AC table (✅/❌/⚠️ + evidence) for code-delivery; contradiction decisions (✅/❌/⚠️ + evidence) when Phase 2 froze any.

## Hash Troubleshooting

- `HASH_MISMATCH` after adding the PR link → you edited post-hash: recompute (step 3) and update the manifest row.
- Mismatch with no visible edit → check trailing whitespace/line-ending changes from the editor or formatter; recompute from the saved file, never hand-copy an old value.
- Hash covers content only (excludes the hash row itself), so moving the file (active → archive) never invalidates it — but the manifest link + status must still be updated together.
- **Recompute ONLY with the shell pipeline** (`grep -v 'SHA-256 Hash' <file> | shasum -a 256 | cut -c1-12`). Never recompute with Python/`splitlines` — several reports use CRLF and `grep` vs Python disagree on trailing-newline bytes (proven 2026-10-12: 1-byte drift → false mismatch). The shell pipeline is canonical; `verify-report-hash.sh` enforces it in CI.

---

## Archiving Old Reports

Lifecycle (single source of truth): `active` on creation (file in `.github/reports/<workflow-type>/`) → `archived` when moved to `.github/reports/archive/YYYY-MM/` (by the post-merge skill for merged PRs; stale leftovers are archived by the on-demand cleanup `bash .github/hooks/report-lifecycle.sh`, e.g. monthly or after merging to main; age = last git commit date, fallback mtime, default: older than 30 days) → row removed only when an archived report older than 90 days is deleted (same entrypoint). Active rows link to `<workflow-type>/<file>`; archiving flips the `REPORTS.md` row status (`active`→`archived`, `legacy-active`→`legacy-archived`) AND repoints its link to `archive/YYYY-MM/<file>`; delete removes the row. Preview anytime with `bash .github/hooks/report-lifecycle.sh --dry-run`; integrity check with `--check`.
