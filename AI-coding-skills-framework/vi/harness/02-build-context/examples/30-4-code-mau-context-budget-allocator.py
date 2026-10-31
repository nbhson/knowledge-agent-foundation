def allocate_context_budget(
    components: dict[str, str],   # system / goal / retrieved / history / immediate
    total_budget: int = 8_000,
    ratios: dict[str, float] | None = None,
) -> dict[str, str]:
    """Chia ngân sách token theo %, cắt ưu tiên thấp trước khi tràn.

    Pin set (system + goal) không bao giờ bị cắt — xem module 14-compaction-context.
    """
    ratios = ratios or {
        "system": 0.15, "goal": 0.10,       # pin set — không cắt
        "retrieved": 0.40, "history": 0.25, "immediate": 0.10,
    }
    evict_order = ["history", "retrieved", "immediate"]   # cắt ưu tiên thấp trước
    parts, used = {}, 0
    for name, text in components.items():
        cap = int(total_budget * ratios.get(name, 0.10))
        parts[name] = text[:cap]
        used += min(len(text), cap)

    i = 0
    while used > total_budget and i < len(evict_order):    # vượt budget → cắt dần
        key = evict_order[i]
        if key in components:
            used -= len(parts[key]) - len(parts[key]) // 2
            parts[key] = parts[key][: len(parts[key]) // 2]  # cắt nửa sau
        i += 1
    return parts

# Usage
ctx = allocate_context_budget({
    "system": SYSTEM_PROMPT, "goal": TASK_GOAL,
    "retrieved": docs_text, "history": chat_text, "immediate": current_file_text,
})
prompt = "\n\n".join(ctx.values())
