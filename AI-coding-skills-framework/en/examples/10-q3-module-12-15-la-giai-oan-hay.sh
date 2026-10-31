# 4 dòng này dựng xong một lần chạy RAG tối giản để bắt đầu
ollama pull gemma3:12b
ollama pull nomic-embed-text
python scripts/extract.py docs/ --out kb.json
python scripts/query.py "báo giá còn hạn bao lâu?"
