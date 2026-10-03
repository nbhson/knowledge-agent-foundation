# ❓ FAQ — AutoGen (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. AutoGen, CrewAI or LangGraph — I only have time for one, which do I pick? [→ Why AutoGen Matters?]

**What you see**

You open three READMEs and they all look the same: several named agents, a plan, a critic, an executor. You cannot tell from the code samples which one you would regret less in six months. The trap is picking on vibes: someone on a forum said LangGraph "feels cleaner", so you start there — and two weeks later you are hand-writing state reducers for something that was always a fixed pipeline.

**Why**

They solve three different shapes of the same problem, and the shape is the decision, not the library.

| Shape | Framework | You get |
|---|---|---|
| Agents must argue until they agree | AutoGen | `GroupChat` + a manager picks who speaks next |
| Each worker has one fixed job | CrewAI | `Agent(role=..., goal=...)` + `Task` |
| The flow has branches and loops | LangGraph | `StateGraph` + `add_conditional_edges` |

AutoGen's core idea is a **conversation**. `User → UserProxyAgent → AssistantAgent (calls tool) → UserProxyAgent (runs code) → AssistantAgent` — agents exchange messages until someone replies to the user. That is the right fit when the number of steps is not known in advance, for example a critic that keeps sending work back to a coder. It maps straight onto `harness/09-multi-agent`.

**What to do**

1. Count your steps before writing code. Fixed order, known count → do not use a conversation framework; a linear pipeline is easier to debug and cheaper.
2. If you must have open-ended back-and-forth (plan → code → review → fix → review), start AutoGen at the smallest shape: one `UserProxyAgent` + one `AssistantAgent`, then add a `Planner` and a `Critic` as plain `AssistantAgent` objects with a `system_message`.
3. Reach for `GroupChat` only after two agents already work. The manager is a model deciding who speaks — one more model call per round.
4. Read `HARNESS_ENGINEERING.md` section 9.1 first. The AutoGen sample there is already written for this repo, and copying a working pair beats assembling your own.

**Verify**

Run the two-agent pair on one tiny task ("write a function that reverses a string"). You should see exactly one tool call, one code execution, and one final reply to the user. If the transcript shows more than a handful of messages, your agents are negotiating instead of working.

---

## Q2. The agents talk to each other forever and my bill goes up — how do I stop it? [→ GroupChat — Multiple Agents]

**What you see**

A run that was supposed to take 30 seconds reaches round 14. The planner asks for a plan, the coder writes code, the critic finds a nit, the coder "fixes" it, the critic finds another nit. `planner` and `coder` keep trading the same two sentences. You kill the process and find `max_round=20` in your `GroupChat` — you were one step from the ceiling you set yourself, and you never noticed the pair had deadlocked.

**Why**

A conversation has no natural end. Two caps exist and you must set both. `max_round=20` in `GroupChat` is the hard ceiling on **group rounds**. `max_consecutive_auto_reply=10` on `UserProxyAgent` is the cap on **one agent replying repeatedly without a human**. If neither is set, an "auto" speaker selection can pick the same pair forever, because from the manager's point of view every message looks like forward progress.

**What to do**

1. Set `max_round` to the smallest number that completes your happy path. Measure it once on a known task, then set the cap slightly above it.
2. Give the critic a stopping condition in its `system_message`: "approve when the only remaining notes are stylistic". A critic with no exit criteria never approves.
3. Make the coder answer only concrete objections. If its reply starts with "You're right, I'll fix", the loop is healthy; if it rewrites the same file with the same content, break the loop.
4. Add a repeat detector on the last message of each agent. Two identical messages in a row → force `END`.
5. If you use `speaker_selection_method`, `"auto"` is a model call per round. `"round_robin"` is free and predictable — use it while debugging.

```python
group_chat = GroupChat(
    agents=[planner, coder, critic],
    messages=[],
    max_round=12,
    speaker_selection_method="round_robin",
)
```

**Verify**

Run the same task three times and compare round counts. If they differ by more than two rounds, the run is not deterministic — pin the model and the speaker selection method. No single run should ever reach `max_round`.

---

## Q3. `human_input_mode="NEVER"` — is it safe to let the harness run with nobody watching? [→ Sample Code From HARNESS_ENGINEERING.md]

**What you see**

You copy the sample from `HARNESS_ENGINEERING.md`, it runs the first task perfectly, and you leave it on while you get coffee. The `UserProxyAgent` writes a file into `work_dir="coding"`, then rewrites it, then a third time. Nobody notices for forty minutes. The word "NEVER" in the code reads like a safety setting; it is actually the opposite.

**Why**

`human_input_mode` controls **when a human is asked**, nothing else.

| Value | Behaviour | Use for |
|---|---|---|
| `"NEVER"` | runs to the limit, no prompts | read-only or throwaway work |
| `"TERMINATE"` | stops only to ask confirmation | production, migrations, anything destructive |
| `"ALWAYS"` | asks before every step | learning, first runs |

`"NEVER"` plus `code_execution_config={"work_dir": "coding"}` gives the agent a shell and a writable folder with no human in the path. That is a fully automatic code writer. It is fine for a scratch directory and dangerous everywhere else, because the agent has no way to ask "are you sure?".

**What to do**

1. Start every new integration on `"ALWAYS"` or `"TERMINATE"`. You cannot debug what you never see.
2. Point `work_dir` at a throwaway directory outside your repository, never at `src/`.
3. Turn `code_execution_config=False` for any task that only needs conversation — planning, review, explanation.
4. Move to `"NEVER"` only for tasks where a full rewrite is acceptable and the output directory is disposable.
5. Log every run's message list. If you cannot replay the transcript, you cannot explain the run.

```python
safe = UserProxyAgent(
    name="harness",
    human_input_mode="TERMINATE",
    code_execution_config=False,
)
```

**Verify**

Run one sensitive task and confirm the process stops and waits for you. If it never pauses, `human_input_mode` is `"NEVER"` and your run is unattended — change it before proceeding.

---

## Q4. How much does one conversation actually cost — and why is it more than I estimated? [→ Sample Code From HARNESS_ENGINEERING.md]

**What you see**

Three agents, a twelve-round conversation, and a cost roughly four times your estimate. The single-agent version of the same task cost a fraction of it. Nothing crashed, nothing looped; you simply paid for the same conversation several times over.

**Why**

In a conversation framework the **whole message history is resent on every model call**. Round 1 is cheap. Round 12 sends the plan, the code, the critique, and all ten previous exchanges again — to whichever agent is speaking. With three agents and twelve rounds you get roughly 36 model calls, and the late ones carry the full transcript. Token cost per round grows with the round number, not with the work done. The README's own roadmap lists "Token cost per conversation round" under `04-savings`, because this is the known cost shape of the pattern.

**What to do**

1. Count agents × rounds to estimate calls before you run. `agents × max_round` is your ceiling.
2. Lower `max_round` first. Rounds are the cheapest dial to turn.
3. Keep every `system_message` short. It is resent on every single call, so a 400-word persona costs 400 words × every call.
4. Measure with the two-agent pair first, then decide whether the critic is worth its price on your actual task.
5. Use `"round_robin"` while measuring — it removes one model call per round from the total.

**Verify**

Log input and output token counts per call for one run. Cost per round should be visible as a rising line. If a single call is more than 3× the median, the transcript has grown past what your model window needs and the fix is fewer rounds, not a bigger context window.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*