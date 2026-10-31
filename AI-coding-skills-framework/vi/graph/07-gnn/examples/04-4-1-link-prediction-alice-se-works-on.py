import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.utils import negative_sampling

class LinkPredictor(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, out_dim)
    
    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x  # (N, out_dim) embeddings
    
    def decode(self, z, edge_label_index):
        """Score edges bằng dot product."""
        src = z[edge_label_index[0]]  # (E, out_dim)
        dst = z[edge_label_index[1]]
        return (src * dst).sum(dim=-1)  # (E,) scores
    
    def forward(self, x, edge_index, edge_label_index):
        z = self.encode(x, edge_index)
        return self.decode(z, edge_label_index)

# Data
edge_index = torch.tensor([[0,1,1,2,2,3],[1,0,2,1,3,2]], dtype=torch.long)
x = torch.randn(4, 8)
# Positive edges (tồn tại) + negative sampling
pos_edges = edge_index
neg_edges = negative_sampling(edge_index, num_nodes=4, num_neg_samples=4)

model = LinkPredictor(8, 16, 8)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(200):
    model.train()
    # Positive scores
    pos_score = model(x, edge_index, pos_edges)
    neg_score = model(x, edge_index, neg_edges)
    
    # BCE loss: pos → 1, neg → 0
    pos_loss = F.binary_cross_entropy_with_logits(pos_score, torch.ones_like(pos_score))
    neg_loss = F.binary_cross_entropy_with_logits(neg_score, torch.zeros_like(neg_score))
    loss = pos_loss + neg_loss
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict: Alice(0) sẽ connect với ai?
model.eval()
z = model.encode(x, edge_index)
for target in range(4):
    if target == 0:
        continue
    score = model.decode(z, torch.tensor([[0],[target]]))
    prob = torch.sigmoid(score).item()
    print(f"  Alice -> node_{target}: prob={prob:.3f}")
