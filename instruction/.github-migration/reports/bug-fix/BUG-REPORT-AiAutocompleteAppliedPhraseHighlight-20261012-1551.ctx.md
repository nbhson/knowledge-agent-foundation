# Bug Report: Applied Multi-Word Suggestion Highlight

## Meta

| Field              | Value                                                                  |
| ------------------ | ---------------------------------------------------------------------- |
| **Workflow Type**  | bug-fix                                                                |
| **Ticket/Feature** | ai-autocomplete applied phrase highlight                               |
| **Date**           | 2026-10-12                                                             |
| **Report File**    | `BUG-REPORT-AiAutocompleteAppliedPhraseHighlight-20261012-1551.ctx.md` |
| **SHA-256 Hash**   | `271b3c9daa2e`                                                         |

## Jira Ticket

- **Ticket Key**: Not supplied; developer reproduction is the source of truth.
- **Ticket URL**: N/A — no ticket key was supplied.
- **Status**: N/A
- **Assignee**: N/A
- **Priority**: N/A
- **Components**: `projects/ai-autocomplete`

## Steps to Reproduce

1. Enter a query and choose two multi-word values from the suggestion dropdown.
2. Press Enter to apply both values into the input.
3. Remove either one of the two applied values, including its comma separator, and leave the caret at the end of the remaining value.
4. Reproduce the follow-up case: choose `Screening Consent`, `Re-consent`, and `Parental Permission Form`; edit `Re-consent` to `Re`, then choose `Parental Permission Form` again while the caret remains at the edited word. The input contains `show Screening Consent, Parental Permission Form, Parental Permission Form`.
5. Apply `Screening Consent` and `Parental Permission Form`, then move the caret from the latter phrase into `Screening Consent`.

## Expected vs. Actual Result

- **Expected**: Highlight the full phrase when its text exactly matches surviving applied-selection metadata. When it does not match, highlight only the word at the caret. Suggestions also follow the focused phrase, including when focus moves to an earlier applied value without editing the query.
- **Actual**: Applying a duplicate before an unchanged phrase discarded its metadata. Separately, moving focus to an earlier applied phrase left suggestions scoped to the previous terminal fragment.

## Root Cause Analysis

The original issue tracked all values inserted by one Apply action as a single `AppliedTextSelection`; removing one value discarded tracking for every value. Per-item ranges fixed that case, but a follow-up exposed metadata loss when applying a duplicate before an unchanged phrase. Range remapping treated the generated terminal space as part of the edit, so it could not preserve the unchanged suffix phrase. The caret could also be clamped against the old input value when applying longer text before Angular refreshed the `[value]` binding.

The focus-suggestion issue had two related causes: `onCaretPosition` suppressed the legacy query event for applied ranges, and the API request contained only the full query string, so the backend could only match its terminal fragment. The focused range was not included in the request context; suggestions for an earlier phrase therefore remained stale. The input value is now synchronized before setting the caret, and a separate context event carries the full query plus focused range. Consent AI requests the focused fragment and maps the response offsets back to the full query. A follow-up `show re` case exposed that the three-character minimum was incorrectly checked against the two-character focused fragment instead of the full query; this suppressed an otherwise valid request.

## Proposed Fix

- Track an applied range for each inserted suggestion instead of one range for the comma-joined string.
- Remap each range independently after input edits and retain only ranges whose exact text still exists in the updated query.
- Treat the caret immediately after one generated trailing space as part of the applied phrase only when that space is at the end of the input; normal navigation into a following word still selects that word.
- During apply, preserve exact metadata for unaffected existing phrases, remapping against the content before the generated trailing space, and add metadata for newly inserted items.
- Resolve the active range from the surviving applied ranges before falling back to the word at the caret.
- Emit a separate focused-query context while preserving the existing full-query `queryChanged` output; request suggestions for the focused fragment and adapt returned offsets to the full input.
- Apply the three-character minimum to the full query, while allowing a shorter focused fragment when the complete query meets the threshold.

## Acceptance Criteria Traceability

| #   | Acceptance Criterion                                                                                                | Status | Evidence                                                                                                        |
| --- | ------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------- |
| 1   | Removing either of two applied values keeps the remaining multi-word value highlighted as a phrase.                 | ✅ Met | `ai-autocomplete.component.spec.ts`: parameterized removal of both the first and second value; both cases pass. |
| 2   | Unchanged applied ranges survive edits to sibling values; modified ranges are dropped.                              | ✅ Met | `ai-autocomplete-text-range.util.spec.ts`: remaps the surviving item and discards the removed selection.        |
| 3   | Reselecting a repeated multi-word value keeps the full phrase highlighted with the caret after the generated space. | ✅ Met | `ai-autocomplete.component.spec.ts`: repeated-value case passes; expected full phrase, not final word.          |
| 4   | Moving the caret to a following word does not keep the prior applied phrase active.                                 | ✅ Met | `ai-autocomplete-text-range.util.spec.ts`: caret at the next word resolves that word range.                     |
| 5   | Existing autocomplete caret/highlight behaviors remain covered.                                                     | ✅ Met | Full library suite: 4 suites, 39 tests passed.                                                                  |

**Follow-up acceptance criterion:** Highlight the full phrase only while its exact text matches surviving applied-selection metadata; otherwise highlight the focused word. ✅ Met — the component regression covers preserving an unchanged duplicate phrase and the existing edit regression verifies word fallback.

**Focus-suggestion acceptance criterion:** Suggestions must be based on the applied phrase currently under the caret, even if that phrase is not terminal in the query. ✅ Met — component context events and service response mapping are covered by focused phrase and fragment-query tests.

**Short-fragment acceptance criterion:** A short focused fragment such as `re` still triggers suggestions when the full query `show re` meets the three-character minimum. ✅ Met — `requests a short focused fragment when the full query meets the minimum length` verifies the API call and mapped response.

## Contradiction Resolution

No blocking contradictions were identified. The developer confirmed full-phrase highlighting only for exact applied metadata and reported that suggestions must match the phrase currently under focus.

| #   | Contradiction / Ambiguity          | Frozen Decision                                                                               | Applied Status | Evidence                                                                |
| --- | ---------------------------------- | --------------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------- |
| 1   | Which applied value may be removed | Preserve the full phrase for whichever applied value remains, whether it was first or second. | ✅ Applied     | Parameterized component regression test covers both removal directions. |

## MCP Status

- **Jira**: Manual fallback — no ticket key or Jira connection was supplied; the developer provided the reproduction.
- **Figma**: Manual fallback — this is a behavior fix with no visual redesign; the attached screenshot supplied the observed state.
- **Bitbucket**: Manual fallback — no PR was requested or created.

## Files Modified

- `projects/ai-autocomplete/src/lib/components/ai-autocomplete/ai-autocomplete.component.ts` — stores per-item applied ranges, preserves unaffected metadata through apply, and resolves ranges during input/caret updates.
- `projects/ai-autocomplete/src/lib/models/ai-autocomplete.models.ts` — defines the focused query context event payload.
- `projects/ai-autocomplete/README.md` — documents the new context event and range response contract.
- `projects/ai-autocomplete/src/lib/utils/ai-autocomplete-text-range.util.ts` — finds and remaps multiple applied ranges independently.
- `projects/ai-autocomplete/src/lib/components/ai-autocomplete/ai-autocomplete.component.spec.ts` — covers removal of either applied value, duplicate insertion before an existing phrase, word fallback, and context changes between focused phrases.
- `projects/ai-autocomplete/src/lib/utils/ai-autocomplete-text-range.util.spec.ts` — verifies unaffected selection remapping.
- `src/app/tracker/smartdraft/consent-ai/consent-ai.component.html` and `.ts` — route focused range events to the feature service.
- `src/app/tracker/smartdraft/consent-ai/consent-ai.component.spec.ts` — verifies focused-fragment requests from the host.
- `src/app/tracker/smartdraft/consent-ai/services/consent-ai.service.ts` and `.spec.ts` — request the focused fragment and rebase response offsets to the full query.
- `src/api/tracker/smart-draft/consent-ai/consent-ai.api.spec.ts` — verifies the development mock returns `Re-consent` for fragment `re`.

## Verification & Validation Results

- **Automated Tests**: Autocomplete library, Consent AI host/service, and API mock suites — 7 suites and 67 tests passed. The library contributes 4 suites and 39 tests.
- **Focused Regression**: Component tests verify context updates when moving between applied phrases; service tests verify fragment requests, full-query range mapping, and the `show re` threshold boundary; API mock test confirms `Re-consent` is returned for `re`.
- **Lint**: Scoped ESLint passed with the unavailable `sonar/no-duplicate-string` rule disabled. The host component lint check also disabled its pre-existing relative-import restriction; the `ConsentAiService` import was unchanged.
- **Formatting**: Scoped Prettier check passed for all changed source, tests, and README files.
- **Compilation Check**: `npm run build` passed for the library and Angular application; application build hash `5fc414c28d7fd8fa`.
- **Diff Hygiene**: `git diff --check` passed for the changed files.
- **Manual Check**: Not performed. The earlier server attempt on port 4200 exited 1. The retry on port 4201 failed Angular serve compilation with unresolved `ai-autocomplete` and unknown `mat-icon` template errors; the HTTP readiness check timed out. The supplied behavior is covered by component, service, and mock regressions.
- **Full Jest**: Not run for this isolated library behavior change; focused library coverage and full app compilation passed.

## Risks & Mitigation

A selection is preserved only while its exact text remains in the query. Edits inside a suggestion intentionally drop that suggestion's applied-range state while leaving unaffected ranges tracked through subsequent applies. Suggestions are now requested using the active fragment and mapped back into the full query; the backend request schema remains unchanged. The generated trailing-space allowance is limited to the end of the input so moving the caret to following text remains normal word selection.

## Pull Request

- **Branch**: Not created.
- **Link**: Not created.
