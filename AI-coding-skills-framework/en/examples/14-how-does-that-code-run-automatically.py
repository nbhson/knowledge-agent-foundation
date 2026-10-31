# NORMALLY:
def ask_llm(prompt):
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": prompt
    }).json()["response"]

# WITH RETRIEVAL:
def ask_llm_with_rag(prompt):
    # Step 1: retrieve context
    context = search_relevant_chunks(prompt)  # the function you already wrote
    
    # Step 2: merge context into the prompt
    augmented = f"Context:\n{chr(10).join(context)}\n\nQuestion: {prompt}"
    
    # Step 3: call the LLM with the augmented prompt
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": augmented
    }).json()["response"]

# Use it the same way:
print(ask_llm_with_rag("Does health insurance cover heart disease?"))
