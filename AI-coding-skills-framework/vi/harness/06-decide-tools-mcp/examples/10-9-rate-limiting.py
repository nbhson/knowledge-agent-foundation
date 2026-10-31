class RateLimiter:
    """
    Rate limiting for tool calls
    
    Strategies:
    - Fixed window: X calls per minute
    - Sliding window: X calls in last 60 seconds
    - Token bucket: Burst + sustained rate
    """
    
    def __init__(self, strategy: str = "sliding_window"):
        self.strategy = strategy
        self._call_records: Dict[str, List[float]] = {}
        self._burst_limits: Dict[str, int] = {}
        self._token_buckets: Dict[str, Dict] = {}
    
    def set_limit(self, tool_name: str, max_calls: int, window_seconds: int = 60):
        """Set rate limit for a tool"""
        self._burst_limits[tool_name] = max_calls
    
    def check(self, tool_name: str) -> Dict:
        """Check if call is allowed"""
        now = time.time()
        
        if tool_name not in self._call_records:
            self._call_records[tool_name] = []
        
        records = self._call_records[tool_name]
        limit = self._burst_limits.get(tool_name, 60)
        window = 60  # 1 minute
        
        if self.strategy == "sliding_window":
            # Remove old records
            records = [t for t in records if now - t < window]
            self._call_records[tool_name] = records
            
            if len(records) >= limit:
                oldest = records[0]
                retry_after = window - (now - oldest)
                return {
                    "allowed": False,
                    "retry_after": round(retry_after, 1),
                    "current_rate": len(records),
                    "limit": limit,
                }
            
            records.append(now)
            return {
                "allowed": True,
                "current_rate": len(records),
                "limit": limit,
                "remaining": limit - len(records),
            }
        
        return {"allowed": True}
    
    def get_usage(self) -> Dict:
        """Get current usage for all tools"""
        usage = {}
        for tool_name, records in self._call_records.items():
            now = time.time()
            recent = [t for t in records if now - t < 60]
            usage[tool_name] = {
                "calls_last_minute": len(recent),
                "limit": self._burst_limits.get(tool_name, 60),
            }
        return usage
