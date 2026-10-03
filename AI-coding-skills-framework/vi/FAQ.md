# ❓ FAQ — AI Coding Skills Framework (chuyện thật, dễ hiểu)

Câu hỏi nào khó hiểu thì đọc phần trong file tên trong ngoặc.

---

## AI_AGENT_FRAMEWORK.md

### Q1. Framework này dùng để làm gì — khác gì so với dùng ChatGPT bình thường? [→ § 🧠 Hiểu Framework Này]

**Bạn sẽ thấy**

Bạn clone repo, mở `AI_AGENT_FRAMEWORK.md` (1.195 dòng), thấy ba thư mục con: `harness/` (15 module), `graph/` (9 module), `loop/` (7 phần). Ngay dòng đầu của tài liệu đã nói thẳng: đây là hướng dẫn để **xây** agent, không phải cách **dùng** AI thông thường. Bảng "Phân biệt rộ: Phần nào cần model?" cũng gây bất ngờ: `BM25 Search` ❌, `Prompt Building` ❌, `Workflow` ❌, `CI/CD Automation` ❌ — chỉ `Vector Search` cần embedding model (model biến text thành vector) và `Generate Answer` cần LLM (mô hình ngôn ngữ lớn).

**Vì sao**

Tài liệu coi framework là "bộ não orchestration", còn mô hình AI chỉ là "bộ não suy luận" — một mảnh trong puzzle. Chính tài liệu ước tính **~60% framework là code thuần không cần model**, ~40% mới cần. Cảm giác "nhiều quá" thường đến từ việc bạn đếm luôn cả phần không liên quan tới AI.

**Làm gì**

1. Mở mục `⚡ Quick Reference`, chọn **một** hàng theo việc bạn định làm — đừng đọc tuần tự 13 phần.
2. Cài môi trường một lần, xài lại cho mọi module.
3. Bắt đầu bằng `harness/01-retrieve-memory-knowledge` và `harness/02-build-context`: bảng Module → Project ghi chúng phục vụ lần lượt 15/20 và 12/20 dự án trong tài liệu.
4. Chưa cần mua API: Ollama chạy local miễn phí, đủ để học hết Phase 1-6.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:12b        # model sinh câu trả lời
ollama pull nomic-embed-text  # model tạo vector, 768 chiều
```

**Kiểm tra**

`curl -s http://localhost:11434/api/tags` trả về cả hai tên model. Nạp 10 file markdown vào module 01, hỏi một câu tiếng Anh, và câu trả lời phải trích đúng đoạn đã nạp. Nếu không trích được, bạn mới đang ở tầng model — chưa chạm tới tầng framework.

---

### Q2. Mới mở repo lên, tôi bắt đầu từ đâu? [→ § 🛠️ Cách Sử Dụng + Lộ Trình Học]

**Bạn sẽ thấy**

Bạn đứng trước 15 module trong `harness/`, rồi `loop/`, rồi `graph/`. Lộ trình 6 phase trong tài liệu trông rất lộn xộn: Phase 1 là `01 Retrieve Memory → 02 Build Context`, nhưng Phase 2 nhảy sang `05 Prompt Builder ← 06 Decide Tools`, rồi Phase 3 quay lại `03 Update Memory → 04 Plan`.

**Vì sao**

Hai module đầu là đường ống lấy dữ liệu về — không có gì để đưa vào ngữ cảnh thì phần còn lại vô nghĩa. Lộ trình cố tình xen kẽ để bạn thấy một vòng chạy trọn vẹn (lấy dữ liệu → dựng ngữ cảnh → sinh câu trả lời) trước khi mở rộng sang ghi nhớ và lên kế hoạch. Tài liệu có sẵn lộ trình 26 tuần nếu bạn muốn đi hết, nhưng mục Tips vẫn dạy thẳng: "START SMALL".

**Làm gì**

1. Làm dự án #1 Personal Knowledge Base trước — 2-3 ngày, chỉ dùng module 01, 03, 06. Dự án này chỉ cần ChromaDB + `nomic-embed-text` + một CLI bằng Python.
2. Rồi tới dự án #2 Document Q&A Chatbot — 3-5 ngày, thêm module 02 và 05. Kết quả mong đợi: chatbot trả lời đúng từ tài liệu nội bộ thay vì bịa.
3. Ghép sau: #1 + #2 = #6 Enterprise RAG Platform.
4. Đo kết quả từng bước (số câu trả lời đúng) trước khi thêm module mới. Ở cấp trung bình, dự án #6 mới được ghi là 2-3 tuần cho bản MVP.

```bash
ollama serve                                     # chạy model local
curl -s localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text","input":"deploy docker"}'
```

**Kiểm tra**

Lệnh `curl` trả về 768 số thực. Lệnh `pkb search "cách deploy Docker"` tìm đúng ghi chú giữa khoảng 1.000 ghi chú. Nếu chưa tìm được, hãy sửa cách **tìm kiếm** (BM25 + vector) chứ đừng đụng tới prompt builder.

---

### Q3. Module 12 là Sandbox mà "Part XII" lại là Loop — tôi bị rối ở chỗ nào? [→ § Cấu Trúc Học Tập]

**Bạn sẽ thấy**

Trong `AI_AGENT_FRAMEWORK.md`, "Part XII" là Loop Engineering và "Part XIII" là Graph Engineering. Nhưng trong thư mục `harness/`, module `12` là Sandbox Execution, `13` là Trajectory & Observability, `14` là Compaction & Context, `15` là Approval Gates. Người mới thấy "số 12" là tìm nhầm sang `loop/`.

**Vì sao**

Hai hệ số cùng tồn tại: số `01`–`15` đánh số **module trong thư mục**, còn nhãn `Part I`–`Part XIII` đánh số **phần của tài liệu**. Tài liệu đã tự cảnh báo chuyện này ngay dưới bảng Quick Reference.

**Làm gì**

1. Đếm bằng **đường dẫn**, không đếm bằng nhãn: `harness/12-sandbox-execution` luôn là sandbox, không bao giờ là loop.
2. Dùng ba file ở gốc thư mục làm bản đồ: `AI_AGENT_FRAMEWORK.md` (trang chủ), `HARNESS_ENGINEERING.md`, `GRAPH_ENGINEERING.md`.
3. Module 12–15 không nằm trên lộ trình học vì chúng **không phải giai đoạn** của đường ống, mà là nền mà mọi giai đoạn 01–11 đều phụ thuộc vào.
4. Muốn agent tự cải thiện qua nhiều vòng chạy thì vào `loop/`, không phải `harness/12`.

| Bạn đang tìm | Đường dẫn đúng |
|---|---|
| Cách ly code agent chạy lệnh | `harness/12-sandbox-execution/` |
| Xem lại một lần chạy đã xảy ra | `harness/13-trajectory-observability/` |
| Giữ context không phình vô hạn | `harness/14-compaction-context/` |
| Xin người duyệt việc không đảo ngược | `harness/15-approval-gates/` |

```bash
ls harness | grep -c '^1[2-5]-'   # → 4: sandbox, trajectory, compaction, approval
ls loop    | grep -c '^0'        # → 7: phần Loop Engineering
```

**Kiểm tra**

Đếm thư mục: `harness/` có 15 module, `graph/` có 9 module, `loop/` có 7 phần. Mở `harness/12-sandbox-execution/README.md`, phần đầu phải nói về cách ly và ranh giới thực thi, không nói về vòng lặp cải thiện.

---

### Q4. Tôi có phải mua model đắt tiền không, và model 12 tỉ tham số có nặng máy không? [→ § Môi Trường Thực Hành + 2 loại model]

**Bạn sẽ thấy**

Tài liệu liệt kê `gemma3:12b` và `nomic-embed-text` chạy qua Ollama, rồi bảng lương ghi 30-80 triệu/tháng cho AI Engineer. Người mới hỏi thẳng: có phải cần mua `GPT-4o` hay `Claude` không, và 12 tỉ tham số có chạy nổi trên laptop không.

**Vì sao**

Framework chỉ cần đúng **hai loại model**: một embedding model để tìm kiếm, một LLM để sinh câu trả lời. Trong ví dụ RAG đầu tiên của tài liệu, chỉ có 2 dòng gọi HTTP là cần model; phần cắt đoạn văn bản, lưu trữ vector, tính điểm cosine — Python thuần.

**Làm gì**

1. Dùng Ollama local miễn phí để học: `nomic-embed-text` chỉ 768 chiều, nhẹ hơn nhiều so với việc thuê API.
2. Chuyển sang API trả phí chỉ khi cần chất lượng cao hơn — đổi đúng **một** dòng, phần còn lại giữ nguyên.
3. Đo chi phí trước khi scale: harness tiết kiệm 40-60% tiền token nhờ nén ngữ cảnh và kiểm tra đầu ra.

| Loại model | Việc của nó | Chạy local | Chạy trả phí |
|---|---|---|---|
| Embedding model | đổi text thành vector để tìm kiếm | `nomic-embed-text` | `text-embedding-3-small` |
| LLM | sinh câu trả lời | `gemma3:12b` | `GPT-4o`, `Claude` |

```python
OLLAMA_URL = "http://localhost:11434"        # miễn phí
MODEL = "gemma3:12b"                         # đổi sang "gpt-4o" = trả phí
r = requests.post(f"{OLLAMA_URL}/api/generate",
    json={"model": MODEL, "prompt": p, "stream": False})
```

**Kiểm tra**

`ollama list` hiện `gemma3:12b`. Chạy cùng một câu hỏi ở local và ở API: nếu local đúng mà API sai, vấn đề nằm ở ngữ cảnh bạn gửi chứ không phải ở model.

---

## GRAPH_ENGINEERING.md

### Q1. Hệ thống của tôi đang ở tầng nào — keyword, vector, hay đã cần graph? [→ § 3 Ba Giai Đoạn Tiến Hóa Của Retrieval]

**Bạn sẽ thấy**

| Tầng | Bạn đang dùng gì | Câu hỏi nó trả lời tốt | Mức kiểm soát |
|---|---|---|---|
| 2020-2022 | BM25, inverted index | đúng từ khóa (mã hợp đồng) | ⭐ thấp |
| 2023-2025 | embeddings + vector DB | câu diễn đạt khác nhau | ⭐⭐⭐ trung bình |
| 2026+ | knowledge graph + GraphRAG | quan hệ nhiều bước | ⭐⭐⭐⭐⭐ cao |

Ký hiệu ⭐ chỉ là mức độ kiểm soát do tài liệu ghi, không phải điểm số hiệu năng. Bạn vừa dựng xong vector search, giờ nghe nói phải lên graph — nhưng câu hỏi thật của người dùng thuộc tầng nào?

**Vì sao**

Ba tầng **cộng dồn**, không thay thế. Tài liệu nói thẳng: vẫn cần BM25 cho mã hợp đồng, vẫn cần vector cho câu diễn đạt khác, và chỉ cần thêm graph cho câu hỏi nhiều bước (multi-hop) và câu hỏi bao quát cả tập tài liệu (global).

**Làm gì**

1. Lấy 20 câu hỏi thật của người dùng, gắn nhãn local / global / multi-hop theo bảng có trong tài liệu.
2. Chỉ mở `graph/` nếu lỗi tập trung ở nhóm global hoặc multi-hop.
3. Nếu lỗi nằm ở nhóm local ("điều 5 hợp đồng X nói gì"), hãy sửa cách cắt đoạn thay vì mua database mới.
4. Ghi lại những câu hỏi mà graph **không** giải quyết được — phần đó vẫn thuộc về BM25 và vector.

```python
# multi-hop: "Ai duyệt dự án X, người đó báo cáo cho ai?"
MATCH p = (X:Project {name:'X'})-[r*1..3]->(Y)
RETURN p, r.confidence AS do_tin_cay
```

**Kiểm tra**

Chạy lại 20 câu đó sau khi nối graph. Nếu số câu trả lời đúng không tăng, hãy xem lại chất lượng trích xuất quan hệ — chứ đừng vội đổi kho dữ liệu.

---

### Q2. Tôi không biết trước cần những quan hệ nào — có phải vẽ schema trước không? [→ § 8.2 The 8 Commandments of Graph Engineering]

**Bạn sẽ thấy**

Bạn có 500 file hợp đồng và email nội bộ. Người trong nghề nói phải có "ontology" (bộ quy tắc về loại thực thể và quan hệ nào là hợp lệ) — nghe giống phải biết trước mọi thứ trước khi bắt đầu. Không có thì đồ thị biến thành một "hairball" (búi tóc) không truy vấn nổi.

**Vì sao**

Tài liệu đặt luật số 1 là **Schema First, Data Second**: định nghĩa ontology trước khi nạp dữ liệu. Luật số 2 là **Every Edge Has Provenance** — mỗi quan hệ phải mang `source`, `confidence`, `timestamp`, vì đó chính là thứ biến một câu trả lời thành câu trả lời kiểm chứng được.

**Làm gì**

1. Chỉ cần 3 loại node và 5 loại edge để bắt đầu — con số này xuất hiện trong lời khuyên của tài liệu.
2. Đặt ontology vào file `data/ontology.yaml`, tách khỏi code.
3. Nạp dữ liệu theo lô kèm checkpoint, không nạp cả kho một lần.
4. Chặn quan hệ sai kiểu trước khi ghi: không cho `Person -[EATS]-> Project`.
5. Ghi rõ nguồn của mỗi quan hệ ngay lúc trích xuất, đừng đợi tới khi trả lời.

```yaml
node_types: [Person, Project, Document]
edge_types: [APPROVES, REPORTS_TO, BELONGS_TO]
constraints:
  - "Person -[REPORTS_TO]-> Person"
  - "Project -[APPROVES]-> Person"
```

**Kiểm tra**

Sau lô đầu tiên: mọi edge đều có đủ ba trường `source`, `confidence`, `timestamp`, và một câu hỏi nối 2 tài liệu trả lời được kèm đường dẫn. Thiếu trường nào thì vá tập trung vào script trích xuất, đừng sửa từng câu trả lời.

---

### Q3. Muốn thử trong một tuần mà chưa mua gì — bắt đầu từ đâu? [→ § 10 Công Cụ và Framework + § 11.3 Lời Khuyên]

**Bạn sẽ thấy**

Bạn muốn biết graph có thật sự giải quyết được vấn đề của mình không, nhưng ngân sách 0 đồng và thời gian 7 ngày. Bảng công cụ trong tài liệu có 6 dòng database; chọn sai thì mất cả tuần.

**Vì sao**

Nút thắt không phải chỗ lưu, mà là **xây graph**: mỗi vòng trích xuất quan hệ đều tốn token gọi LLM, và chất lượng trích xuất quyết định toàn bộ chất lượng phía sau. Vì vậy khối lượng khởi đầu phải nhỏ.

**Làm gì**

1. Bám lời khuyên cuối tài liệu: bắt đầu với **100 tài liệu, 3 loại node, 5 loại edge**. Đừng cố xây đồ thị kiểu Wikipedia ngay ngày đầu.
2. Chọn kho theo quy mô thật: `Kuzu` (nhúng trong Python) hoặc `NetworkX` (thư viện bộ nhớ) cho thử nghiệm; `Neo4j` khi lên production.
3. Dựng theo mẫu có sẵn: `docker-compose.yml` mở Neo4j, `scripts/extract_graph.py` để trích, `scripts/query_graph.py` để truy vấn, `scripts/evaluate.py` để đo.
4. Chặn `max_hops` ở mức 2-3, nếu không truy vấn sẽ nổ.
5. Bỏ qua `graph/07-gnn` lúc đầu — tài liệu coi đây là phần **học** trên đồ thị, không phải điều kiện để có câu trả lời đầu tiên.

```bash
docker compose up -d neo4j
python scripts/extract_graph.py data/raw_docs/ --out data/graph.json
python scripts/evaluate.py            # coverage, path_precision
```

**Kiểm tra**

Sau 100 tài liệu, câu hỏi local phải trả lời đúng ngay cả khi không có graph, còn câu hỏi multi-hop thì phải in ra được đường dẫn. Nếu độ chính xác chưa vượt vector search thuần, hãy thêm dữ liệu thay vì đổi kiến trúc.

---

### Q4. `graph/` khác `harness/` và `loop/` ở chỗ nào? [→ § 6 Tích Hợp Với Harness và Loop]

**Bạn sẽ thấy**

Ba thư mục cùng cấp, mỗi thư mục có con trẻ: `harness/` 15 module, `graph/` 9 module, `loop/` 7 phần. Không file nào nói rõ ai cấp cho ai, nên bạn không biết nên làm Graph trước hay sau Harness.

**Vì sao**

Tài liệu vẽ đúng quan hệ ba chiều: **Harness** (`harness/01-11`) cấp công cụ, bộ nhớ, ngữ cảnh, rào cản cho **một lần chạy** của agent. **Graph** (`graph/01-09`) cấp **lớp tri thức**, thay cho vector database đơn thuần. **Loop** (`loop/01-07`) điều phối **nhiều** lần chạy Harness theo thời gian.

**Làm gì**

1. Đi theo dòng chảy có sẵn trong tài liệu: tài liệu → `graph/02` (xây KG) → `graph/03` (lưu trữ) → `graph/05` (GraphRAG) → `harness/02` (ghép ngữ cảnh) → model.
2. Ánh xạ 7 thành phần sang 9 module trước khi mở code: node/edge → `01`, ontology → `02`, lưu trữ → `03`, embedding → `04`, GraphRAG → `05`, suy luận → `06`, GNN → `07`, pipeline → `08`, đo đạc → `09`.
3. Cập nhật tăng dần bằng `graph/08`, đừng xây lại toàn bộ mỗi khi có tài liệu mới.
4. Muốn hỏi sâu hơn phần này thì đọc FAQ của từng thư mục: `graph/FAQ.md`, `harness/FAQ.md`, `loop/FAQ.md`.

| Bạn muốn | Mở thư mục |
|---|---|
| Agent chạy 1 lần, cần công cụ, quyền, log | `harness/` |
| Câu trả lời cần quan hệ và đường dẫn chứng minh | `graph/` |
| Agent tự cải thiện qua nhiều vòng chạy | `loop/` |

**Kiểm tra**

Chạy `MATCH (n) RETURN count(n)` trên kho đồ thị — con số phải khác 0. Thêm một tài liệu mới rồi chạy lại `scripts/query_graph.py`: số node tăng lên, còn kết quả của câu hỏi cũ **không đổi**. Đó là dấu hiệu cập nhật tăng dần đang chạy đúng.

---

## HARNESS_ENGINEERING.md

### Q1. Thêm harness tốn công hơn không — có đáng không, và tiền thì thế nào? [→ § 4.1 + § 4.5 Tại Sao Harness Engineering Quan Trọng?]

**Bạn sẽ thấy**

Bạn đang xây một agent sửa lỗi. Tự thêm lớp kiểm tra, lớp giới hạn quyền, lớp log nghĩa là mất thêm 2-3 tuần trước khi có tính năng đầu tiên. Sếp muốn thấy kết quả tuần này. Bạn tự hỏi có đáng bỏ công không.

**Vì sao**

Tài liệu dẫn số đo được thay vì niềm tin: nghiên cứu SWE-agent của Princeton NLP cho thấy chỉ bằng cách thiết kế lại giao diện giữa agent và máy tính, tỉ lệ thành công tăng từ **12,5% lên 20,5%** — tăng 64% mà **không đổi model**. Mô hình không yếu; môi trường chưa được thiết kế.

**Làm gì**

1. Bắt đầu bằng bản tối giản: giới hạn output của công cụ, gắn linter vào lúc ghi file, nén lịch sử hội thoại. Ba việc này rẻ hơn nhiều so với viết lại cả hệ thống.
2. Chặn ngay một điều khoản không đổi được: **không cho lưu file nếu linter báo lỗi**.
3. Ghi lại 3 số từ ngày đầu: tỉ lệ thành công, thời gian xử lý một issue, số token mỗi lần chạy.

```typescript
const editTool = { execute: async (file, changes) => {
  const next = applyChanges(file, changes);
  const lint = await linter.check(next);       // kiểm tra ngay
  if (lint.errors.length) return { success: false, errors: lint.errors };
  await saveFile(file, next); return { success: true };
}};
```

**Kiểm tra**

Chạy cùng 20 issue GitHub trên cấu hình cũ và mới. Nếu tỉ lệ pass tăng mà bạn không đụng tới model, đó là bằng chứng giá trị của lớp môi trường. Con số trong ví dụ của tài liệu là $30.000 xuống còn $12.000 trong 3 tháng (giảm 60%), nhưng bạn phải đo trên hệ thống của mình, đừng chép con số này.

---

### Q2. Nghe nói "Prompt Engineering đã chết" — vậy tôi còn viết prompt không? [→ § 3 Ba Giai Đoạn Tiến Hóa Của Kỹ Nghệ AI]

**Bạn sẽ thấy**

Một bài viết bảo prompt engineering lỗi thời rồi; framework này lại dành riêng `harness/05-prompt-builder` và `harness/11-evaluation`. Bạn không biết nên bỏ hẳn prompt hay vẫn viết, và viết thì tới đâu cho đủ.

**Vì sao**

Tài liệu trả lời thẳng ở mục Key Insight: *"Prompt Engineering không chết, nhưng không còn đủ."* Ba giai đoạn cộng dồn mức kiểm soát — prompt (thấp) → context (trung bình) → harness (cao). Bảng "Phần nào cần model?" cũng ghi Prompt Building ❌: dựng prompt chỉ là sắp xếp chữ, không tốn một đồng API nào. Ví dụ trong tài liệu: lời dặn *"Hãy viết code Python. Đảm bảo code không có lỗi cú pháp"* bị thay bằng một đoạn code 9 dòng kiểm tra cú pháp trước khi trả về.

**Làm gì**

1. Vẫn viết prompt, nhưng đừng kỳ vọng nó giữ cả hệ thống. Một prompt 5 trang không cứu được một bước gọi tool sai.
2. Chuyển phần quan trọng từ lời dặn sang hạ tầng: prompt nói "hãy cẩn thận", code thì **không cho phép** trả về code lỗi.
3. Mỗi lần sửa prompt, chạy lại cùng bộ câu hỏi để biết sửa có ích không.

```javascript
harness.addTool({ name: "write_code", execute: async (code) => {
  const lint = await linter.check(code);      // thay vì "nhờ" AI cẩn thận
  return lint.hasErrors ? { status: "error", errors: lint.errors }
                        : { status: "success", code };
}});
```

**Kiểm tra**

Đếm số lần phải sửa prompt trong một tuần. Nếu số đó không giảm, bạn đang chữa bệnh bằng cách viết thêm chữ — hãy thêm một ràng buộc ở tầng công cụ hoặc tầng kiểm tra đầu ra.

---

### Q3. Module 12–15 là giai đoạn hay nền? Bỏ qua có được không? [→ § 🔭 Toàn Cảnh: 7 Components → 15 Modules]

**Bạn sẽ thấy**

Bạn xây xong module 01-11, agent đã tự sửa được lỗi đơn giản. Giờ đọc `harness/12` đến `harness/15` và thấy chúng được mô tả là "mặt phẳng kiểm soát xuyên module", không nằm trên lộ trình học. Bạn định bỏ qua để kịp deadline.

**Vì sao**

Module 01–11 là các giai đoạn của đường ống: làm tuần tự và thấy kết quả ngay. Module 12–15 **không phải** giai đoạn — chúng là nền mà mọi giai đoạn 01–11 đều phụ thuộc, giống xương sống đỡ cả cơ thể. Bỏ qua thì agent vẫn chạy, chỉ là mỗi lần sai không biết dừng ở đâu, không xem lại được lần chạy đó, và không xin được ai bấm nút đồng ý.

**Làm gì**

1. Ưu tiên theo tỉ lệ phủ mà tài liệu ghi sẵn: `01-retrieve-memory` 85%, `07-workflow` 80%, `06-decide-tools` 75%, còn `08-task` chỉ 45%.
2. Ghép `12-sandbox-execution` vào **sớm** — ngay khi agent bắt đầu chạy lệnh thật trên máy bạn, đừng đợi tới cuối dự án.
3. Bật `13-trajectory-observability` trước khi scale lên nhiều agent: không có log là không debug được.
4. Đặt `15-approval-gates` cho đúng những việc không đảo ngược được: deploy, xoá dữ liệu, gửi email hàng loạt.

```bash
# 4 dòng này dựng xong một lần chạy RAG tối giản để bắt đầu
ollama pull gemma3:12b
ollama pull nomic-embed-text
python scripts/extract.py docs/ --out kb.json
python scripts/query.py "báo giá còn hạn bao lâu?"
```

**Kiểm tra**

Chạy đầu-cuối: tài liệu của bạn được nạp, một câu hỏi trả lời đúng mà không cần sửa prompt. Nếu bạn không ghi lại thời gian, số token và tỉ lệ lỗi, bạn chưa có harness — bạn chỉ có một đoạn prompt dài.

---

### Q4. Tôi đã có code tìm kiếm rồi — làm sao cho nó tự chạy giữa prompt và LLM? [→ § 5.3 Vậy Can Thiệp Vào Đâu?]

**Bạn sẽ thấy**

Bạn đã viết và test hàm tìm context, chạy tay thì ra đúng 2 đoạn liên quan. Nhưng mở giao diện chat và gõ câu hỏi thì câu trả lời vẫn chung chung — vì ứng dụng đang gọi thẳng `localhost:11434`, không qua bất kỳ đoạn nào của bạn.

**Vì sao**

Không có ai tự gọi code của bạn. Bạn phải đứng giữa: chặn (intercept) câu hỏi, tìm context, ghép vào câu hỏi, rồi mới gửi đi. Tài liệu vẽ đúng 4 bước này và đưa ra 4 cách cài đặt.

**Làm gì**

1. Chọn một trong bốn cách: **proxy server** (mọi ứng dụng chat), **wrapper hàm** (code Python của bạn), **Open WebUI** (không cần code), **LangChain/LlamaIndex** (production).
2. Cách nhanh nhất là dựng proxy rồi đổi địa chỉ trong app chat: từ `localhost:11434` sang `localhost:5000/api/chat`.
3. Luôn in ra số đoạn context đã ghép — đó là bằng chứng bạn không quên bước trung gian.

| Cách | Dùng khi | Độ khó |
|---|---|---|
| Proxy server | bất kỳ app chat nào (web, mobile, desktop) | ⭐⭐ |
| Wrapper hàm | app Python do bạn tự viết | ⭐ |
| Open WebUI | đã dùng Open WebUI | ⭐ không cần code |

```python
@app.route("/api/chat", methods=["POST"])
def chat():
    ctx = search_relevant(data.get("prompt", ""))          # tìm context
    aug = f"Answer using:\n{chr(10).join(ctx)}\n\nQuestion: {prompt}"
    return jsonify(requests.post(OLLAMA_URL, json={
        "model": "gemma3:12b", "prompt": aug, "stream": False}).json())
```

**Kiểm tra**

Mở log ở proxy, gõ một câu hỏi trên giao diện: log phải hiện các đoạn context được ghép vào **trước** khi có request tới Ollama. Không thấy dòng log đó nghĩa là ứng dụng vẫn đang gọi thẳng model.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: AI_AGENT_FRAMEWORK.md, GRAPH_ENGINEERING.md, HARNESS_ENGINEERING.md.*