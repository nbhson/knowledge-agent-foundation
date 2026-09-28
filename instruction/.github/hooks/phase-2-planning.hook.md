# Phase 2 Hook - Planning

## Goal

Create an implementation plan and enforce the approval gate before coding.
Resolve contradictions before finalizing implementation design.

## Trigger

Run this hook after Phase 1 has completed.

## Error Handling & Edge Cases

- **No contradictions found**: Proceed directly to plan creation; note "no contradictions" in report
- **Developer unavailable for approval**: Document pending decisions with timeout (e.g., "awaiting dev input — defaulting to X if no response in 24h")
- **Plan rejected multiple times**: Escalate to senior developer/architect for decision; document resolution
- **Scope creep detected**: Flag scope changes explicitly; require separate ticket for out-of-scope items
- **Conflicting priority between AC**: Present conflict to developer; block until resolved

## Required Steps

1. Produce a concise draft plan including (see ## Mandatory rules section):
   - intended goal and behavior changes
   - files/modules likely to be touched
   - validation approach (lint, tests, build, manual checks)
2. Run contradiction gate before plan approval:
   - Present identified contradictions/ambiguities from Phase 1.
   - Get developer decisions to resolve each item.
   - Freeze final interpretation (source of truth) for execution.
   - If the developer does not clarify unresolved contradictions, STOP and keep the task in blocked/planning state. Do not proceed to implementation.
3. For non-trivial work, request explicit developer approval before making edits.
4. If plan feedback is provided, revise and re-present the plan.
5. Repeat the approval loop until approved.

## Mandatory rules

[Priority] Strictly apply all that: 

For any non-trivial request, Copilot must first present a concise draft plan before implementation begins. The draft plan should briefly cover:

- the intended change or goal,
- the likely files/modules to touch,
- the validation approach.
- contradiction resolution summary (what was conflicting, what decision was frozen).

**Approval Gate scope (single threshold table — authoritative):**

| # | Signal | Threshold | Outcome |
|---|--------|-----------|---------|
| 1 | Files/modules touched | ≥2 files or ≥2 modules | Non-trivial → explicit approval required |
| 2 | Behavior change | Any runtime behavior, UI contract, API shape, or data-flow change | Non-trivial → explicit approval required |
| 3 | Shared surface | Touches `src/shared/`, `@services/*` shared service, NgRx store/effects, auth guard, or routing | Non-trivial → explicit approval + `implementation_plan.md` file required |
| 4 | Security/sensisitivity | Auth, secrets, tokens, PII, payment, or customer-facing flow | Non-trivial → explicit approval + `implementation_plan.md` file required |
| 5 | Acceptance clarity | Any blocking contradiction, missing/ambiguous AC, or conflicting ticket vs design | Blocked → resolve + freeze before planning completes; no execution until resolved |
| 6 | Trivial | ≤3 lines in ONE file, no behavior change (typo, comment, whitespace) | Brief plan in chat, no pause, still P3+P5 |
| 7 | Pure Q&A | No code change and no report requested | No phases; answer directly |

Rules 6–7 define the trivial / pure-Q&A outcomes. `session.json:quick_mode`
is a pointer-only block (no duplicated rules) referencing this table via
`authoritative_ref`; strict mode still executes the `still_required` phases
listed in rows 6–7 (P3+P5 for rule 6).
Rule 5 always wins: any unresolved blocking item forces Blocked state regardless
of the other rows.

**Plan artifact rule:**
- Rows 3–4 (shared/security) or any multi-module feature/refactor → write
  `implementation_plan.md` at repo root from `report-templates/technical-design.md`
  (working doc, never committed, deleted after approval, content carried into the
  Phase 5 report).
- Other non-trivial work → concise draft plan in chat is sufficient unless the
  developer asks for the file.
- Every code change (including trivial rule 6) still files a Phase 5 report.

Only continue immediately when the user explicitly asks to do so.

---

## Exit Criteria

- Need to create a draft plan and get approve (DO NOT SKIP)
- Contradiction gate is completed: all identified contradictions are resolved or explicitly deferred with owner/action.
- Contradiction gate is completed with explicit developer decisions for all blocking contradictions.
- If any blocking contradiction remains unresolved (including missing developer clarification), execution must not start.
- Approved plan is available (or trivial case acknowledged).
- Execution task list can be derived from the approved plan.