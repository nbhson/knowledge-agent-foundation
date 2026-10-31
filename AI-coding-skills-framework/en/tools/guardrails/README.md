# 🛡️ Guardrails — The Safety Layer for Harness Tool Calls

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Guardrails Matter?](#why-guardrails-matter)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of the Guardrails](#overview-of-the-guardrails)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section shows why agents need a safety layer at all: models write text, and text can trigger harmful actions.

Your harness can call `write_file`, `execute_python`, `send_notification`, `sql_query`. In plain words: write a file to disk, run Python code, send a message to people, run a database query. One day the agent misunderstands the prompt and calls `write_file` with a path like... `/etc/passwd` — a system file that must never be touched. Or it sends the same notification 100 times. Or it runs a command that deletes data.

LLMs have no built-in sense of "bad side effects" — they just produce text. **Guardrails are the safety layer that stops the harness from doing things it should not do**, before the action happens. Think of them as the bouncer at the door: the model asks to act, the guardrail checks the request first.

> *"The model proposes. The guardrail disposes."*

> **One-line summary:** Models can accidentally order dangerous actions; guardrails check every action before it runs.

### Why Guardrails Matter?

This section connects guardrails to the tool pipeline described in the harness docs.

> In harness/06-decide-tools-mcp — every tool call must go through a `GUARDRAILS CHECK`: *"Validate permission, safety, rate limit"*.

How to read the table: **#** is a row number; **Reason** is the short label; **Explanation** gives a concrete example. For instance, row 3 means: if a tool is limited to 60 calls per minute, the guardrail blocks call number 61.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Block side effects** | Stop `write_file` in forbidden folders, or `execute_python` with risky commands |
| 2 | **Permission enforcement** | A tool with `requires_permission="elevated"` needs approval first |
| 3 | **Rate limiting** | `rate_limit_per_minute=60` — stops an agent from calling tools too many times |
| 4 | **Output validation** | Check the output for rule breaks before it goes back into context |

Plain glosses: `write_file` = write content to a file on disk. `requires_permission="elevated"` = a label saying "this tool is dangerous, ask a human first". `rate_limit_per_minute=60` = at most 60 calls per minute, like a speed limit for tool calls.

> **One-line summary:** Guardrails block dangerous writes, force approval for risky tools, cap how often tools fire, and check outputs.

### Relationship to the Harness

This blockquote sets the boundary: this directory lists tools you can adopt; the actual rules live elsewhere in the repo.

> **This directory is a product catalog, not the harness's policy.**
> Each entry below is a *specific library you could adopt*. The canonical
> **authorization and isolation policy** — risk tiers, mandatory gate payloads,
> timeout-deny (fail closed), the two-person rule, the `PAUSED:` protocol — is owned by
> [`harness/15-approval-gates`](../../harness/15-approval-gates/README.md), and the
> **isolation mechanism** by
> [`harness/12-sandbox-execution`](../../harness/12-sandbox-execution/README.md).
> A guardrail library *validates*; it does not decide what is allowed. If you find
> yourself inventing a risk tier here, it belongs in `15`.

In plain words: "canonical policy" = the one official set of rules. "Risk tiers" = levels like low/medium/high risk. "Fail closed" = if the check itself times out, deny the action (safe default). "Two-person rule" = two people must approve a very risky action. `PAUSED:` = a marker the agent prints to stop and wait for approval. "Isolation" = running risky code in a sealed box (sandbox) so it cannot touch the real system.

```
┌────────────────────────────────────────────────────────────┐
│  GUARDRAILS MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  harness/15-approval-gates  → CANONICAL policy + PAUSED:   │
│                              protocol (owns policy)        │
│  harness/12-sandbox-execution → canonical isolation tiers  │
│                                                            │
│  Guardrails AI            → harness/06 (tool input/output) │
│  NeMo Guardrails (NVIDIA) → harness/07 (workflow rails)    │
│  LlamaGuard (Meta)        → harness/05 (prompt safety)     │
│  Permission/rate limit    → harness/06 (decide tools)      │
└────────────────────────────────────────────────────────────┘
```

How to read the map: `→` means "plays the same role as". For example, "Guardrails AI → harness/06" means Guardrails AI does the checking that harness/06 assigns to tool input/output validation.

```
Tool Decision Pipeline (from harness/06):
  User Query → Intent → Tool Selector → Parameter Extractor
      → ❯ GUARDRAILS CHECK (validate permission, safety, rate limit)
      → Tool Executor → Result Processor
```

Reading the pipeline left to right: a user's question becomes an intent, a tool is chosen, its parameters are filled in, the guardrail checks the plan, then the tool runs and the result is processed. The `❯` marks where the safety check sits.

> **One-line summary:** This directory is a catalog of guardrail libraries; the official safety rules live in harness/15 and harness/12.

## Overview of the Guardrails

This table compares the three main guardrail options.

> **One-line summary:** Three options: rule-based checks (Guardrails AI), workflow rails (NeMo), and a safety-classifier model (LlamaGuard). How to read it: **Guardrail** = the library name; **Publisher** = who makes it; **Type** = how it works (open-source code vs a model that classifies); **Standout features** = what makes it different. For example, LlamaGuard is not a rule engine — it is a separate LLM trained to flag dangerous prompts.

| Guardrail | Publisher | Type | Standout features |
|-----------|-----------|------|-------------------|
| **Guardrails AI** | Guardrails AI | Open-source | Validators for input/output, structured intervention |
| **NeMo Guardrails** | NVIDIA | Open-source | Rails: input, dialog, retrieval, execution |
| **LlamaGuard** | Meta | Model-based | LLM classifier specialized in detecting dangerous prompts/responses |

Plain glosses: "validators" = small checks like "is this a valid email? is this string under 100 chars?". "Rails" = fixed tracks the conversation must stay on, like rails a train runs on. "Retrieval rails" = rules for what the agent may fetch. "LLM classifier" = a model that answers "safe or unsafe?".

### Guardrails AI — Validate Input/Output

What this shows: Guardrails AI checking tool inputs and outputs against declared rules.

> 📄 **Example code:** [`examples/01-guardrails-ai-validate-input-output.py`](examples/01-guardrails-ai-validate-input-output.py)

> **One-line summary:** Guardrails AI = rule-based checks on what goes into and comes out of a tool.

### NeMo Guardrails — Rails That Model the Flow

What this shows: NeMo Guardrails defining rails (allowed paths) for a whole conversation or workflow, not just one tool call.

> 📄 **Example code:** [`examples/02-nemo-guardrails-rails-that-model-the-flow.py`](examples/02-nemo-guardrails-rails-that-model-the-flow.py)

> **One-line summary:** NeMo Guardrails puts rails around the whole workflow, not just single calls.

### LlamaGuard — Model-Based Safety Classifier

What this shows: LlamaGuard, a dedicated model that reads a prompt or response and labels it safe or unsafe.

> 📄 **Example code:** [`examples/03-llamaguard-model-based-safety-classifier.py`](examples/03-llamaguard-model-based-safety-classifier.py)

> **One-line summary:** LlamaGuard = a second model whose only job is to flag dangerous content.

### Permission & Rate Limit in the Harness (harness/06)

What this shows: how the harness itself stores permission levels and rate limits on each tool definition, before any external library is involved.

> 📄 **Example code:** [`examples/04-permission-rate-limit-in-the-harness-harness-06.py`](examples/04-permission-rate-limit-in-the-harness-harness-06.py)

> **One-line summary:** Permissions and rate limits are declared on each tool — the guardrail layer then enforces them.

## Learning Roadmap (Directory Structure)

> **One-line summary:** This section maps the folder layout and a step-by-step learning path.

This tree shows the folder layout; `(TODO)` means not written yet.

```
guardrails/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Validators, rails, prompt safety, permission checks
├── 02-setup/            ← (TODO) Installing Guardrails AI / NeMo / LlamaGuard
├── 03-patterns/         ← (TODO) Tool-level guard, workflow rails, PII filtering
├── 04-savings/          ← (TODO) Reducing costs caused by wrong actions
└── 05-troubleshooting/  ← (TODO) False positives, overrides, bypasses
```

### Recommended Roadmap

This is a suggested learning order. Read `↓` as "then do this next". "PII filtering" = blocking personal data (names, emails, ID numbers) from leaving your system.

```
Step 1: Understand the tool decision pipeline + where the guardrail sits (harness/06)
   ↓
Step 2: Install Guardrails AI — validate tool parameters (02-setup)
   ↓
Step 3: Add permissions + rate limits to ToolDefinition (03-patterns)
   ↓
Step 4: Upgrade to NeMo Rails at the workflow level (03-patterns)
   ↓
Step 5: LlamaGuard for prompt safety (measured in 04-savings)
```

This table maps questions to docs. How to read it: left column = your goal; right column = the doc that covers it. For example, "Loop safety" = keeping automated loops from doing damage — read loop/03-safety.

| If you want to... | Read |
|-------------------|------|
| Tool decision pipeline | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Permission system | [harness/08-task](../../harness/08-task/) |
| Safe automation | [harness/10-automation](../../harness/10-automation/) |
| Loop safety | [loop/03-safety](../../loop/03-safety/) |
| Loop gate (mechanical) | [tools/loop-cli](../loop-cli/) |

> **One-line summary:** Learn the pipeline first, then one library at a time: rule checks → permissions → workflow rails → prompt classification.

## Real-World Case Studies

Two worked scenarios with runnable code — read the scenario, then the file.

> **One-line summary:** Two complete scenarios — blocking a destructive call, and stacking rate limit with approval — each with code.

### 1. Blocking Tool Damage

What this shows: catching a harmful tool call (like writing to a forbidden folder) before it executes.

> 📄 **Example code:** [`examples/05-1-blocking-tool-damage.py`](examples/05-1-blocking-tool-damage.py)

> **One-line summary:** A guardrail can stop a destructive tool call at the door, before any damage happens.

### 2. Rate Limit + Elevated Permission

What this shows: combining a call-count cap with a "human must approve" rule on the same tool.

> 📄 **Example code:** [`examples/06-2-rate-limit-elevated-permission.py`](examples/06-2-rate-limit-elevated-permission.py)

> **One-line summary:** Rate limits cap frequency; elevated permission adds human approval — the two stack.

## Reference Materials

Official pages of the three libraries, for deeper reading.

> **One-line summary:** Three official links — one per library above.

- **Guardrails AI**: https://www.guardrailsai.com
- **NeMo Guardrails (NVIDIA)**: https://github.com/NVIDIA/NeMo-Guardrails
- **LlamaGuard (Meta)**: https://ai.meta.com/research/publications/llama-guard

### Links to Other Branches

Related pages in this repo — follow them for the neighboring topic.

> **One-line summary:** Neighboring topics: the harness pipeline, the loop gate, and guardrails inside agent loops.

- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Guardrails check in the pipeline
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (list of guardrails)
- [tools/loop-cli](../loop-cli/) — `loop gate` enforces mechanically
- [tools/langchain](../langchain/) — Guardrails inside agent loops

---

> **"A harness without guardrails is a loaded weapon pointed at production."**

---

## ⚠️ Update 10/2026: Guardrails AI Hub — Major Changes 2026

This section records what changed for Guardrails AI in 2026, so you don't follow outdated install instructions.

**Guardrails AI** is still actively maintained, but two significant changes occurred:

1. **Validators moved to standard PyPI (7/2026):** Validators no longer come via the hosted Guardrails Hub — install directly with `pip`. Remote inferencing has been discontinued.

Plain gloss: PyPI = the standard Python package repository, where `pip install` downloads from. "Validators moved to PyPI" = you now install each check as a normal Python package instead of fetching it from Guardrails' own hub. "Remote inferencing discontinued" = the hosted service that ran checks for you online is gone; everything runs locally.

> 📄 **Example code:** [`examples/07-update-10-2026-guardrails-ai-hub-major-changes.py`](examples/07-update-10-2026-guardrails-ai-hub-major-changes.py)

2. **PyPI 0.6.x still active** — the framework core still works. For lighter alternatives:

How to read this table: **Alternative** = the replacement option; **Why** = when it fits better than Guardrails AI; **Link** = where to find it. For example, Pydantic validators are checks you write with a library most Python projects already have — no new dependency.

| Alternative | Why | Link |
|-------------|-----|------|
| **Pydantic Validators** | Lightweight, built-in Python, no extra dependency | https://docs.pydantic.dev/ |
| **NeMo Guardrails** | NVIDIA, open-source, active development | https://github.com/NVIDIA/NeMo-Guardrails |
| **Llama Guard** | Meta, model-based classifier, runs locally | https://ai.meta.com/research/llama-guard |

> **One-line summary:** Guardrails AI checks now install from PyPI like any Python package; if that feels heavy, Pydantic, NeMo, or Llama Guard are solid lighter options.

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — guardrails*
