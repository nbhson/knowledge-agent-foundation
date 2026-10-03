# ❓ FAQ — Đánh Giá Chất Lượng Graph & GraphRAG

Câu hỏi nào khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Bot trả lời sai mà không biết sai ở tìm kiếm hay ở câu trả lời — đo thế nào? [→ §2 & §3 Retrieval, Generation]

**Bạn sẽ thấy**

Sếp hỏi ba câu. Câu "ngân sách Phoenix?" đúng 500 triệu. Câu "ai duyệt Phoenix?" đúng tên nhưng độ tin cậy chỉ 0.6. Câu "team AI có bao nhiêu người?" trả lời 15 trong khi tài liệu ghi 10 — sai. Bạn không biết lỗi nằm ở đâu: graph thiếu dữ liệu, hệ thống lấy sai ngữ cảnh, hay mô hình ngôn ngữ tự bịa thêm.

**Vì sao**

Nếu chỉ đo điểm câu trả lời cuối, bạn phải chỉnh mù. Chỉ số trung gian đo phần "tìm" và phần "diễn giải" tách bạch; nghiên cứu 2024 ghi nhận việc tách hai phần này giúp giảm một nửa thời gian truy vết lỗi.

**Làm gì**

1. **Phần tìm kiếm**: đo độ chính xác trong 5 kết quả đầu (P@5), độ đầy đủ (R@5), và thứ hạng trung bình của kết quả đúng (MRR).
2. **Phần diễn giải**: đo trung thành (faithfulness) — có mệnh đề nào trong câu trả lời không có bằng chứng; tỉ lệ bịa = 1 trừ trung thành.
3. Với câu hỏi nhiều bước, thêm **độ chính xác đường đi**: có bao nhiêu đường trả về đúng so với đường chuẩn.
4. Chạy cả hai bộ chỉ số trên cùng một bộ câu hỏi đối chiếu chuẩn, tách theo từng câu chứ không gộp chung một điểm.

```python
# retrieved = [doc_1, doc_3, doc_5, doc_7, doc_9], relevant = [doc_1, doc_5, doc_10]
P@5 = 2/5 = 0.40      R@5 = 2/3 = 0.67      MRR = 1.00  # doc_1 ở hạng 1
paths = [["Alice","Bob","Phoenix"], ["Alice","Dave","Atlas"]]  # 1/2 đúng → 0.50
```

**Kiểm tra**

Khi một câu hỏi trả lời sai, bạn phải chỉ ra được ngay: chỉ số nào ở phần tìm đã đỏ. Nếu P@5 và MRR tốt mà câu trả lời vẫn sai thì lỗi nằm ở phần sinh câu trả lời, không phải graph.

---

## Q2. Graph có 5.000 node rồi mà bot vẫn bịa — nên đo graph hay đo bot trước? [→ §1 Graph Quality Metrics]

**Bạn sẽ thấy**

Bạn dựng xong graph, dành công tinh chỉnh câu trả lời mà điểm vẫn đứng yên. Hóa ra trong graph có 400 node không nối với ai cả, 12% tên thực thể bị trùng, và có cảnh `Person —[MANAGES]→ Document` vi phạm quy tắc. Dữ liệu vào sai thì code tốt cũng vô nghĩa.

**Vì sao**

Quy ước đã gọi cho trường hợp này là rác vào — rác ra. Đo phần trả lời trước khi biết graph có ổn thì đang tối ưu sai chỗ, và bạn không có chỉ số nào để biết mình đã tiến bộ bao nhiêu.

**Làm gì**

1. Đo chín thước sức khoẻ: độ phủ node và cạnh, tỉ lệ trùng lặp, độ liên thông, mật độ, số node trung bình, node cô lập, tỉ lệ cạnh vi phạm, độ tươi mới theo thời gian.
2. So với ngưỡng tham khảo: phủ node > 80%, phủ cạnh > 70%, trùng lặp < 5%, liên thông > 90%, trung bình 3–10 quan hệ mỗi node, cạnh vi phạm = 0%, tươi mới > 95%.
3. Khi kiểm tra phủ, đừng so chuỗi ký tự: "Alice" và "Alice Nguyen" phải được coi là có thể cùng một người, nếu không bạn sẽ tưởng mình thiếu dữ liệu.
4. Chạy phép so sánh độ liên thông trên đồ thị hướng bằng cách coi cạnh là không chiều.

```python
metrics = evaluate_graph_quality(G_labeled)
# {'nodes':34,'edges':78,'density':0.139,'avg_degree':4.59,
#  'connectivity':1.0,'isolated_rate':0.0}
evaluate_coverage(["Alice","Bob","Phoenix","Alice Nguyen"],
                  ["Alice","Bob","Phoenix","Atlas"])
# precision 0.75, recall 0.75, missed:['atlas'], hallucinated:['alice nguyen']
```

**Kiểm tra**

Dựng hai graph: một đồng bộ và đầy đủ, một nhiều node cô lập và trùng tên — chạy cùng bộ chỉ số thì phải ra hai bộ số khác rõ rệt. Sửa lỗi node cô lập thì tỉ lệ node cô lập phải giảm, tỉ lệ liên thông phải tăng.

---

## Q3. Bot nói "Phoenix 700 triệu" trong khi graph ghi 500 triệu — tự động phát hiện bằng gì? [→ §3.1 Faithfulness]

**Bạn sẽ thấy**

Câu trả lời có ba mệnh đề: ngân sách 700 triệu, Trần Thị B duyệt, team AI 15 người. Cả ba đều sai, mà mỗi lần bạn phải tự đọc lại đối chiếu. Ở hàng nghìn câu hỏi thì cách này không làm nổi.

**Vì sao**

Có hai nhóm lỗi riêng biệt: graph bị trích sai quan hệ, và phần tóm tắt do mô hình ngôn ngữ sinh ra bịa chi tiết. Gộp chung thành một điểm "trung thành" sẽ giấu mất nguồn lỗi.

**Làm gì**

1. Tách câu trả lời thành các **mệnh đề nhỏ** (claims).
2. Cho một mô hình ngôn ngữ chấm từng mệnh đề có nằm trong ngữ cảnh lấy từ graph không, trả về JSON gồm danh sách claims, cờ `supported` và điểm trung thành.
3. Tỉ lệ bịa = 1 − điểm trung thành. Yêu cầu mô hình trả về đúng định dạng JSON.
4. Kiểm tra thêm phần trích dẫn: mỗi đường dẫn nêu trong câu trả lời có thật trong graph không.

```python
resp = requests.post("http://localhost:11434/api/generate",
    json={"model":"gemma3:12b","prompt":prompt,"format":"json"})
result["hallucination_rate"] = 1.0 - result.get("faithfulness", 0)
# claims: [{"claim":"Phoenix ngân sách 700 triệu","supported":false}, ...]
```

**Kiểm tra**

Chạy một câu trả lời đúng (điểm trung thành 1.0, tỉ lệ bịa 0.0) và một câu trả lời sai, phải cho hai kết quả đối xứng. Mọi phần trích dẫn phải kiểm tra được bằng cách dò từng cặp node liền kề trong graph.

---

## Q4. Điểm khớp đáp án lên tới 85% mà vẫn không dám tin hệ thống — thiếu chỉ số gì? [→ §5.4 Lỗ Hổng Đánh Giá]

**Bạn sẽ thấy**

Bảng điểm báo động đạt, sếp gật đầu, rồi ba tuần sau có người dùng phát hiện hệ thống trả lời đúng bằng may mắn: nó kéo sẵn ngữ cảnh sai lệch nhưng câu hỏi dễ đoán đúng. Bạn không có chỉ số nào bắt được tình huống này.

**Vì sao**

Hai chỉ số khớp đáp án (EM/F1) chỉ đo **kết quả cuối**. Ba chỗ hở phổ biến năm 2025–2026: không đo được phần bằng chứng đưa vào có đúng và đủ không; hệ thống nhiều bước có thể trôi hướng giữa chừng; và báo cáo gộp một chỉ số cho cả hai nguồn bịa.

**Làm gì**

1. Thêm **độ nhớ bằng chứng**: trong các đoạn và đường đi đưa vào, bao nhiêu phần trăm là thực sự cần để trả lời.
2. Thêm **độ liên quan ngữ cảnh**: có bao nhiêu đoạn thừa, đo bằng câu hỏi ngược "đoạn nào không giúp trả lời câu hỏi này?".
3. Theo dõi **trôi hướng** (retrieval drift) ở từng bước: bước sau còn bám câu hỏi gốc không, không chỉ nhìn bước đầu.
4. Tách báo cáo thành **ba nhóm**: hỏi một bước, hỏi nhiều bước, hỏi tổng hợp. Nghiên cứu 2025–2026 cho thấy GraphRAG thắng ở nhóm nhiều bước và tổng hợp nhưng **thua** ở nhóm một bước — gộp chung sẽ che mất điều đó.
5. Với lỗi bịa, báo riêng hai nguồn: bịa do trích sai quan hệ và bịa do tóm tắt.

**Kiểm tra**

Trên 5 câu hỏi global sensemaking, điểm phải cao hơn hẳn RAG thuần. Trên các câu hỏi một bước, hãy chủ động báo cáo điểm thấp hơn thay vì giấu đi — đó là sự thật, không phải lỗi.

---

## Q5. Mô hình dự đoán quan hệ thiếu thì lấy số "đúng 3 trong 10" — có dùng được không? [→ §4 KG Completion Metrics]

**Bạn sẽ thấy**

Bạn huấn luyện mô hình dự đoán quan hệ mới trong graph có 1.000 thực thể. Báo cáo kiểu "đúng 45%" nghe có vẻ tốt, nhưng người đọc không biết trong 10 thứ được xếp hạng đầu thì có bao nhiêu là đáp án thật — và đáp án thật thường nằm ở hạng nào.

**Vì sao**

Bài toán này không phải phân loại hai lớp (đúng/sai) nên không dùng độ chính xác thuần. Người dùng thật chỉ lấy vài kết quả đầu tiên, nên điều quan trọng là **thứ hạng** của đáp án đúng, không phải tổng số câu trả lời đúng.

**Làm gì**

1. Báo cáo tỉ lệ đáp án đúng nằm trong top 1, top 3, top 10 (Hits@K).
2. Báo cáo **thứ hạng nghịch đảo trung bình**: đúng ở hạng 1 được 1.0, hạng 5 được 0.2.
3. Báo cáo thứ hạng trung bình (MR) để thấy đáp án bị bỏ lỡ xa bao nhiêu, và AUC cho bài toán dự đoán cạnh.
4. Ngưỡng tham khảu: Hits@10 > 0.5, MRR > 0.3, MR < 100, AUC > 0.8.
5. Mẫu số liệu từ một lần chạy: Hits@1 = 0.15, Hits@10 = 0.45, MRR = 0.28, MR = 85.3 — đối chiếu đúng với kỳ vọng.

```python
sorted_indices = torch.argsort(scores)
rank = (sorted_indices == t_true).nonzero(as_tuple=True)[0].item() + 1
mrr += 1.0 / rank
# {'Hits@1':0.15,'Hits@10':0.45,'MRR':0.28,'MR':85.3,'num_test':100}
```

**Kiểm tra**

Chạy lại với các ngưỡng 1, 3, 10 và in ra cả ba chỉ số cùng lúc. Nếu Hits@1 thấp nhưng Hits@10 cao, thì hệ thống dùng để gợi ý ("xem 10 gợi ý đầu") vẫn ổn, còn dùng để chốt tự động thì chưa an toàn.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*