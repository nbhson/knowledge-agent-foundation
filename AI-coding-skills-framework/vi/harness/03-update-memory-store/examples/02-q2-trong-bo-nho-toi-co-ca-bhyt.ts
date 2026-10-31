g.sort((a, b) => b.trust - a.trust || b.ts - a.ts);  // highest-trust-wins
this.facts = this.facts.filter(x => !g.slice(1).includes(x));
conflicts.push(g);   // cả hai bản vẫn còn, chỉ ghi cạnh supersedes
