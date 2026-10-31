from datetime import date
days_left = (due_date - date.today()).days     # code tính
ans = decide(state=f"Hóa đơn {inv} đến hạn {due_date}, hôm nay {date.today()}",
             questions={"status": {"type": "choice",
                                   "options": ["overdue", "due_soon", "ok"]}})
