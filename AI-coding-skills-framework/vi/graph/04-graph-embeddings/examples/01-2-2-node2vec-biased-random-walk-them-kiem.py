# p và q hoạt động như thế nào:

p = return parameter (xác suất quay lại node vừa rời đi):
  - p nhỏ (0.5): hay quay lại → khám phá neighborhood chặt
  - p lớn (2.0): ít quay lại → đi xa hơn

q = in-out parameter (xác suất đi ra xa hay quay lại):
  - q nhỏ (0.5): dễ đi xa (DFS-like) → khám phá cấu trúc xa
  - q lớn (2.0): dễ đi gần (BFS-like) → khám phá community.local

# Hiểu đơn giản nhất:
# q < 1 (DFS-like): "Tôi muốn tìm người có CÙNG ROLE" dù ở khác team
# q > 1 (BFS-like): "Tôi muốn tìm người trong CÙNG TEAM"
