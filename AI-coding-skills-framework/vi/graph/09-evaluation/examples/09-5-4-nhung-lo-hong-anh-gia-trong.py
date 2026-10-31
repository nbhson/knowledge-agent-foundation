# Đo Evidence Recall trên kết quả retrieval
def evidence_recall(gold_evidence: list[str], retrieved: list[str]) -> float:
    """% bằng chứng 'vàng' nằm trong các đoạn đưa vào LLM."""
    r = set(c.lower() for c in retrieved)
    hit = sum(1 for ev in gold_evidence if ev.lower() in r)
    return hit / len(gold_evidence) if gold_evidence else 1.0

# Context Relevancy (đơn giản hoá — ngưỡng theo lần đánh giá thủ công)
def context_relevancy(retrieved: list[str], question: str) -> float:
    """Tỷ lệ đoạn thực sự liên quan trong context (điểm từ LLM-as-judge)."""
    ...
