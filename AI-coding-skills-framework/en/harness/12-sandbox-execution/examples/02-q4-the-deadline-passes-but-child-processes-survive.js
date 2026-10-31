// Put the child in its own process group, kill the whole group with SIGKILL
const t = setTimeout(() => {
  try { process.kill(-child.pid, "SIGKILL"); } catch {}
  reject(new SandboxError("deadline-exceeded"));
}, policy.timeoutMs);
