key = f"{runId}:{step.id}:{hashlib.sha256(json.dumps(inputs).encode()).hexdigest()}"
if cached is not None:
    return cached                      # đã làm rồi, trả lại kết quả cũ
