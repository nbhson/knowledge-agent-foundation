# 🔧 02. Installing & Integrating RTK

> How to install RTK on your machine and connect it to the AI coding tool you use. Once you finish this step, the agent's bash commands will be tidied up through RTK automatically.

What this page covers: getting the RTK program onto your machine, then wiring it into your AI coding tool so every shell command comes back compressed.

## Installation

> **One-line summary:** Four install routes, one per platform — brew (macOS, recommended), quick script, cargo, or a Windows binary.

### macOS (Homebrew — recommended)

Homebrew = the standard macOS package manager; "recommended" because it always fetches the correct RTK package.

> 📄 **Example code:** [`examples/01-macos-homebrew-recommended.sh`](examples/01-macos-homebrew-recommended.sh)

> **One-line summary:** On a Mac, `brew install rtk` is the safest route.

### Linux/macOS (Quick Install)

The quick script downloads the binary straight into `~/.local/bin` — remember to add that folder to your PATH (the list of folders the shell searches for programs).

> 📄 **Example code:** [`examples/02-linux-macos-quick-install.sh`](examples/02-linux-macos-quick-install.sh)

> **One-line summary:** The quick script is a one-liner, but check `~/.local/bin` is on your PATH afterwards.

### Cargo

Cargo = the Rust language's package installer. Read the warning below before using it — this is the #1 setup mistake.

> 📄 **Example code:** [`examples/03-cargo.sh`](examples/03-cargo.sh)

> ⚠️ **Name collision**: There is another project called "rtk" (Rust Type Kit) on crates.io (the public Rust package registry). If `rtk gain` fails, you installed the wrong package — use `cargo install --git` above instead.

> **One-line summary:** With cargo, install from the Git repo — the plain name grabs a different, unrelated "rtk" package.

### Windows

Download the `rtk-x86_64-pc-windows-msvc.zip` binary from [releases](https://github.com/rtk-ai/rtk/releases), extract it, and put `rtk.exe` on PATH. Run it from Command Prompt/PowerShell/Windows Terminal — don't double-click the `.exe` (double-clicking opens a console window that closes instantly and installs nothing).

> **One-line summary:** On Windows, unzip the release binary onto PATH and run it from a terminal, not by double-clicking.

### Verify the Installation

Run this to confirm the right RTK is in place — the version line should read `rtk 0.x.x`.

> 📄 **Example code:** [`examples/04-verify-the-installation.sh`](examples/04-verify-the-installation.sh)

> **One-line summary:** `rtk --version` showing `rtk 0.x.x` proves the correct package is installed.

## Integrating into Your AI Coding Tool

Run the command for the tool you use:

> 📄 **Example code:** [`examples/05-integrating-into-your-ai-coding-tool.sh`](examples/05-integrating-into-your-ai-coding-tool.sh)

After installing, **restart the AI tool** (a running tool keeps its old shell setup, so the new hook is not loaded yet), then test:

> 📄 **Example code:** [`examples/06-integrating-into-your-ai-coding-tool.sh`](examples/06-integrating-into-your-ai-coding-tool.sh)

> **One-line summary:** One `rtk init` command per tool, then restart the tool — only then does compression kick in.

## Per-Tool Integration Table

This table is the lookup for step 2 above. How to read it: **AI Tool** = the tool you use; **Init command** = the exact command to run; **Method** = how RTK attaches (a hook = code that rewrites commands before they run, vs an instructions file the agent reads voluntarily); **Lifetime** = global (all projects) or project (this repo only). For example, Claude Code uses a native hook installed globally with `rtk init -g`; "PreToolUse hook" = code the tool runs before every tool call, so RTK can rewrite the command; files like `.clinerules`, `AGENTS.md`, `.windsurfrules` = instruction files the agent reads and follows voluntarily.

| AI Tool | Init command | Method | Lifetime |
|---------|--------------|--------|----------|
| **Claude Code** | `rtk init -g` | PreToolUse hook (native binary) | Global |
| **GitHub Copilot (VS Code)** | `rtk init -g --copilot` | PreToolUse hook — transparent rewrite | Global |
| **GitHub Copilot CLI** | `rtk init -g --copilot` | PreToolUse deny-with-suggestion (CLI limit) | Global |
| **Cursor** | `rtk init -g --agent cursor` | preToolUse hook (hooks.json) | Global |
| **Gemini CLI** | `rtk init -g --gemini` | BeforeTool hook | Global |
| **Codex** | `rtk init -g --codex` | AGENTS.md + RTK.md instructions | Global |
| **Windsurf** | `rtk init -g --agent windsurf` | `.windsurfrules` | Project |
| **Cline / Roo Code** | `rtk init --agent cline` | `.clinerules` | Project |
| **OpenCode** | `rtk init -g --opencode` | Plugin TS (tool.execute.before) | Global |
| **OpenClaw** | `openclaw plugins install ./openclaw` | Plugin TS (before_tool_call) | Global |
| **Pi** | `rtk init -g --agent pi` | TypeScript extension (tool_call) | Global |
| **Hermes** | `rtk init --agent hermes` | Python plugin adapter (`rtk rewrite`) | Project |
| **Mistral Vibe** | `rtk init -g --agent vibe` | `pre_tool` hook (hooks.toml) | Global |
| **Kilo Code** | `rtk init --agent kilocode` | `.kilocode/rules/rtk-rules.md` | Project |
| **Google Antigravity** | `rtk init --agent antigravity` | `.agents/rules/antigravity-rtk-rules.md` | Project |
| **Kimi AI** | `rtk init --agent kimi` | AGENTS.md | Project |
| **Factory Droid** | `rtk init -g --agent droid` | PreToolUse hook in `~/.factory/hooks.json` | Global |

Plain glosses: "Deny-with-suggestion" = the CLI cannot rewrite, so it blocks and suggests the `rtk` version. "Plugin TS" = a small TypeScript plugin. "Transparent rewrite" = the agent never notices the command was changed.

> **One-line summary:** Find your tool's row, run its exact init command, note whether it's a silent hook or a voluntary rules file.

## Configuration

> **One-line summary:** One settings file (`config.toml`) plus per-command flags cover all tuning.

### Main config: `~/.config/rtk/config.toml`

`config.toml` = RTK's settings file (TOML = a simple `key = value` text format). On macOS it lives at `~/Library/Application Support/rtk/config.toml` instead.

> 📄 **Example code:** [`examples/07-main-config-config-rtk-config-toml.toml`](examples/07-main-config-config-rtk-config-toml.toml)

> **One-line summary:** All RTK settings — including which commands to exclude — live in one `config.toml` file.

### Global Flags

"Global flags" = options you can add to any `rtk` command to change its output, e.g. `-u` for even more compact output, `-v` for more detail when debugging.

> 📄 **Example code:** [`examples/08-global-flags.sh`](examples/08-global-flags.sh)

> **One-line summary:** Flags like `-u` and `-v` tune how much RTK prints, per command, without touching the config file.

## Uninstalling

> 📄 **Example code:** [`examples/09-uninstalling.sh`](examples/09-uninstalling.sh)

> **One-line summary:** `rtk init -g --uninstall` detaches the hook; `brew`/`cargo uninstall rtk` removes the binary.

## Quick Install Troubleshooting

This table lists the four most common install problems. How to read it: **Symptom** = what you see; **Cause** = why it happens; **Fix** = the command or action that solves it. For example, row 1: `rtk gain` failing right after install almost always means the wrong "rtk" package got installed from crates.io.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `rtk gain` fails after `cargo install` | Installed the wrong "Rust Type Kit" package | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Missing ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Bash commands not rewritten | Haven't restarted the AI tool, or using a built-in tool (`Read`/`Grep`) | Restart the tool; use a shell command or call `rtk read`/`rtk grep` directly |
| On Windows after upgrading from < 0.37.2 | Still using the legacy `rtk-rewrite.sh` | Re-run `rtk init -g` to migrate to the native binary hook |

> **One-line summary:** Four symptoms, four known fixes — wrong package, missing ripgrep, unrestarted tool, or a legacy Windows script.

---

*Back to [rtk/README.md](../)* · Previous: [01 — Concepts](../01-concepts/) · Next: [03 — Patterns](../03-patterns/)
