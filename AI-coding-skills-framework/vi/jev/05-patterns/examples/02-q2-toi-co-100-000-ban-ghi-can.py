async def classify_one(client, record):
    r = await client.post(API, headers=HEADERS, json={
        "model": "jev-1.13.0", "state": record["text"],
        "questions": {"tag": {"type": "choice", "options": TAGS}}}, timeout=5)
    a = r.json()["answers"]["tag"]
    return {"id": record["id"], "tag": a["selected"], "confidence": a["confidence"]}

# gọi song song theo lô 50, mỗi lượt vẫn 70–500ms
