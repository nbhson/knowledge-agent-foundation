# 💾 III. Update Memory & Knowledge Store

> ## 📑 Mục Lục
>
> - [Tổng Quan](#tổng-quan)
> - [Tại Sao Update Memory & Knowledge Store Quan Trọng?](#tại-sao-update-memory-knowledge-store-quan-trọng)
> - [Nội Dung](#nội-dung)
> - [1. Write-back Memory](#1-write-back-memory)
>   - [1.1 Khi Nào Cần Write-back?](#11-khi-nào-cần-write-back)
>   - [1.2 Write-back Implementation](#12-write-back-implementation)
> - [2. Memory Consolidation](#2-memory-consolidation)
>   - [2.1 Consolidation Là Gì?](#21-consolidation-là-gì)
>   - [2.2 Implementation](#22-implementation)
> - [3. Report Generation](#3-report-generation)
>   - [3.1 Report Types](#31-report-types)
>   - [3.2 Implementation](#32-implementation)
> - [4. KB Maintenance](#4-kb-maintenance)
>   - [4.1 Knowledge Base Operations](#41-knowledge-base-operations)
> - [5. Event Sourcing Pattern](#5-event-sourcing-pattern)
>   - [5.1 Concept](#51-concept)
>   - [5.2 Implementation](#52-implementation)
> - [6. Memory Store Case Studies](#6-memory-store-case-studies)
>   - [6.1. Claude Code — Session Memory & Cross-Session Persistence](#61-claude-code-session-memory-cross-session-persistence)
>   - [6.2. Mem0 — Production Memory Layer for AI Agents](#62-mem0-production-memory-layer-for-ai-agents)
>   - [6.3. OpenMemory — MCP-Based Memory Server](#63-openmemory-mcp-based-memory-server)
>   - [6.4. DeepSeek Harness — Trajectory Fork & Replay Engine](#64-deepseek-harness-trajectory-fork-replay-engine)
> - [7. Advanced Memory Patterns](#7-advanced-memory-patterns)
>   - [7.1. Write-Behind Cache Pattern](#71-write-behind-cache-pattern)
>   - [7.2. Memory Consolidation Pipeline](#72-memory-consolidation-pipeline)
>   - [7.3. Versioned Memory (Git-like Memory)](#73-versioned-memory-git-like-memory)
> - [8. Best Practices & Anti-Patterns](#8-best-practices-anti-patterns)
> - [9. Performance Metrics](#9-performance-metrics)
> - [10. Labs Thực Hành](#10-labs-thực-hành)
>   - [Lab 1: Write-back Memory](#lab-1-write-back-memory)
>   - [Lab 2: Consolidation](#lab-2-consolidation)
>   - [Lab 3: Versioned Memory](#lab-3-versioned-memory)
>   - [Lab 4: Metrics](#lab-4-metrics)
> - [11. Tài Liệu Tham Khảo](#11-tài-liệu-tham-khảo)
>   - [Papers & Research](#papers-research)
>   - [Frameworks & Tools](#frameworks-tools)
>   - [Blogs & Resources](#blogs-resources)
>
---

### Câu Chuyện Mở Đầu

Phần này mở bài bằng một câu chuyện đời thường, để giải thích vì sao ta cần "cập nhật bộ nhớ" thay vì chỉ "ghi thêm" mỗi ngày.

Hãy tưởng tượng bạn mới nhận việc trông thư viện phường. Sáng nào cũng có người mang sách mới tới tặng, chiều lại có người trả sách cũ. Nếu bạn cứ hồn nhiên nhận hết rồi chồng bừa lên kệ, chẳng bao giờ xếp lại cho gọn, chẳng dám bỏ cuốn nào đã mục nát, cũng không buồn ghi thêm vào cuốn catalog — thì chỉ một năm sau thôi, thư viện sẽ thành một **kho chứa đồ lộn xộn**, muốn tìm một cuốn truyện cũng phải bới tung cả đống.

**Bộ nhớ của AI cũng y hệt như vậy nếu chỉ biết "ghi vào" mà quên "dọn lại".**

LLM (mô hình ngôn ngữ lớn — "cái não" đằng sau các trợ lý AI) thì rất ham học cái mới, nhưng nếu mình không giúp nó **consolidate** (gộp cái trùng nhau lại, như gộp 3 tờ ghi chú nói cùng một việc thành 1 tờ), **prune** (mạnh dạn bỏ cái đã cũ, như tỉa cành khô), và **index** (xếp lại cho ngay ngắn để dễ tìm, như dán nhãn trên kệ sách) — thì knowledge base (kho kiến thức của hệ thống) cứ ngày một chậm, ngày một nhiễu, rồi trả lời sai lúc nào không hay. Kết cục quen thuộc là: Agent (trợ lý AI tự hành động) cứ lặp lại đúng một lỗi cũ, hồn nhiên đưa ra thông tin đã hết hạn, và hallucinate (tự bịa ra câu trả lời nghe có vẻ đúng nhưng thật ra sai) chỉ vì thiếu factual grounding (điểm tựa là các fact có thật trong kho) để bám vào.

> **Tóm gọn 1 câu:** Chỉ ghi thêm mà không gộp, bỏ và xếp lại thì bộ nhớ AI sẽ thành kho lộn xộn — agent trả lời sai vì kiến thức cũ và thiếu chỗ đáng tin để dựa vào.

### Tại Sao Update Memory Quan Trọng?

Phần này đưa ra 3 nghiên cứu khoa học chứng minh rằng "dọn dẹp bộ nhớ" thực sự cải thiện chất lượng AI.

#### 3 Bằng Chứng Khoa Học

> *"Bộ não to chưa chắc đã giỏi — quan trọng là mình có chịu lau chùi, sắp xếp cho gọn gàng, cập nhật thường xuyên hay không."*

Cách đọc bảng này: mỗi dòng là một nghiên cứu, cột "Phát Hiện Quan Trọng" là điều họ tìm ra — con số bôi đậm là điểm chính.

| # | Nghiên Cứu | Phát Hiện Quan Trọng |
|---|-----------|----------------------|
| 1 | **Ebbinghaus Forgetting Curve** | Without active reinforcement, **70% thông tin bị quên trong 24h**. Memory write-back giúp AI giữ knowledge fresh |
| 2 | **Google Research (2024)** | Knowledge bases được cập nhật thường xuyên giảm **45% hallucination rate** — factual grounding thay vì training data cũ |
| 3 | **Anthropic (2025)** | Effective memory consolidation giúp **3× fewer repeated mistakes** — agent remember what worked và what didn't |

#### Triết lý cốt lõi:

```
Update Memory = Learn → Consolidate → Preserve → Evolve
```

**4 chặng đường của Memory Update, kể như chuyện chăm vườn**:
- **Phase 1: Capture** — Thấy chuyện gì hay, gặp tình huống gì mới là vội ghi vào sổ tay, kẻo quên
- **Phase 2: Consolidate** — Cuối tuần ngồi lại, gộp mấy mẩu giấy trùng nhau, gạch bớt chỗ mâu thuẫn cho gọn
- **Phase 3: Prune** — Mạnh dạn tỉa cành khô, bỏ tờ giấy đã ố vàng không còn dùng được nữa
- **Phase 4: Index** — Dán nhãn, xếp sổ lên kệ ngay ngắn để bữa sau cần là thò tay lấy được ngay

**Nói cho dễ nhớ**: Update Memory cũng giống cô thủ thư tận tâm — không chỉ ôm sách mới về (Capture), mà còn chịu khó xếp lại kệ (Index), bỏ sách mục nát (Prune), và ghi lại catalog cho ngay ngắn (Consolidate). Thiếu cô thủ thư ấy, thư viện sớm muộn cũng thành nhà kho bừa bộn.

**Nếu mình lười cập nhật**: knowledge base sẽ cũ dần như tờ lịch treo tường — agent cứ dùng lịch năm ngoái để hẹn việc năm nay, trả lời sai, đưa tin cũ, rồi hallucinate vì không còn chỗ nào đáng tin để dựa vào, cuối cùng người dùng mất niềm tin và bỏ đi lúc nào không hay.

> **Tóm gọn 1 câu:** Cập nhật bộ nhớ = ghi mới (Capture) + gộp trùng (Consolidate) + bỏ cũ (Prune) + xếp gọn (Index) — thiếu bước nào bộ nhớ cũng xuống cấp.

## Tổng Quan

Phần này vẽ bức tranh tổng thể: update memory gồm những khối nào, chúng nối với nhau ra sao.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Write-back là chiều "ghi ngược" rất đời thường — nếu retrieve là thò tay lấy kiến thức ra dùng, thì write-back là cẩn thận ghi lại điều mới học được (sự kiện, fact, feedback) vào memory store, rồi mới tính tới consolidation với làm báo cáo.
> 
> **Ẩn dụ/so sánh:** Như cô thủ thư dễ thương — retrieve là ra kệ lấy sách cho bạn mượn, còn write-back là ngồi nắn nót viết thẻ danh mục cho cuốn sách mới vừa nhập về.
> 
> **Vì sao quan trọng:** Chỉ đọc mà không chịu ghi, AI sẽ mãi dùng kiến thức cũ mèm và mỗi cuộc trò chuyện lại ngơ ngác bắt đầu lại từ số 0 như chưa từng quen nhau.

Sau khi đã retrieve và xử lý thông tin xong, việc tiếp theo rất tự nhiên là **ghi ngược trở lại** vào memory store. Người ta gọi bước này là **write-back** — viết thêm kiến thức mới vào knowledge base, dọn dẹp lại memory systems, rồi làm báo cáo cho gọn.

```
┌──────────────────────────────────────────────────────────────────┐
│                UPDATE MEMORY & KNOWLEDGE STORE                    │
│                                                                  │
│  Retrieve (Read)                 Update (Write)                  │
│  ┌──────────────┐               ┌──────────────────────┐        │
│  │  Vector DB   │◄──────────────│  Write-back Engine   │        │
│  │  Knowledge   │               │  ────────────────────│        │
│  │  Graph       │──────────────►│  - Memory Writer     │        │
│  │  Files/DB    │               │  - Consolidation     │        │
│  └──────────────┘               │  - Report Generator  │        │
│                                 │  - KB Maintenance    │        │
│                                 └──────────────────────┘        │
│                                                                  │
│  Operations:                                                     │
│  ├── Write-back Memory (ghi sự kiện mới)                       │
│  ├── Consolidation (merge facts cũ + mới)                      │
│  ├── Report Generation (tạo output có cấu trúc)               │
│  └── KB Maintenance (thêm/sửa/xóa knowledge)                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Cách đọc sơ đồ: bên trái là kho biết đọc (Vector DB, Knowledge Graph, Files/DB), bên phải là "bộ máy ghi" gồm 4 công việc — ghi sự kiện mới, gộp fact cũ+mới, tạo báo cáo, và thêm/sửa/xóa kiến thức. Mũi tên cho thấy ghi và đọc là hai chiều đi lại giữa kho và bộ máy này.

> **Tóm gọn 1 câu:** Tổng quan này nói về chiều "ghi ngược" (write-back) — sau khi tra cứu và xử lý xong, hệ thống phải ghi lại điều mới học được vào kho, dọn kho, rồi làm báo cáo.

## Tại Sao Update Memory & Knowledge Store Quan Trọng?

Phần này giải thích tại sao việc cập nhật bộ nhớ quan trọng hơn cả việc bộ nhớ "to", bằng chuyện bếp núc, bằng số liệu, và bằng chi phí nếu bỏ qua.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Update memory đơn giản là việc "làm mới" bộ não của AI — thấy sự kiện mới thì ghi vào, thấy kiến thức trùng nhau thì gộp lại (consolidation), thấy cái nào hết hạn thì tiễn đi, để lúc nào kiến thức cũng đúng với hiện tại.
> 
> **Ẩn dụ/so sánh:** Như cuốn hồ sơ bệnh án ở trạm xá — bác sĩ không chỉ giở hồ sơ cũ ra đọc, mà mỗi lần có kết quả xét nghiệm mới là phải kẹp thêm vào, nếu không lần sau khám sẽ chẩn đoán lệch.
> 
> **Vì sao quan trọng:** Bộ nhớ mà để mốc meo không dọn, AI sẽ hồn nhiên trả lời bằng kiến thức cũ, ngã đúng cái hố đã ngã hôm qua, rồi dần dần người dùng chẳng còn muốn tin nữa.

> *"Bộ não con người không chỉ là cái kho để nhét đồ – nó suốt ngày tự sắp xếp, nối cái này với cái kia, làm mới liên tục. Memory system của AI cũng phải sống như vậy."*

### Triết Lý Cốt Lõi

Hãy rủ nhau ra phòng khám quen đầu ngõ chơi. Bác sĩ ở đó nhớ vanh vách bệnh án của cả nhà bạn. Nhưng thử nghĩ xem, nếu bác chỉ chăm chăm **đọc** tờ giấy cũ mà không bao giờ **ghi thêm** kết quả xét nghiệm mới vào, thì chỉ một năm sau, xấp hồ sơ đó còn dùng được gì nữa đâu. **Chỉ retrieve mà không write-back thì chưa đủ để tạo ra giá trị thật.**

Ba ý cốt lõi cứ nhớ như nhớ lời dặn của mẹ:

1. **Memory là một khu vườn sống, chứ không phải cái kho khóa cửa để đấy**: thông tin cũ cũng như lá úa — phải cập nhật, gộp lại, có khi phải tỉa bỏ. Bộ não mình còn tự quên bớt chuyện không còn relevance nữa là.
2. **Mỗi lần trò chuyện là một lần học nghề**: mỗi conversation, mỗi lời feedback, mỗi quyết định đều rơi rớt ra chút kiến thức mới. Không nhặt lên ghi lại là mình đang để tiền rơi ngoài chợ.
3. **Gộp gọn ăn đứt ôm đồm**: cứ thấy gì cũng nhét vào thì chỉ tạo ra **noise** ồn ào (nhiễu — thông tin rác khiến bạn khó tìm cái đúng). Chịu khó consolidation — ngồi lại merge (gộp), dedupe (loại trùng lặp), update (cập nhật) — mới chắt được **signal** trong veo (signal = tín hiệu quý, phần thông tin thật sự đúng và đáng dùng).

> **Tóm gọn 1 câu:** Memory là khu vườn sống cần chăm — mỗi lần trò chuyện đều cho kiến thức mới, và gộp gọn luôn tốt hơn ôm đồm.

### Bằng Chứng Nghiên Cûu

#### Google Research (2024): "Memory-Enhanced Agents"
> Mấy bạn agent có chịu khó write-back thì làm multi-turn task ngon hơn hẳn **37%** so với mấy bạn chỉ biết retrieve chay.

Nói dễ hiểu là: bạn agent không ghi lại chuyện mấy turn trước nên cứ hỏi đi hỏi lại người ta, vừa mất thời gian vừa làm người dùng cụt hứng.

#### Anthropic (2025): Claude Code Memory Architecture
Claude Code chơi kiểu **memory 3 tầng** rất ra dáng người lớn:
- **Session Memory** (ngắn hạn như trí nhớ hôm nay): ghi lại facts lượm được trong session hiện tại
- **Project Memory** (sổ tay dự án): chịu khó write-back vào mấy file CLAUDE.md để bữa sau mở ra vẫn còn
- **Global Memory** (vốn sống mang theo): kiến thức xài chung được cho nhiều projects khác nhau

Nhờ vậy mà bớt được **68% câu hỏi lặp lại** qua các sessions — đỡ quê cho cả hai bên.

#### IBM Enterprise AI Research (2025)
> Ở mấy công ty mà không chịu làm memory consolidation, nhân viên mất **gấp 2.3 lần thời gian** cho mấy việc lặp đi lặp lại, chỉ vì con AI cứ như tấm chiếu mới, lần nào cũng phải "học lại từ đầu".

> **Tóm gọn 1 câu:** Số liệu từ Google, Anthropic và IBM cùng chỉ về một điểm: có ghi lại và dọn dẹp bộ nhớ thì agent ít hỏi lại, ít sai, và làm việc nhanh hơn hẳn.

### Cost-Benefit Analysis

Phần này tính bài toán "có đáng công không" khi làm write-back.

Cách đọc bảng này: mỗi dòng là một khía cạnh chi phí/giá trị; cột giữa là hậu quả khi KHÔNG có write-back, cột phải là kết quả khi CÓ write-back kèm consolidation. Ví dụ dòng "Duplicate Work": không ghi lại thì agent làm lại việc cũ, có ghi lại thì nó biết mình đã làm gì.

| Chi Phí / Giá Trị | Không Có Write-back | Có Write-back + Consolidation |
|---|---|---|
| **Duplicate Work** | Agent lặp lại việc đã làm | Agent biết đã làm gì, tiếp tục từ đó |
| **Knowledge Drift** | Facts cũ vẫn tồn tại → sai lệch | Auto-update: facts mới thay thế facts cũ |
| **Storage Cost** | Liên tục tăng, không kiểm soát | Giảm 40-60% qua consolidation |
| **Response Quality** | Giảm dần theo thời gian | Cải thiện liên tục qua feedback loop |
| **User Trust** | Giảm vì phải lặp lại thông tin | Tăng vì agent "nhớ" context |

**Kể chuyện tiền nong cho dễ hình dung**: mỗi tháng bỏ ra $500 nuôi memory infrastructure cho tử tế (hạ tầng lưu bộ nhớ — server, database dùng để ghi/đọc memory), thì tiết kiệm được cỡ $2,000 tiền chạy agent lòng vòng (vì bớt được 75% câu hỏi trùng lặp). Đầu tư một, lời ba — ai mà chê.

> **Tóm gọn 1 câu:** Bảng này trả lời "có đáng không": bỏ ra $500/tháng cho hạ tầng bộ nhớ đổi lại $2,000 tiết kiệm và chất lượng trả lời tăng dần theo thời gian.

### Analogies Minh Họa

Phần này kể 3 chuyện đời thường để bạn hình dung write-back, consolidation và event sourcing mà không cần code.

**Chuyện 1: Bác Sĩ Và Cuốn Hồ Sơ Bệnh Án**
- **Retrieval** = Bác sĩ lật cuốn hồ sơ ra đọc lại
- **Write-back** = Bác kẹp thêm tờ kết quả xét nghiệm mới vào
- **Consolidation** = Bác ngồi tổng hợp hết đống giấy tờ, chốt lại chẩn đoán mới nhất
- **Nếu quên write-back** = Bác kê đơn theo giấy cũ, bệnh nhân uống thuốc trật lất vì thiếu kết quả mới nhất

**Chuyện 2: Cô Thủ Thư Và Kệ Sách**
- **Retrieval** = Ra kệ tìm đúng cuốn mình cần
- **Write-back** = Nhập sách mới về, viết thêm thẻ catalog
- **Consolidation** = Cuối tháng xếp lại kệ, bỏ sách mọt ăn, gộp mấy bản in trùng nhau
- **Nếu lười consolidation** = Thư viện toàn sách trùng, tìm một cuốn mà phải lật tung 5 bản giống nhau

**Chuyện 3: Dân Code Với Git Quen Thuộc**
- **Write-back** = Vừa code xong là commit ngay cho nóng (commit = lưu một "chụp ảnh" thay đổi vào lịch sử Git)
- **Consolidation** = Ngồi merge branches, gỡ rối conflicts (merge = gộp 2 nhánh làm việc riêng thành một; conflict = hai chỗ sửa cùng một dòng phải chọn 1)
- **Event Sourcing** = Cuốn sổ Git log — thích là time-travel về bất kỳ commit nào trong quá khứ
- **Nếu không consolidation** = Hàng trăm branches chĩa ra tứ phía, không ai dám merge vì sợ toang

> **Tóm gọn 1 câu:** Ba câu chuyện một ý: chỉ "đọc" mà không "ghi lại + dọn dẹp" thì cả bác sĩ, thủ thư lẫn dân code đều vấp chính thông tin cũ của mình.

### Evolutionary Context: Từ Simple Storage đến Intelligent Memory

Phần này kể lịch sử 4 thời kỳ của memory system, để bạn thấy vấn đề mỗi thời kỳ và vì sao các giải pháp mới ra đời.

```
┌──────────────────────────────────────────────────────────────────┐
│                  EVOLUTION OF MEMORY SYSTEMS                      │
│                                                                  │
│  2020-2022: Simple Key-Value Storage                            │
│  └── Memory = cache {key: value}                                 │
│      Vấn đề: Không semantic, không temporal                      │
│                                                                  │
│  2022-2023: Vector Store (Embedding-based)                      │
│  └── Memory = vector DB with semantic search                    │
│      Vấn đề: Không có consolidation, không có conflict resolve   │
│                                                                  │
│  2024-2025: Structured Memory Systems                           │
│  └── Memory = Knowledge Graph + Vector + Episodic               │
│      Vấn đề: Manual consolidation, không auto-update            │
│                                                                  │
│  2026+: Intelligent Adaptive Memory                             │
│  └── Memory = Auto-consolidation + Conflict Resolution         │
│      + Temporal Awareness + Cross-session Learning              │
│      Giải pháp: Memory tự tổ chức, tự làm mới, tự cleanup      │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Điều rút ra rất đời**: "Chỗ để đồ thì rẻ, cái đắt là công ngồi sắp xếp cho gọn." Một cái vector store (kho lưu text dạng vector số để tìm kiếm theo nghĩa, không cần khớp từng chữ) ôm 10,000 documents mà không bao giờ consolidation thì thua xa một knowledge graph (kho lưu fact dưới dạng "A liên quan B", như sơ đồ tư duy) chỉ 100 facts nhưng được chăm chút gọn gàng.

> **Tóm gọn 1 câu:** Memory system đã tiến từ "kho key-value ngu" đến "bộ nhớ tự dọn, tự làm mới" — bài học: chất lượng sắp xếp quan trọng hơn số lượng lưu trữ.

### Nếu Bạn Kệ Luôn, Không Thèm Update Memory...

Phần này liệt kê 5 hậu quả cụ thể khi bỏ bê việc cập nhật bộ nhớ — mỗi cái có ví dụ thực tế.

**1. Kiến thức mốc meo (Knowledge Staleness)**
- Facts cũ không ai buồn update → Agent hồn nhiên trả lời bằng tin hết hạn
- Kiểu như: luật thuế 2025 đổi rồi mà memory vẫn khư khư giữ luật 2024

**2. Kho phình to vô tội vạ (Memory Explosion)**
- Cứ thêm mà chẳng bao giờ gộp hay xóa → Storage phình như bong bóng
- Vector search ngày càng ì ạch → Performance rớt 30-50% chỉ sau 6 tháng

**3. Ông nói gà, bà nói vịt (Contradiction Accumulation)**
- Mấy facts đá nhau cứ nằm đó không ai xử → Agent trả lời bữa này đá bữa kia
- Ví dụ dở khóc dở cười: "BHYT đóng 4.5%" và "BHYT đóng 5%" cùng tồn tại song song

**4. Ngã mãi một cái hố (Zero Learning)**
- Agent không ghi lại feedback → Sai ở đâu, bữa sau sai đúng chỗ đó
- Người dùng chán vì session nào cũng phải cầm tay chỉ lại từ đầu

**5. Gặp nhau như người xa lạ (Lost Context Between Sessions)**
- Session mới mở ra trắng trơn như chưa từng quen → Người dùng tủi thân vì phải kể lại từ đầu
- Không có session handoff (bàn giao ngữ cảnh từ phiên cũ sang phiên mới), đồng đội vào sau cũng mù mờ chẳng biết chuyện gì đã xảy ra

> **Tóm gọn 1 câu:** Bỏ bê update memory dẫn tới 5 cái giá: tin cũ, kho phình, fact đá nhau, không học được từ lỗi, và quên sạch context giữa các phiên.

### Best Practices (Và Tại Sao)

Phần này là 6 quy tắc "nên làm" — kèm lý do để bạn hiểu chứ không cần học vẹt.

Cách đọc bảng này: cột "Rule" là quy tắc, cột "Why" là lý do nên làm. Ví dụ dòng đầu: luôn ghi timestamp (dấu thời gian — ghi lại fact này được tạo lúc nào) để khi 2 fact mâu thuẫn, hệ thống biết cái nào mới hơn.

| Rule | Why |
|---|---|
| Luôn ghi timestamp cho mọi fact | Để biết fact nào mới nhất khi có conflict |
| Consolidate định kỳ (không phải real-time) | Real-time consolidation quá tốn compute; batch processing (xử lý theo đợt, ví dụ mỗi giờ một lần) hiệu quả hơn 5x |
| Luôn log mọi write operation (audit trail) | Để debug khi memory bị corruption (hỏng dữ liệu); để rollback (quay lại trạng thái cũ) nếu cần |
| Version facts (với source và confidence) | Để resolve conflict: fact từ source nào đáng tin hơn (confidence = điểm tự tin 0-100% cho một fact) |
| Auto-expire outdated facts | Facts 6 tháng tuổi có 73% chance là đã lỗi thời (research data) |
| Tách Episodic vs Semantic memory | Episodic = "điều gì đã xảy ra", Semantic = "sự thật là gì" — 2 loại memory cần xử lý khác nhau |

> **Tóm gọn 1 câu:** Ghi dấu thời gian, gộp theo đợt, log mọi lần ghi, đánh version cho fact, tự hết hạn tin cũ, tách hai loại nhớ — sáu quy tắc này là nền của mọi memory system tốt.

---

## Nội Dung

Phần này là mục lục tóm tắt của 5 chủ đề chính phía dưới.

Cách đọc bảng này: mỗi dòng là một chủ đề; bấm vào tên chủ đề để nhảy tới phần đó. Ví dụ dòng 1 là "Write-back Memory" — cách ghi sự kiện mới vào bộ nhớ.

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Write-back Memory](#1-write-back-memory) | Ghi sự kiện mới vào memory systems |
| 2 | [Memory Consolidation](#2-memory-consolidation) | Tổng hợp & merge thông tin |
| 3 | [Report Generation](#3-report-generation) | Tạo output có cấu trúc |
| 4 | [KB Maintenance](#4-kb-maintenance) | Thêm/sửa/xóa knowledge base |
| 5 | [Event Sourcing Pattern](#5-event-sourcing-pattern) | Lưu trữ dạng event log |

> **Tóm gọn 1 câu:** Phần nội dung chính gồm 5 chủ đề nối tiếp nhau: ghi mới → gộp dọn → làm báo cáo → bảo trì kho → lưu lịch sử sự kiện.

---

## 1. Write-back Memory

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Write-back Memory là bước ghi lại những gì hệ thống vừa học được — sự kiện (episodic), fact (semantic), feedback — vào memory store sau khi xử lý cuộc trò chuyện.
> 
> **Ẩn dụ/so sánh:** Giống việc ghi chú ngay sau cuộc họp — nếu không ghi, vài giờ sau bạn quên gần hết nội dung.
> 
> **Vì sao quan trọng:** Nếu chỉ retrieve mà không write-back, AI không bao giờ "khôn hơn" qua mỗi lần trò chuyện và luôn lặp lại câu hỏi cũ.

### 1.1 Khi Nào Cần Write-back?

Phần này trả lời câu hỏi "tin gì thì đáng ghi lại?" qua 3 kịch bản.

Không phải cứ có tin mới là ghi — hãy write-back khi nó **thay đổi trạng thái** của user, của hệ thống, hoặc tạo ra bài học. Ba tình huống dưới đây nên đọc như ba kịch bản: dòng đầu là điều xảy ra trong cuộc trò chuyện, các dòng `→` là những việc hệ thống cần làm theo.

```
┌──────────────────────────────────────────────────────────────────┐
│                   WRITE-BACK SCENARIOS                            │
│                                                                  │
│  Scenario 1: User learns something new                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ User: "Tôi vừa chuyển sang làm freelancer"              │   │
│  │ → Store: user.occupation = "freelancer"                  │   │
│  │ → Update: Conversation context                          │   │
│  │ → Trigger: Re-classify user needs                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Scenario 2: System discovers new knowledge                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ RAG found: "Luật BHYT mới 2025: Mức đóng tăng 5%"    │   │
│  │ → Update: Knowledge base with new regulation            │   │
│  │ → Invalidate: Cached old BHYT info                      │   │
│  │ → Notify: Users affected by change                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Scenario 3: Feedback loop                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ User: "Câu trả lời trước sai rồi!"                     │   │
│  │ → Store: feedback (query, wrong_answer, correct_answer) │   │
│  │ → Update: Retriever weights                             │   │
│  │ → Improve: Future responses                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Giải thích nhanh 3 kịch bản: (1) user nói tin cá nhân mới ("tôi chuyển làm freelancer") thì lưu vào hồ sơ user; (2) hệ thống tìm ra kiến thức mới (luật BHYT mới) thì cập nhật kho và vô hiệu hóa bản tin cũ đã cache (cache = bản lưu tạm để trả lời nhanh); (3) user chê câu trả lời sai thì lưu lại cặp "sai → đúng" để lần sau trả lời tốt hơn.

> **Tóm gọn 1 câu:** Chỉ write-back khi tin mới làm thay đổi hồ sơ user, kiến thức của hệ thống, hoặc là feedback có bài học — mỗi lần ghi kèm việc cập nhật những chỗ liên quan.

### 1.2 Write-back Implementation

Phần này giới thiệu class Python làm nhiệm vụ ghi, để bạn biết "cây bút" của hệ thống gồm những cây bút con nào.

Lớp `MemoryWriter` bên dưới là "cây bút" của hệ thống: `write_episodic` ghi sự kiện (episodic memory = loại nhớ "chuyện gì đã xảy ra", như nhật ký), `write_fact` ghi fact (semantic memory = loại nhớ "sự thật là gì", như sách giáo khoa), `update_fact` sửa fact, `write_user_profile` cập nhật thông tin user. Không cần hiểu từng dòng — chỉ cần để ý điểm chung: **hàm nào cũng ghi vào `event_log`** (sổ nhật ký ghi lại mọi lần ghi) để sau này truy vết được ai đã ghi gì, lúc nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/01-1-2-write-back-implementation.py`](examples/01-1-2-write-back-implementation.py)

</details>

> **Tóm gọn 1 câu:** `MemoryWriter` ghi 4 loại dữ liệu (sự kiện, fact, sửa fact, hồ sơ user) và mọi lần ghi đều được ghi log vào `event_log` để truy vết về sau.

---

## 2. Memory Consolidation

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Consolidation là quá trình "dọn dẹp kho" — gộp các fact trùng lặp, thay fact cũ bằng fact mới, và giải quyết các fact mâu thuẫn để kiến thức gọn gàng và chính xác.
> 
> **Ẩn dụ/so sánh:** Giống dọn tủ quần áo định kỳ — cất bớt áo trùng, bỏ áo rách, sắp lại gọn gàng để lần sau tìm nhanh.
> 
> **Vì sao quan trọng:** Kiến thức tích lũy không kiểm soát tạo ra nhiễu (noise), khiến retrieval chậm và dễ trả lời sai.

### 2.1 Consolidation Là Gì?

Phần này so sánh kho nhớ trước và sau khi dọn, để bạn thấy consolidation "làm ra cái gì".

Khối ASCII dưới đây so sánh memory **TRƯỚC** và **SAU** khi consolidation. Phần trên là 5 fact rời rạc về BHYT (Bảo hiểm y tế; trùng lặp, cũ mới lẫn lộn); phần dưới là kết quả sau khi dọn — chỉ còn 2 fact rõ ràng. Ý tưởng cốt lõi nằm ở dòng cuối: **Consolidation = Merge (gộp) + Dedupe (loại trùng) + Update (cập nhật) + Summarize (tóm tắt)**.

```
┌──────────────────────────────────────────────────────────────────┐
│                  MEMORY CONSOLIDATION                              │
│                                                                  │
│  Trước consolidation:                                           │
│  ├── Fact: "BHYT đóng 4.5%" (ngày 1, source A)               │
│  ├── Fact: "BHYT đóng 4.5% lương cơ sở" (ngày 2, source B)  │
│  ├── Fact: "Mức đóng BHYT 2024 là 4.5%" (ngày 3, source C)  │
│  ├── Fact: "BHYT đóng 4.5%" (ngày 5, source A - duplicate!) │
│  └── Fact: "BHYT đóng 5% từ 2025" (ngày 10, source D)       │
│                                                                  │
│  Sau consolidation:                                              │
│  ├── Fact: "BHYT đóng 4.5% (2024)" — merged 3 facts         │
│  ├── Fact: "BHYT đóng 5% (từ 2025)" — latest update          │
│  └── Deleted: duplicate "BHYT đóng 4.5%"                       │
│                                                                  │
│  Consolidation = Merge + Dedupe + Update + Summarize           │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Ví dụ cụ thể: 3 fact "BHYT đóng 4.5%" (ngày 1, 2, 3 từ 3 nguồn) được gộp thành 1 fact kèm năm 2024; bản "đóng 5% từ 2025" là tin mới nên giữ nguyên; bản trùng ngày 5 bị xóa.

### 2.2 Implementation

Phần này giới thiệu class Python thực hiện 4 bước dọn dẹp.

Class `MemoryConsolidator` thực hiện 4 bước dọn dẹp: gộp fact giống nhau (`consolidate_facts`), loại fact quá cũ (`temporal_consolidation` — temporal = theo thời gian), tóm tắt thông tin về một entity (entity = đối tượng được nhắc tới, như "BHYT" hay "user An"), và phát hiện fact mâu thuẫn (`conflict_resolution`). Mỗi hàm trả về các con số thống kê (merged/deleted/removed) — bạn chỉ cần đọc kết quả trả về để biết đã dọn được những gì.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/02-2-2-implementation.py`](examples/02-2-2-implementation.py)

</details>

> **Tóm gọn 1 câu:** Consolidation = dọn kho theo 4 bước (gộp trùng, bỏ cũ, tóm tắt theo đối tượng, xử lý mâu thuẫn); class `MemoryConsolidator` làm hộ bạn cả 4 và báo lại số liệu.

---

## 3. Report Generation

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Report Generation là tạo ra các báo cáo có cấu trúc — tóm tắt cuộc trò chuyện, tổng quan knowledge base, phân tích nhiều nguồn — từ dữ liệu hội thoại và memory store.
> 
> **Ẩn dụ/so sánh:** Giống trợ lý viết biên bản cuộc họp — biến lời nói rời rạc thành văn bản ngắn gọn, có mục rõ ràng để ai đọc cũng hiểu.
> 
> **Vì sao quan trọng:** Báo cáo là "cầu nối" chuyển thông tin thô thành kiến thức tái sử dụng được cho session sau hoặc cho cả đội.

### 3.1 Report Types

Phần này liệt kê 4 loại báo cáo hệ thống có thể tạo, để bạn chọn đúng loại cho đúng nhu cầu.

4 loại báo cáo cơ bản mà hệ thống có thể tạo ra. Đọc mỗi khối theo 3 dòng: **Input** (lấy dữ liệu gì) → **Output** (tạo ra gì) → **Use** (dùng để làm gì). Ví dụ "Conversation Summary" lấy chat history để tạo bản tóm tắt bàn giao cho phiên làm việc kế tiếp (session handoff = bàn giao ngữ cảnh giữa hai phiên).

```
┌──────────────────────────────────────────────────────────────────┐
│                    REPORT TYPES                                   │
│                                                                  │
│  1. CONVERSATION SUMMARY                                        │
│     Input: Chat history                                         │
│     Output: Structured summary                                  │
│     Use: Session handoff, memory storage                        │
│                                                                  │
│  2. KNOWLEDGE REPORT                                             │
│     Input: Knowledge graph + facts                              │
│     Output: Organized knowledge overview                        │
│     Use: KB maintenance, debugging                              │
│                                                                  │
│  3. ANALYSIS REPORT                                              │
│     Input: Multiple sources + retrieved context                 │
│     Output: Analysis with citations                             │
│     Use: Decision support, research                             │
│                                                                  │
│  4. FEEDBACK REPORT                                              │
│     Input: User feedback + ratings                              │
│     Output: Improvement recommendations                         │
│     Use: System improvement                                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Diễn giải 4 loại bằng một câu mỗi loại: (1) Tóm tắt hội thoại — để phiên sau đọc vào là biết chuyện; (2) Knowledge report — nhìn tổng quan kho kiến thức để bảo trì; (3) Analysis report — phân tích nhiều nguồn kèm citations (trích dẫn nguồn) để phục vụ ra quyết định; (4) Feedback report — gom ý kiến người dùng thành gợi ý cải thiện.

> **Tóm gọn 1 câu:** Có 4 loại báo cáo (tóm tắt hội thoại, tổng quan kiến thức, phân tích, feedback) — mỗi loại lấy một nguồn dữ liệu đầu vào để phục vụ một mục đích khác nhau.

### 3.2 Implementation

Phần này giới thiệu class Python tạo báo cáo bằng LLM.

Class `ReportGenerator` hiện thực 3 loại báo cáo: `conversation_summary` (tóm tắt hội thoại), `knowledge_report` (tổng quan knowledge base) và `analysis_report` (phân tích nhiều nguồn kèm citations). Các hàm này gọi LLM để viết báo cáo rồi ép kết quả về JSON (định dạng dữ liệu dạng `{khóa: giá trị}`, máy đọc được) — nếu LLM trả sai định dạng, code có nhánh fallback (kế hoạch dự phòng) trả về dữ liệu mặc định thay vì gây lỗi.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/03-3-2-implementation.py`](examples/03-3-2-implementation.py)

</details>

> **Tóm gọn 1 câu:** `ReportGenerator` nhờ LLM viết 3 loại báo cáo rồi ép về JSON; nếu LLM trả sai định dạng, code dùng nhánh dự phòng thay vì crash.

---

## 4. KB Maintenance

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** KB (Knowledge Base) Maintenance là các thao tác quản lý "kho kiến thức": thêm kiến thức mới, sửa kiến thức sai, xóa kiến thức lỗi thời, và kiểm tra chất lượng kho.
> 
> **Ẩn dụ/so sánh:** Giống bảo trì thư viện — mua sách mới, in lại trang sai, gỡ sách hỏng, và rà soát danh mục định kỳ.
> 
> **Vì sao quan trọng:** Knowledge base không được bảo trì sẽ dần chứa thông tin sai và trùng lặp, kéo theo toàn bộ hệ thống trả lời kém tin cậy.

### 4.1 Knowledge Base Operations

Phần này giới thiệu class Python "quản lý kho kiến thức" với 4 thao tác.

Class `KBMaintainer` là "người quản lý kho kiến thức" với 4 thao tác chính: `add_knowledge` (thêm), `update_knowledge` (sửa), `delete_knowledge` (xóa theo chủ đề hoặc chi tiết), và `validate_knowledge` (rà soát tìm fact mâu thuẫn, entity bị mồ côi — entity mồ côi là đối tượng còn nằm trong kho nhưng không còn nối với fact nào, như cuốn sách không ai mượn và không ai nhắc tới). Điểm đáng chú ý: mọi thao tác đều ghi vào `changelog` (sổ nhật ký thay đổi — giống lịch sử Git) để biết đã đụng vào kiến thức nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/04-4-1-knowledge-base-operations.py`](examples/04-4-1-knowledge-base-operations.py)

</details>

> **Tóm gọn 1 câu:** `KBMaintainer` cho thêm/sửa/xóa/rà soát kho kiến thức, và mọi thao tác đều ghi vào `changelog` để luôn biết ai đã đụng vào đâu.

---

## 5. Event Sourcing Pattern

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Event Sourcing là cách lưu trữ "mọi thứ đã xảy ra" — thay vì chỉ ghi trạng thái hiện tại, ta lưu toàn bộ danh sách sự kiện; còn trạng thái hiện tại thì "phát lại" (replay) từ các sự kiện đó.
> 
> **Ẩn dụ/so sánh:** Giống camera hành trình của một chuyến xe — bạn nhớ từng khúc đường đã qua nên có thể tua lại, hoặc rẽ branch ở bất kỳ điểm nào, chứ không chỉ biết mỗi đích đến.
> 
> **Vì sao quan trọng:** Có đủ lịch sử bạn mới có audit trail, có rollback, và truy vết chính xác lỗi xảy ra từ đâu.

### 5.1 Concept

Phần này giới thiệu ý tưởng gốc của event sourcing qua một khối sơ đồ.

Khối ASCII cho thấy cách lưu theo "nhật ký sự kiện" — mỗi dòng là một sự kiện có đánh dấu thời gian (`@ t=...`). Ba siêu năng lực nằm ở giữa khối: **Current State = Replay all events** (trạng thái hiện tại được dựng lại bằng cách phát lại mọi sự kiện), **Time Travel** (phát lại tới thời điểm T), và **Audit Trail** (giữ đầy đủ lịch sử thay đổi).

```
┌──────────────────────────────────────────────────────────────────┐
│                EVENT SOURCING FOR MEMORY                          │
│                                                                  │
│  Thay vì chỉ lưu state hiện tại, lưu TẤT CẢ events:           │
│                                                                  │
│  Events Log:                                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ 1. [ADD]     BHYT → mức đóng → 4.5%          @ t=0     │   │
│  │ 2. [ADD]     BHYT → thời hạn → 5 năm         @ t=1     │   │
│  │ 3. [UPDATE]  BHYT → mức đóng → 5% (from 4.5%) @ t=2   │   │
│  │ 4. [FEEDBACK] Query="BHYT đóng?" → rating=4  @ t=3     │   │
│  │ 5. [ADD]     BHYT → áp dụng từ → 01/2025     @ t=4     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Current State = Replay all events                              │
│  Time Travel = Replay up to time T                              │
│  Audit Trail = Full history of all changes                      │
│                                                                  │
│  Advantages:                                                    │
│  ├── Complete audit trail                                      │
│  ├── Can undo/rollback                                         │
│  ├── Can analyze changes over time                             │
│  └── Debugging: trace exactly what happened                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Cách đọc khối: phần "Events Log" là cuốn sổ sự kiện — ví dụ dòng 3 nghĩa là "ở thời điểm t=2, fact mức đóng BHYT được sửa từ 4.5% lên 5%". Ba dòng "Current State / Time Travel / Audit Trail" là 3 thứ bạn làm được nhờ cuốn sổ đó: dựng lại hiện tại, quay về quá khứ, và soát lịch sử.

> **Tóm gọn 1 câu:** Event sourcing = thay vì chỉ lưu trạng thái hiện tại, lưu mọi sự kiện đã xảy ra — nhờ đó được 3 siêu năng lực: dựng lại hiện tại, quay về quá khứ, và soát đầy đủ lịch sử.

### 5.2 Implementation

Phần này hiện thực ý tưởng trên bằng class Python `EventSourcedMemory`.

Class `EventSourcedMemory` hiện thực ý tưởng trên bằng code. Hãy chú ý `record_event` — mọi thay đổi đều đi qua hàm này, được lưu vào danh sách `events`, rồi cập nhật `state` bằng `_apply_event`. Hai hàm thú vị nhất: `get_state_at(event_id)` cho phép "time travel" về trạng thái tại một sự kiện nào đó, và `undo_last()` hủy sự kiện cuối bằng cách dựng lại toàn bộ state từ đầu (undo = hoàn tác, trả về như trước khi sự kiện đó xảy ra).

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/05-5-2-implementation.py`](examples/05-5-2-implementation.py)

</details>

> **Tóm gọn 1 câu:** `EventSourcedMemory` đưa mọi thay đổi qua `record_event` vào sổ sự kiện; muốn xem quá khứ dùng `get_state_at`, muốn hoàn tác dùng `undo_last`.

---

## 6. Memory Store Case Studies

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Đây là tuyển tập các case study từ sản phẩm thực tế — Claude Code, Mem0, OpenMemory, DeepSeek Harness — để xem các đội ngũ production giải quyết write-back và memory consolidation như thế nào.
> 
> **Ẩn dụ/so sánh:** Giống đọc review nhà hàng trước khi mở quán riêng — học từ người đi trước để tránh những sai lầm tốn kém.
> 
> **Vì sao quan trọng:** Lý thuyết dễ nói, khó làm; case study cho bạn biết pattern nào thực sự hoạt động khi chạy ở quy mô thật.

Các case studies dưới đây giống như mình đi thăm nhà mấy anh chị đã làm production thật — xem họ xoay xở với write-back và memory consolidation ra sao, để mình khỏi phải tự vấp lại đúng cục đá đó.

---

### 6.1. Claude Code — Session Memory & Cross-Session Persistence

Phần này kể cách Anthropic giải quyết bài toán "AI quên bài" trong công cụ Claude Code.

**Chuyện nhà Claude Code**: team Anthropic đau đầu vì Claude hay "quên bài" qua mỗi session mới (session = một phiên làm việc từ lúc mở đến lúc đóng), không nhớ project đang làm dở kiểu gì. Thế là họ đẻ ra cách nhớ 3 tầng để đi đâu cũng mang theo được.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/06-6-1-claude-code-session-memory-cross-session.ts`](examples/06-6-1-claude-code-session-memory-cross-session.ts)

</details>

**Mấy điểm hay ho rút ra**:
1. ✅ **Nhớ 3 tầng** — Session (nhớ tạm trong buổi) → Project (ghi vào CLAUDE.md để hôm sau còn) → Global (mang theo qua project khác)
2. ✅ **Biến lời chê thành của để dành** — User sửa chỗ nào là ghi ngay thành pitfalls trong CLAUDE.md, lần sau khỏi sai lại
3. ✅ **Biết người biết ta** — Đoán trình độ user để nói ngắn gọn hay giải thích kỹ
4. ✅ **Dọn dẹp cuối buổi** — Hết session là chắt lọc cái hay giữ lại, cái vụn thì cho qua

> **Tóm gọn 1 câu:** Claude Code nhớ theo 3 tầng (trong buổi → trong project qua file CLAUDE.md → dùng chung nhiều project), biến mỗi lần bị sửa thành bài học cho lần sau.

---

### 6.2. Mem0 — Production Memory Layer for AI Agents

Phần này kể cách Mem0 làm "thư ký ghi chép hộ" cho AI agent.

**Mem0** (trước đây mọi người biết với tên EmbedChain) là một memory layer (tầng nhớ — dịch vụ chuyên quản lý bộ nhớ cho agent) open-source (mã nguồn mở — ai cũng tải về, sửa và dùng được) cho AI agents, kiểu như có một bạn thư ký cần mẫn ngồi ghi chép hộ mình:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/07-6-2-mem0-production-memory-layer-for-ai.py`](examples/07-6-2-mem0-production-memory-layer-for-ai.py)

</details>

**Mấy điểm hay ho rút ra**:
1. ✅ **Tự bóc facts** — Để LLM ngồi nghe hội thoại rồi tự nhặt ra facts, khỏi phải ghi tay
2. ✅ **Càng cũ càng mờ** — Memories cũ tự giảm độ quan trọng theo thời gian (temporal decay)
3. ✅ **Dàn xếp mâu thuẫn** — Chấm điểm theo thời gian + độ tin cậy để chọn bên đáng tin hơn
4. ✅ **Mỗi nhà một sổ riêng** — Chia namespacing theo user nên không sợ lẫn lộn (namespacing = chia vùng nhớ riêng cho từng user/project, như mỗi người một ngăn tủ)

> **Tóm gọn 1 câu:** Mem0 nhờ LLM tự bóc facts khỏi hội thoại, cho tin cũ mờ dần theo thời gian (temporal decay = tin cũ tự giảm độ tin), dàn xếp mâu thuẫn theo độ tin cậy, và chia ngăn tủ riêng cho từng user.

---

### 6.3. OpenMemory — MCP-Based Memory Server

Phần này giới thiệu một memory server mở bộ nhớ ra thành các "tool" chuẩn mà AI agent gọi được.

Case study này đóng vai một memory server theo chuẩn MCP (Model Context Protocol — giao thức mở để LLM gọi các công cụ/dịch vụ bên ngoài một cách thống nhất) — tức các thao tác bộ nhớ được "phơi ra" dưới dạng tool mà LLM có thể gọi trực tiếp: `create_memory` (tạo), `search_memory` (tìm), `update_memory` (sửa), `delete_memory` (xóa), `list_memories` (liệt kê), `consolidate_memories` (gộp dọn). Đọc giống như danh mục của một API: mỗi hàm là một thao tác chuẩn, giúp bất kỳ agent nào cũng dùng được bộ nhớ mà không cần biết cách lưu trữ bên trong.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/08-6-3-openmemory-mcp-based-memory-server.py`](examples/08-6-3-openmemory-mcp-based-memory-server.py)

</details>

> **Tóm gọn 1 câu:** OpenMemory biến bộ nhớ thành 6 thao tác chuẩn (tạo/tìm/sửa/xóa/liệt kê/gộp) theo chuẩn MCP — agent nào cũng dùng được mà không cần biết bên trong lưu kiểu gì.

---

### 6.4. DeepSeek Harness — Trajectory Fork & Replay Engine

**Chuyện nhà DeepSeek**: team DeepSeek quan niệm "Agent = Model + Harness", nên việc gì agent đã làm đều phải truy vết được — muốn tua lại, rẽ nhánh thử kiểu khác, hay nghỉ giữa chừng rồi chạy tiếp đều được, giống như có camera hành trình gắn cho mọi session.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

> 📄 **Code ví dụ:** [`examples/09-6-4-deepseek-harness-trajectory-fork-replay-engine.ts`](examples/09-6-4-deepseek-harness-trajectory-fork-replay-engine.ts)

</details>

**Mấy món tủ làm nên tên tuổi**:

1. ✅ **Sổ ghi chép không bao giờ tẩy xóa (Append-only Session Event Stream)** — prompt nào, suy nghĩ nào, gọi tool nào, trả lời gì đều ghi lại hết. Tuyệt đối không sửa lịch sử.
2. ✅ **`replayToStep(n)`** — Thích quay về step `n` xem lúc đó hệ thống đang nghĩ gì là được ngay. Rất hợp để debug với soi lại quá khứ.
3. ✅ **`forkSession(step, newPrompt)`** — Rẽ một nhánh mới từ step cũ để thử "giá như lúc đó mình hỏi khác đi thì sao?" mà không sợ hỏng mạch chính.
4. ✅ **`resumeSession(step)`** — Nghỉ giữa chừng rồi chạy tiếp từ checkpoint, đỡ tốn token cho mấy task dài hơi.
5. ✅ **Tìm kiếm trong hành trình (Event Search)** — Gõ từ khóa là lôi ra được *"mọi lần tool X bị fail"* hay *"mọi prompt có nhắc tới chữ Y"*.
6. ✅ **Đếm tiền từng bước (Cost Tracking)** — Mỗi event đều dán nhãn `cost_usd`, nên cuối buổi biết ngay tiền đi đâu về đâu theo từng session, từng tool, từng step.
7. ✅ **Bắt bệnh tự động (Failure Pattern Detection)** — Tự gom lại xem tool nào hay hỏng nhất, lỗi nào hay gặp nhất để còn chữa dứt điểm.

**DeepSeek Harness có 4 chế độ chạy**:

| Mode | Use Case | Tools Available |
|------|----------|-----------------|
| **Standard** | Full agent loop | All tools + trajectory tracking |
| **Code Mode** | Single-turn SDK (`@deepseek-ai/dsh`) | `bash`, `editor` only, batched |
| **Minimal Benchmark** | SWE-bench evaluation | `bash`, `editor` isolation |
| **Creator Inspector** | Visual timeline/presets | Read-only trajectory view |

**Tài liệu chi tiết**: muốn xem code chạy thật thế nào thì ghé [`trajectory-fork-replay.md`](trajectory-fork-replay.md)

Cách đọc bảng 4 chế độ: cột "Mode" là tên chế độ, "Use Case" là khi nào dùng, "Tools Available" là agent được dùng những công cụ gì trong chế độ đó. Ví dụ "Code Mode" chỉ cho 2 công cụ `bash` (chạy lệnh terminal) và `editor` (sửa file), gom nhóm để chạy nhanh.

> **Tóm gọn 1 câu:** DeepSeek Harness ghi lại toàn bộ hành trình session như camera hành trình — không sửa lịch sử, chỉ nối thêm — nhờ đó replay được từng bước, rẽ nhánh thử phương án khác, nghỉ rồi chạy tiếp, và soi ra pattern lỗi thường gặp.

---

## 7. Advanced Memory Patterns

Phần này nâng cấp từ "ghi và dọn thủ công" lên các pattern tự động, dùng được khi vào production.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Các pattern nâng cao giúp memory system chạy tốt khi vào production: write-behind cache (ghi nhanh rồi flush xuống ổ sau), consolidation pipeline (dọn dẹp tự động định kỳ), và versioned memory (nhớ theo phiên bản như Git).
> 
> **Ẩn dụ/so sánh:** Nếu các mục trước là "học viết", mục này là "học thói quen làm việc chuyên nghiệp" — có tổ chức, có lịch trình, có sao lưu.
> 
> **Vì sao quan trọng:** Khi đưa vào thực tế, ghi và dọn thủ công không đủ — cần cơ chế tự động, vừa nhanh vừa an toàn.

### 7.1. Write-Behind Cache Pattern

Pattern này trả lời câu hỏi: "ghi xuống đĩa chậm quá thì làm sao cho nhanh?". Giải pháp: ghi vào cache trong bộ nhớ tức thì (trả lời người dùng ngay), còn việc ghi xuống kho lâu bền thì chạy ngầm theo batch — ví von như ghi biên lai trước, cuối ngày mới nhập sổ cái. Nói cách khác, đây là **sự đánh đổi: chấp nhận một chút rủi ro mất dữ liệu nếu chương trình sập, để đổi lấy tốc độ phản hồi nhanh hơn rất nhiều khi lượng ghi lớn.**

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/10-7-1-write-behind-cache-pattern.py`](examples/10-7-1-write-behind-cache-pattern.py)

</details>

> **Tóm gọn 1 câu:** Write-behind cache = trả lời người dùng ngay từ cache rồi ghi xuống kho theo đợt chạy ngầm — nhanh hơn nhiều, đổi lại nếu chương trình sập giữa chừng thì có thể mất vài bản ghi chưa kịp xuống kho.

### 7.2. Memory Consolidation Pipeline

Phần này giới thiệu "dây chuyền dọn dẹp tự động" chạy định kỳ, khác với dọn thủ công ở mục 2.

Khác với consolidation thủ công ở mục 2, đây là "dây chuyền dọn dẹp tự động" chạy định kỳ theo 5 giai đoạn: deduplicate (loại trùng) → resolve conflicts (dàn xếp mâu thuẫn) → temporal decay (giảm độ tin của tin cũ) → archive memory cũ (chuyển vào kho lưu trữ) → xóa memory có confidence thấp (confidence = điểm tự tin; tin này hệ thống không chắc đúng). Mỗi giai đoạn là một hàm `_stage_*`, và `run_full_consolidation` chạy cả dây chuyền rồi trả về report thống kê — đọc báo cáo này là biết ngay mỗi giai đoạn đã dọn được bao nhiêu mục.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/11-7-2-memory-consolidation-pipeline.py`](examples/11-7-2-memory-consolidation-pipeline.py)

</details>

> **Tóm gọn 1 câu:** Consolidation pipeline = dây chuyền 5 giai đoạn (loại trùng → dàn xếp mâu thuẫn → giảm tin cũ → lưu trữ → xóa tin không chắc) chạy định kỳ tự động và báo cáo số liệu từng giai đoạn.

### 7.3. Versioned Memory (Git-like Memory)

Phần này mượn ý tưởng Git (hệ thống quản lý phiên bản code mà dân lập trình dùng hằng ngày) để làm bộ nhớ biết "quay lại được".

Pattern này mượn đúng ý tưởng Git áp dụng cho bộ nhớ: mỗi lần `set` một giá trị là tạo một **version** (phiên bản) mới kèm snapshot (ảnh chụp toàn bộ trạng thái tại một thời điểm). Nhờ đó bạn có `diff` (so sánh 2 thời điểm xem cái gì thay đổi), `rollback` (quay lại version cũ như git revert — hủy thay đổi gần nhất), và `log` (xem lịch sử thay đổi). Nói dân dã: bộ nhớ biết mình "từng được sửa thế nào", nên sửa sai là kéo lại được.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/12-7-3-versioned-memory-git-like-memory.py`](examples/12-7-3-versioned-memory-git-like-memory.py)

</details>

> **Tóm gọn 1 câu:** Versioned memory = mỗi lần ghi là một version mới có snapshot; nhờ vậy so sánh được (diff), quay lui được (rollback), và xem lịch sử được (log).

---

## 8. Best Practices & Anti-Patterns

Phần này là bảng luật "đi / dừng" khi làm update memory — gom từ kinh nghiệm production.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Danh sách các việc NÊN làm (best practices) và KHÔNG nên làm (anti-patterns) khi xây dựng update memory, gom từ kinh nghiệm của nhiều hệ thống production.
> 
> **Ẩn dụ/so sánh:** Giống bảng điều luật giao thông — không cần nhớ lý do chi tiết, chỉ cần biết "đèn xanh đi, đèn đỏ dừng" để không gặp tai nạn.
> 
> **Vì sao quan trọng:** Giúp bạn tránh những lỗi đắt giá mà nhiều đội đã vấp phải, tiết kiệm thời gian fix bug về sau.

Hai khối dưới đây nên đọc như bảng điều khiển: khối ✅ DO là 7 việc nên làm (mỗi việc kèm 2 dòng lý do), khối ❌ DON'T là 6 việc không nên làm. Ví dụ DO đầu tiên: luôn log mọi lần ghi — để có bằng chứng truy vết khi cần debug hay rollback.

```
┌──────────────────────────────────────────────────────────────────┐
│              MEMORY UPDATE DO's                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ DO: Always log write operations                              │
│     → Audit trail for debugging                                  │
│     → Event sourcing enables rollback                           │
│                                                                  │
│  ✅ DO: Deduplicate before storing                               │
│     → Check existing memories first                             │
│     → Use similarity threshold (0.85 recommended)               │
│                                                                  │
│  ✅ DO: Apply confidence scoring                                 │
│     → Not all facts are equally reliable                        │
│     → Lower confidence for indirect information                 │
│                                                                  │
│  ✅ DO: Use temporal decay                                        │
│     → Old information may be outdated                           │
│     → Exponential decay: 0.99^days                              │
│                                                                  │
│  ✅ DO: Consolidate periodically                                 │
│     → Background pipeline (hourly/daily)                        │
│     → Merge duplicates, resolve conflicts                       │
│                                                                  │
│  ✅ DO: Version important memories                               │
│     → Enable rollback if updates are wrong                      │
│     → Track how knowledge evolves                               │
│                                                                  │
│  ✅ DO: Separate namespaces per user/project                     │
│     → Prevent cross-contamination                               │
│     → Enable personalized memory                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

```
┌──────────────────────────────────────────────────────────────────┐
│              MEMORY UPDATE DON'Ts                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ❌ DON'T: Overwrite without versioning                          │
│     → Always keep previous version                              │
│     → Enable rollback capability                                │
│                                                                  │
│  ❌ DON'T: Store raw conversation as memory                      │
│     → Extract facts first                                       │
│     → Raw text wastes storage and slows retrieval               │
│                                                                  │
│  ❌ DON'T: Forget to handle conflicts                            │
│     → Same topic, different values = conflict                   │
│     → Always have a resolution strategy                         │
│                                                                  │
│  ❌ DON'T: Store everything forever                              │
│     → Archive old, unused memories                              │
│     → Remove low-confidence garbage                            │
│                                                                  │
│  ❌ DON'T: Write synchronously when write volume is high         │
│     → Use write-behind pattern                                  │
│     → Batch writes for efficiency                               │
│                                                                  │
│  ❌ DON'T: Ignore user feedback                                  │
│     → "Câu trả lời trước sai rồi" MUST update memory           │
│     → Feedback loop is critical for quality                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

> **Tóm gọn 1 câu:** Cẩm nang này tóm lại thành: log mọi lần ghi, loại trùng trước khi lưu, chấm độ tin, cho tin cũ mờ dần, dọn định kỳ, đánh version, chia vùng nhớ riêng — và ngược lại, đừng ghi đè thiếu version, đừng lưu hội thoại thô, đừng bỏ qua feedback.

---

## 9. Performance Metrics

Phần này nói về cách "bắt mạch" cho memory system bằng các chỉ số đo lường.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Lớp đo lường các chỉ số sức khỏe của memory store: latency ghi/đọc, tỉ lệ dedup, số conflict, thời gian mỗi lần consolidation.
> 
> **Ẩn dụ/so sánh:** Giống đồng hồ táp-lô trên xe — không cần nhìn suốt đường đi, nhưng khi nghi ngờ có vấn đề thì phải biết đọc.
> 
> **Vì sao quan trọng:** Không đo lường thì không biết memory system đang dần xuống cấp hay đang hoạt động tốt.

Giải nghĩa các chỉ số: latency = thời gian chờ một thao tác (ghi/đọc) hoàn thành; dedup rate = tỉ lệ bản ghi bị loại vì trùng; conflict rate = tỉ lệ fact mâu thuẫn phải xử lý. Đo vài tuần một lần là đủ — giống soi đồng hồ táp-lô khi nghi xe hao xăng chứ không cần nhìn liên tục.

> **Tóm gọn 1 câu:** Đo 4 thứ cơ bản — tốc độ ghi/đọc, tỉ lệ trùng lặp, số mâu thuẫn, thời gian dọn kho — để phát hiện sớm memory system xuống cấp.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/13-9-performance-metrics.py`](examples/13-9-performance-metrics.py)

</details>

---

## 10. Labs Thực Hành

Phần này là 4 bài tập tự tay chạy bằng Python — làm xong là hiểu sâu hơn chỉ đọc.

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Các bài lab chạy được bằng Python để bạn tự tay trải nghiệm write-back, consolidation, versioned memory và metrics.
> 
> **Ẩn dụ/so sánh:** Giống bài tập thể dục — đọc kỹ thuật không bằng tự tập cho đến khi thuộc động tác.
> 
> **Vì sao quan trọng:** Học bằng tay giúp nhớ lâu gấp nhiều lần so với chỉ đọc lý thuyết.

### Lab 1: Write-back Memory

Trong bài này bạn dùng `MemoryWriter` để ghi một episodic memory, hai fact về BHYT, cập nhật profile user, rồi gọi `get_stats()` xem hệ thống đã "nhớ" được bao nhiêu thứ.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/14-lab-1-write-back-memory.py`](examples/14-lab-1-write-back-memory.py)

</details>

> **Tóm gọn 1 câu:** Lab 1 cho bạn tự tay dùng `MemoryWriter` ghi sự kiện, fact và hồ sơ user, rồi kiểm tra bằng `get_stats()` xem hệ thống đã nhớ được bao nhiêu.

### Lab 2: Consolidation

Thực hành dọn dẹp với `MemoryConsolidator`: tạo 3 fact về BHYT (hai cái gần như trùng nhau, một cái là bản cập nhật mới hơn), chạy `generate_memory_report` và xem `conflict_resolution` phát hiện được mâu thuẫn nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/15-lab-2-consolidation.py`](examples/15-lab-2-consolidation.py)

</details>

> **Tóm gọn 1 câu:** Lab 2 tạo 3 fact gần trùng nhau rồi dùng `MemoryConsolidator` dọn, xem báo cáo và thấy rõ conflict resolution bắt được mâu thuẫn nào.

### Lab 3: Versioned Memory

Mô phỏng một fact về mức đóng BHYT thay đổi qua 3 phiên bản, xem lịch sử bằng `vm.log()`, so sánh hai thời điểm bằng `vm.diff(0, 2)` và cuối cùng thử quay lại bản đầu với `vm.rollback(0)`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/16-lab-3-versioned-memory.py`](examples/16-lab-3-versioned-memory.py)

</details>

> **Tóm gọn 1 câu:** Lab 3 cho fact BHYT "sống" qua 3 phiên bản — xem lịch sử (`vm.log`), so sánh (`vm.diff`), và quay lui (`vm.rollback`) — để cảm nhận versioned memory như Git.

### Lab 4: Metrics

Mô phỏng 100 thao tác ghi/đọc với số liệu ngẫu nhiên và 2 lần consolidation, rồi in ra báo cáo `metrics.report()` để xem hệ thống được đo lường như thế nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/17-lab-4-metrics.py`](examples/17-lab-4-metrics.py)

</details>

> **Tóm gọn 1 câu:** Bốn lab phủ đủ 4 kỹ năng: ghi nhớ (Lab 1), dọn kho (Lab 2), quay lui theo phiên bản (Lab 3), và đo lường (Lab 4).

## 12. Bổ Sung Production: Retention, Consolidation, Hợp Đồng Compaction & SLO

> Nói nôm na: nối chuyện "lược bớt" của §02 với chuyện "giữ lại" của §03 — cái gì được bỏ qua, cái gì nhất định phải giữ lại cho bằng được.

Phần này nói về 4 thứ bắt buộc phải có khi memory system chạy thật: thời hạn sống của dữ liệu, quy tắc dọn dẹp, "hợp đồng" giữa phần được xóa và phần được giữ, và cam kết về tốc độ ghi.

### 12.1 Định nghĩa

Phần này định nghĩa 5 thuật ngữ sẽ dùng xuyên suốt.

Cách đọc bảng này: cột "Thuật ngữ" là từ chuyên môn, cột "Định nghĩa" là nghĩa và cách xử lý. Ví dụ dòng đầu: Retention / TTL (Time To Live = thời gian sống của dữ liệu — mỗi loại nhớ có hạn dùng riêng, hết hạn thì lưu trữ hoặc xóa).

| Thuật ngữ | Định nghĩa |
|------|------------|
| Retention / TTL | Hết hạn theo từng lớp memory (`episodic 30d, fact tới khi bị thay thế, session 24h`); hết hạn → archive hoặc xóa cứng |
| Xóa theo GDPR | Xóa theo phạm vi tenant/user trên primary store, vector index, backup (trong cửa sổ đã công bố) + biên nhận |
| Trigger consolidation | Điều kiện chạy job merge/dedup/conflict: kích thước, thời gian, tín hiệu (tỷ lệ conflict, feedback) |
| Hợp đồng compaction↔memory | Ranh giới: §02 được loại mọi thứ trừ những gì §03 đã ghim là durable |
| SLO đường ghi | p50/p99 + đảm bảo durability cho đường ingest (ví dụ `p99 < 300ms, 0 mất dữ liệu khi đã ack`) |

Giải nghĩa thêm mấy từ trong bảng: archive = chuyển dữ liệu cũ sang kho lưu trữ ít dùng thay vì xóa hẳn; tenant = một khách hàng/đơn vị thuê hệ thống (dữ liệu mỗi tenant phải tách biệt); primary store = kho dữ liệu chính; vector index = chỉ mục tìm kiếm theo nghĩa; p50/p99 = thời gian chờ mà 50% / 99% các yêu cầu không vượt quá (p99 < 300ms nghĩa là chỉ 1% yêu cầu chậm hơn 300ms); durability = độ bền dữ liệu (ghi xong là không mất); ingest = đường đưa dữ liệu vào; ack = xác nhận đã nhận.

> **Tóm gọn 1 câu:** Mục này định nghĩa "luật chơi" production: mỗi loại nhớ có hạn dùng (TTL), có quyền xóa theo luật GDPR, có điều kiện kích hoạt dọn dẹp, có ranh giới rõ với phần lược bớt, và có cam kết tốc độ ghi (SLO).

### 12.2 Retention / Tuân Thủ

Phần này quy định "hạn dùng" của từng loại dữ liệu, cách tách dữ liệu giữa các khách hàng, và cách xóa khi user yêu cầu.

- **TTL mặc định, nhớ như hạn dùng của đồ ăn:** `session: 24h là dọn; episodic: 30–90d thì cho vào kho archive; semantic fact: không đặt hạn cứng nhưng phải ghi valid_until + nguồn gốc; user profile: giữ tới khi user bảo xóa.` Có một bạn sweeper chạy hàng giờ để quét; trước khi xóa cứng là phải archive sang cold store đã.
- **Nhà ai nấy ở theo tenant:** lấy `tenant_id` làm vách ngăn cho mọi bảng/namespace; câu query nào cũng phải kèm bộ lọc; đọc lấn sang nhà hàng xóm là bị chặn ngay ở API + policy DB (RLS). Tenant enterprise nào cũng có chìa khóa mã hóa riêng.
- **Xóa theo kiểu GDPR/CCPA cho đàng hoàng:** gọi `DELETE /memory?user=X` là đi một vòng tombstone (đá mồ — đánh dấu "đã xóa" trước khi xóa thật, để các bản sao biết đường) → xóa ở vector + KG + log (redact — xóa/m che thông tin nhạy cảm trong log) → dọn backup trong ≤30d → trả về `deletion_receipt{id, scope, ts}` làm bằng (biên nhận xóa: id nào, xóa phạm vi nào, lúc nào). SLA 24h là xong (SLA = cam kết mức dịch vụ — ở đây là cam kết xóa xong trong 24h).

> **Tóm gọn 1 câu:** Dữ liệu có hạn dùng như hạn sử dụng (session 24h, episodic 30–90 ngày, fact sống tới khi bị thay thế), dữ liệu các khách hàng ngăn cách tuyệt đối, và yêu cầu xóa phải xóa sạch mọi bản sao kèm biên nhận trong 24h.

### 12.3 Trigger Consolidation + Giải Quyết Xung Đột

Phần này quy định khi nào thì kích hoạt dọn dẹp và khi 2 fact mâu thuẫn thì tin bên nào.

Mình cho chạy consolidation mỗi khi **thấy một trong mấy dấu hiệu này**: `unconsolidated_writes > 500` (hơn 500 lần ghi chưa được dọn), tới giờ cron hàng giờ (cron = hẹn giờ chạy tự động), `conflict_rate > 5%` (hơn 5% fact mâu thuẫn), hay có feedback chê một fact nào đó. Dây chuyền làm như dọn nhà cuối tuần: dedup (cosine ≥0.9 là gộp — cosine = thước đo độ giống giữa 2 câu dựa trên vector; 0.9 = giống 90% trở lên) → soi conflict (cùng subject+predicate mà object khác nhau — tạm hiểu là cùng nói về một thuộc tính của một đối tượng nhưng giá trị khác nhau, ví dụ "BHYT đóng 4.5%" và "BHYT đóng 5%") → dàn xếp: `last-writer-wins` (bản ghi sau thắng — chọn ai sửa sau) chỉ khi nguồn mới tin cậy bằng hoặc hơn nguồn cũ; không thì theo `highest-trust-wins` (nguồn uy tín hơn thắng — ví dụ cổng chính phủ thắng bài blog); bí quá thì `escalate_to_user` (chuyển lên nhờ người dùng phân xử). Lúc nào cũng giữ cả hai version + gắn cạnh `supersedes` (thay thế cho — mối nối ghi rõ fact này thay fact nào) — tuyệt đối không lén ghi đè.

> **Tóm gọn 1 câu:** Dọn dẹp được kích hoạt theo dung lượng, giờ hẹn, tỉ lệ mâu thuẫn hoặc feedback; khi 2 fact đá nhau thì tin bản mới hơn hoặc nguồn uy tín hơn, giữ cả hai bản kèm mối nối "thay thế cho", không bao giờ xóa lặng lẽ.

### 12.4 Hợp Đồng Compaction↔Memory

Phần này vẽ ranh giới giữa 2 bên: phần nào được phép bỏ khi nén context, phần nào buộc phải giữ lại.

Cách đọc bảng này: cột trái là những thứ §02 (bước nén context — compaction = nén hội thoại dài lại cho vừa cửa sổ context) được phép loại; cột phải là những thứ §03 (bộ nhớ) buộc phải giữ. Ví dụ: tán gẫu được bỏ, nhưng quyết định đã chốt và TODO đang mở phải giữ.

| §02 được loại (transient) | §03 phải giữ (durable) |
|---|---|
| stdout tool thô, chunk retrieval cũ, diff đã thay thế, tán gẫu | Fact đã ghim, quyết định, TODO mở, preference user, block resume |
| Được bỏ sau khi tóm tắt resume | Phải sống sót sau compaction; nạp lại được qua retrieve |

Giải nghĩa: transient = tạm thời, dùng xong là bỏ; durable = bền vững, phải sống sót qua mọi lần nén. resume_block = khối thông tin "bàn giao" để mở lại công việc dở (những việc đang làm, quyết định đã chốt).

Quy tắc nằm lòng: compaction có nhả ra `resume_block` thì write-back **phải** cất kỹ `resume_block + decisions + open items` rồi mới được dọn chúng khỏi context. Tới lúc mở lại session, §02 chỉ việc hydrate từ §03 bằng query `tenant+task` là đủ đồ nghề làm tiếp (hydrate = "tưới nước" — nạp lại dữ liệu từ kho vào context cho đầy đủ).

> **Tóm gọn 1 câu:** Hợp đồng giữa 2 bên: những gì tạm (stdout thô, tán gẫu, diff cũ) được bỏ khi nén; những gì bền (fact ghim, quyết định, TODO mở, resume_block) phải được ghi vào bộ nhớ trước rồi mới được nén.

### 12.5 SLO Đường Ghi

Phần này đặt cam kết về tốc độ và độ bền cho việc ghi dữ liệu (SLO = Service Level Objective — mức cam kết đo được, ví dụ "99% yêu cầu dưới 300ms").

- Đường ghi phải nhanh như chớp: `p50 write < 80ms, p99 < 300ms` (nửa số lần ghi dưới 80ms, 99% dưới 300ms); còn consolidation nặng thì cho chạy nền `p99 < 5min`. Lúc đang ghi thì tranh thủ kiểm tra dedup luôn; mấy vụ merge nặng thì đẩy ra hàng đợi write-behind cho khỏi nghẽn critical path (critical path = chặng "giao hàng" cho người dùng — việc gì nằm trên đó mà chậm là người dùng chờ).
- Độ bền thì chắc như đinh: chỉ dám ack (xác nhận "đã ghi xong") khi đã ghi xong WAL (Write-Ahead Log — sổ ghi trước mọi thay đổi để nếu sập giữa chừng vẫn phục hồi được) + primary (kho chính); hàng đợi retry có idempotency key `tenant:doc_hash` (chống ghi trùng: cùng một khóa thì ghi lại bao nhiêu lần kết quả cũng chỉ là một bản) chống ghi trùng. Thấy `write_error% > 1%` (hơn 1% lần ghi thất bại) hay `queue_lag > 10k` (hàng đợi dồn hơn 10 nghìn việc chưa xử) là phải kêu lên ngay.

> **Tóm gọn 1 câu:** Cam kết tốc độ (99% lần ghi dưới 300ms) và độ bền (chỉ báo "thành công" khi dữ liệu đã nằm an toàn trong sổ ghi trước + kho chính), với còi báo động khi tỉ lệ lỗi vượt 1% hoặc hàng đợi dồn quá 10 nghìn việc.

<details>
<summary>TypeScript Code — Memory Có Version với Consolidation (Click to expand/collapse)</summary>

> 📄 **Code ví dụ:** [`examples/18-12-5-slo-uong-ghi.ts`](examples/18-12-5-slo-uong-ghi.ts)

</details>

### 12.6 Checklist

Phần này gom cả mục 12 thành 6 câu kiểm tra nhanh — dùng như danh sách dò trước khi đi production.

Cách đọc bảng này: mỗi dòng là một quy tắc, đánh số để dễ viện dẫn. Ví dụ dòng 1: dữ liệu phải có hạn dùng và có "người quét" hàng giờ, phải lưu trữ trước khi xóa hẳn.

| # | Quy tắc |
|---|------|
| 1 | TTL theo lớp + sweeper hàng giờ (sweeper = "người quét" — job tự động chạy định kỳ tìm và xử lý dữ liệu hết hạn); archive trước khi xóa cứng |
| 2 | Phân vùng `tenant_id` + RLS (Row-Level Security — khóa dữ liệu theo dòng: query của tenant này không bao giờ chạm tới dòng của tenant khác); không tồn tại đường query liên tenant |
| 3 | Xóa GDPR quét facts + vector + log với biên nhận ≤24h |
| 4 | Consolidation theo trigger kích thước/thời gian/tín hiệu; giải conflict theo độ tin cậy, không ghi đè âm thầm |
| 5 | Thực thi hợp đồng compaction↔memory: resume/quyết định được lưu trước khi loại |
| 6 | Dashboard SLO ghi: p99, error%, queue lag, dedup rate, conflict rate |

> **Tóm gọn 1 câu:** Sáu câu dò cuối: có hạn dùng + người quét, tách tenant triệt để, xóa GDPR có biên nhận, dọn dẹp có điều kích hoạt và không ghi đè âm thầm, giữ resume trước khi nén, và có dashboard theo dõi.

---

## 11. Tài Liệu Tham Khảo

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Đây là tủ sách đọc thêm — có papers khoa học, có framework với công cụ, có cả blogs của mấy đội đã lăn lộn làm memory system production thật.
> 
> **Ẩn dụ/so sánh:** Như tờ giấy thầy cho trước hôm thi — muốn đào sâu hơn thì cứ men theo danh sách này mà đọc.
> 
> **Vì sao quan trọng:** Nghề này đổi từng tháng, có danh sách này trong tay thì bạn tự kiểm chứng và tự cập nhật được, khỏi sợ học phải đồ cũ.

### Papers & Research

1. **MemGPT: Towards LLMs as Operating Systems** — UC Berkeley, 2023 — Tiered memory management for LLMs
2. **MemoryBank: Enhancing Large Language Models with Long-Term Memory** — 2023 — Weighted memory decay
3. **A Survey on Long-Term Memory for AI Agents** — 2024 — Comprehensive overview of memory architectures

### Frameworks & Tools

1. **Mem0** — Production memory layer for AI agents — https://mem0.ai
2. **LangMem** — Long-term memory for agents — https://github.com/langchain-ai/langmem
3. **Zep** — Memory server for AI assistants — https://www.getzep.com
4. **OpenMemory** — MCP-based memory server — https://github.com/openmemory

### Blogs & Resources

1. **Anthropic — Memory in Claude Code** — 3-tier memory architecture
2. **LangChain — Building Long-Term Memory** — Practical guide
3. **Mem0 Blog** — Memory patterns for production AI

> **Tóm gọn 1 câu:** Danh sách này là "tủ sách đọc thêm" chia 3 ngăn — papers khoa học (nền lý thuyết), frameworks/tools (đồ dùng có sẵn), blogs (kinh nghiệm thực chiến).

---

**Kết Luận**

Nói gọn một câu: Memory Update & Knowledge Store là việc chăm cho "bộ não" của AI lúc nào cũng tỉnh táo và đúng hẹn. Có ba chiêu chính cứ nhớ như nhớ đường về nhà:

> **"Hệ thống nào không biết tự làm mới kiến thức thì coi như chẳng học được gì."**

1. **Event-driven updates** — Có chuyện mới là ghi ngay, đừng để mai quên
2. **Consolidation pipeline** — Cuối ngày có người dọn dẹp, gộp cái trùng, dàn xếp cái lộn xộn
3. **Temporal decay** — Tin cũ thì nhẹ vía dần đi, để khỏi lấn át tin mới

Mấy điều mang về gối đầu giường:
1. ✅ **Chịu khó dedupe** — trước khi nhét fact mới vào kho thì ngó xem có rồi chưa
2. ✅ **Fact quan trọng thì đánh số version** — để lỡ sai còn rollback được
3. ✅ **Siêng consolidation** — cho chạy nền đều đặn như quét nhà
4. ✅ **Nhớ temporal decay** — cũ không có nghĩa là quý hơn mới
5. ✅ **Đo đếm đàng hoàng** — soi write latency, dedup rate, conflicts thường xuyên

---

*Tài liệu: III. Update Memory & Knowledge Store*  
*Ngày cập nhật: 16/10/2026*  
*Tác giả: AI Knowledge Repository*  
*Môi trường: Ollama (gemma3:12b, nomic-embed-text)*

---

## Cập nhật 10/2026 — Structured Note-Taking & Long-Running Memory

Phần bổ sung này kể 2 pattern mới của Anthropic: agent tự ghi chú ra file bên ngoài, và cách chạy các session kéo dài nhiều ngày không mất mạch.

### 1. Structured note-taking / agentic memory (Anthropic 09/2025)

Phần này giải thích vì sao agent cần tự ghi NOTES.md ra file thay vì ôm hết trong đầu.

Context window (cửa sổ ngữ cảnh — số token tối đa model có thể "nhớ" trong một lần) có hạn, nên agent tự ghi NOTES.md/todo ra ngoài context window để:
- Giữ state giữa các turn trong cùng session
- Bàn giao context cho session tiếp theo
- Tránh quên action items đã đề ra

**Memory tool (Claude Developer Platform):** Persistent memory giữa các summarization (summarization = nén hội thoại dài thành bản tóm tắt; persistent memory = bộ nhớ sống sót qua các lần nén đó) — agent có thể đọc/ghi memory store riêng, không phụ thuộc conversation window.

**Pattern đề xuất:**

```
PROJECT/
├── CLAUDE.md          # System instructions + conventions
├── NOTES.md           # Agent notes, todos, state
├── SPEC.md            # Specifications
└── PROGRESS.md        # Feature progress tracking
```

Giải nghĩa 4 file: CLAUDE.md là "luật nhà" (hướng dẫn hệ thống + quy ước code), NOTES.md là sổ tay của agent (ghi chú, todo, trạng thái), SPEC.md là bản đặc tả yêu cầu, PROGRESS.md là bảng theo dõi tiến độ từng feature.

> **Tóm gọn 1 câu:** Khi context window có hạn, agent phải tự ghi chú ra các file bên ngoài (NOTES.md, todo...) để giữ trạng thái, bàn giao cho phiên sau, và không quên việc đã hẹn.

### 2. Long-running agent memory pattern (Anthropic 11/2025)

Phần này giải thích cách chạy agent qua nhiều session dài hơi: một "initializer" dựng khung ban đầu, các session sau đọc vào và làm tiếp.

Initializer agent tạo cấu trúc ban đầu (initializer = agent "khởi động" — session đầu tiên dựng sẵn các file khung), các session sau đọc và tiếp tục:

Cách đọc bảng này: cột "File" là tên file/kho lưu trữ, cột "Mục đích" là nó dùng để làm gì. Ví dụ `feature_list.json` là danh sách tính năng cần làm, kèm cờ `passes: false` (chưa vượt qua kiểm thử).

| File | Mục đích |
|------|----------|
| `feature_list.json` | Danh sách features với `passes: false` (chưa pass) |
| `init.sh` | Script setup repo, dependencies |
| `claude-progress.txt` | Progress notes, decisions, next steps |
| Git commits | Mỗi feature commit khi pass |

**Session flow:**
1. Đọc `feature_list.json` + `git log` → xác định feature tiếp theo
2. Implement feature → run tests
3. Nếu test pass → mark feature trong JSON + git commit + update progress
4. Nếu fail → ghi note vào progress file

> **Tóm gọn 1 câu:** Session nào cũng mở bằng cách đọc `feature_list.json` + `git log` để biết mình đang ở đâu, làm xong feature nào thì tick trong JSON + commit + cập nhật tiến độ — nhờ đó chạy nhiều ngày vẫn không mất mạch.

**Tại sao JSON được ưa chuộng hơn Markdown:**
- Model ít ghi đè/ghi sai format JSON so với Markdown tự do
- Parse machine-readable, không phải regex parse text (parse = phân tích cú pháp để máy đọc được; regex = biểu thức chính quy — cách "bới" chữ theo khuôn mẫu, dễ gãy với văn bản tự do)
- Dễ diff trong git, conflict resolution đơn giản hơn

> **Tóm gọn 1 câu:** JSON thắng Markdown vì model ít viết sai format, máy đọc trực tiếp được mà không cần "bới chữ", và diff trong git gọn gàng hơn.

### 3. Khi nào reset memory hoàn toàn

Phần này định nghĩa ranh giới: khi nào thì xóa sạch bộ nhớ được, khi nào thì tuyệt đối không.

**Nên reset khi:**
- Task đã hoàn thành hoàn toàn
- Tất cả facts đã được consolidate vào permanent storage
- Milestone cuối cùng đã đạt

**Không nên reset khi:**
- Đang giữa milestone/cuộc họp quan trọng
- Facts chưa được consolidate (sẽ mất insights)
- Cần audit trail cho compliance (compliance = tuân thủ pháp lý/nội bộ — cần sổ sách để đối chiếu khi thanh tra)

> **Tóm gọn 1 câu:** Reset bộ nhớ chỉ khi công việc đã xong và mọi fact quý đã được chuyển vào kho lâu dài — còn đang dở hay cần chứng minh "đã làm gì" thì đừng đụng vào.

### 4. Python code: ProgressStore class

Phần này cung cấp class Python quản lý file tiến độ (PROGRESS) nói ở trên.

> 📄 **Code ví dụ:** [`examples/19-4-python-code-progressstore-class.py`](examples/19-4-python-code-progressstore-class.py)

> **Tóm gọn 1 câu:** `ProgressStore` là bản hiện thực Python của pattern ở mục 2 — đọc/ghi file tiến độ một chỗ, các session sau chỉ cần nạp vào là làm tiếp được.

### 5. Cross-link

Phần này trỏ sang tài liệu liên quan để đọc nối.

- `[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)` — Layer 6 (Agent Memory & State) — structured memory patterns cho production agents.
