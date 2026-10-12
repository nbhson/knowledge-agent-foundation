---
name: unit-test
description: Dedicated workflow for planning Jest test cases, mocking Angular 15 dependencies, and executing/validating tests in the Horizon 2 UI project.
argument-hint: '<target file.ts> <behaviors>'
user-invocable: false
---

# Workflow: Unit Test

This document outlines the systematic flow for writing, updating, and executing unit tests in the Horizon 2 UI application.

---

## Entry Criteria

- Target source file (`*.ts`) and the behaviors to verify are identified; the existing spec (if any) is read first.
- Dependencies to mock (HTTP, services, routes, NgRx store) are listed before writing tests.
- For bug fixes: the failing behavior is reproduced as a test FIRST (red) before the fix.

## Required Steps & Phases

1. **Understanding & Scope (Phase 1)**:
   - Identify the source file (`*.ts`) that needs test coverage and identify the behavior to verify at the lowest relevant level of the stack. Placement and patterns follow [Tech Stack](../../knowledge/tech-stack.md) and [Project Structure](../../knowledge/project-structure.md).
   - Locate its corresponding spec file (`*.spec.ts`). If the spec file does not exist, create a new one next to the source file.
   - Analyze the target code's dependencies (e.g., HTTP clients, custom services, activated routes, or NgRx Store) to determine what must be mocked.

2. **Test Strategy — what to test, per layer (Phase 2)**:
   - **Component**: renders with given inputs; emits outputs on user action (drive via `autoId` selectors, not internal methods); shows loading/error/empty states; dispatches the right service/store calls. Do NOT assert private fields or internal call order.
   - **Feature service**: DTO→view-model mapping; query orchestration (params in → observable out); loading/error state transitions; store interactions. Mock the API layer, test the mapping for real.
   - **Pure pipe / util**: input→output table, including null/undefined/empty and boundary values. These are the cheapest high-value tests — write them first.
   - **NgRx (reducer/selector/effect)**: reducer = state + action → state (pure table); selector = state → derived value; effect = action → (mocked service) → expected follow-up actions. Mock services, never the store itself except via `provideMockStore` in component specs.
   - **Do not test**: framework behavior (routing renders, Material internals), third-party libraries, or exact CSS/text copy.

3. **Planning & Mocking (Phase 2)**:
   - Apply the Phase 2 threshold table (`.github/phases/phase-2-planning.md`): non-trivial campaigns (new harness, shared mocks, multi-module coverage) need an approved plan listing scenarios + mocks before writing specs.
   - Plan the testing scenarios, covering:
     - **Happy paths**: Successful responses, standard renders, expected UI actions.
     - **Edge cases**: Empty lists, null or undefined inputs, extreme pagination values.
     - **Error flows**: HTTP error handling, failed actions, toast reminders.
   - **Mock decision table**:

     | Dependency | Mock with | Notes |
     |---|---|---|
     | HTTP (`HttpClient`) | `HttpClientTestingModule` + `HttpTestingController` | Assert URL/method; flush success AND error cases |
     | Feature/custom service | `jest.spyOn` or `useValue` stub | Stub at the public-method boundary, keep return shapes realistic |
     | `ActivatedRoute` | `useValue` with `paramMap`/`queryParamMap` observables | Cover param-present and param-absent |
     | NgRx Store (component spec) | `provideMockStore({ initialState })` + `overrideSelector` | Set selectors per test; verify dispatched actions where behavior depends on them |
     | `Router` / `MatDialog` / `Toastr` | Lightweight spy objects | Assert navigation/dialog/message triggers, not their internals |
     | Time (`setTimeout`, `debounceTime`) | `fakeAsync` + `tick` | Never real waiting; never wall-clock assertions |

   - **Assertion Strategy**: Prefer real component/service behavior over mock-only assertions where possible. Keep Angular 15 and RxJS patterns consistent with the existing test setup.
   - **Element Selection**: Use `autoId` as the primary selector (`fixture.nativeElement.querySelector('[autoId="..."]')`) instead of fragile CSS/text selectors. Follow the [UI AutoId Skill](../ui-autoid/SKILL.md) for naming conventions.
     - Determine setup dependencies, importing test modules such as `HttpClientTestingModule` or using `jest.spyOn` as appropriate.
     - Place HTTP/transport mocks in the owning API folder as `*.mock.ts` (never inside the spec or the component), per the owner-folder rule in [Angular Architecture §6](../angular-architecture/SKILL.md). Pure utilities get their own `*.util.spec.ts` beside the util.

4. **Execution — fail-first (Phase 3)**:
   - Write the new test FIRST and confirm it fails for the right reason (red — wrong assertion message means a bad test, fix the test).
   - Then implement/fix and confirm it passes (green).
   - Write the tests inside the `*.spec.ts` using `TestBed.configureTestingModule`.
   - Setup mocks for services and state providers (like `provideMockStore` for NgRx store mocks).
   - Use standard Angular test practices:
     ```typescript
     fixture = TestBed.createComponent(MyComponent);
     component = fixture.componentInstance;
     fixture.detectChanges();
     ```
   - **Async discipline**: `fakeAsync`+`tick` for timers/debounce; `fixture.whenStable()` (or `await`) for resolved observables before asserting DOM; flush microtasks before asserting toast/dialog side effects. A test that passes only with real delays is a bad test — rewrite it.
   - **Structure**: group with nested `describe` per behavior (`describe('when list is empty', …)`), name tests `should <expected> when <condition>`.

5. **Formatting & Quality (Phase 3)**:
   - Follow the [Post Code Change Skill](../post-code-change/SKILL.md) for canonical formatting, linting, and formatting checks.

6. **Validation (Phase 4)**:
   - Confirm the Phase 4 validation gate (`.github/phases/phase-4-validation-pr.md`): build OK, tests OK, and every covered AC/behavior traced to its spec.
   - Run the relevant Jest suite and capture the result:
     ```bash
     npm run test
     ```
   - Ensure the tests execute cleanly without memory leaks or uncaught async processes.
   - Re-run the touched spec in isolation AND the neighboring suites (same service/store/component family); a green isolated run with red neighbors is still a failure.

7. **Report (Phase 5)**:
   - File a Phase 5 report using the [Report Generation Skill](../report-generation/SKILL.md) (correct template + stable content-hash + `REPORTS.md` row). Record red→green evidence and the suites re-run.

---

## Test Quality Bar (enterprise)

- **Isolation**: no shared mutable state between tests; each test sets up its own fixtures/mocks (`beforeEach` rebuilds, never leaks).
- **Determinism**: no wall-clock, random, or ordering dependence; async fully flushed. Flaky tests are bugs — quarantine with a ticket, never `skip` silently.
- **Naming**: `should <expected behavior> when <condition>` so failures read as specifications.
- **Fail-first proof**: new regression tests are shown red before the fix and green after (record both runs in the report).
- **Selectors**: `autoId` first; CSS-text selectors only when no interactive/viewable contract exists.

## Exit Criteria

- Full relevant suite green with no new warnings; flaky retries documented (rerun once isolated before counting).
- New/changed behaviors each have at least: one happy path, one edge case (empty/null/extreme), one error flow.
- No test-logic loosening to force green (assertion changes vs the pre-change spec must be justified in the report).
