# .github Framework Charter

## Purpose

This directory contains the **development workflow framework** for the Horizon 2 UI project. It orchestrates GitHub Copilot behavior through a structured 5-phase workflow, ensuring code quality, traceability, and consistency across all development tasks.

## Directory Structure

```
.github/
├── CHARTER.md                  # This file — framework overview and governance
├── copilot-instructions.md     # Main entry point for Copilot — always read first
├── agents/                     # AI agent definitions
│   ├── strict-rules.agent.md     # DEFAULT — Strict 5-phase compliance
│   └── adaptive-rules.agent.md   # LEGACY opt-in — quick mode via `quick:` prefix only
├── hooks/                      # Phase-based execution hooks
│   ├── README.md               # Hook index and execution order
│   ├── session.json            # Hook trigger configuration
│   ├── phase-1-understanding.hook.md
│   ├── phase-2-planning.hook.md
│   ├── phase-3-execution-formatting.hook.md
│   ├── phase-4-validation-pr.hook.md
│   ├── phase-5-report-generation.hook.md
│   └── post-merge.hook.md      # Post-merge sync hook
├── knowledge/                  # Repository-wide technical guidance
│   └── core-engineering-guidelines.md
├── report-templates/           # Report templates by workflow type
├── reports/                    # Generated reports (archived monthly)
│   ├── REPORTS.md              # Auto-generated manifest
│   └── archive/                # Archived reports (>30 days)
├── scripts/                    # Validation and utility scripts
│   └── validate-links.sh
├── skills/                     # Workflow-specific skill definitions
│   ├── angular-architecture/SKILL.md
│   ├── bug-fix/SKILL.md
│   ├── code-review/SKILL.md
│   ├── feature-delivery/SKILL.md
│   ├── jira-ticket-review/SKILL.md
│   ├── post-code-change/SKILL.md
│   ├── post-merge/SKILL.md
│   ├── pre-pull-request/SKILL.md
│   ├── refactor/SKILL.md
│   ├── report-generation/SKILL.md
│   ├── rum-activity-tracking/SKILL.md
│   ├── styling-standards/SKILL.md
│   ├── ui-autoid/SKILL.md
│   └── unit-test/SKILL.md
└── workflows/                  # CI/CD pipeline definitions
    └── ci.yml
```

## Workflow Phases

| Phase | Hook | Purpose |
|-------|------|---------|
| 1 | `phase-1-understanding` | Load context, identify contradictions, apply stack rules |
| 2 | `phase-2-planning` | Draft plan, resolve contradictions, get approval gate |
| 3 | `phase-3-execution-formatting` | Implement changes, update tests, lint/format |
| 4 | `phase-4-validation-pr` | Build + test, AC traceability, prepare PR |
| 5 | `phase-5-report-generation` | Generate report, archive, sync Jira |
| X | `post-merge` | Update Jira status, archive report, cleanup |

### Session & guard hooks (defined in `hooks/session.json`)

| Trigger | Hook ID | Purpose |
|---------|---------|---------|
| `sessionStart` | `phase-load-guidance` | Load hook index + all 5 phase hooks |
| `sessionStart` | `phase-1-understanding` | Same as Phase 1 |
| `userPromptSubmitted` | `phase-2-planning`, `phase-3-execution-formatting` | Plan approval + execution |
| `preToolUse` | `phase-guard-apply-rules`, `phase-guard-plan-approval` | Guards before read/edit tools |
| `postToolUse` | `phase-3-execution-formatting` | Lint/format after edits |
| `sessionEnd` | `phase-4-validation-pr`, `phase-5-report-generation`, `post-merge-sync` | Validation + report + Jira sync |
| `errorOccurred` | `phase-recovery` | Re-align phase order on failure |

## Supported Workflow Types

| Workflow | Skill | Template |
|----------|-------|----------|
| Bug Fix | `bug-fix/SKILL.md` | `bug-report.md` |
| Feature Delivery | `feature-delivery/SKILL.md` | `technical-design.md` + `engineering-report.md` |
| Refactor | `refactor/SKILL.md` | `engineering-report.md` |
| Unit Test | `unit-test/SKILL.md` | `engineering-report.md` |
| Code Review | `code-review/SKILL.md` | `pull-request.md` |
| Jira Ticket Review | `jira-ticket-review/SKILL.md` | `jira-ticket-review.md` |

## MCP Integration

| Server | Purpose | Fallback |
|--------|---------|----------|
| Jira MCP | Fetch tickets, sync status | Dev-provided ticket summary |
| Figma MCP | Fetch design specs | Developer screenshot + visual verification |
| Bitbucket MCP | Create branch/PR | Manual PR creation with prepared description |

## Governance

### Adding a New Skill

1. Create directory: `.github/skills/<skill-name>/`
2. Add `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: <one-line description>
   ---
   ```
3. Reference in `copilot-instructions.md` workflow mapping table
4. Add to `session.json` if it requires a new hook trigger

### Adding a New Hook Phase

1. Create `.github/hooks/phase-N-<name>.hook.md`
2. Define: Goal, Trigger, Required Steps, Exit Criteria, Edge Cases
3. Register in `session.json` under appropriate trigger (`sessionStart`, `sessionEnd`, etc.)
4. Update `README.md` and `copilot-instructions.md`

### Report Lifecycle (single source of truth)

1. Reports generated in `.github/reports/` with `.ctx.md` extension, status `active` in `REPORTS.md`.
2. Post-merge hook moves its report to `.github/reports/archive/YYYY-MM/` and flips its `REPORTS.md` row to `archived`.
3. Monthly scheduled CI moves remaining reports older than 30 days to `archive/YYYY-MM/` and flips their rows to `archived`.
4. Archived reports older than 90 days are deleted and their `REPORTS.md` rows removed.
5. `REPORTS.md` rows are added on creation, flipped on archive, removed on delete — never left stale.

### Hash Integrity (stable content-hash)

- Each report created after 2026-09-11 has SHA-256 hash in `## Meta` section (first 12 hex chars).
- Hash is computed over file content EXCLUDING the `SHA-256 Hash` row itself:
  `grep -v 'SHA-256 Hash' <report> | sha256sum | cut -c1-12`
  so the stored value stays valid after insertion.
- `validate-links.sh` verifies content-hash consistency on CI.
- Reports created on or before 2026-09-11 without `## Meta` are marked `legacy`
  in `REPORTS.md` and emit a WARN (not an error). They are exempt from hash/MCP
  enforcement but should not be used as format examples for new work.

## Contributing

When modifying files in `.github/`:
1. Run `bash .github/scripts/validate-links.sh` before committing
2. Ensure all referenced paths exist
3. Update this CHARTER.md if structure changes
4. Test hooks in both strict and quick mode

## Version

- Framework version: 1.3
- Last updated: 2026-09-11
- Changelog 1.3: single source of truth for trivial/non-trivial threshold
  (`phase-2-planning.hook.md`; `session.json:quick_mode` is pointer-only),
  added root `README.md` (framework-only vs full checkout), hardened
  `.gitignore` (`implementation_plan.md`, node/dist).
- Changelog 1.2: fixed agents description (strict default), clarified legacy-report
  exemption (cutoff 2026-09-11), fixed archive link handling, guarded ClientApp jobs
  in CI, standardized MCP docs to English.
