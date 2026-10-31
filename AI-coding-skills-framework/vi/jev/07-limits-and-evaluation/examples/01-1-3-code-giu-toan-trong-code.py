# ❌ SAI — đừng hỏi Jev những câu này
jev_decide(state, {"days_until_due": {"type": "score", ...}})   # date compare
jev_decide(state, {"line_count": {"type": "choice", ...}})       # counting
jev_decide(state, {"sum": {"type": "choice", ...}})              # arithmetic

# ✅ ĐÚNG — code tính, Jev phân loại kết quả nếu cần schema
from datetime import date
days_left = (due_date - date.today()).days           # arithmetic trong code
result = jev_decide(
    state=f"Invoice {id} due {due_date}, today {date.today()}, amount {amt}.",
    questions={"urgency": {"type": "choice", "options": ["overdue", "due_soon", "ok"]}},
)                                                     # Jev phân loại MỌI TRẠNG THÁI
