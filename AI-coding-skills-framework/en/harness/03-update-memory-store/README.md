# 💾 III. Update Memory & Knowledge Store

> ## 📑 Contents
>
> - [Overview](#overview)
> - [Why Is Update Memory & Knowledge Store Important?](#why-is-update-memory-&-knowledge-store-important)
> - [Content](#content)
> - [1. Write-back Memory](#1-write-back-memory)
>   - [1.1 When Is Write-back Needed?](#11-when-is-write-back-needed)
>   - [1.2 Write-back Implementation](#12-write-back-implementation)
> - [2. Memory Consolidation](#2-memory-consolidation)
>   - [2.1 What Is Consolidation?](#21-what-is-consolidation)
>   - [2.2 Implementation](#22-implementation)
> - [3. Report Generation](#3-report-generation)
>   - [3.1 Report Types](#31-report-types)
>   - [3.2 Implementation](#32-implementation)
> - [4. KB Maintenance](#4-kb-maintenance)
>   - [4.1 Knowledge Base Operations](#41-knowledge-base-operations)
> - [5. Event Sourcing Pattern](#5-event-sourcing-pattern)
>   - [5.1 Concept](#51-concept)
>   - [5.2 Implementation](#52-implementation)
> - [6. Memory Store Case Studies](#6-memory-store-case-studies)
>   - [6.1. Claude Code — Session Memory & Cross-Session Persistence](#61-claude-code--session-memory-&-cross-session-persistence)
>   - [6.2. Mem0 — Production Memory Layer for AI Agents](#62-mem0--production-memory-layer-for-ai-agents)
>   - [6.3. OpenMemory — MCP-Based Memory Server](#63-openmemory--mcp-based-memory-server)
>   - [6.4. DeepSeek Harness — Trajectory Fork & Replay Engine](#64-deepseek-harness--trajectory-fork-&-replay-engine)
> - [7. Advanced Memory Patterns](#7-advanced-memory-patterns)
>   - [7.1. Write-Behind Cache Pattern](#71-write-behind-cache-pattern)
>   - [7.2. Memory Consolidation Pipeline](#72-memory-consolidation-pipeline)
>   - [7.3. Versioned Memory (Git-like Memory)](#73-versioned-memory-git-like-memory)
> - [8. Best Practices & Anti-Patterns](#8-best-practices-&-anti-patterns)
> - [9. Performance Metrics](#9-performance-metrics)
> - [10. Hands-on Labs](#10-hands-on-labs)
>   - [Lab 1: Write-back Memory](#lab-1-write-back-memory)
>   - [Lab 2: Consolidation](#lab-2-consolidation)
>   - [Lab 3: Versioned Memory](#lab-3-versioned-memory)
>   - [Lab 4: Metrics](#lab-4-metrics)
> - [11. Reference Materials](#11-reference-materials)
>   - [Papers & Research](#papers-&-research)
>   - [Frameworks & Tools](#frameworks-&-tools)
>   - [Blogs & Resources](#blogs-&-resources)
>
---

### Opening Story

Picture yourself as the keeper of a cozy neighborhood library. Every day, neighbors drop off new books and return old ones. If you **just keep stacking new arrivals** but never reshelve, never toss out torn pages, never refresh the catalog — within a year your beloved library turns into a **dusty storage room** where nobody can find a thing.

**That's exactly what happens to AI memory when it only "takes notes" but never "tidies up".**

An LLM can happily soak up new facts — but without someone to **merge the duplicates** (consolidate), **toss what's expired** (prune), and **reshelve everything neatly** (index), its knowledge grows messier, slower, and less trustworthy by the week. The ending is always the same: the agent repeats old mistakes, quotes expired info, and starts guessing its way through answers.

### Why Is Update Memory Important?

> *"It's not about having a bigger brain — it's about keeping it clean and current."*

#### 3 Pieces of Scientific Evidence

| # | Research | Key Finding |
|---|-----------|----------------------|
| 1 | **Ebbinghaus Forgetting Curve** | Without active reinforcement, **70% of information is forgotten within 24 hours**. Memory write-back helps AI keep knowledge fresh |
| 2 | **Google Research (2024)** | Knowledge bases that are updated regularly reduce the **hallucination rate by 45%** — factual grounding instead of stale training data |
| 3 | **Anthropic (2025)** | Effective memory consolidation leads to **3x fewer repeated mistakes** — the agent remembers what worked and what didn't |

#### Core Philosophy:

```
Update Memory = Learn → Consolidate → Preserve → Evolve
```

**The 4 Phases of Memory Update**:
- **Phase 1: Capture** — Record interactions, decisions, outcomes
- **Phase 2: Consolidate** — Merge new information into existing knowledge (dedup, reconcile)
- **Phase 3: Prune** — Remove outdated, irrelevant, contradictory information
- **Phase 4: Index** — Re-organize so retrieval stays efficient

**Updating memory is just good librarianship.** A good librarian doesn't only stamp new books (Capture) — she reshelves the stacks (Index), recycles the battered copies (Prune), and refreshes the catalog cards (Consolidate). Skip the housekeeping, and the library quietly turns into a storage room.

**Skip it and here's the slow slide**: the collection goes stale → the agent replays old mistakes, hands out expired answers, and guesses when it should know — until users stop trusting it, and then stop showing up.

## Overview

> **📌 Core Concept**
> 
> **Concept:** Write-back is the "write in reverse" direction — alongside reading (retrieving) knowledge, the system also writes back what it has just learned (events, facts, feedback) into the memory store, and only then comes consolidation and report generation.
> 
> **Analogy:** Like a librarian — retrieval is walking to the shelf to take out a book, while write-back is writing the catalog card for a newly purchased book.
> 
> **Why it matters:** If you only "read" without "writing", the AI answers with stale knowledge and every conversation session starts from zero again.

Once the system has looked things up and done its work, it needs to **write what it learned back** into the memory shelves. That's the **write-back** step — freshening up the knowledge base, the memory systems, and turning the session into handy reports.

```
┌──────────────────────────────────────────────────────────────────┐
│                UPDATE MEMORY & KNOWLEDGE STORE                    │
│                                                                  │
│  Retrieve (Read)                 Update (Write)                  │
│  ┌──────────────┐               ┌──────────────────────┐        │
│  │  Vector DB   │◄──────────────│  Write-back Engine   │        │
│  │  Knowledge   │               │  ────────────────────│        │
│  │  Graph       │──────────────►│  - Memory Writer     │        │
│  │  Files/DB    │               │  - Consolidation     │        │
│  └──────────────┘               │  - Report Generator  │        │
│                                 │  - KB Maintenance    │        │
│                                 └──────────────────────┘        │
│                                                                  │
│  Operations:                                                     │
│  ├── Write-back Memory (record new events)                      │
│  ├── Consolidation (merge old + new facts)                      │
│  ├── Report Generation (create structured output)               │
│  └── KB Maintenance (add/modify/delete knowledge)               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Why Is Update Memory & Knowledge Store Important?

> **📌 Core Concept**
> 
> **Concept:** Updating memory is "refreshing" the AI's brain — recording new events, merging duplicate knowledge (consolidation), and removing outdated information so that knowledge is always correct as of the present moment.
> 
> **Analogy:** Like a patient's medical chart — the doctor must not only read the old chart but update it with new test results, otherwise the diagnosis will drift.
> 
> **Why it matters:** Memory that is not updated makes the AI answer with stale knowledge, repeat mistakes already made, and lose the user's trust.

> *"The human brain is not just a storage place — it is a system that constantly reorganizes, connects, and refreshes information. An AI memory system is the same."*

### Core Philosophy

Picture a doctor who keeps every patient's chart by heart. But imagine he only ever **reads** those charts and **never writes in** the new test results — after a year, those charts are just pretty paper. **Looking things up alone isn't enough — writing back is where the real magic happens.**

Three little rules to live by:

1. **Memory is a garden, not a warehouse**: weeds get pulled, plants get watered, beds get rearranged. Even your own brain quietly forgets what's no longer useful — healthy memory does the same.
2. **Every chat is a lesson**: each conversation, each thumbs-up or thumbs-down, each decision leaves behind a nugget of knowledge. Fail to jot it down, and that gold just washes away.
3. **Tidy beats piled-up**: an endless heap of notes is just **noise**. Merging, deduping, and refreshing turns it into **signal** — the good stuff you can actually use.

### Research Evidence

#### Google Research (2024): "Memory-Enhanced Agents"
> Agents with memory write-back score **37% better** on multi-turn tasks than agents that can only look things up.

Why? Without a notebook, the agent forgets what you told it two minutes ago → it asks you the same thing all over again → everybody's time melts away and the experience sours.

#### Anthropic (2025): Claude Code Memory Architecture
Claude Code uses a **3-tier memory system**:
- **Session Memory** (ephemeral): records facts within the current session
- **Project Memory** (persistent): write-back into CLAUDE.md files
- **Global Memory** (cross-project): knowledge transfer between projects

Result: reduced **duplicate questions between sessions by 68%**.

#### IBM Enterprise AI Research (2025)
> Enterprises without memory consolidation spend **2.3x the time** on repetitive tasks because the AI has to "relearn" from scratch each time.

### Cost-Benefit Analysis

| Cost / Value | Without Write-back | With Write-back + Consolidation |
|---|---|---|
| **Duplicate Work** | Agent repeats work it already did | Agent knows what it did, continues from there |
| **Knowledge Drift** | Old facts still exist → drift | Auto-update: new facts replace old facts |
| **Storage Cost** | Grows continuously, uncontrolled | 40-60% reduction through consolidation |
| **Response Quality** | Gradually degrades over time | Continuously improves through the feedback loop |
| **User Trust** | Drops because of repeated information | Rises because the agent "remembers" context |

**Concrete ROI**: invest $500/month in memory infrastructure → save $2,000/month in agent work costs (75% reduction in duplicate queries).

### Illustrative Analogies

**Analogy 1: The Doctor and the Medical Chart**
- **Retrieval** = the doctor opens the patient chart to read it
- **Write-back** = the doctor writes the new test results into the chart
- **Consolidation** = the doctor synthesizes all the tests and updates the diagnosis
- **Without write-back** = the doctor reads the old chart and prescribes wrongly because he doesn't know about the new tests

**Analogy 2: The Librarian and the Library**
- **Retrieval** = finding a book on the shelf
- **Write-back** = buying a new book, updating the catalog
- **Consolidation** = rearranging the shelves, removing outdated books, merging new editions
- **Without consolidation** = the library is full of duplicate books, and finding one title means sifting through 5 copies

**Analogy 3: Git and the Codebase**
- **Write-back** = committing new code
- **Consolidation** = merging branches, resolving conflicts
- **Event Sourcing** = Git history — you can time-travel to any commit
- **Without consolidation** = hundreds of conflicting branches, no one can merge

### Evolutionary Context: From Simple Storage to Intelligent Memory

```
┌──────────────────────────────────────────────────────────────────┐
│                  EVOLUTION OF MEMORY SYSTEMS                      │
│                                                                  │
│  2020-2022: Simple Key-Value Storage                             │
│  └── Memory = cache {key: value}                                 │
│      Problem: not semantic, not temporal                         │
│                                                                  │
│  2022-2023: Vector Store (Embedding-based)                      │
│  └── Memory = vector DB with semantic search                    │
│      Problem: no consolidation, no conflict resolution          │
│                                                                  │
│  2024-2025: Structured Memory Systems                           │
│  └── Memory = Knowledge Graph + Vector + Episodic               │
│      Problem: manual consolidation, no auto-update              │
│                                                                  │
│  2026+: Intelligent Adaptive Memory                              │
│  └── Memory = Auto-consolidation + Conflict Resolution          │
│      + Temporal Awareness + Cross-session Learning              │
│      Solution: memory self-organizes, self-refreshes, self-cleans│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Key insight**: "Storage is cheap, but organization and consolidation are what create value. A vector store of 10,000 documents without consolidation is worse than a well-organized knowledge graph of 100 facts."

### If You Skip Update Memory...

**1. Knowledge Staleness (System Knowledge)**
- Old facts are not updated → the agent answers with wrong new information
- Example: the 2025 tax law changed, but memory still holds the 2024 law

**2. Memory Explosion (Storage Allocation)**
- Only adding, never deleting/merging → storage grows without bound
- Vector search gets slower → performance degrades 30-50% within 6 months

**3. Contradiction Accumulation**
- Contradicting facts accumulate → the agent gets "confused" and answers inconsistently
- Example: "health insurance contribution is 4.5%" and "health insurance contribution is 5%" coexist

**4. Zero Learning (Not Learning from Experience)**
- The agent does not record feedback → repeats similar mistakes
- The user has to give instructions from scratch in every session

**5. Lost Context Between Sessions**
- A new session starts from zero → the user is frustrated at having to repeat information
- No session handoff → another team member doesn't know the prior context

### Best Practices (And Why)

| Rule | Why |
|---|---|
| Always timestamp every fact | To know which fact is the newest when a conflict arises |
| Consolidate periodically (not real-time) | Real-time consolidation costs too much compute; batch processing is 5x more efficient |
| Always log every write operation (audit trail) | To debug when memory gets corrupted; to enable rollback if needed |
| Version facts (with source and confidence) | To resolve conflicts: which fact's source is more trustworthy |
| Auto-expire outdated facts | Facts that are 6 months old have a 73% chance of being outdated (research data) |
| Separate episodic vs semantic memory | Episodic = "what happened", semantic = "what is true" — two kinds of memory need different handling |

---

## Content

| # | Topic | Description |
|---|--------|-------|
| 1 | [Write-back Memory](#1-write-back-memory) | Record new events into the memory systems |
| 2 | [Memory Consolidation](#2-memory-consolidation) | Aggregate & merge information |
| 3 | [Report Generation](#3-report-generation) | Create structured output |
| 4 | [KB Maintenance](#4-kb-maintenance) | Add/modify/delete knowledge base |
| 5 | [Event Sourcing Pattern](#5-event-sourcing-pattern) | Store as an event log |

---

## 1. Write-back Memory

> **📌 Core Concept**
> 
> **Concept:** Write-back Memory is the step that records what the system has just learned — events (episodic), facts (semantic), feedback — into the memory store after processing the conversation.
> 
> **Analogy:** Like taking notes right after a meeting — if you don't write them down, a few hours later you'll have forgotten almost all of it.
> 
> **Why it matters:** If you only retrieve without write-back, the AI never gets "smarter" with each conversation and keeps repeating the same old questions.

### 1.1 When Is Write-back Needed?

Not every new tidbit deserves a spot on the shelf — save the ink for moments that **change something**: the user's situation shifts, the system learns a fresh fact, or a mistake teaches a lesson. Read the three little scenes below like short stories: the first line is what happens in the chat, and the `→` lines are how our trusty librarian reacts.

```
┌──────────────────────────────────────────────────────────────────┐
│                   WRITE-BACK SCENARIOS                            │
│                                                                  │
│  Scenario 1: User learns something new                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ User: "I just switched to freelancing"                   │   │
│  │ → Store: user.occupation = "freelancer"                  │   │
│  │ → Update: Conversation context                           │   │
│  │ → Trigger: Re-classify user needs                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Scenario 2: System discovers new knowledge                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ RAG found: "New 2025 health insurance law: rate +5%"     │   │
│  │ → Update: Knowledge base with new regulation             │   │
│  │ → Invalidate: Cached old health insurance info           │   │
│  │ → Notify: Users affected by change                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Scenario 3: Feedback loop                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ User: "That last answer was wrong!"                      │   │
│  │ → Store: feedback (query, wrong_answer, correct_answer)  │   │
│  │ → Update: Retriever weights                              │   │
│  │ → Improve: Future responses                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Write-back Implementation

Meet the `MemoryWriter` class — the system's trusty **pen**: `write_episodic` jots down events, `write_fact` files away facts, `update_fact` corrects them, and `write_user_profile` refreshes what we know about you. No need to memorize every line — just catch the golden thread: **every method leaves a note in the `event_log` diary**, so you can always retrace who wrote what, and when.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/01-1-2-write-back-implementation.py`](examples/01-1-2-write-back-implementation.py)

</details>
---

## 2. Memory Consolidation

> **📌 Core Concept**
> 
> **Concept:** Consolidation is the "cleaning the warehouse" process — merging duplicate facts, replacing old facts with new ones, and resolving contradictory facts so knowledge stays tidy and accurate.
> 
> **Analogy:** Like periodically organizing your closet — put away duplicate clothes, toss the torn ones, and rearrange everything neatly so next time you can find things quickly.
> 
> **Why it matters:** Uncontrolled knowledge accumulation creates noise, which makes retrieval slow and answers more likely to be wrong.

### 2.1 What Is Consolidation?

The little diagram below walks you through a before-and-after cleanup. Up top: 5 messy, overlapping notes about health-insurance rates (copies, old mixed with new). Down below: just 2 crisp facts survive. The takeaway sits in the last line: **Consolidation = Merge + Dedupe + Update + Summarize**.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MEMORY CONSOLIDATION                              │
│                                                                  │
│  Before consolidation:                                          │
│  ├── Fact: "HI contribution 4.5%" (day 1, source A)            │
│  ├── Fact: "HI contribution 4.5% of base salary" (day 2, B)    │
│  ├── Fact: "2024 HI rate is 4.5%" (day 3, source C)            │
│  ├── Fact: "HI contribution 4.5%" (day 5, source A - duplicate!)│
│  └── Fact: "HI contribution 5% starting 2025" (day 10, D)     │
│                                                                  │
│  After consolidation:                                            │
│  ├── Fact: "HI contribution 4.5% (2024)" — merged 3 facts      │
│  ├── Fact: "HI contribution 5% (from 2025)" — latest update    │
│  └── Deleted: duplicate "HI contribution 4.5%"                 │
│                                                                  │
│  Consolidation = Merge + Dedupe + Update + Summarize            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Implementation

The `MemoryConsolidator` class is your friendly cleanup crew with 4 chores: folding duplicate facts together (`consolidate_facts`), retiring facts that are past their prime (`temporal_consolidation`), writing a neat summary card per topic (`summarize_entities`), and raising a flag when two facts disagree (`conflict_resolution`). Each chore hands you a little receipt (how many merged / deleted / removed) — just glance at those numbers to see what got tidied.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/02-2-2-implementation.py`](examples/02-2-2-implementation.py)

</details>

---

## 3. Report Generation

> **📌 Core Concept**
> 
> **Concept:** Report Generation is producing structured reports — conversation summaries, knowledge base overviews, multi-source analyses — from dialogue data and the memory store.
> 
> **Analogy:** Like an assistant writing meeting minutes — turning scattered speech into a concise document with clear sections that anyone can read and understand.
> 
> **Why it matters:** Reports are the "bridge" that turns raw information into reusable knowledge for the next session or for the whole team.

### 3.1 Report Types

Here are the 4 everyday reports your system can whip up. Read each little card in 3 lines: **Input** (what goes in) → **Output** (what comes out) → **Use** (who it's for). "Conversation Summary", for instance, turns a long chat into a neat handoff note for the next session.

```
┌──────────────────────────────────────────────────────────────────┐
│                    REPORT TYPES                                   │
│                                                                  │
│  1. CONVERSATION SUMMARY                                        │
│     Input: Chat history                                         │
│     Output: Structured summary                                  │
│     Use: Session handoff, memory storage                        │
│                                                                  │
│  2. KNOWLEDGE REPORT                                             │
│     Input: Knowledge graph + facts                              │
│     Output: Organized knowledge overview                        │
│     Use: KB maintenance, debugging                              │
│                                                                  │
│  3. ANALYSIS REPORT                                              │
│     Input: Multiple sources + retrieved context                 │
│     Output: Analysis with citations                             │
│     Use: Decision support, research                             │
│                                                                  │
│  4. FEEDBACK REPORT                                              │
│     Input: User feedback + ratings                              │
│     Output: Improvement recommendations                         │
│     Use: System improvement                                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Implementation

The `ReportGenerator` class cooks up 3 kinds of reports: `conversation_summary` (a tidy recap of a chat), `knowledge_report` (a tour of what's in the knowledge base), and `analysis_report` (a multi-source write-up with citations). Each one asks the LLM to draft the report and then tidies the answer into JSON — and if the LLM hands back messy formatting, there's a safety net that returns a sensible default instead of crashing.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/03-3-2-implementation.py`](examples/03-3-2-implementation.py)

</details>
---

## 4. KB Maintenance

> **📌 Core Concept**
> 
> **Concept:** Knowledge Base (KB) maintenance is the set of operations that manage the "knowledge warehouse": adding new knowledge, fixing incorrect knowledge, deleting outdated knowledge, and checking warehouse quality.
> 
> **Analogy:** Like library maintenance — purchasing new books, re-printing faulty pages, pulling damaged books, and periodically auditing the catalog.
> 
> **Why it matters:** A knowledge base that is not maintained gradually accumulates wrong and duplicate information, dragging the whole system into unreliable answers.

### 4.1 Knowledge Base Operations

Say hello to the `KBMaintainer` — the **warehouse manager of your knowledge shelves**, with 4 trusty moves: `add_knowledge` (stock a new fact), `update_knowledge` (swap an old one), `delete_knowledge` (clear a topic or a single detail), and `validate_knowledge` (walk the aisles hunting for contradictions and orphaned items). And like any careful manager, it logs every move in the `changelog` diary — so you'll always know which fact was touched, and when.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/04-4-1-knowledge-base-operations.py`](examples/04-4-1-knowledge-base-operations.py)

</details>

---

## 5. Event Sourcing Pattern

> **📌 Core Concept**
> 
> **Concept:** Event Sourcing is a way of storing "everything that ever happened" — instead of only recording the current state, we store the complete list of events; the current state is then "replayed" from those events.
> 
> **Analogy:** Like the dashcam of a car trip — you remember every stretch of road you drove, so you can rewind, or branch off at any point, not just know the destination.
> 
> **Why it matters:** With the full history you get an audit trail, rollback, and the ability to trace exactly where a bug originated.

### 5.1 Concept

Time for a story from the world of banking ledgers. Instead of keeping only today's balance, event sourcing keeps **the whole diary of everything that ever happened** — every deposit and withdrawal, each stamped with a time (`@ t=...`). Those three superpowers in the middle of the drawing say it all: **replay the whole diary to rebuild today**, **stop the replay halfway to visit the past** (time travel), and **never lose the paper trail** (audit trail).

```
┌──────────────────────────────────────────────────────────────────┐
│                EVENT SOURCING FOR MEMORY                          │
│                                                                  │
│  Instead of storing only the current state, store ALL events:   │
│                                                                  │
│  Events Log:                                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. [ADD]     HI → contribution rate → 4.5%   @ t=0     │   │
│  │ 2. [ADD]     HI → validity period → 5 years  @ t=1     │   │
│  │ 3. [UPDATE]  HI → contribution rate → 5% (from 4.5%) @ t=2│
│  │ 4. [FEEDBACK] Query="HI contribution?" → rating=4 @ t=3 │   │
│  │ 5. [ADD]     HI → effective from → 01/2025     @ t=4    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Current State = Replay all events                              │
│  Time Travel = Replay up to time T                              │
│  Audit Trail = Full history of all changes                      │
│                                                                  │
│  Advantages:                                                    │
│  ├── Complete audit trail                                      │
│  ├── Can undo/rollback                                         │
│  ├── Can analyze changes over time                             │
│  └── Debugging: trace exactly what happened                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Implementation

The `EventSourcedMemory` class turns that diary idea into working code. Everything funnels through `record_event` — each change lands in the `events` diary, and then the visible `state` is refreshed via `_apply_event`. Two treats to notice: `get_state_at(event_id)` lets you **hop back in time** to any moment in the diary, and `undo_last()` takes back the most recent entry by rebuilding the story from scratch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/05-5-2-implementation.py`](examples/05-5-2-implementation.py)

</details>

---

## 6. Memory Store Case Studies

> **📌 Core Concept**
> 
> **Concept:** This is a collection of case studies from real products — Claude Code, Mem0, OpenMemory, DeepSeek Harness — showing how production teams solve write-back and memory consolidation.
> 
> **Analogy:** Like reading restaurant reviews before opening your own — learn from those who came first to avoid costly mistakes.
> 
> **Why it matters:** Theory is easy to talk about, hard to do; case studies show which patterns actually work at real scale.

The case studies below show how production systems manage write-back and memory consolidation.

---

### 6.1. Claude Code — Session Memory & Cross-Session Persistence

**Context**: Claude Code (Anthropic) needs to remember context across multiple sessions, know the project structure, and update knowledge when the user learns something new.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>
> 📄 **Example code:** [`examples/06-6-1-claude-code-session-memory-cross-session.ts`](examples/06-6-1-claude-code-session-memory-cross-session.ts)

</details>

**Key Insights**:
1. ✅ **3-tier memory** — Session (ephemeral) → Project (persistent in CLAUDE.md) → Global (cross-project)
2. ✅ **Auto-learn from corrections** — User corrections become pitfalls in CLAUDE.md
3. ✅ **Skill tracking** — Adjusts response detail based on user proficiency
4. ✅ **Session consolidation** — Important info persists after session ends

---

### 6.2. Mem0 — Production Memory Layer for AI Agents

**Mem0** (formerly EmbedChain) is an open-source memory layer for AI agents:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/07-6-2-mem0-production-memory-layer-for-ai.py`](examples/07-6-2-mem0-production-memory-layer-for-ai.py)

</details>

**Key Insights**:
1. ✅ **Auto-extract facts** — LLM extracts facts from conversations automatically
2. ✅ **Temporal decay** — Older memories get lower relevance over time
3. ✅ **Conflict resolution** — Temporal + confidence-based resolution
4. ✅ **User namespacing** — Multi-user memory isolation

---

### 6.3. OpenMemory — MCP-Based Memory Server

This case study plays the role of an MCP (Model Context Protocol) compliant memory server — meaning memory operations are "exposed" as tools that the LLM can call directly: `create_memory`, `search_memory`, `update_memory`, `delete_memory`, `list_memories`, `consolidate_memories`. Read it like an API catalog: each function is a standard operation, so any agent can use the memory without knowing how things are stored internally.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/08-6-3-openmemory-mcp-based-memory-server.py`](examples/08-6-3-openmemory-mcp-based-memory-server.py)

</details>

---

### 6.4. DeepSeek Harness — Trajectory Fork & Replay Engine

**Context**: DeepSeek Harness (developed by the DeepSeek team) is an **agent harness framework** with outstanding **trajectory traceability** — tracking, replaying, forking, and resuming every agent session.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Example code:** [`examples/09-6-4-deepseek-harness-trajectory-fork-replay-engine.ts`](examples/09-6-4-deepseek-harness-trajectory-fork-replay-engine.ts)

</details>

**Key Innovations**:

1. ✅ **Append-only Session Event Stream** — Every prompt, thought, tool call, and output is logged. History is never mutated.
2. ✅ **`replayToStep(n)`** — Restores the exact state at step `n`. Used for debugging, time-travel inspection.
3. ✅ **`forkSession(step, newPrompt)`** — Creates a new branch from any step. Enables "what-if" analysis: *"What if I had asked differently at that point?"*
4. ✅ **`resumeSession(step)`** — Continues running from a checkpoint. Saves tokens on long-running tasks.
5. ✅ **Event Search** — Full-text search across the whole trajectory. Find *"every time tool X failed"* or *"all prompts containing the word Y"*.
6. ✅ **Cost Tracking** — Every event has a `cost_usd`. Enables cost breakdowns per session, per tool, per step.
7. ✅ **Failure Pattern Detection** — Automatically finds patterns: which tools fail most, which error types are common.

**DeepSeek Harness 4 Runtime Modes**:

| Mode | Use Case | Tools Available |
|------|----------|-----------------|
| **Standard** | Full agent loop | All tools + trajectory tracking |
| **Code Mode** | Single-turn SDK (`@deepseek-ai/dsh`) | `bash`, `editor` only, batched |
| **Minimal Benchmark** | SWE-bench evaluation | `bash`, `editor` isolation |
| **Creator Inspector** | Visual timeline/presets | Read-only trajectory view |

**File Reference**: For implementation details, see [`trajectory-fork-replay.md`](trajectory-fork-replay.md)

---

## 7. Advanced Memory Patterns

> **📌 Core Concept**
> 
> **Concept:** Advanced patterns that keep the memory system running well in production: write-behind cache (write fast, then flush to disk later), consolidation pipeline (automated periodic cleanup), and versioned memory (remembering by version, like Git).
> 
> **Analogy:** If the earlier sections were "learning to write", this section is "learning professional work habits" — organized, scheduled, backed up.
> 
> **Why it matters:** In practice, manual writing and cleanup are not enough — you need automated mechanisms that are both fast and safe.

### 7.1. Write-Behind Cache Pattern

This pattern starts from a very relatable headache: "saving to disk feels so slow — how do we speed it up?" The trick is the same one a busy shopkeeper uses: scribble the receipt now (answer the customer instantly), then enter everything into the big ledger in one calm batch at closing time. In plain terms, it's **a fair trade — you accept a tiny risk of losing the very last scribble if the lights go out, in exchange for lightning-fast replies when writes pour in.**

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/10-7-1-write-behind-cache-pattern.py`](examples/10-7-1-write-behind-cache-pattern.py)

</details>

### 7.2. Memory Consolidation Pipeline

Unlike the manual consolidation in section 2, this is an "automated cleanup assembly line" that runs periodically in 5 stages: deduplicate → resolve conflicts → temporal decay → archive old memories → remove low-confidence memories. Each stage is a `_stage_*` function, and `run_full_consolidation` runs the whole pipeline and returns a statistics report — reading this report immediately shows how many items each stage cleaned up.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/11-7-2-memory-consolidation-pipeline.py`](examples/11-7-2-memory-consolidation-pipeline.py)

</details>

### 7.3. Versioned Memory (Git-like Memory)

This pattern borrows Git's exact idea and applies it to memory: every `set` of a value creates a new **version** with a full state snapshot. This gives you `diff` (comparing two points in time), `rollback` (returning to an old version, like git revert), and `log` (viewing the change history). In plain terms: memory remembers how it "has been modified over time", so fixing a mistake means just pulling back to an older state.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/12-7-3-versioned-memory-git-like-memory.py`](examples/12-7-3-versioned-memory-git-like-memory.py)

</details>

---

## 8. Best Practices & Anti-Patterns

> **📌 Core Concept**
> 
> **Concept:** A list of things you SHOULD do (best practices) and SHOULD NOT do (anti-patterns) when building memory updates, gathered from the experience of many production systems.
> 
> **Analogy:** Like a table of traffic rules — you don't need to memorize the detailed reasons, just know "green light go, red light stop" to avoid accidents.
> 
> **Why it matters:** Helps you avoid expensive mistakes that many teams have already hit, saving time on later bug fixes.

```
┌──────────────────────────────────────────────────────────────────┐
│              MEMORY UPDATE DO's                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ DO: Always log write operations                              │
│     → Audit trail for debugging                                  │
│     → Event sourcing enables rollback                            │
│                                                                  │
│  ✅ DO: Deduplicate before storing                               │
│     → Check existing memories first                              │
│     → Use similarity threshold (0.85 recommended)                │
│                                                                  │
│  ✅ DO: Apply confidence scoring                                  │
│     → Not all facts are equally reliable                         │
│     → Lower confidence for indirect information                 │
│                                                                  │
│  ✅ DO: Use temporal decay                                        │
│     → Old information may be outdated                            │
│     → Exponential decay: 0.99^days                              │
│                                                                  │
│  ✅ DO: Consolidate periodically                                   │
│     → Background pipeline (hourly/daily)                         │
│     → Merge duplicates, resolve conflicts                        │
│                                                                  │
│  ✅ DO: Version important memories                                │
│     → Enable rollback if updates are wrong                       │
│     → Track how knowledge evolves                                │
│                                                                  │
│  ✅ DO: Separate namespaces per user/project                     │
│     → Prevent cross-contamination                                │
│     → Enable personalized memory                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

```
┌──────────────────────────────────────────────────────────────────┐
│              MEMORY UPDATE DON'Ts                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ DON'T: Overwrite without versioning                          │
│     → Always keep previous version                               │
│     → Enable rollback capability                                 │
│                                                                  │
│  ❌ DON'T: Store raw conversation as memory                      │
│     → Extract facts first                                        │
│     → Raw text wastes storage and slows retrieval               │
│                                                                  │
│  ❌ DON'T: Forget to handle conflicts                            │
│     → Same topic, different values = conflict                   │
│     → Always have a resolution strategy                          │
│                                                                  │
│  ❌ DON'T: Store everything forever                               │
│     → Archive old, unused memories                               │
│     → Remove low-confidence garbage                              │
│                                                                  │
│  ❌ DON'T: Write synchronously when write volume is high          │
│     → Use write-behind pattern                                   │
│     → Batch writes for efficiency                                │
│                                                                  │
│  ❌ DON'T: Ignore user feedback                                   │
│     → "That last answer was wrong" MUST update memory            │
│     → Feedback loop is critical for quality                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 9. Performance Metrics

> **📌 Core Concept**
> 
> **Concept:** The layer that measures the health indicators of the memory store: write/read latency, dedup ratio, number of conflicts, time per consolidation run.
> 
> **Analogy:** Like the dashboard gauges in a car — you don't watch them the whole way, but when you suspect a problem you must be able to read them.
> 
> **Why it matters:** Without measurement, you don't know whether the memory system is gradually degrading or working well.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/13-9-performance-metrics.py`](examples/13-9-performance-metrics.py)

</details>

---

## 10. Hands-on Labs

> **📌 Core Concept**
> 
> **Concept:** Hands-on labs you can run in Python to experience write-back, consolidation, versioned memory, and metrics with your own hands.
> 
> **Analogy:** Like exercise practice — reading the technique is no substitute for practicing until you know the movements by heart.
> 
> **Why it matters:** Learning by doing helps you remember many times longer than reading theory alone.

### Lab 1: Write-back Memory

In this lab you use `MemoryWriter` to record an episodic memory, two facts about health insurance, update the user profile, then call `get_stats()` to see how much the system has "remembered".

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/14-lab-1-write-back-memory.py`](examples/14-lab-1-write-back-memory.py)

</details>

### Lab 2: Consolidation

Practice cleanup with `MemoryConsolidator`: create 3 facts about health insurance (two nearly duplicates, one a newer update), run `generate_memory_report`, and see which contradiction `conflict_resolution` detects.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/15-lab-2-consolidation.py`](examples/15-lab-2-consolidation.py)

</details>

### Lab 3: Versioned Memory

Simulate a fact about the health insurance contribution rate evolving across 3 versions, view the history with `vm.log()`, compare two points in time with `vm.diff(0, 2)`, and finally try rolling back to the first version with `vm.rollback(0)`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/16-lab-3-versioned-memory.py`](examples/16-lab-3-versioned-memory.py)

</details>

### Lab 4: Metrics

Simulate 100 write/read operations with random figures and 2 consolidation runs, then print the `metrics.report()` report to see how the system is measured.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/17-lab-4-metrics.py`](examples/17-lab-4-metrics.py)

</details>

---

## 12. Production Supplement: Retention, Consolidation, Compaction Contract & SLOs

> Bridges §02 eviction with §03 persistence: what may be dropped vs what must survive.

### 12.1 Definitions

| Term | Definition |
|------|------------|
| Retention / TTL | Per-memory-class expiry (`episodic 30d, fact until superseded, session 24h`); expiry → archive or hard delete |
| GDPR delete | Tenant/user-scoped purge across primary store, vector index, backups (within documented window) + receipt |
| Consolidation trigger | Condition that runs merge/dedup/conflict job: size, time, signal (conflict rate, feedback) |
| Compaction↔memory contract | Boundary: §02 may evict anything except what §03 has pinned as durable |
| Write-path SLO | p50/p99 + durability guarantee for the ingest path (e.g. `p99 < 300ms, 0 data loss on ack`) |

### 12.2 Retention / Compliance

- **TTL defaults:** `session: 24h → drop; episodic: 30–90d → archive; semantic fact: no TTL but needs valid_until + source; user profile: until delete request.` Sweep hourly; archive to cold store before delete.
- **Per-tenant isolation:** `tenant_id` partition key on every table/namespace; queries always filtered; cross-tenant reads rejected at API + DB policy (RLS). Separate encryption key per enterprise tenant.
- **GDPR/CCPA delete:** `DELETE /memory?user=X` → tombstone → purge vector + KG + logs (redact) → vacuum backups ≤30d → return `deletion_receipt{id, scope, ts}`. SLA 24h.

### 12.3 Consolidation Triggers + Conflict Resolution

Run consolidation when **any**: `unconsolidated_writes > 500`, hourly cron, `conflict_rate > 5%`, negative feedback on a fact. Pipeline: dedup (cosine ≥0.9 merge) → conflict detect (same subject+predicate, different object) → resolve: `last-writer-wins` only if newer source trust ≥ old; else `highest-trust-wins`; else `escalate_to_user`. Keep both versions + `supersedes` edge — never silent overwrite.

### 12.4 Compaction↔Memory Contract

| §02 may evict (transient) | §03 must persist (durable) |
|---|---|
| Raw tool stdout, old retrieval chunks, superseded diffs, chit-chat | Pinned facts, decisions, open TODOs, user preferences, resume block |
| May drop after resume summary | Must survive compaction; re-injectable via retrieve |

Rule: compaction emits `resume_block`; write-back **must** persist `resume_block + decisions + open items` before dropping them from context. On session restore, §02 hydrates from §03 by `tenant+task` query.

### 12.5 Write-Path SLOs

- `p50 write < 80ms, p99 < 300ms`; async consolidation `p99 < 5min`. Dedup check inside write path; heavy merge off critical path (write-behind queue).
- Durability: ack only after WAL + primary write; retry queue with idempotency key `tenant:doc_hash`. Alert on `write_error% > 1%`, `queue_lag > 10k`.

<details>
<summary>TypeScript Code — Versioned Memory with Consolidation (Click to expand/collapse)</summary>

> 📄 **Example code:** [`examples/18-12-5-write-path-slos.ts`](examples/18-12-5-write-path-slos.ts)

</details>

### 12.6 Checklist

| # | Rule |
|---|------|
| 1 | TTL per class + hourly sweeper; archive before hard delete |
| 2 | `tenant_id` partition + RLS; no cross-tenant query path exists |
| 3 | GDPR delete purges facts + vectors + logs with receipt ≤24h |
| 4 | Consolidation on size/time/signal triggers; trust-ordered conflict resolution, no silent overwrite |
| 5 | Enforce compaction↔memory contract: resume/decisions persisted before eviction |
| 6 | Write SLO dashboard: p99, error%, queue lag, dedup rate, conflict rate |

---

## 11. Reference Materials

> **📌 Core Concept**
> 
> **Concept:** Additional reading sources including scientific papers, frameworks and tools, plus blogs from teams that actually build memory systems for production.
> 
> **Analogy:** Like a "read before the exam" list — if you want to dig deeper, this is where to start.
> 
> **Why it matters:** This field changes very fast — reference material helps you stay current and verify your knowledge.

### Papers & Research

1. **MemGPT: Towards LLMs as Operating Systems** — UC Berkeley, 2023 — Tiered memory management for LLMs
2. **MemoryBank: Enhancing Large Language Models with Long-Term Memory** — 2023 — Weighted memory decay
3. **A Survey on Long-Term Memory for AI Agents** — 2024 — Comprehensive overview of memory architectures

### Frameworks & Tools

1. **Mem0** — Production memory layer for AI agents — https://mem0.ai
2. **LangMem** — Long-term memory for agents — https://github.com/langchain-ai/langmem
3. **Zep** — Memory server for AI assistants — https://www.getzep.com
4. **OpenMemory** — MCP-based memory server — https://github.com/openmemory

### Blogs & Resources

1. **Anthropic — Memory in Claude Code** — 3-tier memory architecture
2. **LangChain — Building Long-Term Memory** — Practical guide
3. **Mem0 Blog** — Memory patterns for production AI

---

**Conclusion**

Memory Update & Knowledge Store is the process of keeping the AI's "brain" always accurate and up to date. Three main patterns:

> **"A system that cannot update its knowledge is a system that learns nothing."**

1. **Event-driven updates** — When a new event occurs, update immediately
2. **Consolidation pipeline** — Background process that cleans + merges + resolves conflicts
3. **Temporal decay** — Old information gradually loses priority, avoiding outdated knowledge

Key takeaways:
1. ✅ **Always deduplicate** — before storing new facts
2. ✅ **Version important memories** — enable rollback
3. ✅ **Consolidate periodically** — background pipeline
4. ✅ **Apply temporal decay** — older ≠ more important
5. ✅ **Track metrics** — write latency, dedup rate, conflicts

---

*Document: III. Update Memory & Knowledge Store*  
*Last updated: 16/10/2026*  
*Author: AI Knowledge Repository*  
*Environment: Ollama (gemma3:12b, nomic-embed-text)*

---

## October 2026 Update — Structured Note-Taking & Long-Running Memory

### 1. Structured note-taking / agentic memory (Anthropic 09/2025)

The agent writes NOTES.md / a todo list outside the context window in order to:
- Keep state across turns within a session
- Hand off context to the next session
- Avoid forgetting agreed action items

**Memory tool (Claude Developer Platform):** persistent memory across
summarizations — the agent can read/write a dedicated memory store, independent
of the conversation window.

**Suggested pattern:**

```
PROJECT/
├── CLAUDE.md          # System instructions + conventions
├── NOTES.md           # Agent notes, todos, state
├── SPEC.md            # Specifications
└── PROGRESS.md        # Feature progress tracking
```

### 2. Long-running agent memory pattern (Anthropic 11/2025)

An initializer agent creates the initial structure; subsequent sessions read it and continue:

| File | Purpose |
|------|----------|
| `feature_list.json` | List of features with `passes: false` (not yet passing) |
| `init.sh` | Repo setup script, dependencies |
| `claude-progress.txt` | Progress notes, decisions, next steps |
| Git commits | Each feature committed once it passes |

**Session flow:**
1. Read `feature_list.json` + `git log` → determine the next feature
2. Implement the feature → run tests
3. If tests pass → mark the feature in the JSON + git commit + update progress
4. If they fail → write a note into the progress file

**Why JSON is preferred over Markdown:**
- Models overwrite/misformat free-form Markdown more easily than JSON
- Machine-readable parsing — no regex over text
- Easy to diff in git; conflict resolution is simpler

### 3. When to Reset Memory Completely

**Reset when:**
- The task is fully complete
- All facts have been consolidated into permanent storage
- The final milestone has been reached

**Don't reset when:**
- You're mid-milestone / mid-important-meeting
- Facts haven't been consolidated yet (insights would be lost)
- You need an audit trail for compliance

### 4. Python code: ProgressStore class

> 📄 **Example code:** [`examples/19-4-python-code-progressstore-class.py`](examples/19-4-python-code-progressstore-class.py)

### 5. Cross-Links

- `[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)` — Layer 6 (Agent Memory & State) — structured memory patterns for production agents.
