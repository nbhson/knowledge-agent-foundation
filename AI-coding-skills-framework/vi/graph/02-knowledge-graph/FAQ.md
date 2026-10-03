# ❓ FAQ — Xây dựng Knowledge Graph (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc `../README.md` phần trong ngoặc.

---

## Q1. 3 người đọc 1.000 tài liệu, ra 3 node "Alice" khác nhau — gộp bằng cách nào, ngưỡng bao nhiêu? [→ §4 Gộp Trùng Lặp]

**Bạn sẽ thấy**

Intern A ghi `(Phoenix, managed_by, Alice Nguyen)`. Intern B ghi `(Alice N., approves, Contract C-2024)`. Intern C ghi `(Alice Nguyễn, reports_to, Bob)`. Bạn mở graph ra và thấy **ba node "Alice" không nối với nhau**. Hỏi "CTO là ai?" thì câu trả lời chia làm ba, mỗi nhánh một nửa — không nối được với nhau chính vì tên viết khác nhau. Tương tự với "Phoenix", "Dự án Phoenix", "Phoenix Project".

**Vì sao**

Mỗi người trích từ một đoạn văn bản khác nhau, không ai thấy người kia viết gì. Không có bước gộp trùng lặp (deduplication), cùng một thực thể sẽ thành nhiều node rời rạc. Đây không phải lỗi trích xuất — đây là việc bắt buộc phải làm.

**Làm gì**

1. Bắt đầu bằng **chuỗy 3 mức**: chuẩn hoá chữ (bỏ dấu, lowercase) → so khớp mờ (Levenshtein, TF-IDF) → **vector hoá** (embedding) rồi đo độ tương đồng bằng cosin. Cách embedding bắt được cả "CTO Alice" với "giám đốc công nghệ Alice" — hai cụm từ khác nhau nhưng cùng người.
2. Chỉ so sánh **cùng loại thực thể**. "Alice" loại Person không được so với "Phoenix" loại Project.
3. Đặt ngưỡng. Mặc định **0.85**. Lab 3 trong README gợi ý thử 0.80 / 0.85 / 0.90: thấp quá thì gộp nhầm hai người thật sự khác nhau (Alice phòng nhân sự ≠ Alice CTO), cao quá thì sót trùng lặp.
4. Giữ node đầu tiên làm node chuẩn (canonical), ghi lại bảng ánh xạ tên cũ → tên chuẩn.
5. **Sửa cả quan hệ theo bảng ánh xạ** trước khi ghi. Sau khi gộp, một số quan hệ tự thành quan hệ với chính nó — loại bỏ.
6. Luôn để đường lui: cho phép tách lại (split) nếu phát hiện gộp nhầm.

```python
def dedup(entities, threshold=0.85):
    canon, mapping = [], {}
    for e in entities:                      # e = {"name", "type"}
        hit = next((c for c in canon if c["type"] == e["type"]
                    and cosine_sim(embed(e["name"]), embed(c["name"])) >= threshold), None)
        mapping[e["name"]] = hit["name"] if hit else e["name"]
        if not hit: canon.append(e)
    return canon, mapping
```

**Kiểm tra**

In ra dòng `Dedup: 'Alice Nguyen' -> 'Nguyễn Văn A' (sim=0.91)` cho mỗi lần gộp. Sau để ý: số node Person có tên gần giống nhau trong graph sau khi gộp phải bằng số người thật. Đo lại câu "CTO là ai?" — phải ra một người, không phải ba.

---

## Q2. Gọi LLM trích một lần thì bỏ sót entity ở cuối văn bản — làm sao không sót? [→ §2 Trích Xuất Thực Thể]

**Bạn sẽ thấy**

Văn bản hợp đồng dài 4 trang. Bạn gọi LLM một lần, ra 6 thực thể — nhưng đọc tay thấy có 9, và 3 cái bị bỏ đều nằm ở nửa sau trang 3. Câu hỏi "ai ký, ai phê duyệt, dự án nào liên quan" thì LLM trả lời thiếu.

**Vì sao**

Lần gọi một (single-pass) có độ bao phủ cao nhưng độ chính xác thấp, và nó có xu hướng "quên" phần cuối văn bản dài. Microsoft GraphRAG (2024) đo được vòng lặp trích nhiều lần (gleaning loop) tăng **25% độ bao phủ** so với một lần.

**Làm gì**

1. Chia tài liệu thành đoạn nhỏ **trước** khi trích: `chunk_size=1000`, `overlap=100`. Đoạn chồng lấn để không mất thực thể nằm đúng ranh giới.
2. Chạy vòng lặp: vòng 1 trích tự do. Vòng 2 gửi lại văn bản **kèm danh sách đã trích**, và yêu cầu "còn entity nào bỏ sót không?".
3. Chạy tối đa 2 vòng hợp lý. **Dừng sớm** nếu một vòng không ra entity mới nào (biến `added == 0`) — tránh đốt token vô ích.
4. Chặn trùng ngay trong vòng lặp bằng khoá tên đã thấy (chuẩn hoá lowercase + bỏ khoảng trắng thừa).
5. Chạy qua Ollama ở `http://localhost:11434`, yêu cầu trả về đúng định dạng JSON để không phải tự cắt chuỗi.

```python
def extract_entities(text, model="gemma3:12b", max_gleanings=2):
    seen, all_ents = set(), []
    for r in range(max_gleanings + 1):
        p = f"Trích entities (Person, Project, Document, Organization).\n{text}\nĐã trích: {sorted(seen)}\nTrả JSON list."
        added = [e for e in llm_json(p, model) if e["name"].lower().strip() not in seen]  # format=json
        seen |= {e["name"].lower().strip() for e in added}; all_ents += added
        if added == 0: break                        # hết ý, dừng sớm
    return all_ents
```

**Kiểm tra**

Chạy Lab 2: trích cùng một văn bản với `gleaning=0` rồi `gleaning=2`, so sánh số thực thể tìm được và đối chiếu thủ công xem cái nào bị bỏ sót. Nếu vòng 3 không tăng thêm gì thì dừng ở 2 vòng, đừng tăng lên.

---

## Q3. LLM trích ra cả quan hệ bịa, sai kiểu — có giữ vào graph không, lọc bằng gì? [→ §1 và §3 Quan Hệ]

**Bạn sẽ thấy**

Trong graph của bạn xuất hiện `(Project Phoenix, MANAGES, Person Alice)` — quan hệ ngược chiều so với thực tế. Ngoài ra còn một cạnh `APPROVES` với `confidence = 0.31`, tức là LLM tự nói "chỉ 31% chắc thôi", nhưng bạn vẫn lưu. Ba tháng sau, câu hỏi "hợp đồng nào Alice đã duyệt?" trả về kết quả sai.

**Vì sao**

Không có **ontology** (bản thiết kế: loại thực thể nào tồn tại, quan hệ nào hợp lệ), LLM trích tự do sẽ tạo ra một mớ rối không kiểm soát — có 5 loại gọi cùng là "team", 5 reviewer hiểu cùng một khái niệm. Stanford KB Construction (2024) đo được cách định schema trước giảm **60% quan hệ sai** so với trích tự do.

**Làm gì**

1. Viết `ontology.yaml` khai báo trước: `node_types` (Person, Project, Document) và `edge_types` kèm `from` / `to` (MANAGES chỉ Person → Person, WORKS_ON chỉ Person → Project).
2. Thêm ràng buộc (constraint) vào đúng chỗ: dự án có `budget > 0`; quan hệ `APPROVES` chỉ hợp lệ khi `confidence >= 0.7`; cấm `MANAGES` trỏ vào chính mình.
3. **Kiểm tra mọi quan hệ trước khi ghi.** Sai hướng thì báo rõ: `Edge MANAGES requires Person -> Person, got Project -> Person`.
4. Lọc theo `confidence` với ngưỡng **0.7** và **in ra số lượng trước/sau** để bạn thấy mình đang vứt bao nhiêu.
5. Quan hệ lạ không xoá hẳn — cho vào nhóm `pending` để người duyệt định kỳ, rồi mới quyết định có bổ sung vào ontology không.

| Kiểu trích | Độ đúng | Độ đủ | Hợp khi nào |
|---|---|---|---|
| Luật cố định (mã hợp đồng) | Rất cao | Thấp | Mã HĐ, ngày tháng |
| Mô hình nhận dạng tên riêng | Cao | Vừa | Người, tổ chức, địa điểm |
| LLM một vòng | Vừa | Rất cao | Mọi loại thực thể |
| LLM + nhiều vòng | Cao | Rất cao | GraphRAG cần phủ kín |

**Kiểm tra**

Chạy pipeline đầu-cuối: sau bước gộp trùng lặp mới chạy kiểm tra ontology, và in ra ba dòng thống kê: `Raw: N entities`, `After dedup`, `After validation`. Nếu số quan hệ giảm hơn 30% thì hãy đọc lại 10 cạnh bị loại xem đó là rác thật hay quan hệ đúng.

---

## Q4. Graph đã có 5.000 node, có thêm 1 tài liệu mới thì có phải xây lại toàn bộ không? [→ §5 Cập Nhật Tăng Dần]

**Bạn sẽ thấy**

Mỗi sáng có một tài liệu mới về nhân sự. Nếu mỗi lần bạn xử lý lại toàn bộ kho, vừa chậm vừa tốn tiền gọi LLM — và tệ hơn là các quan hệ cũ đã đúng lại bị ghi đè bằng kết quả trích mới có thể kém hơn. Câu hỏi mà ai cũng quên: xoá một node cũng cần xây lại không?

**Vì sao**

Knowledge graph production thay đổi hằng ngày. Cách duy nhất để không phải xây lại là mọi thao tác ghi phải **tăng dần** (incremental) và **chạy lại được** — nghĩa là chạy hai lần cho kết quả giống nhau.

**Làm gì**

1. Ghi node bằng `MERGE` chứ không dùng `CREATE`. `MERGE` nghĩa là "có rồi thì cập nhật, chưa có thì tạo".
2. Nối quan hệ cũng bằng `MERGE`, kèm `confidence` và `updated_at`.
3. Xoá thì dùng **xoá mềm** (soft delete): đặt `deleted = true` và `deleted_at`, không xoá hẳn — giữ được lịch sử để trả lời câu hỏi về quá khứ.
4. Với mỗi tài liệu mới, chạy đúng chuỗi: trích thực thể → trích quan hệ → gộp trùng lặp → sửa quan hệ theo bảng ánh xạ → ghi.
5. Luôn in dòng kết quả để đối chiếu: `Ingested doc #42: 18 entities, 31 relations`.

```python
def upsert_entity(self, e):
    self.graph.run("MERGE (n:Person {name:$name}) "
                   "SET n.role=$role, n.updated_at=datetime()", e)

def soft_delete(self, name):
    self.graph.run("MATCH (n {name:$name}) SET n.deleted=true, "
                   "n.deleted_at=datetime()", {"name": name})
# MERGE chạy lại ba lần vẫn cho đúng một node — đây là điểm mấu chốt
```

**Kiểm tra**

Nạp lại **cùng một tài liệu hai lần** rồi đếm số node và số cạnh. Hai lần phải ra kết quả giống hệt nhau; nếu tăng lên thì đang dùng `CREATE` ở đâu đó. Sau đó thử xoá mềm một node rồi truy vấn lại — node vẫn còn nhưng đã bị đánh dấu, và lịch sử quan hệ cũ không bị cắt.

---

## Q5. Nên chạy pipeline cố định hay để LLM-agent tự xây graph? [→ §7 Agentic Construction]

**Bạn sẽ thấy**

Pipeline cố định chạy xong thì bạn đọc kết quả và thấy một mớ quan hệ sai chỗ. Sửa tay thì lâu, chạy lại pipeline lại mất công. Còn nếu để LLM-agent tự quyết: nó đọc đoạn văn, viết câu lệnh `MERGE`, xem kết quả trả về, nhận ra sai và tự sửa bằng `UPDATE`/`DELETE`.

**Vì sao**

Hai cách khác nhau về bản chất. Pipeline cố định đi **một chiều**: văn bản → trích → gộp → ghi. Hỏng giữa chừng thì phải chạy lại từ đầu, và không lưu bằng chứng đâu là nguồn. Agent đi **vòng lặp**: đọc → ghi → kiểm tra → sửa, và gắn mỗi bộ ba quan hệ với `source_chunk` — tức là biết nó lấy từ đoạn văn bản nào, để sau này bấm ngược lại được.

**Làm gì**

1. Ghi kèm nguồn ngay từ lúc tạo: `MERGE (s {name:$subj}) ON CREATE SET s.source_chunk=$chunk`, tương tự cho cạnh. Không có nguồn thì không trả lời được câu "bằng chứng nào nói vậy?".
2. Hết mỗi đoạn văn bản, cho agent tự hỏi lại: các quan hệ vừa ghi có đúng và đủ không. Sai thì nó tự quyết định sửa hay xoá.
3. Dùng `MERGE` chứ không `CREATE`, để lần chạy sau không sinh bản sao.
4. Cân nhắc chi phí: agentic tốn **2–3 lần** số lần gọi LLM so với batch một vòng. Các hệ thống điển hình là KnoBuilder, KG-Agent, RAGA.
5. Chọn theo quy mô: dữ liệu lớn, chạy theo lô → pipeline. Đồ thị nhỏ, cần chính xác cao, muốn tự điều chỉnh schema → agent.

| Tiêu chí | Pipeline cố định | Agent |
|---|---|---|
| Luồng | Một chiều, gom một lượt | Đọc → ghi → kiểm tra → sửa |
| Khi sai | Chạy lại pipeline | Tự quyết định sửa/xoá |
| Bằng chứng | Không lưu | Gắn `source_chunk` từng quan hệ |

**Kiểm tra**

Lấy 20 tài liệu thật, chạy cả hai cách, rồi đối chiếu 50 quan hệ ngẫu nhiên: bao nhiêu cái đúng, bao nhiêu cái bịa, và chi phí LLM mỗi cách. Quyết định dựa trên con số đó chứ không dựa vào cảm tính.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: README.md.*