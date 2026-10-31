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
