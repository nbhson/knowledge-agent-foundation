# Knowledge: Frontend Architecture

We use **Angular 15.2.1** with classic **Module-Based (NgModule)** architecture. Modern Angular features (Standalone Components, Signals, `resource()`, `@if`/`@for`) are **NOT available** in this codebase.

- **Core Framework**: Angular 15.2.1, Zone.js change detection.
- **Module-Based Architecture**:
  - Components must be declared in an `NgModule` (typically `SharedModule` or feature modules like `EmbeddedModule`, `TrackerModule`, `AdminModule`).
  - To add a new component, also register it in its corresponding module's `declarations` and `exports` arrays (if reusable).
- **State Management & Reactivity**:
  - Do NOT use Angular Signals, computed signals, or the `resource()` API.
  - Use RxJS `Observable`, `Subject`, `BehaviorSubject`, and standard NgRx Store/Effects for state management.
  - Clean up subscriptions (using the `takeUntil` pattern with a destroyer subject or the `async` pipe in templates) to prevent memory leaks.
- **Component Inputs/Outputs**:
  - Use `@Input()` / `@Output()` decorators with `EventEmitter` (NOT signal-based inputs/outputs).
- **Control Flow**:
  - Do NOT use `@if`, `@for`, or `@switch`.
  - Use `*ngIf`, `*ngFor` (always specify `trackBy` for collections), and `*ngSwitch` directives instead. Ensure `CommonModule` is imported in modules using these directives.
- **Change Detection**:
  - Standard Zone.js change detection.
  - Implement `changeDetection: ChangeDetectionStrategy.OnPush` where performance is critical and inputs are immutable.
- **Lazy Loading**:
  - Lazy-load routes using classic module loading: `loadChildren: () => import('./tracker/tracker.module').then((m) => m.TrackerModule)`.
- **Styling**: Classic Dart Sass `@import` modular styles, design system variables (`src/scss/helpers/...`), Bootstrap/Material utility classes.
- **Testing**: Jest (`npm run test`).
- **Formatting**: Prettier (`npm run format`).
- **Linting**: ESLint (`npm run lint`).

---

## Architectural Pattern & Directory Structure

### 1. Component Decomposition
We separate responsibilities cleanly using container and presenter components:

- **Container/Orchestrator Components** (Parent):
  - Responsible for fetching data (via RxJS services + `async` pipe), managing routing, submission handlers, and route guards (`canActivate: MAIN_ROLE_GUARDS`, `canDeactivate`).
- **Stateless Presenter Components** (Children):
  - Located under the feature module's `components/` subfolder.
  - Accept inputs via `@Input()` and emit actions via `@Output()` + `EventEmitter`.
  - Purely presentational and state-free.
- Every component must be registered in its parent `NgModule` `declarations` (and `exports` if reusable).

### 2. Symmetrical Refactoring
Maintain strict symmetry between similar domains — parallel folder structures, module patterns, and route guard patterns.

### 3. Core Assets Organization
- **Shared Components**: `src/shared/` (global components, decorators, directives, DTOs, guards, material configurations, pipes).
- **Global Constants**: `src/constants/` (`constants.ts`, `enum.ts`, `messages.ts`, etc.).
- **Models**: `src/models/` (global interface types, e.g., `table.model.ts`).
- **Global Styles**: `src/scss/` split into `base/`, `components/`, `helpers/`, `pages/`.
- **Path Aliases**: Use `@services/*` for services (mapped to `src/app/services/*`). Do NOT import from the root `@services` barrel — always use specific category subfolders (e.g., `@services/state/custom-view/custom-view.service`). Do NOT use relative paths (like `../services/...`) for services.
