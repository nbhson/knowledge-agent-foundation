# Harness Engineering - Designing Systems Around AI Agents

> **"Every time an agent makes a mistake, you don't pray it does better next time – you build a systematic solution so it never makes that mistake again"**  
> — Mitchell Hashimoto (Founder of HashiCorp, Creator of Terraform)

---

## Table of Contents

- [Harness Engineering - Designing Systems Around AI Agents](#harness-engineering---designing-systems-around-ai-agents)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
    - [Background](#background)
    - [Purpose of This Document](#purpose-of-this-document)
  - [2. What Is Harness Engineering?](#2-what-is-harness-engineering)
    - [Definition](#definition)
    - [Core Philosophy](#core-philosophy)
    - [Illustrative Example](#illustrative-example)
    - [Comparison With Other Concepts](#comparison-with-other-concepts)
  - [3. Three Evolution Phases of AI Engineering](#3-three-evolution-phases-of-ai-engineering)
    - [3.1. Prompt Engineering (2022-2024)](#31-prompt-engineering-2022-2024)
    - [3.2. Context Engineering (2025)](#32-context-engineering-2025)
    - [3.3. Harness Engineering (2026+)](#33-harness-engineering-2026)
    - [Overview Comparison](#overview-comparison)
    - [Key Insight](#key-insight)
  - [4. Why Is Harness Engineering Important?](#4-why-is-harness-engineering-important)
    - [4.1. Outstanding Performance Optimization](#41-outstanding-performance-optimization)
    - [4.2. The Model Is Just a Tool; the System Decides the Outcome](#42-the-model-is-just-a-tool-the-system-decides-the-outcome)
    - [4.3. Control and Reliability](#43-control-and-reliability)
    - [4.4. Scalability and Maintainability](#44-scalability-and-maintainability)
    - [4.5. Significant Cost Savings](#45-significant-cost-savings)
    - [4.6. Competitive Advantage](#46-competitive-advantage)
    - [In Summary](#in-summary)
  - [5. The Core Components of a Harness](#5-the-core-components-of-a-harness)
    - [5.1. Tools - "Hands & Feet"](#51-tools---hands-&-feet)
    - [5.2. Memory - "The Brain"](#52-memory---the-brain)
    - [5.3. Context Management - "The Circulatory System"](#53-context-management---the-circulatory-system)
      - [Where Does the Intervention Happen?](#where-does-the-intervention-happen)
      - [How Does That Code Run Automatically?](#how-does-that-code-run-automatically)
    - [5.4. Guardrails - "The Immune System"](#54-guardrails---the-immune-system)
    - [5.5. Feedback Loops - "Senses"](#55-feedback-loops---senses)
    - [5.6. Permissions - "The Skeleton"](#56-permissions---the-skeleton)
    - [5.7. Orchestration - "The Nervous System"](#57-orchestration---the-nervous-system)
    - [Integrate Everything](#integrate-everything)
    - [Integrate Components With Modules in the Repo](#integrate-components-with-modules-in-the-repo)
      - [Detailed Mapping Table](#detailed-mapping-table)
  - [🔭 Overview: Harness Engineering — AI Coding Skills Framework](#-overview-harness-engineering--ai-coding-skills-framework)
    - [Overall Architecture: 7 Components → 15 Modules](#overall-architecture-7-components--15-modules)
    - [6.2. Anthropic Multi-Agent Architecture](#62-anthropic-multi-agent-architecture)
    - [6.3. Claude Code Leak - A Superlative Harness System](#63-claude-code-leak---a-superlative-harness-system)
      - [A. 5-Level Context Management](#a-5-level-context-management)
      - [B. 3-Tier Memory with Auto-Optimization](#b-3-tier-memory-with-auto-optimization)
      - [C. Strict Tool Permissions](#c-strict-tool-permissions)
      - [D. Tone Detection with Regex (!)](#d-tone-detection-with-regex)
    - [6.4. Cursor IDE - Harness Optimized for Coding](#64-cursor-ide---harness-optimized-for-coding)
    - [6.5. DeepSeek Harness — Micro-Kernel & Trajectory Traceability Framework](#65-deepseek-harness--micro-kernel-&-trajectory-traceability-framework)
      - [A. Micro-Kernel & Ecosystem Plugin Architecture](#a-micro-kernel-&-ecosystem-plugin-architecture)
      - [B. 4 Specialized Runtime Modes](#b-4-specialized-runtime-modes)
      - [C. Trajectory Traceability Engine (Session Event Stream & Branching)](#c-trajectory-traceability-engine-session-event-stream-&-branching)
      - [D. Code Mode SDK & Sandboxed Execution](#d-code-mode-sdk-&-sandboxed-execution)
      - [E. Minimal Benchmark Harness for AI Capability Evaluation](#e-minimal-benchmark-harness-for-ai-capability-evaluation)
    - [Common Lessons From the Case Studies](#common-lessons-from-the-case-studies)
  - [7. Harness Design Principles](#7-harness-design-principles)
    - [7.1. SOLID Principles for Harness](#71-solid-principles-for-harness)
    - [7.2. The 10 Commandments of Harness Engineering](#72-the-10-commandments-of-harness-engineering)
    - [7.3. The Harness Design Pattern](#73-the-harness-design-pattern)
  - [8. Best Practices](#8-best-practices)
    - [8.1. Tool Design](#81-tool-design)
    - [8.2. Memory Management](#82-memory-management)
    - [8.3. Context Building](#83-context-building)
    - [8.4. Guardrails](#84-guardrails)
    - [8.5. Testing the Harness](#85-testing-the-harness)
  - [9. Tools & Frameworks](#9-tools-&-frameworks)
    - [9.1. Popular Frameworks](#91-popular-frameworks)
    - [9.2. Supporting Tools](#92-supporting-tools)
    - [9.3. Starter Template](#93-starter-template)
  - [10. The Future of Harness Engineering](#10-the-future-of-harness-engineering)
    - [10.1. Trends 2026-2028](#101-trends-2026-2028)
    - [10.2. Challenges Ahead](#102-challenges-ahead)
    - [10.3. Advice for the Future](#103-advice-for-the-future)
  - [11. Reference Materials](#11-reference-materials)
    - [Papers & Research](#papers-&-research)
    - [Frameworks & Tools](#frameworks-&-tools)
    - [Communities](#communities)
    - [Blogs & Resources](#blogs-&-resources)
    - [Courses & Tutorials](#courses-&-tutorials)

---

## 1. Introduction

This section sets up the core question: why does the same AI model succeed in one app and fail in another? The answer is rarely the model — it is the setup around it.

In the AI era, we have seen huge growth in large language models (LLMs = AI models trained on massive amounts of text; they read a prompt and generate text). From GPT-3, GPT-4, Claude, to Gemini, these models keep getting smarter. Yet a key question remains: **Why, with the same AI model, do some applications perform exceptionally well while others fail?**

The answer lies in **Harness Engineering** — a discipline that does not improve the AI model itself. It builds the **ecosystem around that model**: tools, permissions, memory, feedback loops, guardrails, and context management. A harness is like a horse's harness: the horse (the model) provides the power, but the harness decides where that power goes.

### Background

When Mitchell Hashimoto (founder of HashiCorp, creator of Terraform) said *"Prompt Engineering is dead"* and introduced **Harness Engineering**, he opened a fresh chapter in how we build AI apps. Instead of fussing over the perfect prompt, we build a full setup that helps the AI do its job well. For example: rather than writing "please check your code for errors" in the prompt, you add an automatic error check that blocks bad code.

> **One-line summary:** A famous engineer argued that perfect prompts are not the answer — the surrounding system is.

### Purpose of This Document

This document gives a full picture of Harness Engineering:
- Definition and core philosophy
- Comparison with earlier techniques (Prompt Engineering, Context Engineering)
- Components and design principles
- Case studies from leading organizations (Princeton NLP, Anthropic)
- Best practices and practical implementation guidance

> **One-line summary:** You will learn what a harness is, how it differs from prompt work, and how to build one.

---

## 2. What Is Harness Engineering?

This section defines the term "harness" and explains why it, not the model, decides output quality.

### Definition

**Harness Engineering** is the practice of building the entire **"environment around"** an AI model — tools, permissions, memory, feedback loops, guardrails, and context management — instead of improving the model itself. Harness = the strap system put on a horse: the horse (the model) provides the muscle, the harness steers where that muscle goes.

Put simply:
- The **AI model** is what **thinks**
- The **harness** is what the AI **thinks about** (the data, tools, and limits it sees)
- And the **harness** is what determines the **final output quality**

> **One-line summary:** The model thinks; the harness controls what it sees and can do — so the harness controls quality.

### Core Philosophy

> *"Every time an agent makes a mistake, you don't pray it does better next time – you build a systematic solution so it never makes that mistake again"*

This philosophy emphasizes:

1. **Systematic Solutions over Prayers**: Instead of hoping the AI "learns" from mistakes, you build a mechanism that blocks the mistake from repeating. Example: if the AI keeps saving broken code, add a syntax check that refuses to save.
2. **Infrastructure over Instructions**: Instead of long prompts telling the AI what to do, you build infrastructure (code, checks, limits) that constrains what the AI can do.
3. **Design over Training**: Instead of fine-tuning (retraining the model on your own data — slow and costly), you design the environment the model operates in.

> **One-line summary:** When the agent errs, fix the system so the error cannot happen again — do not just hope.

### Illustrative Example

Imagine you have an AI coding assistant. This example shows the contrast between asking nicely and enforcing automatically.

**❌ Old approach (Prompt Engineering):**
```
"Write Python code. Make sure your code has no syntax errors.
Check carefully before returning. If there are errors, fix them..."
```

**✅ New approach (Harness Engineering):**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/01-illustrative-example.js`](examples/01-illustrative-example.js)

</details>

In the example above, instead of "asking" the AI to be careful, you build a system that does **not allow** the AI to return code with errors. The old way says "please check yourself"; the new way runs a checker the AI cannot bypass.

> **One-line summary:** Old: beg the model to behave. New: make the system enforce the behavior.

### Comparison With Other Concepts

This table places Harness Engineering next to the two older techniques, one aspect per row.

| Aspect | Prompt Engineering | Context Engineering | Harness Engineering |
|-----------|-------------------|---------------------|---------------------|
| **Focus** | How you ask | Input data | The whole system |
| **Goal** | Better prompts | Better context | Better environment |
| **Example** | Writing an email | Attaching a file | Designing the office + workflows |
| **Control** | Low | Medium | High |
| **Durability** | Low | Medium | High |

How to read it: "Focus" is what the technique works on; "Control" is how much you can force the AI to behave; "Durability" is how long the fix lasts as models change. For instance, "Attaching a file" means giving the model the right documents in the prompt; "Designing the office + workflows" means building the tools, rules, and checks around it.

> **One-line summary:** Prompts tune the request, context tunes the input, the harness tunes everything — so it has the highest control and durability.

---

## 3. Three Evolution Phases of AI Engineering

This section traces how AI engineering matured in three phases. Knowing the phases shows what problem Harness Engineering solves that the earlier ones did not.

To better understand Harness Engineering, we need to look back at the evolution of AI engineering through three main phases:

### 3.1. Prompt Engineering (2022-2024)

**Focus**: *"How do I ask the AI the right way?"*

**Characteristics:**
- Focus on writing good prompts
- Use techniques: few-shot learning (showing the model a few worked examples), chain-of-thought (asking it to reason step by step), role-playing (telling it to "act as a senior developer")
- Heavy dependence on the "art" of prompt writing

**Example:**
```
User: "Act as a senior Python developer. Write a function to..."
User: "Think step by step..."
User: "Here are some examples: ..."
```

**Limitations:**
- Hard to scale and maintain
- Unstable results
- Hard to debug when something goes wrong
- Over-reliance on phrasing

**Analogy:** Like writing an email - you worry about every word, every sentence.

> **One-line summary:** Phase 1 polished the wording of requests, but results were unstable and hard to maintain.

---

### 3.2. Context Engineering (2025)

**Focus**: *"What information do I feed the AI so it answers well?"*

**Characteristics:**
- Focus on providing the right input data
- Use RAG (Retrieval Augmented Generation = search your documents first, then paste the relevant parts into the prompt)
- Efficient context window management (the context window = how much text the model can "see" at once)
- Integrate knowledge bases

**Example:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/02-3-2-context-engineering-2025.js`](examples/02-3-2-context-engineering-2025.js)

</details>

**Advantages:**
- Improves accuracy
- Reduces hallucination (hallucination = the model confidently making things up)
- Can scale with large datasets

**Limitations:**
- Still dependent on context quality
- Does not control the AI's behavior
- Hard to handle complex situations

**Analogy:** Like attaching the right files to an email - you provide all the information needed.

> **One-line summary:** Phase 2 fed the model better data, but you still could not control what it did with that data.

---

### 3.3. Harness Engineering (2026+)

**Focus**: *"How does the entire system around the AI operate?"*

**Characteristics:**
- Design the entire operating environment
- Integrate tools, memory, guardrails
- Strictly control the AI's behavior
- Automatically handle errors and optimize

**Example:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/03-3-3-harness-engineering-2026.js`](examples/03-3-3-harness-engineering-2026.js)

</details>

**Advantages:**
- Full control over AI behavior
- Easy to debug and maintain
- Scalable and reusable
- Stable, reliable results

**Analogy:** Like designing the entire office and workflows - you create a complete ecosystem.

> **One-line summary:** Phase 3 builds the whole operating system around the model: tools, limits, checks, and recovery.

---

### Overview Comparison

How to read the diagram: it lists the three phases top-down in time order; each box shows the guiding question, the focus, and the "Control" level in stars (1 star = little control, 5 stars = full control).

```
┌─────────────────────────────────────────────────────────────┐
│                  EVOLUTION OF AI ENGINEERING                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2022-2024: PROMPT ENGINEERING                              │
│  ┌─────────────────────────────────┐                         │
│  │ "How do I ask it right?"        │                         │
│  │ Focus: The prompt               │                         │
│  │ Control: ⭐ Low                 │                         │
│  └─────────────────────────────────┘                         │
│                    │                                        │
│                    ▼                                        │
│  2025: CONTEXT ENGINEERING                                  │
│  ┌─────────────────────────────────┐                         │
│  │ "What information to feed?"     │                         │
│  │ Focus: Input data               │                         │
│  │ Control: ⭐⭐ Medium             │                         │
│  └─────────────────────────────────┘                         │
│                    │                                        │
│                    ▼                                        │
│  2026+: HARNESS ENGINEERING                                  │
│  ┌─────────────────────────────────┐                         │
│  │ "How does the system run?"     │                         │
│  │ Focus: The entire environment   │                         │
│  │ Control: ⭐⭐⭐⭐⭐ High          │                         │
│  └─────────────────────────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **One-line summary:** Control grows with each era: from 1 star (prompting) to 5 stars (harness engineering).

### Key Insight

> **"Prompt Engineering is not dead, but it is no longer enough"**

Each phase does not completely replace the previous one; it adds another layer of control:
- You still need **good prompts** (Prompt Engineering)
- You still need **appropriate context** (Context Engineering)
- But you also need a **complete system** (Harness Engineering)

> **One-line summary:** Each phase stacks on the last: good prompts and context stay necessary, but the full system is what makes results reliable.

---

## 4. Why Is Harness Engineering Important?

This section lists six concrete reasons, with numbers, why investing in the harness pays off.

### 4.1. Outstanding Performance Optimization

**Research from Princeton NLP** (the SWE-agent paper) demonstrated a breakthrough finding:

> Just by changing the way you design the **"interface/environment"** (ACI - Agent-Computer Interface = the commands and screens the agent uses to work with the computer), AI performance can **improve by up to 64%** without upgrading the model.

**Experimental results:**

| Approach | Success Rate | Improvement |
|---------------|--------------|-------------|
| Baseline (no harness) | 12.5% | - |
| With optimized harness | 20.5% | +64% |

How to read it: "Approach" is the setup tested; "Success Rate" is the percentage of coding tasks completed correctly; "Baseline" is the starting setup with no harness work. For instance, 12.5% → 20.5% means fixing 8 more tasks per 100, purely from interface design.

**What does this mean?**
- Harness design can matter more than which AI model you choose
- Higher ROI (return on investment = benefit per dollar spent) than training/fine-tuning a new model
- Can be applied immediately without large resources

> **One-line summary:** Princeton showed a 64% performance gain from interface design alone — no new model needed.

---

### 4.2. The Model Is Just a Tool; the System Decides the Outcome

**The reality of the AI market:**

```
┌──────────────────────────────────────────────────────┐
│  COMMODITIZATION OF AI MODELS                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  2023: GPT-4 was the "king"                          │
│  2024: Claude 3, Gemini Ultra competing               │
│  2025: Many models of equivalent capability          │
│  2026: Models become a "commodity"                   │
│                                                      │
│  ➜ The difference is no longer in the model          │
│  ➜ The difference lies in the HARNESS                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

("Commodity" = something widely available and interchangeable, like electricity — you do not pick a power brand, you pick what you do with it.)

**A real-world example:**

The same Claude 3.5 Sonnet model:
- **Cursor IDE**: very effective for coding
- **Random chatbot**: not so good

➜ **What makes the difference?** Cursor's harness design!

> **One-line summary:** When every model is equally good, the harness — not the model — is what sets your product apart.

---

### 4.3. Control and Reliability

This section contrasts the old "trust the output" approach with the harness approach of checking everything.

**The problem with the old approach:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/04-4-3-control-and-reliability.js`](examples/04-4-3-control-and-reliability.js)

</details>

**With Harness Engineering:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/05-4-3-control-and-reliability.js`](examples/05-4-3-control-and-reliability.js)

</details>

> **One-line summary:** Without checks the AI's raw output reaches users with its errors; with a harness, every output passes validation first.

---

### 4.4. Scalability and Maintainability

This section shows why fixing one shared component beats patching ten separate prompts.

**A real scenario:**

You have 10 AI agents in your system. You discover a security bug:

**❌ Without a Harness:**
```
- You must update 10 different prompts
- You must re-test 10 agents
- No guarantee it's fully fixed
- Takes 2-3 days
```

**✅ With a Harness:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/06-4-4-scalability-and-maintainability.js`](examples/06-4-4-scalability-and-maintainability.js)

</details>

> **One-line summary:** With a harness, one fix in one shared component updates all 10 agents at once.

---

### 4.5. Significant Cost Savings

This section breaks down where the money goes — and where the harness saves it.

**Cost Savings from Harness Engineering:**

1. **Reduce token usage** (a token = a chunk of text the model reads or writes; API bills count tokens)
   - Context compression (squeezing long input into a shorter summary)
   - Smart caching (reusing earlier results instead of paying to regenerate them)
   - Efficient tool calling
   - **Savings: 40-60% of cost**

2. **Reduce error rate**
   - Automatic validation
   - Built-in guardrails
   - **Reduction: 70-80% of failed requests**

3. **Increase development speed**
   - Reusable components
   - Clear architecture
   - **Increase: 3-5x faster development**

**Calculation example:**

```
Traditional AI Agent project:
- API cost: $2,000/month
- Development time: 3 months
- Error handling: 40 hours/month
Total: ~$30,000 (3 months)

With Harness Engineering:
- API cost: $800/month (60% reduction)
- Development time: 1 month (reuse the harness)
- Error handling: 5 hours/month (automated)
Total: ~$12,000 (3 months)

➜ Savings: $18,000 (60%)
```

> **One-line summary:** Compressing context, cutting errors, and reusing components can save about 60% of total project cost.

---

### 4.6. Competitive Advantage

As AI models become equivalent to one another, **Harness Engineering is the competitive moat** (moat = a lasting advantage competitors cannot easily copy, like a castle's water barrier):

- **Anthropic**: a superlative harness (per the Claude code leak)
- **Cursor**: a harness optimized for coding
- **Perplexity**: a good harness for search & research

➜ This is why they lead the market!

> **One-line summary:** Top AI products win through harness quality, because anyone can access the same models.

---

### In Summary

Harness Engineering matters because:

1. ✅ **Boosts performance by 64%+** (per Princeton research)
2. ✅ **Creates a competitive advantage** as models become commodities
3. ✅ **More controllable and reliable**
4. ✅ **Easy to scale and maintain**
5. ✅ **Saves 40-60% of costs**
6. ✅ **Accelerates development 3-5x**

> **"In the age of AI commoditization, your harness is your moat"**

> **One-line summary:** Better results, lower cost, easier maintenance, and a durable edge — all from the harness, not the model.

---

## 5. The Core Components of a Harness

This section explains the 7 building blocks every harness needs. Each is nicknamed after a body part, so the architecture diagram reads like an anatomy chart.

A complete harness consists of 7 main components. Think of them as the "organs" of the human body:

```
┌─────────────────────────────────────────────────────────┐
│              COMPLETE HARNESS ARCHITECTURE               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │   TOOLS     │◄────►│   MEMORY    │                 │
│  │ (Hands & feet)│    │ (The brain)  │                 │
│  └─────────────┘      └─────────────┘                 │
│         ▲                    ▲                         │
│         │                    │                         │
│         ▼                    ▼                         │
│  ┌─────────────────────────────────┐                  │
│  │      CONTEXT MANAGEMENT         │                  │
│  │      (Circulatory system)        │                  │
│  └─────────────────────────────────┘                  │
│         ▲                    ▲                         │
│         │                    │                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │ GUARDRAILS  │      │  FEEDBACK   │                 │
│  │(Immune sys.)│      │ (Senses)    │                 │
│  └─────────────┘      └─────────────┘                 │
│         ▲                    ▲                         │
│         │                    │                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │ PERMISSIONS │      │ ORCHESTRATION│                │
│  │ (Skeleton)  │      │(Nervous sys.)│                │
│  └─────────────┘      └─────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

How to read the diagram: each box is one component, nicknamed after a body part; arrows show how they feed into each other, all flowing through Context Management at the center.

> **One-line summary:** A harness is 7 "organs" — tools, memory, context, guardrails, feedback, permissions, orchestration — working as one body.

---

### 5.1. Tools - "Hands & Feet"

This section explains tools: the actions the agent can actually perform in the outside world.

**Purpose**: Define what the AI can **do** — read a file, run a command, call an API. Tools are the agent's hands: no tools, no action.

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/07-5-1-tools-hands-feet.ts`](examples/07-5-1-tools-hands-feet.ts)

</details>

**Best Practices:**
- ✅ Limit the scope of each tool (single responsibility = one tool does exactly one job, like a screwdriver, not a Swiss-army knife)
- ✅ Validate inputs and outputs (check the data before and after)
- ✅ Clear error messages
- ✅ Idempotent where possible (idempotent = running the same action twice gives the same result as once, like "set file X to value Y" versus "append Y to file X")
- ❌ Avoid overly powerful tools (e.g., "execute_any_command")

> **One-line summary:** Give the agent many small, safe, well-checked tools — not a few all-powerful ones.

---

### 5.2. Memory - "The Brain"

This section explains memory: how the agent stores and recalls information across steps and sessions.

**Purpose**: Manage the information the AI needs to **remember**

**3 Types of Memory:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/08-5-2-memory-the-brain.ts`](examples/08-5-2-memory-the-brain.ts)

</details>

**Implementation Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/09-5-2-memory-the-brain.ts`](examples/09-5-2-memory-the-brain.ts)

</details>

**Best Practices:**
- ✅ Context compression when needed (summarize old content instead of keeping it all)
- ✅ Prioritize relevant memories
- ✅ Clear working memory after a task (working memory = the scratchpad for the current task)
- ✅ Separate concerns (short/long/working = short-term is this task, long-term is saved knowledge, working is the current scratchpad)

> **One-line summary:** Keep the right things in memory, throw away the rest, and never mix the three memory types.

---

### 5.3. Context Management - "The Circulatory System"

This section explains context management: delivering the right information to the model at the right moment, like blood carrying oxygen.

**Purpose**: Ensure the AI always has the right information at the right time

**5 Context Levels (per Anthropic):**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/10-5-3-context-management-the-circulatory-system.ts`](examples/10-5-3-context-management-the-circulatory-system.ts)

</details>

**Context Optimization Strategies:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/11-5-3-context-management-the-circulatory-system.ts`](examples/11-5-3-context-management-the-circulatory-system.ts)

</details>

> **One-line summary:** Context management keeps the model's "blood supply" clean: the right information, at the right time, in the right amount.

---

#### Where Does the Intervention Happen?

This subsection answers a practical question: where, exactly, does your code touch the prompt before the model sees it?

Your question: **"How do I intervene between the prompt and the LLM?"**

This is exactly the core of RAG. The actual flow is:

```
① User types: "Does health insurance cover heart disease?"
        │
        ▼
② You write code that INTERCEPTS this prompt
        │
        ├── Send the prompt to a Vector DB SEARCH (turn it into a query)
        │      └── Vector DB returns: [relevant_chunk_1, relevant_chunk_2, ...]
        │
        ▼
③ You MERGE the retrieved chunks into the original prompt:
        │
        │   Final prompt that reaches the LLM:
        │   ┌─────────────────────────────────────────────┐
        │   │ System: Answer using the following info:    │
        │   │                                             │
        │   │ [Context from the Vector DB]                │
        │   │ • Health insurance covers 80-100% of costs, │
        │   │   depending on the tier of care             │
        │   │ • Cardiovascular disease is on the covered  │
        │   │   list of health insurance services         │
        │   │                                             │
        │   │ User: Does health insurance cover heart     │
        │   │       disease?                              │
        │   └─────────────────────────────────────────────┘
        │
        ▼
④ LLM receives the prompt WITH context → answers accurately
```

(Glossary for the diagram: **Vector DB** = a database that stores text as vectors, lists of numbers that represent meaning, so similar meanings can be found fast; **chunk** = a small piece of a document, because searching whole long documents is too coarse.)

<details>
<summary><b>Sample code — done in 10 lines (Click to view)</b></summary>

> 📄 **Example code:** [`examples/12-where-does-the-intervention-happen.py`](examples/12-where-does-the-intervention-happen.py)
</details>

To sum up: **You don't modify the LLM; you modify the PROMPT before sending it.**

> **One-line summary:** Intervention happens in your own code, between the user's question and the model — search, then paste relevant chunks into the prompt.

<br>

#### How Does That Code Run Automatically?

This subsection gives four concrete places to install that code, from no-code to full frameworks.

A practical question: **"I have the code already, but how does it run between the prompt and the LLM?"**

There are 4 ways, depending on your setup:

---

**Way 1 — Wrapper API (Simplest, works for any app)**

You write a small server that acts as a **proxy** (proxy = a middleman server: apps talk to it, it talks to the real LLM): your chat app calls this proxy, and the proxy automatically retrieves context before calling the LLM.

```
Chat App (any) ──► YOUR PROXY ──► Ollama API
                        │
                        ├── Receives the prompt from the app
                        ├── Searches the Vector DB
                        ├── Merges context into the prompt
                        └── Sends the augmented prompt to Ollama
```

<details>
<summary><b>Sample code — proxy server with Flask (Click to view)</b></summary>

> 📄 **Example code:** [`examples/13-how-does-that-code-run-automatically.py`](examples/13-how-does-that-code-run-automatically.py)

**How to use it:** In your chat app, instead of calling `localhost:11434`, call `localhost:5000/api/chat`. RAG happens automatically.
</details>

---

**Way 2 — Function Wrapper (Inside your own Python code)**

<details>
<summary><b>Sample code — Function Wrapper (Click to view)</b></summary>

If you're writing your own Python app, just wrap the function that calls the LLM:

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/14-how-does-that-code-run-automatically.py`](examples/14-how-does-that-code-run-automatically.py)

</details>
</details>

---

**Way 3 — Open WebUI (No coding required)**

If you're using [Open WebUI](https://openwebui.com/), it already has this mechanism built in:

```
Settings → Documents → Upload file → 
When chatting: @mention that file → automatic RAG
```

Or use Open WebUI's **Pipeline** feature to write filter middleware (middleware = code that sits in the middle of a request and can modify it before it continues).

---

**Way 4 — LangChain / LlamaIndex (Professional frameworks)**

<details>
<summary><b>Sample code — LangChain (Click to view)</b></summary>

> 📄 **Example code:** [`examples/15-how-does-that-code-run-automatically.py`](examples/15-how-does-that-code-run-automatically.py)
</details>

---

**To summarize: You just need to pick one of the 4 ways:**

| Way | When to use | Difficulty |
|------|-------------|--------|
| **Proxy server** | Any chat app (web, mobile, desktop) | ⭐⭐ |
| **Function wrapper** | Your own Python code | ⭐ |
| **Open WebUI** | Already using Open WebUI | ⭐ (no code) |
| **LangChain/LlamaIndex** | Production, needs many features | ⭐⭐⭐ |

How to read it: "Way" is the option name; "When to use" tells which setup it fits; "Difficulty" uses stars (1 star = easy, 3 stars = hardest). For instance, if your app is Python, the function wrapper is the easiest.

<br>

> **📌 Key Concepts:**
> - **Semantic Search** understands meaning, not just keyword matching (so "car repair" can match "fixing automobiles")
> - **Vector Embedding** turns text into a sequence of numbers (a vector) that computers can compare
> - **Similarity** measures the distance between vectors in a multi-dimensional space
> - **Chunking** splits documents into smaller pieces before embedding (embedding = converting text into that vector of numbers)
> - **Vector Database** stores and retrieves vectors quickly

> **One-line summary:** Four ways to install RAG — proxy server, function wrapper, Open WebUI, or a framework — pick by how much you need to control.

---

### 5.4. Guardrails - "The Immune System"

This section explains guardrails: automatic checks that block harmful or wrong inputs and outputs, like antibodies blocking infection.

**Purpose**: Prevent unwanted behavior

**Types of Guardrails:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/16-5-4-guardrails-the-immune-system.ts`](examples/16-5-4-guardrails-the-immune-system.ts)

</details>

**Implementation Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/17-5-4-guardrails-the-immune-system.ts`](examples/17-5-4-guardrails-the-immune-system.ts)

</details>

> **One-line summary:** Guardrails are automatic checks on every input and output — bad content gets blocked, not just discouraged.

---

### 5.5. Feedback Loops - "Senses"

This section explains feedback loops: the agent measures the result of its own actions and corrects course, like eyes and ears guiding your hands.

**Purpose**: Automatically learn and improve from results

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/18-5-5-feedback-loops-senses.ts`](examples/18-5-5-feedback-loops-senses.ts)

</details>

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/19-5-5-feedback-loops-senses.ts`](examples/19-5-5-feedback-loops-senses.ts)

</details>

> **One-line summary:** Run → check the result → fix and retry, automatically, until the result is good.

---

### 5.6. Permissions - "The Skeleton"

This section explains permissions: the hard limits on what the agent may touch — the skeleton holds the body upright no matter what the muscles try.

**Purpose**: Define what the AI is allowed to do, where, and when. Example: an allowlist ("whitelist" = the only list of allowed items) of folders the agent may write to; anything outside it is refused.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/20-5-6-permissions-the-skeleton.ts`](examples/20-5-6-permissions-the-skeleton.ts)

</details>

> **One-line summary:** Permissions draw a hard boundary around the agent's actions — outside it, nothing happens.

---

### 5.7. Orchestration - "The Nervous System"

This section explains orchestration: the coordinator that makes all other components fire in the right order, like nerves signaling muscles.

**Purpose**: Coordinate all components to work in harmony

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/21-5-7-orchestration-the-nervous-system.ts`](examples/21-5-7-orchestration-the-nervous-system.ts)

</details>

> **One-line summary:** Orchestration is the conductor: it decides which component runs, when, and what happens next.

---

### Integrate Everything

This section combines all 7 components into one working harness.

<details>
<summary><b>Integrate Everything (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/22-integrate-everything.ts`](examples/22-integrate-everything.ts)

</details>

> **One-line summary:** One file wires the 7 components together into a complete, running harness.

---

### Integrate Components With Modules in the Repo

This section connects the theory to this repository: each harness component maps to numbered skill modules (folders) you can study and reuse.

Each component of the Harness maps directly to modules in the **AI Coding Skills Framework**. This is how the components "connect" to practice:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HARNESS → MODULE MAPPING                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   TOOLS     │ ───► │ 06-decide-tools-mcp                 │     │
│  │ (Hands & feet)│    │ Tool selection & MCP integration     │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   MEMORY    │ ───► │ 01-retrieve-memory-knowledge        │     │
│  │  (The brain) │     │ 03-update-memory-store               │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │   CONTEXT   │ ───► │ 02-build-context                    │     │
│  │ (Circulation)│      │ Context building & management       │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ GUARDRAILS  │ ───► │ 05-prompt-builder (Guardrails)      │     │
│  │(Immune sys.)│      │ 11-evaluation (validation)           │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │  FEEDBACK   │ ───► │ 07-workflow (retry, loop patterns)  │     │
│  │  (Senses)   │      │ 11-evaluation (metrics & feedback)  │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ PERMISSIONS │ ───► │ 06-decide-tools-mcp (tool perms)    │     │
│  │  (Skeleton)  │     │ 10-automation (access control)       │     │
│  └─────────────┘      └─────────────────────────────────────┘     │
│                                                                     │
│  ┌─────────────┐      ┌─────────────────────────────────────┐     │
│  │ ORCHESTRATION│───►│ 07-workflow (workflow engine)         │     │
│  │(Nervous sys.)│     │ 09-multi-agent (agent coordination)  │     │
│  └─────────────┘      │ 04-plan-decompose-task (planning)    │     │
│                        │ 08-task (task management)             │     │
│                        └─────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Detailed Mapping Table

This table is the text version of the diagram above: one row per harness component.

| Component | Analogies | Modules in the Repo | Description |
|-----------|-----------|-------------------|-------|
| **Tools** | "Hands & feet" | `06-decide-tools-mcp` | Define which tools the AI may use; MCP integration |
| **Memory** | "The brain" | `01-retrieve-memory-knowledge`, `03-update-memory-store` | Remember & retrieve knowledge; update memory |
| **Context Management** | "The circulatory system" | `02-build-context` | Build the appropriate context for each task |
| **Guardrails** | "The immune system" | `05-prompt-builder`, `11-evaluation` | Protective barriers; input/output checks |
| **Feedback Loops** | "Senses" | `07-workflow`, `11-evaluation` | Feedback loops, retries, quality evaluation |
| **Permissions** | "The skeleton" | `06-decide-tools-mcp`, `10-automation` | Grant resource access permissions |
| **Orchestration** | "The nervous system" | `07-workflow`, `09-multi-agent`, `04-plan-decompose-task`, `08-task` | Coordinate all components to work in harmony |

How to read it: "Component" is the harness part; "Analogies" is the body-part nickname from section 5; "Modules in the Repo" are the numbered skill folders in this repository (backticks = folder names); "Description" says what those folders teach. For instance, Tools ("hands & feet") maps to `06-decide-tools-mcp`, the module about choosing tools and wiring up MCP (MCP = Model Context Protocol, a standard way to plug external tools into an AI model).

> **Insight**: Prompt Engineering (`05-prompt-builder`) is not a separate component of the Harness — it is a **foundational technique** woven throughout many components: System Prompts in Orchestration, Few-shot in Context Management, Structured Output in Guardrails.

> **One-line summary:** Every harness component has a matching numbered module in this repo — start from the component you need and open that folder.

---

## 🔭 Overview: Harness Engineering — AI Coding Skills Framework

This section gives the big-picture map: the full harness architecture and how every numbered module in this repo fits into it.

### Overall Architecture: 7 Components → 15 Modules

The diagram below shows the **entire Harness Engineering system** and how it maps to the **15 modules** in the AI Coding Skills Framework — modules `01`–`11` are pipeline stages (steps that run in order, like an assembly line), and `12`–`15` are the cross-cutting control plane (rules every step must follow, not a step itself):

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║         AI CODING SKILLS FRAMEWORK — HARNESS ENGINEERING AT A GLANCE                 ║
║                 Architecture Overview: 7 Components → 15 Modules                    ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

                         EVOLUTION: THE 3 ERA OF AI ENGINEERING

 ┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────┐
 │  PROMPT ENGINEERING      │   │  CONTEXT ENGINEERING     │   │  HARNESS ENGINEERING │
 │  (2022-2024)             │──►│  (2025)                  │──►│  (2026+)             │
 │  "How to ask it right"   │   │  "What info to feed"     │   │  "Design the whole  │
 │  Control level: ★☆☆      │   │  Control level: ★★☆      │        system"          │
 │                          │   │                          │   │  Control level: ★★★ │
 └──────────────────────────┘   └──────────────────────────┘   └──────────┬───────────┘
                                                                           │
              ┌────────────────────────────────────────────────────────────┘
              ▼

 ┌─────────────────────────────────────────────────────────────────────────────────────┐
 │                              HARNESS — THE WHOLE SYSTEM                             │
 │                                                                                     │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🧠 ORCHESTRATION              │                        │
 │                         │     (Nervous system —            │                        │
 │                         │      coordination)               │                        │
 │                         │                                    │                        │
 │                         │  ┌────────┐ ┌────────┐ ┌────────┐ │                        │
 │                         │  │04-plan │ │07-work │ │08-task │ │                        │
 │                         │  │decom-  │ │ -flow  │ │ (task  │ │                        │
 │                         │  │pose    │ │(work-  │ │ mgmt)  │ │                        │
 │                         │  │(plan-  │ │ flow)  │ │        │ │                        │
 │                         │  │ning)   │ │        │ │        │ │                        │
 │                         │  └────────┘ └────────┘ └────────┘ │                        │
 │                         │  ┌─────────────────────────────┐  │                        │
 │                         │  │ 09-multi-agent (coordination)│  │                        │
 │                         │  └─────────────────────────────┘  │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     📚 MEMORY (THE BRAIN)         │                        │
 │                         │     ─── RAG PIPELINE ───          │                        │
 │                         │                                    │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ① RETRIEVE (01-retrieve)     │ │                        │
 │                         │  │  ┌────────┐ ┌────────┐      │ │                        │
 │                         │  │  │Semantic│ │Keyword │      │ │                        │
 │                         │  │  │Search  │ │BM25    │      │ │                        │
 │                         │  │  │(vector)│ │        │      │ │                        │
 │                         │  │  └────────┘ └────────┘      │ │                        │
 │                         │  │  ┌────────┐ ┌────────┐      │ │                        │
 │                         │  │  │K-Graph │ │Hybrid   │      │ │                        │
 │                         │  │  │Retrieve│ │(RRF)    │      │ │                        │
 │                         │  │  └────────┘ └────────┘      │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ② RE-RANK + BUILD CONTEXT    │ │                        │
 │                         │  │  ├── Cross-Encoder scoring   │ │                        │
 │                         │  │  └── 02-build-context        │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ ③ UPDATE (03-update-memory)  │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🔄 CONTEXT MANAGEMENT          │                        │
 │                         │     (Circulatory system —         │                        │
 │                         │      5 levels)                    │                        │
 │                         │                                    │                        │
 │                         │  ┌──────┐ ┌──────┐ ┌──────┐      │                        │
 │                         │  │Level1│ │Level2│ │Level3│      │                        │
 │                         │  │System│ │Task  │ │Domain│      │                        │
 │                         │  └──────┘ └──────┘ └──────┘      │                        │
 │                         │  ┌──────┐ ┌──────┐               │                        │
 │                         │  │Level4│ │Level5│               │                        │
 │                         │  │Chat   │ │Immed │               │                        │
 │                         │  └──────┘ └──────┘               │                        │
 │                         │  Module: 02-build-context         │                        │
 │                         │  Module: 05-prompt-builder        │                        │
 │                         └────────────┬─────────────────────┘                        │
 │                                      │                                               │
 │            ┌─────────────────────────┼─────────────────────────┐                    │
 │            │                         │                         │                    │
 │            ▼                         ▼                         ▼                    │
 │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                   │
 │  │ 🛠️ TOOLS         │  │ 🛡️ GUARDRAILS   │  │ 🔁 FEEDBACK     │                   │
 │  │ (Hands & feet)   │  │ (Immune system)  │  │ LOOPS (Senses)   │                   │
 │  │                   │  │                  │  │                  │                   │
 │  │ 06-decide-tools   │  │ Input validation│  │ 07-workflow      │                   │
 │  │ MCP integration   │  │ Output validation│ │ (retry patterns) │                   │
 │  │ Tool validation   │  │ Security checks │  │ 11-evaluation    │                   │
 │  │                   │  │ Prompt injection│  │ (metrics)        │                   │
 │  │                   │  │ detection       │  │ loop/ (top-level)│                   │
 │  └──────────────────┘  └──────────────────┘  └──────────────────┘                   │
 │            │                         │                         │                    │
 │            └─────────────────────────┼─────────────────────────┘                    │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🔒 PERMISSIONS (SKELETON)    │                        │
 │                         │                                    │                        │
 │                         │  ┌──────────────┐ ┌────────────┐ │                        │
 │                         │  │ File Access  │ │ Network    │ │                        │
 │                         │  │ Control      │ │ Restrictions│ │                       │
 │                         │  │ (10-auto)    │ │ (06-tools) │ │                        │
 │                         │  └──────────────┘ └────────────┘ │                        │
 │                         │  ┌──────────────────────────────┐ │                        │
 │                         │  │ Isolation & Execution        │ │                        │
 │                         │  │ Boundaries  → 12-sandbox     │ │                        │
 │                         │  │ Approval Gates   → 15        │ │                        │
 │                         │  └──────────────────────────────┘ │                        │
 │                         └──────────────────────────────────┘                        │
 │                                      │                                               │
 │                                      ▼                                               │
 │                         ┌──────────────────────────────────┐                        │
 │                         │     🤖 LLM + RESPONSE             │                        │
 │                         │     (AI model + response)         │                        │
 │                         │     ← final output                │                        │
 │                         └──────────────────────────────────┘                        │
 └─────────────────────────────────────────────────────────────────────────────────────┘

════════════════════════════════════
                        CORE MODULES IN THE FRAMEWORK

  ┌────────────────────────────────────────────────────────────────────────────────┐
  │  01  ── retrieve-memory-knowledge (Retrieve & Memory — RAG Pipeline)           │
  │  02  ── build-context             (Context Management — 5 levels)              │
  │  03  ── update-memory-store       (Memory Update — store new knowledge)        │
  │  04  ── plan-decompose-task       (Planning — break down tasks)                │
  │  05  ── prompt-builder            (Prompt + Guardrails)                        │
  │  06  ── decide-tools-mcp          (Tools + Permissions + MCP)                  │
  │  07  ── workflow                  (Workflow + Feedback Loops)                  │
  │  08  ── task                      (Task Management)                            │
  │  09  ── multi-agent               (Agent Orchestration)                        │
  │  10  ── automation                (Automation + Access Control)                │
  │  11  ── evaluation                (Evaluation + Metrics)                       │
  │  12  ── sandbox-execution         (Sandbox — isolation & execution boundaries) │
  │  13  ── trajectory-observability  (Trajectory — observability spine)           │
  │  14  ── compaction-context        (Compaction — context window management)     │
  │  15  ── approval-gates            (Approval Gates — human-in-the-loop)         │
  └────────────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────────────────────────────────────┐
                         │      CROSS-CUTTING CONTROL PLANE (12–15)        │
                         │      Not a pipeline stage — a substrate that     │
                         │      every module above must satisfy.           │
                         │                                              │
                         │  12 sandbox      → isolation boundaries         │
                         │  13 trajectory   → observable, replayable       │
                         │  14 compaction   → bounded context growth      │
                         │  15 approval     → irreversible ops gated     │
                         │                                              │
                         │  Each is authoritative for its own question;   │
                         │  other modules reference them, never restate.  │
                         └──────────────────────────────────────────────┘

  ══════════════════════════════════════════════════════════════════════════════════

  RELATIONSHIP ANALYSIS:
  - Harness ≈ THE ENTIRE outer frame (including the 7 components)
  - RAG Pipeline (01) ≈ part of the MEMORY component — the "brain" element
  - 15 modules ≈ 15 concrete skills; modules 01–11 are pipeline stages,
    modules 12–15 are the cross-cutting control plane they all depend on
  - Prompt Engineering (05) ≈ a foundational technique, woven through many components
  - The improvement loop is NOT harness/12. It lives in the top-level `loop/`
    part of the framework; harness/12 is sandbox isolation.

  PER-MODULE COVERAGE RATIO IN THE HARNESS:
  ┌─────────────────────────────────────────────────────────────────────────┐
  │  01-retrieve-memory     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  85%   │
  │  02-build-context       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
  │  03-update-memory       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░  50%   │
  │  04-plan-decompose      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░  55%   │
  │  05-prompt-builder      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  60%   │
  │  06-decide-tools        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  75%   │
  │  07-workflow            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  80%   │
  │  08-task                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░  45%   │
  │  09-multi-agent         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░  65%   │
  │  10-automation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░  40%   │
  │  11-evaluation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
  │  ── cross-cutting control plane — every stage above depends on these ──      │
  │  12-sandbox-execution   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  75%   │
  │  13-trajectory-obser   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  80%   │
  │  14-compaction-context  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░  65%   │
  │  15-approval-gates      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  70%   │
  └─────────────────────────────────────────────────────────────────────────┘
```

How to read the coverage bars: each line is one module; ▓ blocks are the share of that module's content that lives inside the harness, ░ blocks are the rest; the percentage is that share. For instance, `01-retrieve-memory` at 85% means most of the RAG retrieval skill is part of the harness's Memory component.

**In summary:**
| Aspect | RAG Pipeline (01) | Harness Engineering (whole) |
|-----------|-------------------|-------------------------------|
| **Scope** | 1 technique: retrieve + augment | 7 components, 15 modules |
| **Role** | Provide knowledge to the LLM | Control everything the AI can do |
| **Coverage** | ~85% of the Memory component | 100% of the whole system |
| **Relation** | Part of Memory | The whole that contains RAG |

How to read it: this table compares RAG (one technique: search your documents and paste the results into the prompt) with the full harness. "Scope" is how much it covers; "Relation" is the key row — RAG is a part inside the harness, not a rival to it.

> **One-line summary:** The harness is the whole frame; RAG is one organ inside it, and modules 01–15 are the concrete skills that build the frame.

---

## 6. Real-World Case Studies

The case studies below show how leading organizations apply Harness Engineering to achieve outstanding results.

---

### 6.1. SWE-agent (Princeton NLP)

This case study shows how small interface fixes — not a bigger model — doubled the fix rate.

**Context**: Princeton NLP developed an AI agent to automatically fix GitHub issues. (GitHub issue = a bug report or feature request filed on a repository.)

**Initial problems**:
- Success rate was only 12.5% with the baseline approach (baseline = the starting version before any improvements)
- The agent often "got lost" in the codebase
- Search results were too many, causing overwhelm
- No way to tell what information was important

**Harness Engineering solution**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

How to read the code below: each numbered block fixes one problem. 1 limits search output (grep = a command that searches file contents for a text pattern), 2 shows only a window of a file, 3 runs a linter (linter = a checker that flags syntax errors) before saving, 4 summarizes old chat history when it grows past 20 messages.

```typescript
// 1. LIMIT THE OUTPUT OF TOOLS
const searchTool = {
  name: "search_file",
  execute: async (pattern: string) => {
    const results = await grep(pattern);
    // ❌ Before: returned everything
    // ✅ After: limit to the first 50 results
    return results.slice(0, 50);
  }
};

// 2. INTELLIGENT VIEWER
const fileViewer = {
  name: "view_file",
  context: {
    showLineNumbers: true,
    contextLines: 100,  // Only show 100 lines at a time
    highlightRelevant: true
  },
  execute: async (file: string, startLine: number) => {
    // Instead of loading the whole file (which can be 1000+ lines)
    // Only load 100 lines around the area of interest
    return loadFileWindow(file, startLine, 100);
  }
};

// 3. REALTIME LINTER INTEGRATION
const editTool = {
  name: "edit_file",
  execute: async (file: string, changes: Change[]) => {
    const newContent = applyChanges(file, changes);
    
    // Automatically check syntax immediately
    const lintResult = await linter.check(newContent);
    
    if (lintResult.errors.length > 0) {
      // Do not allow saving a file with errors
      return {
        success: false,
        errors: lintResult.errors,
        message: "Please fix syntax errors before proceeding"
      };
    }
    
    await saveFile(file, newContent);
    return { success: true };
  }
};

// 4. COMPRESS CHAT HISTORY
const memoryManager = {
  compressHistory: async () => {
    if (history.length > 20) {
      // Summarize old conversations
      const old = history.slice(0, -10);
      const summary = await summarize(old);
      history = [
        { role: 'system', content: summary },
        ...history.slice(-10)
      ];
    }
  }
};
```

</details>

**Results**:
- Success rate increased from **12.5% → 20.5%** (+64%)
- Issue resolution time reduced by 40%
- Token usage reduced by 30%

**Key Insights**:
> "It's not that the model is weak — the environment wasn't well designed"

> **One-line summary:** Capping search output, showing file windows, linting before save, and compressing history took the fix rate from 12.5% to 20.5%.

---

### 6.2. Anthropic Multi-Agent Architecture

This case study shows why splitting work across several specialized agents beats one agent doing everything.

**Context**: Anthropic developed Claude Code to build complex applications (games, DAWs, etc.) (DAW = Digital Audio Workstation, professional music-production software)

**Initial problems**:
- A single agent doing too much at once → overwhelmed
- The agent stopped too early (before finishing)
- Or continued too long (didn't know when to stop)

**Solution: Multi-Agent Orchestration** (multi-agent = several smaller AI agents, each with one job, working under a coordinator)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/23-6-2-anthropic-multi-agent-architecture.ts`](examples/23-6-2-anthropic-multi-agent-architecture.ts)

</details>

**Characteristics of each Agent**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/24-6-2-anthropic-multi-agent-architecture.ts`](examples/24-6-2-anthropic-multi-agent-architecture.ts)

</details>

**Results**:
- Able to build complex applications: 2D games, DAW (Digital Audio Workstation)
- Success rate 80% higher than a single-agent setup
- Better code quality thanks to the evaluation loop

**Key Insights**:
> "Divide and conquer - Each agent focuses on one specific task"

> **One-line summary:** Give each agent one job and add an evaluator that checks the work — output quality and completion rate both jump.

---

### 6.3. Claude Code Leak - A Superlative Harness System

This case study shows what a top-tier harness looks like inside, revealed by a leaked codebase.

**Context**: In 2026, the source code of Claude Code was accidentally leaked, revealing an extraordinarily sophisticated harness architecture.

**Key findings**:

#### A. 5-Level Context Management

<details>
<summary><b>A. 5-Level Context Management (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/25-a-5-level-context-management.ts`](examples/25-a-5-level-context-management.ts)

</details>

#### B. 3-Tier Memory with Auto-Optimization

<details>
<summary><b>B. 3-Tier Memory with Auto-Optimization (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/26-b-3-tier-memory-with-auto-optimization.ts`](examples/26-b-3-tier-memory-with-auto-optimization.ts)

</details>

#### C. Strict Tool Permissions

<details>
<summary><b>C. Strict Tool Permissions (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/27-c-strict-tool-permissions.ts`](examples/27-c-strict-tool-permissions.ts)

</details>

#### D. Tone Detection with Regex (!)

<details>
<summary><b>D. Tone Detection with Regex (!) (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/28-d-tone-detection-with-regex.ts`](examples/28-d-tone-detection-with-regex.ts)

</details>

(Regex = regular expression, a short pattern for matching text — used here to detect the user's mood, e.g., frustration, and adjust the reply.)

**Results**:
- Claude Code became one of the best AI coding assistants
- User satisfaction rate > 90%
- High retention rate (retention = how many users keep coming back)

**Key Insights**:
> "The devil is in the details - Every small detail in the harness is carefully optimized"

> **One-line summary:** Small details — context levels, tiered memory, strict permissions, even tone detection — add up to a best-in-class product.

---

### 6.4. Cursor IDE - Harness Optimized for Coding

This case study shows that the same model, wrapped in a coding-focused harness, wins the market.

**Notable features**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/29-6-4-cursor-ide-harness-optimized-for-coding.ts`](examples/29-6-4-cursor-ide-harness-optimized-for-coding.ts)

</details>

**Results**:
- Became the most beloved coding assistant
- NPS (Net Promoter Score) > 70 (NPS = a 0-100 customer loyalty score; above 50 is considered excellent)
- Many developers switched from GitHub Copilot to Cursor

> **One-line summary:** A coding-first harness turned the same underlying model into a product users actively prefer.

---

### 6.5. DeepSeek Harness — Micro-Kernel & Trajectory Traceability Framework

This case study shows an extreme design: a tiny core where everything else is a detachable plugin, and every session step is recorded and replayable.

The DeepSeek Harness represents a highly extensible generation of AI Agent Harnesses built on the philosophy of **"Agent = Model + Harness"** and **"Everything is a Plugin"**. Built on the Cordis micro-kernel foundation (micro-kernel = the smallest possible core program; everything else loads around it), DeepSeek Harness turns every part of the agent (tools, context, memory, sub-agents) into independent plugins that can be attached and detached flexibly.

#### A. Micro-Kernel & Ecosystem Plugin Architecture
- **Cordis Core Framework**: Manages the plugin lifecycle through 4 stages (`init`, `attach`, `ready`, `detach`) — in plain words: start the plugin, connect it, mark it usable, remove it.
- **Context Service Registry**: Uses `ctx.provide()` and `ctx.inject()` to let plugins register and consume services independently (such as logger, llmProvider, memoryStore) — provide = "I offer this service"; inject = "give me that service".
- **See detailed guide**: [`harness/07-workflow/cordis-kernel-plugin.md`](./harness/07-workflow/cordis-kernel-plugin.md)

#### B. 4 Specialized Runtime Modes
DeepSeek Harness designs 4 dedicated execution environments suited to every need:
1. **Standard Mode**: A full-featured interactive CLI/GUI agent (CLI = typing commands in a terminal; GUI = a graphical app with windows and buttons) with complete MCP tools and middleware guardrails.
2. **Code Mode**: Runs through the SDK (`@deepseek-ai/dsh`) (SDK = a code library you call from your own program), batching many tool calls into a single code scenario, reducing latency and token cost by 70-90%.
3. **Minimal Benchmark Mode**: A minimal environment with just 2 tools (`bash`, `editor`) and a minimal prompt, to evaluate the LLM's native reasoning ability (benchmark = a standardized test to compare model performance).
4. **Creator Inspector Mode**: A runtime that visualizes the timeline, allowing inspection of context state and editing of preset agents.

#### C. Trajectory Traceability Engine (Session Event Stream & Branching)
- **Append-Only Event Log**: Every session development (Prompt, Reason, Tool Call, Output) is stored as an immutable sequence of events (`SessionEventStream`) — append-only = you only add new entries, never edit or delete old ones, like an audit notebook in pen.
- **Time-Travel Replay & Forking**: The ability to "pause" the session at any step, restore context state (`replayToStep`), and branch off (`forkSession`) to experiment with a different solution without breaking the original session — forking = copying the session at that point so you can try another path.
- **See detailed guide**: [`harness/03-update-memory-store/trajectory-fork-replay.md`](./harness/03-update-memory-store/trajectory-fork-replay.md)

#### D. Code Mode SDK & Sandboxed Execution
- Addresses the latency weakness of traditional multi-turn tool calling. The LLM identifies complex scenarios and generates TypeScript/Python code that calls the `@deepseek-ai/dsh` SDK.
- The scenario runs inside a safe Node.js `vm` sandbox (sandbox = an isolated enclosure; code inside can run but cannot touch anything outside), executing dozens of read/write/build operations in a single turn.
- **See detailed guide**: [`harness/06-decide-tools-mcp/code-mode-sdk.md`](./harness/06-decide-tools-mcp/code-mode-sdk.md)

#### E. Minimal Benchmark Harness for AI Capability Evaluation
- Fully isolates noise from complex frameworks. Enables running benchmarks (such as SWE-bench = a standard test set of real GitHub bug-fixing tasks) with high accuracy and absolute repeatability.
- **See detailed guide**: [`harness/11-evaluation/minimal-benchmark-harness.md`](./harness/11-evaluation/minimal-benchmark-harness.md)

> **One-line summary:** DeepSeek's design bets on a tiny core with pluggable parts and a replayable session log — maximum flexibility and testability.

---

### Common Lessons From the Case Studies

This table compares the five case studies, one technique per row.

| Lesson | SWE-agent | Anthropic | Claude Leak | Cursor | DeepSeek Harness |
|--------|-----------|-----------|-------------|--------|------------------|
| **Output limits** | ✅ Max 50 results | - | - | - | ✅ Stream limits |
| **Multi-agent** | - | ✅ 3 agents | ✅ Planner/Generator | - | ✅ Cordis Micro-Kernel |
| **Context layers** | ✅ 3 levels | - | ✅ 5 levels | ✅ Smart context | ✅ Service Registry |
| **Memory tiers** | ✅ Compression | - | ✅ 3 tiers | - | ✅ Session Event Stream |
| **Tool permissions** | - | - | ✅ Strict | ✅ Sandbox | ✅ VM Sandbox & SDK |
| **User feedback** | - | ✅ Evaluation | ✅ Tone detection | ✅ Suggestions | ✅ Creator Inspector |
| **Incremental** | - | - | - | ✅ Smart edits | ✅ Code Mode Single-turn |
| **Time-Travel / Fork** | - | - | - | - | ✅ Replay & Branching |

How to read it: rows are techniques; columns are the five case studies; ✅ = that study uses the technique, "-" = it does not. For instance, "Output limits" is used by SWE-agent (capped at 50 search results) and DeepSeek (limits on streamed output).

**Common principles**:
1. ✅ **Constraints enable creativity** - Limits help the AI focus
2. ✅ **Layered architecture** - Break the problem into smaller pieces
3. ✅ **Feedback loops** - Learn from results
4. ✅ **User-centric design** - Always think about UX (UX = user experience, how pleasant and clear the product feels)
5. ✅ **Obsess over details** - Every detail matters

> **One-line summary:** Every successful harness limits output, layers its parts, loops on feedback, and sweats the small stuff.

---

## 7. Harness Design Principles

This section gives the rules of thumb for designing a harness well.

### 7.1. SOLID Principles for Harness

SOLID = five classic software-design rules, adapted here for harnesses.

**1. Single Responsibility**
- Each tool does exactly one thing (e.g., a tool that reads files should not also delete them)
- Each component has one reason to change

**2. Open/Closed**
- The harness is open for extension (adding tools, guardrails)
- Closed for modification (core logic stays stable — you add, you don't rewrite)

**3. Liskov Substitution**
- Tools can substitute for one another (swap one search tool for another and nothing breaks)
- Same interface, different implementation

**4. Interface Segregation**
- Don't force the AI to use tools it doesn't need (show a code agent only code tools, not a calendar)
- Only expose what's necessary

**5. Dependency Inversion**
- Depend on abstractions, not implementations (call "a storage service", not "exactly Chroma" — so you can swap Chroma for Pinecone)
- Makes swapping components easy

> **One-line summary:** Design each piece for one job, easy to extend, and easy to swap.

---

### 7.2. The 10 Commandments of Harness Engineering

How to read it: each rule pairs the action to take (in capitals) with the mistake to avoid; e.g., "VALIDATE, not HOPE" means add automatic checks instead of hoping the AI behaves.

```
1. Thou shall LIMIT, not GUIDE
   → Constrain what the AI can do; don't just give instructions

2. Thou shall VALIDATE, not HOPE
   → Validate every input/output; don't hope the AI does it right

3. Thou shall DESIGN, not TRAIN
   → Design the environment; don't just train the model

4. Thou shall CONSTRAIN, not INSTRUCT
   → Create constraints; don't write lengthy instructions

5. Thou shall AUTOMATE, not MANUAL
   → Automate checks; don't make the user have to check

6. Thou shall FAIL FAST, not SLOW
   → Detect errors early; don't let them spread

7. Thou shall LOG EVERYTHING
   → Log every action for debugging and improvement

8. Thou shall ITERATE, not PERFECT
   → Ship and improve; don't wait for perfection

9. Thou shall MEASURE, not GUESS
   → Measure metrics; don't guess

10. Thou shall OBSESS OVER UX
    → User experience is the number one priority
```

> **One-line summary:** Limit, validate, automate, measure early — and treat the user's experience as the top priority.

---

### 7.3. The Harness Design Pattern

This section shows the pattern in code: one reusable template for wiring the 7 components together.

<details>
<summary><b>7.3. The Harness Design Pattern (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/30-7-3-the-harness-design-pattern.ts`](examples/30-7-3-the-harness-design-pattern.ts)

</details>

> **One-line summary:** Copy the pattern: tools + memory + context + guardrails + feedback + permissions, coordinated by one orchestrator.

---

## 8. Best Practices

This section is a checklist: what to do and what to avoid, grouped by harness part.

### 8.1. Tool Design

This subsection covers designing the agent's tools.

✅ **DO:**
- Keep tools small and focused
- Validate inputs and outputs
- Provide clear error messages
- Make tools idempotent when possible (idempotent = repeating the action causes no extra change, like "set X = 5" instead of "add 1 to X")
- Include examples in descriptions

❌ **DON'T:**
- Create "god tools" that do everything
- Trust AI to validate itself
- Use vague error messages
- Allow destructive operations without confirmation (e.g., deleting files or force-pushing git)

> **One-line summary:** Small tools, checked inputs, clear errors, and confirmation before anything destructive.

---

### 8.2. Memory Management

This subsection covers what the agent stores and for how long.

✅ **DO:**
- Compress context regularly (replace old turns with a short summary)
- Prioritize relevant information
- Clear working memory after tasks
- Use tiered storage (hot/warm/cold = data you need now, sometimes, or almost never — kept in fast, slower, cheapest storage respectively)

❌ **DON'T:**
- Keep entire conversation history
- Load unnecessary data
- Mix different types of memory
- Forget to clean up

> **One-line summary:** Store less, sort by importance, and delete scratch data when the task ends.

---

### 8.3. Context Building

This subsection covers what goes into the model's limited attention window.

✅ **DO:**
- Layer context by priority (system rules first, then task, then details)
- Include only relevant information
- Monitor token usage (token = a chunk of text the model reads/writes; you pay per token)
- Compress when approaching limits

❌ **DON'T:**
- Include everything
- Ignore token limits
- Use static context (static = the same content every time, regardless of the task)
- Forget immediate context

> **One-line summary:** Treat context as budget: rank by priority, include only what matters, compress before you hit the limit.

---

### 8.4. Guardrails

This subsection covers automatic safety checks.

✅ **DO:**
- Validate at multiple layers
- Check both input and output
- Fail fast and clearly
- Log all violations

❌ **DON'T:**
- Rely only on prompts (a prompt asking nicely is not a guardrail)
- Skip validation steps
- Hide errors from users
- Trust without verifying

> **One-line summary:** Check everything automatically at every layer, and never rely on the prompt alone.

---

### 8.5. Testing the Harness

This subsection covers verifying the harness itself, not just the model.

<details>
<summary><b>8.5. Testing the Harness (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/31-8-5-testing-the-harness.ts`](examples/31-8-5-testing-the-harness.ts)

</details>

> **One-line summary:** The harness is code too — test it with the same rigor as any other system.

---

## 9. Tools & Frameworks

This section lists ready-made software you can build your harness with, so you don't start from zero.

### 9.1. Popular Frameworks

These are full frameworks: pre-built code for tools, memory, and agent coordination.

**LangChain / LangGraph** (LangChain = a library that chains LLM calls with tools and data; LangGraph = its extension that arranges calls into a graph of steps)

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/32-9-1-popular-frameworks.ts`](examples/32-9-1-popular-frameworks.ts)

</details>

**AutoGen (Microsoft)** (a framework where multiple AI agents converse and collaborate)

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/33-9-1-popular-frameworks.py`](examples/33-9-1-popular-frameworks.py)

</details>

**CrewAI** (a framework that organizes agents into a "crew" with roles, like a team with a manager)

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/34-9-1-popular-frameworks.py`](examples/34-9-1-popular-frameworks.py)

</details>

> **One-line summary:** Three mature frameworks cover the main styles: chains (LangChain), conversations (AutoGen), and role-based teams (CrewAI).

---

### 9.2. Supporting Tools

These are specialized utilities that plug into your harness for storage, monitoring, safety, and testing.

**Vector Databases** (store text as vectors — lists of numbers representing meaning — for fast "search by meaning"; see 5.3):
- Pinecone
- Chroma
- Weaviate
- Qdrant

**Monitoring & Logging** (record every call so you can debug and measure):
- LangSmith
- Weights & Biases
- Helicone
- OpenLLMetry

**Guardrails** (pre-built input/output checkers):
- Guardrails AI
- NeMo Guardrails (NVIDIA)
- LlamaGuard (Meta)

**Testing** (tools that test prompts and RAG quality like unit tests):
- PromptFoo
- Deepeval
- Ragas

> **One-line summary:** Pick one tool from each group — storage, monitoring, guardrails, testing — and you have a working toolbox.

---

### 9.3. Starter Template

This section gives a minimal working harness you can copy and extend.

<details>
<summary><b>9.3. Starter Template (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/35-9-3-starter-template.ts`](examples/35-9-3-starter-template.ts)

</details>

> **One-line summary:** Start from the template instead of an empty file — it already wires the core components together.

---

## 10. The Future of Harness Engineering

This section looks ahead: where the field is heading, what will be hard, and how to prepare.

### 10.1. Trends 2026-2028

**1. Self-Optimizing Harnesses**
- Harnesses automatically adjust their parameters
- Automated A/B testing (A/B testing = trying two versions on real users and keeping the winner)
- Continuous learning from usage

**2. Harness-as-a-Service**
- Cloud platforms offering pre-built harnesses
- Plug-and-play harness components
- Marketplaces for harness templates

**3. Visual Harness Builders**
- No-code tools for designing harnesses (no-code = build by clicking and dragging, without writing code)
- Visual workflow editors
- Drag-and-drop tool composition

**4. Cross-Model Harnesses**
- One harness running on multiple models
- Automatic model switching based on the task
- Cost-optimized model routing (routing = choosing which model handles which request)

**5. Regulatory Compliance Harnesses**
- Built-in GDPR, HIPAA compliance (GDPR = the EU's data-privacy law; HIPAA = the US law protecting health data)
- Automated audit trails (audit trail = a recorded history of every action, for inspections)
- Explainability baked in

> **One-line summary:** Harnesses will tune themselves, ship as services, and carry legal compliance by default.

---

### 10.2. Challenges Ahead

This subsection lists the open problems, grouped by type.

**Technical Challenges:**
- Standardization across platforms (agreed common formats so harnesses work everywhere)
- Interoperability between harnesses (harnesses being able to work together)
- Performance optimization at scale
- Security and privacy

**Business Challenges:**
- ROI measurement (ROI = return on investment; proving the harness pays for itself)
- Team skill gaps
- Legacy system integration (legacy = old systems still in use)
- Changing regulations

**Research Challenges:**
- Optimal harness architecture patterns
- Automated harness generation
- Harness testing methodologies
- Cross-domain transferability (whether a harness built for one field works in another)

> **One-line summary:** The hard parts are shared standards, proving business value, and making harnesses work across models and domains.

---

### 10.3. Advice for the Future

How to read it: five pieces of advice, each with a one-line explanation after the arrow.

```
1. Start Simple
   → Don't over-engineer from the start
   → Build an MVP harness first (MVP = minimum viable product, the smallest version that works)

2. Measure Everything
   → Track metrics from day one
   → Data-driven optimization

3. Stay Updated
   → The field is evolving fast
   → Follow best practices

4. Share Knowledge
   → Open source harness components
   → Build community

5. Think Long-term
   → The harness is infrastructure
   → Invest in maintainability
```

> **One-line summary:** Start small, measure from day one, and build the harness to last.

---

## 11. Reference Materials

This section lists the sources behind the document, for going deeper.

### Papers & Research

1. **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
   - Princeton NLP Lab
   - https://arxiv.org/abs/2405.15793

2. **The Rise of AI Agents and the Importance of Harness Engineering**
   - Mitchell Hashimoto, HashiCorp
   - https://www.youtube.com/watch?v=example

3. **Building Reliable AI Agents with Guardrails**
   - Anthropic Research
   - https://www.anthropic.com/research

> **One-line summary:** Start with the SWE-agent paper — it is the empirical proof behind most of this document.

### Frameworks & Tools

1. **LangChain** - https://langchain.com
2. **LangGraph** - https://langchain-ai.github.io/langgraph/
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **CrewAI** - https://www.crewai.com
5. **Guardrails AI** - https://www.guardrailsai.com

> **One-line summary:** These are the official sites of the frameworks named in section 9.

### Communities

1. **LangChain Discord** - Active community (Discord = a chat platform with topic servers)
2. **r/LangChain** - Reddit discussions (Reddit = a forum site; "r/..." names a community board)
3. **AI Engineers** - Slack community (Slack = a workplace chat platform)
4. **HuggingFace Forums** - Technical discussions (HuggingFace = a hub for sharing AI models)

> **One-line summary:** Join one community — they surface new techniques months before blog posts do.

### Blogs & Resources

1. **Anthropic Blog** - https://www.anthropic.com/news
2. **OpenAI Cookbook** - https://cookbook.openai.com
3. **LangChain Blog** - https://blog.langchain.dev
4. **Mitchell Hashimoto's Blog** - https://mitchellh.com

> **One-line summary:** These blogs publish the newest harness design ideas as they happen.

### Courses & Tutorials

1. **DeepLearning.AI - Building AI Agents**
2. **LangChain Academy**
3. **Anthropic Prompt Engineering**
4. **Microsoft AutoGen Tutorial**

> **One-line summary:** Four free/paid courses to learn harness building hands-on.

> **One-line summary:** The SWE-agent paper is the key research source; the rest are tools, communities, and courses to keep learning.

---

**Conclusion**

Harness Engineering is not just a technology trend - it is a paradigm shift in how we build AI applications. As AI models become increasingly powerful and turn into "commodities" (widely available and interchangeable), the ability to design a good harness will be the deciding factor for success.

> **"The model thinks. The harness shapes what it thinks about. And the harness determines the quality of the final output."**

Start today - you don't need perfection, you just need to begin. Build, measure, learn, and iterate. Harness Engineering is a journey, not a destination.

**Happy Building! 🚀**

> **One-line summary:** The model is a commodity; the harness you build around it is the skill that wins.

---

**Last updated:** 16/10/2026  
**Author:** AI Knowledge Repository
