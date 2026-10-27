---
name: 'P-Code-Review'
description: 'Analysis-only P1+P5 peer review with checklist and PR notes.'
argument-hint: '<PR link or branch range> <ticket/design context>'
agent: 'p-standard'
---

# P-Code-Review

Inputs: $ARGUMENTS (diff under review + ticket/design context).

Follow [.github/copilot-instructions.md](../copilot-instructions.md)
and [.github/phases/README.md](../phases/README.md) — analysis-only P1+P5, no code edits.

- P1: Load `skills/code-review/SKILL.md` + `knowledge/tech-stack.md` + `knowledge/project-structure.md`. Load at most one relevant report. Walk passes: correctness → tests → conventions. Cite `file:line`.
- Skip P2–P4 entirely (no planning, no edits, no build/test gates, no PR creation).
- P5: Output pull-request notes per `skills/report-generation/SKILL.md` (findings by severity Major/Minor, no implementation).
