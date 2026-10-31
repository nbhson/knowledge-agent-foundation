neg = negative_sampling(edge_index, num_nodes=4, num_neg_samples=4)
pos_loss = F.binary_cross_entropy_with_logits(pos_score, torch.ones_like(pos_score))
loss = pos_loss + neg_loss
