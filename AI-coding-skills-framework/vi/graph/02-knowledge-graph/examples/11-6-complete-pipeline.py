def build_knowledge_graph(documents: list[str], ontology: Ontology) -> dict:
    """
    Pipeline hoàn chỉnh: Documents -> Knowledge Graph
    """
    all_entities = []
    all_relations = []
    
    # Step 1: Extract từ từng document
    for doc in documents:
        entities = extract_entities(doc, max_gleanings=2)
        relations = extract_relations(doc, entities)
        all_entities.extend(entities)
        all_relations.extend(relations)
    
    print(f"Raw: {len(all_entities)} entities, {len(all_relations)} relations")
    
    # Step 2: Deduplicate
    canonical_entities, mapping = deduplicate_entities(all_entities, threshold=0.85)
    all_relations = remap_relations(all_relations, mapping)
    
    print(f"After dedup: {len(canonical_entities)} entities, {len(all_relations)} relations")
    
    # Step 3: Validate against ontology
    valid_entities = []
    for ent in canonical_entities:
        ok, msg = ontology.validate_node(ent["type"], ent)
        if ok:
            valid_entities.append(ent)
        else:
            print(f"Invalid entity {ent['name']}: {msg}")
    
    valid_relations = []
    for rel in all_relations:
        # Tìm type của source/target
        src_type = next((e["type"] for e in valid_entities if e["name"] == rel["source"]), None)
        tgt_type = next((e["type"] for e in valid_entities if e["name"] == rel["target"]), None)
        if src_type and tgt_type:
            ok, msg = ontology.validate_edge(rel["type"], src_type, tgt_type)
            if ok and rel.get("confidence", 0) >= 0.7:
                valid_relations.append(rel)
            else:
                print(f"Invalid relation {rel}: {msg}")
    
    print(f"After validation: {len(valid_entities)} entities, {len(valid_relations)} relations")
    
    return {"entities": valid_entities, "relations": valid_relations}

# Usage
docs = [
    "Dự án Phoenix do Nguyễn Văn A phê duyệt. Hợp đồng C-2024 thuộc dự án Phoenix.",
    "Nguyễn Văn A báo cáo cho Trần Thị B, CTO. Trần Thị B quản lý team AI gồm 10 engineers.",
]
kg = build_knowledge_graph(docs, ontology)
print(kg)
