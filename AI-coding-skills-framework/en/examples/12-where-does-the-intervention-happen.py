import requests

OLLAMA_URL = "http://localhost:11434"

# 1. User types the prompt
user_prompt = "Does health insurance cover heart disease?"

# 2. INTERCEPT: embed the prompt → search the vector DB
def search_relevant_chunks(query):
    # Embed the query
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text",
        "input": query
    })
    query_vector = resp.json()["embeddings"][0]
    
    # Search ChromaDB/FAISS (simulated results)
    results = [
        "Health insurance covers 80% to 100% of costs, depending on the tier of care.",
        "Cardiovascular disease is on the list of services covered by health insurance.",
    ]
    return results

# 3. MERGE the context into the prompt
context = search_relevant_chunks(user_prompt)
final_prompt = f"""Answer the question using the following information:

{chr(10).join(f'• {c}' for c in context)}

Question: {user_prompt}"""

# 4. Send the AUGMENTED prompt to the LLM
response = requests.post(f"{OLLAMA_URL}/api/generate", json={
    "model": "gemma3:12b",
    "prompt": final_prompt,
    "stream": False
})

print(response.json()["response"])
