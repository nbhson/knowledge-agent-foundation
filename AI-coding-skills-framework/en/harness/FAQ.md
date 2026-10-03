# ❓ FAQ — Harness Engineering (Real Stories, Plain Language)

If a question is unclear, read the section in `README.md` (named in brackets).

---

## Q1. My agent already calls the model — so what am I missing by adding a "harness"? [→ §1. What Is a Harness, in One Diagram]

**What you see**

You send a prompt, you get text back. Same prompt, two different answers. The model once edited three files, then in the next turn said it had "no record of that work". Another time it claimed a test passed and you never ran the test. You have a working demo and zero proof it works.

**Why**

Because the model call is only one arrow. A harness turns `prompt → completion` into `request → verified outcome`, and that means owning **two loops**, not one. The inner loop belongs to the runtime that hosts the model (for example Claude Code or opencode): the model asks for a tool, the harness runs it, returns the result, repeat until it stops. The outer loop belongs to you: decide, build, check, fix, write back. The folders `01`–`15` are that outer loop, unpacked.

Retrieval (find documents, paste them into the prompt — commonly called RAG) only covers the head. It ends at the **first** model call. Everything after it — plan, tools, workflow, task, evaluate, remember — is what turns a good one-shot answer into something you can ship.

**What to do**

1. Write down your outer loop on one line before you add any code.
2. Make every request end in a verdict, not in text.
3. Stop treating retrieval as the whole system.

```text
inner loop (harness runtime): LLM → tool_call → observation → LLM → stop
outer loop (you own it):      plan → execute → validate → fix → persist → evaluate
```

**Verify**

Pick one real request, e.g. *"Fix login bug"*. Walk the 10 steps in §3 and name the folder that owns each one. If you cannot name a folder for "validate", you do not have a harness — you have a prompt. If you have no verdict stored after the run, module `11` is missing.

---

## Q2. Fifteen folders for one agent — is that not overkill? [→ §2. The 7 Components → 15 Modules Map]

**What you see**

You cloned the folder, counted 15 sub-folders next to a 4-page README, and closed the tab. It feels like enterprise scaffolding for a script. Meanwhile your team demo already answers questions 80% of the time, so nobody feels the pain yet.

**Why**

Not overkill — but also not a checklist. The repo splits **7 logical components into 11 stage modules plus 4 cross-cutting ones** so each piece can be studied and tested alone. You are not meant to build 15 things. You are meant to know which 5 carry a first version.

**What to do**

1. Build the minimum: `02 + 05 + 06 + 07 + 11` — build context, prompt, tools, workflow, evaluation.
2. Add `01` / `03` when the agent must remember things between runs.
3. Add `04` / `08` when a request needs more than a couple of steps.
4. Add `09` (many agents) and `10` (runs on a schedule) last. `09` is only worth it once `04` and `07` hit their limits.
5. Never skip `12`–`15`. They wrap every stage, so there is no "later".

```text
start: 02 05 06 07 11   →  add memory: 01 03  →  add tasks: 04 08
then: 10 09             →  always wrap: 12 13 14 15
```

**Verify**

Take one arrow in the §1 diagram and point at the module that owns it. Then run a request with only your minimum five enabled: if the run finishes with a stored verdict and a recorded event, you do not need folder sixteen yet.

---

## Q3. I opened the folder and got lost — which one do I read first? [→ §5. How to Read This Folder]

**What you see**

You started with `01-retrieve-memory-knowledge` (it sounds foundational), then `09-multi-agent` (it sounds impressive), then `../HARNESS_ENGINEERING.md`, which is 40 pages. Forty minutes later you understand embeddings and nothing about your own runtime.

**Why**

Because reading order is not numbered order. `01` is where a request starts, not where you should learn. Retrieval is easy to study and hard to debug, which makes it a trap for beginners.

**What to do**

1. Read `08` first — it is the thinnest module and the README says to start there if you are lost. One trackable unit: id, status, dependencies, budget, timeout.
2. Then `07` (order, retry, compensate) → `02` (what goes in the token window) → `06` (which tool, whose permission).
3. Then the data side: `01` → `03`.
4. Then the prompt and reasoning side: `04` → `05`.
5. Finish with `11` → `10` → `09`, then the wrappers `12` → `13` → `14` → `15`.

**Verify**

From memory, write a task node and a context object. If you can, open `08/README.md` and `04` of §4 and correct yourself in one pass, the order is working.

---

## Q4. Which module do people quietly skip, and why does it blow up weeks later? [→ §4. The Three Shared Contracts]

**What you see**

Retrieval scores look great, and the agent still writes wrong code. A long run dies near the token ceiling with no error message. At night a destructive command executes with nobody watching. Afterwards nobody can tell what the run did, because there is no log to replay.

**Why**

Because two things in §2 are not stages. **Guardrails and permissions wrap every arrow** — input check, tool approval, output validation — so they never appear as a step you can tick off, so people defer them. And `12`–`15` wrap every stage too. Meanwhile `09` and `10` are genuinely optional, and skipping those is fine.

**What to do**

1. Put permission checks in `06` and untrusted-content marking in `02`/`05` on **every** stage, not only the first.
2. Add the four wrappers early: isolation (`12`), recorded runs (`13`), long-run survival (`14`), human authorization (`15`).
3. Do not cache retrieval across tasks. It re-runs whenever the query changes — a replan in `04` sends you back to `01`.

```text
fine to skip : 09 (team of agents), 10 (scheduled runs)
dangerous skip: 13 (cannot replay), 14 (dies at ceiling),
                15 (no gate on irreversible actions), 12 (no isolation)
always inline: permission check in 06 + injection marking in 05
```

**Verify**

Pick yesterday's worst run and try to replay it from its events. If you cannot, `13` was skipped. Separately, per §7, three things still have no owner anywhere — secret scrubbing, tenant isolation, cost-per-task targets — so track them yourself.

---

## Q5. The agent says "done" but the bug is still there — how do I find which stage broke? [→ §3. Request Lifecycle, End to End]

**What you see**

A clean final report: "Patched `auth.py`, tests pass." You run the tests — one still fails. You re-run the agent and get a different patch. Nothing says whether it retrieved the wrong file, put the wrong code in the prompt, called the wrong tool, or was graded by a rubric that rewards looking busy.

**Why**

Because "it worked" was never measured, and no run left a record. §4 fixes both with three shapes everyone shares: the **trajectory event** (what happened), the **built context** (what the model was given), and the **task node** (what it was supposed to finish).

**What to do**

1. Start from the trajectory, not from the code. Every step in §3 emits events.
2. If the context was wrong → module `02`. If the tool was wrong → `06`. If the run "succeeded" wrongly → `11`.
3. Score the run, not the vibe: steps used, tool precision (right tool / total calls), recovery after failure.

```typescript
kind: "prompt" | "tool_call" | "tool_result" | "plan"
    | "eval" | "memory_write" | "approval"
tokens?: { in: number; out: number };
latencyMs?: number;
```

**Verify**

Take one failed run, replay it with `03/trajectory-fork-replay.md`, and name the event id where it went wrong. Then check whether `11` has a stored verdict for it — if the verdict said "pass" while the test failed, the rubric is the bug, and §5 sends you there third.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*