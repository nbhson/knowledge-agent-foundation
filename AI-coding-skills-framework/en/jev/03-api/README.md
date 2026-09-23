# 🔌 03. API & Integrations

> This section covers **the endpoint and authentication**, the **request & response shapes** with a full JSON example, the **official SDKs**, and the four integration surfaces — **Pydantic AI** (`TypeSafeModel`), **LangChain** (`TypeSafeClassifier`), **OpenRouter**, and the **limits & errors** you must handle before production. Read [README.md](../README.md) for context and [02-primitives](../02-primitives/) for Choice / Score / Noul semantics.

---

## 1. Endpoint & Authentication

> **📌 Core Concept**
>
> **Definition:** Jev is reached via **`POST https://api.typesafe.ai/v1/systemone`** with a **Bearer API key**. The body carries `model`, `state`, and `questions`; model aliases map `jev-latest` → `jev-1.13.0`.
> **Analogy:** It looks exactly like calling an LLM API — because the *transport* is deliberately boring. The novelty is entirely in what comes back: typed decisions with distributions, not a token stream.
> **Why it matters:** Zero new protocol skills required. If you can hold an API key and POST JSON, you can ship a decision layer today — the interesting decisions are which questions to ask and which confidence band to act on.

### 1.1 The Basics

| Item | Value |
|------|-------|
| **Endpoint** | `POST https://api.typesafe.ai/v1/systemone` |
| **Auth** | `Authorization: Bearer <TYPESAFE_API_KEY>` |
| **Content-Type** | `application/json` |
| **Body** | `{ model, state, questions }` |
| **Current version** | `jev-1.13.0` |
| **Alias** | `jev-latest` → `jev-1.13.0` (use this unless you must pin) |
| **Latency** | 70–500ms end-to-end |
| **Price** | $0.042 / M input tokens; **output free** |

```bash
curl -sS https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-latest",
    "state": "Deploy pipeline red: auth service OOMKilled after migration.",
    "questions": {
      "team": {"type": "choice", "options": ["billing","infra","bug","other"]}
    }
  }'
```

### 1.2 Key Handling

```
TYPESAFE_API_KEY   env var (never commit)
       │
       ▼
Authorization: Bearer sk-…      ← server-side only; rotate on leak
       │
       ▼
One key → /v1/systemone          (or the same key pointed at OpenRouter — §6)
```

---

## 2. Request & Response

> **📌 Core Concept**
>
> **Definition:** A request is `state` + a named `questions` map; the response nests answers under `answers.<name>` with the primitive-specific payload (`.choice` / `.score` / `.noul`), plus **probabilities** and **confidence**. All questions in one request are evaluated in parallel in one pass.
> **Analogy:** Like a lab requisition form: one specimen (`state`), several tests (`questions`), one report back with a **separate result block per test** — you never re-submit the specimen to run the second test.
> **Why it matters:** One round-trip buys N decisions at 70–500ms. Design your request so a single call covers the whole decision step (classify + gate + rate) rather than three serial LLM-style calls.

### 2.1 Full Request Example

Three questions — one Choice, one Noul, one Score — in a single pass:

```json
{
  "model": "jev-latest",
  "state": "Ticket #4821: Customer charged twice after upgrading to Pro. Wants the extra $49 reversed; mentions chargeback if not fixed by Friday. Third contact today.",
  "questions": {
    "team": {
      "type": "choice",
      "options": ["billing", "infra", "bug", "product", "other"],
      "question": "Which team should own this ticket?"
    },
    "refund_requested": {
      "type": "noul",
      "question": "Does the customer explicitly ask for money back?",
      "criteria": "Yes only if the text requests a refund or reversal of a charge."
    },
    "urgency": {
      "type": "score",
      "levels": [
        { "level": 1, "description": "routine — no time pressure" },
        { "level": 2, "description": "soon — customer waiting, no threat" },
        { "level": 3, "description": "critical — threats, chargeback, churn risk" }
      ],
      "question": "How urgent is this ticket?"
    }
  }
}
```

### 2.2 Response Shape

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "team": {
      "choice": {
        "selected": "billing",
        "probabilities": {
          "billing": 0.93,
          "infra": 0.02,
          "bug": 0.03,
          "product": 0.01,
          "other": 0.01
        },
        "confidence": 0.88
      }
    },
    "refund_requested": {
      "noul": {
        "p_yes": 0.96
      }
    },
    "urgency": {
      "score": {
        "score": 2.71,
        "legend": [
          { "level": 1, "description": "routine — no time pressure" },
          { "level": 2, "description": "soon — customer waiting, no threat" },
          { "level": 3, "description": "critical — threats, chargeback, churn risk" }
        ],
        "probabilities": { "1": 0.04, "2": 0.25, "3": 0.71 },
        "confidence": 0.74
      }
    }
  }
}
```

### 2.3 Reading the Blocks

| Answer key | Payload | How to read it |
|------------|---------|----------------|
| `answers.<name>.choice` | `selected`, `probabilities`, `confidence` | Branch on `selected`; use `confidence` as a **margin** to gate auto-action |
| `answers.<name>.score` | `score`, `legend`, `probabilities`, `confidence` | Threshold the **continuous** `score` (it may sit between levels) |
| `answers.<name>.noul` | `p_yes` | Threshold `p_yes`; intrinsic confidence = `\|p_yes − 0.5\| × 2` |

**Confidence band guidance** (apply uniformly):

```
high    → code auto-acts
medium  → confirm / gather more context
low     → route to a human or another system / LLM
```

> ⚠️ For Choice/Score, `confidence` is concentration of the distribution — a **margin, NOT a probability the answer is right**. Jev can pick a wrong in-schema answer, sometimes with high confidence. Type safety ≠ factual correctness (see [04-calibration](../04-calibration/)).

---

## 3. Official SDKs

> **📌 Core Concept**
>
> **Definition:** TypeSafe ships **official Python and JavaScript SDKs** that wrap `/v1/systemone`. Both accept a custom base URL — which is how you point the TypeSafe TS SDK at **OpenRouter** (§6) without changing application code.
> **Analogy:** A **power adapter** — the appliance (your decision logic) doesn't change when you plug into a different country's outlet (TypeSafe direct vs OpenRouter).
> **Why it matters:** SDKs remove hand-rolled `requests`/`fetch` boilerplate, keep `model` aliases current, and — via base URL — give you a vendor-portable seam for the day you want a second route to the same model.

### 3.1 Python Quickstart

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import os
from typesafe import TypeSafe  # official TypeSafe Python SDK

client = TypeSafe(api_key=os.environ["TYPESAFE_API_KEY"])

result = client.systemone.ask(
    model="jev-latest",
    state="Invoice shows 3 line items; customer says they only ordered 2.",
    questions={
        "discrepancy": {
            "type": "noul",
            "question": "Does the text claim a billing discrepancy?",
            "criteria": "Yes only if the customer states the charge does not match the order.",
        },
        "team": {
            "type": "choice",
            "options": ["billing", "fraud", "support"],
            "question": "Which team owns this?",
        },
    },
)

p_disc = result.answers["discrepancy"].p_yes          # 0.91
team = result.answers["team"].choice.selected          # "billing"
conf = result.answers["team"].choice.confidence        # margin, not P(correct)
```

</details>

### 3.2 JavaScript Quickstart

<details>
<summary>JavaScript Code (Click to expand/collapse)</summary>

```js
import { TypeSafe } from "@typesafe/sdk"; // official TypeSafe JS SDK

const client = new TypeSafe({ apiKey: process.env.TYPESAFE_API_KEY });

const result = await client.systemone.ask({
  model: "jev-latest",
  state: "PR #220 deletes the payment retry limit check.",
  questions: {
    risky: {
      type: "noul",
      question: "Does this change remove a safety guardrail?",
      criteria: "Yes only if a limit, check, or permission gate is deleted or weakened.",
    },
    area: {
      type: "choice",
      options: ["payments", "api", "ui", "docs"],
      question: "Which area of the codebase does this touch?",
    },
  },
});

const risky = result.answers.risky.noul.p_yes;   // e.g. 0.87
const area = result.answers.area.choice.selected;

if (risky > 0.5 && Math.abs(risky - 0.5) * 2 >= 0.6) {
  blockAutoMerge(pr); // Noul intrinsic confidence ≥ 0.6 → hold for review
}
```

</details>

### 3.3 Pointing the SDK at OpenRouter

Same client, different base URL — no application restructure:

```python
client = TypeSafe(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api",   # route via OpenRouter
)
```

Full OpenRouter mechanics in §6.

---

## 4. Pydantic AI — TypeSafeModel

> **📌 Core Concept**
>
> **Definition:** In Pydantic AI, **`TypeSafeModel`** turns your `output_type` into Jev questions: **each field = one question**, **field `description` = the question text**, and **docstring / `instructions` = the framing**. TypeSafe calls this pairing **"probably the most important concept"** — because it is the *opposite habit* from prompting an LLM.
> **Analogy:** An LLM prompt is a **briefing memo** you hope gets followed; a `TypeSafeModel` is a **form with labeled fields** — the label *is* the ask. You wouldn't bury "Rate urgency 1–5" inside a memo's third paragraph; you put it on the line marked *Urgency*.
> **Why it matters:** Once fields and descriptions carry the decisions, your Jev agent becomes typed end-to-end: valid answers by construction, parallel evaluation under the hood, and confidence bands your code can branch on — without any string parsing.

### 4.1 Field → Question Mapping

| Pydantic construct | Becomes |
|--------------------|---------|
| Each field of `output_type` | **One question**, evaluated in the same parallel pass |
| Field `description=...` | **The question text** (what Jev answers) |
| Class docstring / agent `instructions` | **Framing** — tone, persona, global context |
| Nested models | Namespaced questions (`outer.inner`) |
| `list[T]` fields | **Fan-out** — one question per element |
| Bare `bool` **without** description | **`UserError`** — a boolean needs a stated question |

> 📌 **The habit inversion:** with an LLM you invest in *instructions* and hope structure emerges; with `TypeSafeModel` you invest in **field descriptions** (the questions) and keep instructions as light framing. Opposite habit — TypeSafe: *"probably the most important concept."*

### 4.2 Decide-Only Agent

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from typing import Literal
from pydantic import Field
from pydantic_ai import Agent
from pydantic_ai.models.typesafe import TypeSafeModel  # TypeSafeModel
from pydantic_ai.models.fallback import FallbackModel


class Triage(BaseModel):
    """Framing: answer as the support triage desk; evidence is the ticket only."""

    team: Literal["billing", "infra", "bug", "product"] = Field(
        description="Which team should own this ticket?"   # ← the QUESTION
    )
    refund_requested: bool = Field(
        description="Does the customer explicitly ask for money back?"
    )
    urgency: Literal[1, 2, 3] = Field(
        description="Urgency: 1 routine, 2 soon, 3 critical (threat/churn)"
    )


agent = Agent(
    TypeSafeModel("jev-latest"),          # Jev decides…
    output_type=Triage,
    # instructions → FRAMING only; the questions live on the fields
    instructions="Use only the ticket text. Do not speculate about intent.",
)

result = agent.run_sync(
    "Ticket #4821: charged twice, wants $49 back, threatens chargeback by Friday."
)
print(result.output.team)             # "billing"
print(result.output.refund_requested) # True
print(result.output.urgency)          # 3
```

</details>

### 4.3 Tools Attached — The Extra Question

With **tools** attached, every request carries **one more question**: *"which of these does the text call for?"* The flow:

```
text + tools
    │
    ▼
Jev picks a tool (typesafe_tool_call_threshold, default 0.6)
    │
    ├─ NO-ARG tool ──────────────────► called DIRECTLY on Jev's pick
    │                                   (no LLM needed for the call itself)
    │
    └─ ARG tool ─► ToolCallProposed ──► raises ModelAPIError
                                   │
                                   ▼
                        FallbackModel (an LLM behind Jev)
                        handles the WHOLE step — args and all
```

| Mechanism | Behavior |
|-----------|----------|
| `typesafe_tool_call_threshold` | Default **0.6** — below it, Jev abstains from tool selection |
| No-arg tool | **Called directly** on Jev's pick — the fast path |
| Arg tool | `ToolCallProposed` → **`ModelAPIError`** → `FallbackModel` handles the entire step |
| `FallbackModel` | The LLM sits *behind* Jev — Jev routes/decides, LLM writes |

### 4.4 Other TypeSafeModel Details

- **List fan-out:** `list[Item]` → one question per element, same pass — cheap map-reduce (see [02-primitives](../02-primitives/) §5.2).
- **Nested models:** `outer.inner` namespacing keeps deep outputs addressable.
- **Instructions for a single question:** when you only need one verdict, a one-field `output_type` plus framing instructions is the minimal decide-only agent.
- **`UserError` on a bare bool:** `flag: bool` with **no description** raises `UserError` at runtime — Jev refuses to guess what your field means. Always write the question.

---

## 5. LangChain — TypeSafeClassifier

> **📌 Core Concept**
>
> **Definition:** LangChain's **`TypeSafeClassifier`** answers named questions over a state via **`.invoke(state, questions)`** and returns typed answers + distributions — designed to sit in **middleware**: route before the LLM runs, or gate risky tool calls with **`AutoModeMiddleware`**.
> **Analogy:** A **bouncer with a checklist** — the classifier doesn't join the party (generate text); it checks the list at the door and lets the right chain through, or stops the wrong tool call.
> **Why it matters:** Middleware is where decisions multiply: every incoming request, every tool call can carry one cheap parallel Jev pass instead of a deliberative LLM call — the LangChain-native version of "Jev routes and verifies, LLM provides the language."

### 5.1 Classifier Invocation

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
from langchain.classifiers import TypeSafeClassifier

classifier = TypeSafeClassifier(model="jev-latest")

answers = await classifier.ainvoke(
    state="User: my export keeps failing with timeout after 30s",
    questions={
        "intent": {
            "type": "choice",
            "options": ["bug_report", "how_to", "billing", "churn_risk"],
            "question": "What is the user's intent?",
        },
        "is_escalation": {
            "type": "noul",
            "question": "Is the user asking for a human?",
        },
    },
)

intent = answers["intent"].selected          # "bug_report"
p_esc = answers["is_escalation"].p_yes       # e.g. 0.12
```

</details>

### 5.2 Two Middleware Patterns

| Middleware | What Jev does | Effect |
|------------|---------------|--------|
| **Routing middleware** | Classifies each incoming request (Choice) **before** the LLM chain runs | Right chain, right cost — wrong/long LLM calls avoided entirely |
| **AutoModeMiddleware** | Attaches a gate question to **risky tool calls**; Jev's pick **blocks** the call when the answer says no | Tool-use guardrail with a calibrated threshold, not an LLM narration |

```
request ──► TypeSafeClassifier ──► answers (+ distributions)
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
  routing middleware      AutoModeMiddleware
  (pick the chain)        (block risky tool calls)
        │                        │
        └────────► LLM runs only when it should ◄───┘
```

---

## 6. OpenRouter — One Key, Many Models

> **📌 Core Concept**
>
> **Definition:** Jev is available through OpenRouter at **`POST https://openrouter.ai/api/alpha/decisions`** with model **`typesafe/jev-1.13`** — or by setting the TypeSafe TS SDK's **base URL** to OpenRouter. The use case: **one API key, many models**.
> **Analogy:** An **airline alliance** — one booking desk (your OpenRouter key) reaches carriers (models) you'd otherwise open separate accounts for. Jev is a destination on the same ticket.
> **Why it matters:** Teams already standardizing on OpenRouter get System One decisions without a second vendor relationship, second key rotation process, or second billing line — the integration cost drops to one endpoint.

### 6.1 Direct Call

```bash
curl -sS https://openrouter.ai/api/alpha/decisions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "typesafe/jev-1.13",
    "state": "…",
    "questions": { "…": { "type": "noul", "question": "…" } }
  }'
```

| Item | Value |
|------|-------|
| Endpoint | `POST https://openrouter.ai/api/alpha/decisions` |
| Model id | `typesafe/jev-1.13` |
| Auth | OpenRouter key (Bearer) |
| Alternative | TypeSafe TS SDK with `base_url` → OpenRouter (§3.3) |

**Use case:** *one key, many models* — LLMs for writing, `typesafe/jev-1.13` for deciding, single billing/auth surface.

---

## 7. Limits & Errors

> **📌 Core Concept**
>
> **Definition:** jev-1.13 boundaries you must design around: **text input only** (no files, no tool-arg writing), **64k total context** (32k state + longest question → past that, `ModelHTTPError: max_tokens_exceeded`), and the standing rule that **arithmetic, counting, and date comparison stay in code**.
> **Analogy:** A **specialist with a narrow chart** — brilliant on the verdict, but they can't open attachments, can't do long division, and their chart has a hard page limit. Do the mechanics *around* the specialist, not through them.
> **Why it matters:** Every production incident with a decision model starts at a boundary: a state that overflowed context, a count Jev was asked to do, a file it could never read. Learn the edges here — then read [07-limits-and-evaluation](../07-limits-and-evaluation/) before shipping.

### 7.1 Hard Limits (jev-1.13)

| Limit | Detail | What to do instead |
|-------|--------|--------------------|
| **Text input only** | Cannot generate text, write tool arguments, or read files | LLM writes / reads; Jev only decides on the text you send |
| **Context: 64k tokens total** | **32k state** + the longest question | Trim state (state hygiene — small, relevant exhibits) |
| **Past 64k** | `ModelHTTPError` / **`max_tokens_exceeded`** | Chunk the state or summarize in code/LLM first |
| **Arithmetic / counting / dates** | Not reliable — keep in code | Compute deltas and counts *before* the call; feed results as state |
| **Schema escape** | Impossible (closed answer space) — but **wrong in-schema answers** still happen | Confidence bands + human/LLM escalation |

```
┌──────────────────────────────────────────────────────────────┐
│  THE 64K RULE                                                │
│                                                              │
│  32k state  +  longest question  ≤  64k total                │
│       │                         │                            │
│       ▼                         ▼                            │
│  keep exhibits small        keep questions crisp             │
│  (unrelated detail          (framing belongs in              │
│   lowers accuracy)           instructions, not here)         │
│                                                              │
│  overflow → ModelHTTPError: max_tokens_exceeded             │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 Common Errors

| Error / symptom | Likely cause | Fix |
|-----------------|--------------|-----|
| `ModelHTTPError: max_tokens_exceeded` | State + longest question exceeded **64k** | Shrink state; summarize before sending |
| `UserError` (Pydantic AI) | A **bare `bool`** field with no `description` | Write the question — `Field(description="…")` |
| `ModelAPIError` (`ToolCallProposed`) | **Arg tool** proposed — Jev selected a tool but won't write arguments | Expected path: `FallbackModel` (LLM) handles the whole step |
| Confidence always low / `p_yes ≈ 0.5` | State noisy or criterion ambiguous; evidence genuinely balanced | Apply state hygiene; tighten `criteria`; route mid-band to confirm |
| High confidence, wrong answer | In-schema miss — **type safety ≠ correctness** | Calibration bands, not trust; escalate low bands; verify with LLM/human |
| Accuracy drop after "adding more context" | Unrelated detail in state | Build a **small relevant state** within the latency budget |
| Trying to count / diff dates in Jev | Out of scope for 1.13 | Compute in code; pass the numbers as state |

### 7.3 Production Checklist

```
□ API key server-side only; rotated
□ model pinned or deliberately on jev-latest (→ jev-1.13.0)
□ every question typed: Choice ≤255 / Score 2–10 / Noul + criteria
□ state = evidence only; framing in instructions/criteria
□ state sized well under 32k; watch max_tokens_exceeded
□ arithmetic / counting / dates handled in code
□ confidence bands wired: high auto-act · medium confirm · low escalate
□ Noul thresholds use |p − 0.5| × 2 (or p_yes directly), never vibes
□ fallback path exists: human or LLM behind Jev (FallbackModel pattern)
□ latency budget 70–500ms verified under real load
```

---

*Back to [README](../README.md) — Module XIV overview*
