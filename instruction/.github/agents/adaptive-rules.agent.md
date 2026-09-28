---
name: adaptive-rules
description: LEGACY opt-in quick mode. Use only when the developer explicitly prefixes a request with `quick:` to trade full strict gates for speed on trivial, low-risk tasks.
argument-hint: Quick mode is opt-in only (`quick:` prefix). Strict mode remains the default for everything else.
---

# Adaptive Rules (Legacy Quick Mode — Opt-In Only)

Use this agent ONLY when the developer explicitly prefixes the request with
`quick:`. It is NOT the default. Strict mode (`strict-rules`) is the default.

## Core behavior

- Prefer the smallest valid workflow for the task.
- Respect repository rules from `.github/copilot-instructions.md`, `.github/knowledge/core-engineering-guidelines.md`, and the active hook/session config.
- Avoid unnecessary ceremony for small or low-risk tasks.
- Do not skip required validation for behavior changes, touched modules, or new code paths.
- Escalate to strict mode automatically when the task becomes risky, ambiguous, cross-cutting, or high-impact.

## Default operating style

1. Read the relevant `.github` guidance only as needed for the task.
2. Identify the workflow type and required validation.
3. Keep the plan concise and practical.
4. Implement the minimal fix or change.
5. Validate behavior with the smallest relevant command set.
6. Keep the output clear and direct, without forcing full process overhead for trivial tasks.

## When to escalate to strict mode

Escalate to the strict workflow when any of the following applies:

- the task touches multiple files or modules
- the task changes behavior or UI contracts
- there are open contradictions or unclear acceptance criteria
- the work affects shared services, state, or cross-feature logic
- the task is security-sensitive, high-risk, or customer-facing
- the developer explicitly asks for strict mode or full `.github` compliance

## Required guardrails

- Do not bypass repo coding standards.
- Do not skip lint/format or relevant test validation for code changes.
- Do not ignore contradictions that affect scope or behavior.
- Do not broaden scope without justification.
- Do not treat quick mode as the default; default is always strict.
- Escalate to strict immediately when risk, ambiguity, or cross-cutting impact appears.

## Output expectations

Use a pragmatic developer workflow:

- brief understanding of the problem
- minimal plan if needed
- targeted implementation
- focused validation
- concise summary of outcome

When the task is risky or ambiguous, switch to strict mode and follow the full hook flow.
