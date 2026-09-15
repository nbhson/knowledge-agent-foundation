# 🔧 02. Installing & Integrating RTK

> How to install RTK on your machine and integrate it into the AI coding tool you use. After this step, the agent's bash commands will be automatically rewritten through RTK.

## Installation

### macOS (Homebrew — recommended)

```bash
brew install rtk
```

### Linux/macOS (Quick Install)

```bash
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
# Installs into ~/.local/bin — add to PATH if needed:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

### Cargo

```bash
cargo install --git https://github.com/rtk-ai/rtk
```

> ⚠️ **Name collision**: There is another project called "rtk" (Rust Type Kit) on crates.io. If `rtk gain` fails, you installed the wrong package — use `cargo install --git` above instead.

### Windows

Download the `rtk-x86_64-pc-windows-msvc.zip` binary from [releases](https://github.com/rtk-ai/rtk/releases), extract it, and put `rtk.exe` on PATH. Run it from Command Prompt/PowerShell/Windows Terminal — don't double-click the `.exe`.

### Verify the Installation

```bash
rtk --version   # Should print "rtk 0.x.x"
rtk gain        # Should open the token-savings dashboard
```

## Integrating into Your AI Coding Tool

Run the command for the tool you use:

```bash
# Hook-based (transparent rewrite — recommended)
rtk init -g                     # Claude Code / GitHub Copilot (default)
rtk init -g --gemini            # Gemini CLI
rtk init -g --codex             # Codex (OpenAI)
rtk init -g --agent cursor      # Cursor
rtk init -g --agent windsurf    # Windsurf
rtk init -g --opencode          # OpenCode
rtk init -g --agent pi          # Pi
rtk init -g --agent droid       # Factory Droid

# Plugin / Rule-based (project-scoped)
rtk init --agent cline          # Cline / Roo Code  ← uses .clinerules
rtk init --agent kilocode       # Kilo Code
rtk init --agent antigravity    # Google Antigravity
rtk init --agent kimi           # Kimi AI
rtk init --agent hermes         # Hermes
```

After installing, **restart the AI tool**, then test:

```bash
git status  # Will be automatically rewritten to "rtk git status"
```

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

```toml
[hooks]
exclude_commands = ["curl", "playwright"]  # skip rewrite for these commands

[tee]
enabled = true          # save raw output on failure (default: true)
mode = "failures"       # "failures", "always", or "never"
```

### Global Flags

```bash
-u, --ultra-compact    # ASCII icons, inline format (reduces output even more)
-v, --verbose          # Increase verbosity (-v, -vv, -vvv)
```

## Uninstalling

```bash
rtk init -g --uninstall     # Remove the hook, RTK.md, settings.json entry
cargo uninstall rtk          # Remove the binary (if installed via cargo)
brew uninstall rtk           # Remove via Homebrew (if installed via brew)
```

## Quick Install Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `rtk gain` fails after `cargo install` | Installed the wrong "Rust Type Kit" package | `cargo install --git https://github.com/rtk-ai/rtk` |
| `Binary 'rg' not found on PATH` | Missing ripgrep | `brew install ripgrep` (macOS) / `winget install BurntSushi.ripgrep.MSVC` (Windows) |
| Bash commands not rewritten | Haven't restarted the AI tool, or using a built-in tool (`Read`/`Grep`) | Restart the tool; use a shell command or call `rtk read`/`rtk grep` directly |
| On Windows after upgrading from < 0.37.2 | Still using the legacy `rtk-rewrite.sh` | Re-run `rtk init -g` to migrate to the native binary hook |

---

*Back to [rtk/README.md](../)* · Previous: [01 — Concepts](../01-concepts/) · Next: [03 — Patterns](../03-patterns/)
