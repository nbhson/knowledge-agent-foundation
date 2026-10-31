# Install Ollama (run LLM & Embedding locally)
curl -fsSL https://ollama.com/install.sh | sh

# Pull models (Jul-2026 examples — see Oct-2026 note below)
ollama pull gemma3:12b        # Main LLM (example)
ollama pull nomic-embed-text  # Embedding model
