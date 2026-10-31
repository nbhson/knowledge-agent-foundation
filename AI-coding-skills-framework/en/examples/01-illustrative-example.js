// Integrate the linter into the harness
harness.addTool({
  name: "write_code",
  execute: async (code) => {
    // Automatically check syntax
    const lintResult = await linter.check(code);
    if (lintResult.hasErrors) {
      // Automatically reject and ask for a fix
      return { status: "error", errors: lintResult.errors };
    }
    return { status: "success", code };
  }
});
