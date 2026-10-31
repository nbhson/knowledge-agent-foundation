private reloadOpen(): void {
  for (const ev of this.store.query({ kind: "approval_request" }))
    if (!this.verdict(ev.payload.key)) {
      this.gates.set(ev.payload.key, ev.payload);
      this.armTimer(ev.payload);            // nạp lại đồng hồ hết hạn
    }
}
