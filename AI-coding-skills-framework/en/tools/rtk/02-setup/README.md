# 🔧 02. Installing & Integrating RTK

> How to install RTK on your machine and connect it to the AI coding tool you use. Once you finish this step, the agent's bash commands will be tidied up through RTK automatically.

## Installation

### macOS (Homebrew — recommended)

> 📄 **Example code:** [`examples/01-macos-homebrew-recommended.sh`](examples/01-macos-homebrew-recommended.sh)

### Linux/macOS (Quick Install)

> 📄 **Example code:** [`examples/02-linux-macos-quick-install.sh`](examples/02-linux-macos-quick-install.sh)

### Cargo

> 📄 **Example code:** [`examples/03-cargo.sh`](examples/03-cargo.sh)

> ⚠️ **Name collision**: There is another project called "rtk" (Rust Type Kit) on crates.io. If `rtk gain` fails, you installed the wrong package — use `cargo install --git` above instead.

### Windows

Download the `rtk-x86_64-pc-windows-msvc.zip` binary from [releases](https://github.com/rtk-ai/rtk/releases), extract it, and put `rtk.exe` on PATH. Run it from Command Prompt/PowerShell/Windows Terminal — don't double-click the `.exe`.

### Verify the Installation

> 📄 **Example code:** [`examples/04-verify-the-installation.sh`](examples/04-verify-the-installation.sh)

## Integrating into Your AI Coding Tool

Run the command for the tool you use:

> 📄 **Example code:** [`examples/05-integrating-into-your-ai-coding-tool.sh`](examples/05-integrating-into-your-ai-coding-tool.sh)

After installing, **restart the AI tool**, then test:

> 📄 **Example code:** [`examples/06-integrating-into-your-ai-coding-tool.sh`](examples/06-integrating-into-your-ai-coding-tool.sh)

## Per-Tool Integration Table

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

## Configuration

### Main config: `~/.config/rtk/config.toml`

macOS: `~/Library/Application Support/rtk/config.toml`

> 📄 **Example code:** [`examples/07-main-config-config-rtk-config-toml.toml`](examples/07-main-config-config-rtk-config-toml.toml)

### Global Flags

> 📄 **Example code:** [`examples/08-global-flags.sh`](examples/08-global-flags.sh)

## Uninstalling

> 📄 **Example code:** [`examples/09-uninstalling.sh`](examples/09-uninstalling.sh)

## Quick Install Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `rtk gain` fails after `cargo install` | Installed the wrong "Rust Type Kit" package | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Missing ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Bash commands not rewritten | Haven't restarted the AI tool, or using a built-in tool (`Read`/`Grep`) | Restart the tool; use a shell command or call `rtk read`/`rtk grep` directly |
| On Windows after upgrading from < 0.37.2 | Still using the legacy `rtk-rewrite.sh` | Re-run `rtk init -g` to migrate to the native binary hook |

---

*Back to [rtk/README.md](../)* · Previous: [01 — Concepts](../01-concepts/) · Next: [03 — Patterns](../03-patterns/)
