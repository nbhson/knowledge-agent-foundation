# ❓ FAQ — AI Coding Skills Framework (Real Stories, Plain Language)

If a question is unclear, read the section in the named file (named in brackets).

---

## AI_AGENT_FRAMEWORK.md

### Q1. Framework này thực chất là cái gì — khác gì dùng ChatGPT bình thường? [→ § 🧠 Understanding This Framework]

**What you see**

Bạn clone repo, mở `AI_AGENT_FRAMEWORK.md` (1195 dòng), thấy ba thư mục con: `harness/` (15 module), `graph/` (9 module), `loop/` (7 phần). Dòng đầu tiên của tài liệu nói rõ: đây là hướng dẫn **xây** agent, không phải cách **dùng** AI thông thường. Bảng "Which parts need a model?" cũng gây bất ngờ: `BM25 Search` ❌, `Prompt Building` ❌, `Workflow` ❌, `CI/CD Automation` ❌ — chỉ `Vector Search` cần embedding model (model đổi text thành vector) và `Generate Answer` cần LLM (mô hình ngôn ngữ lớn).

**Why**

Tài liệu coi framework là "bộ não điều phối", còn mô hình AI chỉ là "bộ não suy luận" — một mảnh trong puzzle. Chính tài liệu ước tính **~60% framework là code thuần không cần model**, ~40% cần model. Cảm giác "nhiều quá" thường đến từ việc đếm cả phần không liên quan tới AI.

**What to do**

1. Mở mục `⚡ Quick Reference`, chọn **một** hàng theo việc bạn định làm — không đọc tuần tự 13 phần.
2. Cài môi trường một lần, dùng lại cho mọi module.
3. Bắt đầu bằng `harness/01-retrieve-memory-knowledge` và `harness/02-build-context`: ma trận Module → Project ghi chúng phục vụ lần lượt 15/20 và 12/20 dự án trong tài liệu.
4. Chưa cần mua API: Ollama chạy local miễn phí, đủ để học hết Phase 1-6.

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:12b        # model sinh câu trả lời
ollama pull nomic-embed-text  # model tạo vector, 768 chiều
```

**Verify**

`curl -s http://localhost:11434/api/tags` trả về cả hai tên model. Nạp 10 file markdown vào module 01, hỏi một câu tiếng Anh, và câu trả lời phải trích đúng đoạn đã nạp. Nếu không trích được, bạn đang ở tầng model — chưa chạm tới tầng framework.

---

### Q2. Mới vào, tôi nên bắt đầu từ đâu? [→ § 🛠️ How to Use + Lộ Trình Học]

**What you see**

Bạn đứng trước 15 module của `harness/`, rồi `loop/`, rồi `graph/`. Lộ trình 6 phase trong tài liệu trông rất lộn xộn: Phase 1 là `01 Retrieve Memory → 02 Build Context`, nhưng Phase 2 nhảy sang `05 Prompt Builder ← 06 Decide Tools`, rồi Phase 3 quay lại `03 Update Memory → 04 Plan`.

**Why**

Hai module đầu là đường ống lấy dữ liệu về — không có gì để đưa vào ngữ cảnh thì phần còn lại vô nghĩa. Lộ trình cố tình xen kẽ để bạn thấy một vòng chạy trọn vẹn (lấy dữ liệu → dựng ngữ cảnh → sinh câu trả lời) trước khi mở rộng sang ghi nhớ và kế hoạch. Tài liệu cũng có sẵn lộ trình 26 tuần nếu bạn muốn đi hết — nhưng mục Tips vẫn dạy "START SMALL".

**What to do**

1. Làm dự án #1 Personal Knowledge Base trước — 2-3 ngày, chỉ dùng module 01, 03, 06. Dự án này chỉ cần ChromaDB + `nomic-embed-text` + một CLI bằng Python.
2. Rồi tới dự án #2 Document Q&A Chatbot — 3-5 ngày, thêm module 02 và 05. Kết quả mong đợi: chatbot trả lời đúng từ tài liệu nội bộ thay vì bịa.
3. Ghép sau: #1 + #2 = #6 Enterprise RAG Platform.
4. Đo kết quả từng bước (số câu trả lời đúng) trước khi thêm module mới. Ở cấp trung bình, dự án #6 mới được ghi là 2-3 tuần cho bản MVP.

```bash
ollama serve                                     # chạy model local
curl -s localhost:11434/api/embed \
  -d '{"model":"nomic-embed-text","input":"deploy docker"}'
```

**Verify**

Lệnh `curl` trả về 768 số thực. Lệnh `pkb search "cách deploy Docker"` tìm đúng ghi chú giữa khoảng 1000 ghi chú. Nếu chưa tìm được, hãy sửa cách **tìm kiếm** (BM25 + vector) chứ đừng đụng tới prompt builder.

---

### Q3. Module 12 là Sandbox, nhưng "Part XII" lại là Loop — tôi bị lừa ở đâu? [→ § Learning Structure]

**What you see**

Trong `AI_AGENT_FRAMEWORK.md`, "Part XII" là Loop Engineering và "Part XIII" là Graph Engineering. Nhưng trong thư mục `harness/`, module `12` là Sandbox Execution, `13` là Trajectory & Observability, `14` là Compaction & Context, `15` là Approval Gates. Người mới thấy "số 12" là tìm nhầm sang `loop/`.

**Why**

Hai hệ số cùng tồn tại: số `01`–`15` đánh số **module trong thư mục**, còn nhãn `Part I`–`Part XIII` đánh số **phần của tài liệu**. Tài liệu đã tự cảnh báo chuyện này ngay dưới bảng Quick Reference.

**What to do**

1. Đếm bằng **đường dẫn**, không đếm bằng nhãn: `harness/12-sandbox-execution` luôn là sandbox, không bao giờ là loop.
2. Dùng ba file ở gốc thư mục làm bản đồ: `AI_AGENT_FRAMEWORK.md` (trang chủ), `HARNESS_ENGINEERING.md`, `GRAPH_ENGINEERING.md`.
3. Module 12–15 không nằm trên learning path vì chúng **không phải giai đoạn** của đường ống mà là nền mà mọi giai đoạn 01–11 đều dựa vào.
4. Muốn cải thiện liên tục theo thời gian thì vào `loop/`, không phải `harness/12`.

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

**Verify**

Đếm thư mục: `harness/` có 15 module, `graph/` có 9 module, `loop/` có 7 phần. Mở `harness/12-sandbox-execution/README.md`, phần đầu phải nói về cách ly và ranh giới thực thi, không nói về vòng lặp cải thiện.

---

### Q4. Tôi có phải mua model đắt tiền không, và model 12 tỉ tham số có nặng máy không? [→ § Hands-on Environment + 2 loại model]

**What you see**

Tài liệu liệt kê `gemma3:12b` và `nomic-embed-text` chạy qua Ollama, rồi bảng lương ghi 30-80 triệu/tháng cho AI Engineer. Người mới hỏi: có phải cần mua `GPT-4o` hay `Claude` không, và 12 tỉ tham số có chạy nổi trên laptop không.

**Why**

Framework chỉ cần đúng **hai loại model**: một embedding model để tìm kiếm, một LLM để sinh câu trả lời. Trong ví dụ RAG đầu tiên của tài liệu, chỉ có 2 dòng gọi HTTP là cần model; phần cắt đoạn, lưu trữ vector, tính điểm cosine — Python thuần.

**What to do**

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

**Verify**

`ollama list` hiện `gemma3:12b`. Chạy cùng một câu hỏi ở local và ở API: nếu local đúng mà API sai, vấn đề nằm ở ngữ cảnh bạn gửi chứ không phải ở model.

---

## GRAPH_ENGINEERING.md

### Q1. Tôi đang ở tầng truy xuất nào — keyword, vector, hay đã cần graph? [→ § 3 Three Stages of Retrieval Evolution]

**What you see**

| Tầng | Bạn đang dùng gì | Câu hỏi nó trả lời tốt | Mức kiểm soát |
|---|---|---|---|
| 2020-2022 | BM25, inverted index | đúng từ khóa (mã hợp đồng) | ⭐ thấp |
| 2023-2025 | embeddings + vector DB | câu diễn đạt khác nhau | ⭐⭐⭐ trung bình |
| 2026+ | knowledge graph + GraphRAG | quan hệ nhiều bước | ⭐⭐⭐⭐⭐ cao |

Ký hiệu ⭐ chỉ mức độ kiểm soát do tài liệu ghi, không phải điểm số hiệu năng. Bạn vừa dựng xong vector search, giờ nghe nói phải lên graph — nhưng câu hỏi thật của người dùng nằm ở tầng nào?

**Why**

Ba tầng **cộng dồn**, không thay thế. Tài liệu nói thẳng: vẫn cần BM25 cho mã hợp đồng, vẫn cần vector cho câu diễn đạt khác, và chỉ cần thêm graph cho multi-hop và global sensemaking.

**What to do**

1. Lấy 20 câu hỏi thật của người dùng, gắn nhãn local / global / multi-hop theo bảng trong tài liệu.
2. Chỉ mở `graph/` nếu lỗi tập trung ở nhóm global hoặc multi-hop.
3. Nếu lỗi nằm ở nhóm local ("điều 5 hợp đồng X nói gì"), hãy sửa chunking thay vì mua database mới.
4. Ghi lại câu hỏi nào graph **không** giải quyết được — phần đó vẫn thuộc về BM25 và vector.

```python
# multi-hop: "Ai duyệt dự án X, người đó báo cáo cho ai?"
MATCH p = (X:Project {name:'X'})-[r*1..3]->(Y)
RETURN p, r.confidence AS do_tin_cay
```

**Verify**

Chạy lại 20 câu đó sau khi nối graph. Nếu số câu trả lời đúng không tăng, hãy xem lại chất lượng trích xuất quan hệ — chứ đừng vội đổi kho.

---

### Q2. Tôi không biết trước cần những quan hệ nào — có phải vẽ schema trước không? [→ § 8.2 The 8 Commandments of Graph Engineering]

**What you see**

Bạn có 500 file hợp đồng và email nội bộ. Người trong nghề nói phải có "ontology" (bộ quy tắc về loại thực thể và quan hệ hợp lệ) — nghe giống phải biết trước mọi thứ trước khi bắt đầu. Nếu không, tài liệu cảnh báo đồ thị biến thành một "hairball" (búi tóc) không truy vấn được.

**Why**

Tài liệu đặt luật số 1 là **Schema First, Data Second**: định nghĩa ontology trước khi nạp dữ liệu. Luật số 2 là **Every Edge Has Provenance** — mỗi quan hệ phải mang `source`, `confidence`, `timestamp`, vì đó chính là thứ biến một câu trả lời thành câu trả lời kiểm chứng được.

**What to do**

1. Chỉ cần 3 loại node và 5 loại edge để bắt đầu — con số này xuất hiện trong lời khuyên của tài liệu.
2. Đặt ontology vào file `data/ontology.yaml`, tách khỏi code.
3. Nạp dữ liệu theo lô kèm checkpoint, không nạp cả kho một lần.
4. Chặn quan hệ sai kiểu trước khi ghi: không cho `Person -[EATS]-> Project`.
5. Ghi rõ nguồn của mỗi quan hệ ngay khi trích xuất, đừng đợi tới lúc trả lời.

```yaml
node_types: [Person, Project, Document]
edge_types: [APPROVES, REPORTS_TO, BELONGS_TO]
constraints:
  - "Person -[REPORTS_TO]-> Person"
  - "Project -[APPROVES]-> Person"
```

**Verify**

Sau lô đầu tiên: mọi edge đều có đủ ba trường `source`, `confidence`, `timestamp`; và một câu hỏi nối 2 tài liệu trả lời được kèm đường dẫn. Nếu thiếu trường nào, hãy vá tập trung vào script trích xuất, đừng sửa từng câu trả lời.

---

### Q3. Muốn thử trong một tuần mà chưa mua gì — bắt đầu từ đâu? [→ § 10 Tools and Frameworks + § 11.3 Advice]

**What you see**

Bạn muốn xem graph có thực sự giải quyết được vấn đề của mình không, nhưng ngân sách là 0 đồng và thời gian là 7 ngày. Bảng công cụ trong tài liệu có 6 dòng database; chọn sai thì mất cả tuần.

**Why**

Nút thắt không phải nơi lưu, mà là **xây graph**: mỗi vòng trích xuất quan hệ đều tốn token gọi LLM, và chất lượng trích xuất quyết định toàn bộ chất lượng phía sau. Vì vậy khối lượng khởi đầu phải nhỏ.

**What to do**

1. Bám lời khuyên cuối tài liệu: bắt đầu với **100 tài liệu, 3 loại node, 5 loại edge**. Đừng cố xây đồ thị kiểu Wikipedia ngay ngày đầu.
2. Chọn kho theo quy mô thật: `Kuzu` (nhúng trong Python) hoặc `NetworkX` (thư viện bộ nhớ) cho thử nghiệm; `Neo4j` khi lên production.
3. Dựng bằng mẫu sẵn có: `docker-compose.yml` mở Neo4j, `scripts/extract_graph.py` để trích, `scripts/query_graph.py` để truy vấn, `scripts/evaluate.py` để đo.
4. Chặn `max_hops` ở mức 2-3, nếu không truy vấn sẽ nổ.
5. Bỏ qua `graph/07-gnn` lúc đầu — tài liệu coi đây là phần **học** trên đồ thị, không phải điều kiện để có câu trả lời đầu tiên.

```bash
docker compose up -d neo4j
python scripts/extract_graph.py data/raw_docs/ --out data/graph.json
python scripts/evaluate.py            # coverage, path_precision
```

**Verify**

Sau 100 tài liệu, câu hỏi local phải trả lời đúng không cần graph, và câu hỏi multi-hop phải in ra được đường dẫn. Nếu độ chính xác chưa vượt vector search thuần, hãy thêm dữ liệu thay vì đổi kiến trúc.

---

### Q4. `graph/` khác `harness/` và `loop/` ở chỗ nào? [→ § 6 Integration With Harness and Loop]

**What you see**

Ba thư mục cùng cấp, mỗi thư mục có con trẻ: `harness/` 15 module, `graph/` 9 module, `loop/` 7 phần. Không có file nào nói rõ ai cấp cho ai, nên bạn không biết nên làm Graph trước hay sau Harness.

**Why**

Tài liệu vẽ đúng quan hệ ba chiều: **Harness** (`harness/01-11`) cấp công cụ, bộ nhớ, ngữ cảnh, rào cản cho **một lần chạy** của agent. **Graph** (`graph/01-09`) cấp **lớp tri thức**, thay cho vector database đơn thuần. **Loop** (`loop/01-07`) điều phối **nhiều** lần chạy Harness theo thời gian.

**What to do**

1. Đi theo dòng chảy có sẵn trong tài liệu: tài liệu → `graph/02` (xây KG) → `graph/03` (lưu trữ) → `graph/05` (GraphRAG) → `harness/02` (ghép ngữ cảnh) → model.
2. Ánh xạ 7 thành phần sang 9 module trước khi mở code: node/edge → `01`, ontology → `02`, lưu trữ → `03`, embedding → `04`, GraphRAG → `05`, suy luận → `06`, GNN → `07`, pipeline → `08`, đo đạc → `09`.
3. Cập nhật tăng dần bằng `graph/08`, đừng xây lại toàn bộ mỗi khi có tài liệu mới.
4. Nếu hỏi sâu hơn về phần này, đọc FAQ của từng thư mục: `graph/FAQ.md`, `harness/FAQ.md`, `loop/FAQ.md`.

| Bạn muốn | Mở thư mục |
|---|---|
| Agent chạy 1 lần và cần công cụ, quyền, log | `harness/` |
| Câu trả lời cần quan hệ và đường dẫn chứng minh | `graph/` |
| Agent tự cải thiện qua nhiều vòng chạy | `loop/` |

**Verify**

Chạy `MATCH (n) RETURN count(n)` trên kho đồ thị — con số phải khác 0. Thêm một tài liệu mới rồi chạy lại `scripts/query_graph.py`: số node tăng lên, và kết quả của câu hỏi cũ **không đổi**, đó là dấu hiệu cập nhật tăng dần hoạt động đúng.

---

## HARNESS_ENGINEERING.md

### Q1. Thêm harness tốn công hơn không — có đáng không, và tiền thì thế nào? [→ § 4.1 + § 4.5 Why Is Harness Engineering Important?]

**What you see**

Bạn đang xây một agent sửa lỗi. Tự viết thêm lớp kiểm tra, lớp giới hạn quyền, lớp log nghĩa là thêm 2-3 tuần trước khi có tính năng. Sếp muốn thấy kết quả tuần này. Bạn tự hỏi có đáng bỏ công không.

**Why**

Tài liệu dẫn kết quả đo được thay vì niềm tin: nghiên cứu SWE-agent của Princeton NLP cho thấy chỉ bằng cách thiết kế lại giao diện giữa agent và máy tính, tỉ lệ thành công tăng từ **12,5% lên 20,5%** — tăng 64% mà **không đổi model**. Mô hình không yếu; môi trường chưa được thiết kế.

**What to do**

1. Bắt đầu bằng bản tối giản: giới hạn output của công cụ, gắn linter vào lúc ghi file, nén lịch sử hội thoại. Ba thay đổi này rẻ hơn nhiều so với viết lại hệ thống.
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

**Verify**

Chạy cùng 20 issue GitHub trên cấu hình cũ và mới. Nếu tỉ lệ pass tăng mà bạn không đụng tới model, đó là bằng chứng giá trị của lớp môi trường. Con số tiết kiệm trong ví dụ của tài liệu: $30.000 → $12.000 trong 3 tháng (giảm 60%), nhưng bạn phải đo trên hệ thống của mình, không sao chép con số này.

---

### Q2. Nghe nói "Prompt Engineering đã chết" — vậy tôi còn viết prompt không? [→ § 3 Three Evolution Phases of AI Engineering]

**What you see**

Một bài viết bảo prompt engineering đã lỗi thời; framework này lại dành riêng `harness/05-prompt-builder` và `harness/11-evaluation`. Bạn không biết nên bỏ hẳn prompt hay vẫn viết, và viết thì tới đâu.

**Why**

Tài liệu trả lời thẳng ở mục Key Insight: *"Prompt Engineering không chết, nhưng không còn đủ."* Ba giai đoạn cộng dồn mức kiểm soát — prompt (thấp) → context (trung bình) → harness (cao). Bảng "Phần nào cần model?" cũng ghi Prompt Building ❌: dựng prompt chỉ là sắp xếp chữ, không tốn một đồng API nào. Ví dụ trong tài liệu: lời dặn *"Hãy viết code Python. Đảm bảo code không có lỗi cú pháp"* bị thay bằng một đoạn code 9 dòng kiểm tra cú pháp trước khi trả về.

**What to do**

1. Vẫn viết prompt, nhưng đừng kỳ vọng nó giữ hệ thống. Một prompt 5 trang không cứu được một bước tool call sai.
2. Chuyển phần quan trọng từ lời dặn sang hạ tầng: prompt nói "hãy cẩn thận", code thì **không cho phép** trả về code lỗi.
3. Mỗi lần sửa prompt, chạy lại cùng bộ câu hỏi để biết sửa có ích không.

```javascript
harness.addTool({ name: "write_code", execute: async (code) => {
  const lint = await linter.check(code);      // thay vì "nhờ" AI cẩn thận
  return lint.hasErrors ? { status: "error", errors: lint.errors }
                        : { status: "success", code };
}});
```

**Verify**

Đếm số lần phải sửa prompt trong một tuần. Nếu số đó không giảm, bạn đang chữa bệnh bằng cách viết thêm chữ — hãy thêm một ràng buộc ở tầng công cụ hoặc tầng kiểm tra đầu ra.

---

### Q3. Module 12–15 là giai đoạn hay nền? Tôi có thể bỏ qua không? [→ § 🔭 Overview: 7 Components → 15 Modules]

**What you see**

Bạn xây xong module 01-11, agent đã tự sửa được lỗi đơn giản. Giờ bạn đọc `harness/12` đến `harness/15` và thấy chúng được mô tả là "mặt phẳng kiểm soát xuyên module", không nằm trên lộ trình học. Bạn định bỏ qua để kịp deadline.

**Why**

Module 01–11 là các giai đoạn của đường ống: làm tuần tự và thấy kết quả ngay. Module 12–15 **không phải** giai đoạn — chúng là nền mà mọi giai đoạn 01–11 đều phụ thuộc, giống xương sống đỡ cả cơ thể. Bỏ qua thì agent vẫn chạy, chỉ là mỗi lần sai là không biết dừng ở đâu, không replay được, và không xin được ai bấm nút đồng ý.

**What to do**

1. Ưu tiên theo tỉ lệ phủ mà tài liệu ghi sẵn: `01-retrieve-memory` 85%, `07-workflow` 80%, `06-decide-tools` 75%, còn `08-task` chỉ 45%.
2. Ghép `12-sandbox-execution` vào **sớm** — ngay khi agent bắt đầu chạy lệnh thật trên máy bạn, không đợi cuối dự án.
3. Bật `13-trajectory-observability` trước khi scale lên nhiều agent: không có log là không debug được.
4. Đặt `15-approval-gates` cho đúng những việc không đảo ngược được (deploy, xoá dữ liệu, gửi email hàng loạt).

```bash
# 4 dòng này dựng xong một lần chạy RAG tối giản để bắt đầu
ollama pull gemma3:12b
ollama pull nomic-embed-text
python scripts/extract.py docs/ --out kb.json
python scripts/query.py "báo giá còn hạn bao lâu?"
```

**Verify**

Chạy đầu-cuối: tài liệu của bạn được nạp, một câu hỏi trả lời đúng mà không cần sửa prompt. Nếu bạn không ghi lại thời gian, số token và tỉ lệ lỗi, bạn chưa có harness — bạn chỉ có một đoạn prompt dài.

---

### Q4. Tôi đã có code tìm kiếm rồi — làm sao cho nó tự chạy giữa prompt và LLM? [→ § 5.3 Where Does the Intervention Happen?]

**What you see**

Bạn đã viết và test hàm tìm context, chạy tay thì ra đúng 2 đoạn liên quan. Nhưng khi mở giao diện chat và gõ câu hỏi, câu trả lời vẫn chung chung — vì ứng dụng đang gọi thẳng `localhost:11434`, không qua bất kỳ đoạn nào của bạn.

**Why**

Không có ai tự gọi code của bạn. Bạn phải đứng giữa: chặn (intercept) câu hỏi, tìm context, ghép vào câu hỏi, rồi mới gửi đi. Tài liệu vẽ đúng 4 bước này và cho 4 cách cài đặt.

**What to do**

1. Chọn một trong bốn cách: **proxy server** (mọi ứng dụng chat), **wrapper hàm** (code Python của bạn), **Open WebUI** (không cần code), **LangChain/LlamaIndex** (production).
2. Cách nhanh nhất là dựng proxy và đổi địa chỉ trong app chat: từ `localhost:11434` sang `localhost:5000/api/chat`.
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

**Verify**

Mở log ở proxy, gõ một câu hỏi trên giao diện: log phải hiện các đoạn context được ghép vào **trước** khi có request tới Ollama. Không thấy dòng log đó nghĩa là ứng dụng vẫn đang gọi thẳng model.

---

*FAQ file riêng — file nguồn không bị sửa. Nguồn: AI_AGENT_FRAMEWORK.md, GRAPH_ENGINEERING.md, HARNESS_ENGINEERING.md.*