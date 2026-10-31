// Timeout chỉ kill con trực tiếp là timeout không làm gì cả.
const t = setTimeout(() => {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}   // PID âm = process group
  reject(new SandboxError("deadline-exceeded"));
}, policy.timeoutMs);
