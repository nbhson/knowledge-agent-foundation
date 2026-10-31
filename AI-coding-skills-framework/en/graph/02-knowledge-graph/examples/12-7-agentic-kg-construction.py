# Pseudocode — an agent building a KG (using Cypher + check queries)
TOOLS = ["create_entity", "link_entities", "query_graph", "delete_triplet"]

def agent_build_chunk(chunk_text: str, cypher_exec) -> list[str]:
    """The agent reads the chunk, decides CRUD operations, then verifies itself."""
    actions = []
    # 1) PLAN: the LLM decides which triplets to add
    triplets = llm(f"From the passage below, which (entity, relation, entity) are worth recording? {chunk_text}")
    for subj, rel, obj in triplets:
        # 2) ACTION: try MERGE + SET source for traceability
        cypher_exec("""
            MERGE (s {name:$subj}) 
            ON CREATE SET s.source_chunk=$chunk
            WITH s
            MATCH (t {name: $obj})
            MERGE (s)-[r:REL {type:$rel}]->(t)
            SET r.source_chunk=$chunk
        """, subj=subj, rel=rel, obj=obj, chunk=chunk_text[:100])
        actions.append(f"CREATE {subj}--{rel}-->{obj}")
    # 3) VERIFY: at the end of the chunk, ask the LLM again to check what was just written
    review = llm(f"Are these triplets correct/complete? {triplets}")
    if "needs fixing" in review:
        cypher_exec("DELETE ...")  # the agent fixes it itself (UPDATE/DELETE)
        actions.append("FIX: " + review)
    return actions
