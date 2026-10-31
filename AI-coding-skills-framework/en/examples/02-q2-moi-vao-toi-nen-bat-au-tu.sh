ollama serve                                     # chạy model local
curl -s localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text","input":"deploy docker"}'
