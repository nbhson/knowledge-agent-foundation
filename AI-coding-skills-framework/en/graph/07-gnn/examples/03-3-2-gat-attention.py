# pip install torch torch-geometric

import torch
from torch_geometric.nn import GATConv, SAGEConv
from torch_geometric.data import Data

# Prepare data
edge_index = torch.tensor([[0,1,1,2,2,3,0,2],
                           [1,0,2,1,3,2,2,0]], dtype=torch.long)
x = torch.randn(4, 8)  # 4 nodes, 8 features
y = torch.tensor([0, 1, 0, 1])  # labels

data = Data(x=x, edge_index=edge_index, y=y)

# GraphSAGE model
class GraphSAGEModel(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c):
        super().__init__()
        self.conv1 = SAGEConv(in_c, hid_c)
        self.conv2 = SAGEConv(hid_c, out_c)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# GAT model
class GATModel(torch.nn.Module):
    def __init__(self, in_c, hid_c, out_c, heads=4):
        super().__init__()
        self.conv1 = GATConv(in_c, hid_c, heads=heads, dropout=0.6)
        # GATConv with heads: output = hid_c * heads
        self.conv2 = GATConv(hid_c * heads, out_c, heads=1, concat=False, dropout=0.6)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return x

# Train
for name, ModelClass in [("GraphSAGE", GraphSAGEModel), ("GAT", GATModel)]:
    model = ModelClass(8, 16, 2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    for epoch in range(100):
        model.train()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out, data.y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"{name} final loss: {loss.item():.4f}")
