// wrap Gatekeeper cho prod-auth: hai human approve độc lập, persist
export class TwoPersonGatekeeper {
  constructor(private inner: Gatekeeper) {}
  request(g: Omit<Gate, "key" | "state" | "createdAt" | "diffHash"
        | "dryRunHash">): Gate {
    const gate = this.inner.request(g);
    return gate;   // approval yêu cầu MỘT actor khác: settle() enforce ≠ actor
  }
  // settle() trong Gatekeeper cơ sở đã từ chối actorId === approver cho prod-auth.
  // Tất cả thay đổi nằm ở UI + TTL (4h) + page. Invariant ở một chỗ duy nhất.
}
