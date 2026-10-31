import numpy as np

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def embed(text: str, model: str = "nomic-embed-text") -> list[float]:
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={"model": model, "input": text})
    return resp.json()["embeddings"][0]

def deduplicate_entities(entities: list, threshold: float = 0.85) -> list:
    """
    Merge duplicate entities based on embedding similarity.
    Keep the first entity as the canonical one.
    """
    if not entities:
        return []
    
    # Embed each entity name
    embeddings = [embed(e["name"]) for e in entities]
    
    canonical = []  # list of (entity, embedding)
    mapping = {}    # old_name -> canonical_name
    
    for ent, emb in zip(entities, embeddings):
        found = False
        for canon_ent, canon_emb in canonical:
            if ent["type"] != canon_ent["type"]:
                continue  # Only compare the same type
            sim = cosine_sim(emb, canon_emb)
            if sim >= threshold:
                mapping[ent["name"]] = canon_ent["name"]
                # Merge properties
                print(f"Dedup: '{ent['name']}' -> '{canon_ent['name']}' (sim={sim:.3f})")
                found = True
                break
        
        if not found:
            canonical.append((ent, emb))
            mapping[ent["name"]] = ent["name"]
    
    # Return the canonical entities + mapping to fix relations
    canonical_entities = [c[0] for c in canonical]
    return canonical_entities, mapping

def remap_relations(relations: list, mapping: dict) -> list:
    """Fix source/target in relations according to the dedup mapping."""
    for r in relations:
        r["source"] = mapping.get(r["source"], r["source"])
        r["target"] = mapping.get(r["target"], r["target"])
    # Drop self-loops created by dedup
    return [r for r in relations if r["source"] != r["target"]]

# Usage
entities_raw = [
    {"name": "Nguyen Van A", "type": "Person"},
    {"name": "Alice Nguyen", "type": "Person"},
    {"name": "Phoenix", "type": "Project"},
    {"name": "Phoenix Project", "type": "Project"},
]
canonical, mapping = deduplicate_entities(entities_raw, threshold=0.80)
print(f"Canonical: {[c['name'] for c in canonical]}")
print(f"Mapping: {mapping}")
