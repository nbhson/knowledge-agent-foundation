# ❓ FAQ — Vector Database (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `README.md` phần trong ngoặc vuông.

---

## Q1. Chroma, Pinecone, Qdrant, Weaviate — chọn cái nào? [→ Tổng Quan Các Vector DB]

**Bạn sẽ thấy**

Bốn lựa chọn, mỗi cái giải quyết một kiểu vấn đề:

| Tên | Chạy ở đâu | Điểm mạnh | Hợp khi |
|---|---|---|---|
| Chroma | local, cài bằng `pip` | Python thuần, lưu xuống đĩa | học, dự án nhỏ |
| Pinecone | cloud | không phải vận hành, có gói miễn phí | số lượng người dùng lớn |
| Qdrant | local hoặc cloud | lọc theo thuộc tính rất nhanh | cần lọc phức tạp |
| Weaviate | local hoặc cloud | tìm kiếm lai: vector + từ khoá | cần cả hai kiểu tìm |

**Vì sao**

Vì khác biệt thật nằm ở câu hỏi bạn sẽ hỏi thường xuyên. Tìm kiếm ngữ nghĩa dựa trên ý nghĩa thì cả bốn đều làm được. Nhưng nếu câu hỏi của bạn luôn kèm điều kiện lọc — "tài liệu của dự án A, năm 2025, loại đặc tả" — thì Qdrant nhanh hơn hẳn, vì nó lọc trước rồi mới so khớp vector. Nếu bạn cần vừa tìm theo ý nghĩa vừa tìm theo từ khoá chính xác, Weaviate làm việc lai đó sẵn.

**Làm gì**

1. Bắt đầu bằng Chroma local — một lệnh `pip install chromadb` là chạy được, không cần tài khoản, không tốn tiền.
2. Xây xong luồng nhớ và truy xuất rồi hãy nghĩ tới chuyện mở rộng.
3. Lên production với lượng truy vấn lớn thì chuyển sang Pinecone để không phải tự vận hành.
4. Cần lọc theo thuộc tính nhiều thì chọn Qdrant.
5. Chỉ chọn Weaviate khi thật sự cần tìm kiếm lai.

```python
import chromadb
client = chromadb.PersistentClient(path="./memory")
collection = client.get_or_create_collection("project_memory")
```

**Kiểm tra**

Nạp khoảng 100 đoạn tài liệu vào Chroma, hỏi một câu không có từ khoá trùng với tài liệu. Nếu vẫn trả về đoạn đúng, đó là tìm theo ý nghĩa và Chroma đã đủ dùng cho giai đoạn hiện tại.

---

## Q2. Cắt tài liệu thành bao nhiêu token là hợp lý? [→ Case Studies Thực Tế — RAG Cho Project Knowledge]

**Bạn sẽ thấy**

Cắt cả một chương dài vào một đoạn, câu trả lời chung chung và không có mốc liên hệ. Cắt quá nhỏ thì câu hỏi bị cắt làm vỡ nghĩa, mô hình trả lời sai.

**Vì sao**

Vì đoạn tài liệu là đơn vị mà mô hình thực sự nhìn thấy. Đoạn to, một câu hỏi có thể rơi vào giữa và không có đủ ngữ cảnh. Đoạn quá nhỏ, mất mạch. Lộ trình gợi ý **500 đến 1.000 token mỗi đoạn, có phần chồng lấn** (overlap).

Chỗ chồng lấn quan trọng vì nó làm một nội dung xuất hiện ở cuối đoạn này và đầu đoạn kế tiếp — một câu hỏi cắt ngang ranh giới vẫn tìm được đoạn chứa nó.

**Làm gì**

1. Cắt theo ranh giới tự nhiên: tiêu đề, đoạn văn, mục — đừng cắt giữa câu.
2. Giữ mỗi đoạn ở khoảng 500–1.000 token, có phần chồng lấn giữa hai đoạn kề nhau.
3. Với tài liệu kỹ thuật có bảng và danh sách mã, để đoạn dài hơn vì chúng bị vỡ khi cắt nhỏ.
4. Ghi kèm thuộc tính cho mỗi đoạn (chủ đề, nguồn, thời gian) để sau này lọc được.
5. Sau khi có kết quả, đo lại bằng [evaluation](../evaluation/): nếu `context_precision` thấp thì thường là do cắt đoạn, không phải do cơ sở dữ liệu vector.

```python
collection.upsert(
    ids=["doc-1"],
    documents=["BHYT cho người lao động: mức đóng 4.5% từ 2026"],
    metadatas=[{"topic": "insurance", "tier": "warm"}]
)
```

**Kiểm tra**

Đặt một câu hỏi ngay tại ranh giới giữa hai đoạn và xem kết quả có chứa đoạn đó không. Nếu trượt, tăng phần chồng lấn rồi hỏi lại.

---

## Q3. Lấy bao nhiêu đoạn thì đủ? [→ Chroma — Retrieve]

**Bạn sẽ thấy**

Lấy 5 đoạn thì có thêm ngữ cảnh nhưng cũng tốn token; lấy 2 đoạn thì rẻ nhưng thường thiếu. Lấy 20 đoạn thì ngữ cảnh đầy ắp nhưng phần lớn là thừa.

**Vì sao**

Vì đoạn thứ 6 trở đi thường không liên quan, mà mô hình vẫn phải đọc và vẫn bị phân tán. Công cụ tìm kiếm trong danh bạ mặc định lấy 5 (`top_k` mặc định là 5), và lộ trình hướng tới đưa 5 đoạn nổi bật nhất vào ngữ cảnh.

Quy tắc đơn giản: **lấy đúng bằng số đoạn bạn còn đủ chỗ để đọc**.

**Làm gì**

1. Bắt đầu với 5 đoạn cho mỗi lần truy vấn.
2. Nếu ngân sách ngữ cảnh chật, hạ xuống 3 và đo xem điểm có giảm không.
3. Nếu mô hình hay trả lời thiếu, tăng lên 8 — nhưng phải đo, vì thêm đoạn cũng tăng chi phí và tăng nhiễu.
4. Khi có nhiều đoạn liên quan, dùng trường `filters` để thu hẹp theo thuộc tính thay vì tăng `top_k`.
5. Ghi lại cấu hình này cạnh mã nguồn, đừng để trong đầu.

```python
results = collection.query(
    query_texts=["chế độ bảo hiểm lao động"],
    n_results=3
)
```

**Kiểm tra**

Chạy cùng một bộ 30 câu hỏi với `top_k` bằng 3, 5 và 8, rồi so điểm. Nếu điểm không đổi giữa 5 và 8, giữ 5.

---

## Q4. Đổi mô hình tạo vector thì dữ liệu cũ có còn dùng được không? [→ 05-troubleshooting — Embedding Mismatch]

**Bạn sẽ thấy**

Bạn đã nạp hàng nghìn đoạn tài liệu bằng một mô hình tạo vector (embedding). Sau đó bạn đổi sang mô hình khác để tìm ra kết quả chính xác hơn. Câu hỏi vẫn cho kết quả nhưng độ liên quan rất tệ.

**Vì sao**

Vì mỗi mô hình tạo ra một không gian toạ độ riêng. Dãy số của "bảo hiểm lao động" trong mô hình A không có nghĩa gì trong không gian của mô hình B, nên khoảng cách cosine tính ra là vô nghĩa.

**Vì sao nữa không lỗi báo**

Vì phần lớn các cơ sở dữ liệu vector không biết bạn đã đổi mô hình. Chúng vẫn trả về kết quả, chỉ là kết quả vô nghĩa. Đây là loại lỗi nguy hiểm nhất: không báo lỗi nhưng hỏng chất lượng.

**Làm gì**

1. Ghi tên và phiên bản mô hình tạo vector cùng lúc với dữ liệu, để sau này biết đoạn nào dùng mô hình nào.
2. Đổi mô hình thì **tạo lại toàn bộ** chỉ mục từ đầu — không ghép vector cũ với mô hình mới.
3. Trước khi tạo chỉ mục lớn, thử trên một tập nhỏ để xác nhận mô hình mới cho kết quả tốt hơn.
4. Dùng mô hình cục bộ nếu có thể — như `nomic-embed-text` — để việc tạo lại chỉ mục không tốn tiền API.
5. Với mô hình chạy tại chỗ, ghim phiên bản cụ thể, không dùng nhãn "mới nhất".

```text
Sai:  index bằng model A → đổi sang model B → query
Đúng:  index bằng model A → test model B trên tập nhỏ
       → thấy tốt hơn → tạo lại chỉ mục với model B
```

**Kiểm tra**

Đặt một đoạn tài liệu đã biết và hỏi bằng chính câu trong đoạn đó. Nếu hệ thống không trả về chính đoạn ấy ở vị trí đầu tiên thì mô hình đang lệch với dữ liệu đã nạp.

---

## Q5. Nhớ bao nhiêu thì đủ, không phải nhét hết vào? [→ Case Studies — Memory Tiering]

**Bạn sẽ thấy**

Bạn có kho tài liệu nội bộ lớn và muốn agent "nhớ" hết. Nhét hết vào ngữ cảnh thì vừa tốn tiền vừa làm mô hình nhiễu.

**Vì sao**

Vì bộ nhớ được chia thành ba tầng, mỗi tầng một chi phí và một tốc độ khác nhau:

| Tầng | Chứa gì | Truy cập |
|---|---|---|
| Lạnh (Tier 1) | file hệ thống, không tạo vector | chậm, chỉ khi cần |
| Ấm (Tier 2) | cơ sở dữ liệu vector | nhanh, theo ngữ nghĩa |
| Nóng (Tier 3) | ngữ cảnh hiện tại | tức thì, luôn có |

Cơ sở dữ liệu vector nằm ở tầng Ấm — đó là lý do nó tồn tại: thay vì dồn toàn bộ kho vào ngữ cảnh, bạn chỉ lấy ra **vài trang liên quan nhất**.

**Làm gì**

1. Đặt tài liệu luôn luôn cần vào tầng Nóng — thứ mà mọi câu hỏi đều dùng.
2. Đặt tài liệu lớn vào tầng Ấm, gắn thuộc tính `tier` để lọc được sau này.
3. Lưu tài liệu hệ thống và dữ liệu tham chiếu ở tầng Lạnh, không cần tạo vector.
4. Dùng bộ lọc theo thuộc tính để giới hạn phạm vi truy vấn, thay vì lấy tất cả rồi lọc tay.
5. Khi bộ nhớ phình qua nhiều vòng chạy, dùng công cụ quản lý ngữ cảnh ở [loop-cli](../loop-cli/) để không để nó phình vô hạn.

```python
metadatas=[{"topic": "insurance", "tier": "warm"}]
```

**Kiểm tra**

Đo số token ngữ cảnh trung bình một lượt trước và sau khi tách bộ nhớ ba tầng. Nếu con số giảm mà điểm trả lời không giảm thì bạn đang lãng phí tiền.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*