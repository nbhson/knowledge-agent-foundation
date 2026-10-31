def nhận_kết_quả(so_phiên_ban, so_phiên_hiện_tại, so_lan):
    if so_lan > 3: return False      # quá giới hạn → báo người
    return so_phiên_ban == so_phiên_hiện_tại   # cũ hơn → bỏ
