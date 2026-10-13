---
name: 'Report integrity (hash + manifest)'
description: 'Use when creating or editing Phase 5 report files.'
applyTo: '**/*.ctx.md'
---

# Reports (hash-stable, manifest-synced)

- Fill `## Meta` (Workflow Type, Ticket/Feature, Date, Report File) + full Jira ticket URL before archiving.
- Hash covers content EXCLUDING the hash row: `grep -v 'SHA-256 Hash' <file> | sha256sum | cut -c1-12` (macOS: `shasum -a 256`). Insert first 12 hex chars into `SHA-256 Hash`.
- Any post-hash edit (even adding the PR link) invalidates the hash: recompute + update the `REPORTS.md` row together, never one without the other.
- One file → exactly one `REPORTS.md` row; updates replace the row, never append a duplicate. Verify with `npm run reports:check`.
- Details: `.github/skills/libs/shared/report-generation/SKILL.md` (canonical template + filename table).
