# ❓ FAQ — CrewAI (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. My agents keep doing each other's jobs — the "Reviewer" writes code anyway. How do I fix that? [→ Three Core Concepts]

**What you see**

You build a `Reviewer` agent and it returns a rewritten, working login endpoint instead of a review report. The `Planner` starts writing the implementation. Your `Task(description="Review code", expected_output="Review report")` is technically satisfied — you got code, plus prose — so the crew reports success and moves on.

**Why**

Because `Task` is not enforced as a contract; it is **a string handed to a model**. A `Task` has only three fields: `description`, `expected_output`, and which agent runs it. The agent has its own `role`, `goal`, `backstory`, and `tools`, and tools are what actually decide what is possible. If the Reviewer has no tools, it cannot edit files no matter how the task is worded — but if you copy-pasted the same `tools=[code_editor]` onto every agent, the role text is only a suggestion and the tool is a fact.

**What to do**

1. Give each agent **the minimum tool set for its role**. Reviewer with no editor tools; only the Coder gets `tools=[code_editor]`.
2. Write `expected_output` as something you can check mechanically — "a numbered list of `file:line` findings", not "a review".
3. Write `backstory` as a boundary, not a biography: "you never write or modify files; you only report".
4. Split one crew, not one agent. If you need review *and* a fix in the same step, that is two tasks with an explicit hand-off.

```python
reviewer = Agent(role='Reviewer', goal='Find bugs and security issues',
                 backstory='You never modify code, you only report findings',
                 tools=[])
review_task = Task(description='Review the login API code',
                   expected_output='Numbered list of file:line findings')
```

**Verify**

Print the `expected_output` of every task and check that no two tasks share the same string. Then remove one agent's tools and confirm it can no longer produce the neighbouring role's output.

---

## Q2. `Process.sequential` or `Process.hierarchical` — which one should I ship? [→ Process: Sequential vs Hierarchical]

**What you see**

You build a three-agent crew with `Process.sequential` for "Implement login API with rate limiting". It works. Then you add a fourth capability and the crew starts skipping the review task, because the plan changed and nothing forces the reviewer. You switch to `Process.hierarchical` and now a manager agent appears in the logs, re-assigning tasks at run time — and you can no longer predict the order.

**Why**

The process is your **execution order policy**, and each option buys you one thing and costs you one thing.

| Option | You get | You pay |
|---|---|---|
| `Process.sequential` | fixed, replayable order | no re-planning mid-run |
| `Process.hierarchical` | a manager re-assigns work | one more model per decision, no fixed order |

Sequential maps to `harness/07-workflow` (a pipeline); hierarchical maps to `harness/09-multi-agent` (an orchestrator over workers). Neither is "more powerful" — they are different guarantees. Sequential gives you a trace you can diff between runs. Hierarchical gives you recovery when the plan has to change.

**What to do**

1. Ship sequential first. If every run is the same shape of work, you do not need a manager.
2. Add `manager_agent` and `manager_llm` only when a task's scope genuinely changes at run time, and expect to pay for a model call each time the manager decides something.
3. With sequential, make each `Task`'s `expected_output` explicit, because there is no manager to repair an incomplete step.
4. Keep the task count small. Every extra task is another sequential stage, another possible failure point, another token bill.
5. Document which process you chose in the crew's config, so the next person does not "improve" it into hierarchical by accident.

**Verify**

Run the crew twice on the same input and compare the order of executed tasks. Sequential must produce an identical order both times. If the orders differ, you are on hierarchical and your evaluation should account for that.

---

## Q3. The crew will deploy to production — can I stop it before the damage? [→ 2. Human-in-the-Loop]

**What you see**

Someone on the team adds a fourth task to the crew:

```
Task(description="Deploy to production", expected_output="Deployment confirmation")
```

They run it. The crew plans, writes code, reviews, and then deploys in one go with no pause, because the crew executes every task in the list. The reviewer never saw the deploy step — it happens after review, and nobody was asked.

**Why**

Because `human_input` is **per task, and defaults to off**. A crew is a list of tasks; a task runs when its turn comes. If the task that needs a human says nothing about a human, the crew assumes there is none. This is the opposite of AutoGen's `human_input_mode`, where you set the human policy once on the agent — in CrewAI the gate lives on the task, so a new task added without the flag silently removes your approval step.

**What to do**

1. Put `human_input=True` on every task that changes something outside the workspace: deploys, migrations, deletions, anything that costs money or sends messages.
2. Treat a missing `human_input=True` on a destructive task as a review-blocking finding, same as a missing test.
3. Add the approval gate to the last task in the list, not the first, so the crew has done all its work before it stops.
4. Keep read-only tasks (`Plan the login API`, `Review code`) without the flag, or the crew will stop constantly and nobody will read the pauses.
5. Write the expected output so the pause shows the human what will happen: "Deployment confirmation listing the exact commit".

```python
deploy_task = Task(
    description="Deploy the reviewed commit to production",
    expected_output="Deployment confirmation with the commit SHA",
    human_input=True,
)
```

**Verify**

Run the crew with an empty `mcpServers`-free sandbox and confirm it blocks on the deploy task and prints the commit before doing anything. If it completes end to end with no pause, the flag is missing.

---

## Q4. Why does adding one more agent double my token bill? [→ Why CrewAI Matters?]

**What you see**

A two-agent, three-task crew costs a manageable amount per run. You add a fourth agent — a "Security Reviewer" — and the per-run cost roughly doubles, not by 50%. The number of tasks stayed at three. Nobody changed any prompt.

**Why**

Because in CrewAI cost scales with **agents × tasks**, not with tasks alone. Every task in a crew runs through an agent that carries a full `role` + `goal` + `backstory` persona, and that persona is sent on every model call that agent makes. An extra agent also tends to bring extra tasks with it (plan, do, review, security-review), and each new task is another full model call plus the whole preceding task's output in its context. Your roadmap lists "Token usage + cost per crew run" under `04-savings` for exactly this reason.

**What to do**

1. Count tasks first. Tasks are your primary cost unit — adding an agent that owns one task costs roughly one extra call plus its persona.
2. Trim every `backstory` to one or two lines. It is resent on each call that agent makes.
3. Ask whether the new agent needs its **own** task or can be part of an existing one. One Reviewer that checks logic *and* security is often cheaper than two reviewers.
4. Measure before and after on one fixed task. Keep the numbers; without them you are guessing.
5. If cost is the blocker, reduce tasks rather than agents — a shorter sequential crew keeps the ordering guarantees you already chose.

**Verify**

Record input and output tokens per task for one run. Every task should show a cost close to its predecessor. If one task costs 5× its neighbours, it is carrying a large context payload from earlier tasks and is the place to cut.

---

## Q5. Agents hand work to each other and then forget it — where does crew memory come from? [→ Three Core Concepts]

**What you see**

The Coder implements the login API. The Reviewer asks for a specific fix. The fix is applied — and then the final report describes the original, unrevised implementation. Or two agents produce contradictory statements about a decision ("we agreed to use JWT" and "we agreed to use sessions") and both are true in their own context.

**Why**

Because an `Agent`, a `Task`, and a `Crew` define **shape**, not shared history. Each task hands its output to the next one; there is no automatic store that both agents read and write. When you split work across agents, each one sees only what was passed forward. If a decision mattered, it must live in the `Task` description or the `expected_output` — otherwise it dies between stages.

**What to do**

1. Put every decision in `expected_output`, not in the task description alone. A decision that is not an output is not passed on.
2. Write task outputs as data, not prose. A file path, a command, a version number — anything a later agent can read rather than interpret.
3. When an agent needs to remember across **separate crew runs**, wire an explicit store in; the crew does not create one.
4. Keep the number of hand-offs small. Every hand-off is a place to lose context.

**Verify**

Run the crew, then ask the final agent one question only answerable from the first task's output. If it cannot answer, the hand-off dropped it and `expected_output` needs to be more concrete.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*