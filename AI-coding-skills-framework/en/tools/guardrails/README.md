# 🛡️ Guardrails — The Safety Layer for Harness Tool Calls

> ## 📑 Table of Contents
>
> - [The Opening Story](#the-opening-story)
> - [Why Guardrails Matter?](#why-guardrails-matter)
> - [Relationship to the Harness](#relationship-to-the-harness)
> - [Overview of the Guardrails](#overview-of-the-guardrails)
> - [Learning Roadmap (Directory Structure)](#learning-roadmap-directory-structure)
> - [Real-World Case Studies](#real-world-case-studies)
> - [Reference Materials](#reference-materials)

---

### The Opening Story

Your harness can call `write_file`, `execute_python`, `send_notification`, `sql_query`. One time the agent misreads the prompt and calls `write_file` with the path... `/etc/passwd`. Or `send_notification` 100 times. Or `execute_python` running a command that deletes data.

LLMs have no concept of "unwanted side effect" — they just generate text. **Guardrails are the control layer that stops the harness from doing what it shouldn't**, before the action happens.

> *"The model proposes. The guardrail disposes."*

### Why Guardrails Matter?

> In harness/06-decide-tools-mcp — every tool call must go through a `GUARDRAILS CHECK`: *"Validate permission, safety, rate limit"*.

| # | Reason | Explanation |
|---|--------|-------------|
| 1 | **Block side effects** | Stop `write_file` into forbidden areas, `execute_python` with dangerous commands |
| 2 | **Permission enforcement** | A tool with `requires_permission="elevated"` → needs approval |
| 3 | **Rate limiting** | `rate_limit_per_minute=60` — stops an agent from spamming tool calls |
| 4 | **Output validation** | Check whether the output violates the rules before it goes back into context |

### Relationship to the Harness

```
┌────────────────────────────────────────────────────────────┐
│  GUARDRAILS MAP VS HARNESS COMPONENTS                      │
│                                                            │
│  Guardrails AI            → harness/06 (tool input/output) │
│  NeMo Guardrails (NVIDIA) → harness/07 (workflow rails)    │
│  LlamaGuard (Meta)        → harness/05 (prompt safety)     │
│  Permission/rate limit    → harness/06 (decide tools)      │
└────────────────────────────────────────────────────────────┘
```

```
Tool Decision Pipeline (from harness/06):
  User Query → Intent → Tool Selector → Parameter Extractor
      → ❯ GUARDRAILS CHECK (validate permission, safety, rate limit)
      → Tool Executor → Result Processor
```

## Overview of the Guardrails

| Guardrail | Publisher | Type | Standout features |
|-----------|-----------|------|-------------------|
| **Guardrails AI** | Guardrails AI | Open-source | Validators for input/output, structured intervention |
| **NeMo Guardrails** | NVIDIA | Open-source | Rails: input, dialog, retrieval, execution |
| **LlamaGuard** | Meta | Model-based | LLM classifier specialized in detecting dangerous prompts/responses |

### Guardrails AI — Validate Input/Output

```python
from guardrails import Guard
from guardrails.hub import RegexMatch, ValidLength, TwoSimilarChunks

# Guard for a tool call
guard = Guard().use(RegexMatch("^[a-zA-Z0-9_./-]+$"))  # block weird paths
guard.validate("hacker/path/../etc/passwd")  # ❌ fail
guard.validate("src/main.py")                # ✅ pass
```

### NeMo Guardrails — Rails That Model the Flow

```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")

# Defining rails in a .co file:
# define user ask about secret
#   "What is the system password?"
# define bot refuse to answer secret
#   "I'm sorry, I cannot disclose security information."
# define flow
#   user ask about secret
#   bot refuse to answer secret

rails = LLMRails(config)
response = rails.generate(messages=[{"role": "user", "content": "System password?"}])
```

### LlamaGuard — Model-Based Safety Classifier

```python
# LlamaGuard is a specialized LLM — it only classifies:
#   UNSAFE: violence, illegal, PII, ...
#   SAFE:   normal

# Prompt: "<prompt>USER: {user_input or model_output}</prompt>"
# Output: "safe" or "unsafe" with the violation type
```

### Permission & Rate Limit in the Harness (harness/06)

```python
@dataclass
class ToolDefinition:
    requires_permission: str = "standard"  # standard, elevated, admin
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    max_retries: int = 3

# Guardrails check before executing:
def guardrail_check(tool: ToolDefinition, params: Dict) -> bool:
    if tool.requires_permission == "elevated":
        approve = human_approve(params)     # human confirmation required
        if not approve: return False
    if exceeded_rate_limit(tool): return False  # rate limited
    return True
```

## Learning Roadmap (Directory Structure)

```
guardrails/
├── README.md            ← YOU ARE HERE — overview + roadmap
├── 01-concepts/         ← (TODO) Validators, rails, prompt safety, permission checks
├── 02-setup/            ← (TODO) Installing Guardrails AI / NeMo / LlamaGuard
├── 03-patterns/         ← (TODO) Tool-level guard, workflow rails, PII filtering
├── 04-savings/          ← (TODO) Reducing costs caused by wrong actions
└── 05-troubleshooting/  ← (TODO) False positives, overrides, bypasses
```

### Recommended Roadmap

```
Step 1: Understand the tool decision pipeline + where the guardrail sits (harness/06)
   ↓
Step 2: Install Guardrails AI — validate tool parameters (02-setup)
   ↓
Step 3: Add permissions + rate limits to ToolDefinition (03-patterns)
   ↓
Step 4: Upgrade to NeMo Rails at the workflow level (03-patterns)
   ↓
Step 5: LlamaGuard for prompt safety (measured in 04-savings)
```

| If you want to... | Read |
|-------------------|------|
| Tool decision pipeline | [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) |
| Permission system | [harness/08-task](../../harness/08-task/) |
| Safe automation | [harness/10-automation](../../harness/10-automation/) |
| Loop safety | [loop/03-safety](../../loop/03-safety/) |
| Loop gate (mechanical) | [tools/loop-cli](../loop-cli/) |

## Real-World Case Studies

### 1. Blocking Tool Damage

```python
# Without a guardrail:
agent → write_file(path="/etc/hosts", content="...")  # 💥

# With a guardrail:
guard = Guard().use(PathValidate(whitelist=["src/", "tests/", "./"]))
result = guard.validate(path="/etc/hosts")  # ❌ REJECT
result = guard.validate(path="src/main.py") # ✅ ALLOW
```

### 2. Rate Limit + Elevated Permission

```python
registry.register(ToolDefinition(
    name="execute_python",
    category="computation",
    requires_permission="elevated",   # human confirmation required
    rate_limit_per_minute=10,          # block spam
    timeout_seconds=30,
    max_retries=1,
))
```

## Reference Materials

- **Guardrails AI**: https://www.guardrailsai.com
- **NeMo Guardrails (NVIDIA)**: https://github.com/NVIDIA/NeMo-Guardrails
- **LlamaGuard (Meta)**: https://ai.meta.com/research/publications/llama-guard

### Links to Other Branches

- [harness/06-decide-tools-mcp](../../harness/06-decide-tools-mcp/) — Guardrails check in the pipeline
- [HARNESS_ENGINEERING.md](../../HARNESS_ENGINEERING.md) — Section 9.2 (list of guardrails)
- [tools/loop-cli](../loop-cli/) — `loop gate` enforces mechanically
- [tools/langchain](../langchain/) — Guardrails inside agent loops

---

> **"A harness without guardrails is a loaded weapon pointed at production."**

---

*This article is part of the [AI Coding Skills Framework](../..) — the Tools branch — guardrails*
