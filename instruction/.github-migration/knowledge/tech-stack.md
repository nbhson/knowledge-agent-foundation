# Tech Stack

Repo-wide technical facts for the Horizon 2 UI Angular 15 app. Facts only —
procedures (patterns, playbooks, review severity) live in skills, e.g.
`skills/libs/shared/angular-architecture/SKILL.md`.

## Angular Version

- **Angular 15.2.1** with classical NgModule architecture — do NOT assume
  Standalone Components.
- New components must be registered in their module's `declarations`
  (and `exports` if reusable).

## Pinned versions (repo standard — cite these, not latest docs)

| Package | Pinned | Notes |
|---|---|---|
| `typescript` | `~4.9` (Angular 15 requires `>=4.8 <5.0`) | Never suggest TS 5.x syntax |
| `node` | `^16 \|\| ^18` (`^14.20` minimum per Angular 15) | `npm run startdev` uses increased memory |
| `rxjs` | `~7.5.x` | `takeUntil`/`finalize`/`pipe(map)` patterns |
| `@ngrx/store` / `effects` | `15.x` (`StoreModule.forRoot`, no `provideStore`) | `provideMockStore` in specs |
| `jest` + `jest-preset-angular` | `28.x` / `12.x` | Angular 15 default is Karma/Jasmine — this repo uses Jest |
| `@angular/material` | `15.x` (MDC-based) | Prefer theme API over private MDC selectors |
| `@azure/msal-angular` + `msal-browser` | `v2.x` | Redirect flow; `canActivate: MAIN_ROLE_GUARDS` |

## Change Detection

- Standard Zone.js change detection.
- `ChangeDetectionStrategy.OnPush` where performance is critical and inputs
  are immutable.

## Reactivity & State Management

- Do NOT use Angular Signals, computed signals, or the `resource()` API
  (unavailable in Angular 15).
- Use RxJS `Observable` / `Subject` / `BehaviorSubject` plus NgRx
  Store/Effects for state management.
- Clean up subscriptions (`takeUntil` destroyer subject or `async` pipe).

## Lazy Loading

- Classic module syntax:
  `loadChildren: () => import('./tracker/tracker.module').then((m) => m.TrackerModule)`.

## Control Flow

- Do NOT use `@if`, `@for`, or `@switch` (unsupported in Angular 15).
- Use `*ngIf`, `*ngFor` (always specify `trackBy` for collections), and
  `*ngSwitch`; import `CommonModule` in modules using them.

## Auth

- `@azure/msal-angular` for authentication.
- Protect routes with the `canActivate: MAIN_ROLE_GUARDS` configuration.

## Commands

| Task | Command |
|---|---|
| Local dev server | `npm run startdev` (`ng serve` with increased memory limit) |
| Format | `npm run format` (Prettier) |
| Lint | `npm run lint` (ESLint with fix option) |
| Unit tests | `npm run test` (Jest) |
| Production build | `npm run build` or `npm run build-prod` |
