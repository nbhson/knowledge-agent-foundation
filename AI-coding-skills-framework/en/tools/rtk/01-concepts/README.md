# 🧠 01. RTK Architecture — Concepts

> Knowing how RTK works makes it easier to set up, avoid common mistakes, and understand when it can't help (Claude Code's built-in `Read`/`Grep`/`Glob` tools bypass the hook).

## How RTK Intervenes in the Command Flow

This section explains where RTK sits — between the agent and the shell, filtering on the way back. Why it matters: that single position explains both what RTK can and cannot touch. How to read the diagram: the left side is the normal flow — the agent runs `git status` and gets the full raw output back; the right side shows RTK inserted in the middle: the real command still runs, but RTK filters the output before the agent sees it.

```
  Without rtk:                                    With rtk:

  Claude  --git status-->  shell  -->  git         Claude  --git status-->  RTK  -->  git
    ^                                   |            ^                      |          |
    |         full raw output           |            |  compact output      | filter   |
    +-----------------------------------+            +------- (filtered) ---+----------+
```

RTK inserts itself **between the agent and the shell command**. The agent calls `git status` → the hook rewrites it to `rtk git status` → RTK runs the real command and filters/compresses the output → the agent only receives the compact output. A "hook" = a small program the AI tool runs automatically before every shell command.

> **One-line summary:** RTK sits between agent and shell, rewriting commands and handing back only the compact output.

## Two Operating Modes

This section explains why the same RTK install behaves differently in different AI tools — a common source of confusion. How to read the table: **Mode** = the integration style; **How it works** = what actually happens; **AI Tools** = which tools use that mode. For example, hook rewrite = the command is silently rewritten before it runs, so the agent never notices.

| Mode | How it works | AI Tools |
|------|--------------|----------|
| **Hook rewrite** | Intercepts before the command runs, rewrites `git status` → `rtk git status`. Transparent, the agent doesn't notice | Claude Code, Copilot VS Code, Gemini CLI, Cursor... |
| **Plugin / Rule-based** | The agent reads the rules (`.clinerules`, `AGENTS.md`, `RTK.md`) and calls `rtk <cmd>` itself | Cline/Roo Code (`.clinerules`), Codex (AGENTS.md + RTK.md), Windsurf... |

Plain glosses: `.clinerules`, `AGENTS.md`, `RTK.md` = instruction files the agent reads and follows voluntarily. "Transparent" = invisible to the agent. In rule-based mode nothing is forced — the agent only does it if it follows the file.

> **One-line summary:** Hook mode rewrites commands silently; rule mode just leaves instructions the agent may follow.

## The Four Compression Strategies (Core of RTK)

This section lists the four tricks RTK uses to shrink output — the core of how it saves tokens. How to read the table: **#** = row number; **Strategy** = the trick's name; **What it does** = a plain description; **Example** = a before/after. For example, row 1: `git push` normally prints ~15 lines of progress; RTK reduces it to just `ok main`.

| # | Strategy | What it does | Example |
|---|----------|--------------|---------|
| 1 | **Smart Filtering** | Removes noise: comments, whitespace, boilerplate | `git push` → just `ok main` |
| 2 | **Grouping** | Collapses similar items (files by directory, errors by type) | `ls` → tree with file counts |
| 3 | **Truncation** | Keeps the important part, cuts redundancy | `git diff` → drop the headers |
| 4 | **Deduplication** | Merges repeated logs into a count | `docker logs` → `×42 repeated line` |

Plain glosses: "boilerplate" = text repeated on every run that carries no new information. "×42 repeated line" = the same log line appeared 42 times, shown once with a counter.

> 📌 **Key point:** RTK is **not a tokenizer** — it estimates `bytes / 4`. The percentages (90% reduction) are reliable, but absolute token numbers are only approximations. In plain words: it guesses tokens by dividing byte count by 4 — good for ratios, not for exact billing.

> **One-line summary:** RTK shrinks output four ways — filter, group, truncate, dedupe — and estimates tokens, never counts them exactly.

## When a Command Fails: Tee Recovery

This section explains RTK's safety net: failed commands keep their full output on disk. Why it matters: compression is lossy, so this is how you get lost details back without re-running anything.

An important RTK feature: when a command fails, RTK stores **the entire raw output** so the agent can read it back without re-running the command. "Tee" = the Unix idea of a T-splitter: the output flows both to the screen and to a file.

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Reading the example: the agent sees only the failure count plus a path — the path points to the full log saved under your home folder (`~/.local/share/rtk/tee/`).

Configured in `config.toml`:

> 📄 **Example code:** [`examples/01-when-a-command-fails-tee-recovery.toml`](examples/01-when-a-command-fails-tee-recovery.toml)

> **One-line summary:** Failures cost nothing to investigate: RTK saves the whole raw output to a log file you can read later.

## Binary Structure & Dependencies

This section lists what RTK is made of and what it needs on your machine — read it before debugging install problems. How to read the table: **Component** = the part of RTK or its dependency; **Notes** = what to know about it. For example, row 3: ripgrep (`rg`) is a separate search program some RTK filters call; if it is missing, those filters fail.

| Component | Notes |
|-----------|-------|
| Single Rust binary | High performance, overhead <10ms |
| 100+ supported commands | git, cargo, npm, pytest, docker, kubectl, aws... |
| ripgrep (`rg`) | Some filters invoke `rg` — must be installed and kept in PATH |
| `~/.config/rtk/config.toml` | Main configuration (macOS: `~/Library/Application Support/rtk/config.toml`) |
| `~/.local/share/rtk/tee/` | Where full output is stored when a command fails |

Plain glosses: "single Rust binary" = one self-contained executable file, fast to start. "PATH" = the list of folders your shell searches for programs. "Overhead <10ms" = RTK itself adds less than 10 milliseconds per command.

> **One-line summary:** One fast binary, 100+ supported commands, one required helper (ripgrep), two folders to know.

## Basic Configuration

> 📄 **Example code:** [`examples/02-basic-configuration.toml`](examples/02-basic-configuration.toml)

See the full configuration (env vars, per-project filters) in the [Configuration guide](https://www.rtk-ai.app/guide/getting-started/configuration).

> **One-line summary:** Start from the sample `config.toml`; the official guide covers env vars and per-project filters.

## Important Limitations (Scope)

This section states what RTK cannot do — read it to avoid the most common misconception.

- **The hook only runs on Bash tool calls.** Claude Code's built-in tools (`Read`, `Grep`, `Glob`) do **not** go through the hook → they aren't auto-rewritten. In plain words: only shell commands get compressed; the agent's built-in file reading and searching tools bypass RTK entirely.
- For those workflows: use shell commands (`cat`/`head`/`tail` = print a file or its start/end, `rg`/`grep` = search text, `find` = locate files) or call `rtk read`, `rtk grep`, `rtk find` directly.
- RTK measures **bash output reduction**, not total token-bill reduction (input tokens are only one part of the bill).

> **One-line summary:** RTK compresses shell command output only — built-in file tools bypass it, and it does not shrink your whole bill.

## Frequently Asked Questions (Concepts Level)

**Q: Can RTK replace coding your own context compression?**
A: No. RTK optimizes the **Immediate Context tier** (command output). The other tiers (system instructions, task context, domain knowledge, conversation history) are still handled by your harness — as in module `02-build-context`. In plain words: RTK only compresses command output; the rest of what fills the model's context window is your harness's job.

**Q: Is RTK safe for sensitive data?**
A: RTK does not collect source code, file paths, secrets, or env vars (telemetry is off by default). The AWS-specific filters additionally strip secrets from output proactively. "Telemetry" = usage data sent to the developer; "env vars" = environment variables, which often hold API keys.

> **One-line summary:** RTK covers only command output — and it phones nothing home.

---

*Back to [rtk/README.md](../)* · Next: [02 — Setup](../02-setup/)
