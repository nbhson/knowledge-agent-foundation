---
name: 'Angular 15 patterns'
description: 'Use when creating or editing Angular 15 TypeScript/HTML files (NgModule, RxJS, templates).'
applyTo: '**/*.{ts,html}'
---

# Angular 15 (repo-pinned: 15.2.1)

- Classical **NgModule** architecture — do NOT assume standalone components. Register new components in module `declarations` (and `exports` if reusable).
- No **Signals / computed / `resource()`**. Reactivity = RxJS `Observable`/`Subject`/`BehaviorSubject` + NgRx Store/Effects; clean up with `takeUntil(destroy$)` or `async` pipe.
- Templates: `*ngIf` / `*ngFor` (always `trackBy`) / `*ngSwitch` via `CommonModule`. Never `@if` / `@for` / `@switch`.
- Lazy routes: `loadChildren: () => import('./x/x.module').then((m) => m.XModule)`.
- Data flow `API -> service -> component`; services via `@services/<category>/<name>` alias (never root `@services` barrel, never relative `../services/`).
- Templates: no computation calls in bindings (filtering/mapping/sort/styles) — precompute in the service or use a pure pipe; event handlers and `trackBy` callbacks are the only calls allowed.
- New interactive/viewable elements get `autoId` per `.github/skills/libs/shared/ui-autoid/SKILL.md` and keep declarative `rum-*` attributes where user activity matters (see `.github/skills/libs/shared/rum-activity-tracking/SKILL.md`).
- Details: `.github/knowledge/tech-stack.md`, `.github/knowledge/project-structure.md`, `.github/skills/libs/shared/angular-architecture/SKILL.md`.
