import json
from datetime import datetime

# ============================================================
# PATTERN 1: Citation-based Context
# ============================================================
def build_citation_context(documents):
    """
    Gán số nguồn [1], [2], [3]... cho mỗi document
    
    Phù hợp khi cần trích dẫn nguồn trong câu trả lời
    """
    context_parts = []
    for i, doc in enumerate(documents, 1):
        source = doc.get("source", "unknown")
        date = doc.get("date", "")
        content = doc["content"]
        context_parts.append(
            f"[{i}] ({source}, {date})\n{content}"
        )
    
    return "TÀI LIỆU THAM KHẢO:\n" + "\n\n".join(context_parts)


# ============================================================
# PATTERN 2: Relevance-ranked Context
# ============================================================
def build_ranked_context(documents, scores):
    """
    Sắp xếp context theo mức độ liên quan
    
    Thông tin quan trọng nhất ở đầu và cuối (tránh "lost in middle")
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
        context.append("🔴 THÔNG TIN QUAN TRỌNG NHẤT:")
        for doc, score in high:
            context.append(f"  • {doc['content']}")
    
    if medium:
        context.append("\n🟡 THÔNG TIN BỔ SUNG:")
        for doc, score in medium:
            context.append(f"  • {doc['content']}")
    
    if low:
        context.append("\n🔵 THÔNG TIN LIÊN QUAN:")
        for doc, score in low:
            context.append(f"  • {doc['content']}")
    
    return "\n".join(context)


# ============================================================
# PATTERN 3: Categorized Context
# ============================================================
def build_categorized_context(documents):
    """
    Phân loại context theo chủ đề/loại
    
    Giúp LLM dễ dàng tìm thông tin theo category
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
    Xây context theo cuộc trò chuyện hiện tại
    
    Kết hợp: user profile + chat history + retrieved docs
    """
    parts = []
    
    # User profile (if available)
    if user_profile:
        parts.append("👤 VỀ NGƯỜI DÙNG:")
        parts.append(f"  Tên: {user_profile.get('name', 'N/A')}")
        parts.append(f"  Sở thích: {', '.join(user_profile.get('interests', []))}")
        parts.append(f"  Ngôn ngữ: {user_profile.get('language', 'vi')}")
        parts.append("")
    
    # Recent conversation
    if chat_history:
        parts.append("💬 CUỘC TRÒ CHUYỆN GẦN ĐÂY:")
        for msg in chat_history[-5:]:  # Last 5 messages
            role = "👤" if msg["role"] == "user" else "🤖"
            parts.append(f"  {role} {msg['content'][:100]}")
        parts.append("")
    
    # Retrieved documents
    if docs:
        parts.append(f"📚 THÔNG TIN THAM KHẢO ({len(docs)} nguồn):")
        for i, doc in enumerate(docs, 1):
            relevance = doc.get("score", 0)
            parts.append(f"  [{i}] (liên quan: {relevance:.0%}) {doc['content']}")
        parts.append("")
    
    parts.append(f"❓ CÂU HỎI HIỆN TẠI: {query}")
    
    return "\n".join(parts)


# ============================================================
# PATTERN 5: Multi-source Context
# ============================================================
def build_multisource_context(sources):
    """
    Kết hợp nhiều nguồn thông tin khác nhau
    
    sources: dict of {source_name: [documents]}
    
    Ví dụ:
    - Official docs (ưu tiên cao nhất)
    - Expert analysis
    - User data
    - Web search results
    """
    priority_order = ["official", "expert", "database", "web", "general"]
    
    parts = []
    parts.append("Bạn có quyền truy cập các nguồn sau (ưu tiên giảm dần):")
    parts.append("")
    
    for source_name in priority_order:
        if source_name in sources:
            docs = sources[source_name]
            parts.append(f"=== Nguồn: {source_name.upper()} (ưu tiên: {priority_order.index(source_name)+1}) ===")
            for doc in docs:
                parts.append(f"  • {doc}")
            parts.append("")
    
    parts.append("HƯỚNG DẪN: Ưu tiên thông tin từ nguồn oficial, "
                 "sau đó đến expert, rồi đến các nguồn khác.")
    
    return "\n".join(parts)


# ============================================================
# USAGE EXAMPLE
# ============================================================
if __name__ == "__main__":
    # Sample documents
    docs = [
        {"content": "BHYT là bảo hiểm bắt buộc", "source": "Luật BHYT", 
         "category": "legal", "score": 0.95},
        {"content": "Mức đóng 4.5% lương cơ sở", "source": "QĐ 105", 
         "category": "finance", "score": 0.88},
        {"content": "Thẻ BHYT có hiệu lực 5 năm", "source": "Luật BHYT", 
         "category": "legal", "score": 0.72},
        {"content": "Khám tại tuyến huyện trở lên", "source": "Hướng dẫn", 
         "category": "medical", "score": 0.65},
    ]
    
    print("=== Citation Context ===")
    print(build_citation_context(docs))
    
    print("\n=== Categorized Context ===")
    print(build_categorized_context(docs))
