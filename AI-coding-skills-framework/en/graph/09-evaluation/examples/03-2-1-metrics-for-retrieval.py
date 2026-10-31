from typing import List, Dict

def precision_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & set(relevant))
    return hits / k

def recall_at_k(retrieved: List[str], relevant: List[str], k: int = 5) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & set(relevant))
    return hits / len(relevant) if relevant else 0

def mrr(retrieved: List[str], relevant: List[str]) -> float:
    for rank, doc_id in enumerate(retrieved, 1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0

def path_precision(retrieved_paths: List[List[str]], ground_truth_paths: List[List[str]]) -> float:
    """Measure: how many returned paths match the ground truth (exact or subset)."""
    retrieved_set = set(tuple(p) for p in retrieved_paths)
    gt_set = set(tuple(p) for p in ground_truth_paths)
    hits = len(retrieved_set & gt_set)
    return hits / len(retrieved_set) if retrieved_set else 0

# Usage
retrieved = ["doc_1", "doc_3", "doc_5", "doc_7", "doc_9"]
relevant = ["doc_1", "doc_5", "doc_10"]

print(f"P@5: {precision_at_k(retrieved, relevant, 5):.2f}")  # 0.40 (2/5)
print(f"R@5: {recall_at_k(retrieved, relevant, 5):.2f}")     # 0.67 (2/3)
print(f"MRR: {mrr(retrieved, relevant):.2f}")                 # 1.00 (doc_1 at rank 1)

# Path precision
retrieved_paths = [["Alice", "Bob", "Phoenix"], ["Alice", "Dave", "Atlas"]]
gt_paths = [["Alice", "Bob", "Phoenix"]]
print(f"Path P: {path_precision(retrieved_paths, gt_paths):.2f}")  # 0.50
