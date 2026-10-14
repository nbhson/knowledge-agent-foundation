---
name: angular-architecture
description: 'Angular 15 architecture (container/presenter, RxJS, API-service-component) plus checkable repo conventions (§6): domain ownership, type extraction, EMPTY_STRING, color.constants.ts, template-binding ban, 500-line budget.'
user-invocable: false
---

# Angular Architecture & Component Blueprint

This skill guides on how to structure, decompose, and manage Angular components and data flows in this repository.

## How to Use This Skill (enterprise)

- **When**: every feature/refactor/review task that touches components, services, modules, DTOs, or templates.
- **How**: apply §1–§5 as design guidance, then run the §6 checklists as gates before finishing (placement, types, literals, bindings, line budget).
- **Non-goals**: this skill does not cover styling tokens (see `styling-standards`), automation selectors (see `ui-autoid`), or workflow phasing (see `phases/README.md`).
- **Evidence**: cite `file:line` for every architectural claim; mark anything not read as `proposed — needs developer confirmation`.

---

## 1. Container vs. Presentation Component Blueprint

To avoid bloated templates and hard-to-maintain files, decompose components when they grow large or handle complex layouts:

### A. Parent (Container / Orchestrator)

- **Role**: Fetch data, integrate with NgRx store, inject services, manage routing, coordinate submissions, handle dialog boxes, and hold states.
- **Example Template**:
  ```html
  <div class="tracker-main-container">
    <app-tracker-overview-table [data]="trackerData" (rowClicked)="onRowSelect($event)"></app-tracker-overview-table>
    <app-pagination [total]="totalCount" (pageChange)="onPageChange($event)"></app-pagination>
  </div>
  ```

### B. Children (Presenters / Stateless components)

- **Folder Location**: Nested inside a `components/` subdirectory under the parent component directory or inside `src/shared/components/`.
- **Role**: Strictly render UI.
- **Rules**:
  - Accept state via classic `@Input()` decorators.
  - Emit actions via `@Output() outputEvent = new EventEmitter<T>()`.
  - Do NOT inject services directly inside presenters. Let the parent component handle operations.
  - Always implement `changeDetection: ChangeDetectionStrategy.OnPush`.
  - Expose an optional `@Input() autoId?: string` and bind `[attr.autoId]="autoId"` inside the template so callers can pass page-specific IDs (see [UI AutoId Skill](../ui-autoid/SKILL.md)).

---

## 2. Reactivity & Async Data Blueprint

Do NOT use Angular Signals or `resource()`. Always write data loading and reactivity using RxJS Observables and classical Angular patterns:

- **Fetching Data**:

  ```typescript
  // In Service:
  getData(params: PaginationParams): Observable<PaginationResultModel<DataDTO>> {
    return this.apiService.get(params);
  }

  // In Component:
  loadData() {
    this.isLoading = true;
    this.dataService.getData(this.params)
      .pipe(
        takeUntil(this.destroy$),
        finalize(() => this.isLoading = false)
      )
      .subscribe({
        next: (res) => this.items = res.content,
        error: (err) => this.toastr.error('Failed to load data')
      });
  }
  ```

- **Derived State**: Use RxJS `.pipe(map(...))` rather than manual recalculation inside templates to ensure efficiency and clean derived data.

---

## 3. Template Code Blueprint

Use classical Angular 15 template directives:

- Always use `*ngIf`, `*ngFor`, and `*ngSwitch` (imported via `CommonModule` or `SharedModule`).
- Always specify `trackBy` for loops to prevent redundant DOM re-rendering:

  ```html
  <div *ngIf="!isLoading; else loadingTpl">
    <div *ngFor="let item of items; trackBy: trackById" class="item-card">
      <h4>{{ item.title }}</h4>
    </div>
  </div>
  <ng-template #loadingTpl>
    <div class="shimmer-loader">Loading...</div>
  </ng-template>
  ```

- Do not call computation methods from template bindings. Prepare derived
  values in the service/view model or use a pure pipe; event handlers and
  `trackBy` callbacks are allowed.

---

## 4. Feature API-Service-Component Flow

Use the feature service as the boundary between transport contracts and the
view:

1. **API service**: Own HTTP requests, backend DTOs, and transport-specific
   mock behavior. It must not import fixtures or models from `src/app/`.
2. **Feature service**: Own DTO-to-view-model mapping, query orchestration,
   loading/error state, store access, and complex feature calculations. Use
   RxJS and the repository's existing state pattern; do not add NgRx for a
   feature-local stream without an established need.
3. **Component**: Consume service state, render it, and forward user actions.
   Do not inject the feature API directly into a component when a service owns
   the flow.

Keep component files together under the feature's `components/` directory and
put types/constants in owner-specific `models/`, `dto/`, and `constants/`
modules. Follow the 500-line component ceiling in §6.6 below. The full
canonical layout (all 12 feature-private folders + the feature-private vs
app-wide placement table) is the single source of truth in
`knowledge/project-structure.md` (§Standard Feature Module Layout,
§Feature-Private vs App-Wide Placement) — this skill only adds the
checkable gates below.

- **Feature-private by default**: `components/`, `directives/`, `pipes/`,
  `services/`, `models/`, `constants/`, `enums/`, `validators/`, `guards/`,
  `interceptors/`, `utils/`, `store/` under `src/app/<area>/<feature>/`
  are importable ONLY by that feature's own module/service/components.
- **App-wide on second use**: reused by 2+ features/areas → promote to
  `src/shared/` (components, directives, pipes, guards), `src/constants/`
  (constants incl. `EMPTY_STRING`, enums), `src/models/` (shared types),
  `src/scss/` (shared styles), `src/app/services|util|validators/`
  (shared services/utils/validators). Never deep-import a sibling feature
  (`../sibling-feature/...`).
- **API exception**: a feature module NEVER has a local `api/` folder —
  `*.api.ts` + `*.dto.ts` live only in `src/api/<area>/<feature>/` (§6.1).

---

## 5. NgModule Ownership and Consolidation

- Let the feature module own components, directives, and pipes used only by
  that feature. Export only declarations consumed by another module.
- Consolidate fragmented or duplicate modules when their declarations share
  the same feature boundary, lifecycle, and ownership. Keep distinct modules
  for separate lazy routes, public integration points, or independently owned
  features; do not replace them with a monolithic tracker module.
- Before consolidation, verify route loading, provider scope, and every
  declaration/import/export consumer. Avoid duplicate declarations or changing
  provider lifetime as a side effect.

---

## 6. Repo-Specific Conventions (Checkable — With Real Exemplars)

The rules above are abstract; Copilot kept missing them in review. The
subsections below are **checkable procedures with real file paths**. Apply them
on every feature/refactor/review task — they encode repeated review findings.

### 6.1 Feature-domain ownership: check the neighbor folder first

New files must land in the domain that owns the feature, not the folder that
happens to exist nearby.

- **Procedure**: before creating `src/api/<area>/<feature>/...`, list
  `src/api/<area>/` for a sibling domain folder. If one owns the concept
  (DTOs, mocks, data-source already there), put the new files there.
- **Real case**: `src/api/tracker/consents/` is correctly grouped per
  sub-feature (`consent-queue/`, `consent-request-detail/`,
  `consent-request-process/`, `consent-review-detail/`, `icf-assignments/` —
  each with its own `*.api.ts` + `*.dto.ts`). Apply the same per-sub-feature
  split to any `tracker/<area>/` domain before it grows past the grouping
  threshold below.
- **Grouping threshold**: a flat folder with >8 files of mixed kinds
  (dto/model/mock/spec/api) must be grouped into per-component or
  per-responsibility subfolders — see §6.6 exemplar.

### 6.2 Type extraction: split anonymous shapes to the smallest named units

Never declare an anonymous nested object shape in a component when a named
interface clarifies the contract. Split groups AND items.

```typescript
// ❌ BANNED — anonymous nested shape inside a component
modules: Array<{
  modulePk: number;
  module: string;
  permissions: Array<string>;
}> = [];

// ✅ REQUIRED — import the owner DTOs (real pattern already used in
// src/api/admin/roles/roles.dto.ts)
export interface RoleModule {
  modulePk: number;
  module: string;
  permissions: Array<string>;
  description: string;
  childModules: Array<RoleModule> | null;
}
export interface RoleDTO {
  pk: number;
  id: string;
  name: string;
  modules: Array<RoleModule>;
}
// component:
modules: Array<RoleModule> = [];
```

- **Procedure**: on every new property with an object-literal type, search
  `dto/` + `models/` for an existing interface first; only create a new file
  when none fits, placed beside its owner (backend DTO → feature `dto/`,
  view shape → `models/`).
- Backend DTOs stay distinct from UI/view models when ownership or contract
  differs — map between them in the feature service (§4), never in the
  component or template.

### 6.3 `EMPTY_STRING`: never inline `''`

- **Canonical locations**:
  - App code: `src/constants/constants.ts` (`export const EMPTY_STRING = '';`)
  - Reusable library code (`projects/*`): the library's own constants module
    (e.g. `string.constants.ts`) — never the app's `src/constants/`. A
    library must NOT import app-only constants — package boundary
    (`API -> service -> component` §4; reusable packages stay independent of
    `src/app/`).
- **Procedure**: `private _activeContextKey = '';` → 
  `private _activeContextKey = EMPTY_STRING;` with the correct import for the
  layer. Applies to initializers, comparisons (`=== EMPTY_STRING`), and
  fallbacks (`?? EMPTY_STRING`).
- Review severity: **Minor** (nit) per occurrence, **Major** if a new file
  introduces its own third `EMPTY_STRING` definition instead of reusing one.

### 6.4 `color.constants.ts`: one owner-local palette per consumer

- **Pattern** (`*.constants.ts`, plural — the singular
  `graph-color.constant.ts` under forecast-graph is legacy naming, do not copy):
  ```typescript
  // <feature>/constants/color.constants.ts (target shape)
  export const <FEATURE>_COLORS = {
    primary: '#128474',
    background: '#ffffff',
    // ... any grouped palette the feature needs
  } as const;
  ```
- **Rules**:
  - No hardcoded hex in `.ts` (violations on record:
    `contract-graph.service.ts` `borderColor: '#ccc'`,
    `contracts-oversight-data-source.ts` `fill: '#128474'`,
    `sponsor-graph.service.ts` HTML-string `backgroundColor:#1790D0`).
    Move each literal into the owning feature's `color.constants.ts`.
  - Bind palette values to CSS custom properties for SCSS consumption; do not
    duplicate the same palette as TS literals and stylesheet defaults.
  - App features get their own feature-owned file — reusable libraries under
    `projects/*` must not import app-only constants across the library
    boundary, and app features must not import a library's constants either.

### 6.5 Template bindings: properties and pure pipes only

Angular 15 uses default change detection here — every method call in a binding
re-runs on **every** CD pass. Ban list with real violations found in repo:

| ❌ Found in repo | ✅ Fix |
|---|---|
| `studies.component.html:16` `*ngIf="checkAdminRoles(); else notAdmin"` | `isAdmin$ \| async` prepared in service/component init |
| `contract-detail.component.html:121` `*ngIf="canShowDeleteButton()"` | `canShowDelete$` / boolean set on state change |
| `documents.component.html:64` `[ngClass]="getContractStatusClass(...)"` | pure pipe `status \| contractStatusClass` or precomputed map |
| `limit-items.component.html:18` `[ngClass]="getItemClass(item, index)"` + `{{ getValue(item) }}` | precomputed view-model fields (`item.cssClass`, `item.displayValue`) |
| `general.component.html:24` `{{ displayValue(...) }}` | pure pipe or mapped view model |
| `comments.component.html:35` `{{ generateDateMessage(...) }}` | pure pipe |
| `consent-queue.component.html:413` `[ngClass]="getRowClass(row)"` | `row.rowClass` from the service-mapped view model |

- **Allowed in bindings**: property reads, `async` pipe, pure pipes, event
  handlers (`(click)="onSave($event)"`), `trackBy` callbacks.
- **Procedure**: before finishing any template change, grep the touched
  `.html` for `(` inside `{{ }}` / `*ngIf` / `[ng...]` bindings; each hit is a
  **Major** review finding until converted.

### 6.6 Component-file grouping exemplar + 500-line budget

Target layout — canonical source is
`knowledge/project-structure.md` (§Standard Feature Module Layout):
only the module + routing at root, everything else grouped by kind,
`api/` NEVER local (lives in `src/api/<area>/<feature>/`):

```
<feature>/
├── <feature>-routing.module.ts
├── <feature>.module.ts                # ONLY module + routing at root
├── components/<name>/<name>.component.{ts,html,scss,spec.ts}
├── directives/*.directive.ts
├── pipes/*.pipe.ts
├── services/*.service.ts (+ *.spec.ts)
├── models/*.model.ts
├── constants/*.constants.ts
├── enums/*.enum.ts
├── validators/*.validator.ts
├── guards/*.guard.ts
├── interceptors/*.interceptor.ts
├── utils/*.util.ts (+ *.spec.ts beside the util)
└── store/                             # only when NgRx is needed
```

- New components follow this from the first commit — never land 4+ loose
  files flat in a feature root.
- New `.component.ts` has a **500-line budget**: over it at creation time,
  split at a cohesive boundary first (presenter for a visual block, service
  for orchestration/calculation, pure pipe/util for formatting). Existing
  violators (e.g. `sites.component.ts` ~1566, `studies.component.ts` ~1265 —
  measured 2026-10) are tracked refactor debt, not permission to add more.

---

## 7. Layer Dependency Rules (allowed import directions)

```
src/api/<area>/...  ──transport, DTOs, transport mocks──▶  feature service
feature service     ──mapped view-models, state──────────▶  component
src/shared/...      ──reusable primitives────────────────▶  features
src/constants/...   ──app-wide literals (incl. EMPTY_STRING)─▶  app code
src/models/...      ──shared types───────────────────────▶  app code
src/scss/...        ──shared tokens/styles───────────────▶  app styles
library (projects/*) ──self-contained────────────────────▶  (imports nothing from src/app/)
```

- **Allowed**: service → API (`@services/*` precise alias); component → feature service; anyone → owner `dto/`/`models/`; app code → `src/constants/`.
- **Banned**: component → API directly when a feature service owns the flow (§4); presenter → any service (§1B); app constants → reusable library (and vice versa); feature → sibling feature internals (share via `src/shared/` or an explicit contract, never deep imports).
- **Procedure**: on every new import, read the direction off the diagram above. A reversed arrow is a **Major** review finding (Blocker if it crosses the library/app boundary).

## 8. State & Module Decision Tables

**Local service state vs NgRx** (decide once per feature, record in the plan):

| Signal | Choice |
|---|---|
| State lives in one route, dies on navigate-away | Feature service with `BehaviorSubject`/observables |
| State shared across routes/features, needs time-travel/history or multi-consumer sync | NgRx Store/Effects (existing pattern — do not introduce a second store) |
| Unsure | Start with the service; promote to NgRx only with an established multi-consumer need (§4) |

**New module vs existing module**:

| Signal | Choice |
|---|---|
| Separate lazy route, public integration point, or independently owned feature | New module (own declarations, own route entry) |
| Same feature boundary, lifecycle, and ownership as an existing module | Extend the existing module; consolidate duplicates per §5 |
| Unsure | Keep separate — merging is cheap later, splitting a merged module under load is not |
