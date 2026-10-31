# ❓ FAQ — API & Integrations (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (the module overview; `§` = section number there, e.g. §7 = "Limits & Errors").

---

## Q1. My long ticket dump blows up with `ModelHTTPError: max_tokens_exceeded` — what is the limit? [→ §7 Limits & Errors]

**What you see**

You paste a full ticket thread plus a 40-page runbook into `state`, and the call fails with `ModelHTTPError: max_tokens_exceeded` (= the request is rejected because it is bigger than the model's memory window). Nothing comes back, not even an error message with a hint. The same request works fine at 60% of the size.

**Why**

`jev-1.13` has a hard total context of **64k tokens** (a token = one small word-piece a model counts; 64k ≈ 40–50 pages of text). The budget is not shared evenly: **32k is the `state` ceiling**, and the rest has to cover your questions and their framing. `state` = the text evidence you send with the request. It is meant to be *small relevant exhibits*, not the whole file. Go past 64k total and the request is rejected outright.

**What to do**

1. Measure before you send. If the state is near 32k, it is already too big.
2. Cut unrelated detail out of the state. Accuracy usually *drops* when you add more context — noise competes with evidence, like extra witnesses who saw nothing.
3. Chunk the state and run one pass per chunk, or summarize it with an LLM/your own code first, then send the summary.
4. Keep framing (tone, persona, "use only the ticket text") in `instructions` or `criteria`, never in the question text — it eats the budget without adding signal.
5. Remember the other boundary: text only. Jev cannot open attachments or read files, so anything from a file must be inlined (pasted in) by you.

> 📄 **Example code:** [`examples/01-q1-my-long-ticket-dump-blows-up-with.sh`](examples/01-q1-my-long-ticket-dump-blows-up-with.sh)

**Verify**

Send a deliberately oversized state and confirm you get `max_tokens_exceeded` back — so you know the guard is real, not silent truncation (= the model quietly dropping your text instead of erroring). Then send a 2k-character state and check the latency stays inside the 70–500ms budget and the answer does not change when you trim further.

> **One-line summary:** Jev's context is capped at 64k tokens total (32k for `state`), so send small relevant excerpts, not whole files.

---

## Q2. Confidence came back 0.88 but the answer was wrong — so is `confidence` useless? [→ §2.3 Reading the Blocks]

**What you see**

A Choice question returns `"selected": "infra"` with `"confidence": 0.88`, you auto-route the ticket to infrastructure, and it turns out to be a billing bug. You trusted the number and shipped the wrong decision.

**Why**

For Choice and Score, `confidence` is **concentration of the distribution** — a margin saying "the answer stands out from the runners-up", not a probability that the answer is factually right. Think of it as "how sure is the win", not "how likely is it true". Jev guarantees a **valid, in-schema** answer (one that fits the allowed answer format), not a correct one. Type safety and factual correctness are two different things.

**What to do**

1. Treat `confidence` as a routing signal, not a truth signal. Wire three bands and make the code obey them.
2. **High** → the code auto-acts. **Medium** → confirm or gather more context. **Low** → escalate to a human or an LLM.
3. For Noul, do the math explicitly: intrinsic confidence = `|p_yes − 0.5| × 2` (distance from a coin flip, scaled to 0–1). A `p_yes` of 0.8 gives 0.6, not 0.8.
4. Compare `selected` against the runner-up probabilities. 0.93 vs 0.02 is a real margin; 0.45 vs 0.44 with `confidence` 0.88 is not.
5. Always keep an escape hatch: a human queue, or `FallbackModel` (an LLM sitting behind Jev that takes over the step).

```
high    → code auto-acts
medium  → confirm / gather more context
low     → route to a human or another system / LLM
```

**Verify**

Replay a batch of past tickets where you know the right answer, and log the band alongside the outcome. If high-band answers are not reliably right, your bands are wrong — move the high threshold up and let more traffic fall into medium.

> **One-line summary:** `confidence` measures how far the winner is ahead of the runners-up — route on it, but never treat it as proof the answer is correct.

---

## Q3. My Pydantic AI agent raises `UserError` on a plain `flag: bool` field — what did I get wrong? [→ §4 Pydantic AI]

**What you see**

You write `output_type=Triage` with a field `risky: bool` and no description. The agent does not run — it raises `UserError` (= Pydantic AI rejects your configuration before any model call). Add a `description` to every other field and it works.

**Why**

With `TypeSafeModel`, each field of `output_type` becomes **one question**, and the field's `description` **is** the question text. A bare `bool` carries no question, so Jev refuses to guess what your field means. This is the habit inversion: with an LLM you write long instructions and hope structure appears; here you invest in field descriptions and keep instructions as light framing.

**What to do**

1. Every field gets `Field(description="…")` written as a real question.
2. Use `Literal[...]` (= a fixed list of allowed values in Python type hints) when you want a fixed answer set — Pydantic turns the literals into Choice options.
3. Nested models become namespaced questions (`outer.inner`); a `list[Item]` field fans out one question per element.
4. Move the global context into the class docstring or the agent's `instructions`.

> 📄 **Example code:** [`examples/02-q3-my-pydantic-ai-agent-raises-usererror-on.py`](examples/02-q3-my-pydantic-ai-agent-raises-usererror-on.py)

**Verify**

Every `output_type` field has a non-empty `description` — enforce it in a test. Then check the run returns all three primitives at once (`result.output.team`, `.risky`, plus a Noul and a Score field) in a single pass, not three sequential calls.

> **One-line summary:** Every output field needs a `Field(description=…)` phrased as a question — the description *is* the question Jev answers.

---

## Q4. A tool with arguments never actually runs — I see `ToolCallProposed` and `ModelAPIError`. Why? [→ §4.3 Tools Attached]

**What you see**

Your agent attaches a tool like `create_refund(amount: int)`. Jev picks the right tool, then Pydantic AI raises `ModelAPIError: ToolCallProposed` (= "Jev proposed a tool call but stopped before filling in its arguments") and the call stops. Tools that take no arguments work fine on the same agent.

**Why**

This is the expected path, not a bug. Attaching tools adds one extra question: *"which of these does the text call for?"* A no-argument tool is called **directly** on Jev's pick. A tool with arguments stops at `ToolCallProposed` — Jev routes and decides, but it does not write tool arguments. Selection also abstains (= declines to pick anything) below `typesafe_tool_call_threshold` (default **0.6**).

**What to do**

1. Accept that Jev chooses the tool, not the arguments. Do not fight this.
2. Wrap the agent in `FallbackModel`: it receives the whole step (tool plus arguments) from an LLM sitting *behind* Jev.
3. Handle `ModelAPIError` deliberately in your retry logic — retrying the same step alone will loop.
4. If tool selection matters, tune `typesafe_tool_call_threshold` and check the distributions, not just the pick.

```
text + tools ──► Jev picks tool (threshold 0.6)
   ├─ no-arg tool ──► called directly
   └─ arg tool ──► ToolCallProposed ──► ModelAPIError
                        └─► FallbackModel (LLM) does the whole step
```

**Verify**

Unit-test both shapes: a no-arg tool must execute without an LLM in the loop, and an arg tool must land in `FallbackModel` with complete arguments. Log the fallback rate — a spike means Jev is routing but the arguments are genuinely hard.

> **One-line summary:** Jev only picks which tool to call; any tool with arguments stops at `ToolCallProposed` and hands the whole step to `FallbackModel`.

---

## Q5. I make three Jev calls in a row and it takes 1.5s — can I collapse that into one? [→ §2 Request & Response]

**What you see**

Your code classifies the ticket, then checks for a refund, then scores urgency — three sequential requests. Each one costs 70–500ms, so the user waits over a second before anything happens.

**Why**

Nothing forces you to split. A request is `state` + a named `questions` map, and **all questions in one request are evaluated in parallel in one pass** (one round trip, answers computed side by side). Answers come back nested under `answers.<name>`, each with its own payload (`choice`, `score`, or `noul`). Three serial calls is the LLM habit, not a Jev constraint.

**What to do**

1. Merge the questions into one `questions` object, keeping one Choice, one Noul, one Score for the same decision step.
2. Send the state once. Do not re-send it three times with slight edits — that is the latency you are trying to remove.
3. Read each answer at its own path: `answers.team.choice.selected`, `answers.refund_requested.noul.p_yes`, `answers.urgency.score.score`.
4. Threshold the Score on its **continuous** value — 2.71 sits between levels 2 and 3; do not round it into a level and lose the signal.

> 📄 **Example code:** [`examples/03-q5-i-make-three-jev-calls-in-a.json`](examples/03-q5-i-make-three-jev-calls-in-a.json)

**Verify**

Time the merged call under real load — it should land inside the single-call 70–500ms budget, not three times it. Confirm all three answer keys are present in one response, and that Noul questions always ship a `criteria` string.

> **One-line summary:** Put all your questions in one request — Jev evaluates them in parallel in a single 70–500ms pass, so never chain calls you can merge.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md*
