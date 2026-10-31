rtk read src/harness/loop.rs       # xem cấu trúc, không phải toàn bộ nội dung
rtk grep "handleToolCall" .        # tìm chỗ cần sửa
rtk cargo test                     # chỉ còn failure
