# 🧭 05. Production Patterns

> This section catalogs the **five production patterns** for Jev — routing & triage, classification at scale, gating agent actions, verifying LLM output, and ranking & filtering — mapped onto the **four supported workloads**, each with a core-concept card, code, and a thresholds/notes table. Read [README.md](../README.md) first for the overall context of Module XIV — Jev & System One Models.

---

## 1. Overview — 4 Workloads × 5 Patterns

> **📌 Core Concept**
>
> **Definition:** The **division of labor** is simple: **"Jev decides, code acts, LLM writes."** Jev is a semantic decision layer — state in, bounded typed result out; ordinary code performs the action the decision authorizes; the LLM is reserved for anything that requires generating language.
> **Analogy:** Like a **traffic intersection**: Jev is the signal (decides go/stop/which lane), the code is the cars (actually move), and the LLM is the radio announcer (explains, drafts, narrates). Asking the announcer to hold up traffic is how you get a 2-second green light.
> **Why it matters:** Every pattern below is a rearrangement of the same three roles. Get the roles wrong — LLM makes the gate decision, or Jev tries to write the explanation — and you pay in latency, cost, or correctness.

### 1.1 Workload × Pattern Map

| # | Workload | Best-fit patterns | Why |
|---|----------|-------------------|-----|
| 1 | **Decision steps in workflows** | Routing/triage, Gating agent actions | One decision per step, sub-second, typed |
| 2 | **Map-reduce over datasets** | Classification at scale, Ranking & filtering | 70–500 ms per record, cheap ($0.042/1M input tokens, free output) |
| 3 | **Real-time apps** | Routing/triage, Gating | 40–200× faster than an LLM call; added questions barely change latency |
| 4 | **Verification of LLM output** | Verifying LLM output (Verified Cascade) | Noul/Choice check on a draft — fast, parallel |

```
THE COMMON WORKFLOW (all five patterns share this spine):

  Gather small relevant state
           │
           ▼
  ┌─────────────────┐
  │   JEV (one      │  ← all questions evaluated in parallel, one pass
  │   POST, parallel│     70–500 ms
  │   questions)    │
  └────────┬────────┘
           ▼
  selected + probabilities + confidence
           │
           ▼
  compare to THRESHOLD
      │            │
   above         below
      │            │
      ▼            ▼
  CODE ACTS    ESCALATE (human / more context / LLM)
```

> Added questions barely change latency — so batch related decisions (e.g. `route_ticket` + `priority`) into **one call**.

---

## 2. Routing & Triage

> **📌 Core Concept**
>
> **Definition:** Route an incoming item (ticket, email, event) to the **right team, queue, or priority** using a Choice question for the destination and a Score question for urgency — both answered in a single parallel pass.
> **Analogy:** Like a **hospital triage nurse**: one glance, two judgments — *which ward* and *how urgent* — before the patient ever sees a doctor. The nurse doesn't write the chart; she decides where it goes.
> **Why it matters:** Triage is the highest-leverage first pattern: it is low-risk (wrong queue is recoverable), sub-second, and immediately visible in metrics — the ideal way to earn trust in Jev before gating anything destructive.

### Pattern Card — Routing & Triage

| | |
|---|---|
| **Questions** | 1 × Choice (team/queue) + 1 × Score (priority) — one call |
| **Workload fit** | Decision steps, real-time |
| **Latency** | One pass, 70–500 ms for both questions |
| **Threshold posture** | Medium band = auto-route with a review flag; low = human triage |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
TEAMS = ["billing", "infra", "product", "data"]

def triage(ticket: dict) -> dict:
    """One call → queue + priority, evaluated in parallel."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": ticket,          # subject + body snippet + customer tier
            "questions": {
                "queue":   {"type": "choice", "options": TEAMS},
                "priority": {"type": "score",
                             "levels": ["p0", "p1", "p2", "p3"]},
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    queue = res["queue"]
    priority = res["priority"]

    return {
        "queue": queue["selected"],
        "queue_p": queue["probabilities"].get(queue["selected"]),
        "priority": priority["selected"],
        "priority_confidence": priority["confidence"],
        "band": "auto" if queue["confidence"] >= 0.7 else "human_review",
    }
```

</details>

### Thresholds & Notes

| Setting | Guidance |
|---------|----------|
| Queue confidence ≥ 0.7 | Auto-route (starting point — retune on your labels) |
| Below → | Human triage queue with full context attached |
| State | Small & relevant only — unrelated detail lowers accuracy (see [07](../07-limits-and-evaluation/)) |
| Latency note | Sub-second for both questions; safe for interactive intake |

---

## 3. Classification & Tagging at Scale

> **📌 Core Concept**
>
> **Definition:** Run a **Choice/Score classification on every record** of a dataset — the output is a *ready-to-store label* with a probability, not prose. Because each decision costs 70–500 ms and ~$0.042/1M input tokens (output free), bulk classification is economically trivial next to LLM annotation.
> **Analogy:** Like an **assembly-line quality stamp**: each item passes the sensor, gets stamped PASS/FAIL/grade, moves on. The sensor doesn't write an essay about the item.
> **Why it matters:** This is the map-reduce workload's map phase. Labels land in your database; downstream filters, reports, and retrieval all consume them — no tokens spent generating tag explanations.

### Pattern Card — Classification at Scale

| | |
|---|---|
| **Questions** | 1+ Choice (taxonomy) per record |
| **Workload fit** | Map-reduce over datasets |
| **Latency** | Per record 70–500 ms; scale with async concurrency |
| **Threshold posture** | Low-confidence records → second pass, LLM, or human queue |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import asyncio
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
CONCURRENCY = 32
LABEL_THRESHOLD = 0.75

async def classify_one(client: httpx.AsyncClient, record: dict) -> dict:
    r = await client.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": record,
            "questions": {
                "category": {
                    "type": "choice",
                    "options": ["news", "opinion", "research", "spam"],
                }
            },
        },
        timeout=10.0,
    )
    r.raise_for_status()
    cat = r.json()["results"]["category"]
    p = cat["probabilities"].get(cat["selected"], 0.0)
    return {
        "id": record.get("id"),
        "label": cat["selected"],
        "label_p": p,
        # below threshold → send to LLM or human; don't silently accept
        "needs_review": p < LABEL_THRESHOLD,
    }

async def classify_all(records: list[dict]) -> list[dict]:
    sem = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient() as client:
        async def bound(rec):
            async with sem:
                return await classify_one(client, rec)
        return await asyncio.gather(*(bound(r) for r in records))
```

</details>

### Thresholds & Notes

| Setting | Guidance |
|---------|----------|
| `label_p` ≥ 0.75 | Store label directly |
| below → | `needs_review=True` → LLM pass or human queue |
| Fan-out | Map-reduce: per-record decisions, aggregated; **latency scales per decision** |
| Cost | Output is free — storing full distributions is cheap |

---

## 4. Gating Agent Actions

> **📌 Core Concept**
>
> **Definition:** Before an agent executes a **side-effecting tool call**, ask Jev a **Noul** question ("does the user authorize this?") and **block below threshold**. The gate sits *between* intent and execution.
> **Analogy:** Like a **dead man's switch on a machine**: the machine only runs while the switch is held — no switch signal, no motion. The gate doesn't operate the machine; it *permits* the operation.
> **Why it matters:** LLM agents are fluent at deciding to "just do it". A typed, calibrated Noul in front of destructive tools (delete, charge, send) converts an open-ended judgment into a bounded, logged, threshold-controlled check. In LangChain this ships as **AutoModeMiddleware**.

### Pattern Card — Gating Agent Actions

| | |
|---|---|
| **Questions** | 1 × Noul (`P(yes)` + derived confidence) |
| **Workload fit** | Decision steps in workflows (agent tool loop) |
| **Latency** | 70–500 ms — invisible next to the tool's own I/O |
| **Threshold posture** | High (e.g. `typesafe_tool_call_threshold` default 0.6 is a *starting point*) |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
AUTH_THRESHOLD = 0.80   # tune from YOUR labelled examples, not defaults

def authorize_destructive_action(state: dict) -> tuple[bool, dict]:
    """Noul gate before a destructive tool call. Jev classifies; code decides."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": state,   # user's latest message + tool name + target summary
            "questions": {
                "user_authorizes": {"type": "noul"},
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    n = r.json()["results"]["user_authorizes"]
    p_yes = n["probability"]                    # P(yes), 0–1
    # Noul has no separate confidence: margin = |p - 0.5| * 2
    margin = abs(p_yes - 0.5) * 2

    audit = {"p_yes": p_yes, "margin": margin, "threshold": AUTH_THRESHOLD}

    # below threshold → block; the agent must not fire the tool
    allowed = p_yes >= AUTH_THRESHOLD and margin >= 0.5
    return allowed, audit


def run_tool_if_authorized(tool_name: str, args: dict, state: dict):
    allowed, audit = authorize_destructive_action(state)
    log_decision(tool_name, audit)            # request id, probs, threshold, outcome
    if not allowed:
        return escalate_or_ask_human(tool_name, audit)
    return execute_tool(tool_name, args)      # code acts
```

</details>

### Thresholds & Notes

| Setting | Guidance |
|---------|----------|
| Noul `P(yes)` ≥ threshold AND margin healthy | Allow tool |
| below → | Block; ask human / rephrase / gather context |
| **Caveat** | **Jev does not judge whether running the tool is *safe*** — it classifies (e.g. "does the user authorize this"). Approval policy is the **agent's/your** job |
| Related | LangChain `AutoModeMiddleware` gates risky tool calls; Pydantic AI `typesafe_tool_call_threshold` (default **0.6** — a starting point, not validated) |

---

## 5. Verify LLM Output — The Verified Cascade

> **📌 Core Concept**
>
> **Definition:** The LLM **drafts**; Jev **checks** the draft against a known standard (policy text, schema, ground truth) with a Noul or Choice question; pass → continue, fail → fallback (stronger LLM, human, or discard). **"Jev decides, LLM writes."**
> **Analogy:** Like a **press proofreader** who doesn't rewrite the article but marks it APPROVE/REJECT against the style guide — fast, typed, and independent of the writer's mood.
> **Why it matters:** Verification is where a *decision* model earns its keep inside LLM systems: the expensive model produces language once, the cheap calibrated model gates it in <500 ms — and the gate can run in harness loops and CI on every iteration.

### Pattern Card — Verify LLM Output

| | |
|---|---|
| **Questions** | Noul (grounded? matches policy?) or Choice (which violation?) |
| **Workload fit** | Verification of LLM output; harness/loop steps |
| **Latency** | One fast check per draft — parallelizable per criterion |
| **Threshold posture** | High bar to *pass*; fail → fallback path |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
PASS_THRESHOLD = 0.85

def verified_cascade(policy_text: str, draft: str) -> dict:
    """LLM drafts → Jev verifies grounding against policy → pass/fail."""
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "jev-latest",
            "state": {
                "policy": policy_text,     # the standard to check against
                "draft": draft,            # what the LLM wrote
            },
            "questions": {
                "grounded_in_policy": {"type": "noul"},
                "worst_violation": {       # only consulted when Noul fails
                    "type": "choice",
                    "options": ["none", "unsupported_claim",
                                "wrong_number", "tone", "pii_leak"],
                },
            },
        },
        timeout=5.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    p_pass = res["grounded_in_policy"]["probability"]
    if p_pass >= PASS_THRESHOLD:
        return {"status": "pass", "p_pass": p_pass, "draft": draft}

    # fail → fallback: stronger LLM, human review, or discard
    return {
        "status": "fail",
        "p_pass": p_pass,
        "flag": res["worst_violation"]["selected"],
        "next": "fallback_llm",   # e.g. call a stronger model for a rewrite
    }
```

</details>

### Thresholds & Notes

| Setting | Guidance |
|---------|----------|
| Noul `P(yes/pass)` ≥ 0.85 | Accept draft |
| below → | Fallback: stronger LLM / human / discard; use the Choice flag to *route* the rework |
| In loops/harnesses | Run as the **verifier step** each iteration — see [06 — Jev + LLM](../06-jev-and-llm/) |
| Watch | High confidence ≠ correct ([04 — Calibration](../04-calibration/)) — keep a fallback even above threshold for costly outputs |

---

## 6. Ranking & Filtering

> **📌 Core Concept**
>
> **Definition:** Score each candidate against **ordered levels**, then **sort by the probability-weighted score** (which may fall *between* levels) to produce a ranked shortlist; or filter with Noul/Choice thresholds.
> **Analogy:** Like a **sommelier's tasting ladder** — each wine gets a grade on the house scale, and the list comes back ordered. The grade is comparable across wines precisely because the scale is fixed and typed.
> **Why it matters:** RAG pipelines retrieve *too much*; a fast Score pass re-ranks the shortlist with a calibrated, typed judgment instead of asking an LLM to compare every pair (O(n²) prose).

### Pattern Card — Ranking & Filtering

| | |
|---|---|
| **Questions** | Score (relevance/quality levels) per candidate; Noul to filter |
| **Workload fit** | Map-reduce; decision steps inside RAG |
| **Latency** | Per candidate 70–500 ms; shortlist sizes are naturally small |
| **Threshold posture** | Filter below a floor score; rank the rest |

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
LEVELS = ["irrelevant", "weak", "relevant", "core"]
FLOOR = "weak"   # drop everything at or below this level


def rerank_shortlist(query: str, candidates: list[dict]) -> list[dict]:
    """Score each candidate in one batch of parallel questions, then sort."""
    questions = {
        f"rel_{i}": {"type": "score", "levels": LEVELS}
        for i in range(len(candidates))
    }
    r = httpx.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "jev-latest",
              "state": {"query": query, "candidates": candidates},
              "questions": questions},
        timeout=10.0,
    )
    r.raise_for_status()
    res = r.json()["results"]

    ranked = []
    for i, cand in enumerate(candidates):
        s = res[f"rel_{i}"]
        ranked.append({
            "candidate": cand,
            # probability-weighted score — may fall BETWEEN levels
            "weighted_score": s.get("score", 0),
            "selected": s["selected"],
            "confidence": s["confidence"],
            "distribution": s.get("probabilities", {}),
        })

    # filter below floor, then rank by weighted score descending
    kept = [c for c in ranked
            if LEVELS.index(c["selected"]) > LEVELS.index(FLOOR)]
    kept.sort(key=lambda c: c["weighted_score"], reverse=True)
    return kept
```

</details>

### Thresholds & Notes

| Setting | Guidance |
|---------|----------|
| Floor level | Drop at/below `FLOOR`; floor is a *level*, not a float |
| Sort key | Use the **probability-weighted score**, not just `selected` |
| Confidence | Low confidence on a top hit → widen context, not auto-trust |
| Cost | Output free → keep full distributions for later re-tuning |

---

## 7. Map-Reduce

> **📌 Core Concept**
>
> **Definition:** **Map:** run the same typed question(s) over every record — each record gets its own decision. **Reduce:** aggregate the decisions (counts, buckets, ranked lists) in ordinary code. Latency **scales per decision**, not per dataset: records parallelize.
> **Analogy:** Like **polling an electorate**: one ballot per voter (map), then count the ballots (reduce). The counting step never re-interviews anyone.
> **Why it matters:** This is the structural shape behind classification-at-scale and bulk ranking. Because questions run in parallel within one call — and added questions barely change latency — you can also *fuse* map tasks: several questions per record in a single POST.

### Pattern Card — Map-Reduce

| | |
|---|---|
| **Questions** | Same question schema × N records (+ optional extra questions per record) |
| **Workload fit** | Map-reduce over datasets |
| **Latency** | Per-decision 70–500 ms; concurrency-bound overall |
| **Threshold posture** | Per-record bands; aggregates computed only over decisions you trust |

```
   MAP (parallel, per record)                REDUCE (code)

  rec_1 ──► Jev ──► label + p               ┌──────────────────┐
  rec_2 ──► Jev ──► label + p   ──────────►  │ counts by label   │
  rec_3 ──► Jev ──► label + p               │ top-k ranked      │
  ...                                       │ low-p → requeue   │
  rec_N ──► Jev ──► label + p               └──────────────────┘
```

| Setting | Guidance |
|---------|----------|
| Batching | Several questions per record in **one** POST (parallel pass) |
| Concurrency | Bound it (semaphore) — 70–500 ms each, but don't stampede |
| Reduce | Pure code over stored probabilities — no model needed |
| Aggregates | Decide which bands to include (e.g. exclude escalated records from counts) |

---

> **Pattern picker:** start with **Routing & Triage** (low risk, visible wins) → **Classification at Scale** (economics) → **Verified Cascade** (protects LLM output) → **Gating** (highest stakes, needs the strongest eval) → **Ranking** (composes with RAG).

---

*Back to [README](../README.md) — Module XIV overview*

*Previous: [04 — Calibration](../04-calibration/) · Next: [06 — Jev + LLM](../06-jev-and-llm/)*
