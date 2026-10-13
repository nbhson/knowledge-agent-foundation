---
name: h2-jira-ticket-investigate
description: Analysis-only P1+P5 ticket triage with AC scoring and next-step routing.
disable-model-invocation: true
argument-hint: '<Jira-key> (or paste summary when MCP offline)'
---
# H2-Jira-Ticket-Investigate

Inputs: $ARGUMENTS (ticket key; or pasted summary when Jira MCP unreachable — ask once).

Follow [.github/copilot-instructions.md](../../copilot-instructions.md)
and [.github/phases/README.md](../../phases/README.md) — analysis-only P1+P5, no code edits.

- P1: Load `skills/libs/workflows/jira-ticket-investigate/SKILL.md`. Load at most one relevant report. Record anatomy (problem, scope, verbatim AC, priority, links, env). Score each AC testable / non-testable with rewrite proposal. Map technical impact + route to Bug Fix / New Feature / Refactor / Not ready.
- Skip P2–P4 entirely.
- P5: File `jira-ticket-investigate.md` report via `skills/libs/shared/report-generation/SKILL.md` (template + hash + `REPORTS.md` row).
