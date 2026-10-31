# Agent Skills: pack the know-how, open only when needed

> Addendum to `harness/05` + `harness/06` + `loop/01`.
> Canonical spec: https://agentskills.io/specification

## Picture this

This section explains what a "skill" is, using a kitchen analogy — it matters because skills keep the prompt small and cheap.

A skill is like a **recipe card** in a kitchen. You don't read all 100 recipes
every night. You glance at the **dish name + one-line description** on each card,
pick the one matching tonight's dinner, and only then open it for details —
pulling extra tools or ingredients just when the recipe says so.

Agents work the same way. Instead of stuffing every convention into the prompt
(expensive and noisy), split each piece of know-how into a skill folder.
The agent skims names + descriptions, and opens the full card only on a match.

> **One-line summary:** A skill is a folder of know-how the agent only opens
> when its name + description match the task, so the prompt stays small.

## What lives in a skill?

This section shows the folder layout, so you know what files a skill contains before writing one.

```
skill-name/
├── SKILL.md          # Required: the "cover + recipe" — metadata + instructions
├── scripts/          # Optional: runnable code (python, bash, js...)
├── references/       # Optional: read-when-needed docs
├── assets/           # Optional: templates, images, schemas...
```

Read the tree above like this: `SKILL.md` is the only mandatory file
(it holds the description + instructions); the three other folders are optional
extras, loaded only when needed.

Three layers, open only what you need:

| Layer | When? | Cost? |
|---|---|---|
| Name + description | Skimmed every session | Tiny, ~50–100 tokens/skill — 100 skills is fine |
| Full `SKILL.md` body | Only when the description matches the task | Keep under ~5,000 tokens, short with examples |
| Files in `scripts/references/assets` | Only when the instructions say "open this" or "run that" | Costs only when actually used |

How to read the table: "Layer" = how much of the skill is opened; "When?" = at which moment; "Cost?" = token price (tokens = pieces of text the model pays to read). For instance, 100 skills × ~100 tokens ≈ 10,000 tokens of skim cost — still cheaper than pasting all instructions into the prompt.

> **One-line summary:** A skill is one required file (`SKILL.md`) plus optional
> folders, and each layer costs tokens only when the agent actually opens it.

## Writing a SKILL.md that works

This section lists the exact header fields allowed in `SKILL.md` — knowing them stops you from inventing fields that tools will ignore.

Two parts: **header** (YAML frontmatter) + **instructions** (Markdown).
(YAML frontmatter = a small metadata block between `---` lines at the very top
of the file.) Only these 6 header fields exist — don't invent your own:

| Field | Required? | How to write it |
|---|---|---|
| `name` | Yes | ≤64 chars, lowercase + digits + hyphens, no leading/trailing `-`, no `--`, **must match folder name**. Example: `pdf-processing` |
| `description` | Yes | ≤1024 chars. Say **what + when**. Always include `Use when ...`. Example: `Extract PDF text, fill forms, merge files. Use when handling PDFs.` |
| `license` | No | Short name, e.g. `Apache-2.0` |
| `compatibility` | No | ≤500 chars. Env needs, e.g. `needs network, needs python3` |
| `metadata` | No | `name → value` table for extras like `author`, `version` |
| `allowed-tools` | No | Space-separated pre-approved tools. Experimental, support varies. Example: `Bash(git:*) Read` |

How to read it: "Field" = the key you write in the header; "Required?" = must or may appear; "How to write it" = the format rules. For instance, `name` must be identical to the folder name — if the folder is `pdf-processing`, the header must say `name: pdf-processing` too.

Minimal working example:

```markdown
---
name: pdf-processing
description: Extract PDF text, fill forms, merge files. Use when handling PDFs.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
---

# PDF Processing
...steps, examples, common failures...
```

Tip: when unsure whether to pre-approve shell tools, **don't**.
(Pre-approve = let the agent run a command without asking first.)
Let the agent ask you before running terminal commands — much safer.

> **One-line summary:** Use only the 6 standard header fields, keep `name` equal
> to the folder name, and avoid pre-approving shell tools unless you must.

## Skill or something else?

This section helps you pick the right container — skill, prompt, agent, or hook — so you don't force every idea into a skill.

Beginners mix up 4 things. Simple rule of thumb:

- **Always-needed stuff** (coding style, repo conventions) → instructions / `AGENTS.md`, not a skill.
  (`AGENTS.md` = a guidance file every agent reads in every session.)
- **Sometimes-needed specialty** (PDF handling, pipeline debugging) → skill.
- **Skill vs prompt?** Multi-step + bundled files/scripts → skill.
  Small single task with a few inputs → prompt (slash command).
  (Slash command = a short prompt the user triggers by typing `/name`.)
- **Skill vs custom agent?** Same toolset through all steps → skill is enough.
  Need isolation (subagent returning one clean result) or different tool bans per stage → custom agent.
  (Subagent = a child agent doing one job, then returning a result to the parent.)
- **Instructions vs hooks?** Instructions are "advice" — the agent may forget.
  Hooks are "door locks" — shell code at lifecycle points that can actually block.
  (Lifecycle point = a fixed moment such as "before every file write".)
  See `harness/07-workflow/hooks-standard.md`.
- **Don't duplicate `AGENTS.md` in skills.** `AGENTS.md` is the always-on baseline.
  Skills are on-demand procedures on top. See `harness/02-build-context/agents-md-standard.md`.

> **One-line summary:** Put always-on rules in `AGENTS.md`, on-demand procedures
> in skills, one-shot small jobs in prompts, and enforcement in hooks.

## Two safety notes

This section lists two habits that prevent a skill from becoming an attack vector or a source of confusion.

1. **Strange skill = strange code.** A skill from an untrusted source may hide dangerous commands the agent will run. (Example: a `scripts/clean.sh` that actually runs `rm -rf ./` = delete everything in the current folder.) Skim it first, especially `scripts/`.
2. **One source of truth.** Keep skills in `.agents/skills/` (the neutral standard every tool reads). Don't keep 3 copies under `.agents/`, `.github/`, `.claude/` drifting apart. (Drifting apart = the copies get edited separately and slowly contradict each other.)

> **One-line summary:** Read untrusted skills before running them, and keep one
> canonical copy under `.agents/skills/` so copies never contradict each other.
