const editTool = { execute: async (file, changes) => {
  const next = applyChanges(file, changes);
  const lint = await linter.check(next);       // kiểm tra ngay
  if (lint.errors.length) return { success: false, errors: lint.errors };
  await saveFile(file, next); return { success: true };
}};
