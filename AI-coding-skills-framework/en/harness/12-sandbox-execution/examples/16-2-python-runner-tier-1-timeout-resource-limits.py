import resource, subprocess

class SandboxError(Exception):
    """Lỗi có kiểu — planner đọc code, không đọc text (§4.3)."""

def run_sandboxed(cmd: list[str], workdir: str, *,
                  timeout_s: int = 30, cpu_s: int = 10,
                  mem_mb: int = 512, fsize_mb: int = 64) -> subprocess.CompletedProcess:
    """Tier 1 — cách ly ở tầng ngôn ngữ: deadline + resource limits.
    CHỈ cho code tin cậy nội bộ. Code không tin cậy → Tầng 2 (container)."""
    def apply_limits():                       # chạy trong process con, không đụng cha
        resource.setrlimit(resource.RLIMIT_CPU,   (cpu_s, cpu_s))        # chặn vòng lặp vô hạn
        resource.setrlimit(resource.RLIMIT_AS,    (mem_mb << 20,) * 2)   # chặn cạn RAM
        resource.setrlimit(resource.RLIMIT_FSIZE, (fsize_mb << 20,) * 2) # chặn file output khổng lồ
        resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))              # chặn fork bomb
    try:
        return subprocess.run(cmd, cwd=workdir, capture_output=True, text=True,
                              timeout=timeout_s, preexec_fn=apply_limits,
                              env={"PATH": "/usr/bin:/bin"})  # không kế thừa env (secret) của cha
    except subprocess.TimeoutExpired as e:
        raise SandboxError("deadline-exceeded") from e
