# Jira Ticket Investigate: [Ticket-ID] - [Summary]

## Meta

| Field              | Value                          |
| ------------------ | ------------------------------ |
| **Workflow Type**  | jira-ticket-investigate             |
| **Ticket/Feature** | [SP0168-XXXX]                  |
| **Date**           | [YYYY-MM-DD]                   |
| **Report File**    | `[filename].ctx.md`            |
| **SHA-256 Hash**   | `[auto-generated on save]`     |

## Jira Ticket

- **Ticket Key**: [SP0168-XXXX]
- **Ticket URL**: [https://jira.example.com/browse/SP0168-XXXX] *(required — must be filled)*
- **Status**: [Current Jira status]
- **Assignee**: [Assignee name]
- **Priority**: [P0/P1/P2/P3]
- **Components**: [Affected modules]

## Description & Requirements

[A concise summary of the ticket's requirements and business logic from the Jira ticket]

## Ticket Completeness (anatomy — mark MISSING explicitly)

- **Problem statement**: [present / MISSING]
- **Scope boundaries**: [present / MISSING]
- **Acceptance criteria**: [count, verbatim below]
- **Priority/deadline**: [present / MISSING]
- **Links**: [duplicates, blockers, designs — or none stated]

## Acceptance Criteria Checklist (scored)

| # | AC (verbatim) | Testable? | Evidence path / rewrite proposal |
|---|---------------|-----------|----------------------------------|
| 1 | [Criteria 1] | [testable via … / NON-TESTABLE → rewrite: …] | [spec name or manual steps / proposal] |
| 2 | [Criteria 2] | [...] | [...] |

## Technical Impact & Scope

- **Affected Components/Files**:
  - `[Path to file]` - Description of necessary changes
- **State & Reactivity**: [Required updates to RxJS Observables, BehaviorSubjects, NgRx Store, or services]
- **UI & Presentation**: [Angular components, custom templates, or SCSS classes required]

## Recommended Next Steps

- **Target Workflow**: [new-feature / bug-fix / refactor / code-review]
- **Action Items**:
  1. [ ] [Next action 1]
  2. [ ] [Next action 2]

## Blocking Questions (grouped by owner)

| Owner | Question | Why it blocks | Rewrite proposal |
|-------|----------|---------------|------------------|
| [product/dev/design] | [...] | [...] | [...] |

## Readiness Verdict (exactly one)

- **[Ready / Not ready]**: [one-line justification]
- [If Not ready: ticket must not enter Phase 2 until all blockers above are resolved]

## Contradictions & Risks

| # | Conflict (sources quoted) | Proposed resolution + owner |
|---|---------------------------|-----------------------------|
| 1 | [ticket field vs design/comment] | [...] |

- **Risks**: [complexity drivers — shared surface, cross-feature blast radius, missing design, migration involved]

## MCP Status

- **Jira**: Available / Manual fallback — [reason]
