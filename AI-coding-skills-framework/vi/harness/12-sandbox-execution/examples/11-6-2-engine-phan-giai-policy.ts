export function resolvePolicy(role: AgentRole, task: TaskNode, base: SandboxPolicy): SandboxPolicy {
  const tier = maxTier(task.risk, riskOfTool(task.tools));
  return {
    ...base,
    allowWrite: tier === "read" ? [] : [task.worktree],
    allowNet:   netForRole(role),
    timeoutMs:  timeoutFor(tier),       // read 10s, write 30s, elevated 120s
    memory:     tier === "elevated" ? "1g" : "512m",
    cpus:       tier === "elevated" ? "2.0" : "1.0",
    env:        envForRole(role),        // chỉ phần manifest khai báo
    tier,
  };
}
