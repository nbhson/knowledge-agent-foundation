@app.route("/api/chat", methods=["POST"])
def chat():
    ctx = search_relevant(data.get("prompt", ""))          # tìm context
    aug = f"Answer using:\n{chr(10).join(ctx)}\n\nQuestion: {prompt}"
    return jsonify(requests.post(OLLAMA_URL, json={
        "model": "gemma3:12b", "prompt": aug, "stream": False}).json())
