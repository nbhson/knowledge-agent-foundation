from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
from enum import Enum
import statistics


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"


@dataclass
class AlertRule:
    """Rule cho alerting"""
    name: str
    metric_name: str
    condition: str      # "gt", "lt", "eq"
    threshold: float
    severity: AlertSeverity
    message_template: str
    cooldown_seconds: int = 300
    last_triggered: Optional[str] = None


@dataclass
class MetricPoint:
    name: str
    value: float
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)


class MonitoringSystem:
    """
    Lightweight monitoring system cho AI coding pipelines.
    Tracks metrics, detects anomalies, và fires alerts.
    """
    
    def __init__(self):
        self.metrics: List[MetricPoint] = []
        self.alert_rules: List[AlertRule] = []
        self.alert_handlers: List[Callable] = []
    
    def record_metric(self, name: str, value: float,
                      tags: Dict[str, str] = None):
        """Ghi metric point"""
        self.metrics.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now().isoformat(),
            tags=tags or {},
        ))
        
        # Check alert rules
        self._check_alerts(name, value)
    
    def add_alert_rule(self, rule: AlertRule):
        """Thêm alert rule"""
        self.alert_rules.append(rule)
    
    def on_alert(self, handler: Callable):
        """Register alert handler"""
        self.alert_handlers.append(handler)
    
    def get_metric_stats(self, metric_name: str,
                         window_minutes: int = 60) -> Dict:
        """Tính statistics cho metric trong time window"""
        cutoff = datetime.now()
        relevant = [
            m for m in self.metrics
            if m.name == metric_name
        ]
        
        if not relevant:
            return {"error": "No data"}
        
        values = [m.value for m in relevant]
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0,
            "p95": sorted(values)[int(len(values) * 0.95)] if len(values) >= 20 else max(values),
        }
    
    def _check_alerts(self, metric_name: str, value: float):
        """Kiểm tra alert rules"""
        for rule in self.alert_rules:
            if rule.metric_name != metric_name:
                continue
            
            triggered = False
            if rule.condition == "gt" and value > rule.threshold:
                triggered = True
            elif rule.condition == "lt" and value < rule.threshold:
                triggered = True
            elif rule.condition == "eq" and value == rule.threshold:
                triggered = True
            
            if triggered:
                alert = {
                    "rule": rule.name,
                    "severity": rule.severity.value,
                    "metric": metric_name,
                    "value": value,
                    "threshold": rule.threshold,
                    "message": rule.message_template.format(
                        value=value, threshold=rule.threshold
                    ),
                    "timestamp": datetime.now().isoformat(),
                }
                
                for handler in self.alert_handlers:
                    handler(alert)
    
    def generate_dashboard(self) -> str:
        """Tạo text dashboard"""
        metric_names = set(m.name for m in self.metrics)
        
        lines = [
            "=" * 60,
            "  MONITORING DASHBOARD",
            "=" * 60,
            "",
        ]
        
        for name in sorted(metric_names):
            stats = self.get_metric_stats(name)
            lines.append(f"  📊 {name}")
            lines.append(f"     Count: {stats.get('count', 0)}")
            lines.append(f"     Mean:  {stats.get('mean', 0):.2f}")
            lines.append(f"     Min:   {stats.get('min', 0):.2f}")
            lines.append(f"     Max:   {stats.get('max', 0):.2f}")
            lines.append("")
        
        return "\n".join(lines)
