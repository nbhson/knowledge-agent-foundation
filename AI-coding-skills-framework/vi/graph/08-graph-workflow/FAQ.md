# ❓ FAQ — Quy Trình Vận Hành Đồ Thị (Graph Workflow)

Câu hỏi nào khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Thêm đúng 1 tài liệu mới mà phải dựng lại cả graph — có cách nào rẻ hơn không? [→ §2 Incremental Updates]

**Bạn sẽ thấy**

Bạn có 10.000 tài liệu đã nạp xong. Sáng thứ hai có thêm 50 tài liệu, bạn chạy lại toàn bộ: mất khoảng **2 giờ** và **100 USD** chi phí gọi mô hình ngôn ngữ, rồi dịch vụ ngừng phục vụ suốt thời gian đó. Khảo sát Neo4j năm 2024 chỉ ra **68% sự cố** trên graph đến từ đúng chỗ này: không có đường cập nhật từng phần.

**Vì sao**

Dựng lại toàn bộ tốn chi phí tuyến tính theo số tài liệu, kể cả những cái đã xử lý đúng. Chạy từng phần thì chỉ tốn cho tài liệu mới: một tài liệu, 2 lượt gọi mô hình, khoảng **0.01 USD** và **5 giây**. Microsoft GraphRAG đo được giảm **90%** chi phí đánh chỉ mục lại khi dùng cách này.

**Làm gì**

1. Chỉ trích xuất trên tài liệu mới, rồi hỏi graph: thực thể này đã tồn tại chưa; có thì cập nhật thuộc tính, chưa có thì thêm.
2. Ghi bằng `MERGE` chứ không dùng `INSERT` — chạy lại 100 lần kết quả vẫn như nhau.
3. Chọn chế độ theo tần suất: nạp lần đầu dùng batch, hằng ngày dùng micro-batch 10–100 tài liệu, thay đổi tức thì dùng streaming.
4. Ghi lại mã tài liệu nguồn vào mỗi node/cạnh để sau này xoá được đúng nhóm.

```python
entities = [{"name": "NewPerson", "type": "Person"}]
new = [e for e in entities if not self._entity_exists(e["name"])]
for ent in new: self._upsert_entity(ent, "doc_001")
# Neo4j: MERGE (n:Entity {name:$name}) SET n += $props
```

**Kiểm tra**

Nạp 1.000 tài liệu, sau đó thêm 10 tài liệu: so sánh thời gian và chi phí của cách dựng lại 1.010 tài liệu với cách chỉ xử lý 10 tài liệu. Chạy cùng một tài liệu 3 lần, số node phải giữ nguyên — không được nhân đôi.

---

## Q2. Gộp 200 thực thể trùng tên, quan hệ của chúng có biến mất không? [→ §2.2 merge_entities]

**Bạn sẽ thấy**

Danh bạ tài liệu có "Nguyễn Văn A" ở 200 chỗ khác nhau, graph sinh ra 200 node riêng, mỗi node chỉ nối vài cạnh. Gộp lại thành một node thì câu hỏi multi-hop đi qua đứt — một câu trả lời vốn ra bằng đường 3 bước giờ thành không có đường.

**Vì sao**

Gộp không chỉ là đổi tên. Nếu chỉ dùng lệnh đổi nhãn rồi xoá node cũ, toàn bộ cạnh nối vào node cũ sẽ bị xoá theo — đúng trường hợp bạn gặp.

**Làm gì**

1. Chọn một node chuẩn (canonical) làm đích đến.
2. **Chuyển cả cạnh ra lẫn cạnh vào** của mọi node trùng sang node chuẩn, giữ nguyên thuộc tính.
3. Chỉ xoá node trùng **sau khi** đã chuyển đủ cạnh.
4. Trong Cypher thì tạo cạnh mới ở node chuẩn, sao chép thuộc tính rồi mới xoá cạnh cũ.

```python
for successor in list(self.graph.successors(dup_name)):
    edata = self.graph.get_edge_data(dup_name, successor)
    self.graph.add_edge(canonical_name, successor, **edata)
self.graph.remove_node(dup_name)
```

**Kiểm tra**

Trước khi gộp, lưu lại tổng số cạnh. Sau khi gộp 200 node, tổng số cạnh phải bằng hoặc lớn hơn (các cạnh trùng lặp có thể chồng lên nhau). Chạy lại bộ câu hỏi multi-hop quanh node chuẩn và xác nhận không câu nào mất đường.

---

## Q3. Nhân viên chuyển team rồi hỏi "quý 1/2024 ai quản lý?" — không có lịch sử thì không trả lời được [→ §3 Versioning & Temporal Graphs]

**Bạn sẽ thấy**

Bạn cập nhật quan hệ quản lý bằng cách ghi đè cạnh cũ. Sau đó có người hỏi lại lịch sử cũ, hệ thống trả về quan hệ hiện tại — sai hoàn toàn. Cũng có trường hợp gộp nhầm xoá mất dữ liệu mà không có dấu vết để khôi phục.

**Vì sao**

Graph luôn thay đổi: người đổi bộ phận, dự án bị hủy, hợp đồng hết hạn. Xoá cạnh cũ nghĩa là mất lịch sử và không thể trả lời câu hỏi dạng "hồi thời đó thế nào".

**Làm gì**

1. Cho mọi cạnh hai thuộc tính `valid_from` và `valid_until`; `valid_until` rỗng nghĩa là đang hiệu lực. Ghi thêm `created_at` và `created_by`.
2. Cập nhật thì **đóng hạn cạnh cũ** rồi tạo cạnh mới, không xoá.
3. Song song giữ sổ ghi mọi thao tác tạo/cập nhật/xoá, kèm `actor` như `user:alice`, `pipeline:etl`, `loop:daily-triage`, và `prev_state` để quay lui.
4. Xoá cũng chỉ là **ghi thêm một sự kiện**, nên luôn quay lui được.

```python
temporal_edge = {"from":"Alice","to":"TeamA","type":"MANAGES",
  "valid_from":date(2023,1,1), "valid_until":date(2024,6,30),
  "created_by":"ingest:doc_123"}
```

**Kiểm tra**

Hỏi cùng một node ở hai mốc thời gian khác nhau, kết quả phải khác và đúng dữ liệu. Thử quay lui về một sự kiện và đối chiếu trạng thái graph trước đó với bản ghi.

---

## Q4. Batch nạp giữa chừng bị lỗi, khôi phục lại mất 2 ngày — chặn thế nào? [→ §5 & §6 Observability, Error Recovery]

**Bạn sẽ thấy**

Lần chạy 500 tài liệu, chết ở bước 380 vì hết thẻ API. Graph đang ở trạng thái nửa vời: có dữ liệu của 380 tài liệu cộng thêm một phần của tài liệu 381, và không có gì để quay lui. Báo cáo cuối cùng vẫn ghi "thành công". Nghiên cứu 2025 đo được quy trình có checkpoint giúp giảm **80%** thời gian khôi phục.

**Vì sao**

Ba thứ thường thiếu: không có điểm dừng giữa chừng để quay lui, không định nghĩa sẽ làm gì khi một bước lỗi (thử lại / bỏ qua / dừng), và không đo được từng bước mất bao lâu, vào ra bao nhiêu thực thể.

**Làm gì**

1. Đánh dấu `checkpoint` cho các bước quan trọng; khi bước sau lỗi chế độ `fail`, tự quay về điểm gần nhất và ghi trạng thái `rolled_back`.
2. Mỗi bước khai rõ xử lý lỗi: `fail` (dừng cả pipeline), `skip` (bỏ qua bước đó), hoặc `retry` (thử lại).
3. Thử lại có lùi thời gian chờ: lần 1 chờ 2 giây, lần 2 chờ 4 giây, lần 3 thì mới ném lỗi.
4. Dùng circuit breaker: 5 lần lỗi liên tiếp thì ngừng gọi, 60 giây sau mới thử lại — tránh đốt tiền vào một dịch vụ đang chết.
5. Bắt buộc báo cáo số liệu mỗi lần chạy: số thực thể vào/ra, tỉ lệ gộp trùng, số lỗi, thời gian từng bước.

```python
@retry_with_backoff(max_attempts=3, backoff_factor=2.0)
def safe_extract(text): return breaker.call(extract_entities, text)
breaker = CircuitBreaker(failure_threshold=3)   # ngưỡng lỗi
```

**Kiểm tra**

Cố tình làm bước `validate` lỗi giữa pipeline và xác nhận trạng thái là `rolled_back`, dữ liệu về đúng điểm gần nhất. Quy trình lỗi ở bước cuối không được ghi báo cáo "thành công".

---

## Q5. Nên chạy bằng Airflow, Prefect, GitHub Actions hay crontab? [→ §4 Orchestration]

**Bạn sẽ thấy**

Bạn muốn việc nạp tài liệu tự chạy lúc 9h sáng và tự phát hiện file mới trong thư mục dữ liệu. Mở năm công cụ, không biết chọn cái nào: Airflow nặng và học nhiều, crontab lại quá mỏng, không có khả năng thử lại.

**Vì sao**

Khác biệt nằm ở mức độ: lịch chạy, xử lý lỗi, trạng thái, và khả năng nhìn thấy tiến trình. Chọn sai sẽ tốn hàng tuần để dựng lại.

**Làm gì**

1. Dùng **Prefect** cho nghiệp vụ Python: mỗi bước là một `@task`, tự thử lại 3 lần cách nhau 10 giây, và có thể đặt lịch theo biểu thức cron `0 * * * *`.
2. Dùng **GitHub Actions** khi muốn nạp ngay khi có người push tài liệu mới vào `data/raw_docs/*.md`.
3. Dùng **Airflow** khi đã có nhiều luồng dữ liệu phụ thuộc nhau cần vẽ thành đồ thị phụ thuộc.
4. **crontab** chỉ hợp với script nhỏ chạy cục bộ; muốn tự chạy lại và tự phân tích lỗi thì đừng dùng.

```python
@task(retries=3, retry_delay_seconds=10)
def extract_task(documents): ...
schedule={"cron": "0 * * * *"}   # mỗi giờ
```

**Kiểm tra**

Đặt lịch chạy thật 2–3 ngày và xác nhận: lần chạy sau không xử lý lại tài liệu cũ, lỗi tạm thời được thử lại, và khi số node mới vượt 100 thì việc tìm cộng đồng được chạy lại.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*