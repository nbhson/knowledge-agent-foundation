// Tích hợp linter vào harness
harness.addTool({
  name: "write_code",
  execute: async (code) => {
    // Tự động check syntax
    const lintResult = await linter.check(code);
    if (lintResult.hasErrors) {
      // Tự động reject và yêu cầu sửa
      return { status: "error", errors: lintResult.errors };
    }
    return { status: "success", code };
  }
});
