# ❓ FAQ — GNN (Mạng Nơ-Ron Trên Đồ Thị)

Câu hỏi nào khó hiểu thì đọc `README.md` phần được nêu trong ngoặc vuông.

---

## Q1. Tôi đã có rule suy luận ở module 06, có cần học GNN làm gì không? [→ Câu Chuyện Mở Đầu]

**Bạn sẽ thấy**

Bạn viết được khoảng 5 luật thì ổn. Nhưng graph thật có hàng trăm loại quan hệ: `MANAGES`, `WORKS_ON`, `REPORTS_TO`, `APPROVES`, `HAS_BUDGET`, `REVIEWS`... Mỗi loại một quy tắc, tổng cộng lại là một bộ luật không ai bảo trì nổi. Đối chiếu số liệu: GNN tăng **15–25% độ chính xác** so với mô hình chỉ dùng đặc trưng node; hoàn thành KG đạt MRR **0.35** (bộ đo trung bình nghịch đảo thứ hạng) so với TransE chỉ 0.29.

**Vì sao**

Luật viết tay chỉ học được quan hệ bạn đã nghĩ ra. GNN học từ cấu trúc sẵn có: hai người cùng làm một dự án thì vector đặc trưng của họ tự động gần nhau, không cần ai bảo.

**Làm gì**

1. Viết luật cho các quan hệ **hiển nhiên và ổn định** (bắc cầu quản lý, `WORKS_ON` suy ra giám sát) — những cái này giải thích được với người đọc.
2. Dùng GNN cho phần **nhiều quy tắc, mẫu nhiều**: dự đoán ai sẽ làm dự án tiếp, gợi ý quan hệ còn thiếu.
3. Nếu chỉ cần tìm quan hệ thiếu: dùng dự đoán cạnh (link prediction) — đo độ đúng bằng AUC, kết quả tham khảo từ Anthropic 2025 đạt **độ chính xác 72%** trên KG doanh nghiệp.
4. Nhớ đo cả phần trùng lặp: nếu node mới có embedding gần node cũ, đó là dấu hiệu nên gộp.

**Kiểm tra**

Trên cùng một graph, chạy GNN phân loại với chỉ 4 node có nhãn (kiểu học nửa giám sát) và so với một mô hình chỉ đọc đặc trưng node. Mô hình có đọc cạnh phải thắng; nếu không thắng thì graph chưa mang thông tin hữu ích hoặc số lớp quá sâu.

---

## Q2. Cho mô hình nhiều lớp hơn thì tự nhiên tệ đi — sao hai người không liên quan lại giống nhau? [→ §6.1 Over-Smoothing]

**Bạn sẽ thấy**

Ở 2 lớp mô hình dự đoán còn đúng. Thêm lớp thứ 3, thứ 4: mọi node bắt đầu nhận cùng một vector, phân loại "ai thuộc team nào" hỗn loạn. Biểu hiện đúng như bài kiểm tra mẫu: dùng 2 lớp GNN trên đồ thị Karate Club với 4 node có nhãn, thêm lớp nữa thì độ đúng **tụt xuống dưới mức đoán mù**.

**Vì sao**

Mỗi lớp GCN lấy trung bình có trọng số của chính mình và các bạn bè. Càng đào sâu, thông tin càng bị "pha loãng" đều. Giống trò chơi điện thoại hỏng: qua nhiều vòng, câu truyền đi xa bị biến thành một khối vô nghĩa. Đây gọi là **over-smoothing** (quá mượt).

**Làm gì**

1. Giữ lớp mỏng: thực tế GraphSAGE 2 lớp hiệu quả hơn mô hình 10 lớp — đừng chôn sâu.
2. Thêm kết nối tắt (residual): cho phép lớp sau bỏ qua lớp trước, giữ lại thông tin gốc.
3. Chuẩn hoá đặc trưng sau mỗi lớp để các vector không co lại về điểm giữa.
4. Nối thêm cạnh ngắn giữa các node ở xa (graph rewiring) để thông tin không phải đi qua nút thắt cổ chai.
5. Nếu thật sự cần nhìn xa, chuyển sang Graph Transformer: node "nhìn thẳng" mọi node khác, nhưng đổi lại bộ nhớ tăng theo bình phương số node.

**Kiểm tra**

Vẽ độ đúng theo số lớp 1→10. Nếu đường cong đi lên rồi đi xuống dưới điểm ban đầu, bạn đang dính over-smoothing. Thêm residual và chạy lại, đường cong phải phẳng hoặc tốt hơn.

---

## Q3. Thêm một người mới vào KG thì mô hình cũ có dùng được không? [→ §3 GraphSAGE & GAT]

**Bạn sẽ thấy**

Bạn đã huấn luyện xong, thử vài người mới vào thì không sao. Rồi ngày kia thêm một nhóm 50 người, kết quả tự nhiên tệ đi hoặc phải huấn luyện lại từ đầu. Nguyên nhân nằm ở chỗ GCN cần **toàn bộ ma trận kề** trước khi tính, tức là kiểu học chỉ dùng được với node đã có sẵn lúc huấn luyện.

**Vì sao**

Ba mô hình khác nhau ở cách lấy thông tin bạn bè:

| Mô hình | Có học trước node mới? | Chi phí | Hợp nhất khi |
|---|---|---|---|
| GCN | không | O(N²) | graph nhỏ, chỉ huấn luyện một số node |
| GraphSAGE | có | O(E) | graph lớn, node mới xuất hiện liên tục |
| GAT | có | O(E × số đầu) | quan hệ không đồng đều, cần xếp hạng |

**Làm gì**

1. Dùng GraphSAGE: nó học một **công thức gộp bạn bè** (trung bình, LSTM, hoặc lấy giá trị lớn nhất sau một lớp biến đổi), nên node mới chỉ cần chạy công thức đó với bạn bè là xong.
2. Dùng GAT khi quan hệ không đồng đều: mô hình tự học mỗi người đóng góp bao nhiêu phần trăm qua cơ chế chú ý (attention), rồi chuẩn hoá tổng thành 1.
3. Dùng nhiều "góc nhìn" (multi-head) ở GAT để giảm nhiễu, rồi chỉ nối một đầu ra khi vào tầng cuối.
4. Trong đoạn mã mẫu: lớp đầu đặt `heads=4` nên đầu ra dài gấp 4, lớp sau đưa về `heads=1, concat=False`.

**Kiểm tra**

Huấn luyện trên 80% node, giấu 20%. Thêm node mới chưa từng xuất hiện rồi suy ra vector — GraphSAGE và GAT cho kết quả dùng được ngay, GCN thì phải chạy lại toàn bộ.

---

## Q4. Nhét KG thật vào GNN thì sao — graph của tôi có người, dự án, ngân sách lẫn lộn? [→ §5 & §7 Heterogeneous GNN]

**Bạn sẽ thấy**

Bạn có `Person —WORKS_ON→ Project`, `Person —REPORTS_TO→ Person`, `Project —HAS_BUDGET→ Number`. Nhét tất cả vào mô hình GCN thường, kết quả bị trôi: quan hệ "quản lý" và quan hệ "được tài trợ" bị xử lý y hệt nhau, mất hết ý nghĩa. R-GCN chạy trên cùng graph đó lại ra kết quả khác hẳn.

**Vì sao**

KG thật luôn **không đồng nhất** (heterogeneous): nhiều loại node, nhiều loại cạnh. GCN và GraphSAGE giả định mọi node, mọi cạnh cùng một loại. Nếu gộp phẳng, các giá trị trong cột `edge_type` bị ném đi và mô hình không còn biết `MANAGES` khác `HAS_BUDGET` ở chỗ nào.

**Làm gì**

1. Không gộp phẳng — chuyển sang R-GCN: mỗi loại quan hệ một bộ trọng số riêng `W_r`, như "mỗi loại quan hệ là một lăng kính khác nhau".
2. Truyền thêm cột `edge_type` cho mỗi cạnh, ví dụ `[0, 1, 0, 1]` với 0 là `MANAGES`, 1 là `WORKS_ON`.
3. Nếu cần tầng ý nghĩa cao hơn: HAN tổng hợp theo từng "con đường loại" (ví dụ `Person–WORKS_ON–Project–HAS_BUDGET–Budget`) rồi dùng chú ý để gộp; HGT là biến thể Transformer mạnh nhất.
4. Sau khi học, dùng scoring function (TransE, DistMult, ComplEx, RotatE) để chấm điểm bộ ba thiếu.

```python
model = RGCN(8, 16, 8, num_relations=2)
out = model(x, edge_index, edge_type)   # out shape: (4, 8)
```

**Kiểm tra**

Kiểm tra ngẫu nhiên 100 quan hệ đã biết với mô hình phẳng và mô hình R-GCN: độ đúng phải tăng khi dùng bộ trọng số riêng cho từng loại quan hệ.

---

## Q5. Đoán quan hệ mới thì dùng "cặp không tồn tại" ra sao — huấn luyện có bị rò dữ liệu không? [→ §4.1 Link Prediction]

**Bạn sẽ thấy**

Bạn giấu 20% cạnh đi để kiểm tra mô hình dự đoán được không. Kết quả điểm ổn. Nhưng ở bài kiểm tra nghiêm ngặt hơn, cặp bạn giấu vẫn xuất hiện trong dữ liệu huấn luyện dưới dạng đường vòng, nên điểm tốt hơn thực tế rất nhiều.

**Vì sao**

Dự đoán cạnh học theo kiểu "cặp có thật" và "cặp không có thật". Nếu không tách cặp theo **cạnh** mà tách theo node, thì thông tin của cạnh bị giấu vẫn chảy vào mô hình qua các node lân cận. Số cặp âm cũng quyết định chất lượng: tỉ lệ 1:1 khác 1:5 cho kết quả khác nhau rõ.

**Làm gì**

1. Tách **cạnh** trước khi tạo tập dữ liệu, dùng tiện ích tách cạnh sẵn có thay vì tự ngẫu nhiên node.
2. Lấy mẫu cặp âm bằng hàm lấy mẫu âm, ví dụ 4 cặp âm cho một bộ cạnh nhỏ.
3. Dùng hàm mất mát nhị phân: cặp thật về gần 1, cặp âm về gần 0, tổng hai phần lại.
4. Dùng tích của hai vector để chấm điểm cặp (điểm cao = khả năng có quan hệ).

```python
neg = negative_sampling(edge_index, num_nodes=4, num_neg_samples=4)
pos_loss = F.binary_cross_entropy_with_logits(pos_score, torch.ones_like(pos_score))
loss = pos_loss + neg_loss
```

**Kiểm tra**

Báo cáo AUC trên tập cạnh đã giấu thật sự. Thử hai tỉ lệ lấy mẫu 1:1 và 1:5 — nếu điểm nhảy quá nhiều giữa hai lần thì tỉ lệ đang chi phối kết quả, cần cân bằng lại.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*