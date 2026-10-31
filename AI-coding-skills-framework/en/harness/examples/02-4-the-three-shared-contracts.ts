interface BuiltContext {
  system: string;        // identity, rules (never truncated)
  goal: string;          // current task + definition of done
  retrieved: Chunk[];    // from 01, with scores
  history: string;       // compressed summary, not raw log
  immediate: FileSnap[]; // open files, diffs
  budget: { limit: number; used: number };
}
