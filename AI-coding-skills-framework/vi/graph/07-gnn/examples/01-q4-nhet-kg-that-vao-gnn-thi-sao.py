model = RGCN(8, 16, 8, num_relations=2)
out = model(x, edge_index, edge_type)   # out shape: (4, 8)
