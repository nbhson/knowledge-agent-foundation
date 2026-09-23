# 🧩 02. The Three Primitives — Choice, Score, Noul

> This section explains **the request shape** (state + questions), the **three typed primitives** — **Choice**, **Score**, **Noul** — with code samples, **parallel evaluation** (why adding questions barely changes latency), and **how to choose the right primitive**. Read [README.md](../README.md) for context and [01-concepts](../01-concepts/) for what Jev is.

---

## 1. Request Shape

> **📌 Core Concept**
>
> **Definition:** Every Jev call has exactly two payloads: **`state`** — the material being judged (a string, a JSON object, or an array of text) — and **`questions`** — a named map of typed questions, each of which must be one of three primitives: Choice, Score, or Noul.
> **Analogy:** A **court filing**: `state` is the evidence you submit; `questions` are the verdicts you ask the judge to return — and a judge never answers "write me an essay about this evidence"; they check boxes.
> **Why it matters:** The shape is the whole discipline. State is *only* the material being judged; the question lives on the output type (or in `questions`), never buried inside the state. Get this split right and calibration, parallelism, and type-safety all follow.

### 1.1 The Two Halves

```
POST /v1/systemone
{
  "model": "jev-latest",
  "state":    <string | object | array of text>     ← THE MATERIAL
  "questions": {                                     ← THE VERDICTS
      "<name>": { "type": "choice", ... },
      "<name>": { "type": "score",  ... },
      "<name>": { "type": "noul",   ... }
  }
}
```

| Field | Rule |
|-------|------|
| `state` | String, JSON object, or array of text. Keep it **small and relevant** — accuracy falls when state carries unrelated detail |
| `questions` | Named map; every entry is exactly one of the 3 primitives |
| Evaluation | **All questions in parallel, one pass** — added questions barely change latency |
| Model | `jev-latest` → `jev-1.13.0` |

### 1.2 Summary: The Three Primitives

| | **Choice** | **Score** | **Noul** |
|---|---|---|---|
| **Question shape** | Pick 1 from a closed set **you define** | Rate on an **ordered scale** you describe | Answer a **yes/no proposition** |
| **Degrees of freedom** | ≤ **255** options | **2–10** levels | Binary |
| **Primary return** | `selected` + **full probability distribution** + `confidence` | `score` (may fall **between** levels) + legend + per-level probabilities + `confidence` | `P(yes)` ∈ **[0, 1]** |
| **Confidence meaning** | Concentration/shape of the distribution (a **margin**, not P(correct)) | Same as Choice | **Intrinsic**: `\|p − 0.5\| × 2` — no separate field needed |
| **Classic uses** | classification, routing, ontology tagging | severity, sentiment, readiness | gates, verification, policy checks |
| **Can it leave schema?** | Never | Never | Never (it *is* the schema) |

---

## 2. Choice — Pick One From a Closed Set

> **📌 Core Concept**
>
> **Definition:** Choice asks Jev to select **exactly one** option from a closed set you define (up to **255** options) and returns the selected value, the **full probability distribution** over all options, and a confidence derived from how concentrated that distribution is.
> **Analogy:** A **multiple-choice exam with 200 answer sheets graded at once** — Jev doesn't write "I believe the answer is B because…", it hands you `B` plus the odds it assigned to A, B, C, D.
> **Why it matters:** Routing and classification are the highest-volume decisions in production systems. With Choice you can branch on `if answers["team"].selected == "billing"` — no regex, no enum drift, no out-of-schema `"billing-ish"`.

### 2.1 Contract

| Aspect | Rule |
|--------|------|
| Options | **You** define the closed set; **≤ 255** |
| Selection | Exactly one option returned as `selected` |
| Distribution | Probabilities across **all** options |
| Confidence | Concentration/shape — **peaked → high**. It is a **margin, NOT a probability the answer is right** |
| Escape hatch | Jev can still pick a *wrong in-schema* answer, sometimes with high confidence — type safety ≠ factual correctness |

### 2.2 When to Add "Other"

An "other" option is insurance against a state that doesn't fit your taxonomy — but overusing it makes the model lazy:

```
Add "other" when:
  ✅ the real world genuinely has out-of-taxonomy cases (support tickets: yes)
  ✅ you monitor P(other) as a data-quality signal (spikes = taxonomy rot)

Avoid "other" when:
  ✗ the set is truly closed (payment methods, regions) — a wrong pick is a bug
  ✗ you'd route "other" to a human anyway and could instead use LOW CONFIDENCE
```

### 2.3 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = (
    "Ticket #4821: Customer was charged twice after upgrading to the Pro plan. "
    "They want the extra charge reversed and are threatening a chargeback."
)

QUESTIONS = {
    "team": {
        "type": "choice",
        "options": ["billing", "infra", "bug", "product", "other"],
        "question": "Which team should own this ticket?",
    }
}


def classify(text: str, questions: dict) -> dict:
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"model": "jev-latest", "state": text, "questions": questions},
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()["answers"]


answers = classify(STATE, QUESTIONS)
team = answers["team"]["choice"]

print(team["selected"])            # e.g. "billing"
print(team["probabilities"])       # {"billing": 0.91, "infra": 0.02, ...}
print(team["confidence"])          # e.g. 0.87  ← a MARGIN, not P(correct)

# Act on the value — and on the confidence band:
if team["confidence"] >= 0.8:
    route(ticket, team["selected"])            # auto-act
elif team["confidence"] >= 0.5:
    route(ticket, team["selected"], confirm=True)  # confirm / more context
else:
    escalate_to_human(ticket)                  # or hand to an LLM
```

</details>

### 2.4 Mapping to Pydantic Types

Choice maps cleanly onto Python typing — which is exactly what `TypeSafeModel` does under the hood (see [03-api](../03-api/)):

```python
from typing import Literal
from enum import Enum

# Literal  → one Choice question, options = the literals
# Enum     → one Choice question, options = the members
Team = Literal["billing", "infra", "bug", "product", "other"]
```

### 2.5 Pros / Cons

| Pros | Cons |
|------|------|
| Impossible to leave the schema | You must enumerate the world up front (taxonomy design is real work) |
| Full distribution → you see *runner-ups* and near-ties | ≤ 255 options; finer granularity belongs in Score or nested Choice |
| Confidence band gates auto-action cleanly | High confidence ≠ correct — still an in-schema wrong pick |
| Free-form "other" can flag taxonomy drift (`P(other)` spikes) | Flat lists get expensive in attention if you force 200+ options everywhere |

---

## 3. Score — An Ordered Scale You Describe

> **📌 Core Concept**
>
> **Definition:** Score asks Jev to rate state on an **ordered scale of 2–10 levels you describe**. It returns a probability-weighted score — which **can fall between levels** (e.g. **1.4**, between level 1 and 2) — plus the level legend, per-level probabilities, and confidence.
> **Analogy:** A **thermometer, not a text box**. You don't ask "describe how hot it is"; you read a position on a scale — and 1.4°C is a real, useful reading even though no one labeled a level "1.4".
> **Why it matters:** Ordinal judgments (severity, sentiment, readiness) are everywhere, and LLMs answer them with adjectives ("moderately urgent!") that no threshold can compare. A numeric score with a distribution lets your code do `if score >= 3.2:` — once, consistently, everywhere.

### 3.1 Contract

| Aspect | Rule |
|--------|------|
| Levels | **2–10**, ordered, **you describe** each level's meaning |
| Score | Probability-weighted; **may sit between levels** (e.g. 1.4 between 1 and 2) |
| Returns | `score` + **legend** (your level descriptions) + **per-level probabilities** + `confidence` |
| Confidence | Concentration/shape of the level distribution (same margin semantics as Choice) |

### 3.2 Example Scale — Calm → Frustrated → Very Angry

```
LEVEL LEGEND (3-level example)
──────────────────────────────────────────────
1  calm         patient, no urgency signals
2  frustrated   annoyed, repeated contact, mild pressure
3  very angry   hostile language, threats, chargeback talk

STATE: "charged twice… threatening a chargeback"
  distribution: {1: 0.05, 2: 0.20, 3: 0.75}
  score:        2.70      ← weighted, interpretable
  confidence:   0.70      ← moderately peaked → confirm before auto-priority
```

**Why between-level scores matter:** a 2.70 says "mostly angry, with some pull toward frustrated" — richer than argmax(`3`) and far richer than the string `"angry"`. Thresholds on the continuous score let you tune triage **without re-asking the model**.

### 3.3 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = "Third email today. 'If this isn't fixed by Friday I'm filing a chargeback.'"

QUESTIONS = {
    "anger": {
        "type": "score",
        "levels": [
            {"level": 1, "description": "calm — patient, no urgency signals"},
            {"level": 2, "description": "frustrated — annoyed, repeated contact"},
            {"level": 3, "description": "very angry — hostile, threats, chargeback talk"},
        ],
        "question": "How angry is the customer?",
    }
}

resp = requests.post(
    API,
    headers=HEADERS,
    json={"model": "jev-latest", "state": STATE, "questions": QUESTIONS},
    timeout=5,
)
resp.raise_for_status()
anger = resp.json()["answers"]["anger"]["score"]

print(anger["score"])            # e.g. 2.70  (may fall BETWEEN levels)
print(anger["legend"])           # your level descriptions, echoed
print(anger["probabilities"])    # {1: 0.05, 2: 0.20, 3: 0.75}
print(anger["confidence"])       # margin from the distribution shape

if anger["score"] >= 2.5 and anger["confidence"] >= 0.6:
    page_oncall(ticket)          # high band → auto-act
elif anger["score"] >= 2.5:
    flag_for_human_review(ticket)  # right level, weaker margin → confirm
```

</details>

### 3.4 Pros / Cons

| Pros | Cons |
|------|------|
| Continuous, thresholdable numbers instead of adjectives | Levels must be **ordered** — unordered buckets belong in Choice |
| Between-level scores preserve nuance argmax throws away | 2–10 cap: finer measurement needs more levels, not decimals-you-invent |
| Per-level distribution exposes bimodal doubt ("1 or 3, nothing between") | Descriptions are load-bearing: vague level text → vague scores |
| Same confidence-band ergonomics as Choice | Ordinal only — distances between levels aren't guaranteed equal |

---

## 4. Noul — A Proposition With P(yes)

> **📌 Core Concept**
>
> **Definition:** Noul takes a **proposition** (optionally with **criteria** for what counts as yes) and returns **P(yes) ∈ [0, 1]**. A value near **0.5 means genuinely balanced** — *not* "medium" — and certainty is **intrinsic**: `confidence = |p − 0.5| × 2`, so there is no separate confidence field.
> **Analogy:** A **coin weighted by evidence** — not a coin flip. `P(yes)=0.01` is a coin someone loaded toward no; `0.50` is a coin nobody has managed to tilt; `0.99` is a foregone conclusion. You don't need a second opinion on how sure the coin is — the tilt *is* the opinion.
> **Why it matters:** Gates and verification are the glue of agent systems ("did the LLM's answer pass the rubric?"). Noul gives you a **calibrated probability of the proposition itself**, so thresholds mean something: ~80% of answers at 0.8 are correct (RLCD).

### 4.1 Contract

| Aspect | Rule |
|--------|------|
| Input | A proposition; optional **`criteria`** defining what "yes" means |
| Output | **P(yes)** in `[0, 1]` |
| Near 0.5 | **Balanced** — evidence pulls both ways. It is *not* a "medium yes" |
| Confidence | **Intrinsic**: `\|p − 0.5\| × 2`. No separate field |
| Examples | `False` from `p=0.01` → confidence **0.98**; from `p=0.45` → confidence **0.10** |

```
p(yes) :  0.00 ────── 0.45 ── 0.50 ── 0.55 ────── 1.00
          certain no    ◄── balanced ──►          certain yes
          conf 1.00          conf 0.00            conf 1.00

confidence = |p − 0.5| × 2
  p=0.01 → 0.98      p=0.45 → 0.10      p=0.50 → 0.00      p=0.93 → 0.86
```

### 4.2 Used For: Gates & Verification

- **Policy gate** — "Does this tool call touch production data?" → block if `P(yes)` high
- **LLM-output verification** — "Does this answer satisfy the rubric?" → ship if `P(yes) ≥ τ`
- **Extraction check** — "Does the text explicitly request a refund?"
- **Review filter** — auto-approve where `P(yes)` is confidently low-risk

> ⚠️ Noul can still return a **wrong** answer — type safety ≠ factual correctness. Calibration tells you how much to trust the band, not that the model is oracular. Route low/mid bands to a human or an LLM (see [04-calibration](../04-calibration/)).

### 4.3 Code Sample

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import os
import requests

API = "https://api.typesafe.ai/v1/systemone"
HEADERS = {
    "Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}",
    "Content-Type": "application/json",
}

STATE = "Ticket #4821: charged twice after plan upgrade — please refund the extra $49."

QUESTIONS = {
    "refund_requested": {
        "type": "noul",
        "question": "Does the customer explicitly ask for money back?",
        "criteria": "Yes only if the text requests a refund or reversal of a charge.",
    },
    "chargeback_threat": {
        "type": "noul",
        "question": "Does the customer threaten a chargeback?",
    },
}

resp = requests.post(
    API,
    headers=HEADERS,
    json={"model": "jev-latest", "state": STATE, "questions": QUESTIONS},
    timeout=5,
)
resp.raise_for_status()
answers = resp.json()["answers"]

p_refund = answers["refund_requested"]["noul"]["p_yes"]     # e.g. 0.97
p_charge = answers["chargeback_threat"]["noul"]["p_yes"]    # e.g. 0.61

# Intrinsic confidence — no separate field for Noul:
conf = lambda p: abs(p - 0.5) * 2
print(conf(p_refund))   # 0.94  → auto-act (high band)
print(conf(p_charge))   # 0.22  → confirm / more context (mid band)

if p_refund > 0.5 and conf(p_refund) >= 0.8:
    open_refund_workflow(ticket)
elif p_refund > 0.5:
    queue_for_agent_review(ticket)   # right call, thin margin → confirm
else:
    reply_with_clarifying_question(ticket)
```

</details>

### 4.4 Pros / Cons

| Pros | Cons |
|------|------|
| The most natural shape for gates: one threshold on one number | Binary only — multi-class needs Choice, ordinal needs Score |
| Confidence is *derived from p itself* — can't disagree with the answer | `p≈0.5` means "don't know yet", not "medium"; you must handle the band |
| Criteria field documents the decision rule in the request | Criteria drift: vague criteria → thresholds that don't mean what you think |
| Perfect for map-reduce fan-out (one Noul per candidate) | Still can be confidently wrong — pair with human/LLM escalation |

---

## 5. Parallel Evaluation

> **📌 Core Concept**
>
> **Definition:** Jev evaluates **all questions in parallel in a single pass** — so adding questions barely changes latency; you just send slightly more cheap input tokens ($0.042 / M, output free). This is what makes multi-question requests and fan-out patterns economical.
> **Analogy:** A **panel of judges sworn in at once** — one hearing covers all charges. Swearing in a tenth judge doesn't double the trial length; it slightly lengthens the docket.
> **Why it matters:** It inverts the LLM habit of one-question-per-call. Ask your classification, rating, *and* verification in the **same** request: same 70–500ms envelope, more decisions per dollar.

### 5.1 One Pass, Many Questions

```
LLM-style (serial, wasteful):              Jev (one pass):

q1 ──► LLM ──► 3.1s  ┐                    ┌─ q1 (choice) ─┐
q2 ──► LLM ──► 3.4s  ├── ~10s, 3 bills    │─ q2 (score)  ─┼─► 70–500ms, 1 bill
q3 ──► LLM ──► 2.9s  ┘                    └─ q3 (noul)   ─┘
                                              all parallel
```

| Property | Behavior |
|----------|----------|
| Evaluation | **All questions, one pass**, parallel |
| Latency vs #questions | **Barely changes** — more questions ≈ slightly more input tokens |
| Output billing | **Free** — the distributions are cheap to emit; you're billed on input only |
| Failure isolation | Each answer keyed by `name` — inspect per-question confidence independently |

### 5.2 List Fan-Out — One Noul Per Option

Got a list of candidates and a yes/no test? Fan out **one Noul per item** — all evaluated in the same pass:

```python
items = ["candidate A", "candidate B", "candidate C", ...]   # the list
questions = {
    f"hit_{i}": {"type": "noul", "question": "Does this item qualify?", "state_hint": item}
    for i, item in enumerate(items)
}
# One request → answers.hit_0 … answers.hit_n, all in 70–500ms
hits = [i for i in range(len(items)) if answers[f"hit_{i}"]["noul"]["p_yes"] > 0.6]
```

This is the mechanical heart of workload #2 (**map-reduce over large datasets**): the *map* is your row extraction, the *reduce* is a threshold over the fan-out distribution.

### 5.3 Nested Models (`outer.inner`)

Structured outputs nest — so do the questions. With Pydantic AI's `TypeSafeModel`, a nested model's fields become **namespaced questions** (`outer.inner`), each still evaluated in the same pass:

```
output_type = TicketPlan
  ├─ team: Team              → question "team"
  ├─ urgency: Score          → question "urgency"
  └─ actions: list[Action]   → fan-out: "actions.0.reason", "actions.1.reason", ...
```

Nesting composes with parallelism: depth costs structure, not serial round-trips. See [03-api](../03-api/) §4 for the Pydantic AI wiring.

---

## 6. Choosing the Right Primitive

> **📌 Core Concept**
>
> **Definition:** The decision table for primitive selection — classification → **Choice**, ordinal/rating → **Score**, boolean/gate → **Noul** — plus TypeSafe's best-practice split: **put the question on the field/output type, the framing on instructions, and keep questions out of the prompt** (the state is only the material being judged).
> **Analogy:** Choosing **checkbox / sliding scale / yes-no** on a survey. The survey designer who writes the essay prompt inside the evidence packet gets garbage data; the one who separates *packet* from *form* gets answers they can chart.
> **Why it matters:** Most bad Jev results are shape mistakes, not model mistakes — a rating asked as a Choice loses ordering; a gate asked as a 5-option Choice loses the elegance of P(yes); framing stuffed into the state pollutes the evidence (state hygiene).

### 6.1 Decision Table

| Your question is… | Shape | Primitive | You get |
|--------------------|-------|-----------|---------|
| "Which of these categories?" | Classification | **Choice** | `selected` + full distribution |
| "How much / how severe / which step?" | Ordinal, rating | **Score** | between-level `score` + per-level probabilities |
| "Is it true / does it pass / should we block?" | Boolean, gate | **Noul** | `P(yes)` with intrinsic confidence |
| Unordered buckets + ranking | Classification with order | **Choice** (flat) or two calls | distribution over buckets |
| Continuous measurement (dollars, pixels) | Mechanic | **Code** — not a Jev question | exact arithmetic |

```
classification / routing      ──►  Choice
ordinal / rating / severity   ──►  Score
boolean / gate / verify       ──►  Noul
arithmetic / dates / counting ──►  plain code (never Jev)
```

### 6.2 TypeSafe's Best-Practice Split

```
┌───────────────────────────────────────────────────────────────┐
│  PUT HERE                    │  PUT HERE                      │
│  (the QUESTION)              │  (the FRAMING)                 │
├───────────────────────────────┼────────────────────────────────┤
│  field / output type         │  docstring / instructions      │
│  + field description         │  "Answer as if you were …"     │
│  (Pydantic TypeSafeModel)    │  tone, persona, global rules   │
│                              │                                │
│  questions map (raw API)     │  criteria on a Noul            │
│  "Which team owns this?"     │  "Yes only if …"               │
├───────────────────────────────┼────────────────────────────────┤
│  NEVER in the STATE          │  NEVER as hidden prompt hacks  │
│  state = evidence only       │  state is not a prompt         │
└───────────────────────────────┴────────────────────────────────┘
```

The Pydantic AI twist — TypeSafe calls the description↔question pairing **"probably the most important concept"** — is a **habit inversion**: when you prompt an LLM you pour effort into instructions and hope the structure sticks; with Jev you pour effort into the **question/field description** (that *is* the decision), and keep instructions as light framing. Opposite habit, opposite reliability.

**Keep questions out of the prompt (the state):** the state is *only the material being judged*. Smuggling "please classify as billing" into the state contaminates the evidence, breaks calibration, and violates state hygiene (accuracy falls when state carries unrelated detail — [01-concepts](../01-concepts/) §6.3).

### 6.3 Quick Self-Check

Before sending a request, ask:

1. Is the answer a **member of a set**? → Choice (≤255 options)
2. Is it a **position on an ordered scale**? → Score (2–10 levels, describe them)
3. Is it a **gate**? → Noul (add `criteria` if "yes" needs defining)
4. Is it **math or dates**? → leave it in code
5. Is the state **only the evidence**? → move framing to instructions/criteria
6. Do I need **6 answers**? → send 6 questions in **one** call (parallel pass)

---

*Back to [README](../README.md) — Module XIV overview · Next: [03 — API & Integrations](../03-api/) →*
