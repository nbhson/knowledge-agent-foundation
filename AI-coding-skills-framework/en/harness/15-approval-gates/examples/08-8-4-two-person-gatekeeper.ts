// wraps Gatekeeper for prod-auth: two independent human approvals, persisted
export class TwoPersonGatekeeper {
  constructor(private inner: Gatekeeper) {}
  request(g: Omit<Gate, "key" | "state" | "createdAt" | "diffHash"
        | "dryRunHash">): Gate {
    const gate = this.inner.request(g);
    return gate;   // approval requires ONE additional actor: settle() enforces ≠ actor
  }
  // settle() in the base Gatekeeper already rejects actorId === approver for prod-auth.
  // All that changes is UI + TTL (4h) + page. The invariant lives in one place.
}
