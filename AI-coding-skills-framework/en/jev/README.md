# ⚡ XIV. Jev & System One Models

> ## 📑 Table of Contents
>
> - [Opening Story](#opening-story)
> - [Why Jev & System One Models Matter?](#why-jev--system-one-models-matter)
> - [Overview](#overview)
> - [Learning Path (Directory Structure)](#learning-path-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### Opening Story

Your support pipeline just received 4,000 tickets this hour. Each one needs three tiny judgments:

```
1. Classify the team          → billing / infra / bug / other
2. Confirm refund requested   → yes / no
3. Rate severity              → 1..5
```

The obvious 2026 move: call a frontier LLM for every ticket. But that means:

- **3–10 seconds** per ticket, per question, serially or with expensive batching
- A wall of prose back — `"Based on my analysis, the ticket appears to be..."`
- A JSON blob you must parse, validate, retry on malformed quotes, and pray it stayed in schema
- Zero calibration: when it says "high confidence", that word means nothing statistically

Using a frontier LLM for every tiny decision is like **calling in an emergency surgical team to apply a band-aid** — or **hiring a Michelin chef to boil water**. The team *can* do it. It is spectacularly the wrong tool.

When your software makes thousands of decisions an hour and only needs **a typed value plus a probability**, generating strings is waste — pure token-shaped waste.

> *"TypeSafe describes Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."*

> *"Jev decides, LLM writes."*
> — **TypeSafe**

**Jev** is the first **System One Model**: a transformer-based decision model that never generates a single token of text. You send state and named, typed questions; you get back `Choice`, `Score`, or `Noul` answers with full probability distributions and confidence — in **70–500ms**, at **$0.042 per million input tokens** with output free.

This module teaches you when to reach for it, how its three primitives work, how to call it (REST, SDKs, LangChain, Pydantic AI, OpenRouter), and where its limits are.

### Why Jev & System One Models Matter?

> **"Stop generating prose to get a boolean. Ask a typed question. Get a calibrated answer."**

#### 3 Pieces of Scientific & Practical Evidence

| # | Research / Source | Key Finding |
|---|-------------------|----------------------|
| 1 | **TypeSafe (2026)** | On System One-shaped tasks, Jev is **40–200× faster and ~400× cheaper** than frontier LLMs — about **2 orders of magnitude** more efficient overall |
| 2 | **TypeSafe latency data** | End-to-end **70–500ms** per request vs **3–329s** for frontier LLMs on the same decision-shaped work |
| 3 | **RLCD calibration** | **~80% of answers scored 0.8 are actually correct** — confidence is measured, not vibes; and because the answer space is closed, Jev **cannot hallucinate out-of-schema values** |

#### Killer quotes:

> *"A frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."*
> — **TypeSafe, on Jev**

> *"System One Models = Fast, cheap, calibrated decisions a program can act on → No more parsing prose."*

#### Core philosophy:

```
System One Models = Fast, cheap, calibrated decisions a program can act on → No more parsing prose
```

**Important distinctions:**

```
LLM (System Two-ish) = Generates TEXT for PEOPLE   → chat, code, explanations (and occasionally hallucinations)
Jev (System One)     = Returns TYPED DECISIONS      → Choice / Score / Noul + probabilities, for SOFTWARE

They are complements, not replacements:
  "Jev decides and verifies; the LLM provides the language."
```

Where does this sit in the framework? Previous modules built the **harness** (the environment one agent runs in), the **loop** (harness + schedule + state + verification), and the **graph** (the durable knowledge substrate). Jev is a new layer: the **semantic decision engine** you embed *inside* those systems — routing loop items, gating tool calls, verifying LLM output — without paying LLM latency for a yes/no.

**Analogies**: The LLM is an **articulate writer / secretary** — eloquent, flexible, slow to get to the point, occasionally invents facts. Jev is an **ultrafast reflex judge** — reads the case, returns a verdict and the odds, done in a blink. Or: a **traffic light** (Jev — instant, binary/typed, everyone obeys it) versus a **tour guide** (LLM — narrates, explains, wanders). You need both on a trip; you do not ask the tour guide to decide whether the light is red.

**If you skip this**: you keep paying frontier-LLM prices and 3–329 second latencies to classify a ticket and confirm a boolean; you keep regex-parsing JSON booleans out of prose; and you keep accepting overconfident, zero-calibration "high confidence" strings from a model that was never trained to be right *at a stated probability*.

## Overview

**Jev & System One Models** is the practice of putting a **fast, calibrated, typed decision layer** inside your software — so that classification, rating, and gating become function calls instead of prose-generation sessions.

Unlike Modules VII–XIII, which organize how agents *act and remember*, this module focuses on the **decision primitive**: unstructured state in → typed probabilistic decisions out, evaluated in parallel in a single pass.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        JEV & SYSTEM ONE MODELS                              │
│                                                                             │
│   YOUR PROGRAM                                                              │
│   state (string / JSON / array of text)                                     │
│   + questions: { name: {type: choice|score|noul, ...} }                     │
│        │                                                                    │
│        ▼                                                                    │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  INTEGRATION SURFACES                                               │   │
│   │  REST API · Python/JS SDKs · LangChain TypeSafeClassifier           │   │
│   │  Pydantic AI TypeSafeModel · OpenRouter · Spice AI (SQL) · Refix    │   │
│   └───────────────────────────────┬─────────────────────────────────────┘   │
│                                   ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  JEV (jev-1.13.0 / jev-latest)                                     │   │
│   │  Transformer-based · trained on synthetic data via RLCD             │   │
│   │  Closed answer space · all questions evaluated in PARALLEL, 1 pass  │   │
│   │  70–500ms · $0.042 / M input tokens · output free                   │   │
│   └───────────────────────────────┬─────────────────────────────────────┘   │
│                                   ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  TYPED ANSWERS                                                      │   │
│   │  answers.<name>.choice / .score / .noul                             │   │
│   │  + full probability distribution + confidence                       │   │
│   └───────────────────────────────┬─────────────────────────────────────┘   │
│                                   ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  YOUR CODE OBSERVES THE THRESHOLD                                  │   │
│   │  confidence HIGH   → code auto-acts                                │   │
│   │  confidence MEDIUM → confirm / gather more context                 │   │
│   │  confidence LOW    → route to human or another system / LLM        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Division of labor** (the sentence to remember):

```
Jev decides and verifies things → the LLM provides the language.
```

## Learning Path (Directory Structure)

Module XIV is split into **dedicated files** so you can learn one part at a time — consistent with the `harness/` and `loop/` conventions (each module is `NN-name/README.md`):

```
jev/
├── README.md                 ← YOU ARE HERE — overview + learning path + case studies
├── 01-concepts/              ← What Jev is, System 1 vs System 2, naming, architecture,
│                                when to use / not, place in the agent ecosystem
├── 02-primitives/            ← The three primitives: Choice, Score, Noul;
│                                request shape, parallel evaluation, choosing one
├── 03-api/                   ← Endpoint & auth, request/response, SDKs,
│                                Pydantic AI, LangChain, OpenRouter, limits & errors
├── 04-calibration/           ← What confidence means (margin vs probability),
│                                RLCD calibration, confidence bands, failure modes
├── 05-patterns/              ← The 4 target workloads: workflow decisions,
│                                map-reduce, real-time, LLM verification
├── 06-jev-and-llm/           ← "Jev decides, LLM writes": verified cascades,
│                                routing, state hygiene, division of labor
└── 07-limits-and-evaluation/ ← jev-1.13 limits (text-only, 64k context),
                                 keeping arithmetic in code, evaluating decisions
```

> Each directory contains a `README.md` — consistent with the `harness/` and `loop/` conventions.

### Recommended Path

```
Step 1: Read this README.md to understand the context
   ↓
Step 2: 01-concepts/ — what Jev is, System 1 vs System 2, when to use it
   ↓
Step 3: 02-primitives/ — learn Choice, Score, Noul and when to pick each
   ↓
Step 4: 03-api/ — make your first call (REST, SDK, Pydantic AI, LangChain)
   ↓
Step 5: 04-calibration/ — understand confidence bands before trusting them
   ↓
Step 6: 05-patterns/ + 06-jev-and-llm/ — the 4 workloads + Jev/LLM division of labor
   ↓
Step 7: 07-limits-and-evaluation/ — know the edges before production
```

| You want to... | Read |
|-------------|-----|
| Understand what Jev is and why System One | [01-concepts](01-concepts/) |
| Choose between Choice, Score, and Noul | [02-primitives](02-primitives/) |
| Make your first API call | [03-api](03-api/) — endpoint + quickstart |
| Wire Jev into Pydantic AI | [03-api](03-api/) — TypeSafeModel |
| Wire Jev into LangChain middleware | [03-api](03-api/) — TypeSafeClassifier |
| Understand what confidence really means | [04-calibration](04-calibration/) |
| Classify / rate / gate inside a workflow | [05-patterns](05-patterns/) |
| Build "LLM writes, Jev verifies" | [06-jev-and-llm](06-jev-and-llm/) |
| Know jev-1.13's limits & error modes | [07-limits-and-evaluation](07-limits-and-evaluation/) |

---

## Real-World Case Studies

### 1. LangChain — Routing Middleware + AutoModeMiddleware

LangChain ships an official Jev integration. `TypeSafeClassifier` answers named questions via `.invoke()` (state + questions), and two middleware patterns put it to work:

| Pattern | What Jev does |
|---------|----------------|
| **Routing middleware** | Classifies the incoming request → routes it to the right chain/tool before the LLM ever runs |
| **AutoModeMiddleware** | Attaches one more question to risky tool calls — Jev's pick **blocks** the call when the answer says "no" |

The classifier returns typed answers + distributions, so the middleware branches on **values**, not on parsing prose.

### 2. Pydantic AI — TypeSafeModel, a Decide-Only Agent

Pydantic AI gains a `TypeSafeModel`: each field of your `output_type` becomes **one question**; the field `description` is the question text; the docstring/instructions are the framing. TypeSafe calls this pairing **"probably the most important concept"** — because it is the *opposite habit* from prompting an LLM (where instructions dominate and structure is an afterthought). With tools attached, every request carries one extra question: *"which of these does the text call for?"* — `typesafe_tool_call_threshold` defaults to `0.6`.

### 3. OpenRouter — One API Key to jev-1.13

`POST https://openrouter.ai/api/alpha/decisions` with model `typesafe/jev-1.13` — or point the TypeSafe TS SDK's base URL at OpenRouter. The use case is blunt: **one key, many models**. Teams already routing through OpenRouter get Jev decisions without a second vendor integration.

### 4. Verified Cascade — LLM Writes, Jev Verifies

```
LLM drafts the answer / code / ticket reply
        │
        ▼
Jev asks: "is this in policy?" (Noul) + "which category?" (Choice)
        │
        ├─ high confidence, P(pass) ≥ threshold ──► ship it
        └─ low confidence / fail ─────────────────► escalate to human or stronger LLM
```

Cheapest correct architecture for high-volume pipelines: generation stays with the LLM; every gate, rubric check, and category pick is a calibrated Jev call.

### 5. Spice AI — Jev Called from SQL

Spice AI lets you **call Jev from SQL** — decisions become query-shaped:

```sql
SELECT ticket_id, jev_score(state_text) AS urgency FROM tickets;
```

Map-reduce over a large dataset without ever leaving the warehouse: the dataset is the state fan-out, Jev is the reducer, and the typed score lands back in the table.

---

## Reference Materials

### Articles & Sources

- [TypeSafe — Launch blog (Jev & System One Models)](https://typesafe.ai) — the announcement, RLCD, pricing, calibration
- [LangChain — Building a harness with Jev](https://blog.langchain.com) — TypeSafeClassifier + middleware patterns
- [Wikipedia — Jev (AI model)](https://en.wikipedia.org/wiki/Jev_(AI_model)) — model history, naming, release timeline
- [Pydantic AI — TypeSafeModel docs](https://ai.pydantic.dev) — field-per-question, framing, tool calling
- [OpenRouter — Jev on the decisions endpoint](https://openrouter.ai) — `typesafe/jev-1.13`
- [Refix — Jev explainer](https://refix.com) — practical walkthrough
- [Spice AI docs — call Jev from SQL](https://spice.ai) — warehouse-native decisions

### Frameworks & Tools

- **TypeSafe Python SDK** — official Python client for `POST /v1/systemone`
- **TypeSafe JavaScript SDK** — official JS client; base URL overridable (e.g. to OpenRouter)
- **LangChain** — `TypeSafeClassifier`, routing middleware, `AutoModeMiddleware`
- **Pydantic AI** — `TypeSafeModel`, `typesafe_tool_call_threshold`, `FallbackModel`
- **OpenRouter** — `POST /v1/../alpha/decisions`, model `typesafe/jev-1.13`
- **Spice AI** — call Jev from SQL
- **Refix** — workflow integration

---

> **"A frontier LLM can write you a sonnet about a red light. Jev will tell you, in 90 milliseconds, that it is red — with 0.93 confidence."**

> *"Jev decides, LLM writes. Build the decision layer first; the prose is the easy part."*

---

*Part of the [AI Coding Skills Framework](../..) — Module XIV: Jev & System One Models*
