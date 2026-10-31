metrics.record(query_type="factual", latency_ms=250, tokens=8500,
               relevance=[0.95, 0.88, 0.72], cache_hit=False,
               compression_ratio=0.4)
print(metrics.report())   # avg + P95 latency, avg/max tokens,
                         # avg relevance, hit_rate, query distribution
