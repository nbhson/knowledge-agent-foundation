# Test embedding
curl -s http://localhost:11434/api/embed -d '{
  "model": "nomic-embed-text",
  "input": ["What is health insurance?", "Cardiovascular disease prevention"]
}' | jq '.embeddings | length'
# Output: 2

# Check embedding dimensions
curl -s http://localhost:11434/api/embed -d '{
  "model": "nomic-embed-text",
  "input": "test"
}' | jq '.embeddings[0] | length'
# Output: 768
