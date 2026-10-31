OLLAMA_URL = "http://localhost:11434"        # miễn phí
MODEL = "gemma3:12b"                         # đổi sang "gpt-4o" = trả phí
r = requests.post(f"{OLLAMA_URL}/api/generate",
    json={"model": MODEL, "prompt": p, "stream": False})
