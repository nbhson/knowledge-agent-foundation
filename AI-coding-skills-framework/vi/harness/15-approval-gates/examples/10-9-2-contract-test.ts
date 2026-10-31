describe("Gatekeeper contract", () => {
  it("validate bằng chứng trước khi mở", () => {
    expect(() => gates.request({ ...noDryRun })).toThrow(/missing evidence/);
  });

  it("settle đúng một lần", async () => {
    const g = gates.request(validGate);
    gates.settle(g.key, "approved", "alice");
    gates.settle(g.key, "denied", "alice");                  // lời gọi thứ hai là no-op
    expect(gates.verdict(g.key)).toBe("approved");
  });

  it("sống sót qua restart và nạp lại expiry", async () => {
    const g = gates.request(validGate);
    const fresh = new Gatekeeper(store, risk);               // nạp lại gate đang mở
    expect(fresh.verdict(g.key)).toBeUndefined();
    await vi.advanceTimersByTimeAsync(g.expiresAt - Date.now() + 1);
    expect(fresh.verdict(g.key)).toBe("expired");            // fail closed
  });

  it("từ chối tự duyệt trên prod-auth", () => {
    const g = gates.request(validGateProdAuth);
    expect(gates.settle(g.key, "approved", g.actorId)).toBe(false);
  });

  it("phục hồi run sau approve và replan sau deny", async () => {
    const approved = gates.request(gate1); gates.settle(approved.key, "approved", "bob");
    const denied   = gates.request(gate2); gates.settle(denied.key, "denied", "bob", "not today");
    expect(resume(runId, approved.key)).toExecExactlyOnce(stepAtKey(approved.key));
    expect(plan.exclude).toHaveBeenCalledWith(denied.taskId);   // deny → replan, không retry
  });
});
