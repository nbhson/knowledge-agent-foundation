---
name: post-merge
description: Post-merge cleanup workflow — archive report, sync Jira, update manifest, and remove temporary artifacts after a PR is merged.
---

# Workflow: Post-Merge Sync

This skill defines the post-merge cleanup workflow that runs after a PR is confirmed merged. It handles report archiving, Jira status sync, and repository cleanup.

---

## Required Steps & Phases

1. **Update Jira Ticket Status**:
   - **Jira MCP available?** → Yes:
     - Transition ticket to "Done" or "Closed"
     - Add completion comment with PR link and summary
   - **Jira MCP available?** → No:
     - Provide manual steps: transition ticket + add comment
   - Skip for analysis-only workflows (Jira Ticket Review with no code change)

2. **Archive Report**:
   - Move the report from `.github/reports/` to `.github/reports/archive/YYYY-MM/`
   - Update `REPORTS.md` row status from "active" to "archived"
   - Keep the archived copy for historical reference

3. **Cleanup Temporary Artifacts**:
   - Delete `implementation_plan.md` if it exists at repository root
   - Clear any cached MCP sessions

4. **Log Merge Event**:
   - Record merge timestamp, branch, PR link, and Jira ticket in `.github/reports/merge-log.md`

---

## Exit Criteria

- Jira ticket status updated (or manual instructions provided)
- Report archived to `reports/archive/YYYY-MM/`
- `REPORTS.md` updated with archived status
- Temporary artifacts cleaned up
