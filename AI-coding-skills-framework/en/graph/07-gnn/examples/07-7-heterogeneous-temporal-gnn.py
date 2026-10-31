# Pseudocode — HGT: attention per (node_type, edge_type) pair
def hgt_message(head, rel, tail):
    # Project already has a different node type than Person → use dedicated matrices
    W_head = weight_matrix[head.node_type]
    W_edge = weight_matrix[rel.edge_type]
    W_tail = weight_matrix[tail.node_type]
    attn = attention(W_head @ head.h, W_edge @ rel.h, W_tail @ tail.h)
    return attn * (W_head @ head.h)
