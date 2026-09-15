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

Your harness is running a nightly automation loop. One loop starts costing 50,000 tokens per run instead of 10,000. Another agent calls a tool 10 times before finishing. A new prompt lowers quality but you don't know why.

Without observability, you're **flying at night without lights**. You don't know the cost, you don't know which attempt succeeded, you don't know which tool is slow, you don't know which context got truncated.

> *"You can't optimize what you can't measure. You can't fix what you can't see."*

**Observability for AI systems** = tracing every LLM call, every tool call, every token, every latency, every cost — like APM for microservices, but for agent pipes.

### Why Observability Matters?

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Cost tracking** | Know exactly how many tokens/dollars each session costs |
| 2 | **Faster debugging** | Trace each tool call, see which chain failed |
| 3 | **Quality monitoring** | Track feedback, accuracy, do regression detection |
| 4 | **Partner of harness/11 evaluation** | Eval is meaningless without observing the runtime |

### Relationship to the Harness

```
┌─────────────────────────────────────────────────────────────┐
│  OBSERVABILITY MAP VS HARNESS COMPONENTS                    │
│                                                             │
│  harness/06-decide-tools-mcp → log tool calls + outcomes    │
│  harness/07-workflow         → trace flow through components│
│  harness/11-evaluation       → metrics collected            │
│  harness/10-automation       → monitor automation health    │
└─────────────────────────────────────────────────────────────┘
```

```
ToolDefinition already has metrics tracking (harness/06):
  avg_latency_ms  → track tool speed
  success_rate    → track success ratio
  total_calls     → count calls
```

## Overview of the Tools

| Tool | Publisher | Standout features | Best for |
|------|-----------|-------------------|----------|
| **LangSmith** | LangChain | Tracing + evals + monitoring, natural LangChain integration | LangChain stack, full lifecycle |
| **Helicone** | Helicone | LLM API proxy, cost tracking, analytics | Multi-framework, no code changes |
| **OpenLLMetry** | Traceloop | OpenTelemetry-based, vendor-neutral | Standardized, multi-provider |
| **Weights & Biases** | W&B | Experiment tracking, LLM evals | ML research, experiment logs |

### LangSmith — Trace Every Step

```python
from langsmith import Client
from langchain_openai import ChatOpenAI

# Auto-traces every LLM call when using LangChain
llm = ChatOpenAI(model="gpt-4", callbacks=[tracing_callback])

# See it in the LangSmith UI:
#   - Chain steps: retrieve → build → agent → tools
#   - Token usage per call
#   - Latency per node
#   - User feedback/reviews
```

### Helicone — A Proxy That Needs No Code Changes

```bash
# Configure the proxy: swap the API base URL
export OPENAI_API_BASE="https://oai.helicone.ai/v1"
export HELICONE_API_KEY="sk-helicone-..."

# All LLM calls are automatically logged + metered
# → Dashboard: cost, latency, request count, error rate
```

### OpenLLMetry — The OpenTelemetry Standard

```python
# OpenTelemetry-compatible — standard OTLP tracing
from traceloop.sdk import Traceloop

Traceloop.init(app_name="my_harness")

# Every framework (LangChain, LlamaIndex, OpenAI SDK...) traces automatically
# → Export to Jaeger, Grafana, Datadog, ...
```

## Learning Roadmap (Directory Structure)

```
observability/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Traces, spans, metrics, token accounting
├── 02-setup/            ← (TODO) Installing the Helicone proxy / LangSmith / OpenLLMetry
├── 03-patterns/         ← (TODO) Cost alerts, tool latency SLOs, session replay
├── 04-savings/          ← (TODO) Catching token leaks, optimizing prompts via metrics
└── 05-troubleshooting/  ← (TODO) Missing traces, context truncation, cost spikes
```

### Recommended Roadmap

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

| If you want to... | Read |
|-------------------|------|
| Evaluation metrics | [harness/11-evaluation](../../harness/11-evaluation/) |
| Tool metrics tracking | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Automation health | [harness/10-automation](../../harness/10-automation/) |
| Eval tooling | [tools/evaluation](../evaluation/) |
| Tokens wasted by bash output | [tools/rtk](../rtk/) |

## Real-World Case Studies

### 1. Catching a Token Leak in a Loop

```
With observability:
  Loop "ci-sweeper" runs 5 times/day
  → You see: attempt #3 always calls `read_file` 15 times on the same file
  → Debug: the prompt is missing instructions about caching results
  → Fix: add "reuse file contents if already in context" → 40% token reduction
```

### 2. Tool Latency SLOs

```python
# ToolDefinition metrics (from harness/06)
tool.update_metrics(latency_ms=1200, success=True)  # record on call

# Dashboard alerts:
#   If vector_search.avg_latency_ms > 2000 → alert
#   If execute_python.success_rate < 0.95 → alert
```

## Reference Materials

- **LangSmith**: https://smith.langchain.com
- **Helicone**: https://www.helicone.ai
- **OpenLLMetry**: https://github.com/traceloop/openllmetry
- **Weights & Biases**: https://wandb.ai

### Links to Other Branches

- [harness/11-evaluation](../../harness/11-evaluation/) — Measuring harness effectiveness
- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Tool metrics in the registry
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (monitoring list)
- [tools/evaluation](../evaluation/) — Quality evaluation tools
- [tools/rtk](../rtk/) — Token reduction (counterpart: measure + cut)

---

> **"Observability turns your harness from a black box into a dashboard."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — observability*
