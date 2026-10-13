# Pull Request

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | code-review / new-feature |
| **Ticket/Feature** | [SP0168-XXXX]                  |
| **Date**           | [YYYY-MM-DD]                   |
| **Report File**    | `[filename].ctx.md`            |
| **SHA-256 Hash**   | `[auto-generated on save]`     |

## Jira Ticket

- **Ticket Key**: [SP0168-XXXX]
- **Ticket URL**: [https://jira.example.com/browse/SP0168-XXXX] *(required — must be filled)*

## Description & Context

[Detailed description of what problem this PR solves and context]

## Key Changes

- [Change 1]
- [Change 2]

## Acceptance Criteria Status

| # | Acceptance Criterion | Status | Evidence (file/line or test name) |
|---|----------------------|--------|-----------------------------------|
| 1 | [...] | ✅ Met / ⚠️ Partial | [...] |

> Build+test green alone is not enough — every AC needs evidence. Partials carry a follow-up ticket.

## Validation Evidence

- **Build**: [command + output excerpt]
- **Tests**: [command + output excerpt, red→green refs for fixes]
- **Manual**: [walkthrough notes for UI changes, or "docs-only, no build impact"]

## Quality Checklist

- [ ] Compiles successfully without errors
- [ ] Code formatted with Prettier and linted with ESLint
- [ ] Unit tests pass
- [ ] All commit messages follow `SP0168-<ticket number>: <short summary>`
- [ ] Layout verified manually on local dev
- [ ] Report saved to `.github/reports/<workflow-type>/` with valid SHA-256 hash

## Findings (code-review only — severity with boundaries)

List Blockers first with `file:line` + fix proposal + authoritative source.

- **Blocker** (must fix before merge; verdict → `Request changes`): breaks build/tests,
  runtime crash on touched path, data loss, auth bypass or secret leak, missing migration
  for breaking contract change, `autoId` contract break on automated element.
- **Major** (should fix before merge; verdict → `Request changes` unless deferred with owner):
  memory leak, wrong RxJS data flow, hardcoded secret-adjacent config, non-responsive layout,
  missing unit test for new behavior, scope creep.
- **Minor** (nit; verdict → `Approve` or `Comment`): unused import, formatting drift, typo,
  naming deviation, redundant dead code.

## P4-Lite Verification (embedded in Phase 5 — analysis-only, no code edits)

- **Diff hygiene**: `git diff --check` result (PASS/FAIL + output).
- **Build/test**: executed or explicitly skipped with reason (e.g. "docs-only, no build impact").
  Never claim green without evidence.
- **Verdict**: one of `Approve` / `Request changes` / `Comment` with blocking items listed first.

## Risks & Impact

[Potential side-effects on other modules or layout rendering]

## Scope Notes (deliberately excluded)

- [Excluded item → follow-up ticket; so "missing" scope reads as a decision, not an oversight]

## MCP Status

- **Jira**: Available / Manual fallback — [reason]

## Pull Request

- **Branch**: `[feat/feature-name | fix/ticket | refactor/name]`
- **Link**: [PR Link](url)
- **Verdict**: `Approve` / `Request changes` / `Comment`
