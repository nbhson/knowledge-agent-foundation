from torch_geometric.nn import RGCNConv

class RGCN(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, num_relations):
        super().__init__()
        self.conv1 = RGCNConv(in_dim, hidden_dim, num_relations)
        self.conv2 = RGCNConv(hidden_dim, out_dim, num_relations)
    
    def forward(self, x, edge_index, edge_type):
        x = self.conv1(x, edge_index, edge_type).relu()
        x = self.conv2(x, edge_index, edge_type)
        return x

# edge_type: (E,) — relation type for each edge
edge_index = torch.tensor([[0,1,2,0],[1,2,3,2]], dtype=torch.long)
edge_type = torch.tensor([0, 1, 0, 1])  # 0=MANAGES, 1=WORKS_ON
x = torch.randn(4, 8)

model = RGCN(8, 16, 8, num_relations=2)
out = model(x, edge_index, edge_type)
print(f"R-GCN output: {out.shape}")  # (4, 8)
