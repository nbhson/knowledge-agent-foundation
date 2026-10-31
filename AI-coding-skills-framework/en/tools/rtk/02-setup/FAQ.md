# ❓ FAQ — RTK — Setup (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

Each answer below follows the same shape: **What you see** (the symptom), **Why** (the cause in plain words), **What to do** (concrete steps), and **Verify** (how to confirm the fix worked).

---

## 02-setup/README.md

> **One-line summary:** Four setup failures and their fixes: wrong package, wrong flag, missing ripgrep, wrong knob.

### Q9. `rtk gain` fails right after install — did I install the wrong package? [→ Installation]

**What you see**

You ran `cargo install rtk`, the binary exists, and then `rtk gain` errors out or prints something you do not recognise. `rtk --version` does not show the expected `rtk 0.x.x`. (`rtk gain` = the command that opens the token-savings dashboard; `cargo` = the Rust language's package installer.)

**Why**

There is a **name collision**: a different project called "rtk" (Rust Type Kit) is published on crates.io (the public Rust package registry). Installing by plain name gives you that one — a completely different program that happens to share the name. This is the single most common setup failure.

**What to do**

1. On macOS, prefer `brew install rtk` (Homebrew = the macOS package manager, which points at the right package).
2. With cargo, always install from the Git repository, not from crates.io by name.
3. Use the quick-install script only if you prefer it; it installs into `~/.local/bin`, so add that to your PATH (the list of folders the shell searches for programs).

> 📄 **Example code:** [`examples/01-q9-rtk-gain-fails-right-after-install-did.sh`](examples/01-q9-rtk-gain-fails-right-after-install-did.sh)

**Verify**

`rtk --version` prints `rtk 0.x.x` and `rtk gain` opens the token-savings dashboard.

> **One-line summary:** A namesake package on crates.io breaks plain `cargo install rtk` — install from the Git repo or via brew instead.

---

### Q10. I ran `rtk init` but the agent still runs the raw command — what did I miss? [→ Integrating into Your AI Coding Tool]

**What you see**

Setup finished without errors, yet `git status` in the agent returns the usual full listing. You are convinced the hook is broken.

**Why**

Three usual causes: you did not restart the AI tool after `rtk init` (a running tool keeps its old shell setup, so the new hook is not loaded); you used the wrong flag for your tool (there are 16 of them — each AI tool needs its own flag, like `--gemini` or `--opencode`); or you used a rule-based tool with a global flag when it only supports project scope.

**What to do**

1. Run the command matching your tool exactly — for example `rtk init -g --gemini`, `rtk init -g --opencode`, `rtk init -g --agent cursor` (`-g` = global, i.e. for all projects).
2. For rule-based tools (Cline/Roo Code, Kimi, Hermes, Kilo Code, Antigravity) drop `-g` so the rules land in the project.
3. Restart the AI tool, then test.

> 📄 **Example code:** [`examples/02-q10-i-ran-rtk-init-but-the-agent.sh`](examples/02-q10-i-ran-rtk-init-but-the-agent.sh)

**Verify**

The agent's next `git status` returns the compact form, and your tool's hook or rules file exists on disk.

> **One-line summary:** If the hook seems dead: wrong flag for your tool, or you forgot to restart the AI tool.

---

### Q11. Every command fails with `Binary 'rg' not found on PATH` — one missing tool breaks everything? [→ Quick Install Troubleshooting]

**What you see**

RTK itself is fine, but filters crash or print that error. On Windows the same filters fail after upgrading from a version older than 0.37.2.

**Why**

Some filters invoke **ripgrep** (the fast search tool named `rg` on the command line). It is a separate program from RTK and must be installed and visible in your PATH (the list of folders the shell searches for executables) — RTK calls it like you would type `rg` yourself. Separately, older Windows setups kept a legacy `rtk-rewrite.sh` script instead of the native binary hook.

**What to do**

1. Install ripgrep: `brew install ripgrep` on macOS (brew = the macOS package manager), `winget install BurntSushi.ripgrep.MSVC` on Windows (winget = the Windows package manager).
2. Confirm `rg --version` works in the same shell the AI tool launches.
3. On Windows, re-run `rtk init -g` to migrate away from the legacy script.

> 📄 **Example code:** [`examples/03-q11-every-command-fails-with-binary-rg-not.sh`](examples/03-q11-every-command-fails-with-binary-rg-not.sh)

**Verify**

`rtk git status` and `rtk grep "pattern"` both run without the `rg` error, in the AI tool and in your terminal.

> **One-line summary:** The `rg` error just means ripgrep is missing or not on PATH — install it and restart the AI tool.

---

### Q12. Output is still longer than I want, and one command must not be touched — which knob do I turn? [→ Configuration / Global Flags]

**What you see**

Compression works, but a verbose tool still floods the context. Meanwhile `curl` and `playwright` commands behave wrongly once rewritten, and you want them left alone. (`curl` = a command-line tool for making web requests; `playwright` = a browser-automation tool.)

**Why**

Two independent controls exist. Global flags change how much RTK prints; the config file decides which commands RTK may rewrite at all. The main config lives at `~/.config/rtk/config.toml`, or `~/Library/Application Support/rtk/config.toml` on macOS.

**What to do**

1. Add `-u` / `--ultra-compact` for ASCII icons and inline format when you need even less output.
2. Add `-v`, `-vv`, `-vvv` only while debugging — each extra `v` prints more detail, which works against you here.
3. List commands to skip under `exclude_commands` in the config file.
4. To remove everything later, run `rtk init -g --uninstall` and remove the binary with `brew uninstall rtk` or `cargo uninstall rtk`.

> 📄 **Example code:** [`examples/04-q12-output-is-still-longer-than-i-want.toml`](examples/04-q12-output-is-still-longer-than-i-want.toml)

**Verify**

A `curl` command runs untouched; the same verbose command is shorter with `-u`; `rtk init -g --uninstall` removes the hook file afterwards.

> **One-line summary:** `-u` shrinks output further; `exclude_commands` in `config.toml` protects commands that must not be rewritten.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: 02-setup/README.md.*
