# Pseudocode — Think-on-Graph
def Think_on_Graph(question: str, graph):
    entities = find_entities(question, graph)          # Step 1: find the related nodes
    best_reasoning_path = None
    
    for _ in range(max_depth):                         # BFS style
        neighbors = get_neighbors(entities, graph)     # Get the candidate neighbors
        reasoning_paths = llm(f"""
            Question: {question}
            Currently at: {entities}
            Next possible moves: {neighbors}
            Choose the most reasonable direction.""")
        # The LLM decides on its own: here the LLM is the planner
        entities = advance(reasoning_paths)            # Move to the next nodes
        if is_answer(entities): 
            return llm(f"Summary: {reasoning_path}")   # The LLM synthesizes from the evidence
    
    return "Not found"
