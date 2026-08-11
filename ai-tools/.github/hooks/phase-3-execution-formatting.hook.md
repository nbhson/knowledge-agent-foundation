# Phase 3 Hook - Execution and Formatting (w/ Figma Fallback)

## Goal

Implement approved changes, update tests, and perform formatting/linting checks.

## Trigger

Run this hook only after Phase 2 approval.

## Required Steps

1. Convert approved plan into a concrete task list.
2. Implement code changes in focused increments.
3. For UI changes, verify the implementation against the design:
   - **Figma MCP available?** → Yes: compare against Figma specs (layout, spacing, colors, typography, labels, component states) with the design frame.
   - **Figma MCP available?** → No: ask the developer **once** to confirm the UI matches the design (or provide a screenshot); verify visually against the developer-provided reference.
   - Flag and resolve any discrepancies before writing tests.
4. Add or update unit tests where behavior is changed.
5. Execute linting and formatting:
   - `npm run lint`
   - `npm run format`
6. Generate a draft report using report templates from `.github/report-templates/`.

## Related Detailed Hooks

- `.github/skills/post-code-change/SKILL.md`
- `.github/skills/report-generation/SKILL.md`

## Custom Instruction Map & Resources

To optimize code quality and provide context-aware help, GitHub Copilot leverages knowledge files under `.github/knowledge/` and workflow skill files under `.github/skills/`.

### Resource Mapping by Workflow

**Priority — Read this section first**

Strictly follow the mapping below to load the correct workflow instructions, consult the relevant skills and core guidelines, and generate or use the appropriate templates.

Depending on the development task or workflow requested by the developer, Copilot should reference the corresponding guideline files and suggest the appropriate templates:

| **Active Workflow**    | **Workflow File to Load**                    | **Supporting Rules & Skills to Consult**                                                                                                                                                               | **Templates to Generate/Use & Reports**                                                                                                                                       |
| :--------------------- | :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bug Fix**            | `skills/bug-fix/SKILL.md`                    | `knowledge/core-engineering-guidelines.md`                                                                                                                                                             | `report-templates/bug-report.md`<br>**Report**: `BUG-REPORT-[TICKET-ID]-[DATE]-[TIME].ctx.md` → `.github/reports/`                                                             |
| **Feature Delivery**   | `skills/feature-delivery/SKILL.md`           | `knowledge/core-engineering-guidelines.md`<br>`skills/angular-architecture/SKILL.md`<br>`skills/styling-standards/SKILL.md`<br>`skills/ui-autoid/SKILL.md`                                             | `report-templates/technical-design.md` (planning)<br>`report-templates/engineering-report.md` (final)<br>`report-templates/pull-request.md` (PR)<br>**Report**: `ENGINEERING-REPORT-[FEATURE-NAME]-[DATE]-[TIME].ctx.md` → `.github/reports/` |
| **Refactor**           | `skills/refactor/SKILL.md`                   | `knowledge/core-engineering-guidelines.md`<br>`skills/angular-architecture/SKILL.md`<br>`skills/styling-standards/SKILL.md`<br>`skills/ui-autoid/SKILL.md`                                             | `report-templates/technical-design.md`<br>`report-templates/engineering-report.md`<br>**Report**: `REFACTOR-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` → `.github/reports/` |
| **Unit Test**          | `skills/unit-test/SKILL.md`                  | `knowledge/core-engineering-guidelines.md`<br>`skills/angular-architecture/SKILL.md`<br>`skills/ui-autoid/SKILL.md`                                                                                    | `report-templates/engineering-report.md`<br>**Report**: `TEST-REPORT-[COMPONENT-NAME]-[DATE]-[TIME].ctx.md` → `.github/reports/`                                                |
| **Code Review**        | `skills/code-review/SKILL.md`                | `knowledge/core-engineering-guidelines.md`<br>`skills/ui-autoid/SKILL.md`                                                                                                                              | `report-templates/pull-request.md`<br>**Report**: `CODE-REVIEW-[PR-ID]-[DATE]-[TIME].ctx.md` → `.github/reports/`                                                              |
| **Jira Ticket Review** | `skills/jira-ticket-review/SKILL.md`         | `knowledge/core-engineering-guidelines.md`                                                                                                                                                             | `report-templates/jira-ticket-review.md`<br>**Report**: `JIRA-REVIEW-[TICKET-ID]-[DATE]-[TIME].ctx.md` → `.github/reports/`                                                     |

## Exit Criteria

- Code and tests are updated.
- UI implementation matches the design reference (verified via Figma MCP when available; otherwise confirmed with the developer).
- Lint/format are completed.
- Draft report is created.