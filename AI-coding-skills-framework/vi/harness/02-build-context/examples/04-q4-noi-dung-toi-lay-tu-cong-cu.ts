const r = await withTimeout(fetchSource("docs", query), 2500, { source: "docs", docs: [] });
merged.push(`<untrusted source="${r.source}">${d.slice(0, 2000)}</untrusted>`);
return { merged, partial };  // partial = ["docs"]
