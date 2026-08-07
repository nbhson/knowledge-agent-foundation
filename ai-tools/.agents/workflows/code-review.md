# Workflow: Code Review

Instructions for reviewing code contributions and validating coding conventions in the Horizon 2 UI.

---

## 1. Rules Mapping by Scope

Always apply the following coding guidelines. Load additional rules based on the components touched:

| **Scope / Component**               | **Rules to Load** | **Why to Load / Description**                                                                              |
| ----------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------- |
| **All Workflows / Modifications**   | `coding-style.md` | Enforces code reuse, check `/core` assets (constants, styles, models) before coding, and types safety.     |
| **Routing & Folder Structure**      | `angular.md`      | Enforces Angular components structure, file suffixes, and lazy loading configuration.                      |
| **Component Logic & Reactivity**       | `angular.md`      | Enforces Angular 15 module architecture, RxJS reactivity, @Input/@Output, and lazy-loaded feature modules. |
| **Styling, Layout, Responsiveness** | `scss.md`         | Enforces SCSS imports conventions, mixins, glass panels, and prevents styling duplication.                 |
| **Documentation & Reports**         | `templates.md`    | Dictates which markdown templates to use for Jira reviews, bug reports, and pull requests.                 |

## 2. Orchestration Workflow

You MUST NOT immediately start implementation. Always follow these sequential steps for code reviews:

### Step 1 — Load Knowledge
- Load `.agents/knowledge/module-map.md`, `.agents/knowledge/frontend-architecture.md`, and `.agents/knowledge/design-system.md` to establish the baseline standards required to verify that external contributions conform to guidelines.

### Step 2 — Apply Rules
- Enforce rules based on the **Rules Mapping by Scope** table above.

### Step 3 — Review Checklist
- **Architecture**: Ensure NgModule-based components declared in the correct modules with `ChangeDetectionStrategy.OnPush` where appropriate. Verify parent/child container/presenter architecture.
- **TypeScript & Angular**: Enforce Angular 15 patterns: RxJS state management, @Input/@Output, *ngIf/*ngFor (with trackBy), proper NgModule declarations, and services imported via @services/... aliases.
- **Styling & Layout**: Verify classic Dart Sass `@import` modular styles. Avoid hardcoded hex colors, use variables (`var(--primary)`, gradients) and standard mixins. Prohibit inline CSS styling.
- **Security & Tokens**: Confirm environment variables are loaded properly (no hardcoded secrets).
- **Performance**: Verify router paths utilize classic module lazy loading (`loadChildren` -> `.module()`).
- _Do NOT modify source code during this phase._

### Step 4 — Approval Gate
- Present the review feedback to the developer.
- Provide actionable feedback on how to improve or correct any deviations from the project standards.
- _Note: This workflow is review-only. No codebase modifications or automated hooks are executed._
