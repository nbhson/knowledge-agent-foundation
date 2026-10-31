type Fact = { tenant: string; subj: string; pred: string; obj: string; trust: number; ts: number; ttl?: number };

export class MemoryStore {
  private facts: Fact[] = []; private wal: Fact[] = [];
  async write(f: Fact, idemKey: string): Promise<"ok" | "dup"> {
    if (this.wal.some(w => (w as any).idemKey === idemKey)) return "dup";
    if (Date.now() > (f.ttl ?? Infinity)) throw new Error("expired");
    (f as any).idemKey = idemKey;
    this.wal.push(f); // fsync trong production
    const dup = this.facts.find(e => e.tenant === f.tenant && sim(e, f) >= 0.9);
    if (dup) { Object.assign(dup, { obj: f.obj, trust: Math.max(dup.trust, f.trust) }); }
    else this.facts.push(f);
    return "ok"; // ack sau WAL+primary
  }
  consolidate(): { merged: number; conflicts: Fact[][] } {
    const conflicts: Fact[][] = [];
    const byKey = new Map<string, Fact[]>();
    for (const f of this.facts.filter(f => (f.ttl ?? Infinity) > Date.now())) {
      const k = `${f.tenant}|${f.subj}|${f.pred}`;
      byKey.set(k, [...(byKey.get(k) ?? []), f]);
    }
    let merged = 0;
    for (const [, g] of byKey) {
      const objs = new Set(g.map(x => x.obj));
      if (objs.size > 1) {
        g.sort((a, b) => b.trust - a.trust || b.ts - a.ts); // highest-trust-wins
        this.facts = this.facts.filter(x => !g.slice(1).includes(x)); merged += g.length - 1;
        conflicts.push(g);
      }
    }
    return { merged, conflicts };
  }
  gdprDelete(tenant: string): { receipt: string } {
    this.facts = this.facts.filter(f => f.tenant !== tenant);
    this.wal = this.wal.filter(f => f.tenant !== tenant);
    return { receipt: `del:${tenant}:${Date.now()}` };
  }
}
declare function sim(a: Fact, b: Fact): number;
