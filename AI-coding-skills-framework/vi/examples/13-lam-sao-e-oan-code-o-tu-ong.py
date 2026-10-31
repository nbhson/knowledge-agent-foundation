from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434"

def search_relevant(query):
    """Search Vector DB - thay bằng code thật của bạn"""
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text", "input": query
    })
    # Giả lập kết quả - thay bằng ChromaDB/Qdrant thật
    return [
        "BHYT chi trả từ 80% đến 100% chi phí tùy tuyến.",
        "Bệnh tim mạch thuộc danh mục bảo hiểm y tế chi trả.",
    ]

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")
    
    # INTERCEPT: retrieve context
    context = search_relevant(user_prompt)
    
    # GHÉP context vào prompt
    augmented_prompt = f"""Dùng thông tin sau để trả lời:

{chr(10).join(f'• {c}' for c in context)}

Câu hỏi: {user_prompt}"""
    
    # Gửi tới LLM
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": data.get("model", "gemma3:12b"),
        "prompt": augmented_prompt,
        "stream": data.get("stream", False)
    })
    
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(port=5000)
