# AGENTS.md: the house rules on the door for every new agent

> Addendum to `harness/02` + `loop/01`.
> Open standard: https://agents.md · Steward: Agentic AI Foundation (Linux Foundation).
> ~23 tools support it. Claude Code reads `CLAUDE.md` first, falls back to `AGENTS.md` — keep a symlink to be safe.

## Picture this

You hire a new assistant for your repo. Instead of repeating every time
"build with what, test with what, never touch what", you stick a **house-rules
sheet on the door**: short, clear, everyone reads it on entry.
`AGENTS.md` is that sheet, written for agents.

## Simple conventions

- **One sheet at the repo root** is enough for small projects.
- **Monorepo? One sheet per room:** each package gets its own `AGENTS.md`.
  The agent editing a file follows the nearest sheet (**closest wins**).
- Plain Markdown, no required fields. Just answer:
  how to build/test, what conventions, where the no-go zones are.
- The sheet ships with the code and changes via PR like code.
  Change the build command but forget the sheet, and the agent fails right away.
- What you type directly in chat always wins over any file. Files are just defaults.

## A starter template to copy

```markdown
# AGENTS.md — project-name
## Build & Run — `pnpm install`, `pnpm dev`, `pnpm build`
## Testing — `pnpm test`, single file: `pnpm test -- path/to/test.ts`
## Conventions — ...
## Boundaries — NEVER touch package.json without asking
```

The `Boundaries` section matters most: list what the agent must never do alone
(e.g. `NEVER... without asking`).

## Don't cram everything in — split it up

| File | Like | Read when? |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | Company handbook, everyone knows it | Every session |
| `SKILL.md` in `.agents/skills/*/` | Procedure manual per job | Only on description match |
| `*.prompt.md` | Small work ticket, fill inputs and run | On slash command |
| `*.agent.md` | Outside specialist for hard jobs | When you pick it or the main agent calls it |
| `.github/hooks/*.json` | Door locks + alarm bells | At lifecycle points (before/after tool use...) |

Two practical tips:

1. Run `ln -s AGENTS.md CLAUDE.md` so Claude Code and friends share one source.
2. For Copilot, custom agents join the shared instructions with
   `include-custom-instructions: true`. Don't copy the same text verbatim into
   both `copilot-instructions.md` and `CLAUDE.md` — it wastes tokens and drifts.

## Maintenance: treat an expired sheet as a bug

Every build/test change, stack change, or folder reshuffle — open `AGENTS.md` and fix it.
An outdated rules sheet is worse than none, because the agent fails very confidently.
