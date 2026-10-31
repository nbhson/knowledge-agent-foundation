COMPACT_RATIO = 0.70          # trigger: 70% ngân sách
MAX_RECENT_FILES = 5          # giữ 5 file gần nhất được truy cập (Claude Code)
RESUME_BUDGET = 300           # token cho resume block

def should_compact(tokens_used: int, limit: int) -> bool:
    """Trigger compaction khi sử dụng > 70% ngân sách."""
    return (tokens_used / limit) > COMPACT_RATIO


def compact(messages: list[dict], recent_files: list[str] | None = None) -> str:
    """Tóm tắt lịch sử hội thoại, giữ 5 file gần nhất.

    Args:
        messages: lịch sử hội thoại
        recent_files: danh sách file gần nhất được truy cập (mặc định giữ 5)
    Returns:
        Resume block dạng text, ≤ RESUME_BUDGET tokens
    """
    if recent_files is None:
        recent_files = []
    recent_files = recent_files[-MAX_RECENT_FILES:]

    # 1. Filter: tool results cũ deep trong history
    kept = [m for m in messages if m.get("role") != "tool" or m.get("keep")]

    # 2. Gộp lại messages còn lại (nếu nhiều → summarize)
    total = sum(len(str(m.get("content", ""))) for m in kept)
    if total > RESUME_BUDGET * 4:   # rough: ~4 chars/token
        # Ưu tiên: goal + quyết định + unresolved + next + recent_files
        summary_parts = [
            "Goal: [trích nhiệm vụ hiện tại từ system/goal messages]",
            "Decisions: [các quyết định đã đưa ra]",
            "Open issues: [bug/task chưa giải quyết]",
            "Next: [bước kế tiếp]",
            f"Recent files: {', '.join(recent_files)}",
        ]
        return "\n".join(summary_parts)
    return "\n".join(str(m.get("content", "")) for m in kept[-10:])
