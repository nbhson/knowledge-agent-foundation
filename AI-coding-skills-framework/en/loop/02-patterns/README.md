# 🧩 02. Seven Production Patterns

> **📌 Core Concept**
>
> **Definition:** A "production pattern" is **a proven loop template** — a ready-made setup with the scheduler, skills, state, verification approach, and human handoff already figured out. Instead of building a loop from scratch, you pick a fitting pattern and scaffold it with `loop init`. (Scaffold = generate the starter files automatically.)
> **Analogy:** Think of **dishes on a restaurant menu** — you don't need to invent the recipe yourself. The chef (the loop-engineering repo) has already tested them with real customers, and marked which ones are spicy (high cost) and which ones are beginner-friendly (L1). You just pick what suits you.
> **Why it matters:** These patterns have been "dogfooded" on a real repo, so every detail (cadence, token cost, failure mode) comes from real experience, not theory. You get to reuse those lessons instead of making the same 7 mistakes yourself. (Dogfooded = tested by actually using it on a real project.)

> These are **7 loop patterns** proven to run in real environments. Each pattern explains: what problem it solves, how often it runs, which skills and state it uses, how it verifies its work, how it hands off to a human, and any tool-specific notes.

## Summary Table

How to read it: each row is one pattern. **Cadence** = how often it runs (1d = daily, 5–15m = every 5–15 minutes); **Starting level** = the autonomy level to begin at (L1 = report-only, L2 = small fixes with a verifier); **Token cost** = roughly how much AI compute each run burns. For instance, "Daily Triage" runs once or twice a day, only reports, and is cheap — the safest first loop.

| Pattern | Cadence | Starting level | Token cost |
|---------|---------|---------------|------------|
| [Daily Triage](daily-triage.md) | 1d–2h | **L1** report | Low |
| [PR Babysitter](pr-babysitter.md) | 5–15m | L1 watch | High |
| [CI Sweeper](ci-sweeper.md) | 5–15m | L2 cautious | Very high |
| [Dependency Sweeper](dependency-sweeper.md) | 6h–1d | L2 patch-only | Medium |
| [Changelog Drafter](changelog-drafter.md) | 1d or tag | **L1** draft | Low |
| [Post-Merge Cleanup](post-merge-cleanup.md) | 1d–6h | **L1** off-peak | Low |
| [Issue Triage](issue-triage.md) | 2h–1d | **L1** propose-only | Low |

> **One-line summary:** Seven ready-made loops — the four bolded L1 ones are the cheapest and safest to start with.

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

(Plain words: CI = the automated build-and-test system; Dependabot/CVE = automated dependency-update PRs and security vulnerability alerts; merge debt = cleanups piling up after merges.)

### Cost-aware Picks

How to read it: pick a row matching your situation; **Choose** = safe picks; **Avoid** = what burns too much budget until you add cost caps and early exits. (Early-exit = stopping immediately when there's nothing to do, instead of running the full pipeline.)

| Situation | Choose | Avoid (until budget + early-exit are in place) |
|-----------|----------|---------------------------------------------|
| Hobby / tight plan | Changelog Drafter, Daily Triage (L1), Post-Merge | CI Sweeper at 5m, PR Babysitter at 5m |
| CI is red | CI Sweeper at **15m+** with early-exit | Full triage every 5m when main is green |
| Many open PRs | PR Babysitter at 10–15m, L1 watch first | L2 fix loops on every tick |
| Release week | Changelog Drafter daily | Dependency Sweeper + CI Sweeper unattended |

> **One-line summary:** On a tight budget, stick to the L1 patterns and keep high-frequency loops to 10–15m+ intervals.

### Overlap Rules

How to read it: each row is a pair of loops and the rule for running them together without stomping on each other. For instance, when CI is red, pause the Dependency Sweeper — it would fix against a broken base.

| Combination | Rule |
|-------------|------|
| CI Sweeper + PR Babysitter | CI Sweeper owns failing checks; PR Babysitter does not re-fix the same branch in the same hour |
| Daily Triage + any | Daily Triage reports; action loops execute. Triage does not auto-fix at L1 |
| Dependency Sweeper + CI Sweeper | Pause Dependency Sweeper when CI is red on main |
| Post-Merge + PR Babysitter | Post-Merge runs off-peak only |
| Changelog Drafter + any | Changelog Drafter is read-mostly and safe; no auto-publish |

> **One-line summary:** Each pair gets one rule so loops don't fix the same thing twice or fight over a broken base.

## First Loop Recommendation

If you are not sure where to begin, start with **Daily Triage at L1**. It helps you learn good state habits without the risk of auto-merge.

> **One-line summary:** Begin with Daily Triage at L1 — safe, cheap, and it builds good state habits.

## How to Use a Pattern

1. **Pick the pattern**: check the table above or the decision tree above.
2. **Scaffold**: `npx @cobusgreyling/loop init . --pattern <name> --tool grok` (or `--tool claude` / `--tool opencode` / `--tool codex`). (`npx` = run a Node.js package without installing it globally; `--tool` = which agent CLI to target.)
3. **Copy the skills** from `templates/` if you need to customize.
4. **Set up scheduling** (`/loop`, `scheduler_create`, GitHub Action, Codex Automation).
5. **Run week one at L1 report-only** before enabling fixes.
6. **Audit**: `npx @cobusgreyling/loop audit . --suggest` (audit = the tool checks your loop setup and suggests safety improvements).

> **Golden rule**: never jump straight to L3 with a new pattern on a production repo. See [04-operating](../04-operating/) for the safe upgrade path.

> **One-line summary:** Pick → scaffold → schedule → one week report-only → audit; and never jump straight to L3.

## October 2026 Update — Portability: Patterns Without Vendor CLI Lock-in

> **⚠️ Important note**
>
> The patterns in this folder reference the `@cobusgreyling/loop-*` CLI in their examples. These are **concrete examples to make things easier to picture**, NOT a hard dependency. You can implement any of these patterns with a different scheduler / toolchain while keeping the exact same process, metrics, and safety gates. (Vendor CLI lock-in = being forced to keep one company's command-line tool.)

### Pattern → Vendor-CLI-Free Replacement Mapping

How to read it: left column = the pattern; right column = a common free/open tool that can run the same pattern. For instance, the Changelog Drafter can simply be `git-cliff`, a tool that generates release notes from commit history.

| Pattern | Replacement without a vendor CLI |
|---------|-------------------------------|
| Daily Triage | GitHub Actions cron + issue labels |
| PR Babysitter | GitHub Actions + `gh` CLI |
| CI Sweeper | CI webhook + bot |
| Dependency Sweeper | Dependabot / Renovate |
| Changelog Drafter | git-cliff / release-drafter |
| Issue Triage | issue-labeler bot |

> **One-line summary:** Every pattern has a plain, free equivalent — the pattern outlives the tool.

### Principles

**A pattern = process + metrics + safety gates; the CLI is just one implementation.** Any scheduler — cron, Temporal, Airflow, GitHub Actions, Kestra — can implement these patterns, as long as you preserve the three core components above.

> **One-line summary:** The pattern is process + metrics + safety gates; any scheduler can carry it.

### Porting Checklist

When porting a pattern to a different scheduler (porting = moving it to another tool):

1. **Separate logic from the CLI** — the workflow (what the loop does) must be independent of the tool that invokes it.
2. **Keep the exit code convention** — `0` = proceed, `2` = escalate — so control scripts chain together regardless of scheduler. (Exit code = the number a script returns when it finishes; 0 traditionally means "success".)
3. **Keep the `STATE.md` + run-log JSON schema** — state and logs are the contract between runs; they don't change with the tool.
4. **Dry-run for one week** before cutover — run in parallel in report-only mode to confirm the metrics match before retiring the old system. (Dry-run = a trial run with no real actions; cutover = the switch from old to new.)

> **One-line summary:** Port by separating logic from the CLI, keeping exit codes, state, and log schemas — and dry-run a week first.

> **One-line summary:** Pick a proven pattern from the table, run it report-only for a week, respect the overlap rules — and remember the pattern is the process, not the CLI tool it happens to ship with.
