---
name: styling-standards
description: Guidelines for modular SCSS structures, order of imports, CSS variables, and responsive grid layouts in the Horizon 2 UI project.
---

# Styling Standards & SCSS Guidelines

This skill defines the SCSS rules for the Angular 15 application. Follow the
existing structure under `src/scss/` and prefer the smallest local change that
preserves Angular Material, Bootstrap, and component encapsulation behavior.

## 1. Style Ownership and File Placement

Use the narrowest valid scope:

| Need | Location | Examples |
| --- | --- | --- |
| Application-wide reset, fonts, theme, Material, or overlay styles | `src/styles.scss` or an imported `src/scss/` partial | `_reset.scss`, `_theme.scss`, `_material-icon.scss` |
| Reusable visual primitive used by multiple features | `src/scss/components/` or `src/scss/helpers/` | `_button.scss`, `_main-table.scss`, `_mixin.scss` |
| Page/feature layout | The owning component `.component.scss` | `studies.component.scss` |
| One component's internal presentation | That component's `.component.scss` | `header.component.scss` |

- Keep component-specific rules in the component stylesheet. Do not add feature
  selectors to `styles.scss` just to bypass encapsulation.
- Use a shared partial only when the pattern has at least two real consumers;
  do not create a partial for a one-off rule.
- Do not use `autoId`, element text, or generated Material classes as the
  primary styling hook. Use semantic classes; `autoId` is for automation only.
- Do not add inline styles or `[style]` bindings for maintainable layout or
  colors. Use classes and state classes instead.

## 2. SCSS Imports and Layer Order

All imports must appear before variables, declarations, and selectors. For a
component stylesheet, use this order where applicable:

```scss
@import '../../../../scss/helpers/variable';
@import '../../../../scss/helpers/mixin';
@import '../../../../scss/helpers/extend';
@import '../../../../scss/helpers/common';
@import '../../../../scss/components/main-table';
```

The global entrypoint follows the application's layer order:

1. Helpers and tokens (`variable`, `fonts`)
2. Base (`reset`)
3. Shared components and Material helpers
4. Page/feature styles only when they are intentionally global

The project uses legacy `@import` for application partials. The only current
exception is `src/scss/base/_theme.scss`, which uses `@use '@angular/material'
as mat` because Angular Material's Sass API requires a namespace. Do not
replace that exception with an unnamespaced import or introduce `@use` for
ordinary project partials without an Angular/Sass migration plan.

## 3. Tokens, Colors, Typography, and Dimensions

- Reuse tokens from `src/scss/helpers/_variable.scss` for colors, font sizes,
  font weights, fixed header/table dimensions, and shared shadows.
- If a value is a reusable design decision but no token exists, add one to
  `_variable.scss` with a meaningful name, then consume the token. Do not
  scatter new hex colors, rgba values, font sizes, or repeated heights across
  component files.
- Raw values are acceptable for genuinely local geometry, such as a small
  icon offset or a one-off grid calculation. They are not acceptable for a
  repeated color, typography value, breakpoint, or application chrome height.
- Keep `$shadow-small` and similar tokens free of `!important`; importance is a
  selector-level decision, not part of a reusable value.
- Prefer the existing `$font*` and `$fw-*` tokens. Use the project's font
  partial rather than introducing a new font stack in a feature stylesheet.
- Theme-dependent values belong in `_theme.scss` as CSS custom properties
  under `[data-theme='light']`/`[data-theme='dark']`; consume them with
  `var(--...)` in rules that support both themes.

## 4. Helpers, Mixins, and Selector Design

- Search `helpers/_mixin.scss`, `helpers/_extend.scss`, `helpers/_common.scss`,
  and `components/` before adding a duplicate pattern.
- Use a mixin for parameterized output; use `%placeholder`/`@extend` only for
  a genuinely shared structural pattern. Avoid extending selectors across
  unrelated component boundaries.
- Keep selectors shallow (ideally two or three levels). Avoid styling raw
  `div`, `span`, or broad Material classes from a component stylesheet unless
  the rule is intentionally global and documented by its owning partial.
- Follow the existing local naming style: descriptive kebab-case component
  classes and the established BEM-like `__`/`--` state names where that
  component already uses them. Do not rename existing classes only for style.
- Put pseudo-classes and state modifiers next to their base selector. Cover
  hover, focus-visible, disabled, selected, loading, and error states where
  the element supports those states.

## 5. Angular Material, Overlays, and Specificity

- Prefer Angular Material theme configuration and component APIs over private
  DOM selectors. `_theme.scss` is the owner for theme-wide Material output.
- Dialogs, menus, selects, tooltips, autocomplete panels, and similar overlays
  render outside the component host. Their global rules belong in a shared
  global partial, not only in a component stylesheet.
- Use `::ng-deep` only when Angular view encapsulation prevents a required
  third-party/Material override, scope it under the owning component class,
  and add a short reason. Do not use unscoped `::ng-deep`.
- Treat `!important` as an exception for Material/Bootstrap specificity or a
  deliberate state override. Before adding it, try a scoped selector or theme
  configuration. Never put `!important` in a token or use it to compensate
  for unclear ownership.
- Do not target generated MDC internals unless there is no supported API and
  the selector is isolated in the appropriate global partial.

## 6. Layout and Responsive Behavior

- Prefer flexbox for one-dimensional toolbars/forms and CSS grid for
  two-dimensional page/table layouts. Use the existing project dimensions
  (`$header-height`, `$tool-bar`, `$tab-height`, `$sidebar-width`, and related
  tokens) when calculating viewport space.
- Define stable sizing for tables, toolbars, tabs, dialogs, and icon buttons so
  labels, loading states, and validation messages do not shift the layout.
- Every new page or layout change must be checked at the project's desktop and
  narrow viewport targets. Content must not be hidden behind sticky headers,
  overflow containers, sidebars, dialogs, or pagination.
- Prefer fluid tracks (`minmax`, `1fr`), wrapping, and controlled overflow over
  fixed pixel widths. If horizontal scrolling is intentional, scope it to the
  table/list viewport and preserve access to headers and actions.
- Keep sticky/fixed elements paired with responsive behavior; reset `sticky`
  or reduce the layout at the narrow breakpoint when it would obscure content.

```scss
.tracker-main-container {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(18rem, 1fr);
  gap: 1rem;

  @media (max-width: 992px) {
    grid-template-columns: minmax(0, 1fr);
  }
}
```

## 7. Accessibility and Interaction States

- Preserve visible keyboard focus. Do not remove outlines without providing an
  equivalent `:focus-visible` treatment.
- Keep text/background contrast and disabled-state contrast readable; do not
  communicate status by color alone when an icon, label, or text state exists.
- Ensure clickable targets remain usable when labels wrap or browser text size
  increases. Avoid fixed heights that clip translated text, errors, or focus
  rings.
- Respect reduced-motion preferences for non-essential transitions and avoid
  animation that changes layout or blocks interaction.

## 8. Validation Checklist

Before completing a style change:

1. Confirm imports are at the top and partial ownership is correct.
2. Search for an existing token, mixin, extend, Material theme rule, or shared
   partial before adding new CSS.
3. Check for unintended global leakage, excessive specificity, `::ng-deep`,
   and new `!important` usage.
4. Verify desktop and narrow layouts, overflow, sticky regions, dialogs and
   Material overlays affected by the change.
5. Confirm focus, disabled, error, loading, selected, and empty states where
   applicable.
6. Run `npm run format`, `npm run lint`, and `npm run build` for the final
   change. For visual changes, run `npm run startdev` and inspect the affected
   route manually.
