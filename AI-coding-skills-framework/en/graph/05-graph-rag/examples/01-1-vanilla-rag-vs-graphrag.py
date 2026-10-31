# Token cost comparison (estimate for 1000 docs, ~500K tokens)
vanilla_rag_indexing = {
    "embedding": "500K tokens × $0.0001/1K = $0.05",
    "total": "$0.05"
}

graphrag_indexing = {
    "entity_extraction": "500K tokens × $0.005/1K (GPT-4o) × 2 gleanings = $5.00",
    "community_summary": "50 communities × 2K tokens × $0.005/1K = $0.50",
    "embeddings": "$0.05",
    "total": "$5.55 (111× more expensive, but one-time)"
}

# But: query quality improves 30-40% → fewer retries, fewer hallucinations → saves long-term
