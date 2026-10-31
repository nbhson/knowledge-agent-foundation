class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """
    Circuit Breaker — avoids calling a service that keeps failing.
    
    CLOSED → OPEN (when enough failures) → HALF_OPEN (after recovery timeout) → CLOSED/OPEN
    """
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0,
                 half_open_max_calls: int = 1):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.half_open_calls = 0
        self.history: List[Dict] = []
    
    def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                self._log_transition("OPEN", "HALF_OPEN")
            else:
                raise CircuitOpenError(
                    f"Circuit is OPEN. Retry after {self._time_until_half_open():.0f}s"
                )
        
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise CircuitOpenError("Half-open limit reached")
            self.half_open_calls += 1
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= 2:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self._log_transition("HALF_OPEN", "CLOSED")
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                self._log_transition("HALF_OPEN", "OPEN")
            elif self.state == CircuitState.CLOSED:
                self.state = CircuitState.OPEN
                self._log_transition("CLOSED", "OPEN")
    
    def _time_until_half_open(self) -> float:
        return max(0, self.recovery_timeout - (time.time() - self.last_failure_time))
    
    def _log_transition(self, from_state: str, to_state: str):
        self.history.append({
            "from": from_state,
            "to": to_state,
            "failure_count": self.failure_count,
            "timestamp": datetime.now().isoformat(),
        })
    
    def get_state(self) -> Dict:
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "time_until_half_open": self._time_until_half_open() if self.state == CircuitState.OPEN else 0,
        }


class CircuitOpenError(Exception):
    pass
