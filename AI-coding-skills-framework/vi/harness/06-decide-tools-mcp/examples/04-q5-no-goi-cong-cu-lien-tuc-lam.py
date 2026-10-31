records = [t for t in records if now - t < 60]   # cửa sổ trượt
if len(records) >= limit:
    return {"allowed": False,
            "retry_after": round(60 - (now - records[0]), 1)}
