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

This section explains: the problem Jev solves, using a support-desk example you will meet again throughout the module.

Your support pipeline just received 4,000 tickets this hour. Each one needs three tiny judgments:

```
1. Classify the team          → billing / infra / bug / other
2. Confirm refund requested   → yes / no
3. Rate severity              → 1..5
```

The obvious 2026 move: call a frontier LLM (a top-tier chat model like the ones behind AI assistants) for every ticket. But that means:

- **3–10 seconds** per ticket, per question, serially or with expensive batching
- A wall of prose back — `"Based on my analysis, the ticket appears to be..."`
- A JSON blob you must parse, validate, retry on malformed quotes, and pray it stayed in schema (schema = the agreed answer format, e.g. "must be one of billing/infra/bug/other")
- Zero calibration: when it says "high confidence", that word means nothing statistically (calibration = the stated confidence matches the real chance of being right)

Using a frontier LLM for every tiny decision is like **calling an emergency surgical team to put on a band-aid** — or **hiring a top chef just to boil water**. They *can* do it. It is just not the right job for them.

When your software makes thousands of decisions an hour and only needs **a typed value plus a probability** (a value with a fixed type — like "one of these 4 teams" — plus a number for how likely it is right), generating strings is waste — pure token-shaped waste.

> *"TypeSafe describes Jev as a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out."*

> *"Jev decides, LLM writes."*
> — **TypeSafe**

**Jev** is the first **System One Model**: a transformer-based decision model that never generates a single token of text. (System One = the fast, automatic part of human thinking — reflexes, not essays.) You send state and named, typed questions; you get back `Choice`, `Score`, or `Noul` answers (the three answer shapes: pick-an-option, rate-1-to-5, and yes/no-with-odds) with full probability distributions and confidence — in **70–500ms**, at **$0.042 per million input tokens** with output free.

This module teaches you when to reach for it, how its three primitives work, how to call it (REST, SDKs, LangChain, Pydantic AI, OpenRouter), and where its limits are.

> **One-line summary:** Jev is a fast, cheap model that returns typed, calibrated decisions instead of prose — built for thousands of tiny judgments an hour.

### Why Jev & System One Models Matter?

> **"Stop generating prose to get a boolean. Ask a typed question. Get a calibrated answer."**

#### 3 Pieces of Scientific & Practical Evidence

How to read this table: each row is one source of evidence. **#** = row number, **Research / Source** = who measured it, **Key Finding** = the result in one line. For instance, row 2 says Jev answers in 70–500ms where a frontier LLM takes 3 to 329 seconds for the same decision.

| # | Research / Source | Key Finding |
|---|-------------------|----------------------|
| 1 | **TypeSafe (2026)** | On System One-shaped tasks, Jev is **40–200× faster and ~400× cheaper** than frontier LLMs — about **2 orders of magnitude** more efficient overall |
| 2 | **TypeSafe latency data** | End-to-end **70–500ms** per request vs **3–329s** for frontier LLMs on the same decision-shaped work |
| 3 | **RLCD calibration** | **~80% of answers scored 0.8 are actually correct** — confidence is measured, not vibes; and because the answer space is closed, Jev **cannot hallucinate out-of-schema values** |

(RLCD = the training method TypeSafe uses to teach the model to score its own confidence honestly; "closed answer space" = Jev can only answer with values from your allowed list, so it cannot invent "banana" for a yes/no question.)

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

(System Two = the slow, deliberate part of human thinking — the part that writes essays. In short: LLM = talks to people; Jev = answers to code.)

Where does this sit in the framework? Previous modules built the **harness** (the environment one agent runs in), the **loop** (harness + schedule + state + verification), and the **graph** (the durable knowledge substrate). Jev is a new layer: the **semantic decision engine** (a component that turns meaning into decisions) you embed *inside* those systems — routing loop items, gating tool calls, verifying LLM output — without paying LLM latency for a yes/no.

**Analogies**: The LLM is an **articulate writer / secretary** — eloquent, flexible, slow to get to the point, occasionally invents facts. Jev is an **ultrafast reflex judge** — reads the case, returns a verdict and the odds, done in a blink. Or: a **traffic light** (Jev — instant, binary/typed, everyone obeys it) versus a **tour guide** (LLM — narrates, explains, wanders). You need both on a trip; you do not ask the tour guide to decide whether the light is red.

**If you skip this**: you keep paying frontier-LLM prices and 3–329 second latencies to classify a ticket and confirm a boolean; you keep regex-parsing JSON booleans out of prose (that is: extracting a "true"/"false" out of a sentence with pattern matching, which breaks easily); and you keep accepting overconfident, zero-calibration "high confidence" strings from a model that was never trained to be right *at a stated probability*.

> **One-line summary:** Jev and LLMs are complements — the LLM writes language, Jev makes the fast, cheap, calibrated decisions your code acts on.

## Overview

**Jev & System One Models** is the practice of putting a **fast, calibrated, typed decision layer** inside your software — so that classification, rating, and gating become function calls instead of prose-generation sessions.

Unlike Modules VII–XIII, which organize how agents *act and remember*, this module focuses on the **decision primitive**: unstructured state in → typed probabilistic decisions out, evaluated in parallel in a single pass. (A "primitive" here = one of the three basic answer shapes Jev can return.)

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

> **One-line summary:** Jev sits inside your software as a decision layer: state and typed questions go in, calibrated typed answers come out in one parallel pass.

## Learning Path (Directory Structure)

This section explains: how the module files are organized, so you can read one small piece at a time.

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

This section explains: the order to read the directories in, and a "which file answers which question" lookup table.

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

How to read this table: the left column is a goal you might have right now; the right column is the directory that answers it. For instance, "I want to make my first API call" → open `03-api/`.

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

> **One-line summary:** Read top to bottom (concepts → primitives → API → calibration → patterns → limits), or jump straight to the directory matching your current question.

---

## Real-World Case Studies

This section explains: five real integrations, to show Jev working in production-shaped setups rather than toy examples.

### 1. LangChain — Routing Middleware + AutoModeMiddleware

LangChain ships an official Jev integration. `TypeSafeClassifier` answers named questions via `.invoke()` (state + questions), and two middleware patterns put it to work (middleware = a small component that sits in front of your chain and acts before the LLM runs):

How to read this table: each row is one shipped pattern. **Pattern** = its name, **What Jev does** = the single job Jev handles inside it.

| Pattern | What Jev does |
|---------|----------------|
| **Routing middleware** | Classifies the incoming request → routes it to the right chain/tool before the LLM ever runs |
| **AutoModeMiddleware** | Attaches one more question to risky tool calls — Jev's pick **blocks** the call when the answer says "no" |

The classifier returns typed answers + distributions, so the middleware branches on **values**, not on parsing prose.

> **One-line summary:** LangChain uses Jev as a pre-LLM router and a safety gate on risky tool calls.

### 2. Pydantic AI — TypeSafeModel, a Decide-Only Agent

Pydantic AI gains a `TypeSafeModel`: each field of your `output_type` becomes **one question**; the field `description` is the question text; the docstring/instructions are the framing. (Pydantic = the Python library that validates data shapes; `output_type` = the structured answer you ask the agent to produce.) TypeSafe calls this pairing **"probably the most important concept"** — because it is the *opposite habit* from prompting an LLM (where instructions dominate and structure is an afterthought). With tools attached, every request carries one extra question: *"which of these does the text call for?"* — `typesafe_tool_call_threshold` defaults to `0.6`.

> **One-line summary:** In Pydantic AI, you declare typed output fields and each field becomes one Jev question — structure first, prose second.

### 3. OpenRouter — One API Key to jev-1.13

`POST https://openrouter.ai/api/alpha/decisions` with model `typesafe/jev-1.13` — or point the TypeSafe TS SDK's base URL at OpenRouter. (OpenRouter = a service that gives you many AI models behind one key.) The use case is blunt: **one key, many models**. Teams already routing through OpenRouter get Jev decisions without a second vendor integration.

> **One-line summary:** If you already use OpenRouter, you can add Jev with zero new vendor setup — just another model name on your existing key.

### 4. Verified Cascade — LLM Writes, Jev Verifies

This section explains: the cheapest way to keep LLM output safe at high volume — let the LLM draft, then let Jev check the draft.

```
LLM drafts the answer / code / ticket reply
        │
        ▼
Jev asks: "is this in policy?" (Noul) + "which category?" (Choice)
        │
        ├─ high confidence, P(pass) ≥ threshold ──► ship it
        └─ low confidence / fail ─────────────────► escalate to human or stronger LLM
```

Cheapest correct architecture for high-volume pipelines: generation stays with the LLM; every gate, rubric check, and category pick is a calibrated Jev call. (P(pass) = the probability Jev assigns to "this passes the check".)

> **One-line summary:** Let the LLM draft and Jev gate-keep — you only pay for human review when Jev is unsure.

### 5. Spice AI — Jev Called from SQL

Spice AI lets you **call Jev from SQL** (SQL = the query language for databases — so decisions become rows in a query result): decisions become query-shaped:

> 📄 **Example code:** [`examples/01-5-spice-ai-jev-called-from-sql.sql`](examples/01-5-spice-ai-jev-called-from-sql.sql)

Map-reduce over a large dataset without ever leaving the warehouse: the dataset is the state fan-out (each row is one state sent to Jev), Jev is the reducer (it collapses each row's answer into a value), and the typed score lands back in the table.

> **One-line summary:** Spice AI turns Jev into a SQL-callable function, so you can score millions of rows in the warehouse without exporting data.

---

## Reference Materials

This section explains: where to read more — source articles above, and the tools you would actually install below.

### Articles & Sources

- [TypeSafe — Launch blog (Jev & System One Models)](https://typesafe.ai) — the announcement, RLCD, pricing, calibration
- [LangChain — Building a harness with Jev](https://blog.langchain.com) — TypeSafeClassifier + middleware patterns
- [Wikipedia — Jev (AI model)](https://en.wikipedia.org/wiki/Jev_(AI_model)) — model history, naming, release timeline
- [Pydantic AI — TypeSafeModel docs](https://ai.pydantic.dev) — field-per-question, framing, tool calling
- [OpenRouter — Jev on the decisions endpoint](https://openrouter.ai) — `typesafe/jev-1.13`
- [Refix — Jev explainer](https://refix.com) — practical walkthrough
- [Spice AI docs — call Jev from SQL](https://spice.ai) — warehouse-native decisions

> **One-line summary:** These seven links are the primary sources — start with the TypeSafe launch blog, which explains RLCD, pricing, and calibration in one place.

### Frameworks & Tools

How to read this list: each bullet is an installable client or integration; the part after the dash tells you which Jev feature it exposes. For instance, the Python SDK is the official client for the raw `POST /v1/systemone` endpoint.

- **TypeSafe Python SDK** — official Python client for `POST /v1/systemone`
- **TypeSafe JavaScript SDK** — official JS client; base URL overridable (e.g. to OpenRouter)
- **LangChain** — `TypeSafeClassifier`, routing middleware, `AutoModeMiddleware`
- **Pydantic AI** — `TypeSafeModel`, `typesafe_tool_call_threshold`, `FallbackModel`
- **OpenRouter** — `POST /v1/../alpha/decisions`, model `typesafe/jev-1.13`
- **Spice AI** — call Jev from SQL
- **Refix** — workflow integration

> **One-line summary:** Start with the TypeSafe blog for the concepts, then pick the SDK that matches your stack from the tools list.

---

> **"A frontier LLM can write you a sonnet about a red light. Jev will tell you, in 90 milliseconds, that it is red — with 0.93 confidence."**

> *"Jev decides, LLM writes. Build the decision layer first; the prose is the easy part."*

---

*Part of the [AI Coding Skills Framework](../..) — Module XIV: Jev & System One Models*
