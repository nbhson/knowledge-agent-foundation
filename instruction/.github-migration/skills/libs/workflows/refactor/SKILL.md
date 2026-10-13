---
name: refactor
description: Step-by-step workflow for smell assessment, technical planning, incremental edits, unit test updates, and validation of refactored code in the Horizon 2 UI project.
argument-hint: '<target modules> <smell/motivation>'
user-invocable: false
---

# Workflow: Refactor

This document outlines the workflow for improving the structure, style, or performance of the codebase without breaking features in the Horizon 2 UI application.

---

## Entry Criteria

- Refactor target and motivation stated (smell, debt, grouping) with affected modules listed.
- Blast radius mapped BEFORE planning: consumers of every touched declaration, export, route, provider, and `autoId` value (imports, lazy routes, store slices, automation selectors).
- Baseline test result recorded BEFORE editing (step 3); pre-existing failures noted as baseline, not caused by this task.

## Required Steps & Phases

1. **Smell Inventory (Phase 1)**: Turn the smell list into a checkable inventory — one row per smell with evidence, not adjectives. Structural and behavioral smells to cover: flat feature folders, misplaced API files, fragmented/overlapping NgModules, duplicated or anonymous types, component/service responsibility leaks, template-time calculations, repeated colors/constants, and components above 500 lines. Follow the organization and layer boundaries in [Angular Architecture §6](../../shared/angular-architecture/SKILL.md), the patterns in [Tech Stack](../../../../knowledge/tech-stack.md), and placement/naming in [Project Structure](../../../../knowledge/project-structure.md).

    | # | Smell | Evidence (`file:line`) | Playbook move (§4) |
    |---|-------|------------------------|--------------------|
    | 1 | … | … | … |

    Prioritize: shared-surface smells (store, services, routes) first for design agreement; leaf-local smells (single component internals) first for execution.
2. **Plan & Get Approval (Phase 2)**: Apply the Phase 2 threshold table (`.github/phases/phase-2-planning.md`) to decide artifact and approval pause. `implementation_plan.md` lifecycle is defined once in Phase 2 (root working doc, never committed, deleted after approval, carried into the Phase 5 report). The plan must include the smell inventory, the slice order (step 4), and the per-increment checkpoints — a plan that says "refactor the module" without slices is not approvable.
3. **Baseline Before Editing (Phase 3 — no-behavior-change proof)**: Run the relevant test suite and record the baseline result BEFORE making changes (`npm run test` for affected specs). Any pre-existing failures are noted as baseline. Where behavior is only covered manually, write characterization tests FIRST that pin current behavior (inputs → outputs), so the refactor has something to preserve.
4. **Slice & Move Incrementally (Phase 3)**: One slice = one cohesive move + green checkpoint. Never stack multiple moves on a red suite.

    - **Slice order**: agree on shared-surface decisions first (module boundaries, service ownership, DTO placement), then execute leaf-first (pipes/utils → presenters → services → module wiring), so each increment is independently verifiable.
    - **Increment size**: a single playbook move below (or a single folder grouping). If an increment touches more than ~5 files or crosses a module boundary, split it further.
    - **Split playbook** (pick by smell, concrete repo procedures in [Angular Architecture §6](../../shared/angular-architecture/SKILL.md)):
      - Visual block with own template section → extract presenter under `components/<name>/` (`@Input` in, `@Output` out, `OnPush`, no service injection).
      - Filtering/mapping/sort + store orchestration in component → move to feature service as mapped view-model observables; component subscribes and renders.
      - Formatting/date/class logic in template bindings → pure pipe or `utils/*.util.ts` with spec; bind the precomputed field.
      - Anonymous `groups`/`items` shapes → import owner DTOs (named group + item interfaces, e.g. `RoleDTO`/`RoleModule` pattern); backend vs UI models stay distinct with mapping in the service.
      - Flat folder with >8 mixed files → group per component/responsibility (target layout — only the module at root — see [Angular Architecture §6.6](../../shared/angular-architecture/SKILL.md)).
    - **Per-move checklist** (every increment, before calling it green):
      - Module wiring: declarations/imports/exports updated; no duplicate declarations; lazy route `loadChildren` intact.
      - Provider scope unchanged: moving a service between modules must not silently change its lifetime (root vs feature vs component scope).
      - Public surface intact: every export consumed elsewhere still resolves (search consumers from the entry-criteria blast radius).
      - Template bindings still clean: no new computation calls; `trackBy` preserved on moved loops.
      - `autoId` stability: moved elements keep their exact `autoId` values — renames break the automation contract (see [UI AutoId Skill](../../shared/ui-autoid/SKILL.md)). New elements get `autoId` per convention.
     - **Moved styles**: moved/merged `.scss` must follow [Styling Standards](../../shared/styling-standards/SKILL.md) (variable ownership, no global leakage, responsive intact) — a move that forks a token or drops a breakpoint is a failed checkpoint.
     - **Touched tracking**: moved templates with user activity keep their declarative `rum-*` attributes intact (see [RUM Skill](../../shared/rum-activity-tracking/SKILL.md)).
    - **Stop rules** — halt the slice sequence and re-plan when: any increment leaves tests red for reasons beyond mechanical updates; a move reveals a behavior difference (reclassify as Bug Fix / New Feature ticket); the slice grows past its planned file set (scope creep → new slice or new ticket).
    - Add/update `autoId` attributes for any touched template with interactive or viewable elements, following the [UI AutoId Skill](../../shared/ui-autoid/SKILL.md).
5. **Update Unit Tests — mechanical only (Phase 3)**: Update corresponding unit tests in spec files (`*.spec.ts`) to match the refactored code and ensure proper mock configurations. Allowed: import-path updates, selector updates for moved templates, mock re-wiring for moved providers. Forbidden: changing assertions, dropping cases, or loosening mocks to make the new structure pass — any test-logic change means the refactor changed behavior and must be justified as a separate ticket or reverted. Characterization tests from step 3 must pass unmodified.
6. **Formatting & Quality Checks (Phase 3)**: Follow the [Post Code Change Skill](../../shared/post-code-change/SKILL.md) for canonical lint, format, and cleanup requirements.
7. **Validation & Report (Phase 4 → Phase 5)**:
    - Re-run the same test suite and diff against the baseline: behavior diff must be empty (only structural changes allowed). Characterization tests pass unmodified.
    - Run unit tests to verify no regressions: `npm run test`.
    - Run production compilation check: `npm run build`.
    - Manually test and inspect the layouts on local dev: `npm run startdev` — walk the touched routes, confirm identical rendered output and interactions (visual/behavioral parity, not just "it loads").
    - File a Phase 5 report through the [Report Generation Skill](../../shared/report-generation/SKILL.md) including the move log (slice → files → checkpoint result) and the baseline-vs-after comparison.

## Scope Boundaries

- Structural changes only: no behavior, API-shape, or UI-contract changes. Any behavior change splits into a separate New Feature / Bug Fix ticket.
- Do not merge distinct lazy routes, public integration points, or independently owned features into one module.
- Do not rename stable `autoId` values or public exports as a side effect of moving files.

---

## Deliverables

- **Smell Inventory**: Each smell with `file:line` evidence and its assigned playbook move.
- **Slice Plan**: Ordered increments with per-increment checkpoints, from the approved plan.
- **Move Log**: Per slice — files moved/renamed, wiring changes, checkpoint result (green/blocked).
- **Baseline-vs-After Comparison**: Test results before and after, characterization tests unmodified and green.
- **Validation Evidence**: Lint, build, full-suite, and manual parity-walk notes.
- **Risk & Rollback Note**: Blast radius (consumers, routes, providers, automation) and the revert path per slice.

## Exit Criteria

- Baseline-vs-after test diff is empty (or every delta is explained and approved); characterization tests pass unmodified.
- Touched `.component.ts` files do not grow past the 500-line budget; new grouping follows the target layout.
- Module wiring verified (no duplicates, lazy routes intact, provider scopes unchanged); `autoId` values stable.
- Phase 5 report contains the move log, the baseline-vs-after comparison, and the rollback path (revert commit).
