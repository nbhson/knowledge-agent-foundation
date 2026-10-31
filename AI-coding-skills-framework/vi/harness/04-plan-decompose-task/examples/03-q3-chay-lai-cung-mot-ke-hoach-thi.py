k = idem_key(plan, sub, inputs)
if k in store: return store[k]          # phát lại = không tác dụng phụ lần hai
out = fn(inputs); store[k] = {"status": "ok", "out": out}
