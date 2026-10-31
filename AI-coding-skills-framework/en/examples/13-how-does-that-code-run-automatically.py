from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434"

def search_relevant(query):
    """Search the Vector DB - replace with your real code"""
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text", "input": query
    })
    # Simulated results - replace with a real ChromaDB/Qdrant
    return [
        "Health insurance covers 80% to 100% of costs, depending on the tier of care.",
        "Cardiovascular disease is on the list of services covered by health insurance.",
    ]

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")
    
    # INTERCEPT: retrieve context
    context = search_relevant(user_prompt)
    
    # MERGE context into the prompt
    augmented_prompt = f"""Answer using the following information:

{chr(10).join(f'• {c}' for c in context)}

Question: {user_prompt}"""
    
    # Send to the LLM
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": data.get("model", "gemma3:12b"),
        "prompt": augmented_prompt,
        "stream": data.get("stream", False)
    })
    
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(port=5000)
