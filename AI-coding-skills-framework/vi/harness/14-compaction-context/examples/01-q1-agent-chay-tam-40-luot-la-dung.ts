export const COMPACT_AT = 0.70, MAX_TURNS = 20;
export function shouldCompact(used: number, budget: number, turns: number): boolean {
  return used / budget > COMPACT_AT || turns > MAX_TURNS;
}
