# ❓ FAQ — RTK — Measuring Savings (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets). Each answer follows the same shape: **What you see** (the symptom), **Why** (the root cause), **What to do** (the fix), **Verify** (how to confirm it worked).

---

## 04-savings/README.md

### Q28. `rtk gain` says I saved ~300k tokens, but my bill barely moved — is the number fake? [→ Reading the Numbers Right]

**What you see**

```
Commands run: 342
Raw bytes avoided: 1.2 MB
Estimated tokens saved: ~300k
Reduction: 82%
```

The report looks great. The invoice does not. So you either believe the tool and doubt your billing, or the reverse — and either way you stop trusting `rtk gain`.

**Why**

RTK measures **bash output reduction**, not total bill reduction. Bash output is one part of your input tokens, sitting alongside the system prompt and the conversation history — and the model's own output is billed separately. Cut 90% of one component and the total moves far less. Also, RTK estimates tokens as `bytes / 4` (4 characters ≈ 1 token) because there is no tokenizer, so absolute numbers are approximate.

**What to do**

1. Trust the **percentage**, not the absolute token count.
2. Remember the reduction happens at the bash-output step, not at the bill step.
3. Track the trend over weeks (`rtk gain`), not one report.
4. Use `rtk gain --all --format json` to feed your own dashboard, where you can pair it with real billing data.
5. Use `rtk gain --graph` for the last 30 days and `rtk gain --daily` when you want the per-day split.
6. Expect real savings to be diluted across the tiers when the final bill is computed.

How to read this table: it shows where in the pipeline the 90% cut actually lands — at the bash-output step, before input tokens, and long before the bill.

| Bash output | Input tokens | Bill |
|---|---|---|
| 90% cut happens here ✅ | one part, with prompt + system + history | output is billed too |

**Verify**

Compare two weeks of `rtk gain --graph`. The reduction percentage should be stable and high; the "Estimated tokens saved" line should be treated as an order of magnitude, not an invoice forecast. If someone asks "how much did RTK save me?", the honest answer is "82% of bash output".

> **One-line summary:** The number is not fake — it measures 82% off bash output only, one slice of a bill that also charges for prompt, history, and model output.

---

### Q29. `rtk discover` found 5 commands with 0% reduction — what do I do with them? [→ Measurement Commands]

**What you see**

```
Found 5 commands with 0% reduction:
  - terraform plan      (12 calls)
  - kubectl apply       (8 calls)
  - ansible-playbook    (6 calls)
Consider `rtk init` for these or add custom TOML filters.
```

Twenty-six calls producing zero savings. Your instinct: RTK is not doing its job on your actual workload.

**Why**

RTK only compresses commands it has a filter for. `rtk discover` is the honest answer to "what am I still paying full price for" — it scans your command history across projects and ranks by call count, so the top entries are where a filter would pay off most. `terraform plan` is genuinely hard to compress safely (its full output is the point), which is a different problem from a missing filter.

**What to do**

1. Look at the highest call counts first — 12 calls of `terraform plan` beats 6 of something else.
2. Run `rtk init` for the commands it recognises.
3. Write custom TOML filters for the ones it does not. (TOML = a simple `key = value` config format; a "filter" tells RTK how to shrink one command's output.)
4. For commands that must stay raw (`terraform plan`), add them to `exclude_commands` deliberately instead of chasing the number. (`exclude_commands` = a do-not-touch list.)
5. Pair the report with `rtk session` to see how much of your recent sessions actually ran through RTK at all.

> 📄 **Example code:** [`examples/01-q29-rtk-discover-found-5-commands-with-0.sh`](examples/01-q29-rtk-discover-found-5-commands-with-0.sh)

**Verify**

`rtk discover --all --since 7` shows a shorter list week over week, and `rtk gain` shows the reduction percentage climbing without any change to how you work. A report that never shrinks means you stopped writing filters — not that RTK stopped working.

> **One-line summary:** A 0% command is a to-do, not a failure — add a filter for it, or exclude it on purpose if it must stay raw.

---

### Q30. Does RTK send my data anywhere? I am reading proprietary file names all day. [→ Notes on Measuring]

**What you see**

RTK sits in front of every command and records how much output it saved. That record includes command names, file paths, and project names. You also know that failed test runs keep a full raw log on disk — the "tee" copy RTK writes so the agent can read the uncut output later (`tee` = a second, untouched copy saved to disk). You want to know whether any of it leaves your machine.

**Why**

Telemetry is **off by default**. RTK does not send your data anywhere unless you opt in. The savings history is stored locally. Separately, the AWS-related filters proactively strip secrets from captured output — a second reason the stored logs are less sensitive than the raw command output would be.

**What to do**

1. Leave telemetry off; nothing is transmitted.
2. For an absolute block, set `RTK_TELEMETRY_DISABLED=1` in your shell.
3. Export reports locally only: `rtk gain --all --format json > rtk-gain.json`.
4. Know where the stored logs live — `~/.local/share/rtk/` (a hidden folder in your home directory) — and treat them as sensitive, because they hold real output.
5. On Windows, the same idea is `setx RTK_TELEMETRY_DISABLED 1` before restarting the shell.

> 📄 **Example code:** [`examples/02-q30-does-rtk-send-my-data-anywhere-i.sh`](examples/02-q30-does-rtk-send-my-data-anywhere-i.sh)

**Verify**

Check your shell config for the variable, confirm no opt-in flag is set anywhere, and review `ls ~/.local/share/rtk/` to see exactly what is stored on disk. The same privacy-by-default principle says secrets should be stripped from captured output in the first place — the AWS filters do that proactively.

> **One-line summary:** Nothing leaves your machine unless you opt in — telemetry is off by default, logs stay local, and secrets are stripped from captures.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 04-savings/README.md.*
