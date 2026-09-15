# 🗜️ RTK (Rust Token Killer) — Context Optimization Tool for the Harness

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Is RTK Part of the Harness?](#is-rtk-part-of-the-harness)
> - [Why RTK Matters?](#why-rtk-matters)
> - [Overview](#overview)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

Your harness already has tools, memory, context — but there's a quiet context glutton: **bash output**. Every time the agent runs `git status`, `cargo test`, or `ls`, it gets hundreds of lines of noise back — and in that pile of noise, the agent easily misses the very error line it needs to fix.

**RTK (Rust Token Killer)** is a CLI proxy written in Rust that inserts itself between the agent and the shell command, cutting up to **90% of bash output** before it reaches the LLM context. A single binary, 100+ supported commands, overhead <10ms.

> __RTK is part of the harness ecosystem — it's the tooling that materializes `harness/02-build-context`, and it lives in `tools/rtk/`.__ It is not a component inside `harness/`, and now `tools/` has become the fully centralized place for the supporting tooling that materializes all 7 components of the harness.

---

### Is RTK Part of the Harness?

### ✅ **YES — conceptually.**

According to [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md), the harness consists of **7 components**. RTK belongs to **Component #3 — Context Management** (the Context Optimization / Token Reduction branch), and is secondarily related to **Tools** (#1) and **Evaluation**:

| Component | Role | Related to RTK? |
|-----------|------|-----------------|
| **Context Management** (the circulatory system) | The AI always has the right information at the right time | 🟢 **DIRECT** — compresses Immediate Context (Level 5) |
| **Tools** (the hands) | Defines what the AI can do | 🟡 Indirect — RTK is a tool proxy around the shell |
| **Evaluation** | Measures effectiveness | 🟡 Indirect — `rtk gain` measures tokens saved |

**Mapping to the `harness/` directory:**

| Module | Related | Why |
|--------|---------|-----|
| `harness/02-build-context` | 🟢 **Primary** | Context compression at the Immediate Context tier |
| `harness/06-decide-tools-mcp` | 🟡 Secondary | Tool proxy design |
| `harness/11-evaluation` | 🟡 Secondary | `rtk gain` / `rtk discover` |

> **Distinction**: RTK is a **concrete execution tool** (a Rust binary), NOT a knowledge module like `harness/01-11` — which is why it lives in the `tools/` branch, with the same convention as `harness/` and `loop/`.

### Why RTK Matters?

> **"Input tokens are the currency of agent reasoning. Don't spend them on bash noise."**

| # | Reason | Evidence |
|---|--------|----------|
| 1 | **Context management** | RTK cuts up to 90% of `cargo test`/`git push` output — the agent gains space to reason about the parts that actually matter |
| 2 | **Harness evaluation** | `rtk gain` provides token-saved numbers — aligning with the "Cut Costs 40-60%" goal in HARNESS_ENGINEERING.md |
| 3 | **Materializing the theory** | The "limit tool output" technique in module `06` is implemented by RTK at the bash layer |

## Overview

RTK intercepts shell commands and compresses their output with **4 strategies**:

| # | Strategy | Example |
|---|----------|---------|
| 1 | **Smart filtering** (drop noise) | `git push` → `ok main` |
| 2 | **Grouping** (collapse similar) | `ls` → tree with file counts |
| 3 | **Truncation** (keep what matters) | `git diff` → drop the headers |
| 4 | **Deduplication** (merge repeated logs) | `docker logs` → `×42 repeated line` |

Supports **16 AI coding tools** via hooks/plugins: Claude Code, Cline, Copilot VS Code, Gemini CLI, Codex, Cursor, Windsurf, OpenCode...

## Learning Roadmap (Directory Structure)

```
rtk/
├── README.md            ← YOU ARE HERE — overview + roadmap + case studies
├── 01-concepts/         ← Architecture: hook system, 4 compression strategies, tee recovery
├── 02-setup/            ← Installation + integration with each AI tool (16 tools)
├── 03-patterns/         ← 4 production patterns, one file per pattern
│   ├── README.md        ←   Pattern picker + summary table
│   ├── git-speedup.md
│   ├── test-only-failures.md
│   ├── file-smart-read.md
│   └── build-lint-compact.md
├── 04-savings/          ← Measurement: rtk gain, discover, session
└── 05-troubleshooting/  ← Failure modes & mitigations
```

> Each directory contains a `README.md` — consistent with the convention of `harness/` and `loop/`.

### Recommended Roadmap

```
Step 1: Read this README to understand the context
   ↓
Step 2: 01-concepts/ — understand the hook architecture + the 4 compression strategies
   ↓
Step 3: 02-setup/ — install + integrate into your AI tool
   ↓
Step 4: 03-patterns/ — start with Git Speedup
   ↓
Step 5: 04-savings/ — measure the tokens saved with `rtk gain`
   ↓
Step 6: 05-troubleshooting/ — when something goes wrong
```

| If you want to... | Read |
|-------------------|------|
| Understand how RTK works | [01-concepts](01-concepts/) |
| Install + integrate the tool | [02-setup](02-setup/) |
| Which pattern to start with | [03-patterns](03-patterns/) — pattern picker |
| Make git faster | [03-patterns/git-speedup.md](03-patterns/git-speedup.md) |
| See only test failures | [03-patterns/test-only-failures.md](03-patterns/test-only-failures.md) |
| Measure tokens saved | [04-savings](04-savings/) |
| Handle a mis-rewritten command | [05-troubleshooting](05-troubleshooting/) |

---

## Real-World Case Studies

The `rtk-ai/rtk` repo dogfoods itself — supporting 16 AI tools with different integration mechanisms:

| AI Tool | Method | Level |
|---------|--------|-------|
| Claude Code | PreToolUse hook (native binary) | Transparent rewrite |
| GitHub Copilot (VS Code) | PreToolUse hook | Transparent rewrite |
| Cline / Roo Code | `.clinerules` (project-scoped) | Rule-based rewrite |
| Gemini CLI | BeforeTool hook | Transparent rewrite |
| Codex | AGENTS.md + RTK.md instructions | Instruction-based |
| Cursor | preToolUse hook (hooks.json) | Transparent rewrite |

**Measured results:**

| Command | Raw output | RTK output | Reduction |
|---------|-----------|------------|-----------|
| `ls -la` | 45 lines | 12 lines | ~73% |
| `git push` | 15 lines | `ok main` | ~93% |
| `cargo test` (fail) | 200+ lines | ~20 lines | ~90% |
| `docker ps` | Many columns | Essential fields only | ~70%+ |
| `ruff check` | Many lines | Grouped by rule | ~80% |

---

## Reference Materials

- https://github.com/rtk-ai/rtk — The main repo
- https://www.rtk-ai.app/guide — Full user guide (installation, supported agents, configuration, troubleshooting)
- [ARCHITECTURE.md](https://github.com/rtk-ai/rtk/blob/master/docs/contributing/ARCHITECTURE.md) — System design & technical decisions
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — The 7 components of the harness
- [tools/README.md](../README.md) — The Tools branch overview
- [loop/](../../loop/) — Loops that benefit from lighter context

---

> **"A model is only as good as the information it can access at inference time — and every wasted token is information your agent doesn't get to reason with."**

---

*This article is part of the [AI Coding Skills Framework](../../..) — the Tools branch · RTK*
