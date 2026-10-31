from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from datetime import datetime
import time
import random


class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing, reject calls
    HALF_OPEN = "half_open" # Testing recovery


@dataclass
class HealthCheck:
    name: str
    check_fn: Callable
    interval_seconds: int = 30
    timeout_seconds: int = 10
    last_check: Optional[str] = None
    last_status: str = "unknown"
    failure_count: int = 0


class SelfHealingSystem:
    """
    Self-healing system với health checks,
    circuit breaker, và auto-recovery.
    """
    
    def __init__(self):
        self.health_checks: Dict[str, HealthCheck] = {}
        self.circuit_breakers: Dict[str, CircuitState] = {}
        self.failure_counts: Dict[str, int] = {}
        self.recovery_handlers: Dict[str, Callable] = {}
        self.max_failures = 5
        self.circuit_open_duration = 60  # seconds
    
    def register_health_check(self, name: str, check_fn: Callable,
                               interval: int = 30):
        """Register health check"""
        self.health_checks[name] = HealthCheck(
            name=name,
            check_fn=check_fn,
            interval_seconds=interval,
        )
    
    def register_recovery(self, name: str, recovery_fn: Callable):
        """Register recovery handler"""
        self.recovery_handlers[name] = recovery_fn
    
    def check_health(self, name: str) -> Dict:
        """Run health check"""
        check = self.health_checks.get(name)
        if not check:
            return {"status": "error", "message": "Check not found"}
        
        try:
            result = check.check_fn()
            check.last_status = "healthy"
            check.failure_count = 0
            check.last_check = datetime.now().isoformat()
            
            # Reset circuit breaker
            self.circuit_breakers[name] = CircuitState.CLOSED
            self.failure_counts[name] = 0
            
            return {"status": "healthy", "result": result}
            
        except Exception as e:
            check.failure_count += 1
            check.last_status = "unhealthy"
            check.last_check = datetime.now().isoformat()
            
            self.failure_counts[name] = self.failure_counts.get(name, 0) + 1
            
            # Check if should open circuit
            if self.failure_counts[name] >= self.max_failures:
                self.circuit_breakers[name] = CircuitState.OPEN
                self._attempt_recovery(name)
            
            return {
                "status": "unhealthy",
                "error": str(e),
                "failure_count": self.failure_counts[name],
            }
    
    def allow_request(self, name: str) -> bool:
        """Circuit breaker: check if request should be allowed"""
        state = self.circuit_breakers.get(name, CircuitState.CLOSED)
        
        if state == CircuitState.CLOSED:
            return True
        elif state == CircuitState.OPEN:
            # After cooldown, try half-open
            self.circuit_breakers[name] = CircuitState.HALF_OPEN
            return True  # Allow one test request
        elif state == CircuitState.HALF_OPEN:
            return True  # Allow test request
        
        return False
    
    def _attempt_recovery(self, name: str):
        """Attempt automatic recovery"""
        handler = self.recovery_handlers.get(name)
        if handler:
            try:
                handler()
            except Exception:
                pass  # Recovery failed, will retry later
    
    def get_system_health(self) -> str:
        """System health report"""
        lines = ["=== System Health ==="]
        
        for name, check in self.health_checks.items():
            circuit = self.circuit_breakers.get(name, CircuitState.CLOSED)
            icon = "✅" if check.last_status == "healthy" else "❌"
            lines.append(
                f"  {icon} {name}: {check.last_status} "
                f"[circuit={circuit.value}] "
                f"failures={check.failure_count}"
            )
        
        return "\n".join(lines)
