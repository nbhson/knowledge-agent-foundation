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

- `src/shared/` — global components, decorators, directives, DTOs, guards,
  material configurations, pipes.
- `src/constants/` — global constants (`constants.ts`, `enum.ts`,
  `messages.ts`). Constant values (APIs, formats, regexes) live here, not inline.
- `src/models/` — global interface types (e.g. `table.model.ts`).
- `src/scss/` — global stylesheets: `base/`, `components/`, `helpers/`, `pages/`.

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
