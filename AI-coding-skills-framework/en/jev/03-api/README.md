# 🔌 03. API & Integrations

> This section covers **the endpoint and sign-in**, **what requests and replies look like** with a full JSON example, **the official SDKs**, and the four ways to connect — **Pydantic AI**, **LangChain**, **OpenRouter**, plus the **limits and errors** to handle before you ship. See [README.md](../README.md) for context and [02-primitives](../02-primitives/) for what Choice / Score / Noul mean.

---

## 1. Endpoint & Authentication

This section covers where Jev lives on the network and how to sign in. It matters because the transport is deliberately ordinary — nothing new to learn here.

> **📌 Core Concept**
>
> **Definition:** Jev is reached via **`POST https://api.typesafe.ai/v1/systemone`** with a **Bearer API key** (Bearer = a standard HTTP header that carries your secret key: `Authorization: Bearer <key>`). The body carries `model`, `state`, and `questions`; model aliases map `jev-latest` → `jev-1.13.0`.
> **Analogy:** It looks exactly like calling an LLM API — because the *transport* is deliberately boring. The novelty is entirely in what comes back: typed decisions with distributions, not a token stream.
> **Why it matters:** Zero new protocol skills required. If you can hold an API key and POST JSON, you can ship a decision layer today — the interesting decisions are which questions to ask and which confidence band to act on.

### 1.1 The Basics

How to read it: each row is one connection fact; for instance, "Auth" shows the exact header format and "Price" is what you pay per million input tokens.

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

> 📄 **Example code:** [`examples/01-1-1-the-basics.sh`](examples/01-1-1-the-basics.sh)

> **One-line summary:** One boring HTTPS POST with a bearer key — all the novelty is in the typed response.

### 1.2 Key Handling

Read the flow top down: the key lives in an environment variable, travels only in server-side headers, and reaches exactly one endpoint.

```
TYPESAFE_API_KEY   env var (never commit)
       │
       ▼
Authorization: Bearer sk-…      ← server-side only; rotate on leak
       │
       ▼
One key → /v1/systemone          (or the same key pointed at OpenRouter — §6)
```

Gloss: env var = an environment variable, a secret your program reads at runtime instead of hard-coding; rotate = replace the key after it leaks.

> **One-line summary:** Keep the key in a server-side env var, never in code or logs.

---

## 2. Request & Response

This section shows a full request and what comes back, block by block.

> **📌 Core Concept**
>
> **Definition:** A request is `state` + a named `questions` map; the response nests answers under `answers.<name>` with the primitive-specific payload (`.choice` / `.score` / `.noul`), plus **probabilities** and **confidence**. All questions in one request are evaluated in parallel in one pass.
> **Analogy:** Like a lab requisition form: one specimen (`state`), several tests (`questions`), one report back with a **separate result block per test** — you never re-submit the specimen to run the second test.
> **Why it matters:** One round-trip buys N decisions at 70–500ms. Design your request so a single call covers the whole decision step (classify + gate + rate) rather than three serial LLM-style calls.

### 2.1 Full Request Example

Three questions — one Choice, one Noul, one Score — in a single pass:

> 📄 **Example code:** [`examples/02-2-1-full-request-example.json`](examples/02-2-1-full-request-example.json)

### 2.2 Response Shape

> 📄 **Example code:** [`examples/03-2-2-response-shape.json`](examples/03-2-2-response-shape.json)

> **One-line summary:** The reply carries one typed block per question, each with probabilities and confidence.

### 2.3 Reading the Blocks

How to read it: each row is one answer type from the response; "How to read it" tells you which field to act on. For instance, for a `choice` answer you branch on `selected` and use `confidence` as a gate.

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

> **One-line summary:** One request, one report with a separate typed block per question — read the block, gate on the band.

---

## 3. Official SDKs

This section covers the ready-made client libraries. They matter because they remove boilerplate and give you a portable escape hatch.

> **📌 Core Concept**
>
> **Definition:** TypeSafe ships **official Python and JavaScript SDKs** (SDK = a client library that wraps the raw HTTP calls) that wrap `/v1/systemone`. Both accept a custom base URL — which is how you point the TypeSafe TS SDK at **OpenRouter** (§6) without changing application code.
> **Analogy:** A **power adapter** — the appliance (your decision logic) doesn't change when you plug into a different country's outlet (TypeSafe direct vs OpenRouter).
> **Why it matters:** SDKs remove hand-rolled `requests`/`fetch` boilerplate, keep `model` aliases current, and — via base URL — give you a vendor-portable seam for the day you want a second route to the same model.

### 3.1 Python Quickstart

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-3-1-python-quickstart.py`](examples/04-3-1-python-quickstart.py)

</details>

> **One-line summary:** Install the SDK, set the key, send state + questions, get typed answers.

### 3.2 JavaScript Quickstart

<details>
<summary>JavaScript Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-3-2-javascript-quickstart.js`](examples/05-3-2-javascript-quickstart.js)

</details>

> **One-line summary:** Same shape as Python: client, key, state + questions, typed answers.

### 3.3 Pointing the SDK at OpenRouter

Same client, different base URL — no application restructure:

> 📄 **Example code:** [`examples/06-3-3-pointing-the-sdk-at-openrouter.py`](examples/06-3-3-pointing-the-sdk-at-openrouter.py)

Full OpenRouter mechanics in §6.

> **One-line summary:** Change one base-URL string and the same SDK code now reaches Jev through OpenRouter.

---

## 4. Pydantic AI — TypeSafeModel

This section explains the Python integration that turns your data classes into Jev questions.

> **📌 Core Concept**
>
> **Definition:** In Pydantic AI, **`TypeSafeModel`** turns your `output_type` into Jev questions: **each field = one question**, **field `description` = the question text**, and **docstring / `instructions` = the framing** (Pydantic = the Python library for typed data classes; a docstring = the free-text note under a class definition). TypeSafe calls this pairing **"probably the most important concept"** — because it is the *opposite habit* from prompting an LLM.
> **Analogy:** An LLM prompt is a **briefing memo** you hope gets followed; a `TypeSafeModel` is a **form with labeled fields** — the label *is* the ask. You wouldn't bury "Rate urgency 1–5" inside a memo's third paragraph; you put it on the line marked *Urgency*.
> **Why it matters:** Once fields and descriptions carry the decisions, your Jev agent becomes typed end-to-end: valid answers by construction, parallel evaluation under the hood, and confidence bands your code can branch on — without any string parsing.

### 4.1 Field → Question Mapping

How to read it: each row maps one Python construct to what it becomes as a Jev question. For instance, a nested model becomes namespaced questions like `outer.inner`.

| Pydantic construct | Becomes |
|--------------------|---------|
| Each field of `output_type` | **One question**, evaluated in the same parallel pass |
| Field `description=...` | **The question text** (what Jev answers) |
| Class docstring / agent `instructions` | **Framing** — tone, persona, global context |
| Nested models | Namespaced questions (`outer.inner`) |
| `list[T]` fields | **Fan-out** — one question per element |
| Bare `bool` **without** description | **`UserError`** — a boolean needs a stated question |

> 📌 **The habit inversion:** with an LLM you invest in *instructions* and hope structure emerges; with `TypeSafeModel` you invest in **field descriptions** (the questions) and keep instructions as light framing. Opposite habit — TypeSafe: *"probably the most important concept."*

> **One-line summary:** Each field is a question, its description is the question text — effort moves from instructions to field descriptions.

### 4.2 Decide-Only Agent

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-4-2-decide-only-agent.py`](examples/07-4-2-decide-only-agent.py)

</details>

> **One-line summary:** One-field output type + framing instructions = the smallest possible Jev agent.

### 4.3 Tools Attached — The Extra Question

This subsection explains what changes when tools are attached: Jev gains one extra "which tool?" question, and how the two tool kinds behave.

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

Gloss: no-arg tool = a tool that needs no parameters, so Jev's pick alone is enough; arg tool = a tool that needs parameters, which Jev cannot write — so an LLM takes over the whole step.

> **One-line summary:** With tools, Jev picks the tool; no-argument tools run directly, argument tools hand the whole step to a fallback LLM.

### 4.4 Other TypeSafeModel Details

Four leftover rules worth knowing before you ship:

- **List fan-out:** `list[Item]` → one question per element, same pass — cheap map-reduce (see [02-primitives](../02-primitives/) §5.2).
- **Nested models:** `outer.inner` namespacing keeps deep outputs addressable.
- **Instructions for a single question:** when you only need one verdict, a one-field `output_type` plus framing instructions is the minimal decide-only agent.
- **`UserError` on a bare bool:** `flag: bool` with **no description** raises `UserError` at runtime — Jev refuses to guess what your field means. Always write the question.

> **One-line summary:** Lists fan out, nests namespace, and a bare `bool` without a description is a hard error — always write the question.

---

## 5. LangChain — TypeSafeClassifier

This section covers the LangChain integration, whose main use is sitting in front of the LLM as a gatekeeper.

> **📌 Core Concept**
>
> **Definition:** LangChain's **`TypeSafeClassifier`** answers named questions over a state via **`.invoke(state, questions)`** and returns typed answers + distributions — designed to sit in **middleware** (code that runs between the incoming request and the LLM): route before the LLM runs, or gate risky tool calls with **`AutoModeMiddleware`**.
> **Analogy:** A **bouncer with a checklist** — the classifier doesn't join the party (generate text); it checks the list at the door and lets the right chain through, or stops the wrong tool call.
> **Why it matters:** Middleware is where decisions multiply: every incoming request, every tool call can carry one cheap parallel Jev pass instead of a deliberative LLM call — the LangChain-native version of "Jev routes and verifies, LLM provides the language."

### 5.1 Classifier Invocation

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-5-1-classifier-invocation.py`](examples/08-5-1-classifier-invocation.py)

</details>

> **One-line summary:** `.invoke(state, questions)` in, typed answers out — designed for the middleware slot.

### 5.2 Two Middleware Patterns

How to read it: each row is one placement pattern; "What Jev does" is the question it answers and "Effect" is what you get. For instance, routing middleware classifies the request before any LLM chain runs.

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

> **One-line summary:** Two middleware placements: route requests to the right chain, and block risky tool calls before they run.

---

## 6. OpenRouter — One Key, Many Models

This section covers the second way in: routing Jev through OpenRouter so one key reaches many models.

> **📌 Core Concept**
>
> **Definition:** Jev is available through OpenRouter at **`POST https://openrouter.ai/api/alpha/decisions`** with model **`typesafe/jev-1.13`** — or by setting the TypeSafe TS SDK's **base URL** to OpenRouter. The use case: **one API key, many models**.
> **Analogy:** An **airline alliance** — one booking desk (your OpenRouter key) reaches carriers (models) you'd otherwise open separate accounts for. Jev is a destination on the same ticket.
> **Why it matters:** Teams already standardizing on OpenRouter get System One decisions without a second vendor relationship, second key rotation process, or second billing line — the integration cost drops to one endpoint.

### 6.1 Direct Call

> 📄 **Example code:** [`examples/09-6-1-direct-call.sh`](examples/09-6-1-direct-call.sh)

How to read it: each row is one connection fact for the OpenRouter route; "Alternative" names the SDK-based way to the same place.

| Item | Value |
|------|-------|
| Endpoint | `POST https://openrouter.ai/api/alpha/decisions` |
| Model id | `typesafe/jev-1.13` |
| Auth | OpenRouter key (Bearer) |
| Alternative | TypeSafe TS SDK with `base_url` → OpenRouter (§3.3) |

**Use case:** *one key, many models* — LLMs for writing, `typesafe/jev-1.13` for deciding, single billing/auth surface.

> **One-line summary:** Same model through OpenRouter: one key, one bill, LLMs and Jev side by side.

---

## 7. Limits & Errors

This section lists the hard edges of jev-1.13 and the errors they produce. Read it before shipping — most incidents start at one of these boundaries.

> **📌 Core Concept**
>
> **Definition:** jev-1.13 boundaries you must design around: **text input only** (no files, no tool-arg writing), **64k total context** (32k state + longest question → past that, `ModelHTTPError: max_tokens_exceeded`), and the standing rule that **arithmetic, counting, and date comparison stay in code**.
> **Analogy:** A **specialist with a narrow chart** — brilliant on the verdict, but they can't open attachments, can't do long division, and their chart has a hard page limit. Do the mechanics *around* the specialist, not through them.
> **Why it matters:** Every production incident with a decision model starts at a boundary: a state that overflowed context, a count Jev was asked to do, a file it could never read. Learn the edges here — then read [07-limits-and-evaluation](../07-limits-and-evaluation/) before shipping.

### 7.1 Hard Limits (jev-1.13)

How to read it: "Limit" is the boundary, "Detail" explains it, "What to do instead" is the workaround. For instance, the arithmetic row says: compute counts in your code, then pass the numbers as state.

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

> **One-line summary:** Text-only input, 64k context ceiling, math in code — design around these and the model stays reliable.

### 7.2 Common Errors

How to read it: "Error / symptom" is what you observe, "Likely cause" is the usual reason, "Fix" is the remedy. For instance, always-low confidence usually means a noisy state, not a broken model.

| Error / symptom | Likely cause | Fix |
|-----------------|--------------|-----|
| `ModelHTTPError: max_tokens_exceeded` | State + longest question exceeded **64k** | Shrink state; summarize before sending |
| `UserError` (Pydantic AI) | A **bare `bool`** field with no `description` | Write the question — `Field(description="…")` |
| `ModelAPIError` (`ToolCallProposed`) | **Arg tool** proposed — Jev selected a tool but won't write arguments | Expected path: `FallbackModel` (LLM) handles the whole step |
| Confidence always low / `p_yes ≈ 0.5` | State noisy or criterion ambiguous; evidence genuinely balanced | Apply state hygiene; tighten `criteria`; route mid-band to confirm |
| High confidence, wrong answer | In-schema miss — **type safety ≠ correctness** | Calibration bands, not trust; escalate low bands; verify with LLM/human |
| Accuracy drop after "adding more context" | Unrelated detail in state | Build a **small relevant state** within the latency budget |
| Trying to count / diff dates in Jev | Out of scope for 1.13 | Compute in code; pass the numbers as state |

> **One-line summary:** Every common error maps to a known boundary — shrink the state, describe the bool, or route the step to the fallback LLM.

### 7.3 Production Checklist

A pre-ship checklist: each line is one thing to confirm before real traffic.

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

> **One-line summary:** Ten checks — key hygiene, typed questions, clean state, wired bands, a fallback path — and you are ready to ship.

---

*Back to [README](../README.md) — Module XIV overview*
