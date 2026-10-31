import torch
import torch.nn as nn
import torch.nn.functional as F

class GCNLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)
    
    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """
        x: (N, in_dim) — node features
        adj: (N, N) — adjacency matrix (đã chuẩn hóa)
        """
        # Aggregate: adj @ x → mỗi node lấy trung bình neighbors
        agg = adj @ x  # (N, in_dim)
        # Transform + activation
        out = self.linear(agg)  # (N, out_dim)
        return F.relu(out)

def normalize_adjacency(adj: torch.Tensor) -> torch.Tensor:
    """Chuẩn hóa: D^{-1/2} (A + I) D^{-1/2}"""
    n = adj.shape[0]
    adj_hat = adj + torch.eye(n)  # thêm self-loop
    degree = adj_hat.sum(dim=1)
    d_inv_sqrt = torch.diag(torch.pow(degree, -0.5))
    d_inv_sqrt[torch.isinf(d_inv_sqrt)] = 0
    return d_inv_sqrt @ adj_hat @ d_inv_sqrt

# Usage
N, in_dim, out_dim = 4, 8, 16
x = torch.randn(N, in_dim)
adj = torch.tensor([[0,1,1,0],[1,0,1,0],[1,1,0,1],[0,0,1,0]], dtype=torch.float32)
adj_norm = normalize_adjacency(adj)

gcn = GCNLayer(in_dim, out_dim)
h = gcn(x, adj_norm)
print(f"GCN output: {h.shape}")  # (4, 16)
