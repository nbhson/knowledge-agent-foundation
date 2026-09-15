# 📊 04. Measuring Tokens Saved — Savings

> RTK doesn't just compress output — it also **measures** token savings. This is the bridge to the harness's `11-evaluation` module: you need numbers to know how effectively your harness is running.

## Measurement Commands

| Command | Purpose |
|---------|---------|
| `rtk gain` | Overview of tokens saved |
| `rtk gain --graph` | ASCII chart for the last 30 days |
| `rtk gain --history` | Recent command history |
| `rtk gain --daily` | Per-day breakdown |
| `rtk gain --all --format json` | JSON export for dashboards |
| `rtk discover` | Find commands not yet optimized (missed savings opportunities) |
| `rtk discover --all --since 7` | All projects, last 7 days |
| `rtk session` | RTK adoption level across recent sessions |

## Reading the Numbers Right

> ⚠️ **Important**: RTK measures **bash output reduction**, not total token-bill reduction.

```
Bash output ──► Input tokens ──► Bill
     │               │               │
   90% cut       (one part of       (only one part of
    happens       the input, with    the bill; output
    here ✅ ✅ ✅  prompt, system,    is billed too)
                  history)
```

- Token counts reported by RTK estimate `bytes / 4` — there is no tokenizer.
- **The percentage reduction is reliable**; absolute token numbers are only approximations.
- Real savings get diluted across tiers when computing the final bill.

## Sample Reports

```bash
$ rtk gain
Commands run: 342
Raw bytes avoided: 1.2 MB
Estimated tokens saved: ~300k
Reduction: 82%
```

```bash
$ rtk discover
Found 5 commands with 0% reduction:
  - terraform plan      (12 calls)
  - kubectl apply       (8 calls)
  - ansible-playbook    (6 calls)
Consider `rtk init` for these or add custom TOML filters.
```

## Connection to Harness Evaluation

| Harness `11-evaluation` concept | RTK counterpart |
|----------------------------------|-----------------|
| Measuring agent effectiveness | `rtk gain` — tokens saved |
| Finding improvement opportunities | `rtk discover` — 0% reduction commands |
| Automated metrics | `rtk gain --all --format json` — feed a dashboard |
| Continuous improvement | `rtk session` — adoption check |

## RTK Benchmarks

| Command | Raw output | RTK output | Reduction |
|---------|-----------|------------|-----------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `ruff check` | Many lines | Grouped | ~80% |
| `docker ps` | Many columns | Essential fields only | ~70%+ |

## Notes on Measuring

- Run `rtk gain` regularly to track trends (like the `11-evaluation` module — continuous measurement).
- `rtk discover` shows which commands are still unfiltered — opportunities to add custom TOML filters.
- Telemetry is **off** by default — RTK doesn't send your data anywhere unless you opt in.

---

*Back to [rtk/README.md](../)* · Previous: [03 — Patterns](../03-patterns/) · Next: [05 — Troubleshooting](../05-troubleshooting/)
