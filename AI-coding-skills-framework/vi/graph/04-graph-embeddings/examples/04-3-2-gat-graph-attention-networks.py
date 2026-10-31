# pip install torch torch-geometric

import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data

class GraphSAGE(torch.nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        return x  # (N, out_channels) embeddings

# Tạo graph data
# edge_index: (2, E) — danh sách edges
edge_index = torch.tensor([[0, 1, 1, 2, 2, 3],
                           [1, 0, 2, 1, 3, 2]], dtype=torch.long)
x = torch.randn(4, 16)  # 4 nodes, 16 features mỗi node

model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=8)
embeddings = model(x, edge_index)
print(f"Embeddings shape: {embeddings.shape}")  # (4, 8)
print(f"Embedding node 0: {embeddings[0]}")
