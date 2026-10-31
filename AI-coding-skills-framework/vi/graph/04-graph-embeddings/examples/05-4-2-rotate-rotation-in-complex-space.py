import torch
import torch.nn as nn

class TransE(nn.Module):
    def __init__(self, num_entities: int, num_relations: int, dim: int = 100):
        super().__init__()
        self.entity_emb = nn.Embedding(num_entities, dim)
        self.relation_emb = nn.Embedding(num_relations, dim)
        nn.init.xavier_uniform_(self.entity_emb.weight)
        nn.init.xavier_uniform_(self.relation_emb.weight)
    
    def forward(self, h: torch.Tensor, r: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """Score triples — thấp = đúng."""
        h_e = self.entity_emb(h)  # (batch, dim)
        r_e = self.relation_emb(r)
        t_e = self.entity_emb(t)
        # L1 distance: ||h + r - t||
        score = torch.norm(h_e + r_e - t_e, p=1, dim=1)
        return score  # (batch,)
    
    def predict_tail(self, h: int, r: int, all_entities: int) -> torch.Tensor:
        """Cho (h, r, ?), rank tất cả entities theo score."""
        h_e = self.entity_emb(torch.tensor([h]))
        r_e = self.relation_emb(torch.tensor([r]))
        all_t = self.entity_emb.weight  # (num_entities, dim)
        scores = torch.norm(h_e + r_e - all_t, p=1, dim=1)
        return scores  # thấp nhất = dự đoán tốt nhất

# Training
model = TransE(num_entities=1000, num_relations=10, dim=100)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    # Positive triples: (h, r, t) đúng
    h_pos = torch.randint(0, 1000, (32,))
    r_pos = torch.randint(0, 10, (32,))
    t_pos = torch.randint(0, 1000, (32,))
    
    # Negative triples: corrupt tail
    t_neg = torch.randint(0, 1000, (32,))
    
    pos_score = model(h_pos, r_pos, t_pos)
    neg_score = model(h_pos, r_pos, t_neg)
    
    # Margin ranking loss: pos_score + margin < neg_score
    margin = 1.0
    loss = torch.relu(pos_score - neg_score + margin).mean()
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f"Epoch {epoch}: loss={loss.item():.4f}")

# Predict: Alice WORKS_ON ?
# alice_id = entity_to_id["Alice"], works_on_id = relation_to_id["WORKS_ON"]
# scores = model.predict_tail(alice_id, works_on_id, num_entities=1000)
# top_k = torch.topk(scores, k=5, largest=False)  # 5 projects có score thấp nhất
