# 📝 Changelog Drafter Loop

**Goal**: Automatically draft release notes from merge history — reducing the "what's in the upcoming release?" headache.

## Scheduling

**Recommended**:
- `/loop 1d` during release prep
- Manual or tag-triggered when preparing a release
- GitHub Action `changelog-drafter.yml` (e.g. every Monday, opens a release-prep issue)

## Required Skills

- `changelog-draft` — Reads merge history (commits, PRs, issues), groups by category, produces a draft
- Project conventions skill — Knows how your project categorizes changes (breaking/feature/fix)

## State

`changelog-drafter-state.md` or a section in `STATE.md`:

```markdown
# Changelog Drafter State

Last run: 2026-06-09 09:00 UTC

## Since last tag: v1.4.0
- Merged PRs: 42
- Breaking: 2
- Features: 15
- Fixes: 20
- Draft: RELEASE_NOTES_DRAFT.md (awaiting human approval)
```

## How the Loop Runs (Typical Cycle)

1. Identify the last milestone (last tag / last release).
2. Collect merged PRs + commits since that point.
3. Group by category (breaking, feature, fix, docs, deps).
4. Draft `RELEASE_NOTES_DRAFT.md` (or a section for the GitHub release).
5. **A human approves before publishing or updating the CHANGELOG** — no auto-publish.

## Verification Strategy

- Level **L1 draft only** — human review before publishing.
- The draft must be traceable: every entry points to a PR/issue.
- **No auto-publish** — this is a read-mostly pattern, low risk, but never self-published.

## Human Handoff Points

- Approving the draft before publishing/updating the CHANGELOG
- Deciding the version bump (major/minor/patch)
- Highlighting breaking changes

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Draft missing entries | Verify the count of merged PRs vs draft entries |
| Misclassification (breaking vs fix) | Human review; clear conventions skill |
| Accidental publish | No auto-publish; human gate mandatory |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| Draft | ~30k | Read merge history + categorize |
| No-op | ~3k | No new commits |

**Cadence**: 1d or tag · **Tier**: low · **Suggested daily cap**: 50k tokens

```bash
npx @cobusgreyling/loop cost --pattern changelog-drafter --cadence 1d --level L1
```

## Success Metrics

- Time from "release prep" to "draft ready"
- % of draft entries that are correct (no rework)
- Reduction in "what's in this release?" questions

> **An excellent low-risk companion** to Post-Merge Cleanup — runs safely alongside other loops.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
