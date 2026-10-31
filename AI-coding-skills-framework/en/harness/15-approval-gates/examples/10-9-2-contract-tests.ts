describe("Gatekeeper contract", () => {
  it("validates evidence before opening", () => {
    expect(() => gates.request({ ...noDryRun })).toThrow(/missing evidence/);
  });

  it("settles exactly once", async () => {
    const g = gates.request(validGate);
    gates.settle(g.key, "approved", "alice");
    gates.settle(g.key, "denied", "alice");                  // second call is a no-op
    expect(gates.verdict(g.key)).toBe("approved");
  });

  it("survives restart and re-arms expiry", async () => {
    const g = gates.request(validGate);
    const fresh = new Gatekeeper(store, risk);               // reloads open gates
    expect(fresh.verdict(g.key)).toBeUndefined();
    await vi.advanceTimersByTimeAsync(g.expiresAt - Date.now() + 1);
    expect(fresh.verdict(g.key)).toBe("expired");            // fail closed
  });

  it("rejects self-approval on prod-auth", () => {
    const g = gates.request(validGateProdAuth);
    expect(gates.settle(g.key, "approved", g.actorId)).toBe(false);
  });

  it("recovers a run after approve and replans after deny", async () => {
    const approved = gates.request(gate1); gates.settle(approved.key, "approved", "bob");
    const denied   = gates.request(gate2); gates.settle(denied.key, "denied", "bob", "not today");
    expect(resume(runId, approved.key)).toExecExactlyOnce(stepAtKey(approved.key));
    expect(plan.exclude).toHaveBeenCalledWith(denied.taskId);   // deny → replan, not retry
  });
});
