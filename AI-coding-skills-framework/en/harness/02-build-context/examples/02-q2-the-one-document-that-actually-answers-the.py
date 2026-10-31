docs = rank_by_relevance(all_docs)   # never random.shuffle(all_docs)
context = f"""
MOST IMPORTANT: {docs[0]}    ← beginning, high attention
{docs[1:-1]}                  ← middle, lower attention
MOST IMPORTANT: {docs[-1]}   ← end, high attention
"""
