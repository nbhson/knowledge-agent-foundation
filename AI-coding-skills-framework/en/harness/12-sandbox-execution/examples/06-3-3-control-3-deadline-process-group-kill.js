// A timeout that only kills the direct child is a timeout that does nothing.
const t = setTimeout(() => {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}   // negative PID = process group
  reject(new SandboxError("deadline-exceeded"));
}, policy.timeoutMs);
