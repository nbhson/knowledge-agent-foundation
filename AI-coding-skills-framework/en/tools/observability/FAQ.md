# ❓ FAQ — Observability (Real Stories, Plain Language)

If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. A nightly loop jumped from 10,000 to 50,000 tokens per run — where do I look first? [→ Real-World Case Studies]

**What you see**

The nightly automation loop still works, still passes, and now costs five times more. Nothing warns you. You only notice on the bill.

**Why**

Without a trace you cannot tell "more tokens" from "more steps". One real case: a loop called `ci-sweeper` five times a day, and attempt #3 always read the *same file* fifteen times. The prompt never said "reuse what is already in context", so the model paid for the same bytes repeatedly.

**What to do**

1. Turn on tracing for one loop first, not the whole system. Helicone is the fastest start — you change the API base URL, no code edits.
2. Read the trace per attempt and find the repeated tool call.
3. Fix the prompt, then re-measure. That one fix cut the loop's tokens by 40%.

```bash
export OPENAI_API_BASE="https://oai.helicone.ai/v1"
export HELICONE_API_KEY="sk-helicone-..."
# every LLM call is now logged and metered
```

**Verify**

The dashboard shows cost, latency, request count and error rate per loop. After the prompt fix, tokens per run drop and the repeated `read_file` calls disappear from the trace.

---

## Q2. Which tool do I pick — LangSmith, Helicone, OpenLLMetry or W&B? [→ Overview of the Tools]

**What you see**

You want traces "someday", but each product claims full coverage, so you hesitate and install nothing.

**Why**

They differ in *how they attach*, not in what they measure.

| Tool | How it attaches | Best fit |
|---|---|---|
| LangSmith | callback inside LangChain | you already run LangChain |
| Helicone | proxy in front of the API | many frameworks, zero code change |
| OpenLLMetry (Traceloop) | OpenTelemetry standard | vendor-neutral, export to Jaeger/Grafana |
| Weights & Biases | experiment tracking | ML research, prompt experiments |

**What to do**

1. Want visibility today with no refactor → Helicone, two environment variables.
2. Running LangChain and want step-by-step traces plus feedback → LangSmith.
3. Your company already runs OpenTelemetry → OpenLLMetry, one `Traceloop.init()` call.
4. Do not send every vendor the same data; start with one.

```python
from traceloop.sdk import Traceloop
Traceloop.init(app_name="my_harness")
# LangChain, LlamaIndex, OpenAI SDK... all trace automatically
```

**Verify**

Trigger one agent run and confirm a trace exists with a chain broken into steps (retrieve → build → agent → tools), each showing token usage and latency.

---

## Q3. A tool gets slow — how do I know *which* one before users tell me? [→ Relationship to the Harness]

**What you see**

Users say "it feels slow today". You have a log with 40 tool calls and no ranking. Meanwhile `vector_search` averages 1,200 ms and nobody noticed for a week.

**Why**

The tool registry in `harness/06` already tracks three numbers per tool — `avg_latency_ms`, `success_rate`, `total_calls` — but only if something records them on every call. Unused counters stay at zero, which looks like good news.

**What to do**

1. Record metrics inside the executor, not in the dashboard layer: one `update_metrics` per call.
2. Set two alerts: latency above a threshold, and success rate below a threshold.
3. Compare tools, not averages — one slow tool hides inside a fast total.

```python
tool.update_metrics(latency_ms=1200, success=True)
# alert if vector_search.avg_latency_ms > 2000
# alert if execute_python.success_rate < 0.95
```

**Verify**

`total_calls` grows after a run, `avg_latency_ms` is non-zero for the tool you just used, and a deliberately failing call drops `success_rate` below 1.0.

---

## Q4. I defined my own event fields — is that wrong? [→ Relationship to the Harness]

**What you see**

You invent `run_id`, `step_kind`, `cost_usd` and start shipping them from three different places. Then two traces of the same run cannot be joined.

**Why**

This folder is a catalog of products, **not the harness's contract**. The canonical event shape — the `TrajectoryEvent` schema, join keys, retention and redaction — is owned by `harness/13-trajectory-observability`. If you are defining an event shape here, it belongs in `13`.

**What to do**

1. Adopt the schema from `harness/13` first, then pick a tool from this catalog.
2. Carry the join keys on every event: `session_id`, `user_id`, `tool_name`.
3. Add retention and redaction rules before the first production run, not after.

**Verify**

Two log lines from the same session join on `session_id` alone, and every emitted field already exists in the `TrajectoryEvent` schema from `harness/13`.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*