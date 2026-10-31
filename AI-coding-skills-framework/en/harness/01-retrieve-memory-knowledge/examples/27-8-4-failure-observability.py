import time, hashlib, logging, re
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retrieval")

CURRENT_EMBED_VERSION = "nomic-embed-text:v2"
TOP_SCORE_FLOOR, TOP_K = 0.25, 5
PII = [(re.compile(r"[\w.-]+@[\w.-]+\.\w+"), "[REDACTED:EMAIL]"),
       (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED:SSN]"),
       (re.compile(r"sk-[A-Za-z0-9]{8,}"), "[REDACTED:KEY]")]

def scrub(text: str) -> str:
    for rx, rep in PII:
        text = rx.sub(rep, text)
    return text

def get_embedding(text: str, version: str = CURRENT_EMBED_VERSION):
    # stub: call ollama/vLLM; must return (vector, version)
    return [0.1, 0.2], version

def vector_search(q_emb, tenant_id: str, k=TOP_K): ...
def bm25_search(query: str, tenant_id: str, k=TOP_K): ...

def retrieve(query: str, tenant_id: str):
    t0 = time.time()
    q = scrub(query)
    q_emb, ver = get_embedding(q)
    assert ver == CURRENT_EMBED_VERSION, f"drift: {ver}"
    hits = [h for h in vector_search(q_emb, tenant_id) if h["tenant_id"] == tenant_id]
    top = max([h["score"] for h in hits], default=0.0)
    fallback = None
    if not hits or top < TOP_SCORE_FLOOR:
        fallback = "bm25-only-retry"
        hits = [h for h in bm25_search(q, tenant_id) if h["tenant_id"] == tenant_id]
    logger.info("retrieve tenant=%s hits=%d top=%.3f fallback=%s ms=%d ver=%s",
        hashlib.sha256(tenant_id.encode()).hexdigest()[:8],
        len(hits), top, fallback, int((time.time()-t0)*1000), ver)
    if not hits:
        return {"answer": None, "abstain": True, "reason": "no grounding found"}
    return {"hits": hits[:TOP_K], "fallback": fallback, "abstain": False}
