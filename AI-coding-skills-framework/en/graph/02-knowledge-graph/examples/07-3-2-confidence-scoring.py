def filter_by_confidence(relations: list, threshold: float = 0.7) -> list:
    """Keep only relations with confidence >= threshold."""
    filtered = [r for r in relations if r.get("confidence", 0) >= threshold]
    print(f"Filtered: {len(relations)} -> {len(filtered)} (threshold={threshold})")
    return filtered
