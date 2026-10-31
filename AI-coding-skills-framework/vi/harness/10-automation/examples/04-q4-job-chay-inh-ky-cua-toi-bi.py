key = f"{task_name}#{window_start.isoformat()}"   # nightly-e2e#2026-09-28
if key in done_store:          # đã chạy rồi → bỏ qua, không chạy lại lần nữa
    return "skipped"
run()
done_store.add(key)
