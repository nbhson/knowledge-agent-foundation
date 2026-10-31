# Coreference trong text: "Alice ký hợp đồng. Cô ấy giao 200m." 
# → "Cô ấy" = Alice (coreference)
# → "Alice" (doc khác viết "A. Nguyen") = node Alice đang tồn tại (entity linking)

def entity_linking(mention: str, graph_entities: list[str], embedding_fn) -> str:
    """Gắn mention ('A. Nguyen') về canonical entity bằng similarity."""
    best, best_score = None, 0
    v_mention = embedding_fn(mention)
    for ent in graph_entities:
        score = cosine(v_mention, embedding_fn(ent))
        if score > best_score:
            best, best_score = ent, score
    return best if best_score > 0.85 else None   # dưới ngưỡng → entity MỚI
