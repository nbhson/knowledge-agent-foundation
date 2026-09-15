# 🗂️ Issue Triage Loop

**Goal**: Sort noisy issues into an actionable backlog — suggest only, no auto-fix. Feeder for Daily Triage.

## Scheduling

**Recommended**:
- `/loop 2h–1d` (Grok, Claude Code)
- GitHub Action cron multiple times/day for issue-heavy repos

## Required Skills

- `loop-triage` — Reads issues, classifies severity/priority, detects duplicates/stale ones
- `issue-intake` — Handles issues that are too ambiguous: clarify or escalate, no guessing

## State

`issue-triage-state.md`:

```markdown
# Issue Triage State

Last run: 2026-06-09 10:00 UTC

## New Issues (last 24h)
- #1310 — bug: auth timeout — [High, actionable] — suggested: reproduce + fix
- #1311 — "app slow" — [Ambiguous] — loop-intake: needs more info, has asked via comment
- #1312 — duplicate of #1305 — [Dup] — suggested: close

## Needs Human
- #1298 — large feature request — needs a product decision
```

## How the Loop Runs (Typical Cycle)

1. Read new/updated open issues (last 24h).
2. For each issue:
   - **Classify**: bug / feature / question / duplicate / stale.
   - **Ambiguous** (not enough to verify "done"): the loop-intake skill asks for more or escalates — **no guessing**.
   - **Actionable**: write the suggested next action into state.
3. Update `issue-triage-state.md` — suggestions only, no auto-fix (L1 propose-only).
4. High-priority issues become a source for Daily Triage.

## Verification Strategy

- Level **L1 propose-only** — the loop only classifies and suggests, never edits code.
- The triage skill is **signal only** — no inventing architectural work.
- Every finding comes with evidence (issue link, classification reasoning).

## Human Handoff Points

- Feature requests that need a product decision
- Issues that remain unclear after asking
- High-priority issues with no owner
- Security issues (escalate immediately)

## Failure Modes & Mitigations

| Failure | Mitigation |
|---------|------------|
| Triage produces noise | Tighten skill rules; "Noise / Ignore" section |
| Misclassification | Evidence for every finding; periodic human review |
| Guessing at ambiguous issues | loop-intake: ask for more or escalate, no guessing |
| Overwhelmed by many issues | Prioritize by severity; cap processing per run |

## Cost Profile

| Scenario | Tokens/run | Notes |
|----------|------------|-------|
| No-op | ~5k | No new issues |
| Full triage | ~40k | Scan issues + classify |

**Cadence**: 2h–1d · **Tier**: low · **Suggested daily cap**: 100k tokens

```bash
npx @cobusgreyling/loop cost --pattern issue-triage --cadence 2h --level L1
```

## Success Metrics

- Time from "new issue" to "classified + suggested action"
- % of classifications that are correct (no re-triage needed)
- Reduction in "orphaned" backlog issues no one knows about

> **Natural pair**: Issue Triage (classify) → Daily Triage (prioritize) → action loops (execute). Low risk, an excellent first pair with Daily Triage.

---

*Back to [02 — Seven Production Patterns](../02-patterns/)*
