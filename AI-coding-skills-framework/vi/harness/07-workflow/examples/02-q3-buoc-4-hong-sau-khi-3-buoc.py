@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable   # hàm hoàn tác, chạy khi bước sau hỏng
    max_retries: int = 3
