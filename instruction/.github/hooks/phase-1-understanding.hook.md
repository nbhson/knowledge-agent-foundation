# Phase 1 Hook - Understanding

## Goal

Load the correct guidance and build accurate context before proposing or implementing changes.
Surface contradictions/ambiguities early so planning is based on a single agreed interpretation.

## Trigger

Run this hook immediately after receiving a developer request.

## Error Handling & Edge Cases

Before proceeding, handle these common edge cases:

- **Missing Jira ticket**: Use dev-provided summary as source of truth for scope and AC
- **Missing Figma design**: Request screenshot from developer; verify UI visually against developer reference
- **Conflicting AC**: Escalate to developer with explicit contradiction list; never proceed without resolution
- **Missing MCP servers**: Never block workflow; always provide manual fallback instructions
- **Build/test failures**: Return to Phase 3 with specific error context (file/line/error message), not generic message
- **Empty report context**: Proceed with fresh analysis; flag in report as "no prior context — first task for this component"
- **Rapid succession tasks on same ticket**: Link to previous report in `.github/reports/` instead of duplicating analysis
- **Oversized PRs (>500 lines)**: Suggest splitting into multiple tickets/PRs for maintainability
- **No acceptance criteria in ticket**: Propose default AC based on ticket description; mark as "proposed — needs developer confirmation"
- **Circular ticket dependencies**: Flag explicitly; block execution until dependency resolution is documented

## Required Steps

1. Determine workflow type:
   - Jira Ticket Review
   - Feature Delivery
   - Bug Fix
   - Refactor
   - Unit Test
   - Code Review
2. Load guidelines for that workflow from `.github/skills/`.
3. Load repository guidance from:
   - `.github/copilot-instructions.md`
   - `.github/knowledge/`
   - `.github/skills/` (as relevant)
   - `.github/reports/` (as relevant)
4. Load MCP context with an operational availability probe (do not guess — probe once per server, one MCP tool call each, 60s timeout):
   - **Jira MCP → Available** iff one ticket-fetch tool call for the ticket key returns description + AC + status within the timeout. **Otherwise Manual fallback**: ask the developer ONCE to paste ticket summary (key, description, AC list, priority); record `Jira: Manual fallback — <reason>`.
   - **Figma MCP → Available** iff one file/frame-fetch tool call for the design key returns layout/tokens/labels within the timeout. **Otherwise Manual fallback**: ask the developer ONCE for a screenshot or design spec; verify visually; record `Figma: Manual fallback — <reason>`.
   - **Bitbucket MCP → Available** iff one branch/PR tool call (list, or dry-run create) succeeds within the timeout. **Otherwise Manual fallback**: prepare the full PR description for the developer to create manually; record `Bitbucket: Manual fallback — <reason>`.
   - The ticket is the source of truth for scope; the design is the source of truth for UI. Every report's `MCP Status` section must state per-server Available/Manual fallback + reason + what replaced it.
5. Load report context from `.github/reports/`:
   - **Strict Mode**: Must read the latest workflow-relevant `*.ctx.md` (or latest report for the same ticket/component), then carry forward decisions, risks, unresolved items, and validation evidence.
   - **Non-Strict Mode**: For non-trivial/code-change tasks, read the latest relevant report summary first; for trivial/no-code queries, report loading may be skipped.
   - Use report context as planning input to avoid repeated analysis.
6. Investigate code context (grounded — no guessing):
   - Analyze target modules/files and dependencies by READING them; cite `path:line` for every claim.
   - Search for reusable constants, models, shared components, and services before introducing anything new.
   - Avoid duplicate code.

## Source Grounding (anti-guessing — mandatory)

Source hierarchy (higher wins on conflict): (1) repository code just read
(including `package.json`/lockfile versions when present — they override everything
below), (2) Jira ticket (MCP or dev-pasted), (3) Figma design (MCP or screenshot),
(4) official docs for the pinned stack, (5) prior `.github/reports/` context
(may be stale — re-verify).

Pinned doc versions — always include the version in the search query and cite the
doc's stated version (e.g., `angular 15.2 httpclient`, `rxjs 7.8 takeUntil`,
`ngrx 15 store`, `jest 29 mock`, `msal-angular azure v2`):
Angular 15.2.1 (pinned in `knowledge/`), RxJS 7.x, NgRx 15.x, Jest 29.x,
MSAL Angular v2.x. Never cite v16+/v8+ docs for this repo.

Rules:
- Never invent APIs, versions, file paths, behavior, or ticket/design content. If it is not in a listed source, mark it `proposed — needs developer confirmation` and stop before coding on top of it.
- Every factual claim in plans and reports carries its source: `file:line`, ticket key + field, Figma frame + element, or doc URL + version.
- Conflicting sources go to the contradiction list (step 7); do not silently pick one.
- Prior reports are hints, not truth: re-check the code before reusing their conclusions.
7. Identify contradictions and ambiguities:
   - Compare ticket/context, design specs, clarification comments, and current behavior.
   - Capture any conflicting statements, missing rules, or unclear edge cases.
   - Propose default interpretations but mark them as pending until developer confirmation.
8. Apply stack rules:
   - Angular 15 module patterns
   - SCSS conventions
   - service import and coding style constraints

## Exit Criteria

- Workflow type is identified.
- Relevant skills/knowledge are loaded.
- MCP context (Jira ticket / Figma design) is loaded when servers are available, or the developer has supplied equivalent context.
- Strict Mode: relevant report context from `.github/reports/` is loaded.
- Non-Strict Mode: report context is loaded for non-trivial/code-change tasks.
- Contradictions/ambiguities are explicitly listed with proposed resolutions and owner for sign-off.
- Investigation findings are captured and ready for planning.

## Phase Routing Decision

After Phase 1 completes, route to the appropriate phases based on workflow type (see `session.json` → `workflow_phase_config`):

| Workflow Type | Phase 2 (Planning) | Phase 3 (Execution) | Phase 4 (Validation) | Phase 5 (Report) |
| :--- | :---: | :---: | :---: | :---: |
| Bug Fix | ✅ Required | ✅ Required | ✅ Required | ✅ Required |
| Feature Delivery | ✅ Required | ✅ Required | ✅ Required | ✅ Required |
| Refactor | ✅ Required | ✅ Required | ✅ Required | ✅ Required |
| Unit Test | ✅ Required | ✅ Required | ✅ Required | ✅ Required |
| **Jira Ticket Review** | ⏭️ Skip | ⏭️ Skip | ⏭️ Skip | ✅ Required |
| **Code Review** | ⏭️ Skip | ⏭️ Skip | ⏭️ Skip | ✅ Required |

**For Jira Ticket Review and Code Review**: proceed directly from Phase 1 to Phase 5. Do NOT enter Phase 2 planning/approval loop, do NOT execute code changes, do NOT run build/test validation gates.