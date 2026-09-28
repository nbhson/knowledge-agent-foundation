# Technical Design Document (Phase 2 Working Doc)

> Working document for the Phase 2 approval gate. Lives at repo root as
> `implementation_plan.md` (never committed), deleted after approval; its
> content is carried into the Phase 5 final report. See
> `phase-2-planning.hook.md` threshold table for when this file is required
> (shared surface, security-sensitive, or multi-module work) vs a chat draft.
> Filled golden example: `report-templates/examples/technical-design-example.md`.

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | feature-delivery / refactor    |
| **Ticket/Feature** | [SP0168-XXXX or feature name]  |
| **Date**           | [YYYY-MM-DD]                   |
| **Author**         | [developer + agent]            |
| **Status**         | [draft / approved / superseded] |

## Jira Ticket

- **Ticket Key**: [SP0168-XXXX]
- **Ticket URL**: [https://jira.example.com/browse/SP0168-XXXX] *(required — must be filled)*
- **Acceptance Criteria** (copied verbatim, numbered; mark each testable / non-testable):
  1. [AC-1] — testable via [test/manual path]
  2. [AC-2] — NON-TESTABLE as written → proposed rewrite: [...]

## 1. Problem & Background

[What breaks or is missing, with grounded evidence: `file:line`, ticket field, or Figma frame. No uncited claims.]

## 2. Goals & Non-Goals

- **Goals**: [numbered, each traceable to an AC]
- **Non-Goals** (explicit out of scope — prevents creep): [...]

## 3. Current State (as-is)

[How the code works today: modules, data flow (RxJS/NgRx), UI structure. Cite `file:line` per component. Note baseline test result for refactors.]

## 4. Proposed Design (to-be)

[Components (container vs presenter split), services/state changes, module
registration (`declarations`/`exports`), routing (`loadChildren` if lazy),
SCSS plan (variables, responsive breakpoints), `autoId` additions.
Include a minimal diagram or file tree when multi-module.]

## 5. Options Considered & Rejected

| Option | Why rejected (evidence/source) |
|--------|-------------------------------|
| [e.g., standalone component] | [Not available in Angular 15 — official docs v15] |
| [e.g., duplicate util] | [Exists at `src/...:line` — reuse instead] |

## 6. Contradictions & Frozen Decisions

| # | Conflict (sources) | Frozen decision + owner | Affects (files/tests) |
|---|--------------------|------------------------|----------------------|
| 1 | [ticket vs design vs code] | [decision, approved by X] | [...] |

## 7. Test Plan

- **New/updated specs**: [`*.spec.ts` paths] — fail-first (red) then green.
- **Selectors**: prefer `autoId` (`[autoId="..."]`).
- **Manual checks**: [`npm run startdev` scenarios, screenshots].

## 8. Validation & Rollout

- [ ] `npm run lint` + `npm run format`
- [ ] `npm run test` (affected suites + full if shared surface)
- [ ] `npm run build` / `build-prod`
- [ ] AC trace preview (each AC → file/test)
- [ ] Rollback plan: [revert scope, migration reversal if any]

## 9. Risks & Mitigation

| Risk | Likelihood / Impact | Mitigation |
|------|--------------------|------------|
| [...] | [.../...] | [...] |

## 10. Open Questions (must be empty before approval, except deferred with owner)

- [ ] [question → owner → decision]
