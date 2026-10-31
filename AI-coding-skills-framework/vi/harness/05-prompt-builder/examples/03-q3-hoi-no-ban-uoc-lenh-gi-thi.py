( r"ignore.*instructions", "Prompt injection attempt"),
( r"reveal.*instructions", "Instruction leak attempt"),
( r"pretend.*you.*are",   "Role hijacking attempt"),
( r"<\|im_start\|>",      "Token injection attempt"),
# trả dự phòng: "Xin lỗi, tôi không thể thực hiện yêu cầu này."
