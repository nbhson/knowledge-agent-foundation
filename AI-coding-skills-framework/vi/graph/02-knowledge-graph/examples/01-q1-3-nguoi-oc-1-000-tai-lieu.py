def dedup(entities, threshold=0.85):
    canon, mapping = [], {}
    for e in entities:                      # e = {"name", "type"}
        hit = next((c for c in canon if c["type"] == e["type"]
                    and cosine_sim(embed(e["name"]), embed(c["name"])) >= threshold), None)
        mapping[e["name"]] = hit["name"] if hit else e["name"]
        if not hit: canon.append(e)
    return canon, mapping
