def noul_confidence(p_yes: float) -> float:
    return abs(p_yes - 0.5) * 2          # 0.45 → 0.10: gần như không biết

def classify_band(conf, high_t=0.8, low_t=0.5):
    if conf >= high_t: return "high"     # code tự hành động
    if conf >= low_t: return "medium"   # xin xác nhận / bổ sung ngữ cảnh
    return "low"                         # chuyển người hoặc mô hình lớn
