---
name: code-review
description: Peer review checklist covering Angular 15, RxJS subscriptions, SCSS imports, restricted imports, security, and performance in the Horizon 2 UI project.
argument-hint: '<PR link or branch range>'
user-invocable: false
---

# Workflow: Code Review

Instructions for reviewing code changes, pull requests, and validating coding conventions in the Horizon 2 UI application.

**Workflow Note**: This is an **analysis-only workflow**. Only Phase 1 (Understand) and Phase 5 (Report) are executed. Phases 2-4 (Planning, Execution, Validation) are skipped entirely — no code changes, no build/test gates, no PR creation.

---

## Entry Criteria

- Diff under review is identified (PR, branch range, or file list); related ticket/design context is loaded in Phase 1.
- Review scope is bounded: touched files plus direct consumers (imports, routes, store slices).
- Rule baseline: [Tech Stack](../../../../knowledge/tech-stack.md) (Angular 15 patterns) and [Project Structure](../../../../knowledge/project-structure.md) (placement/naming) — findings cite these before appealing to general best practice.

## Review Walk Order

Work the diff in passes so correctness is judged before style. Do not start with nits.

- **Pass 1 — Correctness & contracts**: does the change do what the ticket claims; are API/DTO shapes, route/guard behavior, and store transitions right; is there a runtime crash, data-loss, or auth hole. (Checklist §§1–2, 8.)
- **Pass 2 — Tests & evidence**: does each new behavior have a focused test; do mocks live in the owning API folder; is red→green shown for fixes. (Checklist §4 tail, §9 hygiene.)
- **Pass 3 — Conventions & maintainability**: types, bindings budget, line budget, imports, SCSS ownership, `autoId`. (Checklist §§3–7.)

## Review Checklist

1. **Code Organization & Module Structure**:

   - Verify feature-first placement: API/DTO/mock files belong to the matching `src/api/<area>/<feature>/`; feature components and their templates, styles, and specs are grouped by component; models, constants, services, and utilities live in owner-specific folders.
   - Check for duplicate or overlapping NgModules. Consolidate modules only when their components share a feature boundary, lifecycle, and ownership; preserve separate modules for distinct lazy routes, public APIs, or independently owned features.
   - Ensure components are declared/exported by the correct NgModule and feature routes remain lazy-loaded where required.

2. **Architecture & Separation of Concerns**:

   - Verify the feature flow is `API -> service -> component`: API owns transport, backend DTOs, and transport mocks; feature service owns mapping, store/state, query orchestration, and complex business calculations; component consumes state and forwards user actions.
   - Flag components that call API services directly when a feature service owns the flow, or presenters that inject services instead of receiving inputs and emitting outputs.
   - Verify container/presenter boundaries and `OnPush` on stateless presenters with immutable inputs.

3. **Type Safety & Code Reusability**:

   - Reject `any` and anonymous nested DTO object shapes when named item/group/response interfaces or types clarify the contract (e.g. a `modules` array must reuse named DTOs like `RoleDTO`/`RoleModule` in `src/api/admin/roles/roles.dto.ts` — never redeclare the shape inline; see [Angular Architecture §6.2](../../shared/angular-architecture/SKILL.md)).
   - Ensure types, interfaces, and constants are outside component classes and placed with their owner (`dto/`, `models/`, feature interfaces, or `constants/`). Keep backend DTOs distinct from UI models when ownership or contracts differ. Known inline-type violations to cite as precedent: `roles.component.ts:130` (`PeriodicElement`), `documents-info.component.ts:15`, `update.component.ts:377,385`, `contacts.component.ts:26`, `duplicate-check.component.ts:11`.
   - Check for reusable existing constants/utilities before adding duplicates. Centralize reusable TypeScript colors in an owner-local `color.constants.ts` (plural naming; see [Angular Architecture §6.4](../../shared/angular-architecture/SKILL.md)), bind them to CSS variables for SCSS, and do not import app-only constants into reusable libraries.
   - **EMPTY_STRING check**: flag every new `''` literal — app code must use `src/constants/constants.ts:EMPTY_STRING`, library code its own `string.constants.ts`. A brand-new third `EMPTY_STRING` definition is a **Major** (duplicate constant); single literals are **Minor** nits.
   - **Severity**: inline interface/type in touched code → **Major**; `any` → **Major**; missed constant reuse → **Minor** (Major if it duplicates an existing definition file).

4. **Frontend Performance & Maintainability**:

   - Do not call computation methods from template bindings for filtering, normalization, mapping, or styles; use prepared view models or pure pipes. Event handlers and `trackBy` callbacks are allowed. Precedent violations (each a **Major** if newly introduced, or if touched lines keep the pattern): `studies.component.html:16` (`checkAdminRoles()`), `contract-detail.component.html:121` (`canShowDeleteButton()`), `documents.component.html:64` (`getContractStatusClass()`), `limit-items.component.html:18,21`, `general.component.html:24`, `comments.component.html:35`, `studies-tracker-table.component.html:82`, `consent-queue.component.html:413`. Full ban list + fixes: [Angular Architecture §6.5](../../shared/angular-architecture/SKILL.md).
   - **Check procedure**: grep touched `.html` for `(` inside `{{ }}`, `*ngIf`, `[ngClass]`, `[class.*]`, `[style.*]` bindings; every hit must be a property, `async`/pure pipe, handler, or `trackBy`.
   - Keep every `.component.ts` at or below 500 lines. A touched component already over budget must not grow — new logic goes to an extracted presenter/service/pipe. A **new** component created over 500 lines is a **Major**. Split only at a cohesive responsibility boundary (visual block → presenter, orchestration/calculation → service, formatting → pure pipe/util); never split files arbitrarily to dodge the count.
   - **Check procedure**: count lines of every touched/new `.component.ts` (`(Get-Content f).Count` / `wc -l`); report the number in the review.
   - Check loops use `trackBy`, derived state is prepared with RxJS/view models rather than recalculated on every change-detection pass, and new behavior has focused tests.

5. **TypeScript & Angular 15 Rules**:

   - Check that **NO** Angular Signals or `resource()` APIs are used.
   - Enforce RxJS subscription management (always use `takeUntil(this.destroy$)` or the `async` pipe in templates to prevent memory leaks).
   - Enforce standard decorators (`@Input()`, `@Output()`, `@ViewChild()`).
   - Prohibit `@if` / `@for` syntax; ensure `*ngIf` / `*ngFor` (with `trackBy`) are used.
   - **Restricted Service Imports**:
     - Ensure service files are imported via the `@services/*` alias.
     - Prohibit root `@services` imports (use precise paths like `@services/state/custom-view/custom-view.service`).
     - Prohibit relative service imports (like `../services/...` or `./services/...`).
   - **Severity**: Signals/`resource()` or `@if`/`@for` usage → **Blocker** (unsupported runtime syntax for this stack); unclosed subscription on a touched path → **Major**; wrong import form → **Major** (breaks the alias contract); decorator misuse without behavior impact → **Minor**.

6. **Styling & Layout (SCSS)**:

   - Ensure `@import` is used for partial styles (not `@use`).
   - Validate that variables from `scss/helpers/variable` or CSS variables are used rather than hardcoded hex colors or fonts.
   - Prohibit inline CSS styling.
   - Verify layout is responsive on smaller screens.
   - Full token/ownership rules: [Styling Standards](../../shared/styling-standards/SKILL.md).
   - **Severity**: global leakage or unscoped `::ng-deep` → **Major**; new `!important` without Material/Bootstrap specificity justification → **Major**; hardcoded color/typography for a repeated value → **Minor** (Major if it forks an existing token); missing responsive check on a layout change → **Major**.

7. **UI Automation (autoId)**:

   - Verify new/modified templates comply with the `ui-autoid` naming convention (`<pageName>-<contextLevel...>-<elementId>`, camelCase).
   - Ensure every clickable element (button, link, navbar, dropdown, checkbox, radio, pagination) and viewable/assertable element (title, label, message, table header) has an `autoId` when applicable.
   - Confirm `autoId` values are unique within the page, set via `autoId="..."` or `[attr.autoId]="'...'"` (never `[autoId]`), and no accidental renames of stable `autoId` values.
   - Confirm declarative `rum-*` tracking attributes on new interactive/viewable elements are present where user activity matters (see [RUM Skill](../../shared/rum-activity-tracking/SKILL.md)) — flag silently untracked additions as **Minor** (Major if the touched flow is analytics-gated).
   - **Severity**: `autoId` contract break on an element covered by automation (rename/removal) → **Blocker**; missing `autoId` on new interactive/assertable elements → **Major**; `[autoId]` property binding (renders nothing) → **Major**; naming-style deviation without breakage → **Minor**.

8. **Security & Secrets**:

   - Confirm no passwords, client secrets, API tokens, or credentials are hardcoded.
   - Check route protection: touched routes keep the `canActivate: MAIN_ROLE_GUARDS` configuration; no guarded route is exposed without it.
   - Check DOM-safety: no `innerHTML` with untrusted content and no `bypassSecurityTrust*` without a recorded justification and sanitization boundary.
   - Check logging/telemetry: no PII, tokens, or secrets in console logs, toast text, or tracking labels.
   - **Severity**: hardcoded secret/credential, auth bypass, or unsanitized `innerHTML` with untrusted input → **Blocker**; missing guard on a touched route or PII in logs/labels → **Major**.

9. **Performance & Cleanliness**:

   - Ensure feature modules are lazy loaded in `app-routing.module.ts` via `loadChildren`.
   - Check for and clean up unused imports, variables, console logs, or commented out blocks of code.
   - Confirm that types are explicit (avoid `any`) and formatting/linting expectations are met.
   - **Severity**: eager loading where lazy loading is required, or `any` in touched code → **Major**; dead code, stray logs, formatting drift → **Minor**.

---

## Finding Template

Write every finding in this shape so authors can act without a follow-up round:

```text
[file:line] [Severity] Observed vs expected
Fix: <concrete change>
Source: <repo file:line | ticket AC | versioned doc URL>
```

- One finding per issue; group repeated instances of the same violation with all `file:line` hits listed.
- Quote the offending code (≤10 lines) when the location alone is ambiguous.
- Never file a bare opinion — a finding without a source goes back as a question, not a verdict driver.

## Approval Bar

- **Approve** means: no Blockers, no unresolved Majors (deferred Majors carry owner + ticket), P4-lite recorded, and the diff is limited to its stated scope.
- **Request changes** on any Blocker, any Major that affects behavior/contracts/tests/automation, or an incomplete P4-lite.
- **Comment** for Minor-only reviews or advisory notes the author may defer.

---

## P4-Lite Verification (embedded in Phase 5 — analysis-only, no code edits)

Even though Phases 2–4 are skipped, every review must record:

- **Severity scale with boundaries**:
  - **Blocker** (must fix before merge; verdict → `Request changes`): breaks build/tests, runtime crash on the touched path, data loss or wrong data written, auth bypass or secret leak, missing migration for a breaking contract change, `autoId` contract break on an element covered by automation. Example: injecting `HttpClient` without importing `HttpClientTestingModule`/`HttpClientModule` — component fails at runtime with a NullInjector error.
  - **Major** (should fix before merge; verdict → `Request changes` unless explicitly deferred with owner): memory leak (unclosed subscription without `takeUntil`/`async`), wrong RxJS data flow (manual recalculation instead of `pipe(map)` causing stale UI), hardcoded secret-adjacent config, non-responsive layout on the target breakpoint, missing unit test for new behavior, scope creep unrelated to the ticket.
  - **Minor** (nit; verdict → `Approve` or `Comment`): unused import/variable, formatting drift, comment typo, naming that deviates from convention without breaking automation, redundant dead code (e.g., an empty `ngOnInit` left after logic was moved to a resolver).
  - Mixed findings: verdict is the highest severity present; list Blockers first with `file:line` + fix proposal + authoritative source (repo code, ticket AC, or official doc URL).
- **Diff hygiene**: `git diff --check` result (PASS/FAIL + output).
- **Build/test**: executed or explicitly skipped with reason (e.g., "docs-only, no build impact" or "not run — limited to manifest change"). Never claim green without evidence.
- **Verdict**: one of `Approve` / `Request changes` / `Comment` with blocking items listed first.

## Review Deliverables & Summary

When preparing the review or the Pull Request, summarize:
- **Walk summary**: passes completed (correctness → tests → conventions) and files covered.
- **Findings**: numbered list in Finding Template shape, Blockers first.
- **Risks & Impact**: Potential side-effects on other modules or layout rendering.
- **Required Follow-ups**: Any post-merge actions or technical debt items identified (each with owner + ticket where deferred).
- **Validation Evidence**: Build/test outputs if executed, or an explicit skip reason per P4-lite above. Never claim green without evidence.

## Filing the Review (Phase 5)

File the review through the [Report Generation Skill](../../shared/report-generation/SKILL.md) (canonical table §1: `pr-description.md` template → `code-review/CODE-REVIEW-[PR-ID]-[DATE]-[TIME].ctx.md`, stable content-hash + `REPORTS.md` row).

---

## Review Operating Rules (enterprise)

- **Finding format**: every finding carries `file:line` + severity + observed vs expected + concrete fix proposal + authoritative source (repo code, ticket AC, or versioned doc). No bare opinions.
- **No drive-by scope**: findings outside the diff go to follow-up tickets, except Blockers (build break, crash, data loss, auth/secret issues).
- **Contradiction handling**: conflicting ticket vs design vs code goes to the contradiction list with an owner — never silently pick one side.
- **Verdict discipline**: verdict is the highest severity present (`Approve` / `Comment` / `Request changes`); Blockers and Major findings block merge unless explicitly deferred with owner + ticket.
