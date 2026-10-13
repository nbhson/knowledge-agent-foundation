# Engineering Report: Studies Module Unit Tests Fixes (Strict Mode)

## Summary of Changes

Resolved all unit test failures and TypeScript strict compiler issues across all 48 unit test spec files inside the `src/app/tracker/studies` directory. Key fixes included:
- **Mock Service and Provider Alignments**: Added missing providers and mocks for `UserService` and various permissions injection tokens (`STUDY_TRACKER_TOKEN`, `ADMIN_TOKEN`, etc.) to resolve `NullInjectorError` issues caused by the `PermissionDirective`.
- **Test Assertion Updates**: Updated the expected result for `PlanDetailsComponent` tests to align with the refactored production component behavior (where `list` is no longer populated under basic info, and instead new properties like `planDetailBasicInfo` are set).
- **TypeScript Strict Type Compliance**: Added missing required properties (`firstPlannedSiteSelectionDate`, `sites25PercentSelectedDate`, `region`, `fsaStatus`, etc.) to shared mock constant objects like `mockBaselinePlanDetails` and `mockStudyTrackerDetailData`.
- **JSDOM and Global Environments Mocks**: Configured missing global dependencies like `ResizeObserver` and mocked `MomentService` methods properly to prevent runtime crashes.

## Files Modified

- [study-tracker.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/shared/test-data/tracker/study-tracker.ts)
- [baseline-planning-detail.constant.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/api/shared/test-data/tracker/studies/baseline-planning/baseline-planning-detail.constant.ts)
- [insurance-tracking-table.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-conduct-tab/components/insurance-tracking-table/insurance-tracking-table.component.spec.ts)
- [aging-reports.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-summary-tab/aging-reports/aging-reports.component.spec.ts)
- [country-detail-filter.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/country-detail/components/country-detail-filter/country-detail-filter.component.spec.ts)
- [update-global-regulatory-partner.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/global-regulatory-partner-review/components/update-global-regulatory-partner/update-global-regulatory-partner.component.spec.ts)
- [reactivate-license-tracking.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-conduct-tab/components/reactivate-license-tracking/reactivate-license-tracking.component.spec.ts)
- [add-update-baseline-planning.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/baseline-planning/components/add-update-baseline-planning/add-update-baseline-planning.component.spec.ts)
- [ssu-comment-or-ceo-review.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/ssu-comment-or-ceo-review/ssu-comment-or-ceo-review.component.spec.ts)
- [fsa-program-manager.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/fsa-program-manager/fsa-program-manager.component.spec.ts)
- [engage-details.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/engage-details/engage-details.component.spec.ts)
- [director-review.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/director-review/director-review.component.spec.ts)
- [by-country.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-summary-tab/by-country/by-country.component.spec.ts)
- [metrics-table.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/financials/components/metrics-table/metrics-table.component.spec.ts)
- [financials.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/financials/financials.component.spec.ts)
- [study-detail.service.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/services/study-detail.service.spec.ts)
- [studies.service.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/services/studies.service.spec.ts)
- [baseline-planning.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/baseline-planning/baseline-planning.component.spec.ts)
- [allocation-and-maintenance-ageing.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/country-detail/components/allocation-and-maintenance-ageing/allocation-and-maintenance-ageing.component.spec.ts)
- [license-tracking-table.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-conduct-tab/components/license-tracking-table/license-tracking-table.component.spec.ts)
- [plan-details.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/studies/modules/study-detail/study-tab/baseline-planning/components/plan-details/plan-details.component.spec.ts)

## Verification & Validation Results

- **Automated Tests**:
  Command run:
  ```bash
  npx jest src/app/tracker/studies
  ```
  Result: **48 / 48 test suites passed successfully** (182 / 182 tests passed in 89.458 s).

- **Compilation Check**:
  Command run:
  ```bash
  npm run build
  ```
  Result: **Built successfully** (Hash: 784a6f13992b920a in 61339ms).

- **Manual Check**:
  Verified formatting check:
  ```bash
  npx prettier --write <modified_files>
  ```
  Result: Formatting runs cleanly with no errors.

## Risks & Mitigation

- **Risks**: None. All code modifications are strictly isolated to test specification files (`*.spec.ts`) and shared test mock data objects (`study-tracker.ts`, `baseline-planning-detail.constant.ts`). Production application code is untouched and safe.
- **Strict Mode Alignment**: All mock dependencies and providers have been strictly aligned with their actual service declarations and types inside the project.

## Pull Request

- Link: N/A (Local validation completed successfully)
