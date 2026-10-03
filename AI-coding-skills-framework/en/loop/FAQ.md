# ❓ FAQ — Loop Engineering (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. What is a "loop" — is it just fancier prompting, or a workflow? [→ Why Loop Engineering Matters / Overview]

**What you see**

You keep doing the same thing: type a prompt, wait, read the result, fix the prompt, type it again. Same mistakes come back every session. You're exhausted and nothing is reusable.

**Why**

Three things are being confused:
- **Prompting** — you type each command, the agent does each task.
- **Harness** — the environment one agent runs in: its tools, its context, its permissions.
- **Loop** — harness **+ schedule + state + verification chain**. It runs repeatedly and maintains itself.

The shift is real: you're no longer writing prompts, you're designing control systems. A loop **discovers** the work on its own, **assigns** it, **verifies** it, and **keeps its own state** outside any single conversation. That durable state is the whole difference — it's why the loop remembers what happened last Tuesday.

**What to do**

1. Read one loop end to end: `Schedule → Triage → State → Worktree → Implementer → Verifier → Human Gate → Commit/PR/Escalate`.
2. Know your five building blocks: Automations, Worktrees, Skills, MCP, Sub-agents — plus State, which holds it all together.
3. Start with a **short cadence and a small job**. The cadence is the part people get wrong: a loop that runs every 30 seconds will spend your tokens and your attention.

```
Loop = Harness + schedule + state + verification chain
Result = the agent decides what is worth doing, checks its own work, learns from it
```

**Verify**

Close the chat, wait for the next scheduled run. If it picks up work, checks it, and writes what happened to a file you can read afterwards — that's a loop, not a prompt.

---

## Q2. Is this real, or is it just the current hype? What is the actual evidence? [→ Why Loop Engineering Matters — 3 Pieces of Evidence]

**What you see**

You're being asked to invest days in loops, and everyone you talk to says "agents are changing everything." You want to know whether the loop pattern specifically does anything.

**Why**

Three published results, and they measure different things:
1. **DeepMind (2025)** — agents with structured feedback loops cut **recurring errors by 52%** versus agents without loops.
2. **Anthropic (2025)** — self-refine loops in Claude Code raised **code quality by 38%** on the SWE-bench benchmark.
3. **The loop-engineering reference repo (2026)** — dogfoods its own patterns: the `loop-audit` workflow grades a **Loop Ready score** on every pull request and push, reaching **5.5k+ GitHub stars in 6 months**.

Note what these do *not* claim. None of them says a loop replaces you.

**What to do**

1. Read the three results, then be honest about which one you were already convinced by.
2. Judge your own loop on a **quality bar plus time saved**, not on volume of output.
3. Keep the measurement honest: the readiness score goes up when you scaffold correctly, and it caps at L3 until a budget, a run log, and written rules exist.

**Verify**

Pick one loop you already run. Record the number of manual fixes per week before and after four weeks of running it. If time went down and defects didn't, the evidence applied to you.

---

## Q3. Should I let the agent run unattended (L3) right away? [→ Autonomy Levels L1 → L2 → L3]

**What you see**

You're tempted to go straight to full automation: the loop discovers work, writes code, and merges without asking. The reference repo has four patterns at **L1** and three at **L2** — and all three L2 ones are **paused**. Not one pattern runs unattended.

**Why**

The levels are a staircase, not a switch:
- **L1 Report** — the loop finds and writes up work. It changes nothing. Week one belongs here.
- **L2 Assisted** — it does the work, but a human gates the risky decisions.
- **L3 Unattended** — no human in the loop. Only earned.

Skipping a rung means acting on bad signal before you know whether your triage is any good. Measure triage accuracy at L1 for a week before you enable L2.

**What to do**

1. Week one at L1, report only. Never L3 first.
2. Before L2: check your triage accuracy, then enable L2 on one pattern.
3. Write the pause and kill criteria down **before** you need them, plus a budget template.
4. Give every pattern at least one explicit human gate, even L1 reporting.

```
L1 report  -> L2 assisted -> L3 unattended
week 1 at L1. measure triage. then L2 on one pattern. L3 last.
```

**Verify**

At L1 for seven days, count the reported items a human actually agreed were real. If accuracy is low, you have a triage problem — more autonomy makes it worse, not better.

---

## Q4. There are 7 directories here. Where do I actually start, and in what order? [→ Learning Path / Recommended Path]

**What you see**

`01-concepts` through `07-tools`, plus seven pattern files. You opened `02-patterns/pr-babysitter.md` first, got lost, and closed the tab.

**Why**

The order is deliberate: concepts before patterns, safety and operating **before** a real schedule, multi-loop and anti-patterns only when you're scaling, tools last because the tools automate what you should already understand.

**What to do**

1. Step 1 — this file, for context.
2. Step 2 — `01-concepts/`: the five building blocks, anatomy, L1–L3, the taxonomy.
3. Step 3 — `02-patterns/`: pick your first pattern. The docs suggest **Daily Triage at L1**.
4. Step 4 — `03-safety/`: the loop design checklist and guardrails.
5. Step 5 — `04-operating/`: budget and logging, before any real schedule.
6. Step 6 — `05-multi-loop/` + `06-anti-patterns/`, when you're scaling to many loops.
7. Step 7 — `07-tools/`: use the CLI to scaffold and audit.

**Verify**

You can answer one question per step without opening another file: what are the building blocks, which pattern, is it safe, what does it cost, do the loops collide, what goes wrong, which command do I run.

---

## Q5. Ship velocity is way up and nobody can explain last week's changes. Is that bad? [→ Real-World Case Studies / Cognitive Surrender]

**What you see**

More PRs merged than ever. Review time collapsed to a rubber stamp. When something breaks, nobody — including the person who approved it — can explain why the change was made.

**Why**

This is **comprehension debt**, and it compounds quietly. Three causes: humans stopped actually reading the loop's output, the auto-merge allowlist grew to cover more and more paths, and there was no weekly human synthesis. The success metric became *volume* instead of quality.

**What to do**

1. Mandatory human review for any non-trivial PR. Cap auto-merge to genuinely trivial paths.
2. A weekly **loop digest** where a human writes what the loops actually changed and why.
3. Measure success as time saved **with** a quality bar attached — never merged PRs alone.
4. Watch for **cognitive surrender**: the moment the answer to "is this correct?" becomes "the loop handles it."

```
weekly: loop digest written by a human
trivial paths -> auto-merge allowed
everything else -> a named human reads the diff and the verifier output
```

**Verify**

Pick any PR merged last month. The author can explain the change and the evidence that verified it, in one minute. If they can't, comprehension debt is already being paid — pull the auto-merge allowlist back.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*