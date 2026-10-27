---
name: 'P-Unit-Test'
description: 'Strict P1→P5 Jest test delivery with mocks and red-green proof.'
argument-hint: '<target file.ts> <behaviors to verify>'
agent: 'p-standard'
---

# P-Unit-Test

Inputs: $ARGUMENTS (target `*.ts` + behaviors; existing spec read first).

Follow [.github/copilot-instructions.md](../copilot-instructions.md)
and [.github/phases/README.md](../phases/README.md) — full P1→P5.

- P1: Load `skills/unit-test/SKILL.md`. Jira MCP: fetch ticket, else ask dev once. Load at most one relevant report. List deps to mock (HTTP, services, routes, `provideMockStore`).
- P2: Test strategy per layer (component / service / pipe-util / NgRx). Approval when non-trivial.
- P3: Create task list, then spec beside source (`*.spec.ts`), transport mocks in owning API `*.mock.ts`. Prefer `autoId` selectors. Fail-first red then green. Lint/format per `skills/post-code-change/SKILL.md`.
- P4: `npm run test` (target spec then affected suites) + `npm run build`. Prepare the PR description and propose opening the PR. Run Reviewer diff check.
- P5: File report via `skills/report-generation/SKILL.md` (final-report template + hash + `REPORTS.md` row + Jira sync or manual steps).
