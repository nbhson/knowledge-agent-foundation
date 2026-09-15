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
    - [Overall Architecture: 7 Components → 12 Modules](#overall-architecture-7-components--12-modules)
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

In the AI era, we have witnessed the extraordinary growth of large language models (LLMs). From GPT-3, GPT-4, Claude, to Gemini, these models are getting ever smarter and more powerful. Yet an important question arises: **Why, with the same AI model, do some applications perform exceptionally well while others fail?**

The answer lies in **Harness Engineering** - a discipline that does not focus on improving the AI model itself, but instead focuses on building the entire **ecosystem around that model**: tools, permissions, memory, feedback loops, guardrails, and context management.

### Background

When Mitchell Hashimoto (founder of HashiCorp, author of Terraform) declared that *"Prompt Engineering is dead"* and introduced the concept of **Harness Engineering**, he opened a new chapter in how we think about building AI applications. Instead of worrying about writing the perfect prompt, we need to focus on building a complete system that lets AI operate effectively.

### Purpose of This Document

This document provides a comprehensive look at Harness Engineering, covering:
- Definition and core philosophy
- Comparison with earlier techniques (Prompt Engineering, Context Engineering)
- Components and design principles
- Case studies from leading organizations (Princeton NLP, Anthropic)
- Best practices and practical implementation guidance

---

## 2. What Is Harness Engineering?

### Definition

**Harness Engineering** is the practice of building and designing the entire **"environment around"** an AI model (including tools, permissions, memory, feedback loops, guardrails, context management, ...) instead of focusing on improving the model itself.

Put simply:
- The **AI model** is what **thinks**
- The **harness** is what the AI **thinks about**
- And the **harness** is what determines the **final output quality**

### Core Philosophy

> *"Every time an agent makes a mistake, you don't pray it does better next time – you build a systematic solution so it never makes that mistake again"*

This philosophy emphasizes:

1. **Systematic Solutions over Prayers**: Instead of hoping the AI will "learn" from its mistakes, you build systematic mechanisms that prevent that mistake from recurring.

2. **Infrastructure over Instructions**: Instead of writing long prompts telling the AI what to do, you build infrastructure that constrains what the AI can do.

3. **Design over Training**: Instead of fine-tuning the model, you design the environment in which the model operates.

### Illustrative Example

Imagine you have an AI coding assistant:

**❌ Old approach (Prompt Engineering):**
```
"Write Python code. Make sure your code has no syntax errors.
Check carefully before returning. If there are errors, fix them..."
```

**✅ New approach (Harness Engineering):**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

```javascript
// Integrate the linter into the harness
harness.addTool({
  name: "write_code",
  execute: async (code) => {
    // Automatically check syntax
    const lintResult = await linter.check(code);
    if (lintResult.hasErrors) {
      // Automatically reject and ask for a fix
      return { status: "error", errors: lintResult.errors };
    }
    return { status: "success", code };
  }
});
```

</details>

In the example above, instead of "asking" the AI to be careful, you build a system that does **not allow** the AI to return code with errors.

### Comparison With Other Concepts

| Aspect | Prompt Engineering | Context Engineering | Harness Engineering |
|-----------|-------------------|---------------------|---------------------|
| **Focus** | How you ask | Input data | The whole system |
| **Goal** | Better prompts | Better context | Better environment |
| **Example** | Writing an email | Attaching a file | Designing the office + workflows |
| **Control** | Low | Medium | High |
| **Durability** | Low | Medium | High |

---

## 3. Three Evolution Phases of AI Engineering

To better understand Harness Engineering, we need to look back at the evolution of AI engineering through three main phases:

### 3.1. Prompt Engineering (2022-2024)

**Focus**: *"How do I ask the AI the right way?"*

**Characteristics:**
- Focus on writing good prompts
- Use techniques: few-shot learning, chain-of-thought, role-playing
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

---

### 3.2. Context Engineering (2025)

**Focus**: *"What information do I feed the AI so it answers well?"*

**Characteristics:**
- Focus on providing the right input data
- Use RAG (Retrieval Augmented Generation)
- Efficient context window management
- Integrate knowledge bases

**Example:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

```javascript
// Retrieve relevant context
const relevantDocs = await vectorDB.search(query);
const context = relevantDocs.map(doc => doc.content).join('\n');

// Add to prompt
const prompt = `Context: ${context}\n\nQuestion: ${query}`;
```

</details>

**Advantages:**
- Improves accuracy
- Reduces hallucination
- Can scale with large datasets

**Limitations:**
- Still dependent on context quality
- Does not control the AI's behavior
- Hard to handle complex situations

**Analogy:** Like attaching the right files to an email - you provide all the information needed.

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

```javascript
const harness = new AIHarness({
  model: "claude-3-opus",
  tools: [codeExecutor, fileManager, webSearch],
  memory: {
    shortTerm: conversationHistory,
    longTerm: vectorStore,
    workingMemory: currentContext
  },
  guardrails: {
    maxTokens: 100000,
    allowedDomains: ["github.com", "stackoverflow.com"],
    securityRules: [noSensitiveData, validateOutputs]
  },
  feedback: {
    onError: autoRetry,
    onSuccess: logMetrics
  }
});
```

</details>

**Advantages:**
- Full control over AI behavior
- Easy to debug and maintain
- Scalable and reusable
- Stable, reliable results

**Analogy:** Like designing the entire office and workflows - you create a complete ecosystem.

---

### Overview Comparison

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

### Key Insight

> **"Prompt Engineering is not dead, but it is no longer enough"**

Each phase does not completely replace the previous one; it adds another layer of control:
- You still need **good prompts** (Prompt Engineering)
- You still need **appropriate context** (Context Engineering)
- But you also need a **complete system** (Harness Engineering)

---

## 4. Why Is Harness Engineering Important?

### 4.1. Outstanding Performance Optimization

**Research from Princeton NLP** (the SWE-agent paper) demonstrated a breakthrough finding:

> Just by changing the way you design the **"interface/environment"** (ACI - Agent-Computer Interface), AI performance can **improve by up to 64%** without upgrading the model.

**Experimental results:**

| Approach | Success Rate | Improvement |
|---------------|--------------|-------------|
| Baseline (no harness) | 12.5% | - |
| With optimized harness | 20.5% | +64% |

**What does this mean?**
- Harness design can matter more than which AI model you choose
- Higher ROI than training/fine-tuning a new model
- Can be applied immediately without large resources

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

**A real-world example:**

The same Claude 3.5 Sonnet model:
- **Cursor IDE**: very effective for coding
- **Random chatbot**: not so good

➜ **What makes the difference?** Cursor's harness design!

---

### 4.3. Control and Reliability

**The problem with the old approach:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

```javascript
// ❌ Cannot control
const response = await ai.chat("Fix this bug...");
// You have no idea what the AI will do
// You cannot guarantee the output
// You have a hard time debugging when something goes wrong
```

</details>

**With Harness Engineering:**

<details>
<summary><b>JavaScript Code (Click to expand/collapse)</b></summary>

```javascript
// ✅ Full control
const harness = new AIHarness({
  tools: {
    'file_edit': {
      validator: (path) => path.startsWith('/safe/dir'),
      maxSize: 10000,
      allowedExtensions: ['.js', '.ts', '.py']
    }
  },
  outputValidation: {
    checkSyntax: true,
    checkSecurity: true,
    runTests: true
  }
});

// You know exactly what the AI can do
// You guarantee the output is always valid
// You have detailed logs to debug with
```

</details>

---

### 4.4. Scalability and Maintainability

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

```javascript
// Fix it in one place inside the harness
harness.addSecurityRule({
  name: 'no-sensitive-data',
  validate: (output) => !containsSensitiveData(output)
});

// All agents automatically pick up this rule
// Test once
// Deploy in minutes
```

</details>

---

### 4.5. Significant Cost Savings

**Cost Savings from Harness Engineering:**

1. **Reduce token usage**
   - Context compression
   - Smart caching
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

---

### 4.6. Competitive Advantage

As AI models become equivalent to one another, **Harness Engineering is the competitive moat** (competitive advantage):

- **Anthropic**: a superlative harness (per the Claude code leak)
- **Cursor**: a harness optimized for coding
- **Perplexity**: a good harness for search & research

➜ This is why they lead the market!

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

---

## 5. The Core Components of a Harness

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

---

### 5.1. Tools - "Hands & Feet"

**Purpose**: Define what the AI can **do**

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface Tool {
  name: string;
  description: string;
  parameters: JSONSchema;
  execute: (params: any) => Promise<ToolResult>;
  validation?: {
    preExecution?: (params: any) => boolean;
    postExecution?: (result: any) => boolean;
  };
}

// Example: File Editor Tool
const fileEditorTool: Tool = {
  name: "edit_file",
  description: "Edit a file with specified changes",
  parameters: {
    type: "object",
    properties: {
      path: { type: "string" },
      changes: { type: "array" }
    }
  },
  execute: async (params) => {
    // Implementation
    return { success: true, content: "..." };
  },
  validation: {
    preExecution: (params) => {
      // Check if path is safe
      return params.path.startsWith('/safe/');
    },
    postExecution: (result) => {
      // Validate syntax
      return linter.check(result.content);
    }
  }
};
```

</details>

**Best Practices:**
- ✅ Limit the scope of each tool (single responsibility)
- ✅ Validate inputs and outputs
- ✅ Clear error messages
- ✅ Idempotent where possible
- ❌ Avoid overly powerful tools (e.g., "execute_any_command")

---

### 5.2. Memory - "The Brain"

**Purpose**: Manage the information the AI needs to **remember**

**3 Types of Memory:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface MemorySystem {
  // 1. Short-term Memory (Conversation)
  shortTerm: {
    maxMessages: number;
    messages: Message[];
    compress: () => void;
  };
  
  // 2. Long-term Memory (Knowledge)
  longTerm: {
    vectorStore: VectorDB;
    add: (content: string, metadata: any) => void;
    search: (query: string) => Promise<Document[]>;
  };
  
  // 3. Working Memory (Current Task)
  workingMemory: {
    currentTask: Task;
    subTasks: Task[];
    context: Map<string, any>;
  };
}
```

</details>

**Implementation Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class HarnessMemory implements MemorySystem {
  shortTerm = {
    maxMessages: 20,
    messages: [],
    compress: () => {
      // Summarize old messages when hitting limit
      if (this.messages.length > this.maxMessages) {
        const old = this.messages.slice(0, -10);
        const summary = this.summarize(old);
        this.messages = [
          { role: 'system', content: summary },
          ...this.messages.slice(-10)
        ];
      }
    }
  };
  
  longTerm = {
    vectorStore: new ChromaDB(),
    add: async (content, metadata) => {
      await this.vectorStore.add({
        content,
        metadata,
        embedding: await this.embed(content)
      });
    },
    search: async (query) => {
      return await this.vectorStore.search(query, { limit: 5 });
    }
  };
  
  workingMemory = {
    currentTask: null,
    subTasks: [],
    context: new Map()
  };
}
```

</details>

**Best Practices:**
- ✅ Context compression when needed
- ✅ Prioritize relevant memories
- ✅ Clear working memory after a task
- ✅ Separate concerns (short/long/working)

---

### 5.3. Context Management - "The Circulatory System"

**Purpose**: Ensure the AI always has the right information at the right time

**5 Context Levels (per Anthropic):**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface ContextManager {
  // Level 1: System Instructions
  systemContext: {
    identity: string;
    capabilities: string[];
    limitations: string[];
  };
  
  // Level 2: Task Context
  taskContext: {
    goal: string;
    constraints: string[];
    currentStep: number;
  };
  
  // Level 3: Domain Knowledge
  domainContext: {
    codebase: CodebaseInfo;
    documentation: Document[];
    conventions: Convention[];
  };
  
  // Level 4: Conversation History
  conversationContext: {
    history: Message[];
    summary: string;
  };
  
  // Level 5: Immediate Context
  immediateContext: {
    currentFile: string;
    recentChanges: Change[];
    openFiles: string[];
  };
  
  // Build final context for AI
  buildContext(): string;
}
```

</details>

**Context Optimization Strategies:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class SmartContextManager {
  async buildOptimizedContext(query: string): Promise<string> {
    // 1. Always include system & task
    const core = this.getSystemAndTaskContext();
    
    // 2. Retrieve relevant domain knowledge
    const relevant = await this.retrieveRelevant(query);
    
    // 3. Add compressed conversation history
    const history = this.compressHistory();
    
    // 4. Include immediate context
    const immediate = this.getImmediateContext();
    
    // 5. Ensure under token limit
    return this.fitToLimit([core, relevant, history, immediate]);
  }
  
  private fitToLimit(contexts: string[]): string {
    const limit = 100000; // tokens
    let total = '';
    let tokenCount = 0;
    
    for (const ctx of contexts) {
      const tokens = this.countTokens(ctx);
      if (tokenCount + tokens < limit) {
        total += ctx;
        tokenCount += tokens;
      } else {
        // Truncate or skip
        break;
      }
    }
    
    return total;
  }
}
```

</details>

---


#### Where Does the Intervention Happen?

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

<details>
<summary><b>Sample code — done in 10 lines (Click to view)</b></summary>

```python
import requests

OLLAMA_URL = "http://localhost:11434"

# 1. User types the prompt
user_prompt = "Does health insurance cover heart disease?"

# 2. INTERCEPT: embed the prompt → search the vector DB
def search_relevant_chunks(query):
    # Embed the query
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text",
        "input": query
    })
    query_vector = resp.json()["embeddings"][0]
    
    # Search ChromaDB/FAISS (simulated results)
    results = [
        "Health insurance covers 80% to 100% of costs, depending on the tier of care.",
        "Cardiovascular disease is on the list of services covered by health insurance.",
    ]
    return results

# 3. MERGE the context into the prompt
context = search_relevant_chunks(user_prompt)
final_prompt = f"""Answer the question using the following information:

{chr(10).join(f'• {c}' for c in context)}

Question: {user_prompt}"""

# 4. Send the AUGMENTED prompt to the LLM
response = requests.post(f"{OLLAMA_URL}/api/generate", json={
    "model": "gemma3:12b",
    "prompt": final_prompt,
    "stream": False
})

print(response.json()["response"])
```
</details>

To sum up: **You don't modify the LLM; you modify the PROMPT before sending it.**

<br>

#### How Does That Code Run Automatically?

A practical question: **"I have the code already, but how does it run between the prompt and the LLM?"**

There are 4 ways, depending on your setup:

---

**Way 1 — Wrapper API (Simplest, works for any app)**

You write a small server that acts as a **proxy**: your chat app calls this proxy, and the proxy automatically retrieves context before calling the LLM.

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

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434"

def search_relevant(query):
    """Search the Vector DB - replace with your real code"""
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text", "input": query
    })
    # Simulated results - replace with a real ChromaDB/Qdrant
    return [
        "Health insurance covers 80% to 100% of costs, depending on the tier of care.",
        "Cardiovascular disease is on the list of services covered by health insurance.",
    ]

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")
    
    # INTERCEPT: retrieve context
    context = search_relevant(user_prompt)
    
    # MERGE context into the prompt
    augmented_prompt = f"""Answer using the following information:

{chr(10).join(f'• {c}' for c in context)}

Question: {user_prompt}"""
    
    # Send to the LLM
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": data.get("model", "gemma3:12b"),
        "prompt": augmented_prompt,
        "stream": data.get("stream", False)
    })
    
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(port=5000)
```

**How to use it:** In your chat app, instead of calling `localhost:11434`, call `localhost:5000/api/chat`. RAG happens automatically.
</details>

---

**Way 2 — Function Wrapper (Inside your own Python code)**

<details>
<summary><b>Sample code — Function Wrapper (Click to view)</b></summary>

If you're writing your own Python app, just wrap the function that calls the LLM:

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

```python
# NORMALLY:
def ask_llm(prompt):
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": prompt
    }).json()["response"]

# WITH RETRIEVAL:
def ask_llm_with_rag(prompt):
    # Step 1: retrieve context
    context = search_relevant_chunks(prompt)  # the function you already wrote
    
    # Step 2: merge context into the prompt
    augmented = f"Context:\n{chr(10).join(context)}\n\nQuestion: {prompt}"
    
    # Step 3: call the LLM with the augmented prompt
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": augmented
    }).json()["response"]

# Use it the same way:
print(ask_llm_with_rag("Does health insurance cover heart disease?"))
```

</details>
</details>

---

**Way 3 — Open WebUI (No coding required)**

If you're using [Open WebUI](https://openwebui.com/), it already has this mechanism built in:

```
Settings → Documents → Upload file → 
When chatting: @mention that file → automatic RAG
```

Or use Open WebUI's **Pipeline** feature to write filter middleware.

---

**Way 4 — LangChain / LlamaIndex (Professional frameworks)**

<details>
<summary><b>Sample code — LangChain (Click to view)</b></summary>

```python
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load the existing vector DB
vector_store = Chroma(
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chroma_db"
)

# Create the chain: automatic retrieve + augment + generate
qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model="gemma3:12b"),
    retriever=vector_store.as_retriever(),
    chain_type="stuff"  # stuff = stuffs the context into the prompt
)

# Use it: automatically runs retrieve → augment → LLM
result = qa_chain.invoke("Does health insurance cover heart disease?")
print(result)
```
</details>

---

**To summarize: You just need to pick one of the 4 ways:**

| Way | When to use | Difficulty |
|------|-------------|--------|
| **Proxy server** | Any chat app (web, mobile, desktop) | ⭐⭐ |
| **Function wrapper** | Your own Python code | ⭐ |
| **Open WebUI** | Already using Open WebUI | ⭐ (no code) |
| **LangChain/LlamaIndex** | Production, needs many features | ⭐⭐⭐ |

<br>

> **📌 Key Concepts:**
> - **Semantic Search** understands meaning, not just keyword matching
> - **Vector Embedding** turns text into a sequence of numbers (a vector) that computers can compare
> - **Similarity** measures the distance between vectors in a multi-dimensional space
> - **Chunking** splits documents into smaller pieces before embedding
> - **Vector Database** stores and retrieves vectors quickly

---

### 5.4. Guardrails - "The Immune System"

**Purpose**: Prevent unwanted behavior

**Types of Guardrails:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface GuardrailSystem {
  // Input Guardrails
  inputGuardrails: {
    contentFilter: (input: string) => ValidationResult;
    promptInjectionDetection: (input: string) => boolean;
    rateLimiting: RateLimiter;
  };
  
  // Output Guardrails
  outputGuardrails: {
    sensitiveDataDetection: (output: string) => boolean;
    toxicityFilter: (output: string) => ToxicityScore;
    factualityCheck: (output: string) => Promise<boolean>;
  };
  
  // Behavioral Guardrails
  behavioralGuardrails: {
    maxIterations: number;
    timeoutMs: number;
    allowedDomains: string[];
    forbiddenActions: string[];
  };
  
  // Security Guardrails
  securityGuardrails: {
    sandboxing: boolean;
    fileAccessControl: AccessControl;
    networkRestrictions: NetworkPolicy;
  };
}
```

</details>

**Implementation Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class GuardrailLayer {
  async validateInput(input: string): Promise<ValidationResult> {
    // Check for prompt injection
    if (this.detectPromptInjection(input)) {
      return { valid: false, reason: 'Prompt injection detected' };
    }
    
    // Check for inappropriate content
    const toxicity = await this.checkToxicity(input);
    if (toxicity.score > 0.8) {
      return { valid: false, reason: 'Inappropriate content' };
    }
    
    return { valid: true };
  }
  
  async validateOutput(output: string): Promise<ValidationResult> {
    // Check for sensitive data leaks
    if (this.containsSensitiveData(output)) {
      return { valid: false, reason: 'Sensitive data detected' };
    }
    
    // Check output quality
    if (!this.meetsQualityStandards(output)) {
      return { valid: false, reason: 'Quality check failed' };
    }
    
    return { valid: true };
  }
  
  private detectPromptInjection(input: string): boolean {
    const patterns = [
      /ignore previous instructions/i,
      /system prompt/i,
      /you are now/i,
      // ... more patterns
    ];
    return patterns.some(p => p.test(input));
  }
}
```

</details>

---

### 5.5. Feedback Loops - "Senses"

**Purpose**: Automatically learn and improve from results

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface FeedbackSystem {
  // Automatic feedback
  onSuccess: (task: Task, result: any) => void;
  onError: (task: Task, error: Error) => void;
  onTimeout: (task: Task) => void;
  
  // Metrics tracking
  metrics: {
    successRate: number;
    avgResponseTime: number;
    tokenUsage: number;
    errorTypes: Map<string, number>;
  };
  
  // Auto-optimization
  optimizer: {
    analyzePatterns: () => Insights;
    suggestImprovements: () => Suggestion[];
    autoAdjust: (metric: string) => void;
  };
}
```

</details>

**Example:**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class FeedbackLoop {
  async handleTaskCompletion(task: Task, result: TaskResult) {
    // 1. Log metrics
    await this.logMetrics({
      taskType: task.type,
      duration: result.duration,
      tokensUsed: result.tokensUsed,
      success: result.success
    });
    
    // 2. Analyze for patterns
    if (result.success) {
      await this.memory.longTerm.add(
        `Successful ${task.type}: ${result.approach}`,
        { type: 'success_pattern', task: task.type }
      );
    } else {
      await this.memory.longTerm.add(
        `Failed ${task.type}: ${result.error}`,
        { type: 'failure_pattern', task: task.type }
      );
    }
    
    // 3. Auto-adjust if needed
    if (this.metrics.successRate < 0.7) {
      await this.optimizer.suggestImprovements();
    }
  }
}
```

</details>

---

### 5.6. Permissions - "The Skeleton"

**Purpose**: Define what the AI is allowed to do, where, and when

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
interface PermissionSystem {
  // Resource permissions
  resources: {
    files: FilePermissions;
    network: NetworkPermissions;
    system: SystemPermissions;
  };
  
  // Time-based permissions
  temporal: {
    allowedHours: TimeRange[];
    maxDuration: number;
  };
  
  // Context-based permissions
  contextual: {
    requireApproval: (action: Action) => boolean;
    escalationRules: EscalationRule[];
  };
}

interface FilePermissions {
  read: string[];      // Allowed paths to read
  write: string[];     // Allowed paths to write
  delete: string[];    // Allowed paths to delete
  maxFileSize: number; // Max file size in bytes
}
```

</details>

---

### 5.7. Orchestration - "The Nervous System"

**Purpose**: Coordinate all components to work in harmony

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class HarnessOrchestrator {
  async execute(userRequest: string): Promise<Result> {
    // 1. Validate input
    const inputCheck = await this.guardrails.validateInput(userRequest);
    if (!inputCheck.valid) {
      return { error: inputCheck.reason };
    }
    
    // 2. Build context
    const context = await this.contextManager.buildContext(userRequest);
    
    // 3. Check permissions
    const action = await this.planner.plan(userRequest);
    if (!this.permissions.allows(action)) {
      return { error: 'Permission denied' };
    }
    
    // 4. Execute with tools
    const result = await this.agent.execute(action, context);
    
    // 5. Validate output
    const outputCheck = await this.guardrails.validateOutput(result);
    if (!outputCheck.valid) {
      return await this.retry(action); // Retry logic
    }
    
    // 6. Update memory & feedback
    await this.memory.update(result);
    await this.feedback.log(action, result);
    
    return result;
  }
}
```

</details>

---

### Integrate Everything

<details>
<summary><b>Integrate Everything (Click to expand/collapse)</b></summary>

```typescript
// Complete Harness Example
const harness = new AIHarness({
  model: "claude-3.5-sonnet",
  
  tools: [fileEditor, codeRunner, webSearch],
  
  memory: {
    shortTerm: { maxMessages: 20 },
    longTerm: { vectorStore: chromaDB },
    workingMemory: { maxSize: 10000 }
  },
  
  contextManager: {
    levels: 5,
    optimization: "smart",
    tokenLimit: 100000
  },
  
  guardrails: {
    input: [promptInjectionFilter, toxicityFilter],
    output: [sensitiveDataFilter, qualityChecker],
    behavioral: { maxIterations: 10, timeoutMs: 30000 }
  },
  
  feedback: {
    autoLog: true,
    metricsTracking: true,
    autoOptimize: true
  },
  
  permissions: {
    files: {
      read: ["/project/**"],
      write: ["/project/src/**"],
      delete: []
    },
    network: {
      allowedDomains: ["github.com", "stackoverflow.com"]
    }
  }
});
```

</details>

---

### Integrate Components With Modules in the Repo

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

| Component | Analogies | Modules in the Repo | Description |
|-----------|-----------|-------------------|-------|
| **Tools** | "Hands & feet" | `06-decide-tools-mcp` | Define which tools the AI may use; MCP integration |
| **Memory** | "The brain" | `01-retrieve-memory-knowledge`, `03-update-memory-store` | Remember & retrieve knowledge; update memory |
| **Context Management** | "The circulatory system" | `02-build-context` | Build the appropriate context for each task |
| **Guardrails** | "The immune system" | `05-prompt-builder`, `11-evaluation` | Protective barriers; input/output checks |
| **Feedback Loops** | "Senses" | `07-workflow`, `11-evaluation` | Feedback loops, retries, quality evaluation |
| **Permissions** | "The skeleton" | `06-decide-tools-mcp`, `10-automation` | Grant resource access permissions |
| **Orchestration** | "The nervous system" | `07-workflow`, `09-multi-agent`, `04-plan-decompose-task`, `08-task` | Coordinate all components to work in harmony |

> **Insight**: Prompt Engineering (`05-prompt-builder`) is not a separate component of the Harness — it is a **foundational technique** woven throughout many components: System Prompts in Orchestration, Few-shot in Context Management, Structured Output in Guardrails.

---

## 🔭 Overview: Harness Engineering — AI Coding Skills Framework

### Overall Architecture: 7 Components → 12 Modules

The diagram below shows the **entire Harness Engineering system** and how it maps to the **12 modules** in the AI Coding Skills Framework:

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║         AI CODING SKILLS FRAMEWORK — HARNESS ENGINEERING AT A GLANCE                 ║
║                  Architecture Overview: 7 Components → 12 Modules                    ║
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
 │  │                   │  │ detection       │  │ 12-loop-eng      │                   │
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
 │                         │  │ Execution Permissions          │ │                        │
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

 ┌─────────────────────────────────────────────────────────────────────────────────┐
 │                                                                                 │
 │  01  ── retrieve-memory-knowledge    (Retrieve & Memory — RAG Pipeline)        │
 │  02  ── build-context                 (Context Management — 5 levels)          │
 │  03  ── update-memory-store           (Memory Update — store new knowledge)    │
 │  04  ── plan-decompose-task           (Planning — break down tasks)            │
 │  05  ── prompt-builder                (Prompt + Guardrails)                    │
 │  06  ── decide-tools-mcp              (Tools + Permissions + MCP)              │
 │  07  ── workflow                      (Workflow + Feedback Loops)              │
 │  08  ── task                          (Task Management)                         │
 │  09  ── multi-agent                   (Agent Orchestration)                     │
 │  10  ── automation                    (Automation + Access Control)             │
 │  11  ── evaluation                    (Evaluation + Metrics + Guardrails)      │
 │  12  ── loop-engineering              (Continuous Improvement Loop)            │
 │                                                                                 │
 └─────────────────────────────────────────────────────────────────────────────────┘

 ══════════════════════════════════════════════════════════════════════════════════

 RELATIONSHIP ANALYSIS:
 - Harness ≈ THE ENTIRE outer frame (including the 7 components)
 - RAG Pipeline (01) ≈ part of the MEMORY component — the "brain" element
 - 12 modules ≈ 12 concrete skills; each module serves 1+ harness components
 - Prompt Engineering (05) ≈ a foundational technique, woven through many components

 PER-MODULE COVERAGE RATIO IN THE HARNESS:
 ┌─────────────────────────────────────────────────────────────────────────┐
 │  01-retrieve-memory     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  85%   │
 │  02-build-context       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
 │  03-update-memory       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░  50%   │
 │  04-plan-decompose      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░  55%   │
 │  05-prompt-builder      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  60%   │
 │  06-decide-tools        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  75%   │
 │  07-workflow            ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░  80%   │
 │  08-task                ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░  45%   │
 │  09-multi-agent         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░  65%   │
 │  10-automation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░  40%   │
 │  11-evaluation          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  70%   │
 │  12-loop-engineering    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░  60%   │
 └─────────────────────────────────────────────────────────────────────────┘

**In summary:**
| Aspect | RAG Pipeline (01) | Harness Engineering (whole) |
|-----------|-------------------|-------------------------------|
| **Scope** | 1 technique: retrieve + augment | 7 components, 12 modules |
| **Role** | Provide knowledge to the LLM | Control everything the AI can do |
| **Coverage** | ~85% of the Memory component | 100% of the whole system |
| **Relation** | Part of Memory | The whole that contains RAG |

---

## 6. Real-World Case Studies

The case studies below show how leading organizations apply Harness Engineering to achieve outstanding results.

---

### 6.1. SWE-agent (Princeton NLP)

**Context**: Princeton NLP developed an AI agent to automatically fix GitHub issues.

**Initial problems**:
- Success rate was only 12.5% with the baseline approach
- The agent often "got lost" in the codebase
- Search results were too many, causing overwhelm
- No way to tell what information was important

**Harness Engineering solution**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

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

---

### 6.2. Anthropic Multi-Agent Architecture

**Context**: Anthropic developed Claude Code to build complex applications (games, DAWs, etc.)

**Initial problems**:
- A single agent doing too much at once → overwhelmed
- The agent stopped too early (before finishing)
- Or continued too long (didn't know when to stop)

**Solution: Multi-Agent Orchestration**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// 3-Agent Architecture
class MultiAgentHarness {
  agents = {
    planner: new PlannerAgent(),
    generator: new GeneratorAgent(),
    evaluator: new EvaluatorAgent()
  };
  
  async execute(task: string): Promise<Result> {
    // 1. PLANNER: Plan
    const plan = await this.agents.planner.createPlan(task);
    /*
    Output example:
    {
      steps: [
        "1. Create game canvas",
        "2. Implement player movement",
        "3. Add collision detection",
        "4. Implement scoring system"
      ],
      estimatedComplexity: "medium"
    }
    */
    
    // 2. GENERATOR: Execute each step
    const results = [];
    for (const step of plan.steps) {
      const result = await this.agents.generator.generate(step);
      results.push(result);
      
      // 3. EVALUATOR: Evaluate after each step
      const evaluation = await this.agents.evaluator.evaluate(result, step);
      
      if (!evaluation.passed) {
        // Retry with feedback
        const retry = await this.agents.generator.generate(
          step,
          { previousAttempt: result, feedback: evaluation.feedback }
        );
        results[results.length - 1] = retry;
      }
    }
    
    // 4. FINAL EVALUATION
    const finalEval = await this.agents.evaluator.evaluateFinal(results);
    
    return {
      success: finalEval.passed,
      output: results,
      quality: finalEval.quality
    };
  }
}
```

</details>

**Characteristics of each Agent**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
// PLANNER AGENT
class PlannerAgent {
  systemPrompt = `
    You are a planning specialist.
    Break down complex tasks into clear, actionable steps.
    Consider dependencies and order.
    Output: JSON with steps array.
  `;
  
  tools = []; // No tools, pure planning
}

// GENERATOR AGENT
class GeneratorAgent {
  systemPrompt = `
    You are a code generator.
    Implement exactly what is asked in the step.
    Use provided tools to write and test code.
  `;
  
  tools = [
    writeFile,
    readFile,
    executeCode,
    installPackage
  ];
}

// EVALUATOR AGENT
class EvaluatorAgent {
  systemPrompt = `
    You are a quality evaluator.
    Check if the implementation meets requirements.
    Test for bugs, edge cases, and completeness.
    Decide: PASS or FAIL with specific feedback.
  `;
  
  tools = [
    runTests,
    checkSyntax,
    analyzeCode
  ];
}
```

</details>

**Results**:
- Able to build complex applications: 2D games, DAW (Digital Audio Workstation)
- Success rate 80% higher than a single-agent setup
- Better code quality thanks to the evaluation loop

**Key Insights**:
> "Divide and conquer - Each agent focuses on one specific task"

---

### 6.3. Claude Code Leak - A Superlative Harness System

**Context**: In 2026, the source code of Claude Code was accidentally leaked, revealing an extraordinarily sophisticated harness architecture.

**Key findings**:

#### A. 5-Level Context Management

<details>
<summary><b>A. 5-Level Context Management (Click to expand/collapse)</b></summary>

```typescript
class ClaudeContextManager {
  buildContext(query: string): Context {
    return {
      // Level 1: System Identity
      system: {
        role: "AI Coding Assistant",
        version: "Claude 3.5",
        capabilities: [...],
        limitations: [...]
      },
      
      // Level 2: Task Context
      task: {
        currentGoal: this.getCurrentGoal(),
        progressSoFar: this.getProgress(),
        remainingSteps: this.getRemainingSteps()
      },
      
      // Level 3: Domain Knowledge (Codebase)
      domain: {
        projectStructure: this.getProjectStructure(),
        conventions: this.getCodeConventions(),
        dependencies: this.getDependencies()
      },
      
      // Level 4: Conversation History (Compressed)
      conversation: {
        recentMessages: this.getRecentMessages(10),
        summary: this.getSummary(),
        keyDecisions: this.getKeyDecisions()
      },
      
      // Level 5: Immediate Context
      immediate: {
        currentFile: this.getCurrentFile(),
        openFiles: this.getOpenFiles(),
        recentEdits: this.getRecentEdits(),
        cursorPosition: this.getCursorPosition()
      }
    };
  }
}
```

</details>

#### B. 3-Tier Memory with Auto-Optimization

<details>
<summary><b>B. 3-Tier Memory with Auto-Optimization (Click to expand/collapse)</b></summary>

```typescript
class ClaudeMemorySystem {
  // Tier 1: Hot Memory (RAM)
  hotMemory = {
    currentConversation: [],
    maxSize: 20,
    // Automatically compress when full
    autoCompress: true
  };
  
  // Tier 2: Warm Memory (Vector DB)
  warmMemory = {
    vectorStore: new ChromaDB(),
    recentQueries: new LRUCache(100),
    // Cache frequent queries
    queryCache: new Map()
  };
  
  // Tier 3: Cold Memory (Long-term Storage)
  coldMemory = {
    database: new PostgreSQL(),
    // Store long-term patterns and learnings
    successPatterns: [],
    failurePatterns: []
  };
  
  // AUTO DREAM: run in the background to optimize memory
  async autoDream() {
    // Run during idle time
    setInterval(async () => {
      // 1. Analyze patterns
      const patterns = await this.analyzePatterns();
      
      // 2. Move rarely used items to cold storage
      await this.archiveOldMemories();
      
      // 3. Optimize vector embeddings
      await this.warmMemory.vectorStore.optimize();
      
      // 4. Update the query cache
      await this.updateQueryCache();
    }, 60000); // Every minute
  }
}
```

</details>

#### C. Strict Tool Permissions

<details>
<summary><b>C. Strict Tool Permissions (Click to expand/collapse)</b></summary>

```typescript
class ClaudeToolPermissions {
  // Each tool has its own permissions
  toolPermissions = {
    'read_file': {
      allowedPaths: ['/workspace/**'],
      deniedPaths: ['/workspace/.env', '/workspace/secrets/**'],
      requireApproval: false
    },
    
    'write_file': {
      allowedPaths: ['/workspace/src/**', '/workspace/test/**'],
      deniedPaths: ['/workspace/config/**'],
      requireApproval: true, // Requires user confirmation
      maxFileSize: 100000 // 100KB
    },
    
    'execute_command': {
      allowedCommands: ['npm', 'git', 'python', 'node'],
      deniedCommands: ['rm -rf', 'sudo', 'chmod'],
      requireApproval: true,
      timeout: 30000 // 30s
    },
    
    'web_search': {
      allowedDomains: ['github.com', 'stackoverflow.com', 'docs.*'],
      rateLimitperHour: 50
    }
  };
  
  async checkPermission(tool: string, params: any): Promise<PermissionResult> {
    const perm = this.toolPermissions[tool];
    
    // Check path restrictions
    if (tool.includes('file')) {
      if (!this.isPathAllowed(params.path, perm)) {
        return { allowed: false, reason: 'Path not allowed' };
      }
    }
    
    // Check if approval is needed
    if (perm.requireApproval) {
      const approved = await this.requestUserApproval(tool, params);
      if (!approved) {
        return { allowed: false, reason: 'User denied' };
      }
    }
    
    return { allowed: true };
  }
}
```

</details>

#### D. Tone Detection with Regex (!)

<details>
<summary><b>D. Tone Detection with Regex (!) (Click to expand/collapse)</b></summary>

```typescript
class ClaudeToneDetector {
  // Detect user frustration/dissatisfaction
  frustrationPatterns = [
    /why (is|are) (you|this)/i,
    /stop doing/i,
    /i (told|said) you/i,
    /for the (\d+)(st|nd|rd|th) time/i,
    /just do it/i,
    /seriously\?/i
  ];
  
  detectFrustration(message: string): boolean {
    return this.frustrationPatterns.some(p => p.test(message));
  }
  
  adjustTone(message: string): ToneAdjustment {
    if (this.detectFrustration(message)) {
      return {
        tone: 'apologetic',
        verbosity: 'concise',
        explanation: 'minimal',
        action: 'immediate' // Act now, explain later
      };
    }
    
    return {
      tone: 'helpful',
      verbosity: 'balanced',
      explanation: 'detailed',
      action: 'thoughtful'
    };
  }
}
```

</details>

**Results**:
- Claude Code became one of the best AI coding assistants
- User satisfaction rate > 90%
- High retention rate

**Key Insights**:
> "The devil is in the details - Every small detail in the harness is carefully optimized"

---

### 6.4. Cursor IDE - Harness Optimized for Coding

**Notable features**:

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
class CursorHarness {
  // 1. CONTEXT AWARE - Knows what you're working on
  async buildContext(): Promise<Context> {
    return {
      // Currently open file
      currentFile: editor.getCurrentFile(),
      
      // Currently selected code
      selectedCode: editor.getSelection(),
      
      // Cursor position
      cursorLine: editor.getCursorLine(),
      
      // Recent edits (to understand intent)
      recentEdits: this.getRecentEdits(5),
      
      // Related files (import/export)
      relatedFiles: await this.findRelatedFiles(),
      
      // Git context
      gitBranch: await git.getCurrentBranch(),
      uncommittedChanges: await git.getUncommittedChanges()
    };
  }
  
  // 2. SMART SUGGESTIONS
  async getSuggestions(context: Context): Promise<Suggestion[]> {
    // Based on context, provide fitting suggestions
    const suggestions = [];
    
    if (context.selectedCode) {
      suggestions.push({
        type: 'refactor',
        action: 'Refactor this code',
        confidence: 0.9
      });
      
      suggestions.push({
        type: 'explain',
        action: 'Explain this code',
        confidence: 0.95
      });
    }
    
    if (context.cursorLine.includes('TODO')) {
      suggestions.push({
        type: 'implement',
        action: 'Implement this TODO',
        confidence: 0.85
      });
    }
    
    return suggestions.sort((a, b) => b.confidence - a.confidence);
  }
  
  // 3. INCREMENTAL EDITS
  async applyEdit(edit: Edit): Promise<void> {
    // Don't replace the whole file
    // Only change what's necessary
    await editor.replaceRange(
      edit.startLine,
      edit.endLine,
      edit.newContent
    );
    
    // Auto format
    await editor.formatDocument();
    
    // Run the linter
    const lintResult = await linter.check();
    if (lintResult.errors.length > 0) {
      // Show inline errors
      editor.showErrors(lintResult.errors);
    }
  }
}
```

</details>

**Results**:
- Became the most beloved coding assistant
- NPS (Net Promoter Score) > 70
- Many developers switched from GitHub Copilot to Cursor

---

### 6.5. DeepSeek Harness — Micro-Kernel & Trajectory Traceability Framework

The DeepSeek Harness represents a highly extensible generation of AI Agent Harnesses built on the philosophy of **"Agent = Model + Harness"** and **"Everything is a Plugin"**. Built on the Cordis micro-kernel foundation, DeepSeek Harness turns every part of the agent (tools, context, memory, sub-agents) into independent plugins that can be attached and detached flexibly.

#### A. Micro-Kernel & Ecosystem Plugin Architecture
- **Cordis Core Framework**: Manages the plugin lifecycle through 4 stages (`init`, `attach`, `ready`, `detach`).
- **Context Service Registry**: Uses `ctx.provide()` and `ctx.inject()` to let plugins register and consume services independently (such as logger, llmProvider, memoryStore).
- **See detailed guide**: [`harness/07-workflow/cordis-kernel-plugin.md`](./harness/07-workflow/cordis-kernel-plugin.md)

#### B. 4 Specialized Runtime Modes
DeepSeek Harness designs 4 dedicated execution environments suited to every need:
1. **Standard Mode**: A full-featured interactive CLI/GUI agent with complete MCP tools and middleware guardrails.
2. **Code Mode**: Runs through the SDK (`@deepseek-ai/dsh`), batching many tool calls into a single code scenario, reducing latency and token cost by 70-90%.
3. **Minimal Benchmark Mode**: A minimal environment with just 2 tools (`bash`, `editor`) and a minimal prompt, to evaluate the LLM's native reasoning ability.
4. **Creator Inspector Mode**: A runtime that visualizes the timeline, allowing inspection of context state and editing of preset agents.

#### C. Trajectory Traceability Engine (Session Event Stream & Branching)
- **Append-Only Event Log**: Every session development (Prompt, Reason, Tool Call, Output) is stored as an immutable sequence of events (`SessionEventStream`).
- **Time-Travel Replay & Forking**: The ability to "pause" the session at any step, restore context state (`replayToStep`), and branch off (`forkSession`) to experiment with a different solution without breaking the original session.
- **See detailed guide**: [`harness/03-update-memory-store/trajectory-fork-replay.md`](./harness/03-update-memory-store/trajectory-fork-replay.md)

#### D. Code Mode SDK & Sandboxed Execution
- Addresses the latency weakness of traditional multi-turn tool calling. The LLM identifies complex scenarios and generates TypeScript/Python code that calls the `@deepseek-ai/dsh` SDK.
- The scenario runs inside a safe Node.js `vm` sandbox, executing dozens of read/write/build operations in a single turn.
- **See detailed guide**: [`harness/06-decide-tools-mcp/code-mode-sdk.md`](./harness/06-decide-tools-mcp/code-mode-sdk.md)

#### E. Minimal Benchmark Harness for AI Capability Evaluation
- Fully isolates noise from complex frameworks. Enables running benchmarks (such as SWE-bench) with high accuracy and absolute repeatability.
- **See detailed guide**: [`harness/11-evaluation/minimal-benchmark-harness.md`](./harness/11-evaluation/minimal-benchmark-harness.md)

---

### Common Lessons From the Case Studies

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

**Common principles**:
1. ✅ **Constraints enable creativity** - Limits help the AI focus
2. ✅ **Layered architecture** - Break the problem into smaller pieces
3. ✅ **Feedback loops** - Learn from results
4. ✅ **User-centric design** - Always think about UX
5. ✅ **Obsess over details** - Every detail matters

---

## 7. Harness Design Principles

### 7.1. SOLID Principles for Harness

**1. Single Responsibility**
- Each tool does exactly one thing
- Each component has one reason to change

**2. Open/Closed**
- The harness is open for extension (adding tools, guardrails)
- Closed for modification (core logic stays stable)

**3. Liskov Substitution**
- Tools can substitute for one another
- Same interface, different implementation

**4. Interface Segregation**
- Don't force the AI to use tools it doesn't need
- Only expose what's necessary

**5. Dependency Inversion**
- Depend on abstractions, not implementations
- Makes swapping components easy

---

### 7.2. The 10 Commandments of Harness Engineering

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

---

### 7.3. The Harness Design Pattern

<details>
<summary><b>7.3. The Harness Design Pattern (Click to expand/collapse)</b></summary>

```typescript
// Template for designing any harness
class HarnessDesignPattern {
  // 1. Define what AI CAN do
  defineCapabilities() {
    return {
      tools: [...],
      permissions: {...}
    };
  }
  
  // 2. Define what AI CANNOT do
  defineConstraints() {
    return {
      guardrails: [...],
      validators: [...]
    };
  }
  
  // 3. Define what AI SHOULD remember
  defineMemory() {
    return {
      shortTerm: {...},
      longTerm: {...},
      working: {...}
    };
  }
  
  // 4. Define how AI SHOULD learn
  defineFeedback() {
    return {
      onSuccess: () => {},
      onError: () => {},
      metrics: [...]
    };
  }
  
  // 5. Define how components WORK TOGETHER
  defineOrchestration() {
    return {
      workflow: [...],
      errorHandling: {...}
    };
  }
}
```

</details>

---

## 8. Best Practices

### 8.1. Tool Design

✅ **DO:**
- Keep tools small and focused
- Validate inputs and outputs
- Provide clear error messages
- Make tools idempotent when possible
- Include examples in descriptions

❌ **DON'T:**
- Create "god tools" that do everything
- Trust AI to validate itself
- Use vague error messages
- Allow destructive operations without confirmation

### 8.2. Memory Management

✅ **DO:**
- Compress context regularly
- Prioritize relevant information
- Clear working memory after tasks
- Use tiered storage (hot/warm/cold)

❌ **DON'T:**
- Keep entire conversation history
- Load unnecessary data
- Mix different types of memory
- Forget to clean up

### 8.3. Context Building

✅ **DO:**
- Layer context by priority
- Include only relevant information
- Monitor token usage
- Compress when approaching limits

❌ **DON'T:**
- Include everything
- Ignore token limits
- Use static context
- Forget immediate context

### 8.4. Guardrails

✅ **DO:**
- Validate at multiple layers
- Check both input and output
- Fail fast and clearly
- Log all violations

❌ **DON'T:**
- Rely only on prompts
- Skip validation steps
- Hide errors from users
- Trust without verifying

### 8.5. Testing the Harness

<details>
<summary><b>8.5. Testing the Harness (Click to expand/collapse)</b></summary>

```typescript
// Test suite for the harness
describe('Harness Tests', () => {
  test('Tool validation works', async () => {
    const result = await harness.executeTool('write_file', {
      path: '/unsafe/path'
    });
    expect(result.error).toBe('Path not allowed');
  });
  
  test('Context limits respected', async () => {
    const context = await harness.buildContext(largeQuery);
    const tokens = countTokens(context);
    expect(tokens).toBeLessThan(100000);
  });
  
  test('Guardrails catch sensitive data', async () => {
    const output = "API_KEY=sk_12345";
    const validation = await harness.validateOutput(output);
    expect(validation.valid).toBe(false);
  });
  
  test('Memory compression works', async () => {
    // Add 50 messages
    for (let i = 0; i < 50; i++) {
      await harness.addMessage({ content: `Message ${i}` });
    }
    expect(harness.memory.shortTerm.messages.length).toBeLessThan(25);
  });
});
```

</details>

---

## 9. Tools & Frameworks

### 9.1. Popular Frameworks

**LangChain / LangGraph**

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { DynamicStructuredTool } from "@langchain/core/tools";

const harness = {
  llm: new ChatOpenAI({ model: "gpt-4" }),
  tools: [
    new DynamicStructuredTool({
      name: "search",
      description: "Search the web",
      func: async (input) => { /* ... */ }
    })
  ]
};
```

</details>

**AutoGen (Microsoft)**

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"},
    system_message="You are a helpful assistant"
)

harness = UserProxyAgent(
    name="harness",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "coding"}
)
```

</details>

**CrewAI**

<details>
<summary><b>Python Code (Click to expand/collapse)</b></summary>

```python
from crewai import Agent, Task, Crew

# Multi-agent harness
planner = Agent(role='Planner', goal='Create plan')
executor = Agent(role='Executor', goal='Execute plan')
reviewer = Agent(role='Reviewer', goal='Review output')

harness = Crew(
    agents=[planner, executor, reviewer],
    tasks=[plan_task, execute_task, review_task]
)
```

</details>

---

### 9.2. Supporting Tools

**Vector Databases:**
- Pinecone
- Chroma
- Weaviate
- Qdrant

**Monitoring & Logging:**
- LangSmith
- Weights & Biases
- Helicone
- OpenLLMetry

**Guardrails:**
- Guardrails AI
- NeMo Guardrails (NVIDIA)
- LlamaGuard (Meta)

**Testing:**
- PromptFoo
- Deepeval
- Ragas

---

### 9.3. Starter Template

<details>
<summary><b>9.3. Starter Template (Click to expand/collapse)</b></summary>

```typescript
// Complete starter template
import { ChatAnthropic } from "@langchain/anthropic";
import { ChromaDB } from "chromadb";

class ProductionHarness {
  constructor(config) {
    this.model = new ChatAnthropic({
      model: "claude-3.5-sonnet",
      temperature: 0
    });
    
    this.tools = this.initializeTools();
    this.memory = this.initializeMemory();
    this.guardrails = this.initializeGuardrails();
    this.logger = this.initializeLogger();
  }
  
  async execute(userInput) {
    try {
      // 1. Validate input
      await this.guardrails.validateInput(userInput);
      
      // 2. Build context
      const context = await this.buildContext(userInput);
      
      // 3. Execute with tools
      const result = await this.model.invoke(context, {
        tools: this.tools
      });
      
      // 4. Validate output
      await this.guardrails.validateOutput(result);
      
      // 5. Log metrics
      await this.logger.log({
        input: userInput,
        output: result,
        tokens: result.usage
      });
      
      return result;
    } catch (error) {
      await this.handleError(error);
      throw error;
    }
  }
}

// Usage
const harness = new ProductionHarness({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const result = await harness.execute("Build me a todo app");
```

</details>

---

## 10. The Future of Harness Engineering

### 10.1. Trends 2026-2028

**1. Self-Optimizing Harnesses**
- Harnesses automatically adjust their parameters
- Automated A/B testing
- Continuous learning from usage

**2. Harness-as-a-Service**
- Cloud platforms offering pre-built harnesses
- Plug-and-play harness components
- Marketplaces for harness templates

**3. Visual Harness Builders**
- No-code tools for designing harnesses
- Visual workflow editors
- Drag-and-drop tool composition

**4. Cross-Model Harnesses**
- One harness running on multiple models
- Automatic model switching based on the task
- Cost-optimized model routing

**5. Regulatory Compliance Harnesses**
- Built-in GDPR, HIPAA compliance
- Automated audit trails
- Explainability baked in

---

### 10.2. Challenges Ahead

**Technical Challenges:**
- Standardization across platforms
- Interoperability between harnesses
- Performance optimization at scale
- Security and privacy

**Business Challenges:**
- ROI measurement
- Team skill gaps
- Legacy system integration
- Changing regulations

**Research Challenges:**
- Optimal harness architecture patterns
- Automated harness generation
- Harness testing methodologies
- Cross-domain transferability

---

### 10.3. Advice for the Future

```
1. Start Simple
   → Don't over-engineer from the start
   → Build an MVP harness first

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

---

## 11. Reference Materials

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

### Frameworks & Tools

1. **LangChain** - https://langchain.com
2. **LangGraph** - https://langchain-ai.github.io/langgraph/
3. **AutoGen** - https://microsoft.github.io/autogen/
4. **CrewAI** - https://www.crewai.com
5. **Guardrails AI** - https://www.guardrailsai.com

### Communities

1. **LangChain Discord** - Active community
2. **r/LangChain** - Reddit discussions
3. **AI Engineers** - Slack community
4. **HuggingFace Forums** - Technical discussions

### Blogs & Resources

1. **Anthropic Blog** - https://www.anthropic.com/news
2. **OpenAI Cookbook** - https://cookbook.openai.com
3. **LangChain Blog** - https://blog.langchain.dev
4. **Mitchell Hashimoto's Blog** - https://mitchellh.com

### Courses & Tutorials

1. **DeepLearning.AI - Building AI Agents**
2. **LangChain Academy**
3. **Anthropic Prompt Engineering**
4. **Microsoft AutoGen Tutorial**

---

**Conclusion**

Harness Engineering is not just a technology trend - it is a paradigm shift in how we build AI applications. As AI models become increasingly powerful and turn into "commodities", the ability to design a good harness will be the deciding factor for success.

> **"The model thinks. The harness shapes what it thinks about. And the harness determines the quality of the final output."**

Start today - you don't need perfection, you just need to begin. Build, measure, learn, and iterate. Harness Engineering is a journey, not a destination.

**Happy Building! 🚀**

---

**Last updated:** 13/07/2026  
**Author:** AI Knowledge Repository
