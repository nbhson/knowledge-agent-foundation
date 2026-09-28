# Phase X Hook - Post-Merge Sync (w/ Fallback)

## Goal

After a PR is merged, sync the Jira ticket status and perform cleanup.

## Trigger

Run this hook when a PR is confirmed merged (via MCP notification or developer confirmation).

## Required Steps

1. **Update Jira Ticket Status**:
   - **Jira MCP available?** → Yes:
     - Transition ticket to "Done" or "Closed"
     - Add completion comment with PR link and summary
   - **Jira MCP available?** → No:
     - Provide manual steps: transition ticket + add comment
   - Skip for analysis-only workflows (Jira Ticket Review with no code change)

2. **Archive Report**:
   - Move the report from `.github/reports/` to `.github/reports/archive/YYYY-MM/`
   - Update REPORTS.md row status from "active" to "archived"
   - Keep the archived copy for historical reference

3. **Cleanup Temporary Artifacts**:
   - Delete `implementation_plan.md` if it exists at repository root
   - Clear any cached MCP sessions

4. **Log Merge Event**:
   - Append one row to `.github/reports/merge-log.md` (create with header if missing):
     `| Date (YYYY-MM-DD HH:MM) | Ticket | Branch | PR link | Report file |`
   - File: `.github/reports/merge-log.md`

## Exit Criteria

- Jira ticket status updated (or manual instructions provided)
- Report archived to `reports/archive/YYYY-MM/`
- REPORTS.md updated with archived status
- Temporary artifacts cleaned up
