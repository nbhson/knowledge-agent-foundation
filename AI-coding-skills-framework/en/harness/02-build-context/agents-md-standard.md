# AGENTS.md: the house rules on the door for every new agent

> Addendum to `harness/02` + `loop/01`.
> Open standard: https://agents.md · Steward: Agentic AI Foundation (Linux Foundation).
> ~23 tools support it. Claude Code reads `CLAUDE.md` first, falls back to `AGENTS.md` — keep a symlink to be safe.

## Picture this

This section explains what `AGENTS.md` is: a rules file that every coding agent reads automatically when it enters your repo.

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

> **One-line summary:** `AGENTS.md` is the house-rules sheet agents read on entry — plain Markdown, versioned with the code, and chat instructions always override it.

## A starter template to copy

This section gives a minimal skeleton you can paste and fill in. `pnpm` is a package manager (like npm); the commands below install, run, build, and test.

```markdown
# AGENTS.md — project-name
## Build & Run — `pnpm install`, `pnpm dev`, `pnpm build`
## Testing — `pnpm test`, single file: `pnpm test -- path/to/test.ts`
## Conventions — ...
## Boundaries — NEVER touch package.json without asking
```

The `Boundaries` section matters most: list what the agent must never do alone
(e.g. `NEVER... without asking`).

> **One-line summary:** Copy the template, and spend most of your effort on the `Boundaries` section — the "never do this alone" list.

## Don't cram everything in — split it up

This section explains which file to put what in, so the rules sheet stays short.

How to read it: column 1 is the file type; column 2 compares it to something familiar; column 3 says when the agent reads it. For instance, `SKILL.md` is a per-job procedure manual that loads only when the job description matches.

| File | Like | Read when? |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` | Company handbook, everyone knows it | Every session |
| `SKILL.md` in `.agents/skills/*/` | Procedure manual per job | Only on description match |
| `*.prompt.md` | Small work ticket, fill inputs and run | On slash command |
| `*.agent.md` | Outside specialist for hard jobs | When you pick it or the main agent calls it |
| `.github/hooks/*.json` | Door locks + alarm bells | At lifecycle points (before/after tool use...) |

Two practical tips:

1. Run `ln -s AGENTS.md CLAUDE.md` (creates a symlink — a second file name pointing at the same file) so Claude Code and friends share one source.
2. For Copilot, custom agents join the shared instructions with
   `include-custom-instructions: true`. Don't copy the same text verbatim into
   both `copilot-instructions.md` and `CLAUDE.md` — it wastes tokens and drifts
   (the copies slowly disagree, and nobody knows which is right).

> **One-line summary:** Keep the rules sheet short and move job-specific detail into skills, prompts, and sub-agent files — each with its own trigger.

## Maintenance: treat an expired sheet as a bug

This section is the upkeep rule: the file must change with the code it describes.

Every build/test change, stack change, or folder reshuffle — open `AGENTS.md` and fix it.
An outdated rules sheet is worse than none, because the agent fails very confidently.

> **One-line summary:** Every time the build, stack, or folder layout changes, update `AGENTS.md` in the same change — a stale sheet causes confident failures.

## October 2026 Update — Precedence & Monorepo Example

This section adds two things: which rules file wins when several exist, and a full monorepo skeleton (a monorepo = one repository holding many packages).

> Adds a precedence table across per-tool "rules sheets", plus a complete
> `AGENTS.md` skeleton for monorepos you can copy in one go.

### 1. Precedence: one source of truth, several variants

`AGENTS.md` is the **open standard** (agents.md, maintained by the Agentic AI
Foundation under the Linux Foundation). `CLAUDE.md`, `GEMINI.md` and
`copilot-instructions.md` are **per-tool variants** — same substance, different
file names, each looked up by its own tool:

How to read it: column 1 is the file; column 2 is its role; column 3 says what belongs in it. For instance, `CLAUDE.md` should only summarize or link back to `AGENTS.md`, not hold its own copy of the rules.

| File | Role | Should contain |
|------|------|----------------|
| `AGENTS.md` | **The root** — open standard (Linux Foundation), read by ~23 tools | The full, real rulebook |
| `CLAUDE.md` | Per-tool variant (Claude Code reads it before AGENTS.md) | Summary / symlink / import from the root |
| `GEMINI.md` | Per-tool variant | Summary / symlink / import from the root |
| `.github/copilot-instructions.md` | Per-tool variant (Copilot) | Summary + `include-custom-instructions` |

**Principle: a single source of truth.** The real rules live only in `AGENTS.md`;
the per-tool files are just summaries, symlinks or references back to it. Copying
the same content verbatim into both creates two sources of truth — they will
drift, and once they do, nobody knows which one is correct.

### 2. Example: `AGENTS.md` Skeleton for a Monorepo

This skeleton is copy-paste ready. Read the tree first: `apps/` holds deployable apps, `packages/` shared libraries, `scripts/` operations scripts.

```markdown
# AGENTS.md — acme-monorepo

## Overview
pnpm monorepo: apps/ (deployable apps) + packages/ (shared libraries)
+ scripts/ (ops). An agent editing a file reads the nearest AGENTS.md there.

## Global Rules (apply to every package)
- Package manager: pnpm — NO npm/yarn, NO hand-editing pnpm-lock.yaml.
- Node 22, TypeScript strict — do not disable `strict` in child tsconfigs.
- Commits: conventional commits (`feat:`, `fix:`, `chore:`).
- NO force-push, NO deploys that bypass CI.

## Build & Test
- Build all: `pnpm -r build` · Test all: `pnpm -r test`
- Test one package: `pnpm --filter <pkg> test`

## apps/web
Next.js 15; route handlers live in `app/api/`. NO cross-imports from apps/admin.
Package-specific details: see `apps/web/AGENTS.md`.

## packages/ui
React + CSS modules design system. NO new dependencies without asking.
Every component needs a story + a test.

## scripts/
Run with Node, NO `curl | sh`. Any script touching the prod DB takes its
connection string from env — never hardcode credentials.
```

Precedence structure once this file lands in a monorepo:

```
acme-monorepo/
├── AGENTS.md            ← root: overview + global rules (every agent reads it)
├── apps/web/AGENTS.md   ← overrides/additions for the web package
├── packages/ui/AGENTS.md
└── scripts/AGENTS.md
```

How to read the tree: the root file holds global rules; each sub-folder file adds or overrides rules for that package only.

> **One-line summary:** One rulebook (`AGENTS.md`) + per-package files that override locally — never two full copies of the same rules.

### 3. Two Rules, Restated

1. **"Nearest file wins"** with nesting: an agent editing `apps/web/src/x.ts`
   obeys `apps/web/AGENTS.md` first; the root `AGENTS.md` is just the shared
   baseline. Put package-specific rules in the nearest file — don't pile
   everything onto the root.
2. **Stale AGENTS.md = bug.** Change a build command, a stack, or the folder
   layout and forget to update `AGENTS.md`, and the agent fails *very
   confidently* — see [Maintenance](#maintenance-treat-an-expired-sheet-as-a-bug)
   above. Change this file via PR, in the same PR as the code it describes.

> **One-line summary:** Nearest file wins, and a stale `AGENTS.md` is a bug — update it in the same PR as the change it describes.

### 4. Links

- [README.md](README.md) — Harness Module 02 (Build Context), where this file is an appendix.
- [AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md) — the 9-layer architecture overview.
