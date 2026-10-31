# Cài Ollama (chạy LLM & Embedding local)
curl -fsSL https://ollama.com/install.sh | sh

# Tải model (ví dụ Jul-2026 — xem ghi chú Oct-2026 bên dưới)
ollama pull gemma3:12b        # LLM chính (ví dụ)
ollama pull nomic-embed-text  # Embedding model
