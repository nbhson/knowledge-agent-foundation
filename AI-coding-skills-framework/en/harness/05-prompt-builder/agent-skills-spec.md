# Agent Skills: pack the know-how, open only when needed

> Addendum to `harness/05` + `harness/06` + `loop/01`.
> Canonical spec: https://agentskills.io/specification

## Picture this

A skill is like a **recipe card** in a kitchen. You don't read all 100 recipes
every night. You glance at the **dish name + one-line description** on each card,
pick the one matching tonight's dinner, and only then open it for details —
pulling extra tools or ingredients just when the recipe says so.

Agents work the same way. Instead of stuffing every convention into the prompt
(expensive and noisy), split each piece of know-how into a skill folder.
The agent skims names + descriptions, and opens the full card only on a match.

## What lives in a skill?

```
skill-name/
├── SKILL.md          # Required: the "cover + recipe" — metadata + instructions
├── scripts/          # Optional: runnable code (python, bash, js...)
├── references/       # Optional: read-when-needed docs
├── assets/           # Optional: templates, images, schemas...
```

Three layers, open only what you need:

| Layer | When? | Cost? |
|---|---|---|
| Name + description | Skimmed every session | Tiny, ~50–100 tokens/skill — 100 skills is fine |
| Full `SKILL.md` body | Only when the description matches the task | Keep under ~5,000 tokens, short with examples |
| Files in `scripts/references/assets` | Only when the instructions say "open this" or "run that" | Costs only when actually used |

## Writing a SKILL.md that works

Two parts: **header** (YAML frontmatter) + **instructions** (Markdown).
Only these 6 header fields exist — don't invent your own:

| Field | Required? | How to write it |
|---|---|---|
| `name` | Yes | ≤64 chars, lowercase + digits + hyphens, no leading/trailing `-`, no `--`, **must match folder name**. Example: `pdf-processing` |
| `description` | Yes | ≤1024 chars. Say **what + when**. Always include `Use when ...`. Example: `Extract PDF text, fill forms, merge files. Use when handling PDFs.` |
| `license` | No | Short name, e.g. `Apache-2.0` |
| `compatibility` | No | ≤500 chars. Env needs, e.g. `needs network, needs python3` |
| `metadata` | No | `name → value` table for extras like `author`, `version` |
| `allowed-tools` | No | Space-separated pre-approved tools. Experimental, support varies. Example: `Bash(git:*) Read` |

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
Let the agent ask you before running terminal commands — much safer.

## Skill or something else?

Beginners mix up 4 things. Simple rule of thumb:

- **Always-needed stuff** (coding style, repo conventions) → instructions / `AGENTS.md`, not a skill.
- **Sometimes-needed specialty** (PDF handling, pipeline debugging) → skill.
- **Skill vs prompt?** Multi-step + bundled files/scripts → skill.
  Small single task with a few inputs → prompt (slash command).
- **Skill vs custom agent?** Same toolset through all steps → skill is enough.
  Need isolation (subagent returning one clean result) or different tool bans per stage → custom agent.
- **Instructions vs hooks?** Instructions are "advice" — the agent may forget.
  Hooks are "door locks" — shell code at lifecycle points that can actually block.
  See `harness/07-workflow/hooks-standard.md`.
- **Don't duplicate `AGENTS.md` in skills.** `AGENTS.md` is the always-on baseline.
  Skills are on-demand procedures on top. See `harness/02-build-context/agents-md-standard.md`.

## Two safety notes

1. **Strange skill = strange code.** A skill from an untrusted source may hide
   dangerous commands the agent will run. Skim it first, especially `scripts/`.
2. **One source of truth.** Keep skills in `.agents/skills/` (the neutral standard
   every tool reads). Don't keep 3 copies under `.agents/`, `.github/`, `.claude/` drifting apart.
