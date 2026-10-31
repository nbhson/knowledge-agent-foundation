def is_active(edge, today):
    start, end = edge["valid"]
    return start <= today and (end == "now" or today < end)

live = [e for e in edges if is_active(e, "2026-10-03")]
