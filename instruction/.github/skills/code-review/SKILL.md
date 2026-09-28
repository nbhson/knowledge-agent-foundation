---
name: code-review
description: Peer review checklist covering Angular 15, RxJS subscriptions, SCSS imports, restricted imports, security, and performance in the Horizon 2 UI project.
---

# Workflow: Code Review

Instructions for reviewing code changes, pull requests, and validating coding conventions in the Horizon 2 UI application.

**Workflow Note**: This is an **analysis-only workflow**. Only Phase 1 (Understand) and Phase 5 (Report) are executed. Phases 2-4 (Planning, Execution, Validation) are skipped entirely — no code changes, no build/test gates, no PR creation.

---

## Review Checklist

1. **Architecture & Structure**:
   - Ensure components are module-based and correctly registered in their NgModules (not standalone components).
   - Verify container vs. presenter architecture (container handles services/state; presenter accepts `@Input()`, emits `@Output()`, and implements `changeDetection: ChangeDetectionStrategy.OnPush`).

2. **TypeScript & Angular 15 Rules**:
   - Check that **NO** Angular Signals or `resource()` APIs are used.
   - Enforce RxJS subscription management (always use `takeUntil(this.destroy$)` or the `async` pipe in templates to prevent memory leaks).
   - Enforce standard decorators (`@Input()`, `@Output()`, `@ViewChild()`).
   - Prohibit `@if` / `@for` syntax; ensure `*ngIf` / `*ngFor` (with `trackBy`) are used.
   - **Restricted Service Imports**:
     - Ensure service files are imported via the `@services/*` alias.
     - Prohibit root `@services` imports (use precise paths like `@services/state/custom-view/custom-view.service`).
     - Prohibit relative service imports (like `../services/...` or `./services/...`).

3. **Styling & Layout (SCSS)**:
   - Ensure `@import` is used for partial styles (not `@use`).
   - Validate that variables from `scss/helpers/variable` or CSS variables are used rather than hardcoded hex colors or fonts.
   - Prohibit inline CSS styling.
   - Verify layout is responsive on smaller screens.

4. **UI Automation (autoId)**:
   - Verify new/modified templates comply with the `ui-autoid` naming convention (`<pageName>-<contextLevel...>-<elementId>`, camelCase).
   - Ensure every clickable element (button, link, navbar, dropdown, checkbox, radio, pagination) and viewable/assertable element (title, label, message, table header) has an `autoId` when applicable.
   - Confirm `autoId` values are unique within the page, set via `autoId="..."` or `[attr.autoId]="'...'"` (never `[autoId]`), and no accidental renames of stable `autoId` values.

5. **Security & Secrets**:
   - Confirm no passwords, client secrets, API tokens, or credentials are hardcoded.

6. **Performance & Cleanliness**:
   - Ensure feature modules are lazy loaded in `app-routing.module.ts` via `loadChildren`.
   - Check for and clean up unused imports, variables, console logs, or commented out blocks of code.
   - Confirm that types are explicit (avoid `any`) and formatting/linting expectations are met.

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
- **Risks & Impact**: Potential side-effects on other modules or layout rendering.
- **Required Follow-ups**: Any post-merge actions or technical debt items identified.
- **Validation Evidence**: Build/test outputs if executed, or an explicit skip reason per P4-lite above. Never claim green without evidence.
