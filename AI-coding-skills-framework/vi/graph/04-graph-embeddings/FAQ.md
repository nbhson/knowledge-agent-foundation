# ❓ FAQ — Vector hoá đồ thị (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc.

---

## Q1. Thêm một node mới thì phải huấn luyện lại cả graph — có cách nào không? [→ §2 và §3 Node2Vec so với GNN]

**Bạn sẽ thấy**

Bạn đã huấn luyện xong cách vector hoá đồ thị cho 10.000 node. Ngày mai có thêm 300 nhân viên mới và bạn muốn hỏi "ai giống nhân viên mới này về vai trò?". Kết quả: hàm huấn luyện chỉ nhớ vector của 10.000 node cũ, với người mới nó không có vector nào cả. Hệ thống buộc phải chạy lại toàn bộ.

**Vì sao**

Node2Vec và DeepWalk gán **mỗi node một vector riêng**, đúng như một từ trong từ điển. Thêm một từ mới vào từ điển thì phải dựng lại từ điển — đây gọi là cách tiếp cận *chuyển tiếp* (transductive). GraphSAGE thì học một **hàm gộp**: vector của một node là hàm của vector nó và vector bạn bè trực tiếp. Bất kỳ ai cũng mô tả được bằng cách "trung bình của bạn bè" — nên người mới chỉ cần chạy đúng hàm đó là có vector, không cần huấn luyện lại.

**Làm gì**

1. Nếu graph nhỏ và đóng (hiếm khi thêm node), Node2Vec vẫn ổn: không cần GPU, không cần nhãn.
2. Nếu node tăng liên tục, dùng **GraphSAGE**. Thêm node mới = chạy hàm cho node đó, xong.
3. GraphSAGE tận dụng được **thuộc tính** của node (chức vụ, phòng ban), điều Node2Vec không làm được — nó chỉ nhìn cấu trúc.
4. Nếu quan hệ không đồng đều (quan hệ quan trọng khác nhau), dùng **GAT**: thay vì lấy trung bình bạn bè, mô hình tự học xem ai đáng tin. Ví dụ trong sơ đồ tổ chức: đồng nghiệp báo cáo trực tiếp góp 83%, người quen xã giao góp 17%.
5. Chọn mức "tầm nhìn" bằng số lớp: 3 lớp = biết thông tin cách 3 bước. Thừa dẫn tới mất thông tin và chậm.

| | Node2Vec | GraphSAGE | GAT |
|---|---|---|---|
| Thêm node mới | Huấn luyện lại | Chạy hàm | Chạy hàm |
| Cần thuộc tính node | Không | Có | Có |
| Cách gộp bạn bè | Không rõ | Trung bình | Tự học trọng số |

```python
model = GraphSAGE(in_channels=16, hidden_channels=32, out_channels=8)
emb_cu = model(x_cu, edge_index_cu)      # node mới chưa từng huấn luyện
emb_cu = emb_cu / emb_cu.norm(dim=1, keepdim=True)   # chuẩn hoá để so cosin
```

**Kiểm tra**

Che khoảng 20% cạnh của graph, dự đoán lại xem có đoán đúng không (bài kiểm tra *link prediction*). Chạy cho cả Node2Vec lẫn GraphSAGE, so sánh độ chính xác và thời gian. Nếu đồ thị của bạn thay đổi liên tục, ưu tiên phương án không cần huấn luyện lại.

---

## Q2. Tìm "người giống Alice về vai trò" — chỉnh tham số thế nào cho ra đúng? [→ §2.2 Node2Vec có tham số p và q]

**Bạn sẽ thấy**

Bạn muốn: "tìm người giống Alice về vai trò, kể cả họ ở team khác". Chạy Node2Vec với tham số mặc định thì ra toàn những người cùng team với Alice — gần như không ai mới. Đổi tham số quá tay theo hướng ngược lại thì ra những người có vai trò khác hẳn.

**Vì sao**

Node2Vec không đi bộ hoàn toàn ngẫu nhiên. Hai tham số điều khiển *kiểu* đi:
- `p` (quay lại): nhỏ (~0.5) thì hay quay lại node vừa rời → khám phá khu vực chặt. Lớn (~2.0) thì ít quay lại → đi xa.
- `q` (đi ra hay đi gần): nhỏ (~0.5) thì dễ đi xa, giống quét chiều sâu → tìm người **cùng vai trò** ở team khác. Lớn (~2.0) thì dễ đi gần, giống quét theo bề rộng → tìm người **cùng team**.

**Làm gì**

1. Câu hỏi "cùng vai trò, khác team" → đi theo hướng quét chiều sâu: đặt `q < 1` (thử 0.5). Câu hỏi "cùng team" → đặt `q > 1` (thử 2.0).
2. Giữ `p` khoảng 1.0 khi bạn chưa rõ nên bám hay nên đi rộng; chỉnh `p` sau khi đã có `q` ổn.
3. Tăng số lần đi bộ (mặc định `num_walks=10`, mỗi lần dài 20 bước) khi graph thưa — ít dữ liệu hơn thì vector kém ổn định.
4. Đừng kỳ vọng dùng được thuộc tính: Node2Vec chỉ nhìn cấu trúc, nên "giống Alice" nghĩa là *vị trí trong đồ thị* giống, không phải *mô tả chức vụ* giống. Muốn dùng cả thuộc tính thì chuyển sang GraphSAGE.
5. Kiểm tra chất lượng bằng cách nhìn kết quả theo cụm: vẽ bằng t-SNE và xem các node cùng team có nằm cạnh nhau không.

```python
walks = [get_random_walk(G, n, walk_length=20) for n in G for _ in range(10)]
model = Word2Vec(walks, vector_size=64, window=5, sg=1, min_count=0, epochs=5)
sim = cosine(model.wv["node_0"], model.wv["node_7"])   # càng cao càng giống
```

**Kiểm tra**

Chạy ba bộ tham số: mặc định, `q=0.5` (xa), `q=2.0` (gần). Với mỗi bộ, lấy 10 node giống Alice nhất và tự đánh giá: có đúng là cùng vai trò / cùng team không. Bộ nào cho kết quả đúng với câu hỏi của bạn thì giữ.

---

## Q3. Quan hệ trong graph của tôi có thời gian — dùng TransE có bị sai không? [→ §4 KG Embeddings]

**Bạn sẽ thấy**

Bạn dùng TransE (mô hình vector hoá quan hệ) và nó dự đoán đúng hầu hết quan hệ. Nhưng với một trường hợp nó sai hoàn toàn: `(Nguyễn Văn A, WORKS_ON, Dự án Phoenix)`. Kết quả là mô hình vẫn khẳng định quan hệ này đúng, dù nhân viên đó đã chuyển sang dự án khác từ năm 2025. Với quan hệ đối xứng như "kết hôn", độ chính xác cũng kém hơn mong đợi.

**Vì sao**

TransE học theo nguyên tắc **dịch chuyển**: `vector(Alice) + vector(WORKS_ON) ≈ vector(Phoenix)`. Nó coi mọi quan hệ là bất biến theo thời gian, nên không có chỗ nào để ghi "từ năm 2025 thì sai". Ngoài ra cơ chế cộng không diễn tả được quan hệ đối xứng: từ `A + r = B` không suy ra được `B + r = A`. RotatE coi quan hệ là một **góc quay**, xoay 180 độ thì ra quan hệ ngược — nên xử lý tốt hơn những quan hệ kiểu "đã kết hôn với".

**Làm gì**

1. Nếu quan hệ không đổi theo thời gian: giữ TransE, đơn giản và hiệu quả.
2. Nếu có quan hệ đối xứng và quan hệ nối tiếp ("thuộc về" A→B và B→C thì A→C): dùng **RotatE**.
3. Nếu graph có cột thời gian và câu hỏi phụ thuộc thời điểm (nhân sự, tin tức, lịch sử) → dùng bản **có thời gian** (TKGE): triplet thành `(h, r, t, thời điểm)`, với ba hướng là thêm tham số thời gian vào công thức dịch chuyển, truyền tin theo từng thời điểm, hoặc dự đoán xu hướng thay đổi.
4. Đánh giá cả hai mô hình trên dữ liệu của bạn: che một phần quan hệ đã biết, hỏi mô hình dự đoán, đo tỉ lệ đúng.
5. Nhóm mô hình mới (Graph Transformer) nhìn được toàn đồ thị nhưng tốn bộ nhớ theo bậc hai số node; hàng triệu node vẫn nên dùng mô hình truyền tin theo hàng xóm.

```python
model = TransE(num_entities=1000, num_relations=10, dim=100)
score = torch.norm(h_e + r_e - t_e, p=1, dim=1)   # thấp = đúng, cao = sai
top = torch.topk(model.predict_tail(alice_id, works_on_id, 1000), k=5, largest=False)
# (Alice, WORKS_ON, ?) → 5 entity có điểm thấp nhất
```

**Kiểm tra**

Với `(Nguyễn Văn A, WORKS_ON, ?)`, xem 5 kết quả đầu có chứa cả Phoenix lẫn dự án mới. Thử ngược lại cặp "đã kết hôn với" và xem dự đoán có đối xứng hay không. Nếu mô hình hiện tại không đạt, hãy đổi sang RotatE rồi đo lại cùng bộ câu hỏi.

---

## Q4. Có vector của văn bản lẫn vector của đồ thị — trộn lại bằng cách nào, tỉ lệ bao nhiêu? [→ §5 Hybrid Search]

**Bạn sẽ thấy**

Bạn tạo hai bộ vector: một bộ từ phần mô tả chữ (text embedding), một bộ từ vị trí trong đồ thị (graph embedding). Chạy riêng bộ text thì ra 10 kết quả gần như trùng nhau — toàn những đoạn văn bản viết giống từ. Chạy riêng bộ graph thì ra những node đúng về vai trò nhưng bỏ sót tài liệu có từ khoá cần tìm.

**Vì sao**

Hai bộ vector bắt được hai thứ khác nhau: text bắt "nói gì", graph bắt "đứng ở đâu". Dùng riêng bộ nào cũng mất một nửa thông tin. Cần **pha trộn** (fusion) thành một điểm số duy nhất.

**Làm gì**

1. Cách đơn giản nhất: **pha theo trọng số** — điểm cuối = `alpha × điểm_text + (1 − alpha) × điểm_graph`. Đặt `alpha` theo *loại câu hỏi*, không đặt một con số cho mọi thứ.
2. Tham khảo tỉ lệ theo từng loại câu hỏi:

| Loại câu hỏi | Nên đặt alpha |
|---|---|
| Tìm một đoạn văn cụ thể | 0.8 (thiên về chữ) |
| Nối nhiều thực thể qua nhiều bước | 0.3 (thiên về đồ thị) |
| Hỏi tổng quan, so sánh xu hướng | 0.2 (cực thiên về đồ thị) |
| Cân bằng mặc định | 0.5 – 0.6 |

3. Cách thứ hai: **RRF** (Reciprocal Rank Fusion) — cộng `1 / (60 + thứ hạng)` cho mỗi danh sách kết quả. Ưu điểm: **không cần chuẩn hoá điểm số** giữa các bộ, vì thứ hạng luôn cùng thang.
4. Chọn RRF khi bạn có 3 nguồn trở lên (vector + duyệt đồ thị + tìm toàn văn) và không muốn tinh chỉnh trọng số.
5. Nhớ lấy gấp đôi số kết quả từ mỗi bộ rồi mới pha, vì bộ nào bị lọc sớm thì mất luôn ứng viên.

```python
# RRF — không cần chuẩn hoá điểm, k = 60
fused = {}
for lst in [vector_rank, graph_rank, fulltext_rank]:
    for rank, item in enumerate(lst, start=1):
        fused[item] = fused.get(item, 0.0) + 1.0 / (60 + rank)
final = sorted(fused.items(), key=lambda x: -x[1])[:10]
```

**Kiểm tra**

Làm Lab 3: tạo 50 câu hỏi, 25 câu tìm đoạn cụ thể và 25 câu nối nhiều bước. Chạy ba chế độ: chỉ text (`alpha=1.0`), chỉ đồ thị (`alpha=0.0`), pha trộn (`alpha=0.6`), đo độ chính xác trong 5 kết quả đầu cho từng nhóm. Nếu chế độ pha trộn không thắng ở nhóm nào, hãy dời `alpha` về phía nhóm đó.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*