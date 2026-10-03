# ❓ FAQ — JEV (Real Stories, Plain Language)

If a question is unclear, read the section in `README.md` (named in brackets).

---

## Q1. What even is Jev? My code already calls an LLM for everything — why add another thing? [→ Why Jev & System One Models Matter?]

**What you see**

Your support pipeline gets 4,000 tickets an hour. Each ticket needs three tiny judgments: which team (`billing / infra / bug / other`), is a refund requested (`yes / no`), and severity (`1..5`). Today you send each ticket to a frontier large language model (an expensive, text-generating AI model) and get back a paragraph that starts with *"Based on my analysis, the ticket appears to be..."*, followed by a JSON blob you have to parse, validate, and retry when a quote comes back malformed. Each ticket costs **3–329 seconds**.

**Why**

An LLM is a **System Two-ish tool**: it generates **text for people**. Jev is a **System One model** — a transformer-based decision model that **never generates a single token of text**. You send state (a string, JSON, or an array of text) plus named, typed questions; you get back a `Choice`, a `Score`, or a `Noul` answer, each with a full probability distribution. They are complements, not replacements: *"Jev decides, LLM writes."*

**What to do**

1. Read `01-concepts/` first — it defines System 1 vs System 2 and where the decision layer sits.
2. Spot your own "tiny decision" steps: classify, rate, gate, route, verify. Those are Jev candidates.
3. Keep generation with the LLM. Move only the boolean-and-category steps.
4. Read `06-jev-and-llm/` for the division of labor before you wire anything.

```
State (text/JSON) + named typed questions
        ↓
Jev → answers.<name>.choice / .score / .noul + probability + confidence
        ↓
Your code applies the threshold: high → act, medium → confirm, low → human/LLM
```

**Verify**

Send one ticket and confirm you get typed answers (not prose) in **70–500ms**, with no parsing code. If you still need a JSON parser, you are still using the LLM.

---

## Q2. Is the "40–200× faster, ~400× cheaper" claim real, or is it marketing? [→ Why Jev & System One Models Matter?]

**What you see**

The README quotes TypeSafe (the company that builds Jev): **40–200× faster and ~400× cheaper** than frontier LLMs on System-One-shaped tasks — roughly **two orders of magnitude** better. End-to-end latency is **70–500ms per request**, against **3–329s** for frontier LLMs on the same work. Price is **$0.042 per million input tokens, with output free**. That is roughly 400× cheaper than a typical frontier price point.

**Why**

The speed and cost gap is structural, not a tuning trick. The answer space is **closed** — Jev can only return values you defined, so it cannot hallucinate an out-of-schema label, and it does not need to write a paragraph before the answer. On calibration (how truthful a stated confidence is), RLCD — the training method behind the numbers — gives this: **~80% of answers scored 0.8 are actually correct**.

**What to do**

1. Read `04-calibration/` before you trust any confidence number; it explains margin vs probability and confidence bands.
2. Set your thresholds in **code**, not in the prompt: high confidence auto-acts, medium asks for confirmation, low routes to a human or the LLM.
3. Benchmark your own three questions before/after — do not quote these numbers to your team as your numbers.

| Claim | Source | Number |
|---|---|---|
| Speed | TypeSafe latency data | 70–500ms vs 3–329s |
| Cost | TypeSafe (2026) | $0.042 / M input tokens, output free |
| Calibration | RLCD | ~80% of 0.8-scored answers correct |

**Verify**

Log `confidence` per answer on real tickets for one week and compare against your own human labels. If 0.8-scored answers are not ~80% correct for your data, your data is not shaped like the training data — see Q5.

---

## Q3. There are seven folders here. Where do I actually start? [→ Learning Path (Directory Structure)]

**What you see**

`README.md` plus `01-concepts`, `02-primitives`, `03-api`, `04-calibration`, `05-patterns`, `06-jev-and-llm`, `07-limits-and-evaluation`. Seven files, no obvious entry point, and the temptation to read them in a random order or skip to the API docs.

**Why**

Each folder answers one question, and the order matters because later folders assume earlier vocabulary. `02-primitives` uses the three primitives (`Choice`, `Score`, `Noul`); `03-api` uses them in a request body; `05-patterns` and `06-jev-and-llm` use the confidence bands from `04-calibration`.

**What to do**

Follow the recommended path: read `README.md` → `01-concepts` → `02-primitives` → `03-api` (make one real call) → `04-calibration` → `05-patterns` + `06-jev-and-llm` → `07-limits-and-evaluation`.

| If you want to… | Read |
|---|---|
| Know what Jev is | [01-concepts](01-concepts/) |
| Pick Choice vs Score vs Noul | [02-primitives](02-primitives/) |
| Make your first call | [03-api](03-api/) |
| Trust a confidence number | [04-calibration](04-calibration/) |
| Know the edges before production | [07-limits-and-evaluation](07-limits-and-evaluation/) |

**Verify**

You can name which primitive fits each of your three ticket judgments, and you have one working call returning typed answers before reading `05-patterns`.

---

## Q4. Do I throw out my LLM and run everything on Jev? [→ Overview]

**What you see**

The temptation after reading the pricing table: route *all* model calls to Jev. Then the first real request comes back asking for a written customer reply, and Jev cannot produce it — it never generates text. The model is `jev-1.13.0` (alias `jev-latest`), **text-only**, with a **64k context** limit.

**Why**

The split is simple. Generation — prose, code, explanations — belongs to the LLM. Every gate, rubric check, category pick, and routing decision belongs to Jev. The traffic-light analogy holds: the light decides instantly, the tour guide narrates. You do not ask the tour guide whether the light is red.

**What to do**

1. Keep the LLM for drafting and explanation; call Jev **after** generation to verify, and **before** generation to route.
2. Build the verified cascade from `06-jev-and-llm/` — high confidence and passing threshold means ship it; low confidence or fail means escalate.
3. If you already use a framework, use the official integrations instead of hand-rolling: LangChain's `TypeSafeClassifier` (routing middleware and `AutoModeMiddleware`), Pydantic AI's `TypeSafeModel` (one question per output field, tool-call threshold defaults to `0.6`), OpenRouter's `typesafe/jev-1.13`, or Spice AI for calling it from SQL.

```
LLM drafts → Jev asks "is this in policy?" (Noul) + "which category?" (Choice)
   → high confidence, P(pass) ≥ threshold → ship
   → low confidence / fail → human or a stronger LLM
```

**Verify**

Count how many LLM calls remain per ticket after the change. If the number did not drop, you added Jev without moving any decision out of the LLM.

---

## Q5. When should I *not* use Jev — and what happens when I ignore that? [→ 07-limits-and-evaluation]

**What you see**

You reach for Jev on a task it was never trained for: reading a spreadsheet, counting rows, adding numbers, or checking a 200-page PDF. You ask it for a severity score, treat the number as arithmetic, and ship `3` when the ticket actually described five failed logins. Or the input exceeds its context and the request is rejected.

**Why**

`jev-1.13` is **text-only with a 64k context window**, and its output is a *judgment*, not a computation. The answer space is closed — which is exactly why it cannot invent a label, and also exactly why it cannot do your math. Arithmetic belongs in code; the decision about whether the result is acceptable belongs to Jev.

**What to do**

1. Read `07-limits-and-evaluation/` before production; it lists the `jev-1.13` limits and error modes.
2. Keep every calculation in your own code — count, sum, compare — then let Jev classify or score the result.
3. If your state is not plain text, reduce it to text first (or do the work elsewhere). Images, audio, and binary input are out of scope.
4. Test on your own labels before trusting a threshold; if confidence does not match your accuracy, your data is out of distribution.

| Task | Jev? |
|---|---|
| Classify / rate / gate on text | yes |
| Verify an LLM draft against a rubric | yes |
| Count rows, add numbers | no — do it in code |
| Read an image or spreadsheet | no |

**Verify**

Confirm nothing but text crosses the boundary, that all arithmetic is in your code, and that a deliberately out-of-range input fails loudly instead of returning a plausible wrong number.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*