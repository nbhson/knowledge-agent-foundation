# Gemini Workspace Guidelines

Guidelines for Gemini models working on the Horizon 2 UI (Angular 15) project.

---

## 1. Stack & Standards

- **Core**: Angular 15.2.1, classic **Module-Based (NgModule)** architecture. Do NOT use Standalone Components, Signals, `resource()`, or `@if`/`@for` control flow.
- **State & Binding**: RxJS `Observable`, `Subject`, `BehaviorSubject`, and standard NgRx Store/Effects. Clean up subscriptions with `takeUntil` or the `async` pipe.
- **Control Flow**: Use `*ngIf`, `*ngFor` (always with `trackBy`), and `*ngSwitch` directives. Ensure `CommonModule` is imported.
- **UI & Presentation**: Bootstrap + Angular Material utilities, classic Dart Sass `@import` modular styles (see `.agents/rules/scss.md`). Reuse design system variables.

## 2. Validation & Quality Checklist

Ensure quality checks are performed as follows:

1. **Lint & Format**: Run `npm run lint` and `npm run format` immediately after making code changes (via `post-code-change` hook).
2. **Dedicated Unit Tests**: Write and execute dedicated unit tests using Jest (`npm run test`) for any modified logic (Validation Phase).
3. **Build**: Run `npm run build` to verify zero build and compilation errors (Validation Phase).
4. **Visual Check**: Run `npm run startdev` and manually inspect the responsive layout and browser logs (Validation Phase).

## 3. Workflow Reference & Strict Compliance

- Always refer to [.agents/AGENTS.md](.agents/AGENTS.md) for the main orchestration workflow.
- **CRITICAL COMPLIANCE RULE**: You MUST NOT skip any phases defined in the loaded workflow (e.g., `.agents/workflows/*.md`). You MUST execute them strictly and sequentially. Creating an explicit task checklist (Task Tracker) to track your progress across these phases is MANDATORY.
- **Memory Artifacts**: Every completed task MUST output a `*.ctx.md` engineering report in `.agents/reports/` (Phase 5 — Report Generation). These reports are context memory for future tasks.

## 4. Context & Search Exclusions

- **Strict Ignored Folders**: When executing searches (via `grep_search`, `list_dir`, or shell commands like `find`, `grep`, `ls`), you MUST strictly respect ignore configurations.
- **Excluded Targets**: Absolutely DO NOT search, read, or process files located in folders specified in `.gitignore` and `.aiexclude` (such as `dist/`, `node_modules/`, `.git/`, `.agents/`) unless the user explicitly requests you to inspect a specific excluded path in their prompt.
- **Strict Command Exclusions**: When executing search commands in the shell, you MUST explicitly exclude folders like `dist/`, `node_modules/`, `.git/`, and `.agents/`.