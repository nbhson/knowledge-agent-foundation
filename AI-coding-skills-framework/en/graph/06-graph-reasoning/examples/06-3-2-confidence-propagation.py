def propagate_confidence(path_confidences: List[float], method: str = "product") -> float:
    """
    Compute the confidence of an inferred edge from a chain.
    
    product: conf = c1 * c2 * ... (multiplicative — the longer the chain, the lower the confidence)
    min: conf = min(c1, c2, ...) (take the weakest)
    avg: conf = mean(c1, c2, ...)
    """
    if method == "product":
        result = 1.0
        for c in path_confidences:
            result *= c
        return result
    elif method == "min":
        return min(path_confidences)
    elif method == "avg":
        return sum(path_confidences) / len(path_confidences)

# Example: Alice(0.95) → Bob(0.90) → Carol
# Inferred: Alice INDIRECTLY_MANAGES Carol
print(propagate_confidence([0.95, 0.90], "product"))  # 0.855
print(propagate_confidence([0.95, 0.90], "min"))       # 0.90
