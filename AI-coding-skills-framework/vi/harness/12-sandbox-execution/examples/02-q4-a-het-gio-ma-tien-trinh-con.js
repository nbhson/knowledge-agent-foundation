// Tách tiến trình thành nhóm, giết cả nhóm bằng SIGKILL
const t = setTimeout(() => {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}
  reject(new SandboxError("deadline-exceeded"));
}, policy.timeoutMs);
