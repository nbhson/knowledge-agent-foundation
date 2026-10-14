# Project Structure

Repo-wide placement and naming facts. Facts only — grouping thresholds, split
playbooks, and review severity live in skills (e.g. `skills/libs/shared/angular-architecture/SKILL.md` §6).

## File Suffixes

| Kind | Class name suffix | File suffix |
|---|---|---|
| Component | `Component` | `.component.ts` (e.g. `home-page.component.ts`) |
| Service | `Service` | `.service.ts` (e.g. `custom-view.service.ts`) |
| Module | `Module` | `.module.ts` (e.g. `shared-module.module.ts`) |

## Shared Folders (`src/`)

App-wide reusable code lives here. Anything used by 2+ features (or 2+
areas) must be promoted here — never deep-imported from a sibling feature.

- `src/api/` — transport layer, grouped by area then feature
  (e.g. `src/api/tracker/consents/consent-queue/*.api.ts + *.dto.ts`).
  Owns HTTP calls, endpoint definitions, backend DTOs, transport mocks.
  A feature module NEVER has its own local `api/` folder.
- `src/app/` — feature modules, grouped by area then feature
  (e.g. `src/app/admin/users/`, `src/app/tracker/sites/`). Each feature
  follows the Standard Feature Module Layout below.
- `src/shared/` — global components, decorators, directives (`directive/`),
  DTOs (`dto/`), guards (`guard/`), material configurations (`material/`),
  pipes (`pipe/`), MSAL helpers, RUM helpers, test data, UI helpers.
- `src/constants/` — global constants (`constants.ts`, `enum.ts`,
  `messages.ts`, …). Constant values (APIs, formats, regexes, `EMPTY_STRING`)
  live here, not inline and not duplicated per feature.
- `src/models/` — global interface types (e.g. `table.model.ts`,
  `user.model.ts`). Only shapes shared across areas live here.
- `src/scss/` — global stylesheets: `base/`, `components/`, `helpers/`, `pages/`.

## Standard Feature Module Layout (`src/app/<area>/<feature>/`)

Every feature module uses this layout. All folders below are
**feature-private** — only the feature's own module/service/components may
import them. The single exception is `api/`, which NEVER lives inside the
feature (it lives in `src/api/<area>/<feature>/`).

```
<feature>/
├── components/          # UI components, pages, forms, dialogs
├── directives/          # feature-private attribute + structural directives
├── pipes/               # feature-private format/transform pipes for display
├── services/            # business logic, orchestration, state access
├── models/              # feature-private interfaces, types, view-models,
│                        # request/response view shapes (backend DTOs stay
│                        # in src/api/<area>/<feature>/*.dto.ts)
├── constants/           # feature-private constants (*.constants.ts, plural)
├── enums/               # feature-private enums used within the feature
├── validators/          # feature-private custom form validators
├── guards/              # feature-private route-access guards
├── interceptors/        # feature-private HTTP interception (feature scope only)
├── utils/               # feature-private pure functions, mappers, helpers
├── store/               # feature-private NgRx state (only when needed)
├── <feature>-routing.module.ts  # route declarations
└── <feature>.module.ts           # declarations + imports
```

Real exemplar: `src/app/admin/users/` (`components/`, `services/`,
`users-routing.module.ts`, `users.module.ts`) — new folders from the list
above are added only when the feature actually needs that kind
(no empty placeholder folders).

## Feature-Private vs App-Wide Placement

| Kind | Feature-private (`src/app/<area>/<feature>/…`) | App-wide (`src/…`) |
|---|---|---|
| Components | only this feature renders it → `components/` | 2+ features reuse it → `src/shared/components/` |
| Directives / pipes | only this feature uses it → `directives/` / `pipes/` | reused → `src/shared/directive/` / `src/shared/pipe/` |
| Services / state | feature orchestration → `services/` / `store/` | cross-feature → `src/app/services/` or NgRx root |
| Constants | one feature only → `<feature>/constants/` | 2+ consumers (e.g. `EMPTY_STRING`) → `src/constants/` |
| Enums | one feature only → `<feature>/enums/` | shared → `src/constants/enum.ts` |
| Models / types | feature view-model → `<feature>/models/` | shared shape → `src/models/` (+ backend DTO → `src/api/…/*.dto.ts`) |
| Validators | one form/feature → `<feature>/validators/` | reused → `src/app/validators/` |
| Guards / interceptors | feature route/scope → `<feature>/guards/` etc. | app-wide → `src/shared/guard/` (guards), root provider (interceptors) |
| Utils / mappers | feature-only → `<feature>/utils/` | reused → `src/app/util/` |
| API / DTOs | NEVER local — always `src/api/<area>/<feature>/` | `src/api/` is the only home for `*.api.ts` + `*.dto.ts` |
| Styles | component-scoped → `<name>.component.scss` | shared tokens/layouts → `src/scss/` |

- **Procedure**: before creating a new file, search the app-wide location
  first. Create feature-private only when no shared unit fits; promote to
  app-wide on second use (refactor workflow) instead of duplicating.
- **Banned**: feature → sibling feature deep import
  (`../sibling-feature/...`); share via `src/shared/`, `src/constants/`,
  `src/models/`, or an explicit contract instead.

## Path Aliases & Restricted Imports

- Services: `@services/*` maps to `src/app/services/*`. Never import the root
  `@services` barrel — always a category subfolder (e.g.
  `@services/state/custom-view/custom-view.service`). Never use relative paths
  (`../services/...`, `./services/...`) for services.
- Other shared code: relative paths or direct `src/` paths
  (e.g. `src/shared/components/...`).

## SCSS Facts

- Classic `@import` syntax (not Dart Sass `@use`); all `@import` statements at
  the absolute top of the stylesheet, before any rules or variables.
- Component styles via `styleUrls`, kept in the component's `.component.scss`
  and scoped to the component selector.
- Reuse design variables (e.g. `src/scss/helpers/variable`), Material styles,
  and Bootstrap utilities instead of hardcoding values.
