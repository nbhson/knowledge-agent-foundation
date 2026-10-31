from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class ScheduleType(Enum):
    ONCE = "once"
    INTERVAL = "interval"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class ScheduledTask:
    name: str
    handler: Callable
    schedule_type: ScheduleType
    interval_seconds: int = 3600
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    run_count: int = 0
    failure_count: int = 0


class TaskScheduler:
    """
    Lightweight task scheduler cho automation.
    Supports interval, daily, weekly scheduling.
    """
    
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.execution_log: List[Dict] = []
    
    def schedule(self, name: str, handler: Callable,
                 schedule_type: ScheduleType,
                 interval_seconds: int = 3600) -> ScheduledTask:
        """Schedule a task"""
        task = ScheduledTask(
            name=name,
            handler=handler,
            schedule_type=schedule_type,
            interval_seconds=interval_seconds,
            next_run=datetime.now().isoformat(),
        )
        self.tasks[name] = task
        return task
    
    def run_pending(self) -> List[Dict]:
        """Run all tasks that are due"""
        now = datetime.now()
        results = []
        
        for name, task in self.tasks.items():
            if not task.enabled:
                continue
            if not task.next_run:
                continue
            
            next_run = datetime.fromisoformat(task.next_run)
            if now < next_run:
                continue
            
            # Execute
            start = time.time()
            try:
                task.handler()
                duration = time.time() - start
                
                task.last_run = now.isoformat()
                task.next_run = self._calculate_next(task, now).isoformat()
                task.run_count += 1
                
                results.append({
                    "task": name,
                    "status": "success",
                    "duration": duration,
                })
                
            except Exception as e:
                task.failure_count += 1
                task.last_run = now.isoformat()
                task.next_run = self._calculate_next(task, now).isoformat()
                
                results.append({
                    "task": name,
                    "status": "failed",
                    "error": str(e),
                })
        
        self.execution_log.extend(results)
        return results
    
    def _calculate_next(self, task: ScheduledTask, 
                       now: datetime) -> datetime:
        """Calculate next run time"""
        if task.schedule_type == ScheduleType.INTERVAL:
            return now + timedelta(seconds=task.interval_seconds)
        elif task.schedule_type == ScheduleType.DAILY:
            return now + timedelta(days=1)
        elif task.schedule_type == ScheduleType.WEEKLY:
            return now + timedelta(weeks=1)
        else:
            return now + timedelta(days=365)  # Effectively never
    
    def get_schedule_report(self) -> str:
        """Báo cáo lịch trình"""
        lines = ["=== Scheduled Tasks ==="]
        for name, task in self.tasks.items():
            status = "✅" if task.enabled else "⏸️"
            lines.append(
                f"  {status} {name} [{task.schedule_type.value}] "
                f"runs={task.run_count} "
                f"failures={task.failure_count} "
                f"next={task.next_run}"
            )
        return "\n".join(lines)
