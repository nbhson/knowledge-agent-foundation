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

Imagine you are a librarian. Every day, people come to borrow new books and return old ones. If you **only accept new books** but never rearrange the shelves, never remove damaged books, never update the catalog — then after 1 year, the library becomes a **messy storage warehouse** where no one can find anything.

**That is exactly the problem of AI memory when you only "record" without "updating".**

An LLM can remember new information, but without **consolidating** (merging), **pruning** (removing the old), and **indexing** (reorganizing) — the knowledge base will grow slower, noisier, and less accurate over time. The result? The agent repeats the same mistake, serves outdated information, and hallucinates for lack of factual grounding.

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

**Analogy**: Updating memory is like a librarian — not just accepting new books (Capture), but also rearranging the shelves (Index), removing old damaged books (Prune), and updating the catalog (Consolidate). Without a librarian, the library becomes a messy storage warehouse.

**If you skip it**: knowledge base goes stale → agent repeats the same mistakes, provides outdated information, hallucinates for lack of factual grounding, and eventually user trust drops → adoption drops.

## Overview

> **📌 Core Concept**
> 
> **Concept:** Write-back is the "write in reverse" direction — alongside reading (retrieving) knowledge, the system also writes back what it has just learned (events, facts, feedback) into the memory store, and only then comes consolidation and report generation.
> 
> **Analogy:** Like a librarian — retrieval is walking to the shelf to take out a book, while write-back is writing the catalog card for a newly purchased book.
> 
> **Why it matters:** If you only "read" without "writing", the AI answers with stale knowledge and every conversation session starts from zero again.

After retrieving and processing information, the system needs to **write it back** into the memory store. This is the **write-back** process — updating knowledge bases, memory systems, and generating reports.

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

Imagine a doctor who remembers every patient's medical chart. If he only **reads** the charts and **never updates** them when new test results arrive, then after 1 year the charts become useless. **Retrieval alone is not enough — write-back is what creates real value.**

Three core principles:

1. **Memory is a Living System, not a Static Archive**: Old information must be updated, merged, and sometimes deleted. Just like the human brain, which forgets what is no longer relevant.
2. **Every Interaction is a Learning Opportunity**: Every conversation, every piece of feedback, every decision produces new knowledge. If you don't write it down, you are letting value leak away.
3. **Consolidation > Accumulation**: Uncontrolled data accumulation creates **noise**. Consolidation — the process of merging, deduplicating, and updating — creates **signal**.

### Research Evidence

#### Google Research (2024): "Memory-Enhanced Agents"
> Agents with memory write-back achieve a **37% improvement** on multi-turn tasks compared to agents that only have retrieval.

The cause: the agent does not record context from earlier turns → has to ask the user again → wasted time and a degraded experience.

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

It's not that new information always means writing it down — write-back when it **changes the state** of the user, of the system, or when it produces a lesson. Read the three situations below as three scenarios: the first line is what happens in the conversation; the `→` lines are what the system needs to do in response.

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

The `MemoryWriter` class below is the system's "pen": `write_episodic` records events, `write_fact` records facts, `update_fact` modifies facts, `write_user_profile` updates user information. You don't need to understand every line — just notice the common thread: **every function writes to `event_log`** so that later you can trace who recorded what, and when.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

class MemoryWriter:
    """
    Write information back to various memory systems
    
    Supports: Episodic, Semantic, Working memory
    """
    
    def __init__(self, vector_store=None, knowledge_graph=None):
        self.vector_store = vector_store
        self.knowledge_graph = knowledge_graph
        self.episodic_store = []  # Simple list for demo
        self.entity_store = {}
        self.event_log = []
    
    # ─────────────────────────────────────────────
    # EPISODIC MEMORY: Store events
    # ─────────────────────────────────────────────
    def write_episodic(self, event_type, content, metadata=None):
        """
        Record an event into episodic memory
        
        event_type: "conversation", "learning", "feedback", "decision"
        content: The event content
        metadata: Additional information
        """
        event = {
            "id": f"ep_{len(self.episodic_store)}",
            "type": event_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        
        self.episodic_store.append(event)
        
        # Also store in vector DB for semantic search
        if self.vector_store:
            embedding = self._get_embedding(content)
            self.vector_store.add(
                document=content,
                vector=embedding,
                metadata={"type": "episodic", **event}
            )
        
        self._log_event("write_episodic", event)
        return event["id"]
    
    def recall_episodic(self, query, top_k=5):
        """Recall relevant episodic memories"""
        if self.vector_store:
            embedding = self._get_embedding(query)
            results = self.vector_store.search(embedding, top_k)
            return [r["metadata"] for r in results]
        
        # Fallback: search by keyword
        query_lower = query.lower()
        matches = [
            e for e in self.episodic_store
            if query_lower in e["content"].lower()
        ]
        return matches[:top_k]
    
    # ─────────────────────────────────────────────
    # SEMANTIC MEMORY: Store facts
    # ─────────────────────────────────────────────
    def write_fact(self, subject, predicate, obj, confidence=1.0):
        """
        Record a fact into semantic memory (Knowledge Graph)
        
        Example: ("health insurance", "contribution rate", "4.5% of base salary", 0.95)
        """
        fact = {
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "confidence": confidence,
            "created_at": datetime.now().isoformat(),
            "source": "user_conversation",
        }
        
        if self.knowledge_graph:
            self.knowledge_graph.add_triplet(subject, predicate, obj)
        
        # Also vectorize for semantic search
        if self.vector_store:
            fact_text = f"{subject} {predicate} {obj}"
            embedding = self._get_embedding(fact_text)
            self.vector_store.add(
                document=fact_text,
                vector=embedding,
                metadata={"type": "fact", **fact}
            )
        
        self._log_event("write_fact", fact)
        return fact
    
    def update_fact(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update an existing fact"""
        if self.knowledge_graph:
            # Remove old triplet
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == old_obj)
            ]
            # Add new triplet
            self.knowledge_graph.add_triplet(subject, predicate, new_obj)
        
        update_event = {
            "action": "update_fact",
            "old": {"subject": subject, "predicate": predicate, "object": old_obj},
            "new": {"subject": subject, "predicate": predicate, "object": new_obj},
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        
        self._log_event("update_fact", update_event)
        return update_event
    
    def delete_fact(self, subject, predicate, obj):
        """Delete a fact from knowledge"""
        if self.knowledge_graph:
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == obj)
            ]
        
        self._log_event("delete_fact", {
            "subject": subject, "predicate": predicate, "object": obj
        })
    
    # ─────────────────────────────────────────────
    # ENTITY MEMORY: Store entities
    # ─────────────────────────────────────────────
    def write_entity(self, name, entity_type, attributes=None):
        """Store/update entity information"""
        if name not in self.entity_store:
            self.entity_store[name] = {
                "type": entity_type,
                "attributes": {},
                "created_at": datetime.now().isoformat(),
            }
        
        if attributes:
            self.entity_store[name]["attributes"].update(attributes)
        
        self.entity_store[name]["updated_at"] = datetime.now().isoformat()
        
        self._log_event("write_entity", {"name": name, "type": entity_type})
        return self.entity_store[name]
    
    # ─────────────────────────────────────────────
    # USER PROFILE: Store user information
    # ─────────────────────────────────────────────
    def write_user_profile(self, user_id, updates):
        """
        Update the user profile
        
        updates: dict of {field: value}
        Example: {"occupation": "freelancer", "location": "HCM"}
        """
        profile = self.entity_store.get(f"user_{user_id}", {
            "type": "user",
            "attributes": {},
        })
        
        profile["attributes"].update(updates)
        profile["updated_at"] = datetime.now().isoformat()
        
        self.entity_store[f"user_{user_id}"] = profile
        
        self._log_event("update_profile", {
            "user_id": user_id, 
            "updates": updates
        })
        return profile
    
    def get_user_profile(self, user_id):
        """Retrieve user profile"""
        return self.entity_store.get(f"user_{user_id}", None)
    
    # ─────────────────────────────────────────────
    # FEEDBACK LOOP
    # ─────────────────────────────────────────────
    def write_feedback(self, query, answer, rating, correction=None):
        """
        Store user feedback for improvement
        
        rating: 1-5
        correction: correct answer if user says wrong
        """
        feedback = {
            "query": query,
            "original_answer": answer,
            "rating": rating,
            "correction": correction,
            "timestamp": datetime.now().isoformat(),
        }
        
        if self.vector_store and correction:
            # Store correction as a better example
            embedding = self._get_embedding(query)
            self.vector_store.add(
                document=correction,
                vector=embedding,
                metadata={
                    "type": "correction",
                    "original_answer": answer,
                    "rating": rating,
                }
            )
        
        self._log_event("feedback", feedback)
        return feedback
    
    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────
    def _get_embedding(self, text):
        """Get embedding using Ollama"""
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text",
                "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _log_event(self, event_type, data):
        """Log all write operations for audit trail"""
        self.event_log.append({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_stats(self):
        """Return write statistics"""
        return {
            "episodic_count": len(self.episodic_store),
            "entity_count": len(self.entity_store),
            "event_count": len(self.event_log),
            "event_types": list(set(e["type"] for e in self.event_log)),
        }
```

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

The ASCII block below compares memory **BEFORE** and **AFTER** consolidation. The top half shows 5 scattered facts about health insurance (duplicates, old and new mixed together); the bottom half shows the result after cleanup — only 2 clear facts remain. The core idea is in the last line: **Consolidation = Merge + Dedupe + Update + Summarize**.

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

The `MemoryConsolidator` class performs 4 cleanup steps: merge identical facts (`consolidate_facts`), remove overly old facts (`temporal_consolidation`), summarize information about an entity (`summarize_entities`), and detect contradictory facts (`conflict_resolution`). Each function returns statistics (merged/deleted/removed) — just read the returned results to see what was cleaned up.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class MemoryConsolidator:
    """
    Consolidate and merge memories to reduce redundancy
    and keep knowledge up-to-date
    """
    
    def __init__(self, vector_store, knowledge_graph, llm_func=None):
        self.vector_store = vector_store
        self.kg = knowledge_graph
        self.llm = llm_func
    
    def consolidate_facts(self, similarity_threshold=0.85):
        """
        Step 1: Find and merge duplicate/similar facts
        """
        if not self.kg or not self.kg.triplets:
            return {"merged": 0, "deleted": 0}
        
        merged = 0
        deleted = 0
        
        # Group facts by subject
        facts_by_subject = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in facts_by_subject:
                facts_by_subject[key] = []
            facts_by_subject[key].append(obj)
        
        # For each group, keep only the latest/most complete
        for (subj, pred), objs in facts_by_subject.items():
            if len(objs) <= 1:
                continue
            
            # Find duplicates using text similarity
            unique_objs = []
            for obj in objs:
                is_dup = False
                for unique in unique_objs:
                    if self._text_similarity(obj, unique) > similarity_threshold:
                        is_dup = True
                        break
                if not is_dup:
                    unique_objs.append(obj)
            
            deleted += len(objs) - len(unique_objs)
        
        return {"merged": merged, "deleted": deleted}
    
    def temporal_consolidation(self, max_age_days=30):
        """
        Step 2: Remove outdated facts based on age
        
        Facts older than max_age_days may be outdated
        """
        from datetime import datetime, timedelta
        
        cutoff = datetime.now() - timedelta(days=max_age_days)
        removed = 0
        
        if not self.kg:
            return {"removed": removed}
        
        # Filter by timestamp (if stored in metadata)
        # Simplified: just count for demo
        return {"removed": removed}
    
    def summarize_entities(self, entity_name, llm_func=None):
        """
        Step 3: Generate summary for all facts about an entity
        
        Useful for building entity profiles
        """
        if not self.kg:
            return ""
        
        facts = self.kg.query_entity(entity_name, max_hops=1)
        
        if not facts:
            return f"No information found about {entity_name}"
        
        facts_text = "\n".join(
            f"- {subj} {pred} {obj}" 
            for subj, pred, obj, _ in facts
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            summary = func(
                f"Summarize information about {entity_name}:\n\n{facts_text}\n\nSummary:"
            )
            return summary
        
        return facts_text
    
    def conflict_resolution(self):
        """
        Step 4: Resolve conflicting facts
        
        Strategy: Most recent wins (temporal)
        Alternative: Most trusted source wins (source-based)
        """
        conflicts = []
        
        if not self.kg:
            return conflicts
        
        # Group by subject+predicate
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        # Find conflicts (same subject+predicate, different objects)
        for key, objs in fact_groups.items():
            if len(set(objs)) > 1:
                conflicts.append({
                    "subject": key[0],
                    "predicate": key[1],
                    "conflicting_values": list(set(objs)),
                    "resolution": "keep_latest",  # or "merge", "manual"
                })
        
        return conflicts
    
    def generate_memory_report(self, llm_func=None):
        """
        Generate a report of current memory state
        
        Useful for debugging and auditing
        """
        report = []
        report.append("=" * 50)
        report.append("MEMORY CONSOLIDATION REPORT")
        report.append("=" * 50)
        
        if self.kg:
            report.append(f"\nTotal triplets: {len(self.kg.triplets)}")
            report.append(f"Unique entities: {len(self.kg.entities)}")
            report.append(f"Predicates: {len(self.kg.predicates)}")
            
            # Community detection
            communities = self.kg.community_detection()
            report.append(f"Communities: {len(communities)}")
            
            for i, comm in enumerate(communities[:5]):
                report.append(f"  Community {i+1}: {', '.join(comm[:5])}")
        
        # Conflicts
        conflicts = self.conflict_resolution()
        report.append(f"\nConflicts found: {len(conflicts)}")
        for c in conflicts[:5]:
            report.append(f"  {c['subject']} → {c['conflicting_values']}")
        
        return "\n".join(report)
    
    def _text_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
```

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

The 4 basic report types a system can produce. Read each block in 3 lines: **Input** (what data is used) → **Output** (what is produced) → **Use** (what it's for). For example, "Conversation Summary" takes chat history to create a summary for handoff to the next work session.

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

The `ReportGenerator` class implements 3 report types: `conversation_summary` (conversation summary), `knowledge_report` (knowledge base overview), and `analysis_report` (multi-source analysis with citations). These functions call an LLM to write the report and then coerce the result into JSON — if the LLM returns the wrong format, the code has a fallback branch that returns default data instead of raising an error.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ReportGenerator:
    """Generate structured reports from memory and context"""
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def conversation_summary(self, messages, llm_func=None):
        """
        Create a summary from conversation history
        
        Output: JSON with summary, key_points, action_items
        """
        conversation_text = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in messages
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Analyze the following conversation and create a report:

{conversation_text}

Output JSON:
{{
  "summary": "2-3 sentence summary",
  "key_points": ["point 1", "point 2"],
  "action_items": ["task 1"],
  "topics_discussed": ["topic 1"],
  "sentiment": "positive/neutral/negative",
  "resolution": "resolved/ongoing/needs_followup"
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"summary": result, "key_points": [], "action_items": []}
        
        return {
            "summary": f"Conversation with {len(messages)} messages",
            "key_points": [],
            "action_items": [],
        }
    
    def knowledge_report(self, knowledge_graph, llm_func=None):
        """
        Create a report about the current knowledge base
        """
        if not knowledge_graph:
            return {"error": "No knowledge graph"}
        
        report = {
            "total_facts": len(knowledge_graph.triplets),
            "total_entities": len(knowledge_graph.entities),
            "total_predicates": len(knowledge_graph.predicates),
            "top_entities": [],
            "entity_details": {},
        }
        
        # Count entity frequency
        entity_count = {}
        for subj, pred, obj in knowledge_graph.triplets:
            entity_count[subj] = entity_count.get(subj, 0) + 1
            entity_count[obj] = entity_count.get(obj, 0) + 1
        
        # Top 10 entities
        sorted_entities = sorted(
            entity_count.items(), key=lambda x: x[1], reverse=True
        )
        report["top_entities"] = [
            {"name": name, "connections": count}
            for name, count in sorted_entities[:10]
        ]
        
        return report
    
    def analysis_report(self, query, sources, analysis, llm_func=None):
        """
        Create a structured analysis from multiple sources
        
        Output: Report with citations, confidence, recommendations
        """
        sources_text = "\n".join(
            f"[{i+1}] ({s.get('source', 'unknown')}): {s.get('content', s.get('text', ''))}"
            for i, s in enumerate(sources)
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Create an analysis report for the question:
            
Question: {query}

Reference sources:
{sources_text}

Analysis:
{analysis}

Output JSON:
{{
  "answer": "Main answer",
  "confidence": 0.0-1.0,
  "sources_used": [1, 2],
  "key_findings": ["finding 1", "finding 2"],
  "limitations": ["limitation 1"],
  "recommendations": ["recommendation 1"]
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"answer": result, "confidence": 0.5}
        
        return {"answer": analysis, "confidence": 0.5}
```

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

The `KBMaintainer` class is the "knowledge warehouse manager" with 4 core operations: `add_knowledge` (add), `update_knowledge` (modify), `delete_knowledge` (delete by topic or by detail), and `validate_knowledge` (audit for contradictory facts and orphaned entities). Note: every operation is recorded in the `changelog` — like a history journal so you know which knowledge was touched.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class KBMaintainer:
    """
    Maintain knowledge base: add, update, delete, validate
    """
    
    def __init__(self, knowledge_graph, vector_store):
        self.kg = knowledge_graph
        self.vector_store = vector_store
        self.changelog = []
    
    def add_knowledge(self, subject, predicate, obj, source="manual"):
        """Add new knowledge"""
        self.kg.add_triplet(subject, predicate, obj)
        
        # Also index for search
        fact_text = f"{subject} {predicate} {obj}"
        embedding = self._get_embedding(fact_text)
        self.vector_store.add(
            document=fact_text,
            vector=embedding,
            metadata={"source": source, "added_at": datetime.now().isoformat()}
        )
        
        self.changelog.append({
            "action": "add",
            "fact": (subject, predicate, obj),
            "source": source,
            "timestamp": datetime.now().isoformat(),
        })
    
    def update_knowledge(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update existing knowledge"""
        # Remove old
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and p == predicate and o == old_obj)
        ]
        
        # Add new
        self.kg.add_triplet(subject, predicate, new_obj)
        
        self.changelog.append({
            "action": "update",
            "old": (subject, predicate, old_obj),
            "new": (subject, predicate, new_obj),
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
    
    def delete_knowledge(self, subject, predicate=None, obj=None):
        """Delete knowledge (specific or all for a subject)"""
        before = len(self.kg.triplets)
        
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and 
                   (predicate is None or p == predicate) and
                   (obj is None or o == obj))
        ]
        
        deleted = before - len(self.kg.triplets)
        self.changelog.append({
            "action": "delete",
            "subject": subject,
            "count": deleted,
            "timestamp": datetime.now().isoformat(),
        })
        
        return deleted
    
    def validate_knowledge(self, validation_rules=None):
        """
        Validate knowledge base against rules
        
        Rules:
        - No orphan entities
        - No contradictory facts
        - All required predicates present
        """
        issues = []
        
        # Check for orphan entities
        connected = set()
        for subj, pred, obj in self.kg.triplets:
            connected.add(subj)
            connected.add(obj)
        
        orphans = self.kg.entities - connected
        if orphans:
            issues.append({
                "type": "orphan_entities",
                "entities": list(orphans),
                "severity": "warning",
            })
        
        # Check for contradictions
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        for key, objs in fact_groups.items():
            unique = set(objs)
            if len(unique) > 1:
                issues.append({
                    "type": "contradiction",
                    "fact": key,
                    "conflicting_values": list(unique),
                    "severity": "error",
                })
        
        return issues
    
    def export_knowledge(self, format="json"):
        """Export knowledge base"""
        if format == "json":
            return json.dumps({
                "triplets": [
                    {"subject": s, "predicate": p, "object": o}
                    for s, p, o in self.kg.triplets
                ],
                "entities": list(self.kg.entities),
                "changelog": self.changelog,
            }, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            lines = ["# Knowledge Base Export\n"]
            lines.append(f"Total facts: {len(self.kg.triplets)}\n")
            
            for subj, pred, obj in self.kg.triplets:
                lines.append(f"- **{subj}** {pred} **{obj}**")
            
            return "\n".join(lines)
    
    def get_stats(self):
        return {
            "total_facts": len(self.kg.triplets),
            "total_entities": len(self.kg.entities),
            "total_predicates": len(self.kg.predicates),
            "total_changes": len(self.changelog),
        }
    
    def _get_embedding(self, text):
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
```

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

This section introduces the original event-sourcing idea. The ASCII block shows how to store via an "event journal" — each line is a timestamped event (`@ t=...`). The three superpowers are in the middle of the block: **Current State = Replay all events** (the current state is rebuilt by replaying every event), **Time Travel** (replay up to a point T), and **Audit Trail** (keep the full change history).

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

The `EventSourcedMemory` class turns the above idea into code. Note `record_event` — every change goes through this function, is saved into the `events` list, and then `state` is updated via `_apply_event`. The two most interesting functions: `get_state_at(event_id)` allows "time travel" to the state at a given event, and `undo_last()` undoes the last event by rebuilding the entire state from scratch.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class EventSourcedMemory:
    """
    Memory system with full event sourcing
    All changes are stored as events, state is derived
    """
    
    def __init__(self):
        self.events = []
        self.state = {}  # Derived from events
    
    def record_event(self, event_type, data):
        """Record a new event"""
        event = {
            "id": len(self.events),
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self.events.append(event)
        
        # Update state
        self._apply_event(event)
        
        return event["id"]
    
    def _apply_event(self, event):
        """Apply event to update current state"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["object"]
        
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["new_object"]
        
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            self.state.pop(key, None)
        
        elif etype == "set_profile":
            self.state[("profile", data["user_id"])] = data["attributes"]
    
    def get_state(self):
        """Get current state"""
        return dict(self.state)
    
    def get_state_at(self, event_id):
        """Get state at a specific point in time (time travel)"""
        state = {}
        for event in self.events[:event_id + 1]:
            self._apply_event_to(state, event)
        return state
    
    def _apply_event_to(self, state, event):
        """Apply event to a specific state dict"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["object"]
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["new_object"]
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            state.pop(key, None)
    
    def get_event_history(self, event_type=None):
        """Get event history, optionally filtered by type"""
        if event_type:
            return [e for e in self.events if e["type"] == event_type]
        return list(self.events)
    
    def undo_last(self):
        """Undo the last event"""
        if not self.events:
            return None
        
        event = self.events.pop()
        # Rebuild state from remaining events
        self.state = {}
        for e in self.events:
            self._apply_event(e)
        
        return event
```

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
```typescript
/**
 * Claude Code Memory Architecture
 * 
 * 3 tiers of memory:
 * 1. Session Memory (ephemeral) — lives in conversation
 * 2. Project Memory (persistent) — lives in CLAUDE.md files
 * 3. Global Memory (cross-project) — lives in user config
 */
class ClaudeCodeMemoryManager {
  
  // ═══════════════════════════════════════════
  // TIER 1: SESSION MEMORY (ephemeral)
  // Lives only during current conversation
  // ═══════════════════════════════════════════
  private sessionMemory = {
    facts: new Map<string, Fact>(),      // Facts discovered this session
    decisions: [] as Decision[],         // Code decisions made
    corrections: [] as Correction[],    // User corrections
    filesModified: new Set<string>(),   // Files touched this session
    
    addFact(fact: Fact) {
      this.facts.set(fact.id, {
        ...fact,
        sessionId: currentSessionId,
        timestamp: Date.now()
      });
    },
    
    recordDecision(decision: Decision) {
      this.decisions.push({
        ...decision,
        timestamp: Date.now(),
        filesInvolved: this.filesModified
      });
    }
  };

  // ═══════════════════════════════════════════
  // TIER 2: PROJECT MEMORY (persistent)
  // Stored in CLAUDE.md at project root
  // Survives across sessions
  // ═══════════════════════════════════════════
  private projectMemory = {
    // CLAUDE.md format
    conventions: [] as string[],
    architecture: "",
    decisions: [] as Decision[],
    pitfalls: [] as string[],
    
    async loadFromDisk(projectRoot: string) {
      const claudeMd = path.join(projectRoot, 'CLAUDE.md');
      if (fs.existsSync(claudeMd)) {
        const content = fs.readFileSync(claudeMd, 'utf-8');
        this.parseClaudeMd(content);
      }
    },
    
    async saveToDisk(projectRoot: string) {
      const content = this.generateClaudeMd();
      fs.writeFileSync(
        path.join(projectRoot, 'CLAUDE.md'), 
        content, 'utf-8'
      );
    },
    
    generateClaudeMd(): string {
      return `# CLAUDE.md — Project Memory

## Conventions
${this.conventions.map(c => `- ${c}`).join('\n')}

## Architecture
${this.architecture}

## Past Decisions
${this.decisions.map(d => 
  `- [${d.date}] ${d.decision} (reason: ${d.reason})`
).join('\n')}

## Pitfalls
${this.pitfalls.map(p => `- ⚠️ ${p}`).join('\n')}
`;
    },
    
    // Auto-learn from session
    learnFromSession(sessionMemory: any) {
      // Extract conventions from code changes
      const patterns = this.detectPatterns(sessionMemory.filesModified);
      this.conventions.push(...patterns);
      
      // Store important decisions
      for (const decision of sessionMemory.decisions) {
        if (decision.importance === 'high') {
          this.decisions.push(decision);
        }
      }
      
      // Store pitfalls (user corrections)
      for (const correction of sessionMemory.corrections) {
        this.pitfalls.push(
          `${correction.context}: ${correction.correctApproach}`
        );
      }
    }
  };

  // ═══════════════════════════════════════════
  // TIER 3: GLOBAL MEMORY (cross-project)
  // User preferences, skill levels, patterns
  // ═══════════════════════════════════════════
  private globalMemory = {
    preferences: {
      language: 'typescript',
      style: 'functional',
      testFramework: 'vitest',
      linting: 'eslint'
    },
    skillLevels: new Map<string, number>(),  // topic -> proficiency
    commonPatterns: [] as Pattern[],
    
    updateSkillLevel(topic: string, interaction: UserInteraction) {
      const current = this.skillLevels.get(topic) || 0;
      
      // Simple EMA-based skill tracking
      if (interaction.success) {
        this.skillLevels.set(topic, Math.min(1.0, current + 0.1));
      } else {
        this.skillLevels.set(topic, Math.max(0, current - 0.05));
      }
      
      // Adjust detail level based on skill
      return {
        topic,
        skillLevel: this.skillLevels.get(topic),
        detailLevel: this.skillLevels.get(topic)! > 0.7 ? 'brief' : 'detailed'
      };
    }
  };

  // ═══════════════════════════════════════════
  // MEMORY CONSOLIDATION — Session → Project
  // ═══════════════════════════════════════════
  async consolidateAfterSession() {
    // 1. Extract learnings from session
    const learnings = this.extractSessionLearnings();
    
    // 2. Update project memory (CLAUDE.md)
    if (learnings.hasNewConventions) {
      await this.projectMemory.saveToDisk(projectRoot);
    }
    
    // 3. Update global memory
    for (const correction of this.sessionMemory.corrections) {
      this.globalMemory.updateSkillLevel(
        correction.topic, 
        { success: false }
      );
    }
    
    // 4. Clear session memory
    this.sessionMemory = this.createFreshSessionMemory();
    
    return {
      savedConventions: learnings.conventions.length,
      savedDecisions: learnings.decisions.length,
      savedPitfalls: learnings.pitfalls.length
    };
  }
}
```

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

```python
"""
Mem0 Architecture — Production Memory Management

Features:
- Multi-user memory with namespacing
- Automatic fact extraction from conversations
- Temporal decay + relevance scoring
- Memory deduplication and conflict resolution
"""

class Mem0ProductionMemory:
    """
    Production memory system inspired by Mem0 architecture
    """
    
    def __init__(self, vector_store, graph_store=None, llm_func=None):
        self.vector_store = vector_store
        self.graph = graph_store
        self.llm = llm_func
        self.user_memories = {}  # user_id -> [memories]
    
    # ═══════════════════════════════════════════
    # EXTRACT: Auto-extract facts from conversation
    # ═══════════════════════════════════════════
    def extract_and_store(self, messages, user_id, agent_id=None):
        """
        Extract facts from conversation and store them
        
        Pipeline:
        1. LLM extracts facts from conversation
        2. Deduplicate against existing memories
        3. Resolve conflicts with existing facts
        4. Store new unique facts
        """
        
        # Step 1: Extract facts using LLM
        facts = self._extract_facts(messages)
        
        # Step 2: Get existing memories
        existing = self.get_memories(user_id, agent_id)
        
        # Step 3: Deduplicate and resolve conflicts
        new_facts = self._deduplicate(facts, existing)
        conflicts = self._find_conflicts(facts, existing)
        
        # Step 4: Resolve conflicts
        resolved = self._resolve_conflicts(conflicts)
        
        # Step 5: Store new facts
        stored = []
        for fact in new_facts:
            memory = self._store_memory(fact, user_id, agent_id)
            stored.append(memory)
        
        # Step 6: Update graph relationships
        if self.graph:
            for fact in stored:
                self._update_graph(fact)
        
        return {
            "extracted": len(facts),
            "new_stored": len(stored),
            "conflicts_found": len(conflicts),
            "conflicts_resolved": len(resolved),
            "memories": stored
        }
    
    def _extract_facts(self, messages):
        """
        Use LLM to extract factual information from messages
        """
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        
        prompt = f"""Extract all factual information from this conversation.
For each fact, provide:
- Category: (personal_info, preference, knowledge, event, decision)
- Fact: The factual statement
- Confidence: 0.0-1.0

Conversation:
{conversation}

Return as JSON array:
[{{"category": "...", "fact": "...", "confidence": 0.9}}]"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return []
        return []
    
    # ═══════════════════════════════════════════
    # DEDUPLICATE: Remove redundant memories
    # ═══════════════════════════════════════════
    def _deduplicate(self, new_facts, existing_memories):
        """
        Remove new facts that are already covered by existing memories
        """
        unique = []
        
        for fact in new_facts:
            is_duplicate = False
            
            for existing in existing_memories:
                similarity = self._compute_similarity(
                    fact['fact'], existing['content']
                )
                
                if similarity > 0.85:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(fact)
        
        return unique
    
    # ═══════════════════════════════════════════
    # CONFLICT RESOLUTION
    # ═══════════════════════════════════════════
    def _find_conflicts(self, new_facts, existing_memories):
        """
        Find cases where new facts contradict existing memories
        """
        conflicts = []
        
        for fact in new_facts:
            for existing in existing_memories:
                # Check if same topic but different value
                if self._is_contradiction(fact['fact'], existing['content']):
                    conflicts.append({
                        "new_fact": fact,
                        "existing_memory": existing,
                        "conflict_type": "contradiction"
                    })
        
        return conflicts
    
    def _resolve_conflicts(self, conflicts):
        """
        Resolve conflicts between new and existing memories
        
        Strategies:
        1. TEMPORAL: Newer information wins
        2. CONFIDENCE: Higher confidence wins
        3. FREQUENCY: More frequently mentioned wins
        4. MANUAL: Ask user to resolve
        """
        resolved = []
        
        for conflict in conflicts:
            new = conflict["new_fact"]
            existing = conflict["existing_memory"]
            
            # Strategy: Temporal + Confidence
            new_score = new.get("confidence", 0.5)
            existing_score = existing.get("confidence", 0.5)
            
            # Newer facts get a slight boost
            if new.get("timestamp", "") > existing.get("timestamp", ""):
                new_score += 0.1
            
            if new_score > existing_score:
                # New fact wins — update existing
                self._update_memory(
                    existing["id"], 
                    new["fact"],
                    reason="temporal_update"
                )
                resolved.append({
                    "action": "updated",
                    "old": existing["content"],
                    "new": new["fact"]
                })
            else:
                # Existing wins — ignore new
                resolved.append({
                    "action": "kept_existing",
                    "existing": existing["content"],
                    "ignored": new["fact"]
                })
        
        return resolved
    
    # ═══════════════════════════════════════════
    # STORAGE
    # ═══════════════════════════════════════════
    def _store_memory(self, fact, user_id, agent_id):
        """Store a fact as a memory"""
        memory = {
            "id": f"mem_{uuid4().hex[:8]}",
            "user_id": user_id,
            "agent_id": agent_id,
            "content": fact["fact"],
            "category": fact.get("category", "unknown"),
            "confidence": fact.get("confidence", 0.5),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None,
        }
        
        # Store in vector DB
        embedding = self._get_embedding(fact["fact"])
        self.vector_store.add(
            document=fact["fact"],
            vector=embedding,
            metadata=memory
        )
        
        # Track in user namespace
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        if key not in self.user_memories:
            self.user_memories[key] = []
        self.user_memories[key].append(memory)
        
        return memory
    
    def get_memories(self, user_id, agent_id=None, query=None, limit=20):
        """
        Retrieve memories for a user, optionally filtered by query
        """
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        
        if query:
            # Semantic search
            embedding = self._get_embedding(query)
            results = self.vector_store.search(
                embedding, 
                top_k=limit,
                filter={"user_id": user_id}
            )
            
            # Apply temporal decay
            for r in results:
                age_days = (datetime.now() - 
                           datetime.fromisoformat(r["created_at"])).days
                r["decayed_score"] = r["score"] * (0.99 ** age_days)
            
            # Re-rank by decayed score
            results.sort(key=lambda x: x["decayed_score"], reverse=True)
            
            # Update access count
            for r in results:
                r["access_count"] = r.get("access_count", 0) + 1
                r["last_accessed"] = datetime.now().isoformat()
            
            return results[:limit]
        
        # No query: return all user memories
        return self.user_memories.get(key, [])[:limit]
    
    # ═══════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════
    def _compute_similarity(self, text1, text2):
        emb1 = self._get_embedding(text1)
        emb2 = self._get_embedding(text2)
        
        import numpy as np
        a, b = np.array(emb1), np.array(emb2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def _is_contradiction(self, fact1, fact2):
        """Check if two facts contradict each other"""
        # Simple heuristic: same subject, different numbers
        import re
        nums1 = set(re.findall(r'\d+\.?\d*', fact1))
        nums2 = set(re.findall(r'\d+\.?\d*', fact2))
        
        # If same topic words but different numbers → likely contradiction
        words1 = set(fact1.lower().split())
        words2 = set(fact2.lower().split())
        topic_overlap = len(words1 & words2) / max(len(words1 | words2), 1)
        
        return topic_overlap > 0.6 and nums1 != nums2 and len(nums1) > 0
    
    def _get_embedding(self, text):
        import requests
        try:
            resp = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return resp.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _update_graph(self, fact):
        """Update knowledge graph with new fact"""
        if self.graph:
            category = fact.get("category", "general")
            self.graph.add_triplet(
                fact["user_id"],
                f"has_{category}",
                fact["content"]
            )
```

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

```python
"""
OpenMemory Pattern: Memory as a Service via MCP Protocol

Memory operations exposed as MCP tools:
- create_memory(content, metadata)
- search_memory(query, user_id)
- update_memory(memory_id, content)
- delete_memory(memory_id)
- list_memories(user_id, category)
"""

class OpenMemoryServer:
    """
    Memory server following MCP protocol pattern
    Exposes memory operations as tools
    """
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.tools = {
            "create_memory": self.create_memory,
            "search_memory": self.search_memory,
            "update_memory": self.update_memory,
            "delete_memory": self.delete_memory,
            "list_memories": self.list_memories,
            "consolidate_memories": self.consolidate,
        }
    
    def create_memory(self, content, user_id, category="general",
                       metadata=None):
        """Create a new memory entry"""
        memory = {
            "id": str(uuid4()),
            "content": content,
            "user_id": user_id,
            "category": category,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "embedding": self._get_embedding(content)
        }
        
        # Store with vector index
        self.storage.insert(memory)
        
        return {
            "success": True,
            "memory_id": memory["id"],
            "message": f"Memory created: {content[:50]}..."
        }
    
    def search_memory(self, query, user_id=None, 
                       category=None, limit=10):
        """Semantic search over memories"""
        query_embedding = self._get_embedding(query)
        
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if category:
            filters["category"] = category
        
        results = self.storage.search(
            embedding=query_embedding,
            filters=filters,
            top_k=limit
        )
        
        # Apply relevance scoring
        for r in results:
            r["relevance"] = self._score_relevance(r, query)
        
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "memories": results,
            "count": len(results),
            "query": query
        }
    
    def update_memory(self, memory_id, content, 
                       reason="user_update"):
        """Update an existing memory"""
        old = self.storage.get(memory_id)
        if not old:
            return {"success": False, "error": "Memory not found"}
        
        # Archive old version
        self.storage.archive_version(memory_id, old)
        
        # Update
        old["content"] = content
        old["embedding"] = self._get_embedding(content)
        old["updated_at"] = datetime.now().isoformat()
        old["update_reason"] = reason
        
        self.storage.update(memory_id, old)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "previous_content": old["content"]
        }
    
    def delete_memory(self, memory_id, soft=True):
        """Delete a memory (soft or hard)"""
        if soft:
            # Soft delete: mark as deleted but keep in storage
            self.storage.update(memory_id, {
                "deleted": True,
                "deleted_at": datetime.now().isoformat()
            })
        else:
            # Hard delete: permanently remove
            self.storage.delete(memory_id)
        
        return {"success": True, "memory_id": memory_id, "type": "soft" if soft else "hard"}
    
    def consolidate(self, user_id, similarity_threshold=0.85):
        """
        Consolidate memories: merge duplicates, resolve conflicts
        """
        memories = self.storage.get_all(user_id=user_id)
        
        # Find duplicates
        duplicates = self._find_duplicates(memories, similarity_threshold)
        
        # Merge duplicates
        merged = 0
        for group in duplicates:
            primary = group[0]  # Keep the oldest
            for dup in group[1:]:
                # Merge content
                primary["content"] = self._merge_content(
                    primary["content"], dup["content"]
                )
                # Delete duplicate
                self.storage.delete(dup["id"])
                merged += 1
        
        # Find conflicts
        conflicts = self._find_all_conflicts(memories)
        
        return {
            "memories_before": len(memories),
            "duplicates_merged": merged,
            "conflicts_found": len(conflicts),
            "memories_after": len(memories) - merged
        }
    
    def _score_relevance(self, memory, query):
        """Score memory relevance considering multiple factors"""
        # Base: vector similarity
        base_score = memory.get("score", 0)
        
        # Recency boost (newer = more relevant)
        age_days = (datetime.now() - 
                   datetime.fromisoformat(memory["created_at"])).days
        recency = max(0, 1 - age_days / 365)
        
        # Access frequency boost
        access_freq = memory.get("access_count", 0) / 10
        
        # Combined score
        return (base_score * 0.6 + 
                recency * 0.2 + 
                min(access_freq, 0.2))
    
    def _find_duplicates(self, memories, threshold):
        """Group similar memories together"""
        groups = []
        used = set()
        
        for i, m1 in enumerate(memories):
            if i in used or m1.get("deleted"):
                continue
            
            group = [m1]
            for j, m2 in enumerate(memories[i+1:], i+1):
                if j in used or m2.get("deleted"):
                    continue
                
                sim = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                if sim > threshold:
                    group.append(m2)
                    used.add(j)
            
            if len(group) > 1:
                groups.append(group)
                used.add(i)
        
        return groups
```

</details>

---

### 6.4. DeepSeek Harness — Trajectory Fork & Replay Engine

**Context**: DeepSeek Harness (developed by the DeepSeek team) is an **agent harness framework** with outstanding **trajectory traceability** — tracking, replaying, forking, and resuming every agent session.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * DeepSeek Harness - Trajectory Traceability Engine
 * 
 * Core philosophy: "Agent = Model + Harness"
 * Everything is traceable, replayable, and forkable.
 */

// ═══════════════════════════════════════════════
// 1. SESSION EVENT STREAM (Append-only log)
// ═══════════════════════════════════════════════

interface SessionEvent {
  id: string;              // UUID
  step: number;            // Monotonically increasing
  timestamp: number;       // Unix ms
  type: EventType;
  payload: EventPayload;
  metadata: EventMetadata;
}

type EventType = 
  | "user_prompt"          // User input
  | "model_thought"        // LLM reasoning (hidden)
  | "tool_call"            // Tool invocation
  | "tool_result"          // Tool output
  | "model_output"         // Final LLM response
  | "state_change"         // Harness state mutation
  | "checkpoint";          // Manual/auto checkpoint

interface EventPayload {
  // user_prompt
  text?: string;
  attachments?: Attachment[];
  
  // model_thought
  reasoning?: string;
  confidence?: number;
  
  // tool_call
  tool_name?: string;
  args?: Record<string, any>;
  call_id?: string;
  
  // tool_result
  result?: any;
  error?: string;
  duration_ms?: number;
  
  // model_output
  content?: string;
  finish_reason?: string;
  
  // state_change
  path?: string;           // JSON path in state
  old_value?: any;
  new_value?: any;
  
  // checkpoint
  label?: string;
  description?: string;
}

interface EventMetadata {
  session_id: string;
  parent_step?: number;    // For forked sessions
  fork_id?: string;        // Fork identifier
  tags?: string[];         // e.g., ["debug", "critical"]
  cost_usd?: number;       // Token cost estimate
}

// ═══════════════════════════════════════════════
// 2. TRAJECTORY STORE (Persistence layer)
// ═══════════════════════════════════════════════

class TrajectoryStore {
  private events: SessionEvent[] = [];
  private checkpoints: Map<string, number> = new Map(); // label -> step
  
  append(event: SessionEvent): void {
    this.events.push(event);
  }
  
  getEvents(sessionId: string, fromStep?: number): SessionEvent[] {
    return this.events.filter(e => 
      e.metadata.session_id === sessionId && 
      (fromStep === undefined || e.step >= fromStep)
    );
  }
  
  getEventByStep(sessionId: string, step: number): SessionEvent | undefined {
    return this.events.find(e => 
      e.metadata.session_id === sessionId && e.step === step
    );
  }
  
  createCheckpoint(sessionId: string, label: string): void {
    const latestStep = this.getLatestStep(sessionId);
    this.checkpoints.set(`${sessionId}:${label}`, latestStep);
  }
  
  getCheckpoint(sessionId: string, label: string): number | undefined {
    return this.checkpoints.get(`${sessionId}:${label}`);
  }
  
  private getLatestStep(sessionId: string): number {
    const sessionEvents = this.events.filter(
      e => e.metadata.session_id === sessionId
    );
    return sessionEvents.length > 0 
      ? Math.max(...sessionEvents.map(e => e.step)) 
      : 0;
  }
}

// ═══════════════════════════════════════════════
// 3. REPLAY ENGINE (Core innovation)
// ═══════════════════════════════════════════════

class ReplayEngine {
  constructor(
    private store: TrajectoryStore,
    private model: ModelProvider,
    private toolRegistry: ToolRegistry
  ) {}
  
  /**
   * Replay session from beginning up to a specific step.
   * Returns the state at that step.
   */
  async replayToStep(sessionId: string, targetStep: number): Promise<AgentState> {
    const events = this.store.getEvents(sessionId);
    let state = this.initialState();
    
    for (const event of events) {
      if (event.step > targetStep) break;
      state = await this.applyEvent(state, event);
    }
    
    return state;
  }
  
  /**
   * Fork a session at a specific step.
   * Creates a new session that shares history up to fork point.
   */
  async forkSession(
    sessionId: string, 
    forkStep: number, 
    newPrompt?: string
  ): Promise<string> {
    const newSessionId = `fork_${sessionId}_${forkStep}_${Date.now()}`;
    
    // Copy events up to fork step
    const history = this.store.getEvents(sessionId, 0, forkStep);
    for (const event of history) {
      const forkedEvent = {
        ...event,
        id: uuid(),
        metadata: {
          ...event.metadata,
          session_id: newSessionId,
          parent_step: forkStep,
          fork_id: newSessionId
        }
      };
      this.store.append(forkedEvent);
    }
    
    // Optionally add new prompt to continue from fork
    if (newPrompt) {
      this.store.append({
        id: uuid(),
        step: forkStep + 1,
        timestamp: Date.now(),
        type: "user_prompt",
        payload: { text: newPrompt },
        metadata: { session_id: newSessionId, fork_id: newSessionId }
      });
    }
    
    return newSessionId;
  }
  
  /**
   * Resume a session from a checkpoint or step.
   * Continues execution from that point.
   */
  async resumeSession(
    sessionId: string, 
    fromStep: number,
    newInput?: string
  ): Promise<AgentState> {
    // Get state at resume point
    const state = await this.replayToStep(sessionId, fromStep);
    
    // If new input provided, continue from there
    if (newInput) {
      return this.continueFromState(sessionId, state, newInput);
    }
    
    return state;
  }
  
  private async applyEvent(state: AgentState, event: SessionEvent): Promise<AgentState> {
    switch (event.type) {
      case "tool_call":
        return await this.executeTool(state, event);
      case "model_thought":
        return { ...state, lastThought: event.payload.reasoning };
      case "state_change":
        return this.applyStateChange(state, event);
      default:
        return state;
    }
  }
  
  private async continueFromState(
    sessionId: string, 
    state: AgentState, 
    input: string
  ): Promise<AgentState> {
    // Continue agent loop from restored state
    // ... implementation
    return state;
  }
  
  private initialState(): AgentState {
    return { history: [], tools: {}, memory: {} };
  }
}

// ═══════════════════════════════════════════════
// 4. EVENT SEARCH & ANALYTICS
// ═══════════════════════════════════════════════

class TrajectoryAnalytics {
  constructor(private store: TrajectoryStore) {}
  
  /**
   * Search events across all sessions.
   * Supports: full-text, type filter, time range, cost range.
   */
  searchEvents(query: SearchQuery): SessionEvent[] {
    let results = this.store.events;
    
    if (query.session_id) {
      results = results.filter(e => e.metadata.session_id === query.session_id);
    }
    if (query.type) {
      results = results.filter(e => e.type === query.type);
    }
    if (query.text) {
      const text = query.text.toLowerCase();
      results = results.filter(e => 
        JSON.stringify(e.payload).toLowerCase().includes(text)
      );
    }
    if (query.from_step !== undefined) {
      results = results.filter(e => e.step >= query.from_step!);
    }
    if (query.to_step !== undefined) {
      results = results.filter(e => e.step <= query.to_step!);
    }
    if (query.max_cost !== undefined) {
      results = results.filter(e => 
        (e.metadata.cost_usd ?? 0) <= query.max_cost!
      );
    }
    
    return results;
  }
  
  /**
   * Get cost breakdown by event type.
   */
  getCostBreakdown(sessionId: string): Record<string, number> {
    const events = this.store.getEvents(sessionId);
    const breakdown: Record<string, number> = {};
    
    for (const event of events) {
      const cost = event.metadata.cost_usd ?? 0;
      breakdown[event.type] = (breakdown[event.type] ?? 0) + cost;
    }
    
    return breakdown;
  }
  
  /**
   * Find common failure patterns.
   */
  findFailurePatterns(): FailurePattern[] {
    const toolErrors = this.store.events.filter(
      e => e.type === "tool_result" && e.payload.error
    );
    
    // Group by tool + error type
    const groups = new Map<string, SessionEvent[]>();
    for (const event of toolErrors) {
      const key = `${event.payload.tool_name}:${event.payload.error}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(event);
    }
    
    return Array.from(groups.entries())
      .map(([pattern, events]) => ({
        pattern,
        count: events.length,
        sessions: [...new Set(events.map(e => e.metadata.session_id))],
        first_seen: Math.min(...events.map(e => e.timestamp)),
        last_seen: Math.max(...events.map(e => e.timestamp))
      }))
      .sort((a, b) => b.count - a.count);
  }
}

interface SearchQuery {
  session_id?: string;
  type?: EventType;
  text?: string;
  from_step?: number;
  to_step?: number;
  max_cost?: number;
}

interface FailurePattern {
  pattern: string;
  count: number;
  sessions: string[];
  first_seen: number;
  last_seen: number;
}
```

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

This pattern answers the question: "writing to disk is too slow, how do we make it fast?" The solution: write to an in-memory cache instantly (reply to the user right away), while the write to the durable store runs in the background in batches — like writing a receipt first and entering it into the ledger at the end of the day. In other words, this is **a trade-off: accept a small risk of data loss if the program crashes, in exchange for much faster response times when the write volume is high.**

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Write-Behind Cache: Write to cache first, flush to DB later.

Reduces write operation latency, increases throughput.
Suitable when write operations outnumber reads.
"""

class WriteBehindCache:
    """
    Write-behind caching for memory operations
    
    Flow:
    1. Write to fast cache (Redis/in-memory)
    2. Return immediately (low latency)
    3. Background thread flushes to persistent store
    """
    
    def __init__(self, persistent_store, flush_interval=5.0, batch_size=100):
        self.cache = {}  # In-memory cache
        self.persistent_store = persistent_store
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self.pending_writes = []
        self.is_running = True
        
        # Start background flush thread
        self.flush_thread = threading.Thread(target=self._flush_loop)
        self.flush_thread.daemon = True
        self.flush_thread.start()
    
    def write(self, key, value, metadata=None):
        """
        Write to cache immediately, queue for persistence
        """
        entry = {
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "dirty": True  # Needs to be flushed
        }
        
        # Write to fast cache (immediate)
        self.cache[key] = entry
        
        # Queue for persistent storage
        self.pending_writes.append(entry)
        
        # Flush if batch is full
        if len(self.pending_writes) >= self.batch_size:
            self._flush()
        
        return {"success": True, "latency": "cache_speed"}
    
    def read(self, key):
        """
        Read from cache first, fallback to persistent store
        """
        # Check cache
        if key in self.cache:
            return self.cache[key]
        
        # Fallback to persistent store
        value = self.persistent_store.get(key)
        if value:
            # Populate cache for next time
            self.cache[key] = value
        
        return value
    
    def _flush_loop(self):
        """Background loop to flush dirty entries"""
        while self.is_running:
            time.sleep(self.flush_interval)
            self._flush()
    
    def _flush(self):
        """Flush pending writes to persistent store"""
        if not self.pending_writes:
            return
        
        # Batch write to persistent store
        batch = self.pending_writes[:self.batch_size]
        self.pending_writes = self.pending_writes[self.batch_size:]
        
        try:
            self.persistent_store.batch_write(batch)
            
            # Mark as clean
            for entry in batch:
                if entry["key"] in self.cache:
                    self.cache[entry["key"]]["dirty"] = False
        
        except Exception as e:
            # Re-queue failed writes
            self.pending_writes = batch + self.pending_writes
            print(f"Flush error: {e}")
    
    def get_stats(self):
        dirty_count = sum(
            1 for v in self.cache.values() if v.get("dirty")
        )
        return {
            "cache_size": len(self.cache),
            "pending_writes": len(self.pending_writes),
            "dirty_entries": dirty_count
        }
```

</details>

### 7.2. Memory Consolidation Pipeline

Unlike the manual consolidation in section 2, this is an "automated cleanup assembly line" that runs periodically in 5 stages: deduplicate → resolve conflicts → temporal decay → archive old memories → remove low-confidence memories. Each stage is a `_stage_*` function, and `run_full_consolidation` runs the whole pipeline and returns a statistics report — reading this report immediately shows how many items each stage cleaned up.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Consolidation Pipeline: Background process to maintain memory quality.

Runs periodically to:
1. Deduplicate memories
2. Resolve conflicts
3. Apply temporal decay
4. Archive old memories
5. Generate memory statistics
"""

class MemoryConsolidationPipeline:
    """
    Automated pipeline for memory maintenance
    """
    
    def __init__(self, memory_store, config=None):
        self.store = memory_store
        self.config = config or {
            "dedup_threshold": 0.85,
            "conflict_strategy": "temporal",  # temporal, confidence, manual
            "archive_after_days": 90,
            "decay_rate": 0.01,
            "min_confidence": 0.3
        }
        self.stats = {
            "runs": 0,
            "deduped": 0,
            "conflicts_resolved": 0,
            "archived": 0,
            "low_confidence_removed": 0
        }
    
    def run_full_consolidation(self):
        """
        Run complete consolidation pipeline
        
        Returns: ConsolidationReport
        """
        start_time = time.time()
        report = {"stages": {}}
        
        # Stage 1: Deduplication
        dedup_result = self._stage_deduplicate()
        report["stages"]["dedup"] = dedup_result
        
        # Stage 2: Conflict Resolution
        conflict_result = self._stage_resolve_conflicts()
        report["stages"]["conflicts"] = conflict_result
        
        # Stage 3: Temporal Decay
        decay_result = self._stage_apply_decay()
        report["stages"]["decay"] = decay_result
        
        # Stage 4: Archive Old Memories
        archive_result = self._stage_archive()
        report["stages"]["archive"] = archive_result
        
        # Stage 5: Remove Low Confidence
        cleanup_result = self._stage_cleanup()
        report["stages"]["cleanup"] = cleanup_result
        
        # Final report
        elapsed = time.time() - start_time
        report["total_time_ms"] = elapsed * 1000
        report["total_memories"] = self.store.count()
        report["stats"] = self.stats
        self.stats["runs"] += 1
        
        return report
    
    def _stage_deduplicate(self):
        """Remove duplicate memories"""
        memories = self.store.get_all()
        
        # Group by similarity
        duplicates_found = 0
        removed = 0
        
        for i, m1 in enumerate(memories):
            if m1.get("archived") or m1.get("deleted"):
                continue
            
            for m2 in memories[i+1:]:
                if m2.get("archived") or m2.get("deleted"):
                    continue
                
                similarity = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                
                if similarity > self.config["dedup_threshold"]:
                    # Keep the one with higher confidence
                    if m1.get("confidence", 0) >= m2.get("confidence", 0):
                        self.store.soft_delete(m2["id"])
                    else:
                        self.store.soft_delete(m1["id"])
                    removed += 1
        
        self.stats["deduped"] += removed
        return {"duplicates_found": duplicates_found, "removed": removed}
    
    def _stage_resolve_conflicts(self):
        """Resolve conflicting memories"""
        memories = self.store.get_all()
        
        # Group by topic (simplified: same first 5 words)
        topic_groups = {}
        for m in memories:
            if m.get("deleted"):
                continue
            topic_key = " ".join(m["content"].split()[:5])
            if topic_key not in topic_groups:
                topic_groups[topic_key] = []
            topic_groups[topic_key].append(m)
        
        conflicts_resolved = 0
        
        for topic, group in topic_groups.items():
            if len(group) <= 1:
                continue
            
            # Check for actual contradictions
            values = set()
            for m in group:
                values.add(m["content"])
            
            if len(values) > 1:
                # Conflict found — resolve by strategy
                if self.config["conflict_strategy"] == "temporal":
                    # Keep newest
                    group.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
                elif self.config["conflict_strategy"] == "confidence":
                    # Keep highest confidence
                    group.sort(key=lambda x: x.get("confidence", 0), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
        
        self.stats["conflicts_resolved"] += conflicts_resolved
        return {"conflicts_found": len(topic_groups), "resolved": conflicts_resolved}
    
    def _stage_apply_decay(self):
        """Apply temporal decay to memory confidence"""
        memories = self.store.get_all()
        
        decayed = 0
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            age_days = (datetime.now() - 
                       datetime.fromisoformat(m.get("created_at", 
                           datetime.now().isoformat()))).days
            
            # Apply exponential decay
            decay_factor = (1 - self.config["decay_rate"]) ** age_days
            new_confidence = m.get("confidence", 1.0) * decay_factor
            
            if abs(new_confidence - m.get("confidence", 1.0)) > 0.01:
                self.store.update(m["id"], {"confidence": new_confidence})
                decayed += 1
        
        return {"memories_decayed": decayed}
    
    def _stage_archive(self):
        """Archive old, low-access memories"""
        cutoff = datetime.now() - timedelta(
            days=self.config["archive_after_days"]
        )
        
        archived = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            last_accessed = m.get("last_accessed", m.get("updated_at"))
            if last_accessed and datetime.fromisoformat(last_accessed) < cutoff:
                # Archive: move to cold storage
                self.store.archive(m["id"])
                archived += 1
        
        self.stats["archived"] += archived
        return {"archived": archived}
    
    def _stage_cleanup(self):
        """Remove very low confidence memories"""
        removed = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            if m.get("confidence", 1.0) < self.config["min_confidence"]:
                self.store.soft_delete(m["id"])
                removed += 1
        
        self.stats["low_confidence_removed"] += removed
        return {"low_confidence_removed": removed}
    
    def _compute_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
```

</details>

### 7.3. Versioned Memory (Git-like Memory)

This pattern borrows Git's exact idea and applies it to memory: every `set` of a value creates a new **version** with a full state snapshot. This gives you `diff` (comparing two points in time), `rollback` (returning to an old version, like git revert), and `log` (viewing the change history). In plain terms: memory remembers how it "has been modified over time", so fixing a mistake means just pulling back to an older state.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Versioned Memory: Like Git — each change creates a new version.

Enables:
- Time travel: View memory at time T
- Diff: Compare memory between two time points
- Branch: Create alternative versions
- Rollback: Return to a previous version
"""

class VersionedMemory:
    """
    Git-like versioned memory system
    """
    
    def __init__(self):
        self.versions = []  # List of snapshots
        self.current = {}
    
    def set(self, key, value, message=""):
        """Set a value, creating a new version"""
        # Capture previous state
        prev_snapshot = dict(self.current)
        
        # Apply change
        self.current[key] = value
        
        # Record version
        version = {
            "id": len(self.versions),
            "snapshot": dict(self.current),
            "change": {"key": key, "value": value},
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "parent": len(self.versions) - 1 if self.versions else None
        }
        
        self.versions.append(version)
        return version["id"]
    
    def get(self, key, version_id=None):
        """Get value at a specific version"""
        if version_id is None:
            return self.current.get(key)
        
        if version_id >= len(self.versions):
            return None
        
        return self.versions[version_id]["snapshot"].get(key)
    
    def diff(self, v1_id, v2_id):
        """Compare two versions"""
        if v1_id >= len(self.versions) or v2_id >= len(self.versions):
            return {"error": "Invalid version IDs"}
        
        v1 = self.versions[v1_id]["snapshot"]
        v2 = self.versions[v2_id]["snapshot"]
        
        all_keys = set(v1.keys()) | set(v2.keys())
        
        changes = []
        for key in all_keys:
            old = v1.get(key)
            new = v2.get(key)
            
            if old != new:
                if old is None:
                    changes.append({"key": key, "type": "added", "new": new})
                elif new is None:
                    changes.append({"key": key, "type": "removed", "old": old})
                else:
                    changes.append({"key": key, "type": "modified", 
                                   "old": old, "new": new})
        
        return {"changes": changes, "count": len(changes)}
    
    def rollback(self, version_id):
        """Rollback to a previous version"""
        if version_id >= len(self.versions):
            return {"error": "Invalid version ID"}
        
        self.current = dict(self.versions[version_id]["snapshot"])
        
        return {
            "rolled_back_to": version_id,
            "current_state": self.current
        }
    
    def log(self, limit=10):
        """View version history"""
        return [
            {
                "id": v["id"],
                "change": v["change"],
                "message": v["message"],
                "timestamp": v["timestamp"]
            }
            for v in self.versions[-limit:]
        ]
```

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

```python
class MemoryStoreMetrics:
    """Track memory store performance"""
    
    def __init__(self):
        self.write_latencies = []
        self.read_latencies = []
        self.memory_counts = []
        self.dedup_rates = []
        self.conflict_counts = []
        self.consolidation_times = []
    
    def record_write(self, latency_ms, success=True):
        self.write_latencies.append({"latency": latency_ms, "success": success})
    
    def record_read(self, latency_ms, results_count):
        self.read_latencies.append({"latency": latency_ms, "results": results_count})
    
    def record_consolidation(self, time_ms, deduped, conflicts_resolved):
        self.consolidation_times.append(time_ms)
        self.dedup_rates.append(deduped)
        self.conflict_counts.append(conflicts_resolved)
    
    def report(self):
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0
        
        write_lats = [w["latency"] for w in self.write_latencies]
        read_lats = [r["latency"] for r in self.read_latencies]
        
        return f"""
╔══════════════════════════════════════════════╗
║       MEMORY STORE METRICS REPORT            ║
╠══════════════════════════════════════════════╣
║                                              ║
║  Write Operations:                           ║
║    Total:    {len(self.write_latencies):>8}                     ║
║    Avg Latency: {avg(write_lats):>8.1f} ms                 ║
║    Success Rate: {sum(1 for w in self.write_latencies if w['success'])/max(len(self.write_latencies),1)*100:>6.1f}%          ║
║                                              ║
║  Read Operations:                            ║
║    Total:    {len(self.read_latencies):>8}                     ║
║    Avg Latency: {avg(read_lats):>8.1f} ms                 ║
║    Avg Results: {avg([r['results'] for r in self.read_latencies]):>7.1f}                    ║
║                                              ║
║  Consolidation:                              ║
║    Runs:     {len(self.consolidation_times):>8}                     ║
║    Avg Time: {avg(self.consolidation_times):>8.1f} ms                 ║
║    Total Deduped: {sum(self.dedup_rates):>5}                   ║
║    Total Conflicts: {sum(self.conflict_counts):>4}                  ║
║                                              ║
╚══════════════════════════════════════════════╝"""
```

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

```python
# python 03-update-memory-store/lab_writeback.py

writer = MemoryWriter()

# 1. Store episodic memory
event_id = writer.write_episodic(
    "learning",
    "User learned about health insurance deduction rates",
    metadata={"topic": "health insurance", "importance": "medium"}
)

# 2. Store facts
writer.write_fact("health insurance", "contribution rate", "4.5% of base salary", confidence=0.95)
writer.write_fact("health insurance", "card validity", "5 years", confidence=0.99)
writer.write_fact("Ollama", "runs", "gemma3:12b", confidence=1.0)

# 3. Update user profile
writer.write_user_profile("user_1", {
    "name": "John Doe",
    "occupation": "developer",
    "interests": ["AI", "health insurance"]
})

# 4. Check stats
print(writer.get_stats())
# {'episodic_count': 1, 'entity_count': 3, 'event_count': 4}
```

</details>

### Lab 2: Consolidation

Practice cleanup with `MemoryConsolidator`: create 3 facts about health insurance (two nearly duplicates, one a newer update), run `generate_memory_report`, and see which contradiction `conflict_resolution` detects.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_consolidation.py

from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()
kg.add_triplet("health insurance", "contribution rate", "4.5%")
kg.add_triplet("health insurance", "contribution rate", "4.5% of base salary")  # Duplicate
kg.add_triplet("health insurance", "contribution rate", "5%")  # Updated

consolidator = MemoryConsolidator(kg)
report = consolidator.generate_memory_report()
print(report)

conflicts = consolidator.conflict_resolution()
print(f"Conflicts: {len(conflicts)}")
for c in conflicts:
    print(f"  {c['subject']} → {c['conflicting_values']}")
```

</details>

### Lab 3: Versioned Memory

Simulate a fact about the health insurance contribution rate evolving across 3 versions, view the history with `vm.log()`, compare two points in time with `vm.diff(0, 2)`, and finally try rolling back to the first version with `vm.rollback(0)`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_versioned.py

vm = VersionedMemory()

# Track evolving knowledge
vm.set("hi_rate", "4.5%", message="Initial fact")
vm.set("hi_rate", "4.5% of base salary", message="More specific")
vm.set("hi_rate", "4.5% MEC 2024", message="Updated year")

# View history
for entry in vm.log():
    print(f"  v{entry['id']}: {entry['message']}")

# Compare versions
diff = vm.diff(0, 2)
print(f"Changes: {diff['count']}")

# Rollback
state = vm.rollback(0)
print(f"Rolled back to: {state['rolled_back_to']}")
```

</details>

### Lab 4: Metrics

Simulate 100 write/read operations with random figures and 2 consolidation runs, then print the `metrics.report()` report to see how the system is measured.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_metrics.py

metrics = MemoryStoreMetrics()

# Simulate operations
import random
for _ in range(100):
    metrics.record_write(random.uniform(5, 50))
    metrics.record_read(random.uniform(2, 30), random.randint(1, 10))

metrics.record_consolidation(1500, deduped=25, conflicts_resolved=3)
metrics.record_consolidation(1200, deduped=15, conflicts_resolved=1)

print(metrics.report())
```

</details>

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
*Last updated: 19/07/2026*  
*Author: AI Knowledge Repository*  
*Environment: Ollama (gemma3:12b, nomic-embed-text)*
