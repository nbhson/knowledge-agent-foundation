# Measure Evidence Recall on retrieval results
def evidence_recall(gold_evidence: list[str], retrieved: list[str]) -> float:
    """% of the 'gold' evidence that made it into the chunks fed to the LLM."""
    r = set(c.lower() for c in retrieved)
    hit = sum(1 for ev in gold_evidence if ev.lower() in r)
    return hit / len(gold_evidence) if gold_evidence else 1.0

# Context Relevancy (simplified — threshold from manual evaluations)
def context_relevancy(retrieved: list[str], question: str) -> float:
    """The fraction of context passages that are actually relevant (scored by LLM-as-judge)."""
    ...
