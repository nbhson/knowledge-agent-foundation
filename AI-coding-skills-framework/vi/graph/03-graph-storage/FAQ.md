# ❓ FAQ — Lưu trữ & Truy vấn đồ thị (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc.

---

## Q1. Lưu graph thành file JSON, hỏi một câu mất 2 giây — có nên chuyển sang database đồ thị không? [→ §1 Chọn Graph Database]

**Bạn sẽ thấy**

Bạn trích được 5.000 thực thể và 12.000 quan hệ, lưu thành `graph.json` khoảng 50MB. Một tuần sau cần trả lời: *"Tìm tất cả dự án mà team của Alice đã làm, đi qua tối đa 3 bước quan hệ báo cáo/quản lý."* Bạn tự viết vòng lặp duyệt chiều rộng (BFS), nạp nguyên file vào bộ nhớ, chạy **2 giây**. Chạy 100 câu như vậy thì hết giờ.

**Vì sao**

File JSON không có chỉ mục (index) và không có bộ máy truy vấn. Mỗi lần hỏi, bạn phải tự quét toàn bộ file. Database đồ thị lưu quan hệ theo đúng cấu trúc, có chỉ mục và có ngôn ngữ truy vấn — cùng câu hỏi đó trả lời trong **15ms** bằng một dòng Cypher. Benchmark Neo4j 2024 đo được lưu đồ thị gốc nhanh hơn phép nối bảng (JOIN) của cơ sở dữ liệu quan hệ tới **100–1000 lần** cho truy vấn 3 bước.

**Làm gì**

1. Trước khi chuyển, hỏi một câu: truy vấn của tôi có luôn dạng `A —[…]→ B —[…]→ C` không? Nếu có 2 bước trở lên thì đã là ứng viên cho database đồ thị.
2. Chọn theo giai đoạn, không chọn theo thương hiệu:

| Tình huống | Chọn |
|---|---|
| Học, thử nghiệm trên máy mình | NetworkX (thư viện) hoặc Kuzu (nhúng, không cần Docker) |
| Đang phát triển, cần truy vấn chuẩn | Neo4j Community qua Docker |
| Dữ liệu nhiều, cần nhân bản, có người quản lý | Neo4j Aura hoặc NebulaGraph |
| Cần phản hồi dưới 1 mili giây | FalkorDB hoặc Memgraph (lưu trong RAM) |

3. Nếu cần độ trễ thấp mà vẫn giữ hệ sinh thái quen thuộc, xem FalkorDB: nó là database đồ thị chạy ngay trên Redis, dùng phép nhân ma trận thưa để duyệt đồ thị.
4. Bắt đầu bằng NetworkX để học thuật ngữ (node, cạnh, traversal) — nó để bạn đổi sang Kuzu hoặc Neo4j sau mà không phải học lại.

**Kiểm tra**

Đo thời gian trả lời 3 câu hỏi (1 bước, 2 bước, 3 bước) trên BFS tự viết, rồi chạy lại bằng Cypher. Nếu khoảng cách giữa chúng là hàng chục lần thì đã đủ cơ sở để bỏ file JSON.

---

## Q2. Truy vấn chạy chậm, đo thì thấy DB quét hết — sửa ở đâu? [→ §3 Indexing & Performance]

**Bạn sẽ thấy**

Bạn chạy `MATCH (n:Person) WHERE n.name = 'Alice' RETURN n` trên graph 10.000 node và phải chờ. Thêm `PROFILE` phía trước câu lệnh thì thấy kế hoạch thực thi không hề dùng chỉ mục, phải quét toàn bộ. Câu `MATCH (a)-[*]->(b) RETURN a, b` không giới hạn số bước nên sinh ra hàng triệu kết quả trung gian.

**Vì sao**

Chỉ mục là "mục lục" của database: có nó, tìm "Alice" là tra một dòng; không có nó là lật từng trang. LDBC SNB Benchmark đo được chỉ mục trên nhãn + thuộc tính giảm **80%** độ trễ. Phần còn lại là do câu truy vấn viết quá rộng: `[*]` không chặn số bước, và `RETURN n` trả về cả đồ thị.

**Làm gì**

1. Tạo chỉ mục cho đúng trường hay tìm. Tìm chính xác theo tên/mã → chỉ mục dải (range index). Tìm mơ hồ trong văn bản → chỉ mục toàn văn (full-text). Tìm theo nghĩa → chỉ mục vector. Lọc nhiều thuộc tính → chỉ mục tổ hợp (composite).
2. Chỉ tạo chỉ mục cho trường **thật sự hay truy vấn**. Mỗi lần thêm node đều phải cập nhật chỉ mục — tạo bừa thì chậm ghi.
3. Nếu bắt buộc phải có một node có tên duy nhất, dùng **ràng buộc duy nhất** (unique constraint) — nó vừa chặn trùng vừa tự tạo chỉ mục.
4. Luôn giới hạn số bước: `-[:MANAGES*1..3]` thay vì `-[*]`, và luôn thêm `LIMIT`.
5. Chỉ trả về đúng thứ cần: `RETURN proj.name` thay vì `RETURN n`.
6. Trước khi tối ưu, đo lại bằng `PROFILE` để biết có dùng chỉ mục không và tốn bao nhiêu lần đọc dữ liệu.

```cypher
CREATE INDEX person_name FOR (n:Person) ON (n.name);
CREATE CONSTRAINT person_unique FOR (n:Person) REQUIRE n.name IS UNIQUE;
MATCH (a:Person {name:'Alice'})-[:MANAGES*1..3]->(b:Person)
RETURN b.name LIMIT 100
```

**Kiểm tra**

Làm đúng Lab 2: tạo 10.000 node **không** có chỉ mục, đo thời gian câu truy vấn theo tên; tạo chỉ mục rồi đo lại. Thời gian thường giảm 80–90%. Nếu không giảm, chạy `PROFILE` và kiểm tra có còn câu nào đang dùng `[*]` không giới hạn bước không.

---

## Q3. Nạp lại dữ liệu 3 lần thì node nhân bản 3 bản — làm sao chạy lại cho an toàn? [→ §4 Transactions & Ghi Dữ Liệu]

**Bạn sẽ thấy**

Bạn có script nạp 12.000 quan hệ từ 1.000 tài liệu. Chạy lần thứ hai vì còn sót vài quan hệ — kết quả là graph có "Nguyễn Văn A" xuất hiện 3 lần và các cạnh nối vào cả 3 bản. Truy vấn "cô ấy quản lý dự án nào?" bắt đầu trả về kết quả trùng lặp.

**Vì sao**

`CREATE` trong Cypher nghĩa là "tạo mới", không kiểm tra đã tồn tại chưa. `MERGE` mới là "có rồi thì cập nhật, chưa có thì tạo" — nhờ đó toàn bộ thao tác ghi trở nên **chạy lại được** (idempotent): chạy một lần hay một trăm lần thì kết quả như nhau.

**Làm gì**

1. Thay mọi `CREATE` trong đường nạp dữ liệu bằng `MERGE`.
2. Gom theo lô (batch) thay vì gọi từng dòng: `UNWIND $batch AS row` — đây là cách lặp bên trong Cypher, nhanh hơn gọi nhiều lần từ Python.
3. Ghi trong **transaction** (giao dịch) để cả lô thành công hoặc cả lô không. Lỗi giữa chừng không để lại graph nửa vời.
4. Ghép nối bằng khoá duy nhất (tên hoặc mã), không ghép theo thứ tự thêm vào.
5. Chạy lại toàn bộ pipeline ba lần liên tiếp để xác nhận tính chạy-lại-được trước khi đưa lên production.

```python
query = """
UNWIND $batch AS row
MERGE (n:Entity {name: row.name})
SET n.type = row.type, n.updated_at = datetime()
"""
for i in range(0, len(entities), 500):              # lô 500 dòng
    session.execute_write(lambda tx: tx.run(query, batch=entities[i:i+500]))
```

**Kiểm tra**

Đếm số node trước, nạp lại đúng tập dữ liệu cũ ba lần, đếm lại. Số node không được đổi. Kiểm tra thêm cả cạnh: một quan hệ có `confidence` cập nhật được mà không nhân bản — đó là dấu hiệu `MERGE` đang hoạt động đúng.

---

## Q4. Xoá một node thì báo lỗi vì còn cạnh nối vào — xoá kiểu nào cho đúng? [→ §2 và §4 Xoá Dữ Liệu]

**Bạn sẽ thấy**

`MATCH (n:Person {name:'Bob'}) DELETE n` báo lỗi không xoá được, vì Bob còn đang nối bằng cạnh `MANAGES` từ Alice và `WORKS_ON` tới Phoenix. Kẹt giữa hai lựa chọn: xoá hẳn cả cạnh thì mất thông tin lịch sử; giữ lại thì truy vấn cứ lặp lại ra người đã nghỉ.

**Vì sao**

Cạnh trong database đồ thị là một đối tượng độc lập, không tự biến mất khi một đầu node biến mất. Với knowledge graph, việc "Bob không còn ở công ty" **không giống** việc "Bob chưa từng tồn tại" — nên xoá hẳn gần như luôn là sai.

**Làm gì**

1. Với knowledge graph, chọn **xoá mềm**: đặt `n.deleted = true` và `n.deleted_at = datetime()`, giữ nguyên cạnh. Truy vấn của bạn thêm điều kiện lọc node đã xoá.
2. Khi thật sự cần dọn (ví dụ dữ liệu sai từ đầu), dùng `DETACH DELETE` để xoá node kèm toàn bộ cạnh nối. Chỉ dùng khi bạn chắc không mất thông tin.
3. Xoá riêng một cạnh thì dùng `DELETE r` sau `MATCH` — không cần đụng tới node.
4. Nếu quan hệ có thời hạn, cách đúng là đóng quan hệ: đặt `valid_until` thay vì xoá cạnh.
5. Nhớ chạy kiểm tra quan hệ với ontology sau mỗi lần xoá lớn.

```cypher
// xoá mềm — giữ lịch sử
MATCH (n:Person {name:'Bob'}) SET n.deleted = true, n.deleted_at = datetime();
// dọn dữ liệu sai — xoá node kèm cạnh
MATCH (n:Person {name:'Bob'}) DETACH DELETE n;
```

**Kiểm tra**

Sau khi xoá mềm, truy vấn `MATCH (n:Person) WHERE n.deleted IS NULL RETURN n.name` phải không còn "Bob", nhưng `MATCH ()-[r:MANAGES]->(n {name:'Bob'})` vẫn ra — nghĩa là lịch sử còn nguyên. Đối với `DETACH DELETE`, chạy lại `MATCH (n) RETURN count(n)` để xác nhận số node giảm đúng bằng số bạn kỳ vọng.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*