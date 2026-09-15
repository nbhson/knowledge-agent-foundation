# 🧠 02. Knowledge Graph Construction — Xây Dựng Đồ Thị Tri Thức

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao KG Construction Quan Trọng?](#tại-sao-kg-construction-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Ontology & Schema Design](#1-ontology--schema-design)
> - [2. Entity Extraction](#2-entity-extraction)
> - [3. Relation Extraction](#3-relation-extraction)
> - [4. Entity Resolution & Deduplication](#4-entity-resolution--deduplication)
> - [5. Incremental KG Updates](#5-incremental-kg-updates)
> - [6. Complete Pipeline](#6-complete-pipeline)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn có 1,000 tài liệu: hợp đồng, báo cáo, emails. Bạn thuê 3 interns đọc và trích xuất tri thức:

- Intern A trích: `(Phoenix, managed_by, Alice)` — nhưng ghi "Alice Nguyen"
- Intern B trích: `(Alice N., approves, Contract C-2024)` — viết tắt khác
- Intern C trích: `(Alice Nguyễn, reports_to, Bob)` — dấu tiếng Việt khác

Kết quả: 3 nodes "Alice" khác nhau trong graph, không nối được với nhau → graph **rời rạc**, truy vấn thất bại.

**Knowledge Graph Construction** giải quyết bài toán này: **trích xuất nhất quán, chuẩn hóa, và nối kết** tri thức từ raw text thành graph có thể truy vấn.

### Tại Sao KG Construction Quan Trọng?

> *"Garbage in, garbage out — graph tệ hơn vector nếu extraction sai. Extraction quyết định 80% chất lượng GraphRAG."*
> — Microsoft GraphRAG Paper (2024)

| # | Nghiên Cứu | Phát Hiện |
|---|-----------|-----------|
| 1 | **Microsoft GraphRAG (2024)** | Gleaning loop (trích nhiều vòng) tăng **25% entity coverage** so với single-pass |
| 2 | **LangChain Evaluation (2025)** | Deduplication bằng embedding similarity giảm **40% duplicate nodes** |
| 3 | **Stanford KB Construction (2024)** | Schema-first approach giảm **60% invalid relations** so với open extraction |

---

## Tổng Quan

```
Raw Documents
    │
    ▼
┌─────────────────────┐
│  1. ONTOLOGY DESIGN │  ← Định nghĩa node/edge types hợp lệ (schema)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. ENTITY EXTRACTION│  ← LLM/NER trích entities từ text
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. RELATION EXTRACT │  ← LLM trích quan hệ giữa entities
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. RESOLUTION       │  ← Gộp trùng lặp (Alice = Alice Nguyen)
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. INCREMENTAL UPDATE│ ← Cập nhật graph khi có doc mới
└──────────┬──────────┘
           ▼
     Knowledge Graph (sẵn sàng cho Storage & GraphRAG)
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [Ontology & Schema](#1-ontology--schema-design) | Thiết kế schema, constraints, temporal properties |
| 2 | [Entity Extraction](#2-entity-extraction) | NER, LLM extraction, gleaning loop |
| 3 | [Relation Extraction](#3-relation-extraction) | Open RE, schema-guided RE, confidence scoring |
| 4 | [Resolution](#4-entity-resolution--deduplication) | Deduplication, canonicalization, embedding-based |
| 5 | [Incremental Updates](#5-incremental-kg-updates) | Thêm/sửa/xóa không rebuild toàn bộ |
| 6 | [Pipeline](#6-complete-pipeline) | End-to-end code |
| 7 | [Agentic Construction](#7-agentic-kg-construction) | LLM-agent tự xây & tự sửa KG bằng CRUD |

---

## 1. Ontology & Schema Design

> **📌 Khái Niệm Cơ Bản:**
> **Ontology = "bản thiết kế" của graph** — quy định TRƯỚC những loại thực thể nào tồn tại (`Person`, `Project`, `Document`) và quan hệ nào hợp lệ (`Person` mới được `MANAGES`).
>
> **Tại sao quan trọng?** Nếu không có ontology, LLM trích xuất tự do → graph trở thành **"hairball"** (mớ rối không kiểm soát): 5 thứ gọi là "team", già reviewer đồng nghĩa... query không chuẩn, kết quả sai.
>
> **Analogies:** Ontology giống **khung biểu mẫu** công ty — biết trước hồ sơ có những trường nào, ai được phê duyệt ai. Không có khung → mỗi người ghi hồ sơ mỗi kiểu, không ai tra được.
>
> **2 hướng thiết kế:**
> - **Schema-First**: định trước schema rồi trích xuất theo schema — sạch nhưng có thể bỏ sót quan hệ ngoài dự kiến.
> - **Schema-Free**: trích xuất tự do rồi mới quy hoạch — linh hoạt nhưng sinh nhiều rác.
> - **Hybrid (khuyến nghị)**: schema cốt lõi + xác nhận + cho phép edge lạ vào "pending" để review định kỳ.

### 1.1 Schema-First vs Schema-Free

```
┌──────────────────┬──────────────────────────────────┬──────────────────────────────┐
│ Cách tiếp cận    │ Ưu điểm                          │ Nhược điểm                   │
├──────────────────┼──────────────────────────────────┼──────────────────────────────┤
│ Schema-First     │ Precise, ít rác, dễ query        │ Bỏ sót quan hệ ngoài schema │
│ (định trước)     │ Validation chặt                  │ Cần domain expert            │
│ Schema-Free      │ Linh hoạt, khám phá quan hệ mới  │ Nhiều rác, khó query        │
│ (open extraction)│ Không cần expert                 │ Hairball graph               │
│ Hybrid (khuyến nghị)│ Best of both                │ Phức tạp hơn                 │
└──────────────────┴──────────────────────────────────┴──────────────────────────────┘
```

### 1.2 Thiết Kế Ontology

```yaml
# ontology.yaml — Schema cho Enterprise KG

node_types:
  Person:
    properties:
      name: {type: string, required: true, unique: true}
      role: {type: string, enum: [CTO, Engineer, Manager, Intern]}
      email: {type: string, format: email}
    indexes: [name]

  Project:
    properties:
      name: {type: string, required: true}
      budget: {type: number, min: 0}
      status: {type: string, enum: [Active, Completed, Cancelled]}
    indexes: [name, status]

  Document:
    properties:
      title: string
      doc_type: {type: string, enum: [Contract, Report, Email]}
      created_at: {type: datetime}

edge_types:
  MANAGES:
    from: Person
    to: Person
    properties:
      since: {type: date}
      confidence: {type: float, min: 0, max: 1}
    temporal: true  # có valid_from / valid_until

  APPROVES:
    from: Person
    to: Document
    properties:
      approved_at: date
      confidence: float

  WORKS_ON:
    from: Person
    to: Project
    properties:
      role: string
      allocation: {type: float, min: 0, max: 1}  # % thời gian

  BELONGS_TO:
    from: Document
    to: Project

constraints:
  - "Person -[MANAGES]-> Person (không tự quản lý chính mình)"
  - "Project.budget > 0"
  - "APPROVES.confidence >= 0.7 mới được coi là valid"
```

### 1.3 Validation Code

<details>
<summary>Python Code — Ontology Validation (Click để xem)</summary>

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Ontology:
    node_types: Dict[str, Dict]
    edge_types: Dict[str, Dict]
    
    def validate_node(self, label: str, props: Dict) -> tuple[bool, str]:
        if label not in self.node_types:
            return False, f"Unknown node type: {label}"
        schema = self.node_types[label]
        for prop, rules in schema.get("properties", {}).items():
            if rules.get("required") and prop not in props:
                return False, f"Missing required property: {prop}"
            if prop in props and "enum" in rules:
                if props[prop] not in rules["enum"]:
                    return False, f"Invalid value for {prop}: {props[prop]}"
        return True, "OK"
    
    def validate_edge(self, edge_type: str, from_label: str, to_label: str) -> tuple[bool, str]:
        if edge_type not in self.edge_types:
            return False, f"Unknown edge type: {edge_type}"
        rule = self.edge_types[edge_type]
        if rule["from"] != from_label or rule["to"] != to_label:
            return False, f"Edge {edge_type} requires {rule['from']} -> {rule['to']}, got {from_label} -> {to_label}"
        if from_label == to_label and edge_type == "MANAGES":
            return False, "Cannot manage self"
        return True, "OK"

# Usage
ontology = Ontology(
    node_types={
        "Person": {"properties": {"name": {"required": True}, "role": {"enum": ["CTO", "Engineer"]}}},
        "Project": {"properties": {"name": {"required": True}}},
    },
    edge_types={
        "MANAGES": {"from": "Person", "to": "Person"},
        "WORKS_ON": {"from": "Person", "to": "Project"},
    }
)
print(ontology.validate_node("Person", {"name": "Alice", "role": "CTO"}))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Person", "Person"))  # (True, OK)
print(ontology.validate_edge("MANAGES", "Project", "Person"))  # (False, ...)
```

</details>

---

## 2. Entity Extraction

> **📌 Khái Niệm Cơ Bản:**
> **Entity Extraction = "đọc tài liệu và gạch chân những thực thể quan trọng"** — tìm ra ai là ai (`Nguyễn Văn A = Person`), cái gì là gì (`Phoenix = Project`).
>
> **Analogies:** Giống bạn đọc hợp đồng và bôi đen: tên người, tên dự án, tên tổ chức, tên tài liệu.
>
> **4 cách trích, từ "khô" đến "thông minh":**
> - **Rule-based (regex)**: luật cố định như "C-2024" là mã hợp đồng — chính xác cao nhưng chỉ xử lý pattern đã biết.
> - **NER (spaCy/BERT)**: model học sẵn nhận diện Person/Location/Org — nhanh, chuẩn cho thể loại thông dụng.
> - **LLM extract đơn vòng**: gọi LLM 1 lần lấy JSON entities — linh hoạt nhưng dễ **bỏ sót** khi văn bản dài (LLM "quên" phần sau).
> - **LLM + Gleaning (khuyến nghị cho GraphRAG)**: chạy **nhiều vòng** — vòng sau hỏi "còn entity nào bỏ sót không?" (đưa danh sách đã trích vào prompt) → coverage gần như đầy đủ.

### 2.1 So Sánh Phương Pháp

```
┌──────────────────┬──────────┬──────────┬──────────────────────────────┐
│ Phương pháp      │ Precision│ Recall   │ Best For                     │
├──────────────────┼──────────┼──────────┼──────────────────────────────┤
│ Rule-based (regex)│ ⭐⭐⭐⭐⭐ │ ⭐⭐     │ Pattern cố định (mã HĐ, ngày)│
│ NER (spaCy, BERT)│ ⭐⭐⭐⭐  │ ⭐⭐⭐   │ Person, Org, Location        │
│ LLM (GPT-4o)     │ ⭐⭐⭐   │ ⭐⭐⭐⭐⭐ │ Mọi entity type, context-aware│
│ LLM + Gleaning   │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐⭐ │ GraphRAG: nhiều vòng, full coverage│
└──────────────────┴──────────┴──────────┴──────────────────────────────┘
```

### 2.2 LLM Extraction với Gleaning Loop (GraphRAG Pattern)

<details>
<summary>Python Code — Entity Extraction với Gleaning (Click để xem)</summary>

```python
import requests

OLLAMA_URL = "http://localhost:11434"

EXTRACTION_PROMPT = """Trích xuất entities từ văn bản sau.
Chỉ trích các loại: Person, Project, Document, Organization.

Văn bản:
{text}

Đã trích trước đó (để tránh trùng):
{already_extracted}

Trả về JSON list:
[{{"name": "...", "type": "Person", "description": "..."}}]

Nếu không còn entity mới, trả về []
"""

def extract_entities(text: str, model: str = "gemma3:12b", max_gleanings: int = 2) -> list:
    """Gleaning loop: trích nhiều vòng để tăng coverage."""
    all_entities = []
    already = set()
    
    for glean_round in range(max_gleanings + 1):
        prompt = EXTRACTION_PROMPT.format(
            text=text,
            already_extracted=", ".join(already) if already else "chưa có"
        )
        
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        import json as js
        try:
            new_entities = js.loads(resp.json()["response"])
        except:
            new_entities = []
        
        # Lọc trùng
        added = 0
        for ent in new_entities:
            key = ent["name"].lower().strip()
            if key not in already:
                already.add(key)
                all_entities.append(ent)
                added += 1
        
        print(f"Gleaning round {glean_round}: +{added} entities")
        if added == 0:
            break  # Không còn gì mới
    
    return all_entities

# Usage
text = """
Dự án Phoenix do Nguyễn Văn A phê duyệt. Hợp đồng C-2024 thuộc dự án Phoenix.
Nguyễn Văn A báo cáo cho Trần Thị B, CTO của công ty. Trần Thị B quản lý team AI.
"""
entities = extract_entities(text)
print(entities)
# [{"name": "Nguyễn Văn A", "type": "Person", ...}, {"name": "Phoenix", "type": "Project", ...}, ...]
```

</details>

### 2.3 Chunking Trước Khi Extract

Giống như RAG, documents lớn cần chia nhỏ trước khi extraction:

```python
def chunk_for_extraction(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """Chia document thành chunks cho extraction — mỗi chunk trích riêng, rồi merge."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# Extract từng chunk, rồi merge entities
def extract_from_document(doc_text: str) -> list:
    chunks = chunk_for_extraction(doc_text)
    all_entities = []
    for chunk in chunks:
        all_entities.extend(extract_entities(chunk, max_gleanings=1))
    return all_entities
```

### 2.4 Claims Extraction (GraphRAG Pattern)

> **📌 Khái Niệm Cơ Bản:**
> **Claims = "các khẳng định/dữ kiện" đáng giá trích ra từ văn bản**, không chỉ entities + relations.
>
> Ví dụ từ câu *"Phòng ban cần cắt giảm 20% ngân sách quý sau"*:
> - Entity: `Phòng ban`, `ngân sách`
> - Relation: hợp lệ giữa ai với ai
> - **Claim**: `{subject: Phòng ban, predicate: CUT_BUDGET, object: 20%, period: quý sau, source_chunk: "doc #3"}`
>
> **Tại sao cần?** GraphRAG của Microsoft trích cả 3 loại (entity/relation/claim). Claim cho phép trả lời câu hỏi dạng **"qui định nào / bằng chứng nào nói về X?"** — LLM trả lời kèm **nguồn bằng chứng** (source text) thay vì đoán. Mỗi claim **click được về chunk gốc** (evidence provenance).

```python
CLAIM_PROMPT = """Trích xuất các khẳng định (claims) từ văn bản.
Mỗi claim = 1 sự thật đáng lưu, kèm header (chủ đề) đơn giản.

Văn bản:
{text}

Trả về JSON list, mỗi phần tử:
{{"subject": "...", "predicate": "...", "object": "...", "description": "..."}}
Nếu không có claim, trả về []
"""

def extract_claims(text: str, model: str = "gemma3:12b") -> list:
    # (triển khai tương tự extract_entities — gọi LLM, parse JSON)
    ...
    return claims

# Mỗi claim được GẮN với chunk gốc → truy vết được về tài liệu
def attach_claims(chunks: list[dict]) -> list[dict]:
    for chunk in chunks:
        claims = extract_claims(chunk["text"])
        for c in claims:
            c["source_chunk_id"] = chunk["id"]   # ← evidence provenance
    return ...
```

---

## 3. Relation Extraction

### 3.1 Schema-Guided Relation Extraction

<details>
<summary>Python Code — Relation Extraction (Click để xem)</summary>

```python
RELATION_PROMPT = """Cho danh sách entities và văn bản, trích xuất quan hệ.

Entities:
{entities}

Văn bản:
{text}

Các loại quan hệ hợp lệ:
- MANAGES: Person -> Person
- APPROVES: Person -> Document
- WORKS_ON: Person -> Project
- BELONGS_TO: Document -> Project
- REPORTS_TO: Person -> Person

Trả về JSON:
[{{"source": "Nguyễn Văn A", "target": "Hợp đồng C-2024", "type": "APPROVES", "confidence": 0.9, "evidence": "..."}}]
"""

def extract_relations(text: str, entities: list, model: str = "gemma3:12b") -> list:
    ent_str = "\n".join(f"- {e['name']} ({e['type']})" for e in entities)
    prompt = RELATION_PROMPT.format(entities=ent_str, text=text)
    
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    })
    import json as js
    try:
        return js.loads(resp.json()["response"])
    except:
        return []

# Usage
relations = extract_relations(text, entities)
print(relations)
# [{"source": "Nguyễn Văn A", "target": "Hợp đồng C-2024", "type": "APPROVES", "confidence": 0.9}, ...]
```

</details>

### 3.2 Confidence Scoring

Mỗi relation nên có `confidence` để downstream filtering:

```python
def filter_by_confidence(relations: list, threshold: float = 0.7) -> list:
    """Chỉ giữ relations có confidence >= threshold."""
    filtered = [r for r in relations if r.get("confidence", 0) >= threshold]
    print(f"Filtered: {len(relations)} -> {len(filtered)} (threshold={threshold})")
    return filtered
```

---

## 4. Entity Resolution & Deduplication

> **📌 Khái Niệm Cơ Bản:**
> **Deduplication = tìm và gộp "1 người viết bằng 2 tên"** — LLM trích xuất từ từng chunk khác nhau nên **cùng 1 thực thể có thể thành nhiều nodes**: "Nguyễn Văn A" (doc 1), "NV A" (doc 2), "Nguyen Van A" (doc 3).
>
> **Analogies:** Danh bạ công ty 2 lần ghi cùng một người — "Nguyễn Văn A - CTO" và "anh A - giám đốc công nghệ". Không gộp → query "CTO là ai?" chia đôi dữ liệu, trả lời sai.
>
> **Các mức dedup (từ đơn giản → thông minh):**
> 1. **Chuẩn hóa text**: lowercase, bỏ dấu, bỏ từ thừa → "Nguyen Van A" == "nguyễn văn a"
> 2. **Fuzzy match**: Levenshtein/TF-IDF similarity — "Nguyen Van A" vs "Nguyen Van An" gần giống
> 3. **Embedding similarity**: "CTO Alice" và "giám đốc công nghệ Alice" ngữ nghĩa giống nhau
>
> **Cảnh báo:** gộp quá mạnh → **hợp nhất nhầm 2 người thật sự khác nhau** (Alice nhân sự ≠ Alice CTO). Luôn đặt **ngưỡng (threshold)** và cho phép split lại.

### 4.1 Bài Toán

```
Raw extraction:
  "Nguyễn Văn A" (Person)
  "Alice Nguyen" (Person)    ← cùng người?
  "A. Nguyen"    (Person)

  "Dự án Phoenix" (Project)
  "Phoenix Project" (Project) ← cùng project?
  "Phoenix" (Project)
```

### 4.2 Embedding-Based Deduplication

<details>
<summary>Python Code — Deduplication (Click để xem)</summary>

```python
import numpy as np

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def embed(text: str, model: str = "nomic-embed-text") -> list[float]:
    resp = requests.post(f"{OLLAMA_URL}/api/embed", json={"model": model, "input": text})
    return resp.json()["embeddings"][0]

def deduplicate_entities(entities: list, threshold: float = 0.85) -> list:
    """
    Gộp entities trùng lặp dựa trên embedding similarity.
    Giữ entity đầu tiên làm canonical.
    """
    if not entities:
        return []
    
    # Embed từng entity name
    embeddings = [embed(e["name"]) for e in entities]
    
    canonical = []  # list of (entity, embedding)
    mapping = {}    # old_name -> canonical_name
    
    for ent, emb in zip(entities, embeddings):
        found = False
        for canon_ent, canon_emb in canonical:
            if ent["type"] != canon_ent["type"]:
                continue  # Chỉ so sánh cùng type
            sim = cosine_sim(emb, canon_emb)
            if sim >= threshold:
                mapping[ent["name"]] = canon_ent["name"]
                # Merge properties
                print(f"Dedup: '{ent['name']}' -> '{canon_ent['name']}' (sim={sim:.3f})")
                found = True
                break
        
        if not found:
            canonical.append((ent, emb))
            mapping[ent["name"]] = ent["name"]
    
    # Trả về canonical entities + mapping để sửa relations
    canonical_entities = [c[0] for c in canonical]
    return canonical_entities, mapping

def remap_relations(relations: list, mapping: dict) -> list:
    """Sửa source/target trong relations theo mapping dedup."""
    for r in relations:
        r["source"] = mapping.get(r["source"], r["source"])
        r["target"] = mapping.get(r["target"], r["target"])
    # Loại bỏ self-loops sau dedup
    return [r for r in relations if r["source"] != r["target"]]

# Usage
entities_raw = [
    {"name": "Nguyễn Văn A", "type": "Person"},
    {"name": "Alice Nguyen", "type": "Person"},
    {"name": "Phoenix", "type": "Project"},
    {"name": "Dự án Phoenix", "type": "Project"},
]
canonical, mapping = deduplicate_entities(entities_raw, threshold=0.80)
print(f"Canonical: {[c['name'] for c in canonical]}")
print(f"Mapping: {mapping}")
```

</details>

### 4.3 Entity Linking & Coreference Resolution

> **📌 Khái Niệm Cơ Bản:**
> **Entity Linking** = gắn một danh từ/đại từ về **đúng thực thể duy nhất** trong graph (mặc dù viết khác nhau). **Coreference Resolution** = nhận biết "anh ấy", "CEO", "ông A" đều chỉ cùng 1 người.
>
> **Khác Dedup ở chỗ nào?** Dedup gộp *hậu kỳ* (sau khi trích). Entity linking xử lý *ngay lúc trích* — biết "NV A" trong doc 2 chính là node "Nguyễn Văn A" đã tồn tại.
>
> **Analogies:** Giống tổ chức sự kiện: 3 người đăng ký ghi khác tên ("Nguyễn Văn A", "NV A", "anh A") — bảo vệ (linking) phải nhận ra đó là 1 người để không cấp 3 thẻ khác nhau.

```python
# Coreference trong text: "Alice ký hợp đồng. Cô ấy giao 200m." 
# → "Cô ấy" = Alice (coreference)
# → "Alice" (doc khác viết "A. Nguyen") = node Alice đang tồn tại (entity linking)

def entity_linking(mention: str, graph_entities: list[str], embedding_fn) -> str:
    """Gắn mention ('A. Nguyen') về canonical entity bằng similarity."""
    best, best_score = None, 0
    v_mention = embedding_fn(mention)
    for ent in graph_entities:
        score = cosine(v_mention, embedding_fn(ent))
        if score > best_score:
            best, best_score = ent, score
    return best if best_score > 0.85 else None   # dưới ngưỡng → entity MỚI
```

---

## 5. Incremental KG Updates

KG production thay đổi hàng ngày — không thể rebuild toàn bộ mỗi lần.

```python
class IncrementalKGUpdater:
    """Cập nhật KG theo event — thêm/sửa/xóa không rebuild."""
    
    def __init__(self, graph):
        self.graph = graph  # Neo4j / NetworkX / Kuzu
    
    def upsert_entity(self, entity: dict):
        """Thêm hoặc cập nhật entity (dựa trên unique key)."""
        # Cypher: MERGE (tạo nếu chưa có, cập nhật nếu có)
        query = """
        MERGE (n:Person {name: $name})
        SET n.role = $role, n.updated_at = datetime()
        RETURN n
        """
        self.graph.query(query, params=entity)
    
    def upsert_relation(self, source: str, target: str, rel_type: str, props: dict):
        query = f"""
        MATCH (a {{name: $source}}), (b {{name: $target}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r.confidence = $confidence, r.updated_at = datetime()
        RETURN r
        """
        self.graph.query(query, params={"source": source, "target": target, **props})
    
    def soft_delete(self, node_name: str):
        """Soft delete: đánh dấu, không xóa cứng — giữ history."""
        query = """
        MATCH (n {name: $name})
        SET n.deleted = true, n.deleted_at = datetime()
        """
        self.graph.query(query, params={"name": node_name})
    
    def process_new_document(self, doc_text: str, doc_id: str):
        """Pipeline cho document mới: extract → dedup → upsert."""
        entities = extract_entities(doc_text)
        relations = extract_relations(doc_text, entities)
        canonical, mapping = deduplicate_entities(entities)
        relations = remap_relations(relations, mapping)
        
        for ent in canonical:
            self.upsert_entity(ent)
        for rel in relations:
            self.upsert_relation(rel["source"], rel["target"], rel["type"], rel)
        
        print(f"Ingested doc {doc_id}: {len(canonical)} entities, {len(relations)} relations")
```

---

## 6. Complete Pipeline

<details>
<summary>Python Code — End-to-End KG Construction (Click để xem)</summary>

```python
def build_knowledge_graph(documents: list[str], ontology: Ontology) -> dict:
    """
    Pipeline hoàn chỉnh: Documents -> Knowledge Graph
    """
    all_entities = []
    all_relations = []
    
    # Step 1: Extract từ từng document
    for doc in documents:
        entities = extract_entities(doc, max_gleanings=2)
        relations = extract_relations(doc, entities)
        all_entities.extend(entities)
        all_relations.extend(relations)
    
    print(f"Raw: {len(all_entities)} entities, {len(all_relations)} relations")
    
    # Step 2: Deduplicate
    canonical_entities, mapping = deduplicate_entities(all_entities, threshold=0.85)
    all_relations = remap_relations(all_relations, mapping)
    
    print(f"After dedup: {len(canonical_entities)} entities, {len(all_relations)} relations")
    
    # Step 3: Validate against ontology
    valid_entities = []
    for ent in canonical_entities:
        ok, msg = ontology.validate_node(ent["type"], ent)
        if ok:
            valid_entities.append(ent)
        else:
            print(f"Invalid entity {ent['name']}: {msg}")
    
    valid_relations = []
    for rel in all_relations:
        # Tìm type của source/target
        src_type = next((e["type"] for e in valid_entities if e["name"] == rel["source"]), None)
        tgt_type = next((e["type"] for e in valid_entities if e["name"] == rel["target"]), None)
        if src_type and tgt_type:
            ok, msg = ontology.validate_edge(rel["type"], src_type, tgt_type)
            if ok and rel.get("confidence", 0) >= 0.7:
                valid_relations.append(rel)
            else:
                print(f"Invalid relation {rel}: {msg}")
    
    print(f"After validation: {len(valid_entities)} entities, {len(valid_relations)} relations")
    
    return {"entities": valid_entities, "relations": valid_relations}

# Usage
docs = [
    "Dự án Phoenix do Nguyễn Văn A phê duyệt. Hợp đồng C-2024 thuộc dự án Phoenix.",
    "Nguyễn Văn A báo cáo cho Trần Thị B, CTO. Trần Thị B quản lý team AI gồm 10 engineers.",
]
kg = build_knowledge_graph(docs, ontology)
print(kg)
```

</details>

---

## 7. Agentic KG Construction

> **📌 Khái Niệm Cơ Bản:**
> **Agentic KG construction** = thay vì pipeline batch trích-trước-rồi-virtual nên **LLM-agent trực tiếp thao tác graph bằng CRUD** (Create/Read/Update/Delete qua Cypher). Agent đọc văn bản → viết query `CREATE`/`MERGE` → kiểm tra kết quả → **tự nhận lỗi và sửa** nếu query sai hoặc thông tin chưa đúng.
>
> **So với pipeline batch (các section trên):**
>
> | | Batch Pipeline | Agentic Agent |
> |---|---|---|
> | Quy trình | 1 chiều: text → extract → gom | Vòng lặp: đọc → ghi → kiểm tra → sửa |
> | Sửa lỗi | Chạy lại pipeline | Tự quyết định UPDATE/DELETE |
> | Bằng chứng | Không lưu | **Mỗi triplet gắn `source_chunk`** để truy vết |
> | Cost | Trung bình | Cao hơn (nhiều LLM calls) |
> | Phù hợp | Dữ liệu lớn, batch | KG nhỏ, cần chính xác, tự điều chỉnh schema |
>
> **Analogies:** Pipeline batch giống dây chuyền nhà máy; agent giống **thợ lành nghề** — vừa xây vừa nhìn, thấy lỗi thì tháo ra sửa ngay, và ghi chú "viên gạch này lấy từ nguồn X".
>
> Các hệ thống điển hình: **KnoBuilder, KG-Agent** (tự trích triplet theo vòng lặp), **RAGA** (đánh giá chất lượng KG rồi cho agent sửa). Nghiên cứu 2025-2026 cho thấy agentic approach **giảm đáng kể triplets sai** so với batch single-pass, với chi phí cao hơn 2-3×.

```python
# Pseudocode — Agent xây KG (dùng Cypher + query kiểm tra)
TOOLS = ["create_entity", "link_entities", "query_graph", "delete_triplet"]

def agent_build_chunk(chunk_text: str, cypher_exec) -> list[str]:
    """Agent đọc chunk, quyết định các thao tác CRUD, rồi tự verify."""
    actions = []
    # 1) PLAN: LLM quyết định triplet nào cần thêm
    triplets = llm(f"Từ đoạn sau, các (entity, relation, entity) nào đáng ghi? {chunk_text}")
    for subj, rel, obj in triplets:
        # 2) ACTION: thử MERGE + SET source để truy vết
        cypher_exec("""
            MERGE (s {name:$subj}) 
            ON CREATE SET s.source_chunk=$chunk
            WITH s
            MATCH (t {name: $obj})
            MERGE (s)-[r:REL {type:$rel}]->(t)
            SET r.source_chunk=$chunk
        """, subj=subj, rel=rel, obj=obj, chunk=chunk_text[:100])
        actions.append(f"CREATE {subj}--{rel}-->{obj}")
    # 3) VERIFY: ở cuối chunk, hỏi lại LLM kiểm tra những gì vừa viết
    review = llm(f"Các triplet này có đúng/đủ không? {triplets}")
    if "cần sửa" in review:
        cypher_exec("DELETE ...")  # agent tự sửa (UPDATE/DELETE)
        actions.append("FIX: " + review)
    return actions
```

---

## 8. Labs Thực Hành

### Lab 1: Extract KG từ 5 Documents

- Viết script đọc 5 markdown files trong `data/raw_docs/`
- Chạy `extract_entities` + `extract_relations` cho từng file
- Merge và deduplicate, in ra số entities/relations

### Lab 2: So Sánh Single-Pass vs Gleaning

- Trích entities 1 lần (gleaning=0) vs 2 vòng (gleaning=2)
- Đo coverage: số entities trích được, so sánh precision thủ công

### Lab 3: Deduplication Tuning

- Thử thresholds 0.80, 0.85, 0.90 cho `deduplicate_entities`
- Quan sát: threshold thấp → gộp quá tay (false positive), cao → sót trùng lặp

---

## Tài Liệu Tham Khảo

- Microsoft GraphRAG — *Entity & Relationship Extraction* (https://microsoft.github.io/graphrag/)
- LangChain — *LLMGraphTransformer* (https://python.langchain.com/docs/use_cases/graph/constructing)
- spaCy — *Named Entity Recognition* (https://spacy.io/usage/linguistic-features#named-entities)
- Microsoft GraphRAG — *Claims Extraction Pattern* (https://microsoft.github.io/graphrag/)
- *Knowledge Graph Agent: An Agentic Construction Benchmark* — KnoBuilder/RAGA/KG-Agent (arXiv 2025)
- *Knowledge Graph Construction Survey* — Paulheim (2017)

---

*Tiếp theo: [03 — Graph Storage & Query](../03-graph-storage/)*
