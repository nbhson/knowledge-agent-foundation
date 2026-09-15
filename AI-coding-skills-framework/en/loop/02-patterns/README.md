# 🧩 02. Seven Production Patterns

> **📌 Core Concept**
>
> **Definition:** A "production pattern" is **a proven loop template** — a ready-made frame including the scheduler, skills, state, verification approach, and human handoff. Instead of inventing a loop from scratch, you pick a suitable pattern and scaffold it with `loop init`.
> **Analogy:** Like **dishes on a restaurant menu** — you don't have to reinvent the recipe; the chef (the loop-engineering repo) has tested them, served real customers, and noted "this one is spicy (high cost), this one is safe for beginners (L1)". Your job is to pick the dishes that fit your taste.
> **Why it matters:** These patterns have been "dogfooded" on a real repo — meaning every detail (cadence, token cost, failure mode) is experience bought with real money, not theory. You reuse the lessons, avoiding stumbling 7 times like the person before you.

> These are **7 loop patterns** proven to run in real environments. Each pattern answers: what problem does it solve, at what cadence, with which skills/state, how does it verify, how does it hand off to a human, and what are the tool-specific notes.

## Summary Table

| Pattern | Cadence | Starting level | Token cost |
|---------|---------|---------------|------------|
| [Daily Triage](daily-triage.md) | 1d–2h | **L1** report | Low |
| [PR Babysitter](pr-babysitter.md) | 5–15m | L1 watch | High |
| [CI Sweeper](ci-sweeper.md) | 5–15m | L2 cautious | Very high |
| [Dependency Sweeper](dependency-sweeper.md) | 6h–1d | L2 patch-only | Medium |
| [Changelog Drafter](changelog-drafter.md) | 1d or tag | **L1** draft | Low |
| [Post-Merge Cleanup](post-merge-cleanup.md) | 1d–6h | **L1** off-peak | Low |
| [Issue Triage](issue-triage.md) | 2h–1d | **L1** propose-only | Low |

## Pattern Picker — Which Loop?

> **Easy way to read it:** The table below is an **auto-answer machine** - you just answer one question "what hurts right now?" and follow the branch. If two things hurt at once, read the `Overlap Rules` below to see which loops can run together.

```
What hurts right now?
  ├── CI red? ──► CI Sweeper
  ├── PRs stalling? ──► PR Babysitter
  ├── Morning chaos / noisy issues? ──► Daily Triage + Issue Triage
  ├── Dependabot / CVE noise? ──► Dependency Sweeper
  ├── Merge debt / TODOs piling up? ──► Post-Merge Cleanup
  ├── Release notes stale? ──► Changelog Drafter
  └── Tight token budget? ──► Changelog Drafter / Daily Triage (L1)
```

### Cost-aware Picks

| Situation | Choose | Avoid (until budget + early-exit are in place) |
|-----------|----------|---------------------------------------------|
| Hobby / tight plan | Changelog Drafter, Daily Triage (L1), Post-Merge | CI Sweeper at 5m, PR Babysitter at 5m |
| CI is red | CI Sweeper at **15m+** with early-exit | Full triage every 5m when main is green |
| Many open PRs | PR Babysitter at 10–15m, L1 watch first | L2 fix loops on every tick |
| Release week | Changelog Drafter daily | Dependency Sweeper + CI Sweeper unattended |

### Overlap Rules

| Combination | Rule |
|-------------|------|
| CI Sweeper + PR Babysitter | CI Sweeper owns failing checks; PR Babysitter does not re-fix the same branch in the same hour |
| Daily Triage + any | Daily Triage reports; action loops execute. Triage does not auto-fix at L1 |
| Dependency Sweeper + CI Sweeper | Pause Dependency Sweeper when CI is red on main |
| Post-Merge + PR Babysitter | Post-Merge runs off-peak only |
| Changelog Drafter + any | Changelog Drafter is read-mostly and safe; no auto-publish |

## First Loop Recommendation

If you're not sure, start with **Daily Triage at L1**. It teaches state discipline without the risk of auto-merge.

## How to Use a Pattern

1. **Pick the pattern**: see the table above or the decision tree above.
2. **Scaffold**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (or `--tool claude` / `--tool opencode` / `--tool codex`).
3. **Copy the skills** from `templates/` if you need to customize.
4. **Set up scheduling** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Run week one at L1 report-only** before enabling fixes.
6. **Audit**: `npx @cobusgreyling/loop audit . --suggest`.

> **Golden rule**: never skip to L3 for a new pattern on a production repo. See [04-operating](../04-operating/) for the upgrade path.
