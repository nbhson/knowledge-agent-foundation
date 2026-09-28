# Angular 15 Style Rules & Coding Standards

This document outlines the strict style rules and coding standards for Angular 15 development in this repository.

## 1. Module-Based (NgModule) Architecture

- Every component must be declared in an `NgModule` (`declarations`, and `exports` if reusable). Standalone Components are **NOT used**.
- New feature modules must be registered in the lazy-loaded route configuration: `loadChildren: () => import('./tracker/tracker.module').then((m) => m.TrackerModule)`.
- Import `CommonModule` in modules that use `*ngIf`, `*ngFor`, `*ngSwitch`, or common pipes.

## 2. Component Inputs / Outputs & Reactivity

- Use `@Input()` and `@Output()` decorators with `EventEmitter`. Do NOT use signal-based `input()`/`output()`.
- Manage state with RxJS (`Observable`, `Subject`, `BehaviorSubject`) and NgRx Store/Effects. Do NOT use Angular Signals, `computed()`, or the `resource()` API (not available in Angular 15).
- Remove subscriptions properly with the `takeUntil` (destroyer subject) pattern or the `async` pipe in templates.

## 3. Change Detection & Template Control Flow

- Use standard Zone.js change detection. Use `changeDetection: ChangeDetectionStrategy.OnPush` where inputs are immutable and performance is critical.
- Use `*ngIf`, `*ngFor` (always with a `trackBy` function for collections), and `*ngSwitch`. Do NOT use the modern `@if` / `@for` / `@switch` block control flow.

## 4. Service Imports & Path Aliases

- Import services via path alias `@services/<subfolder>/<service-name>.service` (e.g., `@services/state/custom-view/custom-view.service`).
- **Do NOT** import from the root `@services` barrel file.
- **Do NOT** use relative paths (e.g., `../services/...`) for services.

## 5. File Suffixes

- Components: `*.component.ts` (Class name ends with `Component`)
- Services: `*.service.ts` (Class name ends with `Service`)
- Guards: `*.guard.ts`
- Models: `*.model.ts`
- Constants: `*.constants.ts` or `mock-*.ts`
- Modules: `*.module.ts` (Class name ends with `Module`)