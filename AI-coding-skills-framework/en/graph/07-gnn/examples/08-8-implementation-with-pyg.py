import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from torch_geometric.utils import train_test_split_edges

# 1. Prepare data
edge_index = torch.tensor([
    [0,1,1,2,2,3,3,0,0,2],
    [1,0,2,1,3,2,0,3,2,0]
], dtype=torch.long)
x = torch.randn(4, 16)
y = torch.tensor([0, 0, 1, 1])  # 2 classes

data = Data(x=x, edge_index=edge_index, y=y, num_nodes=4)
# Split edges for link prediction
# data = train_test_split_edges(data)  # for large graphs

# 2. Model
class GNN(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        super().__init__()
        self.conv1 = GCNConv(in_c, hid_c)
        self.conv2 = GCNConv(hid_c, out_c)
        self.classifier = torch.nn.Linear(out_c, 2)
    
    def forward(self, x, edge_index, task="classify"):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        if task == "classify":
            return self.classifier(x)
        return x  # embeddings for link prediction

model = GNN(16, 32, 16)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 3. Training loop
for epoch in range(200):
    model.train()
    out = model(data.x, data.edge_index, task="classify")
    loss = F.cross_entropy(out, data.y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 50 == 0:
        pred = out.argmax(dim=1)
        acc = (pred == data.y).float().mean().item()
        print(f"Epoch {epoch}: loss={loss.item():.4f}, acc={acc:.2f}")

# 4. Evaluation
model.eval()
with torch.no_grad():
    out = model(data.x, data.edge_index, task="classify")
    pred = out.argmax(dim=1)
    print(f"Final predictions: {pred.tolist()}, true: {y.tolist()}")
