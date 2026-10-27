---
name: post-code-change
description: Automated post-code modification rules for cleaning imports, formatting files, running ESLint and checking for credentials in the Horizon 2 UI project.
user-invocable: false
---

# Skill: Post Code Change

After making code changes, execute the following quality and verification steps.
Do NOT generate any report here — the draft report is created in Phase 3 and
the final report in Phase 5, both via the [Report Generation Skill](../report-generation/SKILL.md).
This skill covers lint/format/cleanup only.

---

## Run Order (follow in sequence — each step gates the next)

1. **Scope check**: `git status` + `git diff --stat`. Every touched file must belong to the approved plan. Revert strays now, not at PR time.
2. **Format**: `npm run format` on the touched files. If the command rewrites files outside the plan scope, stop — the formatter config drifted; fix the scope before continuing.
3. **Lint**: `npm run lint` on the touched files. Zero new warnings. A pre-existing warning on a touched line becomes your responsibility once you touch the line — fix it or record why not.
4. **Mechanical convention checks** on every touched file (procedures in [Angular Architecture §6](../angular-architecture/SKILL.md)):
   - Grep touched `.html` for computation calls in bindings (must be property / `async` / pure pipe / handler / `trackBy` only).
   - Count lines of touched `.component.ts` (must not grow past 500; report `wc -l` per file).
   - Replace new `''` literals with `EMPTY_STRING` from the correct constants module (app vs library layer).
   - Types: no new `any`, no new inline interfaces — reuse owner `dto/`/`models/` types (see [Angular Architecture §6.2](../angular-architecture/SKILL.md)).
   - `autoId`: new interactive/viewable elements in touched templates carry `autoId` (see [UI AutoId Skill](../ui-autoid/SKILL.md)); existing values untouched.
5. **Clean Code**: Remove unused imports, variables, class properties, dead code, stray `console.log`s, and commented-out blocks introduced by this change.
6. **Security Check**: Verify that no credentials, passwords, client secrets, API tokens, PII, or sensitive values were introduced. Grep the diff for `password|secret|token|api[_-]?key|private[_-]?key|ssn` (case-insensitive) and eyeball every hit. Any hit stops the flow — remove and rotate if it was ever committed.
7. **Diff self-review**: Read the full diff hunk by hunk. For each hunk state keep (planned) or drop (stray). A hunk you cannot justify in one sentence does not ship.

## On Failure

- **Format churns unrelated files** → do not commit the churn; fix formatter scope/config first.
- **Lint fails on pre-existing issues outside your lines** → leave them, record in the report; fix only your lines.
- **Secret hit** → stop, remove, check git history for exposure, escalate before any push.

## Required Steps (summary)

1. **Format & Lint**: Run formatting and linting for the modified files or package scripts:
   - `npm run lint`
   - `npm run format`

2. **Clean Code**: Remove unused imports, variables, class properties, or dead code. Then run the mechanical convention checks on every touched file (procedures in [Angular Architecture §6](../angular-architecture/SKILL.md)): grep touched `.html` for computation calls in bindings (must be property / `async` / pure pipe / handler / `trackBy` only); count lines of touched `.component.ts` (must not grow past 500); replace new `''` literals with `EMPTY_STRING` from the correct constants module. Types: no new `any`, no new inline interfaces — reuse owner `dto/`/`models/` types (see [Angular Architecture §6.2](../angular-architecture/SKILL.md)). autoId: new interactive/viewable elements in touched templates carry `autoId` (see [UI AutoId Skill](../ui-autoid/SKILL.md)).

3. **Security Check**: Verify that no credentials, passwords, client secrets, API tokens, or sensitive values were introduced.

4. **Alignment Verification**: Ensure all changes remain aligned with [Tech Stack](../../knowledge/tech-stack.md) and [Project Structure](../../knowledge/project-structure.md).

5. **Handoff**: Return to the workflow Phase 3/4 flow. Report drafting happens
   in Phase 3 and finalization in Phase 5, both via the
   [Report Generation Skill](../report-generation/SKILL.md), not here.

---

## Verification Matrix (enterprise)

| Check | Gate | Evidence |
|---|---|---|
| Scope matches approved plan | Required | `git status` / `diff --stat`, strays reverted |
| `npm run format` clean on touched files | Required | Command output, no diffs remaining |
| `npm run lint` clean on touched files | Required | Command output, zero new warnings |
| No `any`, no new inline interfaces | Required | Reuse owner `dto/`/`models/` types |
| No new `''` literals | Required | `EMPTY_STRING` from the correct layer module |
| No computation calls in touched bindings | Required | Property / `async` / pure pipe / handler / `trackBy` only |
| Touched `.component.ts` within 500-line budget | Required | `wc -l` per file reported |
| `autoId` on new interactive/viewable elements | Required | Naming per `ui-autoid` skill |
| No secrets / tokens / PII in diff | Blocking | Manual + grep check; stop on any hit |
| No unrelated files in diff | Required | Each hunk justified or reverted |

---

## Related Templates

- **Bug Report**: `.github/reports/templates/bug-report.md`
- **Final Report**: `.github/reports/templates/final-report.md`
- **PR Description**: `.github/reports/templates/pr-description.md`
- **Jira Ticket Investigate**: `.github/reports/templates/jira-ticket-investigate.md`
