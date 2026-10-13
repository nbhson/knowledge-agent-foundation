# Bug Report

## Header
- Workflow: Bug Fix
- Scope: Failing unit test specs (3 files)
- Timestamp: 2026-07-13 08:09

## Steps to Reproduce
1. Run `npm test -- src/app/services/auth/user/user.service.spec.ts src/app/tracker/contracts/modules/smart-draft/smart-draft.component.spec.ts src/app/tracker/contracts/modules/contract-ai/components/contract-ai-clause/contract-ai-clause-feedback/contract-ai-clause-feedback.component.spec.ts`.
2. Observe TypeScript compile failures in all 3 suites.

## Expected vs. Actual Result
- Expected: all 3 target suites compile and pass.
- Actual: constructor dependency mismatch in 2 specs, incorrect mock variable names and missing imports in 1 spec.

## Root Cause Analysis
- `src/app/services/auth/user/user.service.spec.ts`: `UserService` constructor now requires `ConfigService` as the third dependency.
- `src/app/tracker/contracts/modules/smart-draft/smart-draft.component.spec.ts`: `SmartDraftComponent` constructor now requires `DocumentNotifyService` as the sixth dependency.
- `src/app/tracker/contracts/modules/contract-ai/components/contract-ai-clause/contract-ai-clause-feedback/contract-ai-clause-feedback.component.spec.ts`:
  - missing imports for `FeedbackStatus` and `LOCAL_STORAGE_CONTRACT_AI_FEEDBACK_QUESTION_KEY`.
  - assertions referenced undefined mocks (`loadingServiceMock`, `contractAIClauseServiceMock`, etc.) instead of declared mock variables.

## Proposed Fix
- Updated `user.service.spec.ts`:
  - added `configServiceMock`.
  - passed third constructor argument: `new UserService(userApiServiceMock, userSessionApiServiceMock, configServiceMock)`.
- Updated `smart-draft.component.spec.ts`:
  - added a sixth constructor mock with `startPolling` for `DocumentNotifyService`.
- Updated `contract-ai-clause-feedback.component.spec.ts`:
  - imported `FeedbackStatus` and `LOCAL_STORAGE_CONTRACT_AI_FEEDBACK_QUESTION_KEY`.
  - replaced incorrect assertion mock names with declared variables (`mockLoadingService`, `mockContractAIClauseService`, `mockLocalStorageService`, `mockToastService`).

## Files Modified
- `src/app/services/auth/user/user.service.spec.ts`
- `src/app/tracker/contracts/modules/smart-draft/smart-draft.component.spec.ts`
- `src/app/tracker/contracts/modules/contract-ai/components/contract-ai-clause/contract-ai-clause-feedback/contract-ai-clause-feedback.component.spec.ts`

## Verification
- Targeted test command:
  - `npm test -- src/app/services/auth/user/user.service.spec.ts src/app/tracker/contracts/modules/smart-draft/smart-draft.component.spec.ts src/app/tracker/contracts/modules/contract-ai/components/contract-ai-clause/contract-ai-clause-feedback/contract-ai-clause-feedback.component.spec.ts`
  - Result: 3 passed, 3 total; 11 passed tests.
- Build command:
  - `npm run build`
  - Result: success. Build hash `57033ae6c6bdd18e`.
- Lint command:
  - `npm run lint`
  - Result: failed due to large pre-existing workspace lint issues (including missing `sonar/no-duplicate-string` rule), not introduced by this change set.

## Risk and Backward Compatibility
- Risk: low. Changes are confined to spec files and test setup mocks.
- Backward compatibility: no production runtime code changed.
