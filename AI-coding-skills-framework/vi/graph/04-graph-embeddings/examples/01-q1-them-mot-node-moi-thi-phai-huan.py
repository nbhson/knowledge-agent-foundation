model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=8)
emb_cu = model(x_cu, edge_index_cu)      # node mới chưa từng huấn luyện
emb_cu = emb_cu / emb_cu.norm(dim=1, keepdim=True)   # chuẩn hoá để so cosin
