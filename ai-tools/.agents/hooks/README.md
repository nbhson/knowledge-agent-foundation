# Workflow Hooks Index

This folder contains phase-based hooks derived from the Developer Workflow Orchestration mermaid chart in `.agents/copilot-instructions.md`.

## Execution Order

1. `phase-1-understanding.hook.md`
2. `phase-2-planning.hook.md`
3. `phase-3-execution-formatting.hook.md`
4. `phase-4-validation-pr.hook.md`
5. `phase-5-report-generation.hook.md`

## Phase to Hook Mapping

[Priority] Strictly apply all that is mentioned in these hooks before making any code changes. The hooks are:

- **Phase 1 - Understanding**: `phase-1-understanding.hook.md`
- **Phase 2 - Planning**: `phase-2-planning.hook.md`
- **Phase 3 - Execution & Formatting**: `phase-3-execution-formatting.hook.md`
- **Phase 4 - Validation & PR**: `phase-4-validation-pr.hook.md`
- **Phase 5 - Report Generation**: `phase-5-report-generation.hook.md`

## Inputs and Outputs

- **Input**: Developer request + selected workflow type (Bug Fix, Feature Delivery, Refactor, Unit Test, Code Review, Jira Ticket Review).
- **Output**: Validated changes, report artifact in `.agents/reports/`, and PR-ready summary when applicable.

## Integration with Existing Hook Instructions

The phase hooks orchestrate the process and must be used with the detailed skills:

- `.agents/skills/post-code-change/SKILL.md`
- `.agents/skills/report-generation/SKILL.md`
- `.agents/skills/pre-pull-request/SKILL.md`

## Strict Mode (Always-On)

Strict, step-by-step execution is the default behavior for all tasks:

1. Read `.agents/` before implementation.
2. Execute hooks in exact order:
   1. `.agents/hooks/phase-1-understanding.hook.md`
   2. `.agents/hooks/phase-2-planning.hook.md`
   3. `.agents/hooks/phase-3-execution-formatting.hook.md`
   4. `.agents/hooks/phase-4-validation-pr.hook.md`
   5. `.agents/hooks/phase-5-report-generation.hook.md`
3. Do not skip phase hooks or their order; the Phase 2 approval gate is mandatory for non-trivial tasks, while trivial/no-code queries may proceed after presenting the draft plan.
4. Before implementation, print a checklist of hook steps to run.
5. Before finishing, print a completion checklist mapped to each hook.
6. If Phase 4 validation fails, loop back to Phase 3 to apply fixes, then re-run Phase 4.

## Strict Mode Completion Contract

For every task, the response should include:

1. Pre-implementation checklist by phase hook.
2. Planning gate status (approved or needs refinement).
3. Execution summary (code changes, test updates, lint/format status).
4. Validation summary (`build`, `test`, report generation, PR readiness).
