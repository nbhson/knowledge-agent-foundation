def evaluate_coverage(
    extracted_entities: List[str],
    ground_truth_entities: List[str],
    threshold: float = 0.85,  # embedding similarity threshold
) -> Dict:
    """
    Measure coverage: how many ground truth entities were extracted correctly.
    
    Uses embedding similarity for fuzzy matching (Alice ≈ Alice Nguyen).
    """
    import numpy as np
    
    # Simplified: exact match (production: embedding similarity)
    extracted_set = set(e.lower().strip() for e in extracted_entities)
    gt_set = set(e.lower().strip() for e in ground_truth_entities)
    
    correct = extracted_set & gt_set
    precision = len(correct) / len(extracted_set) if extracted_set else 0
    recall = len(correct) / len(gt_set) if gt_set else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "extracted": len(extracted_set),
        "ground_truth": len(gt_set),
        "correct": len(correct),
        "missed": list(gt_set - extracted_set)[:5],
        "hallucinated": list(extracted_set - gt_set)[:5],
    }

# Usage
print(evaluate_coverage(
    ["Alice", "Bob", "Phoenix", "Alice Nguyen"],  # extracted (has duplicates)
    ["Alice", "Bob", "Phoenix", "Atlas"],           # ground truth
))
# {'precision': 0.75, 'recall': 0.75, 'f1': 0.75, 'missed': ['atlas'], 'hallucinated': ['alice nguyen']}
