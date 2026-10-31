# ❌ SAI — dump toàn bộ repo/file (thừa, dễ vượt budget, accuracy tụt)
state = open("huge_log.txt").read()                     # 40k tokens unrelated

# ✅ ĐÚNG — extract đoạn LIÊN QUAN tới question trước
def build_state(ticket: dict, question: str) -> str:
    # Chỉ phần subject + body đã cắt, bỏ quoted history / signatures
    core = f"{ticket['subject']}\n{ticket['body'][:1500]}"
    return core                                          # nhỏ, liên quan

# Với map-reduce: mỗi record 1 state nhỏ — không cần gộp dataset vào 1 state
# Với questions khác nhau: tách state nếu material khác nhau
#   state_Q1 = extract_for("queue")     ← song song, gần free
#   state_Q2 = extract_for("priority")
