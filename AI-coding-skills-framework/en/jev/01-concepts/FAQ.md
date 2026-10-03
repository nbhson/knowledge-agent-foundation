# ❓ FAQ — Jev & System One Models (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. The endpoint looks exactly like an LLM (large language model) call — JSON over HTTPS, Bearer key, a model name. So is Jev just a small, fast LLM? [→ §1 What Is Jev?]

**What you see**

You send `POST https://api.typesafe.ai/v1/systemone` with `"model": "jev-latest"`, an `Authorization: Bearer …` key, and a JSON body. It comes back in a few hundred milliseconds. Your teammate says "so this is just a tiny LLM, right? Can it write the migration script for us?" — and you stop, because the answer is no.

**Why**

Jev is a transformer, but it was never trained to emit text or tokens. You hold two facts at once: **it looks like an LLM call and it behaves like a calibrated decision function.** It looks like one because the plumbing (JSON over HTTPS, bearer key, model name) is the same. It behaves differently because it has no text output at all — it returns typed answers (`Choice`, `Score`, `Noul`) with a full probability distribution. It cannot write tool arguments, read files, or explain itself.

**What to do**

1. Stop judging models by their transport. Judge them by the shape of your question.
2. Route on question shape: a finite answer set that repeats → Jev; sentences or open invention → the LLM; arithmetic, counting, dates → plain code.
3. Say it out loud in your design review so nobody files the "just use the LLM" ticket: you are choosing an engine, not a brand.

```json
{ "model": "jev-latest",
  "state": "Ticket #4821: charged twice after plan upgrade…",
  "questions": { "team": { "type": "choice",
    "options": ["billing","infra","bug","other"] } } }
```

**Verify**

Send a request whose question is "explain why this failed". You get a typed answer plus probabilities — never prose. Send a state asking it to count and read Q2 next.

---

## Q2. Jev answered my math wrong — I asked "how many rows failed?" and "is March 1 before Feb 28?" and it said yes. Do I need a bigger model? [→ §1.2 What It Is NOT / §6.1 The Big Table]

**What you see**

You send a diff and ask which files changed. You ask whether two dates are in order. Both come back wrong, and the answer was not shy about it. Meanwhile the same call correctly routed a support ticket to the right team. The pattern is confusing until you see the boundary.

**Why**

Jev is explicitly **not reliable at arithmetic, counting, or date comparison.** It has no autoregressive text loop, which means it has no chain of thought to add numbers up with — nothing is written down and summed. Its training (RLCD, Reinforcement Learning for Calibrated Decisions) optimizes probabilities against *outcomes* of semantic judgment, not arithmetic steps. There is also a hard context ceiling: 64k total = 32k state + your longest question.

**What to do**

1. Move every mechanical step into code — `git diff --name-only`, `len()`, `dateutil` — and let Jev handle only the judgment part.
2. If you need both, split the request: code computes the count, Jev rates whether that count is alarming.
3. Never widen the state hoping the model will notice a pattern the code already knows exactly.

```python
changed = subprocess.run(["git","diff","--name-only"]).stdout.split()
# judgment (semantic) -> Jev  |  counting, dates, diffs -> code
```

**Verify**

Run 20 known-answer arithmetic questions against the model. You should expect failures — that is the design, not a bug. Then re-run your *classification* questions; those should hold.

---

## Q3. At 2 a.m. the LLM returned `"urgency": "high!!"` and my enum only has four levels. Can Jev actually guarantee my schema holds? [→ §5 Why Give Up Text Generation?]

**What you see**

The production log shows a parse failure, then a retry, then a second failure: the model returned `"urgency": "high!!"` with two exclamation marks. Yesterday it invented a sixth severity level that is not in your enum at all. Someone added JSON mode, constrained decoding, and a retry wrapper, and it still breaks in production.

**Why**

On a large language model, a schema is a *hope* — you prompt for it, constrain it, retry it. The costs of strings are real: every hedge and newline is billed, one token at a time takes 3–329s to reach a boolean, and parse errors, hallucinated values, and fake calibration all leak in. Jev surrenders text generation, and the answer space is closed **by construction** — `Choice` up to 255 options, `Score` 2–10 levels, `Noul` binary.

**What to do**

1. Stop parsing strings; read typed fields that arrive already typed.
2. Define your levels/options as data and reuse the exact same scale on every request, so comparisons across runs are valid.
3. Ask only for what a distribution can hold — a level or a probability, never an adjective plus an exclamation mark.

```json
"urgency": { "type": "score",
             "levels": ["calm","annoyed","angry","blocked"] }
```

**Verify**

Ask for a 4-level score and confirm every answer lands in those four. Try adding a 301st option and confirm the request is rejected rather than silently truncated.

---

## Q4. I pasted our whole 40MB log file into `state` because "more context is better" — accuracy went down and latency hit 500ms. What did I do wrong? [→ §6.3 State Hygiene]

**What you see**

You believed more context helps, so you dumped the entire incident log into the state field. Accuracy on the routing question dropped. Every call now sits near the top of the latency range. The bill went up too: input is priced at $0.042 per million tokens, and your state is mostly lines that have nothing to do with the decision.

**Why**

**Jev judges the state you send — and accuracy falls when the state carries unrelated detail.** Nothing summarizes the irrelevant parts for you; they compete with the signal. You also hit the 32k state cap, so the part that mattered may simply be gone. The principle is simple: *exhibit, not archive*.

**What to do**

1. Build the smallest state that still answers the question — the one paragraph the decision depends on.
2. Strip identity noise, but keep the phrasing the decision turns on ("charged twice", "explicitly asks for money back").
3. Cut `state` first when latency or cost grows; add lines back one at a time only if a test proves they help.

```python
state = f"{ticket.subject}\n{ticket.last_3_messages}"
# ~400 chars, not 40 MB — then ask "team" / "urgency" / "refund"
```

**Verify**

Run the same 50 questions against a full log and against a trimmed state. Compare the distributions, not just the top choice. The smaller state should win or tie.

---

## Q5. My pipeline is 100% LLM and it works fine. Should I replace the LLM with Jev everywhere? [→ §6 When to Use / When NOT / §7 Place in the Agent Ecosystem]

**What you see**

One frontier model handles everything: triage, verification, drafting the reply. Each decision-shaped call takes seconds, output tokens are billed, and when you need a threshold you find the model wrote "I'm highly confident" — a sentence, not a number you can compare against `0.8`.

**Why**

There is a continuum: deterministic code → **Jev** (narrow semantic judgment) → LLM (open language). Confusing the layers costs twice — once in tokens, once in latency — and you still cannot tell whether your `0.8` means anything. Jev is not trying to replace the expensive model. The Jevons paradox applies: when intelligence gets cheaper, you ask more questions, not fewer. The 4 target workloads are decision steps in workflows, map-reduce over big datasets, real-time paths, and verifying LLM output.

**What to do**

1. Hammer, screwdriver, power drill: pick per question, not per project.
2. Best first swap — LLM writes, Jev verifies: the LLM drafts, a `Noul` gate checks it against a rubric.
3. Watch calibration as you go: roughly 80% of answers scoring `0.8` should be correct. If not, trust the routing, not the number.

```text
finite answer set + repeats often  -> Jev
needs sentences / open invention  -> LLM
mechanical (math, dates, parsing)  -> plain code
```

**Verify**

Before/after on one workflow: p95 latency, dollars per 1,000 decisions, schema failures, and the calibration check above. If only latency improved and nothing else, you moved the wrong question.*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
