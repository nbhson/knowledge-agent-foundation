# ❓ FAQ — Anti-Patterns & Failure Modes (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).
(Glossary used throughout: a **loop** = an agent task that runs on a schedule. **PR** (pull request) = a proposed code change waiting for review. **CI** = the automated build-and-test pipeline. **Verifier** = a separate agent that checks the implementer's work. **Severity S1/S2** = S1 "annoying, no real harm", S2 "actually causes wrong work or damage".)

---

## Q1. The loop keeps auto-fixing the same pull request 5+ times and never converges — is that normal? [→ §2.1 Infinite Fix Loop]

This answer explains the "fix loop that never ends" anti-pattern: why it happens and the cap that makes it impossible.

**What you see**

The same pull request (a proposed code change, called a PR) gets a new "fix failed tests" commit every few minutes. Attempt counter: 1, 2, 3, 4, 5 — then it keeps going. Nobody merged anything. The run log fills with the same test name. In the reference repo this showed up as `stories/ci-sweeper-infinite-flaky-test.md`.

**Why**

Four causes, and only one of them is the obvious one:
- the verifier shares the implementer's session or the same model, so it "agrees" with whatever was just written;
- the root cause was never found — the loop is fixing the *symptom* ("test red") instead of the cause;
- a **flaky test** (a test that fails randomly on an unchanged codebase) was classified as a regression, so every attempt changes real code to satisfy noise. (regression = a real new bug introduced by a recent change.)

A hard cap on attempts makes this impossible. There isn't one, so the loop just keeps trying.

**What to do**

1. Set a **hard cap** — 3 attempts is the usual number — and on the 4th, stop fixing and escalate with full context written into state.
2. Separate the verifier: different instructions, different model, and make it actively hunt reasons to reject.
3. Classify every failure before fixing: is it flaky? Re-run it on the previous commit. Fails there too → flaky, not your change.
4. Record the attempt count **in the state file**, so the loop can see it already tried twice.

```
attempt_count: 2   (last: "fix: handle null in parseConfig")
on reaching 3  ->  stop, write PR #1234 to "High Priority (waiting on human)", ping Slack
```

**Verify**

Feed the loop a test that fails randomly. After 3 attempts the loop stops, the counter in the state file reads 3, and a human notification arrives — no fourth commit is pushed.

> **One-line summary:** An endless fix loop means no attempt cap — set a hard limit (3), make the verifier independent, and classify flaky failures before touching code.

---

## Q2. `STATE.md` still lists pull requests and tickets from three weeks ago — the loop keeps acting on ghosts. Why? [→ §2.2 State Rot]

This answer explains "state rot" — when the loop's memory goes stale and it wastes work on items that no longer exist.

**What you see**

`STATE.md` references a PR that was merged on Monday, a ticket closed last sprint, a branch deleted two days ago. The loop picks one up, "works" on it, and burns tokens on something that no longer exists. Severity creeps from **S1 — Annoying** (wastes time, no harm) to **S2 — Harmful** (wrong work gets done).
(Glossary: **sprint** = a short development cycle, usually 1–2 weeks. **Ghosts** = entries pointing at items that are already merged, closed, or deleted.)

**Why**

Three missing habits: nobody prunes closed items at the end of a run; the state file isn't read at the start of a run, so the loop trusts whatever it wrote last time; and three different loops append to the *same* unstructured `STATE.md` without a schema, so they overwrite each other's sections.

**What to do**

1. Prune at the end of every run, not at the start of the next one.
2. Put a `Last run` timestamp in the file and re-validate every ID against the real tracker before acting on it.
3. One state file per pattern, or clearly separated sections with explicit prune rules — never three loops free-writing one file.
4. Run `npx @cobusgreyling/loop sync .` on a schedule; it reports drift between `STATE.md` and `LOOP.md` (see [07-tools](../07-tools/)). (drift = the two files disagreeing, e.g. state lists an item the plan no longer has.)

```
## High Priority (waiting on human)
- PR #1234 — flaky test parseConfig — attempt 2 — owner: unassigned — age: 2d
<!-- anything older than 24h here raises an alert -->
```

**Verify**

Merge a PR, wait one run, then grep the state file for its number. It is gone. Delete a branch by hand — the next run reports the stale reference instead of opening a worktree for it.

> **One-line summary:** State rot = stale memory causing wasted work — prune at the end of every run, re-validate IDs, and keep one state file per loop.

---

## Q3. The verifier says "approved, looks good" and then continuous integration (CI, the automated test run) fails anyway. What's happening? [→ §2.3 Verifier Theater]

This answer explains "verifier theater" — an approval that looks like a check but isn't — and how to make verification real.

**What you see**

The loop's verifier sub-agent approves its own work. The PR merges. Then the CI run is red, or a human reviewer finds a real bug — an off-by-one, a missing null check. The verifier never ran a single test.

**Why**

This is **verifier theater**: the approval is a performance, not a check. Typical causes: the verifier prompt is vague ("looks good, approve it"), the verifier has no way to run tests or linters so it reviews by reading, and it uses the same model *and* the same conversation context as the implementer — so it inherits the implementer's assumptions, including the wrong ones. (In plain terms: it's like a code reviewer who approves by skimming, without ever pressing "run tests" — and who shares the author's same wrong assumption, so the blind spot is shared too. linter = a tool that flags style/mechanical issues without running the program.)

**What to do**

1. Make the verifier **run** the test and lint commands and paste the real output into its report. No output → no approval.
2. Change its instructions from "approve" to **"find reasons to reject."** Default stance is REJECT.
3. Give the verifier a different model or a much higher reasoning effort when the run is unattended. (reasoning effort = how "hard" the model is told to think, usually a setting.)
4. For unattended work, an approval that can't be reproduced by a human in 60 seconds is a reject.

**Verify**

Deliberately break a line of code and ask only the verifier. It must return REJECT with a failing test output, in a fresh session with no history of the implementer's reasoning. If it approves, the verifier is theater.

> **One-line summary:** Verifier theater = approval without execution — a real verifier must run the tests itself, in a fresh session, with a default of REJECT.

---

## Q4. Slack pings every 5 minutes and the team muted the bot — but last week a real escalation was missed. How do I fix it? [→ §2.4 Notification Fatigue + §2.10 Escalation Failure]

This answer explains the noise-then-missed-alarm spiral, and the notification rules that stop it.

**What you see**

Every run pings the channel, including the 14 runs that found nothing. Someone mutes the bot. Two days later nobody noticed that the loop had been stuck retrying for 9 hours on a broken CI job.

**Why**

Two failures pointing in opposite directions, both caused by the same missing rule. The loop notifies on **every run** instead of every *actionable finding*, and the "high priority" threshold is set so low that everything is high priority. Meanwhile escalation only ever gets *written into a state file* — and nobody reads that file.

**What to do**

1. Notify only when **a human decision is needed**. Report-only loops use a daily digest, not a ping.
2. Tighten triage so "high priority" means high priority; that single change kills most of the volume.
3. On escalation, ping through a connector — a Slack message, a Linear comment — so it lands where people already look.
4. Keep a `High Priority (waiting on human)` section and alert when an item there is **older than 24 hours**. That is the missed-escalation detector. (escalation = the loop handing a problem to a human.)

```
notify when  : human decision required, OR item in "waiting on human" age > 24h
otherwise    : digest (report-only) — never a ping
escalate when: attempts == cap, or verifier cannot reach a verdict
```

**Verify**

Run the loop ten times with nothing to do. Zero pings, one digest. Then make it exhaust its attempt cap — exactly one ping arrives, and it names the PR number and the attempt count. (digest = one summary message per day instead of many pings.)

> **One-line summary:** Ping only when a human decision is needed, everything else goes in a daily digest — and alert on any "waiting on human" item older than 24h.

---

## Q5. The token bill tripled overnight. Where did the money go? [→ §2.5 Token Burn]

This answer explains "token burn" — spending that scales up unnoticed — and the habits that keep cost predictable.

**What you see**

A bill spike that nobody planned for. The loop is running full sub-agent chains — implementer, verifier, reviewer — every 15 minutes, on triage output that is often empty.

**Why**

**Token burn** is severity S1 — annoying, no harm — but it is the fastest way to get a loop cancelled. Three causes: a sub-minute cadence combined with heavy sub-agents; no early exit when the watchlist turns out to be empty; and retrying the entire pipeline when the model API (the service the agent calls) returns a transient error. (transient error = a temporary failure, e.g. a network blip — retrying the *whole* pipeline for it wastes everything already done. early exit = stop immediately when there is nothing to do.)

**What to do**

1. Run a **triage-only pass first** — cheap, no sub-agents. If it finds nothing actionable, stop right there.
2. Estimate before scheduling: `npx @cobusgreyling/loop cost --pattern ci-sweeper --cadence 15m --level L2` (see [07-tools](../07-tools/)).
3. Delete the schedule when the work is done. A finished loop that keeps running is pure waste.
4. Set a **daily token budget**; hitting it pauses the loop instead of quietly spending more.
5. Retry only the failed API call, never the whole pipeline.

**Verify**

Run `loop cost` for your exact pattern, cadence and level, and write the number into `loop-budget.md`. After a week, the real spend is under that number. If it isn't, the early-exit check is missing.

> **One-line summary:** Token burn comes from fast cadence + heavy sub-agents + no early exit — cap it with a daily budget and retry only the failed call.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*