# 🧩 02. Seven Production Patterns

> **📌 Core Concept**
>
> **Definition:** A "production pattern" is **a proven loop template** — a ready-made setup with the scheduler, skills, state, verification approach, and human handoff already figured out. Instead of building a loop from scratch, you pick a fitting pattern and scaffold it with `loop init`.
> **Analogy:** Think of **dishes on a restaurant menu** — you don't need to invent the recipe yourself. The chef (the loop-engineering repo) has already tested them with real customers, and marked which ones are spicy (high cost) and which ones are beginner-friendly (L1). You just pick what suits you.
> **Why it matters:** These patterns have been "dogfooded" on a real repo, so every detail (cadence, token cost, failure mode) comes from real experience, not theory. You get to reuse those lessons instead of making the same 7 mistakes yourself.

> These are **7 loop patterns** proven to run in real environments. Each pattern explains: what problem it solves, how often it runs, which skills and state it uses, how it verifies its work, how it hands off to a human, and any tool-specific notes.

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

> **Easy way to read it:** The diagram below answers things for you automatically — just ask yourself "what hurts right now?" and follow that branch. If two things hurt at the same time, check the `Overlap Rules` below to see which loops can safely run together.

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

If you are not sure where to begin, start with **Daily Triage at L1**. It helps you learn good state habits without the risk of auto-merge.

## How to Use a Pattern

1. **Pick the pattern**: check the table above or the decision tree above.
2. **Scaffold**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (or `--tool claude` / `--tool opencode` / `--tool codex`).
3. **Copy the skills** from `templates/` if you need to customize.
4. **Set up scheduling** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Run week one at L1 report-only** before enabling fixes.
6. **Audit**: `npx @cobusgreyling/loop audit . --suggest`.

> **Golden rule**: never jump straight to L3 with a new pattern on a production repo. See [04-operating](../04-operating/) for the safe upgrade path.
