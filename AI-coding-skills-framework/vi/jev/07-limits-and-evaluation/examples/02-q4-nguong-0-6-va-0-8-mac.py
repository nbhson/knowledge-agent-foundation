rows = sorted(rows, key=lambda r: r["confidence"], reverse=True)
best = None
for i in range(1, len(rows) + 1):
    bucket = rows[:i]
    prec = sum(r["correct"] for r in bucket) / len(bucket)
    if prec < min_precision:
        break                      # thêm mẫu thì độ chính xác tụt
    best = {"threshold": bucket[-1]["confidence"], "precision": prec}
