ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
context = (f"QUAN TRỌNG NHẤT: {ranked[0]}\n"
           f"{[d for d, _ in ranked[1:-1]]}\n"
           f"QUAN TRỌNG NHẤT: {ranked[-1]}")
