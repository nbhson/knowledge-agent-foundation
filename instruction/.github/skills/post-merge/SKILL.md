---
name: post-merge
description: Post-merge cleanup workflow - archive report, sync Jira, update manifest, and remove temporary artifacts after a PR is merged.
user-invocable: false
---

# Workflow: Post-Merge Sync

This skill defines the post-merge cleanup workflow that runs after a PR is confirmed merged. It handles report archiving, Jira status sync, and repository cleanup.

## Trigger

Run when a PR is confirmed merged (via MCP notification or developer confirmation). Never run on PR open or approval — only on confirmed merge. If merge is unconfirmed, stop after Phase 5 step 10.

---

## Required Steps & Phases

1. **Confirm the merge first**:
   - Merge commit or squash-merge SHA recorded (PR link + commit hash in hand).
   - Target branch is the agreed mainline (not a feature-to-feature merge — those do not trigger archiving).
   - If either is missing, stop and record "merge unconfirmed" — do not archive early.

2. **Update Jira Ticket Status**:
   - **Jira MCP available?** - Yes:
     - Transition ticket to 'Done' or 'Closed'
     - Add completion comment with PR link and summary
   - **Jira MCP available?** - No:
     - Provide manual steps: transition ticket + add comment
   - Skip for analysis-only workflows (Jira Ticket Investigate with no code change)

3. **Archive Report**:
   - Move the report from `.github/reports/<workflow-type>/` to `.github/reports/archive/YYYY-MM/` (month of the merge date).
   - Update `REPORTS.md` row status (active to archived, legacy-active to legacy-archived) AND repoint its link to `archive/YYYY-MM/<file>`.
   - Keep the archived copy for historical reference.
   - Verify after moving: the content-hash is content-based (filename-independent), so it stays valid — but re-run `npm run reports:check` to confirm manifest links resolve.

4. **Cleanup Temporary Artifacts**:
   - Delete `implementation_plan.md` if it exists at repository root.
   - Remove `.github/PHASE2_APPROVED` if present (approval marker is per-task, never carried over).
   - Clear any cached MCP sessions.

5. **Log Merge Event**:
   - Append one row to `.github/reports/merge-log.md` (create with header if missing):
     `| Date (YYYY-MM-DD HH:MM) | Ticket | Branch | PR link | Report file |`
   - File: `.github/reports/merge-log.md`
   - One row per merge; never rewrite history rows.

---

## Failure Handling (enterprise)

- **Merge unconfirmed**: stop before step 2; record state, resume when the merge SHA exists.
- **Jira sync fails**: keep the exact manual steps (status transition + comment text) in the report; never silently skip the sync.
- **Archive collision**: if the destination file already exists in `archive/YYYY-MM/`, stop and ask — never overwrite an archived report.
- **Missing artifacts**: if `implementation_plan.md` or the PR link is absent, record the gap explicitly in the report instead of inventing it.
- **Partial completion**: each step above records done/skipped-with-reason so a re-run resumes cleanly without double-archiving or double-logging the merge.

---

## Exit Criteria

- Jira ticket status updated (or manual instructions provided); merge SHA recorded.
- Report archived to `reports/archive/YYYY-MM/` (exactly one copy, manifest repointed + status flipped).
- `npm run reports:check` passes after the manifest change.
- Temporary artifacts cleaned up; merge logged with one row.
