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
