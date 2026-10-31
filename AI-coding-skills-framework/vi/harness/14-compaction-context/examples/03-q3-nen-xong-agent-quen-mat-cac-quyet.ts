const o = compact(spans, budget, goal, pins, plan, loop);
await memory.persist(o.writeBack.facts, { fsync: true });   // bền TRƯỚC khi loại
await traj.append({ kind: "compaction", payload: {
  keptIds: o.kept.map(s => s.id), evictedIds: o.dropped, ratio: o.ratio } });
return o;
