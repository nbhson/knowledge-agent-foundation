# SAI: dữ liệu bị trộn lẫn hướng dẫn
state = "Bạn là bộ phân loại. Hãy trả lời team nào? Khó thì chọn other. Ticket: ..."

# ĐÚNG: dữ liệu sạch, câu hỏi ở đúng chỗ
state = "Ticket #4821: tôi bị tính phí 2 lần cho gói Pro tháng này."
questions = {"team": {"type": "choice",
                      "choices": ["billing", "tech", "account", "other"],
                      "description": "Team nào sở hữu ticket này?"}}
