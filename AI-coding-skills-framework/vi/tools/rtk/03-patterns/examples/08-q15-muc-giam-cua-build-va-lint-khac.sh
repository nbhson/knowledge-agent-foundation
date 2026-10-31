rtk cargo build
rtk cargo clippy
rtk tsc
rtk lint
rtk prettier --check .   # chỉ còn file cần format, ~75%
rtk sbt compile         # chỉ còn lỗi biên dịch, ~75%
