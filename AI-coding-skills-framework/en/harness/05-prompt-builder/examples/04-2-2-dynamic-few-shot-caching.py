class FewShotCache:
    """
    Cache frequently-used few-shot selections to reduce latency
    
    Strategy: Hash(query + k + strategy) → cached examples
    TTL-based expiration for freshness
    """
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def _make_key(self, query: str, k: int, strategy: str) -> str:
        import hashlib
        content = f"{query}:{k}:{strategy}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, query: str, k: int, strategy: str) -> Optional[List[Dict]]:
        key = self._make_key(query, k, strategy)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check TTL
            if (datetime.now() - entry["timestamp"]).seconds < self.ttl:
                return entry["examples"]
            else:
                del self.cache[key]
        
        return None
    
    def set(self, query: str, k: int, strategy: str, examples: List[Dict]):
        key = self._make_key(query, k, strategy)
        self.cache[key] = {
            "examples": examples,
            "timestamp": datetime.now(),
        }
    
    def clear(self):
        self.cache.clear()
    
    def size(self) -> int:
        return len(self.cache)
