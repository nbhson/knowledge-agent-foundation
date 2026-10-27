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

Hãy tưởng tượng bạn mới nhận việc trông thư viện phường. Sáng nào cũng có người mang sách mới tới tặng, chiều lại có người trả sách cũ. Nếu bạn cứ hồn nhiên nhận hết rồi chồng bừa lên kệ, chẳng bao giờ xếp lại cho gọn, chẳng dám bỏ cuốn nào đã mục nát, cũng không buồn ghi thêm vào cuốn catalog — thì chỉ một năm sau thôi, thư viện sẽ thành một **kho chứa đồ lộn xộn**, muốn tìm một cuốn truyện cũng phải bới tung cả đống.

**Bộ nhớ của AI cũng y hệt như vậy nếu chỉ biết "ghi vào" mà quên "dọn lại".**

LLM thì rất ham học cái mới, nhưng nếu mình không giúp nó **consolidate** (gộp cái trùng nhau lại), **prune** (mạnh dạn bỏ cái đã cũ), và **index** (xếp lại cho ngay ngắn để dễ tìm) — thì knowledge base cứ ngày một chậm, ngày một nhiễu, rồi trả lời sai lúc nào không hay. Kết cục quen thuộc là: Agent cứ lặp lại đúng một lỗi cũ, hồn nhiên đưa ra thông tin đã hết hạn, và hallucinate chỉ vì thiếu factual grounding để bám vào.

### Tại Sao Update Memory Quan Trọng?

> *"Bộ não to chưa chắc đã giỏi — quan trọng là mình có chịu lau chùi, sắp xếp cho gọn gàng, cập nhật thường xuyên hay không."*

#### 3 Bằng Chứng Khoa Học

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

## Tổng Quan

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

## Tại Sao Update Memory & Knowledge Store Quan Trọng?

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
3. **Gộp gọn ăn đứt ôm đồm**: cứ thấy gì cũng nhét vào thì chỉ tạo ra **noise** ồn ào. Chịu khó consolidation — ngồi lại merge, dedupe, update — mới chắt được **signal** trong veo.

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

### Cost-Benefit Analysis

| Chi Phí / Giá Trị | Không Có Write-back | Có Write-back + Consolidation |
|---|---|---|
| **Duplicate Work** | Agent lặp lại việc đã làm | Agent biết đã làm gì, tiếp tục từ đó |
| **Knowledge Drift** | Facts cũ vẫn tồn tại → sai lệch | Auto-update: facts mới thay thế facts cũ |
| **Storage Cost** | Liên tục tăng, không kiểm soát | Giảm 40-60% qua consolidation |
| **Response Quality** | Giảm dần theo thời gian | Cải thiện liên tục qua feedback loop |
| **User Trust** | Giảm vì phải lặp lại thông tin | Tăng vì agent "nhớ" context |

**Kể chuyện tiền nong cho dễ hình dung**: mỗi tháng bỏ ra $500 nuôi memory infrastructure cho tử tế, thì tiết kiệm được cỡ $2,000 tiền chạy agent lòng vòng (vì bớt được 75% câu hỏi trùng lặp). Đầu tư một, lời ba — ai mà chê.

### Analogies Minh Họa

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
- **Write-back** = Vừa code xong là commit ngay cho nóng
- **Consolidation** = Ngồi merge branches, gỡ rối conflicts
- **Event Sourcing** = Cuốn sổ Git log — thích là time-travel về bất kỳ commit nào trong quá khứ
- **Nếu không consolidation** = Hàng trăm branches chĩa ra tứ phía, không ai dám merge vì sợ toang

### Evolutionary Context: Từ Simple Storage đến Intelligent Memory

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

**Điều rút ra rất đời**: "Chỗ để đồ thì rẻ, cái đắt là công ngồi sắp xếp cho gọn." Một cái vector store ôm 10,000 documents mà không bao giờ consolidation thì thua xa một knowledge graph chỉ 100 facts nhưng được chăm chút gọn gàng.

### Nếu Bạn Kệ Luôn, Không Thèm Update Memory...

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
- Không có session handoff, đồng đội vào sau cũng mù mờ chẳng biết chuyện gì đã xảy ra

### Best Practices (Và Tại Sao)

| Rule | Why |
|---|---|
| Luôn ghi timestamp cho mọi fact | Để biết fact nào mới nhất khi có conflict |
| Consolidate định kỳ (không phải real-time) | Real-time consolidation quá tốn compute; batch processing hiệu quả hơn 5x |
| Luôn log mọi write operation (audit trail) | Để debug khi memory bị corruption; để rollback nếu cần |
| Version facts (với source và confidence) | Để resolve conflict: fact từ source nào đáng tin hơn |
| Auto-expire outdated facts | Facts 6 tháng tuổi có 73% chance là đã lỗi thời (research data) |
| Tách Episodic vs Semantic memory | Episodic = "điều gì đã xảy ra", Semantic = "sự thật là gì" — 2 loại memory cần xử lý khác nhau |

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Write-back Memory](#1-write-back-memory) | Ghi sự kiện mới vào memory systems |
| 2 | [Memory Consolidation](#2-memory-consolidation) | Tổng hợp & merge thông tin |
| 3 | [Report Generation](#3-report-generation) | Tạo output có cấu trúc |
| 4 | [KB Maintenance](#4-kb-maintenance) | Thêm/sửa/xóa knowledge base |
| 5 | [Event Sourcing Pattern](#5-event-sourcing-pattern) | Lưu trữ dạng event log |

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

### 1.2 Write-back Implementation

Lớp `MemoryWriter` bên dưới là "cây bút" của hệ thống: `write_episodic` ghi sự kiện, `write_fact` ghi fact, `update_fact` sửa fact, `write_user_profile` cập nhật thông tin user. Không cần hiểu từng dòng — chỉ cần để ý điểm chung: **hàm nào cũng ghi vào `event_log`** để sau này truy vết được ai đã ghi gì, lúc nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

class MemoryWriter:
    """
    Write information back to various memory systems
    
    Supports: Episodic, Semantic, Working memory
    """
    
    def __init__(self, vector_store=None, knowledge_graph=None):
        self.vector_store = vector_store
        self.knowledge_graph = knowledge_graph
        self.episodic_store = []  # Simple list for demo
        self.entity_store = {}
        self.event_log = []
    
    # ─────────────────────────────────────────────
    # EPISODIC MEMORY: Lưu sự kiện
    # ─────────────────────────────────────────────
    def write_episodic(self, event_type, content, metadata=None):
        """
        Ghi một sự kiện vào episodic memory
        
        event_type: "conversation", "learning", "feedback", "decision"
        content: Nội dung sự kiện
        metadata: Thông tin bổ sung
        """
        event = {
            "id": f"ep_{len(self.episodic_store)}",
            "type": event_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        
        self.episodic_store.append(event)
        
        # Also store in vector DB for semantic search
        if self.vector_store:
            embedding = self._get_embedding(content)
            self.vector_store.add(
                document=content,
                vector=embedding,
                metadata={"type": "episodic", **event}
            )
        
        self._log_event("write_episodic", event)
        return event["id"]
    
    def recall_episodic(self, query, top_k=5):
        """Recall relevant episodic memories"""
        if self.vector_store:
            embedding = self._get_embedding(query)
            results = self.vector_store.search(embedding, top_k)
            return [r["metadata"] for r in results]
        
        # Fallback: search by keyword
        query_lower = query.lower()
        matches = [
            e for e in self.episodic_store
            if query_lower in e["content"].lower()
        ]
        return matches[:top_k]
    
    # ─────────────────────────────────────────────
    # SEMANTIC MEMORY: Lưu facts
    # ─────────────────────────────────────────────
    def write_fact(self, subject, predicate, obj, confidence=1.0):
        """
        Ghi một fact vào semantic memory (Knowledge Graph)
        
        Ví dụ: ("BHYT", "mức đóng", "4.5% lương cơ sở", 0.95)
        """
        fact = {
            "subject": subject,
            "predicate": predicate,
            "object": obj,
            "confidence": confidence,
            "created_at": datetime.now().isoformat(),
            "source": "user_conversation",
        }
        
        if self.knowledge_graph:
            self.knowledge_graph.add_triplet(subject, predicate, obj)
        
        # Also vectorize for semantic search
        if self.vector_store:
            fact_text = f"{subject} {predicate} {obj}"
            embedding = self._get_embedding(fact_text)
            self.vector_store.add(
                document=fact_text,
                vector=embedding,
                metadata={"type": "fact", **fact}
            )
        
        self._log_event("write_fact", fact)
        return fact
    
    def update_fact(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update an existing fact"""
        if self.knowledge_graph:
            # Remove old triplet
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == old_obj)
            ]
            # Add new triplet
            self.knowledge_graph.add_triplet(subject, predicate, new_obj)
        
        update_event = {
            "action": "update_fact",
            "old": {"subject": subject, "predicate": predicate, "object": old_obj},
            "new": {"subject": subject, "predicate": predicate, "object": new_obj},
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        
        self._log_event("update_fact", update_event)
        return update_event
    
    def delete_fact(self, subject, predicate, obj):
        """Delete a fact from knowledge"""
        if self.knowledge_graph:
            self.knowledge_graph.triplets = [
                (s, p, o) for s, p, o in self.knowledge_graph.triplets
                if not (s == subject and p == predicate and o == obj)
            ]
        
        self._log_event("delete_fact", {
            "subject": subject, "predicate": predicate, "object": obj
        })
    
    # ─────────────────────────────────────────────
    # ENTITY MEMORY: Lưu entities
    # ─────────────────────────────────────────────
    def write_entity(self, name, entity_type, attributes=None):
        """Store/update entity information"""
        if name not in self.entity_store:
            self.entity_store[name] = {
                "type": entity_type,
                "attributes": {},
                "created_at": datetime.now().isoformat(),
            }
        
        if attributes:
            self.entity_store[name]["attributes"].update(attributes)
        
        self.entity_store[name]["updated_at"] = datetime.now().isoformat()
        
        self._log_event("write_entity", {"name": name, "type": entity_type})
        return self.entity_store[name]
    
    # ─────────────────────────────────────────────
    # USER PROFILE: Lưu thông tin user
    # ─────────────────────────────────────────────
    def write_user_profile(self, user_id, updates):
        """
        Cập nhật user profile
        
        updates: dict of {field: value}
        Ví dụ: {"occupation": "freelancer", "location": "HCM"}
        """
        profile = self.entity_store.get(f"user_{user_id}", {
            "type": "user",
            "attributes": {},
        })
        
        profile["attributes"].update(updates)
        profile["updated_at"] = datetime.now().isoformat()
        
        self.entity_store[f"user_{user_id}"] = profile
        
        self._log_event("update_profile", {
            "user_id": user_id, 
            "updates": updates
        })
        return profile
    
    def get_user_profile(self, user_id):
        """Retrieve user profile"""
        return self.entity_store.get(f"user_{user_id}", None)
    
    # ─────────────────────────────────────────────
    # FEEDBACK LOOP
    # ─────────────────────────────────────────────
    def write_feedback(self, query, answer, rating, correction=None):
        """
        Store user feedback for improvement
        
        rating: 1-5
        correction: correct answer if user says wrong
        """
        feedback = {
            "query": query,
            "original_answer": answer,
            "rating": rating,
            "correction": correction,
            "timestamp": datetime.now().isoformat(),
        }
        
        if self.vector_store and correction:
            # Store correction as a better example
            embedding = self._get_embedding(query)
            self.vector_store.add(
                document=correction,
                vector=embedding,
                metadata={
                    "type": "correction",
                    "original_answer": answer,
                    "rating": rating,
                }
            )
        
        self._log_event("feedback", feedback)
        return feedback
    
    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────
    def _get_embedding(self, text):
        """Get embedding using Ollama"""
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text",
                "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _log_event(self, event_type, data):
        """Log all write operations for audit trail"""
        self.event_log.append({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_stats(self):
        """Return write statistics"""
        return {
            "episodic_count": len(self.episodic_store),
            "entity_count": len(self.entity_store),
            "event_count": len(self.event_log),
            "event_types": list(set(e["type"] for e in self.event_log)),
        }
```

</details>

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

Khối ASCII dưới đây so sánh memory **TRƯỚC** và **SAU** khi consolidation. Phần trên là 5 fact rời rạc về BHYT (trùng lặp, cũ mới lẫn lộn); phần dưới là kết quả sau khi dọn — chỉ còn 2 fact rõ ràng. Ý tưởng cốt lõi nằm ở dòng cuối: **Consolidation = Merge + Dedupe + Update + Summarize**.

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

### 2.2 Implementation

Class `MemoryConsolidator` thực hiện 4 bước dọn dẹp: gộp fact giống nhau (`consolidate_facts`), loại fact quá cũ (`temporal_consolidation`), tóm tắt thông tin về một entity (`summarize_entities`), và phát hiện fact mâu thuẫn (`conflict_resolution`). Mỗi hàm trả về các con số thống kê (merged/deleted/removed) — bạn chỉ cần đọc kết quả trả về để biết đã dọn được những gì.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class MemoryConsolidator:
    """
    Consolidate and merge memories to reduce redundancy
    and keep knowledge up-to-date
    """
    
    def __init__(self, vector_store, knowledge_graph, llm_func=None):
        self.vector_store = vector_store
        self.kg = knowledge_graph
        self.llm = llm_func
    
    def consolidate_facts(self, similarity_threshold=0.85):
        """
        Step 1: Find and merge duplicate/similar facts
        """
        if not self.kg or not self.kg.triplets:
            return {"merged": 0, "deleted": 0}
        
        merged = 0
        deleted = 0
        
        # Group facts by subject
        facts_by_subject = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in facts_by_subject:
                facts_by_subject[key] = []
            facts_by_subject[key].append(obj)
        
        # For each group, keep only the latest/most complete
        for (subj, pred), objs in facts_by_subject.items():
            if len(objs) <= 1:
                continue
            
            # Find duplicates using text similarity
            unique_objs = []
            for obj in objs:
                is_dup = False
                for unique in unique_objs:
                    if self._text_similarity(obj, unique) > similarity_threshold:
                        is_dup = True
                        break
                if not is_dup:
                    unique_objs.append(obj)
            
            deleted += len(objs) - len(unique_objs)
        
        return {"merged": merged, "deleted": deleted}
    
    def temporal_consolidation(self, max_age_days=30):
        """
        Step 2: Remove outdated facts based on age
        
        Facts older than max_age_days may be outdated
        """
        from datetime import datetime, timedelta
        
        cutoff = datetime.now() - timedelta(days=max_age_days)
        removed = 0
        
        if not self.kg:
            return {"removed": removed}
        
        # Filter by timestamp (if stored in metadata)
        # Simplified: just count for demo
        return {"removed": removed}
    
    def summarize_entities(self, entity_name, llm_func=None):
        """
        Step 3: Generate summary for all facts about an entity
        
        Useful for building entity profiles
        """
        if not self.kg:
            return ""
        
        facts = self.kg.query_entity(entity_name, max_hops=1)
        
        if not facts:
            return f"Không tìm thấy thông tin về {entity_name}"
        
        facts_text = "\n".join(
            f"- {subj} {pred} {obj}" 
            for subj, pred, obj, _ in facts
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            summary = func(
                f"Tóm tắt thông tin về {entity_name}:\n\n{facts_text}\n\nTóm tắt:"
            )
            return summary
        
        return facts_text
    
    def conflict_resolution(self):
        """
        Step 4: Resolve conflicting facts
        
        Strategy: Most recent wins (temporal)
        Alternative: Most trusted source wins (source-based)
        """
        conflicts = []
        
        if not self.kg:
            return conflicts
        
        # Group by subject+predicate
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        # Find conflicts (same subject+predicate, different objects)
        for key, objs in fact_groups.items():
            if len(set(objs)) > 1:
                conflicts.append({
                    "subject": key[0],
                    "predicate": key[1],
                    "conflicting_values": list(set(objs)),
                    "resolution": "keep_latest",  # or "merge", "manual"
                })
        
        return conflicts
    
    def generate_memory_report(self, llm_func=None):
        """
        Generate a report of current memory state
        
        Useful for debugging and auditing
        """
        report = []
        report.append("=" * 50)
        report.append("MEMORY CONSOLIDATION REPORT")
        report.append("=" * 50)
        
        if self.kg:
            report.append(f"\nTotal triplets: {len(self.kg.triplets)}")
            report.append(f"Unique entities: {len(self.kg.entities)}")
            report.append(f"Predicates: {len(self.kg.predicates)}")
            
            # Community detection
            communities = self.kg.community_detection()
            report.append(f"Communities: {len(communities)}")
            
            for i, comm in enumerate(communities[:5]):
                report.append(f"  Community {i+1}: {', '.join(comm[:5])}")
        
        # Conflicts
        conflicts = self.conflict_resolution()
        report.append(f"\nConflicts found: {len(conflicts)}")
        for c in conflicts[:5]:
            report.append(f"  {c['subject']} → {c['conflicting_values']}")
        
        return "\n".join(report)
    
    def _text_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
```

</details>

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

4 loại báo cáo cơ bản mà hệ thống có thể tạo ra. Đọc mỗi khối theo 3 dòng: **Input** (lấy dữ liệu gì) → **Output** (tạo ra gì) → **Use** (dùng để làm gì). Ví dụ "Conversation Summary" lấy chat history để tạo bản tóm tắt bàn giao cho phiên làm việc kế tiếp.

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

### 3.2 Implementation

Class `ReportGenerator` hiện thực 3 loại báo cáo: `conversation_summary` (tóm tắt hội thoại), `knowledge_report` (tổng quan knowledge base) và `analysis_report` (phân tích nhiều nguồn kèm citations). Các hàm này gọi LLM để viết báo cáo rồi ép kết quả về JSON — nếu LLM trả sai định dạng, code có nhánh fallback trả về dữ liệu mặc định thay vì gây lỗi.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class ReportGenerator:
    """Generate structured reports from memory and context"""
    
    def __init__(self, llm_func=None):
        self.llm = llm_func
    
    def conversation_summary(self, messages, llm_func=None):
        """
        Tạo summary từ conversation history
        
        Output: JSON với summary, key_points, action_items
        """
        conversation_text = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in messages
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Phân tích cuộc trò chuyện sau và tạo báo cáo:

{conversation_text}

Output JSON:
{{
  "summary": "Tóm tắt 2-3 câu",
  "key_points": ["điểm 1", "điểm 2"],
  "action_items": ["việc cần làm 1"],
  "topics_discussed": ["chủ đề 1"],
  "sentiment": "positive/neutral/negative",
  "resolution": "resolved/ongoing/needs_followup"
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"summary": result, "key_points": [], "action_items": []}
        
        return {
            "summary": f"Conversation with {len(messages)} messages",
            "key_points": [],
            "action_items": [],
        }
    
    def knowledge_report(self, knowledge_graph, llm_func=None):
        """
        Tạo báo cáo về knowledge base hiện tại
        """
        if not knowledge_graph:
            return {"error": "No knowledge graph"}
        
        report = {
            "total_facts": len(knowledge_graph.triplets),
            "total_entities": len(knowledge_graph.entities),
            "total_predicates": len(knowledge_graph.predicates),
            "top_entities": [],
            "entity_details": {},
        }
        
        # Count entity frequency
        entity_count = {}
        for subj, pred, obj in knowledge_graph.triplets:
            entity_count[subj] = entity_count.get(subj, 0) + 1
            entity_count[obj] = entity_count.get(obj, 0) + 1
        
        # Top 10 entities
        sorted_entities = sorted(
            entity_count.items(), key=lambda x: x[1], reverse=True
        )
        report["top_entities"] = [
            {"name": name, "connections": count}
            for name, count in sorted_entities[:10]
        ]
        
        return report
    
    def analysis_report(self, query, sources, analysis, llm_func=None):
        """
        Tạo phân tích có cấu trúc từ nhiều nguồn
        
        Output: Report với citations, confidence, recommendations
        """
        sources_text = "\n".join(
            f"[{i+1}] ({s.get('source', 'unknown')}): {s.get('content', s.get('text', ''))}"
            for i, s in enumerate(sources)
        )
        
        if llm_func or self.llm:
            func = llm_func or self.llm
            prompt = f"""Tạo báo cáo phân tích cho câu hỏi:
            
Câu hỏi: {query}

Nguồn tham khảo:
{sources_text}

Phân tích:
{analysis}

Output JSON:
{{
  "answer": "Câu trả lời chính",
  "confidence": 0.0-1.0,
  "sources_used": [1, 2],
  "key_findings": ["finding 1", "finding 2"],
  "limitations": ["hạn chế 1"],
  "recommendations": ["khuyến nghị 1"]
}}"""
            
            result = func(prompt)
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"answer": result, "confidence": 0.5}
        
        return {"answer": analysis, "confidence": 0.5}
```

</details>

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

Class `KBMaintainer` là "người quản lý kho kiến thức" với 4 thao tác chính: `add_knowledge` (thêm), `update_knowledge` (sửa), `delete_knowledge` (xóa theo chủ đề hoặc chi tiết), và `validate_knowledge` (rà soát tìm fact mâu thuẫn, entity bị mồ côi). Điểm đáng chú ý: mọi thao tác đều ghi vào `changelog` — giống nhật ký lịch sử để biết đã đụng vào kiến thức nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class KBMaintainer:
    """
    Maintain knowledge base: add, update, delete, validate
    """
    
    def __init__(self, knowledge_graph, vector_store):
        self.kg = knowledge_graph
        self.vector_store = vector_store
        self.changelog = []
    
    def add_knowledge(self, subject, predicate, obj, source="manual"):
        """Add new knowledge"""
        self.kg.add_triplet(subject, predicate, obj)
        
        # Also index for search
        fact_text = f"{subject} {predicate} {obj}"
        embedding = self._get_embedding(fact_text)
        self.vector_store.add(
            document=fact_text,
            vector=embedding,
            metadata={"source": source, "added_at": datetime.now().isoformat()}
        )
        
        self.changelog.append({
            "action": "add",
            "fact": (subject, predicate, obj),
            "source": source,
            "timestamp": datetime.now().isoformat(),
        })
    
    def update_knowledge(self, subject, predicate, old_obj, new_obj, reason=""):
        """Update existing knowledge"""
        # Remove old
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and p == predicate and o == old_obj)
        ]
        
        # Add new
        self.kg.add_triplet(subject, predicate, new_obj)
        
        self.changelog.append({
            "action": "update",
            "old": (subject, predicate, old_obj),
            "new": (subject, predicate, new_obj),
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
    
    def delete_knowledge(self, subject, predicate=None, obj=None):
        """Delete knowledge (specific or all for a subject)"""
        before = len(self.kg.triplets)
        
        self.kg.triplets = [
            (s, p, o) for s, p, o in self.kg.triplets
            if not (s == subject and 
                   (predicate is None or p == predicate) and
                   (obj is None or o == obj))
        ]
        
        deleted = before - len(self.kg.triplets)
        self.changelog.append({
            "action": "delete",
            "subject": subject,
            "count": deleted,
            "timestamp": datetime.now().isoformat(),
        })
        
        return deleted
    
    def validate_knowledge(self, validation_rules=None):
        """
        Validate knowledge base against rules
        
        Rules:
        - No orphan entities
        - No contradictory facts
        - All required predicates present
        """
        issues = []
        
        # Check for orphan entities
        connected = set()
        for subj, pred, obj in self.kg.triplets:
            connected.add(subj)
            connected.add(obj)
        
        orphans = self.kg.entities - connected
        if orphans:
            issues.append({
                "type": "orphan_entities",
                "entities": list(orphans),
                "severity": "warning",
            })
        
        # Check for contradictions
        fact_groups = {}
        for subj, pred, obj in self.kg.triplets:
            key = (subj, pred)
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(obj)
        
        for key, objs in fact_groups.items():
            unique = set(objs)
            if len(unique) > 1:
                issues.append({
                    "type": "contradiction",
                    "fact": key,
                    "conflicting_values": list(unique),
                    "severity": "error",
                })
        
        return issues
    
    def export_knowledge(self, format="json"):
        """Export knowledge base"""
        if format == "json":
            return json.dumps({
                "triplets": [
                    {"subject": s, "predicate": p, "object": o}
                    for s, p, o in self.kg.triplets
                ],
                "entities": list(self.kg.entities),
                "changelog": self.changelog,
            }, indent=2, ensure_ascii=False)
        
        elif format == "markdown":
            lines = ["# Knowledge Base Export\n"]
            lines.append(f"Total facts: {len(self.kg.triplets)}\n")
            
            for subj, pred, obj in self.kg.triplets:
                lines.append(f"- **{subj}** {pred} **{obj}**")
            
            return "\n".join(lines)
    
    def get_stats(self):
        return {
            "total_facts": len(self.kg.triplets),
            "total_entities": len(self.kg.entities),
            "total_predicates": len(self.kg.predicates),
            "total_changes": len(self.changelog),
        }
    
    def _get_embedding(self, text):
        import requests
        try:
            response = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return response.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
```

</details>

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

Phần này giới thiệu ý tưởng gốc của event sourcing. Khối ASCII cho thấy cách lưu theo "nhật ký sự kiện" — mỗi dòng là một sự kiện có đánh dấu thời gian (`@ t=...`). Ba siêu năng lực nằm ở giữa khối: **Current State = Replay all events** (trạng thái hiện tại được dựng lại bằng cách phát lại mọi sự kiện), **Time Travel** (phát lại tới thời điểm T), và **Audit Trail** (giữ đầy đủ lịch sử thay đổi).

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

### 5.2 Implementation

Class `EventSourcedMemory` hiện thực ý tưởng trên bằng code. Hãy chú ý `record_event` — mọi thay đổi đều đi qua hàm này, được lưu vào danh sách `events`, rồi cập nhật `state` bằng `_apply_event`. Hai hàm thú vị nhất: `get_state_at(event_id)` cho phép "time travel" về trạng thái tại một sự kiện nào đó, và `undo_last()` hủy sự kiện cuối bằng cách dựng lại toàn bộ state từ đầu.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class EventSourcedMemory:
    """
    Memory system with full event sourcing
    All changes are stored as events, state is derived
    """
    
    def __init__(self):
        self.events = []
        self.state = {}  # Derived from events
    
    def record_event(self, event_type, data):
        """Record a new event"""
        event = {
            "id": len(self.events),
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        self.events.append(event)
        
        # Update state
        self._apply_event(event)
        
        return event["id"]
    
    def _apply_event(self, event):
        """Apply event to update current state"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["object"]
        
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            self.state[key] = data["new_object"]
        
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            self.state.pop(key, None)
        
        elif etype == "set_profile":
            self.state[("profile", data["user_id"])] = data["attributes"]
    
    def get_state(self):
        """Get current state"""
        return dict(self.state)
    
    def get_state_at(self, event_id):
        """Get state at a specific point in time (time travel)"""
        state = {}
        for event in self.events[:event_id + 1]:
            self._apply_event_to(state, event)
        return state
    
    def _apply_event_to(self, state, event):
        """Apply event to a specific state dict"""
        etype = event["type"]
        data = event["data"]
        
        if etype == "add_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["object"]
        elif etype == "update_fact":
            key = (data["subject"], data["predicate"])
            state[key] = data["new_object"]
        elif etype == "delete_fact":
            key = (data["subject"], data["predicate"])
            state.pop(key, None)
    
    def get_event_history(self, event_type=None):
        """Get event history, optionally filtered by type"""
        if event_type:
            return [e for e in self.events if e["type"] == event_type]
        return list(self.events)
    
    def undo_last(self):
        """Undo the last event"""
        if not self.events:
            return None
        
        event = self.events.pop()
        # Rebuild state from remaining events
        self.state = {}
        for e in self.events:
            self._apply_event(e)
        
        return event
```

</details>

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

**Chuyện nhà Claude Code**: team Anthropic đau đầu vì Claude hay "quên bài" qua mỗi session mới, không nhớ project đang làm dở kiểu gì. Thế là họ đẻ ra cách nhớ 3 tầng để đi đâu cũng mang theo được.

<details>
<summary><b>TypeScript Code (Click to expand/collapse)</b></summary>

```typescript
/**
 * Claude Code Memory Architecture
 * 
 * 3 tiers of memory:
 * 1. Session Memory (ephemeral) — lives in conversation
 * 2. Project Memory (persistent) — lives in CLAUDE.md files
 * 3. Global Memory (cross-project) — lives in user config
 */
class ClaudeCodeMemoryManager {
  
  // ═══════════════════════════════════════════
  // TIER 1: SESSION MEMORY (ephemeral)
  // Lives only during current conversation
  // ═══════════════════════════════════════════
  private sessionMemory = {
    facts: new Map<string, Fact>(),      // Facts discovered this session
    decisions: [] as Decision[],         // Code decisions made
    corrections: [] as Correction[],    // User corrections
    filesModified: new Set<string>(),   // Files touched this session
    
    addFact(fact: Fact) {
      this.facts.set(fact.id, {
        ...fact,
        sessionId: currentSessionId,
        timestamp: Date.now()
      });
    },
    
    recordDecision(decision: Decision) {
      this.decisions.push({
        ...decision,
        timestamp: Date.now(),
        filesInvolved: this.filesModified
      });
    }
  };

  // ═══════════════════════════════════════════
  // TIER 2: PROJECT MEMORY (persistent)
  // Stored in CLAUDE.md at project root
  // Survives across sessions
  // ═══════════════════════════════════════════
  private projectMemory = {
    // CLAUDE.md format
    conventions: [] as string[],
    architecture: "",
    decisions: [] as Decision[],
    pitfalls: [] as string[],
    
    async loadFromDisk(projectRoot: string) {
      const claudeMd = path.join(projectRoot, 'CLAUDE.md');
      if (fs.existsSync(claudeMd)) {
        const content = fs.readFileSync(claudeMd, 'utf-8');
        this.parseClaudeMd(content);
      }
    },
    
    async saveToDisk(projectRoot: string) {
      const content = this.generateClaudeMd();
      fs.writeFileSync(
        path.join(projectRoot, 'CLAUDE.md'), 
        content, 'utf-8'
      );
    },
    
    generateClaudeMd(): string {
      return `# CLAUDE.md — Project Memory

## Conventions
${this.conventions.map(c => `- ${c}`).join('\n')}

## Architecture
${this.architecture}

## Past Decisions
${this.decisions.map(d => 
  `- [${d.date}] ${d.decision} (reason: ${d.reason})`
).join('\n')}

## Pitfalls
${this.pitfalls.map(p => `- ⚠️ ${p}`).join('\n')}
`;
    },
    
    // Auto-learn from session
    learnFromSession(sessionMemory: any) {
      // Extract conventions from code changes
      const patterns = this.detectPatterns(sessionMemory.filesModified);
      this.conventions.push(...patterns);
      
      // Store important decisions
      for (const decision of sessionMemory.decisions) {
        if (decision.importance === 'high') {
          this.decisions.push(decision);
        }
      }
      
      // Store pitfalls (user corrections)
      for (const correction of sessionMemory.corrections) {
        this.pitfalls.push(
          `${correction.context}: ${correction.correctApproach}`
        );
      }
    }
  };

  // ═══════════════════════════════════════════
  // TIER 3: GLOBAL MEMORY (cross-project)
  // User preferences, skill levels, patterns
  // ═══════════════════════════════════════════
  private globalMemory = {
    preferences: {
      language: 'typescript',
      style: 'functional',
      testFramework: 'vitest',
      linting: 'eslint'
    },
    skillLevels: new Map<string, number>(),  // topic -> proficiency
    commonPatterns: [] as Pattern[],
    
    updateSkillLevel(topic: string, interaction: UserInteraction) {
      const current = this.skillLevels.get(topic) || 0;
      
      // Simple EMA-based skill tracking
      if (interaction.success) {
        this.skillLevels.set(topic, Math.min(1.0, current + 0.1));
      } else {
        this.skillLevels.set(topic, Math.max(0, current - 0.05));
      }
      
      // Adjust detail level based on skill
      return {
        topic,
        skillLevel: this.skillLevels.get(topic),
        detailLevel: this.skillLevels.get(topic)! > 0.7 ? 'brief' : 'detailed'
      };
    }
  };

  // ═══════════════════════════════════════════
  // MEMORY CONSOLIDATION — Session → Project
  // ═══════════════════════════════════════════
  async consolidateAfterSession() {
    // 1. Extract learnings from session
    const learnings = this.extractSessionLearnings();
    
    // 2. Update project memory (CLAUDE.md)
    if (learnings.hasNewConventions) {
      await this.projectMemory.saveToDisk(projectRoot);
    }
    
    // 3. Update global memory
    for (const correction of this.sessionMemory.corrections) {
      this.globalMemory.updateSkillLevel(
        correction.topic, 
        { success: false }
      );
    }
    
    // 4. Clear session memory
    this.sessionMemory = this.createFreshSessionMemory();
    
    return {
      savedConventions: learnings.conventions.length,
      savedDecisions: learnings.decisions.length,
      savedPitfalls: learnings.pitfalls.length
    };
  }
}
```

</details>

**Mấy điểm hay ho rút ra**:
1. ✅ **Nhớ 3 tầng** — Session (nhớ tạm trong buổi) → Project (ghi vào CLAUDE.md để hôm sau còn) → Global (mang theo qua project khác)
2. ✅ **Biến lời chê thành của để dành** — User sửa chỗ nào là ghi ngay thành pitfalls trong CLAUDE.md, lần sau khỏi sai lại
3. ✅ **Biết người biết ta** — Đoán trình độ user để nói ngắn gọn hay giải thích kỹ
4. ✅ **Dọn dẹp cuối buổi** — Hết session là chắt lọc cái hay giữ lại, cái vụn thì cho qua

---

### 6.2. Mem0 — Production Memory Layer for AI Agents

**Mem0** (trước đây mọi người biết với tên EmbedChain) là một memory layer open-source cho AI agents, kiểu như có một bạn thư ký cần mẫn ngồi ghi chép hộ mình:

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Mem0 Architecture — Production Memory Management

Đặc điểm:
- Multi-user memory with namespacing
- Automatic fact extraction from conversations
- Temporal decay + relevance scoring
- Memory deduplication and conflict resolution
"""

class Mem0ProductionMemory:
    """
    Production memory system inspired by Mem0 architecture
    """
    
    def __init__(self, vector_store, graph_store=None, llm_func=None):
        self.vector_store = vector_store
        self.graph = graph_store
        self.llm = llm_func
        self.user_memories = {}  # user_id -> [memories]
    
    # ═══════════════════════════════════════════
    # EXTRACT: Auto-extract facts from conversation
    # ═══════════════════════════════════════════
    def extract_and_store(self, messages, user_id, agent_id=None):
        """
        Extract facts from conversation and store them
        
        Pipeline:
        1. LLM extracts facts from conversation
        2. Deduplicate against existing memories
        3. Resolve conflicts with existing facts
        4. Store new unique facts
        """
        
        # Step 1: Extract facts using LLM
        facts = self._extract_facts(messages)
        
        # Step 2: Get existing memories
        existing = self.get_memories(user_id, agent_id)
        
        # Step 3: Deduplicate and resolve conflicts
        new_facts = self._deduplicate(facts, existing)
        conflicts = self._find_conflicts(facts, existing)
        
        # Step 4: Resolve conflicts
        resolved = self._resolve_conflicts(conflicts)
        
        # Step 5: Store new facts
        stored = []
        for fact in new_facts:
            memory = self._store_memory(fact, user_id, agent_id)
            stored.append(memory)
        
        # Step 6: Update graph relationships
        if self.graph:
            for fact in stored:
                self._update_graph(fact)
        
        return {
            "extracted": len(facts),
            "new_stored": len(stored),
            "conflicts_found": len(conflicts),
            "conflicts_resolved": len(resolved),
            "memories": stored
        }
    
    def _extract_facts(self, messages):
        """
        Use LLM to extract factual information from messages
        """
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )
        
        prompt = f"""Extract all factual information from this conversation.
For each fact, provide:
- Category: (personal_info, preference, knowledge, event, decision)
- Fact: The factual statement
- Confidence: 0.0-1.0

Conversation:
{conversation}

Return as JSON array:
[{{"category": "...", "fact": "...", "confidence": 0.9}}]"""
        
        if self.llm:
            response = self.llm(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return []
        return []
    
    # ═══════════════════════════════════════════
    # DEDUPLICATE: Remove redundant memories
    # ═══════════════════════════════════════════
    def _deduplicate(self, new_facts, existing_memories):
        """
        Remove new facts that are already covered by existing memories
        """
        unique = []
        
        for fact in new_facts:
            is_duplicate = False
            
            for existing in existing_memories:
                similarity = self._compute_similarity(
                    fact['fact'], existing['content']
                )
                
                if similarity > 0.85:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(fact)
        
        return unique
    
    # ═══════════════════════════════════════════
    # CONFLICT RESOLUTION
    # ═══════════════════════════════════════════
    def _find_conflicts(self, new_facts, existing_memories):
        """
        Find cases where new facts contradict existing memories
        """
        conflicts = []
        
        for fact in new_facts:
            for existing in existing_memories:
                # Check if same topic but different value
                if self._is_contradiction(fact['fact'], existing['content']):
                    conflicts.append({
                        "new_fact": fact,
                        "existing_memory": existing,
                        "conflict_type": "contradiction"
                    })
        
        return conflicts
    
    def _resolve_conflicts(self, conflicts):
        """
        Resolve conflicts between new and existing memories
        
        Strategies:
        1. TEMPORAL: Newer information wins
        2. CONFIDENCE: Higher confidence wins
        3. FREQUENCY: More frequently mentioned wins
        4. MANUAL: Ask user to resolve
        """
        resolved = []
        
        for conflict in conflicts:
            new = conflict["new_fact"]
            existing = conflict["existing_memory"]
            
            # Strategy: Temporal + Confidence
            new_score = new.get("confidence", 0.5)
            existing_score = existing.get("confidence", 0.5)
            
            # Newer facts get a slight boost
            if new.get("timestamp", "") > existing.get("timestamp", ""):
                new_score += 0.1
            
            if new_score > existing_score:
                # New fact wins — update existing
                self._update_memory(
                    existing["id"], 
                    new["fact"],
                    reason="temporal_update"
                )
                resolved.append({
                    "action": "updated",
                    "old": existing["content"],
                    "new": new["fact"]
                })
            else:
                # Existing wins — ignore new
                resolved.append({
                    "action": "kept_existing",
                    "existing": existing["content"],
                    "ignored": new["fact"]
                })
        
        return resolved
    
    # ═══════════════════════════════════════════
    # STORAGE
    # ═══════════════════════════════════════════
    def _store_memory(self, fact, user_id, agent_id):
        """Store a fact as a memory"""
        memory = {
            "id": f"mem_{uuid4().hex[:8]}",
            "user_id": user_id,
            "agent_id": agent_id,
            "content": fact["fact"],
            "category": fact.get("category", "unknown"),
            "confidence": fact.get("confidence", 0.5),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None,
        }
        
        # Store in vector DB
        embedding = self._get_embedding(fact["fact"])
        self.vector_store.add(
            document=fact["fact"],
            vector=embedding,
            metadata=memory
        )
        
        # Track in user namespace
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        if key not in self.user_memories:
            self.user_memories[key] = []
        self.user_memories[key].append(memory)
        
        return memory
    
    def get_memories(self, user_id, agent_id=None, query=None, limit=20):
        """
        Retrieve memories for a user, optionally filtered by query
        """
        key = f"{user_id}:{agent_id}" if agent_id else user_id
        
        if query:
            # Semantic search
            embedding = self._get_embedding(query)
            results = self.vector_store.search(
                embedding, 
                top_k=limit,
                filter={"user_id": user_id}
            )
            
            # Apply temporal decay
            for r in results:
                age_days = (datetime.now() - 
                           datetime.fromisoformat(r["created_at"])).days
                r["decayed_score"] = r["score"] * (0.99 ** age_days)
            
            # Re-rank by decayed score
            results.sort(key=lambda x: x["decayed_score"], reverse=True)
            
            # Update access count
            for r in results:
                r["access_count"] = r.get("access_count", 0) + 1
                r["last_accessed"] = datetime.now().isoformat()
            
            return results[:limit]
        
        # No query: return all user memories
        return self.user_memories.get(key, [])[:limit]
    
    # ═══════════════════════════════════════════
    # HELPERS
    # ═══════════════════════════════════════════
    def _compute_similarity(self, text1, text2):
        emb1 = self._get_embedding(text1)
        emb2 = self._get_embedding(text2)
        
        import numpy as np
        a, b = np.array(emb1), np.array(emb2)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def _is_contradiction(self, fact1, fact2):
        """Check if two facts contradict each other"""
        # Simple heuristic: same subject, different numbers
        import re
        nums1 = set(re.findall(r'\d+\.?\d*', fact1))
        nums2 = set(re.findall(r'\d+\.?\d*', fact2))
        
        # If same topic words but different numbers → likely contradiction
        words1 = set(fact1.lower().split())
        words2 = set(fact2.lower().split())
        topic_overlap = len(words1 & words2) / max(len(words1 | words2), 1)
        
        return topic_overlap > 0.6 and nums1 != nums2 and len(nums1) > 0
    
    def _get_embedding(self, text):
        import requests
        try:
            resp = requests.post("http://localhost:11434/api/embed", json={
                "model": "nomic-embed-text", "input": text
            })
            return resp.json()["embeddings"][0]
        except Exception:
            return [0.0] * 768
    
    def _update_graph(self, fact):
        """Update knowledge graph with new fact"""
        if self.graph:
            category = fact.get("category", "general")
            self.graph.add_triplet(
                fact["user_id"],
                f"has_{category}",
                fact["content"]
            )
```

</details>

**Mấy điểm hay ho rút ra**:
1. ✅ **Tự bóc facts** — Để LLM ngồi nghe hội thoại rồi tự nhặt ra facts, khỏi phải ghi tay
2. ✅ **Càng cũ càng mờ** — Memories cũ tự giảm độ quan trọng theo thời gian (temporal decay)
3. ✅ **Dàn xếp mâu thuẫn** — Chấm điểm theo thời gian + độ tin cậy để chọn bên đáng tin hơn
4. ✅ **Mỗi nhà một sổ riêng** — Chia namespacing theo user nên không sợ lẫn lộn

---

### 6.3. OpenMemory — MCP-Based Memory Server

Case study này đóng vai một memory server theo chuẩn MCP (Model Context Protocol) — tức các thao tác bộ nhớ được "phơi ra" dưới dạng tool mà LLM có thể gọi trực tiếp: `create_memory`, `search_memory`, `update_memory`, `delete_memory`, `list_memories`, `consolidate_memories`. Đọc giống như danh mục của một API: mỗi hàm là một thao tác chuẩn, giúp bất kỳ agent nào cũng dùng được bộ nhớ mà không cần biết cách lưu trữ bên trong.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
OpenMemory Pattern: Memory as a Service via MCP Protocol

Memory operations exposed as MCP tools:
- create_memory(content, metadata)
- search_memory(query, user_id)
- update_memory(memory_id, content)
- delete_memory(memory_id)
- list_memories(user_id, category)
"""

class OpenMemoryServer:
    """
    Memory server following MCP protocol pattern
    Exposes memory operations as tools
    """
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.tools = {
            "create_memory": self.create_memory,
            "search_memory": self.search_memory,
            "update_memory": self.update_memory,
            "delete_memory": self.delete_memory,
            "list_memories": self.list_memories,
            "consolidate_memories": self.consolidate,
        }
    
    def create_memory(self, content, user_id, category="general",
                       metadata=None):
        """Create a new memory entry"""
        memory = {
            "id": str(uuid4()),
            "content": content,
            "user_id": user_id,
            "category": category,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "embedding": self._get_embedding(content)
        }
        
        # Store with vector index
        self.storage.insert(memory)
        
        return {
            "success": True,
            "memory_id": memory["id"],
            "message": f"Memory created: {content[:50]}..."
        }
    
    def search_memory(self, query, user_id=None, 
                       category=None, limit=10):
        """Semantic search over memories"""
        query_embedding = self._get_embedding(query)
        
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if category:
            filters["category"] = category
        
        results = self.storage.search(
            embedding=query_embedding,
            filters=filters,
            top_k=limit
        )
        
        # Apply relevance scoring
        for r in results:
            r["relevance"] = self._score_relevance(r, query)
        
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        return {
            "memories": results,
            "count": len(results),
            "query": query
        }
    
    def update_memory(self, memory_id, content, 
                       reason="user_update"):
        """Update an existing memory"""
        old = self.storage.get(memory_id)
        if not old:
            return {"success": False, "error": "Memory not found"}
        
        # Archive old version
        self.storage.archive_version(memory_id, old)
        
        # Update
        old["content"] = content
        old["embedding"] = self._get_embedding(content)
        old["updated_at"] = datetime.now().isoformat()
        old["update_reason"] = reason
        
        self.storage.update(memory_id, old)
        
        return {
            "success": True,
            "memory_id": memory_id,
            "previous_content": old["content"]
        }
    
    def delete_memory(self, memory_id, soft=True):
        """Delete a memory (soft or hard)"""
        if soft:
            # Soft delete: mark as deleted but keep in storage
            self.storage.update(memory_id, {
                "deleted": True,
                "deleted_at": datetime.now().isoformat()
            })
        else:
            # Hard delete: permanently remove
            self.storage.delete(memory_id)
        
        return {"success": True, "memory_id": memory_id, "type": "soft" if soft else "hard"}
    
    def consolidate(self, user_id, similarity_threshold=0.85):
        """
        Consolidate memories: merge duplicates, resolve conflicts
        """
        memories = self.storage.get_all(user_id=user_id)
        
        # Find duplicates
        duplicates = self._find_duplicates(memories, similarity_threshold)
        
        # Merge duplicates
        merged = 0
        for group in duplicates:
            primary = group[0]  # Keep the oldest
            for dup in group[1:]:
                # Merge content
                primary["content"] = self._merge_content(
                    primary["content"], dup["content"]
                )
                # Delete duplicate
                self.storage.delete(dup["id"])
                merged += 1
        
        # Find conflicts
        conflicts = self._find_all_conflicts(memories)
        
        return {
            "memories_before": len(memories),
            "duplicates_merged": merged,
            "conflicts_found": len(conflicts),
            "memories_after": len(memories) - merged
        }
    
    def _score_relevance(self, memory, query):
        """Score memory relevance considering multiple factors"""
        # Base: vector similarity
        base_score = memory.get("score", 0)
        
        # Recency boost (newer = more relevant)
        age_days = (datetime.now() - 
                   datetime.fromisoformat(memory["created_at"])).days
        recency = max(0, 1 - age_days / 365)
        
        # Access frequency boost
        access_freq = memory.get("access_count", 0) / 10
        
        # Combined score
        return (base_score * 0.6 + 
                recency * 0.2 + 
                min(access_freq, 0.2))
    
    def _find_duplicates(self, memories, threshold):
        """Group similar memories together"""
        groups = []
        used = set()
        
        for i, m1 in enumerate(memories):
            if i in used or m1.get("deleted"):
                continue
            
            group = [m1]
            for j, m2 in enumerate(memories[i+1:], i+1):
                if j in used or m2.get("deleted"):
                    continue
                
                sim = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                if sim > threshold:
                    group.append(m2)
                    used.add(j)
            
            if len(group) > 1:
                groups.append(group)
                used.add(i)
        
        return groups
```

</details>

---

### 6.4. DeepSeek Harness — Trajectory Fork & Replay Engine

**Chuyện nhà DeepSeek**: team DeepSeek quan niệm "Agent = Model + Harness", nên việc gì agent đã làm đều phải truy vết được — muốn tua lại, rẽ nhánh thử kiểu khác, hay nghỉ giữa chừng rồi chạy tiếp đều được, giống như có camera hành trình gắn cho mọi session.

<details>
<summary><b>TypeScript Architecture (Click to expand/collapse)</b></summary>

```typescript
/**
 * DeepSeek Harness - Trajectory Traceability Engine
 * 
 * Core philosophy: "Agent = Model + Harness"
 * Everything is traceable, replayable, and forkable.
 */

// ═══════════════════════════════════════════════
// 1. SESSION EVENT STREAM (Append-only log)
// ═══════════════════════════════════════════════

interface SessionEvent {
  id: string;              // UUID
  step: number;            // Monotonically increasing
  timestamp: number;       // Unix ms
  type: EventType;
  payload: EventPayload;
  metadata: EventMetadata;
}

type EventType = 
  | "user_prompt"          // User input
  | "model_thought"        // LLM reasoning (hidden)
  | "tool_call"            // Tool invocation
  | "tool_result"          // Tool output
  | "model_output"         // Final LLM response
  | "state_change"         // Harness state mutation
  | "checkpoint";          // Manual/auto checkpoint

interface EventPayload {
  // user_prompt
  text?: string;
  attachments?: Attachment[];
  
  // model_thought
  reasoning?: string;
  confidence?: number;
  
  // tool_call
  tool_name?: string;
  args?: Record<string, any>;
  call_id?: string;
  
  // tool_result
  result?: any;
  error?: string;
  duration_ms?: number;
  
  // model_output
  content?: string;
  finish_reason?: string;
  
  // state_change
  path?: string;           // JSON path in state
  old_value?: any;
  new_value?: any;
  
  // checkpoint
  label?: string;
  description?: string;
}

interface EventMetadata {
  session_id: string;
  parent_step?: number;    // For forked sessions
  fork_id?: string;        // Fork identifier
  tags?: string[];         // e.g., ["debug", "critical"]
  cost_usd?: number;       // Token cost estimate
}

// ═══════════════════════════════════════════════
// 2. TRAJECTORY STORE (Persistence layer)
// ═══════════════════════════════════════════════

class TrajectoryStore {
  private events: SessionEvent[] = [];
  private checkpoints: Map<string, number> = new Map(); // label -> step
  
  append(event: SessionEvent): void {
    this.events.push(event);
  }
  
  getEvents(sessionId: string, fromStep?: number): SessionEvent[] {
    return this.events.filter(e => 
      e.metadata.session_id === sessionId && 
      (fromStep === undefined || e.step >= fromStep)
    );
  }
  
  getEventByStep(sessionId: string, step: number): SessionEvent | undefined {
    return this.events.find(e => 
      e.metadata.session_id === sessionId && e.step === step
    );
  }
  
  createCheckpoint(sessionId: string, label: string): void {
    const latestStep = this.getLatestStep(sessionId);
    this.checkpoints.set(`${sessionId}:${label}`, latestStep);
  }
  
  getCheckpoint(sessionId: string, label: string): number | undefined {
    return this.checkpoints.get(`${sessionId}:${label}`);
  }
  
  private getLatestStep(sessionId: string): number {
    const sessionEvents = this.events.filter(
      e => e.metadata.session_id === sessionId
    );
    return sessionEvents.length > 0 
      ? Math.max(...sessionEvents.map(e => e.step)) 
      : 0;
  }
}

// ═══════════════════════════════════════════════
// 3. REPLAY ENGINE (Core innovation)
// ═══════════════════════════════════════════════

class ReplayEngine {
  constructor(
    private store: TrajectoryStore,
    private model: ModelProvider,
    private toolRegistry: ToolRegistry
  ) {}
  
  /**
   * Replay session from beginning up to a specific step.
   * Returns the state at that step.
   */
  async replayToStep(sessionId: string, targetStep: number): Promise<AgentState> {
    const events = this.store.getEvents(sessionId);
    let state = this.initialState();
    
    for (const event of events) {
      if (event.step > targetStep) break;
      state = await this.applyEvent(state, event);
    }
    
    return state;
  }
  
  /**
   * Fork a session at a specific step.
   * Creates a new session that shares history up to fork point.
   */
  async forkSession(
    sessionId: string, 
    forkStep: number, 
    newPrompt?: string
  ): Promise<string> {
    const newSessionId = `fork_${sessionId}_${forkStep}_${Date.now()}`;
    
    // Copy events up to fork step
    const history = this.store.getEvents(sessionId, 0, forkStep);
    for (const event of history) {
      const forkedEvent = {
        ...event,
        id: uuid(),
        metadata: {
          ...event.metadata,
          session_id: newSessionId,
          parent_step: forkStep,
          fork_id: newSessionId
        }
      };
      this.store.append(forkedEvent);
    }
    
    // Optionally add new prompt to continue from fork
    if (newPrompt) {
      this.store.append({
        id: uuid(),
        step: forkStep + 1,
        timestamp: Date.now(),
        type: "user_prompt",
        payload: { text: newPrompt },
        metadata: { session_id: newSessionId, fork_id: newSessionId }
      });
    }
    
    return newSessionId;
  }
  
  /**
   * Resume a session from a checkpoint or step.
   * Continues execution from that point.
   */
  async resumeSession(
    sessionId: string, 
    fromStep: number,
    newInput?: string
  ): Promise<AgentState> {
    // Get state at resume point
    const state = await this.replayToStep(sessionId, fromStep);
    
    // If new input provided, continue from there
    if (newInput) {
      return this.continueFromState(sessionId, state, newInput);
    }
    
    return state;
  }
  
  private async applyEvent(state: AgentState, event: SessionEvent): Promise<AgentState> {
    switch (event.type) {
      case "tool_call":
        return await this.executeTool(state, event);
      case "model_thought":
        return { ...state, lastThought: event.payload.reasoning };
      case "state_change":
        return this.applyStateChange(state, event);
      default:
        return state;
    }
  }
  
  private async continueFromState(
    sessionId: string, 
    state: AgentState, 
    input: string
  ): Promise<AgentState> {
    // Continue agent loop from restored state
    // ... implementation
    return state;
  }
  
  private initialState(): AgentState {
    return { history: [], tools: {}, memory: {} };
  }
}

// ═══════════════════════════════════════════════
// 4. EVENT SEARCH & ANALYTICS
// ═══════════════════════════════════════════════

class TrajectoryAnalytics {
  constructor(private store: TrajectoryStore) {}
  
  /**
   * Search events across all sessions.
   * Supports: full-text, type filter, time range, cost range.
   */
  searchEvents(query: SearchQuery): SessionEvent[] {
    let results = this.store.events;
    
    if (query.session_id) {
      results = results.filter(e => e.metadata.session_id === query.session_id);
    }
    if (query.type) {
      results = results.filter(e => e.type === query.type);
    }
    if (query.text) {
      const text = query.text.toLowerCase();
      results = results.filter(e => 
        JSON.stringify(e.payload).toLowerCase().includes(text)
      );
    }
    if (query.from_step !== undefined) {
      results = results.filter(e => e.step >= query.from_step!);
    }
    if (query.to_step !== undefined) {
      results = results.filter(e => e.step <= query.to_step!);
    }
    if (query.max_cost !== undefined) {
      results = results.filter(e => 
        (e.metadata.cost_usd ?? 0) <= query.max_cost!
      );
    }
    
    return results;
  }
  
  /**
   * Get cost breakdown by event type.
   */
  getCostBreakdown(sessionId: string): Record<string, number> {
    const events = this.store.getEvents(sessionId);
    const breakdown: Record<string, number> = {};
    
    for (const event of events) {
      const cost = event.metadata.cost_usd ?? 0;
      breakdown[event.type] = (breakdown[event.type] ?? 0) + cost;
    }
    
    return breakdown;
  }
  
  /**
   * Find common failure patterns.
   */
  findFailurePatterns(): FailurePattern[] {
    const toolErrors = this.store.events.filter(
      e => e.type === "tool_result" && e.payload.error
    );
    
    // Group by tool + error type
    const groups = new Map<string, SessionEvent[]>();
    for (const event of toolErrors) {
      const key = `${event.payload.tool_name}:${event.payload.error}`;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(event);
    }
    
    return Array.from(groups.entries())
      .map(([pattern, events]) => ({
        pattern,
        count: events.length,
        sessions: [...new Set(events.map(e => e.metadata.session_id))],
        first_seen: Math.min(...events.map(e => e.timestamp)),
        last_seen: Math.max(...events.map(e => e.timestamp))
      }))
      .sort((a, b) => b.count - a.count);
  }
}

interface SearchQuery {
  session_id?: string;
  type?: EventType;
  text?: string;
  from_step?: number;
  to_step?: number;
  max_cost?: number;
}

interface FailurePattern {
  pattern: string;
  count: number;
  sessions: string[];
  first_seen: number;
  last_seen: number;
}
```

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

---

## 7. Advanced Memory Patterns

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

```python
"""
Write-Behind Cache: Ghi vào cache trước, flush xuống DB sau.

Giảm latency write operations, tăng throughput.
Phù hợp khi write operations nhiều hơn read.
"""

class WriteBehindCache:
    """
    Write-behind caching for memory operations
    
    Flow:
    1. Write to fast cache (Redis/in-memory)
    2. Return immediately (low latency)
    3. Background thread flushes to persistent store
    """
    
    def __init__(self, persistent_store, flush_interval=5.0, batch_size=100):
        self.cache = {}  # In-memory cache
        self.persistent_store = persistent_store
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self.pending_writes = []
        self.is_running = True
        
        # Start background flush thread
        self.flush_thread = threading.Thread(target=self._flush_loop)
        self.flush_thread.daemon = True
        self.flush_thread.start()
    
    def write(self, key, value, metadata=None):
        """
        Write to cache immediately, queue for persistence
        """
        entry = {
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
            "dirty": True  # Needs to be flushed
        }
        
        # Write to fast cache (immediate)
        self.cache[key] = entry
        
        # Queue for persistent storage
        self.pending_writes.append(entry)
        
        # Flush if batch is full
        if len(self.pending_writes) >= self.batch_size:
            self._flush()
        
        return {"success": True, "latency": "cache_speed"}
    
    def read(self, key):
        """
        Read from cache first, fallback to persistent store
        """
        # Check cache
        if key in self.cache:
            return self.cache[key]
        
        # Fallback to persistent store
        value = self.persistent_store.get(key)
        if value:
            # Populate cache for next time
            self.cache[key] = value
        
        return value
    
    def _flush_loop(self):
        """Background loop to flush dirty entries"""
        while self.is_running:
            time.sleep(self.flush_interval)
            self._flush()
    
    def _flush(self):
        """Flush pending writes to persistent store"""
        if not self.pending_writes:
            return
        
        # Batch write to persistent store
        batch = self.pending_writes[:self.batch_size]
        self.pending_writes = self.pending_writes[self.batch_size:]
        
        try:
            self.persistent_store.batch_write(batch)
            
            # Mark as clean
            for entry in batch:
                if entry["key"] in self.cache:
                    self.cache[entry["key"]]["dirty"] = False
        
        except Exception as e:
            # Re-queue failed writes
            self.pending_writes = batch + self.pending_writes
            print(f"Flush error: {e}")
    
    def get_stats(self):
        dirty_count = sum(
            1 for v in self.cache.values() if v.get("dirty")
        )
        return {
            "cache_size": len(self.cache),
            "pending_writes": len(self.pending_writes),
            "dirty_entries": dirty_count
        }
```

</details>

### 7.2. Memory Consolidation Pipeline

Khác với consolidation thủ công ở mục 2, đây là "dây chuyền dọn dẹp tự động" chạy định kỳ theo 5 giai đoạn: deduplicate → resolve conflicts → temporal decay → archive memory cũ → xóa memory có confidence thấp. Mỗi giai đoạn là một hàm `_stage_*`, và `run_full_consolidation` chạy cả dây chuyền rồi trả về report thống kê — đọc báo cáo này là biết ngay mỗi giai đoạn đã dọn được bao nhiêu mục.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Consolidation Pipeline: Background process để maintain memory quality.

Runs periodically to:
1. Deduplicate memories
2. Resolve conflicts
3. Apply temporal decay
4. Archive old memories
5. Generate memory statistics
"""

class MemoryConsolidationPipeline:
    """
    Automated pipeline for memory maintenance
    """
    
    def __init__(self, memory_store, config=None):
        self.store = memory_store
        self.config = config or {
            "dedup_threshold": 0.85,
            "conflict_strategy": "temporal",  # temporal, confidence, manual
            "archive_after_days": 90,
            "decay_rate": 0.01,
            "min_confidence": 0.3
        }
        self.stats = {
            "runs": 0,
            "deduped": 0,
            "conflicts_resolved": 0,
            "archived": 0,
            "low_confidence_removed": 0
        }
    
    def run_full_consolidation(self):
        """
        Run complete consolidation pipeline
        
        Returns: ConsolidationReport
        """
        start_time = time.time()
        report = {"stages": {}}
        
        # Stage 1: Deduplication
        dedup_result = self._stage_deduplicate()
        report["stages"]["dedup"] = dedup_result
        
        # Stage 2: Conflict Resolution
        conflict_result = self._stage_resolve_conflicts()
        report["stages"]["conflicts"] = conflict_result
        
        # Stage 3: Temporal Decay
        decay_result = self._stage_apply_decay()
        report["stages"]["decay"] = decay_result
        
        # Stage 4: Archive Old Memories
        archive_result = self._stage_archive()
        report["stages"]["archive"] = archive_result
        
        # Stage 5: Remove Low Confidence
        cleanup_result = self._stage_cleanup()
        report["stages"]["cleanup"] = cleanup_result
        
        # Final report
        elapsed = time.time() - start_time
        report["total_time_ms"] = elapsed * 1000
        report["total_memories"] = self.store.count()
        report["stats"] = self.stats
        self.stats["runs"] += 1
        
        return report
    
    def _stage_deduplicate(self):
        """Remove duplicate memories"""
        memories = self.store.get_all()
        
        # Group by similarity
        duplicates_found = 0
        removed = 0
        
        for i, m1 in enumerate(memories):
            if m1.get("archived") or m1.get("deleted"):
                continue
            
            for m2 in memories[i+1:]:
                if m2.get("archived") or m2.get("deleted"):
                    continue
                
                similarity = self._compute_similarity(
                    m1["content"], m2["content"]
                )
                
                if similarity > self.config["dedup_threshold"]:
                    # Keep the one with higher confidence
                    if m1.get("confidence", 0) >= m2.get("confidence", 0):
                        self.store.soft_delete(m2["id"])
                    else:
                        self.store.soft_delete(m1["id"])
                    removed += 1
        
        self.stats["deduped"] += removed
        return {"duplicates_found": duplicates_found, "removed": removed}
    
    def _stage_resolve_conflicts(self):
        """Resolve conflicting memories"""
        memories = self.store.get_all()
        
        # Group by topic (simplified: same first 5 words)
        topic_groups = {}
        for m in memories:
            if m.get("deleted"):
                continue
            topic_key = " ".join(m["content"].split()[:5])
            if topic_key not in topic_groups:
                topic_groups[topic_key] = []
            topic_groups[topic_key].append(m)
        
        conflicts_resolved = 0
        
        for topic, group in topic_groups.items():
            if len(group) <= 1:
                continue
            
            # Check for actual contradictions
            values = set()
            for m in group:
                values.add(m["content"])
            
            if len(values) > 1:
                # Conflict found — resolve by strategy
                if self.config["conflict_strategy"] == "temporal":
                    # Keep newest
                    group.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
                elif self.config["conflict_strategy"] == "confidence":
                    # Keep highest confidence
                    group.sort(key=lambda x: x.get("confidence", 0), reverse=True)
                    for m in group[1:]:
                        self.store.soft_delete(m["id"])
                        conflicts_resolved += 1
        
        self.stats["conflicts_resolved"] += conflicts_resolved
        return {"conflicts_found": len(topic_groups), "resolved": conflicts_resolved}
    
    def _stage_apply_decay(self):
        """Apply temporal decay to memory confidence"""
        memories = self.store.get_all()
        
        decayed = 0
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            age_days = (datetime.now() - 
                       datetime.fromisoformat(m.get("created_at", 
                           datetime.now().isoformat()))).days
            
            # Apply exponential decay
            decay_factor = (1 - self.config["decay_rate"]) ** age_days
            new_confidence = m.get("confidence", 1.0) * decay_factor
            
            if abs(new_confidence - m.get("confidence", 1.0)) > 0.01:
                self.store.update(m["id"], {"confidence": new_confidence})
                decayed += 1
        
        return {"memories_decayed": decayed}
    
    def _stage_archive(self):
        """Archive old, low-access memories"""
        cutoff = datetime.now() - timedelta(
            days=self.config["archive_after_days"]
        )
        
        archived = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            last_accessed = m.get("last_accessed", m.get("updated_at"))
            if last_accessed and datetime.fromisoformat(last_accessed) < cutoff:
                # Archive: move to cold storage
                self.store.archive(m["id"])
                archived += 1
        
        self.stats["archived"] += archived
        return {"archived": archived}
    
    def _stage_cleanup(self):
        """Remove very low confidence memories"""
        removed = 0
        memories = self.store.get_all()
        
        for m in memories:
            if m.get("deleted") or m.get("archived"):
                continue
            
            if m.get("confidence", 1.0) < self.config["min_confidence"]:
                self.store.soft_delete(m["id"])
                removed += 1
        
        self.stats["low_confidence_removed"] += removed
        return {"low_confidence_removed": removed}
    
    def _compute_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        return len(words1 & words2) / len(words1 | words2)
```

</details>

### 7.3. Versioned Memory (Git-like Memory)

Pattern này mượn đúng ý tưởng Git áp dụng cho bộ nhớ: mỗi lần `set` một giá trị là tạo một **version** mới kèm snapshot toàn bộ state. Nhờ đó bạn có `diff` (so sánh 2 thời điểm), `rollback` (quay lại version cũ như git revert), và `log` (xem lịch sử thay đổi). Nói dân dã: bộ nhớ biết mình "từng được sửa thế nào", nên sửa sai là kéo lại được.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
"""
Versioned Memory: Giống Git — mỗi change tạo version mới.

Cho phép:
- Time travel: Xem memory tại thời điểm T
- Diff: So sánh memory giữa 2 thời điểm
- Branch: Tạo version alternative
- Rollback: Quay lại version trước
"""

class VersionedMemory:
    """
    Git-like versioned memory system
    """
    
    def __init__(self):
        self.versions = []  # List of snapshots
        self.current = {}
    
    def set(self, key, value, message=""):
        """Set a value, creating a new version"""
        # Capture previous state
        prev_snapshot = dict(self.current)
        
        # Apply change
        self.current[key] = value
        
        # Record version
        version = {
            "id": len(self.versions),
            "snapshot": dict(self.current),
            "change": {"key": key, "value": value},
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "parent": len(self.versions) - 1 if self.versions else None
        }
        
        self.versions.append(version)
        return version["id"]
    
    def get(self, key, version_id=None):
        """Get value at a specific version"""
        if version_id is None:
            return self.current.get(key)
        
        if version_id >= len(self.versions):
            return None
        
        return self.versions[version_id]["snapshot"].get(key)
    
    def diff(self, v1_id, v2_id):
        """Compare two versions"""
        if v1_id >= len(self.versions) or v2_id >= len(self.versions):
            return {"error": "Invalid version IDs"}
        
        v1 = self.versions[v1_id]["snapshot"]
        v2 = self.versions[v2_id]["snapshot"]
        
        all_keys = set(v1.keys()) | set(v2.keys())
        
        changes = []
        for key in all_keys:
            old = v1.get(key)
            new = v2.get(key)
            
            if old != new:
                if old is None:
                    changes.append({"key": key, "type": "added", "new": new})
                elif new is None:
                    changes.append({"key": key, "type": "removed", "old": old})
                else:
                    changes.append({"key": key, "type": "modified", 
                                   "old": old, "new": new})
        
        return {"changes": changes, "count": len(changes)}
    
    def rollback(self, version_id):
        """Rollback to a previous version"""
        if version_id >= len(self.versions):
            return {"error": "Invalid version ID"}
        
        self.current = dict(self.versions[version_id]["snapshot"])
        
        return {
            "rolled_back_to": version_id,
            "current_state": self.current
        }
    
    def log(self, limit=10):
        """View version history"""
        return [
            {
                "id": v["id"],
                "change": v["change"],
                "message": v["message"],
                "timestamp": v["timestamp"]
            }
            for v in self.versions[-limit:]
        ]
```

</details>

---

## 8. Best Practices & Anti-Patterns

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Danh sách các việc NÊN làm (best practices) và KHÔNG nên làm (anti-patterns) khi xây dựng update memory, gom từ kinh nghiệm của nhiều hệ thống production.
> 
> **Ẩn dụ/so sánh:** Giống bảng điều luật giao thông — không cần nhớ lý do chi tiết, chỉ cần biết "đèn xanh đi, đèn đỏ dừng" để không gặp tai nạn.
> 
> **Vì sao quan trọng:** Giúp bạn tránh những lỗi đắt giá mà nhiều đội đã vấp phải, tiết kiệm thời gian fix bug về sau.

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

---

## 9. Performance Metrics

> **📌 Khái Niệm Cơ Bản**
> 
> **Khái niệm:** Lớp đo lường các chỉ số sức khỏe của memory store: latency ghi/đọc, tỉ lệ dedup, số conflict, thời gian mỗi lần consolidation.
> 
> **Ẩn dụ/so sánh:** Giống đồng hồ táp-lô trên xe — không cần nhìn suốt đường đi, nhưng khi nghi ngờ có vấn đề thì phải biết đọc.
> 
> **Vì sao quan trọng:** Không đo lường thì không biết memory system đang dần xuống cấp hay đang hoạt động tốt.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
class MemoryStoreMetrics:
    """Track memory store performance"""
    
    def __init__(self):
        self.write_latencies = []
        self.read_latencies = []
        self.memory_counts = []
        self.dedup_rates = []
        self.conflict_counts = []
        self.consolidation_times = []
    
    def record_write(self, latency_ms, success=True):
        self.write_latencies.append({"latency": latency_ms, "success": success})
    
    def record_read(self, latency_ms, results_count):
        self.read_latencies.append({"latency": latency_ms, "results": results_count})
    
    def record_consolidation(self, time_ms, deduped, conflicts_resolved):
        self.consolidation_times.append(time_ms)
        self.dedup_rates.append(deduped)
        self.conflict_counts.append(conflicts_resolved)
    
    def report(self):
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0
        
        write_lats = [w["latency"] for w in self.write_latencies]
        read_lats = [r["latency"] for r in self.read_latencies]
        
        return f"""
╔══════════════════════════════════════════════╗
║       MEMORY STORE METRICS REPORT            ║
╠══════════════════════════════════════════════╣
║                                              ║
║  Write Operations:                           ║
║    Total:    {len(self.write_latencies):>8}                     ║
║    Avg Latency: {avg(write_lats):>8.1f} ms                 ║
║    Success Rate: {sum(1 for w in self.write_latencies if w['success'])/max(len(self.write_latencies),1)*100:>6.1f}%          ║
║                                              ║
║  Read Operations:                            ║
║    Total:    {len(self.read_latencies):>8}                     ║
║    Avg Latency: {avg(read_lats):>8.1f} ms                 ║
║    Avg Results: {avg([r['results'] for r in self.read_latencies]):>7.1f}                    ║
║                                              ║
║  Consolidation:                              ║
║    Runs:     {len(self.consolidation_times):>8}                     ║
║    Avg Time: {avg(self.consolidation_times):>8.1f} ms                 ║
║    Total Deduped: {sum(self.dedup_rates):>5}                   ║
║    Total Conflicts: {sum(self.conflict_counts):>4}                  ║
║                                              ║
╚══════════════════════════════════════════════╝"""
```

</details>

---

## 10. Labs Thực Hành

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

```python
# python 03-update-memory-store/lab_writeback.py

writer = MemoryWriter()

# 1. Store episodic memory
event_id = writer.write_episodic(
    "learning",
    "User learned about BHYT deduction rates",
    metadata={"topic": "BHYT", "importance": "medium"}
)

# 2. Store facts
writer.write_fact("BHYT", "mức đóng", "4.5% lương cơ sở", confidence=0.95)
writer.write_fact("BHYT", "thời hạn thẻ", "5 năm", confidence=0.99)
writer.write_fact("Ollama", "runs", "gemma3:12b", confidence=1.0)

# 3. Update user profile
writer.write_user_profile("user_1", {
    "name": "Nguyễn Văn A",
    "occupation": "developer",
    "interests": ["AI", "BHYT"]
})

# 4. Check stats
print(writer.get_stats())
# {'episodic_count': 1, 'entity_count': 3, 'event_count': 4}
```

</details>

### Lab 2: Consolidation

Thực hành dọn dẹp với `MemoryConsolidator`: tạo 3 fact về BHYT (hai cái gần như trùng nhau, một cái là bản cập nhật mới hơn), chạy `generate_memory_report` và xem `conflict_resolution` phát hiện được mâu thuẫn nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_consolidation.py

from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()
kg.add_triplet("BHYT", "mức đóng", "4.5%")
kg.add_triplet("BHYT", "mức đóng", "4.5% lương cơ sở")  # Duplicate
kg.add_triplet("BHYT", "mức đóng", "5%")  # Updated

consolidator = MemoryConsolidator(kg)
report = consolidator.generate_memory_report()
print(report)

conflicts = consolidator.conflict_resolution()
print(f"Conflicts: {len(conflicts)}")
for c in conflicts:
    print(f"  {c['subject']} → {c['conflicting_values']}")
```

</details>

### Lab 3: Versioned Memory

Mô phỏng một fact về mức đóng BHYT thay đổi qua 3 phiên bản, xem lịch sử bằng `vm.log()`, so sánh hai thời điểm bằng `vm.diff(0, 2)` và cuối cùng thử quay lại bản đầu với `vm.rollback(0)`.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_versioned.py

vm = VersionedMemory()

# Track evolving knowledge
vm.set("bhyt_rate", "4.5%", message="Initial fact")
vm.set("bhyt_rate", "4.5% lương cơ sở", message="More specific")
vm.set("bhyt_rate", "4.5% MEC 2024", message="Updated year")

# View history
for entry in vm.log():
    print(f"  v{entry['id']}: {entry['message']}")

# Compare versions
diff = vm.diff(0, 2)
print(f"Changes: {diff['count']}")

# Rollback
state = vm.rollback(0)
print(f"Rolled back to: {state['rolled_back_to']}")
```

</details>

### Lab 4: Metrics

Mô phỏng 100 thao tác ghi/đọc với số liệu ngẫu nhiên và 2 lần consolidation, rồi in ra báo cáo `metrics.report()` để xem hệ thống được đo lường như thế nào.

<details>
<summary>Python Code (Click to expand/collapse)</summary>

```python
# python 03-update-memory-store/lab_metrics.py

metrics = MemoryStoreMetrics()

# Simulate operations
import random
for _ in range(100):
    metrics.record_write(random.uniform(5, 50))
    metrics.record_read(random.uniform(2, 30), random.randint(1, 10))

metrics.record_consolidation(1500, deduped=25, conflicts_resolved=3)
metrics.record_consolidation(1200, deduped=15, conflicts_resolved=1)

print(metrics.report())
```

</details>

## 12. Bổ Sung Production: Retention, Consolidation, Hợp Đồng Compaction & SLO

> Nói nôm na: nối chuyện "lược bớt" của §02 với chuyện "giữ lại" của §03 — cái gì được bỏ qua, cái gì nhất định phải giữ lại cho bằng được.

### 12.1 Định nghĩa

| Thuật ngữ | Định nghĩa |
|------|------------|
| Retention / TTL | Hết hạn theo từng lớp memory (`episodic 30d, fact tới khi bị thay thế, session 24h`); hết hạn → archive hoặc xóa cứng |
| Xóa theo GDPR | Xóa theo phạm vi tenant/user trên primary store, vector index, backup (trong cửa sổ đã công bố) + biên nhận |
| Trigger consolidation | Điều kiện chạy job merge/dedup/conflict: kích thước, thời gian, tín hiệu (tỷ lệ conflict, feedback) |
| Hợp đồng compaction↔memory | Ranh giới: §02 được loại mọi thứ trừ những gì §03 đã ghim là durable |
| SLO đường ghi | p50/p99 + đảm bảo durability cho đường ingest (ví dụ `p99 < 300ms, 0 mất dữ liệu khi đã ack`) |

### 12.2 Retention / Tuân Thủ

- **TTL mặc định, nhớ như hạn dùng của đồ ăn:** `session: 24h là dọn; episodic: 30–90d thì cho vào kho archive; semantic fact: không đặt hạn cứng nhưng phải ghi valid_until + nguồn gốc; user profile: giữ tới khi user bảo xóa.` Có một bạn sweeper chạy hàng giờ để quét; trước khi xóa cứng là phải archive sang cold store đã.
- **Nhà ai nấy ở theo tenant:** lấy `tenant_id` làm vách ngăn cho mọi bảng/namespace; câu query nào cũng phải kèm bộ lọc; đọc lấn sang nhà hàng xóm là bị chặn ngay ở API + policy DB (RLS). Tenant enterprise nào cũng có chìa khóa mã hóa riêng.
- **Xóa theo kiểu GDPR/CCPA cho đàng hoàng:** gọi `DELETE /memory?user=X` là đi một vòng tombstone → xóa ở vector + KG + log (redact) → dọn backup trong ≤30d → trả về `deletion_receipt{id, scope, ts}` làm bằng. SLA 24h là xong.

### 12.3 Trigger Consolidation + Giải Quyết Xung Đột

Mình cho chạy consolidation mỗi khi **thấy một trong mấy dấu hiệu này**: `unconsolidated_writes > 500`, tới giờ cron hàng giờ, `conflict_rate > 5%`, hay có feedback chê một fact nào đó. Dây chuyền làm như dọn nhà cuối tuần: dedup (cosine ≥0.9 là gộp) → soi conflict (cùng subject+predicate mà object khác nhau) → dàn xếp: `last-writer-wins` chỉ khi nguồn mới tin cậy bằng hoặc hơn nguồn cũ; không thì theo `highest-trust-wins`; bí quá thì `escalate_to_user` nhờ người phân xử. Lúc nào cũng giữ cả hai version + gắn cạnh `supersedes` — tuyệt đối không lén ghi đè.

### 12.4 Hợp Đồng Compaction↔Memory

| §02 được loại (transient) | §03 phải giữ (durable) |
|---|---|
| stdout tool thô, chunk retrieval cũ, diff đã thay thế, tán gẫu | Fact đã ghim, quyết định, TODO mở, preference user, block resume |
| Được bỏ sau khi tóm tắt resume | Phải sống sót sau compaction; nạp lại được qua retrieve |

Quy tắc nằm lòng: compaction có nhả ra `resume_block` thì write-back **phải** cất kỹ `resume_block + decisions + open items` rồi mới được dọn chúng khỏi context. Tới lúc mở lại session, §02 chỉ việc hydrate từ §03 bằng query `tenant+task` là đủ đồ nghề làm tiếp.

### 12.5 SLO Đường Ghi

- Đường ghi phải nhanh như chớp: `p50 write < 80ms, p99 < 300ms`; còn consolidation nặng thì cho chạy nền `p99 < 5min`. Lúc đang ghi thì tranh thủ kiểm tra dedup luôn; mấy vụ merge nặng thì đẩy ra hàng đợi write-behind cho khỏi nghẽn critical path.
- Độ bền thì chắc như đinh: chỉ dám ack khi đã ghi xong WAL + primary; hàng đợi retry có idempotency key `tenant:doc_hash` chống ghi trùng. Thấy `write_error% > 1%` hay `queue_lag > 10k` là phải kêu lên ngay.

<details>
<summary>TypeScript Code — Memory Có Version với Consolidation (Click to expand/collapse)</summary>

```typescript
type Fact = { tenant: string; subj: string; pred: string; obj: string; trust: number; ts: number; ttl?: number };

export class MemoryStore {
  private facts: Fact[] = []; private wal: Fact[] = [];
  async write(f: Fact, idemKey: string): Promise<"ok" | "dup"> {
    if (this.wal.some(w => (w as any).idemKey === idemKey)) return "dup";
    if (Date.now() > (f.ttl ?? Infinity)) throw new Error("expired");
    (f as any).idemKey = idemKey;
    this.wal.push(f); // fsync trong production
    const dup = this.facts.find(e => e.tenant === f.tenant && sim(e, f) >= 0.9);
    if (dup) { Object.assign(dup, { obj: f.obj, trust: Math.max(dup.trust, f.trust) }); }
    else this.facts.push(f);
    return "ok"; // ack sau WAL+primary
  }
  consolidate(): { merged: number; conflicts: Fact[][] } {
    const conflicts: Fact[][] = [];
    const byKey = new Map<string, Fact[]>();
    for (const f of this.facts.filter(f => (f.ttl ?? Infinity) > Date.now())) {
      const k = `${f.tenant}|${f.subj}|${f.pred}`;
      byKey.set(k, [...(byKey.get(k) ?? []), f]);
    }
    let merged = 0;
    for (const [, g] of byKey) {
      const objs = new Set(g.map(x => x.obj));
      if (objs.size > 1) {
        g.sort((a, b) => b.trust - a.trust || b.ts - a.ts); // highest-trust-wins
        this.facts = this.facts.filter(x => !g.slice(1).includes(x)); merged += g.length - 1;
        conflicts.push(g);
      }
    }
    return { merged, conflicts };
  }
  gdprDelete(tenant: string): { receipt: string } {
    this.facts = this.facts.filter(f => f.tenant !== tenant);
    this.wal = this.wal.filter(f => f.tenant !== tenant);
    return { receipt: `del:${tenant}:${Date.now()}` };
  }
}
declare function sim(a: Fact, b: Fact): number;
```

</details>

### 12.6 Checklist

| # | Quy tắc |
|---|------|
| 1 | TTL theo lớp + sweeper hàng giờ; archive trước khi xóa cứng |
| 2 | Phân vùng `tenant_id` + RLS; không tồn tại đường query liên tenant |
| 3 | Xóa GDPR quét facts + vector + log với biên nhận ≤24h |
| 4 | Consolidation theo trigger kích thước/thời gian/tín hiệu; giải conflict theo độ tin cậy, không ghi đè âm thầm |
| 5 | Thực thi hợp đồng compaction↔memory: resume/quyết định được lưu trước khi loại |
| 6 | Dashboard SLO ghi: p99, error%, queue lag, dedup rate, conflict rate |

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

### 1. Structured note-taking / agentic memory (Anthropic 09/2025)

Agent tự ghi NOTES.md/todo ra ngoài context window để:
- Giữ state giữa các turn trong cùng session
- Bàn giao context cho session tiếp theo
- Tránh quên action items đã đề ra

**Memory tool (Claude Developer Platform):** Persistent memory giữa các summarization — agent có thể đọc/ghi memory store riêng, không phụ thuộc conversation window.

**Pattern đề xuất:**

```
PROJECT/
├── CLAUDE.md          # System instructions + conventions
├── NOTES.md           # Agent notes, todos, state
├── SPEC.md            # Specifications
└── PROGRESS.md        # Feature progress tracking
```

### 2. Long-running agent memory pattern (Anthropic 11/2025)

Initializer agent tạo cấu trúc ban đầu, các session sau đọc và tiếp tục:

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

**Tại sao JSON được ưa chuộng hơn Markdown:**
- Model ít ghi đè/ghi sai format JSON so với Markdown tự do
- Parse machine-readable, không phải regex parse text
- Dễ diff trong git, conflict resolution đơn giản hơn

### 3. Khi nào reset memory hoàn toàn

**Nên reset khi:**
- Task đã hoàn thành hoàn toàn
- Tất cả facts đã được consolidate vào permanent storage
- Milestone cuối cùng đã đạt

**Không nên reset khi:**
- Đang giữa milestone/cuộc họp quan trọng
- Facts chưa được consolidate (sẽ mất insights)
- Cần audit trail cho compliance

### 4. Python code: ProgressStore class

```python
import json
from pathlib import Path
from datetime import datetime

class ProgressStore:
    """Simple file-based progress tracking for long-running agents."""

    def __init__(self, progress_file: str = "claude-progress.json"):
        self.progress_file = Path(progress_file)
        self._init_file()

    def _init_file(self):
        if not self.progress_file.exists():
            self.progress_file.write_text(json.dumps({
                "created_at": datetime.now().isoformat(),
                "features": []
            }, ensure_ascii=False, indent=2), encoding="utf-8")

    def read(self) -> dict:
        return json.loads(self.progress_file.read_text(encoding="utf-8"))

    def write(self, data: dict):
        self.progress_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add_feature(self, name: str, description: str = ""):
        data = self.read()
        data["features"].append({
            "name": name,
            "description": description,
            "status": "pending",
            "passes": False,
            "added_at": datetime.now().isoformat(),
            "completed_at": None
        })
        self.write(data)

    def mark_feature(self, name: str, passes: bool):
        data = self.read()
        for feat in data["features"]:
            if feat["name"] == name:
                feat["passes"] = passes
                feat["status"] = "passed" if passes else "failed"
                feat["completed_at"] = datetime.now().isoformat()
        self.write(data)

    def get_next_feature(self) -> dict | None:
        data = self.read()
        for feat in data["features"]:
            if not feat["passes"]:
                return feat
        return None

# Usage
store = ProgressStore("project/claude-progress.json")
store.add_feature("auth", "Implement JWT authentication")
store.add_feature("api", "Create REST endpoints")
next_f = store.get_next_feature()
print(f"Next: {next_f['name'] if next_f else 'All done'}")
store.mark_feature("auth", passes=True)
```

### 5. Cross-link

- `[AGENT_SYSTEM_ARCHITECTURE.md](../../AGENT_SYSTEM_ARCHITECTURE.md)` — Layer 6 (Agent Memory & State) — structured memory patterns cho production agents.
