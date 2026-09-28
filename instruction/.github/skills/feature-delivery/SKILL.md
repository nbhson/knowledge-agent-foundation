---
name: feature-delivery
description: Step-by-step workflow for scoping, designing, building component logic, writing unit tests, and delivering new features in the Horizon 2 UI project.
---

# Workflow: Feature Delivery

This document outlines the workflow for developing and delivering new features in the Horizon 2 UI application, keeping them aligned with architecture and code standards.

---

## Required Steps & Phases

1. **Discovery & Setup**: Clarify scope, acceptance criteria, and affected modules. Map out the layout, modules involved, and identify any core dependencies, shared services, constants, models, and components that can be reused before adding new implementation.
2. **Plan & Get Approval**: Apply the Phase 2 threshold table (`.github/hooks/phase-2-planning.hook.md`) to decide artifact (chat draft vs `implementation_plan.md` file) and whether to pause for approval. Lifecycle of `implementation_plan.md` is defined once in Phase 2 (root working doc, never committed, deleted after approval, carried into the Phase 5 report).
3. **Develop Components & Logic**:
   - Follow [Core Engineering Guidelines](../../knowledge/core-engineering-guidelines.md) for all Angular 15 patterns (NgModule, OnPush, RxJS, etc.).
   - Separate container/orchestrator responsibilities from UI presenter components.
   - Use standard styles, variables, and common helper layouts.
   - Add/update `autoId` attributes for any touched template with interactive or viewable elements, following the [UI AutoId Skill](../ui-autoid/SKILL.md).
4. **Data Flows**: Integrate state logic using RxJS/NgRx as specified in [Core Engineering Guidelines](../../knowledge/core-engineering-guidelines.md#2-reactivity--state-management).
5. **Write Unit Tests**: Write or update unit tests inside the corresponding `*.spec.ts` files to test component renderings, data logic, and event flows.
6. **Formatting & Quality Checks**: Follow the [Post Code Change Skill](../post-code-change/SKILL.md) for canonical formatting, lint/format, and cleanup steps.
7. **Validation**:
   - Run unit tests to verify correctness (`npm run test`).
   - Run production compilation check (`npm run build`).
   - Verify layout and logs in the local browser (`npm run startdev`).
8. **Report & Submit**:
   - Validate and prepare PR readiness via Phase 4 (`.github/hooks/phase-4-validation-pr.hook.md`).
   - File the final report in Phase 5 via the [Report Generation Skill](../report-generation/SKILL.md) (engineering-report template + stable content-hash + `REPORTS.md` row). The P2 `technical-design.md` plan is a working doc; the P5 engineering report is the auditable record.

---

## Deliverables

- **Technical Design Summary**: Outlining architecture, modules, and component split.
- **Implementation**: Aligned with the project structure and styling rules.
- **Validation Evidence**: Proof of passing tests and production build checks.
