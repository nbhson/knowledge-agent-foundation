interface BuiltContext {
  system: string;        // identity, rules (không bao giờ cắt)
  goal: string;          // task hiện tại + definition of done
  retrieved: Chunk[];    // từ 01, kèm score
  history: string;       // summary đã nén, không phải raw log
  immediate: FileSnap[]; // files đang mở, diffs
  budget: { limit: number; used: number };
}
