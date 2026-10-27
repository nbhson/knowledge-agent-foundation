# Workflow Phases Index (Strict Default — Phase-Gated Loading)

> NOTE: this folder holds **phase prompt files** (markdown guidance for Copilot
> to read), NOT executable hooks — files never execute. (Suffix renamed from
> legacy hook-md style to `phase-N-*.md` on 2026-10-12; no legacy-suffixed
> files remain.)
> Executable automation lives in `.github/hooks/*.json` (Copilot hooks:
> `phase-gates.json` enforces the Phase 2 approval gate via `preToolUse`,
> reminds lint/format via `postToolUse`, injects routing context via
> `sessionStart`) plus `report-lifecycle.sh` (run on demand via
> `bash .github/hooks/report-lifecycle.sh` — never auto-triggered).
> `phases/session.json` is a machine-readable mirror of the matrix below, not a hook dispatcher.

Strict mode is the default. Routing is owned by `session.json`
(`workflow_phase_config`):

<!-- ROUTING:START (generated from session.json — do not edit by hand; run bash .github/hooks/sync-routing.sh) -->
| Workflow | Phases |
|---|---|
| `bug-fix` | P1→P5 (full) |
| `code-review` | P1+P5 only (skips P2, P3, P4) |
| `jira-ticket-investigate` | P1+P5 only (skips P2, P3, P4) |
| `new-feature` | P1→P5 (full) |
| `refactor` | P1→P5 (full) |
| `unit-test` | P1→P5 (full) |
<!-- ROUTING:END -->

Load ONLY the files listed for the current phase. Do not preload future phases.
This keeps strict gates intact while keeping context lean.

## Execution Order

1. `phase-1-understanding.md`
2. `phase-2-planning.md`
3. `phase-3-execution-formatting.md`
4. `phase-4-validation-pr.md`
5. `phase-5-report-generation.md` (report + Jira sync; step 11 post-merge runs only after merge confirmation)

> Contradiction handling is mandatory across the flow:
> - Identify contradictions/ambiguities in Phase 1.
> - Resolve and freeze decisions before planning is approved in Phase 2.
> - Implement, validate, and report against the frozen decisions in Phases 3-5.

## Phase Load Index (load only this per phase)

| Phase | Hook file | Load (only this) |
|-------|-----------|------------------|
| 1 | `phase-1-understanding.md` | `copilot-instructions.md` (routing) + `knowledge/tech-stack.md` + `knowledge/project-structure.md` + the ONE matching `skills/<workflow>/SKILL.md` + at most ONE latest relevant report from `.github/reports/` + Jira context (MCP or one-time dev fallback) |
| 2 | `phase-2-planning.md` | Threshold table in Phase 2 + `reports/templates/implementation-plan.md` only when an `implementation_plan.md` file is required |
| 3 | `phase-3-execution-formatting.md` | Technical skills as needed: `angular-architecture`, `styling-standards`, `ui-autoid` + `post-code-change/SKILL.md` for lint/format + `report-generation/SKILL.md` + the ONE matching template for the draft report (step 6) |
| 4 | `phase-4-validation-pr.md` | `pre-pull-request/SKILL.md` + build/test outputs + AC + frozen-decision traces |
| 5 | `phase-5-report-generation.md` | `report-generation/SKILL.md` (finalize the Phase 3 draft) + the ONE matching template from `reports/templates/` + `post-merge/SKILL.md` (step 11 only, after merge confirmation) + `reports/merge-log.md` format |

## Phase to Hook Mapping

The hooks are:

- **Phase 1 - Understanding**: `phase-1-understanding.md`
- **Phase 2 - Planning**: `phase-2-planning.md`
- **Phase 3 - Execution & Formatting**: `phase-3-execution-formatting.md`
- **Phase 4 - Validation & PR**: `phase-4-validation-pr.md`
- **Phase 5 - Report Generation (+ Post-Merge)**: `phase-5-report-generation.md` (steps 1–10 report + Jira sync; step 11 post-merge via `skills/post-merge/SKILL.md` only after merge confirmation)

## Inputs and Outputs

- **Input**: Developer request + workflow type + any Jira context available.
- **Output**: Implementation, validation evidence, and final report artifact in `.github/reports/` for every code change.

## Rule Source of Truth

Detailed behavior and strict-default rules are defined in
`.github/copilot-instructions.md`. Workflow → phases mapping is owned SOLELY by
`session.json` → `workflow_phase_config` (this README's matrix above is its
human-readable mirror — generated from it, never edited independently).
Enforcement, where the harness supports it, is
`.github/hooks/phase-gates.json`.

This file is the single loading index; phase files must not duplicate its table.
Workflow → template + report filename mapping lives in exactly one place:
`skills/report-generation/SKILL.md` §1. No other file may copy these tables —
link to the owner instead.

## Related Guidance

- `.github/skills/post-code-change/SKILL.md`
- `.github/skills/report-generation/SKILL.md`
- `.github/skills/pre-pull-request/SKILL.md`

## Execution Notes

- Follow the phase order above; analysis-only review workflows execute P1+P5 with the P4-lite review checks embedded in Phase 5.
- Contradiction handling remains mandatory across the flow: identify, resolve, freeze, and verify decisions in later phases.
- Quick mode (`p-express` agent, selected in the agents dropdown — no prefix) is opt-in only and never the default. Trivial vs non-trivial threshold is defined once in `phase-2-planning.md`; `session.json:quick_mode` is a pointer-only block.

## Extending the Framework

- **New skill**: create `.github/skills/<name>/SKILL.md` (`name` + `description`
  frontmatter); reference it in `copilot-instructions.md`; add to `session.json`
  only if it needs a new phase trigger.
- **New phase prompt**: create `.github/phases/phase-N-<name>.md` (Goal,
  Trigger, Required Steps, Exit Criteria, Edge Cases); register in `session.json`;
  update this index + `copilot-instructions.md`.
- **Executable automation**: `.github/hooks/report-lifecycle.sh` runs on demand
  (`bash .github/hooks/report-lifecycle.sh [--check|--dry-run]`; `npm run reports*`
  only where a package.json exists) — e.g. monthly or after merging to main.
  `phases/` = markdown prompts only; `hooks/` = automation scripts.
  Do not mix the two.

## Contributing

When modifying `.github/`: run `bash .github/hooks/check-refs.sh` to verify
every `.github/...` ref points to an existing file; keep refs canonical
(`.github/...`); test strict + adaptive modes.

Windows 11: run the hooks from Git Bash (ships with Git for Windows) with
Python installed — scripts auto-pick `python3`, `python`, or `py -3`.
Line endings for hooks are forced to LF via `.gitattributes`, so any
`core.autocrlf` setting can't break the bash shebangs.
