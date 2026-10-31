import { TrajectoryEventSchema } from "./schema";

export function validateEmitter(name: string, evts: unknown[]): void {
  for (const e of evts) {
    const r = TrajectoryEventSchema.safeParse(e);
    if (!r.success) throw new Error(`${name} emitted invalid event: ${r.error.message}`);
  }
  const seqs = evts.map((e: any) => e.seq).sort((a: number, b: number) => a - b);
  seqs.forEach((s, i) => { if (s !== i) throw new Error(`${name} produced a seq gap at ${i}`); });
}
