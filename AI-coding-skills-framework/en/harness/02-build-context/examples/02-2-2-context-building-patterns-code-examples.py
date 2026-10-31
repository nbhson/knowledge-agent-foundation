import json
from datetime import datetime

# ============================================================
# PATTERN 1: Citation-based Context
# ============================================================
def build_citation_context(documents):
    """
    Assign source numbers [1], [2], [3]... to each document

    Suitable when the answer must cite its sources
    """
    context_parts = []
    for i, doc in enumerate(documents, 1):
        source = doc.get("source", "unknown")
        date = doc.get("date", "")
        content = doc["content"]
        context_parts.append(
            f"[{i}] ({source}, {date})\n{content}"
        )
    
    return "REFERENCE DOCUMENTS:\n" + "\n\n".join(context_parts)


# ============================================================
# PATTERN 2: Relevance-ranked Context
# ============================================================
def build_ranked_context(documents, scores):
    """
    Arrange the context by relevance

    Most important information at the beginning and end (avoids "lost in middle")
    """
    ranked = sorted(
        zip(documents, scores), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    context = []
    
    # Group by relevance level
    high = [(d, s) for d, s in ranked if s > 0.8]
    medium = [(d, s) for d, s in ranked if 0.5 < s <= 0.8]
    low = [(d, s) for d, s in ranked if s <= 0.5]
    
    if high:
        context.append("🔴 MOST IMPORTANT INFORMATION:")
        for doc, score in high:
            context.append(f"  • {doc['content']}")
    
    if medium:
        context.append("\n🟡 SUPPLEMENTARY INFORMATION:")
        for doc, score in medium:
            context.append(f"  • {doc['content']}")
    
    if low:
        context.append("\n🔵 RELATED INFORMATION:")
        for doc, score in low:
            context.append(f"  • {doc['content']}")
    
    return "\n".join(context)


# ============================================================
# PATTERN 3: Categorized Context
# ============================================================
def build_categorized_context(documents):
    """
    Categorize the context by topic/type

    Helps the LLM find information easily by category
    """
    categories = {}
    for doc in documents:
        cat = doc.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(doc)
    
    parts = []
    for cat_name, docs in sorted(categories.items()):
        parts.append(f"## {cat_name.upper()}")
        for doc in docs:
            parts.append(f"- {doc['content']}")
        parts.append("")  # blank line
    
    return "\n".join(parts)


# ============================================================
# PATTERN 4: Conversation-aware Context
# ============================================================
def build_conversational_context(query, docs, chat_history, user_profile=None):
    """
    Build context around the current conversation

    Combines: user profile + chat history + retrieved docs
    """
    parts = []
    
    # User profile (if available)
    if user_profile:
        parts.append("👤 ABOUT THE USER:")
        parts.append(f"  Name: {user_profile.get('name', 'N/A')}")
        parts.append(f"  Interests: {', '.join(user_profile.get('interests', []))}")
        parts.append(f"  Language: {user_profile.get('language', 'en')}")
        parts.append("")
    
    # Recent conversation
    if chat_history:
        parts.append("💬 RECENT CONVERSATION:")
        for msg in chat_history[-5:]:  # Last 5 messages
            role = "👤" if msg["role"] == "user" else "🤖"
            parts.append(f"  {role} {msg['content'][:100]}")
        parts.append("")
    
    # Retrieved documents
    if docs:
        parts.append(f"📚 REFERENCE INFORMATION ({len(docs)} sources):")
        for i, doc in enumerate(docs, 1):
            relevance = doc.get("score", 0)
            parts.append(f"  [{i}] (relevance: {relevance:.0%}) {doc['content']}")
        parts.append("")
    
    parts.append(f"❓ CURRENT QUESTION: {query}")
    
    return "\n".join(parts)


# ============================================================
# PATTERN 5: Multi-source Context
# ============================================================
def build_multisource_context(sources):
    """
    Combine multiple different information sources

    sources: dict of {source_name: [documents]}

    Example:
    - Official docs (highest priority)
    - Expert analysis
    - User data
    - Web search results
    """
    priority_order = ["official", "expert", "database", "web", "general"]
    
    parts = []
    parts.append("You have access to the following sources (priority in descending order):")
    parts.append("")
    
    for source_name in priority_order:
        if source_name in sources:
            docs = sources[source_name]
            parts.append(f"=== Source: {source_name.upper()} (priority: {priority_order.index(source_name)+1}) ===")
            for doc in docs:
                parts.append(f"  • {doc}")
            parts.append("")
    
    parts.append("GUIDANCE: Prioritize information from official sources, "
                 "then from experts, then from the other sources.")
    
    return "\n".join(parts)


# ============================================================
# USAGE EXAMPLE
# ============================================================
if __name__ == "__main__":
    # Sample documents
    docs = [
        {"content": "Health insurance is mandatory", "source": "Health Insurance Law", 
         "category": "legal", "score": 0.95},
        {"content": "Contribution level is 4.5% of base salary", "source": "Decree 105", 
         "category": "finance", "score": 0.88},
        {"content": "Insurance cards are valid for 5 years", "source": "Health Insurance Law", 
         "category": "legal", "score": 0.72},
        {"content": "See a doctor at district level or above", "source": "Guidelines", 
         "category": "medical", "score": 0.65},
    ]
    
    print("=== Citation Context ===")
    print(build_citation_context(docs))
    
    print("\n=== Categorized Context ===")
    print(build_categorized_context(docs))
