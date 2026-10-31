# Pseudocode — Planner-Executor-Reasoner (PER)
def PER(question: str, graph):
    # PLANNER: LLM sinh sequence relations
    plan = llm(f"""
        Câu hỏi: {question}
        Để trả lời, cần thực hiện theo trình tự:
        1. FIND entities liên quan đến '{question}'
        2. TRAVERSE relation1 → entity2
        3. TRAVERSE relation2 → entity3
        4. SUMMARIZE kết quả
        Trả về JSON list các bước.""")  # ["FIND", "GET_REPORTER", "GET_PROJECT", "SUM"]
    
    # EXECUTOR: graph thực thi từng bước
    entities = find_start_entities(question, graph)
    for step in plan:
        if step.startswith("GET_"):
            entities = traverse(step.replace("GET_", ""), entities, graph)
    
    # REASONER: LLM đọc kết quả graph (không phải LLM tự nhớ) → trả lời
    return llm(f"Kết quả từ graph: {entities}\n\nTrả lời câu hỏi: {question}")
