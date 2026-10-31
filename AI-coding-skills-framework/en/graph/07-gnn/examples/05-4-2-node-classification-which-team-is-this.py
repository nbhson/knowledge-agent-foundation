# Already covered in §2.2 — 2-layer GCN with cross-entropy loss
# Add: class imbalance handling

# If team A has 100 people and team B has 10 → weighted loss
class_weights = torch.tensor([1.0, 10.0])  # weight for the minority class
loss = F.cross_entropy(out[train_mask], labels[train_mask], weight=class_weights)
