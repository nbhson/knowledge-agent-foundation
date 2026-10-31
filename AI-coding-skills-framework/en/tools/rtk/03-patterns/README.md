# 🧩 03. Four Patterns for Using RTK

> These are the **4 most common and handy RTK patterns** for working with AI coding agents. RTK = a wrapper that runs the same commands but returns short, filtered output, so the agent burns far fewer tokens. Each pattern covers: when to use it, which command to run, how much shorter the output gets, and what to watch out for.

## Summary Table

How to read it: each row is one pattern; "When to use" says the situation that calls for it; "Output reduction" says how much smaller the output gets (e.g. ~90% means 10 lines become 1); "Token cost before" says how expensive the raw command was without RTK (token = the billing unit of model usage). For instance, Test Only Failures turns hundreds of test lines into just the failures.

| Pattern | When to use | Output reduction | Token cost before |
|---------|-------------|-----------------|-------------------|
| [Git Speedup](git-speedup.md) | Working with git daily | ~70-93% | High (long status/log/diff) |
| [Test Only Failures](test-only-failures.md) | Running tests, debugging failures | ~90% | Very high (huge test output) |
| [File Smart Read](file-smart-read.md) | Reading large files to understand code | ~60-90% | High (long files) |
| [Build & Lint Compact](build-lint-compact.md) | Daily build/lint | ~75-85% | Medium-High |

> **One-line summary:** Pick the pattern for your most expensive command — git, tests, big files, or builds — and RTK cuts its output by 60-93%.

## Pattern Picker — Which Pattern to Choose?

This decision tree picks a pattern from the pain you feel right now.

```
What hurts right now?
  ├── Git status/log/diff eating context? ──► Git Speedup
  ├── Test output long, agent lost in noise? ──► Test Only Failures
  ├── Agent reads whole large files instead of what it needs? ──► File Smart Read
  ├── Build/lint output verbose? ──► Build & Lint Compact
  └── You use all of them? ──► Install the hook (`rtk init -g`) — it applies everything automatically
```

> **One-line summary:** Find what hurts now in the tree, or just install the hook and let RTK apply all patterns automatically.

### Cost-aware Picks

This table helps you choose when token budget matters, not just comfort.

How to read it: "Situation" describes your constraint; "Choose" is the pattern that fits it; "Avoid" is the wasteful alternative. For instance, if your token budget is tight, use RTK for git commands and do not run full test output on every run.

| Situation | Choose | Avoid |
|-----------|--------|-------|
| Tight token budget | Git Speedup (git push/status) | Test Only Failures on every run |
| CI is red | Test Only Failures | Full test output every time |
| Large repo, little familiarity | File Smart Read | `cat`-ing entire files |
| Frequent builds | Build & Lint Compact | Keeping verbose output |

> **One-line summary:** When tokens are scarce, compress the noisiest command you run most — git for daily work, tests when CI is red.

## Overlap Rules

This table answers: can I use two patterns at once? Usually yes — RTK routes per command.

How to read it: "Combination" is the pair (or all) of patterns in question; "Rule" says whether and how they coexist. For instance, Git Speedup and Test Only Failures can both stay on — RTK picks the right behavior per command.

| Combination | Rule |
|-------------|------|
| Git Speedup + Test Only Failures | Both work fine — RTK routes automatically per command |
| File Smart Read + Git Speedup | `rtk read` for files, `rtk git` for git — no conflict |
| All patterns | Just keep the hook enabled — the agent doesn't need to call manually |

> **One-line summary:** Patterns don't conflict — keep the hook on and RTK routes each command correctly by itself.

## First Pattern Recommendation

If you're just starting, enable **Git Speedup** first — it's safe, easy to verify (`git status` → `rtk git status`), and applies to every git working session.

> **One-line summary:** Start with Git Speedup — the safest, most verifiable pattern, and it pays off in every session.

## How to Use a Pattern

These five steps take one pattern from choice to tuned setup.

1. **Pick a pattern**: see the table above or the decision tree.
2. **Enable via hook**: `rtk init -g` for your tool (see [02-setup](../02-setup/)). (Hook = an automatic interceptor: every matching command gets rewritten to its `rtk` version without you typing it.)
3. **Verify**: run the command and compare raw output vs RTK output.
4. **Measure**: `rtk gain` to see tokens saved (see [04-savings](../04-savings/)).
5. **Tune**: add `exclude_commands` in `config.toml` if a command gets rewritten unexpectedly. (exclude_commands = the list of commands RTK must leave untouched.)

> **Golden rule**: RTK rewrites are transparent — if an important command needs full output, add it to `exclude_commands` instead of disabling the hook entirely.

> **One-line summary:** Enable via hook, verify by comparing outputs, measure with `rtk gain`, and exclude — never disable — commands that need full output.

---

*Back to [rtk/README.md](../)* · Previous: [02 — Setup](../02-setup/) · Next: [04 — Savings](../04-savings/)