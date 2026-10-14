---
name: new-feature
description: Step-by-step workflow for scoping, designing, building component logic, writing unit tests, and delivering new features in the Horizon 2 UI project.
argument-hint: '<Jira-key> <short-desc + AC>'
user-invocable: false
---

# Workflow: New Feature

> **Strict execution — full P1→P5.** Follow `.github/copilot-instructions.md` and the load index in `.github/phases/README.md` in order. P2 needs explicit approval before edits; P4 needs build + tests + every AC traced + every frozen decision applied; P5 files the report via `report-generation/SKILL.md`. Load only the current phase's files.

This document outlines the workflow for developing and delivering new features in the Horizon 2 UI application, keeping them aligned with architecture and code standards.

---

## Entry Criteria

- Scope and acceptance criteria are available (Jira ticket or dev-provided summary); every AC is testable or flagged per the [Jira Ticket Investigate Skill](../../workflows/jira-ticket-investigate/SKILL.md).
- Target workflow confirmed as New Feature (not bug fix / refactor in disguise).
- Phase 1 contradiction scan completed; blocking ambiguities listed before planning.
- Reusable landscape surveyed: existing services, constants, models, utils, pipes, components, and the owning domain folder identified before any new file is created.

## Required Steps & Phases

1. **Discovery & Setup (Phase 1)**: Clarify scope and acceptance criteria; map feature folders, NgModules, API/service/component ownership, and consumers. Identify module consolidation opportunities without merging distinct lazy routes or independently owned features. Search for reusable services, constants, models, utils, pipes, and components before adding new implementation. Apply the four Code Organization, Architecture, Type Safety, and Frontend Maintainability checks in [Angular Architecture §6](../../shared/angular-architecture/SKILL.md).
    - **Placement pre-flight** (all checkable, see [Angular Architecture §6](../../shared/angular-architecture/SKILL.md) + [Project Structure](../../../../knowledge/project-structure.md)): (a) new API files go to `src/api/<area>/<feature>/` — never a local `api/` folder inside the feature; list sibling `src/api/<area>/` folders first; (b) feature-private kinds go to the matching `<feature>/` subfolder (`components/`, `directives/`, `pipes/`, `services/`, `models/`, `constants/`, `enums/`, `validators/`, `guards/`, `interceptors/`, `utils/`, `store/` — create only the kinds the feature needs, no empty placeholders); app-wide kinds go to `src/shared|constants|models|scss/` (e.g. `EMPTY_STRING` → `src/constants/constants.ts`) — promote on second use, never deep-import a sibling feature; (c) new object shapes reuse owner `dto/`/`models/` interfaces (never anonymous inline types); (d) new string/color literals reuse `EMPTY_STRING` and the owner `color.constants.ts` (plural naming); (e) new `.component.ts` gets a 500-line budget from the first commit with grouping per §6.6; (f) no computation calls in template bindings — precompute in the service or use a pure pipe.
    - **Contract-first**: define the API DTO shape, the view-model shape, and the mapping between them up front (owner `dto/` vs `models/`); list new routes/guards and required state (local vs NgRx) before coding.
2. **Design Decisions (Phase 2)**: Record the decisions that shape the implementation, so reviewers can judge them instead of rediscovering them:
    - Component split: which container orchestrates, which presenters render (inputs in, outputs out, `OnPush`, no service injection in presenters).
    - Options considered and rejected, with one-line reasons (e.g. shared vs feature-local service, new module vs existing module).
    - UI states covered by design: loading, error, empty, and permission-denied — each with its observable trigger and template branch.
    - Tracking plan: `autoId` values for new interactive/viewable elements (see [UI AutoId Skill](../../shared/ui-autoid/SKILL.md)) and declarative `rum-*` attributes where user activity matters (see [RUM Skill](../../shared/rum-activity-tracking/SKILL.md)).
3. **Plan & Get Approval (Phase 2)**: Apply the Phase 2 threshold table (`.github/phases/phase-2-planning.md`) to decide artifact (chat draft vs `implementation_plan.md` file) and whether to pause for approval. Lifecycle of `implementation_plan.md` is defined once in Phase 2 (root working doc, never committed, deleted after approval, carried into the Phase 5 report).
4. **Implement Components & Logic (Phase 3)**:
    - Follow [Tech Stack](../../../../knowledge/tech-stack.md) for all Angular 15 patterns (NgModule, OnPush, RxJS, etc.) and [Project Structure](../../../../knowledge/project-structure.md) for placement/naming.
    - Keep data flow `API -> service -> component`; place DTOs, models, constants, and colors with their owning layer. Do not put business calculations in template bindings; keep each `.component.ts` at or below 500 lines and split only at cohesive responsibility boundaries.
    - Separate container/orchestrator responsibilities from UI presenter components.
    - Wire state with RxJS/NgRx per [Tech Stack](../../../../knowledge/tech-stack.md#reactivity--state-management): feature service owns mapping, query orchestration, and loading/error state; subscriptions cleaned up via `takeUntil` or `async` pipe.
    - Use standard styles, variables, and common helper layouts (see [Styling Standards](../../shared/styling-standards/SKILL.md)).
    - Add/update `autoId` attributes and `rum-*` attributes per the step-2 tracking plan.
5. **Write Unit Tests (Phase 3)**: Write or update unit tests inside the corresponding `*.spec.ts` files. Each acceptance criterion gets at least one happy path, one edge case (empty/null/extreme), and one error flow; follow the quality bar in the [Unit Test Skill](../../workflows/unit-test/SKILL.md).
6. **Formatting & Quality Checks (Phase 3)**: Follow the [Post Code Change Skill](../../shared/post-code-change/SKILL.md) for canonical formatting, lint/format, and cleanup steps.
7. **Validation (Phase 4)**:
    - Run unit tests to verify correctness (`npm run test`).
    - Run production compilation check (`npm run build`).
    - Verify manually in the local browser (`npm run startdev`): walk every AC, plus loading/error/empty/denied states, desktop and narrow viewports, and keyboard/focus behavior on new interactive elements.
8. **Report & Submit (Phase 4 → Phase 5)**:
    - Validate and prepare PR readiness via Phase 4 (`.github/phases/phase-4-validation-pr.md`).
    - File the final report in Phase 5 via the [Report Generation Skill](../../shared/report-generation/SKILL.md) (final-report template + stable content-hash + `REPORTS.md` row). The P2 `implementation-plan.md` plan is a working doc; the P5 final report is the auditable record.

## Scope Boundaries

- In scope: feature code, its unit tests, touched templates/styles, docs directly affected.
- Out of scope (require a separate ticket): unrelated refactors, shared-service redesigns, data migrations, releases/deployments.

---

## Deliverables

- **Implementation Plan Summary**: Outlining architecture, modules, and component split.
- **Design-Decision Log**: Options considered/rejected, container/presenter split, state ownership, and UI-state coverage — carried into the Phase 5 report.
- **Implementation**: Aligned with the project structure and styling rules.
- **Validation Evidence**: Proof of passing tests and production build checks, plus manual walkthrough notes (states × viewports).
- **Traceability**: Each acceptance criterion mapped to implementation (`file:line`) and/or test name — carried into the Phase 5 report.
- **Risk & Rollback Note**: Side effects on other modules, backward compatibility, and how to revert (revert commit / feature flag / follow-up ticket).

## Exit Criteria

- Every AC traced to implementation and/or tests; every contradiction decision applied.
- Loading/error/empty/denied states verified manually; no new lint/test/build failures.
- Phase 5 report filed with the design-decision log, traceability, and rollback path.
