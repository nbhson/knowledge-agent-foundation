const recency = Math.exp(-(now - s.turn) / 12);
const reachable = serves.some(t => plan.pendingIds.includes(t)) ? 1.0 : 0.1;
return 0.30 * recency + 0.40 * reachable + 0.30 * failure;
