CONCURRENCY, LABEL_THRESHOLD = 32, 0.75
p = cat["probabilities"].get(cat["selected"], 0.0)
row = {"id": rec["id"], "label": cat["selected"], "needs_review": p < 0.75}
sem = asyncio.Semaphore(CONCURRENCY)      # bound it; don't stampede
