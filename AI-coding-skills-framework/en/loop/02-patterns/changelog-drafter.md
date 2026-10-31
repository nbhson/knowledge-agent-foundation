# 📝 Changelog Drafter Loop

**Goal**: Automatically draft release notes from merge history — reducing the "what's in the upcoming release?" headache. (Release notes = the summary of what changed in a version; merge history = the record of merged PRs and commits.)

## Scheduling

Signpost: this section answers "when does the loop run?" — the heartbeat that turns it from a script into a loop.

**Recommended**:
- `/loop 1d` during release prep
- Manual or tag-triggered when preparing a release (tag = a named marker on a specific commit, e.g. `v1.4.0`)
- GitHub Action `changelog-drafter.yml` (e.g. every Monday, opens a release-prep issue)

> **One-line summary:** Run it daily during release prep, or trigger it manually or on a new tag.

## Required Skills

Signpost: this section lists the knowledge the loop needs loaded — skills are files of instructions the agent reads each run.

- `changelog-draft` — Reads merge history (commits, PRs, issues), groups by category, produces a draft
- Project conventions skill — Knows how your project categorizes changes (breaking/feature/fix) (breaking = changes that force users to update their code)

> **One-line summary:** Two skills: one reads merge history and drafts, the other knows your project's category rules.

## State

Signpost: this section defines the loop's memory — the file it updates every run so the next run (and you) know where things stand.

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

> **One-line summary:** The state file records the last run, counts per category, and where the draft sits.

## How the Loop Runs (Typical Cycle)

Signpost: this is the step-by-step walk of one run, from "find the last release" to "a human approves the draft".

1. Identify the last milestone (last tag / last release).
2. Collect merged PRs + commits since that point.
3. Group by category (breaking, feature, fix, docs, deps).
4. Draft `RELEASE_NOTES_DRAFT.md` (or a section for the GitHub release).
5. **A human approves before publishing or updating the CHANGELOG** — no auto-publish.

> **One-line summary:** Collect merges since the last tag, group them, draft the notes — and always stop for human approval.

## Verification Strategy

Signpost: this section explains how the output is checked before anyone trusts it.

- Level **L1 draft only** — human review before publishing. (L1 = report-only autonomy; the loop never acts on its own.)
- The draft must be traceable: every entry points to a PR/issue. (Traceable = you can click through to the source of every claim.)
- **No auto-publish** — this is a read-mostly pattern, low risk, but never self-published.

> **One-line summary:** L1 draft-only with traceable entries; a human gate before anything is published.

## Human Handoff Points

Signpost: these are the moments a person must step in — the loop stops and waits.

- Approving the draft before publishing/updating the CHANGELOG
- Deciding the version bump (major/minor/patch) (major/minor/patch = the three numbers in a version like 2.3.1, from most to least breaking)
- Highlighting breaking changes

> **One-line summary:** Humans approve the draft, pick the version bump, and confirm what counts as breaking.

## Failure Modes & Mitigations

How to read it: left column = what can go wrong; right column = the defense against it. For instance, "draft missing entries" is caught by comparing the count of merged PRs against the number of draft entries.

| Failure | Mitigation |
|---------|------------|
| Draft missing entries | Verify the count of merged PRs vs draft entries |
| Misclassification (breaking vs fix) | Human review; clear conventions skill |
| Accidental publish | No auto-publish; human gate mandatory |

> **One-line summary:** Count checks catch missing entries; the mandatory human gate catches everything else.

## Cost Profile

How to read it: each row is a scenario and the tokens (AI compute units) one run costs. "No-op" = a run that finds nothing new and exits early — that's why it's cheap.

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| Draft | ~30k | Read merge history + categorize |
| No-op | ~3k | No new commits |

**Cadence**: 1d or tag · **Tier**: low · **Suggested daily cap**: 50k tokens

> 📄 **Example code:** [`examples/01-cost-profile.sh`](examples/01-cost-profile.sh)

> **One-line summary:** ~30k tokens to draft, ~3k when there's nothing new — capped at 50k/day.

## Success Metrics

Signpost: these numbers tell you whether the loop is actually earning its keep.

- Time from "release prep" to "draft ready"
- % of draft entries that are correct (no rework)
- Reduction in "what's in this release?" questions

> **One-line summary:** Success = faster draft-ready time and fewer corrected entries.

> **An excellent low-risk companion** to Post-Merge Cleanup — runs safely alongside other loops.

> **One-line summary:** A cheap, read-only loop that drafts release notes from merge history and never publishes without a human — the safest first companion loop.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*