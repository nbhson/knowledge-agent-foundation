# ❓ FAQ — Observability (Real Stories, Plain Language)

This file answers real questions about **observability** — recording what your agent actually did (traces, metrics), so you can find problems instead of guessing. If a question is unclear, read the section in `../README.md` (named in brackets).

---

## Q1. A nightly loop jumped from 10,000 to 50,000 tokens per run — where do I look first? [→ Real-World Case Studies]

This question is about diagnosing a sudden cost jump. The first tool is a trace (trace = the recorded step-by-step log of one run).

**What you see**

The nightly automation loop still works, still passes, and now costs five times more. Nothing warns you. You only notice on the bill.

**Why**

Without a trace you cannot tell "more tokens" from "more steps". One real case: a loop called `ci-sweeper` five times a day, and attempt #3 always read the *same file* fifteen times. The prompt never said "reuse what is already in context", so the model paid for the same bytes repeatedly.

**What to do**

1. Turn on tracing for one loop first, not the whole system. Helicone is the fastest start — you change the API base URL (URL = the web address your code calls instead of the provider's), no code edits.
2. Read the trace per attempt and find the repeated tool call.
3. Fix the prompt, then re-measure. That one fix cut the loop's tokens by 40%.

> 📄 **Example code:** [`examples/01-q1-a-nightly-loop-jumped-from-10-000.sh`](examples/01-q1-a-nightly-loop-jumped-from-10-000.sh)

**Verify**

The dashboard shows cost, latency (response time), request count and error rate per loop. After the prompt fix, tokens per run drop and the repeated `read_file` calls disappear from the trace.

> **One-line summary:** Turn on a trace for the expensive loop, find the repeated tool call in it, fix the prompt, and re-measure.

---

## Q2. Which tool do I pick — LangSmith, Langfuse, Helicone, OpenLLMetry or W&B? [→ Overview of the Tools]

This question is about picking one observability tool. They measure similar things; the difference is *how they plug into your code*.

**What you see**

You want traces "someday", but each product claims full coverage, so you hesitate and install nothing.

**Why**

They differ in *how they attach*, not in what they measure.

How to read it: each row is one tool; "How it attaches" says what you must change in your code or setup to use it; "Best fit" says who it suits. For instance, Helicone attaches as a proxy (proxy = a middleman server between your code and the model API), so it needs no code change at all.

| Tool | How it attaches | Best fit |
|---|---|---|
| LangSmith | callback inside LangChain | you already run LangChain |
| Langfuse | SDK or OTel export | self-hosting, privacy-sensitive, gen-ai standard |
| Helicone | proxy in front of the API | many frameworks, zero code change |
| OpenLLMetry (Traceloop) | OpenTelemetry standard | vendor-neutral, export to Jaeger/Grafana |
| Weights & Biases | experiment tracking | ML research, prompt experiments |

Glossary for the table: **callback** = a hook LangChain calls at each step; **SDK** = a code library from the vendor; **OTel** = OpenTelemetry, the open standard for trace data; **self-hosting** = running the tool on your own servers; **experiment tracking** = logging model runs like lab experiments.

**On OTel GenAI Semantic Conventions (2025)**

Since 2025, OpenTelemetry has a dedicated spec for LLM calls: spans named `genai.*` (span = one recorded step in a trace) with attributes like `genai.prompt_tokens`, `genai.completion_tokens`, and `genai.model`. Langfuse and OpenLLMetry both emit according to this standard, so the same trace reads correctly in any OTel-compatible backend — Jaeger, Grafana, Datadog. Picking a vendor no longer locks you into a proprietary trace format.

**What to do**

1. Want visibility today with no refactor → Helicone, two environment variables.
2. Need self-hosting or the OTel standard → Langfuse.
3. Running LangChain and want step-by-step traces plus feedback → LangSmith.
4. Your company already runs OpenTelemetry → OpenLLMetry, one `Traceloop.init()` call.
5. Do not send every vendor the same data; start with one.

> 📄 **Example code:** [`examples/02-q2-which-tool-do-i-pick-langsmith-langfuse.py`](examples/02-q2-which-tool-do-i-pick-langsmith-langfuse.py)

**Verify**

Trigger one agent run and confirm a trace exists with a chain broken into steps (retrieve → build → agent → tools), each showing token usage and latency. If you use Langfuse, check the trace carries the GenAI semantic conventions.

> **One-line summary:** Pick the tool by how it attaches — proxy for zero code change, callback for LangChain, OTel standard for vendor neutrality.

---

## Q3. A tool gets slow — how do I know *which* one before users tell me? [→ Relationship to the Harness]

This question is about per-tool metrics (metrics = recorded numbers like speed and success rate), so slowness shows up in a dashboard before users complain.

**What you see**

Users say "it feels slow today". You have a log with 40 tool calls and no ranking. Meanwhile `vector_search` averages 1,200 ms and nobody noticed for a week.

**Why**

The tool registry in `harness/06` already tracks three numbers per tool — `avg_latency_ms` (average response time in milliseconds), `success_rate` (share of calls that succeed), `total_calls` (how many times it was used) — but only if something records them on every call. Unused counters stay at zero, which looks like good news.

**What to do**

1. Record metrics inside the executor (executor = the code that actually runs the tool), not in the dashboard layer: one `update_metrics` per call.
2. Set two alerts: latency above a threshold, and success rate below a threshold.
3. Compare tools, not averages — one slow tool hides inside a fast total.

> 📄 **Example code:** [`examples/03-q3-a-tool-gets-slow-how-do-i.py`](examples/03-q3-a-tool-gets-slow-how-do-i.py)

**Verify**

`total_calls` grows after a run, `avg_latency_ms` is non-zero for the tool you just used, and a deliberately failing call drops `success_rate` below 1.0.

> **One-line summary:** Record latency, success rate and call count inside the executor on every call, and alert on thresholds — then the slow tool names itself.

---

## Q4. I defined my own event fields — is that wrong? [→ Relationship to the Harness]

This question is about who owns the event format. Inventing your own fields breaks joining (joining = matching records from different sources by a shared key) between logs.

**What you see**

You invent `run_id`, `step_kind`, `cost_usd` and start shipping them from three different places. Then two traces of the same run cannot be joined.

**Why**

This folder is a catalog of products, **not the harness's contract**. The canonical event shape (canonical = the one official copy everyone must follow; event shape = the exact fields each log entry carries) — the `TrajectoryEvent` schema, join keys, retention and redaction — is owned by `harness/13-trajectory-observability`. If you are defining an event shape here, it belongs in `13`.

**What to do**

1. Adopt the schema from `harness/13` first, then pick a tool from this catalog.
2. Carry the join keys on every event: `session_id`, `user_id`, `tool_name`.
3. Add retention (how long logs are kept) and redaction (removing secrets from logs) rules before the first production run, not after.

**Verify**

Two log lines from the same session join on `session_id` alone, and every emitted field already exists in the `TrajectoryEvent` schema from `harness/13`.

> **One-line summary:** Don't invent event fields — adopt the TrajectoryEvent schema from harness/13 so every trace joins on the same keys.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*
