# 🧠 01. RTK Architecture — Concepts

> Understanding how RTK works helps you configure it correctly, avoid classic pitfalls, and know when RTK can't help (Claude Code's built-in `Read`/`Grep`/`Glob` tools bypass the hook).

## How RTK Intervenes in the Command Flow

```
  Without rtk:                                    With rtk:

  Claude  --git status-->  shell  -->  git         Claude  --git status-->  RTK  -->  git
    ^                                   |            ^                      |          |
    |         full raw output           |            |  compact output      | filter   |
    +-----------------------------------+            +------- (filtered) ---+----------+
```

RTK inserts itself **between the agent and the shell command**. The agent calls `git status` → the hook rewrites it to `rtk git status` → RTK runs the real command and filters/compresses the output → the agent only receives the compact output.

## Two Operating Modes

| Mode | How it works | AI Tools |
|------|--------------|----------|
| **Hook rewrite** | Intercepts before the command runs, rewrites `git status` → `rtk git status`. Transparent, the agent doesn't notice | Claude Code, Copilot VS Code, Gemini CLI, Cursor... |
| **Plugin / Rule-based** | The agent reads the rules (`.clinerules`, `AGENTS.md`, `RTK.md`) and calls `rtk <cmd>` itself | Cline/Roo Code (`.clinerules`), Codex (AGENTS.md + RTK.md), Windsurf... |

## The Four Compression Strategies (Core of RTK)

| # | Strategy | What it does | Example |
|---|----------|--------------|---------|
| 1 | **Smart Filtering** | Removes noise: comments, whitespace, boilerplate | `git push` → just `ok main` |
| 2 | **Grouping** | Collapses similar items (files by directory, errors by type) | `ls` → tree with file counts |
| 3 | **Truncation** | Keeps the important part, cuts redundancy | `git diff` → drop the headers |
| 4 | **Deduplication** | Merges repeated logs into a count | `docker logs` → `×42 repeated line` |

> 📌 **Key point:** RTK is **not a tokenizer** — it estimates `bytes / 4`. The percentages (90% reduction) are reliable, but absolute token numbers are only approximations.

## When a Command Fails: Tee Recovery

An important RTK feature: when a command fails, RTK stores **the entire raw output** so the agent can read it back without re-running the command:

```
FAILED: 2/15 tests
[full output: ~/.local/share/rtk/tee/1707753600_cargo_test.log]
```

Configured in `config.toml`:

```toml
[tee]
enabled = true          # save raw output on failure (default: true)
mode = "failures"       # "failures", "always", or "never"
```

## Binary Structure & Dependencies

| Component | Notes |
|-----------|-------|
| Single Rust binary | High performance, overhead <10ms |
| 100+ supported commands | git, cargo, npm, pytest, docker, kubectl, aws... |
| ripgrep (`rg`) | Some filters invoke `rg` — must be installed and kept in PATH |
| `~/.config/rtk/config.toml` | Main configuration (macOS: `~/Library/Application Support/rtk/config.toml`) |
| `~/.local/share/rtk/tee/` | Where full output is stored when a command fails |

## Basic Configuration

```toml
# ~/.config/rtk/config.toml (macOS: ~/Library/Application Support/rtk/config.toml)
[hooks]
exclude_commands = ["curl", "playwright"]  # skip rewrite for these commands

[tee]
enabled = true
mode = "failures"
```

See the full configuration (env vars, per-project filters) in the [Configuration guide](https://www.rtk-ai.app/guide/getting-started/configuration).

## Important Limitations (Scope)

- **The hook only runs on Bash tool calls.** Claude Code's built-in tools (`Read`, `Grep`, `Glob`) do **not** go through the hook → they aren't auto-rewritten.
- For those workflows: use shell commands (`cat`/`head`/`tail`, `rg`/`grep`, `find`) or call `rtk read`, `rtk grep`, `rtk find` directly.
- RTK measures **bash output reduction**, not total token-bill reduction (input tokens are only one part of the bill).

## Frequently Asked Questions (Concepts Level)

**Q: Can RTK replace coding your own context compression?**
A: No. RTK optimizes the **Immediate Context tier** (command output). The other tiers (system instructions, task context, domain knowledge, conversation history) are still handled by your harness — as in module `02-build-context`.

**Q: Is RTK safe for sensitive data?**
A: RTK does not collect source code, file paths, secrets, or env vars (telemetry is off by default). The AWS-specific filters additionally strip secrets from output proactively.

---

*Back to [rtk/README.md](../)* · Next: [02 — Setup](../02-setup/)
