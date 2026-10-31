e_vu  = LeakyReLU(a @ (W h_v + W h_u))   # "how much do I trust u"
alpha = softmax(e_vu)                    # sums to 1 over neighbours
h_v   = sigmoid(sum(alpha * W h_u))
