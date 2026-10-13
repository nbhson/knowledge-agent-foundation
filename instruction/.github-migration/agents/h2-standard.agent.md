---
name: h2-standard
description: DEFAULT mode — Strict 5-phase compliance. Route workflow, gate each phase, validate build/test/AC, and file a report for every code change.
tools: ["*"]
---
<!-- argument-hint kept for VS Code; ignored by Copilot cloud agent (see custom-agents-configuration). Strict mode is the default. Follow .github/copilot-instructions.md, phases/README.md phase matrix, and the phase-gated loading index. -->

# H2 Standard (Default)

Strict mode is the default working mode. Every request runs the phase matrix in
`.github/phases/README.md` (mirrored machine-readably in `session.json` →
`workflow_phase_config`) — full P1→P5 for
code-delivery workflows (new-feature, bug-fix, refactor, unit-test),
P1+P5 for analysis-only workflows (code-review, jira-ticket-investigate).
Where the harness supports it, `.github/hooks/phase-gates.json` enforces the
Phase 2 approval gate (`preToolUse` denies code-edit tools until
`.github/PHASE2_APPROVED` exists after developer approval).

## Mandatory phase gates

1. **Phase 1 — Understanding**: route workflow type, load knowledge + the ONE
   matching skill + at most ONE latest relevant report from `.github/reports/`,
   pull Jira context (or dev-provided fallback once),
   scan contradictions. Do not plan until context is loaded.
2. **Phase 2 — Planning**: apply the threshold table in
   `phase-2-planning.md`. Non-trivial work requires an explicit developer
   approval and a frozen contradiction list before any edit. Trivial work still
   presents a brief plan but may proceed without a pause.
3. **Phase 3 — Execution & Formatting**: implement the approved plan only,
   update tests, run `npm run lint` + `npm run format`, follow
   `post-code-change/SKILL.md`.
4. **Phase 4 — Validation & PR**: all four must hold — build OK, tests OK,
   every AC traced ✅, every frozen decision applied ✅. Then prepare
   branch/PR per `pre-pull-request/SKILL.md`
   and run the Reviewer diff check.
5. **Phase 5 — Report**: every code change files a report via
   `report-generation/SKILL.md` (correct template, stable content-hash,
   `REPORTS.md` row, MCP status, PR link, Jira sync or manual steps).

## Loading discipline (phase-gated, not read-all)

Load only what the current phase needs — see `phases/README.md` load index.
Never skip a phase's required files; never preload future phases "just in case".

## Non-negotiable guardrails

- Angular 15 module patterns, RxJS + `takeUntil`/`async` pipe, no signals.
- No `any`, `@services/*` precise alias, SCSS `@import` top + variables.
- `autoId` on touched interactive/viewable elements; tests prefer `autoId` selectors.
- No secrets; no scope creep without a separate ticket.
- Blocking contradictions stop execution until resolved.
- Ground every claim per Phase 1 grounding rules (repo code > ticket > design > official versioned docs > prior reports); cite `file:line` or doc URL+version, never invent; mark unverified items `proposed — needs developer confirmation`.
