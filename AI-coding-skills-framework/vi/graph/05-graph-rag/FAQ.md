# ❓ FAQ — GraphRAG (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc.

---

## Q1. Dựng chỉ mục GraphRAG tốn gấp 111 lần RAG thường — có đáng không? [→ §1 và §8 Chi phí, khi nào dùng]

**Bạn sẽ thấy**

Bạn có 1.000 tài liệu, khoảng 500.000 token chữ. RAG thường chỉ cần nhúng vector (embed) — khoảng **0.05 USD**. GraphRAG thì phải gọi mô hình ngôn ngữ để trích thực thể và quan hệ, tóm tắt từng cụm: khoảng **5.55 USD**, gấp hơn 100 lần. Với 50 tài liệu nội bộ thì con số này chưa đáng lo, nhưng nếu chạy lại mỗi tuần thì tiền bạc đáng cân nhắc.

**Vì sao**

Chi phí phần lớn nằm ở bước *trích xuất* và *tóm tắt*, vì hai việc đó đều cần mô hình ngôn ngữ, không phải chỉ tính toán vector. Nhưng đây là **chi phí một lần khi dựng** (offline), không phải mỗi câu hỏi. Đổi lại, câu hỏi tổng hợp nhiều tài liệu được trả lời đầy đủ hơn rõ rệt.

**Làm gì**

1. Hỏi trước một câu: câu hỏi của tôi có cần **tổng hợp từ nhiều tài liệu** không. Không cần thì RAG thường đã đủ.
2. Nếu kho tài liệu dưới 100 file và phần lớn câu hỏi là kiểu "một sự thật đơn lẻ" → **đừng dựng GraphRAG**.
3. Nếu câu hỏi nhiều bước, cần tổng hợp hoặc so sánh xu hướng trên cả kho → GraphRAG đáng tiền.
4. Đang phân vân thì dùng bản nhẹ hơn: LightRAG (nhanh hơn khoảng 10 lần, chi phí khoảng 1/3–1/4) hoặc HippoRAG bản 2 (trả lời nhiều bước với ít token hơn, rẻ hơn khoảng 20 lần).
5. Dùng mô hình chạy cục bộ qua Ollama (ví dụ `gemma3:12b`) ở bước trích và tóm tắt — đây là bước tốn tiền nhất, chuyển sang local là cách giảm chi phí lớn nhất.

| Loại câu hỏi | Dùng gì |
|---|---|
| Một sự thật đơn lẻ, 1 bước | RAG thường hoặc tìm cục bộ |
| Nối 2–4 bước | Tìm cục bộ trên đồ thị |
| Tổng hợp, xu hướng, so sánh | Tìm toàn cục |

**Kiểm tra**

Làm Lab 1: 20 tài liệu cùng một chủ đề, chạy cả hai kiểu trên 10 câu hỏi, tự đánh giá câu nào thắng. Ghi lại chi phí LLM của mỗi lần. Chỉ dựng GraphRAG đầy đủ khi số câu thắng đủ bù chi phí dựng chỉ mục.

---

## Q2. Hỏi "xu hướng AI 2024 là gì" thì câu trả lời rỗng hoặc nói bừa — dùng cách tìm nào? [→ §3 Tìm Cục Bộ và Toàn Cục]

**Bạn sẽ thấy**

Với câu hỏi "Thị trường AI năm 2024 có xu hướng nào nổi bật?", hệ thống trả về 5 đoạn văn rời rạc, mỗi đoạn nói một khía cạnh, không đoạn nào nói toàn cảnh. Có lần còn trả lời chắc nịch một điều mà không tài liệu nào viết — đó là bịa. Nguyên nhân: câu hỏi không chứa tên thực thể cụ thể nào để bám vào.

**Vì sao**

Có hai kiểu truy vấn khác nhau. **Tìm cục bộ** bám vào thực thể trong câu hỏi rồi mở rộng 1–2 bước quanh nó — giống tra hồ sơ một người. **Tìm toàn cục** không tìm thực thể nào, mà đưa *tóm tắt từng cụm* cho mô hình ngôn ngữ, rồi gộp các câu trả lời bộ phận lại (cách chia xử lý song song rồi tổng hợp — gọi là chia rồi gộp, map-reduce). Câu hỏi tổng quan rơi đúng vào loại thứ hai.

**Làm gì**

1. Tự kiểm trước: câu hỏi có **thực thể cụ thể** không. Có (tên người, tên dự án, mã hợp đồng) → tìm cục bộ.
2. Không có thực thể nào → tìm toàn cục. Đừng cố ép nó vào một node.
3. Với tìm cục bộ, mở rộng 1–2 bước quanh node đã khớp, thu thập cả đường đi (path) để câu trả lời có dẫn chứng.
4. Với tìm toàn cục, yêu cầu mỗi cụm trả lời hoặc nói rõ "không có thông tin" — rồi mới gộp. Nhờ vậy biết cụm nào không liên quan.
5. Đừng hỏi chi tiết dựa trên tóm tắt cụm. Tóm tắt không có chi tiết, hỏi sâu vào đó thì mô hình sẽ bịa. Câu hỏi chi tiết → quay về tìm cục bộ.

```text
Câu hỏi toàn cục: "Xu hướng AI 2024?"
  map   : mỗi tóm tắt cụm → 1 câu trả lời hoặc "Không có thông tin"
  reduce: gộp các câu còn lại thành câu trả lời cuối, kèm nguồn từ cụm nào
```

**Kiểm tra**

Chạy cùng câu hỏi đó qua cả hai chế độ. Chế độ toàn cục phải cho câu trả lời có nhiều mặt (đầu tư, quy định, y tế) và mỗi mặt đều dẫn được về cụm nguồn. Nếu vẫn thấy khẳng định không có bằng chứng, hãy thu hẹp tập cụm được đưa vào.

---

## Q3. Cứ tăng "độ phân giải" của cụm thì cụm toàn vỡ, giảm thì chỉ còn 2 cụm — chọn thế nào? [→ §4 Chia Cụm Leiden]

**Bạn sẽ thấy**

Bạn chạy thuật toán chia cụm trên đồ thị 1.000 thực thể. Với `resolution = 0.5` (mức phân giải thấp) thì ra 3 cụm khổng lồ, mỗi cụm lẫn mọi thứ. Với `resolution = 2.0` (cao) thì ra 180 cụm nhỏ xíu, mỗi cụm chỉ vài node rồi tóm tắt chẳng được gì.

**Vì sao**

Tham số `resolution` quyết định độ mịn của việc chia cụm: thấp → ít cụm lớn; cao → nhiều cụm nhỏ. Giá trị mặc định **1.0** là điểm khởi đầu, không phải giá trị đúng cho dữ liệu của bạn.

**Làm gì**

1. Chạy thử ba mức **0.5, 1.0, 2.0** như README gợi ý, in ra số cụm và vài tên node đầu của mỗi cụm.
2. Tiêu chí chọn: một cụm lý tưởng gom đúng **một chủ đề** và đủ lớn để tóm tắt bằng 2–4 câu.
3. Quá nhiều cụm → giảm `resolution`. Quá ít cụm → tăng.
4. Nhớ rằng mỗi cụm sẽ tốn **một lần gọi mô hình ngôn ngữ** để tóm tắt. Tách quá nhiều cụm làm chi phí tăng vọt với ít giá trị.
5. Cần tóm tắt ở nhiều mức chi tiết thì dựng cụm theo tầng: cấp 0 là toàn bộ đồ thị, cấp 1 là vài cụm lớn, cấp 2 là các cụm nhỏ hơn, cấp cuối là từng thực thể.

```python
comms = detect_communities(G, resolution=1.0)   # thử 0.5 / 1.0 / 2.0
for cid, members in comms.items():
    print(cid, len(members), members[:5])          # tên node đầu để đoán chủ đề
```

**Kiểm tra**

Với mỗi mức, hỏi cùng một câu toàn cục và so sánh chất lượng. Đồng thời đếm số cụm để cân đối với chi phí gọi mô hình. Mức tốt nhất là mức cho câu trả lời tốt nhất *với chi phí thấp nhất*, không phải mức cho nhiều cụm nhất.

---

## Q4. Hỏi một chi tiết lặp về trong một tài liệu, GraphRAG lại tệ hơn RAG thường — vì sao? [→ §8 Khi nào KHÔNG nên dùng]

**Bạn sẽ thấy**

Với câu hỏi kiểu "Điều 5 của hợp đồng X nói gì?", hệ thống GraphRAG trả lời vòng vo, thậm chí tự thêm chi tiết không có trong tài liệu. Bật lại RAG thường thì trả lời đúng ngay. Ngược lại, với câu hỏi tổng quan, RAG thường trả lời yếu hơn hẳn.

**Vì sao**

Nghiên cứu so sánh có hệ thống (RAG so với GraphRAG) cho thấy GraphRAG **không phải lúc nào cũng thắng**. Với câu hỏi một sự thật đơn lẻ, phần tử duyệt đồ thị là chi phí vô ích. Với tìm theo cụm, bản tóm tắt thiếu ngữ cảnh chi tiết nên mô hình dễ "bịa" khi bị hỏi sâu — đây là điểm yếu riêng của cách tìm toàn cục.

**Làm gì**

1. Đừng dựng GraphRAG cho một bộ dữ liệu nhỏ chỉ phục vụ câu hỏi loại một. Quy tắc thực dụng: **dưới 100 tài liệu, câu trả lời chủ yếu là một sự thật đơn → RAG thường đủ dùng**.
2. Dùng cả hai cùng lúc theo loại câu hỏi: chi tiết một sự thật → RAG thường; nhiều bước hoặc tổng hợp → GraphRAG.
3. Khi tìm toàn cục mà cần chi tiết, luôn mở rộng lại xuống cục bộ để lấy đường đi thật trước khi trả lời.
4. Kiểm tra chất lượng trên tập câu hỏi thật của bạn, đừng tin vào kết quả trên tập ví dụ.
5. Đứng ở giữa thì dùng **LightRAG** hoặc **HippoRAG** — nhẹ hơn, ít tốn token hơn.

| Câu hỏi | Thắng hơn |
|---|---|
| Một sự thật đơn lẻ | RAG thường |
| Nối 2–4 bước qua nhiều node | GraphRAG |
| Tổng hợp cả kho tài liệu | GraphRAG |

**Kiểm tra**

Lấy 30 câu hỏi thật của bạn, chạy cả hai kiểu, đánh dấu câu nào trả lời sai. Nếu phần lớn câu sai thuộc nhóm một sự thật đơn lẻ thì đừng dựng GraphRAG; nếu nhóm đa bước chiếm đa số thì nó đang đáng dùng.

---

## Q5. Kết hợp tìm theo chữ, duyệt đồ thị và tìm toàn văn — gộp kết quả bằng cách nào? [→ §6 Các loại Retriever và cách gộp]

**Bạn sẽ thấy**

Bạn chạy đồng thời ba nguồn kết quả: tìm theo vector (nghĩa chữ), duyệt đồ thị (quan hệ), và tìm toàn văn (từ khoá). Cả ba đều cho điểm số, nhưng thang đo khác nhau — vector cho điểm 0–1, duyệt đồ thị trả về số lượng node, toàn văn cho 0–1. Cộng tay xong, một nguồn có điểm lớn hơn đã đẩy hết thứ hạng của các nguồn khác.

**Vì sao**

Khi các nguồn dùng thang điểm khác nhau, phép cộng trực tiếp là vô nghĩa. Có một cách gộp không cần chuẩn hoá: **RRF** — chỉ nhìn **thứ hạng** của mỗi kết quả, không nhìn điểm, cộng `1 / (60 + thứ hạng)` cho mỗi danh sách. Kết quả đầu một danh sách nhận khoảng 1/61; một mục thứ 8 nhưng có mặt ở cả hai danh sách nhận khoảng 1/68 + 1/68, tức là **vượt lên trên**.

**Làm gì**

1. Với 3 nguồn trở lên và không muốn tinh chỉnh trọng số → **RRF**. Giá trị `k = 60` là quy ước thông dụng, không cần chỉnh.
2. Cần câu hỏi tự do như "Ai quản lý dự án nhiều nhất?" → cho mô hình ngôn ngữ dịch thành câu truy vấn Cypher rồi chạy (retriever dạng văn bản sang truy vấn). Đây là lớp retriever dạng văn bản-sang-truy-vấn.
3. Câu hỏi trả về rỗng thì cho mô hình tự sửa câu truy vấn một lần, rồi mới trả lời người dùng.
4. Khi dịch câu hỏi sang truy vấn, **đừng nhồi toàn bộ lược đồ** — chỉ nạp tên loại thực thể, tên thuộc tính và vài quan hệ cha-con quan trọng. Nhồi hết sẽ tốn token và làm mô hình lẫn.
5. Chọn retriever theo dạng câu hỏi: tìm đoạn văn nói về X → tìm vector; biết đoạn văn đó liên quan ai → vector rồi duyệt thêm cạnh.

```python
def rrf_score(lists, k=60):
    fused = {}
    for lst in lists:                     # vector_rank, graph_rank, fulltext_rank
        for rank, item in enumerate(lst, start=1):
            fused[item] = fused.get(item, 0.0) + 1.0 / (k + rank)
    return dict(sorted(fused.items(), key=lambda x: -x[1]))
```

**Kiểm tra**

Chạy cùng 20 câu hỏi với (a) chỉ một nguồn, (b) gộp bằng cộng điểm thô, (c) gộp bằng RRF. Đo độ chính xác trong 10 kết quả đầu. Nếu RRF không hơn (a), đồ thị của bạn chưa đủ thông tin để thêm vào.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*