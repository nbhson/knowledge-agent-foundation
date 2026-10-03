# ❓ FAQ — Truy xuất bộ nhớ & kiến thức (chuyện thật, dễ hiểu)

Nếu câu hỏi khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Bot của tôi trả lời sai luật vừa mới sửa, tôi có phải train lại model không? [→ §1.1, §2.1]

**Bạn sẽ thấy**

Bạn hỏi "mức đóng BHYT hiện tại là bao nhiêu", bot đáp 4,5% — trong khi quy định mới
đã lên 5%. Nó cứ dùng lại kiến thức đóng băng từ thời điểm huấn luyện, hoặc tệ hơn là
bịa ra một con số nghe rất thuyết phục. Nghiên cứu của Google (2020) đo được hiệu ứng
này rõ ràng: có truy xuất tài liệu, tỉ lệ bịa thông tin rơi từ 27% xuống còn 3%.

**Vì sao**

Mô hình ngôn ngữ không có bộ nhớ riêng; thứ nó biết đã bị đóng băng trong trọng số. Nguyên
tắc của phần này là **kiến thức phải được đưa vào lúc trả lời, không phải nạp vào model**.
Cũng vì vậy nhiều đội không nâng cấp model: chi phí một câu hỏi rơi từ 0,03 USD (GPT-4) xuống
0,002 USD nếu dùng GPT-3.5 kèm truy xuất — giảm 93%.

**Làm gì**

1. **Chuẩn bị kho (làm một lần, ngoài đường chạy):** làm sạch → cắt đoạn 500 ký tự, chồng
   lấn 50 → sinh vector bằng `nomic-embed-text` (768 chiều) → lưu vào kho vector kèm
   văn bản gốc và metadata.
2. **Khi có câu hỏi:** sinh vector cho câu hỏi, nhưng nhớ thêm tiền tố `"query: "` để
   phân biệt câu hỏi với tài liệu.
3. **Lấy 50 đoạn thô**, rồi dùng bộ chấm chéo (cross-encoder) chấm lại từng cặp câu hỏi–đoạn
   và giữ lại 5 đoạn đúng nhất.
4. **Dán 5 đoạn đó vào prompt** kèm câu lệnh bắt buộc chỉ trả lời dựa trên tài liệu được
   đưa, không dùng kiến thức ngoài.

```python
embedder = Embedder(model="nomic-embed-text")
embedder.embed_batch(chunks, batch_size=32)   # ngoài đường chạy
qv = embedder.embed_query("mức đóng BHYT hiện tại")  # = embed("query: ...")
hits = vector_store.search(qv, top_k=50)
best = reranker.rerank(query, hits, top_k=5)
```

**Kiểm tra**

Đổi một đoạn trong tài liệu gốc, hỏi lại đúng câu cũ và kiểm tra câu trả lời có dùng số
liệu mới. Đo `Precision@10` trên 50 câu hỏi thật của bạn; dưới 85% thì kho chưa đủ tốt và
nên sửa cách cắt đoạn trước, đừng vội đổi model.

---

## Q2. Tôi gõ mã lỗi vào mà search không ra, đổi sang câu tiếng Việt lại ra — làm sao? [→ §4.1, §4.3]

**Bạn sẽ thấy**

Hỏi `ERR_AUTH_401` thì kết quả trống rỗng, dù trong tài liệu có nguyên cả mục lỗi này.
Nhưng hỏi "lỗi xác thực token hết hạn" thì ra đúng. Ngược lại, hỏi "phòng ngừa bệnh tim"
thì tìm kiếu từ khóa không ra, dù tài liệu viết "phòng ngừa bệnh tim".

**Vì sao**

Tìm theo vector hiểu ý nghĩa nên bỏ sót từ khóa chính xác (mã số, tên hàm, mã hàng);
tìm theo từ khóa BM25 (thuật toán xếp hạng theo tần suất từ, có điều chỉnh độ dài tài liệu)
thì đúng với mã số nhưng không hiểu nghĩa. Đây là hai kiểu lỗi ngược nhau, không phải cái nào
tốt hơn cái nào.

**Làm gì**

1. Chạy **cả hai** cách tìm rồi hợp nhất bằng RRF (Reciprocal Rank Fusion — cộng điểm theo
   thứ hạng, không cần chuẩn hoá điểm của hai bên về cùng thang đo).
2. Với mỗi tài liệu `d` xuất hiện ở hạng `r` trong một danh sách, cộng `1/(60 + r)`; tổng
   của ba danh sách quyết định thứ tự cuối.
3. Với ví dụ trong tài liệu: `doc_A` hạng 1 (vector), hạng 3 (từ khoá), hạng 1 (metadata) →
   `0,0164 + 0,0159 + 0,0164 = 0,0487`, vượt `doc_F` chỉ xuất hiện một lần.
4. Sau khi hợp nhất, chấm lại bằng bộ chấm chéo rồi mới lấy 5 đoạn cuối.

```python
def reciprocal_rank_fusion(rankings, k=60):
    scores = {}
    for lst in rankings:
        for rank, doc_id in enumerate(lst, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)
```

**Kiểm tra**

Chọn 20 câu hỏi thật của bạn, một nửa chứa mã lỗi hoặc mã định danh, một nửa hỏi bằng tiếng
Việt không trùng từ nào trong tài liệu. Chạy ba cách riêng rồi chạy RRF; nếu RRF không tốt
hơn hẳn từng cách trên bộ 20 câu đó, hãy kiểm tra lại xem hai danh sách có thật sự độc lập
hay không — hay bị lấy từ cùng một nguồn.

---

## Q3. Cắt tài liệu dài thành đoạn con kiểu gì, cắt sai thì bot tìm ra nửa câu? [→ §1.4]

**Bạn sẽ thấy**

Một tài liệu 10 trang ra 50 đoạn. Cắt theo số ký tự cố định (500 ký tự, chồng lấn 50) thì
cắt ngang giữa câu: một đoạn kết bằng "mức đóng là 4,5%", đoạn sau mở đầu bằng "% lương cơ
sở" — tìm đúng câu hỏi về mức đóng thì cả hai đoạn đều không đủ ý.

**Vì sao**

Chất lượng tìm kiếm phụ thuộc trực tiếp vào cách cắt, chứ không phải vào lựa chọn kho vector.
Cắt nhỏ quá thì mất ngữ cảnh, cắt lớn quá thì kho phình và nhiễu.

| Cách cắt | Chất lượng | Tốc độ | Hợp với |
|---|---|---|---|
| Cố định theo ký tự | thấp | rất nhanh | thử nhanh |
| Lùi đệ quy theo dấu ngắt dòng | trung bình | nhanh | văn bản thường |
| Theo ngữ nghĩa | cao | chậm | tài liệu phức tạp |
| Theo cấu trúc tài liệu | cao | khá | Markdown, HTML |

**Làm gì**

1. Chọn cắt **theo cấu trúc trước**: tách ở tiêu đề Markdown, giữ tiêu đề làm metadata
   cho mọi đoạn bên trong.
2. Nếu một mục vẫn quá lớn (giới hạn 1.000 ký tự), tách tiếp theo đoạn văn, không tách
   theo ký tự.
3. Muốn dễ hơn thì dùng bộ tách lùi đệ quy với thứ tự ưu tiên: `\n\n` → `\n` → `. ` → ` `.
4. Ghim `start_char` / `end_char` của mỗi đoạn vào metadata để sau này trả về đúng trang.

```python
def recursive_split(text, chunk_size=500, separators=["\n\n", "\n", ". ", " "]):
    if len(text) <= chunk_size: return [text]
    for sep in separators:
        if sep in text:
            return [p.strip() for p in text.split(sep) if p.strip()]
    return [text]
```

**Kiểm tra**

Mở 10 đoạn ngẫu nhiên từ kho và đọc bằng mắt: có đoạn nào bắt đầu bằng dấu phẩy hoặc
kết bằng nửa câu không? Sau đó hỏi lại 10 câu mà bạn biết đáp án nằm ở đâu, và đếm bao
nhiêu câu tìm thấy đoạn chứa đúng đoạn văn đó.

---

## Q4. Kho vector của tôi chậm dần và kết quả tệ hơn mà không biết vì sao — đo cái gì? [→ §8.2, §8.4]

**Bạn sẽ thấy**

Tìm kiếm một câu rất lâu, index phình gấp ba so với số tài liệu thật, và sau khi nâng cấp
mô hình sinh vector thì kết quả tệ đi trong khi không có lỗi nào được báo. Ngưỡng cảnh báo
gợi ý trong tài liệu: điểm số trung bình của kết quả đứng đầu giảm quá 0,08 là lúc cần
dừng lại.

**Vì sao**

Ba lỗi âm thầm phổ biến nhất: trộn vector của hai phiên bản sinh vector khác nhau vào cùng
một chỗ (hỏng hẳn cách xếp hạng nhưng không báo lỗi), cứ chép thêm mà không xoá bản cũ, và
đẩy bản trùng vào chỗ làm cơ chế hợp nhất RRF bị loãng phiếu.

**Làm gì**

1. Lưu kèm mỗi vector: `doc_id`, `content_sha256`, `embed_version`, danh sách `chunk_ids`.
   Chỉ sinh lại dòng nào có `sha` đổi hoặc `embed_version` khác bản đang chạy.
2. Lúc ghi, khử trùng: hash khớp chính xác thì bỏ qua; gần trùng thì kiểm tra vector và
   bỏ qua nếu độ gần ≥ 0,97.
3. Đánh dấu dữ liệu cũ bằng `valid_until` và `supersedes`; lúc truy vấn thì loại điều kiện
   hết hạn hoặc đã bị đánh dấu xoá.
4. Đặt ngưỡng an toàn: không có kết quả hoặc điểm cao nhất dưới 0,25 → thử lại chỉ bằng
   tìm từ khoá; vẫn rỗng thì trả lời thẳng là không tìm thấy căn cứ, tuyệt đối không đoán.
5. Ghi log mỗi câu hỏi: số kết quả, điểm cao nhất, thời gian, phiên bản sinh vector, có
   dùng đường dự phòng hay không.

```python
CURRENT = "nomic-embed-text:v2"
if not hits or top < 0.25:
    hits = bm25_search(q, tenant_id); fallback = "bm25-only-retry"
if not hits:
    return {"answer": None, "abstain": True, "reason": "no grounding found"}
```

**Kiểm tra**

Dựng bảng theo dõi bốn chỉ số: tỉ lệ trúng ở 5 kết quả đầu, tỉ lệ không có kết quả, tỉ lệ
điểm thấp, và độ trễ ở mốc 50%/99%. Thêm đường dự phòng: nếu độ trỷ 99% vượt 800 mili giây
trong 2 phút thì tự hạ xuống chỉ dùng tìm từ khoá.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: `README.md`.*
