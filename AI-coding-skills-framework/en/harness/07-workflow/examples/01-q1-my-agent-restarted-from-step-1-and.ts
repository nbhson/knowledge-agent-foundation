const key = `${runId}:${s.id}:${JSON.stringify(inputs).length}:${s.id}`;
const cached = s.idem !== false ? (idemStore.get(key) ?? this.done(key)) : undefined;
if (cached !== undefined) { inputs = cached; continue; }  // already done → skip
const out = await gate(() => s.run({ idemKey: key }));
idemStore.set(key, out);
this.ckpt({ runId, key, status: "ok", at: Date.now() });
