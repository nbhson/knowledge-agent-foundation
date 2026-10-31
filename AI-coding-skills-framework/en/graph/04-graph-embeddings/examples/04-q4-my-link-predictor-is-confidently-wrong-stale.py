score = torch.norm(h_e + r_e - t_e, p=1, dim=1)          # TransE, lower = better
loss  = torch.relu(pos_score - neg_score + margin).mean()  # margin = 1.0
