# Technical Design Document (Phase 2 Working Doc) — GOLDEN EXAMPLE (fictional)

> EXAMPLE ONLY — every section below shows the expected depth for a real plan.
> Fictional ticket/component; `file:line` values illustrate citation format.

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | feature-delivery               |
| **Ticket/Feature** | SP0168-3417                    |
| **Date**           | 2026-09-11                     |
| **Author**         | dev + agent                    |
| **Status**         | approved                       |

## Jira Ticket

- **Ticket Key**: SP0168-3417
- **Ticket URL**: [https://jira.example.com/browse/SP0168-3417](https://jira.example.com/browse/SP0168-3417)
- **Acceptance Criteria**:
  1. AC-1: Tracker tabs render from server config — testable via `tracker-tabs.component.spec.ts`.
  2. AC-2: Active tab persists across reload — testable via manual check + `localStorage` assertion.
  3. AC-3: "Feels fast" — NON-TESTABLE as written → proposed rewrite: "tab switch renders in <200ms on 100-row dataset, measured in Chrome perf trace".

## 1. Problem & Background

Tracker tabs are hardcoded in `src/app/tracker/tracker-tabs.component.ts:12`, so adding a tab needs a release. Ticket SP0168-3417 §Description requires server-driven tabs.

## 2. Goals & Non-Goals

- **Goals**: (G-1) load tab config from API; (G-2) persist active tab. Maps to AC-1, AC-2.
- **Non-Goals**: tab-level permissions (separate ticket SP0168-3418); mobile redesign.

## 3. Current State (as-is)

`TrackerTabsComponent` (`src/app/tracker/tracker-tabs.component.ts:12-60`) holds a static `tabs` array; parent `TrackerComponent` (`src/app/tracker/tracker.component.ts:40`) embeds it directly with no `@Input()`. Baseline: `npm run test -- tracker-tabs` green (4 tests).

## 4. Proposed Design (to-be)

- Container `TrackerComponent` fetches config via `TabConfigService` (`@services/state/tracker/tab-config.service`, new) with `takeUntil(this.destroy$)` + `finalize` loading flag, passes `tabs` down via `@Input()`.
- Presenter `tracker-tabs` keeps rendering only, `OnPush`, exposes `@Input() autoId`, new ids `trackerPage-tabsPanel-<tab>Tab`.
- Reuse `$primary-color` from `scss/helpers/variable`; responsive collapse under 992px per existing grid pattern.

## 5. Options Considered & Rejected

| Option | Why rejected (evidence/source) |
|--------|-------------------------------|
| Standalone component | Not available in Angular 15.2.1 — official Angular v15 docs |
| Store tabs in NgRx global state | Overkill for single-page config; local service + `BehaviorSubject` suffices (`angular-architecture/SKILL.md` §2) |

## 6. Contradictions & Frozen Decisions

| # | Conflict (sources) | Frozen decision + owner | Affects (files/tests) |
|---|--------------------|------------------------|----------------------|
| 1 | Ticket says "persist tab" but no storage named vs Figma note "session only" | `localStorage`, approved by PO (comment 2026-09-10) | `tab-config.service.ts`, spec persistence test |

## 7. Test Plan

- New specs in `tracker-tabs.component.spec.ts`: config render (fail-first red), active-tab persist, empty-config state. Selectors via `[autoId="..."]`.
- Manual: `npm run startdev`, switch tabs, reload, screenshot.

## 8. Validation & Rollout

- [x] `npm run lint` + `npm run format`
- [x] `npm run test` (tracker suite + full, shared-adjacent)
- [x] `npm run build`
- [x] AC trace preview: AC-1 → service spec; AC-2 → persist spec; AC-3 rewritten, measured 120ms
- [x] Rollback: revert single commit; no migration involved

## 9. Risks & Mitigation

| Risk | Likelihood / Impact | Mitigation |
|------|--------------------|------------|
| Config API slow → tabs flash | Medium / Low | Skeleton loader + 5s timeout fallback to last cached config |

## 10. Open Questions

- None (AC-3 rewrite approved 2026-09-11).
