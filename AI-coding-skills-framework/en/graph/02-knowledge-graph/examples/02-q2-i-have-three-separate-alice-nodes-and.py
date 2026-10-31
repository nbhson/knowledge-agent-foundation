for canon_ent, canon_emb in canonical:
    if ent["type"] != canon_ent["type"]:
        continue                                    # never cross types
    sim = cosine_sim(embed(ent["name"]), canon_emb)
    if sim >= 0.85:
        mapping[ent["name"]] = canon_ent["name"]     # canonical is the first one
relations = [r for r in remap_relations(relations, mapping) if r["source"] != r["target"]]
