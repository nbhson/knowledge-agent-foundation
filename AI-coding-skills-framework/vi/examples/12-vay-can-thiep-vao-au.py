import requests

OLLAMA_URL = "http://localhost:11434"

# 1. User gõ prompt
user_prompt = "BHYT có chi trả bệnh tim không?"

# 2. INTERCEPT: embed prompt → search vector DB
def search_relevant_chunks(query):
    # Embed query
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={
        "model": "nomic-embed-text",
        "input": query
    })
    query_vector = resp.json()["embeddings"][0]
    
    # Search ChromaDB/FAISS (giả lập kết quả)
    results = [
        "BHYT chi trả từ 80% đến 100% chi phí tùy tuyến.",
        "Bệnh tim mạch thuộc danh mục bảo hiểm y tế chi trả.",
    ]
    return results

# 3. GHÉP context vào prompt
context = search_relevant_chunks(user_prompt)
final_prompt = f"""Dùng thông tin sau để trả lời câu hỏi:

{chr(10).join(f'• {c}' for c in context)}

Câu hỏi: {user_prompt}"""

# 4. Gửi prompt ĐÃ AUGMENT tới LLM
response = requests.post(f"{OLLAMA_URL}/api/generate", json={
    "model": "gemma3:12b",
    "prompt": final_prompt,
    "stream": False
})

print(response.json()["response"])
