# ❓ FAQ — The Three Primitives: Choice, Score, Noul (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. I hid my question inside the state — "…please classify this as billing" — and the answers got worse. What did I break? [→ §6.2 TypeSafe's Best-Practice Split]

**What you see**

You send `state` containing both the ticket and your instruction:

```
state: "Ticket #4821: charged twice after upgrading to Pro. Please classify this as billing."
```

The reply still looks fine — `probabilities` come back `{"billing": 0.91, "infra": 0.02, ...}` — but your thresholds stop meaning anything. Raising the "should I auto-route" line from `0.8` to `0.9` changes almost nothing, and a ticket that is clearly a bug still comes back as `billing`. Meanwhile a `confidence` of `0.87` on a state that also contains your instruction is not a number you can trust in calibration testing.

**Why**

`state` is only the material being judged — the evidence. Stuffing the question in there contaminates that evidence, and accuracy falls when the state carries detail unrelated to the decision. The question belongs on the output type or in the `questions` map, never in the evidence packet.

**What to do**

1. Put the question on the field/output type plus its description — that pair *is* the decision.
2. Put the framing (tone, persona, "answer as if you were…") in the docstring or instructions.
3. Put "yes only if…" rules in the `criteria` field of a Noul question.
4. Strip the state back to evidence only, then re-measure.

**Verify**

Send the same ticket twice — once with framing in the state, once with a clean state and a real question. Compare the probability spread and the confidence. The clean version should be more peaked and more stable across repeats.

---

## Q2. Choice returned `confidence: 0.87` and the answer was still wrong — my code was supposed to make that impossible [→ §2.1 Contract, §2.5 Pros / Cons]

**What you see**

A double-charge ticket routes to `infra`. You print three fields and stare at them:

```
selected      "infra"
probabilities {"billing": 0.44, "infra": 0.48, "bug": 0.05, ...}
confidence    0.87
```

The distribution is peaked — one option clearly ahead — and yet `billing` was the right owner. Meanwhile the thing you *thought* the type system bought you, "an out-of-schema value like `billing-ish` can never appear", was never the real risk. The answer was inside the schema and still wrong.

**Why**

`confidence` is a **margin**: how concentrated the distribution is. It is not the probability that the answer is correct. Type safety means the output shape is valid — it says nothing about factual correctness.

**What to do**

1. Stop reading confidence as truth; read it as "how peaked was this". Gate on the band, not on the value.
2. Set three bands and pick thresholds from your own calibration data, not from a hunch.
3. Watch `P(other)` as a health signal: a spike means your option list no longer matches reality (taxonomy rot), not that the model got lazy.
4. Route the low band to a human or to a language model instead of forcing a pick.

```python
if team["confidence"] >= 0.8:
    route(ticket, team["selected"])                   # auto-act
elif team["confidence"] >= 0.5:
    route(ticket, team["selected"], confirm=True)     # confirm / more context
else:
    escalate_to_human(ticket)
```

**Verify**

Pull the last 200 misrouted tickets and check which band they landed in. If most were in the auto-act band, your threshold is too low — not the model. If answers at `0.8` are correct only ~60% of the time, move the line.

---

## Q3. My anger score came back `2.70` but I only defined levels 1, 2, 3 — is the API broken? [→ §3.2 Example Scale]

**What you see**

You asked "How angry is the customer?" with three levels and got:

```
distribution: {1: 0.05, 2: 0.20, 3: 0.75}
score:        2.70      ← not 1, not 2, not 3
confidence:   0.70
```

Your first instinct is that a level you never defined leaked out. Before this, the same ticket through a plain language model returned `"moderately urgent!"` — a string with no threshold you can compare, and a different adjective every time you asked.

**Why**

`score` is probability-weighted, not the top level. `2.70` says "mostly very angry, with some pull toward frustrated" — richer than picking level 3 and much richer than an adjective.

**What to do**

1. Threshold on the continuous score, so you can retune triage without asking again.
2. Keep the `confidence` check beside the score — right level, weak margin still deserves a human.
3. Write each level description carefully; vague level text produces vague scores.
4. If your buckets have no natural order, you wanted Choice, not Score.

```python
if anger["score"] >= 2.5 and anger["confidence"] >= 0.6:
    page_oncall(ticket)            # right level, peaked → auto-act
elif anger["score"] >= 2.5:
    flag_for_human_review(ticket)  # right level, weak margin → confirm
```

**Verify**

Move the threshold from `2.5` to `2.0` and confirm you only changed your code. Then check the per-level probabilities for bimodality — `{1: 0.45, 2: 0.05, 3: 0.50}` means "one or three, nothing in between", and a single score hides that doubt.

---

## Q4. My safety gate returned `P(yes) = 0.45` and my code blocked the ticket — I thought 0.45 meant "probably yes" [→ §4.1 Contract, §4.2 Used For]

**What you see**

The gate question is `"Does this tool call touch production data?"`. The answer is `p_yes = 0.61`, so your code computed confidence `0.22` and a branch like `if p > 0.5: block` fired anyway. Tickets get held for a human on the strength of a number that meant almost nothing. On the refund gate the same code saw `p_yes = 0.97` (confidence `0.94`) and correctly opened the refund workflow.

**Why**

A value near `0.5` means the evidence pulls both ways — genuinely balanced, not "medium yes". Certainty is intrinsic: `confidence = |p − 0.5| × 2`, so there is no separate confidence field to misread.

**What to do**

1. Treat the middle as a real band with its own branch, not as a rounded-up yes.
2. Auto-act only in the high-confidence tails; below that, ask a clarifying question.
3. Add `criteria` so "yes" is written down in the request instead of living in someone's head.

```python
conf = lambda p: abs(p - 0.5) * 2
if p_refund > 0.5 and conf(p_refund) >= 0.8:
    open_refund_workflow(ticket)      # high band
elif p_refund > 0.5:
    queue_for_agent_review(ticket)    # balanced → confirm
else:
    reply_with_clarifying_question(ticket)
```

**Verify**

Histogram `p_yes` per gate over a week of real traffic. A healthy gate is strongly bimodal with a thin middle; a fat middle means your `criteria` is vague. Then confirm that answers at `0.8` are right about 80% of the time.

---

## Q5. Six decisions per ticket and my latency is 10 seconds — do I make six calls? [→ §5 Parallel Evaluation]

**What you see**

You call a language model three times in a row to classify the ticket, rate the anger, and check for a refund request. The three calls take `3.1s`, `3.4s`, and `2.9s` — roughly 10 seconds of waiting and three separate bills. With six questions you are looking at 20 seconds, and the agent feels broken.

**Why**

Jev evaluates every question in a single parallel pass, so latency barely moves as you add questions. It is billed on input only at $0.042 per million tokens; the distributions on the output side are free.

**What to do**

1. Put all six questions in one `questions` map and send one request.
2. Key every answer by its question name so you can inspect confidence per question.
3. For a list of candidates, fan out one Noul per item instead of looping over calls.
4. With nested models, fields become namespaced questions (`outer.inner`) in the same pass — depth costs structure, not round-trips.

```python
questions = {
    f"hit_{i}": {"type": "noul", "question": "Does this item qualify?", "state_hint": item}
    for i, item in enumerate(items)
}
# One request → answers["hit_0"] … answers["hit_n"], all in 70–500ms
hits = [i for i in range(len(items)) if answers[f"hit_{i}"]["noul"]["p_yes"] > 0.6]
```

**Verify**

Time one call with 1 question against one call with 6. If the second is not meaningfully slower, the serial habit is safe to drop. Also check your bill: adding questions should move input cost, never add a second charge.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*