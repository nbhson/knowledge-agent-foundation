type SourceResult = { source: string; docs: string[] };

async function withTimeout<T>(p: Promise<T>, ms: number, fallback: T): Promise<T> {
  return Promise.race([p, new Promise<T>(r => setTimeout(() => r(fallback), ms))]);
}

export async function fanOut(query: string): Promise<{ merged: string[]; partial: string[] }> {
  const tasks: Record<string, Promise<SourceResult>> = {
    vector: fetchSource("vector", query), code: fetchSource("code", query), docs: fetchSource("docs", query),
  };
  const entries = await Promise.all(Object.entries(tasks).map(async ([k, p]) => {
    const r = await withTimeout(p, 2500, { source: k, docs: [] });
    return [k, r] as const;
  }));
  const partial = entries.filter(([, r]) => r.docs.length === 0).map(([k]) => k);
  const seen = new Set<string>(); const merged: string[] = [];
  for (const [, r] of entries) for (const d of r.docs.slice(0, 5)) {
    const h = hash(d); if (!seen.has(h)) { seen.add(h); merged.push(`<untrusted source="${r.source}">${d.slice(0, 2000)}</untrusted>`); }
  }
  return { merged, partial };
}
declare function fetchSource(s: string, q: string): Promise<SourceResult>;
declare function hash(s: string): string;
