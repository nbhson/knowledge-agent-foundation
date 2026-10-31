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
