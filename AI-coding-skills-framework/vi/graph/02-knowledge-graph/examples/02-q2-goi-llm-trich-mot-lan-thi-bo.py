def extract_entities(text, model="gemma3:12b", max_gleanings=2):
    seen, all_ents = set(), []
    for r in range(max_gleanings + 1):
        p = f"Trích entities (Person, Project, Document, Organization).\n{text}\nĐã trích: {sorted(seen)}\nTrả JSON list."
        added = [e for e in llm_json(p, model) if e["name"].lower().strip() not in seen]  # format=json
        seen |= {e["name"].lower().strip() for e in added}; all_ents += added
        if added == 0: break                        # hết ý, dừng sớm
    return all_ents
