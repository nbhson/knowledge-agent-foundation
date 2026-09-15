# ⚙️ 08. Graph Workflow — Pipeline, Cập Nhật và Vận Hành Đồ Thị

> ## 📑 Mục Lục
>
> - [Câu Chuyện Mở Đầu](#câu-chuyện-mở-đầu)
> - [Tại Sao Graph Workflow Quan Trọng?](#tại-sao-graph-workflow-quan-trọng)
> - [Tổng Quan](#tổng-quan)
> - [Nội Dung](#nội-dung)
> - [1. Graph ETL Pipeline](#1-graph-etl-pipeline)
> - [2. Incremental Updates](#2-incremental-updates)
> - [3. Versioning & Temporal Graphs](#3-versioning--temporal-graphs)
> - [4. Orchestration: Airflow, Prefect, Loop](#4-orchestration-airflow-prefect-loop)
> - [5. Observability & Error Recovery](#5-observability--error-recovery)
> - [6. Triển Khai Complete Workflow Engine](#6-triển-khai-complete-workflow-engine)
> - [7. Labs Thực Hành](#7-labs-thực-hành)
> - [Tài Liệu Tham Khảo](#tài-liệu-tham-khảo)

---

### Câu Chuyện Mở Đầu

Bạn đã xây xong Knowledge Graph với 10,000 nodes. Hệ thống chạy tốt.

Tuần sau:

- **Thứ 2**: 50 documents mới → cần ingest, không rebuild toàn bộ
- **Thứ 3**: Phát hiện 200 duplicate entities → cần merge, không mất relations
- **Thứ 4**: Schema thay đổi (thêm edge type `REVIEWS`) → cần migration
- **Thứ 5**: Một batch ingest lỗi → cần rollback

Không có workflow, bạn làm thủ công: chạy script, quên checkpoint, graph bị hỏng, mất 2 ngày khôi phục.

**Graph Workflow** là hệ thống **tự động, có checkpoint, có rollback, có observability** cho mọi thao tác trên graph — giống như CI/CD cho code, nhưng cho knowledge graph.

### Tại Sao Graph Workflow Quan Trọng?

> *"A graph without a workflow is a snapshot. A graph with a workflow is a living system."*

| # | Nguồn | Phát Hiện |
|---|-------|-----------|
| 1 | **Neo4j Production Survey (2024)** | 68% graph incidents do **thiếu incremental pipeline** — rebuild toàn bộ gây downtime |
| 2 | **Microsoft GraphRAG** | Incremental indexing giảm **90% re-indexing cost** khi thêm documents mới |
| 3 | **Prefect + Graph Benchmark (2025)** | Workflow với checkpoint giảm **80% recovery time** khi batch ingest lỗi |

---

## Tổng Quan

```
                    ┌─────────────────────────────────┐
                    │      GRAPH WORKFLOW ENGINE       │
                    │                                  │
  New Documents ───►│  ┌──────────┐  ┌──────────┐     │
                    │  │  ETL     │  │ Incremental│   │
  Schema Changes ──►│  │ Pipeline │  │  Updates │     │
                    │  └──────────┘  └──────────┘     │
  User Edits ──────►│  ┌──────────┐  ┌──────────┐     │
                    │  │Versioning│  │Orchestr. │     │
                    │  │& Temporal│  │(Schedule)│     │
                    │  └──────────┘  └──────────┘     │
                    │  ┌──────────────────────────┐   │
                    │  │ Observability & Recovery │   │
                    │  │ Logs, Metrics, Rollback  │   │
                    │  └──────────────────────────┘   │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │     KNOWLEDGE GRAPH (Neo4j)      │
                    │  + Vector Index + Community Cache│
                    └─────────────────────────────────┘
```

---

## Nội Dung

| # | Chủ đề | Mô tả |
|---|--------|-------|
| 1 | [ETL Pipeline](#1-graph-etl-pipeline) | Extract → Transform → Load cho graph |
| 2 | [Incremental Updates](#2-incremental-updates) | Thêm/sửa/xóa không rebuild |
| 3 | [Versioning](#3-versioning--temporal-graphs) | Temporal, rollback, audit trail |
| 4 | [Orchestration](#4-orchestration-airflow-prefect-loop) | Schedule, DAG, loop integration |
| 5 | [Observability](#5-observability--error-recovery) | Logging, metrics, circuit breaker |
| 6 | [Engine](#6-triển-khai-complete-workflow-engine) | Code workflow engine |

---

## 1. Graph ETL Pipeline

> **📌 Khái Niệm Cơ Bản:**
> **Graph ETL = quy trình "nhồi dữ liệu vào graph"** theo 4 giai đoạn:
> 1. **Extract**: đọc documents → trích xuất entities + relations (bằng LLM)
> 2. **Transform**: làm sạch — gộp trùng (dedup), chuẩn hóa tên ("NV A" = "Nguyễn Văn A")
> 3. **Validate**: kiểm tra entities có hợp lệ theo ontology/schema không (không thể có `Person -[WORKS_ON]-> Person`)
> 4. **Load**: ghi vào graph dùng **MERGE** (không INSERT) — thêm mới nếu chưa có, cập nhật nếu đã có
>
> **Khác ETL bảng tính:**
> - Transform cần **LLM** (trích xuất tri thức từ text — không phải phép tính)
> - Load phải **idempotent** (chạy lại 100 lần cũng kết quả như nhau, không nhân đôi dữ liệu)
> - Bắt buộc **dedup + validation** trước khi ghi — vì LLM extract không lúc nào chính xác 100%

```
ETL thường:  Raw Data → Clean → Transform → Load vào Table
Graph ETL:   Documents → Extract KG → Resolve → Validate → Load vào Graph

Khác biệt:
  - Transform = entity/relation extraction (cần LLM)
  - Load = MERGE (idempotent) thay vì INSERT
  - Cần dedup + ontology validation trước khi load
```

### 1.1 ETL Cho Graph Khác Gì ETL Thường?

<details>
<summary>Python Code — Graph ETL Pipeline (Click để xem)</summary>

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable
from datetime import datetime
import time

@dataclass
class ETLResult:
    success: bool
    entities_in: int = 0
    entities_out: int = 0
    relations_in: int = 0
    relations_out: int = 0
    errors: List[str] = field(default_factory=list)
    duration_ms: float = 0

class GraphETLPipeline:
    """
    ETL Pipeline cho Knowledge Graph.
    
    Stages: Extract → Transform (dedup) → Validate → Load
    Mỗi stage có error handling + metrics.
    """
    
    def __init__(self, name: str = "graph-etl"):
        self.name = name
        self.stages: List[Dict] = []
        self.metrics: Dict[str, Dict] = {}
    
    def add_stage(self, name: str, func: Callable, on_error: str = "fail"):
        """
        on_error: "fail" (dừng pipeline) | "skip" (bỏ qua stage) | "retry"
        """
        self.stages.append({"name": name, "func": func, "on_error": on_error})
        return self
    
    def run(self, data: Any) -> ETLResult:
        start = time.time()
        result = ETLResult(success=True)
        
        for stage in self.stages:
            stage_start = time.time()
            stage_name = stage["name"]
            print(f"  ▶ Stage: {stage_name}")
            
            try:
                data = stage["func"](data)
                duration = (time.time() - stage_start) * 1000
                self.metrics[stage_name] = {"status": "success", "duration_ms": round(duration, 2)}
                print(f"    ✅ {stage_name}: {duration:.0f}ms")
            
            except Exception as e:
                duration = (time.time() - stage_start) * 1000
                self.metrics[stage_name] = {"status": "failed", "error": str(e), "duration_ms": round(duration, 2)}
                result.errors.append(f"{stage_name}: {e}")
                print(f"    ❌ {stage_name}: {e}")
                
                if stage["on_error"] == "fail":
                    result.success = False
                    result.duration_ms = (time.time() - start) * 1000
                    return result
                elif stage["on_error"] == "skip":
                    print(f"    ⏭ Skipping {stage_name}")
                    continue
        
        result.duration_ms = (time.time() - start) * 1000
        return result

# Usage: định nghĩa pipeline
def extract_stage(data: List[str]) -> Dict:
    all_entities, all_relations = [], []
    for doc in data:
        # Gọi LLM extraction (từ 02-knowledge-graph)
        # entities = extract_entities(doc)
        # relations = extract_relations(doc, entities)
        entities = [{"name": "Alice", "type": "Person"}]  # mock
        relations = [{"source": "Alice", "target": "Phoenix", "type": "WORKS_ON"}]
        all_entities.extend(entities)
        all_relations.extend(relations)
    return {"entities": all_entities, "relations": all_relations, "raw_count": len(data)}

def dedup_stage(data: Dict) -> Dict:
    # Deduplicate (từ 02-knowledge-graph)
    # canonical, mapping = deduplicate_entities(data["entities"])
    print(f"    Dedup: {len(data['entities'])} -> {len(data['entities'])} entities")
    return data

def validate_stage(data: Dict) -> Dict:
    # Validate against ontology (từ 02-knowledge-graph)
    print(f"    Validate: {len(data['entities'])} entities, {len(data['relations'])} relations")
    return data

def load_stage(data: Dict) -> Dict:
    # Load vào Neo4j/Kuzu (từ 03-graph-storage)
    print(f"    Load: {len(data['entities'])} entities → Neo4j")
    return data

pipeline = (GraphETLPipeline("enterprise-kg")
    .add_stage("extract", extract_stage)
    .add_stage("dedup", dedup_stage)
    .add_stage("validate", validate_stage)
    .add_stage("load", load_stage))

result = pipeline.run(["Doc 1: Alice works on Phoenix", "Doc 2: Bob manages Carol"])
print(f"Pipeline: success={result.success}, duration={result.duration_ms:.0f}ms")
print(f"Metrics: {pipeline.metrics}")
```

</details>

### 1.2 Batch vs Streaming

```
┌──────────────┬──────────────────────────────────┬──────────────────────────┐
│ Mode         │ Khi nào dùng                     │ Ví dụ                    │
├──────────────┼──────────────────────────────────┼──────────────────────────┤
│ Batch        │ Ingest hàng loạt (100-10K docs)  │ Initial load, nightly job│
│ Streaming    │ Ingest real-time (1 doc/event)   │ User uploads, webhook    │
│ Micro-batch  │ Cân bằng (10-100 docs/lần)       │ Hourly incremental       │
└──────────────┴──────────────────────────────────┴──────────────────────────┘

Khuyến nghị:
  - Initial: batch (toàn bộ corpus, 1 lần)
  - Daily: micro-batch (documents mới trong ngày)
  - Real-time: streaming (user edit, API webhook)
```

---

## 2. Incremental Updates

### 2.1 Tại Sao Incremental?

```
Rebuild toàn bộ (batch):
  10K docs × 2 LLM calls/doc × $0.005/1K = $100 + 2 giờ
  → Không thể làm mỗi khi có 1 doc mới

Incremental:
  1 doc mới × 2 LLM calls × $0.005/1K = $0.01 + 5 giây
  → Chỉ xử lý doc mới, merge vào graph hiện có
```

### 2.2 Incremental Strategies

<details>
<summary>Python Code — Incremental Update Engine (Click để xem)</summary>

```python
from typing import List, Dict, Optional
from datetime import datetime

class IncrementalUpdater:
    """
    Cập nhật KG theo incremental — không rebuild.
    
    Strategies:
      - ADD: thêm entities/relations mới
      - UPSERT: tạo nếu chưa có, cập nhật nếu có
      - SOFT_DELETE: đánh dấu xóa, không xóa cứng
      - MERGE: gộp duplicate entities
    """
    
    def __init__(self, graph):
        self.graph = graph  # Neo4j driver hoặc NetworkX
    
    def add_document(self, doc_id: str, text: str) -> Dict:
        """Thêm 1 document mới vào KG."""
        print(f"Ingesting doc: {doc_id}")
        
        # 1. Extract chỉ doc mới (không re-extract toàn bộ)
        # entities = extract_entities(text)
        # relations = extract_relations(text, entities)
        entities = [{"name": "NewPerson", "type": "Person"}]  # mock
        relations = []
        
        # 2. Dedup với graph hiện có (không chỉ trong batch)
        # Kiểm tra entity đã tồn tại chưa
        new_entities = []
        for ent in entities:
            exists = self._entity_exists(ent["name"])
            if not exists:
                new_entities.append(ent)
                print(f"  + New entity: {ent['name']}")
            else:
                print(f"  ~ Entity exists: {ent['name']} (updating properties)")
                self._update_entity(ent)
        
        # 3. Upsert vào graph
        for ent in new_entities:
            self._upsert_entity(ent, doc_id)
        for rel in relations:
            self._upsert_relation(rel, doc_id)
        
        return {"new_entities": len(new_entities), "relations": len(relations)}
    
    def merge_entities(self, canonical_name: str, duplicate_names: List[str]):
        """Gộp duplicate entities: chuyển tất cả edges về canonical."""
        print(f"Merging {duplicate_names} → {canonical_name}")
        
        # Cypher cho Neo4j:
        # MATCH (dup:Entity) WHERE dup.name IN $duplicates
        # MATCH (dup)-[r]->(other)
        # MATCH (canonical:Entity {name: $canonical})
        # CREATE (canonical)-[r2:RELATED {type: r.type}]->(other)
        # SET r2 = properties(r)
        # DELETE r
        
        # NetworkX:
        if hasattr(self.graph, 'nodes') and canonical_name in self.graph:
            for dup_name in duplicate_names:
                if dup_name in self.graph:
                    # Chuyển edges
                    for successor in list(self.graph.successors(dup_name)):
                        edata = self.graph.get_edge_data(dup_name, successor)
                        self.graph.add_edge(canonical_name, successor, **edata)
                    for predecessor in list(self.graph.predecessors(dup_name)):
                        edata = self.graph.get_edge_data(predecessor, dup_name)
                        self.graph.add_edge(predecessor, canonical_name, **edata)
                    self.graph.remove_node(dup_name)
                    print(f"  Merged {dup_name} → {canonical_name}")
    
    def delete_document(self, doc_id: str, soft: bool = True):
        """Xóa document: soft delete (đánh dấu) hoặc hard delete."""
        if soft:
            # Đánh dấu entities/relations từ doc này là deleted
            print(f"Soft deleting doc: {doc_id}")
            # Cypher: MATCH (n {source_doc: $doc_id}) SET n.deleted = true
        else:
            print(f"Hard deleting doc: {doc_id}")
            # Cypher: MATCH (n {source_doc: $doc_id}) DETACH DELETE n
    
    def _entity_exists(self, name: str) -> bool:
        if hasattr(self.graph, 'has_node'):
            return self.graph.has_node(name)
        return False  # Neo4j: query check
    
    def _upsert_entity(self, entity: Dict, doc_id: str):
        # Neo4j: MERGE (n:Entity {name: $name}) SET n += $props
        if hasattr(self.graph, 'add_node'):
            self.graph.add_node(entity["name"], **entity, source_doc=doc_id)
    
    def _update_entity(self, entity: Dict):
        if hasattr(self.graph, 'nodes') and entity["name"] in self.graph:
            for k, v in entity.items():
                self.graph.nodes[entity["name"]][k] = v
    
    def _upsert_relation(self, relation: Dict, doc_id: str):
        if hasattr(self.graph, 'add_edge'):
            self.graph.add_edge(relation["source"], relation["target"],
                                type=relation["type"], source_doc=doc_id)

# Usage
import networkx as nx
G = nx.DiGraph()
G.add_node("Alice", type="Person")

updater = IncrementalUpdater(G)
updater.add_document("doc_001", "Bob là engineer làm việc trên Phoenix")
print(f"Graph: {list(G.nodes(data=True))}")
print(f"Edges: {list(G.edges(data=True))}")

# Merge duplicates
G.add_node("Alice Nguyen", type="Person")
G.add_edge("Alice Nguyen", "Phoenix", type="WORKS_ON")
updater.merge_entities("Alice", ["Alice Nguyen"])
print(f"After merge: {list(G.nodes())}")
```

</details>

---

## 3. Versioning & Temporal Graphs

> **📌 Khái Niệm Cơ Bản:**
> **Grapactory luôn thay đổi** — nhân viên đổi team, dự án bị hủy, hợp đồng hết hạn. Nếu bạn xóa edge cũ, bạn **mất lịch sử + không thể trả lời câu hỏi "hồi Q1/2024 thì thế nào?"**.
>
> **Giải pháp 2 lớp:**
> 1. **Temporal Properties** — thêm `valid_from`/`valid_until` cho edge: quan hệ có **thời gian hiệu lực**. Query "ai quản lý TeamA vào 2024-02-01?" → chỉ xét edges active lúc đó.
> 2. **Audit Trail (Event Sourcing)** — ghi log **mọi thay đổi** (ai, khi nào, làm gì). Không có "xóa mất", chỉ có "ghi thêm 1 event DELETE" → **rollback được**.
>
> **Analogies:**
> - Temporal = hợp đồng lao động có ngày bắt đầu/kết thúc — chỉ "còn hiệu lực" trong khoảng đó.
> - Audit Trail = sổ nhật ký ghi mọi thao tác — tra được ai đã sửa gì. Không bao giờ tẩy xóa, chỉ thêm dòng mới.

### 3.1 Temporal Properties

```python
from datetime import date

# Mỗi edge có lifecycle
temporal_edge = {
    "from": "Alice",
    "to": "TeamA",
    "type": "MANAGES",
    "valid_from": date(2023, 1, 1),
    "valid_until": date(2024, 6, 30),  # None = vẫn active
    "created_at": datetime.now(),
    "created_by": "ingest:doc_123",
}

# Query tại thời điểm cụ thể
def query_at(graph_edges: List[Dict], query_date: date) -> List[Dict]:
    active = []
    for e in graph_edges:
        vf = e["valid_from"]
        vu = e.get("valid_until") or date(9999, 12, 31)
        if vf <= query_date <= vu:
            active.append(e)
    return active
```

### 3.2 Audit Trail (Event Sourcing)

Giống như `trajectory-fork-replay` trong harness, graph cũng cần audit trail:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class GraphEvent:
    id: str
    timestamp: datetime
    action: Literal["CREATE_NODE", "CREATE_EDGE", "UPDATE", "DELETE", "MERGE"]
    payload: Dict
    actor: str  # "user:alice" | "pipeline:etl" | "loop:daily-triage"
    prev_state: Optional[Dict] = None  # để rollback

class GraphAuditLog:
    def __init__(self):
        self.events: List[GraphEvent] = []
    
    def log(self, event: GraphEvent):
        self.events.append(event)
        print(f"  [Audit] {event.action}: {event.payload} by {event.actor}")
    
    def rollback(self, event_id: str, graph):
        """Rollback về trước event_id."""
        idx = next(i for i, e in enumerate(self.events) if e.id == event_id)
        target_event = self.events[idx]
        if target_event.prev_state:
            # Khôi phục prev_state
            print(f"  Rolling back {event_id}: restoring {target_event.prev_state}")
        # Xóa events sau đó
        self.events = self.events[:idx]
    
    def history(self, node_name: str) -> List[GraphEvent]:
        """Lịch sử của 1 node."""
        return [e for e in self.events if e.payload.get("name") == node_name or
                e.payload.get("source") == node_name or e.payload.get("target") == node_name]
```

---

## 4. Orchestration: Airflow, Prefect, Loop

### 4.1 So Sánh Orchestrators

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────────┐
│ Tool            │ Best For         │ Schedule         │ Graph Integration    │
├─────────────────┼──────────────────┼──────────────────┼──────────────────────┤
│ Airflow         │ Large DAGs, ETL  │ Cron, event      │ PythonOperator + Neo4j│
│ Prefect         │ Modern, Pythonic │ Cron, interval   │ @flow + @task        │
│ Loop (framework)│ Agent loops      │ Schedule + triage│ Automations + worktree│
│ GitHub Actions  │ CI/CD + KG sync  │ Push, schedule   │ Workflow YAML        │
│ Cron (simple)   │ Small, local     │ Cron             │ Shell script         │
└─────────────────┴──────────────────┴──────────────────┴──────────────────────┘
```

### 4.2 Prefect Example

<details>
<summary>Python Code — Prefect Graph Workflow (Click để xem)</summary>

```python
# pip install prefect

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

@task(retries=3, retry_delay_seconds=10)
def extract_task(documents: list) -> dict:
    print(f"Extracting from {len(documents)} docs...")
    # entities = extract_entities_batch(documents)
    return {"entities": [], "relations": []}

@task
def dedup_task(data: dict) -> dict:
    print("Deduplicating...")
    # canonical, mapping = deduplicate_entities(data["entities"])
    return data

@task
def validate_task(data: dict) -> dict:
    print("Validating against ontology...")
    return data

@task
def load_task(data: dict) -> dict:
    print(f"Loading {len(data['entities'])} entities to Neo4j...")
    return {"loaded": len(data["entities"])}

@flow(name="graph-etl", task_runner=ConcurrentTaskRunner())
def graph_etl_flow(documents: list):
    extracted = extract_task(documents)
    deduped = dedup_task(extracted)
    validated = validate_task(deduped)
    result = load_task(validated)
    return result

# Chạy
# graph_etl_flow(["Doc 1", "Doc 2", "Doc 3"])

# Schedule: chạy mỗi giờ
# from prefect.deployments import Deployment
# Deployment.build_from_flow(
#     flow=graph_etl_flow,
#     name="hourly-graph-etl",
#     schedule={"cron": "0 * * * *"},
# )
```

</details>

### 4.3 Tích Hợp Với Loop Engineering

Loop có thể tự động trigger graph updates:

```
Loop: Daily Triage
  Schedule: mỗi ngày 9:00
  Triage: phát hiện documents mới trong /data/raw_docs/
  Action:
    1. So sánh file list với STATE.md (đã ingest chưa)
    2. Với mỗi file mới → gọi IncrementalUpdater.add_document()
    3. Chạy community detection lại nếu >100 nodes mới
    4. Cập nhật STATE.md + graph audit log
    5. Nếu lỗi → escalate to human (loop/03-safety pattern)
```

---

## 5. Observability & Error Recovery

> **📌 Khái Niệm Cơ Bản:**
> **Observability = "nhìn được vào bên trong pipeline"** — bạn cần biết: mỗi lần chạy ETL:
> - Mất bao lâu (mỗi stage)?
> - Vào bao nhiêu entities/relations, ra bao nhiêu (bao nhiêu bị bad)?
> - Dedup (gộp trùng) bao nhiêu phần trăm?
> - Có bao nhiêu lỗi, ở stage nào?
>
> **Error Recovery = kế hoạch "khi lỗi thì làm gì":** thử lại (retry), bỏ qua (skip), hay dừng hẳn (fail). **Không bao giờ để pipeline lỗi âm thầm mà vẫn báo "thành công"**.

### 5.1 Metrics Cho Graph Workflow

```python
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class GraphWorkflowMetrics:
    run_id: str
    stage_durations: Dict[str, float] = field(default_factory=dict)
    entities_in: int = 0
    entities_out: int = 0
    relations_in: int = 0
    relations_out: int = 0
    dedup_rate: float = 0.0  # % entities gộp
    error_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def summary(self) -> Dict:
        return {
            "run_id": self.run_id,
            "entities": f"{self.entities_in} → {self.entities_out} (dedup {self.dedup_rate:.0%})",
            "relations": f"{self.relations_in} → {self.relations_out}",
            "errors": self.error_count,
            "total_ms": sum(self.stage_durations.values()),
            "stages": self.stage_durations,
        }
```

### 5.2 Error Recovery Patterns

```python
import time
from functools import wraps

def retry_with_backoff(max_attempts=3, backoff_factor=2.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    wait = backoff_factor ** attempt
                    print(f"  Attempt {attempt} failed: {e}, retrying in {wait}s...")
                    time.sleep(wait)
        return wrapper
    return decorator

class CircuitBreaker:
    """Ngừng gọi LLM nếu lỗi liên tiếp quá nhiều."""
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.open_since = None
    
    def call(self, func, *args, **kwargs):
        if self.open_since and (time.time() - self.open_since < self.reset_timeout):
            raise RuntimeError("Circuit breaker OPEN — too many failures")
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            self.open_since = None
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.threshold:
                self.open_since = time.time()
                print(f"  Circuit breaker OPEN after {self.failures} failures")
            raise

# Usage
breaker = CircuitBreaker(failure_threshold=3)

@retry_with_backoff(max_attempts=3)
def safe_extract(text: str):
    return breaker.call(extract_entities, text)
```

---

## 6. Triển Khai Complete Workflow Engine

<details>
<summary>Python Code — Graph Workflow Orchestrator (Click để xem)</summary>

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import time
import uuid

@dataclass
class WorkflowRun:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    status: str = "pending"  # pending, running, success, failed, rolled_back
    stages: List[Dict] = field(default_factory=list)
    metrics: Optional[Dict] = None
    error: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ended_at: Optional[str] = None

class GraphWorkflowEngine:
    """
    Orchestrator cho Graph ETL + Incremental + Versioning.
    
    Features:
      - DAG-based stage execution
      - Checkpoint & rollback
      - Metrics & audit log
      - Circuit breaker
    """
    
    def __init__(self, name: str = "graph-workflow"):
        self.name = name
        self.stages: List[Dict] = []
        self.audit_log = GraphAuditLog()
        self.runs: List[WorkflowRun] = []
        self.circuit_breaker = CircuitBreaker()
    
    def add_stage(self, name: str, func: Callable, checkpoint: bool = False,
                  on_error: str = "fail", timeout_s: int = 300):
        self.stages.append({
            "name": name, "func": func, "checkpoint": checkpoint,
            "on_error": on_error, "timeout_s": timeout_s,
        })
        return self
    
    def run(self, initial_data: Any) -> WorkflowRun:
        run = WorkflowRun()
        run.status = "running"
        data = initial_data
        checkpoints: List[Dict] = []
        
        print(f"\n{'='*60}")
        print(f"  Workflow: {self.name} | Run: {run.run_id}")
        print(f"{'='*60}")
        
        for stage in self.stages:
            stage_name = stage["name"]
            print(f"\n  ▶ Stage: {stage_name} {'[checkpoint]' if stage['checkpoint'] else ''}")
            stage_start = time.time()
            
            try:
                data = stage["func"](data)
                duration = (time.time() - stage_start) * 1000
                
                entry = {"stage": stage_name, "status": "success", 
                         "duration_ms": round(duration, 2),
                         "timestamp": datetime.now().isoformat()}
                run.stages.append(entry)
                
                if stage["checkpoint"]:
                    checkpoints.append({"stage": stage_name, "data": data, "run_id": run.run_id})
                    print(f"    💾 Checkpoint saved: {stage_name}")
                
                self.audit_log.log(GraphEvent(
                    id=str(uuid.uuid4())[:8], timestamp=datetime.now(),
                    action="CREATE_EDGE", payload={"stage": stage_name},
                    actor=f"workflow:{self.name}"
                ))
                
                print(f"    ✅ {stage_name}: {duration:.0f}ms")
            
            except Exception as e:
                duration = (time.time() - stage_start) * 1000
                run.stages.append({"stage": stage_name, "status": "failed",
                                    "error": str(e), "duration_ms": round(duration, 2)})
                run.error = str(e)
                
                print(f"    ❌ {stage_name}: {e}")
                
                if stage["on_error"] == "fail":
                    # Rollback về checkpoint gần nhất
                    if checkpoints:
                        last_cp = checkpoints[-1]
                        print(f"    ↩ Rolling back to checkpoint: {last_cp['stage']}")
                        run.status = "rolled_back"
                    else:
                        run.status = "failed"
                    run.ended_at = datetime.now().isoformat()
                    self.runs.append(run)
                    return run
                elif stage["on_error"] == "skip":
                    print(f"    ⏭ Skipping {stage_name}")
                    continue
        
        run.status = "success"
        run.ended_at = datetime.now().isoformat()
        run.metrics = {"stages": len(run.stages), "checkpoints": len(checkpoints)}
        self.runs.append(run)
        
        print(f"\n  ✅ Workflow {run.run_id} completed: {len(run.stages)} stages")
        return run
    
    def get_stats(self) -> Dict:
        total = len(self.runs)
        success = sum(1 for r in self.runs if r.status == "success")
        return {
            "total_runs": total,
            "success": success,
            "failed": total - success,
            "success_rate": round(success / total, 2) if total else 0,
            "avg_stages": round(sum(len(r.stages) for r in self.runs) / total, 1) if total else 0,
        }

# Usage
engine = (GraphWorkflowEngine("enterprise-kg-daily")
    .add_stage("extract", extract_stage, checkpoint=True)
    .add_stage("dedup", dedup_stage, checkpoint=True)
    .add_stage("validate", validate_stage, on_error="fail")
    .add_stage("load", load_stage, checkpoint=True))

result = engine.run(["Doc 1", "Doc 2"])
print(f"\nStats: {engine.get_stats()}")
print(f"Audit events: {len(engine.audit_log.events)}")
```

</details>

---

## 7. Labs Thực Hành

### Lab 1: ETL Pipeline Cho 100 Docs

1. Tạo 100 synthetic documents (dùng LLM generate)
2. Chạy `GraphETLPipeline` với 4 stages, đo thời gian từng stage
3. Thêm checkpoint và test rollback khi stage `validate` fail

### Lab 2: Incremental vs Rebuild Benchmark

1. Ingest 1000 docs (batch) — đo thời gian + cost
2. Thêm 10 docs mới: incremental (chỉ 10 docs) vs rebuild (1010 docs) — so sánh
3. Tính cost savings của incremental

### Lab 3: Loop Integration

1. Viết 1 GitHub Actions workflow: khi push `data/raw_docs/*.md` → trigger graph ETL
2. Hoặc: Prefect flow schedule mỗi giờ, kiểm tra `data/` có file mới không

---

## Tài Liệu Tham Khảo

- Prefect Docs — *Flows & Tasks* (https://docs.prefect.io/)
- Airflow Docs — *DAGs* (https://airflow.apache.org/docs/)
- Neo4j — *Import & ETL Tools* (https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/)
- *Data Pipelines with Apache Airflow* — Harenslak & de Ruiter (Manning)

---

*Tiếp theo: [09 — Evaluation](../09-evaluation/)*
