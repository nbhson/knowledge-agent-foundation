class GCN(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout: float = 0.5):
        super().__init__()
        self.gc1 = GCNLayer(in_dim, hidden_dim)
        self.gc2 = GCNLayer(hidden_dim, out_dim)
        self.dropout = dropout
    
    def forward(self, x, adj):
        x = self.gc1(x, adj)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)  # (N, num_classes)

# Training
model = GCN(in_dim=8, hidden_dim=16, out_dim=3)  # 3 classes
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Labels: chỉ 1 vài nodes có label (semi-supervised)
labels = torch.tensor([0, 1, -1, -1])  # -1 = unlabeled
train_mask = labels != -1

for epoch in range(200):
    model.train()
    out = model(x, adj_norm)
    loss = F.nll_loss(out[train_mask], labels[train_mask])
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict unlabeled
model.eval()
pred = model(x, adj_norm).argmax(dim=1)
print(f"Predictions: {pred}")
