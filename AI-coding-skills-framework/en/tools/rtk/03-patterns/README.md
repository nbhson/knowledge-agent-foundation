# 🧩 03. Four Patterns for Using RTK

> These are the **4 most common and useful RTK patterns** when working with AI coding agents. Each pattern answers: when to use it, which command, the output reduction level, and caveats.

## Summary Table

| Pattern | When to use | Output reduction | Token cost before |
|---------|-------------|-----------------|-------------------|
| [Git Speedup](git-speedup.md) | Working with git daily | ~70-93% | High (long status/log/diff) |
| [Test Only Failures](test-only-failures.md) | Running tests, debugging failures | ~90% | Very high (huge test output) |
| [File Smart Read](file-smart-read.md) | Reading large files to understand code | ~60-90% | High (long files) |
| [Build & Lint Compact](build-lint-compact.md) | Daily build/lint | ~75-85% | Medium-High |

## Pattern Picker — Which Pattern to Choose?

```
What hurts right now?
  ├── Git status/log/diff eating context? ──► Git Speedup
  ├── Test output long, agent lost in noise? ──► Test Only Failures
  ├── Agent reads whole large files instead of what it needs? ──► File Smart Read
  ├── Build/lint output verbose? ──► Build & Lint Compact
  └── You use all of them? ──► Install the hook (`rtk init -g`) — it applies everything automatically
```

### Cost-aware Picks

| Situation | Choose | Avoid |
|-----------|--------|-------|
| Tight token budget | Git Speedup (git push/status) | Test Only Failures on every run |
| CI is red | Test Only Failures | Full test output every time |
| Large repo, little familiarity | File Smart Read | `cat`-ing entire files |
| Frequent builds | Build & Lint Compact | Keeping verbose output |

## Overlap Rules

| Combination | Rule |
|-------------|------|
| Git Speedup + Test Only Failures | Both work fine — RTK routes automatically per command |
| File Smart Read + Git Speedup | `rtk read` for files, `rtk git` for git — no conflict |
| All patterns | Just keep the hook enabled — the agent doesn't need to call manually |

## First Pattern Recommendation

If you're just starting, enable **Git Speedup** first — it's safe, easy to verify (`git status` → `rtk git status`), and applies to every git working session.

## How to Use a Pattern

1. **Pick a pattern**: see the table above or the decision tree.
2. **Enable via hook**: `rtk init -g` for your tool (see [02-setup](../02-setup/)).
3. **Verify**: run the command and compare raw output vs RTK output.
4. **Measure**: `rtk gain` to see tokens saved (see [04-savings](../04-savings/)).
5. **Tune**: add `exclude_commands` in `config.toml` if a command gets rewritten unexpectedly.

> **Golden rule**: RTK rewrites are transparent — if an important command needs full output, add it to `exclude_commands` instead of disabling the hook entirely.

---

*Back to [rtk/README.md](../)* · Previous: [02 — Setup](../02-setup/) · Next: [04 — Savings](../04-savings/)
