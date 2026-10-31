# 📊 Observability — Monitoring & Logging for the Harness

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Observability Matters?](#why-observability-matters)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of the Tools](#overview-of-the-tools)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

This section shows what goes wrong without monitoring: problems happen, but you cannot see them.

Your harness runs a nightly job. One night a loop starts using 50,000 tokens per run instead of 10,000 — five times the cost, and nothing tells you. Another agent calls the same tool 10 times before it finishes. A new prompt makes answers worse, but you cannot tell why.

Without observability, you are **flying at night with no lights**. You cannot see the cost, you cannot tell which try worked, you cannot see which tool is slow, and you cannot see which context got cut off.

> *"You can't optimize what you can't measure. You can't fix what you can't see."*

**Observability for AI systems** means tracking every LLM call, every tool call, every token, every delay, and every cost — like health tracking for apps, but for agent workflows. "Token" = the unit of text models read and charge for (roughly 4 characters).

> **One-line summary:** Observability records every call, token, delay, and dollar, so problems become visible instead of mysterious.

### Why Observability Matters?

This section lists the four concrete payoffs of adding monitoring to a harness.

How to read the table: **#** is a row number; **Reason** is the short label; **Explanation** says what you gain. For example, row 1: you see exactly how many tokens and dollars each run used, instead of guessing from the invoice.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Cost tracking** | See exactly how many tokens and dollars each run uses |
| 2 | **Faster debugging** | Follow each tool call, and find which step broke |
| 3 | **Quality monitoring** | Watch feedback and accuracy, and catch drops early |
| 4 | **Partner of harness/11 evaluation** | Evals mean little if you cannot see what happens at runtime |

Plain gloss: "evals" = evaluation — scoring the harness's answers against known-good ones.

> **One-line summary:** Monitoring pays off four ways: cost visibility, faster debugging, early quality alerts, and meaningful evaluation.

### Relationship to the Harness

This blockquote sets the boundary: this directory lists monitoring tools; the data contract lives in harness/13.

> **This directory is a product/tool catalog, not the harness's contract.**
> Everything below is a *specific vendor or library you could adopt*. The canonical
> **event contract** — what the harness emits, the `TrajectoryEvent` schema, join keys,
> retention, redaction — is owned by
> [`harness/13-trajectory-observability`](../../harness/13-trajectory-observability/README.md).
> Pick a tool from here; conform to the contract there. If you find yourself defining an
> event shape here, it belongs in `13` instead.

Plain glosses: "event contract" = the agreed format of the records your harness emits. `TrajectoryEvent` = one record of a step the agent took. "Join keys" = shared IDs that let you connect records from different places. "Retention" = how long logs are kept. "Redaction" = removing secrets from logs before storing them.

```
┌─────────────────────────────────────────────────────────────┐
│  OBSERVABILITY MAP VS HARNESS COMPONENTS                    │
│                                                             │
│  harness/13-trajectory-obser → CANONICAL event contract     │
│                              (owns schema, this is not it)  │
│  harness/06-decide-tools-mcp → log tool calls + outcomes    │
│  harness/07-workflow         → trace flow through components│
│  harness/11-evaluation       → metrics collected            │
│  harness/10-automation       → monitor automation health    │
└─────────────────────────────────────────────────────────────┘
```

How to read the map: `→` means "supplies this". For example, harness/07-workflow supplies the trace of how a request flows through components; a "trace" = the recorded path of one request through the system.

```
ToolDefinition already has metrics tracking (harness/06):
  avg_latency_ms  → track tool speed
  success_rate    → track success ratio
  total_calls     → count calls
```

Plain glosses: `avg_latency_ms` = average response time in milliseconds. `success_rate` = share of calls that ended well, e.g. 0.98 = 98%.

> **One-line summary:** Tools here just record data; the format of that data is defined once in harness/13.

## Overview of the Tools

This table compares the five main monitoring tools.

> **One-line summary:** Five tools, three styles: native tracing (LangSmith), a logging proxy (Helicone), or open standards (Langfuse, OpenLLMetry, W&B). How to read it: **Tool** = the name; **Publisher** = who makes it; **Standout features** = what makes it different; **Best for** = the situation it fits. For example, "self-hostable" = you can run it on your own servers, so data never leaves your company.

| Tool | Publisher | Standout features | Best for |
|------|-----------|-------------------|----------|
| **LangSmith** | LangChain | Tracing + evals + monitoring, natural LangChain integration | LangChain stack, full lifecycle |
| **Langfuse** | Langfuse (open source) | Open-source tracing + agent graphs, OTel export, self-hostable | Self-hosting, privacy-sensitive, multi-framework |
| **Helicone** | Helicone | LLM API proxy, cost tracking, analytics | Multi-framework, no code changes |
| **OpenLLMetry** | Traceloop | OpenTelemetry-based, vendor-neutral | Standardized, multi-provider |
| **Weights & Biases** | W&B | Experiment tracking, LLM evals | ML research, experiment logs |

Plain glosses: "proxy" = a middleman server your API calls pass through, so it can log them without touching your code. "OTel" = OpenTelemetry, the open standard for traces (see below). "Vendor-neutral" = not tied to one provider.

### LangSmith — Trace Every Step

What this shows: LangSmith recording each step of a LangChain run so you can replay and inspect it.

> 📄 **Example code:** [`examples/01-langsmith-trace-every-step.py`](examples/01-langsmith-trace-every-step.py)

> **One-line summary:** LangSmith = the built-in choice if you already use LangChain: it sees every step natively.

### Helicone — A Proxy That Needs No Code Changes

What this shows: pointing your LLM API calls at Helicone's middleman server, which logs everything with zero code edits.

> 📄 **Example code:** [`examples/02-helicone-a-proxy-that-needs-no-code-changes.sh`](examples/02-helicone-a-proxy-that-needs-no-code-changes.sh)

> **One-line summary:** Helicone = fastest way to get cost and usage logging: change one URL, change no code.

### OpenLLMetry — The OpenTelemetry Standard

What this shows: OpenLLMetry emitting traces in the OpenTelemetry format, so any OTel-compatible backend can read them.

> 📄 **Example code:** [`examples/03-openllmetry-the-opentelemetry-standard.py`](examples/03-openllmetry-the-opentelemetry-standard.py)

> **One-line summary:** OpenLLMetry = the vendor-neutral option: one standard format, many possible backends.

## OpenTelemetry GenAI Semantic Conventions (2025)

This section explains a 2025 standard that makes LLM traces portable between monitoring tools — why it matters: without it, switching tools means rewriting your logging.

The OTel GenAI spec standardizes traces for LLM calls:
- span.name: "genai.*"
- genai.* attributes (genai.prompt_tokens, genai.completion_tokens, genai.model)
- Langfuse supports OTel export from LangChain/LangGraph

Plain glosses: a "span" = one timed step in a trace; "attributes" = named values attached to it, e.g. `genai.prompt_tokens` = number of tokens in the prompt.

Ref: https://opentelemetry.io/docs/specs/semconv/gen-ai/

Why it matters: before 2025, every vendor invented its own span names and attributes, so traces were not portable across backends. With the GenAI semantic conventions, the same trace reads correctly in Jaeger, Grafana, Datadog, or Langfuse — switching observability backends no longer means rewriting instrumentation. OpenLLMetry and Langfuse both emit according to this standard.

> **One-line summary:** The OTel GenAI spec gives all tools one shared trace format, so your logging survives a tool switch.

## Learning Roadmap (Directory Structure)

> **One-line summary:** This section maps the folder layout and a step-by-step learning path.

This tree shows the folder layout; `(TODO)` means not written yet.

```
observability/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Traces, spans, metrics, token accounting
├── 02-setup/            ← (TODO) Installing the Helicone proxy / LangSmith / OpenLLMetry
├── 03-patterns/         ← (TODO) Cost alerts, tool latency SLOs, session replay
├── 04-savings/          ← (TODO) Catching token leaks, optimizing prompts via metrics
└── 05-troubleshooting/  ← (TODO) Missing traces, context truncation, cost spikes
```

Plain glosses: "SLO" = service level objective, a target like "95% of tool calls under 2 seconds". "Session replay" = re-watching a whole agent session step by step. "Context truncation" = the prompt being cut short because it hit a size limit.

### Recommended Roadmap

A suggested learning order; read `↓` as "then do this next".

```
Step 1: Understand the measurement results the harness needs (harness/11)
   ↓
Step 2: Install the Helicone proxy — fastest, no code changes (02-setup)
   ↓
Step 3: Add tracing metadata: session_id, user_id, tool_name (03-patterns)
   ↓
Step 4: Set up cost alerts + latency SLOs per tool (03-patterns)
   ↓
Step 5: If using LangChain → move to LangSmith for deep tracing
```

This table maps goals to docs. How to read it: left column = what you want to learn; right column = where to read it. For example, the last row: tokens wasted by bash output is the specialty of tools/rtk — the cutting tool, while this page is the measuring tool.

| If you want to... | Read |
|-------------------|------|
| Evaluation metrics | [harness/11-evaluation](../../harness/11-evaluation/) |
| Tool metrics tracking | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Automation health | [harness/10-automation](../../harness/10-automation/) |
| Eval tooling | [tools/evaluation](../evaluation/) |
| Tokens wasted by bash output | [tools/rtk](../rtk/) |

> **One-line summary:** Start with the no-code proxy, add labels and alerts, then go deep with LangSmith if you use LangChain.

## Real-World Case Studies

Two worked scenarios: catching waste, and setting speed targets.

> **One-line summary:** Two scenarios — a 40% token saving found in traces, and a speed target you can alert on.

### 1. Catching a Token Leak in a Loop

This block diagram shows a real debugging story, top to bottom: the symptom, the clue visible in traces, the cause, and the fix. A "token leak" = spending tokens on the same content again and again.

```
With observability:
  Loop "ci-sweeper" runs 5 times/day
  → You see: attempt #3 always calls `read_file` 15 times on the same file
  → Debug: the prompt is missing instructions about caching results
  → Fix: add "reuse file contents if already in context" → 40% token reduction
```

> **One-line summary:** Traces reveal repeated wasted calls; one prompt fix cut this loop's tokens by 40%.

### 2. Tool Latency SLOs

What this shows: setting and checking a speed target per tool — alerting when a tool gets slower than its target.

> 📄 **Example code:** [`examples/04-2-tool-latency-slos.py`](examples/04-2-tool-latency-slos.py)

> **One-line summary:** A latency SLO turns "the tool feels slow" into a number you can alert on.

## Reference Materials

Official pages of the tools and the OTel spec, for deeper reading.

> **One-line summary:** Five tool links plus the OpenTelemetry GenAI spec.

- **LangSmith**: https://smith.langchain.com
- **Langfuse**: https://langfuse.com
- **Helicone**: https://www.helicone.ai
- **OpenLLMetry**: https://github.com/traceloop/openllmetry
- **Weights & Biases**: https://wandb.ai
- **OTel GenAI Semantic Conventions**: https://opentelemetry.io/docs/specs/semconv/gen-ai/

### Links to Other Branches

Related pages in this repo — follow them for the neighboring topic.

> **One-line summary:** Neighboring topics: evaluation, tool metrics, automation health, and the token-cutting counterpart (rtk).

- [harness/11-evaluation](../../harness/11-evaluation/) — Measuring harness effectiveness
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool metrics in the registry
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (monitoring list)
- [tools/evaluation](../evaluation/) — Quality evaluation tools
- [tools/rtk](../rtk/) — Token reduction (counterpart: measure + cut)

---

> **"Observability turns your harness from a black box into a dashboard."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — observability*
