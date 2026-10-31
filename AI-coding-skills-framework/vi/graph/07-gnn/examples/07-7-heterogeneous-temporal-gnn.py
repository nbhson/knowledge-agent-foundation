# Pseudocode — HGT: attention theo từng cặp (node_type, edge_type)
def hgt_message(head, rel, tail):
    # Project đã có node type khác Person → dùng ma trận riêng
    W_head = weight_matrix[head.node_type]
    W_edge = weight_matrix[rel.edge_type]
    W_tail = weight_matrix[tail.node_type]
    attn = attention(W_head @ head.h, W_edge @ rel.h, W_tail @ tail.h)
    return attn * (W_head @ head.h)
