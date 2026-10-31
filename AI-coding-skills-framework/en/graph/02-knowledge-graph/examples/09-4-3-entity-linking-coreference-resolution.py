# Coreference in text: "Alice signed the contract. She delivered 200m."
# → "She" = Alice (coreference)
# → "Alice" (written "A. Nguyen" in another doc) = the existing Alice node (entity linking)

def entity_linking(mention: str, graph_entities: list[str], embedding_fn) -> str:
    """Link a mention ('A. Nguyen') to the canonical entity via similarity."""
    best, best_score = None, 0
    v_mention = embedding_fn(mention)
    for ent in graph_entities:
        score = cosine(v_mention, embedding_fn(ent))
        if score > best_score:
            best, best_score = ent, score
    return best if best_score > 0.85 else None   # below threshold → NEW entity
