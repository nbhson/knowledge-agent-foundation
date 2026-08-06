---
name: jira-ticket-review
description: Step-by-step workflow for analyzing Jira tickets, extracting requirements and acceptance criteria, assessing technical impact, and producing a structured review in the Horizon 2 UI project.
---

# Workflow: Jira Ticket Review

This document outlines the workflow for reviewing a Jira ticket before implementation begins, ensuring scope, acceptance criteria, and technical impact are well understood in the Horizon 2 UI application.

---

## Required Steps & Phases

1. **Read & Understand the Ticket**:
   - Identify the ticket key (e.g., `SP0168-1234`), summary, status, assignee, priority, and affected components.
   - Read the full description and any linked subtasks, comments, or attachments to capture the business logic.

2. **Extract Requirements & Acceptance Criteria**:
   - Translate the ticket description into concrete, testable requirements.
   - List all acceptance criteria explicitly; flag any missing, ambiguous, or contradictory criteria.

3. **Assess Technical Impact & Scope**:
   - Map affected modules, components, services, DTOs, and SCSS files using the [Core Engineering Guidelines](../../knowledge/core-engineering-guidelines.md).
   - Note required state management changes (RxJS Observables, BehaviorSubjects, NgRx Store/Effects).
   - Identify reusable constants, models, shared components, and services to avoid duplicate implementation.
   - Estimate complexity and risk, including dependencies on other in-flight tickets.

4. **Recommend Next Steps**:
   - Determine the target workflow: **Feature Delivery**, **Bug Fix**, **Refactor**, or **Code Review**.
   - Produce actionable action items with acceptance criteria mapping.
   - For non-trivial tickets, recommend creating an `implementation_plan.md` (see Technical Design template) and pausing for developer approval before coding.

5. **Report**:
   - Complete the `jira-ticket-review.md` template from `/.github/report-templates/`.
   - Save the report to `.github/reports/` with the naming convention: `JIRA-REVIEW-[TICKET-ID]-[DATE]-[TIME].ctx.md`.
   - Reference the [Report Generation Skill](../report-generation/SKILL.md) for formatting details.

---

## Deliverables

- **Clarified Requirements**: A concise summary of the ticket's business logic.
- **Acceptance Criteria Checklist**: A reviewable, testable criteria list.
- **Technical Impact Assessment**: Affected files, state management, and UI changes.
- **Recommended Workflow & Action Items**: Clear next steps for the developer.