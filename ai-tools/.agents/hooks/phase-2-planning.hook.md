# Phase 2 Hook - Planning

## Goal

Create an implementation plan and enforce the approval gate before coding.

## Trigger

Run this hook after Phase 1 has completed.

## Required Steps

1. Produce a concise draft plan including (see ## Mandatory rules section):
   - intended goal and behavior changes
   - files/modules likely to be touched
   - validation approach (lint, tests, build, manual checks)
2. For non-trivial work, request explicit developer approval before making edits.
3. If plan feedback is provided, revise and re-present the plan.
4. Repeat the approval loop until approved.

## Mandatory rules

[Priority] Strictly apply all that: 

For any non-trivial request, Copilot must first present a concise draft plan before implementation begins. The draft plan should briefly cover:

- the intended change or goal,
- the likely files/modules to touch,
- the validation approach.

**Approval Gate scope:**
- **Non-trivial requests** (multiple files, behavior changes, or significant implementation work): Copilot MUST pause and wait for the developer to review/approve the plan before proceeding to code changes.
- **Trivial/no-code queries**: Copilot presents the draft plan (or brief summary) and may proceed without an explicit pause.

Only continue immediately when the user explicitly asks to do so.

---

## Exit Criteria

- Need to create a draft plan and get approve (DO NOT SKIP)
- Approved plan is available (or trivial case acknowledged).
- Execution task list can be derived from the approved plan.