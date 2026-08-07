# Copilot Instructions — Entry Point

This is the entry point for all AI agents working on the Horizon 2 UI (Angular 15) repository.

## 1. Read These First

1. `.agents/AGENTS.md` — main orchestration workflow (request classification, 5-phase workflow, strict compliance & memory artifacts).
2. `.agents/GEMINI.md` — guidelines for Gemini models (stack, validation checklist, strict compliance).
3. `.agents/hooks/session.json` — maps phase hooks to lifecycle events.
4. `.agents/knowledge/core-engineering-guidelines.md` — repository-wide technical guidance (Angular 15, SCSS, imports, services, security).
5. `.agents/knowledge/frontend-architecture.md` — Angular 15 module-based architecture and directory structure.

## 2. Strict-Mode Contract

- Execute all 5 phases in order: Understanding → Planning → Execution → Validation/PR → Report.
- Respect the Planning Gate: present an implementation plan and wait for developer approval before writing code (non-trivial tasks).
- Reference `.agents/workflows/<workflow>.md` for the request-type-specific execution plan, and `.agents/rules/*.md` for coding standards.
- Run hooks via `.agents/hooks/` (post-code-change, pre-pull-request, report-generation) as defined.
- Always produce a `*.ctx.md` engineering report in `.agents/reports/` on completion.

## 3. Validation Checklist

- `npm run lint` + `npm run format` after each code change.
- `npm run build` + `npm run test` before opening a Pull Request.