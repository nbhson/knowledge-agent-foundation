import torch

def evaluate_kg_completion(
    model, test_triples: list, all_entities: int, k_values: list = [1, 3, 10]
) -> dict:
    """
    Đánh giá KG completion.
    
    model: có method predict_tail(h, r) -> scores cho tất cả entities
    test_triples: [(h, r, t), ...] — ground truth
    """
    hits = {k: 0 for k in k_values}
    mrr = 0.0
    ranks = []
    
    for h, r, t_true in test_triples:
        scores = model.predict_tail(h, r, all_entities)  # (num_entities,)
        # Rank: vị trí của t_true khi sort scores tăng dần (thấp = tốt cho TransE)
        sorted_indices = torch.argsort(scores)
        rank = (sorted_indices == t_true).nonzero(as_tuple=True)[0].item() + 1  # 1-indexed
        ranks.append(rank)
        mrr += 1.0 / rank
        for k in k_values:
            if rank <= k:
                hits[k] += 1
    
    n = len(test_triples)
    return {
        **{f"Hits@{k}": round(hits[k] / n, 3) for k in k_values},
        "MRR": round(mrr / n, 3),
        "MR": round(sum(ranks) / n, 1),
        "num_test": n,
    }

# Usage (với TransE model từ 04-graph-embeddings)
# metrics = evaluate_kg_completion(transe_model, test_triples, num_entities=1000)
# print(metrics)
# {'Hits@1': 0.15, 'Hits@10': 0.45, 'MRR': 0.28, 'MR': 85.3, 'num_test': 100}
