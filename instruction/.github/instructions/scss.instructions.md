---
name: 'SCSS standards'
description: 'Use when creating or editing SCSS stylesheets.'
applyTo: '**/*.scss'
---

# SCSS (legacy @import project)

- Classic `@import` at the **absolute top** of the stylesheet (before any rules/variables). Only exception: `src/scss/base/_theme.scss` uses `@use '@angular/material' as mat`.
- Component styles via `styleUrls`, scoped to the component selector, in the component `.component.scss`.
- Reuse tokens from `src/scss/helpers/_variable.scss` (colors, fonts, header/table dims, shadows) — no new hardcoded hex/typography for repeated values.
- Details: `.github/skills/styling-standards/SKILL.md`. TS-side palette colors live in the owning feature `*.constants.ts` (plural), bound to CSS custom properties — never duplicated as literals.
