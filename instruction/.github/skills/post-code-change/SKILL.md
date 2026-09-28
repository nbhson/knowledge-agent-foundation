---
name: post-code-change
description: Automated post-code modification rules for cleaning imports, formatting files, running ESLint and checking for credentials in the Horizon 2 UI project.
---

# Skill: Post Code Change

After making code changes, execute the following quality and verification steps.
Do NOT generate any report here — draft/final reports are owned by the Phase 3
hook via the [Report Generation Skill](../report-generation/SKILL.md) (Phase 5).
This skill covers lint/format/cleanup only.

---

## Required Steps

1. **Format & Lint**: Run formatting and linting for the modified files or package scripts:
   - `npm run lint`
   - `npm run format`

2. **Clean Code**: Remove unused imports, variables, class properties, or dead code.

3. **Security Check**: Verify that no credentials, passwords, client secrets, API tokens, or sensitive values were introduced.

4. **Alignment Verification**: Ensure all changes remain aligned with the [Core Engineering Guidelines](../../knowledge/core-engineering-guidelines.md).

5. **Handoff**: Return to the workflow Phase 3/4 flow. Report drafting happens
   in the [Report Generation Skill](../report-generation/SKILL.md), not here.

---

## Related Templates

- **Bug Report**: `.github/report-templates/bug-report.md`
- **Engineering Report**: `.github/report-templates/engineering-report.md`
- **Pull Request**: `.github/report-templates/pull-request.md`
- **Jira Ticket Review**: `.github/report-templates/jira-ticket-review.md`
