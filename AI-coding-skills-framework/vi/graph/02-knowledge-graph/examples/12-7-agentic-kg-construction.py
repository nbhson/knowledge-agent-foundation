# Pseudocode — Agent xây KG (dùng Cypher + query kiểm tra)
TOOLS = ["create_entity", "link_entities", "query_graph", "delete_triplet"]

def agent_build_chunk(chunk_text: str, cypher_exec) -> list[str]:
    """Agent đọc chunk, quyết định các thao tác CRUD, rồi tự verify."""
    actions = []
    # 1) PLAN: LLM quyết định triplet nào cần thêm
    triplets = llm(f"Từ đoạn sau, các (entity, relation, entity) nào đáng ghi? {chunk_text}")
    for subj, rel, obj in triplets:
        # 2) ACTION: thử MERGE + SET source để truy vết
        cypher_exec("""
            MERGE (s {name:$subj}) 
            ON CREATE SET s.source_chunk=$chunk
            WITH s
            MATCH (t {name: $obj})
            MERGE (s)-[r:REL {type:$rel}]->(t)
            SET r.source_chunk=$chunk
        """, subj=subj, rel=rel, obj=obj, chunk=chunk_text[:100])
        actions.append(f"CREATE {subj}--{rel}-->{obj}")
    # 3) VERIFY: ở cuối chunk, hỏi lại LLM kiểm tra những gì vừa viết
    review = llm(f"Các triplet này có đúng/đủ không? {triplets}")
    if "cần sửa" in review:
        cypher_exec("DELETE ...")  # agent tự sửa (UPDATE/DELETE)
        actions.append("FIX: " + review)
    return actions
