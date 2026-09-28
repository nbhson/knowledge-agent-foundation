---
name: refactor
description: Step-by-step workflow for smell assessment, technical planning, incremental edits, unit test updates, and validation of refactored code in the Horizon 2 UI project.
---

# Workflow: Refactor

This document outlines the workflow for improving the structure, style, or performance of the codebase without breaking features in the Horizon 2 UI application.

---

## Required Steps & Phases

1. **Smell Assessment**: Identify candidates for refactoring (such as large modules that need decomposition into container/presenter roles, duplicate `@import` rules, hardcoded variables in SCSS, direct DOM manipulation, or duplicate interfaces).
2. **Plan & Get Approval**: Apply the Phase 2 threshold table (`.github/hooks/phase-2-planning.hook.md`) to decide artifact and approval pause. `implementation_plan.md` lifecycle is defined once in Phase 2 (root working doc, never committed, deleted after approval, carried into the Phase 5 report).
3. **Baseline Before Editing (no-behavior-change proof)**: Run the relevant test suite and record the baseline result BEFORE making changes (`npm run test` for affected specs). Any pre-existing failures are noted as baseline.
4. **Incremental Changes**: Make changes incrementally while preserving existing behavior. Keep refactoring sets focused, reuse shared assets, and strictly follow the project naming, module, and styling conventions.
   - Add/update `autoId` attributes for any touched template with interactive or viewable elements, following the [UI AutoId Skill](../ui-autoid/SKILL.md).
5. **Update Unit Tests**: Update corresponding unit tests in spec files (`*.spec.ts`) to match the refactored code and ensure proper mock configurations.
6. **Formatting & Quality Checks**: Follow the [Post Code Change Skill](../post-code-change/SKILL.md) for canonical lint, format, and cleanup requirements.
7. **Validation & Report**:
   - Re-run the same test suite and diff against the baseline: behavior diff must be empty (only structural changes allowed).
   - Run unit tests to verify no regressions: `npm run test`.
   - Run production compilation check: `npm run build`.
   - Manually test and inspect the layouts on local dev: `npm run startdev`.
   - File a Phase 5 report through the [Report Generation Skill](../report-generation/SKILL.md) including the baseline-vs-after comparison.
