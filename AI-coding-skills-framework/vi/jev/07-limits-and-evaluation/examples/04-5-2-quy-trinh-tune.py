def tune_threshold(eval_rows: list[dict],
                   min_precision: float = 0.95) -> dict:
    """
    eval_rows: [{confidence, correct}, ...]  — correct = outcome thật
    Chọn threshold THẤP NHẤT đạt min_precision (tối đa coverage).
    """
    rows = sorted(eval_rows, key=lambda r: r["confidence"], reverse=True)
    best = None
    for i in range(1, len(rows) + 1):
        bucket = rows[:i]                       # confidence >= rows[i-1]
        precision = sum(r["correct"] for r in bucket) / len(bucket)
        threshold = bucket[-1]["confidence"]
        if precision >= min_precision:
            best = {                            # giữ threshold thấp nhất
                "threshold": threshold,
                "precision": round(precision, 3),
                "coverage": round(len(bucket) / len(rows), 3),
            }
        else:
            break                               # thêm case → precision rơi
    return best or {"threshold": 1.0, "precision": None, "coverage": 0.0}


# Áp dụng:
# tuned = tune_threshold(eval_rows, min_precision=0.95)
# settings.typesafe_tool_call_threshold = tuned["threshold"]
#   thay vì mặc định 0.6 chưa validated cho domain bạn
