# Đã cover ở §2.2 — GCN 2-layer với cross-entropy loss
# Thêm: class imbalance handling

# Nếu team A có 100 người, team B có 10 người → weighted loss
class_weights = torch.tensor([1.0, 10.0])  # weight cho minority class
loss = F.cross_entropy(out[train_mask], labels[train_mask], weight=class_weights)
