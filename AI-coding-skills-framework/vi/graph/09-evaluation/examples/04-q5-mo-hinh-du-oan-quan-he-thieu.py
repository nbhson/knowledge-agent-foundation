sorted_indices = torch.argsort(scores)
rank = (sorted_indices == t_true).nonzero(as_tuple=True)[0].item() + 1
mrr += 1.0 / rank
# {'Hits@1':0.15,'Hits@10':0.45,'MRR':0.28,'MR':85.3,'num_test':100}
