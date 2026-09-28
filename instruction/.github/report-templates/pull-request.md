# Pull Request

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | code-review / feature-delivery |
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

## Quality Checklist

- [ ] Compiles successfully without errors
- [ ] Code formatted with Prettier and linted with ESLint
- [ ] Unit tests pass
- [ ] All commit messages follow `SP0168-<ticket number>: <short summary>`
- [ ] Layout verified manually on local dev
- [ ] Report saved to `.github/reports/` with valid SHA-256 hash

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

## MCP Status

- **Jira**: Available / Manual fallback — [reason]
- **Figma**: Available / Manual fallback — [reason]
- **Bitbucket**: Available / Manual fallback — [reason]

## Pull Request

- **Branch**: `[feat/feature-name | fix/ticket | refactor/name]`
- **Link**: [PR Link](url)
- **Verdict**: `Approve` / `Request changes` / `Comment`
