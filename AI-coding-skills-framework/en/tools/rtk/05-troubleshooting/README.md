# 🛠️ 05. Troubleshooting — Handling Failures

> Common failures when using RTK, how to diagnose and fix them. Includes failure modes, exclude rules, and when you should turn RTK off.

## Failure Modes & Mitigations Table

| Failure | Cause | Solution |
|---------|-------|----------|
| Bash commands not rewritten | Haven't restarted the AI tool after `rtk init` | Restart the tool and retest `git status` |
| Outside the hook: built-in tools (`Read`/`Grep`/`Glob`) bypass | Use shell commands or call `rtk read`/`rtk grep` directly |
| `Binary 'rg' not found on PATH` | Missing ripgrep — some filters need `rg` | `brew install ripgrep` / `winget install BurntSushi.ripgrep.MSVC` |
| `rtk gain` fails after `cargo install` | Installed the wrong "Rust Type Kit" package (crates.io collision) | `cargo install --git https://github.com/rtk-ai/rtk` |
| Important commands compressed too far | Filter too aggressive | Add to `exclude_commands` in `config.toml` |
| Output loses context in pipelines (`\| grep`) | Compressed format not parseable | Check the pipeline; call the original command directly if needed |
| Token cost still high | Not using all RTK features | `rtk discover` finds 0%-reduction commands; add custom TOML filters |
| On Windows: legacy shell hook | Version < 0.37.2 | Re-run `rtk init -g` to migrate to the native binary hook |
| Filter not applied for a specific project | Needs per-project config | See the Configuration guide (per-project filters) |

## Exclude Rules — When to Keep the Original Command

Add a command to `exclude_commands` if:

- It needs the **exact full** output (e.g., detailed `git diff`, `terraform plan`).
- It **should not be rewritten** to avoid danger (curl downloading binaries, playwright).
- A pipeline/script depends on the original output format.

```toml
# ~/.config/rtk/config.toml
[hooks]
exclude_commands = ["curl", "playwright", "terraform plan"]
```

## Safety Notes (harness Guardrails connection)

| Principle | Applied to RTK |
|-----------|----------------|
| Per the harness guardrails principle | RTK rewrites are transparent — the agent can still call the original command. Always check important output before the agent acts on it. |
| Tee recovery | When a command fails, RTK stores the full output — the agent should read the complete log before deciding on a fix. |
| Privacy by default | Telemetry is off by default. AWS filters proactively strip secrets. Set `RTK_TELEMETRY_DISABLED=1` for an absolute block if desired. |

## When You Should Turn RTK Off

- Debugging the exact output of a specific tool and you need the raw version.
- A command with important side effects where you want to see the full log.
- A pipeline/CI script that parses output in the original format.

```bash
rtk init -g --uninstall   # Remove the hook entirely
```

Or use `exclude_commands` per command instead of turning it off entirely.

---

*Back to [rtk/README.md](../)* · Previous: [04 — Savings](../04-savings/)
