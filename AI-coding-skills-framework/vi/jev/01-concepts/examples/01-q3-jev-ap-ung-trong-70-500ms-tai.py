r = requests.post(API, headers=HEADERS, json={
    "model": "jev-1.13.0",
    "state": core,                       # đã cắt còn phần liên quan
    "questions": questions,              # tất cả trong 1 pass
}, timeout=5)
