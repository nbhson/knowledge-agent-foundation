# BÌNH THƯỜNG:
def ask_llm(prompt):
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": prompt
    }).json()["response"]

# CÓ RETRIEVE:
def ask_llm_with_rag(prompt):
    # Bước 1: retrieve context
    context = search_relevant_chunks(prompt)  # hàm bạn đã viết
    
    # Bước 2: ghép context vào prompt
    augmented = f"Context:\n{chr(10).join(context)}\n\nQuestion: {prompt}"
    
    # Bước 3: gọi LLM với prompt đã augment
    return requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:12b", "prompt": augmented
    }).json()["response"]

# Dùng y hệt:
print(ask_llm_with_rag("BHYT có chi trả bệnh tim không?"))
