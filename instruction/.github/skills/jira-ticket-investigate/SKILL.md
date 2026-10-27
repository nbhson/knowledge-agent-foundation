---
name: jira-ticket-investigate
description: Step-by-step workflow for analyzing Jira tickets, extracting requirements and acceptance criteria, assessing technical impact, and producing a structured review in the Horizon 2 UI project.
argument-hint: '<Jira-key>'
user-invocable: false
---

# Workflow: Jira Ticket Investigate

This document outlines the workflow for reviewing a Jira ticket before implementation begins, ensuring scope, acceptance criteria, and technical impact are well understood in the Horizon 2 UI application.

**Workflow Note**: This is an **analysis-only workflow**. Only Phase 1 (Understand) and Phase 5 (Report) are executed. Phases 2-4 (Planning, Execution, Validation) are skipped entirely — no code changes, no build/test gates, no PR creation.

---

## Entry Criteria

- Ticket key available (e.g., `SP0168-1234`); ticket fetched via Jira MCP or pasted as dev-provided summary (key, description, AC list, priority, status).
- No task ever blocks on a missing MCP connection — one fallback request, then proceed manual.

## Required Steps & Phases

1. **Read & Understand the Ticket**:
   - Identify the ticket key, summary, status, assignee, priority, and affected components.
   - Read the full description and any linked subtasks, comments, or attachments to capture the business logic.
   - **Ticket anatomy checklist** — record each explicitly, or mark MISSING:
     - Problem statement (what is wrong / what is wanted, for whom).
     - Scope boundaries (what is explicitly out of scope, affected vs unaffected areas).
     - Acceptance criteria (list verbatim; never paraphrase away detail).
     - Priority/urgency and any deadline or release-train constraint.
     - Links: duplicates, blockers/blocked-by, related tickets, designs/specs.
     - Environment/route context for UI tickets (page, tab, role).

2. **Extract Requirements & Acceptance Criteria**:
   - Translate the ticket description into concrete, testable requirements.
   - List all acceptance criteria explicitly; flag any missing, ambiguous, or contradictory criteria.
   - Score each AC: **testable** (verifiable by test/manual check with evidence path) or **non-testable** (rewrite proposal included). Non-testable ACs are returned as blocking questions — the ticket is not implementation-ready until they are rewritten.
   - **AC quality rubric** — fail an AC (with rewrite proposal) when it:
     - Uses unmeasurable adjectives without thresholds ("fast", "user-friendly", "stable") → propose the metric + threshold + where observed.
     - Describes internals instead of outcomes ("refactor the service") without an observable result → propose the observable behavior + regression guard.
     - Omits states (loading/error/empty/permission-denied) for a UI change → propose one AC per missing state.
     - Hides scope (migration, backfill, permission, notification) → split into its own AC or ticket.
     - Contradicts another AC or the linked design → file under contradictions with both sources quoted.

3. **Assess Technical Impact & Scope**:
   - Map affected modules, components, services, DTOs, and SCSS files using [Tech Stack](../../knowledge/tech-stack.md) and [Project Structure](../../knowledge/project-structure.md). Method: keyword search over routes (`app-routing`), store slices, `src/api/<area>/` siblings, and shared components — record the search terms used so the mapping is reproducible.
   - Note required state management changes (RxJS Observables, BehaviorSubjects, NgRx Store/Effects).
   - Identify reusable constants, models, shared components, and services to avoid duplicate implementation.
   - Pre-flag the owning domain folder for the future implementation (list sibling `src/api/<area>/` folders to find which domain already owns the concept) and any object shapes that will need owner `dto/`/`models/` interfaces instead of anonymous inline types (see [Angular Architecture §6](../angular-architecture/SKILL.md)).
   - Estimate complexity and risk, including dependencies on other in-flight tickets. Name the risk factors explicitly: shared-surface touch (store/services/routes/guards), cross-feature blast radius, ambiguous AC, missing design, data migration involved.

4. **Recommend Next Steps**:
   - Determine the target workflow using this decision guide:
     - Observable misbehavior on an existing path → **Bug Fix** (needs repro steps; if absent, request them as blockers).
     - New observable capability or UI contract → **New Feature**.
     - Same behavior, better structure (smells from [Angular Architecture §6](../angular-architecture/SKILL.md)) → **Refactor** (needs baseline plan).
     - Ticket unclear on all three → stays **Not ready**, do not guess the workflow.
   - Produce actionable action items with acceptance criteria mapping.
   - For non-trivial tickets, recommend creating an `implementation_plan.md` from `reports/templates/implementation-plan.md` when the Phase 2 threshold table (`.github/phases/phase-2-planning.md`) requires it (shared surface, security-sensitive, or multi-module scope), and pausing for developer approval before coding.

5. **Report**:
   - Complete the `jira-ticket-investigate.md` template from `.github/reports/templates/`.
   - Save the report to `.github/reports/jira-ticket-investigate/` with the naming convention: `JIRA-INVESTIGATE-[TICKET-ID]-[DATE]-[TIME].ctx.md`.
   - Reference the [Report Generation Skill](../report-generation/SKILL.md) for formatting details.

---

## Blocking Questions Template

Send back to the ticket owner grouped by owner, one row per question:

```text
[Owner] Q: <precise question> | Why it blocks: <what cannot be planned/built without it>
Rewrite proposal: <concrete AC/wording to unblock>
```

- Questions without a rewrite proposal are complaints, not reviews — always propose.
- Contradictions quote both sources verbatim with their locations (ticket field/comment/design section).

---

## Deliverables

- **Clarified Requirements**: A concise summary of the ticket's business logic.
- **Acceptance Criteria Checklist**: A reviewable, testable criteria list (each AC scored testable/non-testable with evidence path or rewrite).
- **Technical Impact Assessment**: Affected files, state management, and UI changes, with the search method recorded.
- **Recommended Workflow & Action Items**: Clear next steps for the developer.

## Readiness Verdict (enterprise)

End every ticket investigation with exactly one verdict:

- **Ready**: scope bounded, every AC testable, no blocking contradictions, target workflow + impacted modules identified.
- **Not ready**: list blocking questions grouped by owner (product/dev/design), each with a rewrite proposal for non-testable ACs. The ticket must not enter Phase 2 until all blockers are resolved.

## AC Testability Bar

- Each AC gets: **testable** (verifiable by test/manual check with evidence path: spec name or manual steps + observable result) or **non-testable** (with a concrete rewrite proposal).
- Flag: missing edge cases (empty/null/error states), unmeasurable adjectives ("fast", "user-friendly" without thresholds), and hidden scope (migrations, backfills, permissions) as blockers.
