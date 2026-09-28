# Workflow Hooks Index (Strict Default — Phase-Gated Loading)

Strict mode is the default. Execute the phase matrix in `session.json`
(`workflow_phase_config`) in order: full P1→P5 for code-delivery workflows
(feature-delivery, bug-fix, refactor, unit-test); P1+P5 for analysis-only
workflows (code-review, jira-ticket-review).

Load ONLY the files listed for the current phase. Do not preload future phases.
This keeps strict gates intact while keeping context lean.

## Execution Order

1. `phase-1-understanding.hook.md`
2. `phase-2-planning.hook.md`
3. `phase-3-execution-formatting.hook.md`
4. `phase-4-validation-pr.hook.md`
5. `phase-5-report-generation.hook.md`
6. `post-merge.hook.md` (after merge confirmation)

> Contradiction handling is mandatory across the flow:
> - Identify contradictions/ambiguities in Phase 1.
> - Resolve and freeze decisions before planning is approved in Phase 2.
> - Implement, validate, and report against the frozen decisions in Phases 3-5.

## Phase Load Index (load only this per phase)

| Phase | Hook file | Load (only this) |
|-------|-----------|------------------|
| 1 | `phase-1-understanding.hook.md` | `copilot-instructions.md` (routing) + `knowledge/core-engineering-guidelines.md` + the ONE matching `skills/<workflow>/SKILL.md` + at most ONE latest relevant report from `.github/reports/` + Jira/Figma context (MCP or one-time dev fallback) |
| 2 | `phase-2-planning.hook.md` | Threshold table in Phase 2 + `report-templates/technical-design.md` only when an `implementation_plan.md` file is required |
| 3 | `phase-3-execution-formatting.hook.md` | Technical skills as needed: `angular-architecture`, `styling-standards`, `ui-autoid` + `post-code-change/SKILL.md` for lint/format |
| 4 | `phase-4-validation-pr.hook.md` | `pre-pull-request/SKILL.md` + build/test outputs + AC + frozen-decision traces |
| 5 | `phase-5-report-generation.hook.md` | `report-generation/SKILL.md` + the ONE matching template from `report-templates/` |
| X | `post-merge.hook.md` | `post-merge/SKILL.md` + the merged report + `reports/merge-log.md` format |

## Phase to Hook Mapping

The hooks are:

- **Phase 1 - Understanding**: `phase-1-understanding.hook.md`
- **Phase 2 - Planning**: `phase-2-planning.hook.md`
- **Phase 3 - Execution & Formatting**: `phase-3-execution-formatting.hook.md`
- **Phase 4 - Validation & PR**: `phase-4-validation-pr.hook.md`
- **Phase 5 - Report Generation**: `phase-5-report-generation.hook.md`
- **Phase X - Post-Merge**: `post-merge.hook.md`

## Inputs and Outputs

- **Input**: Developer request + workflow type + any Jira/Figma/Bitbucket context available.
- **Output**: Implementation, validation evidence, and final report artifact in `.github/reports/` for every code change.

## Rule Source of Truth

Detailed behavior, strict-default rules, and workflow routing are defined in
`.github/copilot-instructions.md` and `.github/hooks/session.json`
(`workflow_phase_config` + `guard_hooks`).

This file is the single loading index; phase hooks must not duplicate its table.

## Related Guidance

- `.github/skills/post-code-change/SKILL.md`
- `.github/skills/report-generation/SKILL.md`
- `.github/skills/pre-pull-request/SKILL.md`

## Execution Notes

- Follow the phase order above; analysis-only review workflows execute P1+P5 with the P4-lite review checks embedded in Phase 5.
- Contradiction handling remains mandatory across the flow: identify, resolve, freeze, and verify decisions in later phases.
- Quick mode (`quick:` prefix, `adaptive-rules` agent) is legacy opt-in only and never the default. Trivial vs non-trivial threshold is defined once in `phase-2-planning.hook.md`; `session.json:quick_mode` is a pointer-only block.
