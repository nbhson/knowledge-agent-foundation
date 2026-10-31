# Pseudocode — Planner-Executor-Reasoner (PER)
def PER(question: str, graph):
    # PLANNER: the LLM generates a sequence of relations
    plan = llm(f"""
        Question: {question}
        To answer, perform in order:
        1. FIND entities related to '{question}'
        2. TRAVERSE relation1 → entity2
        3. TRAVERSE relation2 → entity3
        4. SUMMARIZE the result
        Return a JSON list of the steps.""")  # ["FIND", "GET_REPORTER", "GET_PROJECT", "SUM"]
    
    # EXECUTOR: the graph executes each step
    entities = find_start_entities(question, graph)
    for step in plan:
        if step.startswith("GET_"):
            entities = traverse(step.replace("GET_", ""), entities, graph)
    
    # REASONER: the LLM reads the graph results (not from its own memory) → answers
    return llm(f"Results from the graph: {entities}\n\nAnswer to the question: {question}")
