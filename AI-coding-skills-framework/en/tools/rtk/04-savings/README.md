# 📊 04. Measuring Tokens Saved — Savings

> RTK doesn't just trim output — it also **measures** how much you saved. That makes it a friendly bridge to the harness's `11-evaluation` module: you get real numbers that show how well your harness is running.

## Measurement Commands

This table is the command menu. How to read it: **Command** is what you type, **Purpose** is what you get. For instance, `rtk gain` gives one overall report; `rtk gain --daily` splits the same report by day.

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

> **One-line summary:** `rtk gain` shows what you saved; `rtk discover` shows what you are still wasting.

## Reading the Numbers Right

> ⚠️ **Important**: RTK measures **bash output reduction**, not total token-bill reduction.

The diagram below shows where the cut happens: only at the bash-output step — the bill also includes the prompt, history, and the model's own output.

```
Bash output ──► Input tokens ──► Bill
     │               │               │
   90% cut       (one part of       (only one part of
    happens       the input, with    the bill; output
    here ✅ ✅ ✅  prompt, system,    is billed too)
                  history)
```

- Token counts reported by RTK estimate `bytes / 4` — there is no tokenizer, so 4 characters ≈ 1 token. (A "token" is roughly a word piece the model reads.)
- **The percentage reduction is reliable**; absolute token numbers are only approximations.
- Real savings get diluted across tiers when computing the final bill.

> **One-line summary:** Trust the percentage, not the absolute token count — RTK shrinks one ingredient of the bill, not the whole bill.

## Sample Reports

This section links to real command output you can compare against your own runs.

> 📄 **Example code:** [`examples/01-sample-reports.sh`](examples/01-sample-reports.sh)

> 📄 **Example code:** [`examples/02-sample-reports.sh`](examples/02-sample-reports.sh)

> **One-line summary:** Look at the sample reports first so you know what a healthy `rtk gain` output looks like.

## Connection to Harness Evaluation

This table maps each RTK measuring command to the evaluation idea it implements. How to read it: left = the concept from the harness `11-evaluation` module, right = the RTK command that does it.

| Harness `11-evaluation` concept | RTK counterpart |
|----------------------------------|-----------------|
| Measuring agent effectiveness | `rtk gain` — tokens saved |
| Finding improvement opportunities | `rtk discover` — 0% reduction commands |
| Automated metrics | `rtk gain --all --format json` — feed a dashboard |
| Continuous improvement | `rtk session` — adoption check |

> **One-line summary:** Every RTK measuring command is a hands-on version of one evaluation idea from the harness.

## RTK Benchmarks

How to read this table: each row is one command, its raw output size, its RTK-compressed size, and the saving. For instance, `git push` normally prints 15 lines; RTK reduces it to just `ok main` (~93% smaller).

| Command | Raw output | RTK output | Reduction |
|---------|-----------|------------|-----------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `ruff check` | Many lines | Grouped | ~80% |
| `docker ps` | Many columns | Essential fields only | ~70%+ |

> **One-line summary:** Typical cuts are 70-93% of command output — the biggest wins come from verbose test and push output.

## Notes on Measuring

- Run `rtk gain` regularly to track trends (like the `11-evaluation` module — continuous measurement).
- `rtk discover` shows which commands are still unfiltered — opportunities to add custom TOML filters. (TOML = a simple `key = value` config file format.)
- Telemetry is **off** by default — RTK doesn't send your data anywhere unless you opt in.

> **One-line summary:** Measure weekly, fix the 0% commands `rtk discover` finds, and know that nothing leaves your machine by default.

---

*Back to [rtk/README.md](../)* · Previous: [03 — Patterns](../03-patterns/) · Next: [05 — Troubleshooting](../05-troubleshooting/)
