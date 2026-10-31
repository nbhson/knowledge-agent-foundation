model = TransE(num_entities=1000, num_relations=10, dim=100)
score = torch.norm(h_e + r_e - t_e, p=1, dim=1)   # thấp = đúng, cao = sai
top = torch.topk(model.predict_tail(alice_id, works_on_id, 1000), k=5, largest=False)
# (Alice, WORKS_ON, ?) → 5 entity có điểm thấp nhất
