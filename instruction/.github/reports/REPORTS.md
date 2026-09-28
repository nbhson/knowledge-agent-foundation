# Report Index / Manifest

> Auto-generated index of all reports in `.github/reports/`.
> Content-hash = first 12 hex chars of sha256 over file content EXCLUDING the `SHA-256 Hash` row.
> Re-generate after adding or deleting reports: `bash .github/scripts/validate-links.sh`
> Status `legacy-active` = created on or before 2026-09-11 without `## Meta`/hash/MCP;
> exempt from strict enforcement (WARN only). New reports must be `active` with full Meta.

| # | Workflow Type | Ticket/Feature | Date | File | SHA-256 (truncated) | Status |
|---|----------------|--------------------|------------|------|---------------------|----------|
| 1 | Bug Fix | TEST-SPECS | 2026-07-13 | [BUG-REPORT-TEST-SPECS-20260713-0809.ctx.md](archive/2026-07/BUG-REPORT-TEST-SPECS-20260713-0809.ctx.md) | 14d59551be1f | legacy-archived |
| 2 | Code Review | PR-2798 | 2026-09-04 | [CODE-REVIEW-PR-2798-20260904.ctx.md](CODE-REVIEW-PR-2798-20260904.ctx.md) | 2543aecab0fd | active |
| 19 | Refactor | GitHub framework alignment | 2026-09-11 | [ENGINEERING-REPORT-GITHUB-FRAMEWORK-20260911-0000.ctx.md](ENGINEERING-REPORT-GITHUB-FRAMEWORK-20260911-0000.ctx.md) | ceed046f5762 | active |
| 3 | Feature Delivery | STUDIES-HEADER-VISIBILITY | 2026-08-19 | [ENGINEERING-REPORT-STUDIES-HEADER-VISIBILITY-20260819-1617.md](ENGINEERING-REPORT-STUDIES-HEADER-VISIBILITY-20260819-1617.md) | 0da8cc1c1b0b | legacy-active |
| 4 | Feature Delivery | STUDIES-TRACKER-HEADER-COMPLETE-HIDING | 2026-08-19 | [ENGINEERING-REPORT-STUDIES-TRACKER-HEADER-COMPLETE-HIDING-20260819-1636.md](ENGINEERING-REPORT-STUDIES-TRACKER-HEADER-COMPLETE-HIDING-20260819-1636.md) | 1dcc4f8bcd89 | legacy-active |
| 5 | Feature Delivery | STUDIES-TRACKER-TABS | 2026-08-19 | [ENGINEERING-REPORT-STUDIES-TRACKER-TABS-20260819-1528.md](ENGINEERING-REPORT-STUDIES-TRACKER-TABS-20260819-1528.md) | b62f5203bc27 | legacy-active |
| 6 | Refactor | monitoring-component | 2026-07-01 | [REFACTOR-REPORT-monitoring-component-20260701.ctx.md](archive/2026-07/REFACTOR-REPORT-monitoring-component-20260701.ctx.md) | 429763848956 | legacy-archived |
| 7 | Refactor | ValidatorSupportUtil | 2026-07-01 | [REFACTOR-REPORT-ValidatorSupportUtil-20260701-1531.ctx.md](archive/2026-07/REFACTOR-REPORT-ValidatorSupportUtil-20260701-1531.ctx.md) | fa89cff4063b | legacy-archived |
| 8 | Unit Test | AdminModule | 2026-07-08 | [TEST-REPORT-AdminModule-20260708-1115.ctx.md](archive/2026-07/TEST-REPORT-AdminModule-20260708-1115.ctx.md) | 465353490b22 | legacy-archived |
| 9 | Unit Test | ConsentsUnitTests | 2026-07-09 | [TEST-REPORT-ConsentsUnitTests-20260709-2042.ctx.md](archive/2026-07/TEST-REPORT-ConsentsUnitTests-20260709-2042.ctx.md) | fe57d61f55b8 | legacy-archived |
| 10 | Unit Test | contract-ai | 2026-07-07 | [TEST-REPORT-contract-ai-20260707-1200.ctx.md](archive/2026-07/TEST-REPORT-contract-ai-20260707-1200.ctx.md) | d637b7e3ba3b | legacy-archived |
| 11 | Unit Test | contracts | 2026-07-09 | [TEST-REPORT-contracts-20260709-1530.ctx.md](archive/2026-07/TEST-REPORT-contracts-20260709-1530.ctx.md) | 04195d45cd34 | legacy-archived |
| 12 | Unit Test | FsaQcModule | 2026-07-09 | [TEST-REPORT-FsaQcModule-20260709-1444.ctx.md](archive/2026-07/TEST-REPORT-FsaQcModule-20260709-1444.ctx.md) | c6e7f9a7faa6 | legacy-archived |
| 13 | Unit Test | ServicesModule | 2026-07-08 | [TEST-REPORT-ServicesModule-20260708-1132.ctx.md](archive/2026-07/TEST-REPORT-ServicesModule-20260708-1132.ctx.md) | b83e17c60776 | legacy-archived |
| 14 | Unit Test | SharedModule | 2026-07-08 | [TEST-REPORT-SharedModule-20260708-1215.ctx.md](archive/2026-07/TEST-REPORT-SharedModule-20260708-1215.ctx.md) | e3c38000c4d3 | legacy-archived |
| 15 | Unit Test | SitesModule | 2026-07-08 | [TEST-REPORT-SitesModule-20260708-1753.ctx.md](archive/2026-07/TEST-REPORT-SitesModule-20260708-1753.ctx.md) | 45628b4d4f16 | legacy-archived |
| 16 | Unit Test | SmartDraft | 2026-07-07 | [TEST-REPORT-SmartDraft-20260707-1607.ctx.md](archive/2026-07/TEST-REPORT-SmartDraft-20260707-1607.ctx.md) | 789eff85ebcd | legacy-archived |
| 17 | Unit Test | StudiesModule | 2026-07-08 | [TEST-REPORT-StudiesModule-20260708-1735.ctx.md](archive/2026-07/TEST-REPORT-StudiesModule-20260708-1735.ctx.md) | 0c8a2844d5fc | legacy-archived |
| 18 | Unit Test | UtilityModule | 2026-07-08 | [TEST-REPORT-UtilityModule-20260708.ctx.md](archive/2026-07/TEST-REPORT-UtilityModule-20260708.ctx.md) | 7febc8900699 | legacy-archived |

---

### How to update this manifest

After adding or removing reports, validate (manifest rows are checked, archive status is maintained by post-merge/monthly job):

```bash
bash .github/scripts/validate-links.sh
```

Lifecycle: `active` on creation → `archived` when moved to `.github/reports/archive/YYYY-MM/` (post-merge or monthly schedule) → row removed when archived file older than 90 days is deleted. Legacy equivalents: `legacy-active` → `legacy-archived`.
