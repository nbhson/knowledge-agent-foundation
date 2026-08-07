# Phase 1 Hook - Understanding

## Goal

Load the correct guidance and build accurate context before proposing or implementing changes.

## Trigger

Run this hook immediately after receiving a developer request.

## Required Steps

1. Determine workflow type:
   - Jira Ticket Review
   - Feature Delivery
   - Bug Fix
   - Refactor
   - Unit Test
   - Code Review
2. Load guidelines for that workflow from `.agents/skills/`.
3. Load repository guidance from:
   - `.agents/copilot-instructions.md`
   - `.agents/knowledge/`
   - `.agents/skills/` (as relevant)
   - `.agents/reports/` (as relevant)
4. Load MCP context (when servers are available):
   - **Jira MCP**: Fetch the ticket (`SP0168-...`) — description, acceptance criteria, comments, status. The ticket is the source of truth for scope.
   - **Figma MCP**: Fetch the design file/frame — layout, tokens, labels, component states. The design is the source of truth for UI.
   - If a server is unavailable, do NOT block; request the developer to paste the equivalent ticket/design summary.
5. Load report context from `.agents/reports/`:
   - **Strict Mode**: Must read the latest workflow-relevant `*.ctx.md` (or latest report for the same ticket/component), then carry forward decisions, risks, unresolved items, and validation evidence.
   - **Non-Strict Mode**: For non-trivial/code-change tasks, read the latest relevant report summary first; for trivial/no-code queries, report loading may be skipped.
   - Use report context as planning input to avoid repeated analysis.
6. Investigate code context:
   - Analyze target modules/files and dependencies.
   - Search for reusable constants, models, shared components, and services.
   - Avoid duplicate code.
7. Apply stack rules:
   - Angular 15 module patterns
   - SCSS conventions
   - service import and coding style constraints

## Exit Criteria

- Workflow type is identified.
- Relevant skills/knowledge are loaded.
- MCP context (Jira ticket / Figma design) is loaded when servers are available, or the developer has supplied equivalent context.
- Strict Mode: relevant report context from `.agents/reports/` is loaded.
- Non-Strict Mode: report context is loaded for non-trivial/code-change tasks.
- Investigation findings are captured and ready for planning.