harness.addTool({ name: "write_code", execute: async (code) => {
  const lint = await linter.check(code);      // thay vì "nhờ" AI cẩn thận
  return lint.hasErrors ? { status: "error", errors: lint.errors }
                        : { status: "success", code };
}});
