# TEST-REPORT-ConsentsUnitTests-20260709-2042

## Summary of Changes

A comprehensive refactoring and correction of the unit tests in the Consents module (`src/app/tracker/consents`) was performed under strict mode compilation. The changes fixed compiler and runtime issues across all 33 spec files, focusing on the following areas:
- **NullInjectorErrors & Missing Providers**: Fully mocked necessary routes, route params, navigation, and service providers (like `ActivatedRoute`, `Router`, `Location`, `ToastService`, `UserService`, `LoadingService`, `StepperService`, `CommonDialogService`, `PayloadService`).
- **Form Value Accessor Errors**: Bypassed `No value accessor for form control name` errors by declaring dummy mock components implementing Angular `ControlValueAccessor` (for `app-autocomplete-cdk-virtual-scroll` and `app-form-field-comment`) in tests utilizing `NO_ERRORS_SCHEMA`.
- **Cleanup and Tear Down Faults**: Rectified teardown exceptions in specs (e.g. `DocumentsComponent`, `ConsentTemplateComponent`) by aligning mock service returns with their actual void/Subscription patterns instead of returning incompatible Observables.
- **Obsolete Reference Removal**: Removed references to retired methods and variables (like retired click handlers and obsolete contact email listings).

## Files Modified

- [general.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/general/general.component.spec.ts)
- [documents.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/documents/documents.component.spec.ts)
- [contacts.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/contacts/contacts.component.spec.ts)
- [landing-page-header.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/components/landing-page-header/landing-page-header.component.spec.ts)
- [consents.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/consents.component.spec.ts)
- [consent-request-detail.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/consent-request-detail.component.spec.ts)
- [consent-review-detail.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-review-detail/consent-review-detail.component.spec.ts)
- [country-consent-template.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/country-consent-template/country-consent-template.component.spec.ts)
- [site-revision.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-review-detail/components/site-revision/site-revision.component.spec.ts)
- [site-consent-template.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/site-consent-template/site-consent-template.component.spec.ts)
- [consent-queue.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-queue/consent-queue.component.spec.ts)
- [icf-workload-overview-table.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/icf-assignments/components/icf-workload-overview-table/icf-workload-overview-table.component.spec.ts)
- [upload-consent.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/upload-consent/upload-consent.component.spec.ts)
- [step-three.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/request-process/components/step-three/step-three.component.spec.ts)
- [step-one.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/request-process/components/step-one/step-one.component.spec.ts)
- [step-four.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/request-process/components/step-four/step-four.component.spec.ts)
- [request-process.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/request-process/request-process.component.spec.ts)
- [step-two.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/request-process/components/step-two/step-two.component.spec.ts)
- [add-supplementary-icf.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/site-consent-template/add-supplementary-icf/add-supplementary-icf.component.spec.ts)
- [view-history.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/view-history/view-history.component.spec.ts)
- [section-consent-details.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/section-consent-details/section-consent-details.component.spec.ts)
- [sites-table.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/shared/sites-table/sites-table.component.spec.ts)
- [consent-template.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/shared/consent-template/consent-template.component.spec.ts)
- [update-consent-template.component.spec.ts](file:///d:/bitbucket/horizon2/horizon2-ui/ClientApp/src/app/tracker/consents/modules/consent-request-detail/components/shared/update-consent-template/update-consent-template.component.spec.ts)

## Verification & Validation Results

- **Automated Tests**: Ran `npm run test -- src/app/tracker/consents` from `ClientApp/`. All 33 test suites (45 tests total) successfully compiled and passed:
  ```
  Test Suites: 33 passed, 33 total
  Tests:       45 passed, 45 total
  Snapshots:   0 total
  Time:        39.369 s
  ```
- **Compilation Check**: The workspace compiles without errors when running unit test workflows. Mocks are aligned with class interfaces in strict mode.

## Risks & Mitigation

No production source files (`.ts` or `.html` or `.scss`) were modified during this task. All changes were restricted entirely to test files (`.spec.ts`). Therefore, there is zero risk of regression or breaking backward compatibility in the production application.

## Pull Request

- Link: N/A
