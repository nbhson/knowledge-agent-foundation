ROLES = {
    "implementer": {
        "goal_example": "Sửa refresh auth trong src/auth/refresh.ts; AC: refresh thành công sau expiry, không chạm file khác",
        "definition_of_done": ["diff giới hạn trong files[]", "build pass", "artifact patch sẵn sàng PR"],
        "forbidden": ["merge", "tự verify", "chạm file ngoài worktree"],
    },
    "verifier": {
        "goal_example": "Verify patch ART-123 theo rubric: build OK, test OK, AC trace",
        "definition_of_done": ["verdict ACCEPT/REJECT kèm bằng chứng", "tên test fail + log"],
        "default_stance": "REJECT cho tới khi bằng chứng đủ",
        "forbidden": ["sửa code", "duyệt khi chưa có output test"],
    },
    "reviewer": {
        "goal_example": "Review diff PR #1234; gắn Blocker/Major/Minor kèm file:line",
        "definition_of_done": ["danh sách severity", "mỗi Blocker ít nhất một comment actionable"],
        "forbidden": ["chạy shell", "ghi file"],
    },
    "researcher": {
        "goal_example": "Token refresh xử lý ở đâu? Trả 3 file ứng viên kèm file:line + 5 dòng context",
        "definition_of_done": ["facts + citations", "không đổi behavior"],
        "forbidden": ["ghi memory", "đề xuất patch khi chưa được hỏi"],
    },
}
